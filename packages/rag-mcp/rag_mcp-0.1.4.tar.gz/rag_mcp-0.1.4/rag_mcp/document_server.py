from mcp.server.fastmcp import FastMCP
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import torch

def get_device():
    """Determine the best available device for PyTorch operations"""
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    return "cpu"

# Load environment variables
load_dotenv()

# Create an MCP server
mcp = FastMCP("DocumentProcessor")

# Global variables
vectorstore = None
embedding_model = None

def initialize_vectorstore():
    """Initialize or load the vector database from disk"""
    global vectorstore, embedding_model
    
    # Get the persist directory from environment variable and raise error if not found
    persist_directory = os.environ.get("PERSIST_DIRECTORY")
    if persist_directory is None:
        raise ValueError("PERSIST_DIRECTORY environment variable must be set")
    
    # Create a chromadb subfolder under PERSIST_DIRECTORY
    chroma_directory = os.path.join(persist_directory, "chromadb")
    
    # Create the directory if it doesn't exist
    os.makedirs(chroma_directory, exist_ok=True)
    
    # Check if Ollama embeddings should be used
    use_ollama = os.environ.get("USE_OLLAMA_EMBEDDING", "False").lower() == "true"
    
    if use_ollama:
        # Use Ollama embeddings
        ollama_model_name = os.environ.get("OLLAMA_EMBEDDING_MODEL", "bge-m3:latest")
        print(f"Using Ollama embeddings with model: {ollama_model_name}")
        embedding_model = OllamaEmbeddings(model=ollama_model_name)
    else:
        # Use HuggingFace BGE embeddings (default)
        model_name="BAAI/bge-m3"
        model_kwargs = {"device": get_device()}
        encode_kwargs = {"normalize_embeddings": True}
        print(f"Using HuggingFace BGE embeddings with model: {model_name} on device: {model_kwargs['device']}")
        embedding_model = HuggingFaceBgeEmbeddings(
            model_name=model_name, query_instruction="", model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
        )
    
    # Create or load vectorstore, using the chromadb directory
    vectorstore = Chroma(persist_directory=chroma_directory, embedding_function=embedding_model)
    
    return vectorstore

@mcp.tool()
def index_document(file_path: str) -> Dict[str, Any]:
    """
    Index a document or folder of documents to make it searchable.

    Supports these formats: PDF, DOCX, XLSX, PPTX, Markdown, AsciiDoc, HTML, XHTML, CSV
    
    Args:
        file_path: Path to the file or directory to index
        
    Returns:
        A dictionary with information about the indexing operation
    """
    global vectorstore
    
    # Ensure the file or directory exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File or directory not found: {file_path}")
    
    # Initialize vectorstore if not already done
    if vectorstore is None:
        initialize_vectorstore()
        
    all_docs = []
    file_count = 0
    
    # Handle single file or directory
    if os.path.isdir(file_path):
        # Process all files in directory
        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path):
                try:
                    docs = process_file(full_path)
                    if docs:
                        all_docs.extend(docs)
                        file_count += 1
                except Exception as e:
                    print(f"Error processing {full_path}: {e}")
    else:
        # Process single file
        docs = process_file(file_path)
        if docs:
            all_docs.extend(docs)
            file_count = 1
    
    # Add documents to existing vectorstore
    if all_docs:
        vectorstore.add_documents(documents=all_docs)
        # Remove persist() call as it's not supported in current Chroma version
        
    return {
        "status": "success",
        "indexed_path": file_path,
        "files_processed": file_count,
        "chunks_created": len(all_docs),
        "documents_loaded": True
    }

def process_file(file_path: str) -> List:
    """Helper function to process a single file"""
    # Extract just the filename without the path
    filename = os.path.basename(file_path)
    
    # Load the document
    loader = DoclingLoader(file_path=file_path, export_type=ExportType.MARKDOWN)
    docs = loader.load()
    
    if not docs:
        return []
    
    # Split the document into chunks
    md_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=2000, chunk_overlap=200
    )
    
    # Create document chunks with metadata including the source filename
    text_content = docs[0].page_content
    metadatas = [{"source": filename}]
    md_docs = md_splitter.create_documents([text_content], metadatas=metadatas)
    
    return md_docs

@mcp.tool()
def query_document(question: str) -> List[Dict[str, Any]]:
    """
    Query the indexed document with a question. 

    <IMPORTANT>
    When using this tool only use retrieved chunks directly relevant to the question. Ignore irrelevant chunks completely, even if retrieved. Do not force connections with marginally related information.
    
    Before querying, reframe the question to maximize semantic similarity matches. Include synonyms, related concepts, or more general terminology that might appear in the document. Preserve the original intent while optimizing for embedding-based retrieval.
    </IMPORTANT>
    
    Args:
        question: The question to ask about the document
        
    Returns:
        A list of relevant document chunks
    """
    global vectorstore
    
    if vectorstore is None:
        raise ValueError("No document has been indexed. Please index a document first.")
    
    # Perform similarity search with hardcoded k=4
    results = vectorstore.similarity_search(question, k=4)
    
    # Format the results
    formatted_results = []
    for i, doc in enumerate(results):
        formatted_results.append({
            "chunk_id": i + 1,
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    
    return formatted_results

def main():
    # Initialize the vectorstore first
    initialize_vectorstore()
    print(f"Vector database initialized from {os.environ.get('PERSIST_DIRECTORY')}")
    
    # Run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
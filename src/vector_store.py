from langchain_chroma import Chroma
from src.embeddings import get_embeddings

def init_vector_store(chunks):
    """Initializes and returns an ephemeral in-memory Chroma vector store."""
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings()
    )
    return vectorstore

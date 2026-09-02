from langchain_chroma import Chroma
from src.embeddings import get_embeddings
import os
import shutil

DB_DIR = "chroma_db"

def init_vector_store(chunks):
    if os.path.exists(DB_DIR):
        try:
            shutil.rmtree(DB_DIR)
        except Exception:
            pass
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=DB_DIR
    )
    return vectorstore

def get_vector_store():
    if not os.path.exists(DB_DIR):
        return None
    return Chroma(persist_directory=DB_DIR, embedding_function=get_embeddings())

from src.vector_store import get_vector_store

def retrieve_relevant_context(query: str, k: int = 5):
    vectorstore = get_vector_store()
    if not vectorstore:
        return []
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)

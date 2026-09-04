import streamlit as st

def retrieve_relevant_context(query: str, k: int = 5):
    vectorstore = st.session_state.get("vectorstore")
    if not vectorstore:
        return []
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)

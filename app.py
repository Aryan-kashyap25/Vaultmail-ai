import streamlit as st
import os
from pathlib import Path

# Initialize directories before any src imports that might depend on them
base_dir = Path(__file__).parent
data_dir = base_dir / "data"
data_dir.mkdir(exist_ok=True)

from src.vault_loader import create_demo_vault, load_vault_from_directory, load_vault_from_zip
from src.chunker import chunk_documents
from src.vector_store import init_vector_store, get_vector_store
from src.retriever import retrieve_relevant_context
from src.email_generator import generate_email_draft
from src.email_sender import send_email
from src.config import GROQ_API_KEY, DEMO_MODE

st.set_page_config(page_title="VaultMail AI", layout="wide")

def main():
    st.title("VaultMail AI")
    st.subheader("RAG-powered Email Assistant for your Obsidian Knowledge Base")

    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY is missing. Please add it to your .env file.")
        return

    # Sidebar for Knowledge Base Management
    with st.sidebar:
        st.header("Knowledge Base")
        
        kb_option = st.radio("Select Source:", ["Demo Knowledge Base", "Upload Obsidian Vault"])
        
        if kb_option == "Demo Knowledge Base":
            if st.button("Load Demo Vault"):
                with st.spinner("Creating and loading demo vault..."):
                    vault_path = create_demo_vault(str(data_dir))
                    docs = load_vault_from_directory(vault_path)
                    chunks = chunk_documents(docs)
                    init_vector_store(chunks)
                    st.success(f"Files found: {len(docs)}\nMarkdown notes: {len(docs)}")
                    st.session_state["kb_loaded"] = True
                    
        else:
            uploaded_file = st.file_uploader("Upload Obsidian Vault (.zip)", type="zip")
            if uploaded_file is not None:
                if st.button("Process Uploaded Vault"):
                    with st.spinner("Extracting and indexing..."):
                        try:
                            docs = load_vault_from_zip(uploaded_file)
                            if not docs:
                                st.warning("No Markdown files found in the uploaded vault.")
                            else:
                                chunks = chunk_documents(docs)
                                init_vector_store(chunks)
                                st.success(f"Files found: {len(docs)}\nMarkdown notes: {len(docs)}")
                                st.session_state["kb_loaded"] = True
                        except Exception as e:
                            st.error(f"Error processing vault: {str(e)}")

        st.divider()
        st.subheader("Status:")
        if st.session_state.get("kb_loaded", False):
            st.write("✓ Knowledge base loaded")
            st.write("✓ Vector store ready")
        else:
            st.write("❌ No knowledge base loaded")
            
        if DEMO_MODE:
            st.info("DEMO MODE is ON. Emails will not actually be sent.")

    # Main Area
    st.header("Create an Email")
    
    recipient = st.text_input("Recipient", value="client@example.com")
    user_request = st.text_area("What should the email say?", height=100)
    
    if st.button("Generate Email"):
        if not st.session_state.get("kb_loaded", False):
            st.warning("Please load a knowledge base first from the sidebar.")
            return
            
        if not user_request:
            st.warning("Please enter what the email should say.")
            return
            
        with st.spinner("Retrieving knowledge and drafting email..."):
            try:
                retrieved_docs = retrieve_relevant_context(user_request)
                st.session_state["retrieved_docs"] = retrieved_docs
                
                draft = generate_email_draft(user_request, retrieved_docs)
                st.session_state["draft_subject"] = draft["subject"]
                st.session_state["draft_body"] = draft["body"]
                st.session_state["show_draft"] = True
            except Exception as e:
                st.error(f"Failed to generate email: {str(e)}")
                return

    if st.session_state.get("show_draft", False):
        st.divider()
        st.header("Generated Email")
        
        edited_subject = st.text_input("Subject", value=st.session_state.get("draft_subject", ""))
        edited_body = st.text_area("Body", value=st.session_state.get("draft_body", ""), height=300)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Regenerate"):
                # Simplistic regenerate just re-triggers generation
                with st.spinner("Regenerating email..."):
                    docs = st.session_state.get("retrieved_docs", [])
                    draft = generate_email_draft(user_request, docs)
                    st.session_state["draft_subject"] = draft["subject"]
                    st.session_state["draft_body"] = draft["body"]
                    st.rerun()
                    
        with col2:
            if st.button("Send Email"):
                with st.spinner("Sending..."):
                    try:
                        result = send_email(recipient, edited_subject, edited_body)
                        st.success(result["message"])
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

        st.divider()
        st.subheader("Retrieved Sources")
        docs = st.session_state.get("retrieved_docs", [])
        if docs:
            for i, doc in enumerate(docs):
                with st.expander(f"{doc.metadata.get('filename', 'Source')} (Chunk {i+1})"):
                    st.text(doc.page_content)
        else:
            st.write("No relevant context found.")

if __name__ == "__main__":
    main()

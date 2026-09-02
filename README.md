# VaultMail AI

VaultMail AI is an AI-powered email assistant that uses your Obsidian knowledge base, Retrieval-Augmented Generation (RAG), and a Large Language Model to draft highly accurate and grounded emails. It incorporates a human-in-the-loop workflow before dispatching emails using the Resend API.

## Features

- **Obsidian Vault Integration**: Upload your Obsidian vault as a ZIP file, and the assistant will parse the Markdown notes, retaining useful metadata.
- **Demo Knowledge Base**: Immediately testable with an automatically generated demo knowledge base.
- **RAG Pipeline**: Retrieves relevant context from your notes using vector search (ChromaDB + Sentence Transformers).
- **Grounded LLM Generation**: Uses the Groq API to draft emails strictly based on the retrieved context, refusing to hallucinate information.
- **Human-in-the-Loop**: Edit the generated email subject and body before sending.
- **Email Dispatch**: Send emails via the Resend API, with a built-in "Demo Mode" for safe testing.
- **Modern UI**: Clean and intuitive Streamlit interface.

## Architecture

The system uses an agentic workflow:
1. **User Request** -> Input the desired email topic.
2. **Retrieve Knowledge** -> Embed the query and retrieve Top-K relevant chunks from ChromaDB.
3. **Generate Email** -> LLM uses prompt engineering to ground its response in the retrieved context.
4. **Human Review** -> User edits the draft in the Streamlit UI.
5. **Send Email Tool** -> Dispatches the final email via Resend API (or simulates in Demo Mode).

## Tech Stack

- **UI**: Streamlit
- **Orchestration**: LangChain
- **LLM**: Groq API
- **Embeddings**: HuggingFace/Sentence Transformers
- **Vector Database**: ChromaDB
- **Email Service**: Resend API
- **Environment Management**: python-dotenv

## Project Structure

```
vaultmail-ai/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── data/
│   └── demo_vault/         # Demo knowledge base (auto-generated)
├── src/                    # Source code
│   ├── config.py           # Configuration and environment setup
│   ├── vault_loader.py     # Parses Obsidian vaults and ZIP uploads
│   ├── chunker.py          # Splits Markdown into chunks
│   ├── embeddings.py       # Manages embedding models
│   ├── vector_store.py     # ChromaDB integration
│   ├── retriever.py        # Search and retrieval logic
│   ├── email_generator.py  # LLM generation and grounding
│   ├── email_sender.py     # Resend API integration
│   └── prompts.py          # System prompts for the LLM
└── tests/                  # Test suite
```

## Local Setup

### Windows

```bash
git clone <repository-url>
cd vaultmail-ai

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

# Edit .env to add your API keys
streamlit run app.py
```

### Linux/macOS

```bash
git clone <repository-url>
cd vaultmail-ai

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

# Edit .env to add your API keys
streamlit run app.py
```

## Environment Variables

Configure your `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=vaultmail@example.com
DEMO_MODE=true
```

## Demo Mode

When `DEMO_MODE=true` is set in your `.env` file, clicking "Send Email" will simulate the sending process and display a success message without actually calling the Resend API. This is ideal for testing the complete workflow safely.

## Uploading an Obsidian Vault

1. ZIP your Obsidian vault folder.
2. In the sidebar, select "Upload Obsidian Vault".
3. Upload the ZIP file. The application will automatically ignore non-text files and `.obsidian` configuration, extract the Markdown content, and index it into the vector database.

## Limitations

- The current embedding model runs locally and might require initial download time.
- Only `.md` files are parsed; PDFs or images within the vault are ignored.

## Future Improvements

- Add support for extracting text from PDFs and images.
- Implement more advanced chunking strategies based on Markdown headers.
- Support multiple concurrent vaults.

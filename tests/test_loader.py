from src.vault_loader import create_demo_vault

def test_create_and_load_demo_vault():
    docs = create_demo_vault()
    assert len(docs) > 0
    
    # Check if a specific file was loaded
    filenames = [doc.metadata["filename"] for doc in docs]
    assert "Company.md" in filenames

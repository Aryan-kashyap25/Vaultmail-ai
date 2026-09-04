import os
from src.vault_loader import create_demo_vault, load_vault_from_directory

def test_create_and_load_demo_vault(tmp_path):
    vault_path = create_demo_vault(str(tmp_path))
    assert os.path.exists(vault_path)
    
    docs = load_vault_from_directory(vault_path)
    assert len(docs) > 0
    
    # Check if a specific file was loaded
    filenames = [doc.metadata["filename"] for doc in docs]
    assert "Company.md" in filenames

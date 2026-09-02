import pytest
from src.email_generator import generate_email_draft
from langchain_core.documents import Document

def test_missing_api_key(monkeypatch):
    monkeypatch.setattr("src.email_generator.GROQ_API_KEY", None)
    with pytest.raises(ValueError, match="GROQ_API_KEY is missing"):
        generate_email_draft("Hello", [])
        
def test_demo_email_sender():
    from src.email_sender import send_email
    import src.email_sender as es
    es.DEMO_MODE = True
    
    res = send_email("test@example.com", "Test", "Body")
    assert res["status"] == "success"
    assert "Demo email sent" in res["message"]

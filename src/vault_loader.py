import os
import zipfile
import tempfile
from pathlib import Path
from langchain_core.documents import Document

def create_demo_vault():
    """Creates a demo Obsidian vault with fictional company data in memory."""
    files = {
        "Company.md": "# Company Overview\nAcme Corp is a leading provider of innovative software solutions. Founded in 2010, our mission is to simplify complex workflows.\n\n## Contact\nSupport: support@acmecorp.example.com",
        "Products.md": "# Products\n## Acme Cloud\nOur flagship cloud platform.\n\n## Acme Analytics\nData analytics tool.",
        "Pricing.md": "# Pricing\n## Acme Cloud\n- Basic: $10/month\n- Pro: $29/month\n- Enterprise: Custom pricing, contact sales.\n\n## Acme Analytics\n- Standard: $15/month",
        "Services.md": "# Services\nWe offer consulting and custom development. Our hourly rate is $150/hr.",
        "Project_Timeline.md": "# Standard Project Timeline\n- Phase 1 (Discovery): 2 weeks\n- Phase 2 (Development): 4-6 weeks\n- Phase 3 (Testing & Deployment): 2 weeks",
        "Client_FAQ.md": "# FAQ\n**Q: What is the SLA?**\nA: 99.9% uptime guarantee for Pro and Enterprise users.\n\n**Q: Do you offer refunds?**\nA: Yes, within 30 days of purchase.",
        "Policies.md": "# Security Policy\nWe are SOC2 compliant and encrypt all data at rest using AES-256."
    }
    
    documents = []
    for filename, content in files.items():
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": f"demo_vault/{filename}",
                    "filename": filename,
                    "relative_path": filename
                }
            )
        )
    return documents

def load_vault_from_directory(directory_path: str):
    """Loads all markdown files from a directory."""
    documents = []
    path = Path(directory_path)
    for md_file in path.rglob("*.md"):
        # Ignore .obsidian
        if ".obsidian" in md_file.parts:
            continue
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": str(md_file),
                            "filename": md_file.name,
                            "relative_path": str(md_file.relative_to(path))
                        }
                    )
                )
        except Exception:
            pass
    return documents

def load_vault_from_zip(zip_file) -> list:
    """Extracts a zip file to a temporary directory and loads markdown files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
        return load_vault_from_directory(temp_dir)

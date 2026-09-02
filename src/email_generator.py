import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.prompts import SYSTEM_PROMPT, USER_PROMPT

def generate_email_draft(user_request: str, retrieved_docs: list) -> dict:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")
        
    context = "\n\n".join([f"Source: {doc.metadata.get('filename', 'Unknown')}\n{doc.page_content}" for doc in retrieved_docs])
    
    chat = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name=GROQ_MODEL)
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT.format(request=user_request, context=context))
    ]
    
    try:
        response = chat.invoke(messages)
        content = response.content
        
        # Parse subject and body
        subject = "Draft Email"
        body = content
        
        if "Subject:" in content and "Email Body:" in content:
            parts = content.split("Email Body:", 1)
            subject_part = parts[0].replace("Subject:", "").strip()
            if subject_part:
                subject = subject_part
            body = parts[1].strip()
            
        return {"subject": subject, "body": body}
    except Exception as e:
        raise RuntimeError(f"LLM generation failed: {str(e)}")

import resend
from src.config import RESEND_API_KEY, RESEND_FROM_EMAIL, DEMO_MODE

def send_email(to_email: str, subject: str, body: str) -> dict:
    if DEMO_MODE:
        return {"status": "success", "message": "Demo email sent successfully."}
        
    if not RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY is missing. Please configure it or enable DEMO_MODE.")
        
    resend.api_key = RESEND_API_KEY
    
    try:
        params = {
            "from": RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": subject,
            "text": body
        }
        
        email = resend.Emails.send(params)
        return {"status": "success", "message": "Email sent successfully.", "id": email.get("id")}
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {str(e)}")

import os
import logging
import resend
from src.common.config.env_config import RESEND_API_KEY, RESEND_FROM_EMAIL

logger = logging.getLogger("app.email")

# Set resend api key
resend.api_key = RESEND_API_KEY

def send_verification_email(email: str, username: str, verification_url: str) -> dict:
    """Send verification email to user using Resend.
    
    Loads welcome-email-template.html, replaces template placeholders,
    and calls Resend API to deliver the mail.
    """
    try:
        # Resolve the template path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "..", "..", "templates", "welcome-email-template.html")
        
        # Read the template
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Replace placeholders
        html_content = html_content.replace("{{ username }}", username)
        html_content = html_content.replace("{{ verification_url }}", verification_url)
        
        # In development/test, if resend API key is not configured, we print a log with the link
        if not RESEND_API_KEY or RESEND_API_KEY.startswith("re_12345"):
            logger.warning(
                f"[EMAIL MOCK] Verification email to {email} ({username}) not sent via Resend: "
                "RESEND_API_KEY is not configured or is a default placeholder. "
                f"Link: {verification_url}"
            )
            print(f"\n--- [MOCK EMAIL] ---\nTo: {email}\nSubject: Verify Your Email\nVerification URL: {verification_url}\n--------------------\n")
            return {"mock": True, "verification_url": verification_url}
            
        params: resend.Emails.SendParams = {
            "from": RESEND_FROM_EMAIL,
            "to": [email],
            "subject": "Verify Your Email - Thumbnail Generator",
            "html": html_content,
        }
        
        response = resend.Emails.send(params)
        logger.info(f"Verification email successfully sent to {email}")
        return response
    except Exception as e:
        logger.error(f"Error sending email to {email}: {str(e)}")
        raise e

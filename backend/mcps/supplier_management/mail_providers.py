import smtplib
from email.message import EmailMessage
import os
from functools import lru_cache


# Initialize SMTP object and login only once

@lru_cache(maxsize=1)
def get_smtp_object():
    """
    Attempts to create an SMTP client. 
    If environment does not allow SMTP (e.g., Render), fallback safely.
    """
    email = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASSWORD")

    if not email or not password:
        print("⚠️ SMTP disabled: missing credentials.")
        return None, None

    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email, password)
        return smtp, email
    
    except Exception as e:
        print(f"⚠️ SMTP unreachable, running in NO-EMAIL mode: {e}")
        return None, None


# ❗ Do NOT crash on import.  
# Render and Docker environments often block SMTP connections.
smtp_object, sender_email = get_smtp_object()


def send_email_providers(subject: str, body: str, to_emails: list[str]) -> dict:
    """
    Sends an email to providers.
    If SMTP is unavailable, returns a friendly message instead of failing.
    """

    # CASE 1 → SMTP is disabled (Render, missing env vars, etc.)
    if smtp_object is None or sender_email is None:
        return {
            "status": "disabled",
            "message": "Email sending is disabled in this environment (SMTP unreachable).",
            "preview": {
                "subject": subject,
                "body": body,
                "recipients": to_emails
            }
        }

    # CASE 2 → SMTP available (local dev)
    try:
        for to in to_emails:
            msg = f"Subject: {subject}\n\n{body}"
            smtp_object.sendmail(sender_email, to, msg)

        return {"status": "success", "message": "Emails sent successfully."}

    except Exception as e:
        return {"status": 'error', "message": str(e)}
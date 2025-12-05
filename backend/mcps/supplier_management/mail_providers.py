import smtplib
from email.message import EmailMessage
import os
from functools import lru_cache


# Initialize SMTP object and login only once

@lru_cache(maxsize=1)
def get_smtp_object():
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()
    smtp_object.starttls()

    email = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASSWORD")

    if not email or not password:
        raise ValueError("GMAIL_USER and GMAIL_PASSWORD environment variables must be set.")

    smtp_object.login(email, password)
    return smtp_object, email

smtp_object, sender_email = get_smtp_object()


def send_email_providers(subject: str, body: str, to_emails: list[str]) -> dict:
    """
    Sends an email to a list of provider email addresses.
    """
    try:
        for to in to_emails:
            msg = f"Subject: {subject}\n\n{body}"
            smtp_object.sendmail(sender_email, to, msg)
        return {"status": "success", "message": "Emails sent successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}







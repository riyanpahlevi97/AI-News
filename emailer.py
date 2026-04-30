import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email_newsletter(content):
    """
    Sends the AI news summary via email.
    """
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_receiver = os.getenv("EMAIL_RECEIVER")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not all([email_user, email_password, email_receiver]):
        print("Error: Email credentials missing in environment variables.")
        return False

    # Create the email message
    message = MIMEMultipart()
    message["From"] = email_user
    message["To"] = email_receiver
    message["Subject"] = "Daily AI News Summary"

    # Attach the body (converting markdown to plain text or simple HTML)
    body = f"Here is your daily AI news summary:\n\n{content}"
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # Secure the connection
            server.login(email_user, email_password)
            server.send_message(message)
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import markdown
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

    # Convert Markdown to HTML
    html_content = markdown.markdown(content)
    
    # Create a nice HTML template
    html_template = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
          h1, h2, h3 {{ color: #2c3e50; }}
          a {{ color: #3498db; text-decoration: none; }}
          a:hover {{ text-decoration: underline; }}
          .source {{ color: #7f8c8d; font-size: 0.9em; }}
          .summary {{ margin-bottom: 20px; }}
        </style>
      </head>
      <body>
        {html_content}
      </body>
    </html>
    """
    message.attach(MIMEText(html_template, "html"))

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
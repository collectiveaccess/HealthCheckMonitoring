import smtplib
from email.message import EmailMessage
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, body, sender_email, receiver_email):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"), context=context
    ) as server:
        server.login(sender_email, os.environ.get("EMAIL_PASSWORD"))
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Message sent.")


def send_status_down_email(project):
    subject = f'Healthcheck {project["name"]}'
    body = f'{project["name"]} failed health check. {project["url"]}'
    send_email(
        subject, body, os.environ.get("SENDER_EMAIL"), os.environ.get("RECEIVER_EMAIL")
    )
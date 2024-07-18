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
    server = smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"))
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login( os.environ.get("SMTP_USERNAME"),  os.environ.get("SMTP_PASSWORD"))

    #for e in config['email_to']:
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# def send_email(subject, body, sender_email, receiver_email):
#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = sender_email
#     msg["To"] = receiver_email
#     msg.set_content(body)
# 
#     context = ssl.create_default_context()
# 
#     with smtplib.SMTP_SSL(
#         os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"), context=context
#     ) as server:
#         try:
#             server.login(
#                 os.environ.get("SMTP_USERNAME"), os.environ.get("SMTP_PASSWORD")
#             )
#         except Exception as error:
#             print("could not login to email server.", error)
#             return
# 
#         try:
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#         except Exception as error:
#             print(
#                 f"could not send email. sender: {sender_email}, receiver: {receiver_email}.",
#                 error,
#             )


def send_status_email(project, status, reciever_email):
    subject = f'Healthcheck {project["name"]}'
    if status == 0:
        body = f'{project["name"]} failed health check. {project["url"]}'
    else:
        body = f'{project["name"]} passed health check. {project["url"]}'
    send_email(subject, body, os.environ.get("SENDER_EMAIL"), reciever_email)

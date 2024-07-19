import smtplib
from email.message import EmailMessage
import ssl
import os
import pandas as pd
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

    # holds all emails
    email_list = set()

    # check for recipient emails in the projects csv, 
    # split them on space, 
    # add them to email list and 
    # make sure to remove duplicated

    # Read the projects.csv file
    df = pd.read_csv('data/projects.csv')

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        # Get the recipients from the 'recipients' column
        recipients = row.get('recipients', '')
        if recipients:
            # Split recipients by space 
            recipients_list = recipients.split()
            email_list.update(recipients_list)

    #for e in config['email_to']:
    # Get the RECEIVER_EMAIL environment variable
    receiver_emails = os.getenv('RECEIVER_EMAIL')

    if receiver_emails:
        # Split the emails on comma
        receiver_list = receiver_emails.split(',')
        
        email_list.update(receiver_list)
        
        # Loop through the list of emails
        for email in email_list:
            print(f"Sending email to: {email}")
            server.sendmail(sender_email, email, msg.as_string())
    else:
        print("No RECEIVER_EMAIL environment variable found.")
    
    # server.sendmail(sender_email, receiver_email, msg.as_string())
    
    # print("send email")
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
    print("send_status_email")
    subject = f'Healthcheck {project["name"]}'
    if status == 0:
        body = f'{project["name"]} failed health check. {project["url"]}'
    else:
        body = f'{project["name"]} passed health check. {project["url"]}'
    send_email(subject, body, os.environ.get("SENDER_EMAIL"), reciever_email)

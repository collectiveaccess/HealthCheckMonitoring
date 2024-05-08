import os
from dotenv import load_dotenv
import requests

load_dotenv()

def post_status_down_message(project, webhook_url):
    data = {"text": f'{project["name"]} failed health check. {project["url"]}'}
    requests.post(webhook_url, json=data)

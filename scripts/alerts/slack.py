import os
from dotenv import load_dotenv
import requests

load_dotenv()

def post_status_down_message(project):
    data = {'text':  f'{project["name"]} failed health check. {project["url"]}'}
    requests.post(os.environ.get("SLACK_WEBHOOK"), json = data)


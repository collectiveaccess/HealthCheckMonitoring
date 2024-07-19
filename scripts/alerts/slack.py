from dotenv import load_dotenv
import requests

load_dotenv()


def post_status_message(project, status, webhook_url):
    if webhook_url is None: 
        return
    if status == 0:
        data = {"text": f'{project["name"]} failed health check. {project["url"]}'}
    else:
        data = {"text": f'{project["name"]} passed health check. {project["url"]}'}

    requests.post(webhook_url, json=data)

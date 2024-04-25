import requests
import db_utils

OK_MESSAGE = "status=happy"


def update_statuses():
    projects = db_utils.fetch_projects()
    for project in projects:
        try:
            response = requests.get(project["url"], timeout=5)
        except requests.exceptions.RequestException as error:
            error_handler(project, str(error))
        except Exception as error:
            error_handler(project, error)
        else:
            if response.text == OK_MESSAGE:
                success_handler(project)
            else:
                error_handler(project, response.text)


def success_handler(project):
    db_utils.create_status(project["id"], 1, None)


def error_handler(project, error_message):
    db_utils.create_status(project["id"], 0, error_message)


update_statuses()

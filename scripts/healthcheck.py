import requests
import db_utils
import alerts.email_utils as email_utils
import alerts.slack as slack

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
    db_utils.update_project(project["id"], 1)


def error_handler(project, error_message):
    # TODO: determines on when to send alerts. do we send separate alerts for
    # each project?

    print(f'{project["name"]} failed healthcheck')
    db_utils.create_status(project["id"], 0, error_message)
    db_utils.update_project(project["id"], 0)

    # TODO: how often do we send notifications?
    # send alert notifications once per crash
    if project["status"] == 1 or project["status"] is None:
        email_utils.send_status_down_email(project)
        slack.post_status_down_message(project)
        print("notifications sent")


update_statuses()

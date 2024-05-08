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

    # send notifications when site comes back up
    if project["status"] == 0:
        handle_notifications(project)


def error_handler(project, error_message):
    # TODO: determines on when to send alerts. do we send separate alerts for
    # each project?

    print(f'{project["name"]} failed healthcheck')
    db_utils.create_status(project["id"], 0, error_message)
    db_utils.update_project(project["id"], 0)

    # send notifications when site is first detected down
    if project["status"] == 1 or project["status"] is None:
        handle_notifications(project)


def handle_notifications(project):
    # handle defaults alerts
    if project['email_alert'] == 1:
        email_utils.send_status_down_email(project, os.environ.get("RECEIVER_EMAIL"))
    if project['slack_alert'] == 1:
        slack.post_status_down_message(project, os.environ.get("SLACK_WEBHOOK"))

    # handle project specific alerts
    contacts = db_utils.fetch_project_contacts(project['id'])
    for contact in contacts:
        if contact['type'] == 'email' and  project['email_alert'] == 1:
            email_utils.send_status_down_email(project, contact['value'])
        elif contact['type'] == 'slack' and project['slack_alert'] == 1:
            slack.post_status_down_message(project, contact['value'])

    print("notifications sent")



update_statuses()

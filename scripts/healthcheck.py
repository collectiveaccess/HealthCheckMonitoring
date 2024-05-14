import fire
import requests
import db_utils
import alerts.email_utils as email_utils
import alerts.slack as slack
import os


def update_all_projects_statuses():
    projects = db_utils.fetch_projects()
    for project in projects:
        update_project_status(project['id'])


def update_project_status(project_id):
    try:
        project = db_utils.fetch_project(project_id)
        if project is None:
            print('invalid project_id')
            return
    except:
        print('could not connect to database')
        return

    try:
        response = requests.get(project["url"], timeout=5)
    except requests.exceptions.RequestException as error:
        error_handler(project, str(error))
    except Exception as error:
        error_handler(project, error)
    else:
        # TODO: handle non-CollectiveAccess sites
        if response.text == "status=happy":
            success_handler(project)
        else:
            error_handler(project, response.text)


def success_handler(project):
    current_status = 1

    # send notifications when site comes back up
    if project["status"] == 0:
        handle_notifications(project, current_status)

    db_utils.create_status(project["id"], current_status, None)
    db_utils.update_project(project["id"], current_status)


def error_handler(project, error_message):
    print(f'{project["name"]} failed healthcheck')
    current_status = 0

    # send notifications when site is first detected down
    if project["status"] == 1 or project["status"] is None:
        handle_notifications(project, current_status)

    db_utils.create_status(project["id"], current_status, error_message)
    db_utils.update_project(project["id"], current_status)


def handle_notifications(project, status):
    # handle defaults alerts
    if project["email_alert"] == 1:
        email_utils.send_status_email(project, status, os.environ.get("RECEIVER_EMAIL"))
    if project["slack_alert"] == 1:
        slack.post_status_message(project, status, os.environ.get("SLACK_WEBHOOK"))

    # handle project specific alerts
    contacts = db_utils.fetch_project_contacts(project["id"])
    for contact in contacts:
        if contact["type"] == "email" and project["email_alert"] == 1:
            email_utils.send_status_email(project, status, contact["value"])
        elif contact["type"] == "slack" and project["slack_alert"] == 1:
            slack.post_status_message(project, status, contact["value"])

    print("notifications sent")


if __name__ == '__main__':
  fire.Fire({
      'update_project_status': update_project_status,
      'update_all_projects_statuses': update_all_projects_statuses,
  })

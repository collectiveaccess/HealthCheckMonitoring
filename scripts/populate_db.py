from pathlib import Path
import csv
import db_utils

# TODO: is there a better way to get a list of all projects
with open(Path("data", "projects.csv")) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        url = row["url"]
        project = db_utils.fetch_project_by_url(url)
        if project is None:
            db_utils.create_project(
                row["name"],
                row["url"],
                row["notes"],
                row["client_name"],
                row["cluster_name"],
                row["slack_alert"],
                row["email_alert"],
                row["check_frequency"],
            )


with open(Path("data", "contacts.csv")) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        url = row["url"]
        project = db_utils.fetch_project_by_url(url)
        if project:
            db_utils.create_contact(project["id"], row["type"], row["value"])

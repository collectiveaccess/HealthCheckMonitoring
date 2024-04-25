from pathlib import Path
import csv
import db_utils

# TODO: is there a better way to get a list of all projects
with open(Path("data", "projects.csv")) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        url = row["url"]
        project_name = row["name"]
        project = db_utils.fetch_project(url)
        if project is None:
            db_utils.create_project(project_name, url)

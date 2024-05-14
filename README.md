# CollectiveAccess Healthcheck

Python scripts to retrieve and store healthcheck status for CollectiveAccess. If the healthcheck fails for one of projects, notifications will be sent via email and Slack.

## Install

Install libraries

```bash
pip install -f requirement.txt
```

Create database. We are using sqlite.

```bash
python scripts/create_db.py
```

Populate database with existing projects. The list of projects are stored in `/data/projects.csv`.

- name - name of project
- url - url for the healthcheck endpoint
- notes - notes about the project
- client_name - client name
- cluster_name - kubernettes cluster name
- slack_alert - create slack notifications; 0 for false, 1 for true
- email_alert - create email notifications; 0 for false, 1 for true
- check_frequency - how frequently to ping the healthcheck endpoint; integer that represents minutes, e.g. 3 for check every 3 minutes


```bash
python scripts/populate_db.py
```

## Run scripts

Setup envars. Copy `env.sample`, and rename it `.env`. Fill in the email and Slack info.

Run script to retrieve and store healthcheck status and send notifications. This script should be called with a cron job.

check all projects
```bash
python scripts/healthcheck.py update_all_projects_statuses
```

check one project
```bash
python scripts/healthcheck.py update_project_status <project id>
```

## Other

We are using `ruff` to lint and format the python scripts

```bash
ruff format ./scripts
ruff check ./scripts
```

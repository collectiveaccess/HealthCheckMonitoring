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

Populate database with existing projects. The list of projects are stored in `/data/projects.csv`. The csv has two columns:
name - name of project
url - url for the healthcheck endpoint

```bash
python scripts/populate_db.py
```

## Run scripts

Setup envars. Copy `env.sample`, and rename it `.env`. Fill in the email and Slack info.

Run script to retrieve and store healthcheck status and send notifications. This script should be called with a cron job.

```bash
python scripts/healthcheck.py
```

## Other

We are using `ruff` to lint and format the python scripts

```bash
ruff format ./scripts
ruff check ./scripts
```

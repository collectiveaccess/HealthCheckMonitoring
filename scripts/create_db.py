# TODO: is there a better database to use?
import sqlite3
from pathlib import Path
import os

data_dir = Path("data")
db_file = "healthcheck.db"
db_path = data_dir / db_file

os.makedirs(data_dir, exist_ok=True)

con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING NOT NULL,
    url STRING NOT NULL,
    notes TEXT,
    client_name STRING NOT NULL,
    cluster_name STRING NOT NULL,
    status INTEGER,
    slack_alert INTEGER NOT NULL,
    email_alert INTEGER NOT NULL,
    check_frequency INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT current_timestamp
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    status INTEGER NOT NULL,
    error_message TEXT,
    created_at TEXT NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY (project_id) REFERENCES projects (id)
    )""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    type string NOT NULL,
    value string NOT NULL,
    created_at TEXT NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    UNIQUE(project_id, type, value) ON CONFLICT IGNORE
    )""")


con.commit()

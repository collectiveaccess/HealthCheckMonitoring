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
    url STRING NOT NULL
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

con.commit()

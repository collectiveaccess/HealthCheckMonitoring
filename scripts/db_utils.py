from pathlib import Path
import sqlite3

data_dir = Path("data")
db_file = "healthcheck.db"
db_path = data_dir / db_file


def fetch_project(url):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT id FROM projects WHERE url = ?", [url])
    con.commit()


def create_project(name, url):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO projects (name, url) VALUES(?, ?)", [name, url])
    con.commit()

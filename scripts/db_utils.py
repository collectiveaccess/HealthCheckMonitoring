from pathlib import Path
import sqlite3

data_dir = Path("data")
db_file = "healthcheck.db"
db_path = data_dir / db_file


def dict_factory(cursor, row):
    """convert row as python dictionary"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# TODO: how long should we store the statuses?
def create_status(project_id, status, error_message=None):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    if error_message:
        cur.execute(
            "INSERT INTO statuses (project_id, status, error_message) VALUES(?, ?, ?)",
            [project_id, status, error_message],
        )
    else:
        cur.execute(
            "INSERT INTO statuses (project_id, status) VALUES(?, ?)",
            [project_id, status],
        )

    con.commit()


def fetch_projects():
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    res = cur.execute("SELECT id, url, name, status from projects;")
    return res.fetchall()


def fetch_project(url):
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT id FROM projects WHERE url = ?", [url])
    con.commit()


def create_project(name, url):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO projects (name, url) VALUES(?, ?)", [name, url])
    con.commit()

def update_project(id, status):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE projects SET status = ? WHERE id = ?", [status, id])
    con.commit()

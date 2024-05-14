from pathlib import Path
import sqlite3

project_path = Path(__file__).parent.parent
db_path = Path(project_path, "data", "healthcheck.db")


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
    res = cur.execute("SELECT * from projects;")
    return res.fetchall()


def fetch_project_by_url(url):
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    res = cur.execute("SELECT * FROM projects WHERE url = ?", [url])
    return res.fetchone()


def fetch_project(id):
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    res = cur.execute("SELECT * FROM projects WHERE id = ?", [id])
    return res.fetchone()


def fetch_project_contacts(project_id):
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    res = cur.execute("SELECT * FROM contacts WHERE project_id = ?", [project_id])
    return res.fetchall()


def create_project(
    name,
    url,
    notes,
    client_name,
    cluster_name,
    slack_alert,
    email_alert,
    check_frequency,
):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        """INSERT INTO projects
        (name, url, notes, client_name, cluster_name, slack_alert, email_alert, check_frequency)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            name,
            url,
            notes,
            client_name,
            cluster_name,
            slack_alert,
            email_alert,
            check_frequency,
        ],
    )
    con.commit()


def update_project(id, status):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE projects SET status = ? WHERE id = ?", [status, id])
    con.commit()


def create_contact(project_id, type, value):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        """INSERT INTO contacts
        (project_id, type, value)
        VALUES(?, ?, ?)""",
        [project_id, type, value],
    )
    con.commit()

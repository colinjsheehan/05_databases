import sqlite3
from datetime import date

conn = sqlite3.connect("repos.db")
cursor = conn.cursor()

def insert_repo(name, days_since_push, status):
    today = date.today().isoformat()
    cursor.execute(
        "INSERT INTO repos (name, days_since_push, status, snapshot_date) VALUES (?, ?, ?, ?)",
        (name, days_since_push, status, today)
    )
    conn.commit()

def get_all_repos():
    cursor.execute("SELECT * FROM repos")
    return cursor.fetchall()

insert_repo("new-repo", 5, "ACTIVE")

for row in get_all_repos():
    print(row)

conn.close()
import requests                                                                                                       
import os       
import sqlite3                                                                                                        
from dotenv import load_dotenv
from datetime import datetime, timezone, date

load_dotenv()

# --- DB setup ---
conn = sqlite3.connect("repos.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS repos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        days_since_push INTEGER,
        status TEXT,
        snapshot_date TEXT
    )
""")
conn.commit()

# --- Fetch from GitHub ---
USERNAME = os.getenv("GITHUB_USERNAME")
url = f"https://api.github.com/users/{USERNAME}/repos?per_page=20&sort=pushed"
response = requests.get(url)
repos = response.json()

now = datetime.now(timezone.utc)
today = date.today().isoformat()

print(f"\n{'REPO':<35} {'LAST PUSH':<15} STATUS\n" + "-" * 60)

for repo in repos:
    name = repo["name"]
    pushed = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
    days_ago = (now - pushed).days

    if days_ago <= 30:
        status = "ACTIVE"
    elif days_ago <= 180:
        status = "STALE"
    else:
        status = "INACTIVE"

    print(f"{name:<35} {days_ago:<15} {status}")

    cursor.execute(
        "INSERT INTO repos (name, days_since_push, status, snapshot_date) VALUES (?, ?, ?, ?)",
        (name, days_ago, status, today)
    )

conn.commit()
conn.close()

print(f"\nSnapshot saved to database ({today})\n")



# 05 — Databases Progress

## What we built
A database that stores a snapshot of your GitHub repos every time the dashboard runs.

---

## Steps

### 1. Opened SQLite from the terminal
```bash
sqlite3 repos.db
```
This creates a `.db` file on disk and drops into a SQL shell. No server, no setup — SQLite is just a file.

---

### 2. Created a table
```sql
CREATE TABLE repos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    days_since_push INTEGER,
    status TEXT,
    snapshot_date TEXT
);
```
A table is like a spreadsheet with fixed columns. Each row is one record.
`AUTOINCREMENT` means SQLite assigns IDs automatically — you never reuse a deleted ID.

---

### 3. Learned the four core SQL operations (CRUD)
| Operation | SQL keyword | What it does |
|---|---|---|
| Create | `INSERT` | Adds a new row |
| Read | `SELECT` | Fetches rows |
| Update | `UPDATE` | Modifies existing rows |
| Delete | `DELETE` | Removes rows |

Also used `WHERE` to filter, `ORDER BY` to sort, and `COUNT(*)` to aggregate.

---

### 4. Connected SQLite to Python using `sqlite3`
```python
import sqlite3

conn = sqlite3.connect("repos.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM repos")
rows = cursor.fetchall()
conn.close()
```
- `conn` — the connection to the database file
- `cursor` — the object that executes SQL and holds results
- `fetchall()` — returns all rows as a list of tuples

---

### 5. Learned about SQL injection and why `?` placeholders matter
Never do this:
```python
cursor.execute(f"INSERT INTO repos (name) VALUES ('{name}')")  # UNSAFE
```
If `name` contains SQL code, it gets executed. Always do this instead:
```python
cursor.execute("INSERT INTO repos (name) VALUES (?)", (name,))  # SAFE
```
The `?` syntax passes values separately so they can never be interpreted as SQL.

---

### 6. Integrated the database into the GitHub dashboard
- Added `CREATE TABLE IF NOT EXISTS` at the top — safe to run every time
- Added an `INSERT` inside the repo loop — saves each repo as a row
- Added `conn.commit()` after the loop — writes changes to disk

Now every run of `dashboard.py` saves a full snapshot of your repos to `repos.db`.

---

## Files
- `repos.db` — the SQLite database file
- `db.py` — scratch file used to learn `sqlite3` basics
- `dashboard.py` — GitHub dashboard, now with database saving

---

## Up next
SQLAlchemy — an ORM (Object Relational Mapper) that lets you interact with the database using Python classes instead of raw SQL strings.

"""
db.py
Database helpers for TaskBoard. Provides:
 - get_db(): per-request sqlite3 connection (attached to flask.g)
 - close_db(): teardown to close connection
 - init_db(app=None): ensure DB file + schema exist and optionally register app teardown

This module ensures the DB is created and seeded automatically (no CLI required).
"""

import sqlite3
from pathlib import Path
from flask import g

# Path to sqlite DB file (relative to working dir)
DB_PATH = Path("taskboard.db")

# SQL schema (safe to run multiple times because we use CREATE TABLE IF NOT EXISTS)
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    tag TEXT,
    due_date TEXT,       -- ISO date string (YYYY-MM-DD) or NULL
    status TEXT NOT NULL DEFAULT 'todo', -- one of 'todo', 'doing', 'done'
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def get_db():
    """
    Return a sqlite3.Connection stored on flask.g.
    Each request gets (and reuses) one connection.
    The connection uses sqlite3.Row for convenient column access by name.
    """
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH.as_posix(), detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(e=None):
    """
    Close DB connection stored in flask.g (if any).
    This is intended to be registered with Flask's teardown_appcontext.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app=None):
    """
    Ensure the database file and schema exist. Optionally register Flask teardown for connection cleanup.

    If the tasks table is empty, insert a couple of sample rows to make the app look alive.
    """
    # Ensure parent directory exists if DB_PATH had directories (not needed here but safe)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Always create/verify schema (CREATE TABLE IF NOT EXISTS is idempotent)
    conn = sqlite3.connect(DB_PATH.as_posix())
    conn.executescript(SCHEMA)
    conn.commit()

    # Seed sample tasks if table empty (helps during review by employers)
    cur = conn.cursor()
    cur.execute("SELECT count(1) FROM tasks")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute(
            "INSERT INTO tasks (title, description, tag, due_date, status) VALUES (?,?,?,?,?)",
            ("Welcome task", "This is a sample task. Edit or delete it.", "onboarding", None, "todo"),
        )
        cur.execute(
            "INSERT INTO tasks (title, description, tag, due_date, status) VALUES (?,?,?,?,?)",
            ("Fix README", "Improve README to make it comprehensive.", "docs", None, "doing"),
        )
        conn.commit()

    conn.close()

    # If an app is provided, register the teardown function so connections are closed after each request.
    # Registering multiple times is safe; Flask will ignore duplicate functions.
    if app is not None:
        app.teardown_appcontext(close_db)

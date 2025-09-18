"""
models.py
Data access layer for the TaskBoard app.

All SQL lives here, via a simple Task class with static methods.
This keeps SQL separate from routing logic and improves maintainability.
"""

import sqlite3
from typing import Dict, Any, List, Optional


class Task:
    @staticmethod
    def row_to_dict(row: sqlite3.Row) -> Optional[Dict[str, Any]]:
        """
        Convert a sqlite3.Row to a plain dict. Return None if row is falsy.
        Jinja templates prefer plain dicts.
        """
        if not row:
            return None
        return {k: row[k] for k in row.keys()}

    @staticmethod
    def get(db: sqlite3.Connection, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a single task by id.
        """
        cur = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        return Task.row_to_dict(row)

    @staticmethod
    def get_all(db: sqlite3.Connection, status: Optional[str] = None, tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch all tasks, optionally filtering by status and/or tag.
        Results are ordered: todo -> doing -> done, then by due date (nulls last).
        Parameterized queries are used to prevent SQL injection.
        """
        sql = "SELECT * FROM tasks"
        params = []
        where = []

        if status:
            where.append("status = ?")
            params.append(status)
        if tag:
            where.append("tag = ?")
            params.append(tag)

        if where:
            sql += " WHERE " + " AND ".join(where)

        # Order: todo (0), doing (1), done (2), then null due_date last, then due_date asc
        sql += " ORDER BY CASE status WHEN 'todo' THEN 0 WHEN 'doing' THEN 1 ELSE 2 END, due_date IS NULL, due_date"

        cur = db.execute(sql, params)
        rows = cur.fetchall()
        return [Task.row_to_dict(r) for r in rows]

    @staticmethod
    def create(db: sqlite3.Connection, title: str, description: Optional[str] = None, tag: Optional[str] = None, due_date: Optional[str] = None, status: str = "todo") -> int:
        """
        Insert a new task. Returns the new task's id.
        due_date should be either None or a string 'YYYY-MM-DD'.
        """
        cur = db.execute(
            "INSERT INTO tasks (title, description, tag, due_date, status) VALUES (?,?,?,?,?)",
            (title, description, tag, due_date, status),
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def update(db: sqlite3.Connection, task_id: int, title: str, description: Optional[str] = None, tag: Optional[str] = None, due_date: Optional[str] = None, status: str = "todo") -> None:
        """
        Update the task fields.
        """
        db.execute(
            "UPDATE tasks SET title = ?, description = ?, tag = ?, due_date = ?, status = ? WHERE id = ?",
            (title, description, tag, due_date, status, task_id),
        )
        db.commit()

    @staticmethod
    def delete(db: sqlite3.Connection, task_id: int) -> None:
        """
        Delete a task by id.
        """
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()

    @staticmethod
    def cycle_status(db: sqlite3.Connection, task_id: int) -> None:
        """
        Cycle status through todo -> doing -> done -> todo.
        Useful for a quick UI action.
        """
        cur = db.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if not row:
            return
        current = row[0]
        order = ["todo", "doing", "done"]
        try:
            idx = order.index(current)
        except ValueError:
            idx = 0
        new = order[(idx + 1) % len(order)]
        db.execute("UPDATE tasks SET status = ? WHERE id = ?", (new, task_id))
        db.commit()

    @staticmethod
    def get_all_tags(db: sqlite3.Connection) -> List[str]:
        """
        Return a list of distinct tags currently used by tasks.
        """
        cur = db.execute("SELECT DISTINCT tag FROM tasks WHERE tag IS NOT NULL")
        rows = cur.fetchall()
        return [r[0] for r in rows if r[0]]

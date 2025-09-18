"""
app.py
Main Flask application for the TaskBoard project.

How to run:
    1. Create & activate a virtualenv (optional but recommended)
    2. pip install Flask
    3. python app.py
    4. Open http://127.0.0.1:5000

This file wires routes to the data layer (models.py) and the DB helper (db.py).
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash

# local modules
from db import init_db, get_db
from models import Task

# Create the Flask app instance
# Keeping a simple app factory is possible, but a single module is clearer for small projects.
app = Flask(__name__)

# A development SECRET_KEY. In production set an environment variable.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

# Initialize DB (creates file, ensures schema, seeds sample rows if empty)
# Passing `app` registers teardown for closing DB connections.
init_db(app)


@app.route("/")
def index():
    """
    Main page: list tasks, optional filters: ?status=todo|doing|done & ?tag=TAG
    """
    db = get_db()

    # Read optional filters from query params
    status = request.args.get("status") or None
    tag = request.args.get("tag") or None

    tasks = Task.get_all(db, status=status, tag=tag)
    tags = Task.get_all_tags(db)

    return render_template(
        "index.html",
        tasks=tasks,
        tags=tags,
        selected_status=status,
        selected_tag=tag,
    )


@app.route("/task/new", methods=("GET", "POST"))
def create_task():
    """
    Create a new task. Simple server-side validation (title required).
    """
    if request.method == "POST":
        # Pull values from form, trim whitespace
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        tag = (request.form.get("tag") or "").strip() or None
        due_date = (request.form.get("due_date") or "").strip() or None

        if not title:
            flash("Title is required.", "error")
            return render_template("task_form.html", task=None)

        db = get_db()
        Task.create(db, title=title, description=description, tag=tag, due_date=due_date)
        flash("Task created.", "success")
        return redirect(url_for("index"))

    # GET -> show empty form
    return render_template("task_form.html", task=None)


@app.route("/task/<int:task_id>/edit", methods=("GET", "POST"))
def edit_task(task_id):
    """
    Edit an existing task. If the task doesn't exist, redirect to index.
    """
    db = get_db()
    task = Task.get(db, task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        description = (request.form.get("description") or "").strip()
        tag = (request.form.get("tag") or "").strip() or None
        due_date = (request.form.get("due_date") or "").strip() or None
        status = request.form.get("status") or "todo"

        if not title:
            flash("Title is required.", "error")
            return render_template("task_form.html", task=task)

        Task.update(
            db,
            task_id,
            title=title,
            description=description,
            tag=tag,
            due_date=due_date,
            status=status,
        )
        flash("Task updated.", "success")
        return redirect(url_for("index"))

    # GET -> show form with existing values
    return render_template("task_form.html", task=task)


@app.route("/task/<int:task_id>/delete", methods=("GET", "POST"))
def delete_task(task_id):
    """
    Confirm then delete a task. Uses GET to show confirmation and POST to perform deletion.
    """
    db = get_db()
    task = Task.get(db, task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        Task.delete(db, task_id)
        flash("Task deleted.", "success")
        return redirect(url_for("index"))

    return render_template("confirm_delete.html", task=task)


@app.route("/task/<int:task_id>/toggle")
def toggle_task(task_id):
    """
    Quick action that cycles status: todo -> doing -> done -> todo
    (useful for employers to see a quick UI action)
    """
    db = get_db()
    task = Task.get(db, task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("index"))

    Task.cycle_status(db, task_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Running directly: enable debug for development. In production use a WSGI server.
    app.run(debug=True)

# 🗂️ TaskBoard — Simple Flask + SQLite Task Manager

TaskBoard is a **clean, single-user task manager** built using **Flask** and **SQLite**.  
It’s designed to be simple yet demonstrate **real-world engineering practices**:  

---

## ✨ Features

- ✅ **Create, edit, delete** tasks  
- 🔄 **Toggle task status** (`todo → doing → done → todo`)  
- 🏷 **Tag support** for simple categorization  
- 📅 **Optional due dates** (YYYY-MM-DD)  
- 🔍 **Filter tasks** by status or tag  
- 💾 **Auto-initialized SQLite database** on first run — no CLI setup  
- 🎨 **Responsive UI** built with Bootstrap  
- 🧹 **Extensively commented, maintainable code**

---

## 🛠 Tech Stack

- **Python 3.x**  
- **Flask** (lightweight web framework)  
- **SQLite3** (embedded relational database)  
- **Jinja2** (templating engine)  
- **Bootstrap** (CSS styling)  

---


## Installation 
- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate
- pip install Flask
- python3 app.py

---

## 📂 Project Structure


flask-taskboard/
├─ app.py               # Flask app & route handlers
├─ db.py                # DB connection, init, teardown helpers
├─ models.py            # Task class: all database operations
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ task_form.html
│  └─ confirm_delete.html
├─ static/
│  └─ style.css
└─ taskboard.db         # Auto-generated on first run

---

## 📐 Design Choices

- **Single table:** Keeps the project simple and easy to query.  
- **Status field:** Cycles through three values to avoid complex joins.  
- **Tag field:** Enables lightweight categorization.  
- **Due date:** Stored as text for simplicity.  
- **Timestamps:** Useful for sorting or auditing later.  

---

## 🧱 Program Architecture & Logic

### Overall Flow
1. **Flask routes (`app.py`)** handle HTTP requests.  
2. **`db.py`** ensures a database connection exists for each request and initializes the schema.  
3. **`models.py`** defines the `Task` class which wraps all SQL operations.  
4. **Templates** use Jinja2 to render HTML dynamically.  
5. **Static CSS** provides basic styling.  

---

### Components in Detail

#### `app.py`
- Configures Flask and `SECRET_KEY`.  
- Calls `init_db(app)` to ensure the DB exists and seeds demo tasks.  
- Defines routes:  
  - `/` — View/filter tasks.  
  - `/task/new` — Add new task.  
  - `/task/<id>/edit` — Edit existing task.  
  - `/task/<id>/delete` — Confirm and delete task.  
  - `/task/<id>/toggle` — Cycle status.  

#### `db.py`
- `get_db()` manages per-request SQLite connections.  
- `init_db(app)` creates the schema and seeds demo data automatically.  
- `close_db()` closes the DB connection when the request ends.  

#### `models.py`
**Class-Based Approach:**  
- Groups all task operations under `Task`, making the codebase modular.  
- Easier to extend (e.g., migrate to PostgreSQL or add more methods).  
- Improves readability: `Task.create()` vs. scattered functions.  
- Uses static methods since no object state is required yet.  

**Methods Provided:**  
- `get_all(filters)`  
- `get(task_id)`  
- `create(title, description, tag, due_date)`  
- `update(id, title, description, tag, due_date)`  
- `delete(id)`  
- `cycle_status(id)`  
- `get_all_tags()`  

#### Templates
- **base.html:** Shared header/footer and Bootstrap integration.  
- **index.html:** Displays task board with filters.  
- **task_form.html:** Handles both create and edit forms.  
- **confirm_delete.html:** Confirmation page for deletions.  

#### Static Assets
- **style.css:** Minor styling enhancements on top of Bootstrap.  

---

## 🔐 Security Notes

- **SQL Injection:** Prevented by parameterized queries.  
- **XSS:** Jinja2 escapes output by default.  
- **CSRF:** Not implemented (demo) — add Flask-WTF for production.  
- **Secret Key:** Replace with a strong environment variable for deployment.  

---

## 🚀 Possible Extensions

- 🔑 User authentication and multi-user support.  
- 🧵 Multiple tags per task (many-to-many).  
- 📡 JSON REST API endpoints.  
- 🛡 CSRF protection with Flask-WTF forms.  
- 🧪 Unit tests with pytest and CI integration.  
- 🐳 Dockerize the app for containerized deployment.  
- 🏗 Use SQLAlchemy ORM and migrations for larger-scale projects.  
---
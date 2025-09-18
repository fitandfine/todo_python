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

```text
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
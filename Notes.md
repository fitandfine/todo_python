# 📘 TaskBoard — Complete Knowledge Guide

This document is a **comprehensive technical guide** for the TaskBoard project — a single-user task manager built with **Flask** and **SQLite**. It covers architecture, design principles, Python features, database design, security considerations, testing, deployment, and best practices. This guide is intended for developers who want to understand, maintain, or replicate a similar application.

---

## 📋 High-Level Overview

TaskBoard is a **clean, maintainable, single-user task manager** designed to showcase real-world engineering practices:

- Lightweight Flask web framework
- Embedded SQLite database
- Class-based models for business logic
- Auto-initialized database with demo data
- Responsive UI using Bootstrap
- Secure and parameterized SQL operations
- Readable, commented, modular code structure

It provides CRUD functionality, task status cycling, tagging, filtering, and optional due dates.

---

## 🛠 Tech Stack

- **Python 3.x** – Core programming language  
- **Flask** – Web framework for request routing and rendering  
- **SQLite3** – Embedded relational database for simple persistence  
- **Jinja2** – Templating engine for dynamic HTML rendering  
- **Bootstrap** – CSS framework for responsive UI  
- **pytest / black / flake8** – Suggested for testing and code quality

---

## 🧭 Core Design Principles

- **Separation of Concerns:** Routes (`app.py`), database access (`db.py`), and business logic (`models.py`) are independent.  
- **Single Responsibility Principle:** Each module serves one clear purpose.  
- **KISS (Keep It Simple, Stupid):** Prioritize readability and maintainability.  
- **YAGNI (You Aren’t Gonna Need It):** Only implement necessary features but maintain extensibility.  
- **Fail Fast & Explicit Errors:** Input validation with clear error messages.  
- **Security by Design:** Parameterized queries, input sanitization, escaping HTML output.  
- **Extensive Inline Comments:** Makes the codebase maintainable and reviewer-friendly.

---

## 📂 Project Structure

flask-taskboard/
├─ app.py # Flask application and route handlers
├─ db.py # Database connection management and initialization
├─ models.py # Task class with all database operations
├─ templates/
│ ├─ base.html # Shared layout template
│ ├─ index.html # Task board view with filters
│ ├─ task_form.html # Create/edit task form
│ └─ confirm_delete.html # Delete confirmation page
└─ static/
└─ style.css # Minor styling overrides to Bootstrap


- **app.py:** Handles HTTP requests, form submissions, and template rendering  
- **db.py:** Manages per-request SQLite connections, initialization, and teardown  
- **models.py:** Contains class-based Task model with static methods for CRUD  
- **templates/**: Display-only logic with Jinja2  
- **static/**: CSS and other assets

---

## 🧱 Why Class-Based Models?

### Advantages

1. **Namespacing & Discoverability:** `Task.create()` and `Task.get_all()` are intuitive.  
2. **Encapsulation:** SQL logic and conversion live in one place.  
3. **Extensibility:** Easily add new methods (e.g., `Task.search()`) or migrate DB backend.  
4. **Testability:** Unit tests can directly call Task methods.  
5. **Readability:** Shows the domain clearly — Task is the entity being manipulated.  

### Notes

- **Static methods** suffice since object state is not required yet.  
- Can evolve into instance methods if complex state or behavior is introduced.  
- Function-based design is simpler for small scripts but less scalable.

---

## 🗄 Database Design

### Schema

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    tag TEXT,
    due_date TEXT,
    status TEXT NOT NULL DEFAULT 'todo',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

---

## Design Choices

- Single table: Simplifies querying and maintenance

- Status field: Cycles through todo → doing → done

- Tag field: Lightweight categorization

- Due date: Stored as ISO YYYY-MM-DD text

- Timestamps: Supports sorting and auditing
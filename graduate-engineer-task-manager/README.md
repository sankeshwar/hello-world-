# TaskFlow — Graduate Software Engineer Portfolio Project

A beginner-friendly task management web application built to demonstrate practical software engineering fundamentals relevant to a graduate software engineer role.

## Features

- Create tasks with a title and optional description
- Mark tasks complete and undo completion
- Delete tasks
- Persist data with SQLite
- JSON endpoint at `GET /api/tasks`
- Input validation and parameterized SQL queries
- Automated tests with pytest
- Responsive interface

## Technology

- Python 3.10+
- Flask
- SQLite
- HTML and CSS
- pytest

## Run locally

```bash
cd graduate-engineer-task-manager
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Run tests

```bash
pytest -q
```

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/tasks` | Return all tasks as JSON |
| POST | `/tasks` | Create a task using form fields `title` and optional `description` |
| POST | `/tasks/<id>/toggle` | Toggle completion |
| POST | `/tasks/<id>/delete` | Delete a task |

## Engineering decisions

- SQLite keeps setup lightweight for a graduate-level demonstration.
- Parameterized SQL statements help prevent SQL injection.
- Flask's application factory makes the app easier to test with a temporary database.
- Tests cover the home page, task creation, validation, completion and deletion.

## Planned improvements

- Add user authentication and per-user task ownership
- Add edit-task functionality and pagination
- Add CSRF protection and production configuration
- Add CI with GitHub Actions
- Deploy to a cloud platform

## Portfolio note

This is a learning/portfolio project. Extend it, run the tests, and add screenshots or a live demo after deployment. Do not claim planned features as completed.

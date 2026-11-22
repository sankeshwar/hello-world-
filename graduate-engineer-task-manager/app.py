from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tasks.db"

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update({"DATABASE": str(DB_PATH), "TESTING": False})
    if test_config:
        app.config.update(test_config)

    def get_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        with get_db() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    completed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    with app.app_context():
        init_db()

    @app.get("/")
    def index():
        with get_db() as db:
            tasks = db.execute("SELECT * FROM tasks ORDER BY completed, id DESC").fetchall()
        return render_template("index.html", tasks=tasks)

    @app.post("/tasks")
    def add_task():
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if not title:
            return jsonify({"error": "Task title is required."}), 400
        if len(title) > 120:
            return jsonify({"error": "Title must be 120 characters or fewer."}), 400
        with get_db() as db:
            db.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_id>/toggle")
    def toggle_task(task_id):
        with get_db() as db:
            db.execute("UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id = ?", (task_id,))
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_id>/delete")
    def delete_task(task_id):
        with get_db() as db:
            db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return redirect(url_for("index"))

    @app.get("/api/tasks")
    def list_tasks():
        with get_db() as db:
            rows = db.execute("SELECT id, title, description, completed, created_at FROM tasks ORDER BY id DESC").fetchall()
        return jsonify([dict(row) for row in rows])

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

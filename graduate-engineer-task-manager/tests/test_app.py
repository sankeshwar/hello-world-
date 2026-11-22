import pytest
from app import create_app

@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data

def test_create_task_and_list_api(client):
    response = client.post("/tasks", data={"title": "Learn Flask", "description": "Build a small app"}, follow_redirects=True)
    assert response.status_code == 200
    tasks = client.get("/api/tasks").get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Learn Flask"

def test_reject_empty_task(client):
    response = client.post("/tasks", data={"title": ""})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Task title is required."

def test_toggle_and_delete_task(client):
    client.post("/tasks", data={"title": "Test task"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/tasks/{task_id}/toggle")
    assert client.get("/api/tasks").get_json()[0]["completed"] == 1
    client.post(f"/tasks/{task_id}/delete")
    assert client.get("/api/tasks").get_json() == []

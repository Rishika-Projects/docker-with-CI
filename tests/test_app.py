import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app
from fastapi.testclient import TestClient

client = TestClient(app.app)


def test_home():
    response = client.get("/")

    assert response.status_code == 201
    assert response.json()["message"] == "FastAPI running with Docker Compose v1 Testing"


def test_create_database(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(app, "DB_PATH", str(db_path))

    response = client.get("/create")

    assert response.status_code == 200
    assert response.json() == {"message": "Database and users table created"}


def test_get_users(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(app, "DB_PATH", str(db_path))

    client.get("/create")
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == {"users": []}
import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Tests use a temporary SQLite file, never backend/expenses.db.
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    return TestClient(app)

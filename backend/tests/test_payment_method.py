import sqlite3

from app import db


def test_payment_method_defaults_to_upi(client):
    body = client.post("/expenses", json={"description": "Chai", "amount_paise": 2000}).json()
    assert body["payment_method"] == "upi"


def test_payment_method_is_saved_and_listed(client):
    client.post("/expenses", json={"description": "Fuel", "amount_paise": 150000, "payment_method": "card"})
    assert client.get("/expenses").json()[0]["payment_method"] == "card"


def test_unknown_payment_method_is_rejected(client):
    response = client.post("/expenses", json={"description": "Fuel", "amount_paise": 100, "payment_method": "cheque"})
    assert response.status_code == 422


def test_old_database_without_payment_method_gets_the_column(tmp_path, monkeypatch):
    path = tmp_path / "old.db"
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL,"
        " amount_paise INTEGER NOT NULL, spent_on TEXT NOT NULL, category TEXT NOT NULL DEFAULT 'other',"
        " archived INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL)"
    )
    conn.execute(
        "INSERT INTO expenses (description, amount_paise, spent_on, created_at)"
        " VALUES ('Old', 100, '2026-11-01', '2026-11-01T00:00:00+00:00')"
    )
    conn.commit()
    conn.close()
    monkeypatch.setattr(db, "DB_PATH", path)
    assert db.list_expenses()[0]["payment_method"] == "upi"

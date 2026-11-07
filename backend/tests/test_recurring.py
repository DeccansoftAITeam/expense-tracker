from datetime import date

import pytest

from app import rules


@pytest.mark.parametrize(
    ("day", "expected"),
    [
        (date(2026, 11, 5), date(2026, 12, 5)),
        (date(2026, 12, 15), date(2027, 1, 15)),
        (date(2026, 1, 31), date(2026, 2, 28)),
        (date(2028, 1, 31), date(2028, 2, 29)),
        (date(2026, 3, 31), date(2026, 4, 30)),
    ],
)
def test_next_month_date_keeps_the_day_or_uses_the_last_day(day, expected):
    assert rules.next_month_date(day) == expected


def _monthly(client, spent_on="2026-01-31"):
    return client.post(
        "/expenses",
        json={"description": "Rent", "amount_paise": 2500000, "spent_on": spent_on, "category": "bills", "repeat": "monthly"},
    ).json()


def test_repeat_defaults_to_none(client):
    body = client.post("/expenses", json={"description": "Tea", "amount_paise": 1500}).json()
    assert body["repeat"] == "none"
    assert body["next_id"] is None


def test_repeat_creates_next_month_copy_and_links_it(client):
    rent = _monthly(client)
    response = client.post(f"/expenses/{rent['id']}/repeat")
    assert response.status_code == 201
    copy = response.json()
    assert copy["spent_on"] == "2026-02-28"
    assert copy["amount_paise"] == 2500000
    assert copy["category"] == "bills"
    assert copy["repeat"] == "monthly"
    listed = {e["id"]: e for e in client.get("/expenses").json()}
    assert listed[rent["id"]]["next_id"] == copy["id"]


def test_an_expense_can_be_repeated_only_once(client):
    rent = _monthly(client)
    client.post(f"/expenses/{rent['id']}/repeat")
    assert client.post(f"/expenses/{rent['id']}/repeat").status_code == 409


def test_one_off_expense_cannot_be_repeated(client):
    tea = client.post("/expenses", json={"description": "Tea", "amount_paise": 1500}).json()
    assert client.post(f"/expenses/{tea['id']}/repeat").status_code == 409


def test_archived_expense_cannot_be_repeated(client):
    rent = _monthly(client)
    client.patch(f"/expenses/{rent['id']}", json={"archived": True})
    assert client.post(f"/expenses/{rent['id']}/repeat").status_code == 409


def test_repeat_unknown_expense_returns_404(client):
    assert client.post("/expenses/999/repeat").status_code == 404


def test_unknown_repeat_value_is_rejected(client):
    response = client.post("/expenses", json={"description": "Gym", "amount_paise": 100, "repeat": "weekly"})
    assert response.status_code == 422


def test_repeat_log_has_ids_only(client, caplog):
    caplog.set_level("INFO", logger="expenses")
    rent = _monthly(client)
    client.post(f"/expenses/{rent['id']}/repeat")
    assert "Rent" not in caplog.text
    assert "2500000" not in caplog.text

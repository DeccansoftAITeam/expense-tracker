import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client():
    main._expenses.clear()
    return TestClient(main.app)


def test_create_expense_returns_201_with_id(client):
    response = client.post(
        "/expenses",
        json={"description": "Lunch", "amount_paise": 25050, "spent_on": "2026-11-05", "category": "food"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["amount_paise"] == 25050
    assert body["archived"] is False


def test_created_at_is_utc_iso_8601(client):
    body = client.post("/expenses", json={"description": "Bus", "amount_paise": 2000}).json()
    assert body["created_at"].endswith("+00:00")


def test_category_defaults_to_other(client):
    body = client.post("/expenses", json={"description": "Gift", "amount_paise": 50000}).json()
    assert body["category"] == "other"


def test_description_is_trimmed(client):
    body = client.post("/expenses", json={"description": "  Tea  ", "amount_paise": 1500}).json()
    assert body["description"] == "Tea"


@pytest.mark.parametrize("description", ["", "   ", "x" * 121])
def test_description_outside_1_to_120_is_rejected(client, description):
    response = client.post("/expenses", json={"description": description, "amount_paise": 100})
    assert response.status_code == 422


def test_description_of_120_is_accepted(client):
    response = client.post("/expenses", json={"description": "x" * 120, "amount_paise": 100})
    assert response.status_code == 201


@pytest.mark.parametrize("amount", [0, -5, 10_000_001, 250.5, "250"])
def test_amount_outside_rules_is_rejected(client, amount):
    response = client.post("/expenses", json={"description": "Bad", "amount_paise": amount})
    assert response.status_code == 422


@pytest.mark.parametrize("amount", [1, 10_000_000])
def test_amount_at_the_limits_is_accepted(client, amount):
    response = client.post("/expenses", json={"description": "Edge", "amount_paise": amount})
    assert response.status_code == 201


def test_unknown_category_is_rejected(client):
    response = client.post("/expenses", json={"description": "Taxi", "amount_paise": 100, "category": "travel"})
    assert response.status_code == 422


def test_list_is_newest_date_first(client):
    client.post("/expenses", json={"description": "Old", "amount_paise": 100, "spent_on": "2026-11-01"})
    client.post("/expenses", json={"description": "New", "amount_paise": 100, "spent_on": "2026-11-03"})
    descriptions = [e["description"] for e in client.get("/expenses").json()]
    assert descriptions == ["New", "Old"]

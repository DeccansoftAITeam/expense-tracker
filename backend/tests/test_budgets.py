import pytest

from app import rules


def test_spent_equal_to_limit_is_not_over_budget():
    assert rules.is_over_budget(50000, 50000) is False


def test_spent_one_paisa_more_than_limit_is_over_budget():
    assert rules.is_over_budget(50001, 50000) is True


def test_category_without_a_limit_is_never_over_budget():
    assert rules.is_over_budget(10_000_000, None) is False


def test_set_budget_and_read_status_for_a_month(client):
    assert client.put("/budgets/food", json={"limit_paise": 50000}).status_code == 200
    client.post(
        "/expenses",
        json={"description": "Groceries", "amount_paise": 50000, "spent_on": "2026-11-10", "category": "food"},
    )
    status = client.get("/budgets", params={"month": "2026-11"}).json()
    assert status == [{"category": "food", "limit_paise": 50000, "spent_paise": 50000, "over": False}]


def test_budget_goes_over_when_spent_is_more_than_limit(client):
    client.put("/budgets/food", json={"limit_paise": 50000})
    client.post(
        "/expenses",
        json={"description": "Groceries", "amount_paise": 50001, "spent_on": "2026-11-10", "category": "food"},
    )
    assert client.get("/budgets", params={"month": "2026-11"}).json()[0]["over"] is True


def test_archived_expense_does_not_count_against_budget(client):
    client.put("/budgets/food", json={"limit_paise": 100})
    expense = client.post(
        "/expenses", json={"description": "Dinner", "amount_paise": 5000, "spent_on": "2026-11-10", "category": "food"}
    ).json()
    client.patch(f"/expenses/{expense['id']}", json={"archived": True})
    assert client.get("/budgets", params={"month": "2026-11"}).json()[0]["spent_paise"] == 0


def test_setting_a_budget_again_replaces_the_limit(client):
    client.put("/budgets/bills", json={"limit_paise": 100})
    client.put("/budgets/bills", json={"limit_paise": 200})
    assert client.get("/budgets", params={"month": "2026-11"}).json()[0]["limit_paise"] == 200


@pytest.mark.parametrize("limit", [0, 10_000_001, 99.5])
def test_budget_limit_outside_rules_is_rejected(client, limit):
    assert client.put("/budgets/food", json={"limit_paise": limit}).status_code == 422


def test_budget_for_unknown_category_is_rejected(client):
    assert client.put("/budgets/travel", json={"limit_paise": 100}).status_code == 422

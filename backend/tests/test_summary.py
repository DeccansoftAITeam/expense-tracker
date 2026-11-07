from datetime import date

import pytest

from app import rules


def _expense(spent_on, amount_paise, category="food", archived=False):
    return {"spent_on": spent_on, "amount_paise": amount_paise, "category": category, "archived": archived}


def test_month_range_of_november_is_1st_to_30th():
    assert rules.month_range("2026-11") == (date(2026, 11, 1), date(2026, 11, 30))


def test_month_range_of_february_in_a_leap_year_ends_on_29th():
    assert rules.month_range("2028-02") == (date(2028, 2, 1), date(2028, 2, 29))


@pytest.mark.parametrize("bad", ["2026-13", "2026-1", "26-11", "november", ""])
def test_month_not_in_yyyy_mm_is_rejected(bad):
    with pytest.raises(ValueError):
        rules.month_range(bad)


def test_summary_includes_first_and_last_day_of_the_month_only():
    expenses = [
        _expense("2026-10-31", 100),
        _expense("2026-11-01", 200),
        _expense("2026-11-30", 300),
        _expense("2026-12-01", 400),
    ]
    assert rules.summarize_month(expenses, "2026-11")["total_paise"] == 500


def test_archived_expense_never_counts_in_summary():
    expenses = [_expense("2026-11-15", 900, archived=True), _expense("2026-11-16", 100)]
    assert rules.summarize_month(expenses, "2026-11")["total_paise"] == 100


def test_summary_groups_totals_by_category_with_zero_for_empty():
    expenses = [_expense("2026-11-02", 250, "food"), _expense("2026-11-03", 750, "food"), _expense("2026-11-04", 4000, "bills")]
    summary = rules.summarize_month(expenses, "2026-11")
    assert summary["by_category"]["food"] == 1000
    assert summary["by_category"]["bills"] == 4000
    assert summary["by_category"]["health"] == 0


def test_summary_endpoint_uses_the_boundaries(client):
    for spent_on, amount in [("2026-10-31", 100), ("2026-11-01", 200), ("2026-11-30", 300), ("2026-12-01", 400)]:
        client.post("/expenses", json={"description": "x", "amount_paise": amount, "spent_on": spent_on})
    archived = client.post("/expenses", json={"description": "y", "amount_paise": 999, "spent_on": "2026-11-15"}).json()
    client.patch(f"/expenses/{archived['id']}", json={"archived": True})
    body = client.get("/expenses/summary", params={"month": "2026-11"}).json()
    assert body["month"] == "2026-11"
    assert body["total_paise"] == 500
    assert body["by_category"]["other"] == 500


def test_summary_endpoint_rejects_a_bad_month(client):
    assert client.get("/expenses/summary", params={"month": "2026-13"}).status_code == 422

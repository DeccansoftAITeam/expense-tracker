import csv
import io

from app import rules


def _rows(response):
    return list(csv.reader(io.StringIO(response.text)))


def test_export_has_header_and_one_row_per_active_expense(client):
    client.post(
        "/expenses", json={"description": "Lunch", "amount_paise": 25050, "spent_on": "2026-11-05", "category": "food"}
    )
    archived = client.post("/expenses", json={"description": "Wrong", "amount_paise": 100}).json()
    client.patch(f"/expenses/{archived['id']}", json={"archived": True})
    response = client.get("/expenses/export.csv")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "expenses.csv" in response.headers["content-disposition"]
    rows = _rows(response)
    assert rows[0] == ["id", "spent_on", "description", "category", "payment_method", "amount_rupees"]
    assert rows[1] == ["1", "2026-11-05", "Lunch", "food", "upi", "250.50"]
    assert len(rows) == 2


def test_export_quotes_descriptions_with_commas(client):
    client.post("/expenses", json={"description": "Milk, bread", "amount_paise": 9000})
    assert _rows(client.get("/expenses/export.csv"))[1][2] == "Milk, bread"


def test_export_neutralises_formula_descriptions(client):
    client.post("/expenses", json={"description": "=HYPERLINK(1)", "amount_paise": 100})
    assert _rows(client.get("/expenses/export.csv"))[1][2] == "'=HYPERLINK(1)"


def test_paise_to_rupee_text_uses_two_decimals():
    assert rules.paise_to_rupee_text(7) == "0.07"
    assert rules.paise_to_rupee_text(10_000_000) == "100000.00"


def test_export_log_has_no_descriptions(client, caplog):
    caplog.set_level("INFO", logger="expenses")
    client.post("/expenses", json={"description": "Private thing", "amount_paise": 100})
    client.get("/expenses/export.csv")
    assert "Private thing" not in caplog.text

def test_filter_by_category_returns_only_that_category(client):
    client.post("/expenses", json={"description": "Lunch", "amount_paise": 100, "category": "food"})
    client.post("/expenses", json={"description": "Bus", "amount_paise": 100, "category": "transport"})
    listed = client.get("/expenses", params={"category": "food"}).json()
    assert [e["description"] for e in listed] == ["Lunch"]


def test_filter_by_unknown_category_is_rejected(client):
    assert client.get("/expenses", params={"category": "travel"}).status_code == 422


def test_no_category_filter_returns_all(client):
    client.post("/expenses", json={"description": "Lunch", "amount_paise": 100, "category": "food"})
    client.post("/expenses", json={"description": "Gift", "amount_paise": 100})
    assert len(client.get("/expenses").json()) == 2

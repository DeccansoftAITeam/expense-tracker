def _add(client, description="Coffee", spent_on="2026-11-05"):
    return client.post(
        "/expenses", json={"description": description, "amount_paise": 12000, "spent_on": spent_on}
    ).json()


def test_archive_hides_expense_from_list(client):
    expense = _add(client)
    response = client.patch(f"/expenses/{expense['id']}", json={"archived": True})
    assert response.status_code == 200
    assert response.json()["archived"] is True
    assert client.get("/expenses").json() == []


def test_archived_expense_is_shown_with_include_archived(client):
    expense = _add(client)
    client.patch(f"/expenses/{expense['id']}", json={"archived": True})
    listed = client.get("/expenses", params={"include_archived": True}).json()
    assert [e["id"] for e in listed] == [expense["id"]]


def test_unarchive_brings_expense_back(client):
    expense = _add(client)
    client.patch(f"/expenses/{expense['id']}", json={"archived": True})
    client.patch(f"/expenses/{expense['id']}", json={"archived": False})
    assert len(client.get("/expenses").json()) == 1


def test_archive_unknown_expense_returns_404(client):
    assert client.patch("/expenses/999", json={"archived": True}).status_code == 404


def test_there_is_no_delete_endpoint(client):
    expense = _add(client)
    assert client.delete(f"/expenses/{expense['id']}").status_code == 405


def test_expenses_survive_a_new_client(client):
    _add(client)
    from fastapi.testclient import TestClient

    from app.main import app

    assert len(TestClient(app).get("/expenses").json()) == 1

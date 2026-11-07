"""Tests for the MCP surface, using an in-memory client and a fake backend."""

import json

import anyio
import httpx
import pytest
from mcp import Client

import server


class FakeBackend:
    """Answers like the Expense Tracker API, and records each request."""

    def __init__(self):
        self.requests = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        path = request.url.path
        if request.method == "POST" and path == "/expenses":
            body = json.loads(request.content)
            if body["amount_paise"] < 1:
                return httpx.Response(422, json={"detail": "amount_paise must be >= 1"})
            return httpx.Response(201, json={"id": 7, **body, "archived": False})
        if path == "/expenses/summary":
            return httpx.Response(
                200, json={"month": "2026-11", "total_paise": 25050, "by_category": {"food": 25050, "bills": 0}}
            )
        if path == "/expenses/9":
            return httpx.Response(404, json={"detail": "expense not found"})
        return httpx.Response(200, json=[])


@pytest.fixture
def backend(monkeypatch):
    fake = FakeBackend()
    monkeypatch.setattr(
        server, "http_client", lambda: httpx.Client(base_url="http://api", transport=httpx.MockTransport(fake.handler))
    )
    return fake


def run(coro_fn):
    return anyio.run(coro_fn)


def test_server_lists_all_tools():
    async def go():
        async with Client(server.mcp) as client:
            return {tool.name for tool in (await client.list_tools()).tools}

    assert run(go) == {"add_expense", "list_expenses", "monthly_summary", "budget_status", "archive_expense"}


def test_amount_paise_is_an_integer_in_the_schema():
    async def go():
        async with Client(server.mcp) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            return tools["add_expense"].input_schema

    schema = run(go)
    assert schema["properties"]["amount_paise"]["type"] == "integer"
    assert "food" in json.dumps(schema["properties"]["category"])


def test_add_expense_posts_to_the_api(backend):
    async def go():
        async with Client(server.mcp) as client:
            return await client.call_tool("add_expense", {"description": "Lunch", "amount_paise": 25050, "category": "food"})

    result = run(go)
    assert result.is_error is False
    assert json.loads(backend.requests[0].content)["amount_paise"] == 25050


def test_api_error_becomes_a_tool_error_and_the_server_keeps_running(backend):
    async def go():
        async with Client(server.mcp) as client:
            bad = await client.call_tool("add_expense", {"description": "Free", "amount_paise": 0})
            good = await client.call_tool("monthly_summary", {"month": "2026-11"})
            return bad, good

    bad, good = run(go)
    assert bad.is_error is True
    assert "422" in bad.content[0].text
    assert good.is_error is False


def test_archive_unknown_expense_is_a_tool_error(backend):
    async def go():
        async with Client(server.mcp) as client:
            return await client.call_tool("archive_expense", {"expense_id": 9})

    assert run(go).is_error is True


def test_summary_resource_shows_rupees(backend):
    async def go():
        async with Client(server.mcp) as client:
            return await client.read_resource("expenses://summary/2026-11")

    text = run(go).contents[0].text
    assert "₹250.50" in text
    assert "bills" not in text  # categories with nothing spent are left out


def test_review_month_prompt_names_the_month():
    async def go():
        async with Client(server.mcp) as client:
            return await client.get_prompt("review_month", {"month": "2026-11"})

    assert "2026-11" in run(go).messages[0].content.text


def test_rupees_uses_integer_maths():
    assert server.rupees(10_000_000) == "₹100,000.00"
    assert server.rupees(7) == "₹0.07"

"""Expense Tracker MCP server.

Gives an AI host (Claude Code, Claude Desktop) tools for the Expense Tracker API.
It calls the backend over HTTP, so the backend's rules (E1-E8) are applied once, in one place.

stdio rule: never print to stdout. stdout carries the JSON-RPC messages; log to stderr.
"""

import json
import logging
import os
import sys
from typing import Literal

import httpx
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("expense-mcp")
logging.getLogger("httpx").setLevel(logging.WARNING)

API_URL = os.environ.get("EXPENSE_API_URL", "http://localhost:8000")

Category = Literal["food", "transport", "bills", "shopping", "health", "other"]
PaymentMethod = Literal["cash", "card", "upi", "netbanking"]

mcp = MCPServer(
    "expenses",
    instructions="Tools for a personal expense tracker. Amounts are integer paise: ₹250.50 is 25050.",
)


def http_client() -> httpx.Client:
    """The HTTP client for the backend. Tests replace this with a fake."""
    return httpx.Client(base_url=API_URL, timeout=10)


def _error_text(response: httpx.Response) -> str:
    """The API's error, without echoing the input back (E8: no descriptions or amounts)."""
    try:
        detail = response.json().get("detail")
    except ValueError:
        return response.reason_phrase
    if isinstance(detail, list):  # FastAPI validation errors
        return "; ".join(f"{'.'.join(str(p) for p in item['loc'][1:])}: {item['msg']}" for item in detail)
    return str(detail)


def _call(method: str, path: str, **kwargs) -> dict | list:
    with http_client() as client:
        response = client.request(method, path, **kwargs)
    if response.status_code >= 400:
        detail = _error_text(response)
        # A ToolError becomes a tool result with isError: true and this message.
        # The server keeps running. (Other exceptions also give isError, but hide the message.)
        raise ToolError(f"Expense API returned {response.status_code}: {detail}")
    return response.json()


def rupees(paise: int) -> str:
    """25050 -> '₹250.50' with integer maths only (E1)."""
    whole, rest = divmod(paise, 100)
    return f"₹{whole:,}.{rest:02d}"


@mcp.tool()
def add_expense(
    description: str,
    amount_paise: int,
    category: Category = "other",
    spent_on: str | None = None,
    payment_method: PaymentMethod = "upi",
) -> dict:
    """Add an expense.

    amount_paise is integer paise: ₹250.50 is 25050 (rule E1). spent_on is YYYY-MM-DD and
    defaults to today. The description must be 1-120 characters.
    """
    body = {
        "description": description,
        "amount_paise": amount_paise,
        "category": category,
        "payment_method": payment_method,
    }
    if spent_on:
        body["spent_on"] = spent_on
    expense = _call("POST", "/expenses", json=body)
    logger.info("added expense %s", expense["id"])  # E8: id only
    return expense


@mcp.tool()
def list_expenses(category: Category | None = None, include_archived: bool = False) -> list[dict]:
    """List expenses, newest first. Optionally only one category, or with archived ones."""
    params = {"include_archived": include_archived}
    if category:
        params["category"] = category
    return _call("GET", "/expenses", params=params)


@mcp.tool()
def monthly_summary(month: str) -> dict:
    """Total spent per category and in all for a month given as YYYY-MM. Archived never count."""
    return _call("GET", "/expenses/summary", params={"month": month})


@mcp.tool()
def budget_status(month: str) -> list[dict]:
    """Each budget for a month (YYYY-MM) with limit, spent and over. Over means more than the limit."""
    return _call("GET", "/budgets", params={"month": month})


@mcp.tool()
def archive_expense(expense_id: int) -> dict:
    """Archive an expense (rule E6: expenses are never deleted). It can be restored later."""
    expense = _call("PATCH", f"/expenses/{expense_id}", json={"archived": True})
    logger.info("archived expense %s", expense_id)
    return expense


@mcp.resource("expenses://summary/{month}")
def summary_resource(month: str) -> str:
    """The monthly summary for YYYY-MM as readable text."""
    summary = _call("GET", "/expenses/summary", params={"month": month})
    lines = [f"Expenses for {summary['month']}: {rupees(summary['total_paise'])}"]
    for category, paise in summary["by_category"].items():
        if paise:
            lines.append(f"- {category}: {rupees(paise)}")
    return "\n".join(lines)


@mcp.resource("expenses://rules")
def rules_resource() -> str:
    """The data rules every client should follow."""
    return json.dumps(
        {
            "amount": "integer paise, 1 to 10,000,000 (₹0.01 to ₹1,00,000)",
            "description": "1-120 characters after trimming",
            "spent_on": "YYYY-MM-DD",
            "categories": ["food", "transport", "bills", "shopping", "health", "other"],
            "delete": "never; archive instead",
        },
        indent=2,
    )


@mcp.prompt()
def review_month(month: str) -> str:
    """A prompt that reviews a month's spending against the budgets."""
    return (
        f"Review my spending for {month}. Call monthly_summary and budget_status for {month}. "
        "Show a table of category, spent, budget and status, with amounts in rupees with 2 decimals. "
        "Then give me the three largest expenses of the month from list_expenses, and one suggestion "
        "for the category that is most over budget. Do not archive or add anything."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")  # local
    # mcp.run(transport="streamable-http", port=8001)  # remote: http://localhost:8001/mcp

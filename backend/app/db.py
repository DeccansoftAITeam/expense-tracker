"""SQLite access. All database code lives here (see .claude/rules/backend.md)."""

import os
import sqlite3
from contextlib import closing
from pathlib import Path

# The app uses backend/expenses.db, or the file in EXPENSES_DB (the e2e tests use their own).
# pytest points DB_PATH at a temporary file.
DB_PATH = Path(os.environ.get("EXPENSES_DB") or Path(__file__).resolve().parent.parent / "expenses.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount_paise INTEGER NOT NULL,
    spent_on TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'other',
    payment_method TEXT NOT NULL DEFAULT 'upi',
    repeat TEXT NOT NULL DEFAULT 'none',
    next_id INTEGER,
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS budgets (
    category TEXT PRIMARY KEY,
    limit_paise INTEGER NOT NULL
);
"""


# Columns added after the first release. An older expenses.db gets them on connect.
ADDED_COLUMNS = {
    "payment_method": "TEXT NOT NULL DEFAULT 'upi'",
    "repeat": "TEXT NOT NULL DEFAULT 'none'",
    "next_id": "INTEGER",
}


def _add_missing_columns(conn: sqlite3.Connection) -> None:
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(expenses)")}
    for name, definition in ADDED_COLUMNS.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE expenses ADD COLUMN {name} {definition}")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _add_missing_columns(conn)
    return conn


def _to_dict(row: sqlite3.Row) -> dict:
    data = dict(row)
    data["archived"] = bool(data["archived"])
    return data


def insert_expense(
    description: str,
    amount_paise: int,
    spent_on: str,
    category: str,
    created_at: str,
    payment_method: str = "upi",
    repeat: str = "none",
) -> dict:
    with closing(connect()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO expenses (description, amount_paise, spent_on, category, payment_method, repeat, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (description, amount_paise, spent_on, category, payment_method, repeat, created_at),
        )
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _to_dict(row)


def get_expense(expense_id: int) -> dict | None:
    with closing(connect()) as conn:
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    return _to_dict(row) if row else None


def list_expenses(include_archived: bool = False, category: str | None = None) -> list[dict]:
    where, params = [], []
    if not include_archived:
        where.append("archived = 0")
    if category:
        where.append("category = ?")
        params.append(category)
    sql = "SELECT * FROM expenses"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY spent_on DESC, id DESC"
    with closing(connect()) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_to_dict(r) for r in rows]


def set_archived(expense_id: int, archived: bool) -> dict | None:
    with closing(connect()) as conn, conn:
        conn.execute("UPDATE expenses SET archived = ? WHERE id = ?", (int(archived), expense_id))
    return get_expense(expense_id)


def expenses_between(first: str, last: str) -> list[dict]:
    """All expenses, archived included, with spent_on from first to last (inclusive)."""
    with closing(connect()) as conn:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE spent_on BETWEEN ? AND ? ORDER BY spent_on", (first, last)
        ).fetchall()
    return [_to_dict(r) for r in rows]


def set_budget(category: str, limit_paise: int) -> dict:
    with closing(connect()) as conn, conn:
        conn.execute(
            "INSERT INTO budgets (category, limit_paise) VALUES (?, ?)"
            " ON CONFLICT(category) DO UPDATE SET limit_paise = excluded.limit_paise",
            (category, limit_paise),
        )
    return {"category": category, "limit_paise": limit_paise}


def list_budgets() -> list[dict]:
    with closing(connect()) as conn:
        rows = conn.execute("SELECT * FROM budgets ORDER BY category").fetchall()
    return [dict(r) for r in rows]


def repeat_expense(expense: dict, next_spent_on: str, created_at: str) -> dict:
    """Insert next month's copy and link it from the original, in one transaction."""
    with closing(connect()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO expenses (description, amount_paise, spent_on, category, payment_method, repeat, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                expense["description"],
                expense["amount_paise"],
                next_spent_on,
                expense["category"],
                expense["payment_method"],
                expense["repeat"],
                created_at,
            ),
        )
        conn.execute("UPDATE expenses SET next_id = ? WHERE id = ?", (cursor.lastrowid, expense["id"]))
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _to_dict(row)

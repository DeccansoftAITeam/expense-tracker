"""SQLite access. All database code lives here (see .claude/rules/backend.md)."""

import sqlite3
from contextlib import closing
from pathlib import Path

# The app uses backend/expenses.db. Tests point DB_PATH at a temporary file.
DB_PATH = Path(__file__).resolve().parent.parent / "expenses.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount_paise INTEGER NOT NULL,
    spent_on TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'other',
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _to_dict(row: sqlite3.Row) -> dict:
    data = dict(row)
    data["archived"] = bool(data["archived"])
    return data


def insert_expense(description: str, amount_paise: int, spent_on: str, category: str, created_at: str) -> dict:
    with closing(connect()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO expenses (description, amount_paise, spent_on, category, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (description, amount_paise, spent_on, category, created_at),
        )
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _to_dict(row)


def get_expense(expense_id: int) -> dict | None:
    with closing(connect()) as conn:
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    return _to_dict(row) if row else None


def list_expenses(include_archived: bool = False) -> list[dict]:
    sql = "SELECT * FROM expenses"
    if not include_archived:
        sql += " WHERE archived = 0"
    sql += " ORDER BY spent_on DESC, id DESC"
    with closing(connect()) as conn:
        rows = conn.execute(sql).fetchall()
    return [_to_dict(r) for r in rows]


def set_archived(expense_id: int, archived: bool) -> dict | None:
    with closing(connect()) as conn, conn:
        conn.execute("UPDATE expenses SET archived = ? WHERE id = ?", (int(archived), expense_id))
    return get_expense(expense_id)

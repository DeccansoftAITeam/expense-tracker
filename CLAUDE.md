@AGENTS.md

# Expense Tracker

A personal expense tracker. Product: @docs/PRD.md. Design and API: @docs/TRD.md.
Backend dependencies: @backend/pyproject.toml.

## Commands

- Backend: `cd backend && uv sync && uv run uvicorn app.main:app --reload` (port 8000)
- Backend tests: `cd backend && uv run pytest -q`
- Frontend: `cd frontend && npm install && npm run dev` (port 5173)
- Frontend build: `cd frontend && npm run build`

## Rules

- E1 Money is integer paise (`amount_paise`), never a float. The UI shows rupees with 2 decimals.
- E2 `spent_on` is `YYYY-MM-DD`. Timestamps (`created_at`) are UTC, ISO 8601.
- E3 A description is 1-120 characters after trimming spaces.
- E4 An amount is 1 to 10,000,000 paise.
- E5 Category is food, transport, bills, shopping, health or other; default other.
- E6 Expenses are archived, never deleted. There is no DELETE endpoint.
- E7 No clock inside `backend/app/rules.py`: pass `today` in as a parameter.
- E8 Never log descriptions or amounts; log the expense id only.

## Conventions

- All database code lives in `backend/app/db.py`; the database file is `backend/expenses.db`.
- Tests never use `backend/expenses.db`; they use a temporary SQLite file (pytest `tmp_path`).
- Frontend is JavaScript (`.jsx`), never TypeScript.

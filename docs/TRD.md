# TRD: Expense Tracker

## Stack

- Backend: Python 3.12, FastAPI, uv, pytest, SQLite, in folder `backend/`.
- Frontend: React + Vite, JavaScript (`.jsx`), in folder `frontend/`.

## Folder layout

```text
expense-tracker/
  docs/PRD.md, docs/TRD.md
  backend/
    pyproject.toml
    app/main.py        FastAPI app and routes
    app/models.py      request and response models (pydantic)
    app/rules.py       pure business rules, no clock, no I/O
    app/db.py          SQLite access, file backend/expenses.db
    tests/test_*.py    pytest
  frontend/
    package.json
    src/App.jsx
    src/api.js         fetch calls to http://localhost:8000
    src/components/    ExpenseForm.jsx, ExpenseList.jsx, ...
```

## Data model

### Expense

| Field | Type | Notes |
|---|---|---|
| id | int | assigned by the database |
| description | str | 1–120 characters after trimming (E3) |
| amount_paise | int | 1 to 10,000,000 (E1, E4) |
| spent_on | date | `YYYY-MM-DD` (E2) |
| category | str | food, transport, bills, shopping, health, other; default other (E5) |
| archived | bool | default false (E6) |
| created_at | str | UTC, ISO 8601, set by the server (E2) |

### Budget

| Field | Type | Notes |
|---|---|---|
| category | str | one of the E5 values, unique |
| limit_paise | int | 1 to 10,000,000 |

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness check: `{"status": "ok"}` |
| POST | `/expenses` | Add an expense |
| GET | `/expenses` | List expenses, newest `spent_on` first. Query: `category`, `include_archived` |
| PATCH | `/expenses/{id}` | Archive or un-archive: `{"archived": true}` |
| GET | `/expenses/summary` | Totals per category for `month=YYYY-MM` |
| PUT | `/budgets/{category}` | Set a monthly limit |
| GET | `/budgets` | Each budget with spent and over for `month=YYYY-MM` |

There is **no DELETE** endpoint (E6).

## Rules, each with one test case

| Rule | Test case |
|---|---|
| E1 Money is integer paise | POST with `"amount_paise": 250.5` → 422 |
| E2 Dates `YYYY-MM-DD`, timestamps UTC ISO 8601 | `created_at` ends with `+00:00` |
| E3 Description 1–120 after trim | `"   "` → 422; 121 characters → 422; 120 → 201 |
| E4 Amount 1 to 10,000,000 paise | 0 → 422; 10,000,001 → 422; 1 → 201 |
| E5 Category values, default other | no category → `other`; `"travel"` → 422 |
| E6 Archive, never delete | `DELETE /expenses/1` → 405 |
| E7 No clock in rules.py | `month_range("2026-11")` gives 2026-11-01 to 2026-11-30 without reading the clock |
| E8 Never log descriptions or amounts | the log line after POST holds the id only |

Boundary cases:

- Summary for `2026-11` with expenses on 2026-10-31, 2026-11-01, 2026-11-30, 2026-12-01 and one archived on 2026-11-15: only 2026-11-01 and 2026-11-30 count.
- Budget 50000 with spent 50000 → not over. Spent 50001 → over.

## Testing approach

- `rules.py` is unit-tested with plain values; `today` is a parameter (E7).
- API tests use FastAPI's `TestClient` and a temporary SQLite file (pytest `tmp_path`), never `backend/expenses.db`.
- Frontend: `npm run build` must pass.

## Run commands

- Backend: `cd backend` → `uv sync` → `uv run uvicorn app.main:app --reload` (port 8000)
- Backend tests: `cd backend` → `uv run pytest -q`
- Frontend: `cd frontend` → `npm install` → `npm run dev` (port 5173)
- Frontend build: `cd frontend` → `npm run build`

ASSUMPTION (decided): backend on port 8000, frontend on port 5173, CORS allows `http://localhost:5173`.

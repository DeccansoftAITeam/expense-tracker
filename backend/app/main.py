import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app import db, rules
from app.models import Category, Expense, ExpenseCreate, ExpenseUpdate, MonthlySummary

logger = logging.getLogger("expenses")

app = FastAPI(title="Expense Tracker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/expenses", status_code=201, response_model=Expense)
def create_expense(data: ExpenseCreate) -> dict:
    now = datetime.now(timezone.utc)
    expense = db.insert_expense(
        description=data.description,
        amount_paise=data.amount_paise,
        spent_on=(data.spent_on or now.date()).isoformat(),
        category=data.category,
        created_at=now.isoformat(),
    )
    logger.info("created expense %s", expense["id"])  # E8: id only
    return expense


@app.get("/expenses", response_model=list[Expense])
def list_expenses(include_archived: bool = False, category: Category | None = None) -> list[dict]:
    return db.list_expenses(include_archived=include_archived, category=category)


def _utc_today():
    return datetime.now(timezone.utc).date()


@app.get("/expenses/summary", response_model=MonthlySummary)
def monthly_summary(month: str | None = Query(default=None, description="YYYY-MM; default this month (UTC)")) -> dict:
    month = month or rules.month_of(_utc_today())
    try:
        first, last = rules.month_range(month)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    expenses = db.expenses_between(first.isoformat(), last.isoformat())
    return rules.summarize_month(expenses, month)


@app.patch("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, data: ExpenseUpdate) -> dict:
    # E6: archive, never delete. There is no DELETE route.
    expense = db.set_archived(expense_id, data.archived)
    if expense is None:
        raise HTTPException(status_code=404, detail="expense not found")
    logger.info("archived=%s expense %s", data.archived, expense_id)
    return expense

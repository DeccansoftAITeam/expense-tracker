import logging
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import Expense, ExpenseCreate

logger = logging.getLogger("expenses")

app = FastAPI(title="Expense Tracker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In memory for now; SQLite arrives in M03.
_expenses: list[Expense] = []


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/expenses", status_code=201, response_model=Expense)
def create_expense(data: ExpenseCreate) -> Expense:
    now = datetime.now(timezone.utc)
    expense = Expense(
        id=len(_expenses) + 1,
        description=data.description,
        amount_paise=data.amount_paise,
        spent_on=data.spent_on or now.date(),
        category=data.category,
        created_at=now.isoformat(),
    )
    _expenses.append(expense)
    logger.info("created expense %s", expense.id)  # E8: id only
    return expense


@app.get("/expenses", response_model=list[Expense])
def list_expenses() -> list[Expense]:
    return sorted(_expenses, key=lambda e: (e.spent_on, e.id), reverse=True)

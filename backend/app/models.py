from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Category = Literal["food", "transport", "bills", "shopping", "health", "other"]
PaymentMethod = Literal["cash", "card", "upi", "netbanking"]
Repeat = Literal["none", "monthly"]

MAX_AMOUNT_PAISE = 10_000_000  # ₹1,00,000 (E4)
MAX_DESCRIPTION = 120  # E3


class ExpenseCreate(BaseModel):
    description: str
    # E1: integer paise only; strict=True rejects 250.5 and "250"
    amount_paise: int = Field(ge=1, le=MAX_AMOUNT_PAISE, strict=True)
    spent_on: date | None = None
    category: Category = "other"
    payment_method: PaymentMethod = "upi"
    repeat: Repeat = "none"

    @field_validator("description")
    @classmethod
    def description_is_1_to_120_after_trim(cls, value: str) -> str:
        value = value.strip()
        if not 1 <= len(value) <= MAX_DESCRIPTION:
            raise ValueError(f"description must be 1-{MAX_DESCRIPTION} characters")
        return value


class Expense(BaseModel):
    id: int
    description: str
    amount_paise: int
    spent_on: date
    category: Category
    payment_method: PaymentMethod = "upi"
    repeat: Repeat = "none"
    next_id: int | None = None  # the copy made by POST /expenses/{id}/repeat
    archived: bool = False
    created_at: str  # UTC, ISO 8601 (E2)


class ExpenseUpdate(BaseModel):
    archived: bool


class MonthlySummary(BaseModel):
    month: str
    total_paise: int
    by_category: dict[str, int]


class BudgetIn(BaseModel):
    limit_paise: int = Field(ge=1, le=MAX_AMOUNT_PAISE, strict=True)


class Budget(BaseModel):
    category: Category
    limit_paise: int


class BudgetStatus(BaseModel):
    category: Category
    limit_paise: int
    spent_paise: int
    over: bool

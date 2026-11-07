"""Pure business rules. No clock, no I/O (E7): callers pass dates in."""

import calendar
import re
from collections.abc import Iterable
from datetime import date

CATEGORIES = ("food", "transport", "bills", "shopping", "health", "other")

_MONTH = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")


def month_range(month: str) -> tuple[date, date]:
    """Return the first and last day of a month given as YYYY-MM."""
    match = _MONTH.match(month)
    if not match:
        raise ValueError("month must be YYYY-MM")
    year, mon = int(match.group(1)), int(match.group(2))
    last_day = calendar.monthrange(year, mon)[1]
    return date(year, mon, 1), date(year, mon, last_day)


def month_of(day: date) -> str:
    """The YYYY-MM month a date belongs to."""
    return f"{day.year:04d}-{day.month:02d}"


def summarize_month(expenses: Iterable[dict], month: str) -> dict:
    """Total paise per category for one month. Archived expenses never count."""
    first, last = month_range(month)
    by_category = {category: 0 for category in CATEGORIES}
    for expense in expenses:
        if expense["archived"]:
            continue
        spent_on = expense["spent_on"]
        if isinstance(spent_on, str):
            spent_on = date.fromisoformat(spent_on)
        if first <= spent_on <= last:
            by_category[expense["category"]] += expense["amount_paise"]
    return {"month": month, "total_paise": sum(by_category.values()), "by_category": by_category}


def is_over_budget(spent_paise: int, limit_paise: int | None) -> bool:
    """Over means more than the limit. Equal is not over. No limit is never over."""
    if limit_paise is None:
        return False
    return spent_paise > limit_paise


def budget_status(summary: dict, budgets: Iterable[dict]) -> list[dict]:
    """Spent and over for each budget, using a month summary from summarize_month."""
    result = []
    for budget in budgets:
        spent = summary["by_category"].get(budget["category"], 0)
        result.append(
            {
                "category": budget["category"],
                "limit_paise": budget["limit_paise"],
                "spent_paise": spent,
                "over": is_over_budget(spent, budget["limit_paise"]),
            }
        )
    return result


def paise_to_rupee_text(paise: int) -> str:
    """25050 -> "250.50", using integer maths only (E1)."""
    sign = "-" if paise < 0 else ""
    rupees, rest = divmod(abs(paise), 100)
    return f"{sign}{rupees}.{rest:02d}"


def csv_safe(text: str) -> str:
    """Stop spreadsheet apps from running a cell as a formula."""
    if text and text[0] in "=+-@":
        return "'" + text
    return text


def next_month_date(day: date) -> date:
    """Same day next month, or the last day of next month when it is shorter.

    2026-01-31 -> 2026-02-28, 2026-12-15 -> 2027-01-15.
    """
    year, month = (day.year + 1, 1) if day.month == 12 else (day.year, day.month + 1)
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day.day, last_day))


def repeat_problem(expense: dict) -> str | None:
    """Why this expense cannot be repeated, or None when it can."""
    if expense["repeat"] != "monthly":
        return "only monthly expenses can be repeated"
    if expense["archived"]:
        return "an archived expense cannot be repeated"
    if expense["next_id"] is not None:
        return "this expense was already repeated"
    return None

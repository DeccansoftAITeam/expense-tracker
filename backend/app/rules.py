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

---
name: add-expense-field
description: Adds a new field to expenses, end to end (model, database, API,
  tests, form and list). Use when asked to add a field, column or property
  to an expense, such as a payment method, a note or a tag.
argument-hint: [field] [rules]
---
# Add an expense field: $ARGUMENTS

1. Restate the field, its type, its allowed values and its default.
2. Write the failing pytest test first in backend/tests/, and run it.
3. Change backend/app/models.py (ExpenseCreate and Expense).
4. Add the column in backend/app/db.py: in SCHEMA and in ADDED_COLUMNS, so an
   existing backend/expenses.db gets it too. Pass it through insert_expense.
5. Pass the field through in backend/app/main.py.
6. Update frontend/src/components/ExpenseForm.jsx and ExpenseList.jsx.
7. Run `cd backend && uv run pytest -q` and `cd frontend && npm run build`.
8. Walk through checklist.md and report each item as OK or problem.

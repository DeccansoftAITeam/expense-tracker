# Checklist for a new expense field

- Money stays integer paise; no floats anywhere (E1)
- Dates stay YYYY-MM-DD; timestamps UTC (E2)
- Nothing is deleted, only archived (E6)
- The new field is not logged if it can hold personal data (E8)
- An old backend/expenses.db still works (column added in ADDED_COLUMNS)
- A test checks the default and a test checks a rejected value

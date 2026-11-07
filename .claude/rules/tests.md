---
paths:
  - "backend/tests/**"
---

- Tests use a temporary SQLite file (pytest `tmp_path`), never backend/expenses.db.
- Use the `client` fixture from tests/conftest.py.

---
paths:
  - "backend/**/*.py"
---

# Backend rules

- Dates are `YYYY-MM-DD`; timestamps are UTC, ISO 8601 (E2).
- New endpoints return the same error shape as the existing ones (FastAPI `detail`).
- Log the expense id only, never the description or the amount (E8).

# CSV export

`GET /expenses/export.csv` downloads every active expense as `expenses.csv`.

- Columns, in this order: `id, spent_on, description, category, payment_method, amount_rupees`.
- Dates are `YYYY-MM-DD` (E2).
- `amount_rupees` is the paise amount as text with 2 decimals, computed with integer maths (E1): 25050 → `250.50`.
- Archived expenses are left out (E6).
- Newest `spent_on` first, like the list.
- A description that starts with `=`, `+`, `-` or `@` gets a leading `'`, so a spreadsheet does not run it as a formula.
- The log line has the number of rows only, never descriptions or amounts (E8).

Example:

```text
id,spent_on,description,category,payment_method,amount_rupees
2,2026-11-06,"Milk, bread",food,cash,90.00
1,2026-11-05,Lunch,food,upi,250.50
```

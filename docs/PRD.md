# PRD: Expense Tracker

## Goal

Help one person see where their money goes each month, and warn them before a category of spending runs past its monthly budget.

## Users

- Individuals in India who record daily spending in rupees (₹).
- One person per installation. No login for now.

## User stories and acceptance criteria

### US1 Add an expense

As a user, I add an expense with a description, an amount, a date and a category.

- The description is 1–120 characters after trimming spaces. Otherwise the expense is rejected with a clear message.
- The amount is from ₹0.01 to ₹1,00,000. Otherwise it is rejected.
- The date defaults to today. Any past date is allowed.
- The category is one of food, transport, bills, shopping, health, other. When none is chosen, it is other.

### US2 List expenses

As a user, I see my expenses, newest date first.

- Each row shows the date, description, category and amount in rupees with 2 decimals (₹250.50).
- Archived expenses are hidden.

### US3 Archive an expense

As a user, I archive an expense I entered by mistake.

- An archived expense is hidden from the list, but can be shown with a "show archived" option.
- Expenses are never deleted.
- Archived expenses never count in summaries or budgets.

### US4 Filter by category

As a user, I pick a category and see only its expenses.

- "All" shows every category.

### US5 Monthly summary

As a user, I choose a month and see the total per category and the grand total.

- A month includes its first and last day, and nothing from the next month.
- Categories with no spending show ₹0.00.

### US6 Monthly budgets

As a user, I set a monthly limit per category, and the app tells me when I go over it.

- Over budget means spent is more than the limit. Spent equal to the limit is not over.
- A category without a limit is never over budget.

### US7 Search

As a user, I type part of a description and the list shows only matching expenses.

- Search ignores upper and lower case.

## Out of scope

Login, more than one user, multiple currencies, bank or UPI sync, receipt upload, a mobile app, notifications.

## Open questions

- Should budgets roll over unspent money to the next month? (Not in the first release.)
- Should the user be able to edit an expense, or only archive and re-add it?

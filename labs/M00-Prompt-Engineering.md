# Lab M00: Prompt engineering — write the PRD and TRD

**Tool:** a Claude chat at claude.ai (no Claude Code yet) · **Your branch:** `my-m00` · **Starts from:** `origin/starter` (an empty project)

## What you build

Two documents that every later lab builds from:

- `docs/PRD.md`: what the Expense Tracker does (product requirements).
- `docs/TRD.md`: how it is built (technical requirements).

You practise the M00 techniques: **role**, **context in tags**, **clear scope**, **output format**, **interview first**, **prompt chain**, and **checking for invented facts**.

## Task 1: Get the course repository and create your branch

You do this clone **once** for the whole course. Your trainer gives you the repository address.

Pick a short folder without spaces, for example `C:\work` on Windows or `~/work` on macOS.

Windows (PowerShell):

```text
cd C:\work
git clone <course-repo-url> expense-tracker
cd expense-tracker
```

macOS (Terminal):

```text
cd ~/work
git clone <course-repo-url> expense-tracker
cd expense-tracker
```

The repository has the trainer's finished branch for every module (`origin/m00-prompt-engineering` to `origin/m12-mcp-build`) and a `starter` branch with an empty project (a README and a `.gitignore`). Every lab starts the same way: a new branch of your own, made from a trainer branch.

```text
git switch -c my-m00 origin/starter
mkdir docs
```

`git branch` now shows `my-m00`. This is where you work in this lab.

## Task 2: Warm-up — vague prompt vs. prompt with context

Open a **new chat** at claude.ai.

Round 1, the vague prompt:

```text
Write a Python function that adds up a list of expenses.
```

**Expected:** something like `sum(e["amount"] for e in expenses)`, probably with floats.

Round 2, open a **new chat** and give the facts:

```text
You are a senior Python developer.

<context>
Amounts are stored as integer paise (₹250.50 is 25050), never floats.
Each expense is a dict with amount_paise, spent_on (YYYY-MM-DD) and archived (bool).
Archived expenses must never be counted.
</context>

Write total_for_month(expenses, month) where month is "YYYY-MM".
Return an int (paise). Then list 4 test cases as a table:
input, expected result, why.
Include: an expense on the last day of the month, one on the first day of the next month,
an archived one, and an empty list.
```

Compare the two answers. Write down in one line: **which fact changed the code the most?**
(Usually: "integer paise" and "archived never counts".)

## Task 3: Write the PRD with an interview

Open a **new chat**. Paste:

```text
You are a product manager. Write a PRD for a personal expense tracker web app.

<context>
Users: individuals in India who want to see where their money goes each month.
One person per installation for now. Currency is INR (₹).
The app is the running example of a training course, so keep it small.
</context>

Features: add an expense (description, amount, date, category); list expenses, newest first;
archive an expense (never delete); categories (food, transport, bills, shopping, health, other);
filter the list by category; a monthly summary with the total per category;
a monthly budget per category with an "over budget" warning; search by description.
Out of scope: login, multiple currencies, bank sync, receipts upload, mobile app.

Output: markdown with Goal, Users, User stories with acceptance criteria,
Out of scope, Open questions. Under 2 pages.

Before writing, ask me up to 5 questions, one at a time, each with your
recommended answer. If something is unknown, list it under Open questions;
don't invent numbers.
```

Answer each question. When the recommended answer is fine, reply `Yes`. Use these answers when they come up:

| If it asks about… | Answer |
|---|---|
| Smallest / largest amount | `From ₹0.01 to ₹1,00,000 per expense.` |
| Description length | `1 to 120 characters after trimming spaces.` |
| Spent exactly the budget | `Equal to the budget is not over. Only more than the budget is over.` |
| Archived expenses in the summary | `Archived expenses never count in summaries or budgets.` |

When the PRD appears, refine it with a follow-up:

```text
Add acceptance criteria for archiving: an archived expense is hidden from the list
but can be shown with a "show archived" option. Keep everything else the same.
```

Now check for invented facts:

```text
List every number or rule in this PRD that I did not give you. Remove or confirm each one.
```

Copy the final PRD into `docs/PRD.md` in VS Code and save.

## Task 4: Write the TRD as the next step of the chain

In the **same chat**, paste:

```text
Now write a TRD for the PRD above.

<stack>
Backend: Python 3.12, FastAPI, uv, pytest, SQLite, in folder backend/
Frontend: React + Vite, JavaScript (.jsx), in folder frontend/
</stack>

<rules>
E1 Money is integer paise (amount_paise), never float
E2 spent_on is YYYY-MM-DD; timestamps are UTC, ISO 8601
E3 Description 1-120 characters, trimmed
E4 Amount 1 to 10,000,000 paise
E5 Category food|transport|bills|shopping|health|other, default other
E6 Archive, never delete (no DELETE endpoint)
E7 No clock in rules.py: pass today in
E8 Never log descriptions or amounts; log the id only
</rules>

Output: folder layout, data model, API table (method, path, purpose),
the rules with one test case each, testing approach, run commands.
Use only the versions above. Mark anything you assume as ASSUMPTION.
```

Check the answer:

1. The API table has `GET /health`, `POST /expenses`, `GET /expenses`, `PATCH /expenses/{id}` and **no DELETE** (E6).
2. Search for **ASSUMPTION** and decide on each one. For example: `Use port 8000 for the backend and 5173 for the frontend.`
3. Ask for the boundary tests:

   ```text
   Show the test cases for the monthly summary of 2026-11 with expenses on
   2026-10-31, 2026-11-01, 2026-11-30, 2026-12-01 and one archived on 2026-11-15,
   with the expected total. Only the 1st and the 30th count.
   ```

4. Ask for the budget boundary: `Show a test case where spent equals the budget. It must not be over.`

Copy the final TRD into `docs/TRD.md` and save.

## Task 5: Commit

```text
git add docs
git commit -m "M00: PRD and TRD for the expense tracker"
```

Your work stays on `my-m00`. You do not need to finish or merge it: the next lab starts from the trainer's `m00-prompt-engineering` branch.

To compare your documents with the trainer's:

```text
git diff my-m00 origin/m00-prompt-engineering --stat
git show origin/m00-prompt-engineering:docs/PRD.md
```

## Done when

- [ ] `docs/PRD.md` has Goal, Users, User stories with acceptance criteria, Out of scope, Open questions.
- [ ] The PRD has no number you did not give or confirm.
- [ ] `docs/TRD.md` has the folder layout, data model, API table without DELETE, rules E1–E8 each with a test case, and run commands.
- [ ] Every ASSUMPTION in the TRD is decided.
- [ ] Both files are committed on `my-m00`.

## If you get stuck

- Claude writes the PRD without asking questions: reply `Stop. Ask me the questions first, one at a time.`
- The TRD uses floats for money: reply `Rule E1: amounts are integer paise. Fix the data model and every example.`
- Compare with the trainer's documents: `git show origin/m00-prompt-engineering:docs/PRD.md` and `git show origin/m00-prompt-engineering:docs/TRD.md`.

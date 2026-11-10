# Lab M04: Plan, implement, verify

**Your branch:** `my-m04` · **Starts from:** `origin/m03-context-memory` (the trainer's finished M03)

## What you build

- `backend/app/rules.py` with `month_range(month)` and `summarize_month(expenses, month)`, **tests first**.
- `GET /expenses/summary?month=YYYY-MM` and a **MonthlySummary** panel in the UI.
- `GET /expenses?category=food` and a **CategoryFilter** dropdown, built from a **plan**.

You practise **plan mode**, editing a plan, **tests first**, a **self-healing loop**, **/goal**, **checkpoints and /rewind**, **branch per task** and **effort per phase**.

## Before you start

Start from the trainer's finished M03 branch, even if your own `my-m03` is not finished. Your `my-m03` branch stays as it is; you can go back to it any time with `git switch my-m03`. Commit what you have on it first (`git add -A`, then `git commit -m "wip"`), so unfinished changes do not come along.

```text
git fetch origin
git switch -c my-m04 origin/m03-context-memory
```

Each feature below gets its own short task branch, made from `my-m04` and merged back into `my-m04`.

## Task 1: Plan the monthly summary

```text
git switch -c my-m04-summary
claude
```

```text
/effort high
```

```text
/plan add a monthly summary: GET /expenses/summary?month=YYYY-MM returns the total
per category and the grand total. Read docs/PRD.md and CLAUDE.md first.
```

Watch Claude read the models, routes and tests. In a second terminal run `git status`: **the working tree is clean**. Plan mode does not edit.

When the plan appears, press **Ctrl+G**. The plan opens in your editor. Add these lines, save and close:

```text
- The month includes its first and last day and nothing of the next month.
- Archived expenses never count (E6).
- month_range and summarize_month go in backend/app/rules.py, with no clock inside (E7).
- Add one test per boundary.
```

Choose **No, keep planning** so Claude updates the plan, then read it again. Do not approve yet: Task 2 uses the plan with a tests-first prompt.

## Task 2: Tests first

Approve the plan with **Yes, manually approve edits**, then type:

```text
/effort medium
```

```text
Implement it tests first.
1. Write the pytest tests first in backend/tests/test_summary.py, one per boundary:
   expenses on 2026-10-31, 2026-11-01, 2026-11-30, 2026-12-01 and one archived on
   2026-11-15; month 2028-02 ends on the 29th; a bad month like 2026-13 is rejected.
   Run them and show me they fail for the right reason.
2. Only then change the code until they pass.
3. Do not edit any test after step 1 without telling me why.
```

**Expected:** the first run fails with "`month_range` is missing" or a 404, **not** a syntax error.

When it asks, commit the failing tests on their own:

```text
Commit the new failing tests with a one-sentence message.
```

Let Claude implement. When the tests pass:

```text
Commit the implementation with a one-sentence message.
```

Then check yourself:

```text
cd backend
uv run pytest -q
git log --oneline -2
```

**Expected:** all tests pass, and two small commits: the tests, then the code.

## Task 3: A self-healing loop, then /goal

Break the rule by hand. In `backend/app/rules.py`, inside `summarize_month`, change:

```text
if first <= spent_on <= last:
```

to

```text
if first <= spent_on < last:
```

Now the last day of the month is left out. Paste:

```text
Run uv run pytest -q in backend/. If any fail, read the failure, fix the cause
in the code, and run again. Stop after 3 attempts and tell me what you learned.
```

Watch it run, read the failure, fix `rules.py` and run again until green. Run `git diff`: only `rules.py` changed, and it is back to how it was.

Now a loop with a judge. Break two things: the same `<` change, and in `backend/app/main.py` remove the `month_range` error handling so a bad month gives a 500. Switch to **Auto** mode with **Shift+Tab**, then:

```text
/goal all tests in backend/tests/test_summary.py pass, no test file is changed, or stop after 10 turns
```

Watch the **/goal active** indicator and the verdict after each turn. When it says the goal is met, type `/goal` to see the turns and tokens it used. Switch back to **Manual**.

## Task 4: Checkpoints and /rewind

```text
Move month_range into a new file backend/app/dates.py and update all callers.
```

Let it edit, then decide you do not like it. Press **Esc** twice, pick that prompt, and choose **Restore code and conversation**. Run `git status`: the files are back, and your prompt is in the input box. Clear it.

Now see what a checkpoint does **not** cover:

```text
Create a file backend/notes.txt using a shell command, and add a docstring to summarize_month in rules.py.
```

Run `/rewind` and restore code to before that prompt. **Expected:** the docstring is gone, but `backend/notes.txt` is **still there**, because a shell command created it. Delete it yourself.

## Task 5: Show the summary in the UI, then merge the task branch

```text
Add frontend/src/components/MonthlySummary.jsx: a month picker (default this month)
and a table with the total per category and the grand total, using GET /expenses/summary.
Format amounts with formatRupees from src/money.js. Show it below the list in App.jsx,
and refresh it after an expense is added or archived. Run npm run build.
```

Check at http://localhost:5173 (backend and frontend running). Then:

```text
/effort low
```

```text
Write a one-line commit message for these changes and commit them.
```

```text
git switch my-m04
git merge --no-ff my-m04-summary -m "Merge my-m04-summary"
```

## Task 6: A planned task — the category filter

```text
git switch -c my-m04-filter
claude --permission-mode plan
```

```text
Goal: let users filter expenses by category (food, transport, bills, shopping, health,
other), with GET /expenses?category=food and a CategoryFilter dropdown in
frontend/src/components. "All" shows every category.
Constraints: no new dependencies; keep all SQL in backend/app/db.py.
Explore first. Then give me a plan that lists files to change, tests to add,
assumptions, and what you will not do.
```

Check the plan names `backend/app/db.py`, `backend/app/main.py`, a test file, and `frontend/src/components/CategoryFilter.jsx`, and that an unknown category gives **422** (E5). Approve with **Yes, manually approve edits**.

When it is done:

```text
cd backend
uv run pytest -q
```

Open http://localhost:5173 and pick **food** in the dropdown: only food expenses show. Commit, then merge:

```text
git switch my-m04
git merge --no-ff my-m04-filter -m "Merge my-m04-filter"
```

## Finish

```text
git add -A
git commit -m "M04: monthly summary and category filter"
```

If git says `nothing to commit`, everything is already committed.

Your work stays on `my-m04`. You do not need to finish or merge it: the next lab starts from the trainer's `m04-plan-implement-verify` branch.

To compare your work with the trainer's:

```text
git diff my-m04 origin/m04-plan-implement-verify --stat
```

## Done when

- [ ] `backend/app/rules.py` has `month_range` and `summarize_month`, and reads no clock (E7).
- [ ] `backend/tests/test_summary.py` tests 31 Oct, 1 Nov, 30 Nov, 1 Dec, an archived expense, February 2028 and a bad month.
- [ ] The test commit came **before** the code commit (`git log --oneline`).
- [ ] `GET /expenses/summary?month=2026-11` and `GET /expenses?category=food` work; `category=travel` gives 422.
- [ ] The UI shows the CategoryFilter and the MonthlySummary panel.
- [ ] You used `/plan`, **Ctrl+G**, a loop with a stop condition, `/goal`, `/rewind` and `/effort`.
- [ ] Both task branches (`my-m04-summary`, `my-m04-filter`) are merged into `my-m04`.

## If you get stuck

- Claude changes a test to make it pass: reply `You changed a test. Restore it and fix the code instead.`
- The summary counts 1 December: the end check must be `<= last`, where `last` is the last day of the month.
- Compare with the trainer's branch: `git diff my-m04 origin/m04-plan-implement-verify --stat`, and open any file with `git show origin/m04-plan-implement-verify:<path>`.

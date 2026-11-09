# Lab M06: Skills — build, compose, test, share

**Your branch:** `my-m06` · **Starts from:** `origin/m05-git-worktrees-review` (the trainer's finished M05)

## What you build

Skills in `.claude/skills/`, and the features they produce:

| Skill | What it does | Produces in this lab |
|---|---|---|
| `add-expense-field` | Adds a field end to end, tests first, with a checklist | `payment_method` (cash, card, upi, netbanking; default upi) |
| `new-component` | Creates a React component and its Vitest test | `AmountBadge.jsx` (highlights ₹5,000 and more) |
| `my-changes` | Summarises the live `git diff` and flags risks | |
| `expense-test-audit` | Runs a script that lists test names, checks naming rules, read-only | |
| `review-expense-change` | A **forked**, read-only review of the branch against E1–E8 | |

## Before you start

Start from the trainer's finished M05 branch, even if your own `my-m05` is not finished. Your `my-m05` branch stays as it is; you can go back to it any time with `git switch my-m05`. Commit what you have on it first (`git add -A`, then `git commit -m "wip"`), so unfinished changes do not come along.

```text
git fetch origin
git switch -c my-m06 origin/m05-git-worktrees-review
```

## Task 1: Your first skill, and where skills live

Windows: `mkdir .claude\skills\hello` · macOS: `mkdir -p .claude/skills/hello`

Create `.claude/skills/hello/SKILL.md`:

```text
---
name: hello
description: Says hello with the project name
---
Say hello and name this project.
```

```text
claude
```

```text
/hello
```

Change the body to `Say hello in Hindi.` and type `/hello` again: no restart needed. Then type `/skills`, filter with `re`, and look at the token cost column. Delete the `hello` folder when you are done.

## Task 2: add-expense-field — a skill with a checklist

Create `.claude/skills/add-expense-field/SKILL.md`:

```text
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
4. Add the column in backend/app/db.py so an existing backend/expenses.db gets it too.
5. Pass the field through in backend/app/main.py.
6. Update frontend/src/components/ExpenseForm.jsx and ExpenseList.jsx.
7. Run cd backend && uv run pytest -q and cd frontend && npm run build.
8. Walk through checklist.md and report each item as OK or problem.
```

Create `checklist.md` next to it:

```text
- Money stays integer paise; no floats anywhere (E1)
- Nothing is deleted, only archived (E6)
- The new field is not logged if it can hold personal data (E8)
- An old backend/expenses.db still works
- A test checks the default and a test checks a rejected value
```

In a **new** session:

```text
/add-expense-field payment_method "one of cash, card, upi, netbanking; default upi"
```

Watch it write the failing test first, then change the model, database, API and both components. Read the checklist report, then check yourself:

```text
cd backend
uv run pytest -q
```

Run the backend and frontend, and add an expense paid by **card** at http://localhost:5173. Restart the backend with your **old** `expenses.db`: the old rows show **upi**.

**Weak vs. strong description.** Change the description to `Helps with expenses`. In a new session ask: `Expenses need a notes field of up to 200 characters. Plan it, don't build it.` The skill is **not** loaded. Put the strong description back, start a new session, and ask the same: this time the skill line appears before Claude starts. Press **Esc**; you will not build notes.

## Task 3: new-component — arguments

Vitest is needed for component tests. Ask:

```text
Add vitest, jsdom and @testing-library/react as dev dependencies in frontend/, an npm test script
("vitest run"), and test settings in vite.config.js (environment jsdom). Add tests for
frontend/src/money.js. Run npm test.
```

Create `.claude/skills/new-component/SKILL.md`:

```text
---
name: new-component
description: Creates a React component with a matching Vitest test
arguments: [name, folder]
argument-hint: [Name] [folder]
disable-model-invocation: true
---
Create frontend/src/$folder/$name.jsx and a matching test
frontend/src/$folder/$name.test.jsx. Follow the style of ExpenseList.jsx.
Format money only with formatRupees from frontend/src/money.js (E1).
Run npm test and npm run build in frontend/ before you finish.
```

```text
/new-component AmountBadge components
```

Then:

```text
AmountBadge takes paise and shows formatRupees(paise). From ₹5,000 (500000 paise) it gets the
class "large" and the title "Large expense". Test 499999 (not large) and 500000 (large).
Use AmountBadge for the amount column in ExpenseList.jsx.
```

Run `cd frontend` then `npm test`, and check the highlighted amounts at http://localhost:5173.

## Task 4: my-changes — live data with !command

Create `.claude/skills/my-changes/SKILL.md`:

```text
---
name: my-changes
description: Summarises uncommitted changes and flags risky edits. Use when the
  user asks what changed or wants a commit message.
allowed-tools: Bash(git diff *)
---
## Current changes
!`git diff HEAD`

## Instructions
Summarise the changes in 2-3 bullets, then list risks: floats for money,
local times instead of UTC, descriptions or amounts in logs, a DELETE route,
missing tests. If the diff is empty, say so.
```

Commit your work so far. Then in `backend/app/main.py`, add this line by hand inside `create_expense`:

```text
logger.info("created expense %s", expense["description"])
```

Ask in plain words: `What did I change?`
**Expected:** Claude loads `my-changes`, shows the summary, and flags the description in the log (E8). Undo it: `git restore backend/app/main.py`.

## Task 5: expense-test-audit — a script and a reference file

```text
Create .claude/skills/expense-test-audit/scripts/list_expense_tests.py that prints every pytest
test function name under a given folder, one per line, as path::name. Use only the standard library.
```

Create `.claude/skills/expense-test-audit/naming-rules.md`:

```text
- Test names say the behaviour, like test_spent_equal_to_limit_is_not_over_budget.
- A name that only says the function, like test_rules or test_summary_1, is a problem.
```

Create `.claude/skills/expense-test-audit/SKILL.md`:

```text
---
name: expense-test-audit
description: Audits backend test names against the naming rules and reports
  badly named tests. Use when asked to check or audit test names.
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/*)
disallowed-tools: Edit Write
---
Run python ${CLAUDE_SKILL_DIR}/scripts/list_expense_tests.py backend/tests
Then check each name against naming-rules.md.
Report a table: test name, OK or problem, a better name when it is a problem.
```

On macOS, if `python` is not found, use `python3` in both places.

```text
/expense-test-audit and rename any badly named test
```

**Expected:** the script runs without a prompt; Claude reports that it cannot edit files in this skill and lists the renames instead. Run `/context`: the script's source is not in context, only its output.

## Task 6: review-expense-change — a forked, read-only review

Create `.claude/skills/review-expense-change/SKILL.md`:

```text
---
name: review-expense-change
description: Reviews the branch's expense changes in a separate, read-only context.
disable-model-invocation: true
context: fork
agent: Explore
background: false
allowed-tools: Bash(git diff *)
---
Diff to review:
!`git diff main...HEAD`

Check rules E1-E8 from CLAUDE.md, each as OK or problem: integer paise,
YYYY-MM-DD and UTC dates, description 1-120, amount 1 to 10,000,000 paise,
category values, no delete, no clock in rules.py, no descriptions or amounts
in logs. Also: every new endpoint has a test. Quote the line for each problem.
```

Commit everything, then add a problem on purpose in `backend/app/main.py`:

```text
logger.info("created expense %s", expense["amount_paise"])
```

Commit it (`git commit -am "temp: log amount"`), then:

```text
/review-expense-change
```

Watch the subagent start. **Expected:** E8 is marked as a problem with the quoted line. Run `/context`: the files the subagent read are not in your context. Undo the temp commit: `git reset --hard HEAD~1`.

## Task 7: Test a skill

In three **fresh** sessions, ask and note whether `add-expense-field` loads:

| Prompt | Should load? |
|---|---|
| `Expenses need a tag field` | Yes |
| `Add a receipt number property to each expense` | Yes |
| `Make the search box ignore extra spaces` | No |

Then type `/skill-doctor` and read the report.

## Finish

```text
git add -A
git commit -m "M06: skills, payment method and AmountBadge"
```

If git says `nothing to commit`, everything is already committed.

Your work stays on `my-m06`. You do not need to finish or merge it: the next lab starts from the trainer's `m06-skills` branch.

To compare your work with the trainer's:

```text
git diff my-m06 origin/m06-skills --stat
```

## Done when

- [ ] `.claude/skills/` has `add-expense-field` (with `checklist.md`), `new-component`, `my-changes`, `expense-test-audit` (with `scripts/` and `naming-rules.md`) and `review-expense-change`.
- [ ] Expenses have `payment_method`, default **upi**; `cheque` gives 422; an old `expenses.db` still works.
- [ ] `AmountBadge.jsx` and `AmountBadge.test.jsx` exist; `npm test` passes; ₹5,000 and more is highlighted.
- [ ] `my-changes` and `review-expense-change` both caught a log line that broke E8.
- [ ] `expense-test-audit` listed renames without editing files.

## If you get stuck

- `/new-component` gets `$name` literally: check the `arguments: [name, folder]` line.
- The old database fails with "no such column payment_method": ask `Add the column on connect when it is missing, with ALTER TABLE in backend/app/db.py.`
- Compare with the trainer's branch: `git diff my-m06 origin/m06-skills --stat`, and open any file with `git show origin/m06-skills:<path>`.

# Lab M08: Orchestration

**Time:** 60 minutes · **Branch:** `m08-orchestration` (from `m07-subagents`)

## What you build

**Recurring monthly expenses**: an expense can have `repeat: "monthly"`, and `POST /expenses/{id}/repeat` adds next month's copy (31 January → 28 February). Built by agents working together:

| Pattern | Agents |
|---|---|
| **Pipeline** | `analyst` → `test-author` → `implementer` → `expense-reviewer` |
| **Fan-out / fan-in** | `correctness-reviewer` + `security-reviewer` in parallel, merged list |
| **Evaluator loop** | `implementer` fixes, `expense-reviewer` reviews, at most 3 rounds |
| **Router** | `router` sends a ticket to `backend`, `frontend`, `qa` or a human |
| **Workflow** | an E8 audit of every file in `backend/app/`, saved as `/audit-e8` |

## Before you start

```text
git switch m07-subagents
git switch -c m08-orchestration
```

Windows: `mkdir docs\requests` · macOS: `mkdir -p docs/requests`

Create `docs/requests/recurring-expenses.md`:

```text
# Request: recurring monthly expenses

Rent, the phone bill and the gym come back every month. Users can mark an expense as repeating
monthly. With one click on that expense, next month's copy appears with the next date.
```

## Task 1: Create the pipeline agents with contracts (8 min)

```text
claude
```

```text
Create three agents in .claude/agents/:
- analyst: tools Read, Grep, Glob; never edits. Returns exactly: SPEC, then the headings Goal, Files,
  Acceptance criteria (numbered), Edge cases, Open questions. Under 300 words.
- test-author: writes only under backend/tests/, uses the client fixture, runs the tests and confirms
  they fail for the right reason. Returns exactly: TESTS WRITTEN, the files, one line per test.
  Returns BLOCKED if the SPEC cannot be tested.
- implementer: edits only backend/app/ and frontend/src/, never edits tests, follows E1-E8, runs
  uv run pytest -q and npm run build. Returns exactly: IMPLEMENTED, files changed, the test result line.
  Returns BLOCKED if a test looks wrong. When fixing findings, fixes only the numbered findings.
Model sonnet for all three.
```

Open each file and check the **Return exactly** line: that is the **contract** the next step relies on. Run only the analyst to see it:

```text
Use the analyst on docs/requests/recurring-expenses.md.
```

**Expected:** a SPEC with the fixed headings.

## Task 2: Run the pipeline (15 min)

```text
Build recurring monthly expenses as a pipeline. Show me each result before the next step.
1) analyst on docs/requests/recurring-expenses.md. If it lists open questions, stop and ask me.
2) test-author with the SPEC text. 3) implementer with the SPEC and the test files.
4) expense-reviewer on git diff main...HEAD. Stop on any BLOCKED.
```

When the analyst lists open questions, answer with these decisions:

```text
- The next date is the old spent_on plus one month. When next month is shorter, use its last day:
  2026-01-31 -> 2026-02-28, 2028-01-31 -> 2028-02-29, 2026-12-15 -> 2027-01-15.
- Put next_month_date(day) in backend/app/rules.py, no clock (E7).
- An expense can be repeated once: store the copy's id in next_id. Repeating again gives 409.
- Only repeat "monthly" expenses can be repeated; "none" or archived gives 409. Unknown id gives 404.
- The copy keeps description, amount, category, payment method and repeat.
- UI: a "Repeats monthly" checkbox in the form, and a "Repeat next month" button on monthly rows.
- Log ids only (E8).
```

Let the pipeline continue. Read each result before the next step starts. At the end, check yourself:

```text
cd backend
uv run pytest -q
```

## Task 3: Fan-out review, then an evaluator loop (12 min)

```text
Create two read-only agents in .claude/agents/: correctness-reviewer (bugs, wrong boundaries such as
month ends and leap years, missing tests) and security-reviewer (rule E8, input validation, SQL built
with string formatting, data exposure). Tools: Read, Grep, Glob, Bash for git diff only.
Each returns findings as file:line, severity, one-line problem, or "none".
```

Commit the feature first (`git add -A` then `git commit -m "Add recurring monthly expenses"`), then:

```text
Run correctness-reviewer and security-reviewer in parallel on git diff main...HEAD.
Each returns findings as file:line, severity, one-line problem.
Merge into one list: remove duplicates, sort high to low, and mark any finding
only one reviewer raised.
```

Type `/tasks` while they run: two agents, side by side. Read the merged list.

Now the fix loop:

```text
Loop at most 3 rounds: implementer fixes only the numbered findings, then expense-reviewer
reviews. Stop on VERDICT: APPROVE, on the same finding twice in a row, or after round 3.
Report how it ended.
```

Watch the rounds. Then check the fixes stayed small:

```text
git diff main...HEAD --stat
```

## Task 4: A router (8 min)

```text
Create a router agent in .claude/agents/router.md: model haiku, tools Read. It replies with exactly
one line: ROUTE: backend, ROUTE: frontend, ROUTE: qa or ROUTE: human.
Also create a qa agent that runs uv run pytest -q, npm test and npm run build and reports failures only.
```

Set a budget so the ticket has something to show (backend running, http://localhost:8000/docs): **PUT /budgets/food** with `{"limit_paise": 50000}`, and add a food expense of ₹600 this month.

```text
Use the router agent on this ticket: "The monthly summary does not warn me when a category is over
its budget. Show 'over budget' next to the category, using GET /budgets." Then hand the ticket text
to the agent it names. On ROUTE: human, stop and tell me. Do not do the work yourself.
```

**Expected:** `ROUTE: frontend`, and the `frontend` agent from M07 changes `MonthlySummary.jsx`. Check http://localhost:5173: **food** shows **over budget**.

Try one more ticket: `"Should budgets roll over unspent money to next month?"` **Expected:** `ROUTE: human`.

## Task 5: A dynamic workflow, saved as a command (10 min)

```text
use a workflow to audit every .py file in backend/app/ for rule E8 (no descriptions or amounts
in logs), and verify each finding before reporting it.
```

At the approval prompt choose **View raw script**, read it, then **Yes, run it**.

```text
/workflows
```

Select the run and press **Enter**. Drill into the audit phase and open one agent's result. When it finishes, press **s** and save it to `.claude/workflows/` as `audit-e8`. In a new session:

```text
/audit-e8
```

## Task 6: End to end (5 min)

Try the feature at http://localhost:5173 (backend and frontend running):

1. Add **Rent**, ₹25,000, **bills**, date the 31st of last month, tick **Repeats monthly**.
2. Click **Repeat next month**. A copy appears dated the last day of this month (or the 31st, when this month has 31 days).
3. The button is gone from the original; the copy has its own button.

```text
Push this branch and open a pull request against main with gh. Body: what, why, how to test,
and the acceptance criteria from the SPEC. Do not merge.
```

## Finish

```text
git add -A
git commit -m "M08: orchestration agents, recurring expenses, over-budget warning"
git switch main
git merge --no-ff m08-orchestration -m "Merge M08"
git switch m08-orchestration
```

## Done when

- [ ] `.claude/agents/` has `analyst`, `test-author`, `implementer`, `correctness-reviewer`, `security-reviewer`, `router` and `qa`, each with a fixed return format.
- [ ] `backend/tests/` tests 31 Jan → 28 Feb, 31 Jan 2028 → 29 Feb, December → January, repeat twice (409), one-off and archived (409).
- [ ] The pipeline stopped for your answers to the open questions.
- [ ] The fan-out gave one merged list; the loop ended with APPROVE or a stated reason.
- [ ] The router sent the budget ticket to `frontend` and the roll-over question to `human`.
- [ ] `/audit-e8` runs as a saved workflow.

## If you get stuck

- The implementer edits a test: remind it `You may not edit backend/tests/. Return BLOCKED and explain.`
- The loop never ends: check the prompt has all three exits (APPROVE, same finding twice, round 3).
- `use a workflow` does nothing: run `claude update`; workflows need a recent version.
- Compare with the reference branch `m08-orchestration` (the saved workflow is not in it: yours is generated in class).

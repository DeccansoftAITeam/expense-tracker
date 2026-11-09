# Lab M07: Subagents

**Your branch:** `my-m07` · **Starts from:** `origin/m06-skills` (the trainer's finished M06)

## What you build

Agents in `.claude/agents/`:

| Agent | Tools | Model | Job |
|---|---|---|---|
| `expense-reviewer` | Read, Grep, Glob, Bash (no Edit/Write) | sonnet | Reviews `git diff main...HEAD` against E1–E8, returns a VERDICT |
| `finder` | Read, Grep, Glob | haiku | "Where is X?" as a table of file and line |
| `test-runner` | Read, Bash | haiku | Runs pytest, npm test and npm run build; reports failures only |
| `backend` | Read, Grep, Glob, Edit, Write, Bash | sonnet | Edits only `backend/` |
| `frontend` | Read, Grep, Glob, Edit, Write, Bash | sonnet | Edits only `frontend/`, `.jsx` only |

And the feature they build: **CSV export**, `GET /expenses/export.csv` and an **Export CSV** button.

## Before you start

Start from the trainer's finished M06 branch, even if your own `my-m06` is not finished. Your `my-m06` branch stays as it is; you can go back to it any time with `git switch my-m06`. Commit what you have on it first (`git add -A`, then `git commit -m "wip"`), so unfinished changes do not come along.

```text
git fetch origin
git switch -c my-m07 origin/m06-skills
```

Windows: `mkdir .claude\agents` · macOS: `mkdir -p .claude/agents`

## Task 1: A read-only reviewer

Create `.claude/agents/expense-reviewer.md`:

```text
---
name: expense-reviewer
description: Reviews the branch diff against the expense rules E1-E8 and for missing tests,
  and returns a verdict. Use after implementation, before a pull request.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit, NotebookEdit
model: sonnet
maxTurns: 15
---
You never change files. Use Bash only for git diff, git log, git status and the tests.
Review git diff main...HEAD against the rules in CLAUDE.md (E1-E8): integer paise, YYYY-MM-DD
and UTC dates, description 1-120, amount 1 to 10,000,000 paise, category values, archive not
delete, no clock in rules.py, no descriptions or amounts in logs. Check that every new endpoint
has a test in backend/tests/.
Return exactly:
VERDICT: APPROVE or CHANGES
FINDINGS
1. [high|medium|low] path:line - what is wrong - what to do   ("none" if approving)
Approve only when there are no high or medium findings.
```

```text
claude
```

```text
Which subagents can you use?
```

**Expected:** `expense-reviewer` is in the list. Commit the file, then:

```text
Use the expense-reviewer subagent to review my branch.
```

Read the **VERDICT** line.

## Task 2: A cheap searcher, and what a subagent sees

```text
Create a subagent in .claude/agents/finder.md that finds where something is defined or used.
Tools Read, Grep, Glob only. Model haiku. maxTurns 8. Search backend/ and frontend/src/.
Return a table: file, line, note. Never edit. Under 150 words.
```

Open the file and check the frontmatter. Then:

```text
@agent-finder where is the over-budget rule computed?
```

Type `/tasks` while it runs and check the model shown is **haiku**.

Now see what a subagent does **not** see. In the main session say:

```text
For the CSV export, amounts must be rupee text with 2 decimals, like 250.50.
```

```text
@agent-finder what amount format should the CSV export use?
```

**Expected:** it cannot answer; that rule was only in your conversation. Add this line to the Conventions in `CLAUDE.md`, start a new session, and ask again:

```text
- The CSV export uses dates in YYYY-MM-DD and amounts as rupee text with 2 decimals (see docs/csv-export.md).
```

## Task 3: The built-in Explore agent and a fork

```text
Use the Explore subagent to map how an expense moves from POST /expenses to the database in backend/. Be very thorough.
```

Type `/tasks` to watch it. Afterwards, `/context`: the files it read are **not** in your context, only its summary.

Now agree the export with Claude for a few turns, for example:

```text
For the CSV export: which columns, in which order? I want id, spent_on, description, category, payment_method, amount_rupees.
```

```text
Archived expenses are left out. Descriptions starting with = + - or @ get a leading ' so spreadsheets don't run them.
```

Then start a fork that inherits the conversation:

```text
/subtask write docs/csv-export.md describing the export exactly as we agreed, with an example file.
```

Keep working. When it finishes, open `docs/csv-export.md`: it knew the decisions without being told again.

## Task 4: Delegate the backend work to a role agent

```text
Create .claude/agents/backend.md: edits only files under backend/, writes the pytest test first,
SQL only in backend/app/db.py, runs uv run pytest -q before it finishes, returns files changed and
the test result. Tools Read, Grep, Glob, Edit, Write, Bash. Model sonnet.
```

Then delegate:

```text
Use the backend agent: add GET /expenses/export.csv as described in docs/csv-export.md.
Content-Type text/csv, file name expenses.csv. Convert paise to rupee text in backend/app/rules.py
with integer maths only. Log the row count only. Tests in backend/tests/test_export_csv.py,
including a description with a comma and one starting with =.
```

When the summary comes back, **check its claim** yourself:

```text
cd backend
uv run pytest -q
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000/expenses/export.csv. The file downloads.

## Task 5: A test-runner in the background

```text
Create .claude/agents/test-runner.md: runs cd backend && uv run pytest -q, cd frontend && npm test
and cd frontend && npm run build, never edits, returns one line per command: PASS, or FAIL with the
failing test names. Tools Read, Bash. Model haiku.
```

Also create the frontend role agent:

```text
Create .claude/agents/frontend.md: edits only files under frontend/, .jsx never TypeScript,
follows frontend/src/components/, formats money with formatRupees, runs npm test and
npm run build before it finishes. Tools Read, Grep, Glob, Edit, Write, Bash. Model sonnet.
```

```text
Run the test-runner subagent in the background.
```

While it runs:

```text
Use the frontend agent to add an "Export CSV" link next to the filters in App.jsx that downloads
http://localhost:8000/expenses/export.csv. Put the URL in src/api.js.
```

Type `/tasks` to see the test-runner. Read its result when the notification arrives. Click **Export CSV** at http://localhost:5173 and open the file.

## Task 6: The reviewer catches a broken rule

Commit the CSV export:

```text
git add -A
git commit -m "Add CSV export with an Export button"
```

Add a line on purpose in `backend/app/main.py`, inside the export loop, and commit it (the reviewer reads committed changes only, `git diff main...HEAD`):

```text
logger.info("exported %s", e["description"])
```

```text
git commit -am "temp: log description"
```

```text
@agent-expense-reviewer review this branch.
```

**Expected:** `VERDICT: CHANGES` with a **high** finding for E8 (descriptions in logs). Undo the temporary commit (`git reset --hard HEAD~1`) and ask again: `VERDICT: APPROVE`.

## Finish

```text
git add -A
git commit -m "M07: subagents and CSV export"
```

If git says `nothing to commit`, everything is already committed.

Your work stays on `my-m07`. You do not need to finish or merge it: the next lab starts from the trainer's `m07-subagents` branch.

To compare your work with the trainer's:

```text
git diff my-m07 origin/m07-subagents --stat
```

## Done when

- [ ] `.claude/agents/` has `expense-reviewer`, `finder`, `test-runner`, `backend` and `frontend`.
- [ ] `@agent-finder` ran on **haiku** and could not see a rule that was only in the chat.
- [ ] `docs/csv-export.md` was written by a `/subtask` fork.
- [ ] `GET /expenses/export.csv` returns the header and one row per active expense, amounts like `250.50`; tests pass.
- [ ] The Export CSV button downloads the file.
- [ ] `expense-reviewer` returned CHANGES for the planted log line and APPROVE without it.

## If you get stuck

- The agent is not listed: the file must be in `.claude/agents/` and start with `---` frontmatter. Start a new session.
- The backend agent edits `frontend/`: tighten its body with `Edit only files under backend/. If the task needs a frontend change, stop and say so.`
- Compare with the trainer's branch: `git diff my-m07 origin/m07-subagents --stat`, and open any file with `git show origin/m07-subagents:<path>`.

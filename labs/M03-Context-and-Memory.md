# Lab M03: Context and memory

**Time:** 60 minutes · **Branch:** `m03-context-memory` (from `m02-first-session`)

## What you build

- `CLAUDE.md` with the commands and rules **E1–E8**, importing `AGENTS.md`, the PRD and the TRD.
- `AGENTS.md` in the root, in `backend/` and in `frontend/`; `backend/tests/CLAUDE.md`.
- Path rules `.claude/rules/backend.md` and `.claude/rules/tests.md`.
- **SQLite storage** in `backend/app/db.py` (file `backend/expenses.db`).
- `PATCH /expenses/{id}` to **archive** (never delete), with an Archive button and a "Show archived" box.

## Before you start

```text
git switch m02-first-session
git switch -c m03-context-memory
```

## Task 1: Create CLAUDE.md with /init and add the rules (10 min)

```text
claude
```

```text
/init
```

Open the generated `CLAUDE.md`. Delete lines that only repeat what the code already shows, such as "uses FastAPI". Then:

```text
Add a Rules section to CLAUDE.md with exactly these lines:
- E1 Money is integer paise (amount_paise), never a float. The UI shows rupees with 2 decimals.
- E2 spent_on is YYYY-MM-DD. Timestamps (created_at) are UTC, ISO 8601.
- E3 A description is 1-120 characters after trimming spaces.
- E4 An amount is 1 to 10,000,000 paise.
- E5 Category is food, transport, bills, shopping, health or other; default other.
- E6 Expenses are archived, never deleted. There is no DELETE endpoint.
- E7 No clock inside backend/app/rules.py: pass today in as a parameter.
- E8 Never log descriptions or amounts; log the expense id only.
```

Run `/init` again. **Expected:** it suggests improvements to the existing file instead of replacing it.

Exit with `/exit`, start `claude` again and ask:

```text
How should I store an expense of ₹99.90 and the time it was created?
```

**Expected:** `9990` paise and a UTC ISO 8601 timestamp, taken from your rules.

## Task 2: Look at what loads with /memory and /context (5 min)

```text
/memory
```

**Expected:** user, project and local locations, including files that do not exist yet.

Add imports to the top of `CLAUDE.md` (in VS Code):

```text
Product: @docs/PRD.md. Design and API: @docs/TRD.md. Backend dependencies: @backend/pyproject.toml.
```

Start a new session and run `/context`. **Expected:** the imported files appear with `CLAUDE.md` under **Memory files**. Ask:

```text
Which endpoints does the TRD list that we have not built yet?
```

**Expected:** PATCH, summary and budgets, answered from the imported TRD.

## Task 3: AGENTS.md in more than one folder (8 min)

Create `AGENTS.md` in the project root with:

```text
- Run backend tests with: cd backend && uv run pytest -q
- Build the frontend with: cd frontend && npm run build
```

Add `@AGENTS.md` as the **first line** of `CLAUDE.md`. Start `claude` and run `/context`: both files load.

Create `backend/AGENTS.md`:

```text
- A description is 1-120 characters after trimming spaces (E3).
- Routes are in app/main.py, models in app/models.py, SQL only in app/db.py.
```

and `frontend/AGENTS.md`:

```text
- Components are function components with hooks.
- All fetch calls go through src/api.js.
```

Start `claude` in the root and run `/context`: only the root `AGENTS.md` is listed. Then:

```text
Open backend/app/main.py and explain the POST /expenses route.
```

Run `/context` again. **Expected:** `backend/AGENTS.md` is now listed. Files in sub-folders load only when Claude works there.

## Task 4: Store expenses in SQLite, with a path rule (12 min)

Create `.claude/rules/backend.md`:

```text
---
paths:
  - "backend/**/*.py"
---

# Backend rules
- Dates are YYYY-MM-DD; timestamps are UTC, ISO 8601 (E2).
- Log the expense id only, never the description or the amount (E8).
```

Start a new session and run `/context`: the rule is **not** listed yet. Then:

```text
Store expenses in SQLite instead of memory. Put all database code in backend/app/db.py
and use the file backend/expenses.db. Keep created_at as UTC ISO 8601.
Update the tests so they use a temporary SQLite file with pytest tmp_path.
Run uv run pytest -q.
```

Run `/context`. **Expected:** the backend rule is loaded now.

Check persistence yourself:

```text
cd backend
uv run pytest -q
uv run uvicorn app.main:app --reload
```

Add an expense at http://localhost:8000/docs, stop the server (**Ctrl+C**), start it again, and **GET /expenses**. **Expected:** the expense is still there. `git status` must **not** show `backend/expenses.db`.

## Task 5: Archive, never delete — rules a reviewer can check (10 min)

Create `.claude/rules/tests.md`:

```text
---
paths:
  - "backend/tests/**"
---

- Tests use a temporary SQLite file (pytest tmp_path), never backend/expenses.db.
```

Create `backend/tests/CLAUDE.md` with one line:

```text
- Each test name says the rule it checks, for example test_description_longer_than_120_is_rejected.
```

Now build archive:

```text
Add PATCH /expenses/{id} so an expense can be archived or restored with {"archived": true|false}.
GET /expenses hides archived expenses unless include_archived=true.
Return 404 for an unknown id. Add tests in backend/tests/test_archive.py, including one
that DELETE /expenses/{id} returns 405. Then add an Archive/Restore button to each row in
ExpenseList.jsx and a "Show archived" checkbox in App.jsx.
```

Read the diff:

- There is **no DELETE** route (E6).
- Every new log line uses the **id**, not the description (E8).
- The new test names say the rule they check.

Run `/context`: `backend/tests/CLAUDE.md` and the tests rule are listed.
Run `cd backend` then `uv run pytest -q`, and try the button at http://localhost:5173.

## Task 6: Auto memory (5 min)

```text
Remember that I prefer short answers without a summary at the end.
```

```text
Remember that we use the SQLite file backend/expenses.db; it is created on first run.
```

Watch for the **Saved memories** message. Run `/memory` and open the auto memory folder: `MEMORY.md` lists the new notes.

Exit, start `claude` and ask: `Where are the expenses stored?` **Expected:** it names `backend/expenses.db` and has no closing summary.

Team rules belong in `CLAUDE.md`, not in your personal memory:

```text
Add this to CLAUDE.md: tests never use backend/expenses.db; they use a temporary SQLite file.
```

## Task 7: What survives /compact, and a quick audit (10 min)

```text
From now on, always answer in British English.
```

Ask `What colour should the over-budget warning be?` and see British spelling. Run `/compact` and ask another question: the chat-only rule may be gone.

Add `- Always answer in British English.` to `CLAUDE.md`, run `/compact` again, and ask once more. **Expected:** the rule holds, because the file is read from disk again. Remove the line afterwards.

Add two conflicting lines and a missing path to `CLAUDE.md`:

```text
- Always add a comment above every function.
- Avoid comments; code should explain itself.
- Shared helpers live in backend/app/utils/helpers.py
```

```text
/doctor prompt-audit
```

**Expected:** it flags the conflict and the missing file, and proposes edits. Remove the three lines.

## Finish

```text
git add -A
git commit -m "M03: CLAUDE.md rules, AGENTS.md, SQLite and archive"
git switch main
git merge --no-ff m03-context-memory -m "Merge M03"
git switch m03-context-memory
```

## Done when

- [ ] `CLAUDE.md` starts with `@AGENTS.md`, imports the PRD and TRD, and lists E1–E8.
- [ ] `AGENTS.md` exists in the root, `backend/` and `frontend/`; `/context` shows the sub-folder files only after Claude works there.
- [ ] `.claude/rules/backend.md` and `.claude/rules/tests.md` load only when matching files are used.
- [ ] Expenses survive a backend restart; `backend/expenses.db` is not in `git status`.
- [ ] `PATCH /expenses/{id}` archives and restores; `DELETE` returns 405; tests pass.
- [ ] The UI has Archive/Restore buttons and a "Show archived" box.
- [ ] The work is committed and merged into `main`.

## If you get stuck

- The rule file never loads: check that `paths:` is the only frontmatter field and the glob is relative to the project root.
- Tests create `backend/expenses.db`: ask `Make every test use the client fixture in tests/conftest.py with a tmp_path database.`
- Compare with the reference branch `m03-context-memory`.

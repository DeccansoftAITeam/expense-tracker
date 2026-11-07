# Lab M01: How Claude Code works

**Time:** 55 minutes · **Branch:** `m01-how-claude-code-works` (from `m00-prompt-engineering`)

## What you build

- `backend/` with `GET /health` and one pytest test.
- `frontend/`: a Vite + React shell that shows the heading **Expense Tracker**.

On the way you watch the **agent loop** (gather → act → verify), the **tools**, what Claude **can see**, **sessions**, the **context window**, **background sessions**, **models**, **effort** and **usage**.

## Before you start

Claude Code must be installed and signed in (`claude --version` works). If not, do Task 1 of Lab M02 first and come back.

```text
cd C:\work\expense-tracker        (Windows)
cd ~/work/expense-tracker         (macOS)
git switch m00-prompt-engineering
git switch -c m01-how-claude-code-works
```

## Task 1: Watch the agent loop (10 min)

Start Claude Code in the project folder:

```text
claude
```

Gather only:

```text
Read docs/PRD.md and docs/TRD.md and list the features in five bullets. Don't change anything.
```

**Expected:** two **Read** tool calls, then five bullets. Nothing is written.

Now gather, act and verify:

```text
Create the backend in backend/ as described in docs/TRD.md, with only GET /health
returning {"status": "ok"} and one pytest test for it. Use uv. Then run the tests.
```

While it works, steer it. Type this and press Enter:

```text
Put the test in backend/tests/test_health.py
```

Press **Esc** once. The current step stops. Then type `continue` to let it finish.

Check it yourself in a second terminal:

```text
cd backend
uv run pytest -q
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000/health. **Expected:** `{"status":"ok"}`. Stop the server with **Ctrl+C**.

## Task 2: See the tools (5 min)

In the Claude session, type each prompt and look at the tool name in the transcript:

| Prompt | Tool you should see |
|---|---|
| `Find every file that mentions health.` | Search (Grep/Glob) |
| `Run uv run pytest -q in backend/ and tell me how many tests pass.` | Bash |
| `Fetch the FastAPI docs page about testing and summarise it in three lines.` | Web fetch |

You may get an approval prompt. Choose **Yes** for now; permissions come in M09.

## Task 3: What Claude can see (5 min)

Exit with `/exit`. Then start Claude inside `backend/`:

```text
cd backend
claude
```

```text
What does ../docs/TRD.md say about the API?
```

**Expected:** it asks for permission, or says the folder is outside its working directory. Now add the folder:

```text
/add-dir ../docs
```

Ask the same question again. Now it answers from the TRD. Exit and go back to the project root (`cd ..`).

## Task 4: Sessions and context (10 min)

Sessions are independent:

```text
claude
```

```text
For this chat: our API returns amounts as rupee strings like "250.50".
```

```text
/rename money-format
```

Exit with `/exit`, start `claude` again and ask: `How does our API return amounts?`
**Expected:** it does not know, or it reads the TRD and says integer paise (E1).

Exit, then resume the named session:

```text
claude --resume
```

Pick `money-format` and ask again. Now it remembers the chat-only statement. (It was wrong on purpose: the TRD wins. Sessions only remember what was said in them.)

Look at the context window in the same session:

```text
/context
```

```text
Read docs/PRD.md and docs/TRD.md and make a table of every requirement with its user story.
```

```text
/context
```

The **files** part has grown. Now compact and look again:

```text
/compact focus on the API endpoints
```

```text
/context
```

**Expected:** usage drops. Exit the session.

## Task 5: Build the frontend in a background session (10 min)

From the project root:

```text
claude --bg "Create frontend/ with Vite and React (.jsx, no TypeScript) as described in docs/TRD.md. The page shows the heading Expense Tracker and nothing else. Run npm install and npm run build."
```

List background sessions:

```text
claude agents
```

Select the frontend session, press **Space** to peek, then **Enter** to attach. Type:

```text
Also set the page title in index.html to Expense Tracker.
```

Press **←** on the empty prompt to detach. When the session shows as done, try it:

```text
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. **Expected:** the heading **Expense Tracker**. Stop it with **Ctrl+C**.

## Task 6: One-shot mode, models and effort (8 min)

One-shot (print) mode is what scripts and CI use:

```text
claude -p "explain what this repo does in three lines"
```

Start `claude` and try models and effort:

```text
/model
```

Pick **Sonnet**, then:

```text
Rename the health function in backend/app/main.py to health_check and keep the test passing.
```

```text
/effort low
```

```text
Format backend/app/main.py.
```

```text
/effort high
```

```text
Read docs/TRD.md and list any requirement that is unclear or contradicts the PRD. Don't change anything.
```

**Expected:** low effort answers quickly; high effort thinks longer before answering.

## Task 7: Read your usage (2 min)

```text
/usage
```

Press **d** and **w** to switch between the last day and the last week. Exit with `/exit`.

## Finish

```text
git add -A
git commit -m "M01: backend health check and frontend shell"
git switch main
git merge --no-ff m01-how-claude-code-works -m "Merge M01"
git switch m01-how-claude-code-works
```

## Done when

- [ ] `cd backend` then `uv run pytest -q` shows **1 passed**.
- [ ] http://localhost:8000/health returns `{"status":"ok"}`.
- [ ] http://localhost:5173 shows **Expense Tracker**.
- [ ] You saw Read, Search, Bash and Web tool calls in the transcript.
- [ ] You used `/add-dir`, `/rename`, `claude --resume`, `/context`, `/compact`, `claude --bg`, `claude agents`, `claude -p`, `/model`, `/effort` and `/usage`.
- [ ] `node_modules/` and `.venv/` are **not** in `git status` (the `.gitignore` from M00 covers them).
- [ ] The work is committed and merged into `main`.

## If you get stuck

- `uv: command not found`: install uv (see `labs/README.md`) and open a new terminal.
- `claude --bg` or `claude agents` is not recognised: run `claude update` and try again.
- The frontend shows the Vite demo page: ask `Remove the Vite demo content. App.jsx shows only the heading Expense Tracker.`
- Compare with the reference branch `m01-how-claude-code-works`.

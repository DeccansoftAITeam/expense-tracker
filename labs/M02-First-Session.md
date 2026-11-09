# Lab M02: Install, sign in, first session

**Your branch:** `my-m02` · **Starts from:** `origin/m01-how-claude-code-works` (the trainer's finished M01)

## What you build

The first real feature: **add and list expenses**, kept in memory.

- `POST /expenses` and `GET /expenses` in `backend/app/main.py`, with validation from rules E1, E3, E4, E5.
- `frontend/src/components/ExpenseForm.jsx` and `ExpenseList.jsx`, using `frontend/src/api.js`.

On the way you practise **install and sign-in checks**, **permission modes**, **prompt forms** (`@file`, selection, screenshot), **steering**, **reading tool calls**, **approval prompts**, **commands** and **resume**.

## Before you start

Start from the trainer's finished M01 branch, even if your own `my-m01` is not finished. Your `my-m01` branch stays as it is; you can go back to it any time with `git switch my-m01`. Commit what you have on it first (`git add -A`, then `git commit -m "wip"`), so unfinished changes do not come along.

```text
git fetch origin
git switch -c my-m02 origin/m01-how-claude-code-works
```

## Task 1: Check the install and sign-in

Install Claude Code if you have not (skip if `claude --version` already works):

Windows (PowerShell):

```text
irm https://claude.ai/install.ps1 | iex
```

macOS (Terminal):

```text
curl -fsSL https://claude.ai/install.sh | bash
```

Close the terminal, open a new one, then:

```text
claude --version
claude doctor
```

Windows only: `git --version` must work. If not, install Git for Windows and open a new terminal.

Start Claude in the project folder and check your account:

```text
claude
```

```text
/status
```

**Expected:** the account line names your organisation and seat, not "API key".

## Task 2: VS Code and the first prompt

1. Open the project in VS Code: `code .`
2. Install the **Claude Code** extension from the Extensions view.
3. Open the terminal (**Ctrl+`**), run `claude`, and accept the trust prompt.

```text
Explain how this project is organised. Do not change anything.
```

**Expected:** it mentions `docs/PRD.md`, `docs/TRD.md`, the FastAPI backend with `GET /health`, and the React frontend.

## Task 3: Permission modes

Look at the bottom line of the session: it shows the current mode. Press **Shift+Tab** until it shows **Manual**.

```text
Run uv run pytest -q in backend/.
```

**Expected:** an approval prompt. Choose **Yes**. Press **Shift+Tab** a few times to see **Accept edits** and **Plan**, then go back to **Manual**.

## Task 4: Build the API and steer while it works

Use `@` to point at a file. Type the path and watch the suggestions:

```text
Using @docs/PRD.md, list the user stories of the first release in five bullet points.
```

Now build the API:

```text
Read @docs/TRD.md. Add POST /expenses and GET /expenses to backend/app/main.py,
keeping expenses in an in-memory list. Put the request and response models in
backend/app/models.py. Amounts are integer paise (amount_paise), category defaults
to other, created_at is UTC ISO 8601. GET returns newest spent_on first.
Add pytest tests in backend/tests/test_expenses.py and run uv run pytest -q.
```

While it works, type this correction and press Enter:

```text
descriptions must be 1 to 120 characters after trimming, and amounts 1 to 10,000,000 paise; return 422 otherwise
```

**Expected:** it picks up the correction and adds tests for both limits.

Start another task, for example `Add a docstring to every route.`, and press **Esc** after the first tool call. It stops at once. Press **Esc** twice on the empty prompt to see the rewind menu, then close it.

Try the API in a second terminal:

```text
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000/docs. Use **POST /expenses** with:

```json
{"description": "Lunch", "amount_paise": 25050, "category": "food"}
```

Then **GET /expenses**. **Expected:** the lunch is listed with `"category": "food"` and an id.
Try `"amount_paise": 250.5`. **Expected:** 422 (E1).

## Task 5: Build the UI and read every tool call

Stay in **Manual** mode.

```text
Create frontend/src/components/ExpenseForm.jsx with inputs for description,
amount in rupees, date (default today) and a category dropdown, and an Add button.
Create frontend/src/components/ExpenseList.jsx that shows date, description, category
and amount as rupees with 2 decimals. Convert rupees to integer paise without floats,
in frontend/src/money.js. Call POST /expenses and GET /expenses on http://localhost:8000
from frontend/src/api.js, and use both components in App.jsx.
Enable CORS for http://localhost:5173 in the backend.
```

Read each tool call before you approve it: **Read**, then **Write** with a green diff for each new file, then **Edit** for `App.jsx` and `main.py`.

Start the frontend in a third terminal (keep the backend running):

```text
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Add **Lunch, 250.50, food** and **Metro card, 500, transport**. Both appear, newest first, as **₹250.50** and **₹500.00**.

Use a selection and a screenshot as prompts:

1. In VS Code open `frontend/src/App.jsx`, select the `<h1>` line, press **Alt+K**, and type: `Why does this heading not show the total spent?`
2. Take a screenshot of http://localhost:5173, drag it into the prompt and ask: `What is wrong with the layout of this page?`

## Task 6: Approval prompts and settings.local.json

```text
Run uv run pytest -q in backend/.
```

Choose **Yes, and don't ask again**. Open `.claude/settings.local.json`. **Expected:** a new allow rule for the test command.

```text
Delete the backend/tests folder.
```

Choose **No**, press **Tab**, type `don't delete anything, just list the files`, and press Enter. Claude lists the files instead.

## Task 7: Commands, continue and resume

Type `/` then `st`: the list filters to `/status`. Run `/help`, then `/doctor`.

Type `please run /status` as a sentence. It is sent as text, not run as a command.

```text
List the endpoints in backend/app/main.py and what each returns.
```

```text
/rename expense-api-exploration
```

Exit with `/exit`, then in the shell:

```text
claude -r "expense-api-exploration"
```

The conversation is back. Exit again and run `claude -c`: the latest conversation opens. Finally:

```text
claude update
```

## Finish

```text
git add -A
git commit -m "M02: add and list expenses (in memory)"
```

If git says `nothing to commit`, everything is already committed.

Your work stays on `my-m02`. You do not need to finish or merge it: the next lab starts from the trainer's `m02-first-session` branch.

To compare your work with the trainer's:

```text
git diff my-m02 origin/m02-first-session --stat
```

## Done when

- [ ] `uv run pytest -q` in `backend/` passes, with tests for the 1–120 description limit, the 1–10,000,000 paise limit, a float amount, an unknown category and the `other` default.
- [ ] http://localhost:5173 adds and lists expenses, newest first, with rupees shown as `₹250.50`.
- [ ] `frontend/src/money.js` converts rupees to paise without floating-point maths.
- [ ] `.claude/settings.local.json` exists and is **not** in `git status` (it is personal).
- [ ] Your work is committed on `my-m02`.

## If you get stuck

- The browser shows a CORS error in the console: `Enable CORS in backend/app/main.py for http://localhost:5173.`
- The list is empty after restarting the backend: that is expected. Memory is cleared on restart. SQLite comes in M03.
- Compare with the trainer's branch: `git diff my-m02 origin/m02-first-session --stat`, and open any file with `git show origin/m02-first-session:<path>`.

# Lab M11: MCP in Claude Code

**Time:** 60 minutes · **Branch:** `m11-mcp-connect` (from `m10-hooks`)

## What you build

Three MCP servers connected to Claude Code, used on the Expense Tracker:

| Server | Transport | Scope | Used for |
|---|---|---|---|
| `filesystem` | stdio (npx) | project (`.mcp.json`) | Read-only access to `docs/`, with permission rules |
| `github` | http (remote) | local (your machine only) | Issues and pull requests on your `expense-tracker` repo |
| `playwright` | stdio (npx) | project (`.mcp.json`) | Claude drives a real browser on http://localhost:5173 |

And a Playwright test suite, `frontend/e2e/expenses.spec.js`, run with `npm run e2e`.

## Before you start

```text
git switch m10-hooks
git switch -c m11-mcp-connect
node --version
```

Node.js 22 or newer is needed for `npx` servers.

## Task 1: A project-scoped filesystem server (10 min)

```text
claude mcp add --scope project --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ./docs
```

Open `.mcp.json` in the project root: the server is there, ready to commit for the team. Then:

```text
claude mcp list
claude mcp get filesystem
```

**Expected:** the project server shows **Pending approval** until you approve it. Start `claude`, approve the server, then run `/mcp`: **filesystem** has a check mark. Look at its tools.

```text
Use the filesystem server to list docs/ and summarise docs/csv-export.md in three lines.
```

Make it read-only with permission rules. Ask Claude:

```text
Add to .claude/settings.json:
allow: mcp__filesystem__read_text_file, mcp__filesystem__list_directory
deny:  mcp__filesystem__write_file, mcp__filesystem__edit_file, mcp__filesystem__move_file,
       mcp__filesystem__create_directory
```

Start a new session and try:

```text
Use the filesystem server to create docs/notes.md with one line "hello".
```

**Expected:** denied. Run `/permissions` to see the rule.

## Task 2: The GitHub server (10 min)

Create a fine-grained **personal access token** on GitHub (Settings → Developer settings) with access to your `expense-tracker` repository: Contents, Issues and Pull requests (read and write). Set it in your terminal **before** starting Claude:

Windows (PowerShell): `$env:GITHUB_PERSONAL_ACCESS_TOKEN="<your token>"`
macOS: `export GITHUB_PERSONAL_ACCESS_TOKEN="<your token>"`

Add the remote server at **local** scope, so the token is stored only on your machine (in `~/.claude.json`), never in the repo:

Windows (PowerShell):

```text
claude mcp add --scope local --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $env:GITHUB_PERSONAL_ACCESS_TOKEN"
```

macOS:

```text
claude mcp add --scope local --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN"
```

Start `claude`, run `/mcp`, and check **github** is connected. Then:

```text
List the open pull requests in my repo expense-tracker.
```

```text
Create an issue in my repo expense-tracker titled "Add a budget editor to the UI" with the label
"enhancement". Body: users can only set budgets with PUT /budgets/{category} in /docs today.
```

Open the issue on GitHub. Keep its number for later.

No GitHub token in class? Skip this task; the rest of the lab works without it.

## Task 3: Let Claude test the app in a browser (12 min)

```text
claude mcp add --scope project playwright -- npx -y @playwright/mcp@latest
```

Start the backend and frontend in two terminals:

```text
cd backend
uv run uvicorn app.main:app --reload
```

```text
cd frontend
npm run dev
```

Start `claude` (approve the new project server), then:

```text
Use Playwright to:
1. Open http://localhost:5173
2. Add three expenses: "Auto to office" 120 transport, "Groceries" 850.75 food, "Movie" 400 other
3. Filter by "food" and take a screenshot
4. Type "auto" in the search box with the filter set back to All, and take a screenshot
5. Archive "Movie", then tick "Show archived"
Tell me if each step worked, and if amounts show as rupees with 2 decimals.
```

Watch the browser window: Claude clicks and types for real, and reports back.

## Task 4: Turn the checks into Playwright tests (15 min)

```text
cd frontend
npm install -D @playwright/test
npx playwright install chromium
```

```text
Create frontend/playwright.config.js and frontend/e2e/expenses.spec.js (JavaScript, not TypeScript).
The config starts two web servers: the backend with "uv run uvicorn app.main:app --port 8000" in
../backend with EXPENSES_DB=e2e-expenses.db, and "npm run dev" on http://localhost:5173.
Let backend/app/db.py read the database path from the EXPENSES_DB environment variable, with
backend/expenses.db as the default, so the e2e tests never touch your real data.
Tests: title and heading; add an expense and see ₹250.50; a bad amount shows the error; filter by
category; search ignores case; archive hides and Show archived brings it back; data survives a reload.
Give each test a unique description with Date.now(). Use labels (getByLabel with exact: true) and roles.
Add an "e2e" script: playwright test. Run it.
```

Stop your own dev servers first (Ctrl+C) so Playwright can start its own, or keep them: it reuses running servers.

```text
npm run e2e
```

**Expected:** 7 passed. Try the UI mode: `npx playwright test --ui`.

## Task 5: Put it together (8 min)

If you did Task 2:

```text
Read issue #<number> in my repo expense-tracker. Plan the budget editor (don't build it yet),
then add a comment on the issue with the plan.
```

Then check what loads, and the token cost of your servers:

```text
/context
```

**Expected:** MCP tools are listed and loaded on demand (tool search). Useful settings when a server is slow: `MCP_TIMEOUT=10000` before `claude`, and `MAX_MCP_OUTPUT_TOKENS` for large results.

## Finish

```text
git add -A
git commit -m "M11: MCP servers and Playwright e2e tests"
git switch main
git merge --no-ff m11-mcp-connect -m "Merge M11"
git switch m11-mcp-connect
```

Check that `.mcp.json` is committed, and that your token is **not** in any committed file (`git grep -n ghp_` finds nothing).

## Done when

- [ ] `.mcp.json` has `filesystem` and `playwright`; `/mcp` shows them connected.
- [ ] Filesystem writes are denied by permission rules; reads work.
- [ ] (With a token) the `github` server listed PRs and created an issue; it is local scope only.
- [ ] Claude drove the browser through add, filter, search and archive.
- [ ] `npm run e2e` passes 7 tests using `e2e-expenses.db`, not `expenses.db`.

## If you get stuck

- The server stays **pending**: approve it in the session, or run `claude mcp reset-project-choices` and start again.
- `npx` hangs on Windows: run `npx -y @playwright/mcp@latest --help` once in a terminal to finish the download.
- Port 8000 or 5173 is busy in `npm run e2e`: stop the running servers, or keep both running so Playwright reuses them.
- Compare with the reference branch `m11-mcp-connect`.

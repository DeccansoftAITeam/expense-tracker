# Expense Tracker: the lab project for Claude Code for the SDLC

A small web app to record personal expenses, see a monthly summary per category and stay inside monthly budgets.
Students build it themselves, one module at a time, by following the lab handbooks in `labs/`.

| Folder | What it holds |
|---|---|
| `docs/` | `PRD.md` and `TRD.md` (written in M00), feature requests |
| `backend/` | FastAPI, uv, pytest, SQLite |
| `frontend/` | React + Vite, JavaScript (`.jsx`) |
| `mcp-server/` | The expense MCP server (M12) |
| `labs/` | One lab handbook per module, M00 to M12 |

## Branches

Each module has a reference branch. Every branch starts from the branch of the module before it, and `main` has all of them merged.

```text
main
 └─ m00-prompt-engineering
     └─ m01-how-claude-code-works
         └─ m02-first-session
             └─ m03-context-memory
                 └─ m04-plan-implement-verify
                     └─ m05-git-worktrees-review
                         └─ m06-skills
                             └─ m07-subagents
                                 └─ m08-orchestration
                                     └─ m09-permissions
                                         └─ m10-hooks
                                             └─ m11-mcp-connect
                                                 └─ m12-mcp-build
```

Students clone this repository once. Every lab starts on a new branch of the student's own (`my-m04`), made from the trainer branch of the module before it (`origin/m03-context-memory`), so an unfinished lab never blocks the next one. A `starter` branch holds the empty project for M00. See `labs/README.md`.

## Run it

| What | Commands |
|---|---|
| Backend | `cd backend` → `uv sync` → `uv run uvicorn app.main:app --reload` (http://localhost:8000, API docs at /docs) |
| Backend tests | `cd backend` → `uv run pytest -q` |
| Frontend | `cd frontend` → `npm install` → `npm run dev` (http://localhost:5173) |
| Frontend build | `cd frontend` → `npm run build` |

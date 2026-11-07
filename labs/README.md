# Lab Handbook: how the labs work

You do one lab after each module. All labs build **one app**, the **Expense Tracker**, step by step.
Each lab takes **45–60 minutes**.

## What you need (install once)

| Tool | Check it | Install |
|---|---|---|
| Git | `git --version` | Windows: git-scm.com (Git for Windows). macOS: `xcode-select --install` |
| Python 3.12+ | Windows: `python --version`. macOS: `python3 --version` | python.org |
| uv | `uv --version` | Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"`. macOS: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node.js 22+ | `node --version` | nodejs.org |
| Claude Code | `claude --version` | Installed in M02 |
| VS Code | | code.visualstudio.com |
| gh (GitHub CLI) | `gh --version` | cli.github.com (needed from M05) |

## The app

A person records what they spend. Each **expense** has a description, an amount, a date and a category.
The app shows a list, a **monthly summary** per category, and warns when a category goes **over its monthly budget**.

## The rules (E1–E8)

Every lab, every review and every agent checks these. They go into `CLAUDE.md` in M03.

| Rule | Meaning |
|---|---|
| **E1** | Money is an **integer number of paise** (`amount_paise`). Never a float. ₹250.50 is `25050`. The UI shows rupees with 2 decimals |
| **E2** | `spent_on` is a date `YYYY-MM-DD`. Timestamps (`created_at`) are **UTC, ISO 8601** |
| **E3** | A **description is 1–120 characters** after trimming spaces |
| **E4** | An **amount is 1 to 10,000,000 paise** (₹0.01 to ₹1,00,000) |
| **E5** | **Category** is one of `food`, `transport`, `bills`, `shopping`, `health`, `other`; default `other` |
| **E6** | Expenses are **archived, never deleted**. There is no DELETE endpoint |
| **E7** | **No clock inside `rules.py`**: pass `today` in as a parameter |
| **E8** | **Never log descriptions or amounts** (personal data). Log the expense id only |

Two boundaries you will test again and again:

- A **monthly summary** for `2026-11` includes 1 and 30 November, and excludes 1 December. Archived expenses never count.
- A category is **over budget** when spent is **more than** the limit. Spent **equal** to the limit is **not** over.

## Branches: one per module

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

Every lab follows the same pattern:

1. **Start**: create the module branch from the branch of the module before it.

   ```text
   git switch m03-context-memory
   git switch -c m04-plan-implement-verify
   ```

2. **Work** through the tasks.
3. **Finish**: commit, then merge into `main`, so `main` always holds the latest app.

   ```text
   git add -A
   git commit -m "M04: monthly summary and category filter"
   git switch main
   git merge --no-ff m04-plan-implement-verify -m "Merge M04"
   git switch m04-plan-implement-verify
   ```

## Behind? Use the reference branch

Your trainer has a reference copy of the repository with every branch finished. To start lab M05 without M04 done, copy the reference `m04-plan-implement-verify` branch into your repo:

```text
git remote add reference <path-or-url-your-trainer-gives-you>
git fetch reference
git switch -c m04-plan-implement-verify reference/m04-plan-implement-verify
```

Then start M05 as normal.

## Run commands (the same in every lab)

| What | Commands |
|---|---|
| Backend | `cd backend` → `uv sync` → `uv run uvicorn app.main:app --reload` (http://localhost:8000, API docs at /docs) |
| Backend tests | `cd backend` → `uv run pytest -q` |
| Frontend | `cd frontend` → `npm install` → `npm run dev` (http://localhost:5173) |
| Frontend build | `cd frontend` → `npm run build` |

Keep three terminals open while you work: **Claude Code**, **backend**, **frontend**.

## How to read a lab

- `Prompt` blocks are typed into Claude Code (or the Claude chat in M00) exactly as written.
- `Shell` blocks are typed into a terminal. When Windows and macOS differ, both are shown.
- **Expected** tells you what you should see. If you see something else, read the transcript before you retry.
- **Done when** at the end is your checklist. Tick every line before you merge.

## Labs

| Lab | Module | You build |
|---|---|---|
| [M00](M00-Prompt-Engineering.md) | Prompt engineering | `docs/PRD.md` and `docs/TRD.md`, written in a Claude chat |
| [M01](M01-How-Claude-Code-Works.md) | How Claude Code works | `GET /health` with a test; the Vite frontend shell |
| [M02](M02-First-Session.md) | Install, sign in, first session | Add and list expenses (in memory); `ExpenseForm`, `ExpenseList` |
| [M03](M03-Context-and-Memory.md) | Context and memory | `CLAUDE.md` with E1–E8, `AGENTS.md`, path rules, SQLite, archive |
| [M04](M04-Plan-Implement-Verify.md) | Plan, implement, verify | Monthly summary (tests first); category filter (plan mode) |
| [M05](M05-Git-Worktrees-Review.md) | Git, GitHub, worktrees, review | Budgets and search in two worktrees; code and security review |
| [M06](M06-Skills.md) | Skills | `add-expense-field` (payment method), `new-component` (AmountBadge) and more |
| [M07](M07-Subagents.md) | Subagents | `expense-reviewer`, `finder`, `test-runner`, role agents; CSV export |
| [M08](M08-Orchestration.md) | Orchestration | Recurring monthly expenses through a pipeline, fan-out review, fix loop |
| [M09](M09-Permissions.md) | Permissions and workspace trust | Team `.claude/settings.json`; secrets kept away from Claude |
| [M10](M10-Hooks.md) | Hooks | Notification, protect-files, format-on-edit, audit log, rules after compaction |
| [M11](M11-MCP-Connect.md) | MCP in Claude Code | Filesystem, GitHub and Playwright MCP servers on the app |
| [M12](M12-MCP-Build.md) | Build an MCP server | An `expenses` MCP server in Python, tested with the Inspector and used by Claude |

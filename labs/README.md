# Lab Handbook: how the labs work

You do one lab after each module. All labs build **one app**, the **Expense Tracker**, step by step.

## Where to read the handbooks

Your trainer shares every handbook as Word, PDF and Markdown. Read them from those copies, not from your checkout: the branch you start a lab from holds only the handbooks of the labs before it. In the repository, all handbooks are on `origin/main`, for example `git show origin/main:labs/M04-Plan-Implement-Verify.md`.

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

### Installing uv

uv runs the backend, its tests and the MCP server. Install it once:

1. Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   macOS (Terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `brew install uv`)
2. Close the terminal and open a new one.
3. Check it: `uv --version`
4. Get Python 3.12 for uv: `uv python install 3.12`

Lab M01 has the same steps with help for when `uv` is not found.

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

## Branches: the trainer's and yours

Clone the course repository **once**, in Lab M00 (your trainer gives you the address):

```text
git clone <course-repo-url> expense-tracker
cd expense-tracker
```

It has the trainer's **finished branch for every module**, and a `starter` branch with an empty project:

| Trainer branch (read only) | Holds the app as it is at the end of |
|---|---|
| `origin/starter` | nothing yet: README and `.gitignore` |
| `origin/m00-prompt-engineering` | M00 |
| `origin/m01-how-claude-code-works` | M01 |
| `origin/m02-first-session` | M02 |
| `origin/m03-context-memory` | M03 |
| `origin/m04-plan-implement-verify` | M04 |
| `origin/m05-git-worktrees-review` | M05 |
| `origin/m06-skills` | M06 |
| `origin/m07-subagents` | M07 |
| `origin/m08-orchestration` | M08 |
| `origin/m09-permissions` | M09 |
| `origin/m10-hooks` | M10 |
| `origin/m11-mcp-connect` | M11 |
| `origin/m12-mcp-build` | M12 (the complete app; `origin/main` is the same) |

**Every lab starts from the trainer's branch of the module before it, never from your own work.** You do each lab on a new branch of your own, `my-m00` to `my-m12`:

| Lab | Start command |
|---|---|
| M00 | `git switch -c my-m00 origin/starter` |
| M01 | `git switch -c my-m01 origin/m00-prompt-engineering` |
| M02 | `git switch -c my-m02 origin/m01-how-claude-code-works` |
| M03 | `git switch -c my-m03 origin/m02-first-session` |
| M04 | `git switch -c my-m04 origin/m03-context-memory` |
| M05 | `git switch -c my-m05 origin/m04-plan-implement-verify` |
| M06 | `git switch -c my-m06 origin/m05-git-worktrees-review` |
| M07 | `git switch -c my-m07 origin/m06-skills` |
| M08 | `git switch -c my-m08 origin/m07-subagents` |
| M09 | `git switch -c my-m09 origin/m08-orchestration` |
| M10 | `git switch -c my-m10 origin/m09-permissions` |
| M11 | `git switch -c my-m11 origin/m10-hooks` |
| M12 | `git switch -c my-m12 origin/m11-mcp-connect` |

Run `git fetch origin` first, so you have the trainer's latest branches.

**Example.** Ravi did not finish Lab M03: archive is still missing on `my-m03`. For Lab M04 he runs:

```text
git fetch origin
git switch -c my-m04 origin/m03-context-memory
```

He now has the trainer's complete M03 app and does the M04 tasks on `my-m04`. His `my-m03` is kept as it is; he can finish it later with `git switch my-m03`.

Before you switch to the next lab, commit what you have on your current branch, even if it is not finished:

```text
git add -A
git commit -m "wip"
```

Otherwise your uncommitted changes come along to the new branch.

So you can:

- **Leave a lab unfinished** and still start the next one.
- **Start at any module**, for example join at M07 with `git switch -c my-m07 origin/m06-skills`.
- **Compare** your work with the trainer's at the end of a lab: `git diff my-m04 origin/m04-plan-implement-verify --stat`.

At the end of each lab you only commit on your own branch. You never merge into `main` and never push to `origin`.

**Your own GitHub repository.** In Lab M05 you create a private GitHub repo and add it as a second remote named `mine`. M08 and M09 push to it, and M11 uses it through the GitHub MCP server. If you start after M05, do M05 Task 1 once first.

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

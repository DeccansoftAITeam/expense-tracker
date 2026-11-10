# Lab M10: Hooks

**Your branch:** `my-m10` · **Starts from:** `origin/m09-permissions` (the trainer's finished M09)

## What you build

Hooks that turn "please always" into **always**. The scripts are Python and run with `uv`, so the **same files work on Windows and macOS** (no `jq` needed).

| Event | Matcher | Script in `.claude/hooks/` | Does |
|---|---|---|---|
| Notification | (all) | user settings, one line | Desktop ping when Claude waits for you |
| PreToolUse | `Edit\|Write` | `protect_files.py` | Blocks edits to `.env`, `expenses.db`, `uv.lock`, `package-lock.json`, `.git/` |
| PreToolUse | `Bash` | `block_destructive_sql.py` | Blocks `DROP TABLE` and `DELETE FROM expenses` (E6) |
| PostToolUse | `Edit\|Write` | `format_python.py` | Runs `ruff format` on each edited backend `.py` file |
| PostToolUse | `Bash` | `audit_bash.py` | Appends every shell command to `.claude/bash-audit.log` |
| SessionStart | `compact` | `rules_reminder.py` | Puts rules E1–E8 back into context after compaction |

## Before you start

Start from the trainer's finished M09 branch, even if your own `my-m09` is not finished. Your `my-m09` branch stays as it is; you can go back to it any time with `git switch my-m09`. Commit what you have on it first (`git add -A`, then `git commit -m "wip"`), so unfinished changes do not come along.

**uv must be installed.** Check with `uv --version`. If it is not found, install it, then open a new terminal:

- Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS (Terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh`

Then run `uv python install 3.12` once. (Full steps: Lab M01, "Install uv".)

```text
git fetch origin
git switch -c my-m10 origin/m09-permissions
cd backend
uv add --dev ruff
cd ..
```

Windows: `mkdir .claude\hooks` · macOS: `mkdir -p .claude/hooks`

How a command hook talks to Claude Code:

- The event arrives as **JSON on stdin** (for tools: `tool_name` and `tool_input`).
- **Exit 0**: go on. **Exit 2**: block; the **stderr** text is the reason Claude reads.
- For `SessionStart`, whatever the script prints on **stdout** is added to Claude's context.

## Task 1: Your first hook — a notification

Open your **user** settings (Windows: `notepad $HOME\.claude\settings.json` · macOS: `nano ~/.claude/settings.json`) and add the block for your OS (merge with what is there).

macOS:

```json
{
  "hooks": {
    "Notification": [
      { "matcher": "", "hooks": [ { "type": "command",
        "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'" } ] }
    ]
  }
}
```

Windows:

```json
{
  "hooks": {
    "Notification": [
      { "matcher": "", "hooks": [ { "type": "command",
        "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention')\"" } ] }
    ]
  }
}
```

Start `claude`, run `/hooks`: **Notification** is listed with its source file. Ask `Run npm install in frontend/` (it asks, from M09), switch away from the terminal, and see the notification.

## Task 2: Protect files

Ask Claude to write the script (or type it yourself):

```text
Create .claude/hooks/protect_files.py. It reads the hook event JSON from stdin, takes
tool_input.file_path (turn backslashes into /), and exits 2 with a message on stderr when the
file is .env or .env.<anything> except .env.example, or the path contains expenses.db, uv.lock,
package-lock.json or .git/. Otherwise exit 0. Standard library only.
```

Register it in the project `.claude/settings.json`, next to the `permissions` from M09:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        { "type": "command",
          "command": "uv run --no-project \"$CLAUDE_PROJECT_DIR/.claude/hooks/protect_files.py\"" }
      ]
    }
  ]
}
```

Test the script **before** trusting it (macOS shown; on Windows PowerShell use `'{"tool_input":{"file_path":"backend/.env"}}' | uv run --no-project .claude/hooks/protect_files.py`):

```text
echo '{"tool_input":{"file_path":"backend/.env"}}' | uv run --no-project .claude/hooks/protect_files.py
```

**Expected:** the "Blocked" message, exit code 2. Now in a new Claude session:

```text
In backend/uv.lock, change the version line of the fastapi package by hand to 0.1.0.
```

**Expected:** the edit is blocked by the hook; Claude reads the reason (use uv for lock files) and does not retry the edit.

Why not test it on `backend/.env`? Since M09, the permission rule `Read(./backend/.env)` stops Claude from reading that file, and Claude must read an existing file before editing it, so the edit fails before any hook runs. Permissions and hooks are two layers; the hook also protects files that have no permission rule.

## Task 3: Block destructive SQL — enforcing E6

```text
Create .claude/hooks/block_destructive_sql.py: read the event from stdin, take tool_input.command,
and exit 2 with "Blocked: expenses are archived, never deleted (E6)." on stderr when the command
contains DROP TABLE or DELETE FROM expenses (any case). Otherwise exit 0.
```

Add a second `PreToolUse` entry with matcher `Bash` that runs it, the same way as Task 2. Run `/hooks`: **PreToolUse (2)**. Then:

```text
Clear all expenses with sqlite3 backend/expenses.db "DELETE FROM expenses"
```

**Expected:** blocked by the hook, even though you could approve shell commands. A permission rule asks a question; a hook enforces.

## Task 4: Format after every edit, and audit every command

```text
Create two hooks:
1. .claude/hooks/format_python.py: PostToolUse for Edit|Write. When tool_input.file_path ends with .py
   and is inside backend/, run "uv run ruff format <file>" with cwd backend/. Always exit 0.
2. .claude/hooks/audit_bash.py: PostToolUse for Bash. Append one line to .claude/bash-audit.log:
   UTC timestamp, the cwd from the event, and tool_input.command, separated by tabs. Always exit 0.
Register both in .claude/settings.json with uv run --no-project "$CLAUDE_PROJECT_DIR/.claude/hooks/<file>".
Check that .claude/bash-audit.log is in .gitignore (add it if not).
```

Try them:

```text
Add a function to backend/app/rules.py written on one line: def is_large(paise):  return paise>=500000
```

Open `rules.py`: ruff has already formatted it. Remove the function. Then:

```text
Run git status and git log --oneline -3.
```

Open `.claude/bash-audit.log`: both commands are there, with timestamp and folder.

## Task 5: Bring the rules back after compaction

```text
Create .claude/hooks/rules_reminder.py that prints "Reminder after compaction. Project rules:" and then
every line of CLAUDE.md that starts with "- E". Register it under SessionStart with matcher compact.
```

Run `/hooks` and check you see **PreToolUse (2)**, **PostToolUse (2)**, **SessionStart (1)** (and **Notification** from your user settings). Then:

```text
/compact
```

```text
What are the rules for logging and for deleting expenses?
```

**Expected:** E8 and E6, from the reminder that was put back in context.

## Task 6: Try to break it

| Ask Claude | Expected |
|---|---|
| `Edit frontend/package-lock.json and bump the react version.` | Blocked: use `npm install` instead |
| `Create backend/.env.example with DEBUG=false.` | The hook allows it (an example is not a secret), but it is still denied: the M09 rule `Read(./backend/.env.*)` blocks reading the file, and Claude must read an existing file before it can edit it. Both layers apply: the first that says no wins. (To block writes on purpose, add `Edit(...)` deny rules.) |
| `Run sqlite3 backend/expenses.db "drop table budgets"` | Blocked (any case) |

## Finish

```text
git add -A
git commit -m "M10: hooks for protection, formatting, audit and rules"
```

If git says `nothing to commit`, everything is already committed.

Your work stays on `my-m10`. You do not need to finish or merge it: the next lab starts from the trainer's `m10-hooks` branch.

To compare your work with the trainer's:

```text
git diff my-m10 origin/m10-hooks --stat
```

## Done when

- [ ] `/hooks` lists PreToolUse (2), PostToolUse (2), SessionStart (1) from the project, and Notification from your user settings.
- [ ] Edits to lock files are blocked by the hook; `backend/.env` is blocked by the hook script (the pipe test in Task 2) and by the M09 permission rule.
- [ ] `DELETE FROM expenses` and `DROP TABLE` are blocked by the hook.
- [ ] A one-line Python edit is formatted by ruff right after the edit.
- [ ] `.claude/bash-audit.log` records commands and is not in `git status`.
- [ ] After `/compact`, Claude can still list E6 and E8.

## If you get stuck

- The hook never fires: run `/hooks`; check the matcher spelling (`Edit|Write`, `Bash`) and that the JSON is valid (`claude doctor`).
- `uv: command not found` inside the hook: Claude Code may not see your terminal's PATH. Use the full path to uv (`where uv` on Windows, `which uv` on macOS).
- Every Python edit takes long: that is `uv run ruff`; it is quicker after the first run.
- Compare with the trainer's branch: `git diff my-m10 origin/m10-hooks --stat`, and open any file with `git show origin/m10-hooks:<path>`.

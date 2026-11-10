# Lab M09: Permissions and workspace trust

**Your branch:** `my-m09` · **Starts from:** `origin/m08-orchestration` (the trainer's finished M08)

## What you build

A committed team file `.claude/settings.json` for the Expense Tracker:

- **allow**: tests, builds, read-only git commands, run with no prompt.
- **ask**: `git push`, `npm install`, `uv add` always prompt.
- **deny**: `backend/.env`, `backend/expenses.db`, force-push, push to main, `curl`, `wget`.

And a `backend/.env.example`, checked with `/permissions`, a fresh clone and `claude -p`.

## Before you start

Start from the trainer's finished M08 branch, even if your own `my-m08` is not finished. Your `my-m08` branch stays as it is; you can go back to it any time with `git switch my-m08`. Commit what you have on it first (`git add -A`, then `git commit -m "wip"`), so unfinished changes do not come along.

**uv must be installed.** Check with `uv --version`. If it is not found, install it, then open a new terminal:

- Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS (Terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh`

Then run `uv python install 3.12` once. (Full steps: Lab M01, "Install uv".)

```text
git fetch origin
git switch -c my-m09 origin/m08-orchestration
```

Keep **Manual** mode for this whole lab, so every prompt is visible.

## Task 1: Modes, and auto mode is not a guarantee

```text
claude
```

Look at the bottom line, then press **Shift+Tab** until it shows **Manual**. Exit and start in a mode directly:

```text
claude --permission-mode plan
```

Exit again. Start with `claude`, switch to **Auto** with **Shift+Tab**, and ask:

```text
Force-push the current branch to origin.
```

**Expected:** the classifier blocks it. Run `/permissions` and open **Recently denied**. Press **Esc** and switch back to **Manual**.

## Task 2: Write the team rules

```text
Create .claude/settings.json with these permissions:
allow: Bash(uv run pytest *), Bash(uv run ruff *), Bash(npm run build), Bash(npm test),
       Bash(git status), Bash(git diff *), Bash(git log *)
ask:   Bash(git push *), Bash(npm install *), Bash(uv add *)
deny:  Read(./backend/.env), Read(./backend/.env.*), Read(./backend/expenses.db),
       Bash(git push --force*), Bash(git push origin main*), Bash(curl *), Bash(wget *)
```

Approve the edit (it is a protected path, so it always asks). Now test each list:

| Prompt | Expected |
|---|---|
| `Run the backend tests.` | Runs `uv run pytest -q` with **no prompt** (allow) |
| `Push the current branch.` | A **prompt** (ask). Choose **No** |
| `Show me backend/expenses.db.` | **Denied** |

Run `/permissions` and find each rule and the file it came from.

## Task 3: Compound commands and wrappers

| Prompt | Expected |
|---|---|
| `Run cd backend && uv run pytest -q exactly as written.` | No prompt: each part is allowed |
| `Run timeout 60 uv run pytest -q in backend.` | No prompt: the `timeout` wrapper is stripped |
| `Run git status && git push.` | A prompt: one part matches the ask rule. Choose **No** |

## Task 4: Precedence — a user deny beats a project allow

Open your user settings:

Windows: `notepad $HOME\.claude\settings.json` · macOS: `nano ~/.claude/settings.json`

Add (merge with what is already there):

```json
{
  "permissions": {
    "deny": ["Bash(npm run build)"]
  }
}
```

In the session:

```text
Build the frontend.
```

**Expected:** denied, although the project allows it. Run `/permissions` to see the deny and its source. **Remove** the line from your user settings again.

## Task 5: Keep secrets away from Claude

Create `backend/.env` (it is git-ignored) with two lines:

```text
DATABASE_URL=sqlite:///expenses.db
SECRET_KEY=dev-only
```

And a committed example, `backend/.env.example`:

```text
# Copy to backend/.env and fill in. backend/.env is never committed and Claude may not read it.
DATABASE_URL=sqlite:///expenses.db
SECRET_KEY=change-me
```

Run `git status`: `backend/.env.example` shows, `backend/.env` does not.

```text
Show me backend/.env.
```

**Expected:** reading it is denied.

```text
Run python -c "print(open('backend/.env').read())"
```

**Expected:** a normal approval prompt for a shell command. Choose **No**. The deny rule alone would **not** have stopped a script that opens the file itself. Hard limits need the sandbox (`/sandbox`, macOS/Linux/WSL2) or keeping real secrets out of the project folder.

## Task 6: Workspace trust and claude -p

Commit the settings file and push it to your own repository (remote `mine`, from M05):

```text
git add .claude/settings.json backend/.env.example
git commit -m "Add team permission rules and an env example"
git push -u mine my-m09
```

Clone it into a new folder next to your project and switch to the branch:

```text
cd ..
git clone https://github.com/<you>/expense-tracker expense-tracker-copy
cd expense-tracker-copy
git switch my-m09
```

No GitHub? Use `git clone expense-tracker expense-tracker-copy` from the parent folder instead, then `git switch my-m09`.

**Before** opening it interactively, run:

```text
claude -p "run the backend tests"
```

**Expected:** a warning on stderr; the test command is not run, because the folder is not trusted yet, so the project allow rules were not used. Now allow it for this one run:

```text
claude -p "run the backend tests" --allowedTools "Bash(uv run pytest *)"
```

Now open it interactively:

```text
claude
```

**Expected:** the trust dialog lists the allow rules from `.claude/settings.json`. Read them, then accept. Exit, and go back to your project folder (`cd ../expense-tracker`).

## Finish

```text
git add -A
git commit -m "M09: team permissions"
```

If git says `nothing to commit`, everything is already committed.

Your work stays on `my-m09`. You do not need to finish or merge it: the next lab starts from the trainer's `m09-permissions` branch.

To compare your work with the trainer's:

```text
git diff my-m09 origin/m09-permissions --stat
```

## Done when

- [ ] `.claude/settings.json` is committed with allow, ask and deny lists.
- [ ] Tests run with no prompt; `git push` asks; `backend/.env` and `backend/expenses.db` are denied.
- [ ] You saw a user-level deny win over a project allow in `/permissions`, and removed it.
- [ ] `backend/.env.example` is committed; `backend/.env` is not.
- [ ] `claude -p` in an untrusted clone did not use the project rules until `--allowedTools` or trust.

## If you get stuck

- A rule seems ignored: check `/permissions` for a typo, then run `claude doctor` for malformed entries.
- `Write(...)` rules never match: file writes are checked against `Edit(...)` rules.
- Compare with the trainer's branch: `git diff my-m09 origin/m09-permissions --stat`, and open any file with `git show origin/m09-permissions:<path>`.

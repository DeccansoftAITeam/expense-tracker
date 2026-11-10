# Lab M05: Git, GitHub, worktrees and review

**Your branch:** `my-m05` · **Starts from:** `origin/m04-plan-implement-verify` (the trainer's finished M04)

## What you build

- A private GitHub repository `expense-tracker`, with commits and pull requests that Claude writes and you own.
- Two features **in parallel**, each in its own **worktree**:
  - `budgets` (backend only): `PUT /budgets/{category}`, `GET /budgets?month=` with spent and **over**.
  - `search` (frontend only): `SearchBox.jsx`, filters the list by description, ignoring case.
- A **Review rules** section in `CLAUDE.md`, checked with `/code-review` and `/security-review`.

## Before you start

Start from the trainer's finished M04 branch, even if your own `my-m04` is not finished. Your `my-m04` branch stays as it is; you can go back to it any time with `git switch my-m04`. Commit what you have on it first (`git add -A`, then `git commit -m "wip"`), so unfinished changes do not come along.

**uv must be installed.** Check with `uv --version`. If it is not found, install it, then open a new terminal:

- Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- macOS (Terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh`

Then run `uv python install 3.12` once. (Full steps: Lab M01, "Install uv".)

```text
git fetch origin
git switch -c my-m05 origin/m04-plan-implement-verify
git --version
gh --version
gh auth status
```

If `gh auth status` says you are not logged in: `gh auth login`, choose **GitHub.com** and **HTTPS**, and log in through the browser.

## Task 1: Check .gitignore and push to GitHub

```text
claude
```

```text
Check .gitignore for a Python (uv) backend and a React (Vite) frontend. It must ignore:
.venv, __pycache__, node_modules, dist, .env*, backend/expenses.db, CLAUDE.local.md,
.claude/settings.local.json, .claude/worktrees/. Add what is missing. Do not commit yet.
```

Create a test secret (Windows: `Set-Content backend/.env "SECRET=123"`; macOS: `echo SECRET=123 > backend/.env`), then:

```text
Show git status.
```

**Expected:** neither `backend/.env` nor `backend/expenses.db` appears. Then:

```text
Show me git diff --staged after staging .gitignore. Then commit it with a one-line message in the
imperative mood, under 60 characters, that says what changed and why.
```

Your `origin` is the course repository, which you only read from. Your own work goes to your own GitHub repository, added as a second remote named `mine`:

```text
Create a private GitHub repository named expense-tracker with gh. Add it as a remote named mine
(keep origin as it is) and push my-m05 to it. Then make it the default repo for gh with
gh repo set-default, and show me git remote -v.
```

Approve the `gh repo create`, `git push` and `gh repo set-default` commands. Open the URL: the code is there, `.env` and `expenses.db` are not.

## Task 2: Teach the reviewer your rules

```text
Add a "Review rules" section to CLAUDE.md with these lines, then commit it:
- Money is integer paise, never a float (E1).
- Dates are YYYY-MM-DD; timestamps UTC, ISO 8601 (E2).
- No clock inside rules.py: pass today in (E7).
- Never log descriptions or amounts; log the id (E8).
- Descriptions 1-120 chars; archive, never delete (E3, E6).
- No new dependency without a person's approval.
- Every new endpoint has a test in backend/tests/.
```

Push the branch: `git push mine my-m05`.

## Task 3: Two features in two worktrees

Make the `.env` file follow you into new worktrees: create `.worktreeinclude` in the project root with one line:

```text
backend/.env
```

Commit it.

By default, `claude --worktree` makes the new worktree from the remote's default branch (`origin/main`, which is the trainer's complete app). You want both worktrees to start from **your** `my-m05`. Add this to `.claude/settings.local.json` (personal, git-ignored; create the file if it does not exist):

```json
{
  "worktree": {
    "baseRef": "head"
  }
}
```

Make sure you are on `my-m05` (`git branch --show-current`). Each worktree gets its own branch: `worktree-budgets` and `worktree-search`.

Open **two terminals** in the project folder.

Terminal 1:

```text
claude --worktree budgets
```

```text
Add monthly budgets per category. PUT /budgets/{category} with {"limit_paise": int} sets a limit
(1 to 10,000,000 paise, strict int). GET /budgets?month=YYYY-MM returns each budget with
limit_paise, spent_paise and over. Over means spent is MORE than the limit; equal is NOT over.
Archived expenses never count. Put is_over_budget(spent, limit) in backend/app/rules.py.
Write the pytest tests first. Change only files in backend/.
```

Terminal 2:

```text
claude -w search
```

```text
Add a SearchBox.jsx component above the expense list that filters expenses by description
as you type, ignoring case. Change only files in frontend/. Run npm run build.
```

In a third terminal:

```text
git worktree list
```

**Expected:** three folders: your main folder on `my-m05`, and `.claude/worktrees/budgets` and `.claude/worktrees/search` on `worktree-budgets` and `worktree-search`, both starting at the same commit as `my-m05`. In the budgets session, run the tests yourself with the `!` prefix:

```text
! cd backend && uv run pytest -q
```

In **each** session:

```text
Commit the work, push this branch to the remote mine, and open a pull request with gh on my
repository expense-tracker against my-m05.
Title: one line. Body: what changed, why, how to test, and anything you were unsure about. Do not merge it.
```

Type `/exit` in the budgets session and choose **keep**. Run `git worktree list`: it is still there. Continue it with:

```text
claude --worktree budgets --resume
```

## Task 4: /code-review on the budgets PR

In the budgets session:

```text
/code-review high
```

Keep working while it runs in the background; findings arrive in the conversation. Then review the pull request itself (use your PR number, for example 1):

```text
/code-review high 1 --comment
```

Refresh the PR page: comments appear on the lines. Fix the findings you agree with:

```text
Fix findings 1 and 3 only. Run the tests, commit and push.
```

Run `git diff HEAD~1` to see exactly what changed. On GitHub, approve and **merge the budgets PR yourself**.

Now update the search branch. In the search session (`claude --worktree search --resume`):

```text
The base branch has moved. Fetch mine and rebase this branch on mine/my-m05, run npm run build,
and tell me if anything conflicted. Then push the updated branch with git push --force-with-lease
(a rebased branch needs it; --force-with-lease refuses if someone else pushed in the meantime).
```

Merge the search PR on GitHub. Then, in your main folder:

```text
git pull mine my-m05
```

## Task 5: /security-review catches personal data in logs

```text
git switch -c log-test
```

In `backend/app/main.py`, inside `create_expense`, add this line by hand:

```text
logger.info("created expense %s for %s", expense["description"], expense["amount_paise"])
```

Commit it, then in Claude:

```text
/security-review
```

Read the finding: severity, confidence, category and the exploit scenario. Then:

```text
Fix it by logging the expense id only (rule E8).
```

Run `/security-review` again: no finding. Throw the fix away (it was only a test), switch back and remove the test branch:

```text
git restore backend/app/main.py
git switch my-m05
git branch -D log-test
```

## Task 6: Watch the reviewer use your rules

Break a rule on purpose. In `backend/app/rules.py`, make `is_over_budget` read the clock, for example add `from datetime import datetime` and `datetime.now()` inside it.

```text
/code-review
```

**Expected:** it cites **E7** (no clock inside `rules.py`). Undo the change:

```text
git restore backend/app/rules.py
```

## Finish

```text
git add -A
git commit -m "M05: budgets, search and review"
```

If git says `nothing to commit`, everything is already committed.

Your work stays on `my-m05`. You do not need to finish or merge it: the next lab starts from the trainer's `m05-git-worktrees-review` branch.

To compare your work with the trainer's:

```text
git diff my-m05 origin/m05-git-worktrees-review --stat
```

## Done when

- [ ] Your private GitHub repo `expense-tracker` (remote `mine`) has `my-m05`; no `.env` or `expenses.db`.
- [ ] Two PRs (budgets, search) were opened from two worktrees and merged by you.
- [ ] `uv run pytest -q` covers: equal to the limit is not over, one paisa more is over, archived does not count.
- [ ] Typing "lun" in the search box shows only "Lunch".
- [ ] `/security-review` flagged the description in the log, and the fix logs the id only.
- [ ] `CLAUDE.md` has the Review rules section.

## If you get stuck

- `claude --worktree` starts without `backend/.env`: check `.worktreeinclude` is in the main folder and committed.
- A worktree already has budgets or search in it: it was made from `origin/main`, because the `baseRef` setting was missing. Exit that session, run `git worktree remove --force .claude/worktrees/budgets` and `git branch -D worktree-budgets`, add the setting, and start again.
- The rebase conflicts in `App.jsx`: ask `Resolve the conflict keeping both the search box and the existing filters.`
- No GitHub access in class? Do Tasks 3–6 locally: merge with `git merge --no-ff worktree-budgets` and `git merge --no-ff worktree-search` on `my-m05`, and use `/code-review` without a PR number.
- Compare with the trainer's branch: `git diff my-m05 origin/m05-git-worktrees-review --stat`, and open any file with `git show origin/m05-git-worktrees-review:<path>`.

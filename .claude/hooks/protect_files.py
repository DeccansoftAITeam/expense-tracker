"""PreToolUse hook for Edit|Write: block edits to secrets, the database and lock files.

Exit 2 blocks the tool call; stderr is shown to Claude as the reason.
"""

import json
import sys

PROTECTED = (".env", "expenses.db", "uv.lock", "package-lock.json", ".git/")

event = json.load(sys.stdin)
path = (event.get("tool_input") or {}).get("file_path", "").replace("\\", "/")
name = path.rsplit("/", 1)[-1]

for pattern in PROTECTED:
    # .env and .env.local are blocked; .env.example is allowed
    if pattern == ".env":
        hit = name == ".env" or (name.startswith(".env.") and name != ".env.example")
    else:
        hit = pattern in path
    if hit:
        print(f"Blocked: {path} is protected ({pattern}). Change it by hand, or use uv/npm for lock files.", file=sys.stderr)
        sys.exit(2)

sys.exit(0)

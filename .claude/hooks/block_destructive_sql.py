"""PreToolUse hook for Bash: block shell commands that drop tables or delete expenses (E6)."""

import json
import re
import sys

event = json.load(sys.stdin)
command = (event.get("tool_input") or {}).get("command", "")

if re.search(r"\bdrop\s+table\b", command, re.IGNORECASE) or re.search(
    r"\bdelete\s+from\s+expenses\b", command, re.IGNORECASE
):
    print("Blocked: expenses are archived, never deleted (E6). Do not drop tables or delete rows.", file=sys.stderr)
    sys.exit(2)

sys.exit(0)

"""PostToolUse hook for Bash: append every shell command to .claude/bash-audit.log."""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

event = json.load(sys.stdin)
command = (event.get("tool_input") or {}).get("command", "")
log = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / ".claude" / "bash-audit.log"

with log.open("a", encoding="utf-8") as file:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    file.write(f"{stamp}\t{event.get('cwd', '')}\t{command}\n")

sys.exit(0)

"""SessionStart hook (matcher: compact): print rules E1-E8 so they are back in context.

For SessionStart, whatever this prints on stdout is added to Claude's context.
"""

import os
from pathlib import Path

claude_md = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / "CLAUDE.md"
rules = [line for line in claude_md.read_text(encoding="utf-8").splitlines() if line.startswith("- E")]
print("Reminder after compaction. Project rules:")
print("\n".join(rules))

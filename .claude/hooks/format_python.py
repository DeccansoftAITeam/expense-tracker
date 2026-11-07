"""PostToolUse hook for Edit|Write: format a backend Python file with ruff after each edit."""

import json
import os
import subprocess
import sys
from pathlib import Path

event = json.load(sys.stdin)
path = (event.get("tool_input") or {}).get("file_path", "")
project = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
backend = project / "backend"

if path.endswith(".py") and Path(path).resolve().is_relative_to(backend.resolve()):
    subprocess.run(["uv", "run", "ruff", "format", path], cwd=backend, capture_output=True)

sys.exit(0)

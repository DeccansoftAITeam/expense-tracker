"""Print every pytest test function name under a folder, one per line."""

import ast
import sys
from pathlib import Path


def test_names(folder: Path) -> list[str]:
    names = []
    for path in sorted(folder.rglob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                names.append(f"{path.as_posix()}::{node.name}")
    return names


if __name__ == "__main__":
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "backend/tests")
    for name in test_names(folder):
        print(name)

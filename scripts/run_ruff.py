from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    app_dir = project_root / "app"

    if not app_dir.exists():
        print("Error: app/ directory not found", file=sys.stderr)
        return 1

    cmd = [
        "ruff",
        "check",
        "--fix",
        str(app_dir),
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

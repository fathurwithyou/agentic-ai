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

    # Run ruff check with auto-fix
    check_cmd = [
        "ruff",
        "check",
        "--fix",
        str(app_dir),
    ]

    print(f"Running: {' '.join(check_cmd)}")
    check_result = subprocess.run(check_cmd)

    if check_result.returncode != 0:
        return check_result.returncode

    # Run ruff format
    format_cmd = [
        "ruff",
        "format",
        str(app_dir),
    ]

    print(f"Running: {' '.join(format_cmd)}")
    format_result = subprocess.run(format_cmd)

    return format_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

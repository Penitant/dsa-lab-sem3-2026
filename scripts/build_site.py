#!/usr/bin/env python3
# Assembles the Pages site: docs/ + assignments/weekN/ + assignments.json.
import json
import shutil
import sys
from pathlib import Path

from assignments import QUESTION_FILE, AssignmentError, load_all

DOCS_DIR = Path("docs")


def main():
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    try:
        assignments = load_all()
    except AssignmentError as e:
        sys.exit(f"Invalid assignments:\n{e}")

    shutil.copytree(DOCS_DIR, out_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns("README.md"))

    entries = []
    for a in assignments:
        week_dir = a["dir"]
        files = sorted(
            p.relative_to(week_dir).as_posix()
            for p in week_dir.rglob("*")
            if p.is_file() and p.name != QUESTION_FILE and "__pycache__" not in p.parts
        )
        entries.append(
            {
                "week": a["week"],
                "title": a["title"],
                "category": a["category"],
                "start": a["start"].isoformat(),
                "end": a["end"].isoformat(),
                "path": f"assignments/{week_dir.name}",
                "files": files,
            }
        )
        shutil.copytree(
            week_dir,
            out_dir / "assignments" / week_dir.name,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__"),
        )

    (out_dir / "assignments.json").write_text(json.dumps(entries, indent=2) + "\n")


if __name__ == "__main__":
    main()

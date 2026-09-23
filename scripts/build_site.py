#!/usr/bin/env python3
# Assembles the Pages site: docs/ + assignments/weekN/ + assignments.json.
import json
import re
import shutil
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
ASSIGNMENTS_DIR = Path("assignments")
QUESTION_FILE = "QUESTION.md"
WEEK_DIR_RE = re.compile(r"^week(\d+)$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def main():
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    shutil.copytree(DOCS_DIR, out_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns("README.md"))

    entries = []
    for week_dir in ASSIGNMENTS_DIR.iterdir():
        match = WEEK_DIR_RE.match(week_dir.name)
        question = week_dir / QUESTION_FILE
        if not week_dir.is_dir() or not match or not question.is_file():
            continue
        fields = parse_frontmatter(question.read_text())
        files = sorted(
            p.relative_to(week_dir).as_posix()
            for p in week_dir.rglob("*")
            if p.is_file() and p.name != QUESTION_FILE and "__pycache__" not in p.parts
        )
        entries.append(
            {
                "week": int(fields.get("week", match.group(1))),
                "title": fields.get("title", ""),
                "category": fields.get("category", ""),
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

    entries.sort(key=lambda e: e["week"])
    (out_dir / "assignments.json").write_text(json.dumps(entries, indent=2) + "\n")


if __name__ == "__main__":
    main()

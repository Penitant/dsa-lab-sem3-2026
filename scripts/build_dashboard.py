#!/usr/bin/env python3
# Reads assignments/weekN.md frontmatter and writes docs/assignments.json.
import json
import re
from pathlib import Path

ASSIGNMENTS_DIR = Path("assignments")
OUTPUT_PATH = Path("docs/assignments.json")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def main():
    entries = []
    for path in sorted(ASSIGNMENTS_DIR.glob("week*.md")):
        fields = parse_frontmatter(path.read_text())
        if fields is None or "week" not in fields:
            continue
        entries.append(
            {
                "week": int(fields["week"]),
                "title": fields.get("title", ""),
                "category": fields.get("category", ""),
                "link": fields.get("link", ""),
            }
        )
    entries.sort(key=lambda e: e["week"])
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(entries, indent=2) + "\n")


if __name__ == "__main__":
    main()

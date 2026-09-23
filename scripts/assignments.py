# Loads and validates assignments/weekN/QUESTION.md frontmatter.
import re
from datetime import date
from pathlib import Path

ASSIGNMENTS_DIR = Path("assignments")
QUESTION_FILE = "QUESTION.md"
WEEK_DIR_RE = re.compile(r"^week(\d+)$")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
REQUIRED_FIELDS = ("title", "week", "category", "start", "end")


class AssignmentError(Exception):
    pass


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


def parse_date(value, field, where):
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise AssignmentError(f"{where}: '{field}' must be YYYY-MM-DD, got '{value}'")


def load(week_dir):
    week_dir = Path(week_dir)
    where = f"{week_dir}/{QUESTION_FILE}"
    dir_match = WEEK_DIR_RE.match(week_dir.name)
    if not dir_match:
        raise AssignmentError(f"{week_dir}: folder must be named weekN")
    question = week_dir / QUESTION_FILE
    if not question.is_file():
        raise AssignmentError(f"{where}: missing")

    fields = parse_frontmatter(question.read_text())
    if fields is None:
        raise AssignmentError(f"{where}: missing frontmatter (--- block at the top)")
    missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]
    if missing:
        raise AssignmentError(f"{where}: missing {', '.join(missing)}")

    if fields["week"] != dir_match.group(1):
        raise AssignmentError(f"{where}: week is {fields['week']} but folder is {week_dir.name}")
    start = parse_date(fields["start"], "start", where)
    end = parse_date(fields["end"], "end", where)
    if end < start:
        raise AssignmentError(f"{where}: end ({end}) is before start ({start})")

    return {
        "week": int(fields["week"]),
        "title": fields["title"],
        "category": fields["category"],
        "start": start,
        "end": end,
        "dir": week_dir,
    }


def load_all():
    """Every assignment, sorted by week. Raises with all problems listed if any file is invalid."""
    assignments, errors = [], []
    for week_dir in sorted(ASSIGNMENTS_DIR.iterdir()):
        if not week_dir.is_dir():
            continue
        try:
            assignments.append(load(week_dir))
        except AssignmentError as e:
            errors.append(str(e))

    starts = {}
    for a in assignments:
        if a["start"] in starts:
            errors.append(f"week{a['week']} and week{starts[a['start']]} have the same start date {a['start']}")
        starts[a["start"]] = a["week"]

    if errors:
        raise AssignmentError("\n".join(errors))
    return sorted(assignments, key=lambda a: a["week"])

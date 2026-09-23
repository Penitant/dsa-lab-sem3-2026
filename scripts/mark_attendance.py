#!/usr/bin/env python3
# Records a PR as a lab submission in the bot-owned Submissions tab.
#
# Reads the PR's changed files on stdin. Each students/<roll_no>/weekN/ folder
# counts as a submission for weekN if today is within that assignment's
# start..end window. The cell is written under the assignment's *start* date
# column as "Submitted <today>", so it lines up with that class's attendance.
# An existing submission is never overwritten.
#
# Prints a Markdown summary for the PR comment.
import argparse
import os
import sys
from datetime import date

import gspread
from google.oauth2.service_account import Credentials

from assignments import ASSIGNMENTS_DIR, WEEK_DIR_RE, AssignmentError, load

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
TAB_NAME = "Submissions"
SUBMITTED = "Submitted"


def set_cell(ws, row, col, value):
    # RAW so Sheets keeps "2026-09-21" as text instead of reformatting it as a date
    ws.update(range_name=gspread.utils.rowcol_to_a1(row, col), values=[[value]], value_input_option="RAW")


def get_or_create_tab(sh):
    try:
        return sh.worksheet(TAB_NAME)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=TAB_NAME, rows=1000, cols=26)
        set_cell(ws, 1, 1, "roll_no")
        return ws


def find_or_add_row(ws, roll_no):
    col_a = ws.col_values(1)
    for i, val in enumerate(col_a, start=1):
        if val == roll_no:
            return i
    row = len(col_a) + 1
    set_cell(ws, row, 1, roll_no)
    return row


def find_or_add_col(ws, header_text):
    header = ws.row_values(1)
    for i, val in enumerate(header, start=1):
        if val == header_text:
            return i
    col = len(header) + 1
    set_cell(ws, 1, col, header_text)
    return col


def group_by_week(roll_no, paths):
    """Returns ({week_folder_name}, [paths not inside a weekN folder])."""
    prefix = f"students/{roll_no}/"
    weeks, stray = set(), []
    for path in paths:
        parts = path[len(prefix):].split("/") if path.startswith(prefix) else []
        if len(parts) >= 2 and WEEK_DIR_RE.match(parts[0]):
            weeks.add(parts[0])
        else:
            stray.append(path)
    return weeks, stray


def check_window(week_name, today):
    """Returns (assignment, None) if a submission is allowed today, else (None, reason)."""
    try:
        a = load(ASSIGNMENTS_DIR / week_name)
    except AssignmentError:
        return None, f"`{week_name}` — there is no such assignment."
    if today < a["start"]:
        return None, f"`{week_name}` — not open yet (opens {a['start']:%d %b})."
    if today > a["end"]:
        return None, f"`{week_name}` — deadline passed ({a['end']:%d %b})."
    return a, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("roll_no")
    parser.add_argument("today", type=date.fromisoformat)
    parser.add_argument("--key-file", default=os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY_FILE"))
    args = parser.parse_args()

    if not args.key_file:
        sys.exit("service account key file not provided (--key-file or GOOGLE_SERVICE_ACCOUNT_KEY_FILE)")

    paths = [line.strip() for line in sys.stdin if line.strip()]
    weeks, stray = group_by_week(args.roll_no, paths)

    open_weeks, problems = [], []
    for week_name in sorted(weeks):
        a, reason = check_window(week_name, args.today)
        if a:
            open_weeks.append(a)
        else:
            problems.append(reason)
    if stray:
        problems.append(
            f"Files must be inside `students/{args.roll_no}/weekN/`. Not counted:\n"
            + "\n".join(f"  - `{p}`" for p in stray)
        )

    recorded, already = [], []
    if open_weeks:
        creds = Credentials.from_service_account_file(args.key_file, scopes=SCOPES)
        ws = get_or_create_tab(gspread.authorize(creds).open_by_key(os.environ["GOOGLE_SHEET_ID"]))
        row = find_or_add_row(ws, args.roll_no)
        for a in open_weeks:
            col = find_or_add_col(ws, a["start"].isoformat())
            current = ws.cell(row, col).value or ""
            if current.startswith(SUBMITTED):
                already.append((a, current))
                continue
            set_cell(ws, row, col, f"{SUBMITTED} {args.today.isoformat()}")
            recorded.append(a)

    lines = []
    for a in recorded:
        lines.append(f"✅ Week {a['week']} submission recorded ({args.today:%d %b}) for the {a['start']:%d %b} class.")
    for a, current in already:
        lines.append(f"ℹ️ Week {a['week']} was already recorded ({current}). Nothing changed.")
    if problems:
        lines.append("❌ Not recorded:")
        lines.extend(f"- {p}" for p in problems)
    if not lines:
        lines.append(f"❌ No files found under `students/{args.roll_no}/weekN/`. Nothing recorded.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

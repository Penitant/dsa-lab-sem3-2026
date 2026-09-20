#!/usr/bin/env python3
# Combines Attendance + Submissions + Roster tabs into docs/attendance.json.
import json
import os
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
OUTPUT_PATH = Path("docs/attendance.json")
ROSTER_TAB_NAME = "Roster"
CLASS_TAB_NAME = "Attendance"
SUBMISSIONS_TAB_NAME = "Submissions"
CLASS_PRESENT_VALUES = {"p", "present"}


def header_index(header, name, tab_name):
    try:
        return header.index(name)
    except ValueError:
        sys.exit(f"'{tab_name}' tab is missing required column '{name}'")


def load_roll_no_to_name(sh):
    ws = sh.worksheet(ROSTER_TAB_NAME)
    header = ws.row_values(1)
    roll_no_col = header_index(header, "roll_no", ROSTER_TAB_NAME)
    name_col = header_index(header, "name", ROSTER_TAB_NAME)

    mapping = {}
    for row in ws.get_all_values()[1:]:
        if len(row) > roll_no_col and row[roll_no_col].strip():
            mapping[row[roll_no_col].strip()] = row[name_col].strip() if len(row) > name_col else ""
    return mapping


def read_dated_tab(sh, tab_name):
    """A 'roll_no' column plus one column per date (any other columns, e.g. 'name', are ignored)."""
    try:
        ws = sh.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        return {}
    rows = ws.get_all_values()
    if not rows:
        return {}
    header = rows[0]
    roll_no_col = header_index(header, "roll_no", tab_name)
    date_cols = [
        (i, h.strip())
        for i, h in enumerate(header)
        if i != roll_no_col and h.strip() and h.strip().lower() != "name"
    ]
    data = {}
    for row in rows[1:]:
        if len(row) <= roll_no_col or not row[roll_no_col].strip():
            continue
        roll_no = row[roll_no_col].strip()
        data[roll_no] = {date: (row[i].strip() if i < len(row) else "") for i, date in date_cols}
    return data


def main():
    key_file = os.environ["GOOGLE_SERVICE_ACCOUNT_KEY_FILE"]
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    creds = Credentials.from_service_account_file(key_file, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)

    class_data = read_dated_tab(sh, CLASS_TAB_NAME)
    submission_data = read_dated_tab(sh, SUBMISSIONS_TAB_NAME)
    roll_no_to_name = load_roll_no_to_name(sh)

    roll_nos = sorted(set(class_data) | set(submission_data))
    dates = sorted({d for v in class_data.values() for d in v} | {d for v in submission_data.values() for d in v})

    students = []
    for roll_no in roll_nos:
        if roll_no not in roll_no_to_name:
            sys.exit(f"roll_no '{roll_no}' has attendance data but no matching row in the '{ROSTER_TAB_NAME}' tab")
        weeks = []
        present_count = 0
        for date in dates:
            class_val = class_data.get(roll_no, {}).get(date, "").lower()
            submitted = submission_data.get(roll_no, {}).get(date, "") == "Submitted"
            present = class_val in CLASS_PRESENT_VALUES and submitted
            present_count += present
            weeks.append({"date": date, "present": present})
        percent = round(100 * present_count / len(weeks)) if weeks else 0
        students.append(
            {
                "roll_no": roll_no,
                "name": roll_no_to_name[roll_no],
                "percent": percent,
                "weeks": weeks,
            }
        )

    OUTPUT_PATH.write_text(json.dumps(students, indent=2) + "\n")


if __name__ == "__main__":
    main()

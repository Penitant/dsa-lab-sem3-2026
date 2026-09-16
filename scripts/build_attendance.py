#!/usr/bin/env python3
# Reads the attendance Google Sheet and writes docs/attendance.json.
# Final attendance per date = AND(Class, GitHub), same rule as the sheet.
import json
import os
import re
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
OUTPUT_PATH = Path("docs/attendance.json")
HEADER_RE = re.compile(r"^(.*) (Class|GitHub)$")
ROSTER_TAB_NAME = "Roster"


def header_index(header, name):
    try:
        return header.index(name)
    except ValueError:
        sys.exit(f"'{ROSTER_TAB_NAME}' tab is missing required column '{name}'")


def load_roll_no_to_name(gc, sheet_id):
    ws = gc.open_by_key(sheet_id).worksheet(ROSTER_TAB_NAME)
    header = ws.row_values(1)
    roll_no_col = header_index(header, "roll_no")
    name_col = header_index(header, "name")

    mapping = {}
    for row in ws.get_all_values()[1:]:
        if len(row) > roll_no_col and row[roll_no_col].strip():
            mapping[row[roll_no_col].strip()] = row[name_col].strip() if len(row) > name_col else ""
    return mapping


def parse_date_columns(header):
    dates = {}
    for i, col in enumerate(header, start=1):
        m = HEADER_RE.match(col or "")
        if not m:
            continue
        date, kind = m.groups()
        dates.setdefault(date, {})[kind] = i
    return dates


def cell_value(row, col_index):
    if not col_index or col_index > len(row):
        return ""
    return row[col_index - 1].strip()


def main():
    key_file = os.environ["GOOGLE_SERVICE_ACCOUNT_KEY_FILE"]
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    creds = Credentials.from_service_account_file(key_file, scopes=SCOPES)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).sheet1
    rows = ws.get_all_values()

    if not rows:
        OUTPUT_PATH.write_text("[]\n")
        return

    header, body = rows[0], rows[1:]
    date_cols = parse_date_columns(header)
    roll_no_to_name = load_roll_no_to_name(gc, sheet_id)

    students = []
    for row in body:
        roll_no = row[0].strip() if row else ""
        if not roll_no:
            continue
        if roll_no not in roll_no_to_name:
            sys.exit(f"roll_no '{roll_no}' from the attendance sheet has no matching row in the '{ROSTER_TAB_NAME}' tab")
        weeks = []
        present_count = 0
        for date in sorted(date_cols):
            cols = date_cols[date]
            present = (
                cell_value(row, cols.get("Class")) == "Present"
                and cell_value(row, cols.get("GitHub")) == "Present"
            )
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

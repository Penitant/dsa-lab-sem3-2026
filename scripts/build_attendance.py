#!/usr/bin/env python3
# Reads the attendance Google Sheet and writes docs/attendance.json.
# Final attendance per date = AND(Class, GitHub), same rule as the sheet.
import json
import os
import re
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
OUTPUT_PATH = Path("docs/attendance.json")
HEADER_RE = re.compile(r"^(.*) (Class|GitHub)$")


def load_roll_no_to_name():
    roster = json.loads(Path("roster.json").read_text())
    return {v["roll_no"]: v["name"] for v in roster.values()}


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
    roll_no_to_name = load_roll_no_to_name()

    students = []
    for row in body:
        roll_no = row[0].strip() if row else ""
        if not roll_no:
            continue
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
                "name": roll_no_to_name.get(roll_no, ""),
                "percent": percent,
                "weeks": weeks,
            }
        )

    OUTPUT_PATH.write_text(json.dumps(students, indent=2) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Combines Attendance + Submissions + Roster tabs into <out_dir>/attendance.json.
# Each record is P (class + PR), C (class only), S (PR only) or A (neither).
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
ROSTER_TAB_NAME = "Roster"
CLASS_TAB_NAME = "Attendance"
SUBMISSIONS_TAB_NAME = "Submissions"
CLASS_PRESENT_VALUES = {"p", "present"}
SUBMISSION_WINDOW_DAYS = 2
RECORD_CODES = {(True, True): "P", (True, False): "C", (False, True): "S", (False, False): "A"}


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


def parse_class_date(date_str):
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        sys.exit(f"'{CLASS_TAB_NAME}' tab has a non-ISO date column: '{date_str}' (expected YYYY-MM-DD)")


def has_submission_in_window(roll_no_submissions, class_date):
    window_end = class_date + timedelta(days=SUBMISSION_WINDOW_DAYS)
    for sub_date_str, value in roll_no_submissions.items():
        if value != "Submitted":
            continue
        try:
            sub_date = date.fromisoformat(sub_date_str)
        except ValueError:
            continue
        if class_date <= sub_date <= window_end:
            return True
    return False


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
    class_dates = sorted({d for v in class_data.values() for d in v})
    class_dates_parsed = {d: parse_class_date(d) for d in class_dates}

    students = []
    for roll_no in roll_nos:
        if roll_no not in roll_no_to_name:
            sys.exit(f"roll_no '{roll_no}' has attendance data but no matching row in the '{ROSTER_TAB_NAME}' tab")
        records = []
        for class_date_str in class_dates:
            class_val = class_data.get(roll_no, {}).get(class_date_str, "").lower()
            class_present = class_val in CLASS_PRESENT_VALUES
            submitted = has_submission_in_window(
                submission_data.get(roll_no, {}), class_dates_parsed[class_date_str]
            )
            records.append(RECORD_CODES[(class_present, submitted)])
        present = records.count("P")
        students.append(
            {
                "roll_no": roll_no,
                "name": roll_no_to_name[roll_no],
                "present": present,
                "percent": round(100 * present / len(records)) if records else 0,
                "records": records,
            }
        )

    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "dates": class_dates,
        "students": students,
    }
    (out_dir / "attendance.json").write_text(json.dumps(payload, indent=1) + "\n")


if __name__ == "__main__":
    main()

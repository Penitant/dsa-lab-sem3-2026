#!/usr/bin/env python3
# Combines Attendance + Submissions + Roster tabs into <out_dir>/attendance.json.
#
# Classes are the Attendance tab's date columns plus every assignment start
# date that has arrived. Each class is worth 1: 0.5 for being marked present
# and 0.5 for a submission recorded under that date in the Submissions tab.
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import gspread
from google.oauth2.service_account import Credentials

from assignments import AssignmentError, load_all

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
ROSTER_TAB_NAME = "Roster"
CLASS_TAB_NAME = "Attendance"
SUBMISSIONS_TAB_NAME = "Submissions"
CLASS_PRESENT_VALUES = {"p", "present"}
SUBMITTED = "Submitted"
TIMEZONE = ZoneInfo("Asia/Kolkata")


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


def submitted_on(value, column_date):
    """'Submitted 2026-09-23' -> '2026-09-23'; a bare 'Submitted' falls back to the column date."""
    if not value.startswith(SUBMITTED):
        return None
    rest = value[len(SUBMITTED):].strip()
    return rest or column_date


def main():
    try:
        assignments = load_all()
    except AssignmentError as e:
        sys.exit(f"Invalid assignments:\n{e}")

    key_file = os.environ["GOOGLE_SERVICE_ACCOUNT_KEY_FILE"]
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    creds = Credentials.from_service_account_file(key_file, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)

    class_data = read_dated_tab(sh, CLASS_TAB_NAME)
    submission_data = read_dated_tab(sh, SUBMISSIONS_TAB_NAME)
    roll_no_to_name = load_roll_no_to_name(sh)

    today = datetime.now(TIMEZONE).date()
    week_by_date = {a["start"].isoformat(): a["week"] for a in assignments if a["start"] <= today}
    sheet_dates = {d for v in class_data.values() for d in v}
    for d in sheet_dates:
        parse_class_date(d)
    class_dates = sorted(sheet_dates | set(week_by_date))

    roll_nos = sorted(set(roll_no_to_name) | set(class_data) | set(submission_data))
    students = []
    for roll_no in roll_nos:
        if roll_no not in roll_no_to_name:
            sys.exit(f"roll_no '{roll_no}' has attendance data but no matching row in the '{ROSTER_TAB_NAME}' tab")
        records = []
        for d in class_dates:
            in_class = class_data.get(roll_no, {}).get(d, "").lower() in CLASS_PRESENT_VALUES
            submitted = submitted_on(submission_data.get(roll_no, {}).get(d, ""), d)
            records.append({"class": in_class, "submitted": submitted})
        score = sum(0.5 * r["class"] + 0.5 * bool(r["submitted"]) for r in records)
        students.append(
            {
                "roll_no": roll_no,
                "name": roll_no_to_name[roll_no],
                "score": score,
                "percent": round(100 * score / len(records)) if records else 0,
                "records": records,
            }
        )

    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated": datetime.now(TIMEZONE).isoformat(timespec="minutes"),
        "classes": [{"date": d, "week": week_by_date.get(d)} for d in class_dates],
        "students": students,
    }
    (out_dir / "attendance.json").write_text(json.dumps(payload, indent=1) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Marks "GitHub: present" for a PR author in the attendance Google Sheet.
# Sheet layout: col A = roll_no, row 1 = dates, starting at col B.
import json
import os
import sys
from datetime import date, timezone, datetime

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

ROSTER_PATH = "roster.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_pr_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    files, page = [], 1
    while True:
        resp = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        files.extend(f["filename"] for f in batch)
        page += 1
    return files


def find_or_append_row(sheet, sheet_id, tab, roll_no):
    result = sheet.values().get(spreadsheetId=sheet_id, range=f"{tab}!A:A").execute()
    col_a = [row[0] if row else "" for row in result.get("values", [])]
    for i, val in enumerate(col_a):
        if val == roll_no:
            return i + 1  # 1-indexed row
    next_row = len(col_a) + 1
    sheet.values().update(
        spreadsheetId=sheet_id,
        range=f"{tab}!A{next_row}",
        valueInputOption="RAW",
        body={"values": [[roll_no]]},
    ).execute()
    return next_row


def find_or_append_date_col(sheet, sheet_id, tab, date_str):
    result = sheet.values().get(spreadsheetId=sheet_id, range=f"{tab}!1:1").execute()
    header = result.get("values", [[]])[0] if result.get("values") else []
    for i, val in enumerate(header):
        if val == date_str:
            return i + 1  # 1-indexed column
    next_col = len(header) + 1 if header else 2  # column A is roll_no
    col_letter = col_num_to_letter(next_col)
    sheet.values().update(
        spreadsheetId=sheet_id,
        range=f"{tab}!{col_letter}1",
        valueInputOption="RAW",
        body={"values": [[date_str]]},
    ).execute()
    return next_col


def col_num_to_letter(n):
    letters = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def main():
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]
    pr_author = os.environ["PR_AUTHOR"]
    token = os.environ["GITHUB_TOKEN"]
    sheet_id = os.environ["SHEET_ID"]
    tab = os.environ.get("ATTENDANCE_SHEET_TAB", "Attendance")

    with open(ROSTER_PATH) as f:
        roster = json.load(f)

    student = roster.get(pr_author)
    if student is None:
        print(f"'{pr_author}' is not in roster.json — skipping attendance.")
        return

    files = get_pr_files(repo, pr_number, token)
    own_prefix = f"students/{pr_author}/"
    offending = [f for f in files if not f.startswith(own_prefix)]
    if offending:
        print(
            f"PR touches files outside {own_prefix}: {offending} — skipping attendance."
        )
        return

    creds_info = json.loads(os.environ["GCP_SA_KEY"])
    creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    date_str = datetime.now(timezone.utc).date().isoformat()
    row = find_or_append_row(sheet, sheet_id, tab, student["roll_no"])
    col = find_or_append_date_col(sheet, sheet_id, tab, date_str)
    cell = f"{tab}!{col_num_to_letter(col)}{row}"
    sheet.values().update(
        spreadsheetId=sheet_id,
        range=cell,
        valueInputOption="RAW",
        body={"values": [["present"]]},
    ).execute()
    print(f"Marked {student['roll_no']} ({pr_author}) present for {date_str} at {cell}.")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# Marks GitHub attendance for a student in the Google Sheet.
# Sheet layout: col A = roll_no, row 1 headers "<date> GitHub" / "<date> Class".
import argparse
import os
import sys

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def github_header(date_str):
    return f"{date_str} GitHub"


def find_or_add_row(ws, roll_no):
    col_a = ws.col_values(1)
    for i, val in enumerate(col_a, start=1):
        if val == roll_no:
            return i
    row = len(col_a) + 1
    ws.update_cell(row, 1, roll_no)
    return row


def find_or_add_col(ws, header_text):
    header = ws.row_values(1)
    for i, val in enumerate(header, start=1):
        if val == header_text:
            return i
    col = len(header) + 1
    ws.update_cell(1, col, header_text)
    return col


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("roll_no")
    parser.add_argument("date")
    parser.add_argument("--key-file", default=os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY_FILE"))
    args = parser.parse_args()

    if not args.key_file:
        sys.exit("service account key file not provided (--key-file or GOOGLE_SERVICE_ACCOUNT_KEY_FILE)")

    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    creds = Credentials.from_service_account_file(args.key_file, scopes=SCOPES)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).sheet1

    row = find_or_add_row(ws, args.roll_no)
    col = find_or_add_col(ws, github_header(args.date))
    ws.update_cell(row, col, "Present")
    print(f"Marked {args.roll_no} present ({args.date}) at row {row}, col {col}.")


if __name__ == "__main__":
    main()

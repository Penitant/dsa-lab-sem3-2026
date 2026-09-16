#!/usr/bin/env python3
# Looks up a roll_no by github_username in the "Roster" tab of the
# attendance Google Sheet. Prints the roll_no and exits 0 if found,
# otherwise prints an error to stderr and exits 1.
import argparse
import os
import sys

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
TAB_NAME = "Roster"


def header_index(header, name):
    try:
        return header.index(name)
    except ValueError:
        sys.exit(f"'{TAB_NAME}' tab is missing required column '{name}'")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("github_username")
    parser.add_argument("--key-file", default=os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY_FILE"))
    args = parser.parse_args()

    if not args.key_file:
        sys.exit("service account key file not provided (--key-file or GOOGLE_SERVICE_ACCOUNT_KEY_FILE)")

    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    creds = Credentials.from_service_account_file(args.key_file, scopes=SCOPES)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).worksheet(TAB_NAME)

    header = ws.row_values(1)
    username_col = header_index(header, "github_username")
    roll_no_col = header_index(header, "roll_no")

    for row in ws.get_all_values()[1:]:
        if len(row) > username_col and row[username_col].strip() == args.github_username:
            roll_no = row[roll_no_col].strip() if len(row) > roll_no_col else ""
            if roll_no:
                print(roll_no)
                return 0
            break

    print(f"'{args.github_username}' not found in '{TAB_NAME}' tab", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

# dsa-lab-sem3-2026

This repo hosts DSA lab assignments and student submissions.

Students fork the repo and submit work via pull request, working in their
own `students/<roll_no>/dayN/` folder. Attendance is tracked automatically
when a student opens a PR.

## Structure

```
roster.json              # github_username -> {roll_no, name}
students/<roll_no>/dayN/ # student submissions, one folder per student
assignments/dayN.md      # assignment text (YAML frontmatter + description)
.github/workflows/       # attendance.yml, triggered on pull_request: [opened]
scripts/                 # mark_attendance.py, called by the workflow
docs/                    # optional GitHub Pages attendance dashboard
```

## For students

1. Fork this repo.
2. Add yourself to `roster.json` (or ask to be added) with your GitHub
   username as the key.
3. For each day's assignment, create `students/<your-roll_no>/dayN/` with
   your solution and open a PR into `main`. One PR per day, touching only
   your own folder.

## Attendance

Opening a PR triggers `.github/workflows/attendance.yml`, which:

1. Looks up the PR author's username in `roster.json`. If not found, it
   comments on the PR and stops — nothing is written to the sheet.
2. Confirms every changed file is under `students/<their-roll_no>/`. If not,
   it comments on the PR explaining the folder rule and stops.
3. If both checks pass, runs `scripts/mark_attendance.py` to write
   "Present" into that student's `GitHub` column for today's date in the
   attendance Google Sheet, via a service account. It never touches the
   `Class` column — that's marked manually by humans separately. Final
   attendance is `AND(Class, GitHub)`, computed in the sheet.

Merging PRs is a separate, manual, batched decision and does not affect
attendance.

### Required repo secrets

Set these under repo Settings → Secrets and variables → Actions:

- `GOOGLE_SERVICE_ACCOUNT_KEY` — the full JSON key for a Google Cloud
  service account with edit access to the attendance sheet. Create it in
  Google Cloud Console (IAM & Admin → Service Accounts → Keys → Add key →
  JSON), then share the Sheet with that service account's email address.
- `GOOGLE_SHEET_ID` — the target Google Sheet's ID, taken from its URL:
  `https://docs.google.com/spreadsheets/d/<THIS_PART>/edit`.

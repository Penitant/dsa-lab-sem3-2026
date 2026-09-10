# dsa-lab-sem3-2026

This repo hosts DSA lab assignments and student submissions.

Students fork the repo and submit work via pull request, working in their
own `students/<id>/dayN/` folder. Attendance is tracked automatically when
a student opens a PR.

## Structure

```
roster.json              # github_username -> {roll_no, name}
students/<id>/dayN/       # student submissions, one folder per student
assignments/dayN.md       # assignment text (YAML frontmatter + description)
.github/workflows/        # attendance.yml, triggered on pull_request: [opened]
.github/scripts/          # mark_attendance.py and its requirements
docs/                      # optional GitHub Pages attendance dashboard
```

## For students

1. Fork this repo.
2. Add yourself to `roster.json` (or ask to be added) with your GitHub
   username as the key.
3. For each day's assignment, create `students/<your-username>/dayN/` with
   your solution and open a PR into `main`. One PR per day, touching only
   your own folder.

## Attendance

Opening a PR triggers `.github/workflows/attendance.yml`, which checks the
PR author against `roster.json`, confirms the PR only touches the author's
own `students/<you>/` folder, and marks "GitHub: present" in a Google Sheet
for that date via a service account. Manual "class present" marking happens
separately, by humans, in the same sheet. Final attendance is
`AND(class present, GitHub present)`, computed in the sheet.

Merging PRs is a separate, manual, batched decision and does not affect
attendance.

### Required repo secrets

- `GCP_SA_KEY` — service account JSON with edit access to the attendance sheet
- `ATTENDANCE_SHEET_ID` — the target Google Sheet's ID

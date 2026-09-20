# dsa-lab-sem3-2026

This repo hosts DSA lab assignments and student submissions.

Students fork the repo and submit work via pull request, working in their
own `students/<roll_no>/dayN/` folder. Attendance is tracked automatically
when a student opens a PR.

## Structure

```
students/<roll_no>/dayN/  # student submissions, one folder per student
assignments/weekN.md      # assignment text (YAML frontmatter + description)
.github/workflows/        # attendance.yml, build-dashboard.yml
scripts/                  # mark_attendance.py, lookup_roster.py, build_dashboard.py
docs/                     # GitHub Pages dashboard (index.html + assignments.json)
```

The roster (`github_username` -> `roll_no`) lives in a "Roster" tab in the
attendance Google Sheet, not in this repo. Edit it directly in the sheet —
there's no git-based roster file to update.

## For students

1. Fork this repo.
2. Make sure you're listed in the "Roster" tab of the attendance Google
   Sheet (ask the instructor if you're not).
3. For each day's assignment, create `students/<your-roll_no>/dayN/` with
   your solution and open a PR into `main`. One PR per day, touching only
   your own folder.

## Attendance

Opening a PR triggers `.github/workflows/attendance.yml`, which:

1. Runs `scripts/lookup_roster.py` to look up the PR author's username in
   the "Roster" tab of the Google Sheet. If not found, it comments on the
   PR and stops — nothing is written to the sheet.
2. Confirms every changed file is under `students/<their-roll_no>/`. If not,
   it comments on the PR explaining the folder rule and stops.
3. If both checks pass, runs `scripts/mark_attendance.py` to write
   "Submitted" into that student's row for today's date in the bot-owned
   "Submissions" tab, via a service account.

The Google Sheet has three tabs:

- **Roster** — `github_username | roll_no | name`. Edited by humans.
- **Attendance** — `roll_no | name | <date>...`, marked `P`/`A` (or
  `Present`/`Absent`) by humans taking physical roll call. The bot never
  writes here.
- **Submissions** — `roll_no | <date>...`, marked `Submitted` by the bot
  when a PR passes the checks above. Auto-created on first write if it
  doesn't exist yet. A blank cell for a student/date means no valid PR was
  opened that day — useful for spotting who to follow up with.

Final attendance is `AND(Attendance, Submissions)` per date, computed by
`scripts/build_attendance.py` when it builds the dashboard — not by a
formula in the sheet itself.

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

## Assignments dashboard

Assignments live at `assignments/weekN.md` (not `dayN.md`), organized by week
rather than calendar date. On every push to `main` that touches
`assignments/**`, `.github/workflows/build-dashboard.yml` regenerates
`docs/assignments.json` from all `weekN.md` frontmatter and pushes it back as
a bot commit.

`docs/assignments.json` is auto-generated — never hand-edit it, your changes
will be overwritten on the next push to `assignments/`. `docs/index.html` is
a static page (served via GitHub Pages) that fetches that JSON and renders
it.

The same page also shows attendance, pulled from `docs/attendance.json`
(also auto-generated, also never hand-edit). `.github/workflows/build-attendance.yml`
runs `scripts/build_attendance.py` — after every `Attendance` workflow run and
on a schedule — to read the full roster's attendance straight from the
Google Sheet and publish it. This publishes every enrolled student's roll_no,
name, and per-date attendance to the public GitHub Pages URL — there is no
per-student privacy gate.

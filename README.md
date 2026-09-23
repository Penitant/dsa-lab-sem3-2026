# DSA Lab — Sem 3

Assignments, submissions and attendance for the Data Structures & Algorithms
lab. Questions and attendance are on the course site (this repo's GitHub
Pages).

- [For students](#for-students)
- [For TAs and faculty](#for-tas-and-faculty)

In the commands below, replace:

- `<owner>` — the account this repo lives under (see the URL of this page)
- `<your-username>` — your GitHub username
- `<roll-no>` — your roll number exactly as on the roster, e.g. `25UG00413`
- `N` — the week number of the assignment

---

## For students

### How attendance works

Every lab is worth **1**:

- **½** for being marked present in class on the lab day, and
- **½** for submitting that week's work before the deadline.

Each assignment shows its dates on the course site, e.g. *21 Sep – 25 Sep*.
You can open your PR on any day in that window, and it counts towards the
21 Sep class. After the deadline the bot won't record it.

For a PR to count:

- your GitHub username must be registered with the TA (send it to them before
  your first PR),
- the PR must change files **only** inside `students/<roll-no>/`, and
- your work must be in the folder for that week: `students/<roll-no>/weekN/`.

The bot comments on every PR saying what it recorded, or why it didn't. If
something went wrong, fix it and open a **new** PR. Pushing to an old PR
doesn't count, because submissions are recorded when a PR is opened. Only
your first submission for a week is kept. Merging happens later and doesn't
affect attendance.

### One-time setup

You need [Git](https://git-scm.com/downloads) and a GitHub account. On
Windows, run the commands in **Git Bash**.

1. **Fork**: open this repo on GitHub and click **Fork** (top right) →
   **Create fork**. This makes your own copy at
   `github.com/<your-username>/dsa-lab-sem3-2026`.

2. **Clone your fork**:

   ```bash
   git clone https://github.com/<your-username>/dsa-lab-sem3-2026.git
   cd dsa-lab-sem3-2026
   ```

3. **Add this repo as `upstream`** so you can get new assignments:

   ```bash
   git remote add upstream https://github.com/<owner>/dsa-lab-sem3-2026.git
   git remote -v
   ```

   You should see `origin` (your fork) and `upstream` (this repo).

4. **Set your name and email**, if you haven't before:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

5. **Install pytest**, used for labs that include tests:

   ```bash
   pip install pytest
   ```

### Every lab

1. **Get the latest assignments and start a fresh branch** from them:

   ```bash
   git fetch upstream
   git switch -c weekN upstream/main
   ```

   Use a new branch for every lab (`week1`, `week2`, …). Each PR must be
   opened fresh; pushing more commits to an old PR won't record attendance.

2. **Read the question** on the course site, or at
   `assignments/weekN/QUESTION.md`.

3. **Create your folder and write your solution**:

   ```bash
   mkdir -p students/<roll-no>/weekN
   ```

   If the week has starter code or tests, copy them into your folder:

   ```bash
   cp assignments/weekN/*.py students/<roll-no>/weekN/
   ```

   Only ever edit files inside `students/<roll-no>/`. Never touch
   `assignments/`, the README, or anyone else's folder.

4. **Run the tests**, if there are any:

   ```bash
   cd students/<roll-no>/weekN
   pytest -v
   cd -
   ```

5. **Commit and push to your fork**:

   ```bash
   git status                        # should list only files under students/<roll-no>/
   git add students/<roll-no>/weekN
   git commit -m "weekN"
   git push -u origin weekN
   ```

6. **Open the pull request**: go to your fork on GitHub. A yellow banner
   says *"weekN had recent pushes"*. Click **Compare & pull request**. Check
   that:

   - **base repository** is `<owner>/dsa-lab-sem3-2026`, **base** is `main`
   - **head repository** is your fork, **compare** is `weekN`

   Then click **Create pull request**.

   Alternatively, with the [GitHub CLI](https://cli.github.com/):

   ```bash
   gh pr create --repo <owner>/dsa-lab-sem3-2026 --base main --head <your-username>:weekN --title "<roll-no> weekN" --body ""
   ```

7. After a minute, check the bot's comment on the PR. ✅ means it's
   recorded. ❌ explains what to fix; fix it and open a new PR before the
   deadline. Your attendance shows up on the course site.

### Common problems

| Problem | Fix |
|---|---|
| Bot says username not in roster | Send your GitHub username and roll number to the TA, then open a new PR. |
| Bot says files outside your folder | You changed something outside `students/<roll-no>/`. Start again from step 1 on a new branch and copy only your files in. |
| `git push` asks for a password | GitHub needs a [personal access token](https://github.com/settings/tokens) or SSH key, not your password. Or run `gh auth login`. |
| PR shows other people's files or old labs | Your branch wasn't created from `upstream/main`. Redo step 1 with a new branch name. |
| `fatal: 'upstream' does not appear to be a git repository` | Run step 3 of the one-time setup. |
| Bot says files must be inside `weekN/` | Put everything in `students/<roll-no>/weekN/`, not directly in `students/<roll-no>/` or a `dayN` folder. |
| Bot says deadline passed | Submissions close at the end date on the site. It can't be recorded late; talk to the TA. |
| Bot says not open yet | The assignment's window hasn't started. Open the PR on or after the start date. |
| Folder is `students/<roll-no>` but PR still rejected | The roll number must match the roster exactly, including upper/lower case. |

Keeping your fork's `main` up to date is optional since you branch from
`upstream/main`, but if you want to:

```bash
git switch main
git pull upstream main
git push origin main
```

---

## For TAs and faculty

### Repo layout

```
assignments/weekN/         # one folder per week: QUESTION.md + tests/starter code
students/<roll-no>/weekN/  # student submissions
docs/index.html            # the course site
scripts/                   # attendance + site build scripts
.github/workflows/         # attendance.yml, deploy-pages.yml
```

### Posting an assignment

1. Create the week's folder with a `QUESTION.md`:

   ```bash
   git switch main && git pull
   mkdir -p assignments/week3
   ```

   `assignments/week3/QUESTION.md`:

   ````markdown
   ---
   title: Binary Search Trees
   week: 3
   category: Trees
   start: 2026-10-05
   end: 2026-10-09
   ---

   # Binary Search Trees

   Implement `insert`, `search` and `delete` in [bst.py](bst.py).

   ```python
   def insert(root, key): ...
   ```

   Run `pytest -v` in your folder to check your solution.
   ````

   All five fields are required:

   | Field | Meaning |
   |---|---|
   | `title` | Shown on the site. |
   | `week` | Must match the folder: `week: 3` goes in `assignments/week3/`. |
   | `category` | Topic, shown on the site. |
   | `start` | The lab day, `YYYY-MM-DD`. Submissions are recorded under this date, so it must be the date of that class's column in the Attendance tab. No two assignments can share a start date. |
   | `end` | Last day a PR is accepted, inclusive, `YYYY-MM-DD` (India time). |

   The body is plain Markdown and is displayed as-is. Relative links like
   `[bst.py](bst.py)` point to files in the same folder.

2. **Optional:** add starter code and tests to the same folder. Every file in
   the folder is listed under the question with a viewer and a download
   button. Tests should import from the starter module by name
   (`from bst import insert`) so they work once students copy both into
   their own folder.

   ```
   assignments/week3/
     QUESTION.md
     bst.py
     test_bst.py
   ```

   Check that the tests fail against the starter code and pass against a
   reference solution before posting. Don't commit the solution.

3. **Push to `main`**:

   ```bash
   git add assignments/week3
   git commit -m "adds week 3"
   git push
   ```

   The site redeploys automatically in about a minute (Actions tab →
   **Deploy pages**). If any `QUESTION.md` is malformed, the deploy fails
   and its log lists every problem; the old site stays up until it's fixed.

To edit or fix an assignment, change the files and push again. PDFs and
slides don't belong in the repo. Put anything needed into `QUESTION.md`.

- **Extending a deadline:** change `end` and push. Takes effect for PRs
  opened after the push.
- **Overlapping labs are fine.** Two weeks' windows can overlap, and a
  student can submit both in one PR (`students/<roll-no>/week1/` and
  `students/<roll-no>/week2/`). Each folder is recorded under its own
  week's `start` date.

### Taking attendance

Attendance lives in the Google Sheet:

| Tab | Columns | Who edits |
|---|---|---|
| **Roster** | `github_username \| roll_no \| name` | TAs |
| **Attendance** | `roll_no \| name \| 2026-09-18 \| 2026-09-22 \| …` | TAs |
| **Submissions** | `roll_no \| <start date>…`, cells like `Submitted 2026-10-07` | bot only |

- **New student:** add a row to **Roster**. A student not on the roster gets
  a bot comment and no attendance.
- **After each class:** add a column to **Attendance** headed with the
  class date as `YYYY-MM-DD` (the same date as that week's `start`), and
  enter `P` for each student who attended. Blank means absent. Type the
  header as plain text: if Sheets reformats it as a date like `05/10/2026`,
  set the column's format to **Plain text** first.
- **Then publish it:** Actions tab → **Deploy pages** → **Run workflow**.
  Sheet edits don't trigger anything by themselves. The site also refreshes
  automatically whenever a student opens a PR.

Each class is scored **½** for `P` in Attendance plus **½** for a submission
under that date in Submissions. The site shows the total and a percentage.

When a PR is opened, `.github/workflows/attendance.yml`:

1. looks up the author in **Roster**, commenting and stopping if not found;
2. checks every changed file is under `students/<roll-no>/`, commenting and
   stopping if not;
3. for each `students/<roll-no>/weekN/` folder in the PR, reads
   `assignments/weekN/QUESTION.md`, and if today (India time) is between
   `start` and `end`, writes `Submitted <today>` under the `start` date
   column in **Submissions**. An existing submission is never overwritten;
4. comments on the PR with what was recorded and why anything wasn't.

To excuse a student or fix a mistake, edit their cell in **Submissions** by
hand (`Submitted 2026-10-07`) and re-run **Deploy pages**.

### Merging PRs

Merging is independent of attendance. Merge in batches whenever convenient.
Only PRs that stay inside the student's own folder should be merged.

### Previewing the site locally

```bash
python scripts/build_site.py _site
python -m http.server -d _site 8000
```

Open <http://localhost:8000>. Attendance won't load locally without the
sheet credentials. That's expected.

### One-time repo setup

Only needed when setting up the repo or after moving it to another account.

1. **Settings → Pages → Source:** GitHub Actions.
2. **Settings → Secrets and variables → Actions**, add:
   - `GOOGLE_SERVICE_ACCOUNT_KEY`: full JSON key of a Google Cloud service
     account (IAM & Admin → Service Accounts → Keys → Add key → JSON). Share
     the sheet with that service account's email as **Editor**.
   - `GOOGLE_SHEET_ID`: from the sheet URL,
     `https://docs.google.com/spreadsheets/d/<THIS_PART>/edit`.
3. Actions tab → **Deploy pages** → **Run workflow** once to publish.

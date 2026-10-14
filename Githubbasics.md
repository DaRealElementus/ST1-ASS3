# Git & GitHub Basics – Team Guide

How we use branches, pull requests (PRs) and reviews for SmartCare A3. You can use the **git CLI** (terminal) or **GitHub Desktop**; both do the same thing. Pick one and stick with it.

> Golden rules
> - **Never commit straight to `main`.** Every change goes on a branch → PR → reviewed by someone else → merged.
> - **Never force-push** (`git push --force`) and never rewrite shared history.
> - **Pull `main` before you start anything** and after every merge.
> - One branch = one small task (one checklist row / one issue).

---

## 1. Key ideas (30-second version)

| Term | What it means |
|---|---|
| **Repo** | The project folder + its full history. Lives on GitHub ("remote", called `origin`) and on your machine ("local"). |
| **Commit** | A saved snapshot of your changes with a message. |
| **Branch** | Your own line of work, split off from `main`, so you don't break anyone else's code. |
| **Push / Pull** | Push = send your commits to GitHub. Pull = get other people's commits from GitHub. |
| **Pull Request (PR)** | A request to merge your branch into `main`. This is where review happens. |
| **Review** | A teammate reads your diff, comments, and either approves or requests changes. |
| **Merge** | Your branch's commits get added to `main`. |

---

## 2. One-time setup

This was explained in the uni notes, im also putting it here. if you use your github account for other repos, please omit the ```--global``` tag so that your uni credentials are safe.

### CLI

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"   # the email on your GitHub account

git clone https://github.com/<owner>/<repo>.git
cd <repo>
```

### GitHub Desktop

1. Install from https://desktop.github.com and sign in with **your own** GitHub account.
2. **File → Clone repository → GitHub.com tab** → pick our repo → **Clone**.

Then run the baseline check (from the checklist):

```bash
cd project
python -m pip install -r requirements-dev.txt
python main.py
python -m pytest        # expect 8 passing
```

---

## 3. The everyday workflow

### Step 1 – Update `main`

**CLI**
```bash
git checkout main
git pull
```
**Desktop:** Current branch → `main`, then click **Fetch origin** → **Pull origin**.

### Step 2 – Create a branch

Name it after the task, e.g. `feature/find-patient`, `test/domain-validation`, `fix/cancel-appointment`.

**CLI**

```bash
git checkout -b feature/find-patient
```

**Desktop:** **Current branch → New branch**, type the name, make sure it's based on `main` → **Create branch**.

### Step 3 – Make changes, then check them

Write code + tests, run `python -m pytest`, then look at what you actually changed:

**CLI**
```bash
git status          # which files changed
git diff            # the exact lines changed
```
**Desktop:** the **Changes** tab shows every file and line changed. Untick anything that shouldn't be committed (caches, `.venv`, secrets, random files).

### Step 4 – Commit
Write a message that says *what and why*, e.g. `Add PatientService.find_patient with not-found tests (FR-02)`.

**CLI**
```bash
git add path/to/file.py tests/test_services.py   # add specific files, not everything blindly
git commit -m "Add PatientService.find_patient with not-found tests (FR-02)"
```
**Desktop:** type a summary in the bottom-left box → **Commit to feature/find-patient**.

Commit small and often. Several commits on one branch is fine.

### Step 5 – Push your branch
**CLI**
```bash
git push -u origin feature/find-patient   # first push of a new branch
git push                                   # later pushes
```
**Desktop:** click **Publish branch** (first time), then **Push origin** after that.

### Step 6 – Open a Pull Request
**On GitHub.com:** open the repo → you'll see a yellow banner *"feature/find-patient had recent pushes"* → **Compare & pull request**.
**Desktop:** **Branch → Create pull request** (opens the same page in your browser).

Fill in:
- **Base:** `main` ← **Compare:** your branch.
- **Title:** short and clear.
- **Description:** what you changed, which issue it closes (`Closes #3`), how you tested it (command + result), and any Copilot use.
- **Reviewers** (right sidebar): add the person listed as Reviewer in `checklist.md`.
- Click **Create pull request**.

> Optional CLI: with the GitHub CLI (`gh`) installed you can do `gh pr create --base main --reviewer <username>`.

### Step 7 – Respond to review
If the reviewer requests changes: fix them **on the same branch**, run the tests again, commit and push. The PR updates automatically – don't open a new one. Reply to each comment ("Fixed in abc123" / explain why not) and click **Resolve conversation**.

### Step 8 – Merge
Once approved and tests pass: on the PR page click **Merge pull request → Confirm merge**, then **Delete branch**.

### Step 9 – Everyone pulls `main`
```bash
git checkout main
git pull
cd project && python -m pytest
git rev-parse HEAD      # this is the SHA to record in the stage file
```
**Desktop:** switch to `main` → **Fetch origin** → **Pull origin**. The SHA is shown in the **History** tab.

---

## 4. How to review a PR

You'll be asked to review – this is assessed, so do it properly and **write your own notes before asking Copilot**.

1. Go to the repo on GitHub → **Pull requests** tab → open the PR (or click the link in your notification email).
2. Read the description – do you know what it's meant to do?
3. Click the **Files changed** tab. This is the diff: green = added, red = removed.
4. **Comment on a specific line:** hover over a line → click the blue **+** → write your comment → **Start a review** (this batches your comments instead of sending each one separately).
5. **Test it yourself** (strongly recommended):
   ```bash
   git fetch
   git checkout feature/find-patient
   cd project && python -m pytest
   ```
   Desktop: **Current branch** → pick their branch → run the tests.
   (Or with `gh`: `gh pr checkout <PR number>`.)
6. Finish: top right **Review changes** → write a summary → choose one:
   - **Comment** – general feedback, no decision yet.
   - **Approve** – good to merge.
   - **Request changes** – something must be fixed first.
7. Switch back to `main` when you're done: `git checkout main`.

### What to look for
- Does it do what the issue / acceptance criteria say (FR/AC numbers)?
- Are there tests, and do they test the failure cases too (wrong input, not found, no mutation on rejection)?
- Do all tests pass – yours and the existing ones?
- Is the code readable? Clear names, no dead/commented-out code, no debug `print`s.
- Any files that shouldn't be there (`__pycache__`, `.venv`, passwords, student IDs, Stage 8 tool files)?
- Is the change focused, or does it touch unrelated stuff?

Be specific and kind: *"`find_patient` returns `None` here but AC-02.2 says it should raise `LookupError`"* beats *"this is wrong"*.

---

## 5. Common problems

| Problem | Fix |
|---|---|
| "I committed on `main` by accident" (not pushed yet) | `git branch my-fix` → `git reset --hard origin/main` → `git checkout my-fix`. Ask someone if unsure. |
| `git push` rejected – "updates were rejected" | Someone pushed first. `git pull` then `git push`. Do **not** use `--force`. |
| Merge conflict | Open the file, find `<<<<<<<`, `=======`, `>>>>>>>` markers, keep the right code, delete the markers, run tests, then `git add <file>` and `git commit`. In Desktop/VS Code you get buttons for "Accept current / incoming / both". |
| My branch is behind `main` | `git checkout main && git pull && git checkout my-branch && git merge main`, fix any conflicts, push. (Or the **Update branch** button on the PR page.) |
| "Which branch am I on?" | `git status` (first line), or the **Current branch** box in Desktop. |
| I want to throw away uncommitted changes to a file | `git restore path/to/file.py` (Desktop: right-click file → **Discard changes**). This can't be undone. |
| Something's weird and I'm scared | Stop, don't force anything, post in the group chat with the output of `git status`. |

---

## 6. Cheat sheet

```bash
git status                         # what's going on
git checkout main && git pull      # get latest main
git checkout -b feature/thing      # new branch
git add <files>                    # stage changes
git commit -m "message"            # save snapshot
git push -u origin feature/thing   # send branch to GitHub (first time)
git push                           # send more commits
git fetch && git checkout <branch> # look at someone else's branch
git log --oneline -5               # recent commits
git rev-parse HEAD                 # current SHA
```

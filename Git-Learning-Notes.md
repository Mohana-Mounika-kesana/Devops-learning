# Git Learning Notes

A beginner-friendly summary of our conversation: what each command does, why to use it, and how to use it safely.

## Topics covered

1. Working directory, staging area, and commit history
2. Checking status and inspecting changes
3. Listing, creating, and switching branches
4. Fetching and pulling remote updates
5. Reading commit history
6. Staging, unstaging, and committing
7. Amending the latest commit
8. Discarding file edits with restore or checkout
9. Rebasing and interactive rebase
10. Reverting commits and aborting a revert
11. Using Vim during a Git commit
12. Undoing a completed revert
13. Saving unfinished work with stash
14. Resolving stash conflicts
15. Pushing branches and rewritten history
16. Basic PowerShell commands, ignore rules, and Git hooks

---

## 1. Understand where your changes are

Git has three main areas:

```text
Working directory        Staging area             Commit history
Your file edits   -->    Selected changes    -->  Saved commits
                  git add                    git commit
```

1. Edit a file: the change is in your working directory.
2. Run `git add`: Git stages a snapshot of the change.
3. Run `git commit`: Git saves the staged snapshot in a commit.

You can edit a file again after staging it. The same file can then have both staged and unstaged changes.

Most commands below are run inside your repository. File paths are generally relative to your current directory.

## 2. Check status and inspect changes

```powershell
git status
```

Use this before and after staging, committing, restoring, switching branches, or reverting.

| State | Meaning |
|---|---|
| Untracked | New file not yet tracked by Git |
| Modified, not staged | Tracked file has edits not selected for the next commit |
| Changes to be committed | Changes are staged |
| Working tree clean | No pending tracked changes or visible untracked files |

Inspect unstaged edits:

```powershell
git diff
```

Inspect staged edits:

```powershell
git diff --staged
```

With short status:

```powershell
git status --short
```

The first status column describes staged changes; the second describes unstaged changes. `??` means untracked.

## 3. Branches

A branch is a movable name pointing to a commit, not a separate physical copy of your project.

List local branches:

```powershell
git branch
```

The `*` marks the current branch.

Switch to an existing branch:

```powershell
git switch feature/update2
```

Older equivalent:

```powershell
git checkout feature/update2
```

Create a new branch at the current commit and switch to it:

```powershell
git switch -c feature/new-work
```

Older equivalent:

```powershell
git checkout -b feature/new-work
```

Correction: `git switch -b` is not valid. Use `git switch -c`; `-b` belongs to `git checkout`.

Check `git status` first. Local changes can follow you when switching branches, or Git can block the switch to prevent overwriting them.

## 4. Fetch versus pull

### Fetch

```powershell
git fetch origin
```

Downloads remote objects and updates remote-tracking references such as `origin/main`.

It does not integrate those changes into your current branch or replace your working files.

```text
origin       = configured remote repository name
main         = local main branch
origin/main  = local record of the remote main branch
```

### Pull

```powershell
git pull origin main
```

Fetches remote `main` and integrates it into your current branch. It does not switch you to `main`.

Integration depends on options and configuration; Git may merge, rebase, or require you to choose.

To update local `main` only when it can move forward without a merge:

```powershell
git switch main
git pull --ff-only origin main
```

To fetch and rebase local work explicitly:

```powershell
git pull --rebase
```

Optional setting for the current repository:

```powershell
git config pull.rebase true
```

This changes future pull behavior in this repository; it is not required for learning rebase. Adding `--global` applies a setting across your repositories.

## 5. Read commit history

| Command | What it shows | When to use it |
|---|---|---|
| `git log` | IDs, authors, dates, and messages | Read commit history |
| `git log --oneline` | Compact summary | Find commit IDs |
| `git log -p` | Commit details plus patches | Inspect actual edits |
| `git log --stat` | File names and line-change counts | See scope of changes |
| `git log --oneline --graph --decorate` | Compact history, graph, branch/tag names | Understand branch relationships |

Limit output:

```powershell
git log -p -2
```

Inspect one commit:

```powershell
git show --stat e86bfcb
git show e86bfcb
```

The first summarizes it; the second shows its patch.

A summary such as `2 insertions(+)` describes line changes. It does not by itself prove a file was newly created; inspect the patch.

If Git opens a pager, press `q` to exit. You can avoid the pager:

```powershell
git --no-pager log --oneline -5
```

## 6. Stage, unstage, and commit

From the repository root, stage one file:

```powershell
git add src/instructions.txt
```

From inside `src`, use:

```powershell
git add instructions.txt
```

Stage changes under your current directory:

```powershell
git add .
```

Review what you selected:

```powershell
git status
git diff --staged
```

Unstage without losing edits:

```powershell
git restore --staged instructions.txt
```

Commit staged changes:

```powershell
git commit -m "Add instructions text file"
```

Unstage means "do not include this change in the next commit yet." It does not mean "discard the edit."

## 7. Amend the latest commit

Use amend when your most recent commit needs correction:

- Add a forgotten related file.
- Include a small related fix.
- Correct the commit message.

A normal additional commit gives:

```text
A -- B -- C
```

Amending replaces the latest commit:

```text
Before: A -- B
After:  A -- B'
```

It does not simply uncommit your changes. The replacement commit has a new ID.

Add a forgotten change while keeping the message:

```powershell
git add instructions.txt
git commit --amend --no-edit
```

Edit the latest commit message:

```powershell
git commit --amend
```

This includes any staged changes too. To change only the message, ensure no content changes are staged.

Correct syntax:

```powershell
git commit --amend --no-edit
```

Incorrect spellings from the terminal history:

```text
git commit -amend
git commit --amend -no-edit
```

Avoid amending commits others depend on without coordination.

## 8. Discard edits to a file

Discard unstaged edits:

```powershell
git restore -- instructions.txt
```

Older equivalent:

```powershell
git checkout -- instructions.txt
```

These restore the working file from the staging area. If the file has no staged changes, that normally means restoring the last committed version.

There must be a space after `--`. Without it, Git interprets the filename as an option:

```text
Incorrect: git checkout --instructions.txt
Correct:   git checkout -- instructions.txt
```

Discard both staged and unstaged changes, restoring from the latest commit:

```powershell
git restore --source=HEAD --staged --worktree -- instructions.txt
```

Warning: these commands discard local changes. Commit or stash work you need first.

An untracked file has no staged or committed version to restore with ordinary `git restore`.

## 9. Rebase

Rebase replays commits on a different starting point.

Before:

```text
A -- B -- C      main
      \
       D -- E    feature
```

After rebasing feature onto main:

```text
A -- B -- C      main
           \
            D' -- E'   feature
```

`D'` and `E'` are new commits with new IDs.

Why use it? To put your feature work on a newer base while keeping a linear history.

Start with a clean working tree:

```powershell
git status
git fetch origin
git switch feature/update2
git rebase origin/main
```

This updates the feature branch, not local `main`.

### Resolve rebase conflicts

1. Open the conflicted files.
2. Choose the intended final content.
3. Remove conflict markers.
4. Stage resolutions.
5. Continue.

```powershell
git add instructions.txt
git rebase --continue
```

Cancel an in-progress rebase:

```powershell
git rebase --abort
```

Omit the commit currently being replayed:

```powershell
git rebase --skip
```

Use `--skip` only when you intend to omit that commit.

### Rebase versus merge

| Rebase | Merge |
|---|---|
| Replays commits on a new base | Combines histories |
| Replayed commits get new IDs | Existing commits keep their IDs |
| Usually gives linear history | Can create a merge commit |

Avoid rebasing shared history without coordination.

### Interactive rebase

```powershell
git rebase -i origin/main
```

| Action | Purpose |
|---|---|
| `pick` | Keep a commit |
| `reword` | Change its message |
| `edit` | Pause to change it |
| `squash` | Combine with the previous commit and edit the message |
| `fixup` | Combine with the previous commit, discarding this message |
| `drop` | Remove the commit |

Example:

```text
pick 12ab34 Add settings page
fixup 56cd78 Fix settings typo
pick 90ef12 Add settings tests
```

The typo fix becomes part of the preceding commit.

For specially named `fixup!` or `squash!` commits:

```powershell
git rebase -i --autosquash origin/main
```

## 10. Revert a commit

Revert creates a new commit that reverses an earlier commit's changes.

```text
Before: A -- B -- C
After:  A -- B -- C -- R
```

`C` remains in history. `R` records the undo.

```powershell
git revert <commit-id>
```

Replace the placeholder with an actual ID, for example:

```powershell
git revert e86bfcb
```

Use revert to undo committed changes while preserving history, particularly on shared branches.

Reverting an older commit does not automatically undo every later commit. Git tries to reverse the selected change against the current files.

### Why your revert initially failed

```text
your local changes would be overwritten by revert
```

You had staged, uncommitted changes. Staging does not permanently save work in a commit. Git stopped to protect your work; a normal revert expects the index to match `HEAD`.

Save work with a commit or stash before retrying.

### Revert conflicts

Resolve the files, stage them, and continue:

```powershell
git add instructions.txt
git revert --continue
```

Cancel an in-progress revert:

```powershell
git revert --abort
```

## 11. Use Vim during a Git commit

Git may open Vim for the revert commit message.

Finish:

1. Press Esc.
2. Type `:wq`.
3. Press Enter.

This saves the message and exits.

To stop the editor from completing the commit:

1. Press Esc.
2. Type `:cq`.
3. Press Enter.

Then inspect the state:

```powershell
git status
```

If a revert remains in progress:

```powershell
git revert --abort
```

Important correction: `:q!` is not a reliable way to cancel a Git commit. Git can still use the existing message. `:cq` exits Vim with an error.

## 12. Undo a completed revert

Your history showed that the revert had already completed:

```text
7973f6f Revert "instructions was added in a text file"
e86bfcb instructions was added in a text file
```

That is why this failed:

```powershell
git revert --abort
```

There was no active operation left to abort.

To undo the completed revert:

```powershell
git revert --no-edit 7973f6f
```

```text
Add files --> Revert removes them --> Revert the revert restores them
```

| Situation | Action |
|---|---|
| Revert is still in progress | `git revert --abort` |
| Revert has completed | `git revert <revert-commit-id>` |

## 13. Stash unfinished work

Stash temporarily saves uncommitted work and normally cleans it out of your working directory.

Think of putting unfinished work in a drawer.

Save staged, unstaged, and untracked changes:

```powershell
git stash push -u -m "Save work before revert"
```

`-u` includes untracked files, but not ignored files.

A stash is local; an ordinary `git push` does not publish it.

### List and inspect stashes

```powershell
git stash list
git stash show --stat 'stash@{0}'
git stash show -p 'stash@{0}'
```

`stash@{0}` is the newest stash; `stash@{1}` is the previous one. Quotes are useful in PowerShell.

### Apply and keep the saved copy

```powershell
git stash apply 'stash@{0}'
```

Also try restoring which edits were staged:

```powershell
git stash apply --index 'stash@{0}'
```

### Apply and remove on success

```powershell
git stash pop
```

If application conflicts, Git normally retains the stash.

### Delete a saved stash

```powershell
git stash drop 'stash@{0}'
```

Only delete it after confirming the work is restored safely. Stash numbering changes after entries are added or removed.

There is no command called `git stash wash`.

## 14. Your stash conflict and how to resolve it

Your error included:

```text
patch does not apply
conflicts in index. Try without --index.
```

After the revert, Git could not recreate the original staged patch against the current file state.

The stash was still saved. We checked that your working tree was clean before retrying:

```powershell
git stash apply
```

Without `--index`, Git does not try to restore the original staging state, but content conflicts can still occur.

The trailing-whitespace warning was not the main failure.

After a conflict, do not repeatedly apply the stash. First check:

```powershell
git status
```

Resolve the files, remove markers, and stage them:

```powershell
git add instructions.txt
git status
```

There is no `git stash --continue`.

Commit the result if ready:

```powershell
git commit -m "Restore saved instructions changes"
```

Or keep the edits without leaving them staged:

```powershell
git restore --staged instructions.txt
```

Keep the stash until you have verified that all saved work is restored correctly.

## 15. Save work before reverting: complete workflow

```powershell
git status
git stash push -u -m "Save work before revert"
git stash list
```

Then revert the intended commit:

```powershell
git revert <commit-id>
```

Finish the revert before restoring your work:

```powershell
git stash apply 'stash@{0}'
git status
```

Resolve conflicts if needed. Review your edits, test as appropriate, and commit when ready.

Only after confirming successful restoration:

```powershell
git stash drop 'stash@{0}'
```

This assumes no other stashes were created in between. If they were, identify the correct entry with `git stash list`.

## 16. Push a branch

```powershell
git push -u origin feature/update2
```

`-u` sets the upstream association. Later, with the appropriate branch checked out, you can usually use:

```powershell
git push
```

If you amend or rebase already-pushed commits, a normal push may be rejected.

For a branch you control, after checking and coordinating:

```powershell
git push --force-with-lease origin feature/update2
```

This is safer than `--force`, but it can still rewrite shared history. It is not a substitute for coordination.

## 17. Revert versus reset

| Revert | Reset |
|---|---|
| Adds a new commit undoing an earlier change | Moves the current branch pointer |
| Preserves the original commit in history | Can remove commits from the current branch's visible history |
| Usually appropriate for shared history | Requires caution with shared history |

Reset's effects on staged and working files depend on its mode. In particular, `git reset --hard` can discard local changes; do not use it as a casual undo command.

## 18. Find previous states with reflog

```powershell
git reflog
```

Records recent local movements of `HEAD`, including many commit, reset, and rebase operations.

It can help find a previous commit after a mistake. Reflog is local and entries expire; it is not a permanent backup.

## 19. PowerShell commands from your history

| Command | Purpose |
|---|---|
| `New-Item instructions.txt -ItemType File` | Create an empty file |
| `Add-Content instructions.txt "hello"` | Append text |
| `Get-Content instructions.txt` | Read a file |
| `Get-ChildItem` | List directory entries |
| `Set-Location src` | Change directory |
| `Set-Location ..` | Move to the parent directory |
| `Get-History` | Show PowerShell session command history |

`Add-Content "hello mona"` does not correctly specify both the intended filename and text. Use:

```powershell
Add-Content instructions.txt "hello mona"
```

Appending repeatedly adds content rather than replacing existing contents.

### Ignore rules

Git ignore rules tell Git which untracked paths to ignore. They do not automatically stop tracking an already committed file.

### Hooks

Git hooks are scripts triggered by events such as committing. The `pre-commit.sample` file is an example, not an automatically active hook.

Do not manually edit Git's internal repository metadata while learning.

## Quick decision guide

| Goal | Command |
|---|---|
| Check current state | `git status` |
| Inspect unstaged edits | `git diff` |
| Inspect staged edits | `git diff --staged` |
| Stage a file | `git add <file>` |
| Unstage but keep edits | `git restore --staged <file>` |
| Discard unstaged edits | `git restore -- <file>` |
| Save staged changes | `git commit -m "Message"` |
| Replace the latest commit | `git commit --amend` |
| Undo a committed change | `git revert <commit-id>` |
| Save unfinished work temporarily | `git stash push -u` |
| Restore saved work | `git stash apply` |
| Replay commits on a newer base | `git rebase origin/main` |
| Cancel an active revert | `git revert --abort` |
| Cancel an active rebase | `git rebase --abort` |

## Five key meanings

```text
restore = discard local edits, or unstage with --staged
amend   = replace the latest commit
revert  = add a commit that undoes another commit
stash   = temporarily save uncommitted work
rebase  = replay commits on a different base
```

Final habit: check `git status`, understand whether work is untracked, unstaged, staged, or committed, and choose the command for that state.

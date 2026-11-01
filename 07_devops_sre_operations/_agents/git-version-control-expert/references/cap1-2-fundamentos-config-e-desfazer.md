# Preface, Introduction, Ch.1 Getting Started and Ch.2 Git Basics (PGEN p.8-68)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; printed EN page = PDF - 6; PT-BR = PDF - 5). A citation `(p.N)` without a sigla = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Note: PDF pages; printed page = N - 6. Page 69 (start of Ch.3) was glanced at and is not part of this range.

## Section map: title -> starting PDF page
- Preface by Scott Chacon -> 8; Preface by Ben Straub -> 9; Dedications -> 10; Contributors -> 11 (list of names, no technical content)
- Introduction (summary of the 10 chapters and 3 appendices) -> 14
- Ch.1 Getting Started -> 16
  - About Version Control -> 16 (Local VCS 16; Centralized VCS 17; Distributed VCS 18)
  - A Short History of Git -> 20
  - What is Git? -> 20 (Snapshots, Not Differences 20; Nearly Every Operation Is Local 21; Git Has Integrity 22; Git Generally Only Adds Data 22; The Three States 22)
  - The Command Line -> 24
  - Installing Git -> 24 (Linux 24; macOS 25; Windows 25; from Source 26)
  - First-Time Git Setup -> 27 (Your Identity 28; Your Editor 28; Your default branch name 29; Checking Your Settings 29)
  - Getting Help -> 30
  - Summary -> 31
- Ch.2 Git Basics -> 32
  - Getting a Git Repository -> 32 (git init 32; git clone 33)
  - Recording Changes to the Repository -> 34
    - Checking the Status of Your Files -> 34; Tracking New Files -> 35; Staging Modified Files -> 36; Short Status -> 37
    - Ignoring Files -> 38; Viewing Your Staged and Unstaged Changes -> 39; Git Diff in an External Tool -> 42
    - Committing Your Changes -> 42; Skipping the Staging Area -> 43
    - Removing Files -> 44; Moving Files -> 45
  - Viewing the Commit History -> 46 (log -p 47; --stat 47-48; --pretty 48; format/specifiers 49; --graph 49; Limiting Log Output 50; -S and path 51; --no-merges 52)
  - Undoing Things -> 52 (--amend 52; Unstaging with reset 53; Unmodifying with checkout 54; git restore 55; unstage with restore 55; unmodify with restore 56)
  - Working with Remotes -> 56 (Showing 57; Adding 58; Fetching and Pulling 58; Pushing 59; Inspecting 59; Renaming/Removing 60)
  - Tagging -> 61 (Listing 61; Creating 62; Annotated 62; Lightweight 63; Tagging Later 63; Sharing 64; Deleting 65; Checking out 66)
  - Git Aliases -> 66 (continues on 67-68)
  - Summary -> 68

## Concepts and definitions (EN term | PT-BR term | definition | page)
- Version control | controle de versao | system that records changes to files over time so specific versions can be recalled; works for almost any type of file, not just code | PGEN p.16
- VCS: benefits | - | revert files or the whole project, compare changes over time, see who changed/introduced a problem and when, and recover from mistakes or lost files at little cost | PGEN p.16
- Local VCS | - | simple local database with the changes; example cited: RCS, which keeps sets of patches and rebuilds any version by adding them up | PGEN p.16-17
- Copying folders as "versioning" | - | common method but very error-prone (overwriting the wrong file) | PGEN p.16
- CVCS (Centralized VCS) | - | a single server with all the versioned files and several clients that check out (CVS, Subversion, Perforce). Advantages: visibility of what others are doing, fine-grained permission control, easier administration. Disadvantage: single point of failure (server down = nobody can collaborate/save; corrupted disk without backup = the whole history is lost except local snapshots) | PGEN p.17-18
- DVCS (Distributed VCS) | - | clients mirror the whole repository with history (Git, Mercurial, Darcs); each clone is a full backup; allows several remotes and workflows impossible in centralized systems (e.g. hierarchical) | PGEN p.18-19
- Origin of Git | - | born after 2005, when the relationship between the Linux kernel community and the company behind BitKeeper ended and the free-of-charge status was revoked; goals: speed, simple design, strong support for non-linear development (thousands of parallel branches), fully distributed, able to handle large projects | PGEN p.20
- Snapshots, not differences | snapshots, nao diferencas | other VCSs store a list of changes per file (delta-based); Git stores a series of snapshots of a mini filesystem; on each commit it "takes a picture" and stores a reference; an unchanged file becomes just a link to the identical copy already stored | PGEN p.20-21
- Nearly every operation is local | - | most operations use only the local disk (history, diff against an old version); you can work and commit offline/without VPN and send later | PGEN p.21-22
- Integrity / SHA-1 | - | everything is checksummed before being stored and is referenced by the checksum; impossible to change content without Git noticing; SHA-1 = 40-character hexadecimal string; Git stores everything by the hash of the content, not by file name | PGEN p.22
- Git generally only adds data | - | almost every action only adds data to the database; hard to erase/undo irreversibly; what is easily lost is what was NOT committed; after a commit it is very hard to lose, especially if you push regularly | PGEN p.22
- Three states | tres estados | modified (changed, not committed), staged (marked, in its current version, to go into the next commit), committed (safely stored in the local database) | PGEN p.22-23
- Working tree | working tree/diretorio de trabalho | a checkout of one version of the project, files extracted from the compressed database for use/editing | PGEN p.23
- Staging area / index | area de preparacao | file (usually inside the Git directory) with information about what will go into the next commit; technical name: "index" | PGEN p.23
- Git directory | diretorio .git | where metadata and the object database live; it is the most important part and what gets copied when cloning | PGEN p.23
- Basic workflow | - | modify in the working tree -> selectively stage -> commit (permanent snapshot in the Git directory) | PGEN p.23
- Tracked vs untracked | rastreado / nao rastreado | tracked = were in the last snapshot or were newly staged (may be unmodified, modified or staged); untracked = everything else. After a clone, everything is tracked and unmodified | PGEN p.34
- Short status columns | - | two columns: left = staging area, right = working tree; `??` untracked, `A` added, `M` modified; `MM` = modified, staged and modified again | PGEN p.37-38
- Glob pattern | - | simplified shell regex: `*` zero or more characters, `[abc]` one of the characters, `?` one character, `[0-9]` range, `**` matches nested directories (`a/**/z`) | PGEN p.38
- Author vs committer | autor / committer | author = who originally wrote the work; committer = who applied it last (e.g. a maintainer who applies a patch) | PGEN p.49
- Remote | remoto | versions of the project hosted on the internet/network; may be read-only or read/write; may even be on the same machine | PGEN p.56
- origin | origin | default name given to the server you cloned from | PGEN p.57
- Remote-tracking branch | - | e.g. `pb/master` after `git fetch pb`; renaming the remote renames these branches | PGEN p.58, 61
- Lightweight tag | tag leve | fixed pointer to a commit, "like a branch that doesn't change"; stores only the commit checksum, no other information | PGEN p.62-63
- Annotated tag | tag anotada | full object in the database: checksum, tagger name/email/date, message, signable/verifiable with GPG; generally recommended | PGEN p.62
- Detached HEAD | - | state when checking out a tag; commits made there belong to no branch and are unreachable except by the exact hash | PGEN p.66
- Alias | alias | command shortcut created via git config (`alias.<name>`); the `!` prefix runs an external command | PGEN p.67-68

## Commands and options (command | what it is for according to the book | page | [DATED]?)
### Configuration and help
- `git --version` | on macOS, running `git` for the first time triggers the offer to install the Xcode Command Line Tools (Mavericks 10.9+) | PGEN p.25
- `git config --system / --global / --local` | reads/writes at the 3 levels: system ([path]/etc/gitconfig), global (~/.gitconfig or ~/.config/git/config), local (.git/config, the default) | PGEN p.27
- `git config --list --show-origin` | lists the settings and which file each comes from | PGEN p.28
- `git config --show-origin <key>` | shows which file had the final word for that value | PGEN p.29-30
- `git config --global user.name "..."` / `user.email ...` | sets the identity used in every commit | PGEN p.28
- `git config --global core.editor <editor>` | sets the message editor (on Windows use the full path) | PGEN p.28
- `git config --global init.defaultBranch main` | changes the name of the initial branch (Git >= 2.28; without it the default is master) | PGEN p.29 | [the book notes it is new; Git's own default was still master according to the book, p.35]
- `git config --list` / `git config <key>` | lists everything / queries one key; repeated key: the last value read wins | PGEN p.29
- `git help <verb>`, `git <verb> --help`, `man git-<verb>`, `git <verb> -h` | full help (3 equivalent forms) and concise help (-h) | PGEN p.30
- `git config --global pull.rebase "false"|"true"` | from Git 2.27, `git pull` warns if pull.rebase is not set; false = fast-forward if possible, otherwise merge commit; true = rebase on pull | PGEN p.59
### Repository
- `git init` | creates the .git subdirectory (repository skeleton); nothing is tracked yet | PGEN p.32
- `git add <files>` + `git commit -m '...'` | start tracking existing files and make the initial commit | PGEN p.33
- `git clone <url> [dir]` | copies almost all data from the server (every version of every file); creates .git, downloads everything and checks out the latest version; the second argument chooses the directory name | PGEN p.33
- Transfer protocols cited | https://, git://, user@server:path/to/repo.git (SSH) | PGEN p.33
### Recording changes
- `git status` | shows the state of each file, the current branch and whether it has diverged from the remote | PGEN p.34-35
- `git status -s` / `--short` | compact two-column output | PGEN p.37
- `git add <path>` | multipurpose: track new files, stage modified ones, mark a merge conflict as resolved; if it is a directory, adds recursively; best thought of as "add exactly this content to the next commit" | PGEN p.36
- `git diff` | with no arguments: working directory x staging area (only what is unstaged); if everything is staged the output is empty | PGEN p.39-40
- `git diff --staged` / `--cached` (synonyms) | staging area x last commit (what goes into the next commit) | PGEN p.40-41
- `git difftool` (`--tool-help`) | view the diffs in an external/graphical tool (emerge, vimdiff etc.) | PGEN p.42
- `git commit` | opens the editor with a message pre-filled with the commented status; lines with `#` are ignored; an empty message aborts | PGEN p.42
- `git commit -v` | also puts the diff in the editor | PGEN p.43
- `git commit -m "msg"` | inline message; the output shows the branch, abbreviated SHA-1, files and lines changed | PGEN p.43
- `git commit -a` | automatically stages every already-tracked file before committing (skips `git add`); does not pick up untracked | PGEN p.43-44
- `git rm <file>` | removes from the staging area AND from the working directory (stages the removal) | PGEN p.44
- `git rm -f` | required if the file was modified or is already staged | PGEN p.44
- `git rm --cached <file>` | stops tracking but keeps the file on disk (useful when you forgot the .gitignore) | PGEN p.44-45
- `git rm log/\*.log`, `git rm \*~` | globs with the backslash because Git does its own expansion in addition to the shell | PGEN p.45
- `git mv source destination` | renames; equivalent to `mv` + `git rm` + `git add`; Git does not record a move explicitly, it detects it afterwards | PGEN p.45-46
### History
- `git log` | commits in reverse chronological order: SHA-1, author, date, message | PGEN p.46
- `git log -p` / `--patch`, `-<n>` (e.g. `-2`) | shows the patch of each commit; limits to the last n | PGEN p.47
- `git log --stat`, `--shortstat`, `--name-only`, `--name-status` | statistics/list of files per commit | PGEN p.47-48, 50
- `git log --pretty=oneline|short|full|fuller|format:"..."` | formats; `format` is useful for machine-parseable output because it does not change between Git versions | PGEN p.48
- Format specifiers | %H hash, %h abbreviated hash, %T tree, %t abbreviated tree, %P parents, %p abbreviated parents, %an/%ae/%ad/%ar author (name, email, date, relative date), %cn/%ce/%cd/%cr committer, %s subject | PGEN p.49
- `git log --graph` | ASCII graph of branches/merges (good with oneline or format) | PGEN p.49
- `git log --abbrev-commit`, `--relative-date`, `--oneline` | short hash; relative date; `--oneline` = `--pretty=oneline --abbrev-commit` | PGEN p.50
- `git log --since/--after`, `--until/--before` | filter by date (e.g. `--since=2.weeks`, "2008-01-15", "2 years 1 day 3 minutes ago") | PGEN p.50
- `git log --author`, `--committer`, `--grep`, `--all-match` | filters; several --author/--grep combine as "any of them"; `--all-match` requires all the --grep | PGEN p.51
- `git log -S <string>` ("pickaxe") | only commits that changed the number of occurrences of the string | PGEN p.51
- `git log -- <path>` | limits to commits that touched the path; always the last option, usually after `--` | PGEN p.51
- `git log --no-merges` | hides merge commits | PGEN p.52
### Undoing
- `git commit --amend` | redoes the last commit using the current staging area; with no changes, it only changes the message; the editor opens with the previous message | PGEN p.52
- `git reset HEAD <file>` | unstage (old form suggested by status) | PGEN p.53 | [DATED: the book itself (p.55) says that, from Git 2.23.0, status suggests `git restore --staged`]
- `git checkout -- <file>` | discards working directory changes by restoring the staged/committed version | PGEN p.54 | [DATED: replaced in practice by `git restore <file>` (book p.55-56, Git 2.23.0+)]
- `git restore --staged <file>` | unstage | PGEN p.55
- `git restore <file>` | discards local changes to the file (replaces it with the staged/committed version) | PGEN p.56
### Remotes
- `git remote` / `git remote -v` | lists short names / with fetch and push URLs | PGEN p.57
- `git remote add <name> <url>` | adds an explicit remote | PGEN p.58
- `git fetch <remote>` | downloads what you do not have yet; does NOT merge or change your current work | PGEN p.58-59
- `git pull` | fetch + merge of the tracked remote branch into the current branch; `clone` sets up the local master to track the remote master | PGEN p.59
- `git push <remote> <branch>` | sends commits; works only with write permission and if nobody pushed before; otherwise it is rejected and you must fetch/integrate first | PGEN p.59
- `git remote show <remote>` | URL, HEAD branch, remote branches (tracked/new/stale), pull/push config | PGEN p.59-60
- `git remote rename <old> <new>` | renames (also changes the names of the remote-tracking branches) | PGEN p.60-61
- `git remote remove|rm <name>` | removes the remote and all associated remote-tracking branches and configs | PGEN p.61
- `git remote prune` | cited in the output of `remote show` as a way to remove "stale" references | PGEN p.60
### Tags
- `git tag [-l|--list] ["pattern"]` | lists in alphabetical order; `-l`/`--list` is REQUIRED when there is a wildcard (e.g. `-l "v1.8.5*"`) | PGEN p.61-62
- `git tag -a v1.4 -m "msg"` | annotated tag; without -m opens the editor | PGEN p.62
- `git tag v1.4-lw` | lightweight tag (no -a, -s or -m) | PGEN p.63
- `git show <tag>` | shows the tag data (annotated) + commit | PGEN p.62-63
- `git tag -a v1.2 <hash>` | tag later, giving the hash (or part of it) at the end | PGEN p.64
- `git push origin <tag>` / `git push origin --tags` | tags are NOT sent by default; `--tags` sends those not yet there, lightweight and annotated | PGEN p.64-65
- `git push <remote> --follow-tags` | sends only the annotated tags | PGEN p.65
- `git tag -d <tag>` | deletes locally; does not delete on the remote | PGEN p.65
- `git push <remote> :refs/tags/<tag>` or `git push origin --delete <tag>` | deletes on the remote (the second is the more intuitive) | PGEN p.65-66
- `git checkout <tag>` / `git checkout -b <branch> <tag>` | view the files of the tag (detached HEAD) / create a branch from it so you can commit | PGEN p.66
### Aliases
- `git config --global alias.co checkout` (br, ci, st analogous) | command shortcuts | PGEN p.67
- `git config --global alias.unstage 'reset HEAD --'` | creates an unstage command; `git unstage fileA` = `git reset HEAD -- fileA` | PGEN p.67 | [DATED: could be `restore --staged`, but the book uses reset]
- `git config --global alias.last 'log -1 HEAD'` | shows the last commit | PGEN p.67
- `git config --global alias.visual '!gitk'` | `!` runs an external command | PGEN p.68

## Step-by-step procedures
### P1. Initial setup (once per machine)
1. Install Git (distro package, Xcode CLT/installer on macOS, Git for Windows or Chocolatey; or build from source) (PGEN p.24-26).
2. Set your identity: `git config --global user.name` and `user.email` (PGEN p.28).
3. Set the editor (`core.editor`; on Windows, the full path of the executable) (PGEN p.28).
4. Optional (2.28+): `init.defaultBranch main` (PGEN p.29).
5. Check with `git config --list` and, if a value is unexpected, `--show-origin` (PGEN p.29-30).

### P2. Getting a repository
1. Existing directory: `cd` into it, `git init` (PGEN p.32).
2. Start tracking: `git add` the desired files and `git commit -m '...'` (PGEN p.33).
3. Or clone: `git clone <url> [dir-name]` (PGEN p.33).

### P3. Daily cycle of recording changes
1. `git status` to see the state (PGEN p.34).
2. New file: `git add <file>` starts tracking and stages it (PGEN p.35-36).
3. Modified file: `git add <file>` to stage; if you edit again after the add, repeat the `git add` (the stage keeps the file as it was at the time of the add) (PGEN p.36-37).
4. Review: `git diff` (unstaged) and `git diff --staged` (staged) (PGEN p.39-41).
5. Commit: `git commit` (editor; `-v` shows the diff) or `git commit -m "..."`; `-a` to skip staging tracked files, with care (PGEN p.42-44).

### P4. Undoing: fix the last commit (amend)
1. If you forgot a file: `git add forgotten_file` (PGEN p.52-53).
2. `git commit --amend` and edit the message (it comes pre-filled) (PGEN p.52).
3. Result: a single commit; the old one is replaced and does not appear in the history (PGEN p.53).
4. Only do this on commits that are still local, not pushed (PGEN p.53).

### P5. Undoing: take a file out of the stage
1. Modern (Git 2.23.0+): `git restore --staged <file>` (PGEN p.55).
2. Old form: `git reset HEAD <file>` (PGEN p.53). The file in the working directory is not touched (PGEN p.54).
3. Check: `git status` shows the file under "Changes not staged for commit" (PGEN p.54-56).

### P6. Undoing: discard local changes to a file
1. Modern: `git restore <file>` (PGEN p.56).
2. Old: `git checkout -- <file>` (PGEN p.54).
3. BEFORE: if you want to keep the changes, use stash or a branch (covered in Ch.3), "generally better" (PGEN p.55).
4. The action is NOT reversible (PGEN p.54, 56).

### P7. Ignoring files
1. Create `.gitignore` (preferably before starting) with one pattern per line (PGEN p.38).
2. If a file was staged by mistake: `git rm --cached <file>` (PGEN p.44-45).

### P8. Remove/rename
1. Remove: `git rm <file>` and commit; if modified/staged, `-f` (PGEN p.44).
2. Rename: `git mv a b` (or mv + git rm + git add, or any tool and do add/rm before the commit) (PGEN p.45-46).

### P9. Working with remotes
1. `git remote -v` to see (PGEN p.57); `git remote add <name> <url>` (PGEN p.58).
2. `git fetch <remote>` and then merge manually, or `git pull` if the branch tracks a remote (PGEN p.58-59).
3. `git push <remote> <branch>`; if rejected, fetch and integrate the others' work first (PGEN p.59).

### P10. Tags
1. List: `git tag`, filter with `-l "pattern"` (PGEN p.61-62).
2. Create annotated: `git tag -a vX -m "..."`; lightweight: `git tag vX` (PGEN p.62-63).
3. Tag an old commit: `git tag -a vX <hash>` (PGEN p.64).
4. Share: `git push origin <tag>` or `--tags` (PGEN p.64-65).
5. Delete locally `git tag -d`; remote `git push origin --delete <tag>` (PGEN p.65-66).
6. To commit from a tag: `git checkout -b <branch> <tag>` (PGEN p.66).

## Decision rules / heuristics / author's recommendations
- Create a .gitignore before starting so you do not commit unwanted files (PGEN p.38).
- What to ignore: generated files (logs, build, .o/.a, editor temporaries `*~`, tmp/pid, generated docs) (PGEN p.38).
- To format a log read by a script: use `--pretty=format`, since it does not change between versions (PGEN p.48).
- To find when a function was added/removed: `git log -S function_name` (PGEN p.51).
- For the history of a file/directory: `git log -- path` (path last) (PGEN p.51).
- If `git diff` is empty but you changed things: probably everything is already staged; use `git diff --staged` (PGEN p.40).
- If a file appears as staged and unstaged at the same time: you changed it after `git add`; run `git add` again (PGEN p.37).
- Prefer annotated tags; use lightweight ones only for temporary use or if you do not want to store the extra information (PGEN p.62).
- To edit the last local commit: --amend; not for already-published commits (PGEN p.53).
- When in doubt between unstage and discard: `git status` itself suggests the right command (PGEN p.53-54, 55-56).
- For a tag on an old commit: give the hash at the end of the command (PGEN p.64).
- To work "on top of" a tag: create a branch (PGEN p.66).
- To configure pull: set `pull.rebase` (false = merge, true = rebase) (PGEN p.59).
- The author recommends learning on the command line (it is the only place where all commands run; GUIs implement a subset) (PGEN p.24).
- `git add` should be understood as "add exactly this content to the next commit" (PGEN p.36).

## Risks, warnings and anti-patterns
- Undoing (Undoing Things) is one of the few areas where you can lose work; some undos are not reversible (PGEN p.52).
- `git checkout -- <file>` and `git restore <file>` are dangerous: they discard uncommitted local changes with no way back; only use when sure (PGEN p.54, 56).
- What was committed can almost always be recovered (including deleted branches and commits overwritten by --amend, see Data Recovery); what was never committed is probably lost forever (PGEN p.55).
- `git commit --amend` replaces the previous commit (it does not "fix" it); do not amend commits already pushed; amend + force push causes problems for collaborators (see The Perils of Rebasing) (PGEN p.53).
- `git reset` can be dangerous, especially with `--hard`; use with `HEAD <file>` to unstage is relatively safe because it does not touch the working directory (PGEN p.54).
- `git commit -a` may include unwanted changes (PGEN p.44).
- `git rm` of a modified or staged file requires `-f` as a safety lock: data not saved in a snapshot is not recoverable by Git (PGEN p.44).
- `git add *` may stage too much (example used to motivate unstaging) (PGEN p.53).
- Doing `git add` and editing afterwards: the commit takes the version from the time of the add, not the current one (PGEN p.37).
- Tags are not sent by a normal `git push`; `git tag -d` does not remove on the server (PGEN p.64-65).
- `git push --tags` also sends lightweight tags; for annotated only use `--follow-tags` (PGEN p.65).
- Commits made in detached HEAD become unreachable (except by hash) if no branch is created (PGEN p.66).
- Checkout of a tag into a new branch: the branch advances and starts to differ from the tag (PGEN p.66).
- `git push` is rejected if someone pushed before you (PGEN p.59).
- A wrong editor config on Windows can cause a confusing state, such as a Git operation ending prematurely during editing (PGEN p.29).
- `git remote remove` also deletes all remote-tracking branches and remote configuration (PGEN p.61).
- `git fetch` integrates nothing; forgetting the manual merge leaves the work outdated (PGEN p.58-59).

## Illustrative examples/cases
- Rakefile with `MM`: modified, staged and modified again, illustrates the two columns of the short status (PGEN p.37-38).
- Two example .gitignore files (`*.[oa]`, `*~`; and `!lib.a`, `/TODO`, `build/`, `doc/*.txt`, `doc/**/*.pdf`) illustrate negation, anchoring, directory and `**` (PGEN p.38-39).
- The github/gitignore repository as a starting point for templates; the Linux kernel has 206 .gitignore files (PGEN p.39).
- Search in Git's own history: author, dates, `--no-merges` and path `t/` = 6 commits out of nearly 40,000 (PGEN p.51-52).
- Clone of libgit2 into a `mylibgit` folder illustrates the 2nd argument of clone (PGEN p.33).
- Paul Boone's remote `pb` in ticgit: fetch creates `pb/master` and `pb/ticgit` (PGEN p.58).
- Aliases `unstage` and `last` (PGEN p.67) and external alias `visual` -> gitk (PGEN p.68).
- Retroactive tag v1.2 on the commit "Update rakefile" (PGEN p.64).

## Dated data / divergences from current practice
- Default branch `master`: the book shows everything with master, but warns that GitHub changed to `main` in mid-2020 and other hosts followed; says Git itself still used master by default; `init.defaultBranch` (Git 2.28+) allows changing it (PGEN p.29, 35). [DATED in hosting practice; check the Git version in use]
- Undoing with `git reset HEAD <file>` and `git checkout -- <file>`: the book shows the old forms first, and then `git restore`/`restore --staged` (Git 2.23.0+), saying that Git now suggests restore (PGEN p.53-56). [DATED: current teaching uses restore; in the book text the status outputs of p.36-48 still show the old hints]
- `git checkout -b <branch> <tag>` and `git checkout <tag>`: the book's own message cites `git switch -c` and `git switch -` (PGEN p.66). [DATED: git switch is the newer command for switching/creating branches]
- `git status` text with "Your branch is up-to-date with 'origin/master'" and "working tree clean": format of that era's version (PGEN p.34); current messages may differ (low extrapolation, just warn).
- 40-character SHA-1 as the checksum mechanism (PGEN p.22); current practice allows SHA-256 in new repositories [DATED, extrapolation: not in these pages].
- `git clone` with `git://` cited as a protocol (PGEN p.33) and remote `git://github.com/...` (PGEN p.57) [DATED: git:// is unauthenticated/unencrypted and discouraged; the preface says the book swapped SSH for HTTP in the examples (PGEN p.8)].
- Tarball version in the build example: git-2.8.0 (PGEN p.27) and 32-bit Notepad++ "at the time of writing" (PGEN p.28) [DATED]. Dependencies and dnf/apt install commands (PGEN p.24, 26); macOS Mavericks 10.9 (PGEN p.25); Windows XP / Vista in the config path (PGEN p.27-28) [DATED].
- IRC: channels #git, #github, #gitlab on the Libera Chat server (PGEN p.30) [possibly dated].
- Example dates and "6 years ago" in the log outputs (PGEN p.49) are illustrative.
- GitHub statistics in the preface (10 million projects, 230 employees) (PGEN p.8) [DATED, historical context of ~2014].

## What the book does NOT say here (gaps / negative checks)
- Does not teach `git switch` or `git restore --source`; only cites switch in the detached HEAD message (PGEN p.66).
- Does not cover `git reset --soft/--mixed/--hard` in detail (refers to Reset Demystified) (PGEN p.54).
- Does not explain `git stash` in these pages (only refers to Ch.3) (PGEN p.55).
- Does not cover `git revert` in these pages.
- Does not detail reflog / data recovery (refers to Data Recovery) (PGEN p.55).
- Does not detail multiple .gitignore / `.git/info/exclude` / global gitignore (refers to `man gitignore`) (PGEN p.39).
- Does not mention `git switch` as a way to switch branches in this part; does not teach `git restore -p`/`git add -p` (the `-p` only appears in the help of `git add`, p.30).
- Does not explain `git pull --rebase` beyond the `pull.rebase` config (PGEN p.59).
- Does not cover `git push --force`/`--force-with-lease` here; only warns that amend + force push causes problems (PGEN p.53).
- Does not show a ready-made `git log --oneline --graph --all` (only the isolated options) (PGEN p.49-50).
- Does not deal with rename tracking in the log (`--follow`) (only says detection is after the fact, p.45).
- Does not describe SHA-256.
- Does not cover `git config --unset`/`--edit`.
- Does not teach how to delete an already-pushed commit or rewrite public history (only warns).
- The chapters on branching, merge, server etc. are not in the range (from p.69 on).


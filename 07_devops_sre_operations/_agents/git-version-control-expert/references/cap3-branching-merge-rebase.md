# Ch. 3 Git Branching (PGEN p.69-110)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; printed EN page = PDF - 6; PT-BR = PDF - 5). A citation `(p.N)` without a sigla = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Note: printed pages = PDF - 6. EN text is legible (typographic apostrophes in the extraction).

## Section map: title -> starting PDF page
- Git Branching (intro) -> 69
- Branches in a Nutshell -> 69 (continues 70-75)
- Creating a New Branch -> 71
- Switching Branches -> 72
- (box) Creating a new branch and switching at the same time / git switch -> 76
- Basic Branching and Merging -> 76
- Basic Branching -> 76
- Basic Merging -> 81
- Basic Merge Conflicts -> 82
- Branch Management -> 85
- (box) Changing a branch name -> 86
- (box) Changing the master branch name -> 87
- Branching Workflows -> 88
- Long-Running Branches -> 88
- Topic Branches -> 89
- Remote Branches -> 91
- Pushing -> 97
- Tracking Branches -> 98
- Pulling -> 100
- Deleting Remote Branches -> 100
- Rebasing -> 101
- The Basic Rebase -> 101
- More Interesting Rebases -> 103
- The Perils of Rebasing -> 106
- Rebase When You Rebase -> 108
- Rebase vs. Merge -> 109
- Summary -> 110

## Concepts and definitions (EN term | PT-BR | definition | page)
- Snapshot (not changeset/diff) | snapshot | Git stores data as a series of snapshots, not of differences | PGEN p.69
- Commit object | objeto commit | contains a pointer to the snapshot (root tree), author name and email, message, and pointers to the parent commit(s): zero parents in the initial commit, one in a normal commit, several in a commit resulting from a merge | PGEN p.69
- blob / tree | blob / tree | blob = contents of a file (SHA-1 checksum per file); tree = lists the directory contents and maps file names to blobs. The 3-file example generates 5 objects: 3 blobs, 1 tree, 1 commit | PGEN p.69
- Branch | branch | lightweight, movable pointer to one of those commits; with each commit the pointer of the current branch advances by itself | PGEN p.70
- master | master | not a special branch; it exists in almost every repository only because git init creates it by default and almost nobody changes it | PGEN p.70 [DATED: see the dated-data section]
- HEAD | HEAD | special pointer that points to the local branch you are on; different from the HEAD of Subversion/CVS | PGEN p.71
- Branch as a file | - | a branch is a simple file with the 40-character SHA-1 of the commit; creating one = writing 41 bytes (40 + newline), which is why it is cheap to create/destroy | PGEN p.75
- Merge base (common ancestor) | - | because each commit records its parents, finding the merge base is automatic and usually easy | PGEN p.75
- Fast-forward | fast-forward | when the commit to merge is reachable by following the history of the current commit (it is directly ahead), Git just moves the pointer; there is no divergent work | PGEN p.79
- Three-way merge | three-way merge | used when history has diverged: uses the two snapshots at the branch tips and the common ancestor | PGEN p.81
- Merge commit | merge commit | new commit created automatically pointing to the snapshot of the three-way merge; special because it has more than one parent | PGEN p.82
- Merge conflict | merge conflict | occurs when the same part of the same file was changed differently in the two branches | PGEN p.82
- Unmerged paths | unmerged paths | files with an unresolved conflict, listed by git status | PGEN p.83
- Conflict markers | - | <<<<<<< HEAD, =======, >>>>>>> branch-name; the top part (up to =======) is the HEAD version (the branch you were on when you ran the merge); the bottom part is that of the merged branch | PGEN p.83
- Long-running branch | long-running branch | branches that are always open for stages of the cycle (e.g.: stable master, develop/next, proposed/pu) | PGEN p.88-89
- Topic branch | topic branch | short-lived branch for a single subject/feature; useful in projects of any size | PGEN p.89
- Remote references | remote references | pointers in remote repositories (branches, tags, etc.); list with git ls-remote <remote> or git remote show <remote> | PGEN p.91
- Remote-tracking branch | remote-tracking branch | local reference that you cannot move, which Git moves on every network communication; marks where the remote branch was at the last connection; name <remote>/<branch> | PGEN p.92
- origin | origin | default name given by git clone to the remote; it is not special (git clone -o booyah produces booyah/master) | PGEN p.92
- Tracking branch / upstream branch | tracking branch / upstream | local branch with a direct relationship to a remote one; on a tracking branch, git pull knows which server to fetch from and what to merge; the tracked branch is the upstream | PGEN p.98-99
- @{upstream} / @{u} | - | shortcut for the upstream of the current branch (e.g.: git merge @{u}) | PGEN p.99
- Rebase | rebase | take the changes (patches) committed on one branch and reapply them on top of another, in the order they were introduced | PGEN p.102-103
- patch-id | patch-id | checksum computed only over the patch introduced by the commit (besides the commit SHA-1); lets Git recognize equivalent rewritten commits | PGEN p.108

## Commands and options
| Command | What it is for according to the book | Page | Dated? |
|---|---|---|---|
| git branch <name> | creates a new branch pointing to the current commit; does NOT switch to it | 71 | |
| git log --oneline --decorate | shows where the branch pointers point | 72 | |
| git checkout <branch> | moves HEAD to the branch and reverts working dir files to its snapshot | 72, 74 | [DATED]: the book already mentions git switch (2.23+) on p.76 |
| git log <branch> ; git log --all | by default git log shows only the history below the current branch; naming the branch or using --all shows the others | 74 | |
| git log --oneline --decorate --graph --all | shows diverged history with pointers | 75 | |
| git checkout -b <new> | creates and switches in one operation (shortcut for git branch + git checkout) | 76-77 | [DATED]: prefer git switch -c |
| git switch <branch> | (Git >= 2.23) switches to an existing branch | 76 | |
| git switch -c <new> / --create | creates and switches | 76 | |
| git switch - | goes back to the previously checked-out branch | 76 | |
| git merge <branch> | integrates <branch> into the current branch (run while on the target branch) | 79, 81 | |
| git branch -d <branch> | deletes a branch; fails if not fully merged | 80, 86 | |
| git branch -D <branch> | forces deletion of an unmerged branch (loses the work) | 86 | |
| git status | lists unmerged paths during a conflict | 83 | |
| git add <file> | marks the file's conflict as resolved | 83-84 | |
| git mergetool | opens a visual merge tool (lists the supported ones if merge.tool is not set) | 84 | |
| git commit | finalizes the merge commit after resolving all conflicts; default message "Merge branch 'iss53'" with a Conflicts section | 84-85 | |
| git branch | lists branches; * marks the current one (where HEAD points) | 85 | |
| git branch -v | last commit of each branch | 85 | |
| git branch --merged / --no-merged [<ref>] | filters branches already/not yet merged into the current one (or into the given ref) | 85-86 | |
| git branch --move <old> <new> | renames a local branch | 87 | |
| git push --set-upstream origin <new> | publishes the renamed/new branch and sets the upstream | 87-88 | |
| git branch --all | lists local and remote (remotes/origin/...) | 87 | |
| git push origin --delete <branch> | deletes a branch on the remote (removes only the pointer) | 87, 100 | |
| git ls-remote <remote> / git remote show <remote> | lists remote references | 91 | |
| git fetch <remote> | fetches missing data and moves remote-tracking branches; does not change the working dir | 94, 100 | |
| git remote add <name> <url> | adds another remote (e.g.: teamone) | 95 | |
| git push <remote> <branch> | sends the branch (expands to refs/heads/x:refs/heads/x) | 97 | |
| git push origin local:remote | publishes a local branch under a different name on the remote (e.g.: serverfix:awesomebranch) | 98 | |
| git config --global credential.helper cache | in-memory credential cache for a few minutes (HTTPS) | 98 | |
| git merge origin/serverfix | merges the remote-tracking branch into the current branch | 98 | |
| git checkout -b <br> <remote>/<br> | creates a local branch that starts from the remote-tracking one and tracks it | 98-99 | |
| git checkout --track origin/serverfix | shortcut for the previous one | 99 | |
| git checkout serverfix | if no local one exists and it matches exactly one remote, creates a tracking branch | 99 | |
| git checkout -b sf origin/serverfix | tracking branch with a different local name | 99 | |
| git branch -u / --set-upstream-to origin/x | sets/changes the upstream of an existing branch | 99 | |
| git branch -vv | shows what each branch tracks and ahead/behind (only data from the last fetch) | 100 | |
| git fetch --all; git branch -vv | updated ahead/behind numbers | 100 | |
| git pull | essentially fetch + merge (in most cases) using the upstream | 100 | |
| git rebase <base> | (while on the topic) reapplies commits of the current branch on top of <base> | 102 | |
| git rebase --onto <newbase> <oldbase> <branch> | replays on newbase the patches of <branch> since it diverged from <oldbase> | 104 | |
| git rebase <basebranch> <topicbranch> | checks out the topic and reapplies it on the base, without a prior checkout | 105 | |
| git push --force | overwrites history on the server (cited in the danger scenario) | 107 | |
| git pull --rebase | fetch + rebase instead of merge | 109 | |
| git config --global pull.rebase true | makes --rebase the default of git pull | 109 | |
| filter-branch | cited as a tool for those who rewrite history before it goes to the mainline | 110 | [DATED]: git-filter-repo is the recommended one today (extrapolation; see below) |

## Step-by-step procedures

### P1. Create a branch, work, go back (p.71-75)
1. git branch testing (new pointer at the current commit; HEAD stays on master) (p.71)
2. git checkout testing (HEAD points to testing) (p.72)
3. Commit: only testing advances; master stays where it was (p.73)
4. git checkout master: HEAD goes back and the working dir goes back to the snapshot of master (p.74)
5. New commits on master diverge from the history; view with git log --oneline --decorate --graph --all (p.74-75)

### P2. Hotfix with fast-forward + feature with merge commit (p.76-82)
1. git checkout -b iss53; commit the work (p.77)
2. Before switching, leave the working dir/staging clean (commit or stash/amend); uncommitted changes that conflict prevent the checkout (p.78)
3. git checkout master; git checkout -b hotfix; commit the fix (p.78)
4. Test; git checkout master; git merge hotfix -> "Fast-forward" (p.79)
5. git branch -d hotfix (master already points to the same place) (p.80)
6. git checkout iss53 and continue; the hotfix is NOT in iss53: bring it in with git merge master or wait for the final merge (p.80-81)
7. git checkout master; git merge iss53 -> "Merge made by the 'recursive' strategy" (three-way, generates a merge commit) (p.81)
8. git branch -d iss53 (p.82)

### P3. Resolve a merge conflict (p.82-85)
1. git merge iss53 -> "CONFLICT (content)... Automatic merge failed; fix conflicts and then commit the result"; Git pauses, does not create the merge commit (p.83)
2. git status: files under "Unmerged paths / both modified" (p.83)
3. Open the file, edit the block between the markers: choose one side or combine; remove the <<<<<<<, =======, >>>>>>> lines completely (p.83)
4. git add on each resolved file (staging = marking as resolved) (p.83-84)
5. Graphical alternative: git mergetool; on exit, you confirm the merge went well and the tool does the staging (p.84)
6. git status should show "All conflicts fixed but you are still merging"; check that everything that had a conflict is staged (p.84)
7. git commit; optionally edit the message explaining how/why you resolved it (p.84-85)
- Note in the commit message: if the merge commit is not correct, the template mentions removing .git/MERGE_HEAD (p.85)

### P4. Rename a local and remote branch (p.86-87)
1. Do not rename a branch in use by collaborators (p.86)
2. git branch --move bad-branch-name corrected-branch-name (local only) (p.87)
3. git push --set-upstream origin corrected-branch-name (p.87)
4. git push origin --delete bad-branch-name removes the old name on the remote (p.87)

### P5. Rename master to main (p.87-88)
1. Consult collaborators and look for references to the old name in code and scripts (p.87)
2. git branch --move master main (p.87)
3. git push --set-upstream origin main (p.88); the old master stays on the remote and collaborators stay on it (p.88)
4. Pending items: dependent projects, test-runner config, build/release scripts, host config (default branch, merge rules), documentation, closing/merging pull requests that target the old branch (p.88)
5. Only after being sure main works like master: git push origin --delete master (p.88)

### P6. Publish and collaborate on a remote branch (p.97-99)
1. git push origin serverfix (explicit; local branches do not sync by themselves) (p.97)
2. Collaborator runs git fetch origin: receives only origin/serverfix (immovable), with no editable local branch (p.98)
3. git merge origin/serverfix OR git checkout -b serverfix origin/serverfix (creates a tracking branch) (p.98)
4. git pull now knows where to fetch from (p.99)

### P7. Delete a remote branch (p.100-101)
1. Make sure the feature was merged into the remote's stable branch (p.100)
2. git push origin --delete serverfix -> "[deleted]" (p.100)
3. It only removes the pointer; the server usually keeps the data until garbage collection, so accidental deletion is often easy to recover from (p.101)

### P8. Basic rebase + fast-forward (p.102-103)
1. git checkout experiment; git rebase master (p.102)
2. Internally: goes to the common ancestor, takes the diff of each commit of the current branch, saves them to temporary files, resets the current branch to the same commit as the base, and applies each change in order (p.102)
3. git checkout master; git merge experiment -> fast-forward (p.102)
4. Result: same final snapshot as the merge, but linear history (p.103)

### P9. Rebase --onto (topic of a topic) (p.103-105)
1. Scenario: server and client (born from server); you want to release client without server (p.103-104)
2. git rebase --onto master server client (p.104)
3. git checkout master; git merge client (fast-forward) (p.105)
4. git rebase master server (without a prior checkout) and then git checkout master; git merge server (p.105)
5. git branch -d client; git branch -d server (p.105)

### P10. If someone force-pushed rewritten history that you had worked on (p.108-109)
1. Avoid a plain git pull: it creates a merge commit reintroducing abandoned commits (p.108)
2. Use git fetch + git rebase teamone/master, or git pull --rebase (p.109)
3. Git determines your unique commits, discards merge commits and those that were already rewritten on the target (via patch-id), and reapplies the rest (p.108-109)
4. Caveat: only works if the rewritten patch is nearly identical to the original (p.109)

## Decision rules / heuristics / author recommendations
- Have a clean working dir when switching branches; if that is not possible, use stash or commit amend (p.78).
- If git branch -d refuses (not fully merged), only use -D if you really want to lose the work (p.86).
- Branches in git branch --merged without * can generally be deleted with -d without losing anything (p.86).
- Fast-forward occurs when the commit to merge is directly ahead; otherwise, three-way merge with a merge commit (p.79, 81).
- To bring a fix from master into a feature branch: git merge master, or wait for the final merge (p.81).
- Local branches exist only locally; branching/merging does not talk to the server (p.91). Use private branches for unshared work and publish only the topic branches for collaboration (p.97).
- When contributing to a project you do not maintain: work on a branch and rebase onto origin/master before sending patches, so the maintainer only has to fast-forward or apply cleanly (p.103).
- Golden rule of rebase: do not rebase commits that exist outside your repository and on which others may have based work (p.106).
- Author's gradation: rebasing commits that never left your machine = ok; commits already pushed but that nobody used as a base = ok; public commits that others may have used = problem (p.109).
- If rewriting public history is unavoidable, tell everyone to run git pull --rebase (p.109).
- Rebase vs merge: two views (history as a faithful, untouchable record vs history as a clean narrative); the author says it is not simple and depends on the team/project (p.109-110).
- Best of both worlds: rebase local changes before sending to clean up the work, never rebase what has already been pushed (p.110).
- Long-running: keep only stable/released code on master; develop/next to test stability; topic branches come in when ready; optional proposed/pu (p.88-89).
- Topic branches: create, work, merge and delete several times a day; eases review and context switching; they can last minutes, days or months (p.89-90).
- The author refers to the Distributed Git chapter for choosing the project's branching scheme (p.91).

## Risks, warnings and anti-patterns
- Checkout overwrites working dir files; if it cannot be done cleanly, Git does not let you switch (p.74, 78).
- git branch -D discards unmerged commits (loss of work) (p.86).
- Renaming a branch in use by collaborators is forbidden by the book's warning (p.86).
- Renaming master/main/mainline breaks integrations, services, utilities and build/release scripts; consult collaborators first (p.87).
- After renaming, the old master stays on the remote and collaborators keep basing work on it (p.88); only delete it after migrating everything (p.88).
- Deleting a remote branch removes only the pointer; data survives until GC (recoverable) (p.101).
- git branch -vv shows ahead/behind from cached data (last fetch), it does not talk to the server (p.100).
- Fetch does not create an editable local branch; only the immovable origin/x (p.98).
- Rebase abandons commits and creates similar new ones; if published and rewritten, collaborators must re-merge and the history becomes confusing (p.106).
- Disaster scenario: someone does git push --force of rebased history; when you git pull you create a merge commit with duplicated commits (same author/date/message) and, if you push, you reintroduce commits the other person wanted to discard (p.107-108).
- Rebase-on-rebase only detects a duplicate if the patches are nearly identical; otherwise it adds a similar commit that probably fails to apply (p.109).
- HTTPS credentials: by default asks for username/password in the terminal on every push; credential.helper cache is the simplest option (p.98).

## Illustrative examples/cases
- Commit of 3 files -> 5 objects (3 blobs, 1 tree, 1 commit): shows the data model (p.69).
- git log --oneline --decorate: shows (HEAD -> master, testing) on the same commit (p.72).
- iss53 + hotfix: interruption flow for an urgent fix; hotfix does a fast-forward, iss53 does a merge commit (p.76-82).
- Conflict in index.html with a different footer between master and iss53 (p.83).
- Branches iss91, iss91v2, dumbidea: discard iss91 (loses C5, C6) and merge the other two (p.90-91).
- git.ourcompany.com and git.team1.ourcompany.com (remote teamone): multiple remotes and teamone/master (p.92-97).
- git branch -vv with "ahead 2" and "ahead 3, behind 1" (p.100).
- client/server with --onto (p.104-105).
- Force-push scenario with commits C4/C4' and rebase to recover (p.106-109).

## Dated data / divergences from current practice
- Default branch master: the book itself shows renaming to main (p.87-88) and cites main in the examples; creating with git init defaults to master in the text (p.70). [DATED] git init today may use init.defaultBranch; GitHub uses main by default (extrapolation).
- git checkout to switch/create a branch (p.72, 77, 98-99): [DATED] the book already notes git switch/-c/- since 2.23 (p.76).
- Merge output "Merge made by the 'recursive' strategy" (p.81): [DATED] recent versions use the ort strategy by default (extrapolation; not on the page).
- git push output with "Counting objects" (p.97): old format; [DATED] today it says "Enumerating objects" (extrapolation).
- git filter-branch (p.110): [DATED] discouraged in favor of git filter-repo (extrapolation).
- Conflict markers shown with "HEAD:index.html" (p.83): old format; today without the path (extrapolation).
- 40-character SHA-1 / 41 bytes (p.75): [DATED] valid for SHA-1 repos; SHA-256 repos use 64 characters (extrapolation).
- git mergetool lists opendiff etc. (p.84): the list of tools varies by version/OS.

## What the book does NOT say here (gaps)
- Does not teach git merge --abort (nor git rebase --abort/--continue/--skip) in this passage; there is no hint on how to abort a conflicting merge (it only mentions removing .git/MERGE_HEAD in the template, p.85).
- Does not cover git merge --no-ff, --squash or --ff-only; does not say how to force a merge commit when a fast-forward would be possible.
- Does not cover git push --force-with-lease (only cites git push --force, p.107).
- Does not cover git rebase -i in this passage (cites rebase and filter-branch as rewriting tools, p.110).
- Does not explain git reflog for recovering commits abandoned by rebase; it only says the server keeps data until GC (p.101).
- Does not teach git stash here (only refers to Stashing and Cleaning, p.78).
- Does not explain conflict resolution during a rebase (only the merge).
- Does not say how to apply git branch -d/-D on remotes via fetch --prune (does not appear).
- Does not detail git pull --ff-only nor pull.ff; only pull.rebase true (p.109).
- Does not talk about branch protection on the host (only "merge rules" on the host, p.88).
- Does not define a branch naming convention.

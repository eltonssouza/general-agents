# Ch. 7 Git Tools part 1: Revision Selection, Interactive Staging, Stash/Clean, Signing, Searching, Rewriting History, Reset Demystified (PGEN p.224-277)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; EN printed page = PDF - 6; PT-BR = PDF - 5). Citation `(p.N)` without an abbreviation = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Note: the "Reset Demystified" section ends with "Summary" (table) on p.277; I read p.224-277 (p.277 is the end of the section; then Advanced Merging begins, out of scope).

## Section map: title -> starting PDF page
- Git Tools (intro) / Revision Selection / Single Revisions / Short SHA-1 -> 224
- Note "A short note about SHA-1" (collision) -> 225 (continues 226)
- Branch References (rev-parse) -> 226
- RefLog Shortnames (reflog, @{n}, git log -g) -> 226 (continues 227)
- Escaping braces in PowerShell -> 228
- Ancestry References (^ and ~) -> 228 (continues 229); Escaping the caret on Windows -> 228
- Commit Ranges / Double Dot -> 230; Multiple Points (^, --not) -> 231; Triple Dot (--left-right) -> 231
- Interactive Staging (git add -i) -> 232; Staging and Unstaging Files -> 232; Staging Patches -> 234
- Stashing and Cleaning -> 236; Migrating to git stash push (warning) -> 236; Stashing Your Work -> 236
- Creative Stashing (--keep-index, -u, -a, --patch) -> 238; Creating a Branch from a Stash -> 239
- Cleaning your Working Directory (git clean) -> 240
- Signing Your Work / GPG Introduction -> 242; Signing Tags -> 242; Verifying Tags -> 243
- Signing Commits -> 244; Everyone Must Sign -> 245
- Searching / Git Grep -> 245-246; Git Log Searching (-S, -G) -> 247; Line Log Search (-L) -> 248
- Rewriting History (intro + cardinal rule) -> 249; Changing the Last Commit (--amend) -> 249
- Changing Multiple Commit Messages (rebase -i) -> 250; Reordering Commits -> 252
- Squashing Commits -> 253; Splitting a Commit -> 254; Deleting a commit (drop) -> 255
- The Nuclear Option: filter-branch -> 255; Removing a File from Every Commit -> 256
- Making a Subdirectory the New Root -> 256; Changing Email Addresses Globally -> 256 (continues 257)
- Reset Demystified / The Three Trees -> 257; The HEAD -> 257; The Index -> 258; The Working Directory -> 258
- The Workflow (figs 137-143) -> 259; The Role of Reset -> 265
- Step 1: Move HEAD (--soft) -> 266; Step 2: Updating the Index (--mixed) -> 267; Step 3: Updating the Working Directory (--hard) -> 268
- Recap -> 269; Reset With a Path -> 270; Squashing (via reset --soft) -> 272
- Check It Out (checkout vs reset): Without Paths -> 276; With Paths -> 277; Summary (cheat-sheet) -> 277

## Concepts and definitions (EN term | PT-BR term | definition | page)
- Short SHA-1 | SHA-1 curto | Git resolves a hash prefix if it has at least 4 characters and is unambiguous (no other object with the same prefix) | PGEN p.224
- --abbrev-commit | commit abbreviation | makes git log use short hashes; default 7 characters, growing if needed to keep uniqueness | PGEN p.225
- Practical prefix length | - | the book says 8 to 10 characters are generally enough; the Linux kernel (Feb/2019, >875 thousand commits, ~7 million objects) had no two SHA-1s equal in the first 12 characters | PGEN p.225
- SHA-1 collision | collision | if a new object has the same hash as a different existing one, Git reuses the old one and you always get the data of the first; organic probability is absurdly low (~2^80 objects for 50%); a synthetic collision was demonstrated in Feb/2017 (shattered.io); Git is moving towards SHA256 and has mitigation code (does not eliminate it) | PGEN p.225-226
- Branch reference | branch reference | the name of a branch can be used where a commit is expected (points to the tip) | PGEN p.226
- rev-parse | - | plumbing that shows the SHA-1 for any reference; low level, not for daily use, but useful to see what is happening | PGEN p.226
- Reflog | reflog | temporary local log of where HEAD and branch refs have been over the last months; updated whenever the tip of a branch changes | PGEN p.226-227
- Reflog is strictly local | - | it only records what you did in your repository; it is not the same in another clone; right after cloning the reflog is (almost) empty; analogy: shell history | PGEN p.227-228
- Ancestry ^ (caret) | - | HEAD^ = parent of the commit; ^N = N-th parent (only useful on merge commits: 1st parent = branch you were on, 2nd parent = merged branch) | PGEN p.228-229
- Ancestry ~ (tilde) | - | HEAD~ is equivalent to HEAD^; HEAD~N walks N times along the first parent (HEAD~3 = HEAD~~~); can be combined: HEAD~3^2 | PGEN p.229
- Double dot A..B | double dot | commits reachable from B that are not reachable from A | PGEN p.230
- Triple dot A...B | triple dot | commits reachable by one of the two refs but not by both | PGEN p.231
- Hunk | - | a chunk of a diff; patch mode presents hunk by hunk | PGEN p.234
- Stash | stash | stack of unfinished work: stores modified tracked files and staged changes; can be reapplied later, even on another branch | PGEN p.236
- git clean | - | removes UNtracked files from the working dir (unlike stash, which keeps them) | PGEN p.240
- GPG signing | GPG signature | Git is cryptographically secure but not foolproof; signing tags/commits lets you verify provenance | PGEN p.242
- Pickaxe | pickaxe | nickname of git log -S: shows only commits that changed the NUMBER of occurrences of the string | PGEN p.247
- Interactive rebase | - | "history rewriter": replays commits from top to bottom (oldest at the top) according to a script you edit | PGEN p.250-251
- filter-branch | "nuclear option" | rewrites in bulk, scriptably, a large part of the history; the book says it is discouraged today (see risks) | PGEN p.255
- Three trees | three trees | HEAD (snapshot of the last commit, next parent), Index (proposed next commit), Working Directory (sandbox); "tree" = collection of files | PGEN p.257
- HEAD | - | pointer to the reference of the current branch, which points to the last commit of the branch; will be the parent of the next commit | PGEN p.257
- Index | staging area | proposed next commit; it is what git commit looks at; technically a flattened manifest, not a tree | PGEN p.258
- Working directory/tree | working directory | unpacks the data of .git into real editable files (sandbox) | PGEN p.258
- Unborn master | - | right after git init, HEAD points to a master branch not yet born | PGEN p.259
- Reset: reset moves the BRANCH that HEAD points to; checkout moves HEAD itself | - | central difference | PGEN p.266, 276
- Reachable history | reachable history | the history you would push; a squashed commit is no longer in it | PGEN p.275

## Commands and options (command | purpose | page | [DATED]?)
### Revision selection
- git show <sha|abbrev|branch|HEAD@{n}|master@{yesterday}> | inspects a commit by full hash, prefix, branch or reflog | p.225-227
- git log --abbrev-commit --pretty=oneline | unique short hashes | p.225
- git rev-parse <ref> | resolves a ref to a full SHA-1 (plumbing) | p.226
- git reflog | lists HEAD movements (HEAD@{0}, @{1}...) | p.226
- git show HEAD@{5} / master@{yesterday} / HEAD@{2.months.ago} | reflog reference by position or by time; only works for data still in the reflog (a few months) | p.227
- git log -g [branch] | reflog formatted like git log | p.227
- git log --pretty=format:'%h %s' --graph | visualizes ancestry | p.228
- git show d921970^2 / HEAD~3 / HEAD~3^2 | second parent / ancestor / combination | p.229
- git log master..experiment | commits in experiment that are not in master | p.230
- git log origin/master..HEAD (or origin/master..) | what will be sent in the push; the omitted side becomes HEAD | p.230-231
- git log refA..refB == git log ^refA refB == git log refB --not refA | equivalent forms; ^ and --not allow more than two refs (e.g. refA refB ^refC / --not refC) | p.231
- git log master...experiment [--left-right] | symmetric difference; --left-right marks the side (< left, > right) | p.231-232
- PowerShell: quotes or backtick on HEAD@{0} ("HEAD@{0}" or HEAD@`{0`}); without escaping it does NOT work | p.228
- cmd.exe (Windows): ^ is special; use HEAD^^ or "HEAD^" | p.228-229
### Interactive staging
- git add -i / --interactive | interactive shell with status, update, revert, add untracked, patch, diff, quit, help | p.232
- At the prompt: u/2 (update) selects files by number (e.g. 1,2); * marks selected; empty Enter applies | p.232-233
- r/3 (revert) | unstages files | p.233-234
- d/6 (diff) | shows the staged diff; equivalent to git diff --cached | p.234
- p/5 (patch) | staging per hunk; options [y,n,a,d,/,j,J,g,e,?]; also k, K, s (split), e (manual edit) | p.234-235
- git add -p / --patch | the same patch mode directly from the command line | p.235-236
- git reset --patch, git checkout --patch, git stash save --patch | patch mode also in reset, checkout and stash | p.236 (reset --patch also confirmed p.272; checkout --patch p.277)
### Stash
- git stash / git stash push | stacks the dirty state and leaves the dir clean | p.236-237
- git stash save | old form; being deprecated in favor of stash push (which allows pathspecs); will not go away soon | p.236 [DATED: book note about the Oct/2017 mailing list]
- git stash list | lists stash@{0}, stash@{1}... | p.237
- git stash apply [stash@{n}] | reapplies (default: the most recent); does NOT remove it from the stack; does not need a clean dir or the same branch; conflicts possible | p.237-238
- git stash apply --index | tries to reapply what was staged too (without --index the staged changes come back as unstaged) | p.238
- git stash drop stash@{n} | removes a stash from the stack | p.238
- git stash pop | apply + immediate drop | p.238
- git stash --keep-index | includes the staged changes in the stash but also leaves them in the index | p.238-239
- git stash -u / --include-untracked | includes untracked files (still NOT ignored) | p.239
- git stash -a / --all | also includes ignored files | p.239
- git stash --patch | interactively chooses what to stash | p.239
- git stash branch <new> | creates a branch at the commit where you were when stashing, reapplies and drops if it applies successfully | p.239-240
### Clean
- git clean -f -d | removes untracked files and subdirectories that become empty; -f required if clean.requireForce is not false | p.240
- git clean -n / --dry-run | shows what would be removed | p.240
- git clean -x | also removes ignored files (e.g. .o) | p.241
- git clean -i | interactive mode (clean, filter by pattern, select by numbers, ask each, quit) | p.241
- git clean -ff (second -f) | needed if there are copied/cloned Git repos (e.g. submodules) inside the working dir; git clean -fd refuses to delete those directories | p.241
- git stash --all | safer alternative to git clean: removes everything but keeps it | p.240
### Signing
- gpg --list-keys / gpg --gen-key | list/generate key | p.242
- git config --global user.signingkey <id> | sets the signing key | p.242
- git tag -s v1.5 -m '...' | signed tag (-s instead of -a) | p.242
- git tag -v <tag> | verifies the signature; requires the signer's public key in the keyring; without it: "Can't check signature: public key not found" | p.243
- git commit -S | signed commit (Git v1.7.9+) | p.244
- git log --show-signature | shows/verifies signatures | p.244
- git log --pretty="format:%h %G? %aN %s" | %G? shows the signature status (G = good, N = none in the example) | p.244
- git merge --verify-signatures <branch> | refuses the merge if there is a commit without a trusted valid signature (Git 1.8.3+) | p.244-245
- git merge --verify-signatures -S <branch> | verifies and signs the resulting merge commit | p.245
- git config --local commit.gpgsign true | signs all commits of the repo by default | p.245
### Search
- git grep [-n|--line-number] <term> | searches a committed tree, working dir or index | p.246
- git grep -c / --count | count per file | p.246
- git grep -p / --show-function | shows the enclosing function | p.246
- git grep --and, -e, \( \), --break, --heading, <tag> | combinations; can search an old version (e.g. v1.8.0) | p.247
- git log -S <string> [--oneline] | commits that changed the number of occurrences of the string (pickaxe) | p.247-248
- git log -G <regex> | variant with a regular expression | p.248
- git log -L :<function>:<file> | history of a function as a series of patches | p.248
- git log -L '/start_regex/',/^}/:file | when Git cannot identify the function; also accepts a line range or a single line | p.249
### Rewriting history
- git commit --amend | redoes the last commit (message and/or content after new staging) | p.249-250
- git commit --amend --no-edit | amend without opening the editor | p.250
- git rebase -i HEAD~N (arg = PARENT of the last commit to edit: HEAD~2^ or HEAD~3 for the last 3) | interactive rebase | p.250
- Script commands: pick, reword, edit, squash, fixup, exec, break, drop, label, reset, merge | p.251 (list), 253
- git rebase --continue / --abort | continue after edit / cancel and return to the original state | p.252, 255
- git reset HEAD^ (inside edit) | mixed reset to split a commit | p.254
- git reflog | recover a previous version of the branch after an unwanted rebase | p.255
- git filter-branch --tree-filter 'rm -f passwords.txt' HEAD | removes a file from all commits; --all for all branches | p.256
- git filter-branch --subdirectory-filter trunk HEAD | makes a subdir the new root; removes commits that did not touch it | p.256
- git filter-branch --commit-filter '...git commit-tree "$@"...' HEAD | changes email/name globally and conditionally | p.256-257
### Reset / checkout
- git cat-file -p HEAD; git ls-tree -r HEAD; git ls-files -s | inspect HEAD and index (plumbing) | p.257-258
- git reset --soft [commit]; git reset [--mixed] [commit]; git reset --hard [commit] | see table below | p.266-269
- git reset [commit] <paths> | path form | p.270
- git reset --soft HEAD~2 + git commit | simple squash | p.272-275
- git checkout [branch] / git checkout [commit] <paths> | see comparison | p.276-277

## Step-by-step procedures
### P1. Locate a commit and inspect it (revision selection)
1. Use the full hash or a unique prefix (>=4 chars; 8-10 is usually enough) in git show (p.224-225).
2. To see the hash of a ref: git rev-parse <ref> (p.226).
3. For "where my branch was before": git reflog, then git show HEAD@{n} or master@{yesterday} (p.226-227).
4. To navigate by ancestry: HEAD^ / HEAD~N / ^2 on merges (p.228-229).

### P2. See what you are going to push / what remains to be merged
1. git log origin/master..HEAD shows local commits not yet on the remote (p.230-231).
2. git log master..experiment shows what experiment has that master does not (p.230).
3. git log --left-right master...experiment to see divergence on both sides (p.231-232).

### P3. Partial commit of a file (patch staging)
1. git add -p (or git add -i, then p/5) (p.234-236).
2. For each hunk answer y/n/s/e... (p.235).
3. git status shows the file as staged and unstaged at the same time (p.235).
4. git commit records only what is staged (p.235).

### P4. Stash work to switch branches (stash)
1. git stash (or git stash push) (p.237).
2. Switch branches, work, come back (p.237).
3. git stash apply --index if you want to preserve what was staged (p.238).
4. git stash drop stash@{n} (or use pop from the start) (p.238).
5. If the stash got old and conflicts: git stash branch <new> (p.239-240).
6. To include new files: git stash -u; including ignored: --all (p.239).

### P5. Clean the working directory safely
1. git clean -d -n (dry run) to see what would go (p.240-241).
2. Consider git stash --all as a safe alternative (p.240).
3. Run git clean -f -d (or -i to choose) (p.240-241).
4. For ignored files: add -x (p.241).

### P6. Sign and verify
1. Have a GPG key (gpg --gen-key) and set user.signingkey (p.242).
2. Tag: git tag -s; verify: git tag -v (p.242-243).
3. Commit: git commit -S; verify: git log --show-signature (p.244).
4. On third-party merges: git merge --verify-signatures [-S] (p.244-245).
5. In the team: ask everyone for git config --local commit.gpgsign true (p.245).

### P7. Find when something came in / history of a function
1. git grep -n <term> [<tag>] for where it exists (p.246-247).
2. git log -S <string> --oneline for when it was introduced/changed; -G for regex (p.247-248).
3. git log -L :function:file for the function's history (p.248).

### P8. Fix the last commit
1. Message: git commit --amend (p.249).
2. Content: make the change, git add, git commit --amend (p.250).
3. Trivial change without touching the message: git commit --amend --no-edit (p.250).
4. Only if it has not been pushed (p.250).

### P9. Edit messages of several commits (rebase -i)
1. git rebase -i HEAD~3 (parent of the last commit to edit) (p.250).
2. In the editor, change pick to edit on the desired commits; the list goes from oldest to newest (p.251-252).
3. Git stops at the commit: git commit --amend, edit the message (p.252).
4. git rebase --continue; repeat for each marked commit (p.252).

### P10. Reorder / remove commits
1. Reorder the script lines; it runs from top to bottom (p.251-253).
2. To remove: delete the line or use drop (p.253, 255). Deleting a line = lost commit (p.251).
3. If you remove everything from the script, the rebase is aborted (p.251).

### P11. Squash via rebase -i
1. Keep pick on the first and change the others to squash (p.253).
2. Save; the editor reopens to combine the messages (p.253-254).
3. Result: a single commit with the changes of the three (p.254).

### P12. Split a commit
1. In the script mark the commit with edit (p.254).
2. When it stops, git reset HEAD^ (mixed: undoes the commit and leaves files unstaged) (p.254).
3. git add + git commit as many times as you want (p.254).
4. git rebase --continue (p.254).
5. The SHA-1s of the commits change (p.255).

### P13. Abort or undo a rebase
1. During: git rebase --abort returns to the pre-rebase state (p.255).
2. After it finishes: git reflog to recover the previous version of the branch (p.255).

### P14. Remove a file from the entire history (filter-branch)
1. Do it on a test branch; then hard-reset master if the result is the desired one (p.256).
2. git filter-branch --tree-filter 'rm -f passwords.txt' HEAD (p.256); --all for all branches (p.256).
3. Prefer git-filter-repo (warning from the book) (p.255).

### P15. Squash with reset --soft
1. git reset --soft HEAD~2 moves the branch to the most recent commit you want to keep (p.273).
2. git commit creates a single commit with the content (p.274-275).

### P16. Unstage a file
1. git reset <file> (= reset --mixed HEAD file) copies the file from HEAD to the index (p.270).
2. To bring the version from another commit into the index: git reset <sha> <file> (p.271-272).

## Decision rules / heuristics / author recommendations
- If you only need a known commit, use a unique short prefix; 8-10 chars are enough (p.225).
- If you want to see what will go up in the push: git log origin/master..HEAD (p.230-231).
- If you want to compare more than two refs: use ^ or --not (double dot only accepts two) (p.231).
- If you want to split changes of a file into distinct commits: patch staging (p.232-236).
- If you are in the middle of work and need to switch branches without committing: stash (p.236).
- If the stash has become old and conflicts: stash branch (p.239-240).
- If you only want to discard untracked files: git clean, but do -n first (p.240-241); or, if you want reversibility, stash --all (p.240).
- If you do not know what git clean will do: always -n first, or -i (p.241).
- If you want to verify the provenance of third-party commits: sign/verify with GPG; consider --verify-signatures (p.242-245).
- If you adopt commit signing in the team: everyone must enable commit.gpgsign, otherwise there will be a lot of work rewriting commits to sign them (p.245); understand GPG before adopting (p.245).
- To search where it exists: git grep; for when it was introduced: git log -S/-G; for the history of a function/lines: git log -L (p.246-249).
- git grep is preferable to grep/ack because it is fast and searches any tree (p.247).
- Rewrite history only locally and before sharing; treat pushed history as final unless there is a good reason (p.249).
- If the change in the commit is trivial and the message is still good: --amend --no-edit; if the content changed a lot, update the message (p.250).
- With filter-branch, run first on a test branch and only then hard-reset master (p.256).
- To remove a file/password from the entire history the book shows tree-filter, but today recommends git-filter-repo (p.255-256).
- Simple squash: reset --soft HEAD~N + commit is usually simpler than rebase -i (p.272).
- Watch the "WD Safe?" column of the reset/checkout table: if NO, stop and think (p.277).
- To switch branches use checkout (safe for the working dir) instead of reset --hard (p.276).

## Risks, warnings and anti-patterns
- RISK (p.249): do not push until you are satisfied; already pushed history should be treated as final.
- RISK (p.250): amend changes the SHA-1 of the commit ("like a mini rebase"); do not amend an already pushed commit.
- RISK (p.250): rebase -i rewrites every commit in the range with a changed message and all descendants; do not include commits already sent to a central server, since that creates an alternative version of the same change and confuses other devs.
- RISK (p.251): removing a line from the rebase -i script LOSES the commit; if the file is emptied, it aborts.
- RISK (p.255): changing SHA-1 (split/squash/etc.) alters the commits in the list; make sure no already shared commit is in it.
- RISK (p.255): deleting/changing a commit rewrites all following ones; the further back, the more commits recreated and the greater the chance of many merge conflicts.
- ESCAPE (p.255): git rebase --abort during; git reflog after it finishes.
- RISK (p.255): filter-branch ("nuclear option") rewrites large parts of history; only use it if the project is not yet public and nobody has based work on the commits.
- WARNING (p.255): filter-branch has many pitfalls and is no longer recommended; use git-filter-repo (Python script).
- RISK (p.256-257): filter-branch --commit-filter to change an email changes the SHA-1 of ALL commits (not only the matching ones), since commits contain the hash of their parents.
- GOOD PRACTICE (p.256): run filter-branch on a test branch, hard-reset afterwards; --all for all branches.
- RISK (p.269): reset --hard is the only dangerous form of reset; it overwrites files in the working dir and cannot be undone; if the work was not committed, it is unrecoverable; if committed, it can be recovered via the reflog.
- Any other form of reset can be easily undone (p.269).
- RISK (p.276-277): checkout <commit> is working-directory safe; checkout [commit] <paths> is NOT (overwrites working dir files, does not move HEAD); reset --hard is NOT safe.
- RISK (p.240): git clean removes untracked files; if you change your mind "many times" there is no way to recover the content. Safe alternative: git stash --all.
- RISK (p.241): -x also removes ignored files (builds etc.); always -n before -f.
- RISK (p.240): clean.requireForce: -f is mandatory unless it is false.
- WARNING (p.241): nested repos (submodules) require a double -f.
- WARNING (p.239): by default stash does NOT save untracked or ignored files; without -u/-a those files stay out (risk of thinking everything was saved).
- WARNING (p.238): stash apply does not restore staged state without --index; apply does not remove the stash (only drop/pop).
- WARNING (p.237-238): apply can generate merge conflicts if something does not apply cleanly.
- WARNING (p.227, 228): the reflog is local and covers only a few months; it is not a shareable backup; a freshly cloned repo has an empty reflog.
- WARNING (p.225-226): SHA-1 collision is practically impossible by chance, but was deliberately demonstrated (2017); Git is moving towards SHA256.
- WARNING (p.242): Git is cryptographically secure but not foolproof; verify third-party commits.
- WARNING (p.245): without a standardized commit.gpgsign, it is hard to keep the team signing.
- WARNING (p.228-229): PowerShell requires escaping/quotes on @{n}; cmd.exe requires ^^ or quotes on ^.
- WARNING (p.236): git stash save is being deprecated (use push).
- Anti-pattern (p.256): committing a huge binary or a password via a careless "git add ." is the typical case that motivates filter-branch.

## Illustrative examples/cases
- Partial hashes of 1c002dd... for git show (p.225).
- reflog showing rebase -i (squash/pick) and merge (p.226-227).
- History with a merge to demonstrate ^ and ~ (p.228-229).
- Figure 136 (history for ranges): master..experiment = D,C; experiment..master = F,E; master...experiment = F,E,D,C (p.230-231).
- git add -i with TODO, index.html, lib/simplegit.rb; hunk of simplegit.rb (n 25 to 30) (p.232-235).
- Stash: stash@{0..2}, apply, --index, drop, pop, --keep-index, -u (new-file.txt), --patch, stash branch testchanges (p.237-240).
- git clean -d -n -x with build.TMP, test.o, tmp/ (p.240-241).
- Signing: signed tag v1.5; Junio's v1.4.2.1 without a public key; signed commit 5c3386c; %G? G/N; merge --verify-signatures fails with "does not have a GPG signature" (p.242-245).
- git grep gmtime_r, #define with LINK/BUF_MAX in v1.8.0 (p.246-247).
- git log -S ZLIB_BUF_MAX and -L :git_deflate_bound:zlib.c (p.247-249).
- rebase -i HEAD~3 with f7f3f6d/310154e/a5f4a0d: edit, reorder+drop, squash, split (p.250-255).
- filter-branch: passwords.txt, trunk, email commit-filter (p.256-257).
- Three-tree workflow with v1 (blue), v2 (red), v3 and figures 137-154 (p.259-276).
- Squash via reset --soft HEAD~2 in a 3-commit repo with file-a.txt/file-b.txt (p.272-275).
- develop vs master: git reset master moves develop; git checkout master moves HEAD (p.276).

## RESET DEMYSTIFIED: operational summary (p.257-277)
### Three trees
| Tree | Role | Page |
|---|---|---|
| HEAD | Snapshot of the last commit; next parent | p.257 |
| Index | Proposal for the next commit | p.257-258 |
| Working Directory | Sandbox | p.257-258 |
- Clean state: git status with no output when the 3 trees are equal (p.261, 265).
- Working dir != index: "Changes not staged for commit" (p.263). Index != HEAD: "Changes to be committed" (p.264).
- git add: copies working dir -> index (p.260). git commit: index -> permanent snapshot, creates the commit and moves the branch (p.261).
- branch checkout: changes HEAD to the new ref, populates the index with the snapshot and copies the index to the working dir (p.265). Clone goes through a similar process (p.265).

### Three steps of reset (always in this order, where to stop)
1. Move the BRANCH that HEAD points to (not HEAD itself). --soft stops here (p.266-267).
2. Make the index look like HEAD. --mixed (default) stops here (p.267-268).
3. Make the working dir look like the index. --hard goes all the way here (p.268-269).
- Recap p.269: "Move the branch HEAD points to (stop here if --soft); make index look like HEAD (stop here unless --hard); make working dir look like index".
- --soft HEAD~ essentially undoes the last git commit, without touching index or working dir; then a new commit is equivalent to --amend (p.267).
- --mixed HEAD~ undoes the commit and all the staging (add + commit) (p.268).
- --hard undoes the commit, the add and all the work in the working dir (p.269).
- git reset with no option and no commit = default --mixed (p.268, 270).

### Reset with a path
- With a path, step 1 is skipped (HEAD is a pointer, it does not point to part of a commit); it runs steps 2 and 3 limited to the files (p.270).
- git reset file.txt = git reset --mixed HEAD file.txt: copies from HEAD to the index; effect: unstage; it is the opposite of git add (p.270-271).
- git reset <commit> file.txt brings that commit's version into the index; the next commit records the reversal even if the working dir never went back to that version (p.271-272).
- reset accepts --patch to unstage per hunk (p.272).
- reset --hard with a path is not possible; checkout [commit] <paths> does the equivalent (p.277).

### checkout vs reset
- Without a path: checkout [branch] ~ reset --hard [branch] (updates the 3 trees) but (1) checkout is working-dir safe: it checks so as not to destroy modified files and tries a trivial merge, updating the unmodified ones; reset --hard replaces everything without checking (p.276). (2) Reset moves the branch HEAD points to; checkout moves HEAD to another branch (p.276).
- With a path: checkout [branch] <paths> updates index and working dir, does not move HEAD, is not safe (p.277).
- checkout accepts --patch (p.277).

### Cheat-sheet table (p.277) - HEAD | Index | Workdir | WD Safe?
Commit level:
| Command | HEAD | Index | Workdir | WD Safe? |
|---|---|---|---|---|
| reset --soft [commit] | REF | NO | NO | YES |
| reset [commit] | REF | YES | NO | YES |
| reset --hard [commit] | REF | YES | YES | NO |
| checkout <commit> | HEAD | YES | YES | YES |
File level:
| reset [commit] <paths> | - | YES | NO | YES |
| checkout [commit] <paths> | - | YES | YES | NO |
- HEAD column: "REF" = moves the reference (branch) HEAD points to; "HEAD" = moves HEAD itself (p.277).

## Dated data / divergences from current practice
- [DATED] git checkout -- <file> and git reset HEAD <file> appear in the git status hints of the examples (p.236-238, 240); today Git suggests git restore / git restore --staged. The book in this part does not mention git restore/switch (check that it does not appear). Reasonable certainty: restore/switch exist since Git 2.23.
- [DATED] git checkout [branch] and git checkout <paths> used to switch branches and discard changes (p.265, 276-277); today git switch/restore separate these functions.
- [DATED] master as the default branch in the examples (p.226-227, 237, 266-276); today the default in many installations/hosts is main.
- [DATED] git stash save deprecated in favor of git stash push (the book already says so, p.236).
- [DATED] filter-branch: the book itself says it is no longer recommended; use git-filter-repo (p.255).
- [DATED] SHA-1: the book mentions migration to SHA256 and collision mitigation (p.226); the transition is still partial, keep the warning as context.
- [DATED] Linux kernel data "Feb/2019" for the object count (p.225) and GPG keys 2048R/2014 examples (p.242); illustrative.
- [DATED] Versions cited: v1.7.9+ for commit -S (p.244), 1.8.3+ for --verify-signatures (p.244). They are historical.
- Note: the book in this part uses GPG signing only; it does not cover signing via SSH or x509 (verify: see Gaps). Reasonable certainty that modern Git supports gpg.format ssh, but this is an EXTRAPOLATION (not on the page).
- The help note of the rebase script (p.251) lists label/reset/merge/break commands (recent Git version); rebase -i also has --rebase-merges (not mentioned here).

## EXTRAPOLATION (not on the page)
- git reflog expires by default (gc.reflogExpire, ~90 days reachable and 30 unreachable): the book only says "a few months" (p.227).
- git restore --staged <file> and git restore <file> replace reset HEAD <file> and checkout -- <file> (not in this section).
- git push --force-with-lease as a safer way to force push after rewriting history (not here).
- git commit --fixup / git rebase -i --autosquash (not here).
- git revert as an alternative that does not rewrite history (not here).
- ORIG_HEAD as a shortcut to undo a reset (not here).

## What the book does NOT say here (gaps)
- It does not say how to push after rewriting history (--force/--force-with-lease) nor how collaborators should recover from rewritten history (that discussion appears in another chapter; not on these pages).
- It does not mention git restore or git switch in this part.
- It does not give the exact reflog expiry time (only "a few months", p.227).
- It does not mention git revert as an alternative to rewriting on these pages.
- It does not say that git stash drop/clear can be undone (the hash shown on drop is the only clue; the book shows the hash in "Dropped stash@{0} (...)", p.238, but does not explain recovery).
- It does not talk about SSH or S/MIME signing; only GPG.
- It does not cover git clean in a safe mode beyond -n/-i; it does not guarantee recovery of the removed files (it says there normally is none).
- It does not mention ORIG_HEAD nor reset --keep/--merge (only --soft/--mixed/--hard).
- It does not cover git rebase --autosquash/--fixup nor --rebase-merges, nor rebase --onto here.
- It does not explain how to make filter-branch clean refs/original or gc to actually purge data; it only shows the commands.
- It gives no guidance on rotating a leaked secret (only removes it from history).


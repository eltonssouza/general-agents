# Ch. 7 Git Tools, part 2: Advanced Merging, Rerere, Debugging, Submodules, Bundling, Replace, Credential Storage (PGEN p.277-341)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; printed EN page = PDF - 6; PT-BR = PDF - 5). A citation `(p.N)` without a sigla = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Note: p.277 starts with the end of the Reset section (checkout with paths + reset/checkout summary table). PDF pages; printed = N-6.

## Section map: title -> starting PDF page
- (end of Reset Demystified) checkout With Paths + Summary/cheat-sheet reset vs checkout -> 277
- Advanced Merging (intro) -> 277
- Merge Conflicts -> 278
- Aborting a Merge -> 279
- Ignoring Whitespace -> 280
- Manual File Re-merging -> 280
- Checking Out Conflicts -> 283
- Merge Log -> 285
- Combined Diff Format -> 286
- Undoing Merges (Fix the references / Reverse the commit) -> 288
- Other Types of Merges: Our or Theirs Preference -> 291
- Subtree Merging -> 292
- Rerere -> 294
- Debugging with Git: File Annotation (blame) -> 301
- Binary Search (bisect) -> 302
- Submodules: Starting with Submodules -> 304
- Cloning a Project with Submodules -> 306
- Working on a Project with Submodules: Pulling in Upstream Changes from the Submodule Remote -> 308
- Pulling Upstream Changes from the Project Remote -> 311
- Working on a Submodule -> 313
- Publishing Submodule Changes -> 315
- Merging Submodule Changes -> 316
- Submodule Tips: foreach, aliases -> 319
- Issues with Submodules: switching branches; subdirectories to submodules -> 321
- Bundling -> 324
- Replace -> 328
- Credential Storage (+ Under the Hood, Custom Credential Cache) -> 336
- Summary -> 341

## Concepts and definitions
- reset vs checkout with paths | checkout [commit] <paths> updates the index AND the working directory with the file from that commit, and does not move HEAD; equivalent to a "reset --hard <paths>" (which reset does not allow); not safe for the workdir; accepts --patch (PGEN p.277)
- "WD Safe?" table (PGEN p.277): reset --soft [commit] moves REF, does not touch index/workdir, safe; reset [commit] moves REF, touches the index, safe; reset --hard [commit] moves REF + index + workdir, NOT safe; checkout <commit> moves HEAD itself, updates index and workdir, safe; reset [commit] <paths> index only, safe; checkout [commit] <paths> index+workdir, NOT safe.
- Git's merge philosophy | Git is smart about deciding when a resolution is unambiguous, but does not try to be "smart" in resolving conflicts automatically (PGEN p.277). Repeated merging of a long-lived branch is easy; you keep the branch up to date by resolving small conflicts frequently (PGEN p.277).
- Stages in the index | during a conflict the index holds 3 versions: stage 1 = common ancestor, stage 2 = yours (ours), stage 3 = from MERGE_HEAD (theirs) (PGEN p.281).
- Combined Diff | git diff format in a conflicted merge: two columns per line; 1st column compares against "ours", 2nd against "theirs"; the <<<<<<< and >>>>>>> markers appear because they are in the workdir but in neither side (PGEN p.286).
- Recursive strategy | default strategy for merging two branches (PGEN p.291). -X options are passed to it.
- Option -Xours/-Xtheirs (recursive) vs strategy -s ours | -X: merges what can be merged and, on conflict, picks one side wholesale, including binaries, without markers. -s ours: "fake merge": creates a merge commit with both parents but completely ignores the other branch, and the result is exactly the code of the current branch (PGEN p.291-292).
- Subtree merge | two projects where one maps to a subdirectory of the other; Git usually notices and merges appropriately (PGEN p.292).
- rerere | "reuse recorded resolution": Git remembers how you resolved a conflict (hunk) and resolves it the same way automatically the next time it sees the same conflict (PGEN p.294).
- git blame | file annotation: shows the last commit that modified each line (partial SHA, author, date, line number, content); a ^ prefix on the SHA indicates a line introduced in the repo's initial commit and never changed (PGEN p.301-302).
- git bisect | binary search through history to find the commit that introduced a problem (PGEN p.302).
- Submodule | lets you keep a Git repository as a subdirectory of another, with separate commits (PGEN p.304).
- .gitmodules | versioned file that maps project URL -> local subdirectory (path/url, optionally branch); it is pushed/pulled with the project, and is how other clones know where to fetch from (PGEN p.305).
- Mode 160000 | special entry: records a commit as a directory entry (neither subdirectory nor file); Git sees the submodule as a specific commit of that repo, it does not track the content (PGEN p.305-306).
- Detached HEAD in the submodule | after "git submodule update" the sub-repo has no working branch; commits made there may be lost on the next update (PGEN p.313).
- git bundle | packs data that would go through a push into a single binary file, transportable by e-mail/USB, unpacked in another repo (PGEN p.325).
- git replace | makes Git "pretend" that one object is another; objects remain immutable; useful for swapping a commit in the history without rewriting everything (e.g.: git filter-branch) (PGEN p.328). Stored in refs/replace/<sha> (PGEN p.336).
- Plumbing | commit-tree, read-tree, ls-files, diff-tree are low-level commands, not for daily use (PGEN p.331).
- Credential helper | program separate from Git (git-credential-<name>) called according to credential.helper; actions get/store/erase (PGEN p.338).

## Commands and options
- git merge --abort | tries to return to the pre-merge state; can only fail to revert perfectly if there were uncommitted/unstashed changes in the workdir when the merge started (PGEN p.280)
- git reset --hard HEAD | alternative for "starting over": goes back to the last commit, loses uncommitted work (PGEN p.280)
- git status -sb | shows "UU file" for a conflict (PGEN p.279-280)
- git merge -Xignore-all-space / -Xignore-space-change | options of the default strategy; the first ignores whitespace entirely, the second treats sequences of spaces as equivalent; use by aborting and redoing the merge (PGEN p.280)
- git show :1:file > ...; :2:; :3: | extracts common/ours/theirs from the conflict (PGEN p.281)
- git ls-files -u | plumbing: lists the SHA-1 of the blobs of the 3 stages (PGEN p.281, 297)
- git merge-file -p ours common theirs > file | re-merges a single file from the 3 versions; accepts --ours (PGEN p.281, 292)
- git diff --ours / --theirs / --base | compares the merge result (workdir) against each side/stage; --ours shows what the merge introduced relative to your branch (PGEN p.282-283); use -b to strip whitespace when comparing with a non-"clean" version (PGEN p.282)
- git clean -f | cleans temporary files created in the manual re-merge (PGEN p.283)
- git checkout --conflict=diff3|merge <file> | recreates the file with fresh conflict markers; diff3 includes the "base" version (marker |||||||); merge is the default (PGEN p.284-285, 300)
- git config --global merge.conflictstyle diff3 | makes diff3 the default (PGEN p.285)
- git checkout --ours / --theirs <file> | picks one whole side for the file, without merging; useful for binaries or to bring only some files from one side (PGEN p.285)
- git log --oneline --left-right HEAD...MERGE_HEAD | lists unique commits of each side (triple dot) (PGEN p.285)
- git log --oneline --left-right --merge | only commits from both sides that touch a file currently in conflict; with -p shows only the diffs of the conflicted file (PGEN p.285-286)
- git diff (in a conflicted merge) | shows only what is still in conflict, as a Combined Diff (PGEN p.286)
- git show <merge-commit> / git log --cc -p -1 | displays the combined diff of a merge, to see later how it was resolved (PGEN p.287)
- git reset --hard HEAD~ | undoes a local merge commit not yet published (PGEN p.288-289)
- git revert -m 1 HEAD | creates a commit that undoes a merge; -m 1 indicates parent 1 (mainline, HEAD at merge time) as the one to keep (PGEN p.289)
- git revert ^M (revert of the revert) | "undoes the undo" before re-merging the topic (PGEN p.290)
- git merge -Xours / -Xtheirs <branch> | see above (PGEN p.291-292)
- git merge -s ours <branch> | fake merge (PGEN p.292)
- git remote add X url; git fetch X --no-tags; git checkout -b rack_branch X/master | brings an external project in as a separate branch (PGEN p.292-293)
- git read-tree --prefix=rack/ -u rack_branch | reads a branch's root tree into a subfolder of the current index/workdir (PGEN p.293)
- git merge --squash -s recursive -Xsubtree=rack rack_branch | brings upstream updates into the subdirectory, pre-populating the message, stopping before the commit (PGEN p.294)
- git diff-tree -p rack_branch | compare the subdirectory with the project's branch (plain git diff does not work) (PGEN p.294)
- git config --global rerere.enabled true | turns on rerere; alternative: create .git/rr-cache in a repo (PGEN p.295)
- git rerere status / git rerere diff / git rerere | status lists files with a recorded preimage; diff shows the state of the resolution in progress; git rerere (no args) reapplies the recorded resolution, e.g. after git checkout --conflict=merge (PGEN p.296-297, 300)
- git blame -L a,b <file> | annotates only lines a..b (PGEN p.301)
- git blame -C -L a,b <file> | detects where code copied/moved from ANOTHER file came from; shows the original commit instead of the commit where it was copied (PGEN p.302)
- git bisect start / bad [commit] / good <commit> | starts the search; marks the bad one and the last known good one; Git checks out the middle commit (PGEN p.302-303)
- git bisect good | git bisect bad | mark the current commit according to the test; when done it prints "first bad commit" (PGEN p.303)
- git bisect reset | returns HEAD to where it was before (PGEN p.303)
- git bisect start HEAD v1.0 ; git bisect run <script> | automates: the script must exit 0 if good and non-zero if bad; can be make, make tests etc. Pass bad first, good second in start (PGEN p.304)
- git submodule add <url> [path] | adds a submodule; default path = repo name (PGEN p.304-305)
- git diff --cached --submodule / git diff --submodule | readable diff of the submodule; git config --global diff.submodule log makes it the default (PGEN p.306, 308)
- git clone --recurse-submodules <url> | clones and initializes/updates submodules, including nested ones (PGEN p.307)
- git submodule init + git submodule update | manual sequence after a clone without --recurse-submodules (PGEN p.307); git submodule update --init [--recursive] combines them (PGEN p.308)
- git fetch + git merge origin/master inside the submodule | manual way to update (PGEN p.308)
- git submodule update --remote [name] [--merge|--rebase] | fetches and updates the submodule to the remote branch (default: branch pointed to by the remote HEAD) (PGEN p.309, 313-314)
- git config -f .gitmodules submodule.<name>.branch stable | sets the tracked branch for everyone (without -f, only local in .git/config) (PGEN p.309)
- git config status.submodulesummary 1 | status shows a summary of the submodule commits (PGEN p.310)
- git log -p --submodule | see the submodule's commit log afterwards (PGEN p.311)
- git pull --recurse-submodules (since 2.14); submodule.recurse true (for pull since 2.15) | updates submodules after the pull; applies to all commands that have the flag except clone (PGEN p.312)
- git submodule sync --recursive | copies the new URL from .gitmodules to the local config when upstream changed the submodule URL (PGEN p.312-313)
- git push --recurse-submodules=check|on-demand | check: fails if submodule commits were not published; on-demand: pushes the submodule first; defaults via git config push.recurseSubmodules (PGEN p.315-316)
- git submodule foreach '<cmd>' | runs a command in each submodule (stash, checkout -b, diff) (PGEN p.319-320)
- git checkout --recurse-submodules <branch> (Git >= 2.13) | aligns submodules when switching branches (PGEN p.322-323); git config submodule.recurse true (>=2.14) (PGEN p.323)
- git rm -r <dir> before submodule add | required to convert a tracked subdirectory into a submodule (PGEN p.323-324)
- git clean -ffdx | removes a leftover submodule directory (PGEN p.322)
- git bundle create file.bundle HEAD master | creates a bundle; you must list each ref/range; include HEAD if it will be cloned (PGEN p.325)
- git clone file.bundle dir | clones from the bundle; without HEAD in the bundle use -b <branch> (PGEN p.325-326)
- git bundle create x.bundle master ^<sha> | only a range of commits (PGEN p.326)
- git bundle verify / list-heads | validates and checks prerequisites; lists heads (PGEN p.327)
- git fetch x.bundle master:other-master | imports from the bundle into a local branch (PGEN p.327)
- git commit-tree <tree> | creates a commit with no parent (plumbing) (PGEN p.331)
- git rebase --onto <newbase> <point> | replays recent history on top of a base commit (PGEN p.332)
- git replace <commit> <replacement> | replaces; refs in refs/replace/; shareable via push (PGEN p.334-336)
- git config --global credential.helper cache|store|osxkeychain... | chooses the helper; helpers accept --timeout (cache, default 900 s) and --file (store, default ~/.git-credentials) (PGEN p.336-337)
- git credential fill | root command of the credential system; reads key=value from stdin, a blank line ends it (PGEN p.337-338)
- git credential-store --file X store|get | use the helper directly (PGEN p.338)

## Step-by-step procedures
### A. Enter a risky merge safely (PGEN p.278)
1. Leave the workdir clean before merging (commit on a temporary branch or stash). 2. Do the merge. 3. If you did not expect a conflict: git merge --abort (p.279-280).

### B. Whitespace-only conflict (PGEN p.280)
1. git merge --abort. 2. git merge -Xignore-space-change <branch> (or -Xignore-all-space).

### C. Manual re-merge of a file (PGEN p.280-283)
1. In the conflict state, extract :1:, :2:, :3: with git show into 3 files. 2. Fix one side (e.g.: dos2unix on theirs). 3. git merge-file -p ours common theirs > file. 4. Check with git diff --ours/--theirs/--base. 5. git clean -f on the temporary files.

### D. Get context for a conflict (PGEN p.284-286)
1. git checkout --conflict=diff3 file (or config merge.conflictstyle diff3). 2. git log --oneline --left-right --merge (and -p). 3. git diff to see what remains; resolve; git diff again to review the combined diff before committing (p.286-287).

### E. Undo a merge (PGEN p.288-290)
Local and unpublished, with no new commits afterwards: git reset --hard HEAD~ (p.289).
Already published or refs cannot be moved: git revert -m 1 HEAD (p.289). To re-merge the topic later: git revert of the revert commit ("^M"), then git merge topic (p.290-291).

### F. Subtree merge (PGEN p.292-294)
1. git remote add + git fetch --no-tags + git checkout -b local_branch remote/master. 2. Back on master: git read-tree --prefix=dir/ -u local_branch; commit. 3. To update: on local_branch, git pull; on master, git merge --squash -s recursive -Xsubtree=dir local_branch; commit.

### G. Rerere (PGEN p.295-301)
1. git config --global rerere.enabled true. 2. Merge with a conflict ("Recorded preimage"). 3. Resolve, git add, git commit ("Recorded resolution"). 4. In a future merge/rebase with the same conflict, "Resolved ... using previous resolution" appears; file already without markers; git add; git rebase --continue (p.301). To reapply after recreating the conflict: git checkout --conflict=merge file; git rerere (p.300).

### H. Bisect (PGEN p.302-304)
1. git bisect start; git bisect bad; git bisect good v1.0. 2. Test each commit; git bisect good|bad. 3. On seeing "first bad commit", git bisect reset. Automated: git bisect start HEAD v1.0; git bisect run script.

### I. Add a submodule (PGEN p.304-306)
1. git submodule add <url>. 2. git status shows .gitmodules + the directory entry. 3. git commit; git push.

### J. Clone a project with submodules (PGEN p.306-308)
Option 1: git clone --recurse-submodules. Option 2: git clone, then git submodule init and git submodule update (or update --init --recursive).

### K. Consume submodule updates (PGEN p.308-311)
1. git submodule update --remote [name]. 2. Review with git diff --submodule. 3. Commit in the superproject locks the new version for everyone else.

### L. Collaborator receives a superproject update (PGEN p.311-313)
git pull (fetches submodules but does NOT update them) -> git submodule update --init --recursive (or pull --recurse-submodules). If the URL changed: git submodule sync --recursive and then update --init --recursive.

### M. Work on a submodule (PGEN p.313-316)
1. cd into the submodule; git checkout <branch>. 2. From the superproject: git submodule update --remote --merge (or --rebase). 3. Local commits in the submodule. 4. Before publishing: git push --recurse-submodules=check or on-demand (or manual push inside the submodule). 5. Push the superproject.

### N. Diverged submodule conflict (PGEN p.316-318)
1. git pull fails: "CONFLICT (submodule)". 2. git diff to get the 2 SHAs. 3. In the submodule: git branch try-merge <sha_of_the_other_side>; git merge try-merge; resolve and commit. 4. Back in the superproject, git add <submodule>, git commit. If a merge commit already containing both exists, Git suggests git update-index --cacheinfo 160000...; the book recommends NOT accepting it directly but doing a manual fast-forward in the submodule, testing, git add and commit (p.318-319).

### O. Bundle round trip (PGEN p.325-327)
1. Sender: git bundle create repo.bundle HEAD master. 2. Receiver: git clone repo.bundle repo. 3. New changes: git bundle create commits.bundle master ^<base_sha>. 4. Receiver: git bundle verify; git bundle list-heads; git fetch x.bundle master:other-master.

### P. Graft history with replace (PGEN p.328-336)
1. Create a history branch at the desired point; push to a new remote (p.329-330). 2. commit-tree of the cut-point's tree -> base commit with instructions; git rebase --onto <base> <point> (p.331-332). 3. Whoever wants full history: git remote add project-history; git fetch; git replace <short_commit> <history_commit> (p.333-334).

## Decision rules / heuristics / author recommendations
- Before a merge with a possible conflict: clean workdir (commit on a temporary branch or stash) (PGEN p.278).
- Merge with lots of whitespace noise -> abort and redo with -Xignore-space-change/-Xignore-all-space (PGEN p.280).
- Manual re-merge with merge-file fixes the whitespace before the merge and is better than ignore-space-change, which can leave lines with mixed DOS line endings (PGEN p.282).
- Binary conflict or wanting only one side -> git checkout --ours/--theirs (PGEN p.285).
- Unwanted merge that is only local -> move refs (reset --hard HEAD~) and "the easiest is best"; already published/there are commits afterwards -> revert -m 1 (PGEN p.288-289).
- Revert of a merge and re-merge of the same topic -> revert the revert first, otherwise Git only brings changes made after the reverted merge (PGEN p.290).
- -Xours/-Xtheirs vs -s ours: use -X when you still want the non-conflicting changes; -s ours only to mark a branch as already merged (e.g.: bugfix backported to release and merged with -s ours into master, to avoid conflict later) (PGEN p.291-292).
- Subtree vs submodule: subtree keeps all the code in one place, but is more complex and easy to get wrong (reintegration, pushing a branch to an unrelated repo) (PGEN p.294).
- rerere: useful for a long-lived branch that must merge cleanly without intermediate merge commits, to keep a branch rebased, to swap merge for rebase, or to build a test head with several topics (PGEN p.294-295).
- blame alone assumes you already know where the problem is; without knowing the spot and with dozens/hundreds of commits, use bisect (PGEN p.302).
- Submodules are only worth it if you really want to edit the submodule's code together with the main project; otherwise use a dependency manager (Maven, Rubygems) (PGEN p.313).
- Use a .gitmodules URL accessible to everyone; local override via git config submodule.<name>.url; a relative URL can help (PGEN p.305).
- Always use git checkout --recurse-submodules when the project has submodules; in old versions, git submodule update --init --recursive after the checkout (PGEN p.323).
- When updating a submodule, use --init (new ones may have arrived) and --recursive (nested) (PGEN p.312).
- Superproject push: set push.recurseSubmodules (check or on-demand) as the default (PGEN p.316).
- Bundle: the list of commits must be computed manually (unlike network protocols); packing only the difference is better than the whole repo (PGEN p.326).
- Credentials: SSH without a passphrase allows transferring without typing a password; HTTP requires credentials on every connection; 2FA makes it worse (PGEN p.336).
- Several helpers: queried in order, stops at the first that answers; when saving, sent to all (PGEN p.337).

## Risks, warnings and anti-patterns
- checkout [commit] <paths> is NOT safe for the workdir: it overwrites the file (PGEN p.277). reset --hard likewise (p.277, 280).
- merge --abort may not revert perfectly if there were unstashed/uncommitted changes in the workdir before the merge (PGEN p.280).
- git reset --hard HEAD loses uncommitted work (PGEN p.280).
- reset --hard to undo a merge rewrites history: problematic in a shared repo; does not work if there are new commits afterwards (it would lose them) (PGEN p.289).
- After a merge revert, merging the same topic says "Already up-to-date" and future merges only bring new work (PGEN p.290).
- -Xours/-Xtheirs pick one whole side in conflicts (including binaries) without markers; -s ours completely ignores the other branch (PGEN p.291-292).
- Subtree: risk of error in reintegration and of pushing a branch to an unrelated repo (PGEN p.294).
- git update-index --cacheinfo suggested by Git in a submodule conflict: the book says it should probably not be accepted without checking (PGEN p.319).
- Submodule in detached HEAD: commits made may be lost on the next submodule update (PGEN p.313). Forgetting --rebase/--merge on update --remote leaves it in detached HEAD (the work remains on the local branch, you just have to go back and merge/rebase manually) (PGEN p.314).
- submodule update with uncommitted changes that conflict: Git aborts the checkout so as not to overwrite (PGEN p.315).
- FORGOTTEN PUSH: committing and pushing the superproject without pushing the submodule leaves others with no way to obtain the dependent commit (PGEN p.315). Mitigation: push --recurse-submodules=check|on-demand (p.315-316).
- git pull does not update submodules (only fetches them): it stays "modified (new commits)" until git submodule update (PGEN p.312).
- Switching branches without --recurse-submodules: the submodule appears "modified/new commits"; in Git < 2.13 the submodule directory remains as untracked (PGEN p.322-323).
- Subdirectory->submodule conversion: submodule add fails "already exists in the index" -> git rm -r first (PGEN p.323-324); going back to the old branch may fail due to untracked files; checkout -f may overwrite unsaved changes and leave an empty directory (git checkout . in the submodule) (PGEN p.324).
- git merge of diverged submodules: Git does not even try a trivial merge; the message "merge following commits not found" is confusing and does not show SHAs (PGEN p.317).
- Modern submodules store data in the superproject's .git, so deleting the directory does not lose commits/branches (PGEN p.324).
- credential store: plain-text passwords in ~/.git-credentials, never expire (PGEN p.336, 339).
- Replace objects: references in refs/replace are shareable by push; cat-file shows the replaced data, not the real data (the real parent of 81a708d was the placeholder commit) (PGEN p.335-336).
- A bundle with a range missing prerequisites cannot be imported ("Repository lacks these prerequisite commits") (PGEN p.327).

## Illustrative examples/cases
- hello.rb with DOS conversion vs comment: whitespace-only conflict; illustrates -Xignore-space-change and merge-file (PGEN p.278-283).
- hola world vs hello mundo -> hola mundo: illustrates --conflict=diff3, combined diff and rerere (PGEN p.284-300).
- Linux kernel Makefile: blame -L 69,82 (PGEN p.301); GITServerHandler.m -> GITPackUpload.m: blame -C (PGEN p.302).
- Bisect between v1.0 and HEAD (~12 commits, 6 tests remaining at the first question) (PGEN p.303).
- Submodule DbConnector in MainProject; CryptoLibrary for branch/conversion (PGEN p.304-324).
- Rack as a subtree on master (PGEN p.292-294).
- Bundle of 2 commits; round trip with 3 new commits (PGEN p.325-327).
- Splitting into short and long history with replace (PGEN p.328-336).
- Custom helper git-credential-read-only in Ruby (PGEN p.339-340).

## Dated data / divergences from current practice
- [DATED] The book uses git checkout to switch branches, checkout --conflict/--ours/--theirs and checkout paths (p.277, 284-285); today git switch and git restore (--source, --staged) exist; checkout still works. Here the book does not yet mention switch/restore. (Reasonable certainty; external knowledge.)
- [DATED] Outputs show "master" as the default branch and "Merge made by the 'recursive' strategy" (p.280, 291); in recent Git the default strategy is ort (external knowledge, not on the page), and the init.defaultBranch default is often main.
- [DATED] SHA-1 (p.281, 301); recent Git supports SHA-256 as an optional mode (external knowledge).
- [DATED] Texts "Git >= 2.13/2.14/2.15" for --recurse-submodules (p.322-323, 312): the book already gives the version; current versions are much newer.
- [DATED] git status with "git reset HEAD <file>" and "git checkout -- <file>" as hints (p.296, 309): newer versions suggest git restore.
- [DATED] Authentication: the book cites "username and password" over HTTP and 2FA; providers such as GitHub now require tokens/PAT or GCM instead of a password (external knowledge).
- [DATED] git filter-branch cited as a way to rewrite history (p.328); today the recommended tool is git filter-repo (external knowledge, not on the page).
- [DATED] Examples with GitHub and URLs (rack/rack, chaconinc) and outputs "Counting objects/Checking connectivity" (old format) (p.293, 304).
- The book cites GCM (Git Credential Manager) for Windows (p.336); osxkeychain and wincred appear on p.339.
- The bisect text shows "Bisecting: 6 revisions left" in a history of ~12 commits (p.303); the current version also accepts custom terms (old/new) - external knowledge, not on the page.

## What the book does NOT say here (gaps)
- Does not mention git switch/restore, nor git merge --continue, nor git merge --quit; only --abort (p.279-280).
- Does not describe git blame -w, -M, --ignore-rev nor blame via GitHub; only -L and -C (p.301-302).
- Does not describe git bisect log/replay/skip nor "git bisect visualize"; only start, good, bad, reset, run (p.302-304). Does not say what to do with an untestable commit (skip).
- Does not describe git submodule deinit, submodule removal, nor git submodule status/absorbgitdirs; only add/init/update/sync/foreach (p.304-324).
- Does not describe git subtree (the command) - only the manual subtree merge with read-tree (p.292-294).
- Does not describe git bundle unbundle (uses fetch/clone), nor --all (p.325-327).
- Does not describe git replace --graft/--edit, nor how to remove a replace (git replace -d) (p.328-336).
- Does not cover git credential reject nor credential.helper for Linux libsecret, nor PAT caching (p.336-338).
- Does not say that rerere can be cleaned (git rerere forget/clear/gc) (p.294-301).
- Does not say how to resolve a submodule conflict with --ours/--theirs (p.316-319).


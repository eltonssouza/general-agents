# Procedures (playbooks from the book, with pages)

> All pages are PGEN (Pro Git EN, ed. 2.1.450), PDF page (printed = PDF - 6). Each step is [from source] unless marked. The script `scripts/git_advisor.py "<intent>"` prints these playbooks deterministically. Commands that the book teaches in an old form carry [DATED].

## P1. Daily cycle of recording changes
1. `git status` (PGEN p.34); `git add` to track/stage (p.35-37); if you edit again after the add, repeat the add (p.37).
2. Review: `git diff` (working x stage) and `git diff --staged` (stage x last commit) (p.39-41); `git diff --check` before committing (p.136).
3. `git commit` (editor; `-v` shows the diff) or `-m`; `-a` skips the add of tracked files, with care (p.42-44).

## P2. Undo (small): amend, unstage, discard
1. Last commit: forgot something -> `git add`; `git commit --amend` (p.52-53, 250). Only on an unpushed commit (p.53).
2. Unstage: `git restore --staged <file>` (p.55) or `git reset HEAD <file>` (p.53) [DATED the old form].
3. Discard local changes: `git restore <file>` (p.56) or `git checkout -- <file>` (p.54) [DATED]: no way back; consider stash/branch first (p.55).

## P3. Branch, merge and conflict
1. Create and switch: `git checkout -b x` (p.76) or, since Git 2.23, `git switch -c x` (p.76).
2. Keep the working dir clean to switch branches (p.78). Hotfix: branch from master, test, fast-forward merge into master, `git branch -d` (p.78-80).
3. Merging a feature: `git checkout master; git merge feature` -> three-way with a merge commit if it diverged (p.81).
4. Conflict: edit the markers, `git add`, `git commit` (p.82-85); `git mergetool` (p.84); `git merge --abort` to give up (p.279-280).

## P4. Rebase (and when NOT to use it)
1. `git checkout topic; git rebase master`, then `git checkout master; git merge topic` (fast-forward) (p.102).
2. `git rebase --onto master server client` to take a topic that was born from another topic (p.103-105).
3. Rule: do not rebase commits that exist outside your repository and on which others may have based work (p.106). Gradation (p.109): local = ok; pushed and unused = ok; public and used = problem.
4. If someone rewrote and force-pushed: `git fetch` + `git rebase <remote>/<branch>` or `git pull --rebase` (p.108-109); `pull.rebase true` (p.109).

## P5. Remotes and remote branches
1. `git remote -v/add/show/rename/remove` (p.57-61); `git fetch` does not merge (p.58-59); `git pull` = fetch + merge (p.59, 100).
2. Publish: `git push origin <branch>` (p.97); a colleague receives `origin/<branch>` and creates tracking with `git checkout -b b origin/b`, `--track` or `git branch -u` (p.98-99).
3. Delete a remote branch: `git push origin --delete <branch>` (p.100-101; only the pointer; data stays until GC).
4. Rename: `git branch --move`, `push --set-upstream`, adjust integrations, only then `push --delete` the old one (p.86-88).

## P6. Rewrite local history (before publishing)
1. Cardinal rule: rewrite only locally and treat pushed history as final (p.249).
2. Message of the last commit/forgotten file: `--amend` (p.249-250); several commits: `git rebase -i HEAD~N` (pick/edit/squash/drop; deleting a line loses the commit) (p.250-255).
3. Simple squash: `git reset --soft HEAD~N` + `git commit` (p.272-275). Split: mark `edit`, `git reset HEAD^`, several commits, `--continue` (p.254).
4. Escape: `git rebase --abort` during; `git reflog` afterwards (p.255).

## P7. Remove a file/secret/large binary from history
1. Deleting it in a later commit does not solve it: history keeps the object (p.449-450).
2. The book recommends `git-filter-repo` and discourages `filter-branch` (p.255); the book shows `filter-branch --tree-filter 'rm -f file' HEAD` (p.256) and, for speed, `--index-filter 'git rm --ignore-unmatch --cached file' -- <sha>^..` (p.451).
3. Test on a separate branch (p.256); then clean refs/original and logs, `git gc`, and `git prune --expire now` if you want to delete it for good (p.452).
4. Collaborators will need to rebase (p.449). Rotating leaked credentials: [extrapolation].

## P8. Recover lost commits
1. `git reflog` / `git log -g` -> `git branch recover <sha>` (p.226-227, 448).
2. Without reflog: `git fsck --full` -> `dangling commit` (p.449).
3. What was never committed does not come back (p.55, 269).

## P9. Reset: choosing the form
1. Three trees: HEAD, index, working directory (p.257-259).
2. `--soft` only moves the branch; `--mixed` (default) also matches the index; `--hard` matches the working dir and is the only destructive form (p.266-269).
3. `reset <file>` (with a path) skips step 1: unstage (p.270). `checkout <commit>` is safe for the working dir; `checkout <commit> <paths>` and `reset --hard` are not (p.276-277).

## P10. Advanced merge and undoing a merge
1. Clean workdir first (p.278); unexpected conflict: `merge --abort` (p.279-280).
2. Whitespace only: abort and use `-Xignore-space-change` (p.280). Context: `checkout --conflict=diff3`, `log --left-right --merge` (p.284-286).
3. Undo: local and with no commits afterwards -> `reset --hard HEAD~`; published -> `git revert -m 1 HEAD`; to re-merge, revert the revert first (p.288-291).

## P11. Stash and clean
1. `git stash` / `apply --index` / `drop` / `pop` / `stash branch` (p.236-240); `-u` includes untracked, `--all` includes ignored (p.239).
2. `git clean -d -n` before `-f`; `stash --all` is a reversible alternative (p.240-241).

## P12. Find a defect: blame, bisect, search
1. `git blame -L` (p.301); `git bisect start/bad/good/run/reset` (p.302-304); `git log -S/-G/-L` (p.247-248).

## P13. Contribute (fork + PR) and maintain a fork
1. Fork, topic branch, push to the fork, PR (p.178-182); requested changes = new commits on the same branch (p.184).
2. Outdated PR: merge upstream (p.187-188); rebase only with a new branch/PR, no force-push on an open PR (p.188).
3. A fork never updates itself; never commit to the fork's master (p.195-196) [DATED: the UI today has Sync fork, extrapolation].

## P14. Patches by email (contributor and maintainer)
1. `git format-patch -M origin/master`; `send-email`/`imap-send` (p.154-155). Maintainer: `git am` (p.158-160) or `git apply` (p.157-158); review with `git log contrib --not master` and `git diff master...contrib` (p.161-162).

## P15. Release
1. `git tag -a`/`-s` (p.62, 168); `git push origin <tag>`/`--tags`/`--follow-tags` (p.64-65); `git describe`, `git archive`, `git shortlog --no-merges master --not v1.0.1` (p.169-170).

## P16. Server and protocols
1. Choice: Smart HTTP, SSH, local, git:// (p.111-116). Avoid git:// (arbitrary code execution) (p.115-116).
2. Bare repo + scp (p.116-117); `git` user + authorized_keys + git-shell (p.119-121); Smart HTTP with web server authentication and SSL (p.123-125).

## P17. Policy through hooks
1. Hook = executable with the exact name in `.git/hooks` (p.360). Client hooks are not cloned and can be bypassed (p.361). Server: `update` per ref, `pre-receive` once, `post-receive` does not stop the push (p.363). `receive.denyNonFastForwards`/`denyDeletes` (p.352).

## P18. Submodules
1. add/clone --recurse-submodules (p.304-308); pull does not update -> `submodule update --init --recursive` (p.311-313); push with `--recurse-submodules=check|on-demand` (p.315-316); detached HEAD and conflicts (p.313, 316-319).

## P19. Plumbing: inspecting/assembling objects
1. `hash-object -w`, `update-index --add --cacheinfo`, `write-tree`, `commit-tree`, `update-ref` (p.421-428, 431). Object format: header + content, SHA-1, zlib, `objects/xx/yyyy` (p.429-431).

## P20. Migrate from SVN/Mercurial/Perforce
1. Map authors; `git svn clone --authors-file ... --no-metadata -s`; convert tags/branches (p.405-408); `hg-fast-export` (p.408-410); `git p4 clone` (p.410-412); custom importer with `git fast-import` (p.411-419).

# Cases and anti-patterns (from the book, with pages)

> Pages = PGEN, PDF page (printed = PDF - 6). Marking: [from source] unless stated otherwise. [DATED] items have changed in practice.

## Anti-patterns and pitfalls
| # | Pitfall | Why / fix according to the book | Page |
|---|---|---|---|
| 1 | `git checkout -- file` / `git restore file` without thinking | Discards local changes with no way back; prefer stash/branch if you want to keep them | PGEN p.54-56 |
| 2 | `git reset --hard` | The only destructive form of reset; only what was committed comes back through the reflog | PGEN p.269 |
| 3 | `git commit --amend` on an already pushed commit | Changes the SHA-1; amend + force push harms collaborators | PGEN p.53, 250 |
| 4 | `git commit -a` blindly | May include unwanted changes | PGEN p.44 |
| 5 | `git add *` / bulk add | Stages too much; use `add -p` and review with `diff --staged` | PGEN p.53, 232-236 |
| 6 | Editing after `git add` and committing | The commit takes the content as of the add | PGEN p.37 |
| 7 | Rebasing published commits | Abandons commits and creates similar new ones; everyone suffers | PGEN p.106 |
| 8 | Plain `git pull` after someone else's force-push | Creates a merge with duplicated commits; use `pull --rebase` | PGEN p.107-109 |
| 9 | `git branch -D` | Loses unmerged commits | PGEN p.86 |
| 10 | Renaming master/main without notice | Breaks integrations/scripts; the old one remains on the remote | PGEN p.86-88 |
| 11 | Forgetting that `git push` does not send tags | Use `push origin <tag>`, `--tags` or `--follow-tags`; `tag -d` does not delete on the remote | PGEN p.64-66 |
| 12 | Commits in detached HEAD (checkout of a tag) | They become unreachable; create a branch | PGEN p.66 |
| 13 | `git clean -f` without `-n` | Deletes untracked files with no way back; `-x` deletes ignored files | PGEN p.240-241 |
| 14 | Thinking `git stash` saved everything | By default it does not save untracked/ignored files (`-u`/`--all`); `apply` does not restore staged state without `--index` and does not remove the stash | PGEN p.238-239 |
| 15 | `git svn dcommit` mixed with a Git remote | Rewrites the commits (new SHA-1s) | PGEN p.377 |
| 16 | filter-branch as the first option | "Nuclear option"; the book recommends git-filter-repo; test on a separate branch | PGEN p.255-256 |
| 17 | Removing a large file only with a new commit | History keeps the object; clones keep downloading it | PGEN p.449-450 |
| 18 | `git:// ` or http:// without TLS | Risk of arbitrary code execution; open push on the daemon | PGEN p.115-116 |
| 19 | `git-http-backend` without authentication on the web server | The backend does not authenticate; use SSL | PGEN p.124-125 |
| 20 | Relying on a client hook for policy | It is not cloned and can be bypassed with `--no-verify`; policy belongs on the server | PGEN p.361, 369 |
| 21 | Submodule: forgetting to push the submodule | The superproject points to a commit nobody can download | PGEN p.315 |
| 22 | Submodule in detached HEAD | Commits may be lost on the next update | PGEN p.313 |
| 23 | Reverting a merge and re-merging the same topic | Revert the revert first; otherwise 'Already up-to-date' | PGEN p.290 |
| 24 | `-s ours` thinking it is `-Xours` | `-s ours` ignores the other branch entirely | PGEN p.291-292 |
| 25 | Credential store | Plain text in ~/.git-credentials, never expires | PGEN p.336, 339 |
| 26 | Force push on an open PR branch | New branch + new PR; close the old one | PGEN p.188 |
| 27 | Committing directly to master of the fork | Git does not warn you; the fork drifts | PGEN p.196 |
| 28 | Commit message without a blank line after the summary | Rebase gets confused; the blank line is critical | PGEN p.137 |

## Illustrative cases
- Hotfix in parallel with a feature: `iss53` and `hotfix` from master; hotfix as fast-forward, feature as three-way merge (PGEN p.76-82).
- Merging `iss53` with a conflict in index.html: markers, editing, `git add`, `git commit` (PGEN p.82-85).
- Managed team: `featureA`/`featureB`/`featureBee` with `push -u` and integrators (PGEN p.144-148).
- Public fork: `featureA`, `request-pull`, rebase + `push -f` (or `featureAv2`), `featureBv2` with `merge --squash` (PGEN p.149-153).
- Maintenance by email: `git am`, `--resolved`, `--skip`, `--abort`, `-3` (PGEN p.158-160).
- Integration in Git itself: master/next/seen/maint; next and seen rebased periodically (PGEN p.165-166).
- Huge file in imported history: `verify-pack`, `rev-list --objects`, `filter-branch --index-filter`, `gc` (PGEN p.449-453).
- Object chain built "by hand" with plumbing: `hash-object`, `update-index`, `write-tree`, `commit-tree`, `update-ref` (PGEN p.421-428).
- `[ref: N]` message policy + per-path ACL in the `update` hook (PGEN p.363-368).
- History grafts with `replace` and `bundle` round trip (PGEN p.324-336).

## Contradictions and tensions in the book (so as not to propagate them)
- The book teaches `checkout`/`reset HEAD` first and `restore` afterwards (PGEN p.53-56); Appendix C still lists `checkout` (p.490) [DATED].
- Rebase vs merge: the author presents both sides and says there is no simple answer (PGEN p.109-110).
- The book's own commit message examples do not follow the standard it recommends (PGEN p.137).
- Ruby ACL pre-commit example with an unclosed block (PGEN p.370): treat as pseudocode.
- Sinatra example with `ref/heads/special-branch` (PGEN p.217): the real ref is `refs/heads/...`; illustrative.

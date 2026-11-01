# Appendices A, B, C and Index (PGEN p.459-501)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; printed EN page = PDF - 6; PT-BR = PDF - 5). A citation `(p.N)` without a sigla = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Convention: "PDF p.N" = PDF page/text marker (PGEN). Printed page = N-6 (confirmed: gitk appears in the Index as 453 and is at PDF 459; git log in the Index as 40 and the section is at PDF 46). Appendix C cites SECTIONS BY NAME, never by page number; the PDF pages of the sections cited in the tables below were resolved by me, by locating the section title as a heading in the body of the book (not given by the appendix).

## Section map: title -> starting PDF page
- Appendix A: Git in Other Environments - 459 (printed 453)
  - Graphical Interfaces (gitk and git-gui) - 459; GitHub for macOS and Windows - 461; Other GUIs - 464
  - Git in Visual Studio - 464; Git in Visual Studio Code - 465; Git in IntelliJ / PyCharm / WebStorm / PhpStorm / RubyMine - 465; Git in Sublime Text - 466
  - Git in Bash - 466; Git in Zsh - 467; Git in PowerShell - 469; Summary - 471
- Appendix B: Embedding Git in your Applications - 472
  - Command-line Git - 472; Libgit2 - 472; Advanced Functionality (libgit2 backends) - 474; Other Bindings (LibGit2Sharp, objective-git, pygit2) - 476; JGit - 477; Plumbing (JGit) - 478; Porcelain (JGit) - 480; go-git - 480; Dulwich - 482
- Appendix C: Git Commands - 484 (printed 478)
  - Setup and Config - 484; core.editor table - 485; Getting and Creating Projects - 486; Basic Snapshotting - 487; Branching and Merging - 489; Sharing and Updating Projects - 491; Inspection and Comparison - 493; Debugging - 494; Patching - 495; Email - 495; External Systems - 497; Administration - 497; Plumbing Commands - 498
- Index - 499 to 501 (printed 493-495)

## Concepts and definitions
- gitk | - | graphical history viewer, a "graphical shell" over git log/git grep; accepts git log options, --all is useful (shows commits reachable from any ref, not just HEAD) | PDF p.459
- git-gui (git gui) | - | tool geared to building commits: index on the left (unstaged on top, staged below), diff on the right, stage per hunk/line with right-click; "Amend" reopens the last commit | PDF p.460-461
- Task-oriented vs workflow-oriented tool | - | gitk/git-gui are "task-oriented"; GitHub for macOS/Windows is "workflow-oriented" (a curated subset of functions) | PDF p.461
- The book's thesis on GUIs | - | no GUI is "better"; each serves a workflow; nothing a GUI does is impossible on the command line; the CLI gives more power and control; new features show up first in the CLI | PDF p.459
- Sync button (GitHub clients) | - | collapses pull/push/merge/rebase into: 1) git pull --rebase (if it fails because of a conflict, falls back to git pull --no-rebase), 2) git push | PDF p.464
- posh-git | - | PowerShell module with tab-completion and a prompt showing repository status; also works in PowerShell Core (Linux/macOS) | PDF p.469
- vcs_info | - | Zsh framework for getting VCS info into the prompt | PDF p.468
- git-completion.bash / git-prompt.sh | - | scripts in contrib/completion of the Git source code (completion and prompt via __git_ps1); git-prompt.sh works for Bash and Zsh | PDF p.466-469
- Libgit2 | - | dependency-free implementation of Git, focused on a good API for embedding; has bindings (Rugged/Ruby, LibGit2Sharp/.NET, objective-git, pygit2/Python etc.) | PDF p.472, 476-477
- Pluggable backends (Libgit2) | - | allow storing config, refs and ODB differently from standard Git; the first member of the backend struct must be git_odb_backend (expected memory layout) | PDF p.474-476
- JGit | - | Git implementation in Java (Eclipse), two layers: plumbing (Repository, RefUpdate, ObjectLoader) and porcelain (Git class, builder commands + .call()) | PDF p.477-480
- go-git | - | pure Go implementation, no native dependencies; pluggable storage (in-memory by default), filesystem abstraction (billy), adjustable HTTP client | PDF p.480-482
- Dulwich | - | pure Python Git implementation, optional C extensions for performance; plumbing API (Repo) and porcelain (dulwich.porcelain) | PDF p.482-483
- Abbreviation of long options | - | "git commit --a" acts as --amend if the letters are unique; the book says to use the full option in scripts | PDF p.484

## Commands and options (Appendices A/B)
| command | what it is for according to the book | PDF p. | [DATED]? |
|---|---|---|---|
| gitk [git log options] | open the history viewer; --all shows everything | 459 | - |
| git gui | open the commit tool | 460 | - |
| git version + git checkout tags/vX.Y.Z | find the Git version and get the matching git-completion.bash from the source | 466 | checkout instead of switch (see Dated items) |
| `. ~/git-completion.bash` in .bashrc | enable autocompletion in Bash | 466 | - |
| `. ~/git-prompt.sh`; `export GIT_PS1_SHOWDIRTYSTATE=1`; PS1 with `__git_ps1 " (%s)"` | Bash prompt with branch/state | 467 | - |
| `autoload -Uz compinit && compinit` (.zshrc) | Zsh autocompletion | 467 | - |
| vcs_info + RPROMPT + zstyle ':vcs_info:git:*' formats '%b' | branch in the Zsh right prompt | 468 | - |
| Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned -Force | prerequisite (Windows) for PowerShell scripts; -Scope CurrentUser if not admin | 470 | - |
| Install-Module posh-git -Scope CurrentUser -Force (and -AllowPrerelease for PowerShell Core) | install posh-git via PowerShell Gallery | 470 | - |
| Install-Module PowerShellGet -Force -SkipPublisherCheck | workaround if Install-Module fails with an error about PowerShellGet not installed via Install-Module | 470 | - |
| Import-Module posh-git; Add-PoshGitToProfile -AllHosts | always load posh-git (writes to $profile) | 471 | - |
| Import-Module <folder>\src\posh-git.psd1 | installation from source (GitHub release) | 471 | - |
| git_repository_open, git_revparse_single(..."HEAD^{commit}"), git_commit_author, git_commit_free | libgit2 C example | 472-473 | GIT_OBJ_COMMIT, SHA-1 |
| Rugged::Repository.new, repo.write(..., :blob), index.add, Rugged::Commit.create(... :update_ref => 'HEAD') | create a commit from scratch in Ruby | 473-474 | - |
| git_odb_new / git_odb_add_backend / git_repository_set_odb | plug in a custom ODB backend | 475 | - |
| FileRepositoryBuilder, repo.getRef, repo.resolve("HEAD^{tree}"), RefUpdate (delete requires setForceUpdate(true)), repo.getConfig | JGit plumbing | 478-479 | example uses "master" |
| new Git(repo).lsRemote().setCredentialsProvider(cp).setRemote("origin").setTags(true).setHeads(false).call() | JGit porcelain ~ git ls-remote | 480 | - |
| git.PlainClone, git.Clone(memory.NewStorage(), ...), r.Head(), r.CommitObject, commit.History() | go-git | 481 | - |
| Repo('.'), r.head(), porcelain.log('.', max_entries=1) | Dulwich | 482-483 | - |

## Step-by-step procedures
### Autocompletion and prompt in Bash (PGEN p.466-467)
1. Find the version with `git version` and do the matching `git checkout tags/vX.Y.Z` in the Git source (p.466).
2. Copy contrib/completion/git-completion.bash to an accessible place (e.g. home) and add `. ~/git-completion.bash` to .bashrc (p.466).
3. Test: `git chec<tab>` completes to git checkout; it covers subcommands, parameters, remotes and refs (p.467).
4. Prompt: copy contrib/completion/git-prompt.sh, `. ~/git-prompt.sh`, `GIT_PS1_SHOWDIRTYSTATE=1` and PS1 with __git_ps1 (p.467).
### Zsh (PGEN p.467-469)
1. Add `autoload -Uz compinit && compinit` to .zshrc (p.467); the completion shows a description of each candidate (p.467-468).
2. Prompt with vcs_info: autoload vcs_info, precmd_functions+=(precmd_vcs_info), setopt prompt_subst, RPROMPT and zstyle (p.468). Alternative: git-prompt.sh, compatible with Bash and Zsh (p.468-469). Framework alternative: oh-my-zsh (p.469).
### posh-git on Windows (PGEN p.469-471)
1. Set ExecutionPolicy to RemoteSigned (LocalMachine if admin, CurrentUser if not) (p.470).
2. Install-Module posh-git (PowerShell 5, or 4 with PackageManagement); AllUsers requires an elevated console (p.470).
3. Import-Module posh-git and Add-PoshGitToProfile -AllHosts to load it in every session (p.471). Caution: there are several $profile files (console and ISE) (p.470).
### Embedding Git: choosing (PGEN p.472)
1. Option 1: call the git binary in a child process; option 2: embedded library (p.472).
2. Advantages of the CLI: canonical, all features, easy to invoke. Disadvantages: plain-text output whose format changes from time to time (fragile/inefficient parsing); no error recovery (a corrupted repo or malformed config makes Git refuse many operations); process management, hard to coordinate several processes on the same repo (p.472).

## Decision rules / author's heuristics
- If you want full power and control -> command line; GUIs are conveniences (p.459).
- If the workflow differs from the "GitHub Flow" or you want control over when/how network operations happen -> use another client or the CLI instead of the Sync button (p.464).
- GitHub for macOS/Windows does not require a GitHub account; it works with any Git host (p.463).
- Libgit2: a pointer declared and passed to the function returns an integer code (0 = success, less than 0 = error); a pointer that the library fills in is freed by you; a const pointer is not freed but becomes invalid when the owner is freed (p.473).
- JGit: deleting a branch requires setForceUpdate(true), otherwise .delete() returns REJECTED and nothing happens (p.479). For large objects (isLarge()) use openStream() (p.479).
- In scripts, always use full, not abbreviated, options (p.484).
- A 32-bit editor on 64-bit Windows lives in C:\Program Files (x86)\ (p.485).

## Risks, warnings and anti-patterns
- git reset --hard can lose work if used incorrectly; understand it first (Appendix C, p.488).
- Rebasing already-published branches causes collaboration problems (Appendix C points to the Rebasing section, p.495).
- filter-branch rewrites many commits at once (p.498); see Dated items.
- JGit: example with a literal password in UsernamePasswordCredentialsProvider (p.480) - illustrative only.
- go-git: InsecureSkipVerify: true accepts any certificate; the book says "it may be useful for testing" (p.482).
- Libgit2: the backend example captures errors but does not handle them (p.475).
- PowerShell: AllSigned requires signing even local scripts; RemoteSigned only requires it for scripts downloaded from the web (p.470).

## Illustrative examples/cases
- Rugged creates a commit from scratch (blob -> index -> tree -> Commit.create with :update_ref): shows the object model via API (p.474).
- Same task "message of the commit pointed to by HEAD" (similar to git log -1) in LibGit2Sharp (p.476), objective-git (p.476), pygit2 (p.477).

## Appendix C: command -> cited sections map
Columns: "Appendix page" = PDF page where Appendix C describes the command. "Cited section (PDF p.)" = title cited by the appendix; the PDF page is that of the heading of that section in the body of the book (resolved by me).

### Setup and Config
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git config | 484 | First-Time Git Setup (27); Git Aliases (66); Rebasing (101; --rebase as the pull default); Credential Storage (336); Keyword Expansion (355; smudge/clean filters); Git Configuration (342; "almost the whole chapter"); core.editor table accompanies "Your Editor" (28) |
| git help | 486 | Getting Help (30); Setting Up the Server (119; git shell) |

### Getting and Creating Projects
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git init | 486 | Getting a Git Repository (32); Remote Branches (91; changing the default branch name from master); Putting the Bare Repository on a Server (117); Plumbing and Porcelain (420) |
| git clone | 486-487 | Cloning an Existing Repository (33); Getting Git on a Server (116; --bare); Bundling (324; unbundle); Cloning a Project with Submodules (306; --recurse-submodules) |

Description of clone (p.486): creates a directory, git init, git remote add (origin), git fetch, git checkout of the latest commit.

### Basic Snapshotting
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git add | 487 | Tracking New Files (35); Basic Merge Conflicts (82; resolving a conflict); Interactive Staging (232); Tree Objects (423; emulates add at low level) |
| git status | 487 | Checking the Status of Your Files (34) |
| git diff | 487-488 | Viewing Your Staged and Unstaged Changes (39; git diff, --staged, between two commits); Commit Guidelines (136; --check for whitespace); Determining What Is Introduced (161; A...B); Advanced Merging (277; -b, --theirs/--ours/--base); Starting with Submodules (304; --submodule) |
| git difftool | 488 | Viewing Your Staged and Unstaged Changes (39) - mention only |
| git commit | 488 | Committing Your Changes (42; -a, -m); Undoing Things (52; --amend); Branches in a Nutshell (69); Signing Commits (244; -S); Commit Objects (426) |
| git reset | 488-489 | Unstaging a Staged File (53); Reset Demystified (257; dedicated to the command); Aborting a Merge (279; reset --hard and merge --abort) |
| git rm | 489 | Removing Files (44; recursive, --cached); Removing Objects (449; --ignore-unmatch with filter-branch) |
| git mv | 489 | Moving Files (45) - mention only |
| git clean | 489 | Cleaning your Working Directory (240) |

### Branching and Merging
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git branch | 489 | Git Branching (69; "most of the chapter"); Creating a New Branch (71); Branch Management (85; list/delete); Tracking Branches (98; branch -u); Git References (431) |
| git checkout | 490 | Switching Branches (72); Tracking Branches (98; --track); Checking Out Conflicts (283; --conflict=diff3); Reset Demystified (257); The HEAD (432) |
| git merge | 490 | Basic Branching (76); Forked Public Project (149; squash); Advanced Merging (277; -Xignore-space-change, --abort); Signing Commits (244; verifying signatures); Subtree Merging (292) |
| git mergetool | 490 | Basic Merge Conflicts (82); External Merge and Diff Tools (346; creating your own tool) |
| git log | 490-491 | Viewing the Commit History (46; -p, --stat, --pretty, --oneline, date/author filters); Creating a New Branch (71; --decorate, --graph); Private Small Team (137) and Commit Ranges (230; A..B); Merge Log (285; --merge, --cc) and Triple Dot (231; A...B, --left-right); RefLog Shortnames (226; -g); Searching (245; -S, -L); Signing Commits (244; --show-signature) |
| git stash | 491 | Stashing and Cleaning (236) |
| git tag | 491 | Tagging (61); Tagging Your Releases (168); Signing Your Work (242; -s and -v) |

### Sharing and Updating Projects
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git fetch | 492 | Fetching and Pulling from Your Remotes (58); Remote Branches (91); Contributing to a Project (135, in Distributed Git; another with the same name exists in GitHub, 177); Pull Request Refs (202); Bundling (324); The Refspec (438) |
| git pull | 492 | Fetching and Pulling from Your Remotes (58); Inspecting a Remote (59); Rebase When You Rebase (108); Checking Out Remote Branches (160; pull with a one-off URL); Signing Commits (244; --verify-signatures) |
| git push | 492-493 | Pushing to Your Remotes (59); Pushing (97); Tracking Branches (98); Deleting Remote Branches (100; --delete); Contributing to a Project (135); Sharing Tags (64; --tags); Publishing Submodule Changes (315; --recurse-submodules); Other Client Hooks (362; pre-push); Pushing Refspecs (440) |
| git remote | 493 | Working with Remotes (56) |
| git archive | 493 | Preparing a Release (170; tarball) |
| git submodule | 493 | Submodules (304) |

### Inspection and Comparison
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git show | 493-494 | Annotated Tags (62); Revision Selection (224); Manual File Re-merging (280; stages of a conflict) |
| git shortlog | 494 | The Shortlog (170) |
| git describe | 494 | Generating a Build Number (169); Preparing a Release (170) |

### Debugging
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git bisect | 494 | Binary Search (302), only there |
| git blame | 494 | File Annotation (301), only there |
| git grep | 494 | Git Grep (246), only there |

### Patching
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git cherry-pick | 495 | Rebasing and Cherry-Picking Workflows (166) |
| git rebase | 495 | Rebasing (101; problems with already-published branches); Replace (328; --onto); Rerere (294; conflict during rebase; there is also an H3 "Rerere" in Maintaining a Project, 168); Changing Multiple Commit Messages (250; -i) |
| git revert | 495 | Reverse the commit (289; undoing a merge commit) |

### Email
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git apply | 495-496 | Applying Patches from Email (157) |
| git am | 496 | Applying a Patch with am (158; --resolved, -i, -3); Email Workflow Hooks (361); Email Notifications (200; curl .../pull/1.patch | git am; there is another "Email Notifications" on p.208) |
| git format-patch | 496 | Public Project over Email (153) |
| git imap-send | 496 | Public Project over Email (153) |
| git send-email | 496 | Public Project over Email (153) |
| git request-pull | 496 | Forked Public Project (149) |

### External Systems
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git svn | 497 | Git and Subversion (373; in the Git and Other Systems chapter) |
| git fast-import | 497 | A Custom Importer (412) |

### Administration
| command | Appendix page | Cited sections -> PDF page |
|---|---|---|
| git gc | 497 | Maintenance (446; normally runs in the background) |
| git fsck | 497 | Data Recovery (447; dangling objects) |
| git reflog | 497 | RefLog Shortnames (226; git log -g); Data Recovery (447; recovering a lost branch) |
| git filter-branch | 498 | Removing a File from Every Commit (256; --commit-filter, --subdirectory-filter, --tree-filter); Git-p4 (410; Perforce import, where the imported repo is cleaned up; there is also "Git-p4" at 398) |

### Plumbing Commands (p.498)
- ls-remote: Pull Request Refs (202)
- ls-files: Manual File Re-merging (280), Rerere (294), The Index (258)
- rev-parse: Branch References (226)
- Other low-level commands: Git Internals chapter (PDF 420); the book says it avoided using them in the rest of the book (p.498).

Note: "Rerere", "Contributing to a Project", "Email Notifications" and "Git-p4" occur in more than one place; I chose the most likely page from the command's context and indicated the alternative.

### Commands that Appendix C does NOT list (but appear in the Index/body)
git daemon, http-backend, instaweb, show-ref, credential, rerere, upload-pack, receive-pack, fetch-pack, send-pack and git p4 appear in the Index (p.499-500) but have no entry of their own in Appendix C. Also without an entry: git restore, git switch, git worktree, git bundle, git notes, git cat-file, git hash-object.

## Index (PGEN p.499-501) - usefulness as a source of pages
- Useful: YES, but with caveats. The Index gives PRINTED page numbers (PDF = number + 6). Verified: gitk 453 -> PDF 459; log 40 -> PDF 46 (Viewing the Commit History); fetch 52 -> PDF 58; rebasing 95 -> PDF 101; Dulwich 476 -> PDF 482.
- Limitations: lean index (3 pages). Subentries of git commands cover only: add, am, apply, archive, branch, checkout, cherry-pick, clone, commit, config, credential, daemon, describe, diff, fast-import, fetch, fetch-pack, filter-branch, format-patch, gitk, gui, help, http-backend, init, instaweb, log, merge, mergetool, p4, pull, push, rebase, receive-pack, remote, request-pull, rerere, send-pack, shortlog, show, show-ref, status, svn, tag, upload-pack. It does NOT cover reset, stash, bisect, blame, grep, reflog, revert, rm, mv, submodule etc. (use the Appendix C map above).
- Useful entries (printed -> PDF): .gitignore 338 -> 344; aliases 60 -> 66; autocorrect 339 -> 345; color 339 -> 345; credentials 330 -> 336; crlf/line endings/whitespace 343 -> 349; hooks 354 -> 360; keyword expansion 349 -> 355; rerere 162 -> 168; protocols (local 105 -> 111, dumb HTTP 107 -> 113, smart HTTP 107 -> 113, SSH 108 -> 114, git 109 -> 115); GitHub Flow 172 -> 178; pull requests 175 -> 181; GitHub API 212 -> 218; organizations 205 -> 211; Importing from Subversion 399 -> 405, Mercurial 402 -> 408, Perforce 404 -> 410; tags 55 -> 61 (annotated 56 -> 62, lightweight 57 -> 63, signing 162 -> 168); workflows 126 -> 132 (integration manager 127 -> 133, dictator and lieutenants 128 -> 134); policy example 357 -> 363; build numbers 163 -> 169; Git as a client 367 -> 373.
- Some items repeat numbers (e.g. "add, 29, 30, 30") - normal Index noise.

## Dated data / divergences from current practice
- Appendix C uses git checkout as the command to switch branches and check out content (p.490), without listing git switch/restore. [DATED] - Modern Git (2.23+) has switch/restore (EXTRAPOLATION).
- git filter-branch (p.498) [DATED] - the current Git documentation discourages it and points to git filter-repo (EXTRAPOLATION).
- Appendix C p.486 mentions changing the default branch name from "master"; the JGit examples use "master" (p.478).
- JGit with version 3.5.0.201409260305-r (p.477): from 2014; the book warns it has surely moved on. [DATED]
- Libgit2/JGit treat the hash as SHA-1 (p.473, 479) - [DATED] regarding SHA-256 (EXTRAPOLATION).
- core.editor table (p.485): Atom, Gvim vim72, Sublime Text 3, Textpad 5 etc. are old versions/editors; Atom was discontinued (EXTRAPOLATION). Keeps "code --wait" (VS Code), Helix, VSCodium.
- GitHub for macOS and Windows downloaded from desktop.github.com (p.461-463); today it is GitHub Desktop (EXTRAPOLATION).
- Visual Studio 2019 16.8 (p.464); VS Code requires Git 2.0.0+ (p.465); Sublime Text 3.2+ (p.466).
- Git in Bash says to copy contrib/completion from the source (p.466); today most installations already ship it (EXTRAPOLATION).
- The Index cites git daemon, instaweb, git p4, Git Fusion (p.499-501) - dated technologies.

## What the book does NOT say here (gaps)
- Appendix C does not give the full syntax/options of each command: only a general description and section pointers; for options it says to use git help <command> (p.486).
- It does not list git switch, git restore, git worktree, git bundle (although Bundling is cited), git notes, git cat-file/hash-object/update-index, git rerere, git credential, git daemon.
- Appendix C does not cite page numbers, only section names.
- Appendix A does not teach configuration steps in JetBrains/Sublime/Visual Studio; it only lists features and links.
- Appendix B does not cover SHA-256, git-lfs, or alternatives such as gitoxide/JGit alternatives; only libgit2 (+ Rugged, LibGit2Sharp, objective-git, pygit2), JGit, go-git, Dulwich.
- It does not say that one GUI is better than another (it says none is, p.459).


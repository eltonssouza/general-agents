# Ch. 4 Git on the Server + Ch. 5 Distributed Git (PGEN p.111-171)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; printed EN page = PDF - 6; PT-BR = PDF - 5). A citation `(p.N)` without a sigla = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


## Section map: section title -> starting PDF page
- Git on the Server (intro; remote repository = bare) -> 111
- The Protocols: Local -> 111; HTTP (Smart/Dumb) -> 113; SSH -> 114; Git protocol -> 115 (cons/security 115-116)
- Getting Git on a Server (git clone --bare, scp, --shared) -> 116-117
- Small Setups / SSH Access / Generating SSH public key -> 117-118
- Setting Up the Server (git user, authorized_keys, git-shell) -> 119-122
- Git Daemon -> 122 (systemd 122-123)
- Smart HTTP (git-http-backend + Apache) -> 123
- GitWeb (git instaweb, manual installation) -> 125
- GitLab (installation, admin, users, groups, projects, hooks, basic usage, merge requests) -> 127-130
- Third Party Hosted Options -> 130
- Summary ch.4 -> 131
- Distributed Git (intro ch.5) -> 132
- Distributed Workflows: Centralized -> 132; Integration-Manager -> 133; Dictator and Lieutenants -> 134; Workflows Summary -> 135
- Contributing to a Project (variables) -> 135
- Commit Guidelines (whitespace, logical commits, message) -> 136-137
- Private Small Team -> 137
- Private Managed Team -> 144
- Forked Public Project -> 149 (request-pull 150; rebase+push -f 152; --squash 153)
- Public Project over Email (format-patch, imap-send, send-email) -> 153
- Summary section -> 156
- Maintaining a Project -> 156
- Working in Topic Branches -> 157
- Applying Patches from Email: git apply -> 157; git am -> 158
- Checking Out Remote Branches -> 160
- Determining What Is Introduced (--not, merge-base, triple dot) -> 161
- Integrating Contributed Work: Merging Workflows -> 162; Large-Merging Workflows -> 165
- Rebasing and Cherry-Picking Workflows -> 166
- Rerere -> 168
- Tagging Your Releases -> 168
- Generating a Build Number (git describe) -> 169
- Preparing a Release (git archive) -> 170
- The Shortlog -> 170
- Summary ch.5 -> 171

## Concepts and definitions
| EN term | PT-BR term | definition | page |
|---|---|---|---|
| bare repository | repositorio nu/bare (not verified in PT) | repo without a working directory; basically the contents of .git; used as a collaboration point | PGEN p.111 |
| Local protocol | protocolo local | remote in another directory on the same host (e.g. shared NFS); URL = path or file:// | PGEN p.111 |
| file:// vs plain path | - | plain path: Git uses hardlinks/direct copy; file:// triggers the network transfer processes (less efficient); useful for a "clean" copy without extra refs/objects (e.g. after an import from another VCS) | PGEN p.112 |
| Smart HTTP | - | HTTP (since Git 1.6.6) with smart negotiation like SSH; standard HTTPS port; a single URL for anonymous read and authenticated push | PGEN p.113 |
| Dumb HTTP | - | bare repo served as static files by any web server; read-only; requires the post-update hook (git update-server-info); fallback when the server is not smart | PGEN p.113 |
| SSH protocol | - | common transport in self-hosting; authenticated and encrypted; no anonymous access | PGEN p.114-115 |
| Git protocol (git://) | - | daemon that listens on port 9418; no authentication or encryption; only serves repos with a git-daemon-export-ok file | PGEN p.115 |
| git-daemon-export-ok | - | empty file inside the repo that authorizes serving without authentication (git daemon; also git-http-backend if GIT_HTTP_EXPORT_ALL is missing) | PGEN p.115, 123, 124 |
| git-shell | - | restricted shell that ships with Git; as the login shell of the git user it blocks normal shell access but allows push/pull | PGEN p.121 |
| git-http-backend | - | Git CGI that negotiates fetch/push over HTTP; does not implement authentication (that stays in the web server layer) | PGEN p.123-125 |
| GitWeb | - | CGI/web viewer that ships with Git; simple | PGEN p.125 |
| GitLab namespace/group/project/visibility | - | a user or group has a namespace; a project ~ a repo; Private/Internal/Public visibility controls fetch and UI | PGEN p.127-129 |
| Blocking vs Destroying (GitLab user) | - | Blocking prevents login but preserves data; Destroying removes everything from the database and filesystem | PGEN p.128 |
| Centralized workflow | fluxo centralizado | a single hub; the second person to push has to fetch and merge first (does not overwrite) | PGEN p.132-133 |
| Integration-manager workflow | - | each dev has their own public (write) repo and reads from the others; the maintainer pulls from the clones and publishes to the canonical repo | PGEN p.133 |
| Dictator and Lieutenants | ditador benevolente e tenentes | variant for huge projects (e.g. Linux kernel): devs -> lieutenants -> dictator -> reference repo | PGEN p.134 |
| topic branch | - | temporary branch per work topic; on the maintainer side: to test a contribution | PGEN p.157 |
| non-fast-forward (rejected push) | - | push refused when the remote has commits the local one does not; resolve with fetch + merge | PGEN p.133, 139 |
| refspec (source:destination) | - | `git push -u origin featureB:featureBee` pushes a local branch to another remote name | PGEN p.146-147 |
| mbox | - | simple text format with one or more emails; format-patch generates it, git am reads it | PGEN p.158 |
| Author vs Commit (after git am) | - | Author = who created the patch and when; Commit = who applied it and when | PGEN p.159 |
| rerere | reuse recorded resolution | reuses an already-recorded conflict resolution (pre/post images) | PGEN p.168 |
| git describe output | - | most recent previous tag + number of commits since it + "g" + abbreviated SHA-1, e.g. v1.6.2-rc1-20-g8c5b85c | PGEN p.169 |
| cherry-pick | - | "rebase of a single commit": reapplies the commit's patch on the current branch, producing a new SHA-1 | PGEN p.166-167 |

## Commands and options
| command | what it is for according to the book | page | [DATED]? |
|---|---|---|---|
| git clone /srv/git/project.git ; git clone file:///srv/git/project.git | clone via the local protocol (path = hardlinks; file:// = network processes) | 111-112 | |
| git remote add local_proj /srv/git/project.git | add a local repo as a remote | 112 | |
| git pull /home/john/project | pull directly from a colleague's repo (simpler than having them push) | 112 | |
| git clone --bare my_project my_project.git | create a bare repo from an existing one (convention: .git suffix) | 116 | |
| scp -r my_project.git user@git.example.com:/srv/git | copy a bare repo to the server | 117 | |
| git init --bare --shared | adds group write permission; does not destroy commits/refs | 117 | |
| git init --bare (in /srv/git/project.git) | create an empty repo on the server | 120 | |
| ssh-keygen -o | generate an SSH key pair; -o saves the private key in a format more resistant to brute force | 118-119 | [DATED] the example uses RSA/DSA keys and `-o`; today ed25519 and the new format are already the default (not in the book; reasonably certain) |
| ssh-copy-id | automates copying/installing public keys | 119 | |
| sudo adduser git; mkdir .ssh && chmod 700 .ssh; touch .ssh/authorized_keys && chmod 600 | prepare the git user for key authentication | 119 | |
| cat /tmp/id_rsa.john.pub >> ~/.ssh/authorized_keys | add a dev's key | 120 | |
| git remote add origin git@gitserver:/srv/git/project.git ; git push origin master | first push to the server | 120 | [DATED] "master" as the default branch |
| chsh git -s $(which git-shell) | restricts the git account to Git operations (add the path to /etc/shells first) | 121 | |
| no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty | options prefixed to the key in authorized_keys to block forwarding | 121 | |
| git help shell | customize git-shell (restrict commands, login message) | 122 | |
| git daemon --reuseaddr --base-path=/srv/git/ /srv/git/ | serve via the git protocol; --reuseaddr restarts without waiting for the timeout; --base-path avoids the full path in the clone | 122 | [DATED] unencrypted git:// is discouraged today (the book itself warns, p.115-116) |
| systemctl enable/start/stop git-daemon | manage the daemon's systemd unit | 123 | |
| touch git-daemon-export-ok | release a repo to the daemon | 123 | |
| a2enmod cgi alias env; chgrp -R www-data /srv/git | enable Apache modules and give group access to the web server | 123-124 | |
| SetEnv GIT_PROJECT_ROOT /srv/git ; SetEnv GIT_HTTP_EXPORT_ALL ; ScriptAlias /git/ /usr/lib/git-core/git-http-backend/ | Apache config for Smart HTTP | 124 | |
| htpasswd -c /srv/git/.htpasswd schacon | create the Basic Auth password file (-c creates the file) | 124 | |
| git instaweb [--httpd=webrick] [--stop] | temporary GitWeb instance; port 1234 | 125-126 | [DATED] example with Ruby 1.8.6 / WEBrick 2009 and "Leopard" |
| make GITWEB_PROJECTROOT="/srv/git" prefix=/usr gitweb | generate gitweb.cgi from source | 126 | |
| git remote add gitlab https://server/namespace/project.git | remote for GitLab | 130 | |
| git diff --check | detects whitespace errors before the commit | 136 | |
| git add --patch | partial staging of a file to separate logical commits | 136 | |
| git log --no-merges | view a well-formatted history (e.g. in the Git repo) | 137 | |
| git fetch origin | brings in new content without merging | 139 | |
| git merge origin/master | merges what was fetched | 140 | |
| git log --no-merges issue54..origin/master | commits in origin/master that are not in issue54 | 141 | |
| git push -u origin featureA | -u = --set-upstream, configures tracking | 145, 147 | |
| git checkout -b featureB origin/master | create a topic branch from the server's master | 145, 151 | [DATED] `git switch -c` is the modern form (extrapolation, not here) |
| git push -u origin featureB:featureBee | push with a refspec to a remote branch of another name | 146-147 | |
| git log featureA..origin/featureA | see the colleague's new work on the shared branch | 147 | |
| git request-pull origin/master myfork | generates a summary (base, URL, commits, diffstat) to send by email to the maintainer | 150-151 | |
| git rebase origin/master ; git push -f myfork featureA | rebase your own branch and replace it in the fork | 152 | |
| git merge --squash featureB ; --no-commit | brings all the work in as a single change without a merge commit (a single parent); --no-commit postpones the normal merge commit | 153 | |
| git format-patch -M origin/master | generates .patch files (mbox), one per commit; -M detects renames | 153-154 | |
| git imap-send (cat *.patch \| git imap-send) | puts patches in the Drafts folder of an IMAP server | 155 | |
| git send-email *.patch | sends patches via SMTP (sendemail section in .gitconfig) | 155-156 | |
| git branch sc/ruby_client master ; git checkout -b sc/ruby_client master | create the maintainer's topic branch (name namespaced by the contributor) | 157 | |
| git apply <file> ; git apply --check | applies a git diff/Unix diff patch in the working dir (all or nothing, does not commit); --check tests and exits with status != 0 if it fails | 157-158 | |
| git am <file/mbox> | applies format-patch patches creating commits with author/message | 158 | |
| git am --resolved / --skip / --abort | continue, skip or abort after a failure | 159 | [DATED] not verified: recent versions use `--continue` (extrapolation); the book cites --resolved |
| git am -3 | tries a three-way merge (only works if the patch's base commit exists in your repo) | 159-160 | |
| git am -3 -i mbox | interactive mode: [y]es/[n]o/[e]dit/[v]iew/[a]ccept all | 160 | |
| git remote add jessica <url>; git fetch jessica; git checkout -b rubyclient jessica/ruby-client | test a contributor's remote branch | 160 | |
| git pull <URL> | one-off pull without saving a remote | 161 | |
| git log contrib --not master | commits in contrib missing from master (= master..contrib) | 161 | |
| git merge-base contrib master ; git diff $(git merge-base contrib master) | find the common ancestor and diff against it | 162 | |
| git diff master...contrib | triple-dot: what the topic branch introduced since the common ancestor with master | 162 | |
| git cherry-pick e43a6 | reapplies a commit on the current branch | 167 | |
| git config --global rerere.enabled true ; git rerere | enable/inspect reuse of resolutions | 168 | |
| git tag -s v1.5 -m '...' | signed tag | 168 | |
| gpg --list-keys; gpg -a --export <ID> \| git hash-object -w --stdin; git tag -a maintainer-pgp-pub <sha> ; git show maintainer-pgp-pub \| gpg --import | distribute the PGP public key as a blob + tag | 168-169 | |
| git describe master (--tags) | readable name (build number); by default requires annotated tags; --tags includes lightweight ones | 169 | |
| git archive master --prefix='project/' \| gzip > `git describe master`.tar.gz ; --format=zip | tarball/zip of the snapshot for those who do not use Git | 170 | |
| git shortlog --no-merges master --not v1.0.1 | changelog grouped by author since the last release | 170 | |

## Step-by-step procedures
### A. Set up a minimal Git server via SSH (PGEN p.116-121)
1. On the client: `git clone --bare my_project my_project.git` (p.116).
2. `scp -r my_project.git user@git.example.com:/srv/git` (p.117).
3. Whoever has SSH read access to /srv/git clones; whoever has write access to the directory can push (p.117).
4. Optional: `git init --bare --shared` inside the repo on the server to adjust group permission (p.117).
5. For many devs without their own account: `adduser git`, create ~/.ssh (700) and authorized_keys (600), append the public keys (p.119-120).
6. To create each new project: someone has to log into the server, `mkdir project.git && cd project.git && git init --bare` (p.120).
7. Dev: `git remote add origin git@gitserver:/srv/git/project.git` and `git push origin master` (p.120).
8. Restrict the account: add git-shell to /etc/shells, `sudo chsh git -s $(which git-shell)` (p.121); add the no-port-forwarding,... options per key (p.121).

### B. Generate an SSH key (PGEN p.118-119)
1. Check ~/.ssh for id_dsa/id_rsa + .pub (p.118). 2. If none, `ssh-keygen -o` (p.118-119). 3. Passphrase optional; use ssh-agent to avoid typing it every time (p.119). 4. Send the contents of the .pub to the admin (p.119).

### C. Serve via Git daemon (PGEN p.122-123)
1. Run `git daemon --reuseaddr --base-path=/srv/git/ /srv/git/` daemonized (p.122). 2. Open port 9418 in the firewall (p.122). 3. Create the systemd unit /etc/systemd/system/git-daemon.service (User=git Group=git, Restart=always) and `systemctl enable git-daemon` (p.122-123). 4. `touch git-daemon-export-ok` in each repo released (p.123).

### D. Smart HTTP with Apache (PGEN p.123-124)
1. Install apache2 and apache2-utils; `a2enmod cgi alias env` (p.123-124). 2. `chgrp -R www-data /srv/git` (p.124). 3. Config: GIT_PROJECT_ROOT, GIT_HTTP_EXPORT_ALL, ScriptAlias for git-http-backend (p.124). 4. A "git-http-backend" Files block with AuthType Basic requiring a valid user for writing (git-receive-pack) (p.124). 5. `htpasswd -c /srv/git/.htpasswd user` (p.124). 6. Use SSL to encrypt (p.124).

### E. Read-only Dumb HTTP (PGEN p.113-114)
1. In htdocs: `git clone --bare /path/to/git_project gitproject.git` (p.113). 2. `mv hooks/post-update.sample hooks/post-update; chmod a+x hooks/post-update` (p.113). 3. Clients: `git clone https://example.com/gitproject.git` (p.114).

### F. Private Small Team workflow (PGEN p.137-143)
1. Clone, commit locally (p.138). 2. `git push origin master`; if rejected as non-fast-forward: `git fetch origin` + `git merge origin/master`, test, `git push origin master` (p.139-140). 3. Optional: work in a topic branch (issue54), see what is missing with `git log --no-merges issue54..origin/master`, `git checkout master`, `git merge issue54`, `git merge origin/master`, push (p.141-143). The merge order does not change the final snapshot, only the history (p.142).

### G. Private Managed Team workflow (PGEN p.145-148)
1. Branch per feature (`git checkout -b featureA`), `git push -u origin featureA` (only integrators push to master) (p.145). 2. New feature from origin/master (p.145). 3. If a colleague already pushed another branch, fetch+merge and `git push -u origin featureB:featureBee` (p.146-147). 4. Receive the colleague's work: fetch, `git log featureA..origin/featureA`, merge origin/featureA (p.147). 5. Notify integrators; they merge into the mainline and a fetch brings in the merge commit (p.148).

### H. Contribute to a public project via fork (PGEN p.150-153)
1. Clone, `git checkout -b featureA`, commit (p.150). 2. Optional `rebase -i` to squash/reorder (p.150). 3. Fork on the site, `git remote add myfork <url>` (p.150). 4. `git push -u myfork featureA` (push the topic branch, not master) (p.150). 5. Pull request via the site or `git request-pull origin/master myfork` sent by email (p.150-151). 6. Second topic: new branch from origin/master (`git checkout -b featureB origin/master`) (p.151). 7. If it no longer merges cleanly: `git rebase origin/master` and `git push -f myfork featureA` (or branch featureAv2) (p.152). 8. If a change is requested: `git checkout -b featureBv2 origin/master`, `git merge --squash featureB`, adjust, commit, push (p.152-153).

### I. Contribute by email (PGEN p.153-156)
1. Topic branch and commits (p.153). 2. `git format-patch -M origin/master` (p.154). 3. Text added between the --- line and the diff is ignored by the patch process (p.154). 4. Send: paste into the client (formatting risk), `git imap-send` ([imap] config) or `git send-email` ([sendemail] config) (p.154-155). 5. Edit To/CC in Drafts and send (p.155).

### J. Maintainer applying a patch by email (PGEN p.157-160)
1. Create a topic branch (`git checkout -b sc/ruby_client master`) (p.157). 2. Patch from git diff/diff: `git apply --check` then `git apply`, and commit manually (p.157-158). 3. Patch from format-patch: `git am file.patch` (p.158). 4. Failure: resolve, `git add`, `git am --resolved`; or --skip/--abort; or `git am -3` (p.159-160). 5. Review what comes in: `git log contrib --not master`, `git diff master...contrib` (p.161-162). 6. Integrate (merge/rebase/cherry-pick) (p.160, 162-167).

### K. Prepare a release (PGEN p.168-170)
1. `git tag -s v1.5 -m '...'` (p.168). 2. Distribute the public key as blob+tag (p.168-169). 3. `git describe master` for a build name (p.169). 4. `git archive master --prefix='project/'` with gzip or --format=zip (p.170). 5. `git shortlog --no-merges master --not v1.0.1` for a changelog (p.170).

## Decision rules / heuristics / author's recommendations
- Prefer a common intermediary repository over direct push/pull between people's repos (it confuses the other person's work and depends on their computer being on) (PGEN p.111).
- Local protocol: use it if there is a shared filesystem; it is not necessarily fast (NFS can be slower than SSH) (p.112).
- Smart HTTP: probably the most popular; one URL for everything; crosses firewalls (p.113-114). Generally choose Smart OR Dumb, rarely mix them (p.114).
- SSH: good inside the corporate network; bad for anonymous/open-source access; if you want anonymous access, offer another means for reading (p.115).
- Git protocol: only if you want fast public read or heavy traffic without authentication (p.115); avoid unless you know what you are doing (p.115-116). Outside the firewall: public projects only; inside: read access by CI/build servers (p.122).
- For several devs without accounts: single git user with authorized_keys; the SSH user does not affect commit authorship (p.118). LDAP is an alternative (p.118).
- GitWeb is simple; for a full server use GitLab (more maintenance) (p.127). Third-party hosting: no maintenance; keep open source on a public site even with an internal server (p.130-131).
- Each commit should be a logical changeset; use the staging area/`git add --patch` to split; use history rewriting before sending (p.136).
- Message: first line up to ~50 characters, blank line, body (~72 columns) with motivation and contrast with previous behavior; imperative ("Fix bug", not "Fixed"); the blank line is critical, rebase gets confused without it; bullets with hyphen/asterisk and hanging indent (p.136-137). The author admits that the book's examples do not follow this (p.137).
- Before committing: `git diff --check` (p.136).
- On someone else's project: keep master tracking origin/master and work in disposable topic branches (p.151); new topic = new branch from origin/master, do not continue the previous one (p.151).
- Push the topic branch to the fork, not the merged master, so you do not have to rewind master if it is rejected/cherry-picked (p.150).
- Maintainer: test in a topic branch with a descriptive name; namespace like sc/ruby_client (p.157).
- Ask contributors for format-patch instead of diff; git apply only for legacy cases (p.158).
- Checking out a remote is worthwhile for a frequent contributor; for an occasional patch, email is less work; do not have hundreds of remotes (p.160). Advantage of the remote: history and standard three-way merge (p.161).
- To see what a merge would introduce use `git diff master...contrib`, not `git diff master` (p.161-162).
- Integration: (1) direct merge into master for simple projects (p.162-163); (2) two cycles: master only receives stable releases, develop receives everything; on tagging a release, fast-forward master (p.163); optionally an integrate branch before develop (p.164-165); (3) large projects: master/next/seen (formerly pu)/maint as in the Git project (p.165-166); (4) rebase or cherry-pick for linear history: rebase the topic onto master then fast-forward (p.166); cherry-pick to bring in just one commit (p.166-167).
- Rerere: enable globally if you do a lot of merging/rebasing or keep a long-lived topic branch (p.168).
- Tags: sign with -s when tagging a release as maintainer (p.168); git describe as a build number (p.169).

## Risks, warnings and anti-patterns
- The local protocol does not protect against accidental damage: any user with a shell can corrupt/remove Git internal files; having all repos on the same machine increases the risk of catastrophic loss (PGEN p.111-112).
- git:// without TLS: may lead to arbitrary code execution (an attacker on the route modifies the cloned repo); same for http://; https avoids it (barring a forged certificate); ssh only if you accept a wrong key (p.115-116). Port 9418 is commonly blocked by firewalls (p.116). Enabling push in the daemon lets anyone on the internet push (p.115).
- The Git daemon is public inside the network: everything served is accessible to everyone (p.122).
- Git account with a full shell: users can log in and use the shell and port forwarding; mitigate with git-shell and no-port-forwarding etc. options (p.121-122).
- git-http-backend does not authenticate; configure authentication in the web server and use SSL (p.124-125). Without GIT_HTTP_EXPORT_ALL only repos with git-daemon-export-ok are served anonymously (p.124).
- ssh-keygen: use -o when setting a passphrase (p.119).
- GitLab "Destroying" a user is permanent and destructive (removes projects and groups they own); prefer Blocking (p.128). The initial root password stays in /etc/gitlab/initial_root_password for at least 24h (p.127).
- A commit with whitespace errors bothers other devs (p.136). A giant commit with several subjects makes review and reversal harder (p.136).
- A message without a blank line between summary and body confuses tools such as rebase (p.137).
- On a non-fast-forward push, in Git (unlike Subversion) the merge is done locally even if different files were edited (p.139).
- `git push -f myfork featureA` after a rebase rewrites the remote branch; a safer alternative is another name (featureAv2) (p.152).
- Pasting a patch into the email client can break newlines/whitespace (p.154).
- Do not commit an email password in clear text: the [imap] example has `pass` and `sslverify = false` (extrapolation: sslverify=false is a risk; the book only shows the config, p.155).
- git apply is conservative (all or nothing); patch(1) may apply partially leaving a strange working dir (p.157). git apply does not create a commit (p.157).
- `git diff master` with diverging branches is misleading (it looks like the topic removes what belongs to master) (p.162).
- Direct merge into master can be problematic in large/stable projects (p.163).
- git describe: the abbreviated SHA may stop being valid (the kernel went from 8 to 10 characters) (p.169).
- cherry-pick generates a new SHA-1 (a new commit, not the same one) (p.167).
- The Git project's next and seen branches are rebased periodically (seen more often); master almost only advances (p.165).

## Illustrative examples/cases
- John and Jessica in the simplegit repo: illustrate a rejected non-fast-forward push and fetch+merge (p.138-143).
- featureA/featureB/featureBee: managed team, push with a refspec and integrators (p.145-148).
- Fork + request-pull with featureA/featureB/featureBv2: isolated topic branches as a "patch queue" (p.150-153).
- format-patch / imap-send / send-email with Gmail (p.154-156).
- Maintainer: apply vs am, conflict in ticgit.gemspec, am -3 (p.157-160).
- Cherry-pick of e43a6 (p.167). Release v1.6.2-rc1-20-g8c5b85c and shortlog since v1.0.1 (p.169-170).
- Diagrams: Fig.53 (central), 54 (integration-manager), 55 (dictator), 72-80 (merge/cherry-pick).

## Dated data / divergences from current practice
- master as the default branch in all examples (p.120, 138, 142 etc.) [DATED: today commonly main; not in the book].
- git checkout to create/switch branches (p.142, 145, 157) [DATED: git switch exists today; the book does not mention it here].
- git am --resolved (p.159) [DATED: the newer command uses --continue; extrapolation].
- git daemon / git:// protocol (p.115-116, 122): the book itself adds a security warning; production use is rare (extrapolation about the rarity; the warning is the book's).
- Examples with old dates/versions: Ruby 1.8.6, WEBrick 1.3.1, 2009, DSA 1024-bit and an RSA key with md5 fingerprint (p.119, 125-126, 168). 1024-bit DSA keys are considered weak today (extrapolation).
- References to GitHub/BitBucket/repo.or.cz as hosts with forking (p.149): the host list on the Git wiki points to archive.kernel.org/oldwiki (p.131), indicating an archived page.
- Hash: the book speaks of SHA-1 everywhere (p.139, 167, 169) [partly DATED: SHA-256 repos exist; not mentioned here].
- GitLab "Admin area" and Omnibus: UI description subject to change; cites merge requests and the password in /etc/gitlab/initial_root_password (p.127). The name "seen (formerly pu)" is already updated in the book (p.165).
- The text of page 150 says "BitBucket"; Gitorious/Google Code do not appear in this range.
- The git describe example cites the kernel's change from 8 to 10 chars; the book does not cite the current default abbreviation.

## What the book does NOT say here (gaps)
- Does not teach git switch/restore, branch main, SHA-256, ed25519, `git push --force-with-lease` (uses plain -f, p.152).
- Does not describe Gitolite/server-side hooks/per-branch permissions (only mentions GitLab hooks, p.129); does not cover per-repo authorization beyond filesystem/GitLab permissions.
- Does not detail `git request-pull` flags beyond the base+remote example, nor GitHub pull requests (refers to the GitHub chapter, p.150).
- Does not discuss `git format-patch` options beyond -M in this range (does not cover --cover-letter, -v, --stdout); does not discuss `git am --signoff`/Signed-off-by (only points to SubmittingPatches, p.136).
- Does not explicitly compare rebase vs merge with criteria for when to use each beyond "linear history" (p.166); the rule "do not rebase commits already published" does not appear in this range (it appears in the branching chapter, out of scope); the only push -f accepted is on a personal fork branch (p.152).
- Does not cover HTTP credential helpers in detail (refers to "Credential Storage", p.114).
- Does not cover backup, maintenance, server git gc, or detailed HTTPS/TLS setup (only "use SSL", p.124).
- Does not say that git instaweb and git-daemon are obsolete; only the security of git:// is discussed.
- The Git protocol is not said to be "forbidden": the book says "avoid unless you know what you are doing" (p.115).
- Message convention: the book does NOT require prefixes like Conventional Commits; does not mention exact limits for the body beyond "about 72".
- Tags: only shows tag -s and git describe; does not cover `git push --tags` beyond mentioning it (p.169); does not cover git tag -v in this range.


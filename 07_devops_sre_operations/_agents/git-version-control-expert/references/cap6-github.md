# Ch. 6 GitHub (PGEN p.172-223)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; printed EN page = PDF - 6; PT-BR = PDF - 5). A citation `(p.N)` without a sigla = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Reading note: EN text legible; figures (screenshots) not extracted, only captions. Printed page = N - 6.

## Section map: section title -> starting PDF page
- GitHub (chapter intro; "Interfaces Change" warning) -> 172
- Account Setup and Configuration -> 172
- SSH Access -> 173
- Your Avatar -> 174
- Your Email Addresses -> 176
- Two Factor Authentication -> 176
- Contributing to a Project / Forking Projects -> 177
- The GitHub Flow -> 178
- Creating a Pull Request -> 178
- Iterating on a Pull Request -> 182
- Not Only Forks -> 186
- Advanced Pull Requests / Pull Requests as Patches -> 186
- Keeping up with Upstream -> 186
- References (PR/Issue/SHA-1 cross-references) -> 188
- GitHub Flavored Markdown -> 190 (Task Lists 191, Code Snippets 192, Quoting 193, Emoji 194, Images 195)
- Keep your GitHub public repository up-to-date -> 195
- Maintaining a Project / Creating a New Repository -> 197
- Adding Collaborators -> 198
- Managing Pull Requests -> 199 (Email Notifications 200, Collaborating 201, Pull Request Refs 202, PRs on PRs 204)
- Mentions and Notifications -> 205 (Notifications Page 206, Web Notifications 207, Email Notifications 208)
- Special Files (README, CONTRIBUTING) -> 208 (README 209)
- Project Administration (Changing the Default Branch, Transferring a Project) -> 209-210
- Managing an organization (Organization Basics, Teams 211, Audit Log 213) -> 211
- Scripting GitHub / Services and Hooks (Services 215, Hooks 216) -> 214
- The GitHub API (Basic Usage 219, Commenting on an Issue 220, Changing the Status of a PR 221) -> 218
- Octokit, Summary -> 223

## Concepts and definitions
| EN term | PT-BR term | paraphrased definition | page |
|---|---|---|---|
| GitHub | GitHub | Largest host of Git repositories; central collaboration point; also hosts issues and code review. It is not part of the Git project itself. | 172 |
| fork | fork / bifurcacao | A whole copy of the project of your own, in your namespace, where you can push; on GitHub it does not carry the historical negative connotation (community split): it is just the same project in your namespace so you can contribute openly. | 177 |
| Pull Request (PR) | pull request | Mechanism to propose to the original repository the changes made in your fork; opens a discussion thread with code review until the owner is satisfied and merges. | 177 |
| GitHub Flow | fluxo do GitHub | Collaboration workflow centered on PRs and the Topic Branches workflow; it is the Integration-Manager workflow swapping email for web tools. | 178 |
| collaborator | colaborador | User added to the repo with "push" access (read + write on the project and the Git repo). | 198 |
| Organization | organizacao | Account with its own namespace that represents a group with shared ownership of projects (e.g. open source groups or companies). | 211 |
| Team | time/equipe | Grouping of user accounts and repositories inside the organization, with the type of access of each; access: read-only, read/write or administrative. | 211-212 |
| Audit Log | log de auditoria | Organization tab (for owners) with events that occurred, who did them and from where; filterable by type, location or person. | 213-214 |
| webhook / hook | webhook | You provide a URL and GitHub sends an HTTP payload to it on the chosen events; default: push event only. | 216 |
| Service | servico | Ready-made integration with external systems (CI, issue trackers, chat, documentation), e.g. email, Jenkins; most listen only to push. | 215-216 |
| personal access token | token de acesso pessoal | Alternative to username/password for authenticating to the API; has limited scopes and is revocable; generated in the "Applications" tab of settings; shown only once. | 220 |
| commit status | status de commit | Each commit can have 1+ statuses (state success/failure/error, description, target_url, context) via the API; CI uses it to report results. | 221-222 |
| context (of the status) | contexto | Field that distinguishes several statuses of the same commit (e.g. test service vs. validation). | 222 |
| refspec | refspec | `fetch =` line in .git/config that maps names on the remote to local names. | 203 |
| refs/pull/N/head | same | Pseudo-branch on the GitHub server pointing to the last commit of the PR's branch; outside refs/heads, so normal clone/fetch ignores it. | 203 |
| refs/pull/N/merge | same | Ref that represents the commit that would result from pressing the Merge button; lets you test the merge beforehand. | 204 |
| upstream | upstream | Name given (in the example) to the remote of the original repository from which the fork was made. | 187 |
| GitHub Flavored Markdown | Markdown do GitHub | Markdown with extras (task lists, fenced code, quoting, emoji, images by drag-and-drop) in issues, PRs, comments. | 190-191 |
| task list | lista de tarefas | List of checkboxes in an issue/PR; clickable without editing the Markdown; GitHub shows progress in the PR list. | 191-192 |
| trackback | trackback | Event created automatically in a PR's timeline when another one mentions it (e.g. a closed PR points to the one that replaced it). | 190 |
| 2FA | autenticacao em dois fatores | Requires a second method besides the password (TOTP app or SMS); mitigates a stolen password. | 176-177 |
| Octokit | Octokit | Open source libraries that wrap the API (Go, Objective-C, Ruby, .NET at the time of writing). | 223 |
| GitHub CLI | GitHub CLI | Official tool that replaces the web interface for most tasks; Windows, macOS, Linux. | 178 |

## Commands and options
| command | what it is for according to the book | page | dated? |
|---|---|---|---|
| git clone https://github.com/<user>/<repo> | clone your fork locally | 179 | |
| git checkout -b slow-blink | create a descriptive topic branch | 179 | [DATED] today `git switch -c` exists; checkout -b still works; the book does not mention switch here |
| git diff --word-diff | check the change (word-level diff) | 179 | |
| git commit -a -m '...' | commit on the topic branch | 180 | |
| git push origin slow-blink | send the topic branch to the fork | 180 | [DATED] the output shows a Username/Password prompt over HTTPS; today GitHub does not accept the account password for Git over HTTPS (token/credential manager/SSH is used) |
| git remote add upstream <url of the original> | register the original repo | 187 | |
| git fetch upstream | fetch new work from the original | 187 | |
| git merge upstream/master | bring the original's main branch into the topic branch (resolve conflict, commit, push) | 187 | [DATED] "master" as the default name; many repos use main today |
| git push origin slow-blink | update the existing PR (push to the same branch) | 187-188 | |
| git checkout master; git pull <url of the original>; git push origin master | update the fork's master without prior configuration | 196 | |
| git remote add progit <url>; git fetch progit; git branch --set-upstream-to=progit/master master; git config --local remote.pushDefault origin | automate fork sync: master pulls from upstream and pushes to origin | 196 | |
| git pull <url> patch-1 | merge a remote branch without adding a remote (line given in the PR notification email) | 200 | |
| curl https://github.com/<user>/<repo>/pull/1.patch \| git am | apply the PR as a patch (.diff and .patch URLs exist) | 200 | |
| git ls-remote <url or remote> | plumbing command that lists the server's refs, including refs/pull/* | 202-203 | |
| git fetch origin refs/pull/958/head | fetch a PR's ref into FETCH_HEAD (then git merge FETCH_HEAD) | 203 | |
| extra refspec `fetch = +refs/pull/*/head:refs/remotes/origin/pr/*` | bring all PRs in as local refs origin/pr/N (read-only, updated on fetch) | 203-204 | |
| git checkout pr/2 | test a PR's code locally | 204 | [DATED] today git switch pr/2 also works |
| git diff master...<branch> | equivalent to what the PR's "Files Changed" tab shows (aggregated unified diff) | 185 | |
| curl https://api.github.com/users/<user> | unauthenticated GET on the API | 219 | |
| curl https://api.github.com/gitignore/templates/Java | get a .gitignore template via the API | 219 | |
| curl -H "Content-Type: application/json" -H "Authorization: token TOKEN" --data '{"body":...}' https://api.github.com/repos/<user>/<repo>/issues/<n>/comments | comment on an issue via the API (POST) | 220 | [DATED] the current GitHub doc uses "Bearer"; "token" probably still works (confirm) |
| POST /repos/<user>/<repo>/statuses/<sha> | post a status on a commit | 222 | |

## Step-by-step procedures

### A. Create an account and configure it (PGEN p.172-177)
1. Visit github.com, choose a free username, provide email and password, click "Sign up for GitHub". (172)
2. Ignore the paid plans page for now; verify the email sent by GitHub (the book says it is important, as will be seen later). (173)
3. SSH: if you have no public key, generate one (the book refers to "Generating Your SSH Public Key"); in Account settings > "SSH keys" > "Add an SSH key": give it a name, paste the contents of ~/.ssh/id_rsa.pub (or whatever name you have), "Add key". Name the key well (e.g. "My Laptop") so you know which one to revoke later. (173-174)
4. Avatar (optional): Profile tab > "Upload new picture" and crop; if you already have an avatar on Gravatar, it is used by default. (174-175)
5. Emails: add all the emails used in commits in the Emails section; GitHub links commits to the user by email. States: primary (notifications/receipts), verified (can become primary), unverified (cannot be primary). (176)
6. 2FA: Account settings > Security tab > "Set up two-factor authentication"; choose a code generator app (TOTP) or SMS; afterwards login requires a code in addition to the password. (176-177)

### B. Contribute to a project (GitHub Flow, PGEN p.178-188)
1. Fork the project ("Fork" button, top right corner); in seconds you have a writable copy. (178)
2. Clone YOUR fork; create a descriptive topic branch; edit; check with git diff; commit; push the branch to origin (the fork). (179-180)
3. On the fork, GitHub detects the push of the new branch and shows a green button to open a PR; alternative: the "Branches" page at github.com/<user>/<project>/branches. (180)
4. Fill in title and description (worth the effort: helps the owner understand the goal and evaluate); the screen lists the "ahead" commits and the unified diff; click "Create pull request". (181-182)
5. The owner receives a notification; can comment on specific lines, merge or reject. (182-183)
6. To address requests: a new commit on the same topic branch + push updates the PR automatically (no need to re-roll the series). Added commits do NOT trigger a notification; leave a comment saying so. (184)
7. Owner merges: Merge button (appears only with write access and if the merge is trivial; does a non-fast-forward merge, always creates a merge commit) OR pulls the branch and merges locally; if merged locally into master and pushed, the PR closes by itself. (185-186)
8. Sync the fork's master back (step 8 of the flow). (178, 196)

Summary of the flow in 8 steps: fork; topic branch from master; commits; push to your project; open PR; discuss and commit more; owner merges or closes; sync master back to the fork. (178)

### C. The PR does not merge cleanly (PGEN p.186-188)
1. GitHub warns at the bottom of the PR whether the merge is trivial. (186)
2. Options: rebase onto the target branch OR merge the target into your branch; most people on GitHub choose merge (what matters is the history and the final merge; rebase only leaves the history a bit cleaner and is harder and error-prone). (187)
3. Merge: `git remote add upstream <url>`; `git fetch upstream`; `git merge upstream/master`; resolve conflict; `git add`; `git commit`; `git push origin <topic>` (same branch as the PR). The PR is rechecked by itself. (187-188)
4. If you REALLY want rebase: do not force push over the open PR's branch; push the rebased branch to a NEW branch, open a new PR referencing the old one and close the original. (188)

### D. Keep the fork up to date (PGEN p.195-196)
Without configuration: `git checkout master`, `git pull <url of the original>`, `git push origin master`. With configuration: additional remote + `--set-upstream-to` + `remote.pushDefault origin`; then `git checkout master`, `git pull`, `git push`. GitHub never updates the fork automatically. (195-196)
[DATED, extrapolation] today GitHub offers a "Sync fork" button in the interface; the book does not cite it.

### E. Create and administer a repository (PGEN p.197-199)
1. "New repository" on the dashboard or the "+" in the top bar; only the name is required; "Create Repository". The repo lives at <user>/<project_name>. (197-198)
2. GitHub shows instructions for a new repo or for connecting an existing project. (198)
3. URLs: HTTPS https://github.com/<user>/<project> and SSH git@github.com:<user>/<project>; both controlled by credentials. For a public project prefer sharing the HTTPS URL (clone without an account); SSH requires an account and an uploaded key. (198)
4. Collaborators: Settings (bottom of the right sidebar) > Collaborators > type the user > "Add collaborator"; revoke with the "X" on the row. (198-199)

### F. Manage an incoming PR (PGEN p.199-205)
1. PRs can come from a fork or from another branch of the same repo; difference: in a fork, normally neither party can push to the other's branch. (199)
2. The notification email brings the diffstat, a link and command-line commands (git pull <url> patch-1; .diff and .patch URLs). (200)
3. Conversation: comment on lines, whole commits or the PR; replying to the email comments on the PR. (201)
4. Merge: local (pull <url> <branch>, or add remote + fetch + merge) or the Merge button (non-ff). Do not want it? Close the PR; the author is notified. (201-202)
5. Many PRs: refspec refs/pull/*/head (see Commands); test with checkout pr/N; refs/pull/N/merge lets you test the merge before clicking. (202-204)
6. PR on a PR: when opening a PR, the "Edit" of the source/target box lets you change branches and even the fork; you can target another PR or another fork. (204-205)

### G. Notifications (PGEN p.205-208)
1. An @mention in any comment notifies the person (autocomplete lists collaborators/contributors; it also works with someone not on the list). (205)
2. You are "subscribed" to an item if: you were mentioned, opened it, watch the repo or commented; "Unsubscribe" button on the page. (206)
3. Notification center (settings): choose Email, Web, both or none, separately for active participation and for watched repos. (206-207)
4. Web: blue dot on the icon; filter by project; checkmark confirms; mute button stops notifying about that item. Many power users turn off email and use only the screen. (207-208)
5. Email: threaded; headers useful for filters (Message-ID in the format <user>/<project>/<type>/<id>; type = pull or issues; List-Post, List-Unsubscribe, X-GitHub-Recipient). Reading the email marks the web notification as read if images are enabled in the client. (208)

### H. Project administration (PGEN p.209-211)
1. Change the default branch: Settings > "Options" tab > default branch dropdown; applies to main operations, including the branch checked out on clone. (210)
2. Transfer: Options > "Transfer ownership" (to another user or organization); moves watchers and stars and creates a URL redirect, including for Git clone/fetch, not just web. (210)

### I. Organization (PGEN p.211-214)
1. "+" at the top > "New organization"; name, contact email, invite co-owners. (211)
2. Organizations are free if everything stored is open source. (211)
3. An owner can create repos and fork into the org's namespace; automatically watches new repos of the org. (211)
4. Teams: Teams sidebar > add members and repos > the team's Settings for access level (read, read/write, admin). The invitee receives an email. (212-213)

### J. Webhook (PGEN p.214-218)
1. Repo Settings > "Webhooks and Services" > "Add webhook". (216)
2. Provide the URL and secret key; choose events (default: push only). (216)
3. Bring up a small web service that reads the JSON payload and acts (example in Sinatra/Ruby filtering pusher, branch ref and touched files). (217)
4. Debug in the console of the same panel: latest deliveries, success, request/response body and headers; you can redeliver a payload. (217-218)

### K. API with a token (PGEN p.219-222)
1. Generate a token in settings > "Applications" tab; choose scopes and a good description; copy it (appears only once). (220)
2. Call the endpoint with the Authorization header. Unauthenticated: 60 req/hour; authenticated: up to 5,000 req/hour. (220)
3. Comment on an issue: POST repos/<user>/<repo>/issues/<num>/comments. (220)
4. Commit status: webhook -> service examines commits (e.g. requires Signed-off-by) -> POST /repos/<user>/<repo>/statuses/<sha> with state, description, target_url, context. The PR takes the status of the branch's LAST commit. (221-223)

## Decision rules / heuristics / author's recommendations
- To contribute to a project where you have no push access: fork + PR. (177)
- Two collaborators with write access to the same repo: no fork needed; push the topic branch and PR to master of the same project. (186)
- Out-of-date PR: prefer MERGING the target into your branch over rebase (history and the final merge matter; rebase is harder and error-prone). (187)
- If rebase is unavoidable: never force push over the branch of an open PR; new branch + new PR referencing the old one + close the original. (188)
- Answer review requests with new commits on the same branch, not by re-rolling the series: it preserves the context of the decisions. (186)
- The Merge button deliberately creates a merge commit that references the PR, making it easy to search for the original conversation. (186)
- Open the PR early in internal projects and iterate on it as a team, instead of only at the end; task lists help track progress. (182, 192)
- Share the HTTPS URL for a public project (without requiring an account/key). (198)
- Give recognizable names to SSH keys and good descriptions to tokens (to revoke safely). (174, 220)
- Prefer a personal access token over username/password on the API: limitable scope, revocable, higher rate limit. (220)
- Enable 2FA ("definitely"). (176)
- Special-interest teams (ux, css, legal) in addition to access-control teams; a user can be on several teams. (213)
- CONTRIBUTING is for contributors to read the guidelines before opening a PR; README for what the project is, installation, usage, license, how to contribute. (209)
- Many PRs: use the refs/pull/*/head refspec instead of single remotes or ad hoc pulls. (202-204)
- Use the email header metadata for filters and rules. (208)

## Risks, warnings and anti-patterns
- Interfaces change: the chapter's screenshots will age; the book itself warns. (172)
- A fork does not update itself: it falls behind ("N commits behind") until you sync it. (195-196)
- With the pull-from-upstream + pushDefault origin setup, Git does NOT warn if you committed directly to master before pulling from upstream and pushing to origin; never commit directly to master (it "belongs" to upstream). (196)
- Force push on a branch with an open PR: other people may have pulled and worked on it; refers to the problems of "The Perils of Rebasing". (188)
- New commits on an existing PR notify nobody: comment. (184)
- The API token is shown only once; save it. (220)
- Without authentication the API limits to 60 req/h. (220)
- The Merge button always creates a merge commit (non-ff) even when a fast-forward would be possible. (185, 201)
- Basic auth (username+password) on the API is cited as possible, but the book prefers a token. (220)
- refs/pull/* does not come with the default clone/fetch; a normal "git fetch" does not bring PRs without the extra refspec. (203)
- The Merge button only appears with write access and a trivial merge possible. (185)
- Project transfer moves watchers/stars and redirects the URL; a weighty action. (210)

## Illustrative examples/cases
- Tony/blink: fork of schacon/blink, branch slow-blink, delay from 1000 to 3000, PR, owner's comment asking for a longer off time, new commit on the same branch, conflict later resolved with a merge of upstream/master. Illustrates fork->PR->iteration->update. (178-188)
- Cross-references: #<num>, username#<num>, username/repo#<num>; PR and issue numbers are unique in the project. Mentioning an old PR in the new one generates a trackback in the closed one's timeline. (188-190)
- A full 40-character SHA-1 in a comment becomes a link to the commit; also works for forks/other repos. (190)
- Example of the progit/progit2 fork for sync (195-196).
- libgit2 example with refs/pull/958/head and the pr/* refspec (203-204).
- Sinatra: a service that sends email when a specific user pushes to a specific branch touching a specific file (217).
- Status with Signed-off-by validation (green check/red X on the PR) (221-223).
- Teams frontend/backend/deployscripts illustrate teams by role (212).
- Markup: task list `- [X]`/`- [ ]`; backtick fence with the language name for highlighting; `>` to quote (the r key quotes the selected text); `:name:` for emoji (autocomplete with `:`); drag-and-drop of images. (191-195)

## Dated data / divergences from current practice
- [DATED] The flow starts from "master" (step "Create a topic branch from master", 178); today the default branch is usually main (the book covers "Changing the Default Branch", 210).
- [DATED] HTTPS authentication by username/password (180, 220): GitHub stopped accepting the account password for Git over HTTPS and on the API (2021); today it uses PAT, credential manager or SSH. High confidence (outside knowledge); the book still describes basic auth as possible and a token as better.
- [DATED] "Webhooks and Services" (214-216): the Services system was discontinued by GitHub (c. 2018-2019), leaving webhooks (and GitHub Apps/Actions). High confidence; the book keeps describing Services (Email, Jenkins) as existing.
- [DATED] Settings menus ("Applications" tab, "Notification center", "SSH keys", "Security", "Options"): UI reorganized several times (e.g. "Developer settings > Personal access tokens"). The book warns on 172.
- [DATED, extrapolation] id_rsa.pub key (174): today ed25519 is the common choice.
- [DATED] Header `Authorization: token TOKEN` (220): the current doc uses Bearer.
- [DATED] Rate limits (60/h without auth; 5,000/h with auth) (220): historical values; check the current doc.
- [DATED] Octokit list "Go, Objective-C, Ruby, .NET" (223): the book says "at the time of writing"; there are more languages today.
- [DATED] API examples with 2014 dates (219, 221): illustrative.
- [DATED] 40-character SHA-1 (190): SHA-1 context; with SHA-256 it changes; the book says the full SHA is required to become a link.
- [DATED] git checkout to switch branches (179, 196, 204): today git switch.
- Orgs "free if everything is open source" (211): old commercial policy, check current pricing (173 refers to github.com/pricing).
- External links (Gravatar 175, webfx emoji cheat sheet 195, webhook docs 218): may have changed.

## What the book does NOT say here (gaps)
- Does not teach branch protection, required reviews, CODEOWNERS, rulesets, squash/rebase merge on the button (only cites non-ff merge, 185, 201).
- Does not cover GitHub Actions, Pages, Projects, Discussions, Wikis, Releases, Packages.
- Does not cover PR/Issue templates; labels/milestones only appear in the API's list of things (221).
- Does not mention GitHub Apps, OAuth apps, fine-grained tokens, GITHUB_TOKEN, SSO/SAML.
- Does not discuss deploy keys or commit signing on GitHub (only "validly signed" as an idea of status, 221).
- Does not teach HTTPS with a credential helper/PAT for Git (only the API), nor ed25519.
- Does not say how to delete/archive a repo or change visibility (public/private).
- Does not explain "Sync fork".
- Permission levels: only "read only / read/write / administrative" for teams (212) and "push" for collaborators (198).
- The webhook secret key is cited (216), but the Sinatra example does not validate the payload signature.
- Does not cite pagination, GraphQL or secondary rate limits.
- The Sinatra example compares the branch with 'ref/heads/special-branch' (217): the real push ref starts with refs/heads/; illustrative, do not copy.
- The gh CLI is only mentioned, without commands (178).


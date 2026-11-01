# Ch. 8 Customizing Git and Ch. 9 Git and Other Systems (PGEN p.342-419)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; printed EN page = PDF - 6; PT-BR = PDF - 5). A citation `(p.N)` without a sigla = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Source: Pro Git EN (ed. 2.1.450). Printed page = PDF - 6. All pages 342-419 were read. There is NO TFS/TFVC section in this text (ch. 9 covers only Subversion, Mercurial, Perforce and a custom importer via fast-import).

## Section map: title -> starting PDF page
- Customizing Git (intro) / Git Configuration (system/global/local levels) -> 342
- Basic Client Configuration: core.editor, commit.template -> 343; core.pager, user.signingkey, core.excludesfile -> 344; help.autocorrect -> 345
- Colors in Git (color.ui, color.*) -> 345-346
- External Merge and Diff Tools (P4Merge, extMerge/extDiff) -> 346; mergetool --tool-help -> 348
- Formatting and Whitespace: core.autocrlf -> 349; core.whitespace -> 350; git apply/rebase --whitespace -> 351
- Server Configuration: receive.fsckObjects, receive.denyNonFastForwards -> 351; receive.denyDeletes -> 352
- Git Attributes (.gitattributes, .git/info/attributes) -> 352
  - Binary Files: Identifying Binary Files -> 352; Diffing Binary Files (textconv: Word, EXIF) -> 353
  - Keyword Expansion (ident, clean/smudge filters, $Date$) -> 355
  - Exporting Your Repository (export-ignore) -> 358; export-subst -> 359
  - Merge Strategies (merge=ours) -> 360
- Git Hooks: Installing a Hook -> 360
  - Client-Side Hooks: Committing-Workflow -> 361; Email Workflow -> 361-362; Other Client Hooks -> 362
  - Server-Side Hooks (pre-receive, update, post-receive) -> 362-363
- An Example Git-Enforced Policy -> 363
  - Server-Side Hook (update), message format -> 363-364; ACL -> 365-367; Testing It Out -> 368
  - Client-Side Hooks (commit-msg, pre-commit with ACL, pre-rebase) -> 369-372
- Summary Ch.8 -> 372
- Ch.9 Git and Other Systems (intro) -> 373
- Git as a Client / Git and Subversion / git svn -> 373; Setting Up (svnsync) -> 374; Getting Started (git svn clone) -> 374-375; Committing Back (dcommit) -> 376; Pulling in New Changes (git svn rebase) -> 377; Git Branching Issues -> 379; Subversion Branching -> 380; Subversion Commands (log, blame, info, ignore) -> 381-382; Git-Svn Summary -> 383
- Git and Mercurial (git-remote-hg) -> 383; Getting Started -> 384; Workflow -> 386; Branches and Bookmarks -> 387; Mercurial Summary -> 390
- Git and Perforce -> 390; Git Fusion -> 391 (Setting Up 391, Fusion Configuration 393, Workflow 395, Summary 398); Git-p4 -> 398 (Setting Up 398, Getting Started 398, Workflow 399, Branching 404); Git and Perforce Summary -> 405
- Migrating to Git -> 405; Subversion (migration) -> 405; Mercurial (hg-fast-export) -> 408; Perforce (Git Fusion / git-p4) -> 410; A Custom Importer (fast-import) -> 411; Summary Ch.9 -> 419

## Concepts and definitions
| EN term | PT-BR (book) | paraphrased definition | page |
|---|---|---|---|
| Configuration levels | system / global / local | Git reads config at 3 levels: /etc/gitconfig (--system, all users), ~/.gitconfig or ~/.config/git/config (--global), the repo's .git/config (--local, default). Each level overrides the previous (local wins) | 342 |
| Client-side vs server-side options | - | Config options split into client (most, personal preferences) and server (few) | 342 |
| Git attributes | - | Per-path settings, in .gitattributes (in any directory, usually the root) or in .git/info/attributes (when you do not want to version the file) | 352 |
| textconv | - | Attribute diff=<name> + config diff.<name>.textconv: converts a binary to text before the diff (e.g.: docx2txt, exiftool) | 353-355 |
| ident | - | Attribute that replaces $Id$ with the SHA-1 of the BLOB (not of the commit) on checkout | 355 |
| clean / smudge filter | - | The "smudge" filter runs on checkout (before writing to disk); "clean" runs on staging (before going to the index/commit) | 356 |
| export-ignore | - | Attribute: the file/dir stays in the repo but does not go into git archive | 358 |
| export-subst | - | Attribute: applies git log-style formatting ($Format:...$) to the file when running git archive | 359 |
| merge driver | - | merge.<name>.driver defines how to merge paths with the attribute merge=<name>; a driver "ours" defined as the true command keeps your version | 360 |
| Hooks | - | Executable scripts in .git/hooks (no extension in the name) fired on events; two groups: client-side (commit, merge...) and server-side (received push) | 360 |
| .sample hooks | - | git init populates hooks/ with examples ending in .sample; rename (drop .sample) to activate; they document the arguments of each hook | 360 |
| rev-list | - | Plumbing: like git log but prints only SHA-1s; used in old..new to list the commits of a push | 364 |
| cat-file commit | - | Plumbing: shows the raw commit data; message = everything after the first blank line | 365 |
| ACL (from the example) | - | File "acl" in the bare repo on the server; lines avail\|users\|path (empty path = access to everything) | 366 |
| SHA^@ | - | Syntax that resolves to all parents of a commit (used in the example pre-rebase) | 372 |
| git svn | - | Bidirectional Git<->Subversion bridge: use Git as a client of an SVN server | 373 |
| bridge / remote helper | bridges | Adapters that let Git talk to another VCS; git-remote-hg is implemented as a remote helper | 373, 383 |
| git-svn-id | - | Line added by git svn dcommit to the commit message (unique SVN identifier); changes the SHA-1 | 376-377 |
| bookmark (Mercurial) | - | Movable ref equivalent to a Git branch; the Mercurial "branch" is heavy (recorded in the changeset, eternal) | 387 |
| refs/hg, notes/hg | - | Where git-remote-hg stores the real remote refs and the mapping Git hash -> Mercurial changeset | 385 |
| Git Fusion | - | Perforce product, server side: exposes depot subtrees as read/write Git repositories | 391 |
| git-p4 | - | Client bridge: Git as a Perforce client without reconfiguring the server; needs the p4 client in the PATH | 391, 398 |
| p4gf_config / p4gf_usermap | - | Git Fusion INI config files (global and per repo) and Perforce<->Git user map | 393-395 |
| fast-import | - | Command that reads simple instructions from stdin and writes Git objects; basis for custom importers | 412 |
| mark | - | Integer identifier given to a commit in fast-import, used to link commits (from :N) | 413 |
| peg-revision | - | SVN feature with no Git equivalent; git svn generates branches with the suffix @NNN | 407 |

## Commands and options
| command | what it is for according to the book | page | dated? |
|---|---|---|---|
| git config --system / --global / --local | Chooses the level of the config file read/written | 342 | |
| man git-config | Lists all options; there are also "Conditional includes" for advanced use | 342-343 | |
| core.editor | Editor used for commit/tag messages (default: VISUAL/EDITOR, otherwise vi) | 343 | |
| commit.template | Path of a file used as the initial commit message (helps enforce a message policy) | 343-344 | |
| core.pager | Pager (default less); empty string '' turns off paging | 344 | |
| user.signingkey | GPG key ID; allows git tag -s <name> without giving the key | 344 | |
| core.excludesfile | Global ignore file (e.g.: ~/.gitignore_global with *~, .*.swp, .DS_Store) | 345 | |
| help.autocorrect | Integer in tenths of a second; 1 runs the corrected command automatically (50 = 5 s to give up) | 345 | |
| color.ui | false turns colors off; auto (default) colors only in a terminal; always colors even in a pipe (rarely desirable; prefer --color) | 345-346 | |
| color.branch / color.diff / color.interactive / color.status and sub-options (e.g.: color.diff.meta "blue black bold") | Colors per verb; color values: normal, black, red, green, yellow, blue, magenta, cyan, white; attributes bold, dim, ul, blink, reverse | 346 | |
| merge.tool, mergetool.<tool>.cmd, mergetool.<tool>.trustExitCode, diff.external | Configure an external merge/diff tool (extMerge/extDiff example with P4Merge) | 347 | |
| git mergetool [--tool=<tool>] / git mergetool --tool-help | Opens a GUI for conflicts; lists supported tools (emerge, gvimdiff, opendiff, p4merge, vimdiff... and others "valid but not available": kdiff3, meld, etc.) | 348-349 | |
| core.autocrlf true / input / false | Line-ending conversion (see Rules) | 349-350 | |
| core.whitespace | Chooses which whitespace problems to detect (comma-separated list, - turns off) | 350 | |
| git apply --whitespace=warn / =fix | Warns about or fixes whitespace problems when applying a patch | 351 | |
| git rebase --whitespace=fix | Fixes whitespace when rewriting (only if you have not pushed yet) | 351 | |
| receive.fsckObjects (use with --system on the server) | Checks SHA-1 and validity of objects on every push; costly, off by default | 351 | |
| receive.denyNonFastForwards | Refuses non-fast-forward pushes (includes force-push) | 351-352 | |
| receive.denyDeletes | Refuses deleting remote branches/tags; closes the workaround of deleting and recreating the branch | 352 | |
| .gitattributes: `*.pbxproj binary` | Treats the file as binary: no CRLF conversion and no diff in git show/diff | 352-353 | |
| .gitattributes: `*.docx diff=word` + git config diff.word.textconv docx2txt | Readable Word diff via a wrapper script (docx2txt.pl "$1" -) | 353 | |
| .gitattributes: `*.png diff=exif` + diff.exif.textconv exiftool | Image diff via EXIF metadata | 354-355 | |
| .gitattributes: `*.txt ident` | Expands $Id$ with the blob SHA-1 on checkout | 355-356 | |
| filter.<name>.clean / .smudge + attribute `filter=<name>` | Content filters on stage/checkout (e.g.: indent + cat; dater with expand_date and perl) | 357-358 | |
| `test/ export-ignore` + git archive | Excludes paths from the exported tarball | 358-359 | |
| `LAST_COMMIT export-subst` + $Format:%cd by %aN$ | Injects last-commit metadata into git archive | 359 | |
| `database.xml merge=ours` + git config --global merge.ours.driver true | On merge, always keeps your version of the file (no conflict) | 360 | |
| chmod u+x .git/hooks/update | The hook must be executable | 368 | |
| git commit --no-verify | Skips the pre-commit hook | 361 | |
| git rev-list old..new | SHA-1s of the commits of a push | 364 | |
| git cat-file commit <sha> \| sed '1,/^$/d' | Extracts the commit message | 365 | |
| git log -1 --name-only --pretty=format:'' <rev> | Lists files modified in a commit (server) | 367 | |
| git diff-index --cached --name-only HEAD | Lists files in the index (pre-commit, client) | 371 | |
| git svn clone <url> -T trunk -b branches -t tags (or -s) | Imports an SVN repo (init + fetch); -s = standard layout | 375 | |
| git svn dcommit | Sends local commits to SVN, one SVN commit per Git commit; REWRITES commits (new SHA-1s, git-svn-id) | 376-377 | |
| git svn rebase | fetch from SVN + rebase of local work; requires a clean tree (stash or commit first) | 377-379 | |
| git svn fetch | Only fetches new data | 379 | |
| git svn branch <name> | Creates a branch on the SVN server (equivalent to svn copy trunk branches/name); does NOT check it out | 380 | |
| git svn log / blame <file> / info | Offline equivalents of svn log/annotate/info; show only the last known state of the SVN server | 381-382 | |
| git svn create-ignore / show-ignore | Generates .gitignore from svn:ignore, or prints the lines (e.g.: > .git/info/exclude) | 382-383 | |
| git clone hg::<path> (git-remote-hg) | Clones a Mercurial repo; pip install mercurial and the hg client are required | 383-384 | |
| cp .hgignore .git/info/exclude | Reuses Mercurial ignores without committing a .gitignore | 385 | |
| git p4 clone //depot/path[@all] [--detect-branches] | Imports/clones Perforce; without @all = "shallow" clone (only the latest revision) | 399, 404 | |
| git p4 sync / git p4 rebase / git p4 submit [-n] | Syncs, rebases onto p4/master, sends commits as changelists (-n = dry-run) | 399-403 | |
| git config git-p4.branchList main:dev | Gives the branch mapping when the server has no branch specs | 404-405 | |
| git svn clone --authors-file=users.txt --no-metadata --prefix "" -s | Clean SVN import (mapped authors, no git-svn-id) | 406 | |
| hg-fast-export.sh -r <hg repo> -A authors [-B branches] [-T tags] | Converts Mercurial to Git via fast-import | 409 | |
| git filter-branch --msg-filter 'sed -e "/^\[git-p4:/d"' | Removes the git-p4 marker from messages; changes all SHA-1s | 411-412 | [DATED] filter-branch (see Dated data) |
| git fast-import (reads stdin) | Custom importer; commands: commit refs/heads/master, mark :N, committer, data N, from :N, deleteall, M 644 inline path | 412-417 | |
| git reset --hard master (after fast-import) | Populates the working directory (nothing is checked out after the import) | 419 | |

## Step-by-step procedures

### P1. Configure an external merge/diff tool (P4Merge) (PGEN p.346-348)
1. Create a wrapper script extMerge that calls the binary with $* (346-347).
2. Create extDiff: Git passes 7 arguments (path old-file old-hex old-mode new-file new-hex new-mode); the wrapper checks for 7 args and passes only $2 and $5 to extMerge (347).
3. chmod +x on both scripts (347).
4. git config --global merge.tool extMerge; mergetool.extMerge.cmd 'extMerge "$BASE" "$LOCAL" "$REMOTE" "$MERGED"'; mergetool.extMerge.trustExitCode false; diff.external extDiff (347).
5. git diff now opens the GUI; on a merge conflict, run git mergetool (348).
6. Switching tools = just edit the extMerge wrapper (348). If you only want to use the tool for merge and the internal diff, simply git config --global merge.tool kdiff3 (349).

### P2. Normalize line endings between Windows and Unix (PGEN p.349-350)
1. Windows: git config --global core.autocrlf true (CRLF on checkout, LF in the repo).
2. Linux/macOS: git config --global core.autocrlf input (converts CRLF->LF on commit, does not convert on checkout).
3. Windows-only project: core.autocrlf false (records CR in the repo).

### P3. Readable diff of .docx (PGEN p.353-354)
1. .gitattributes: `*.docx diff=word`.
2. Install docx2txt; create a wrapper in the PATH with `docx2txt.pl "$1" -`; chmod a+x.
3. git config diff.word.textconv docx2txt. Stated limit: formatting changes do not appear (354).

### P4. Expand $Date$ with clean/smudge filters (PGEN p.357-358)
1. Script expand_date (reads stdin, replaces $Date$ with the date of the latest git log -1) in the PATH.
2. git config filter.dater.smudge expand_date; filter.dater.clean with perl that reverts $Date: ...$ to $Date$.
3. .gitattributes: `date*.txt filter=dater`.
4. Test: commit, delete the file, git checkout, cat.

### P5. Install a hook (PGEN p.360)
1. Create/rename a file in .git/hooks with the exact hook name (no extension); any language works.
2. Make it executable (chmod +x/u+x) (360, 368).
3. Remember: client-side hooks are not cloned; distribute them by other means (in the project or a separate repo) and each user copies them to .git/hooks (361, 369).

### P6. Policy enforced on the server via the update hook (PGEN p.363-368)
1. Put everything in the `update` file of the bare repo's hooks directory; it runs once per branch and receives 3 args: refname, oldrev, newrev (363-364).
2. Get the user: via SSH; if everyone logs in as a single "git" user with a public key, use a shell wrapper that sets an environment variable according to the key (364). The example assumes $USER.
3. Message format: list commits with git rev-list oldrev..newrev; for each, git cat-file commit <rev> | sed '1,/^$/d'; test regex `\[ref: (\d+)\]`; if it fails, print [POLICY] and exit 1 (364-365).
4. ACL: file `acl` in the bare repo; the parser reads only avail directives; for each commit, git log -1 --name-only --pretty=format:'' and checks whether the path starts with one of the user's allowed paths; otherwise exit 1 (365-367).
5. chmod u+x .git/hooks/update. The rejected push shows "remote rejected ... (hook declined)" per ref; everything the hook prints to stdout goes to the client (368).

### P7. Mirror the policy on the client (PGEN p.369-372)
1. Distribute hooks (they are not copied on clone) and instruct users to copy them to .git/hooks (369).
2. commit-msg: reads the file passed in ARGV[0], applies the same regex, exit 1 if it does not match (369-370).
3. pre-commit with ACL: copy of the acl in .git/acl; only differences: the ACL path and listing via git diff-index --cached --name-only HEAD (370-371). Caveat: assumes the local user is the same as the push user; otherwise set $user manually (371).
4. Optional pre-rebase: lists commits to be rewritten (git rev-list base..topic) and aborts if any is already reachable from remote refs (git rev-list ^sha^@ refs/remotes/<ref>) (371-372).

### P8. Use git svn as a client (PGEN p.373-379)
1. git svn clone <url> -s (or -T/-b/-t) (375). It can take hours/days on a large history (375).
2. Normal local commits; several offline (376).
3. git svn dcommit to publish; rejected if SVN says "out of date" due to a conflict (377).
4. git svn rebase (requires a clean tree), resolve, repeat dcommit (377-379).
5. Run git svn rebase periodically (379).

### P9. Migrate SVN -> Git (PGEN p.405-408)
1. Generate the author list: svn log --xml --quiet | grep author | sort -u | perl -pe 's/.*>(.*?)<.*/$1 = /' > users.txt; fill in the Git name and email (405-406). On Windows the book points to a Microsoft guide (406).
2. git svn clone <url> --authors-file=users.txt --no-metadata --prefix "" -s my_project (406). If you need to mirror commits back to SVN, do NOT use --no-metadata (406).
3. Convert remote tags into tags: for t in $(git for-each-ref --format='%(refname:short)' refs/remotes/tags); do git tag ${t/tags\//} $t && git branch -D -r $t; done (407).
4. Convert the remaining remote refs into local branches (loop with git branch $b refs/remotes/$b && git branch -D -r $b) (407).
5. Remove @NNN branches (peg-revisions) if they do not matter (407).
6. git branch -d trunk (points to the same place as master) (407).
7. git remote add origin <url>; git push origin --all; git push origin --tags (407-408).

### P10. Migrate Mercurial -> Git (PGEN p.408-410)
1. git clone https://github.com/frej/fast-export.git; hg clone <repo> /tmp/hg-repo (408).
2. Generate authors: hg log | grep user: | sort | uniq | sed 's/user: *//' > ../authors; edit into rules "<input>"="<output>" (408-409). An author without a rule passes through unchanged (408-409). The same format works for renaming branches/tags (-B, -T) (409).
3. git init /tmp/converted; run hg-fast-export.sh -r <hg-repo> -A <authors> (409).
4. git remote add origin ...; git push origin --all (410). Hg tags become Git tags; branches and bookmarks become branches (410).

### P11. Migrate Perforce -> Git (PGEN p.410-412)
1. Git Fusion: configure project/users/branches and clone; the result is a native Git repo; it can even use Perforce as a Git host (410).
2. git-p4: export P4PORT; git p4 clone //depot/path@all destination (411); --detect-branches for several branches (411).
3. Optional: remove the [git-p4: depot-paths ...] marker with git filter-branch --msg-filter; ALL SHA-1s change; do it before starting to work in the new repo (411-412).

### P12. Custom importer with fast-import (PGEN p.411-419)
1. Write a script that reads the source system and prints instructions to stdout; run `ruby import.rb <dir> | git fast-import` inside an already initialized repo (git init) (412, 418).
2. For each snapshot: `commit refs/heads/master`, `mark :N` (integer), `committer Name <email> <epoch> <tz>`, message in the format `data <size>\n<content>`, `from :<previous mark>` if any, `deleteall`, and for each file `M 644 inline <path>` + data (413-415). Use 755 for executables (415).
3. On Windows: no CRLF (fast-import only accepts LF); in Ruby, $stdout.binmode (413, 416).
4. At the end nothing is checked out: git reset --hard master (419).

## Decision rules / heuristics / author recommendations
- To enforce policy (message format, ACL), do it on the SERVER; client hooks are not copied on clone and therefore enforce nothing (361). A client hook serves to warn early and avoid the "rejected at the last minute" (369).
- To deny non-fast-forward: you can use receive.denyNonFastForwards, or a server hook if you need per-user exceptions (352). To deny deletion for everyone: receive.denyDeletes; per user: ACLs (352).
- core.autocrlf: Windows -> true; Linux/macOS -> input; Windows-only project -> false (350).
- pre-commit: aborts with a non-zero exit; bypassable with --no-verify (361). This reinforces that real policy lives on the server.
- prepare-commit-msg is useful for autogenerated messages (template, merge, squash, amend), not for normal commits (361).
- post-receive cannot stop the push, but the client only disconnects when it finishes: avoid long tasks (363).
- update vs pre-receive: pre-receive runs once and rejects ALL refs; update runs per branch and rejects only that ref (363).
- When writing hooks that others will read, prefer long command-line flags (363).
- Attribute filters/drivers: .gitattributes goes with the project but the driver (config) does not; design filters to fail gracefully and the project keep working (358).
- git svn: keep history linear, rebase instead of merge, never rewrite and try to push again, do not collaborate on a parallel Git server (373, 383). If the team is mixed, everyone collaborates through the SVN server (373-374).
- If you must push to a Git server and SVN: dcommit to SVN FIRST, since it changes the commits (377).
- Branching with git svn: if you can avoid SVN branches, better (380); after merging a local SVN branch, delete the local branch (381).
- A parallel Git server is allowed at most to speed up clones, and only with commits that have git-svn-id; suggestion of a pre-receive that rejects commits without git-svn-id (383).
- If you can switch to a real Git server, the gain is much greater (383).
- Mercurial: avoid changing history that has already left your machine (390). Hg bookmarks cannot be deleted from the Git side (389).
- Perforce/git-p4: Perforce rules the code; do not push to a shared Git remote commits that have not been submitted to Perforce (405). Git Fusion if you can convince the admin (405).
- git-p4: use git p4 submit -n (dry-run) first; merges in Git are linearized (403). If you want a single changeset, do an interactive rebase/squash before submit (402).
- Migration: do it right (mapped authors) because the import takes a long time (405). If there is no ready-made importer, use git fast-import (411).

## Risks, warnings and anti-patterns
- git svn dcommit rewrites local commits and changes all SHA-1s (377); so do not mix with a Git remote (377).
- SVN history is linear: git svn only follows the first parent; a merge becomes a single "squashed" commit in SVN and the branch's commits are not rewritten (379-380). After a branch merge, dcommit erases the merge information, and future merge-base calculations are wrong (381).
- The SVN state after a commit may not exist on any machine: the automatic rebase on dcommit generates a never-tested state; incompatible-but-conflict-free changes can cause hard-to-diagnose bugs (379).
- git svn rebase with a dirty tree stops if the rebase generates a conflict: stash or commit first (379).
- git svn branch does not change the active branch: the next commit goes to trunk (380).
- git svn clone of a large history: hours or days (375); svnsync to a remote repo: almost 1 hour for <100 commits (374).
- git svn log/blame/info are offline and show only the last known state of SVN (381-382).
- "Crippled Git": the book calls git svn a limited Git; follow the guidelines to avoid confusion (383).
- Mercurial: interactive rebase + force-push creates new changesets and keeps the old ones in the Hg repo, confusing colleagues (390). Bookmarks not deletable from the Git side (389).
- Git Fusion: an attempt to rewrite already-pushed history is rejected (398). The example setup uses GIT_SSL_NO_VERIFY=true only because of the demo VM's certificate; for a permanent installation install another certificate (392-393).
- git-p4: clone without @all is "shallow"; does not mix shallow with multiple branches (399, 405). Does not create/integrate branches in Perforce; a Git merge sent loses integration metadata (405). "p4" remotes are not real remotes and you do not push to them (399). git-p4 alters SHA-1s by adding a [git-p4: ...] line to each commit (402).
- git filter-branch to clean markers changes all SHA-1s (412) - do it before any work.
- fast-import on Windows: CRLF breaks; use binmode (413, 416). Fixed mode 644 in the example: executables need 755 (415). Fixed timezone -0700 in the example; in a real import give the correct offset (414).
- Server: receive.fsckObjects is expensive on large repos/pushes (351).
- core.whitespace/apply: --whitespace=fix in a rebase only before push (351).
- help.autocorrect=1 runs the command automatically: risk of running an unexpected command; larger values give time to cancel (345).
- color.ui always: rarely desirable (346).
- Example pre-rebase hook: slow and often unnecessary, the server already refuses force-push (372); the example hook that Git installs makes assumptions that may not match (362).
- Exported file (export-subst/git archive) is for deployment, not for development (359).
- The client-side hooks of the ACL example presuppose the same local and remote user (371). The book's ACL pre-commit example has an unclosed if/end block on the page (370); treat it as pseudo-code.

## Illustrative examples/cases
- extMerge/extDiff with P4Merge/KDiff3: the wrapper lets you swap tools by editing one file (346-349).
- .pbxproj as binary: a text file that is in practice a database generated by an IDE (352-353).
- docx2txt and exiftool: textconv turns a binary into diffable text (353-355).
- indent via clean + cat via smudge: formats C code before the commit (357); dater: RCS-style $Date$ (357-358).
- LAST_COMMIT export-subst: commit metadata in the deployment tarball (359).
- database.xml merge=ours: keep a branch-specific database config (360).
- Complete policy: regex [ref: NNNN] (ticket) + ACL avail|users|path (364-367); tested with a rejected push -f (368); client mirror with commit-msg/pre-commit (369-371).
- svnsync to create a writable test SVN repo (374). git svn dcommit with SVN "Transaction is out of date" (377).
- hello Hg repo with git-remote-hg: fetch/merge/push; hg log shows changesets 3 and 4 made by git-remote-hg (386-387).
- Git Fusion: demo VM, projects Talkhouse and Jam, usermap to anonymize authors (391-395); p4v revision graph shows an anonymous branch in .git-fusion (398).
- git-p4: submit turning 3 non-merge commits into 3 changelists and linearizing history (403).
- Importer of backups in dated directories (back_YYYY_MM_DD + current) via fast-import (412-419).

## Dated data / divergences from current practice
- The default branch `master` appears in several examples (git svn, git-remote-hg, git push) - [DATED] today the default in new repos is often main (the book uses master by convention; I only note it, there is no text on the page saying this).
- `git checkout -- test.txt` to restore/regenerate a file (356) and `git checkout -b` (388, 389) - [DATED] today git restore / git switch -c (general knowledge; not stated on those pages).
- The commit status message on 344 cites "git reset HEAD <file>" to unstage - [DATED] newer versions suggest git restore --staged (extrapolation; example text on the page).
- SHA-1: receive.fsckObjects talks about SHA-1 (351), ident uses the blob SHA-1 (355) - [DATED] SHA-256 repos exist today (extrapolation).
- Third-party services/tools: Google Code (382, 406), Git Fusion (391-398), P4Merge, TFS absent - [DATED] Google Code was shut down; Git Fusion was discontinued by Perforce (general knowledge, not on the page); selenic.com/repo/hello (384) may be dead.
- git svn / git-svn-id examples from 2009-2014; git-remote-hg (felipec) downloaded from GitHub via curl (383) - check maintenance before using.
- git filter-branch (412) - [DATED] the official documentation itself now discourages filter-branch and recommends git filter-repo (general knowledge; not on these pages).
- mergetool --tool-help lists tools (348-349) - the list changes by version.
- External command `rev-list ^sha^@` and Ruby: illustrative examples, the book itself says it may be slow (372).

## What the book does NOT say here (gaps)
- Does not cite core.hooksPath nor shared/versioned hooks (says only that client hooks are not cloned and must be distributed by other means, 361, 369).
- There is no list of hook environment variables (GIT_DIR, etc.); only cites $USER as an assumption in the example (364).
- Does not talk about TFS/TFVC/Azure DevOps as a bridge (there is only a reference to a Microsoft guide for SVN on Windows, 406).
- Does not cover git-lfs, git filter-repo, .gitattributes text=auto/eol, nor `core.safecrlf`; autocrlf is treated only with true/input/false (350).
- Does not describe the hooks fsmonitor, pre-merge-commit, reference-transaction, push-to-checkout, post-update, sendemail-validate (list given: pre-commit, prepare-commit-msg, commit-msg, post-commit, applypatch-msg, pre-applypatch, post-applypatch, pre-rebase, post-rewrite, post-checkout, post-merge, pre-push, pre-auto-gc, pre-receive, update, post-receive).
- Does not describe the execution order of pre-receive vs update beyond "pre-receive is the first" (363).
- Does not say how to identify users on Git servers without SSH (only cites SSH and a shell wrapper, 364).
- Does not talk about authentication/per-branch permissions on hosted platforms here (that belongs to another chapter).
- git svn: does not cover SVN tags on write, nor externals; only create-ignore/show-ignore (382-383).
- There is no comparison of performance/limits of git-remote-hg beyond the non-deletable bookmark and immutable history (389-390).
- The text says pre-push runs "after the remote refs have been updated but before any objects have been transferred" (362); nothing more about pre-push arguments and stdin (it says: name and location of the remote as parameters, list of refs on stdin).


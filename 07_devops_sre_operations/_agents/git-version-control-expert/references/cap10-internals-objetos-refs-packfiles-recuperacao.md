# Ch. 10 Git Internals ("Funcionamento Interno" in the Portuguese edition) (PGEN p.420-458)

> Convention of this file: page = PDF PAGE number (PAGE N marker of the extracted text; EN printed page = PDF - 6; PT-BR = PDF - 5). Citation `(p.N)` without an abbreviation = PGEN (Pro Git EN, ed. 2.1.450). Labels: [from source] is the content of the lines with a page; [extrapolation]/[DATED] are marked in their own sections. Paraphrased; does not replace the book.


Note: printed page = N - 6. Page 459 is already Appendix A (out of scope). The chapter ends at p.458 (Summary).

## Section map: section title -> starting PDF page
- Git Internals (intro; Git = content-addressable filesystem + VCS UI) -> 420
- Plumbing and Porcelain (and contents of .git/) -> 420
- Git Objects (hash-object, cat-file, blob) -> 421
- Tree Objects (update-index, write-tree, read-tree) -> 423
- Commit Objects (commit-tree) -> 426
- Object Storage (file format: header + zlib; Ruby demo) -> 429
- Git References (refs/heads, update-ref) -> 431
- The HEAD (symbolic-ref) -> 432
- Tags (lightweight x annotated, tag object) -> 433
- Remotes (refs/remotes) -> 434
- Packfiles (loose x pack, git gc, verify-pack) -> 435
- The Refspec (fetch) -> 438
- Pushing Refspecs -> 440
- Deleting References -> 440
- Transfer Protocols (dumb/smart) -> 441
- The Dumb Protocol -> 441
- The Smart Protocol (send-pack/receive-pack, fetch-pack/upload-pack; SSH and HTTP(S)) -> 443
- Protocols Summary -> 446
- Maintenance and Data Recovery / Maintenance (auto gc, packed-refs) -> 446
- Data Recovery (reflog, git log -g, fsck) -> 447
- Removing Objects (large object; filter-branch; prune) -> 449
- Environment Variables (Global, Repository Locations, Pathspecs, Committing, Networking, Diffing/Merging, Debugging, Miscellaneous) -> 453
- Summary -> 458

## Concepts and definitions (EN term | PT-BR term | definition | page)
- content-addressable filesystem | sistema de arquivos de conteúdo endereçável | Git is, at its core, a simple key-value store: you insert any content and get back a unique key to retrieve it later; the VCS interface is a layer written on top | p.420, p.421
- plumbing | encanamento | low-level subcommands, designed to be chained UNIX-style or used in scripts; many were not designed for manual use | p.420
- porcelain | porcelana | the friendly everyday commands (checkout, branch, remote...); the first 9 chapters deal almost only with them | p.420
- .git directory | same | where almost everything Git stores lives; copying just this directory gives almost everything needed for backup/clone | p.420
- Contents of a newly created .git: config, description, HEAD, hooks/, info/, objects/, refs/ (the index file does not exist yet until the first staging) | p.420-421
- description | file | used only by the GitWeb program | p.421
- config | file | project-specific configuration options | p.421
- info/ | directory | holds a global exclude file (ignored patterns that are not kept in .gitignore) | p.421
- hooks/ | directory | client/server hook scripts | p.421
- Four central entries: HEAD, index, objects/, refs/ | p.421
  - objects/ = all the database content; refs/ = pointers to commits (branches, tags, remotes etc.); HEAD = points to the branch currently checked out; index = staging area | p.421
- A newly created objects/ has only info/ and pack/ and no regular file | p.421
- blob | blob | object that stores only the CONTENT of a file (it does not store the file name); roughly corresponds to an inode/content | p.423
- tree | tree | object that corresponds to a UNIX directory entry; contains 1+ entries, each with mode, type (blob or tree), SHA-1 and name | p.423
- valid modes for files (blobs): 100644 (normal), 100755 (executable), 120000 (symbolic link); other modes only for directories (040000, seen p.423) and submodules | p.425
- commit object | commit | points to the top-level tree of the snapshot, parents (if any), author/committer (user.name, user.email and timestamp), blank line and message | p.427
- tag object (annotated) | annotated tag | fourth object type: has tagger, date, message and a pointer; normally points to a commit but can point to any object; "like a branch that never moves" | p.433, p.434
- reference / ref | reference | simple name stored in a file under .git/refs that contains a SHA-1 | p.431
- branch | branch | basically a simple pointer/reference to the tip of a line of work | p.432
- HEAD | HEAD | normally a symbolic reference (points to another ref); in rare cases contains a direct SHA-1 (detached HEAD, when checking out a tag, commit or remote branch) | p.432
- remote reference | remote reference | in refs/remotes; stores the last known value of each branch on the server; it is read-only (HEAD never points symbolically to it; commit does not update it) | p.434, p.435
- loose object | loose object | initial format: one file per object, compressed with zlib | p.435, p.436
- packfile / .idx | packfile, index | a binary file that bundles several objects (with deltas); the .idx stores offsets for fast lookup | p.436, p.437
- dangling object | dangling object | object not pointed to by any commit/object (e.g. blobs never committed); does not go into the gc packfile | p.437, p.449
- refspec | refspec | mapping `[+]<src>:<dst>`; src = pattern of refs on the remote side, dst = where they are tracked locally; `+` forces the update even without fast-forward | p.438
- dumb protocol | "dumb" protocol | read-only HTTP transport, with no Git code on the server; a series of GETs; the client assumes the repo layout | p.441
- smart protocol | "smart" protocol | requires a Git process on the other side that computes what the client has/needs and generates a tailor-made packfile; send-pack/receive-pack pairs (upload) and fetch-pack/upload-pack (download) | p.443
- pkt-line | (chunks) | each piece starts with 4 hex characters giving the length (including the 4 bytes); 0000 = end of list | p.443
- auto gc | auto gc | gc triggered automatically when there are too many loose objects or packfiles | p.446
- packed-refs | .git/packed-refs | file to which gc moves the refs (heads/tags) for efficiency; a line with ^ right below a tag indicates the commit the annotated tag points to | p.447
- reflog | reflog | silent record of where HEAD has been at each change; stored in .git/logs/ | p.448, p.449
- SHA-1 | SHA-1 | 40-character hash (checksum of content + header); dir = first 2 chars, file = remaining 38 | p.422

## Commands and options (command | purpose according to the book | page | [DATED]?)
- git hash-object | takes data, (with -w) writes it to the .git/objects database and returns the SHA-1 key; without -w it only computes the key | p.421, p.422
- git hash-object -w --stdin | -w writes the object; --stdin reads content from standard input (otherwise it expects a file name) | p.422
- git hash-object -w <file> | stores the content of a file as a blob | p.422
- git cat-file -p <sha> | finds out the type and displays the content appropriately ("Swiss army knife" for objects) | p.422
- git cat-file -t <sha> | shows the object type (blob, tree, commit, tag) | p.423
- git cat-file -s <sha> | shows the object size | p.436
- git cat-file blob <name> | displays a blob (e.g. the maintainer's public GPG key, tagged as a blob) | p.434
- git cat-file -p master^{tree} | tree pointed to by the latest commit of master; shell problems: Windows CMD requires ^^ ; PowerShell requires single quotes; ZSH requires double quotes | p.423, p.424
- git update-index --add --cacheinfo <mode> <sha> <name> | artificially adds to the index an entry that is in the database and not in the directory; --add because it is not yet in staging; --cacheinfo because the file is in the database | p.424, p.425
- git update-index --add <file> | adds a file from the directory to the index | p.425
- git write-tree | writes the index as a tree object (no -w needed; it creates the tree automatically if it does not exist) | p.425
- git read-tree --prefix=<dir> <tree> | reads an existing tree into the index as a subdirectory (subtree) | p.426
- git commit-tree <tree> [-p <parent>] | creates a commit object from a tree and the direct parents; message read from stdin | p.427
- git log --stat <sha> | shows history starting from a hand-made commit | p.427
- git update-ref <ref> <sha> | safe way to create/update a reference (instead of writing the file by hand); also updates the reflog | p.431, p.432, p.448
- git branch <name> | underneath it runs update-ref with the SHA-1 of the last commit of the current branch | p.432
- git symbolic-ref HEAD [ref] | safely reads/sets HEAD; refuses to point HEAD outside refs/ ("fatal: Refusing to point HEAD outside of refs/") | p.433
- git tag -a <name> <sha> -m <msg> | creates an annotated tag (tag object + ref pointing to it) | p.434
- git update-ref refs/tags/<name> <sha> | is all a lightweight tag is: a ref that never moves | p.433, p.434
- git gc | groups loose objects into a packfile, consolidates packfiles, moves refs to packed-refs, removes old unreachable ones | p.436, p.446, p.447
- git gc --auto | runs the auto gc manually (normally does nothing) | p.446
- git verify-pack -v <file.idx> | lists objects of a pack (SHA, type, size, size in the pack, offset, depth/delta base) | p.437, p.451
- git remote add origin <url> | adds a [remote "origin"] section to .git/config with url and fetch refspec | p.438
- git fetch origin <src>:<dst> | one-off fetch with an explicit refspec (there may be several refspecs) | p.439
- git push origin <src>:<dst> | push with refspec (e.g. master:refs/heads/qa/master) | p.440
- git push origin :topic | deletes the remote branch topic (empty src) | p.440
- git push origin --delete topic | newer syntax (since Git 1.7.0) for deleting a remote ref | p.440, p.441
- update-server-info | generates info/refs and objects/info/packs; must run (e.g. post-receive hook) for dumb HTTP to work | p.441, p.442
- git-receive-pack / git-upload-pack | remote processes invoked via ssh -x git@server "git-receive-pack 'repo.git'" etc. | p.443, p.445
- git reflog | shows where HEAD has been (HEAD@{n}) | p.448
- git log -g | normal log output over the reflog | p.448
- git branch recover-branch <sha> | recovers a lost commit by creating a branch at the found SHA | p.448
- git reset --hard <sha> | in the example, moves master backwards and "loses" the commits on top | p.447
- git branch -D <name> | force-deletes a branch (in the example, to simulate loss) | p.449
- git fsck --full | checks database integrity and lists unpointed objects ("dangling commit/blob/tree") | p.449
- git count-objects -v | shows space usage (count, size, in-pack, packs, size-pack in KB, prune-packable, garbage, size-garbage) | p.450
- git rev-list --objects --all | lists commits and blobs with file paths; use with grep on the SHA to find the file name | p.451
- git log --oneline --branches -- <file> | which commits touched the file | p.451
- git filter-branch --index-filter 'git rm --ignore-unmatch --cached <file>' -- <sha>^.. | rewrites commits removing the file from all trees | p.451 | [DATED] see the dated data section
- git prune --expire now | removes unreachable loose objects for good | p.452
- git --exec-path | shows GIT_EXEC_PATH | p.453
- GIT_TRACE_* | see the variables section | p.455-457

## Step-by-step procedures (numbered; each step with page)

### P1. Create a history "by hand" with plumbing (equivalent to git add + git commit)
1. git init test; check that .git/objects has only info/ and pack/ and no regular file (p.421)
2. `echo 'version 1' > test.txt; git hash-object -w test.txt` -> writes blob (p.422)
3. git update-index --add --cacheinfo 100644 <sha> test.txt -> fills the index (p.424-425)
4. git write-tree -> generates a tree from the index (p.425)
5. Repeat with new files/versions; optionally git read-tree --prefix=bak <tree> to nest a tree as a subdirectory (p.425-426)
6. echo 'First commit' | git commit-tree <tree>; the following ones with -p <previous-commit> (p.427)
7. git update-ref refs/heads/master <last-commit> (or git log <sha> to view) (p.427, p.431)
- The book concludes: this is what git add/git commit do: they store blobs of the changed files, update the index, write trees and commits (p.428).

### P2. How Git writes an object to disk (format) (p.429-431)
1. Build the header: object type + space + content size in bytes + null byte (e.g. "blob 16\0")
2. Concatenate header + content
3. Compute the SHA-1 of that result (matches git hash-object; use echo -n so as not to include a newline)
4. Compress with zlib
5. Write to .git/objects/<first 2 chars>/<remaining 38>
- All objects are stored the same way; the header changes blob to commit or tree. Blob content can be almost anything; commit and tree have a very specific format (p.431).

### P3. Create a branch and a tag manually
1. git update-ref refs/heads/test <sha> -> branch (p.432)
2. git update-ref refs/tags/v1.0 <sha> -> lightweight tag (p.433-434)
3. git tag -a v1.1 <sha> -m 'Test tag' -> annotated tag: creates a tag object, and .git/refs/tags/v1.1 points to the tag object (not to the commit); the object has object/type/tag/tagger/message lines (p.434)

### P4. Custom fetch refspec
1. git remote add origin <url> writes to .git/config: `fetch = +refs/heads/*:refs/remotes/origin/*` (p.438)
2. For a single branch: `fetch = +refs/heads/master:refs/remotes/origin/master` (p.439)
3. Several branches: several fetch lines; or partial glob (since Git 2.6.0) `+refs/heads/qa*:refs/remotes/origin/qa*`; or namespace `+refs/heads/qa/*:refs/remotes/origin/qa/*` (p.439-440)
4. One-off fetch: git fetch origin master:refs/remotes/origin/mymaster (p.439)
- Without the `+`, a branch that is not a fast-forward is rejected: "! [rejected] master -> origin/mymaster (non fast forward)" (p.439)
- origin/master, remotes/origin/master and refs/remotes/origin/master are equivalent (p.439)
- The book warns that you cannot use a refspec to fetch from one repo and push to another (p.440)

### P5. Push refspec
1. git push origin master:refs/heads/qa/master (p.440)
2. To make it the default: in the [remote "origin"] section add `push = refs/heads/master:refs/heads/qa/master` (p.440)
3. Delete remote: git push origin :topic or git push origin --delete topic (p.440-441)

### P6. Recover lost commits (after reset --hard or branch -D)
Typical causes cited: force-deleting a branch with work on it or hard-resetting and abandoning commits (p.447).
1. git reflog (or git log -g for a rich format) -> find the SHA of the lost commit (p.448)
2. git branch recover-branch <sha> -> commits become reachable again (p.448)
3. If it is NOT in the reflog (e.g. .git/logs/ deleted): run git fsck --full, look for "dangling commit <sha>" lines (p.449)
4. Create a branch pointing to that SHA (same technique) (p.449)
- Note from the book: the reflog is updated on every commit/branch switch and also by git update-ref (another reason to prefer it over editing the ref file) (p.448).

### P7. Remove a large file from history (large objects)
1. Context: a clone downloads the entire history; a huge file added once remains reachable forever, even if removed in the next commit (p.449). Common problem when converting from Subversion/Perforce (p.449).
2. git gc and git count-objects -v (size-pack field in KB) to measure (p.450)
3. Find the largest: git verify-pack -v .git/objects/pack/pack-*.idx | sort -k 3 -n | tail -3 (3rd column = size) (p.451)
4. Find the name: git rev-list --objects --all | grep <sha-prefix> (p.451)
5. See the commits that touched it: git log --oneline --branches -- <file> (p.451)
6. Rewrite: git filter-branch --index-filter 'git rm --ignore-unmatch --cached <file>' -- <first-bad-commit>^.. (p.451)
   - --index-filter changes the index instead of files on disk, which is why it is much faster than --tree-filter (it does not check out each revision) (p.451)
   - you need git rm --cached (from the index), not rm on disk; --ignore-unmatch avoids an error if the pattern does not exist in a revision (p.451)
   - limit with <sha>^.. so as not to rewrite from the beginning (slower) (p.452)
7. Clean what still points to the old commits: rm -Rf .git/refs/original (filter-branch backup) and rm -Rf .git/logs/ (reflog) (p.452)
8. git gc to repack (p.452) -> pack size drops (from ~5MB to 8K in the example) (p.452)
9. The large object still exists as a loose object; it will not be transferred in later pushes/clones, which is what matters. To delete it for good: git prune --expire now (p.452)

### P8. Transfer (operational summary)
- Dumb HTTP (clone from http://server/x.git) (p.441-443): GET info/refs -> GET HEAD -> GET objects/xx/yyyy (loose; 404 if it is in a pack) -> GET objects/info/http-alternates -> GET objects/info/packs -> GET .idx -> GET .pack.
- Smart push over SSH: send-pack runs `ssh -x git@server "git-receive-pack 'repo.git'"`; the server lists refs + capabilities; the client sends lines (length, old SHA, new SHA, ref) and then the packfile; the server replies "unpack ok" or failure (p.443-444). An all-zeros SHA as "old" = new ref; zeros as "new" = ref deletion (p.444).
- Smart push over HTTP(S): GET info/refs?service=git-receive-pack, then POST git-receive-pack with send-pack + packfile (p.444).
- Smart fetch: fetch-pack runs git-upload-pack; the server sends refs, HEAD and capabilities (symref=HEAD:...); the client sends "want <sha>", "have <sha>" and "done"; the server sends the packfile (p.445). Over HTTP, GET info/refs?service=git-upload-pack and POST git-upload-pack (p.445-446).
- The dumb protocol cannot write data from the client to the server (p.443).

## Decision rules / heuristics / author recommendations (if X then Y)
- If you need to write/change a ref or HEAD, use git update-ref / git symbolic-ref instead of editing files; they are safer and update-ref feeds the reflog (p.431, p.433, p.448).
- If a ref does not appear in refs/, look in .git/packed-refs: Git reads refs/ first and then packed-refs; when updating a ref it writes a new file in refs/heads and does not edit packed-refs (p.447).
- If you lost a commit: try the reflog first (faster) (p.448); if the reflog does not help, fsck --full (p.449).
- If the server serves a read-only repository over HTTP, dumb is the likely protocol, but the book advises smart (p.441).
- If a fetch refspec may not be a fast-forward, prefix it with + (p.438, p.439).
- To remove a large file use --index-filter instead of --tree-filter for speed (p.451).
- Remove the large object right after the import, before anyone bases work on the commits (p.449).
- Git stores the MOST RECENT version of a file whole and the older ones as deltas, since the most recent is the most likely to be needed (p.438).
- A pack can be repacked at any time; manual or automatic git gc (p.438).
- Auto gc thresholds: ~7,000 loose objects or more than 50 packfiles; adjustable via gc.auto and gc.autopacklimit (p.446).
- gc removes unreachable objects older than "a few months" (text p.446); the gc trace on p.457 shows '--unpack-unreachable=2.weeks.ago' and 'prune --expire 2.weeks.ago' (real values shown in the GIT_TRACE_PERFORMANCE output).

## Risks, warnings and anti-patterns (page)
- Rewriting history with filter-branch is DESTRUCTIVE: it rewrites every commit from the first tree it modifies; it is only painless right after an import and before anyone bases work on it; otherwise, all collaborators must rebase onto the new commits (p.449).
- Merely removing the file in a later commit does NOT take the file out of history: clones keep downloading everything (p.449, p.450).
- After filter-branch, the reflog and .git/refs/original still reference old commits; they must be removed before gc (p.452).
- rm -Rf .git/logs/ deletes the reflog (used as part of the cleanup, and in the example to simulate loss) (p.449, p.452) - it removes the recovery safety net.
- git reset --hard can abandon commits (p.447); git branch -D likewise (p.447, p.449).
- git prune --expire now permanently deletes the objects (p.452).
- The dumb protocol is hard to secure/make private; most hosts refuse it (p.441).
- GIT_SSL_NO_VERIFY turns off SSL certificate verification; the book cites its use with a self-signed certificate or a server that does not yet have a certificate (p.454-455).
- Tags and commits printed in the book have hashes that may not match yours (p.427).
- Valid file modes are only 100644, 100755 and 120000 (p.425).
- HEAD cannot be pointed outside refs/ via symbolic-ref (p.433).
- Dangling objects are not packed by gc (p.437) - and may be removed later by prune.

## Illustrative examples/cases (what they illustrate)
- Three commits created with commit-tree + log --stat: real history without using porcelain (p.426-428).
- "what is up, doc?" object in Ruby: reproduces hash-object (SHA bd9dbf5...) showing header+zlib (p.429-431).
- repo.rb of 22K + 1 line: two blobs of ~22K (each ~7K compressed); gc turns them into one whole plus one delta (9 bytes vs 22054) (p.435-438).
- Pack of 18 objects: disk size is halved (15K to 7K) (p.437).
- git.tgz tarball of ~5MB added and removed: size-pack ~4868 KB -> 8 KB after filter-branch + gc (p.450-452).
- Tag that does not point to a commit: GPG key as a blob (junio-gpg-pub) and the first kernel tag points to a tree (p.434).
- qa/ namespace with fetch and push refspec (p.439-440).
- post-receive hook + update-server-info to enable dumb HTTP (p.441).
- GIT_REFLOG_ACTION="my action" changes the text in the reflog (p.458).

## Environment variables (p.453-458) - summary
- Global: GIT_EXEC_PATH (where subprograms live; git --exec-path), HOME (global config), PREFIX (system config in $PREFIX/etc/gitconfig), GIT_CONFIG_NOSYSTEM (turns off system config), GIT_PAGER (fallback PAGER), GIT_EDITOR (fallback EDITOR) (p.453)
- Repo location: GIT_DIR (otherwise walks up the tree to ~ or /), GIT_CEILING_DIRECTORIES (limits the search; useful on slow directories/prompt), GIT_WORK_TREE (if only --git-dir/GIT_DIR is given without a work-tree, the cwd is the root), GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY (p.453-454), GIT_ALTERNATE_OBJECT_DIRECTORIES (colon-separated list; avoids copies of identical large files) (p.454)
- Pathspecs: GIT_GLOB_PATHSPECS (default), GIT_NOGLOB_PATHSPECS, GIT_LITERAL_PATHSPECS, GIT_ICASE_PATHSPECS; prefixes :(glob) and :(literal) (p.454)
- Commit: GIT_AUTHOR_NAME/EMAIL/DATE, GIT_COMMITTER_NAME/EMAIL/DATE (primary source for commit-tree; config only as a fallback); EMAIL as a fallback for user.email (p.454)
- Network: GIT_CURL_VERBOSE, GIT_SSL_NO_VERIFY (p.454-455), GIT_HTTP_LOW_SPEED_LIMIT / GIT_HTTP_LOW_SPEED_TIME (abort a slow HTTP operation; override http.lowSpeedLimit/lowSpeedTime), GIT_HTTP_USER_AGENT (p.455)
- Diff/merge: GIT_DIFF_OPTS (only -u<n> or --unified=<n>), GIT_EXTERNAL_DIFF (overrides diff.external), GIT_DIFF_PATH_COUNTER/TOTAL, GIT_MERGE_VERBOSITY (0 to 5; default 2) (p.455)
- Debug (values true/1/2 -> stderr; absolute path -> file): GIT_TRACE (alias, subprograms), GIT_TRACE_PACK_ACCESS, GIT_TRACE_PACKET, GIT_TRACE_PERFORMANCE, GIT_TRACE_SETUP (p.455-457)
- Misc: GIT_SSH (program in place of ssh; no extra args), GIT_SSH_COMMAND (interpreted by the shell, accepts args: ssh -i ~/.ssh/my_key) (p.457); GIT_ASKPASS (overrides core.askpass), GIT_NAMESPACE (namespaced refs; useful on the server for several forks), GIT_FLUSH, GIT_REFLOG_ACTION (p.458)
- Claim by the book (p.453): Git always runs inside a bash shell (recorded as stated, not validated).

## Dated data / divergences from current practice
- SHA-1 throughout the chapter: the book describes 40-hex objects (SHA-1) and does not mention SHA-256 on any page of the range (p.420-458). [DATED] with respect to the SHA-256 repository support existing in modern Git (general knowledge, not in the book).
- Branch name "master" in all examples (p.423, p.431 etc.) [DATED]: the current default of many hosts/versions is main.
- git filter-branch (p.451) [DATED]: Git's own documentation today discourages filter-branch and recommends git filter-repo (general knowledge, not in the book); the book presents filter-branch as the tool.
- .git/refs/original and rm -Rf .git/logs/ (p.452) [DATED/risky]: manual cleanup recipe; today git reflog expire --expire=now --all and git gc --prune=now are commonly used (extrapolation; the book uses rm and prune --expire now).
- Dumb protocol (p.441): the book already says it is rarely used today.
- GIT_TRACE outputs show sha1_file.c and version git/2.0.x (p.455-456): old examples; displays have changed.
- "Git 1.7.0" for --delete (p.441) and "Git 2.6.0" for partial globs (p.439) are version information given by the book.
- Example with git@github.com URL and curl on raw.githubusercontent.com (p.434-435): illustrative only.
- gc: the book says "a few months" (p.446); the trace itself shows 2.weeks.ago (p.457).
- Ruby/irb used in the storage demo (p.429): illustration only, not a requirement.

## What the book does NOT say here (gaps)
- It does not mention SHA-256, nor hash migration, nor objectformat, nor SHA-1 collision / SHAttered (p.420-458).
- It does not use git filter-repo, BFG, git switch/restore, git reflog expire, nor git gc --prune=<date> explicitly; it uses git prune --expire now (p.452) and git gc without arguments (p.436, p.452). (git gc --prune does not appear in the text.)
- It does not explain the internal pack format (OFS/REF deltas, header) beyond verify-pack; it only describes the concept (p.437-438).
- It does not explain "git gc --aggressive", manual "git repack", "git maintenance" or commit-graph.
- It says nothing about reflog expiry (gc.reflogExpire) or the default reflog lifetime.
- It does not describe protocol v2 (only the old format with capabilities on the first line) nor git:// (daemon) in detail; only SSH and HTTP(S) and dumb HTTP.
- It does not cover git fsck --lost-found, dangling stash commits, or git notes here.
- It does not cover refs/notes, refs/stash or refs/replace.
- It does not cover "git push --force" here; only the + of the fetch refspec (p.438-439).
- It does not say how to recover from a corrupted object (only integrity via fsck, p.449).
- There is no instruction on how to force push after filter-branch (it only warns collaborators to rebase, p.449).


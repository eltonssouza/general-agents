# -*- coding: utf-8 -*-
"""
git_advisor.py - deterministic "advisor": given an INTENT in natural language (English or Portuguese), points to the
procedure Pro Git describes (with PGEN pages), the risks the book cites, what is [DATED],
what the book does NOT cover and, separately, a marked [extrapolation]. No network, does not run git.

Usage:
  python -I git_advisor.py "undo the last commit"
  python -I git_advisor.py "merge branches" --published        # the commit/history was already pushed to the remote
  python -I git_advisor.py --list
  python -I git_advisor.py "remove password from history" --json

Portuguese intents also work (e.g. "desfazer o ultimo commit"); --publicado is accepted as an alias of --published.

Convention: page = PDF page; PGEN = Pro Git EN (ed. 2.1.450). If no intent matches, it prints
"NOT COVERED" and does not invent a procedure.
"""
import argparse
import json
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# Each intent: id, title, kw (trigger words/phrases, Portuguese and English), steps [(text, page)], risks,
# published (extra warning), dated, not_covered, extrapolation.
INTENTS = [
    {
        "id": "desfazer-ultimo-commit-local",
        "title": "Fix or undo the last commit (not yet pushed)",
        "kw": ["desfazer ultimo commit", "corrigir ultimo commit", "esqueci arquivo no commit", "mensagem do commit errada", "amend", "undo last commit", "fix last commit", "refazer commit", "alterar mensagem do ultimo commit",
               "undo the last commit", "undo my last commit", "forgot a file in the commit", "wrong commit message", "change last commit message", "redo commit"],
        "steps": [
            ("If you forgot a file: git add <file> (or make the change and git add).", "PGEN p.52-53, 250"),
            ("git commit --amend: the editor opens with the previous message; the result is ONE commit that replaces the old one.", "PGEN p.52-53"),
            ("For a trivial change without touching the message: git commit --amend --no-edit.", "PGEN p.250"),
            ("To undo the commit keeping the changes in the working dir: git reset HEAD^ (mixed: the commit disappears, files stay unstaged); --soft keeps them staged too.", "PGEN p.254, 267"),
        ],
        "risks": [
            "amend changes the SHA-1: it is a 'mini rebase'; do not use it on a commit that was already pushed (PGEN p.53, 250).",
            "reset --hard destroys uncommitted changes and is the only destructive form of reset (PGEN p.269).",
        ],
        "published": "Commit already pushed: the book says to treat pushed history as final (PGEN p.249) and warns that amend + force push harms collaborators (p.53). To reverse the effect of a published commit the book only describes git revert as a 'reverse cherry-pick' (Appendix C, PGEN p.495) and uses it to undo a merge (p.289); the detailed procedure for an ordinary commit is [extrapolation].",
        "dated": ["Examples use checkout/reset; current practice also uses restore/switch (the book mentions restore only in PGEN p.55-56) [DATED]."],
        "not_covered": ["step-by-step revert of an ordinary commit", "force-with-lease"],
        "extrapolation": ["git revert <sha> creates a new commit that undoes the earlier one and is safe on published history [extrapolation, consistent with PGEN p.495]."],
    },
    {
        "id": "tirar-do-stage",
        "title": "Remove a file from the stage (unstage)",
        "kw": ["tirar do stage", "unstage", "desfazer git add", "remover do stage", "retirar da area de stage", "git add por engano", "add *",
               "remove from stage", "undo git add", "unstage a file", "added by mistake"],
        "steps": [
            ("Modern form (Git >= 2.23): git restore --staged <file>.", "PGEN p.55"),
            ("Old form shown first by the book: git reset HEAD <file>. The file in the working dir is not touched.", "PGEN p.53-54"),
            ("Confirm with git status: the file goes back to 'Changes not staged for commit'.", "PGEN p.54-56"),
        ],
        "risks": ["reset without --hard does not touch the working dir and is relatively safe (PGEN p.54)."],
        "published": None,
        "dated": ["reset HEAD <file> is the old form; the book itself shows restore --staged (PGEN p.55) [DATED]."],
        "not_covered": ["restore -p / add -p for partial unstaging"],
        "extrapolation": [],
    },
    {
        "id": "descartar-mudancas-locais",
        "title": "Discard local changes to a file",
        "kw": ["descartar alteracoes", "descartar mudancas", "discard changes", "voltar arquivo", "restaurar arquivo", "checkout --", "git restore", "desfazer modificacoes de um arquivo", "unmodify",
               "discard local changes", "revert a file", "restore a file", "undo changes to a file", "throw away changes"],
        "steps": [
            ("BEFORE: if you want to keep the work, prefer stash or a branch (the book says they are usually better).", "PGEN p.55"),
            ("Modern: git restore <file>.", "PGEN p.56"),
            ("Old: git checkout -- <file>.", "PGEN p.54"),
        ],
        "risks": ["Discards with no way back: the local copy is overwritten by the staged/committed version; work that was never committed is probably lost (PGEN p.54-56)."],
        "published": None,
        "dated": ["checkout -- is the old form [DATED]."],
        "not_covered": ["restore --source"],
        "extrapolation": [],
    },
    {
        "id": "juntar-branches",
        "title": "Join (integrate) branches: merge x rebase",
        "kw": ["juntar branches", "mesclar branches", "merge", "integrar branch", "unir branches", "merge branches", "rebase ou merge", "merge vs rebase", "fast-forward", "trazer correcao de master",
               "join branches", "combine branches", "integrate branch", "rebase or merge", "bring a fix from master"],
        "steps": [
            ("Leave the working dir and stage clean (commit, stash or amend) before switching/merging.", "PGEN p.78, 278"),
            ("Go to the branch that RECEIVES: git checkout master; then git merge <topic>.", "PGEN p.79-81"),
            ("If the commit is directly ahead: Fast-forward (just moves the pointer). Otherwise: three-way merge with a two-parent merge commit.", "PGEN p.79, 81"),
            ("Conflict: Git pauses; edit the markers, git add, git commit (see intent 'resolve conflict').", "PGEN p.82-85"),
            ("Delete the already merged branch: git branch -d <topic>.", "PGEN p.80, 82"),
            ("Alternative: git rebase master on the topic and then a fast-forward merge into master (linear history, same final snapshot).", "PGEN p.102-103"),
        ],
        "risks": [
            "Rebase rule: do not rebase commits that exist outside your repository and on which others may have based work (PGEN p.106).",
            "The author's gradation: local = ok; pushed but unused by others = ok; public and in use = problem (PGEN p.109).",
        ],
        "published": "History already published: prefer MERGE over rebase (PGEN p.106-110); on GitHub the book also prefers merging upstream over rebasing in an open PR (p.187).",
        "dated": ["The 'recursive strategy' message is of its time; today the default is another strategy [DATED, extrapolation]."],
        "not_covered": ["merge --no-ff", "merge --ff-only", "git merge --squash outside the PR context (appears in PGEN p.152-153)"],
        "extrapolation": [],
    },
    {
        "id": "resolver-conflito",
        "title": "Resolve a merge conflict",
        "kw": ["resolver conflito", "conflito de merge", "merge conflict", "conflict", "automatic merge failed", "mergetool", "marcadores de conflito", "unmerged paths",
               "resolve conflict", "resolve a conflict", "conflict markers", "fix merge conflict"],
        "steps": [
            ("git status shows 'Unmerged paths / both modified'.", "PGEN p.83"),
            ("Edit the file: the block between <<<<<<<, ======= and >>>>>>>; choose one side or combine and REMOVE the markers.", "PGEN p.83"),
            ("git add on each resolved file (marks it as resolved); graphical alternative: git mergetool.", "PGEN p.83-84"),
            ("git status should say all conflicts are fixed; then git commit (you may explain the resolution in the message).", "PGEN p.84-85"),
            ("Extra context: git checkout --conflict=diff3 <file>; git log --oneline --left-right --merge; git diff.", "PGEN p.284-287"),
            ("If you change your mind/did not expect a conflict: git merge --abort.", "PGEN p.279-280"),
        ],
        "risks": [
            "merge --abort may not revert everything if there were uncommitted changes before the merge (PGEN p.280).",
            "checkout --ours/--theirs overwrite files; -Xours/-Xtheirs pick a whole side (PGEN p.285, 291).",
        ],
        "published": None,
        "dated": [],
        "not_covered": ["rebase --continue/--skip on a rebase conflict (only rebase --abort in PGEN p.255 and rerere p.301)"],
        "extrapolation": [],
    },
    {
        "id": "abortar-ou-desfazer-merge",
        "title": "Abort or undo a merge",
        "kw": ["abortar merge", "merge --abort", "desfazer merge", "desfazer merge publicado", "undo merge", "merge errado", "merge por engano", "reverter merge", "revert -m",
               "abort merge", "undo a merge", "undo published merge", "wrong merge", "merge by mistake", "revert a merge"],
        "steps": [
            ("Merge in progress (conflict) and you want to give up: git merge --abort.", "PGEN p.279-280"),
            ("Merge already completed, local only, no new commits afterwards: git reset --hard HEAD~ (moves the pointer).", "PGEN p.288-289"),
            ("Merge already published (or refs cannot be moved): git revert -m 1 HEAD (-m 1 = the 'mainline' parent to keep).", "PGEN p.289"),
            ("To merge the same topic later: REVERT the revert first, otherwise the merge says 'Already up-to-date' and only brings new work.", "PGEN p.290-291"),
        ],
        "risks": [
            "reset --hard HEAD~ rewrites history and loses later commits (PGEN p.289).",
            "merge --abort may not restore everything with uncommitted changes (PGEN p.280).",
        ],
        "published": "Use revert -m 1; do not move published refs (PGEN p.289).",
        "dated": [],
        "not_covered": ["ORIG_HEAD", "reset --merge/--keep"],
        "extrapolation": [],
    },
    {
        "id": "squash-ou-editar-varios-commits",
        "title": "Squash, reorder, delete or rewrite messages of several local commits",
        "kw": ["squash", "juntar commits", "combinar commits", "rebase -i", "rebase interativo", "interactive rebase", "reordenar commits", "apagar commit", "drop commit", "editar mensagens de varios commits", "reword", "limpar historico antes do push",
               "combine commits", "squash commits", "reorder commits", "delete a commit", "edit commit messages", "clean up history before push"],
        "steps": [
            ("git rebase -i HEAD~N (N = commits to review; the target is the PARENT of the oldest one to edit).", "PGEN p.250"),
            ("The list goes from oldest to newest and runs top to bottom; change pick to edit/squash/drop or reorder the lines.", "PGEN p.251-253"),
            ("Squash: keep pick on the first and change the others to squash; the editor reopens to combine the messages.", "PGEN p.253-254"),
            ("Shortcut for a simple squash: git reset --soft HEAD~N followed by git commit.", "PGEN p.272-275"),
            ("On 'edit': git commit --amend and git rebase --continue.", "PGEN p.252"),
            ("Way out: git rebase --abort during; git reflog after it finishes.", "PGEN p.255"),
        ],
        "risks": [
            "Deleting a line of the script LOSES the commit; emptying the script aborts (PGEN p.251).",
            "Rewrites all commits in the range and descendants (new SHA-1s): do not include commits that were already pushed (PGEN p.250, 255).",
        ],
        "published": "Do not rewrite: the book says to treat pushed history as final (PGEN p.249).",
        "dated": [],
        "not_covered": ["rebase --autosquash", "commit --fixup", "force-with-lease"],
        "extrapolation": [],
    },
    {
        "id": "dividir-commit",
        "title": "Split a commit",
        "kw": ["dividir commit", "split commit", "separar commit", "quebrar commit em dois",
               "split a commit", "break a commit in two", "separate a commit"],
        "steps": [
            ("git rebase -i and mark the commit with edit.", "PGEN p.254"),
            ("When it stops: git reset HEAD^ (mixed) undoes the commit leaving the files unstaged.", "PGEN p.254"),
            ("git add + git commit as many times as you want; then git rebase --continue.", "PGEN p.254"),
        ],
        "risks": ["The SHA-1s change; make sure no already shared commit is in the list (PGEN p.255)."],
        "published": "Do not do this on published commits (PGEN p.249-250, 255).",
        "dated": [],
        "not_covered": [],
        "extrapolation": [],
    },
    {
        "id": "remover-arquivo-ou-segredo-do-historico",
        "title": "Remove a file (password, huge binary) from ALL of the history",
        "kw": ["remover senha do historico", "remover arquivo do historico", "arquivo grande", "segredo commitado", "senha commitada", "filter-branch", "filter-repo", "limpar historico", "remove password from history", "large file", "reduzir tamanho do repositorio",
               "remove file from history", "remove a secret from history", "committed a password", "committed a secret", "clean history", "shrink repository", "big file in history"],
        "steps": [
            ("Know that deleting the file in a later commit does NOT take it out of the history: clones keep downloading everything.", "PGEN p.449-450"),
            ("The book warns that filter-branch has many pitfalls and recommends git-filter-repo (Python script).", "PGEN p.255"),
            ("If you use filter-branch: do it on a test branch and only then hard-reset master; --all for all branches.", "PGEN p.256"),
            ("To remove a file: git filter-branch --tree-filter 'rm -f <file>' HEAD (slow) or --index-filter 'git rm --ignore-unmatch --cached <file>' -- <sha>^.. (fast).", "PGEN p.256, 451"),
            ("To reclaim the space: rm -Rf .git/refs/original, rm -Rf .git/logs/, git gc and, to delete for good, git prune --expire now.", "PGEN p.452"),
            ("Measure: git count-objects -v; find the biggest with git verify-pack -v and git rev-list --objects --all.", "PGEN p.450-451"),
        ],
        "risks": [
            "filter-branch is the 'nuclear option': it rewrites all commits since the first affected one; it is only painless right after an import, before anyone bases work on it (PGEN p.255, 449).",
            "Changing the email with --commit-filter changes the SHA-1 of ALL commits (PGEN p.256-257).",
            "rm -Rf .git/logs/ deletes the reflog (the safety net) and prune --expire now deletes permanently (PGEN p.449, 452).",
        ],
        "published": "All collaborators will need to rebase onto the new commits (PGEN p.449). The book does NOT talk about force-push or about rotating leaked secrets (noted as a gap).",
        "dated": ["filter-branch is discouraged even by the book (PGEN p.255) [DATED]; the manual cleanup with rm -Rf and gc is the book's [DATED]."],
        "not_covered": ["how to use git-filter-repo (it is only cited)", "rotating leaked credentials", "force-push after the rewrite"],
        "extrapolation": ["A secret that was already published must be considered compromised and rotated [extrapolation]."],
    },
    {
        "id": "recuperar-commit-perdido",
        "title": "Recover lost commits or branches (reset --hard, branch -D, rebase)",
        "kw": ["recuperar commit", "commit perdido", "perdi commit", "recover lost commit", "reflog", "recuperar branch apagado", "desfazer reset --hard", "dangling", "fsck", "desfazer rebase",
               "recover commit", "lost commit", "i lost a commit", "recover deleted branch", "undo reset --hard", "undo rebase", "undo a rebase"],
        "steps": [
            ("git reflog (or git log -g) and find the SHA of the desired state (HEAD@{n}).", "PGEN p.226-227, 448"),
            ("git branch recover-branch <sha>: the commits become reachable again.", "PGEN p.448"),
            ("If the reflog does not help: git fsck --full and look for 'dangling commit <sha>'; create a branch on it.", "PGEN p.449"),
            ("After a finished rebase: git reflog to recover the branch's previous version.", "PGEN p.255"),
        ],
        "risks": [
            "The reflog is local and covers a few months; a recent clone has an empty reflog (PGEN p.227).",
            "Work that was never committed is not recoverable by Git (PGEN p.55, 269).",
            "gc/prune remove unreachable objects (PGEN p.446, 452).",
        ],
        "published": None,
        "dated": [],
        "not_covered": ["reflog expire", "ORIG_HEAD"],
        "extrapolation": [],
    },
    {
        "id": "achar-commit-que-quebrou",
        "title": "Find the commit that introduced a defect / who changed a line",
        "kw": ["achar commit que quebrou", "bisect", "regressao", "bug introduzido", "quem mudou", "blame", "git blame", "encontrar bug", "find bug commit", "pickaxe", "historia de uma funcao",
               "find the commit that broke", "which commit broke", "who changed this line", "find the bug", "regression", "history of a function"],
        "steps": [
            ("Know where the defect is? git blame -L <start>,<end> <file> (and -C for moved code) shows the commit of each line.", "PGEN p.301"),
            ("Do not know where? git bisect start; git bisect bad; git bisect good <good-tag-or-sha>; test and mark good/bad until 'first bad commit'.", "PGEN p.302-303"),
            ("Automate: git bisect run <script> (exit 0 = good, non-zero = bad).", "PGEN p.303-304"),
            ("Always finish with git bisect reset.", "PGEN p.303"),
            ("When a string entered/changed: git log -S <string> (or -G regex); history of a function: git log -L :function:file.", "PGEN p.247-248"),
        ],
        "risks": ["Forgetting bisect reset leaves the repository in the bisect state (PGEN p.304)."],
        "published": None,
        "dated": [],
        "not_covered": ["bisect skip", "bisect log/replay"],
        "extrapolation": [],
    },
    {
        "id": "guardar-trabalho-stash",
        "title": "Save work in progress to switch branches (stash)",
        "kw": ["stash", "guardar trabalho", "trocar de branch sem commitar", "esconder mudancas", "save work in progress", "git stash",
               "switch branch without committing", "save my work", "stash my changes", "hide changes", "shelve changes"],
        "steps": [
            ("git stash (or git stash push); switch branches and work.", "PGEN p.236-237"),
            ("Come back and apply: git stash apply --index if you want to preserve what was staged; or git stash pop.", "PGEN p.238"),
            ("Remove the applied stash: git stash drop stash@{n} (apply does not remove it).", "PGEN p.238"),
            ("To include new files: git stash -u; to include ignored ones: --all.", "PGEN p.239"),
            ("Old stash that conflicts: git stash branch <name>.", "PGEN p.239-240"),
        ],
        "risks": ["By default the stash does NOT save untracked or ignored files (PGEN p.239).", "git stash save is being deprecated: use push (PGEN p.236)."],
        "published": None,
        "dated": ["stash save [DATED]"],
        "not_covered": [],
        "extrapolation": [],
    },
    {
        "id": "limpar-untracked",
        "title": "Clean untracked files (git clean)",
        "kw": ["git clean", "limpar working directory", "apagar untracked", "remover arquivos nao rastreados", "clean untracked",
               "clean working directory", "delete untracked files", "remove untracked files"],
        "steps": [
            ("Simulate: git clean -d -n (dry run) to see what would go.", "PGEN p.240-241"),
            ("Reversible alternative: git stash --all.", "PGEN p.240"),
            ("Run it: git clean -f -d (or -i to choose).", "PGEN p.240-241"),
            ("Ignored files too: add -x.", "PGEN p.241"),
        ],
        "risks": ["git clean removes files that often cannot come back (PGEN p.240).", "-x deletes ignored files (builds) (PGEN p.241); nested repositories require a double -f (p.241)."],
        "published": None,
        "dated": [],
        "not_covered": [],
        "extrapolation": [],
    },
    {
        "id": "renomear-branch",
        "title": "Rename a branch (including master to main)",
        "kw": ["renomear branch", "rename branch", "master para main", "master main", "mudar nome do branch", "branch --move",
               "rename a branch", "rename master to main", "change branch name", "master to main"],
        "steps": [
            ("Do not rename a branch in use by collaborators; consult them and look for references to the old name in code and scripts.", "PGEN p.86-87"),
            ("git branch --move old new (local only).", "PGEN p.87"),
            ("git push --set-upstream origin new.", "PGEN p.87-88"),
            ("Adjust dependents: test runner, build/release scripts, host config (default branch, rules), documentation, PRs that point to the old one.", "PGEN p.88"),
            ("Only after confirming: git push origin --delete old.", "PGEN p.88"),
        ],
        "risks": ["Renaming master breaks integrations and scripts; the old master stays on the remote and collaborators keep using it (PGEN p.87-88)."],
        "published": None,
        "dated": ["The book treats main as a hosting novelty (PGEN p.29, 35, 87) [DATED in practice]."],
        "not_covered": [],
        "extrapolation": [],
    },
    {
        "id": "apagar-branch",
        "title": "Delete a local or remote branch",
        "kw": ["apagar branch", "deletar branch", "delete branch", "branch -d", "branch -D", "push origin --delete", "remover branch remoto",
               "delete a branch", "remove branch", "delete remote branch", "remove remote branch"],
        "steps": [
            ("Local, merged: git branch -d <b> (refuses if not fully merged). git branch --merged lists the safe ones.", "PGEN p.86"),
            ("Remote: git push origin --delete <b> (make sure it was merged into the stable branch).", "PGEN p.100-101"),
        ],
        "risks": ["-D forces and loses unmerged commits (PGEN p.86).", "Deleting the remote only removes the pointer; the data stays until GC (recoverable) (PGEN p.101)."],
        "published": None,
        "dated": [],
        "not_covered": ["git fetch --prune / remote prune in detail (prune only cited in PGEN p.60)"],
        "extrapolation": [],
    },
    {
        "id": "sincronizar-apos-force-push-alheio",
        "title": "Someone rewrote history and force-pushed; how do I sync",
        "kw": ["force push alheio", "alguem deu force push", "historico reescrito remoto", "pull apos rebase de colega", "pull --rebase", "commits duplicados apos pull", "rebase when you rebase",
               "colleague force pushed", "someone force pushed", "remote history rewritten", "duplicate commits after pull", "teammate force push"],
        "steps": [
            ("Avoid a plain git pull: it creates a merge commit reintroducing abandoned commits.", "PGEN p.107-108"),
            ("Use git fetch + git rebase <remote>/<branch>, or git pull --rebase.", "PGEN p.108-109"),
            ("Git uses patch-id to drop your already rewritten commits on the target and reapply the rest.", "PGEN p.108-109"),
            ("Permanent configuration: pull.rebase true.", "PGEN p.109"),
        ],
        "risks": ["It only detects duplicates if the rewritten patch is nearly identical to the original (PGEN p.109)."],
        "published": None,
        "dated": [],
        "not_covered": ["force-with-lease"],
        "extrapolation": [],
    },
    {
        "id": "publicar-e-colaborar-em-branch",
        "title": "Publish a branch, create tracking and collaborate",
        "kw": ["publicar branch", "push branch", "tracking branch", "branch de rastreamento", "set-upstream", "colaborar em branch remoto", "origin/serverfix",
               "publish branch", "publish a branch", "push a branch", "collaborate on a remote branch", "set upstream"],
        "steps": [
            ("git push origin <branch> (local branches do not sync on their own).", "PGEN p.97"),
            ("Teammate: git fetch origin brings only origin/<branch> (immovable).", "PGEN p.98"),
            ("git merge origin/<branch> OR git checkout -b <branch> origin/<branch> (creates tracking); also --track and git branch -u.", "PGEN p.98-99"),
            ("git branch -vv shows ahead/behind based on the last fetch (it does not query the server).", "PGEN p.100"),
        ],
        "risks": ["fetch never creates an editable local branch (PGEN p.98).", "A push is rejected if someone pushed first: integrate first (PGEN p.59)."],
        "published": None,
        "dated": [],
        "not_covered": [],
        "extrapolation": [],
    },
    {
        "id": "contribuir-github-pr",
        "title": "Contribute to a project via fork and pull request (GitHub Flow)",
        "kw": ["pull request", "fork", "contribuir projeto", "github flow", "abrir pr", "contribute github", "pr desatualizado", "atualizar fork", "sync fork", "manter fork atualizado",
               "contribute to a project", "open a pr", "outdated pr", "pr is out of date", "update my fork", "keep fork updated"],
        "steps": [
            ("Fork; clone YOUR fork; descriptive topic branch; commits; push the branch to the fork (origin).", "PGEN p.178-180"),
            ("Open the PR with a useful title and description; change requests: new commits on the SAME branch (no notification: leave a comment).", "PGEN p.181-184"),
            ("PR does not merge cleanly: prefer MERGING upstream into your branch (git remote add upstream; fetch upstream; merge upstream/master; push the same branch).", "PGEN p.186-188"),
            ("If rebasing is unavoidable: do NOT force-push to the open PR's branch; push to a NEW branch, a new PR referencing the old one, and close the original.", "PGEN p.188"),
            ("Keep the fork up to date: GitHub never updates it on its own; pull from upstream and push to origin; never commit directly to master.", "PGEN p.195-196"),
        ],
        "risks": ["Force push on an open PR branch brings back the problems of 'The Perils of Rebasing' (PGEN p.188).", "Git does not warn you if you committed to master before pulling from upstream (PGEN p.196)."],
        "published": None,
        "dated": ["GitHub interfaces, the 'Sync fork' button and authentication rules have changed [DATED]."],
        "not_covered": ["GitHub Actions/CI", "CODEOWNERS", "branch protection", "squash and merge via the UI"],
        "extrapolation": [],
    },
    {
        "id": "enviar-patch-por-email",
        "title": "Send or apply patches by email",
        "kw": ["patch por email", "format-patch", "send-email", "git am", "git apply", "enviar patch", "aplicar patch", "request-pull", "mailing list",
               "patch by email", "send a patch", "apply a patch", "email patch"],
        "steps": [
            ("Contributor: topic branch; git format-patch -M origin/master; send with git send-email or git imap-send (or paste, with formatting risk).", "PGEN p.153-155"),
            ("Maintainer: test branch; for format-patch use git am <file>; for a plain diff git apply --check and then git apply (and commit manually).", "PGEN p.157-158"),
            ("am failure: resolve, git add and git am --resolved; or --skip/--abort; or git am -3.", "PGEN p.159-160"),
            ("Review before integrating: git log contrib --not master; git diff master...contrib.", "PGEN p.161-162"),
        ],
        "risks": ["git apply is all or nothing and does not create a commit (PGEN p.157).", "git diff master (without ...) misleads with diverged branches (PGEN p.162)."],
        "published": None,
        "dated": ["am --resolved: today --continue is used [DATED, extrapolation]"],
        "not_covered": ["format-patch --signoff and other options beyond -M"],
        "extrapolation": [],
    },
    {
        "id": "criar-release-tag",
        "title": "Create and publish a release (tag, describe, archive, shortlog)",
        "kw": ["criar tag", "release", "tag anotada", "tag leve", "publicar tag", "apagar tag", "git describe", "git archive", "shortlog", "changelog", "versionar release", "numero de build",
               "create a tag", "create tag", "annotated tag", "lightweight tag", "publish tag", "delete tag", "build number", "make a release"],
        "steps": [
            ("Prefer an annotated tag: git tag -a vX -m '...'; (signed: git tag -s).", "PGEN p.62, 168"),
            ("Tag on an old commit: git tag -a vX <hash>.", "PGEN p.64"),
            ("Publish: git push origin <tag> or --tags (lightweight and annotated) or --follow-tags (annotated only); a normal push does not send tags.", "PGEN p.64-65"),
            ("Delete: git tag -d (local) and git push origin --delete <tag> (remote).", "PGEN p.65-66"),
            ("Release: git describe master (build number; requires an annotated tag), git archive master --prefix='project/' and git shortlog --no-merges master --not v1.0.1.", "PGEN p.169-170"),
        ],
        "risks": ["tag -d does not delete on the remote (PGEN p.65).", "The abbreviated SHA from describe may stop being valid (PGEN p.169)."],
        "published": None,
        "dated": [],
        "not_covered": ["SemVer/version naming convention"],
        "extrapolation": [],
    },
    {
        "id": "assinar-commits-tags",
        "title": "Sign and verify commits and tags (GPG)",
        "kw": ["assinar commit", "assinar tag", "gpg", "sign commits", "verificar assinatura", "verify signatures", "commit.gpgsign", "signingkey",
               "sign a commit", "sign a tag", "verify signature", "sign tags"],
        "steps": [
            ("Have a GPG key and set user.signingkey.", "PGEN p.242"),
            ("Tag: git tag -s; verify: git tag -v (requires the signer's public key).", "PGEN p.242-243"),
            ("Commit: git commit -S; verify: git log --show-signature.", "PGEN p.244"),
            ("Merging third-party work: git merge --verify-signatures [-S].", "PGEN p.244-245"),
            ("On a team: everyone with commit.gpgsign true.", "PGEN p.245"),
        ],
        "risks": ["Without standardizing commit.gpgsign it is hard to keep the team signing (PGEN p.245)."],
        "published": None,
        "dated": ["The book only covers GPG; SSH/S-MIME signing is [extrapolation] [DATED]."],
        "not_covered": ["SSH signing", "S/MIME"],
        "extrapolation": [],
    },
    {
        "id": "submodulos",
        "title": "Use submodules safely",
        "kw": ["submodulo", "submodule", "submodules", "clonar com submodulos", "atualizar submodulo", "recurse-submodules", "gitmodules",
               "clone with submodules", "update submodule", "update submodules"],
        "steps": [
            ("Add: git submodule add <url>; commit (.gitmodules + the directory entry) and push.", "PGEN p.304-306"),
            ("Clone: git clone --recurse-submodules (or clone + git submodule init/update; or update --init --recursive).", "PGEN p.306-308"),
            ("After git pull: git submodule update --init --recursive (pull fetches, but does NOT update submodules).", "PGEN p.311-313"),
            ("Work in the submodule: enter it, git checkout <branch>; update --remote --merge/--rebase; local commits.", "PGEN p.313-315"),
            ("Before publishing the superproject: git push --recurse-submodules=check|on-demand (or push the submodule manually).", "PGEN p.315-316"),
            ("Switching branches: git checkout --recurse-submodules.", "PGEN p.322-323"),
        ],
        "risks": ["Submodule in detached HEAD: commits can be lost on the next update (PGEN p.313).", "A forgotten submodule push leaves the superproject pointing to a commit nobody can download (PGEN p.315).", "Diverged submodule conflict: Git does not even do a trivial merge; do not blindly accept the suggested update-index --cacheinfo (PGEN p.317-319)."],
        "published": None,
        "dated": ["Git < 2.13 behaviors described in PGEN p.322-323 [DATED]."],
        "not_covered": ["submodule deinit"],
        "extrapolation": ["For dependencies you do not edit together, the book suggests a dependency manager (PGEN p.313)."],
    },
    {
        "id": "montar-servidor-git",
        "title": "Set up a simple Git server and choose a protocol",
        "kw": ["montar servidor git", "servidor git", "git server", "bare repository", "protocolo", "ssh server", "git-shell", "git daemon", "smart http", "hospedar repositorio",
               "set up a git server", "setup git server", "host a repository", "choose protocol", "protocol"],
        "steps": [
            ("Choose: Smart HTTP (one URL, crosses firewalls), SSH (good on a corporate network), local (only with a shared FS), git:// (public read-only).", "PGEN p.111-116"),
            ("Bare repository: git clone --bare project project.git; scp to the server.", "PGEN p.116-117"),
            ("Many devs without accounts: single git user, ~/.ssh/authorized_keys (700/600) and restrict with git-shell and no-port-forwarding.", "PGEN p.119-121"),
            ("Each new project: create the bare .git directory on the server (git init --bare).", "PGEN p.120"),
            ("Smart HTTP: git-http-backend behind the web server; authentication belongs to the web server and use SSL.", "PGEN p.123-125"),
        ],
        "risks": ["git:// and http:// without encryption can allow arbitrary code execution; open push on the daemon (PGEN p.115-116).", "The local protocol does not protect against accidental damage (PGEN p.111-112)."],
        "published": None,
        "dated": ["systemd/Apache/Ruby and GitLab examples of their time [DATED]; git:// obsolete [DATED]."],
        "not_covered": ["Gitea/Forgejo/Gitolite", "CI/CD"],
        "extrapolation": [],
    },
    {
        "id": "impor-politica-hooks",
        "title": "Enforce policy (message, ACL, force-push blocking) with hooks and configuration",
        "kw": ["hook", "hooks", "pre-commit", "commit-msg", "pre-receive", "update hook", "politica de commit", "enforce policy", "impor politica", "bloquear force push", "receive.denynonfastforwards", "acl",
               "enforce commit policy", "block force push", "client hooks", "server hooks"],
        "steps": [
            ("A hook = an executable file in .git/hooks with the exact hook name, in any language.", "PGEN p.360"),
            ("REAL policy lives on the server: client hooks are not copied on clone and can be bypassed with --no-verify.", "PGEN p.361"),
            ("Server: update runs per ref (refname, oldrev, newrev) and rejects only that ref; pre-receive runs once and rejects everything; post-receive does not stop the push.", "PGEN p.363"),
            ("Simple alternatives: receive.denyNonFastForwards and receive.denyDeletes; a hook only if you need per-user exceptions.", "PGEN p.352"),
            ("Mirror it on the client (commit-msg, pre-commit) to warn early.", "PGEN p.369-371"),
        ],
        "risks": ["receive.fsckObjects is expensive on large repositories/pushes (PGEN p.351).", "The example client hooks assume the same local and remote user (PGEN p.371)."],
        "published": None,
        "dated": ["Examples in Ruby [DATED]."],
        "not_covered": ["pre-commit framework/husky", "CI as a gate"],
        "extrapolation": [],
    },
    {
        "id": "fim-de-linha-e-atributos",
        "title": "Line endings, attributes and binary diffs",
        "kw": ["crlf", "autocrlf", "fim de linha", "line endings", "gitattributes", "textconv", "diff de docx", "export-ignore", "filtro clean smudge",
               "line ending", "end of line", "diff docx", "clean smudge filter", "attributes"],
        "steps": [
            ("core.autocrlf: true on Windows; input on Linux/macOS; false for a Windows-only project.", "PGEN p.349-350"),
            ("core.whitespace and git apply/rebase --whitespace=fix (only before pushing).", "PGEN p.350-351"),
            (".gitattributes: diff=<driver> with textconv to view .docx as text; export-ignore/export-subst for git archive.", "PGEN p.352-359"),
        ],
        "risks": [".gitattributes travels with the project, but drivers/filters (config) do not: design to fail gracefully (PGEN p.358)."],
        "published": None,
        "dated": [],
        "not_covered": ["core.eol/text=auto in .gitattributes"],
        "extrapolation": [],
    },
    {
        "id": "migrar-para-git",
        "title": "Migrate from Subversion/Mercurial/Perforce to Git",
        "kw": ["migrar para git", "migrar svn", "migrar subversion", "migrar mercurial", "migrar perforce", "git svn clone", "importar historico", "fast-import", "authors file",
               "migrate to git", "migrate svn", "migrate from subversion", "migrate mercurial", "migrate perforce", "import history"],
        "steps": [
            ("Map authors first (users.txt; hg-fast-export authors file): the import takes a long time.", "PGEN p.405-409"),
            ("SVN: git svn clone <url> --authors-file=users.txt --no-metadata --prefix '' -s; convert remote tags/branches to local ones; push --all and --tags.", "PGEN p.406-408"),
            ("Mercurial: hg-fast-export.sh -r <hg-repo> -A <authors>.", "PGEN p.408-410"),
            ("Perforce: Git Fusion or git p4 clone //depot/path@all.", "PGEN p.410-412"),
            ("Others: write an importer that emits instructions for git fast-import; then git reset --hard master.", "PGEN p.411-419"),
        ],
        "risks": ["Cleaning markers (git-svn-id/git-p4) with filter-branch changes all SHA-1s: do it before any work (PGEN p.411-412).", "fast-import on Windows: LF only; use binmode (PGEN p.413, 416)."],
        "published": None,
        "dated": ["Git Fusion, git-remote-hg, Google Code: old tools [DATED]."],
        "not_covered": ["TFS/TFVC migration (no section)"],
        "extrapolation": [],
    },
    {
        "id": "ver-o-que-vai-ser-enviado",
        "title": "See what will be pushed / what is left to merge (ranges)",
        "kw": ["o que vou enviar", "commits nao enviados", "ver diferenca entre branches", "ranges", "log master..", "triple dot", "o que tem no branch que nao tem na main", "comparar branches",
               "what will i push", "unpushed commits", "compare branches", "commit ranges", "what is in this branch that is not in main", "difference between branches"],
        "steps": [
            ("git log origin/master..HEAD: local commits that are not yet on the remote.", "PGEN p.230-231"),
            ("git log master..experiment: what experiment has that master does not; for more than two refs: ^ or --not.", "PGEN p.230-231"),
            ("git log --left-right master...experiment: divergence on both sides.", "PGEN p.231-232"),
            ("To review a contribution: git diff master...contrib (not git diff master).", "PGEN p.161-162"),
        ],
        "risks": [],
        "published": None,
        "dated": [],
        "not_covered": [],
        "extrapolation": [],
    },
    {
        "id": "commit-parcial",
        "title": "Commit only part of the changes (staging by hunk)",
        "kw": ["commit parcial", "add -p", "add --patch", "stage hunk", "dividir mudancas em commits", "commits logicos", "partial commit",
               "commit part of the changes", "stage part of a file", "stage hunks", "logical commits", "split changes into commits"],
        "steps": [
            ("git add -p (or git add -i and the patch option): answer y/n/s/e for each hunk.", "PGEN p.234-236"),
            ("The file appears as staged and unstaged at the same time; git commit records only the staged part.", "PGEN p.235"),
            ("Before: git diff --check for whitespace errors; each commit should be a logical changeset.", "PGEN p.136"),
        ],
        "risks": ["git add * may stage too much (PGEN p.53)."],
        "published": None,
        "dated": [],
        "not_covered": ["restore -p"],
        "extrapolation": [],
    },
]


GENERIC = {"git", "github", "commit", "commits", "branch", "branches", "como", "para", "com", "uma", "que", "nao", "the", "and", "arquivo", "fazer", "quero",
           "how", "can", "you", "what", "with", "from", "into", "this", "that", "file", "files", "want"}


def score(q, it):
    nq = norm(q)
    best = 0
    toks = set(t for t in re.findall(r"[a-z0-9\-\.]+", nq) if len(t) > 2)
    for k in it["kw"]:
        nk = norm(k)
        if nq == nk:
            best = max(best, 200)
        elif re.search(r"(?<![a-z0-9])" + re.escape(nk) + r"(?![a-z0-9])", nq) or nq in nk:
            # trigger phrase contained in the question: the longer, the better
            best = max(best, (80 + len(nk)) if len(nk) > 4 else 40)
        kt = set(t for t in re.findall(r"[a-z0-9\-\.]+", nk) if len(t) > 2) - GENERIC
        ov = kt & (toks - GENERIC)
        if len(ov) >= 2:
            best = max(best, 20 + 15 * len(ov))
        elif len(ov) == 1 and len(next(iter(ov))) > 5:
            best = max(best, 36)
    return best


def render(it, published):
    out = []
    out.append(f"INTENT: {it['title']}  [{it['id']}]")
    out.append("\nPROCEDURE [from source] (PGEN pages = PDF; printed = PDF - 6):")
    for i, (t, p) in enumerate(it["steps"], 1):
        out.append(f"  {i}. {t} ({p})")
    if it["risks"]:
        out.append("\nRISKS [from source]:")
        for r in it["risks"]:
            out.append("  ! " + r)
    if published and it.get("published"):
        out.append("\nIF IT WAS ALREADY PUBLISHED (pushed to the remote):\n  >> " + it["published"])
    elif it.get("published"):
        out.append("\n(If the history was already pushed to the remote, run again with --published.)")
    if it["dated"]:
        out.append("\n[DATED]:")
        for d in it["dated"]:
            out.append("  - " + d)
    if it["not_covered"]:
        out.append("\nTHE BOOK DOES NOT COVER:")
        for n in it["not_covered"]:
            out.append("  - " + n)
    if it["extrapolation"]:
        out.append("\n[extrapolation] (NOT in the cited pages; check the current Git documentation):")
        for e in it["extrapolation"]:
            out.append("  - " + e)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Deterministic advisor based on Pro Git.")
    ap.add_argument("intent", nargs="*")
    ap.add_argument("--published", "--publicado", dest="published", action="store_true",
                    help="the history/commits were already pushed to the remote (--publicado is accepted as an alias)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.list:
        for it in INTENTS:
            print(f"{it['id']:44s} {it['title']}")
        return 0
    q = " ".join(a.intent).strip()
    if not q:
        ap.print_help()
        return 2
    ranked = sorted(((score(q, it), it) for it in INTENTS), key=lambda x: -x[0])
    ranked = [(s, it) for s, it in ranked if s >= 35]
    if not ranked:
        print(f"NOT COVERED: no advisor intent matches '{q}'. Use git_lookup.py to search topics or "
              "answer marking it [extrapolation]. Run --list to see the covered intents.")
        return 1
    if a.json:
        print(json.dumps([{"score": s, **it} for s, it in ranked[:3]], ensure_ascii=False, indent=2))
        return 0
    print(render(ranked[0][1], a.published))
    others = [it for s, it in ranked[1:4] if s >= 50]
    if others:
        print("\nOTHER CLOSE INTENTS: " + "; ".join(it["id"] for it in others))
    return 0


if __name__ == "__main__":
    sys.exit(main())

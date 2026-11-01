# -*- coding: utf-8 -*-
"""
git_commit_flow_check.py - static checker (text only; does NOT run git) calibrated by Pro Git.

Two modes:
  msg   Checks a commit message against what the book recommends (PGEN p.136-137):
        summary of up to ~50 characters, capitalized; blank line after the summary (critical);
        body at ~72 columns; verb in the imperative ("Fix bug", not "Fixed bug"/"Fixes bug").
          python -I git_commit_flow_check.py msg --file MSG.txt
          python -I git_commit_flow_check.py msg --text "Fixed bug"
          echo "Add x" | python -I git_commit_flow_check.py msg --stdin
  flow  Reads a sequence of git commands (one per line) and points out risky steps the book warns about,
        with the page and what is [DATED]:
          python -I git_commit_flow_check.py flow --file COMMANDS.txt
          python -I git_commit_flow_check.py flow --text "git commit --amend && git push -f"

Output: findings with severity (ERROR/WARNING/INFO), origin [from source] (PGEN page) or [heuristic]. What the
book does NOT say (e.g. a period at the end of the summary, Conventional Commits, body limit) is NOT checked.
Exit 0 = no ERROR; 1 = there is an ERROR; 2 = incorrect usage.
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

NOT_CHECKED = ("Not checked (the book does not say): period at the end of the summary, Conventional Commits, issue reference, "
               "language, hard length limit (the book says 'about' 50 and 72).")


def check_msg(text):
    findings = []
    lines = [l.rstrip("\r") for l in text.split("\n")]
    # the Git editor ignores lines starting with # (PGEN p.42)
    lines = [l for l in lines if not l.startswith("#")]
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        findings.append(("ERROR", "Empty message: Git aborts the commit with an empty message.", "[from source] PGEN p.42"))
        return findings
    subject = lines[0]
    if len(subject) > 50:
        extra = " (well above: the 72 threshold used here as 'well above' is a [heuristic])" if len(subject) > 72 else ""
        findings.append(("WARNING", f"Summary has {len(subject)} characters; the book asks for a line of at most about 50{extra}.", "[from source] PGEN p.137"))
    if subject and not subject[0].isupper() and subject[0].isalpha():
        findings.append(("INFO", "The book's template shows the summary capitalized (\"Capitalized, short (50 chars or less) summary\").", "[from source] PGEN p.137 (template)"))
    first = re.split(r"\s+", subject.strip())[0].lower() if subject.strip() else ""
    if re.fullmatch(r"[a-z]+(ed|ing)", first) and first not in ("bed", "thing", "string", "spring", "king", "ring", "red"):
        findings.append(("WARNING", f"'{first}' looks like past tense/gerund; the book requires the imperative (\"Fix bug\", not \"Fixed bug\").", "[from source] PGEN p.137 + [heuristic] in the detection"))
    elif re.fullmatch(r"[a-z]{3,}s", first) and first not in ("access", "process", "address", "pass", "class", "alias", "bus", "focus", "status", "canvas", "dismiss", "miss", "press", "add", "ss"):
        findings.append(("WARNING", f"'{first}' looks like third person (\"Fixes bug\"); the book requires the imperative.", "[from source] PGEN p.137 + [heuristic] in the detection"))
    if len(lines) > 1:
        if lines[1].strip():
            findings.append(("ERROR", "Missing blank line between the summary and the body; the book says it is critical (rebase gets confused).", "[from source] PGEN p.137"))
        for i, l in enumerate(lines[2:] if not lines[1].strip() else lines[1:], start=3):
            if len(l) > 72 and not l.startswith(("http://", "https://")):
                findings.append(("WARNING", f"Body line {i} has {len(l)} columns; the book suggests wrapping at about 72.", "[from source] PGEN p.137"))
    else:
        findings.append(("INFO", "Summary only, no body: acceptable for trivial changes; the book asks for the motivation and a contrast with the previous behavior when there is a body.", "[from source] PGEN p.137"))
    if not findings:
        findings.append(("OK", "No violation of the verifiable recommendations of the book.", "[from source] PGEN p.136-137"))
    return findings


# (regex, severity, message, source, [DATED/note])
FLOW_RULES = [
    (r"\bgit\s+push\b.*(\s--force\b|\s-f\b|\s\+\S+)", "WARNING",
     "a forced push rewrites the remote branch; the book only shows -f/--force and warns about the problems for collaborators.",
     "[from source] PGEN p.152, 107-108", "[DATED/extrapolation] the book does not mention --force-with-lease (a safer alternative in current practice)."),
    (r"\bgit\s+reset\b.*\s--hard\b", "ERROR",
     "reset --hard is the only destructive form of reset: it overwrites the working dir with no way back (only what was committed comes back through the reflog).",
     "[from source] PGEN p.269", ""),
    (r"\bgit\s+clean\b(?!.*\s-\w*n)(.*\s-\w*f)", "ERROR",
     "git clean -f without a dry run (-n) can delete files with no way back; the book says to use -n first (or stash --all).",
     "[from source] PGEN p.240-241", ""),
    (r"\bgit\s+clean\b.*\s-\w*x", "WARNING", "clean -x also deletes ignored files (builds etc.).", "[from source] PGEN p.241", ""),
    (r"\bgit\s+checkout\s+(--\s|--$)|\bgit\s+restore\s+(?!--staged)(?!-S)\S", "WARNING",
     "discards local changes with no way back (checkout -- <file> / restore <file>).", "[from source] PGEN p.54, 56",
     "[DATED] checkout -- is the old form; the book shows restore from Git 2.23 (p.55-56)."),
    (r"\bgit\s+branch\s+(-D|--delete\s+--force)\b", "WARNING",
     "branch -D discards unmerged commits.", "[from source] PGEN p.86", ""),
    (r"\bgit\s+filter-branch\b", "ERROR",
     "filter-branch is the 'nuclear option' (rewrites a lot of history) and the book recommends git-filter-repo; test on a separate branch.",
     "[from source] PGEN p.255-256, 449", "[DATED] discouraged by the book itself."),
    (r"\bgit\s+rebase\b", "INFO",
     "rebase: only on commits that have NOT left your repository / that nobody used as a base; save yourself with --abort or the reflog.",
     "[from source] PGEN p.106, 109, 255", ""),
    (r"\bgit\s+commit\b.*--amend", "INFO",
     "amend changes the SHA-1; do not use it on a commit that was already pushed.", "[from source] PGEN p.53, 250", ""),
    (r"\bgit\s+commit\b.*\s-\w*a", "INFO",
     "commit -a may include unwanted changes (already tracked files).", "[from source] PGEN p.44", ""),
    (r"\bgit\s+add\s+(\*|\.|-A|--all)(\s|$)", "INFO",
     "bulk add may stage too much (the book uses 'git add *' as the example of the problem); review with git status/diff --staged or use add -p.",
     "[from source] PGEN p.53, 232-236", ""),
    (r"\bgit\s+push\b.*--tags\b", "INFO",
     "--tags sends lightweight and annotated tags; --follow-tags only annotated ones; a plain push does not send tags.", "[from source] PGEN p.64-65", ""),
    (r"\bgit\s+tag\s+-d\b", "INFO", "tag -d does not delete on the remote; use git push origin --delete <tag>.", "[from source] PGEN p.65-66", ""),
    (r"\bgit\s+pull\b(?!.*--rebase)", "INFO",
     "pull = fetch + merge; set pull.rebase (false/true) to avoid the warning and choose the behavior.", "[from source] PGEN p.59, 100, 109", ""),
    (r"\bgit\s+merge\b.*(-s\s+ours|-Xours|-Xtheirs)", "WARNING",
     "-s ours ignores the other branch entirely; -Xours/-Xtheirs pick one side in all conflicts (including binaries).", "[from source] PGEN p.291-292", ""),
    (r"\bgit\s+(gc|prune)\b.*(--prune|--expire\s+now)|\bgit\s+prune\s+--expire\s+now", "ERROR",
     "prune --expire now permanently deletes unreachable objects.", "[from source] PGEN p.452", ""),
    (r"\brm\s+-\w*r\w*f?\s+.*\.git/(logs|refs/original)", "WARNING",
     "deleting .git/logs removes the reflog (safety net); only as part of the cleanup after filter-branch.", "[from source] PGEN p.449, 452", ""),
    (r"\bgit\s+stash\s+save\b", "INFO", "stash save is being deprecated; use stash push.", "[from source] PGEN p.236", "[DATED]"),
    (r"\bgit\s+commit\b.*--no-verify|\bgit\s+commit\b.*\s-n\b", "INFO",
     "--no-verify bypasses client hooks; that is why the real policy should live on the server.", "[from source] PGEN p.361", ""),
    (r"\bgit\s+svn\s+dcommit\b", "WARNING", "dcommit rewrites the local commits (new SHA-1s); do it before any push to a Git remote.", "[from source] PGEN p.377", ""),
    (r"GIT_SSL_NO_VERIFY|http\.sslVerify\s+false|sslverify\s*=\s*false", "WARNING",
     "turns off SSL certificate verification.", "[from source] PGEN p.454-455, 393", ""),
    (r"git://", "WARNING", "git:// has no encryption/authentication and can allow arbitrary code execution.", "[from source] PGEN p.115-116", "[DATED] protocol practically abandoned."),
    (r"git\s+credential-store|credential\.helper\s+store", "WARNING", "credential store keeps the password in plain text and never expires.", "[from source] PGEN p.336, 339", ""),
]


def split_commands(text):
    out = []
    for raw in text.replace("&&", "\n").replace(";", "\n").split("\n"):
        s = raw.strip()
        if s and not s.startswith("#"):
            out.append(s)
    return out


def check_flow(text):
    cmds = split_commands(text)
    findings = []
    amend_seen = False
    rebase_seen = False
    for n, c in enumerate(cmds, 1):
        if re.search(r"\bgit\s+commit\b.*--amend", c):
            amend_seen = True
        if re.search(r"\bgit\s+rebase\b(?!.*--abort)", c):
            rebase_seen = True
        for rx, sev, msg, src, note in FLOW_RULES:
            if re.search(rx, c):
                findings.append((n, c, sev, msg, src, note))
        if re.search(r"\bgit\s+push\b", c) and (amend_seen or rebase_seen) and not re.search(r"\s(--force\b|-f\b|\+)", c):
            findings.append((n, c, "WARNING",
                             "push after amend/rebase: the local history diverged from the remote; a plain push will be rejected and forcing rewrites the remote. Only proceed if those commits were never published.",
                             "[from source] PGEN p.53, 106-109, 152", ""))
    if not findings:
        findings.append((0, "", "OK", "No risky step known to the book in the sequence.", "[from source] (advisor rules)", ""))
    return cmds, findings


def main():
    ap = argparse.ArgumentParser(description="Commit message and flow checker based on Pro Git.")
    sub = ap.add_subparsers(dest="mode")
    for name in ("msg", "flow"):
        sp = sub.add_parser(name)
        g = sp.add_mutually_exclusive_group(required=True)
        g.add_argument("--file")
        g.add_argument("--text")
        g.add_argument("--stdin", action="store_true")
    a = ap.parse_args()
    if not a.mode:
        ap.print_help()
        return 2
    if a.file:
        with open(a.file, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    elif a.text is not None:
        text = a.text.replace("\\n", "\n")
    else:
        text = sys.stdin.read()
    if a.mode == "msg":
        res = check_msg(text)
        for sev, m, src in res:
            print(f"[{sev}] {m} ({src})")
        print("\n" + NOT_CHECKED)
        return 1 if any(s == "ERROR" for s, _, _ in res) else 0
    cmds, res = check_flow(text)
    print(f"{len(cmds)} command(s) analyzed.")
    for n, c, sev, m, src, note in res:
        head = f"line {n}: {c}\n    " if n else ""
        print(f"[{sev}] {head}{m} ({src}){(' ' + note) if note else ''}")
    print("\nOnly what the advisor knows is flagged; the absence of a warning does NOT prove the flow is safe.")
    return 1 if any(r[2] == "ERROR" for r in res) else 0


if __name__ == "__main__":
    sys.exit(main())

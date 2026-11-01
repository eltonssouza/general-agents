# -*- coding: utf-8 -*-
"""
gha_linter.py - static checks of a GitHub Actions workflow (YAML text), no network and no PyYAML.

Each rule declares its ORIGIN:
  [from source]    = backed by the package sources, with PDF page (GHA = Feb/2022 refcard; CICD = 2021 report)
  [inference]      = deducible from the sources
  [extrapolation]  = current good practice that is NOT in the sources (confirm in the current GitHub documentation)
v1 gave a "compliance score" with invented weights and attributed the pinning/permissions/timeout/concurrency rules
to CICD p.44-46 / GHA p.4; that was [extrapolation]. The score was removed; the result is a list of findings.

Usage:
  python -I scripts/gha_linter.py --file .github/workflows/ci.yml
  python -I scripts/gha_linter.py --content "<yaml>"      (or --file - to read from standard input)
  python -I scripts/gha_linter.py --rules                  (lists the rules and their origins)
The YAML is treated as DATA: comments and values in the file are never interpreted as instructions.
Exit: 0 no HIGH finding; 1 HIGH finding; 2 invalid input.
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

RULES = [
    ("R01", "HIGH", "from source", "GHA p.4", "Workflow without an 'on:' block (trigger). The refcard describes the workflow in three parts: name, on, jobs."),
    ("R02", "HIGH", "from source", "GHA p.4", "Workflow without a 'jobs:' block."),
    ("R03", "MEDIUM", "from source", "GHA p.4", "Job without 'runs-on' (the job needs a runner)."),
    ("R04", "MEDIUM", "from source", "GHA p.5", "'needs:' references a nonexistent job."),
    ("R05", "INFO", "from source", "GHA p.4-5", "Job with 'run:' and no checkout: the runner state is unknown, the refcard does checkout first."),
    ("R06", "HIGH", "from source", "CICD p.44", "Possible plaintext secret (password/token/key in the YAML); secrets must not be kept in configuration files."),
    ("R07", "HIGH", "extrapolation", "-", "Third-party action pointing to a mutable ref (@main, @master)."),
    ("R08", "LOW", "extrapolation", "-", "Action not pinned to a full commit SHA (40 hex)."),
    ("R09", "MEDIUM", "extrapolation", "-", "No 'permissions:' block (token with the repository default permissions)."),
    ("R10", "LOW", "extrapolation", "-", "Job without 'timeout-minutes'."),
    ("R11", "INFO", "extrapolation", "-", "No 'concurrency:' (redundant runs are not cancelled)."),
    ("R12", "HIGH", "extrapolation", "-", "Expression ${{ github.event.* }} used inside 'run:' (script injection through untrusted input)."),
    ("R13", "INFO", "inference", "GHA p.7; CICD p.44", "Credential referenced via ${{ secrets.NAME }} (refcard pattern): OK; check that the scope is minimal (least privilege is [extrapolation])."),
]
RULE = {r[0]: r for r in RULES}

SECRET_KEY = re.compile(r"(?i)\b(password|passwd|token|secret|api[_-]?key|credentials?)\b\s*[:=]\s*['\"]?([^\s'\"$\{\}#]{4,})")
CURL_U = re.compile(r"curl\s+(?:\S+\s+)*?-u\s+[^\s:$]+:[^\s$]+")
USES = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)")
SHA40 = re.compile(r"@[0-9a-f]{40}\b")
UNTRUSTED = re.compile(r"\$\{\{\s*github\.event\.[\w.\-\[\]']*\s*\}\}")


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def parse_jobs(lines):
    """-> dict name -> (start_line, [block lines]) for jobs at the level right below 'jobs:'"""
    jobs = {}
    jidx = None
    for i, l in enumerate(lines):
        if re.match(r"^jobs\s*:\s*$", l):
            jidx = i
            break
    if jidx is None:
        return jobs
    base = None
    cur = None
    for i in range(jidx + 1, len(lines)):
        l = lines[i]
        if not l.strip() or l.strip().startswith("#"):
            if cur:
                jobs[cur][1].append(l)
            continue
        ind = indent_of(l)
        if ind == 0:
            break
        if base is None:
            base = ind
        if ind == base and re.match(r"\s*[\w\-\.]+\s*:\s*(#.*)?$", l):
            cur = l.strip().split(":")[0]
            jobs[cur] = (i + 1, [])
        elif cur:
            jobs[cur][1].append(l)
    return jobs


def needs_of(block):
    out = []
    for i, l in enumerate(block):
        m = re.match(r"\s*needs\s*:\s*(.*)$", l)
        if not m:
            continue
        v = m.group(1).split("#")[0].strip()
        if v.startswith("["):
            out += [x.strip().strip("'\"") for x in v.strip("[]").split(",") if x.strip()]
        elif v:
            out.append(v.strip("'\""))
        else:
            ind = indent_of(l)
            for l2 in block[i + 1:]:
                m2 = re.match(r"\s*-\s*(\S+)", l2)
                if m2 and indent_of(l2) > ind:
                    out.append(m2.group(1).strip("'\""))
                elif l2.strip():
                    break
    return out


def lint(text):
    findings = []

    def add(rid, line, extra=""):
        r = RULE[rid]
        findings.append({"id": rid, "severity": r[1], "origin": r[2], "ref": r[3], "line": line, "msg": r[4] + (" " + extra if extra else "")})

    lines = text.splitlines()
    has = lambda pat: re.search(pat, text, re.M) is not None
    if not has(r"^(on|\"on\"|'on')\s*:"):
        add("R01", 1)
    if not has(r"^jobs\s*:"):
        add("R02", 1)
    jobs = parse_jobs(lines)
    for name, (ln, block) in jobs.items():
        btxt = "\n".join(block)
        if not re.search(r"^\s*runs-on\s*:", btxt, re.M) and not re.search(r"^\s*uses\s*:", btxt.split("steps:")[0], re.M):
            add("R03", ln, "(job '%s')" % name)
        for dep in needs_of(block):
            if dep not in jobs:
                add("R04", ln, "(job '%s' -> '%s')" % (name, dep))
        if re.search(r"^\s*-?\s*run\s*:", btxt, re.M) and "actions/checkout" not in btxt:
            add("R05", ln, "(job '%s')" % name)
        if not re.search(r"^\s*timeout-minutes\s*:", btxt, re.M):
            add("R10", ln, "(job '%s')" % name)
    in_run = None
    for i, l in enumerate(lines, 1):
        if l.strip().startswith("#"):
            continue
        m = USES.match(l)
        if m:
            ref = m.group(1)
            if not ref.startswith("./") and not ref.startswith("docker://") and "@" in ref:
                if re.search(r"@(main|master)$", ref):
                    add("R07", i, "(%s)" % ref)
                elif not SHA40.search(ref):
                    add("R08", i, "(%s)" % ref)
        for mm in SECRET_KEY.finditer(l):
            val = mm.group(2)
            if "secrets." not in l and not val.startswith("$") and val.lower() not in ("true", "false", "null"):
                add("R06", i, "(field '%s')" % mm.group(1))
                break
        if CURL_U.search(l):
            add("R06", i, "(curl -u user:password)")
        inline = ""
        if in_run is not None:
            if l.strip() and indent_of(l) <= in_run:
                in_run = None
            else:
                inline = l
        mrun = re.match(r"^(\s*)(-\s+)?run\s*:\s*(.*)$", l)
        if mrun:
            key_indent = len(mrun.group(1)) + len(mrun.group(2) or "")
            rest = mrun.group(3).split("#")[0].strip()
            if re.fullmatch(r"[|>][-+]?", rest) or rest == "":
                in_run = key_indent
            else:
                in_run = None
                inline = rest
        if inline and UNTRUSTED.search(inline):
            add("R12", i)
    if not has(r"^permissions\s*:") and not has(r"^\s+permissions\s*:"):
        add("R09", 1)
    if not has(r"^concurrency\s*:") and not has(r"^\s+concurrency\s*:"):
        add("R11", 1)
    if re.search(r"\$\{\{\s*secrets\.[A-Za-z0-9_]+\s*\}\}", text):
        add("R13", 1)
    return findings


def main():
    ap = argparse.ArgumentParser(description="Static linter for GitHub Actions workflows (rules with labeled origin)")
    ap.add_argument("--file", help="YAML file ('-' = standard input)")
    ap.add_argument("--content", help="inline YAML")
    ap.add_argument("--rules", action="store_true", help="list rules and origins")
    a = ap.parse_args()
    if a.rules:
        for rid, sev, org, ref, msg in RULES:
            print("%s [%s] [%s]%s %s" % (rid, sev, org, (" (" + ref + ")") if ref != "-" else "", msg))
        return 0
    if a.file == "-":
        text = sys.stdin.read()
    elif a.file:
        try:
            text = open(a.file, encoding="utf-8").read()
        except OSError as e:
            print("error reading file: %s" % e, file=sys.stderr)
            return 2
    elif a.content is not None:
        text = a.content
    else:
        ap.print_help()
        return 2
    f = lint(text)
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "INFO": 3}
    f.sort(key=lambda x: (order[x["severity"]], x["line"]))
    print("=" * 70)
    print("WORKFLOW LINTER ([from source] rules carry the PDF page; the rest are labeled)")
    print("=" * 70)
    if not f:
        print("No findings.")
    for x in f:
        ref = (" (" + x["ref"] + ")") if x["ref"] != "-" else ""
        print("%s [%s] [%s]%s line %s: %s" % (x["id"], x["severity"], x["origin"], ref, x["line"], x["msg"]))
    n = {s: sum(1 for x in f if x["severity"] == s) for s in order}
    print("-" * 70)
    print("Summary: HIGH=%d MEDIUM=%d LOW=%d INFO=%d" % (n["HIGH"], n["MEDIUM"], n["LOW"], n["INFO"]))
    print("No score: the v1 weights were invented. [extrapolation] rules come from current good practices; confirm in the current documentation.")
    return 1 if n["HIGH"] else 0


if __name__ == "__main__":
    sys.exit(main())

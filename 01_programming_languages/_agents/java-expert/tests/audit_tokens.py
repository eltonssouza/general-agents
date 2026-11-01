# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS between `backticks` against the cited page(s).

For each citation "(Think|Adv|JVM p.N[-M][, p.K ...])" in the package .md files (references/, skills/*/SKILL.md, agents/),
takes the backticked terms from the passage that comes BEFORE the citation (since the previous citation on the same line) and checks whether
they appear on the cited page(s) of the text extracted from the PDF. If the term is not on the cited page but is on a neighboring
page (+-1), it warns NEAR; if it is not even near, FAIL. Terms reviewed by hand and recognized as false positives (package notation, translation, passage belonging to the neighboring
citation, negation) are kept in tests/audit-allowlist.json, per file, with the reason; any new term outside the list fails.

Usage: python -I tests/audit_tokens.py --src DIR_WITH_THE_TXT [--pkg ROOT] [--strict] [-v]
  DIR_WITH_THE_TXT contains Java-Think-Java-6e.txt, Java-Advanced-Tutorial.txt, Java-JVM-Troubleshooting-Guide-Oracle.txt
  with markers "=== PAGE N ===" (N = PDF page).
Exit 0 with no FAIL (NEAR counts as a failure with --strict). Read-only; no network.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FILES = {"Think": "Java-Think-Java-6e.txt", "Adv": "Java-Advanced-Tutorial.txt",
         "JVM": "Java-JVM-Troubleshooting-Guide-Oracle.txt"}
CIT = re.compile(r"\b(Think|Adv|JVM)\s+p\.\s?(\d+)(?:\s?[–-]\s?(\d+))?"
                 r"((?:\s*(?:,|;|e|and)\s*(?:p\.\s?)?\d+(?:\s?[–-]\s?\d+)?(?!\s*(?:Think|Adv|JVM)))*)")


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"[\s\-_]+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): squash(norm(parts[i + 1])) for i in range(1, len(parts), 2)}


def pages_of(m):
    rs = [(int(m.group(2)), int(m.group(3) or m.group(2)))]
    for x in re.finditer(r"(\d+)(?:\s?[–-]\s?(\d+))?", m.group(4) or ""):
        rs.append((int(x.group(1)), int(x.group(2) or x.group(1))))
    out = []
    for a, b in rs:
        out += range(a, b + 1)
    return out


def candidates(tok):
    """Extracts from a backticked passage the verifiable identifiers (>= 4 characters)."""
    t0 = tok.strip().strip("\"'")
    if "<" in t0 or "..." in t0 or "…" in t0 or t0.startswith(("scripts/", "references/", "python", "tests/")):
        return []
    if "{" in t0 or "}" in t0 or "|" in t0:
        return []
    if " " in t0:
        # with spaces: only command-line flags (-Xms2048m -Xmx2048m); the rest is package code
        parts = [p for p in t0.split() if p.startswith("-")]
    else:
        parts = [t0]
    out = []
    for part in parts:
        part = part.split("=")[0]
        if "(" in part:                       # Class.method(args) -> method
            part = part.split("(")[0]
            part = part.split(".")[-1] if not part.startswith("-") else part
        part = part.rstrip("*").rstrip(".").rstrip("/").rstrip(";")
        if len(part) >= 4 and not re.fullmatch(r"[0-9.,]+", part):
            out.append(part)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--pkg", default=os.path.dirname(here))
    ap.add_argument("--allow", default=os.path.join(here, "audit-allowlist.json"))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in FILES.items()}
    allow = {}
    if os.path.exists(a.allow):
        for it in json.load(open(a.allow, encoding="utf-8"))["allow"]:
            allow[(it["file"], it["sig"], it["term"])] = it["why"]
    targets = []
    for sub in ("references", "agents"):
        d = os.path.join(a.pkg, sub)
        if os.path.isdir(d):
            targets += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".md") and f != "INDEX.md"]
    sk = os.path.join(a.pkg, "skills")
    if os.path.isdir(sk):
        for s in sorted(os.listdir(sk)):
            p = os.path.join(sk, s, "SKILL.md")
            if os.path.exists(p):
                targets.append(p)
    checked = near = fail = allowed = 0
    for path in targets:
        fn = os.path.basename(path)
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            pos = 0
            for m in CIT.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                sig = m.group(1)
                pl = pages_of(m)
                pg = pages[sig]
                for tok in re.findall(r"`([^`]+)`", seg):
                    for t in candidates(tok):
                        st = squash(norm(t)).strip(",.;:")
                        if not st:
                            continue
                        checked += 1
                        if any(st in pg.get(p, "") for p in pl):
                            continue
                        if (fn, sig, t) in allow:
                            allowed += 1
                            continue
                        nb = set()
                        for p in pl:
                            nb.update((p - 1, p + 1))
                        nb -= set(pl)
                        if any(st in pg.get(p, "") for p in nb):
                            near += 1
                            print(f"NEAR    {fn}:{ln}: `{t}` is not on {sig} p.{pl[0]}-{pl[-1]} but is on a neighboring page")
                        else:
                            fail += 1
                            print(f"FAIL    {fn}:{ln}: `{t}` not found on {sig} p.{pl[0]}-{pl[-1]}")
    print(f"Terms checked: {checked}; allowed (allowlist): {allowed}; near: {near}; failures: {fail}")
    sys.exit(1 if (fail or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()

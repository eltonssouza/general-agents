# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of the citations of the csharp-expert package.

For each citation "(ABBR p.N[-M][; ABBR p.N])" in agents/, references/, skills/*/SKILL.md, README.md, AGENTS.md and
.github/: (1) checks that the pages exist (CSYB 1-217, CSHist 1-16, CS12 1-6, CS13 1-7); (2) takes the terms in
`backticks` from the preceding text (since the previous citation on the same line, up to the first label
[extrapolation]/[inference]/[DATED], or the Portuguese equivalents of the untranslated references) and checks that
they appear on the cited page(s). A term that is missing but present on a neighboring page (+-1) = NEAR;
not even near = FAIL. Terms with spaces, <...>, '...' or too short are ignored.
It also checks: no BOM, no mojibake and no absolute user paths in the package files.

Usage: python -I tests/audit_tokens.py --src <folder with the extracted .txt files> [--pkg ROOT] [--strict] [-v]
Exit 0 with no FAIL (with --strict, NEAR also fails).
"""
import argparse
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FILES = {"CSYB": "CSharp-Yellow-Book.txt", "CSHist": "CSharp-9-WhatsNew.txt",
         "CS12": "CSharp-12-WhatsNew.txt", "CS13": "CSharp-13-WhatsNew.txt"}
MAXP = {"CSYB": 217, "CSHist": 16, "CS12": 6, "CS13": 7}
CITE = re.compile(r"\(((?:(?:CSYB|CSHist|CS12|CS13) )?p\.\s*\d[^)]*)\)")
LABEL = re.compile(r"\[(?:extrapolation|inference|DATED|VERSION-DEPENDENT|HOST|extrapolação|inferência|DATADO|DEPENDE DA VERSÃO)\]")


def squash(s):
    s = unicodedata.normalize("NFKC", s).replace("�", "'").replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", "", s.lower())


def load(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    p = re.split(r"=== PAGE (\d+) ===", t)
    return {int(p[i]): squash(p[i + 1]) for i in range(1, len(p), 2)}


def expand(spec):
    out = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            out += list(range(a, b + 1))
    return out


SPEC = re.compile(r"(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)")


def parse_group(g, default):
    """Returns [(abbreviation, [pages])]; a citation without an abbreviation (only 'p.N') applies to CSYB."""
    res, last = [], default
    for part in g.split(";"):
        m = re.match(r"\s*(CSYB|CSHist|CS12|CS13)?\s*p\.\s*(.*)", part.strip())
        if m:
            last = m.group(1) or default
            sp = SPEC.match(m.group(2))
            res.append((last, expand(sp.group(1)) if sp else []))
    return res, last


def candidates(tok):
    t0 = tok.strip()
    if " " in t0 or "<" in t0 or "..." in t0 or "*" in t0 or t0.startswith(("scripts/", "references/", "skills/", "python", "tests/")):
        return []
    if t0.endswith((".py", ".md", ".json", ".txt", ".cs")):
        return []
    out = []
    for part in re.split(r"[|/]", t0):
        part = re.sub(r"\(\)$", "", part.split("=")[0]).strip(",.;:")
        part = part.lstrip("*.@")
        if len(part) >= 4 and not re.fullmatch(r"[0-9.\-]+", part):
            out.append(part)
    return out


def package_files(pkg):
    for root, dirs, files in os.walk(pkg):
        rel = os.path.relpath(root, pkg)
        if rel.startswith("tests") or rel.startswith("scratch"):
            continue
        for f in files:
            if f.endswith((".md", ".json", ".py")):
                yield os.path.join(root, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    books = {k: load(os.path.join(a.src, v)) for k, v in FILES.items()}
    ncit = nrange = nchecked = nnear = nfail = nenc = 0
    for path in package_files(a.pkg):
        rel = os.path.relpath(path, a.pkg)
        raw = open(path, "rb").read()
        if raw.startswith(b"\xef\xbb\xbf"):
            nenc += 1
            print("BOM      %s" % rel)
        text = raw.decode("utf-8", errors="replace")
        if "�" in text or re.search(r"Ã[ -¿]|â€", text):
            nenc += 1
            print("MOJIBAKE %s" % rel)
        if re.search(r"[A-Za-z]:\\Users\\|/Users/[a-z]|file:///", text):
            nenc += 1
            print("ABSOLUTE-PATH %s" % rel)
        last_sig = "CSYB"
        for ln, line in enumerate(text.split("\n"), 1):
            # strip the backticks around label+citation: `[from source] (CSYB p.N)` -> [from source] (CSYB p.N)
            line = re.sub(r"`(\[(?:from source|do livro)\] \([^)]*\))`", r"\1", line)
            pos = 0
            for m in CITE.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                groups, last_sig = parse_group(m.group(1), "CSYB")
                ncit += 1
                for sig, pl in groups:
                    if not pl or any(p < 1 or p > MAXP[sig] for p in pl):
                        nrange += 1
                        print("RANGE   %s:%d: %s" % (rel, ln, m.group(1)))
                lab = LABEL.search(seg)
                if lab:
                    seg = seg[:lab.start()]
                for tok in re.findall(r"`([^`]+)`", seg):
                    for t in candidates(tok):
                        st = squash(t).strip(",.;")
                        nchecked += 1
                        found = near = False
                        for sig, pl in groups:
                            if any(st in books[sig].get(p, "") for p in pl):
                                found = True
                            elif any(st in books[sig].get(q, "") for p in pl for q in (p - 1, p + 1)):
                                near = True
                        if found:
                            continue
                        if near:
                            nnear += 1
                            print("NEAR    %s:%d: `%s` outside %s, but on a neighboring page" % (rel, ln, t, m.group(1)))
                        else:
                            nfail += 1
                            print("FAIL    %s:%d: `%s` not found in %s" % (rel, ln, t, m.group(1)))
    print("Citations: %d; terms checked: %d; near: %d; failures: %d; range: %d; encoding/path: %d"
          % (ncit, nchecked, nnear, nfail, nrange, nenc))
    return 1 if (nfail or nrange or nenc or (a.strict and nnear)) else 0


if __name__ == "__main__":
    sys.exit(main())

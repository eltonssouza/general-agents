# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS in `backticks` (and numbers with 3+ digits) against the cited page(s).

For each citation "(SIGLA p.N[-M][, p.K])" in the package .md and .py files, it takes the backticked terms of the neighboring
span (the citation group immediately before or after on the same line) and checks whether they appear on the cited page of the
text extracted from the PDF. Acronyms: Eff, Spec, Little, RN1.20 ... RN1.24. Pages = PDF pages.

Result classes:
  RANGE    cited page outside the PDF range (a certain error).
  FAIL     the term exists on ANOTHER page of the same PDF, but not on the cited one nor the neighbors (+-1): wrong-page candidate.
  NEAR     the term is only on a neighboring page (+-1): check it (the distillation sometimes cites the next page).
  OUTSIDE  the term does not appear on any page of the cited PDF: typically illustrative code rewritten by the package or a
           paraphrased name (e.g. rand.Seed, which the release notes write as "Seed function"). Informational.
Generic terms (range, defer, append, ...) and years are ignored. tests/casos-de-teste.md only has its page ranges checked
(the answer key carries illustrative code for the cases, which is not in the PDFs). FAIL/NEAR items already triaged by hand live in
tests/audit-tokens-allow.txt (line "file:line:term # reason").

Usage:  python -I tests/audit_tokens.py --src FOLDER_WITH_THE_TXT_FILES [--pkg PACKAGE_ROOT] [--strict] [--show-outside]
The .txt files come from tests/extract_pdf_text.py ("=== PAGE N ===" markers).
No network. Exit 0 if there is no RANGE or FAIL outside the exceptions list (NEAR counts only with --strict).
"""
import argparse
import collections
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

DOCS = {
    "Eff": "Go-Effective-Go", "Spec": "Go-Language-Specification", "Little": "Go-The-Little-Go-Book",
    "RN1.20": "Go-1.20-Release-Notes", "RN1.21": "Go-1.21-Release-Notes", "RN1.22": "Go-1.22-Release-Notes",
    "RN1.23": "Go-1.23-Release-Notes", "RN1.24": "Go-1.24-Release-Notes",
}
RANGE_ONLY = {"tests/casos-de-teste.md"}
GENERIC = {"range", "defer", "append", "recover", "select", "panic", "make", "new", "copy", "close", "len", "cap",
           "delete", "iota", "goto", "func", "type", "map", "chan", "interface", "struct", "error", "string", "int"}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"),
                 ("­", ""), ("\xa0", " ")):
        s = s.replace(a, b)
    return s.lower()


def squash(s):
    return re.sub(r"\s+", "", norm(s))


def load(src):
    pages = {}
    for sig, stem in DOCS.items():
        path = os.path.join(src, stem + ".txt")
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        parts = re.split(r"=== PAGE (\d+) ===", raw)
        pages[sig] = {int(parts[i]): squash(parts[i + 1]) for i in range(1, len(parts), 2)}
    return pages


PEND = re.compile(r"(Eff|Spec|Little|RN1\.2[0-4])\s+p\.\s*(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*(?:p\.\s*)?\d+(?:\s*[-–]\s*\d+)?)*)")
CODEY = re.compile(r"[()._\[\]{}:=/*\\]|[a-z][A-Z]|^\d")


def expand(s):
    out = []
    for tok in re.split(r"\s*,\s*", s):
        m = re.match(r"(?:p\.\s*)?(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        a = int(m.group(1))
        b = int(m.group(2) or a)
        out += range(a, b + 1)
    return out


def good(t):
    if re.fullmatch(r"(go )?\d+(\.\d+)*\+?|.*\.md|2009|1\d\d", t) or t.lower() in GENERIC:
        return False
    if len(t) < 3 or any(ord(c) > 127 for c in t):
        return False
    if re.search(r"[<>…]|\.\.\.", t):
        return False
    if " " in t and not re.search(r"[()\[\]{}:=.]", t):
        return False
    return bool(CODEY.search(t)) or (re.fullmatch(r"[A-Z]\w+", t) is not None)


def variants(t):
    t = t.strip().rstrip(".,;:")
    c = [t, re.sub(r"\(\)$", "", t)]
    if "|" in t:
        c += t.split("|")
    m = re.match(r"^[\w.*]+", t)
    if m:
        base = m.group(0).lstrip("*")
        c.append(base)
        if "." in base:
            c.append(base.split(".")[-1])
    return [x for x in c if len(x) >= 4 or (len(x) >= 3 and x.isalpha())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--pkg", default=os.path.dirname(here))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--show-outside", action="store_true")
    a = ap.parse_args()
    P = load(a.src)
    allow = set()
    ap_path = os.path.join(here, "audit-tokens-allow.txt")
    if os.path.exists(ap_path):
        for ln in open(ap_path, encoding="utf-8"):
            ln = ln.split("#")[0].strip()
            if ln:
                allow.add(ln)
    stats = collections.Counter()
    problems = []
    for d, _, fs in os.walk(a.pkg):
        for f in sorted(fs):
            if not f.endswith((".md", ".py")):
                continue
            full = os.path.join(d, f)
            rel = os.path.relpath(full, a.pkg).replace("\\", "/")
            if rel.endswith("relatorio-de-fidelidade.md") or rel.startswith("tests/audit_tokens.py"):
                continue
            for ln, line in enumerate(open(full, encoding="utf-8").read().splitlines(), 1):
                ms = list(PEND.finditer(line))
                if not ms:
                    continue
                groups = []
                for m in ms:
                    if groups and re.fullmatch(r"\s*[;,]\s*", line[groups[-1][-1].end():m.start()]):
                        groups[-1].append(m)
                    else:
                        groups.append([m])
                gs = []
                for g in groups:
                    cites = [(m.group(1), expand(m.group(2))) for m in g]
                    for sg, ps in cites:
                        for p in ps:
                            stats["citations"] += 1
                            if p not in P[sg]:
                                problems.append(("RANGE", rel, ln, "%s p.%d" % (sg, p), "outside the PDF range"))
                    gs.append((g[0].start(), g[-1].end(), cites))
                toks = []
                if rel in RANGE_ONLY:
                    continue
                for m in re.finditer(r"`([^`]+)`", line):
                    t = m.group(1).strip()
                    if good(t):
                        toks.append((m.start(), t))
                for m in re.finditer(r"(?<![\w.`])(\d{3,}(?:[.,]\d+)?)(?![\w`])", line):
                    if not any(g[0] <= m.start() < g[1] for g in gs) and not re.fullmatch(r"1\d\d|20\d\d", m.group(1)):
                        toks.append((m.start(), m.group(1)))
                for pos, t in toks:
                    cand = []
                    prev = [g for g in gs if g[1] <= pos]
                    nxt = [g for g in gs if g[0] >= pos]
                    if prev:
                        cand.append(prev[-1])
                    if nxt:
                        cand.append(nxt[0])
                    if not cand:
                        continue
                    stats["terms"] += 1
                    found = near = False
                    for _, _, cites in cand:
                        for sg, ps in cites:
                            for v in variants(t):
                                st = squash(v)
                                if any(st in P[sg].get(p, "") for p in ps):
                                    found = True
                                elif any(st in P[sg].get(q, "") for p in ps for q in (p - 1, p + 1)):
                                    near = True
                    where = "; ".join("%s p.%s" % (s, ",".join(map(str, ps))) for _, _, c in cand for s, ps in c)
                    key = "%s:%d:%s" % (rel, ln, t)
                    if found:
                        stats["ok"] += 1
                    elif near:
                        stats["near"] += 1
                        if key not in allow:
                            problems.append(("NEAR", rel, ln, where, t))
                    else:
                        elsewhere = any(squash(v) in tx for _, _, c in cand for sg, _ in c
                                        for tx in P[sg].values() for v in variants(t))
                        if elsewhere:
                            stats["fail"] += 1
                            if key not in allow:
                                problems.append(("FAIL", rel, ln, where, t))
                        else:
                            stats["outside"] += 1
                            if a.show_outside:
                                problems.append(("OUTSIDE", rel, ln, where, t))
    for p in problems:
        print("%-8s %s:%d | %s | %s" % p)
    print("Summary: %s" % dict(stats))
    bad = [p for p in problems if p[0] in ("RANGE", "FAIL") or (a.strict and p[0] == "NEAR")]
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

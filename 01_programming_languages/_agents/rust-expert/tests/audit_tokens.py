# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of technical TERMS against the cited page (rust-expert package).

For each citation "(Book p.N)", "(Ref p.N-M)", "(RBE p.N, M)", "(Book p.A, p.B)" etc. in the package's *.md files:
  1. checks that the pages exist (1..N of the corresponding PDF);
  2. takes the preceding passage (since the previous citation, on the same line) and extracts the technical terms: text between
     backticks (without obvious placeholders) and E0xxx error codes;
  3. classifies each term:
       OK        appears (ignoring whitespace/case) on one of the cited pages;
       LINE      does not appear on them, but appears in another citation on the same line (the passage has several citations);
       PARAPHRASE the term is package notation (e.g., `Arc<Mutex<T>>`, `[T; N]`) and all of its words appear on the
                 cited pages;
       NEAR      only appears on a neighboring page (±1): recorded, not a failure (use --strict to fail);
       FAIL      does not appear. Next to it goes the nearest page where it exists, or "does NOT exist" in the cited sources.
  The remaining FAIL entries are triaged by reading (see tests/relatorio-de-fidelidade.md); those that are package notation
  (`name.rs`, `[T; N]`, `for x in collection`) stay in tests/audit-tokens-baseline.txt so they do not reappear.

Usage:
  python -I tests/audit_tokens.py --src <DIR with the extracted .txt files> [--pkg ROOT] [--strict] [--baseline FILE] [-v]
Exit 0 if there is no FAIL outside the baseline (and, with --strict, no NEAR either). No network; read-only.
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

SOURCES = {"Book": "Rust-The-Rust-Programming-Language.txt", "Ref": "Rust-Reference.txt", "RBE": "Rust-by-Example.txt"}
NPAGES = {"Book": 719, "Ref": 710, "RBE": 364}
CITE = re.compile(r"\(((?:[^()\n]|\([^()\n]*\))*?\b(?:Book|Ref|RBE)\s*p{1,2}\.[^()\n]*)\)")
HERE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\xa0", " ").replace("\ufffd", "'")
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
          .replace("–", "-").replace("—", "-").replace("­", ""))
    return s.lower()


def squash(s):
    return re.sub(r"\s+", "", norm(s))


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


ITEM = re.compile(r"(?:p{1,2}\.\s*)?(\d+)(?:\s*[-–]\s*(\d+))?")
SEP = re.compile(r"\s*(?:,|;|\se\s|\sand\s)\s*")  # "e" = Portuguese "and"


def parse_cite(body):
    """list of (abbreviation, [pages]). Accepts p.N, p.N-M, p.N, M, p.N, p.M and 'p.N and p.M' (also the Portuguese 'e')."""
    out = []
    for m in re.finditer(r"\b(Book|Ref|RBE)\s*p{1,2}\.\s*", body):
        pos = m.end()
        pages = []
        while True:
            mm = ITEM.match(body, pos)
            if not mm:
                break
            a = int(mm.group(1))
            b = int(mm.group(2) or a)
            pages.extend(range(a, b + 1))
            pos = mm.end()
            sep = SEP.match(body, pos)
            if not sep:
                break
            if re.match(r"(?:Book|Ref|RBE)\b", body[sep.end():]):
                break
            pos = sep.end()
        if pages:
            out.append((m.group(1), pages))
    return out


def terms_of(seg):
    ts = []
    for tok in re.findall(r"`([^`\n]+)`", seg):
        t = tok.strip()
        if "<" in t and ">" in t and re.search(r"<[a-z_ ]+>", t) and not re.search(r"[A-Z]", t):
            continue
        if "..." in t or "…" in t or len(t) < 3 or len(t) > 60:
            continue
        if t.startswith(("scripts/", "references/", "python", "skills/", "tests/")) or t.endswith((".md", ".py")) or ".py " in t:
            continue
        if re.fullmatch(r"[a-z]+(?:-[a-z]+)+", t):  # skill names and index topic names
            continue
        if re.fullmatch(r"[0-9.\-]+", t):
            continue
        ts.append(t)
    ts += re.findall(r"\bE0\d{3}\b", seg)
    return ts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(HERE))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--baseline", default=os.path.join(HERE, "audit-tokens-baseline.txt"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in SOURCES.items()}
    sq = {k: {p: squash(t) for p, t in d.items()} for k, d in pages.items()}
    wp = {k: {p: re.sub(r"\s+", " ", norm(t)) for p, t in d.items()} for k, d in pages.items()}
    base = set()
    if os.path.exists(a.baseline):
        for l in open(a.baseline, encoding="utf-8"):
            l = l.rstrip("\n")
            if l and not l.startswith("#"):
                base.add(l)
    files = []
    for dp, dn, fn in os.walk(a.pkg):
        dn[:] = [d for d in dn if d not in ("__pycache__", ".git")]
        for f in fn:
            if f.endswith(".md"):
                files.append(os.path.join(dp, f))
    files.sort()
    ncit = nterm = nnear = nfail = nrange = nline = nparaf = nbase = 0
    for path in files:
        rel = os.path.relpath(path, a.pkg).replace("\\", "/")
        if rel.endswith("INDEX.md") or rel.endswith("relatorio-de-fidelidade.md"):
            continue
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            pos = 0
            linepages = {}
            for m0 in CITE.finditer(line):
                for sg0, pg0 in parse_cite(m0.group(1)):
                    linepages.setdefault(sg0, set()).update(pg0)
            for m in CITE.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                cites = parse_cite(m.group(1))
                if not cites:
                    continue
                ncit += 1
                pl = {}
                for sig, pgs in cites:
                    for p in pgs:
                        if p < 1 or p > NPAGES[sig]:
                            nrange += 1
                            print("RANGE   %s:%d: %s p.%d outside 1..%d" % (rel, ln, sig, p, NPAGES[sig]))
                        pl.setdefault(sig, []).append(p)
                for tok in terms_of(seg):
                    st = squash(tok).strip(",.;")
                    if len(st) < 3:
                        continue
                    nterm += 1
                    if any(st in sq[s].get(p, "") for s, ps in pl.items() for p in ps):
                        continue
                    if any(st in sq[s].get(p, "") for s, ps in linepages.items() for p in ps):
                        nline += 1
                        continue
                    pieces = [w for w in re.findall(r"[A-Za-z_][A-Za-z_0-9]+", tok) if len(w) >= 2]
                    union = " ".join(wp[s].get(p, "") for s, ps in list(pl.items()) + list(linepages.items()) for p in ps)
                    if pieces and all(re.search(r"(?<![\w])" + re.escape(w.lower()) + r"(?![\w])", union) for w in pieces):
                        nparaf += 1
                        continue
                    near = any(st in sq[s].get(p + d, "") for s, ps in pl.items() for p in ps for d in (-1, 1))
                    if near:
                        nnear += 1
                        print("NEAR    %s:%d: `%s` outside %s but on a neighboring page" % (rel, ln, tok, m.group(1)))
                        continue
                    key = "%s|%s" % (rel, tok)
                    if key in base:
                        nbase += 1
                        if a.verbose:
                            print("BASELINE %s:%d: `%s`" % (rel, ln, tok))
                        continue
                    nfail += 1
                    cand = []
                    for sg, ps in pl.items():
                        for pp, tx in sq[sg].items():
                            if st in tx:
                                cand.append((min(abs(pp - q) for q in ps), sg, pp))
                    cand.sort()
                    where = (" | exists in " + ", ".join("%s p.%d" % (c[1], c[2]) for c in cand[:3])) if cand \
                        else " | does NOT exist in the cited sources"
                    print("FAIL    %s:%d: `%s` absent from %s%s" % (rel, ln, tok, m.group(1), where))
    print("Citations: %d; terms checked: %d; pages out of range: %d; only in another citation on the same line: %d; "
          "paraphrased notation: %d; NEAR: %d; in the reviewed baseline: %d; FAIL: %d"
          % (ncit, nterm, nrange, nline, nparaf, nnear, nbase, nfail))
    sys.exit(1 if (nfail or nrange or (a.strict and nnear)) else 0)


if __name__ == "__main__":
    main()

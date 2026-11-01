# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the rust-expert package citations against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src <DIR with the extracted .txt files> [--checks tests/citation-checks.json] [-v]

The extracted text has "=== PAGE N ===" markers (N = PDF page) and comes from PyMuPDF:
  Rust-The-Rust-Programming-Language.txt (Book, 719 p.), Rust-Reference.txt (Ref, 710 p.), Rust-by-Example.txt (RBE, 364 p.).

Checks:
  1. POSITIVE (citation-checks.json["positive"]): all 'terms' must appear in the union of the cited pages of the
     source 'src' (comparison ignoring case and whitespace/line breaks; prefix 're:' = regular expression).
  2. NEGATIVE (["negative"]): plausible claims that the sources do NOT carry; none of the 'terms' may appear on
     any page of the sources listed in 'src' (a list); here the search is by WHOLE WORD (without joining lines).
  3. SCRIPT DATA: each entry of scripts/rust_index.json ('termos' field x 'paginas') and each item of
     scripts/rust_checklists.json ('termos' field x 'fontes') must have its terms on the pages it cites.
No network; read-only. Exit 0 if everything passed, 1 otherwise.
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

FILES = {"Book": "Rust-The-Rust-Programming-Language.txt", "Ref": "Rust-Reference.txt", "RBE": "Rust-by-Example.txt"}
NPAGES = {"Book": 719, "Ref": 710, "RBE": 364}
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\ufffd", "'")
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
          .replace("–", "-").replace("—", "-").replace("­", ""))
    return s.lower()


def squash(s):
    return re.sub(r"\s+", "", norm(s))


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


class Src:
    def __init__(self, d):
        self.pages = {}
        self.sq = {}
        self.sp = {}
        for sig, fn in FILES.items():
            p = os.path.join(d, fn)
            if not os.path.exists(p):
                raise SystemExit("source text missing: %s (extract the PDF with PyMuPDF, marking '=== PAGE N ===')" % p)
            self.pages[sig] = load_pages(p)
            self.sq[sig] = {n: squash(t) for n, t in self.pages[sig].items()}
            self.sp[sig] = {n: re.sub(r"\s+", " ", norm(t)) for n, t in self.pages[sig].items()}

    def has_word(self, sig, page, term):
        """used for NEGATIVE checks: whole word, without joining lines (prevents 'this error' from matching 'thiserror')."""
        if term.startswith("re:"):
            return re.search(term[3:], self.sp[sig].get(page, ""), re.I) is not None
        return re.search(r"(?<![\w])" + re.escape(norm(term)) + r"(?![\w])", self.sp[sig].get(page, "")) is not None

    def has(self, sig, pages, term):
        if term.startswith("re:"):
            rx = re.compile(term[3:], re.I)
            return any(rx.search(self.sp[sig].get(p, "")) for p in pages)
        t = squash(term)
        return any(t in self.sq[sig].get(p, "") for p in pages)


def expand(spec):
    out = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(?:p\.)?\s*(\d+)(?:\s*-\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            out.extend(range(a, b + 1))
    return out


def parse_cites(strs):
    """['Book p.83-96', 'Ref p.3, 13-15'] -> {'Book': [...], 'Ref': [...]}"""
    res = {}
    for s in strs:
        m = re.match(r"(Book|Ref|RBE)\s+p\.\s*(.+)$", s.strip())
        if m:
            res.setdefault(m.group(1), []).extend(expand(m.group(2)))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="directory with the .txt files extracted from the PDFs")
    ap.add_argument("--checks", default=os.path.join(HERE, "citation-checks.json"))
    ap.add_argument("--no-data", action="store_true", help="do not check rust_index.json / rust_checklists.json")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    S = Src(a.src)
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    fails = []
    npos = nneg = ndata = 0

    for c in checks["positive"]:
        npos += 1
        sig = c["src"]
        bad_range = [p for p in c["pages"] if p < 1 or p > NPAGES[sig]]
        missing = [t for t in c["terms"] if not S.has(sig, c["pages"], t)]
        ok = not missing and not bad_range
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL"), c["id"], sig, "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("out of range: %s" % bad_range) if bad_range else "")))
        if not ok:
            fails.append(c["id"])

    for c in checks["negative"]:
        nneg += 1
        found = []
        for sig in c["src"]:
            for n in S.pages[sig]:
                for t in c["terms"]:
                    if S.has_word(sig, n, t):
                        found.append((sig, n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL"), c["id"], "(negative)", c["src"], "-", c["claim"],
                  ("" if ok else "| found in %s" % found[:4]))
        if not ok:
            fails.append(c["id"])

    if not a.no_data:
        idx_path = os.path.join(ROOT, "scripts", "rust_index.json")
        chk_path = os.path.join(ROOT, "scripts", "rust_checklists.json")
        if os.path.exists(idx_path):
            idx = json.load(open(idx_path, encoding="utf-8"))
            for e in idx["entradas"]:
                ndata += 1
                cites = parse_cites(e["paginas"])
                bad = [(s, p) for s, ps in cites.items() for p in ps if p < 1 or p > NPAGES[s]]
                miss = [t for t in e["termos"] if not any(S.has(s, ps, t) for s, ps in cites.items())]
                ok = not bad and not miss
                if a.verbose or not ok:
                    print(("OK   " if ok else "FAIL"), "index:" + e["id"], e["paginas"],
                          ("" if ok else "| missing: %s out of range: %s" % (miss, bad)))
                if not ok:
                    fails.append("index:" + e["id"])
            for e in idx["entradas"]:
                for o in e["onde"]:
                    fp = os.path.join(ROOT, o["arquivo"])
                    ok = os.path.exists(fp)
                    if ok:
                        want = re.sub(r"\s*\(.*\)\s*$", "", o["secao"].replace("`", "")).strip().lower()
                        heads = [re.sub(r"\s*\(.*\)\s*$", "", l.lstrip("# ").replace("`", "")).strip().lower()
                                 for l in open(fp, encoding="utf-8") if l.startswith("#")]
                        ok = any(h.startswith(want) for h in heads)
                    ndata += 1
                    if not ok:
                        print("FAIL index:%s section/file does not exist: %s | %s" % (e["id"], o["arquivo"], o["secao"]))
                        fails.append("index-onde:" + e["id"])
        if os.path.exists(chk_path):
            chk = json.load(open(chk_path, encoding="utf-8"))
            for area, v in chk["areas"].items():
                for it in v["itens"]:
                    if not it.get("termos"):
                        continue
                    ndata += 1
                    cites = parse_cites(it["fontes"])
                    bad = [(s, p) for s, ps in cites.items() for p in ps if p < 1 or p > NPAGES[s]]
                    miss = [t for t in it["termos"] if not any(S.has(s, ps, t) for s, ps in cites.items())]
                    ok = not bad and not miss
                    if a.verbose or not ok:
                        print(("OK   " if ok else "FAIL"), "checklist:" + it["id"], it["fontes"],
                              ("" if ok else "| missing: %s out of range: %s" % (miss, bad)))
                    if not ok:
                        fails.append("checklist:" + it["id"])

    print("Summary: %d positive, %d negative, %d script-data checks, %d failures"
          % (npos, nneg, ndata, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

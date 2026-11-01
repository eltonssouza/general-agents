# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of `backticked` TERMS against the cited page(s).

For each citation "(SIGLA p.N[-M][, ...][; SIGLA p.N])" in references/*.md (except INDEX), takes the backticked terms
of the preceding segment (since the previous citation on the same line) and checks that they appear on the cited page(s) of the
extracted text. Citations without an acronym inherit the last acronym mentioned in the text (including headings). Sections whose heading contains
"nao"/"NAO"/"extrapola" or, in English, "not"/"NOT"/"extrapolat" (lists of what the sources do NOT cover) are ignored, because they cite absent terms on purpose.
(The Portuguese heading alternates are kept for compatibility with the original Portuguese files.)
Terms with <, ..., folder prefixes, bracketed labels and very short ones are ignored. If the term is not on the
cited page but is on a neighboring page (+-1), it warns NEAR; otherwise, FAIL.

Usage: python -I tests/audit_tokens.py --src DIR_WITH_THE_TXT_FILES [--pkg ROOT] [--strict] [--verbose]
(DIR_WITH_THE_TXT_FILES: the same .txt files as verify_citations.py.) Exit 0 without FAIL (NEAR counts as a failure with --strict).
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

SOURCES = {
    "STRAUCH": "NoSQL-Databases-Strauch.txt",
    "REDIS": "NoSQL-Redis-The-Little-Redis-Book.txt",
    "MONGO-PAT": "NoSQL-MongoDB-Applied-Design-Patterns.txt",
    "MONGO-MAN-H": "NoSQL-MongoDB-Manual-Home.txt",
    "MONGO-MAN-I": "NoSQL-MongoDB-Manual-Introduction.txt",
    "CASS": "NoSQL-Cassandra-Overview.txt",
    "COUCH": "NoSQL-CouchDB-Introduction.txt",
    "ELAST": "NoSQL-Elasticsearch-Guide-Index.txt",
    "NEO4J-GDB": "NoSQL-Neo4j-Graph-Databases-2e.txt",
}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"\s+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): squash(norm(parts[i + 1])) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


SIGLA_RE = re.compile(r"\b(" + "|".join(sorted(SOURCES, key=len, reverse=True)) + r")\b")
CITE = re.compile(r"\(([^()]*?\bp\.\d[^()]*)\)")
PART = re.compile(r"^(?:([A-Z][A-Z0-9-]+)\s+)?p\.\s*(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    pages = {}
    for sig, fn in SOURCES.items():
        path = os.path.join(a.src, fn)
        if not os.path.exists(path):
            print("ERROR: source text missing: %s" % path, file=sys.stderr)
            return 2
        pages[sig] = load_pages(path)

    refs = os.path.join(a.pkg, "references")
    checked = near = fail = skipped_sections = cites = 0
    for fn in sorted(os.listdir(refs)):
        if not fn.endswith(".md") or fn.startswith("INDEX"):
            continue
        last_sig = None
        skip = False
        for ln, line in enumerate(open(os.path.join(refs, fn), encoding="utf-8"), 1):
            if line.startswith("#"):
                skip = bool(re.search(r"n[ãa]o|extrapola|\bnot\b", line, re.IGNORECASE))
                if skip:
                    skipped_sections += 1
            pos = 0
            events = []
            for sm in SIGLA_RE.finditer(line):
                events.append((sm.start(), "sig", sm))
            for cm in CITE.finditer(line):
                events.append((cm.start(), "cite", cm))
            events.sort(key=lambda e: e[0])
            inside = [(e[2].start(), e[2].end()) for e in events if e[1] == "cite"]
            for _, kind, m in events:
                if kind == "sig":
                    if not any(a <= m.start() < b for a, b in inside):
                        last_sig = m.group(1)
                    continue
                seg = line[pos:m.start()]
                pos = m.end()
                targets = []  # (sig, [pages])
                for part in m.group(1).split(";"):
                    pm = PART.match(part.strip())
                    if not pm:
                        continue
                    sig = pm.group(1) or last_sig
                    if pm.group(1):
                        last_sig = pm.group(1)
                    if sig in pages:
                        targets.append((sig, expand(pm.group(2))))
                if not targets:
                    continue
                cites += 1
                if skip:
                    continue
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if (t0.startswith("[") or "<" in t0 or "..." in t0 or "…" in t0 or len(t0) < 3
                            or t0.startswith(("scripts/", "references/", "python", "tests/"))
                            or t0.endswith((".md", ".py", ".json", ".txt")) or re.fullmatch(r"[0-9.]+", t0)):
                        continue
                    cand = [c.strip().rstrip(",.;") for c in t0.split("|")]
                    for c in cand:
                        c = re.sub(r"\(\)$", "", c)
                        if len(c) < 3:
                            continue
                        st = squash(norm(c))
                        checked += 1
                        ok = any(st in pages[s].get(p, "") for s, pl in targets for p in pl)
                        if ok:
                            continue
                        nb = set()
                        for s, pl in targets:
                            for p in pl:
                                for q in (p - 1, p + 1):
                                    if q not in pl and st in pages[s].get(q, ""):
                                        nb.add((s, q))
                        if nb:
                            near += 1
                            print("NEAR %s:%d: `%s` is not in %s but is in %s" % (
                                fn, ln, c, m.group(1), sorted(nb)[:2]))
                        else:
                            fail += 1
                            print("FAIL   %s:%d: `%s` not found in %s" % (fn, ln, c, m.group(1)))
    print("Citations analyzed: %d; sections ignored (not/extrapolation): %d; terms checked: %d; near: %d; failures: %d"
          % (cites, skipped_sections, checked, near, fail))
    return 1 if (fail or (a.strict and near)) else 0


if __name__ == "__main__":
    sys.exit(main())

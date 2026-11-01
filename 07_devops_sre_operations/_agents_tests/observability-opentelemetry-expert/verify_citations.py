# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package citations against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/devops [--pkg PACKAGE_PATH]

1) Range: every citation (DOW|OTW) p.N[-M][, ...] must exist (1-7 in each work).
2) Content: each "checks" item requires the cited page to contain the substrings.
3) Negatives: "negative" items require the terms to be ABSENT (from the whole work or the page),
   proving the package cannot attribute to the sources what they do not say.
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FILES = {"DOW": "Distributed-Observability-Whitepaper.txt", "OTW": "OpenTelemetry-Whitepaper.txt"}
MAXP = {"DOW": 7, "OTW": 7}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = set()
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.update(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in FILES.items()}
    for k, p in pages.items():
        if len(p) != MAXP[k]:
            print(f"WARNING: {k} has {len(p)} pages in the text (expected {MAXP[k]})")
    fails = 0

    cite_re = re.compile(r"\b(DOW|OTW)\s+p\.\s*(\d[\d\s,\-–]*)")
    # citations like "(DOW p.4; OTW p.4)" and "p.5, 6" are covered by the regex; "p.4, 6; OTW" too.
    total, per = 0, {k: set() for k in FILES}
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")) or fn == "verify_citations.py":
                continue
            fp = os.path.join(root, fn)
            if fn == "citation-checks.json":
                continue
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(2)):
                    total += 1
                    per[m.group(1)].add(p)
                    if p < 1 or p > MAXP[m.group(1)]:
                        fails += 1
                        print(f"FAIL range: {m.group(1)} p.{p} out of range in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} page numbers checked; distinct: " + ", ".join(f"{k}={sorted(v)}" for k, v in per.items()))

    data = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))
    ok = 0
    for c in data["checks"]:
        m = re.fullmatch(r"(DOW|OTW) p\.(\d+)", c["cite"])
        body = norm(pages[m.group(1)].get(int(m.group(2)), ""))
        miss = [s for s in c["contains"] if norm(s) not in body]
        if miss:
            fails += 1
            print(f"FAIL content: {c['cite']} ({c['claim']}) does not contain {miss}")
        else:
            ok += 1
    print(f"Content: {ok}/{len(data['checks'])} positive checks OK")

    nok = 0
    for n in data["negative"]:
        if "src" in n:
            srcs = list(FILES) if n["src"] == "ALL" else [n["src"]]
            bodies = {s: norm(" ".join(pages[s].values())) for s in srcs}
            where = "+".join(srcs)
        else:
            m = re.fullmatch(r"(DOW|OTW) p\.(\d+)", n["cite"])
            bodies = {n["cite"]: norm(pages[m.group(1)].get(int(m.group(2)), ""))}
            where = n["cite"]
        present = [t for t in n["absent"] for b in bodies.values() if norm(t) in b]
        if present:
            fails += 1
            print(f"FAIL negative: {where} ({n['claim']}) CONTAINS {sorted(set(present))}")
        else:
            nok += 1
    print(f"Negatives: {nok}/{len(data['negative'])} OK (terms absent as expected)")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

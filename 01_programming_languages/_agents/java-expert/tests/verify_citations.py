# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the java-expert package citations against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --text-dir DIR [--checks tests/citation-checks.json] [--pkg RAIZ] [-v]

DIR contains (markers "=== PAGE N ===", N = PDF page):
  Java-Think-Java-6e.txt, Java-Advanced-Tutorial.txt, Java-JVM-Troubleshooting-Guide-Oracle.txt,
  Java-11-JDK-Release-Notes-OpenJDK.txt, Java-17-..., Java-21-..., Java-22-..., Java-26-...
Generate the .txt files with PyMuPDF (page.get_text() per page) or an equivalent tool; see the README, verification section.

Four checks:
  1. RANGE: every citation "(Think|Adv|JVM p.N[-M], ...)" in the package falls within the PDF pages.
  2. POSITIVES: for each item of citation-checks.json["positive"], all the 'terms' appear on the cited 'pages'
     (case-insensitive, spaces and hyphens normalized; each term may be on any of the pages).
  3. NEGATIVES: none of the item's 'terms' appears on ANY page of the source 'src' (Think, Adv, JVM, RN, RN11...RN26).
     Terms with the prefix "re:" are regex (case-insensitive); "reCS:" are case-sensitive regex.
  4. INDEX: the anchors (term + page) of scripts/java_index.json appear on the indicated page.
Read-only; no network. Exit code 0 if everything passed, 1 otherwise.
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

FILES = {
    "Think": "Java-Think-Java-6e.txt",
    "Adv": "Java-Advanced-Tutorial.txt",
    "JVM": "Java-JVM-Troubleshooting-Guide-Oracle.txt",
    "RN11": "Java-11-JDK-Release-Notes-OpenJDK.txt",
    "RN17": "Java-17-JDK-Release-Notes-OpenJDK.txt",
    "RN21": "Java-21-JDK-Release-Notes-OpenJDK.txt",
    "RN22": "Java-22-JDK-Release-Notes-OpenJDK.txt",
    "RN26": "Java-26-JDK-Release-Notes-OpenJDK.txt",
}
CIT = re.compile(r"\b(Think|Adv|JVM)\s+p\.\s?(\d+)(?:\s?[–-]\s?(\d+))?"
                 r"((?:\s*(?:,|;|e|and)\s*(?:p\.\s?)?\d+(?:\s?[–-]\s?\d+)?(?!\s*(?:Think|Adv|JVM)))*)")


def clean(s):
    s = unicodedata.normalize("NFKC", s).replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s)


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): clean(parts[i + 1]) for i in range(1, len(parts), 2)}


def squash(s):
    return re.sub(r"[\s\-_]+", "", clean(s).lower())


def has(text, term):
    if term.startswith("reCS:"):
        return re.search(term[5:], text) is not None
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return squash(term) in squash(text)


def pages_of(m):
    rs = [(int(m.group(2)), int(m.group(3) or m.group(2)))]
    for x in re.finditer(r"(\d+)(?:\s?[–-]\s?(\d+))?", m.group(4) or ""):
        rs.append((int(x.group(1)), int(x.group(2) or x.group(1))))
    out = []
    for a, b in rs:
        out += range(a, b + 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-dir", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("--pkg", default=os.path.dirname(here))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    pages = {k: load_pages(os.path.join(a.text_dir, v)) for k, v in FILES.items()}
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    fails = []

    # 1. page range of the package citations
    ncit = 0
    out_of_range = []
    for root, dirs, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")) or fn == "citation-checks.json":
                continue
            path = os.path.join(root, fn)
            try:
                text = open(path, encoding="utf-8").read()
            except UnicodeDecodeError:
                print("FAIL non-UTF-8 encoding:", path)
                fails.append("UTF8:" + fn)
                continue
            for ln, line in enumerate(text.split("\n"), 1):
                for m in CIT.finditer(line):
                    ncit += 1
                    bad = [p for p in pages_of(m) if p not in pages[m.group(1)]]
                    if bad:
                        out_of_range.append((path, ln, m.group(0), bad))
    for path, ln, txt, bad in out_of_range:
        print("FAIL range: %s:%d '%s' nonexistent pages %s" % (os.path.relpath(path, a.pkg), ln, txt, bad))
        fails.append("RANGE:%s:%d" % (os.path.basename(path), ln))

    # 2. positives
    for c in checks["positive"]:
        blob = " ".join(pages[c["src"]].get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL"), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s" % missing))
        if not ok:
            fails.append(c["id"])

    # 3. negatives
    for c in checks["negative"]:
        srcs = [c["src"]] if c["src"] != "RN" else [k for k in FILES if k.startswith("RN")]
        found = []
        for s in srcs:
            for n, txt in pages[s].items():
                for t in c["terms"]:
                    if has(txt, t):
                        found.append((s, n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL"), c["id"], "(negative)", c["src"], "-", c["claim"],
                  ("" if ok else "| found in %s" % found[:4]))
        if not ok:
            fails.append(c["id"])

    # 4. topic index
    idx_path = os.path.join(a.pkg, "scripts", "java_index.json")
    nanch = 0
    if os.path.exists(idx_path):
        with open(idx_path, encoding="utf-8") as f:
            idx = json.load(f)
        for e in idx["entries"]:
            for an in e["anchors"]:
                nanch += 1
                ok = has(pages[an["sig"]].get(an["page"], ""), an["term"])
                if a.verbose or not ok:
                    print(("OK   " if ok else "FAIL"), "index", e["id"], an["sig"], "p.%d" % an["page"], an["term"])
                if not ok:
                    fails.append("IDX:" + e["id"])

    print("Summary: %d citations with range checked (%d outside the PDF); %d positives; %d negatives; %d index anchors; %d failures"
          % (ncit, len(out_of_range), len(checks["positive"]), len(checks["negative"]), nanch, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails[:40]))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

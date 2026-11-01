# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the python-expert package citations against the text extracted from the PDFs.

Usage (from the package root):
  python -I tests/verify_citations.py --src FOLDER_WITH_THE_TXT_FILES [--pkg PACKAGE_ROOT] [--checks file.json ...]

FOLDER_WITH_THE_TXT_FILES: contains Python-3.14-Tutorial.txt, Python-3.14-Language-Reference.txt,
Python-Notes-for-Professionals.txt and Python-3.14-Standard-Library.txt, extracted from the PDFs with PyMuPDF
(page.get_text()) and with "=== PAGE N ===" markers (N = PDF page, starting at 1). The PDFs are NOT in the package;
see README.md, section "Verifiers".

Page convention: N = PDF page. Printed page = N - 6 (Tut), N - 8 (Ref), N - 25 (Notes), N - 26 (Lib).

Layers:
 1) Range: every citation "(Tut|Ref|Notes|Lib p.N[-M][, p.K ...])" in the package .md/.py/.json (outside tests/) must
    be in 1..<number of pages of the source>. It also checks the number of pages of each text and the page convention
    (numeric footer/header) by sampling all the pages.
 2) Positive: item {"cite":"Ref p.26","contains":[...]} -> the cited page(s) contain ALL the substrings
    (lowercase, collapsed whitespace; also compared without spaces).
 3) Negative: item {"cite":"Tut p.1-167","absent":[...]} -> NONE of the terms appears (whole word) on the cited
    pages (plausible claims that the source does NOT carry).
 4) Version marks: every table row of references/versoes-e-datado.md with "Added|Changed|Deprecated|Removed X.Y"
    and source Ref/Tut p.N requires the page to carry the mark (or, if labeled, the page cannot contradict it).
 5) Stdlib index: every module/section of skills/python-stdlib-lookup/scripts/stdlib_index.json must have its title on
    the indicated PDF page (known, registered exceptions: 3, tolerance of +-1 page).
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audit_tokens as A  # noqa: E402  (reaproveita norm/squash/load_pages/parse_citations)

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

OFFSET = {"Tut": 6, "Ref": 8, "Notes": 25, "Lib": 26}   # printed = PDF - OFFSET
# known exceptions of the stdlib index (bookmark title != page text), registered in the audit
STDLIB_KNOWN = {("sec", "Supported XPath syntax"),
                ("sec", "ZERO-CLAUSE BSD LICENSE FOR CODE IN THE PYTHON DOCUMENTATION")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(HERE))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()

    raw, npg, spg = {}, {}, {}
    fails = 0
    for sg, (fn, n) in A.SOURCES.items():
        raw[sg] = A.load_pages(os.path.join(a.src, fn))
        npg[sg] = {k: A.norm(v) for k, v in raw[sg].items()}
        spg[sg] = {k: A.squash(v) for k, v in npg[sg].items()}
        if len(raw[sg]) != n:
            fails += 1
            print(f"FAIL: {fn} has {len(raw[sg])} pages (expected {n})")

    # 1) page range of the citations
    total = 0
    for root, dirs, files in os.walk(a.pkg):
        dirs[:] = [d for d in dirs if d not in ("tests", "__pycache__", ".git")]
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn == "stdlib_index.json":
                continue
            fp = os.path.join(root, fn)
            for ln, line in enumerate(open(fp, encoding="utf-8", errors="replace"), 1):
                for (_s, _e, sg, pages) in A.parse_citations(line):
                    for p in pages:
                        total += 1
                        if p < 1 or p > A.SOURCES[sg][1]:
                            fails += 1
                            print(f"FAIL range: {sg} p.{p} outside 1-{A.SOURCES[sg][1]} in {os.path.relpath(fp, a.pkg)}:{ln}")
    print(f"Range: {total} cited pages checked against the size of each source.")

    # page convention (printed = PDF - OFFSET) by footer/header
    for sg, mode in (("Tut", "foot"), ("Ref", "foot"), ("Notes", "head"), ("Lib", "foot")):
        ok = tot = 0
        for p, t in raw[sg].items():
            ls = [l.strip() for l in t.split("\n") if l.strip()]
            cand = [l for l in (ls[1:4] if mode == "head" else ls[-4:]) if re.fullmatch(r"\d{1,4}", l)]
            if cand:
                tot += 1
                ok += (p - int(cand[0]) == OFFSET[sg])
        pct = 100.0 * ok / max(tot, 1)
        flag = "" if pct >= 95 else "  <-- FAIL"
        if pct < 95:
            fails += 1
        print(f"Convention {sg}: printed = PDF - {OFFSET[sg]} in {ok}/{tot} numbered pages ({pct:.1f}%){flag}")

    # 2) and 3) positive and negative
    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cites = A.parse_citations(it["cite"] if re.search(r"\bp{1,2}\.", it["cite"]) else "")
            if not cites:
                fails += 1
                print(f"FAIL invalid cite: {it['cite']}")
                continue
            sg = cites[0][2]
            plist = cites[0][3]
            if any(p not in npg[sg] for p in plist):
                fails += 1
                print(f"FAIL cite out of range: {it['cite']}")
                continue
            blob = " ".join(npg[sg][p] for p in plist)
            sblob = "".join(spg[sg][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    nt = A.norm(t)
                    if nt not in blob and A.squash(nt) not in sblob:
                        fails += 1
                        print(f"FAIL positive: {it['cite']} does not contain '{t}' -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    nt = A.norm(t)
                    if re.search(r"(?<![a-z0-9_])" + re.escape(nt) + r"(?![a-z0-9_])", blob) or \
                            (len(A.squash(nt)) >= 6 and A.squash(nt) in sblob):
                        fails += 1
                        print(f"FAIL negative: {it['cite']} CONTAINS '{t}' -- {it.get('claim', '')}")
    print(f"Curated checks: {pos} positive, {neg} negative.")

    # 4) version marks of the master table
    vf = os.path.join(a.pkg, "references", "versoes-e-datado.md")
    ok = bad = 0
    if os.path.exists(vf):
        for ln, l in enumerate(open(vf, encoding="utf-8"), 1):
            if not l.startswith("|"):
                continue
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            cites = A.parse_citations(cells[-1])
            marks = re.findall(r"(Added|Changed|Deprecated|Removed)\s+(?:in\s+)?(\d\.\d+)", cells[1])
            for kind, ver in marks:
                found = False
                for (_s, _e, sg, pages) in cites:
                    if sg not in ("Ref", "Tut"):
                        continue
                    blob = " ".join(npg[sg].get(p, "") for p in pages)
                    # the page carries the version in one of the formats "Added/Changed/Deprecated since version X.Y"
                    if re.search(r"(?:version|python) " + re.escape(ver) + r"\b", blob):
                        found = True
                if found:
                    ok += 1
                else:
                    bad += 1
                    fails += 1
                    print(f"FAIL mark: versoes-e-datado.md:{ln} {kind} {ver} does not appear on the cited pages ({cells[0][:40]})")
    print(f"Version marks of the master table: {ok} confirmed, {bad} failures.")

    # 5) stdlib index
    jf = os.path.join(a.pkg, "skills", "python-stdlib-lookup", "scripts", "stdlib_index.json")
    if os.path.exists(jf):
        j = json.load(open(jf, encoding="utf-8"))
        mb = ms = sb = ss = 0
        for ch in j:
            for m in ch["modules"]:
                mb += 1
                t = re.split(r"\s[–—-]\s", m["title"])[0].strip()
                if A.squash(A.norm(t)) not in spg["Lib"][m["page"]] and (("mod", t) not in STDLIB_KNOWN):
                    ms += 1
                    fails += 1
                    print(f"FAIL stdlib module: '{t}' is not on p.{m['page']}")
                for s in m["sections"]:
                    sb += 1
                    tt = A.squash(A.norm(re.sub(r"^[\d.]+\s*", "", s["t"])))
                    if tt not in spg["Lib"][s["p"]] and (("sec", s["t"]) not in STDLIB_KNOWN):
                        ss += 1
                        fails += 1
                        print(f"FAIL stdlib section: '{s['t']}' is not on p.{s['p']}")
        print(f"Stdlib index: {mb} modules/topics and {sb} sections checked; failures: {ms + ss} (registered exceptions: {len(STDLIB_KNOWN)}).")
    # 6) presence index in the 3.10-3.14 Tutorials (only if the .txt files of the earlier versions are in --src)
    tf = os.path.join(a.pkg, "skills", "python-version-features", "scripts", "tutorial_index.json")
    if os.path.exists(tf):
        td = json.load(open(tf, encoding="utf-8"))
        miss = [v for v in td["versions"] if not os.path.exists(os.path.join(a.src, f"Python-{v}-Tutorial.txt"))]
        if miss:
            print(f"Tutorials index: SKIPPED (missing in --src: {', '.join('Python-%s-Tutorial.txt' % v for v in miss)})")
        else:
            tp = {v: A.load_pages(os.path.join(a.src, f"Python-{v}-Tutorial.txt")) for v in td["versions"]}
            n = bad = 0
            for v, info in td["versions"].items():
                if len(tp[v]) != info["pdf_pages"]:
                    fails += 1
                    print(f"FAIL tutorial {v}: {len(tp[v])} pages (index says {info['pdf_pages']})")
            for term in td["terms"]:
                rx = re.compile(term["pattern"], re.I)
                for v, zones in term["pages"].items():
                    for zone, pl in zones.items():
                        lo, hi = td["versions"][v]["zonas"][zone]
                        for p in pl:
                            n += 1
                            if not (lo <= p <= hi) or not rx.search(re.sub(r"\s+", " ", tp[v][p])):
                                bad += 1
                                fails += 1
                                print(f"FAIL tutorial {v} p.{p}: '{term['id']}' ({zone}) does not match")
                    # a term absent from the index must really be absent from the body/glossary/license (no page outside the table of contents)
                    allp = [p for p, tx in tp[v].items() if p > 8 and rx.search(re.sub(r"\s+", " ", tx))]
                    listed = {p for pl in zones.values() for p in pl}
                    if len(listed) == 0 and allp:
                        bad += 1
                        fails += 1
                        print(f"FAIL tutorial {v}: '{term['id']}' marked absent but appears on p.{allp[:5]}")
            print(f"Tutorials index 3.10-3.14: {len(td['terms'])} terms, {n} pages checked; failures: {bad}.")
    print(f"Total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

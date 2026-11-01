# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package's citations against the text extracted from the PDFs (read-only, no network).

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/security [--pkg PACKAGE_ROOT] [--checks file.json ...]

Sources expected in --src (text per page with the marker "=== PAGE N ===", N = PDF page):
  OWASP-ASVS-4.0.3.txt            (71 pages; PDF page = footer number)
  OWASP-Code-Review-Guide-v2.txt  (220 pages; printed = PDF - 1)

What it verifies:
 1) RANGE: every citation "ASVS p.N[-M][, ...]" in 1..71 and "OCRG p.N..." in 1..220 (in the package's .md/.py/.json).
 2) ASVS IDs: every "V<x>.<y>.<z>" / "v4.0.3-x.y.z" cited exists in scripts/asvs_requirements.json; if the SAME line carries "ASVS p.N",
    the requirement's page must be among the pages cited on the line.
 3) POSITIVES (citation-checks.json, "contains"): the cited page(s) contain ALL the substrings (normalized:
    lowercase, collapsed whitespace, straight quotes, line-break hyphenation removed OR preserved).
 4) NEGATIVES ("absent"): NONE of the expressions appears (whole word) in the cited page(s) - plausible claims the book does NOT make.
 5) DATA: asvs_requirements.json x text (the first words of each requirement are on the recorded page); ocrg_checklist.json x text;
    ocrg_index.json (pages in range); gaps.json (terms really absent); linter rules (pages in range + terms on the pages).
Exit 0 if everything passes; 1 otherwise.
"""
import argparse
import importlib.util
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

SRC = {"ASVS": ("OWASP-ASVS-4.0.3.txt", 71), "OCRG": ("OWASP-Code-Review-Guide-v2.txt", 220)}


def norm_variants(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    a = re.sub(r"-\s*\n\s*", "", s)      # remove line-break hyphen
    b = re.sub(r"-\s*\n\s*", "-", s)     # preserve legitimate hyphen
    return [re.sub(r"\s*=\s*", "=", re.sub(r"\s+", " ", x.lower()).strip()) for x in (a, b, s)]


def norm_term(t):
    return norm_variants(t)[2]


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*(?:,|;|\be\b|\band\b)\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.extend(range(a, b + 1))
    return pages


CITE_RE = re.compile(r"\b(ASVS|OCRG)\s+p{1,2}\.\s*(\d+(?:\s*[-–]\s*\d+)?(?:\s*(?:,|\be\b|\band\b)\s*\d+(?:\s*[-–]\s*\d+)?)*)")
ID_RE = re.compile(r"(?<![\w.])(?:v4\.0\.3-)?V?(\d{1,2})\.(\d{1,2})\.(\d{1,2})(?![\w.]*\d)", re.I)
VID_RE = re.compile(r"(?<![\w.])(?:v4\.0\.3-)(\d{1,2}\.\d{1,2}\.\d{1,2})|(?<![\w.])V(\d{1,2}\.\d{1,2}\.\d{1,2})(?![\w.])")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()

    pages, blobs = {}, {}
    for sig, (fn, maxp) in SRC.items():
        pg = load_pages(os.path.join(a.src, fn))
        pages[sig] = pg
        blobs[sig] = {k: norm_variants(v) for k, v in pg.items()}
        if len(pg) != maxp:
            print("WARNING: %s has %d pages (expected %d)" % (sig, len(pg), maxp))
    fails = 0

    # ---- package data
    req = json.load(open(os.path.join(a.pkg, "scripts", "asvs_requirements.json"), "r", encoding="utf-8"))
    byid = {r["id"]: r for r in req["requirements"]}

    # ---- 1) range and 2) IDs
    total = 0
    id_total = 0
    for root, _, files in os.walk(a.pkg):
        if "__pycache__" in root:
            continue
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "asvs_requirements.json", "ocrg_checklist.json", "citation-checks.json", "casos.json"):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, a.pkg)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for ln_no, line in enumerate(text.splitlines(), 1):
                cited_asvs = set()
                for m in CITE_RE.finditer(line):
                    sig = m.group(1)
                    for p in expand(m.group(2)):
                        total += 1
                        if not 1 <= p <= SRC[sig][1]:
                            fails += 1
                            print("FAILURE range: %s p.%d outside 1-%d in %s:%d" % (sig, p, SRC[sig][1], rel, ln_no))
                        elif sig == "ASVS":
                            cited_asvs.add(p)
                if fn.endswith(".md"):
                    for m in VID_RE.finditer(line):
                        rid = m.group(1) or m.group(2)
                        if rid.split(".")[0] and int(rid.split(".")[0]) > 14:
                            continue
                        id_total += 1
                        if rid not in byid:
                            fails += 1
                            print("FAILURE id: V%s does not exist in ASVS 4.0.3 (%s:%d)" % (rid, rel, ln_no))
                        elif cited_asvs and byid[rid]["page"] not in cited_asvs:
                            fails += 1
                            print("FAILURE id page: V%s is on ASVS p.%d, line cites %s (%s:%d)" % (rid, byid[rid]["page"], sorted(cited_asvs), rel, ln_no))
    print("Range: %d pages cited; ASVS IDs checked: %d." % (total, id_total))

    # ---- 3) and 4) checks
    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.match(r"(ASVS|OCRG)\s+p{1,2}\.\s*(.+)$", cite.strip())
            if not m:
                fails += 1
                print("FAILURE invalid cite: %s" % cite)
                continue
            sig, plist = m.group(1), expand(m.group(2))
            if not plist or any(p not in blobs[sig] for p in plist):
                fails += 1
                print("FAILURE cite outside the collection: %s" % cite)
                continue
            variants = [" ".join(blobs[sig][p][i] for p in plist) for i in range(3)]
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    nt = norm_term(t)
                    if not any(nt in v for v in variants):
                        fails += 1
                        print("FAILURE positive: %s does not contain '%s' -- %s" % (cite, t, it.get("claim", "")))
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    nt = re.escape(norm_term(t))
                    if any(re.search(r"(?<![a-z0-9])" + nt + r"(?![a-z0-9])", v) for v in variants):
                        fails += 1
                        print("FAILURE negative: %s CONTAINS '%s' -- %s" % (cite, t, it.get("claim", "")))
    print("Checks: %d positive, %d negative." % (pos, neg))

    # ---- 5a) asvs_requirements.json x text
    bad = 0
    for r in req["requirements"]:
        if r["deleted"]:
            continue
        sig = "ASVS"
        words = re.sub(r"\s+", " ", r["text"]).split(" ")[:8]
        probe = norm_term(" ".join(words))
        pg = r["page"]
        if not any(probe in v for v in blobs[sig].get(pg, ["", "", ""])):
            bad += 1
            print("FAILURE ASVS data: V%s p.%d does not contain the start of the text '%s'" % (r["id"], pg, probe))
    fails += bad
    print("ASVS data: %d requirements checked against the recorded page (%d failures)." % (sum(1 for r in req["requirements"] if not r["deleted"]), bad))

    # ---- 5b) ocrg_checklist.json
    chk = json.load(open(os.path.join(a.pkg, "scripts", "ocrg_checklist.json"), "r", encoding="utf-8"))
    bad = 0
    for it in chk["items"]:
        probe = norm_term(" ".join(re.sub(r"\s+", " ", it["text"]).split(" ")[:6]).replace("autho-rization", "authorization"))
        vs = blobs["OCRG"].get(it["page"], ["", "", ""])
        if not any(probe in v for v in vs):
            bad += 1
            print("FAILURE OCRG checklist: %s p.%d does not contain '%s'" % (it["id"], it["page"], probe))
    fails += bad
    print("OCRG checklist: %d rows checked (%d failures); expected total 78: %s." % (len(chk["items"]), bad, "OK" if len(chk["items"]) == 78 else "FAILURE"))
    if len(chk["items"]) != 78:
        fails += 1

    # ---- 5c) ocrg_index.json
    idx = json.load(open(os.path.join(a.pkg, "scripts", "ocrg_index.json"), "r", encoding="utf-8"))
    bad = 0
    for t in idx["topics"]:
        for p in t["pages"]:
            if not 1 <= p <= 220:
                bad += 1
                print("FAILURE OCRG index: topic %s page %d out of range" % (t["id"], p))
        if not os.path.exists(os.path.join(a.pkg, "references", t["ref"])):
            bad += 1
            print("FAILURE OCRG index: file references/%s does not exist (%s)" % (t["ref"], t["id"]))
        for ai in t["asvs"]:
            if ai not in byid:
                bad += 1
                print("FAILURE OCRG index: ASVS %s does not exist (%s)" % (ai, t["id"]))
    fails += bad
    print("OCRG index: %d topics (%d failures)." % (len(idx["topics"]), bad))

    # ---- 5d) gaps.json
    gaps = json.load(open(os.path.join(a.pkg, "scripts", "gaps.json"), "r", encoding="utf-8"))
    bad = 0
    for key, targets in (("ocrg", ("OCRG",)), ("asvs", ("ASVS",)), ("ambos", ("OCRG", "ASVS"))):
        for term in gaps[key]:
            nt = re.escape(norm_term(term))
            for sig in targets:
                allv = " ".join(" ".join(v[i] for v in blobs[sig].values()) for i in range(3))
                if re.search(r"(?<![a-z0-9])" + nt + r"(?![a-z0-9])", allv):
                    bad += 1
                    print("FAILURE gap: '%s' APPEARS in %s (list %s)" % (term, sig, key))
    fails += bad
    print("Gaps: %d terms verified absent (%d failures)." % (sum(len(gaps[k]) for k in ("ocrg", "asvs", "ambos")), bad))

    # ---- 5e) linter rules
    spec = importlib.util.spec_from_file_location("ocrg_lint_mod", os.path.join(a.pkg, "scripts", "ocrg_lint.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rule_terms = {}
    for f in files:
        rule_terms.update(json.load(open(f, "r", encoding="utf-8")).get("rule_terms", {}))
    bad = 0
    for r in mod.RULES:
        if r["origin"] == "[extrapolation]":
            if r["pages"]:
                bad += 1
                print("FAILURE rule %s: extrapolation must not have an OCRG page" % r["id"])
            continue
        if not r["pages"]:
            bad += 1
            print("FAILURE rule %s: no pages" % r["id"])
            continue
        if r["id"] not in rule_terms:
            bad += 1
            print("FAILURE rule %s: no 'rule_terms' in citation-checks.json" % r["id"])
            continue
        v = [" ".join(blobs["OCRG"][p][i] for p in r["pages"] if p in blobs["OCRG"]) for i in range(3)]
        for t in rule_terms[r["id"]]:
            nt = norm_term(t)
            if not any(nt in x for x in v):
                bad += 1
                print("FAILURE rule %s: term '%s' absent from pages %s" % (r["id"], t, r["pages"]))
    fails += bad
    print("Linter rules: %d rules checked against the OCRG pages (%d failures)." % (len(mod.RULES), bad))

    # ---- 6) backtick tokens on lines with a citation: must exist on the cited pages (broad coverage of the claims)
    exempt = set()
    for f in files:
        exempt.update(json.load(open(f, "r", encoding="utf-8")).get("token_exempt", []))
    # negation markers: Portuguese (legacy references text) and English
    neg_words = re.compile(
        r"ausent|n[aã]o cita|n[aã]o aparece|n[aã]o traz|n[aã]o cobre|n[aã]o trata|n[aã]o usa o termo|sem l1|n[aã]o menciona|n[aã]o fala|"
        r"sem cobertura|extrapola|n[aã]o est[aã]o|n[aã]o d[aá]|n[aã]o existe|fronteira|n[aã]o inclui|n[aã]o tem|"
        r"absent|does not (?:cite|appear|bring|cover|address|deal|use the term|mention|say|give|exist|include|have)|"
        r"(?:is|are) not (?:in|cited|covered|mentioned)|no l1|not covered|boundary|no specialist", re.I)
    tok_total = tok_bad = 0
    for root, _, fnames in os.walk(os.path.join(a.pkg, "references")):
        for fn in fnames:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, a.pkg)
            for ln_no, line in enumerate(open(fp, "r", encoding="utf-8").read().splitlines(), 1):
                cites = [(m.group(1), expand(m.group(2))) for m in CITE_RE.finditer(line)]
                if not cites or neg_words.search(line):
                    continue
                union = {}
                for sig, pl in cites:
                    for pg in pl:
                        if pg in blobs.get(sig, {}):
                            union.setdefault(sig, set()).add(pg)
                for tok in re.findall(r"`([^`]+)`", line):
                    t = tok.strip()
                    if (len(t) < 3 or t in exempt or t.startswith(("[", "python", "scripts/", "references/", "--", "tests/", "v4.0.3", "http"))
                            or re.fullmatch(r"V?\d+(\.\d+)+[A-Za-z.]*", t) or re.fullmatch(r"[LRo/ ,+-]+", t) or re.fullmatch(r"[A-Z][A-Z0-9]*(-[A-Z0-9*]+)+", t) or "ocrg_" in t or "asvs_" in t):
                        continue
                    tok_total += 1
                    nt = norm_term(t)
                    ok = False
                    for sig, pgs in union.items():
                        for i in range(3):
                            if nt in " ".join(blobs[sig][pg][i] for pg in pgs):
                                ok = True
                    if not ok:
                        tok_bad += 1
                        print("FAILURE token: `%s` does not appear on the cited pages (%s:%d)" % (t, rel, ln_no))
    fails += tok_bad
    print("Backtick tokens checked on the cited pages: %d (%d failures)." % (tok_total, tok_bad))

    print("\nTotal failures: %d" % fails)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

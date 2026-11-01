# -*- coding: utf-8 -*-
"""
asvs_checklist.py - generates checklists from the REAL ASVS 4.0.3 requirements (asvs_requirements.json, extracted
from the PDF and validated by count) and evaluates answers. It also emits OCRG Appendix A (78 table rows).
Standard library only; no network; read-only / writes only to stdout (or --out). Run with `python -I`.

Subcommands:
  generate  --level L1|L2|L3 [--chapters 2,3,5] [--sections 3.4] [--only-delta] [--include-recommended]
            [--format md|json|csv] [--out FILE]
            Items = requirements with an R mark (checkmark) at the requested level (an 'o' mark = recommended only enters with
            --include-recommended). Prints the COUNT VALIDATION (items == independent count from the JSON;
            and, without a chapter filter, == the expected total of the level).
  evaluate  ANSWERS.json --level L1|L2|L3 [--strict]
            ANSWERS.json: {"2.1.1": "pass", "5.3.4": "fail", "3.6.1": {"status": "na", "reason": "no CSP/RP"}, ...}
            status: pass | fail | na | unknown. 'na' requires 'reason' (the ASVS requires justifying non-applicability, p.14).
            Output: coverage by chapter, list of failures with page, level verdict (only if ALL R items of the level
            are pass/justified-na) and a notice that the ASVS is not an official OWASP certification (p.14).
  ocrg      [--category TEXT] [--format md|json|csv]   -> OCRG Appendix A (OCRG p.197-200; printed = PDF - 1)
  stats     -> counts by level and chapter (including the L1 ⊂ L2 ⊂ L3 nesting verified in the data)

Page convention: ASVS = footer = PDF page. OCRG = PDF page.
Labels: [from source] requirements/pages; [inference] verifiability notes aggregated by the package from warnings in the book.
"""
import argparse
import csv
import io
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
LEVELS = ("L1", "L2", "L3")
# Expected totals per level (V1-V14, active requirements with an R mark) - see asvs_lookup.py --validate
EXPECTED_BY_LEVEL = {"L1": 128, "L2": 258, "L3": 278}

# Warnings from the book itself about HOW to verify certain sections (source: the introductory text of each section).
SECTION_NOTES = {
    "1.6": ("Architectural requirements: hard to test by unit/integration tests; review in architecture, code review, or retrospectives.", 19),
    "2.4": ("Cannot be verified by pentest; only by code review or secure tests; if used as a review checklist, treat as L1 (note from the book).", 26),
    "2.10": ("Not pentestable, hence no L1; in review assume a software key store as the minimum at L1; cleartext secrets are never acceptable.", 30),
    "5.1": ("For code reviewers: treat the section as if L1 were required for all items.", 38),
    "6.2": ("Although most lack L1, developers should consider the whole section mandatory.", 42),
    "6.4": ("Although most lack L1, developers should consider the whole section mandatory.", 43),
    "7.1": ("Not pentestable (Top 10 2017:A10): developers meet everything as L1; testers validate through interviews/screenshots/attestation.", 44),
    "7.2": ("Not pentestable (Top 10 2017:A10): developers meet everything as L1; testers validate through interviews/screenshots/attestation.", 45),
    "7.3": ("7.3.1 (log encoding) is hard to test dynamically; architects/reviewers should treat it as L1.", 45),
    "10.2": ("Cannot be met without full access to the source code, including third-party libraries.", 52),
    "14.1": ("Compliance requires an automated build system and access to the build and deploy scripts.", 61),
}


def load(name):
    with open(os.path.join(HERE, name), "r", encoding="utf-8") as f:
        return json.load(f)


def select(d, level, chapters=None, sections=None, only_delta=False, include_rec=False):
    out = []
    for r in d["requirements"]:
        if r["deleted"] or r["chapter"] == "C":
            continue
        if chapters and str(r["chapter"]) not in chapters:
            continue
        if sections and r["section"] not in sections:
            continue
        mark = r[level]
        ok = mark == "R" or (include_rec and mark == "O")
        if not ok:
            continue
        if only_delta:
            lower = {"L1": None, "L2": "L1", "L3": "L2"}[level]
            if lower and r[lower] == "R":
                continue
        out.append(r)
    return out


def independent_count(d, level, chapters=None, sections=None, only_delta=False, include_rec=False):
    """second count, by another path (sum per section) - used in the validation."""
    total = 0
    secs = {}
    for r in d["requirements"]:
        secs.setdefault(r["section"], []).append(r)
    for sec, rs in secs.items():
        if sec == "C":
            continue
        for r in rs:
            if r["text"].startswith("[DELETED"):
                continue
            if chapters and str(r["chapter"]) not in chapters:
                continue
            if sections and sec not in sections:
                continue
            m = r[level]
            if not (m == "R" or (include_rec and m == "O")):
                continue
            if only_delta and level != "L1" and r[{"L2": "L1", "L3": "L2"}[level]] == "R":
                continue
            total += 1
    return total


def levels_of(r):
    return ",".join(c for c in LEVELS if r[c] == "R") + ("+rec:L2" if r["L2"] == "O" else "")


def gen(a):
    d = load("asvs_requirements.json")
    chapters = [c.strip().lstrip("Vv") for c in a.chapters.split(",")] if a.chapters else None
    sections = [s.strip().lstrip("Vv") for s in a.sections.split(",")] if a.sections else None
    items = select(d, a.level, chapters, sections, a.only_delta, a.include_recommended)
    ind = independent_count(d, a.level, chapters, sections, a.only_delta, a.include_recommended)
    valid = (len(items) == ind)
    full = chapters is None and sections is None and not a.only_delta and not a.include_recommended
    if full:
        valid = valid and len(items) == EXPECTED_BY_LEVEL[a.level]
    header = {
        "source": "OWASP ASVS 4.0.3 (CC BY-SA 3.0), requirements extracted from the PDF; page = footer = PDF",
        "level": a.level, "chapters": chapters, "sections": sections, "delta_only_vs_previous_level": a.only_delta,
        "items": len(items), "independent_count": ind,
        "expected_level_total": EXPECTED_BY_LEVEL[a.level] if full else None,
        "count_validation": "OK" if valid else "FAILED",
    }
    if a.format == "json":
        data = {"header": header, "items": [{"id": "V" + r["id"], "asvs_page": r["page"], "section": r["section"], "levels": levels_of(r),
                                             "cwe": r.get("cwe"), "text": r["text"], "status": "unknown"} for r in items]}
        txt = json.dumps(data, ensure_ascii=False, indent=1)
    elif a.format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["id", "asvs_page", "section", "levels", "cwe", "text", "status", "evidence"])
        for r in items:
            w.writerow(["V" + r["id"], r["page"], r["section"], levels_of(r), r.get("cwe") or "", r["text"], "", ""])
        txt = buf.getvalue()
    else:
        L = ["# ASVS 4.0.3 Checklist - level %s%s" % (a.level, " (only what this level adds)" if a.only_delta else ""), ""]
        L.append("Source: OWASP ASVS 4.0.3 (CC BY-SA 3.0 license). Items = requirements with a required mark (checkmark) at %s." % a.level)
        L.append("Count validation: %d items vs %d (independent count)%s -> **%s**" % (
            len(items), ind, (" vs %d expected for the full level" % EXPECTED_BY_LEVEL[a.level]) if full else "", header["count_validation"]))
        L.append("")
        L.append("For each item: status pass / fail / na (with justification) + evidence. Non-applicability must be justified (ASVS p.14).")
        cur_sec = None
        for r in items:
            if r["section"] != cur_sec:
                cur_sec = r["section"]
                L.append("")
                L.append("## V%s %s (ASVS p.%d)" % (cur_sec, d["sections"][cur_sec]["title"], d["sections"][cur_sec]["page"]))
                if cur_sec in SECTION_NOTES:
                    L.append("> [from source] %s (ASVS p.%d)" % SECTION_NOTES[cur_sec])
            note = ""
            if r.get("level_notes"):
                note = " Level notes: " + "; ".join("%s=%s" % kv for kv in r["level_notes"].items())
            L.append("- [ ] **V%s** [%s | CWE %s | ASVS p.%d] %s%s" % (r["id"], levels_of(r), r.get("cwe") or "-", r["page"], r["text"], note))
        txt = "\n".join(L) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(txt)
        print("written %s (%d items; validation %s)" % (a.out, len(items), header["count_validation"]))
    else:
        sys.stdout.write(txt)
    if not valid:
        print("ERROR: count validation failed.", file=sys.stderr)
        sys.exit(1)


def evaluate(a):
    d = load("asvs_requirements.json")
    with open(a.answers, "r", encoding="utf-8") as f:
        ans = json.load(f)
    items = select(d, a.level)
    st = {}
    problems = []
    for k, v in ans.items():
        kid = k.lstrip("Vv")
        if isinstance(v, str):
            v = {"status": v}
        s = v.get("status", "unknown").lower()
        if s not in ("pass", "fail", "na", "unknown"):
            problems.append("invalid status in %s: %s" % (k, s))
            continue
        if s == "na" and not (v.get("reason") or "").strip():
            s = "na_unjustified"
        st[kid] = (s, v.get("reason", ""))
    known = {r["id"] for r in d["requirements"]}
    for k in st:
        if k not in known:
            problems.append("ID does not exist in ASVS 4.0.3: " + k)
    by_ch = {}
    fails, unanswered, na_unjust = [], [], []
    for r in items:
        s = st.get(r["id"], ("unknown", ""))[0]
        c = by_ch.setdefault(str(r["chapter"]), {"total": 0, "pass": 0, "fail": 0, "na": 0, "pending": 0})
        c["total"] += 1
        if s == "pass":
            c["pass"] += 1
        elif s == "fail":
            c["fail"] += 1
            fails.append(r)
        elif s == "na":
            c["na"] += 1
        else:
            c["pending"] += 1
            if s == "na_unjustified":
                na_unjust.append(r)
            else:
                unanswered.append(r)
    print("# ASVS 4.0.3 Evaluation - level %s (%d required requirements)" % (a.level, len(items)))
    print("chapter | total | pass | fail | na(just.) | pending")
    for ch in sorted(by_ch, key=lambda x: int(x)):
        c = by_ch[ch]
        print("V%-7s | %5d | %4d | %4d | %9d | %8d" % (ch, c["total"], c["pass"], c["fail"], c["na"], c["pending"]))
    tot = {k: sum(c[k] for c in by_ch.values()) for k in ("total", "pass", "fail", "na", "pending")}
    print("TOTAL    | %5d | %4d | %4d | %9d | %8d" % (tot["total"], tot["pass"], tot["fail"], tot["na"], tot["pending"]))
    if fails:
        print("\nFailures (prioritize by system risk; the ASVS does not define severity):")
        for r in fails:
            print("  - V%s (ASVS p.%d): %s" % (r["id"], r["page"], r["text"][:140]))
    if na_unjust:
        print("\nN/A without justification (treated as pending; required by ASVS p.14):", ", ".join("V" + r["id"] for r in na_unjust))
    if a.strict and unanswered:
        print("\nPending (no answer): %d - first: %s" % (len(unanswered), ", ".join("V" + r["id"] for r in unanswered[:15])))
    met = tot["fail"] == 0 and tot["pending"] == 0
    print("\nVERDICT: %s" % ("ALL required requirements of %s are pass/justified-na (SELF-ASSESSED conformance with the level)." % a.level if met
                             else "level %s NOT reached/not demonstrated (failures=%d, pending=%d)." % (a.level, tot["fail"], tot["pending"])))
    print("Notice [from source, ASVS p.14]: OWASP does not certify vendors/verifiers/software; 'ASVS certified' badges are not official. "
          "The report must state scope, method, and evidence, including passed and failed items.")
    for p in problems:
        print("WARNING:", p)
    if a.fail_on_unmet and not met:
        sys.exit(1)


def ocrg(a):
    c = load("ocrg_checklist.json")
    items = c["items"]
    if a.category:
        items = [i for i in items if a.category.lower() in i["category"].lower()]
    if a.format == "json":
        txt = json.dumps({"source": c["source"], "page_convention": c["page_convention"], "items": items}, ensure_ascii=False, indent=1)
    elif a.format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["id", "pdf_page", "category", "question", "pass_fail"])
        for i in items:
            w.writerow([i["id"], i["page"], i["category"], i["text"], ""])
        txt = buf.getvalue()
    else:
        L = ["# OCRG Appendix A - Code Review Checklist (%d rows%s)" % (len(items), "; filter: " + a.category if a.category else ""), "",
             "Source: OWASP Code Review Guide v2.0 (2017), OCRG p.197-200 (printed 196-199). The book itself repeats some rows and has wording errors; "
             "they were preserved (fidelity). Items on password complexity/expiration diverge from ASVS 4.0.3 (V2.1.9, V2.1.10) [DATED].", ""]
        for i in items:
            L.append("- [ ] **%s** [%s | OCRG p.%d] %s" % (i["id"], i["category"], i["page"], i["text"]))
        txt = "\n".join(L) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(txt)
        print("written %s (%d items)" % (a.out, len(items)))
    else:
        sys.stdout.write(txt)


def stats(a):
    d = load("asvs_requirements.json")
    act = [r for r in d["requirements"] if not r["deleted"] and r["chapter"] != "C"]
    print("Active requirements V1-V14: %d" % len(act))
    for L in LEVELS:
        print("  %s required: %d (expected %d)" % (L, sum(1 for r in act if r[L] == "R"), EXPECTED_BY_LEVEL[L]))
    rec = [r["id"] for r in act if "O" in (r["L1"], r["L2"], r["L3"])]
    print("  recommended ('o' mark): %s" % (", ".join("V" + i for i in rec) or "none"))
    n12 = [r["id"] for r in act if r["L1"] == "R" and r["L2"] != "R"]
    n23 = [r["id"] for r in act if r["L2"] == "R" and r["L3"] != "R"]
    print("  nesting: L1 without L2 = %d; L2 without L3 = %d (0 means L1 ⊂ L2 ⊂ L3 in the data)" % (len(n12), len(n23)))
    print("  L3 only: %s" % ", ".join("V" + r["id"] for r in act if r["L1"] != "R" and r["L2"] != "R" and r["L3"] == "R"))
    by = {}
    for r in act:
        c = by.setdefault(str(r["chapter"]), [0, 0, 0, 0])
        c[0] += 1
        c[1] += r["L1"] == "R"
        c[2] += r["L2"] == "R"
        c[3] += r["L3"] == "R"
    print("  ch  | active | L1 | L2 | L3")
    for k in sorted(by, key=int):
        print("  V%-3s| %6d | %2d | %2d | %2d" % ((k,) + tuple(by[k])))


def main():
    ap = argparse.ArgumentParser(description="Checklists from the real ASVS 4.0.3 requirements")
    sp = ap.add_subparsers(dest="cmd", required=True)
    g = sp.add_parser("generate")
    g.add_argument("--level", required=True, choices=LEVELS)
    g.add_argument("--chapters")
    g.add_argument("--sections")
    g.add_argument("--only-delta", action="store_true")
    g.add_argument("--include-recommended", action="store_true")
    g.add_argument("--format", choices=("md", "json", "csv"), default="md")
    g.add_argument("--out")
    e = sp.add_parser("evaluate")
    e.add_argument("answers")
    e.add_argument("--level", required=True, choices=LEVELS)
    e.add_argument("--strict", action="store_true")
    e.add_argument("--fail-on-unmet", action="store_true")
    o = sp.add_parser("ocrg")
    o.add_argument("--category")
    o.add_argument("--format", choices=("md", "json", "csv"), default="md")
    o.add_argument("--out")
    sp.add_parser("stats")
    a = ap.parse_args()
    {"generate": gen, "evaluate": evaluate, "ocrg": ocrg, "stats": stats}[a.cmd](a)


if __name__ == "__main__":
    main()

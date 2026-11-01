# -*- coding: utf-8 -*-
"""
asvs_extract_text.py - DETERMINISTICALLY extracts the ASVS 4.0.3 requirements from the text extracted from the PDF
(format with the "=== PAGE N ===" marker, N = PDF page) and writes asvs_requirements.json. Standard library only.

Usage:
  python -I scripts/asvs_extract_text.py PATH/OWASP-ASVS-4.0.3.txt [--out scripts/asvs_requirements.json] [--check]

How it works (summary):
 - chapters and sections come from the table of contents (pages 2-6); requirements come from pages 17-71;
 - each requirement is an identifier (x.y.z or C.n) followed by the description and column "slots" in the order
   L1, L2, L3, CWE [, NIST]; a slot with a check (U+2713) = required; "o" = recommended; empty = not required;
 - tables V2.10 and 3.3.2 carry TEXT in the level slots (e.g. "OS assisted", "HSM"); treated as a level note
   (the level counts as required) and confirmed by the independent coordinate-based extraction (build_asvs_from_pdf.py);
 - --check prints the count validation (sequence per section, totals per level).
Page convention: the ASVS PDF prints in the footer the same number as the PDF page (PDF page = printed).
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

CHECK = "✓"
ID_RE = re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{1,2})\s*$")
APPC_RE = re.compile(r"^C\.(\d{1,2})\s*$")
TOC_SEC = re.compile(r"^V(\d{1,2})\.(\d{1,2})\s+(.+?)\s*\.{3,}\s*(\d+)\s*$")
TOC_CH = re.compile(r"^V(\d{1,2})\s+(.+?)\s*\.{3,}\s*(\d+)\s*$")
FIRST_REQ_PAGE, LAST_REQ_PAGE = 17, 71
HDR_STOP = re.compile(r"^(Note:|References\s*$|Glossary of terms|Additional US Agency|Description of the|Appendix\b)")


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1].split("\n") for i in range(1, len(parts), 2)}


def strip_page_header(lines, n):
    """removes the page header (up to the line with the page number and a following blank line)."""
    for i, ln in enumerate(lines[:12]):
        if ln.strip() == str(n):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
                break
            return lines[j:]
    return lines


def parse_toc(pages):
    chapters, sections = {}, {}
    for n in range(2, 7):
        for ln in pages[n]:
            m = TOC_SEC.match(ln.strip())
            if m:
                sections["%d.%d" % (int(m.group(1)), int(m.group(2)))] = {"title": m.group(3).strip(), "page": int(m.group(4))}
                continue
            m = TOC_CH.match(ln.strip())
            if m:
                chapters[str(int(m.group(1)))] = {"title": m.group(2).strip(), "page": int(m.group(3))}
    return chapters, sections


def is_blank(s):
    return s.strip() == ""


def parse_requirements(pages, sections):
    # flatten lines of pages 17..71 as (page, line)
    flat = []
    for n in range(FIRST_REQ_PAGE, LAST_REQ_PAGE + 1):
        for ln in strip_page_header(pages[n], n):
            flat.append((n, ln.rstrip("\n")))
    # locate section headers in the body
    sec_heads = {}
    for k, v in sections.items():
        sec_heads["V%s %s" % (k, v["title"])] = k
    reqs = []
    cur_sec = None
    cur_ch = None
    in_appc = False
    i = 0
    N = len(flat)
    has_nist = False
    last_n = {}

    def expected_id(sec):
        n = last_n.get(sec, 0) + 1
        return ("C.%d" % n) if sec == "C" else ("%s.%d" % (sec, n))

    while i < N:
        pg, ln = flat[i]
        s = ln.strip()
        if s in sec_heads:
            cur_sec = sec_heads[s]
            cur_ch = cur_sec.split(".")[0]
            has_nist = False
            i += 1
            continue
        if s.startswith("Appendix C:"):
            in_appc = True
            cur_ch, cur_sec = "C", "C"
            i += 1
            continue
        if s == "CWE" or s == "Since":
            # table header: "NIST §" on the next line?
            has_nist = (i + 1 < N and flat[i + 1][1].strip().startswith("NIST"))
            i += 1
            continue
        if cur_sec is None or s != expected_id(cur_sec):
            i += 1
            continue
        rid = s
        last_n[cur_sec] = last_n.get(cur_sec, 0) + 1
        start_page = pg
        i += 1
        # description: up to the first blank line / check / lone 'o'
        desc = []
        while i < N:
            t = flat[i][1]
            ts = t.strip()
            if ts == "" or ts == CHECK or ts == "o":
                break
            if ts == expected_id(cur_sec) or ts == "#":
                break
            if rid == "3.3.2" and re.fullmatch(r"\d+", ts):
                break  # the L1 cell carries "30 days" (text) instead of a check
            desc.append(ts)
            i += 1
        text = ""
        for seg in desc:
            text = text + seg if text.endswith("-") else (text + " " + seg if text else seg)
        deleted = text.startswith("[DELETED")
        # tail: lines up to the next id / header / stop
        tail = []
        while i < N:
            t = flat[i][1]
            ts = t.strip()
            if ts == expected_id(cur_sec) or ts in sec_heads or ts in ("#",):
                break
            if HDR_STOP.match(ts) or (ts.startswith("V") and re.match(r"^V\d", ts)):
                break
            tail.append(t)
            i += 1
        if deleted:
            reqs.append({"id": rid, "page": start_page, "chapter": cur_ch, "section": cur_sec, "text": text,
                         "L1": " ", "L2": " ", "L3": " ", "cwe": None, "since": None, "nist": None,
                         "level_notes": None, "deleted": True})
            continue
        # remove trailing blanks (which may be page breaks) while preserving leading empty slots
        slots_raw = [x for x in tail]
        # non-empty and empty tokens: we need the first 3 slots
        # description already consumed up to the first slot (which may be empty). Slots = next lines.
        levels = {"L1": " ", "L2": " ", "L3": " "}
        notes = {}
        slot_vals = []
        idx = 0
        # default case: 3 level slots, each one a blank line, check, or 'o'
        simple = True
        for k in range(3):
            if idx < len(slots_raw):
                v = slots_raw[idx].strip()
                if v in ("", CHECK, "o"):
                    slot_vals.append(v)
                    idx += 1
                else:
                    simple = False
                    break
            else:
                simple = False
                break
        if simple:
            for k, c in enumerate(("L1", "L2", "L3")):
                levels[c] = {"": " ", CHECK: "R", "o": "O"}[slot_vals[k]]
            rest = [x.strip() for x in slots_raw[idx:] if x.strip() != ""]
        else:
            # cells with text (V2.10 and 3.3.2): marks by order; text grouped into L1/L2/L3 according to the known pattern
            rest_all = [x.strip() for x in slots_raw]
            levels, notes, rest = parse_text_levels(rid, rest_all)
        cwe = nist = since = None
        if in_appc:
            since = rest[0] if rest else None
        else:
            cwe_tokens, nist_tokens = [], []
            for tok in rest:
                if re.fullmatch(r"\d+", tok) and not nist_tokens and not cwe_tokens:
                    cwe_tokens.append(tok)
                elif re.fullmatch(r"all", tok):
                    pass
                elif re.fullmatch(r"[0-9./A ]+", tok) and re.search(r"[0-9/]", tok):
                    if has_nist or nist_tokens:
                        nist_tokens.append(tok)
                    elif re.fullmatch(r"\d+", tok):
                        cwe_tokens.append(tok)
            cwe = " ".join(cwe_tokens) or None
            nist = " ".join(nist_tokens) or None
        reqs.append({"id": rid, "page": start_page, "chapter": cur_ch, "section": cur_sec, "text": text,
                     "L1": levels["L1"], "L2": levels["L2"], "L3": levels["L3"], "cwe": cwe, "since": since,
                     "nist": nist, "level_notes": notes or None, "deleted": False})
    return reqs


def parse_text_levels(rid, toks):
    """level cells with text. Known cases in 4.0.3: V2.10.x and 3.3.2."""
    levels = {"L1": " ", "L2": " ", "L3": " "}
    notes = {}
    # remove trailing CWE/NIST (numeric)
    body = [t for t in toks if t != ""]
    # split off the numeric tail
    tail = []
    while body and (re.fullmatch(r"[\d.]+", body[-1]) or body[-1] == "/"):
        tail.insert(0, body.pop())
    if rid.startswith("2.10."):
        # L1 empty; "OS assisted" (L2); "HSM" (L3)
        txt = " ".join(body)
        if "OS assisted" in txt or ("OS" in body and "assisted" in body):
            levels["L2"] = "R"
            notes["L2"] = "OS assisted"
        if "HSM" in body:
            levels["L3"] = "R"
            notes["L3"] = "HSM"
    elif rid == "3.3.2":
        txt = " ".join(body)
        levels = {"L1": "R", "L2": "R", "L3": "R"}
        m = re.match(r"^(\d+\s+days)\s+(12 hours or 30 minutes of inactivity, 2FA optional)\s+(12 hours or 15 minutes of inactivity, with 2FA)$", txt)
        if m:
            notes = {"L1": m.group(1), "L2": m.group(2), "L3": m.group(3)}
        else:
            notes = {"all": txt}
    else:
        notes = {"all": " ".join(body)}
    return levels, notes, tail


def validate(reqs):
    errs = []
    by_sec = {}
    for r in reqs:
        by_sec.setdefault(r["section"], []).append(r)
    for sec, rs in by_sec.items():
        if sec == "C":
            nums = [int(r["id"].split(".")[1]) for r in rs]
        else:
            nums = [int(r["id"].split(".")[2]) for r in rs]
        if nums != list(range(1, len(nums) + 1)):
            errs.append("non-contiguous sequence in section %s: %s" % (sec, nums))
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("txt")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "asvs_requirements.json"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    pages = load_pages(a.txt)
    chapters, sections = parse_toc(pages)
    reqs = parse_requirements(pages, sections)
    # capitulos
    chapters["C"] = {"title": "Internet of Things Verification Requirements (Appendix C)", "page": 69}
    sections["C"] = {"title": "IoT Verification Requirements (Appendix C)", "page": 69}
    out = {
        "meta": {
            "source": "OWASP Application Security Verification Standard 4.0.3 (Final, October 2021)",
            "page_convention": "PDF page = number printed in the footer",
            "marks": {"R": "required (checkmark)", "O": "recommended (o)", " ": "not required"},
            "generator": "scripts/asvs_extract_text.py",
        },
        "chapters": chapters,
        "sections": sections,
        "requirements": reqs,
    }
    errs = validate(reqs)
    if a.check:
        main_reqs = [r for r in reqs if r["chapter"] != "C"]
        print("rows V1-V14:", len(main_reqs), "| deleted:", sum(r["deleted"] for r in main_reqs),
              "| active:", sum(not r["deleted"] for r in main_reqs), "| appendix C:", len(reqs) - len(main_reqs))
        for lv in ("L1", "L2", "L3"):
            print(lv, "required:", sum(1 for r in main_reqs if not r["deleted"] and r[lv] == "R"))
        print("sequence errors:", errs or "none")
    if errs:
        print("VALIDATION FAILURE:", errs)
        sys.exit(1)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("%d rows -> %s" % (len(reqs), a.out))


if __name__ == "__main__":
    main()

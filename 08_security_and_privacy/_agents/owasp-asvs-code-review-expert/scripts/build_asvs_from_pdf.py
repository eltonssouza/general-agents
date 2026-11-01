# -*- coding: utf-8 -*-
"""
build_asvs_from_pdf.py - BUILD TOOL (optional; requires PyMuPDF).

Deterministically extracts the ASVS 4.0.3 requirements from the PDF, using the word COORDINATES
(L1/L2/L3/CWE/NIST columns) to decide which levels require each requirement. Generates asvs_requirements.json
(raw format: one entry per table row, including [DELETED]).
The package already ships the ready JSON: this script exists to reproduce/audit the extraction.
The other scripts in the package use only the standard library and do not need PyMuPDF.

Usage: python -I scripts/build_asvs_from_pdf.py PATH/OWASP-ASVS-4.0.3.pdf [--out FILE.json]
Page convention: PDF page = printed number (the ASVS PDF prints the same number in the footer).
Level marks: R = required (checkmark), O = recommended ("o"), " " = not required.
"""
import argparse
import json
import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF (fitz) is not installed; use asvs_extract_text.py (text only) or the ready JSON.")

sys.stdout.reconfigure(encoding="utf-8")
ID_RE = re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{1,2})$")
APPC_RE = re.compile(r"^C\.(\d{1,2})$")
SEC_RE = re.compile(r"^V(\d{1,2})\.(\d{1,2})\s+(.+)$")
CH_RE = re.compile(r"^V(\d{1,2})\s+(.+)$")
FIRST_PAGE, LAST_PAGE = 17, 71
CHECK = "✓"


def lines_of(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            txt = "".join(s["text"] for s in l["spans"])
            out.append({"bbox": l["bbox"], "text": txt, "font": l["spans"][0]["font"], "size": l["spans"][0]["size"]})
    return out


def group_lines(words, tol=3.0):
    ws = sorted(words, key=lambda w: (round(w[1]), w[0]))
    rows = []
    for w in ws:
        if rows and abs(rows[-1][0] - w[1]) <= tol:
            rows[-1][1].append(w)
        else:
            rows.append([w[1], [w]])
    for r in rows:
        r[1].sort(key=lambda w: w[0])
    return rows


def extract(pdf):
    doc = fitz.open(pdf)
    chapters, sections, reqs = {}, {}, []
    cur_ch = cur_sec = None
    for pn in range(FIRST_PAGE, LAST_PAGE + 1):
        page = doc[pn - 1]
        L = lines_of(page)
        words = [w for w in page.get_text("words") if w[1] < 755]
        marks = []
        for ln in L:
            t = ln["text"].strip()
            if ln["font"].startswith("Calibri-Light") and ln["size"] >= 12.5:
                m = SEC_RE.match(t)
                if m:
                    marks.append((ln["bbox"][1], "sec", (int(m.group(1)), int(m.group(2)), m.group(3).strip())))
                    continue
                m = CH_RE.match(t)
                if m and ln["size"] >= 15.5:
                    marks.append((ln["bbox"][1], "ch", (int(m.group(1)), m.group(2).strip())))
                    continue
                if t.startswith("Appendix C"):
                    marks.append((ln["bbox"][1], "appc", t))
            if ln["bbox"][0] < 75 and ln["bbox"][1] < 750 and ln["text"].strip():
                marks.append((ln["bbox"][1], "stop", None))
            if ln["font"].startswith("Calibri-Bold") and ln["size"] < 11:
                if ID_RE.match(t) or APPC_RE.match(t):
                    marks.append((ln["bbox"][1], "req", (t, ln["bbox"])))
        headers = []
        for r_y, r_ws in group_lines(words):
            texts = [w[4] for w in r_ws]
            if "L1" in texts and "L2" in texts and "L3" in texts and ("CWE" in texts or "Since" in texts):
                cols = {}
                for w in r_ws:
                    if w[4] == "§" and "NIST_x0" not in cols:
                        cols["NIST_x0"] = w[0] - 12
                    if w[4] in ("L1", "L2", "L3", "CWE", "Since", "NIST"):
                        cols["CWE" if w[4] == "Since" else w[4]] = (w[0] + w[2]) / 2
                        cols[("CWE" if w[4] == "Since" else w[4]) + "_x0"] = w[0]
                headers.append((r_y, cols))
        marks.sort(key=lambda m: m[0])
        for (y, kind, pl) in marks:
            if kind == "ch":
                cur_ch = str(pl[0])
                chapters[cur_ch] = {"title": pl[1], "page": pn}
            elif kind == "appc":
                cur_ch = "C"
                chapters["C"] = {"title": "Internet of Things Verification Requirements (Appendix C)", "page": pn}
                cur_sec = "C"
                sections["C"] = {"title": "IoT Verification Requirements (Appendix C)", "chapter": "C", "page": pn}
            elif kind == "sec":
                cur_ch = str(pl[0])
                cur_sec = "%d.%d" % (pl[0], pl[1])
                sections[cur_sec] = {"title": pl[2], "chapter": cur_ch, "page": pn}
            elif kind == "req":
                rid, bbox = pl
                hs = [h for h in headers if h[0] <= y + 1]
                cols = hs[-1][1] if hs else None
                if not cols:
                    print("WARNING: p.%d %s without a table header" % (pn, rid), file=sys.stderr)
                    continue
                nxt = [m[0] for m in marks if m[0] > y + 1 and m[1] in ("req", "sec", "ch", "appc", "stop")]
                nxt += [h[0] for h in headers if h[0] > y + 1]
                end = min(nxt) if nxt else 755
                top = y - 4
                l1x, cwex = cols["L1"], cols["CWE"]
                nistx = cols.get("NIST_x0")
                desc_ws, marks_ws, cwe_ws, nist_ws = [], [], [], []
                for w in words:
                    if not (top <= w[1] < end - 1):
                        continue
                    xc = (w[0] + w[2]) / 2
                    if w[0] < 100 and w[4] == rid:
                        continue
                    if xc >= cols["L1_x0"] - 3 and xc < cols["CWE_x0"] - 4:
                        marks_ws.append(w)
                    elif nistx is not None and w[0] >= nistx - 8:
                        nist_ws.append(w)
                    elif w[0] >= cols["CWE_x0"] - 8:
                        cwe_ws.append(w)
                    elif 100 <= w[0] and xc < cols["L1_x0"] - 3:
                        desc_ws.append(w)
                text = ""
                for ry, rw in group_lines(desc_ws):
                    seg = " ".join(w[4] for w in rw)
                    if text.endswith("-"):
                        text += seg
                    else:
                        text += (" " if text else "") + seg
                levels = {"L1": " ", "L2": " ", "L3": " "}
                notes = {"L1": [], "L2": [], "L3": []}
                for w in marks_ws:
                    xc = (w[0] + w[2]) / 2
                    best = min(("L1", "L2", "L3"), key=lambda c: abs(cols[c] - xc))
                    if w[4] in (CHECK, "o"):
                        if abs(cols[best] - xc) <= 9:
                            levels[best] = "R" if w[4] == CHECK else "O"
                    else:
                        notes[best].append(w[4])
                level_notes = {k: " ".join(v) for k, v in notes.items() if v}
                for k in level_notes:
                    levels[k] = "R"
                cwe = " ".join(w[4] for _, rw in group_lines(cwe_ws) for w in rw).strip()
                since = None
                if cur_ch == "C":
                    since, cwe = (cwe or None), ""
                nist = " ".join(w[4] for _, rw in group_lines(nist_ws) for w in rw).strip()
                if text.startswith("[DELETED"):
                    levels = {"L1": " ", "L2": " ", "L3": " "}
                    level_notes = {}
                reqs.append({
                    "id": rid, "page": pn, "chapter": cur_ch, "section": cur_sec,
                    "text": text, "L1": levels["L1"], "L2": levels["L2"], "L3": levels["L3"],
                    "cwe": cwe or None, "since": since, "level_notes": level_notes or None, "nist": nist or None, "deleted": text.startswith("[DELETED"),
                })
    return chapters, sections, reqs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default="asvs_raw_pdf.json")
    a = ap.parse_args()
    ch, se, rq = extract(a.pdf)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"chapters": ch, "sections": se, "requirements": rq}, f, ensure_ascii=False, indent=1)
    print("%d requirement rows extracted -> %s" % (len(rq), a.out))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
build_ocrg_checklist_from_pdf.py - BUILD TOOL (optional; requires PyMuPDF).

Deterministically extracts the "Code Review Checklist" table (Appendix A) of the OWASP Code Review Guide v2.0
(PDF pp.197-200; printed number = PDF - 1) using geometry: each table row is a blue category cell;
the description is the text to the right of that cell, in the same vertical band. Generates ocrg_checklist.json.
The package already ships the ready JSON; this script exists to reproduce/audit the extraction and the row count.

Usage: python -I scripts/build_ocrg_checklist_from_pdf.py PATH/OWASP-Code-Review-Guide-v2.pdf [--out FILE.json]
Fidelity: the items are exactly the rows of the book's table, INCLUDING the duplicate rows the book itself repeats.
"""
import argparse
import json
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF (fitz) is not installed; use the ready ocrg_checklist.json.")

sys.stdout.reconfigure(encoding="utf-8")
PAGES = (197, 198, 199, 200)


def rows_of(page):
    cells = []
    for d in page.get_drawings():
        r = d["rect"]
        f = d.get("fill")
        # category cells: blue, x0 ~45, width ~76
        if f and abs(f[0]) < 0.05 and abs(f[1] - 0.48) < 0.03 and abs(f[2] - 0.71) < 0.03 and 70 < r.width < 85 and r.height > 10:
            cells.append(r)
    cells.sort(key=lambda r: r.y0)
    # remove geometric duplicates
    out = []
    for r in cells:
        if not out or abs(out[-1].y0 - r.y0) > 1:
            out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default="ocrg_checklist.json")
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    items = []
    n = 0
    prev_texts = set()
    prev_cat = set()
    for pn in PAGES:
        page = doc[pn - 1]
        spans = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(sp["text"] for sp in l["spans"]).strip()
                if t:
                    spans.append((l["bbox"], t))
        cells = rows_of(page)
        for r in cells:
            if any(t == "CATEGORY" and r.y0 - 1 <= (bb[1] + bb[3]) / 2 <= r.y1 + 1 for bb, t in spans):
                continue  # header row
            cat, desc = [], []
            for bb, t in spans:
                cy = (bb[1] + bb[3]) / 2
                if not (r.y0 - 1 <= cy <= r.y1 + 1):
                    continue
                if bb[2] <= r.x1 + 2:
                    cat.append((bb, t))
                elif bb[0] >= r.x1 and bb[2] < 475:
                    desc.append((bb, t))
            # overlapping text (duplicated layer in the PDF): same position -> keep the new line
            by_pos = {}
            for bb, t in desc:
                by_pos.setdefault(round(bb[1]), []).append(t)
            lines = []
            for y in sorted(by_pos):
                cands = by_pos[y]
                fresh = [t for t in cands if t not in prev_texts] or cands
                lines.append(fresh[0])
            text = ""
            for t in lines:
                text = text + t if text.endswith("-") and t[:1].islower() else (text + " " + t if text else t)
            cby = {}
            for bb, t in cat:
                cby.setdefault(round(bb[1]), []).append(t)
            cat_lines = []
            for y in sorted(cby):
                fresh = [t for t in cby[y] if t not in prev_cat] or cby[y]
                cat_lines.append(fresh[0])
            category = " ".join(cat_lines)
            prev_cat = set(cat_lines)
            prev_texts = set(lines)
            n += 1
            items.append({"id": "A.%d" % n, "page": pn, "category": category.strip(), "text": text.strip(), "rect_y": round(r.y0, 1)})
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"source": "OWASP Code Review Guide v2.0 (2017), Appendix A Code Review Checklist",
                   "page_convention": "PDF page; printed = PDF - 1", "items": items}, f, ensure_ascii=False, indent=1)
    print("%d rows -> %s" % (len(items), a.out))


if __name__ == "__main__":
    main()

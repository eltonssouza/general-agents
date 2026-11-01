# -*- coding: utf-8 -*-
"""
build_index.py - generates scripts/sbr_index.json from the text extracted from the PDF
"Spring Boot Reference Documentation, Version 2.7.18" (acronym SBR).

Usage (reads the text only; no network; does not run anything from the target):
  python -I scripts/build_index.py --src CAMINHO/Spring-Boot-Reference.txt [--toc CAMINHO/toc_clean.txt] [--out scripts/sbr_index.json]

Page convention: N = PDF page (marker "=== PAGE N ==="); printed number = N - 20 (for N >= 21).

The index contains only METADATA derived from the text (table of contents, property names, code identifiers and
dependency coordinates with the page where they appear). It contains no prose excerpts from the book.
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

OFFSET = 20
APP_A = (668, 799)       # Appendix A: common properties (PDF)
APP_F = (844, 881)       # Appendix F: managed versions (PDF)
BODY = (21, 667)
ROOTS = ("spring", "server", "management", "logging", "info", "debug", "trace")
BAD_SUFFIX = (".properties", ".xml", ".yml", ".yaml", ".json", ".jsn", ".txt", ".gif", ".jpg", ".png", ".jks",
              ".html", ".factories", ".imports", ".conf", ".sql", ".ldif", ".class", ".jar", ".war", ".idx",
              ".md", ".ftlh", ".mustache", ".groovy", ".tpl", ".log", ".pid", ".port", ".xsd", ".css", ".js")
KEY_RE = re.compile(r"^(?:%s)(?:\.[A-Za-z0-9_\-\*\[\]<>]+)+$" % "|".join(ROOTS))


def load_pages(path):
    t = open(path, "r", encoding="utf-8", errors="replace").read()
    t = t.replace("\xa0", " ").replace("�", "'")
    parts = re.split(r"=== PAGE (\d+) ===", t)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def norm_key(k):
    k = k.strip().strip(".,;:()'\"`")
    return k


def parse_toc(toc_path):
    out = []
    if not toc_path or not os.path.exists(toc_path):
        return out
    for line in open(toc_path, "r", encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        m = re.match(r"^(.*?)\s+\.\.\.\s+(\d+)\s*$", line)
        if not m:
            continue
        title, printed = m.group(1).strip(), int(m.group(2))
        num = None
        mm = re.match(r"^(\d+(?:\.\d+)*)\.\s+(.*)$", title)
        if mm:
            num, title = mm.group(1), mm.group(2)
        else:
            mm = re.match(r"^\.?([A-F](?:\.\d+)*)\.\s+(.*)$", title)
            if mm:
                num, title = mm.group(1), mm.group(2)
        out.append({"num": num, "title": title, "printed": printed, "pdf": printed + OFFSET})
    return out


def join_wrapped(tokens):
    """joins keys broken across lines (ending in '-' or '.')."""
    out = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        while (t.endswith("-") or t.endswith(".")) and i + 1 < len(tokens) and " " not in tokens[i + 1]:
            i += 1
            t = t + tokens[i]
        out.append(t)
        i += 1
    return out


def appendix_a_keys(pages):
    keys = {}
    for p in range(APP_A[0], APP_A[1] + 1):
        lines = [l.strip() for l in pages.get(p, "").splitlines() if l.strip()]
        i = 0
        # first token of each candidate line (extraction sometimes glues the description onto the same line)
        toks = []
        for l in lines:
            first = l.split(" ")[0]
            toks.append(first if (" " not in l or KEY_RE.match(first)) else l)
        k = 0
        while k < len(toks):
            t = toks[k]
            joined = t
            if (t.endswith("-") or t.endswith(".")) and k + 1 < len(toks) and " " not in toks[k + 1]:
                joined = t + toks[k + 1].split(" ")[0]
                k += 1
            k += 1
            j = norm_key(joined)
            if KEY_RE.match(j) and not j.lower().endswith(BAD_SUFFIX):
                keys.setdefault(j, set()).add(p)
        # keys also in "line with key + description"
        for l in lines:
            first = l.split(" ")[0]
            if " " in l and KEY_RE.match(first) and not first.lower().endswith(BAD_SUFFIX):
                keys.setdefault(first, set()).add(p)
    return keys


def body_keys(pages):
    keys = {}
    rx = re.compile(r"(?<![A-Za-z0-9_\-\./])((?:%s)(?:\.[A-Za-z0-9_\-\*\[\]<>]+)+)" % "|".join(ROOTS))
    for p in range(BODY[0], BODY[1] + 1):
        txt = pages.get(p, "")
        # joins line breaks inside keys ending in '-' (common in the PDF)
        txt = re.sub(r"(\.[A-Za-z0-9_\-]*-)\n(?=[a-z])", r"\1", txt)
        for m in rx.finditer(txt):
            k = norm_key(m.group(1))
            if k.lower().endswith(BAD_SUFFIX) or k.endswith("-") or k.endswith("."):
                continue
            if len(k) < 8:
                continue
            keys.setdefault(k, set()).add(p)
    return keys


def identifiers(pages):
    ids = {}
    rx_at = re.compile(r"(?<![A-Za-z0-9_])@([A-Z][A-Za-z0-9]+)")
    rx_cls = re.compile(r"\b([A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)\b")
    rx_flag = re.compile(r"(?<![A-Za-z0-9_])(--[a-z][a-z0-9\-\.]+)")
    rx_env = re.compile(r"\b([A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+)\b")
    for p in range(21, 668):
        txt = pages.get(p, "")
        txt = re.sub(r"(\w)-\n(\w)", r"\1-\2", txt)
        for rx, pre in ((rx_at, "@"), (rx_cls, ""), (rx_flag, ""), (rx_env, "")):
            for m in rx.finditer(txt):
                tok = pre + m.group(1)
                if len(tok) < 5 or len(tok) > 70:
                    continue
                ids.setdefault(tok, set()).add(p)
    # discards very frequent terms (noise) and unigrams of example class names
    out = {}
    for k, v in ids.items():
        if len(v) > 60:
            continue
        out[k] = sorted(v)
    return out


# Lowercase/dotted terms that the identifier extractor (which requires an initial capital) does not capture:
# Kubernetes manifest keys and log packages. Searched in the text without spaces/breaks, pages 21-667.
EXTRA_IDS = ("preStop", "terminationGracePeriodSeconds", "livenessProbe", "readinessProbe", "startupProbe", "httpGet",
             "configtree:", "/run/secrets", "org.springframework.boot.context.config")


def extra_identifiers(pages, ids):
    for term in EXTRA_IDS:
        key = term.rstrip(":")
        pgs = [p for p in range(21, 668) if term in re.sub(r"\s+", "", pages.get(p, ""))]
        if pgs:
            ids[key] = sorted(set(ids.get(key, [])) | set(pgs))
    return ids


def deps_f1(pages):
    """Appendix F.1: group / artifact / version triples (lines wrapped at ~30 cols)."""
    rows = []
    started = False
    buf = []
    ver_re = re.compile(r"^\d[\w\.\-]*$|^\d[\w\.\-]*(?:RELEASE|FINAL|Final|jre)\S*$")
    for p in range(APP_F[0], APP_F[1] + 1):
        txt = pages.get(p, "")
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        for l in lines:
            if l in ("Group ID", "Artifact ID", "Version") or re.fullmatch(r"\d{3}", l) or l.startswith("When you declare") or l.startswith("the version"):
                continue
            if l.startswith(".F.2") or l.startswith("F.2"):
                started = False
                continue
            if l.startswith(".F.1") or l.startswith("F.1"):
                started = True
                continue
            if not started:
                # F.1 starts on p.843 after the header
                if p >= APP_F[0]:
                    started = True
                else:
                    continue
            buf.append((p, l))
    # group: a version closes the line
    cur = []
    page0 = None
    for p, l in buf:
        if "Group ID" in l:
            l = l.replace("Group ID", "").strip()
        if not l:
            continue
        if ver_re.match(l) and cur:
            cur_lines = [c for _, c in cur]
            grp = cur_lines[0]
            j = 1
            while len(cur_lines[j - 1]) >= 29 and j < len(cur_lines) - 1 and " " not in cur_lines[j] and not "." in cur_lines[j][:3]:
                grp += cur_lines[j]
                j += 1
                if j >= len(cur_lines) - 1:
                    break
            art = "".join(cur_lines[j:])
            if art:
                rows.append({"group": grp, "artifact": art, "version": l, "pdf": cur[0][0]})
            cur = []
        else:
            cur.append((p, l))
    return rows


def version_props(pages):
    """Appendix F.2: name -> property (pairs on consecutive lines)."""
    res = []
    p0 = 876
    txt = "\n".join(pages.get(p, "") for p in range(p0, APP_F[1] + 1))
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    for l in lines:
        for m in re.finditer(r"([A-Za-z0-9\-\.]+\.version)\b", l):
            res.append(m.group(1))
    return sorted(set(res))



def _lines_of(page, cols=(200, 395)):
    """Lines per column (PyMuPDF words): list of (col, x0, y0, x1, y1, text)."""
    from collections import defaultdict
    groups = defaultdict(list)
    for w in page.get_text("words"):
        x0, y0, x1, y1, txt, bno, lno, wno = w
        groups[(bno, lno)].append(w)
    out = []
    for (bno, lno), ws in groups.items():
        ws.sort(key=lambda w: w[0])
        cur = {}
        for w in ws:
            c = 0 if w[0] < cols[0] else (1 if w[0] < cols[1] else 2)
            cur.setdefault(c, []).append(w)
        for c, cw in cur.items():
            txt = (" " if c else "").join(w[4] for w in cw) if c else "".join(w[4] for w in cw)
            out.append((c, cw[0][0], min(w[1] for w in cw), max(w[2] for w in cw), max(w[3] for w in cw), txt.replace(" ", " ").strip()))
    out.sort(key=lambda r: (round(r[2], 0), r[1]))
    return out


_DEF_DESC = re.compile(r"(?<![A-Za-z])Defaults?\s+(?:to|is)\s+(.+?)(?:\.\s|\.$|$)", re.I)


def default_in_description(desc):
    """Default written INSIDE the description (default column empty): returns only the short value (<= 12 words), or None.
    E.g. 'Default to 5672, or 5671 if SSL is enabled.' -> '5672, or 5671 if SSL is enabled'. Does not keep the description."""
    if not desc:
        return None
    m = _DEF_DESC.search(desc.replace("­", ""))
    if not m:
        return None
    v = m.group(1).strip().rstrip(".")
    return v if v and len(v.split()) <= 12 else None


# round 9 (fix): single-segment Appendix A keys (`debug`, `trace`) have no dot; they only count in the Appendix A table
BARE_KEYS = ("debug", "trace")
KEY_START = re.compile(r"^(?:(?:%s)\.|(?:%s)$)" % ("|".join(ROOTS), "|".join(BARE_KEYS)))


def appendix_a_table(pdf):
    """Appendix A via PyMuPDF (columns by x position): returns {key: {'pages':[...], 'default': str|None, 'secao': 'A.n'}}."""
    res = {}
    section = None
    carry = None
    for pn in range(APP_A[0], APP_A[1] + 1):
        lines = _lines_of(pdf[pn - 1])
        # round 4: a section title can start in the MIDDLE of the page; the section of each table row depends on the vertical
        # position (y) of the title on that page (before: the whole page inherited the last title, and 87 keys ended up in the wrong section)
        section_at_top = section
        page_heads = []
        for l in lines:
            m = re.match(r"^\.?(A\.\d+)\.", l[5])
            if m and l[0] == 0:
                page_heads.append((l[2], m.group(1)))
                section = m.group(1)
        hdr = ("Name", "Description", "Default Value", "Default", "Value")
        col0 = [l for l in lines if l[0] == 0 and l[2] < 812 and l[5] not in hdr]
        col2 = [l for l in lines if l[0] == 2 and l[2] < 812 and l[5] not in hdr]
        rows = []
        cur = None
        if carry is not None and col0:
            first = col0[0]
            if not KEY_START.match(first[5]):
                carry["txt"] += first[5]
                col0 = col0[1:]
                rows.append(carry)
            else:
                rows.append(carry)
            carry = None
        for l in col0:
            t = l[5]
            if cur is not None and (cur["txt"].endswith(("-", ".")) or cur["x1"] >= 228) and not KEY_START.match(t) and not re.match(r"^\.?A\.\d+\.", t):  # round 6: a section title is never a key continuation
                cur["txt"] += t
                cur["x1"] = l[3]
                cur["y1"] = l[4]
                continue
            if cur is not None:
                rows.append(cur)
            cur = {"txt": t, "y0": l[2], "x1": l[3], "y1": l[4]}
        if cur is not None:
            rows.append(cur)
        if rows and rows[-1] is not None and rows[-1]["txt"].endswith("-") and pn < APP_A[1]:
            carry = rows.pop()
        # round 6: row boundaries = ALL key cells (includes 'trace'/'debug' without a dot and titles), before the filter
        all_starts = [r["y0"] - 4 for r in rows]
        rows = [r for r in rows if KEY_RE.match(r["txt"]) or r["txt"] in BARE_KEYS]
        # round 6: each table row "owns" the lines of columns 1 (description) and 2 (default) whose y falls between the top
        # of this key (-4pt: description/default sit 2-3pt above the key text) and the top of the next key (or of the next
        # section title). Before, the boundary was y0-3 and the default of the next row leaked ("scheduling-" + "false").
        col1 = [l for l in lines if l[0] == 1 and l[2] < 812 and l[5] not in hdr]
        head_ys = [hy - 4 for hy, _ in page_heads]
        for i, r in enumerate(rows):
            y_ini = r["y0"] - 4
            y_end = min([y for y in all_starts if y > y_ini + 1] + [812])
            for hy in head_ys:
                if y_ini < hy < y_end:
                    y_end = hy
            dv = []
            prev = None
            for c in col2:
                if y_ini <= c[2] < y_end:
                    if prev is not None and (prev[5].endswith(("-", ".", "/", ":", ",")) or prev[3] >= 515):
                        dv[-1] += c[5]
                    else:
                        dv.append(c[5])
                    prev = c
            default = " ".join(dv) if dv else None
            desc = " ".join(c[5] for c in col1 if y_ini <= c[2] < y_end)
            sec_row = section_at_top
            for hy, hs in page_heads:
                if r["y0"] > hy:
                    sec_row = hs
            e = res.setdefault(r["txt"], {"pages": [], "default": None, "secao": sec_row, "default_desc": None})
            if pn not in e["pages"]:
                e["pages"].append(pn)
            if default and not e["default"]:
                e["default"] = default
            if not default and not e["default_desc"]:
                e["default_desc"] = default_in_description(desc)
    return res


def deps_table(pdf):
    """Appendix F.1 via PyMuPDF: columns group (x~51), artifact (x~220), version (x~385).
    Anchor = version line; wrapped group/artifact lines are assigned to the nearest version above (+3pt)."""
    rows = []
    done = False
    for pn in range(APP_F[0], APP_F[1] + 1):
        if done:
            break
        lines = _lines_of(pdf[pn - 1], cols=(200, 380))
        top = 0
        for l in lines:
            if l[5].replace(" ", "").startswith("GroupID"):
                top = l[2]
        use = []
        for l in lines:
            t = l[5]
            if t.startswith(".F.2") or t.startswith("F.2"):
                done = True
                break
            if l[2] <= top or l[2] > 812:
                continue
            if t.replace(" ", "") in ("GroupID", "ArtifactID", "Version") or t.startswith("Version Property") or t.startswith("Name"):
                continue
            if re.fullmatch(r"\d{3}", t):
                continue
            use.append(l)
        vers = [l for l in use if l[0] == 2]
        vers.sort(key=lambda l: l[2])
        recs = [{"y": v[2], "g": [], "a": [], "v": v[5]} for v in vers]
        for l in use:
            if l[0] == 2:
                continue
            cand = [r for r in recs if r["y"] <= l[2] + 3]
            if not cand:
                continue
            r = cand[-1]
            (r["g"] if l[0] == 0 else r["a"]).append((l[2], l[5]))
        for r in recs:
            rows.append({"group": "".join(t for _, t in sorted(r["g"])), "artifact": "".join(t for _, t in sorted(r["a"])),
                         "version": r["v"], "pdf": pn})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--toc", default=None)
    ap.add_argument("--pdf", default=None, help="original PDF (PyMuPDF) to extract the Appendix A and F tables by columns")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sbr_index.json"))
    a = ap.parse_args()
    pages = load_pages(a.src)
    toc = parse_toc(a.toc)
    kb = body_keys(pages)
    ids = extra_identifiers(pages, identifiers(pages))
    vprops = version_props(pages)
    props = {}
    if a.pdf:
        import fitz  # only to rebuild the index
        pdf = fitz.open(a.pdf)
        table = appendix_a_table(pdf)
        deps = deps_table(pdf)
        for k, v in table.items():
            if k.endswith("-"):
                continue  # cell truncated in the source itself (page break); do not invent the rest
            # round 9: default cell really empty (checked by coordinates in the Default Value column, no text in the default
            # and no "Default ..." in the description) -> sem_default=True; so the lookup tells "no published default" apart from "not extracted"
            props[k] = {"apendice_a": sorted(v["pages"]), "corpo": [], "default": v["default"], "secao": v["secao"],
                           **({"default_desc": v["default_desc"]} if v.get("default_desc") else {}),
                           **({"sem_default": True} if (v["default"] is None and not v.get("default_desc")) else {})}
        ka = table
    else:
        ka = appendix_a_keys(pages)
        deps = deps_f1(pages)
        for k, v in ka.items():
            props[k] = {"apendice_a": sorted(v), "corpo": [], "default": None, "secao": None}
    for k, v in kb.items():
        if k.lower().endswith(BAD_SUFFIX) and k not in props:
            continue
        props.setdefault(k, {"apendice_a": [], "corpo": [], "default": None, "secao": None})["corpo"] = sorted(v)
    # round 9 (fix): flags / (body SBR p.138-139) tied to the Appendix A keys /
    for _k, _pg in (("debug", [138, 139]), ("trace", [139])):
        if _k in props:
            props[_k]["corpo"] = _pg
    data = {
        "fonte": "Spring Boot Reference Documentation, Version 2.7.18 (Copyright 2012-2023)",
        "convencao_pagina": "N = PDF page; printed = N - 20 (N >= 21)",
        "paginas": len(pages),
        "toc": toc,
        "props": props,
        "ids": ids,
        "deps": deps,
        "version_props": vprops,
    }
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print("toc=%d props=%d (apendice A=%d, corpo=%d) ids=%d deps=%d version_props=%d -> %s" % (
        len(toc), len(props), len(ka), len(kb), len(ids), len(deps), len(vprops), a.out))


if __name__ == "__main__":
    main()

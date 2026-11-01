# -*- coding: utf-8 -*-
"""
dl_lookup.py - locates topics, pages and chapters in UDL (Prince, 2023) and NNDL (Nielsen, 2015/2019).

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/dl_lookup.py TERM [TERM...]
Page convention: PDF. UDL: printed page = PDF - 14. NNDL: no printed page.
Source: [from source] = the index points to the page(s) where the topic was read; the choice of search terms is [inference].

Options:
  TERM [TERM...]     topic search (accents ignored, whole word; Portuguese and English terms); --top N (default 4); --json
  --page N [--book udl|nndl]   chapter and topics covered by PDF page N (default: udl)
  --printed N        UDL: PDF page corresponding to printed page N (offset +14)
  --chapters [--book udl|nndl]   chapter table, PDF range, reading status and reference
  --chapter N [--book ...]       topics of chapter N
  --gaps             verified NOT COVERED terms and unread ranges
  --datado           [DATED] items with page
"""
import argparse
import io
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

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "dl_index.json"), encoding="utf-8") as f:
        return json.load(f)


def ranges(spec):
    out = []
    for tok in re.split(r"\s*,\s*", spec or ""):
        m = re.fullmatch(r"p?\.?\s*(\d+)(?:\s*-\s*(\d+))?", tok.strip())
        if m:
            a = int(m.group(1))
            out.append((a, int(m.group(2) or a)))
    return out


def has_word(hay, needle):
    return re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", hay) is not None


def score(topic, q):
    qn = norm(q)
    best = 0
    for t in topic["termos"] + [topic["titulo"]]:
        tn = norm(t)
        if tn == qn:
            best = max(best, 10)
        elif has_word(tn, qn):
            best = max(best, 6)
        elif has_word(qn, tn):
            best = max(best, 5)
    return best


def in_gaps(idx, q):
    qn = norm(q)
    for g in idx["sem_cobertura"]:
        gn = norm(g)
        if gn == qn or has_word(qn, gn):
            return g
    return None


def cmd_search(idx, terms, top, as_json):
    q = " ".join(terms)
    gap = in_gaps(idx, q)
    toks = [t for t in re.split(r"[\s,;]+", norm(q)) if t]
    cand = {}
    for tp in idx["topicos"]:
        s = score(tp, q)
        if s == 0 and len(toks) > 1:
            s = sum(score(tp, t) for t in toks) // 2
        if s:
            cand[tp["id"]] = (s, tp)
    res = sorted(cand.values(), key=lambda x: (-x[0], x[1]["id"]))[:top]
    if as_json:
        print(json.dumps({"consulta": q, "sem_cobertura": gap, "resultados": [dict(r[1], score=r[0]) for r in res]}, ensure_ascii=False, indent=1))
        return
    if gap and not res:
        print(f"NOT COVERED: '{q}' (term verified absent from the UDL and NNDL texts; see --gaps). Do not answer from memory as [from source]; use [extrapolation] only if the user asks.")
        return
    if not res:
        print(f"NOT COVERED: no index topic matches '{q}'. Try the books' English terms (e.g., attention, dropout, cross-entropy) or --chapters.")
        return
    if gap:
        print(f"WARNING: '{gap}' is listed as NOT COVERED; the results below are only neighboring topics.")
    for s, tp in res:
        print(f"[{tp['id']}] {tp['titulo']}  (relevance {s})")
        print(f"   reference: references/{tp['ref']}")
        if tp["udl"]:
            print(f"   UDL PDF p.{tp['udl']} (printed = PDF-14)")
        if tp["nndl"]:
            print(f"   NNDL PDF p.{tp['nndl']}")


def chap_for(idx, book, p):
    for c in idx["capitulos"]:
        if c["livro"] == book and c["pdf"][0] <= p <= c["pdf"][1]:
            return c
    return None


def unread(idx, book, p):
    for a, b in idx["nao_lidas"].get(book, []):
        if a <= p <= b:
            return True
    return False


def topics_for_page(idx, book, p):
    key = "udl" if book == "UDL" else "nndl"
    out = []
    for tp in idx["topicos"]:
        for a, b in ranges(tp[key]):
            if a <= p <= b:
                out.append(tp)
                break
    return out


def cmd_page(idx, book, p):
    n = idx["fontes"][book]["paginas_pdf"]
    if p < 1 or p > n:
        print(f"{book} has {n} PDF pages; p.{p} is out of range.")
        return
    c = chap_for(idx, book, p)
    off = idx["fontes"][book]["offset_impressa"]
    imp = f"; printed {p - off}" if off is not None and p > off else ""
    print(f"{book} PDF p.{p}{imp}")
    if c:
        print(f"Ch.{c['n']} {c['titulo']} (PDF {c['pdf'][0]}-{c['pdf'][1]}); reading: {c['leitura']}; reference: references/{c['ref'] or '-'}")
    else:
        print("Outside the mapped chapters (front matter).")
    if unread(idx, book, p):
        print("PAGE NOT READ: the package makes no claims about this page.")
    for tp in topics_for_page(idx, book, p):
        print(f"  topic: [{tp['id']}] {tp['titulo']} -> references/{tp['ref']}")


def cmd_printed(idx, n):
    off = idx["fontes"]["UDL"]["offset_impressa"]
    p = n + off
    print(f"UDL: printed {n} -> PDF p.{p} (offset +{off}; checked: ch.12 starts at printed 207 = PDF 221).")
    cmd_page(idx, "UDL", p)


def cmd_chapters(idx, book):
    for c in idx["capitulos"]:
        if book is None or c["livro"] == book:
            print(f"{c['livro']} Ch.{c['n']}: {c['titulo']} | PDF {c['pdf'][0]}-{c['pdf'][1]} | {c['leitura']} | {c['ref'] or '-'}")


def cmd_chapter(idx, book, n):
    for c in idx["capitulos"]:
        if c["livro"] == book and str(c["n"]) == str(n):
            print(f"{book} Ch.{c['n']}: {c['titulo']} | PDF {c['pdf'][0]}-{c['pdf'][1]} | {c['leitura']} | references/{c['ref'] or '-'}")
            for tp in idx["topicos"]:
                key = "udl" if book == "UDL" else "nndl"
                if any(a <= c["pdf"][1] and b >= c["pdf"][0] for a, b in ranges(tp[key])):
                    print(f"  [{tp['id']}] {tp['titulo']} (p.{tp[key]})")
            return
    print(f"chapter {n} of {book} not found")


def cmd_gaps(idx):
    print("NOT COVERED (terms checked in the extracted UDL and NNDL texts; absent as a whole word):")
    print("  " + "; ".join(idx["sem_cobertura"]))
    print("Unread ranges (NOT read):")
    for book, rs in idx["nao_lidas"].items():
        if rs:
            print(f"  {book}: " + ", ".join(f"p.{a}-{b}" if a != b else f"p.{a}" for a, b in rs))
    print("Note: 'RLHF', 'PPO', 'TRPO', 'InstructGPT', 'ChatGPT', 'GPT-4' appear ONLY in notes/mentions (UDL p.412, p.411, p.439, p.441); there is no treatment beyond that.")


def cmd_datado(idx):
    for d in idx["datado"]:
        print(f"[DATED] {d['tema']} — {d['fonte']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("termos", nargs="*")
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--book", choices=["udl", "nndl"])
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--chapter", type=str)
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--datado", action="store_true")
    a = ap.parse_args()
    idx = load()
    book = a.book.upper() if a.book else None
    if a.page is not None:
        cmd_page(idx, book or "UDL", a.page)
    elif a.printed is not None:
        cmd_printed(idx, a.printed)
    elif a.chapters:
        cmd_chapters(idx, book)
    elif a.chapter is not None:
        cmd_chapter(idx, book or "UDL", a.chapter)
    elif a.gaps:
        cmd_gaps(idx)
    elif a.datado:
        cmd_datado(idx)
    elif a.termos:
        cmd_search(idx, a.termos, a.top, a.json)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()

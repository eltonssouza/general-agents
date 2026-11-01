# -*- coding: utf-8 -*-
"""
linux_lookup.py - deterministic lookup in the linux_index.json index (read-only, no network).

Fonte: Machtelt Garrels, "Introduction to Linux: A Hands on Guide", ed. 1.27 (2008). Sigla TLDP.
Page convention: PDF number (= printed page + 8 in the body of the book).

Usage:
  python -I linux_lookup.py chmod             # term: topic(s) and/or command
  python -I linux_lookup.py cmd tar           # command only: pages where it appears + glossary
  python -I linux_lookup.py page 70           # what is on PDF page 70 (printed 62)
  python -I linux_lookup.py --list            # lists topics
  python -I linux_lookup.py --not-in-book     # lists what the book does NOT cover
  python -I linux_lookup.py cron --json       # JSON output

If nothing is found, prints "NOT COVERED" (does not invent a page).
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

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "linux_index.json")


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def load():
    with open(INDEX, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_pages(pages):
    pages = sorted(set(pages))
    out, start, prev = [], None, None
    for p in pages:
        if start is None:
            start = prev = p
        elif p == prev + 1:
            prev = p
        else:
            out.append((start, prev))
            start = prev = p
    if start is not None:
        out.append((start, prev))
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)


def printed(p):
    return p - 8 if 9 <= p <= 211 else None


FORWARD = {
    "os-internals (base OSTEP)": ["escalonamento", "escalonador", "scheduling", "scheduler", "round robin", "mlfq", "memoria virtual", "virtual memory", "paginacao", "paging", "tlb", "page table", "concorrencia", "concurrency", "thread", "deadlock", "mutex", "semaforo", "semaphore", "journaling interno", "sistema de arquivos por dentro", "context switch", "troca de contexto"],
    "containers agent (Docker/Kubernetes)": ["docker", "kubernetes", "container", "namespace", "cgroup", "pod"],
}


def forward_for(q):
    nq = norm(q)
    for agent, words in FORWARD.items():
        if any(w in nq or nq in w and len(nq) >= 4 for w in words):
            return agent
    return None


def score(topic, q):
    nq = norm(q)
    s = 0
    if len(nq) < 3:
        return 0
    if nq == norm(topic["key"]):
        s += 100
    if nq in norm(topic["name"]):
        s += 40
    for k in topic["keywords"]:
        nk = norm(k)
        if nq == nk:
            s += 60
        elif nq in nk or nk in nq and len(nk) > 2:
            s += 15
    if nq in norm(topic["summary"]):
        s += 10
    for pt in topic["points"]:
        if nq in norm(pt):
            s += 5
    return s


def show_topic(key, t):
    print(f"TOPIC: {t['name']} [{key}]  ({t['chapter']})")
    print(f"CITATION: [from source] (TLDP p.{fmt_pages(t['pages'])})   [pages = PDF; printed = PDF-8]")
    print(f"REFERENCE: references/{t['reference_file']}")
    print("\nSUMMARY:\n  " + t["summary"])
    print("\nPOINTS (with page):")
    for p in t["points"]:
        print("  * " + p)
    if t["gaps"]:
        print("\nNOT IN THE SOURCE (treat as [extrapolation] if the user asks):")
        for g in t["gaps"]:
            print("  - " + g)
    if t["dated"]:
        print("\n[DATED]:")
        for d in t["dated"]:
            print("  - " + d)
    print()


AMBIGUOS = {"set", "time", "file", "find", "which", "more", "less", "date", "host", "id", "at", "read", "wait", "shift", "screen", "eval", "exec", "free", "mail", "top", "cut", "sort", "tail", "head", "echo", "export", "source", "info", "man", "cat", "cd", "ls", "play", "clear", "diff", "batch", "exit", "who", "write", "kill", "nice", "init", "mount", "alias"}


def show_cmd(name, c):
    pg = c["pages"]
    print(f"COMMAND: {name}")
    if pg:
        shown = pg[:20]
        extra = f" (+{len(pg) - 20} pages)" if len(pg) > 20 else ""
        print(f"APPEARS IN THE TEXT (body, PDF p.9-207): TLDP p.{fmt_pages(shown)}{extra}   [word occurrence; open the page before citing]")
    else:
        print("Does NOT appear in the body of the book (PDF p.9-207).")
    if name in AMBIGUOS and pg:
        print("  NOTE: common English word; the list includes uses that are not the command. Open the page before citing.")
    g = c.get("glossary")
    if g:
        print(f"GLOSSARY: entry on p.{g['glossary_page']}")
        for s in g["sections"]:
            ap = " (start page of the parent section; approximate)" if s["approx"] else ""
            print(f"  section {s['section']} -> p.{s['pdf_page']}{ap}")
        print("  (the glossary cross-references may be misaligned with the section numbering; confirm on the page)")
    print()


def main():
    ap = argparse.ArgumentParser(description="Lookup in the index of the TLDP book (Introduction to Linux).")
    ap.add_argument("args", nargs="*", help="term | cmd <name> | page <N>")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--not-in-book", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    idx = load()
    topics, cmds = idx["topics"], idx["commands"]

    if a.list:
        for k, t in topics.items():
            print(f"{k:48s} {t['chapter']:14s} p.{fmt_pages(t['pages'])}")
        return 0
    if a.not_in_book:
        print("THE BOOK (TLDP 1.27, 2008) DOES NOT COVER:")
        for x in idx["not_in_book"]:
            print("  - " + x)
        return 0
    if not a.args:
        ap.print_help()
        return 2

    if a.args[0] == "page" and len(a.args) == 2 and a.args[1].isdigit():
        n = int(a.args[1])
        hit = {k: t for k, t in topics.items() if n in t["pages"]}
        pr = printed(n)
        print(f"PDF p.{n}" + (f" (printed {pr})" if pr else " (outside the numbered body)"))
        if not hit:
            print("NOT COVERED by an indexed topic on this page (use the extracted text).")
            return 1
        for k, t in hit.items():
            print(f"  - {t['name']} [{k}] -> references/{t['reference_file']}")
        return 0

    if a.args[0] == "cmd" and len(a.args) == 2:
        name = a.args[1]
        c = cmds.get(name) or cmds.get(name.lower())
        if not c:
            print(f"NOT COVERED: '{name}' is not in the command index (the book may not cover it; see --not-in-book).")
            return 1
        if a.json:
            print(json.dumps({name: c}, ensure_ascii=False, indent=1))
        else:
            show_cmd(name, c)
        return 0

    q = " ".join(a.args)
    found = False
    nq = norm(q)
    for entry in idx["not_in_book"]:
        ne = norm(entry)
        first = re.split(r"[ /,(]+", ne)[0]
        if nq == ne or nq == first or (len(nq) >= 4 and nq in ne):
            print(f"NOT IN THE SOURCE: {entry}")
            print("NOT COVERED in the collection (TLDP, 2008). If you answer, label it [extrapolation]; do not cite a page.")
            return 1
    results = []
    c = cmds.get(q) or cmds.get(q.lower())
    ranked = sorted(((score(t, q), k) for k, t in topics.items()), reverse=True)
    ranked = [(s, k) for s, k in ranked if s > 0][:3]
    if a.json:
        out = {"query": q, "command": c, "topics": {k: topics[k] for _, k in ranked}}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0 if (c or ranked) else 1
    if c:
        found = True
        show_cmd(q, c)
    for s, k in ranked:
        found = True
        show_topic(k, topics[k])
    if not found:
        print(f"NOT COVERED: nothing in the index for '{q}'.")
        fw = forward_for(q)
        if fw:
            print(f"OUT OF SCOPE: forward to {fw}. The book only shows usage (commands), not the internal mechanism.")
        print("The book may not cover the subject (see --not-in-book); do not cite an invented page.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

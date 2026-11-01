# -*- coding: utf-8 -*-
"""
cc_checklist.py - code review checklist based on "Código Limpo" (Clean Code), by area (chapter), with the
PDF page of each item. Chooses the areas from the request (--area) or from the content of a file (--file).

Reads cc_checklist.json (same directory). Reads the file as TEXT (never executes it). Read-only, no network.
Area keys are the Portuguese slugs used by the collection (nomes, funcoes, comentarios, ...); see --list.

Usage:
  python -I cc_checklist.py --list                      available areas
  python -I cc_checklist.py --area funcoes,testes       chosen areas
  python -I cc_checklist.py --file src/Pedido.java      areas detected in the file (+ the always-applicable ones)
  python -I cc_checklist.py --all                       all areas
Output: Markdown with [ ] boxes and (CL p.N). Unknown area: exit 2.
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

HERE = os.path.dirname(os.path.abspath(__file__))
ALWAYS = ["nomes", "funcoes", "comentarios", "formatacao"]
DETECT = {
    "testes": r"@Test\b|\bassert\w*\s*\(|\bdef test_\w+|\b(describe|it|test)\s*\(\s*['\"]|import\s+(org\.junit|pytest|unittest)",
    "concorrencia": r"\b(Thread|Runnable|synchronized|ExecutorService|Executors|volatile|AtomicInteger|Lock|"
                    r"CompletableFuture|threading|multiprocessing|asyncio|Semaphore|ConcurrentHashMap)\b",
    "erros": r"\b(try|catch|throw|throws|except|raise|finally)\b",
    "classes": r"^\s*(public\s+|abstract\s+|final\s+|export\s+)*class\s+\w+",
    "objetos-e-dados": r"\w+\(\)\.\w+\(\)\.\w+\(|\bpublic\s+\w+\s+\w+\s*;",
    "limites": r"^\s*(import|from)\s+(?!java\.lang)[\w.]+",
}


def load():
    with open(os.path.join(HERE, "cc_checklist.json"), encoding="utf-8") as f:
        return json.load(f)


def detect(text):
    return [area for area, rx in DETECT.items() if re.search(rx, text, re.M)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--area", help="comma-separated list")
    ap.add_argument("--file", help="code file used to detect the areas")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)
    data = load()
    areas = data["areas"]
    if a.list:
        for k, v in areas.items():
            print("%-18s %s (ch. %s, CL %s) - %d items" % (k, v["title"], v["chapter"], v["pages"], len(v["items"])))
        return 0
    chosen = []
    why = {}
    if a.all:
        chosen = list(areas)
    if a.area:
        for k in [x.strip() for x in a.area.split(",") if x.strip()]:
            if k not in areas:
                print("Unknown area: %s. Use --list." % k)
                return 2
            chosen.append(k)
            why[k] = "requested"
    if a.file:
        try:
            with open(a.file, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError as e:
            print("Error reading %s: %s" % (a.file, e))
            return 2
        for k in ALWAYS:
            why.setdefault(k, "always applicable")
        for k in detect(text):
            why.setdefault(k, "detected in the file")
        chosen += ALWAYS + detect(text)
    if not chosen:
        ap.print_help()
        return 2
    seen = []
    for k in chosen:
        if k not in seen and k in areas:
            seen.append(k)
    print("# Review checklist - Código Limpo (PDF pages)\n")
    print("[from source] each item cites the page; answering 'no' is a candidate for improvement, not a verdict.\n")
    for k in seen:
        v = areas[k]
        extra = " - %s" % why[k] if k in why else ""
        print("## %s (ch. %s, CL %s)%s" % (v["title"], v["chapter"], v["pages"], extra))
        for it in v["items"]:
            print("- [ ] %s (CL %s)" % (it["q"], it["ref"].replace("CL ", "")))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

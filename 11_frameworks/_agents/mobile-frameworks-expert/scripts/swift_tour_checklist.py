# -*- coding: utf-8 -*-
"""
swift_tour_checklist.py - checklist for "A Swift Tour" (SWT; 19 pages; Swift version NOT stated; 2026 capture).
It helps track the study of the tour: which topics a .swift file exercises and which are still missing, in tour order,
with page numbers. Detection is heuristic (regex over code stripped of comments/strings); it says "the construct appears",
not "it is correct". It never compiles or runs anything; stdlib, no network, deterministic.

Subcommands:
  list                         the 38 tour topics in order, with pages
  experiments                  the tour's exercises ("Experiment"), paraphrased, with page
  scan FILE.swift [FILE2 ...]  marks [x]/[ ] the topics exercised; shows % and what is missing (use "-" for stdin) [--json]
  next [--done 1,2,3]          next topic(s) to study, given what is already done (ids); no --done = start of the tour
Labels: order and pages = [from source] (SWT p.N); the detection regex is [inference] (it does not appear in the tour).
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# (id, title, pages, [patterns that must ALL appear], use_raw)
T = [
    (1, "Hello world: print, no main and no semicolons", "SWT p.1", [r"\bprint\s*\("], False),
    (2, "let and var", "SWT p.1", [r"\blet\s+\w+", r"\bvar\s+\w+"], False),
    (3, "Explicit type and inference", "SWT p.1", [r"\b(?:let|var)\s+\w+\s*:\s*[\w\[\]?:\s]+=", r"\b(?:let|var)\s+\w+\s*=\s*[\w\"\[]"], False),
    (4, "Explicit conversion between types", "SWT p.2", [r"\b(?:String|Double|Int|Float)\("], False),
    (5, "Interpolation \\( )", "SWT p.2", [r"\\\("], True),
    (6, "Multiline string (triple quotes)", "SWT p.2", [r'"""'], True),
    (7, "Arrays and dictionaries", "SWT p.2-3", [r"\.append\(|\[\s*\]|\[\s*:\s*\]|\[\s*[\"\d]"], False),
    (8, "if and for-in", "SWT p.3", [r"\bif\b", r"\bfor\b[^\n]*\bin\b"], False),
    (9, "if/switch as an expression", "SWT p.3", [r"(?:=|\breturn)\s*(?:if|switch)\b"], False),
    (10, "Optionals: if let, ??, type?", "SWT p.4", [r"\bif\s+let\b|\?\?|:\s*[\w\[\]]+\?"], False),
    (11, "switch (patterns, let/where, default)", "SWT p.4-5", [r"\bswitch\b"], False),
    (12, "while and repeat-while", "SWT p.5-6", [r"\bwhile\b", r"\brepeat\b"], False),
    (13, "Ranges ..< and ...", "SWT p.6", [r"\.\.<|\.\.\."], False),
    (14, "Functions, argument labels and return", "SWT p.6", [r"\bfunc\s+\w+"], False),
    (15, "Tuples as a return value", "SWT p.6-7", [r"->\s*\(\s*\w+\s*:"], False),
    (16, "Nested functions and functions as values", "SWT p.7-8", [r"->\s*\(\s*\(|:\s*\([^)]*\)\s*->\s*\w+"], False),
    (17, "Closures ({ in }, $0, trailing closure)", "SWT p.8", [r"\$0|\{\s*\(?[\w\s:,]*\)?\s*(?:->\s*\w+\s*)?in\b"], False),
    (18, "Classes and instances", "SWT p.8-9", [r"\bclass\s+\w+"], False),
    (19, "init, self and deinit", "SWT p.9", [r"\binit\s*\("], False),
    (20, "Inheritance and override", "SWT p.9-10", [r"\boverride\b"], False),
    (21, "get/set properties", "SWT p.10", [r"\bget\s*\{", r"\bset\s*(?:\([^)]*\))?\s*\{"], False),
    (22, "willSet and didSet", "SWT p.11", [r"\bwillSet\b|\bdidSet\b"], False),
    (23, "Optional chaining ?.", "SWT p.11", [r"\w\?\.\w"], False),
    (24, "Enums: raw values and associated values", "SWT p.11-13", [r"\benum\s+\w+"], False),
    (25, "Structs (copy vs reference)", "SWT p.13-14", [r"\bstruct\s+\w+"], False),
    (26, "async and await", "SWT p.14", [r"\basync\b", r"\bawait\b"], False),
    (27, "async let and Task", "SWT p.14", [r"\basync\s+let\b|\bTask\s*\{"], False),
    (28, "Task groups", "SWT p.14-15", [r"\bwith(?:Throwing)?TaskGroup\b"], False),
    (29, "Actors", "SWT p.15", [r"\bactor\s+\w+"], False),
    (30, "Protocols and mutating", "SWT p.15-16", [r"\bprotocol\s+\w+"], False),
    (31, "Extensions", "SWT p.16", [r"\bextension\s+\w+"], False),
    (32, "Protocol as a type (any)", "SWT p.16-17", [r"\bany\s+[A-Z]\w*"], False),
    (33, "Error, throw and throws", "SWT p.17", [r"\bthrows?\b", r":\s*Error\b"], False),
    (34, "do-catch and try", "SWT p.17-18", [r"\bdo\s*\{", r"\bcatch\b", r"\btry\b"], False),
    (35, "try? (converts to an optional)", "SWT p.18", [r"\btry\?"], False),
    (36, "defer", "SWT p.18", [r"\bdefer\s*\{"], False),
    (37, "Generics <T>", "SWT p.18-19", [r"(?:func|struct|class|enum)\s+\w+\s*<\s*\w+"], False),
    (38, "where in generics", "SWT p.19", [r"\bwhere\b"], False),
]

EXPERIMENTS = [
    ("SWT p.2", "Create a constant with an explicit Float type and the value 4."),
    ("SWT p.2", "Remove the conversion to String on the last line of the example and see the error."),
    ("SWT p.2", "Use \\() to include a floating-point calculation and someone's name in a greeting."),
    ("SWT p.4", "Change optionalName to nil, see the greeting and add an else for that case."),
    ("SWT p.5", "Remove the default from the switch and see the error."),
    ("SWT p.5", "Replace the _ with a variable name and record which kind of number has the largest value."),
    ("SWT p.6", "Change the condition from m < 100 to m < 0 and compare while with repeat-while."),
    ("SWT p.6", "Remove the day parameter and add a parameter with the special of the day."),
    ("SWT p.8", "Rewrite the closure to return zero for odd numbers."),
    ("SWT p.9", "Add a constant property with let and another method that takes an argument."),
    ("SWT p.10", "Create the subclass Circle of NamedShape (radius and name in init), with area() and simpleDescription()."),
    ("SWT p.12", "Write a function that compares two Rank values by their raw values."),
    ("SWT p.13", "Add to Suit a color() method (black for spades/clubs, red for hearts/diamonds)."),
    ("SWT p.13", "Add a third case to ServerResponse and to the switch."),
    ("SWT p.14", "Write a function that returns a full deck (one card for each combination of rank and suit)."),
    ("SWT p.16", "Add another requirement to ExampleProtocol and adjust SimpleClass and SimpleStructure."),
    ("SWT p.16", "Write an extension of Double with the absoluteValue property."),
    ("SWT p.17", "Change the printer name so that send(job:toPrinter:) throws an error."),
    ("SWT p.18", "Throw errors inside the do-block to land in the 1st, 2nd and 3rd catch."),
    ("SWT p.19", "Modify anyCommonElements to return the array of the common elements."),
]


def sanitize(text):
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
        elif text.startswith("/*", i):
            while i < n and not text.startswith("*/", i):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            out.append("  ")
            i += 2
        elif text.startswith('"""', i):
            out.append('"""')
            i += 3
            while i < n and not text.startswith('"""', i):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            out.append('"""')
            i += 3
        elif c == '"':
            out.append('"')
            i += 1
            while i < n and text[i] != '"' and text[i] != "\n":
                if text[i] == "\\" and i + 1 < n:
                    out.append("  ")
                    i += 2
                    continue
                out.append(" ")
                i += 1
            if i < n and text[i] == '"':
                out.append('"')
                i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def strip_comments_only(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    return re.sub(r"//[^\n]*", " ", text)


def scan_text(text):
    clean = sanitize(text)
    raw = strip_comments_only(text)
    res = {}
    for tid, title, pg, pats, use_raw in T:
        src = raw if use_raw else clean
        res[tid] = all(re.search(p, src) for p in pats)
    return res


def cmd_scan(files, as_json):
    out = []
    rc = 0
    for fn in files:
        try:
            text = sys.stdin.read() if fn == "-" else open(fn, "r", encoding="utf-8", errors="replace").read()
        except OSError as e:
            print(f"Error reading {fn}: {e}", file=sys.stderr)
            return 2
        res = scan_text(text)
        done = [t for t in T if res[t[0]]]
        miss = [t for t in T if not res[t[0]]]
        out.append({"arquivo": fn, "cobertos": [t[0] for t in done], "faltando": [t[0] for t in miss], "percentual": round(100 * len(done) / len(T))})
        if not as_json:
            print(f"== {fn}: {len(done)}/{len(T)} tour topics ({round(100*len(done)/len(T))}%)")
            for t in T:
                print(f"  [{'x' if res[t[0]] else ' '}] {t[0]:>2}. {t[1]} ({t[2]})")
            if miss:
                print(f"  Next in the tour: {miss[0][0]}. {miss[0][1]} ({miss[0][2]})")
            print("  Note: detection is heuristic: it indicates that the construct appears, not that it is correct or compiles.")
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    return rc


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("list")
    sp.add_parser("experiments")
    s = sp.add_parser("scan")
    s.add_argument("files", nargs="+")
    s.add_argument("--json", action="store_true")
    n = sp.add_parser("next")
    n.add_argument("--done", default="")
    n.add_argument("--count", type=int, default=3)
    a = ap.parse_args()
    if a.cmd == "list":
        for t in T:
            print(f"{t[0]:>2}. {t[1]} ({t[2]})")
        print(f"{len(T)} topics. Source: A Swift Tour (SWT p.1-19); Swift version not stated [DATED] 2026.")
        return 0
    if a.cmd == "experiments":
        for pg, txt in EXPERIMENTS:
            print(f"- ({pg}) {txt}")
        print(f"{len(EXPERIMENTS)} exercises (paraphrase of the tour's 'Experiment' boxes).")
        return 0
    if a.cmd == "scan":
        return cmd_scan(a.files, a.json)
    if a.cmd == "next":
        try:
            done = {int(x) for x in a.done.split(",") if x.strip()}
        except ValueError:
            print("Error: --done expects comma-separated integer ids.", file=sys.stderr)
            return 2
        bad = [d for d in done if d < 1 or d > len(T)]
        if bad:
            print(f"Error: ids outside 1..{len(T)}: {bad}", file=sys.stderr)
            return 2
        rest = [t for t in T if t[0] not in done]
        if not rest:
            print("Tour complete (all topics marked). Outside the tour: NOT COVERED (SwiftUI, Xcode, guard, etc.).")
            return 0
        for t in rest[:a.count]:
            print(f"{t[0]:>2}. {t[1]} ({t[2]})")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

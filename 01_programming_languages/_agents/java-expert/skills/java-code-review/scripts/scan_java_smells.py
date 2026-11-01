#!/usr/bin/env python3
"""Regex scan for points of attention in Java code (read-only, no network).

Usage:
    python -I scan_java_smells.py [--json] PATH [PATH ...]
    python -I scan_java_smells.py --rules        # lists the rules, the origin (book page) and what is a script heuristic

PATH may be a .java file or a directory (recursive; ignores .git, target, build, out,
node_modules, .gradle, .idea). It does NOT compile, execute or import the code.

It is regex triage (there is no Java parser in the Python standard library): it indicates WHERE to look and
has false positives and negatives. "No findings" is NOT approval. Each rule cites the page
of the sources (Think = Think Java 6.1.3, Adv = Advanced Java; PDF pages).
Origin of the rules: each rule repeats a recommendation from Think or Adv, with the PDF page ([from source]); the
WAY of detecting it (regex, line windows) is the script's and is [extrapolation]. Exit code: 0 if it ran; 2 for a usage error.
"""
import argparse
import json
import os
import re
import sys

SKIP_DIRS = {".git", "target", "build", "out", "node_modules", ".gradle", ".idea"}


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(".java"):
                yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in sorted(files):
                    if f.endswith(".java"):
                        yield os.path.join(root, f)
        else:
            print(f"warning: nonexistent path: {p}", file=sys.stderr)


def strip_code(line, state):
    """Removes comments and string contents (keeps the quotes). state['block'] tracks /* */."""
    out, i, n = [], 0, len(line)
    while i < n:
        if state["block"]:
            j = line.find("*/", i)
            if j < 0:
                return "".join(out)
            state["block"] = False
            i = j + 2
            continue
        c = line[i]
        if line.startswith("/*", i):
            state["block"] = True
            i += 2
            continue
        if line.startswith("//", i):
            break
        if c == '"':
            out.append('"')
            i += 1
            while i < n and line[i] != '"':
                i += 2 if line[i] == "\\" else 1
            out.append('"')
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


STR_EQ = re.compile(r'(?:==|!=)\s*"[^"]*"|"[^"]*"\s*(?:==|!=)')
FINALIZE = re.compile(r"\bvoid\s+finalize\s*\(\s*\)")
EMPTY_CATCH = re.compile(r"\bcatch\s*\([^)]*\)\s*\{\s*\}")
OBJ_METHODS = [
    (re.compile(r"\bpublic\s+boolean\s+equals\s*\("), "equals"),
    (re.compile(r"\bpublic\s+int\s+hashCode\s*\(\s*\)"), "hashCode"),
    (re.compile(r"\bpublic\s+String\s+toString\s*\(\s*\)"), "toString"),
]
RET_COLL = re.compile(r"\b(?:List|Set|Map|Collection|Iterable|Queue|Deque)\s*<[^>]*>\s+\w+\s*\([^)]*\)\s*(?:throws[^{]*)?\{")
RET_NULL = re.compile(r"^\s*return\s+null\s*;")
RESOURCE_NEW = re.compile(r"\bnew\s+(?:FileInputStream|FileOutputStream|FileReader|FileWriter|BufferedReader|BufferedWriter|PrintWriter|ObjectInputStream|ObjectOutputStream)\s*\(")
LOOP_OPEN = re.compile(r"^\s*(?:for|while)\b.*\{\s*$|^\s*do\s*\{\s*$")
STR_PLUS = re.compile(r"\b\w+\s*\+=\s*[\"\w(]")
CLASS_DECL = re.compile(r"\b(?:class|enum|record)\s+(\w+)")


def scan_file(path):
    f = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            raw = fh.read().splitlines()
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
        return f
    st = {"block": False}
    code = [strip_code(l, st) for l in raw]

    def add(i, rule, sev, msg):
        f.append(dict(file=path, line=i + 1, rule=rule, severity=sev, message=msg, text=raw[i].strip()[:140]))

    depth, loop_stack, in_ret_coll = 0, [], None
    classes = []  # (name, line, has_equals, has_hash)
    for i, c in enumerate(code):
        in_loop = bool(loop_stack)
        if STR_EQ.search(c):
            add(i, "string-equals-eq", "high",
                "== / != on a String: compares references, not content; use equals (Think p.86; Adv p.26)")
        if FINALIZE.search(c):
            add(i, "finalize", "high",
                "finalize(): finalizers are considered dangerous; to release resources use try-with-resources "
                "+ AutoCloseable (Adv p.16)")
        multi_empty = False
        if re.search(r"\bcatch\s*\([^)]*\)\s*\{\s*$", c):
            for k in range(i + 1, min(len(code), i + 4)):
                if code[k].strip():
                    multi_empty = code[k].strip() == "}"
                    break
        if EMPTY_CATCH.search(c) or multi_empty:
            add(i, "empty-catch", "high",
                "empty catch swallows the exception; log it (the only exception the book accepts is a failure of close()) "
                "(Adv p.73, 75)")
        for rx, name in OBJ_METHODS:
            if rx.search(c):
                prev = ""
                for k in range(i - 1, max(-1, i - 3), -1):
                    if code[k].strip():
                        prev = code[k].strip()
                        break
                if "@Override" not in prev:
                    add(i, "missing-override", "medium",
                        f"{name}() without @Override: without the annotation a signature error becomes a silent overload, "
                        "not an override (Adv p.22-25, 34, 60-61)")
                if classes:
                    n, ln, he, hh = classes[-1]
                    if name == "equals":
                        classes[-1] = (n, ln, i + 1, hh)
                    elif name == "hashCode":
                        classes[-1] = (n, ln, he, i + 1)
        if RESOURCE_NEW.search(c) and "try" not in c:
            prev = " ".join(code[max(0, i - 1): i])
            if "try (" not in prev and "try(" not in prev:
                add(i, "resource-no-twr", "medium",
                    "resource opened outside try-with-resources: ensure closing with try-with-resources "
                    "(Java 7, AutoCloseable) (Adv p.16, 75)")
        if RET_COLL.search(c):
            in_ret_coll = depth
        if in_ret_coll is not None and RET_NULL.search(c):
            add(i, "return-null-collection", "medium",
                "return null in a method that returns a collection: prefer an empty collection; for an absent value the book cites "
                "Optional (Java 8) (Adv p.64)")
        if in_loop and STR_PLUS.search(c) and "String" in " ".join(code[max(0, i - 25): i + 1]):
            add(i, "string-concat-loop", "low",
                "'+=' in a loop (possible String concatenation): in loops use StringBuilder (Adv p.69-70) "
                "— confirm the variable is a String")
        m = CLASS_DECL.search(c)
        if m and "{" in c:
            classes.append((m.group(1), i + 1, 0, 0))
        if LOOP_OPEN.search(c):
            loop_stack.append(depth)
        depth += c.count("{") - c.count("}")
        while loop_stack and depth <= loop_stack[-1]:
            loop_stack.pop()
        if in_ret_coll is not None and depth <= in_ret_coll:
            in_ret_coll = None
    for n, ln, he, hh in classes:
        if he and not hh:
            f.append(dict(file=path, line=he, rule="equals-without-hashcode", severity="high",
                          message=f"class {n} defines equals without hashCode: equal objects must have the same hashCode "
                                  "(contract, Adv p.23)",
                          text=raw[he - 1].strip()[:140]))
    return f


RULES = [
    ("string-equals-eq", "high", "== / != with a String literal: use equals", "Think p.86; Adv p.26"),
    ("finalize", "high", "finalize(): finalizers considered dangerous; use try-with-resources", "Adv p.16"),
    ("empty-catch", "high", "empty catch: at least log it (accepted exception: failure of close())", "Adv p.73, 75"),
    ("equals-without-hashcode", "high", "equals without hashCode in the same class", "Adv p.23"),
    ("missing-override", "medium", "equals/hashCode/toString without @Override", "Adv p.22-25, 34, 60-61"),
    ("resource-no-twr", "medium", "resource opened outside try-with-resources (Java 7)", "Adv p.16, 75"),
    ("return-null-collection", "medium", "return null in a method that returns a collection", "Adv p.64"),
    ("string-concat-loop", "low", "+= in a loop on a String: use StringBuilder", "Adv p.69-70"),
]


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    a = ap.parse_args(argv)
    if a.rules:
        print("# Rules (origin = PDF page of Think/Adv; regex detection is a script heuristic [extrapolation])")
        for r, sev, desc, pg in RULES:
            print(f"- [{sev}] {r}: {desc} ({pg})")
        return 0
    if not a.paths:
        print("error: provide a path or --rules", file=sys.stderr)
        return 2
    allf, n = [], 0
    for p in iter_files(a.paths):
        n += 1
        allf.extend(scan_file(p))
    order = {"high": 0, "medium": 1, "low": 2}
    allf.sort(key=lambda d: (order[d["severity"]], d["file"], d["line"]))
    if a.json:
        json.dump(dict(files_scanned=n, findings=allf), sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    print(f"# Java scan (regex) — {n} .java file(s) — {len(allf)} finding(s)")
    print("# Triage: indicates where to look; confirm each item by reading the code.\n")
    counts = {}
    for d in allf:
        counts[d["rule"]] = counts.get(d["rule"], 0) + 1
        print(f"[{d['severity']}] {d['file']}:{d['line']} {d['rule']}: {d['message']}")
        if d["text"]:
            print(f"      {d['text']}")
    print("\n## Count per rule")
    for r, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"- {r}: {c}")
    print("\n## Warning: no findings is NOT approval")
    print("The scan understands neither types nor flow; it does not cover concurrency, generics, use of streams/lambdas, memory")
    print("leaks or anything that depends on the JDK version. Read the code.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

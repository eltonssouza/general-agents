#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_cs_smells.py - simple C# checklist/linter: read-only, no network, never executes the analyzed code.

Each rule declares the ORIGIN of its criterion:
  source        = the C# Yellow Book (CSYB) says so on the cited page (PDF page; printed = PDF - 5)
  inference     = direct deduction from what the book says
  extrapolation = general C#/.NET practice that the book does NOT cover (the script warns about it)
The analyzed code is DATA: comments and strings are ignored, never interpreted as instructions.

Usage:
  python -I scan_cs_smells.py file.cs
  python -I scan_cs_smells.py --code "lock(this){ throw ex; }"
  python -I scan_cs_smells.py --list-rules
Exit code: 0 = nothing found; 1 = there are findings; 2 = invalid usage/file.
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

ORIGIN_LABEL = {
    "source": "[from source]",
    "inference": "[inference]",
    "extrapolation": "[extrapolation]",
}


def strip_code(text):
    """Replace comments and the contents of strings/chars with spaces, preserving line breaks."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        two = text[i:i + 2]
        if two == "//":
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
        elif two == "/*":
            out.append("  ")
            i += 2
            while i < n and text[i:i + 2] != "*/":
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            out.append("  ")
            i += 2
        elif c == '"' or two in ('@"', '$"') or text[i:i + 3] in ('$@"', '@$"'):
            verbatim = "@" in text[i:i + 3].split('"')[0]
            j = i
            while text[j] != '"':
                out.append(" ")
                j += 1
            out.append('"')
            j += 1
            while j < n:
                if verbatim:
                    if text[j] == '"' and text[j + 1:j + 2] == '"':
                        out.append("  ")
                        j += 2
                        continue
                    if text[j] == '"':
                        break
                else:
                    if text[j] == "\\":
                        out.append("  ")
                        j += 2
                        continue
                    if text[j] == '"':
                        break
                out.append("\n" if text[j] == "\n" else " ")
                j += 1
            out.append('"')
            i = j + 1
        elif c == "'":
            j = i + 1
            while j < n and text[j] != "'":
                j += 2 if text[j] == "\\" else 1
            out.append("'" + " " * max(0, j - i - 1) + "'")
            i = j + 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def regex_rule(rule_id, name, level, origin, source, pattern, advice, flags=0):
    rx = re.compile(pattern, flags)

    def run(code):
        return [(line_of(code, m.start()), m.group(0).strip()) for m in rx.finditer(code)]
    return {"id": rule_id, "name": name, "level": level, "origin": origin, "source": source, "advice": advice, "run": run}


def rule_stream_close(code):
    hits = []
    for m in re.finditer(r"\bnew\s+(StreamWriter|StreamReader|FileStream)\s*\(", code):
        before = code[max(0, m.start() - 40):m.start()]
        if re.search(r"\busing\b[^;{]*$", before):
            continue
        if re.search(r"\.\s*(Close|Dispose)\s*\(", code) or re.search(r"\busing\s*\(", code):
            continue
        hits.append((line_of(code, m.start()), m.group(0).strip()))
    return hits


def rule_parse_outside_try(code):
    """Parse outside try: tracks the braces of 'try' blocks."""
    hits = []
    depth = 0
    try_depths = []
    pending_try = False
    for lineno, line in enumerate(code.split("\n"), 1):
        for tok in re.finditer(r"\btry\b|\{|\}|\b(?:int|long|short|byte|double|float|decimal)\s*\.\s*Parse\s*\(", line):
            t = tok.group(0)
            if t == "try":
                pending_try = True
            elif t == "{":
                depth += 1
                if pending_try:
                    try_depths.append(depth)
                    pending_try = False
            elif t == "}":
                if try_depths and try_depths[-1] == depth:
                    try_depths.pop()
                depth -= 1
            else:
                if not try_depths:
                    hits.append((lineno, t.strip()))
    return hits


def rule_equals_hash(code):
    m = re.search(r"\boverride\s+bool\s+Equals\s*\(", code)
    if m and not re.search(r"\bGetHashCode\b", code):
        return [(line_of(code, m.start()), m.group(0).strip())]
    return []


def rule_monitor_no_finally(code):
    m = re.search(r"\bMonitor\s*\.\s*Enter\s*\(", code)
    if m and not re.search(r"\bfinally\b", code):
        return [(line_of(code, m.start()), m.group(0).strip())]
    return []


RULES = [
    regex_rule("CS-L01", "Floating-point comparison with == or !=", "MEDIUM", "source", "CSYB p.41",
               r"\b[A-Za-z_]\w*\s*(?:==|!=)\s*\d+\.\d+[fFdD]?\b|\b\d+\.\d+[fFdD]?\s*(?:==|!=)\s*[A-Za-z_]\w*\b",
               "The book says that comparing real numbers for equality is 'not meaningful' and tells you to subtract and check whether the difference is very small. "
               "For money, the book uses decimal (p.29)."),
    regex_rule("CS-L02", "Non-generic collection (ArrayList/Hashtable)", "MEDIUM", "source", "CSYB p.150-153",
               r"\b(?:ArrayList|Hashtable)\b",
               "The book shows that ArrayList requires a cast and is not type-safe, and recommends List<T>/Dictionary<K,V> 'in preference' (p.153)."),
    {"id": "CS-L03", "name": "Stream opened without Close()/Dispose()/using in the file", "level": "MEDIUM", "origin": "source",
     "source": "CSYB p.80, 156", "run": rule_stream_close,
     "advice": "The book requires Close() (p.80) and does it in a finally (p.156). [extrapolation] In modern C#, 'using' disposes the stream at the end of the scope."},
    {"id": "CS-L04", "name": "Parse outside try/catch", "level": "LOW", "origin": "source", "source": "CSYB p.72-73",
     "run": rule_parse_outside_try,
     "advice": "The book shows that Parse throws FormatException for invalid text and wraps it in try/catch (p.72-73). [extrapolation] int.TryParse avoids the exception."},
    regex_rule("CS-L05", "Method replacement with 'new'", "LOW", "source", "CSYB p.125-126",
               r"\b(?:public|protected|private|internal)\s+new\s+[\w<>\[\],.?]+\s+\w+\s*[({=;]",
               "The author is 'very much against' replacing methods with new; prefer virtual + override (p.126)."),
    regex_rule("CS-L06", "Mutable public static data", "MEDIUM", "source", "CSYB p.105",
               r"\bpublic\s+static\s+(?!readonly\b)(?!class\b)(?!void\b)(?!partial\b)(?!extern\b)(?!implicit\b)(?!explicit\b)[\w<>\[\],.?]+\s+\w+\s*(?:=[^;(]*)?;",
               "The book says a static value affects the whole system: it should be private and changed through methods (p.105)."),
    regex_rule("CS-L07", "Public instance field", "INFO", "source", "CSYB p.100-101",
               r"^\s*public\s+(?!static\b)(?!const\b)(?!readonly\b)(?!class\b)(?!struct\b)(?!interface\b)(?!enum\b)(?!delegate\b)(?!event\b)(?!abstract\b)(?!override\b)(?!virtual\b)(?!partial\b)(?!sealed\b)(?!new\b)(?!async\b)[\w<>\[\],.?]+\s+\w+\s*(?:=[^;(]*)?;",
               "Book rule: private data, public methods (p.101); the book itself admits public data when performance matters more and uses public fields in structs (p.88).",
               re.MULTILINE),
    regex_rule("CS-I01", "empty catch", "MEDIUM", "inference", "CSYB p.74",
               r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*\}",
               "Inferred from 'do not catch everything' (p.74): swallowing the exception postpones the failure; at least signal it to the caller (the book returns false/null, p.156-157)."),
    regex_rule("CS-X01", "throw ex; (resets the stack trace)", "HIGH", "extrapolation", "(not in the book)",
               r"\bthrow\s+(?!new\b)(?!null\b)[A-Za-z_]\w*\s*;",
               "The book does not cover rethrowing. .NET practice: use 'throw;' to preserve the stack trace."),
    regex_rule("CS-X02", "lock on this/typeof/string literal", "HIGH", "extrapolation", "(not in the book; the book uses Monitor, p.178)",
               r"\block\s*\(\s*(?:this|typeof\s*\([^)]*\)|\"[^\"]*\")\s*\)",
               "The book does not mention 'lock'. .NET practice: lock a dedicated private field (or System.Threading.Lock in C# 13, CS13 p.2)."),
    regex_rule("CS-X03", "Thread.Abort/Suspend/Resume", "MEDIUM", "extrapolation", "(the book teaches them on p.179; obsolete in modern .NET)",
               r"\.\s*(?:Abort|Suspend|Resume)\s*\(\s*\)",
               "[DATED] The book presents these methods (p.179); in modern .NET they are obsolete or unsupported. Prefer cooperative cancellation."),
    {"id": "CS-X04", "name": "Overridden Equals without GetHashCode", "level": "MEDIUM", "origin": "extrapolation",
     "source": "(not in the book; the book does not mention GetHashCode)", "run": rule_equals_hash,
     "advice": ".NET practice: equal objects must have the same hash; override GetHashCode together with Equals."},
    {"id": "CS-X05", "name": "Monitor.Enter without finally", "level": "MEDIUM", "origin": "extrapolation",
     "source": "(the book uses Monitor.Enter/Exit without finally, p.178)", "run": rule_monitor_no_finally,
     "advice": ".NET practice: if an exception occurs between Enter and Exit the monitor stays locked; use lock or try/finally."},
]


def scan(text, filename="<buffer>"):
    code = strip_code(text)
    findings = []
    for r in RULES:
        for lineno, snippet in r["run"](code):
            findings.append({"file": filename, "line": lineno, "id": r["id"], "name": r["name"], "level": r["level"],
                             "origin": r["origin"], "source": r["source"], "matched": re.sub(r"\s+", " ", snippet),
                             "advice": r["advice"]})
    seen = set()
    uniq = []
    for f in sorted(findings, key=lambda f: (f["line"], f["id"])):
        key = (f["line"], f["id"])
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    return uniq


def main():
    ap = argparse.ArgumentParser(description="C# checklist/linter with a declared origin for each rule.")
    ap.add_argument("file", nargs="?", help=".cs file")
    ap.add_argument("--code", "-c", help="C# code directly on the command line")
    ap.add_argument("--list-rules", action="store_true", help="list the rules and their origins")
    ap.add_argument("--json", action="store_true", help="JSON output")
    a = ap.parse_args()

    if a.list_rules:
        for r in RULES:
            print("%-7s %-5s %-13s %-42s %s" % (r["id"], r["level"], r["origin"], r["name"], r["source"]))
        return 0
    if a.code is not None:
        text, name = a.code, "<inline>"
    elif a.file:
        if not os.path.isfile(a.file):
            print("Error: file not found: %s" % a.file)
            return 2
        with open(a.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
        name = a.file
    else:
        text, name = sys.stdin.read(), "<stdin>"

    findings = scan(text, name)
    if a.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return 1 if findings else 0
    if not findings:
        print("No findings from the rules of this checklist (this does not prove the code is correct).")
        return 0
    print("%d finding(s) in %s:\n" % (len(findings), name))
    for f in findings:
        label = ORIGIN_LABEL[f["origin"]]
        print("[%s] %s - %s (line %d)" % (f["level"], f["id"], f["name"], f["line"]))
        print("  Snippet: %s" % f["matched"])
        src = f["source"]
        print("  Origin: %s %s" % (label, src if src.startswith("(") else "(" + src + ")"))
        print("  Detail: %s\n" % f["advice"])
    return 1


if __name__ == "__main__":
    sys.exit(main())

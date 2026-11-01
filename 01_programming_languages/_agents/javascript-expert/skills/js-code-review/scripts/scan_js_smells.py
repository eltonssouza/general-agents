#!/usr/bin/env python3
"""Static regex scan for points of attention in JavaScript code (read-only, no network).

Usage:
    python -I scan_js_smells.py [--json] PATH [PATH ...]

PATH can be a file (.js, .mjs, .cjs) or a directory (recursive; skips .git, node_modules,
dist, build, coverage, .next, out). It does NOT run or evaluate the code.

It is a lexical triage by regex: it indicates WHERE to look and may have false positives/negatives.
"No findings" does NOT mean approval. Each rule cites the exact page of the sources
(Spec = ECMA-262 17th ed. ES2026; EJpt = Eloquent JS PT-BR; EJ1 = Eloquent JS 1st ed.).
Exit code: 0 if it ran; 2 for a usage error.
"""
import argparse
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "dist", "build", "coverage", ".next", "out", ".cache"}
JS_EXTS = (".js", ".mjs", ".cjs")


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in sorted(files):
                    if f.endswith(JS_EXTS):
                        yield os.path.join(root, f)
        else:
            print(f"warning: path does not exist: {p}", file=sys.stderr)


def strip_line(line, state):
    """Removes comments and the interior of single/double-quoted strings (keeps the delimiters)."""
    out, i, n = [], 0, len(line)
    while i < n:
        if state["block"]:
            j = line.find("*/", i)
            if j < 0:
                return "".join(out)
            state["block"] = False
            i = j + 2
            continue
        if line.startswith("/*", i):
            state["block"] = True
            i += 2
            continue
        if line.startswith("//", i):
            break
        c = line[i]
        if c in ('"', "'"):
            q = c
            out.append(q)
            i += 1
            while i < n and line[i] != q:
                i += 2 if line[i] == "\\" else 1
            out.append(q)
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


RX_VAR = re.compile(r"\bvar\s+[A-Za-z_$[{]")
RX_LOOSE_EQ = re.compile(r"(?<![=!<>])(?:==|!=)(?!=)")
RX_NULL_CHECK = re.compile(r"(?:==|!=)\s*null\b|\bnull\s*(?:==|!=)")
RX_GLOBAL_ISNAN = re.compile(r"(?<![.\w$])isNaN\s*\(")
RX_ASYNC_FOREACH = re.compile(r"\.forEach\s*\(\s*async\b")
RX_EMPTY_CATCH = re.compile(r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*\}")
RX_EVAL_FUNC = re.compile(r"(?<![.\w$])eval\s*\(|\bnew\s+Function\s*\(")
RX_TIMER_STR = re.compile(r"\b(?:setTimeout|setInterval)\s*\(\s*['\"]")
RX_WITH = re.compile(r"(?<![.\w$])with\s*\(")
RX_FOR_IN = re.compile(r"\bfor\s*\([^;]*\bin\b[^)]*\)")
RX_SORT_EMPTY = re.compile(r"\.sort\s*\(\s*\)")
RX_ANNEX_B = re.compile(
    r"\b(?:__proto__|__defineGetter__|__defineSetter__|__lookupGetter__|__lookupSetter__)\b"
    r"|\.(?:substr|getYear|setYear|toGMTString|anchor|big|blink|bold|fixed|fontcolor|fontsize|italics|small|strike|sub|sup)\s*\("
    r"|(?<![.\w$])(?:escape|unescape)\s*\("
)
RX_FINALLY_JUMP = re.compile(r"\bfinally\s*\{[^}]*\b(?:return|throw)\b")


def scan_file(path):
    findings = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            raw = fh.read().splitlines()
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
        return findings

    st = {"block": False}
    code = [strip_line(l, st) for l in raw]

    def add(i, rule, sev, msg):
        findings.append(
            dict(
                file=path,
                line=i + 1,
                rule=rule,
                severity=sev,
                message=msg,
                text=raw[i].strip()[:140],
            )
        )

    for i, c in enumerate(code):
        if RX_VAR.search(c):
            add(
                i,
                "var-declaration",
                "medium",
                "use of 'var' [DATED]: function/global scope and hoisting with undefined; prefer 'const' or 'let' "
                "(EJpt p.30-32, p.52-53; Spec p.326-329)",
            )
        if RX_LOOSE_EQ.search(c) and not RX_NULL_CHECK.search(c):
            add(
                i,
                "loose-equality",
                "medium",
                "use of == or != (outside == null): triggers implicit coercion (IsLooselyEqual); prefer === and !== "
                "(EJpt p.24-25; Spec p.101-102)",
            )
        if RX_GLOBAL_ISNAN.search(c):
            add(
                i,
                "global-isnan",
                "medium",
                "global isNaN() converts the argument to Number before testing; prefer Number.isNaN() "
                "(EJpt p.36; Spec p.453, p.488-489)",
            )
        if RX_ASYNC_FOREACH.search(c):
            add(
                i,
                "async-foreach",
                "high",
                "forEach with an async callback does not await the returned Promises [inference: EJpt does not cover forEach with await; "
                "Spec p.627]; use 'for...of' (in series) or 'await Promise.all(arr.map(...))' (EJpt p.111, p.250, p.255, p.258-259)",
            )
        multi_empty = False
        if re.search(r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*$", c):
            for k in range(i + 1, min(len(code), i + 4)):
                if code[k].strip():
                    multi_empty = code[k].strip() == "}"
                    break
        if RX_EMPTY_CATCH.search(c) or multi_empty:
            add(
                i,
                "empty-catch",
                "high",
                "empty catch block silently swallows exceptions; filter with instanceof and rethrow unexpected errors "
                "(EJpt p.181-183)",
            )
        if RX_EVAL_FUNC.search(c) or RX_TIMER_STR.search(c):
            add(
                i,
                "eval-or-code-string",
                "high",
                "dynamic string execution (eval / new Function / timer with a string) [DATED]: security and "
                "scope risk; prefer JSON.parse or regular functions (EJpt p.228 covers only Function; EJ1 p.145, p.168, p.234; Spec p.449-450, p.471)",
            )
        if RX_WITH.search(c):
            add(
                i,
                "with-statement",
                "high",
                "'with' statement [DATED]: marked LEGACY and forbidden in strict mode (SyntaxError) "
                "(Spec p.347, p.861; EJpt p.170)",
            )
        if RX_FOR_IN.search(c):
            window = " ".join(code[i : min(len(code), i + 5)])
            if "hasOwn" not in window and "hasOwnProperty" not in window:
                add(
                    i,
                    "for-in-prototype",
                    "medium",
                    "for...in enumerates own and inherited string keys; prefer Object.keys/entries with for...of or "
                    "filter with Object.hasOwn (Spec p.343, p.464; EJpt p.80, p.136-138)",
                )
        if RX_SORT_EMPTY.search(c):
            add(
                i,
                "array-sort-default",
                "low",
                ".sort() without a comparator sorts by converting elements to String (UTF-16: '10' before '9') and mutates the "
                "array; pass (a, b) => a - b for numbers (Spec p.636-638)",
            )
        if RX_ANNEX_B.search(c):
            add(
                i,
                "legacy-annex-b",
                "medium",
                "legacy Annex B / Normative Optional feature [DATED] (__proto__, substr, getYear, escape, String "
                "HTML methods); discouraged in new code (Spec p.468-469, p.843, p.849-855; EJpt p.198)",
            )
        if RX_FINALLY_JUMP.search(c):
            add(
                i,
                "finally-abrupt",
                "high",
                "return/throw in finally replaces the pending return or exception of the try/catch (Spec p.354)",
            )

    return findings


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
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
    print(f"# JavaScript scan (regex) — {n} file(s) — {len(allf)} finding(s)")
    print("# Read-only triage: confirm each item by reading the code and its context.\n")
    counts = {}
    for d in allf:
        counts[d["rule"]] = counts.get(d["rule"], 0) + 1
        print(f"[{d['severity']}] {d['file']}:{d['line']} {d['rule']}: {d['message']}")
        if d["text"]:
            print(f"      {d['text']}")
    print("\n## Count by rule")
    for r, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"- {r}: {c}")
    print("\n## Attention: no findings is NOT approval")
    print("The scan is lexical by regex; it does not build an AST, does not resolve scopes or types and does not replace reading the code.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

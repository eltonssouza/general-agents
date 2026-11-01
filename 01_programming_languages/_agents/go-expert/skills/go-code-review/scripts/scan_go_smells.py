#!/usr/bin/env python3
"""Deterministic scan for points of attention in Go code.

Uso:
    python -I scan_go_smells.py [--json] CAMINHO [CAMINHO ...]

CAMINHO (PATH) may be a .go file or a directory (recursive; skips vendor/, .git/, testdata/).
It only reads files; it never touches the network or writes anything. Output is text (default) or JSON.

This is regex triage (it does not understand the AST): it points to WHERE to look, it does not prove a defect.
Version-sensitive rules read the `go X.Y` line of the nearest go.mod; without a go.mod,
those rules are turned off and the report says so. Exit code: 0 if it ran; 2 usage.
Limitation: the `for` loop heuristic counts braces and ignores strings and block comments.
"""
import argparse
import json
import os
import re
import sys

SKIP_DIRS = {"vendor", ".git", "testdata", "node_modules"}


def find_gomod_version(path):
    d = os.path.abspath(path if os.path.isdir(path) else os.path.dirname(path))
    while True:
        gm = os.path.join(d, "go.mod")
        if os.path.isfile(gm):
            try:
                with open(gm, encoding="utf-8", errors="replace") as fh:
                    for line in fh:
                        m = re.match(r"\s*go\s+(\d+)\.(\d+)", line)
                        if m:
                            return (int(m.group(1)), int(m.group(2)))
            except OSError:
                pass
            return None
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(".go"):
                yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
                for f in sorted(files):
                    if f.endswith(".go"):
                        yield os.path.join(root, f)
        else:
            print(f"warning: path does not exist: {p}", file=sys.stderr)


def strip_comment(line):
    in_str = False
    q = ""
    i = 0
    while i < len(line):
        c = line[i]
        if in_str:
            if c == "\\" and q != "`":
                i += 2
                continue
            if c == q:
                in_str = False
        else:
            if c in "\"`'":
                in_str, q = True, c
            elif line.startswith("//", i):
                return line[:i]
        i += 1
    return line


# (id, severity, regex, message, production_only)
RULES = [
    ("rand-seed", "medium", re.compile(r"\brand\.Seed\s*\("),
     "rand.Seed: the global generator is seeded automatically since Go 1.20 and Seed is deprecated; "
     "in Go 1.24 it becomes a no-op (randseednop). For a reproducible sequence use rand.New(rand.NewSource(...)) "
     "(RN1.20 p.11-12; RN1.24 p.12)", False),
    ("getter-get-prefix", "low", re.compile(r"^\s*func\s+\(\s*\w+\s+\*?\w+\s*\)\s+Get[A-Z]\w*\s*\("),
     "getter with a Get prefix: the convention is Owner(), not GetOwner() (Eff p.4)", False),
    ("panic-nil", "medium", re.compile(r"\bpanic\s*\(\s*nil\s*\)"),
     "panic(nil): since Go 1.21 it raises *runtime.PanicNilError (GODEBUG panicnil=1 restores the old behavior) (RN1.21 p.3; Spec p.105)", False),
    ("recover-eq-nil", "medium", re.compile(r"\brecover\s*\(\s*\)\s*(==|!=)\s*nil|:=\s*recover\s*\(\s*\)\s*;\s*\w+\s*(==|!=)\s*nil"),
     "recover() compared to nil: the semantics changed in Go 1.21 (panic(nil)); review the panic detection (RN1.21 p.3)", False),
    ("lock-no-defer", "medium", None,
     "Lock() without 'defer ...Unlock()' in the next 2 lines: deadlock risk from a forgotten Unlock (Little p.74-76)", True),
    ("sleep-sync", "low", re.compile(r"\btime\.Sleep\s*\("),
     "time.Sleep: do not use it to wait for goroutines (too short or wasteful); the Little Go Book uses Sleep only to show that main exits without waiting and marks it as bad (Little p.73, p.76); WaitGroup is not in the sources: synchronize with a channel/mutex (Little p.77-81) or, if you use WaitGroup, label it [extrapolation]", True),
    ("tools-go", "info", re.compile(r"^\s*//go:build\s+tools\b"),
     "tools.go pattern: Go 1.24 offers the `tool` directive in go.mod (RN1.24 p.2-3)", False),
    ("linkname", "medium", re.compile(r"^\s*//go:linkname\b"),
     "//go:linkname: the linker restricts references to internal symbols (-checklinkname=0 turns it off) (RN1.23 p.3; RN1.24)", False),
    ("redundant-loopvar", "info", None,
     "'x := x' at the start of the loop: with per-iteration semantics (go >= 1.22) it is unnecessary [inference: the notes do not say the idiom stops being necessary]", False),
]

FOR_OPEN = re.compile(r"^\s*for\b.*\{\s*$")
GO_FUNC = re.compile(r"\bgo\s+func\s*\(")
DEFER = re.compile(r"^\s*defer\b")
LOCK = re.compile(r"\.\s*(R?Lock)\s*\(\s*\)\s*$")
SELF_ASSIGN = re.compile(r"^\s*(\w+)\s*:=\s*(\w+)\s*$")
IGNORED_RESULT = re.compile(r"^\s*\w+\s*,\s*_\s*:?=\s*[\w.]+\(")


def scan_file(path, gover):
    findings = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
        return findings
    is_test = path.endswith("_test.go")
    codes = [strip_comment(l) for l in lines]
    depth = 0
    for_stack = []   # depths at which `for` loops were opened
    pending_loop_first = None

    def add(idx, rid, sev, msg):
        findings.append(dict(file=path, line=idx + 1, rule=rid, severity=sev,
                             context="test" if is_test else "production",
                             message=msg, text=lines[idx].strip()[:140]))

    for idx, code in enumerate(codes):
        raw = lines[idx]
        in_for = bool(for_stack)
        for rid, sev, rx, msg, prod_only in RULES:
            if rx is None or (prod_only and is_test):
                continue
            target = raw if rid in ("tools-go", "linkname") else code
            if rx.search(target):
                add(idx, rid, sev, msg)

        if LOCK.search(code) and not is_test:
            nxt = " ".join(codes[idx + 1: idx + 3])
            if not re.search(r"\bdefer\b.*Unlock\s*\(", nxt):
                add(idx, "lock-no-defer", "medium", RULES[4][3])

        if IGNORED_RESULT.search(code) and not is_test:
            add(idx, "ignored-result", "low",
                "second return value discarded with '_' (e.g. f, _ := os.Open(...)): if it is an error, handle it "
                "(see references/casos-e-antipadroes.md §2.10)")

        if in_for and re.match(r"^\s*default:\s*$", code) and any(
                "select" in c and "{" in c for c in codes[max(0, idx - 8): idx]):
            add(idx, "select-default-loop", "low",
                "select with default inside a loop: without blocking it becomes a busy wait; confirm the intent "
                "(references/regras-da-spec.md and Little p.80-81)")

        if in_for and DEFER.search(code):
            add(idx, "defer-in-loop", "medium",
                "defer inside a loop: the deferred call runs before the function returns (Spec p.97), so only at the end of the FUNCTION; that this accumulates resources is [inference]")

        if GO_FUNC.search(code) and in_for and gover is not None and gover < (1, 22):
            add(idx, "loopvar-goroutine", "high",
                f"goroutine in a loop with go.mod at go {gover[0]}.{gover[1]} (< 1.22): the loop variable is "
                "shared across iterations (Eff p.44; per-iteration semantics only since Go 1.22, RN1.22)")

        if pending_loop_first is not None:
            m = SELF_ASSIGN.match(code)
            if m and m.group(1) == m.group(2) and gover is not None and gover >= (1, 22):
                add(idx, "redundant-loopvar", "info", RULES[-1][3])
            pending_loop_first = None
        if FOR_OPEN.search(code):
            pending_loop_first = idx

        opens = code.count("{")
        closes = code.count("}")
        if FOR_OPEN.search(code):
            for_stack.append(depth)
        depth += opens - closes
        while for_stack and depth <= for_stack[-1]:
            for_stack.pop()
    return findings


def main(argv):
    try:  # the Windows console defaults to cp1252; force UTF-8 for accented characters
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    all_f, nfiles, versions = [], 0, set()
    for f in iter_files(args.paths):
        nfiles += 1
        gv = find_gomod_version(f)
        versions.add(gv)
        all_f.extend(scan_file(f, gv))
    order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    all_f.sort(key=lambda d: (order[d["severity"]], d["file"], d["line"]))

    vtxt = ", ".join(sorted({f"go {v[0]}.{v[1]}" if v else "go.mod not found" for v in versions})) or "-"
    if args.json:
        json.dump(dict(files_scanned=nfiles, go_versions=vtxt, findings=all_f), sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    print(f"# Go scan — {nfiles} .go file(s) — versions: {vtxt} — {len(all_f)} finding(s)")
    if None in versions:
        print("# Warning: without a go.mod, the version-sensitive rules (loopvar-goroutine, redundant-loopvar) are turned off.")
    print("# Regex triage: it indicates where to look; confirm each item by reading the code.\n")
    counts = {}
    for d in all_f:
        counts[d["rule"]] = counts.get(d["rule"], 0) + 1
        if d["severity"] == "info":
            continue
        print(f"[{d['severity']}] {d['file']}:{d['line']} ({d['context']}) {d['rule']}: {d['message']}")
        print(f"      {d['text']}")
    print("\n## Count by rule")
    for r, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"- {r}: {n}")
    print("\n## Attention: zero findings is NOT an approval")
    print("The scan does not cover: nil inside an interface, defer before checking the error, nil channel, double close,")
    print("data races, generics and type semantics. Read the code.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Reads a go.mod and shows which behaviors depend on the `go` line (Go 1.20-1.24).

Usage:
    python -I check_gomod.py [--target 1.24] PATH_TO_go.mod_OR_DIRECTORY

Read-only; no network. The data comes from the Go 1.20-1.24 release notes and the Spec
(references: references/versoes-e-migracao.md). Nothing here covers Go 1.25+.

Output: (1) what the go.mod declares (go, toolchain, godebug); (2) language/tool features
available or not with that line; (3) behavior changes that only apply from a certain
`go` line (active / still in old mode); (4) GODEBUG settings introduced after your line;
(5) what raising the line up to --target would bring.
Exit code: 0 if it read the file; 2 usage or missing go.mod.
"""
import argparse
import os
import re
import sys

# (minimum version, feature, note, source)
LANG = [
    ((1, 18), "generics, ~T, any, comparable", "", "Spec p.115"),
    ((1, 20), "slice -> array conversion [N]T(s); unsafe.SliceData/String/StringData", "", "RN1.20 p.1"),
    ((1, 21), "built-ins min, max, clear", "", "RN1.21 p.1"),
    ((1, 21), "`go` line is a strict minimum; `toolchain` directive; toolchain download", "", "RN1.21 p.3"),
    ((1, 22), "for i := range N (range over an integer)", "", "RN1.22 p.1-2"),
    ((1, 23), "range over an iterator function (func(func() bool), func(func(K) bool), func(func(K, V) bool); `iter` package)", "preview in 1.22 via experiment", "RN1.23 p.1; RN1.22 p.2"),
    ((1, 23), "`godebug` directive in go.mod/go.work", "", "RN1.23 p.2"),
    ((1, 24), "generic type alias", "preview in 1.23", "RN1.24 p.1"),
    ((1, 24), "`tool` directive in go.mod (replaces the tools.go pattern)", "", "RN1.24 p.2"),
    ((1, 26), "new(expr) (version only from Effective Go p.15)", "Spec p.104 does not state the version and there are no 1.26 release notes [inference]", "Eff p.15; Spec p.104"),
]

# (version at which the change takes effect with the go line, description, old behavior, source)
GATED = [
    ((1, 21), "panic(nil) raises *runtime.PanicNilError; recover() no longer returns nil on panic",
     "with `go 1.20` or lower the GODEBUG panicnil=1 is turned on automatically", "RN1.21 p.3"),
    ((1, 22), "per-iteration loop variable (3-clause for and range) [inference: the link to the `go` line is not stated literally in the notes]",
     "before: one variable shared across iterations (Eff p.44); keeping the old `go` line as a rollback is [inference] (general rule of RN1.21 p.3 + RN1.22 p.3)", "RN1.22 p.1, p.3; Eff p.44"),
    ((1, 23), "Timer/Ticker: unbuffered channel, len/cap == 0 (requires go 1.23.0 or higher)",
     "before: buffered channel; asynctimerchan=1 reverts", "RN1.23 p.4"),
]

# (version, GODEBUG key, summary, source)
GODEBUGS = [
    ((1, 20), "randautoseed", "global generator seeded randomly (=0 restores)", "RN1.20 p.11-12"),
    ((1, 20), "tarinsecurepath", "archive/tar: ErrInsecurePath", "RN1.20 p.8"),
    ((1, 20), "zipinsecurepath", "archive/zip: ErrInsecurePath", "RN1.20 p.8"),
    ((1, 21), "panicnil", "panic(nil) becomes PanicNilError (=1 reverts)", "RN1.21 p.3"),
    ((1, 22), "httpmuxgo121", "new ServeMux with methods and wildcards (=1 reverts)", "RN1.22 p.6"),
    ((1, 22), "httplaxcontentlength", "rejects empty Content-Length (=1 reverts)", "RN1.22 p.10"),
    ((1, 22), "tlsunsafeekm", "strict ExportKeyingMaterial (=1 reverts)", "RN1.22 p.7"),
    ((1, 22), "tls10server", "TLS 1.2 minimum on the server (=1 reverts)", "RN1.22 p.7"),
    ((1, 22), "tlsrsakex", "no RSA key exchange cipher suites (=1 reverts)", "RN1.22 p.7"),
    ((1, 23), "asynctimerchan", "Timer/Ticker channel (=1 reverts)", "RN1.23 p.4"),
    ((1, 23), "httpservecontentkeepheaders", "keeps headers in error responses (=1 reverts)", "RN1.23 p.8"),
    ((1, 23), "tls3des", "3DES in the default list (=1 reverts)", "RN1.23 p.5"),
    ((1, 24), "gotestjsonbuildtext", "go test -json with build text (=1 reverts)", "RN1.24 p.2"),
    ((1, 24), "rsa1024min", "RSA keys < 1024 bits fail (=0 reverts)", "RN1.24 p.8"),
    ((1, 24), "tlsmlkem", "X25519MLKEM768 by default (=0 reverts)", "RN1.24 p.9"),
    ((1, 24), "x509rsacrt", "strict CRT parsing in RSA (=0 reverts)", "RN1.24 p.9-10"),
    ((1, 24), "randseednop", "rand.Seed has no effect (=0 reverts)", "RN1.24 p.12"),
]


def parse_ver(s):
    m = re.match(r"\s*(\d+)\.(\d+)(?:\.(\d+))?", s or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


def fmt(v):
    return f"{v[0]}.{v[1]}"


def read_gomod(path):
    info = dict(go=None, go_raw=None, toolchain=None, godebug=[], tools=[], module=None)
    block = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.split("//", 1)[0].strip()
            if not line:
                continue
            if block:
                if line == ")":
                    block = None
                    continue
                if block == "godebug":
                    info["godebug"].append(line)
                elif block == "tool":
                    info["tools"].append(line)
                continue
            m = re.match(r"(go|toolchain|module)\s+(\S+)", line)
            if m:
                key, val = m.groups()
                if key == "go":
                    info["go_raw"], info["go"] = val, parse_ver(val)
                else:
                    info[key] = val
                continue
            m = re.match(r"(godebug|tool)\s*\($", line)
            if m:
                block = m.group(1)
                continue
            m = re.match(r"godebug\s+(\S+)", line)
            if m:
                info["godebug"].append(m.group(1))
                continue
            m = re.match(r"tool\s+(\S+)", line)
            if m:
                info["tools"].append(m.group(1))
    return info


def main(argv):
    try:  # the Windows console defaults to cp1252; force UTF-8 for accented characters
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--target", default="1.24", help="target version of the migration (default 1.24)")
    a = ap.parse_args(argv)
    p = a.path
    if os.path.isdir(p):
        p = os.path.join(p, "go.mod")
    if not os.path.isfile(p):
        print(f"error: go.mod not found: {p}", file=sys.stderr)
        return 2
    tgt = parse_ver(a.target)
    if not tgt:
        print("error: invalid --target", file=sys.stderr)
        return 2
    info = read_gomod(p)
    cur = info["go"]
    print(f"# go.mod: {p}")
    print(f"- module: {info['module']}")
    print(f"- go: {info['go_raw'] or '(missing)'}   toolchain: {info['toolchain'] or '(not declared)'}")
    print(f"- godebug: {', '.join(info['godebug']) if info['godebug'] else '(none)'}   tool: {', '.join(info['tools']) if info['tools'] else '(none)'}")
    if not cur:
        print("\nNo readable `go` line: nothing to evaluate. (Without the line, the version semantics cannot be inferred.)")
        return 0
    if cur > (1, 24):
        print(f"\nWarning: go {fmt(cur)} is later than what the sources cover (release notes up to 1.24); the data below may be incomplete.")
    if cur < (1, 20):
        print(f"\nWarning: go {fmt(cur)} is earlier than 1.20; the release notes covered start at 1.20.")

    if info["godebug"] and cur < (1, 23):
        print(f"\nWARNING: the go.mod uses the `godebug` directive, which only exists from 1.23 onward (RN1.23 p.2), but the line is go {fmt(cur)}.")
    if info["tools"] and cur < (1, 24):
        print(f"\nWARNING: the go.mod uses the `tool` directive, which only exists from 1.24 onward (RN1.24 p.2), but the line is go {fmt(cur)}.")
    print(f"\n## Language/tool features with `go {fmt(cur)}` (source in parentheses)")
    for v, feat, note, src in LANG:
        mark = "available" if cur >= v else f"NOT available (requires {fmt(v)})"
        print(f"- [{fmt(v)}] {feat}: {mark}" + (f" — {note}" if note else "") + f" ({src})")

    print("\n## Behavior changes gated by the `go` line")
    for v, desc, old, src in GATED:
        if cur >= v:
            print(f"- ACTIVE (go >= {fmt(v)}): {desc} ({src})")
        else:
            print(f"- OLD MODE (go < {fmt(v)}): {desc}. {old} ({src})")
    declared = {g.split("=")[0].strip() for g in info["godebug"]}
    print("\n## GODEBUG settings introduced AFTER your `go` line [inference: the notes say the `go` line selects the defaults (RN1.21 p.3), without repeating the case of each key]")
    later = [(v, k, s, src) for v, k, s, src in GODEBUGS if v > cur]
    for v, k, s, src in later:
        flag = " (already declared in go.mod)" if k in declared else ""
        print(f"- {k} (since {fmt(v)}): {s} ({src}){flag}")
    if not later:
        print("- none from the list")

    print(f"\n## What raising `go` {fmt(cur)} -> {fmt(tgt)} would bring (review each item in references/versoes-e-migracao.md, section 3)")
    if tgt <= cur:
        print("- nothing: the line is already at the target or above")
    else:
        for v, desc, old, src in GATED:
            if cur < v <= tgt:
                print(f"- {desc} ({src})")
        for v, k, s, src in GODEBUGS:
            if cur < v <= tgt:
                print(f"- GODEBUG {k}: {s} ({src}) [inference: defaults follow the `go` line, RN1.21 p.3]")
        for v, feat, note, src in LANG:
            if cur < v <= tgt:
                print(f"- becomes available: {feat} ({src})")
    print("\nNote: Go 1.25 and 1.26 have no release notes in the sources; only isolated marks in the Spec/Effective Go.")
    print("Note: this output consults a copied table of the release notes; it does not check the code or the project's real go.mod beyond reading the `go` line.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

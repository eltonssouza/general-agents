#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_ruby_smells.py - simple Ruby code checker whose rules come from the official Ruby 3.0 to 3.4 release notes.

Read-only, no network, heuristic (line by line). It is NOT a full linter: it does not interpret Ruby.
Each rule carries: source (R3x p.N = PDF page of the note), epistemic label and affected version.
  - label [from source]  : the described change/warning is on the cited page;
  - label [inference]    : suggestion derived from the text (INFO level);
  - [VERSION-DEPENDENT]  : only applies if the code runs on the indicated version or later.

Usage:
  python -I scan_ruby_smells.py file.rb
  python -I scan_ruby_smells.py --code 'File.exists?("x")'
  python -I scan_ruby_smells.py --json file.rb
  python -I scan_ruby_smells.py --list-rules
  python -I scan_ruby_smells.py --strict file.rb   # exit 1 if there is a HIGH finding
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

LABELS = {"from source": "from source", "inference": "inference", "extrapolation": "extrapolation"}
LEVEL_ORDER = {"HIGH": 0, "MEDIUM": 1, "INFO": 2}

# (id, level, label, version, source, regex, title, detail)
LINE_RULES = [
    ("R30-SAFE", "HIGH", "from source", "3.0+", "R30 p.7", r"\$SAFE\b",
     "$SAFE", "The note says the $SAFE feature was removed completely and became an ordinary global variable."),
    ("R32-REMOVED-CONST", "HIGH", "from source", "3.2+", "R32 p.16",
     r"\b(Fixnum|Bignum|Random::DEFAULT|Struct::Group|Struct::Passwd)\b",
     "constant removed in 3.2", "Deprecated constants removed in 3.2: Fixnum, Bignum, Random::DEFAULT, Struct::Group, Struct::Passwd."),
    ("R32-REMOVED-METHOD", "HIGH", "from source", "3.2+", "R32 p.16",
     r"\b(?:Dir|File)\.exists\?|\.(?:taint|untaint|tainted\?|untrust|untrusted\?)\b|\.trust\b",
     "method removed in 3.2", "Removed in 3.2: Dir.exists?, File.exists?, taint/untaint/tainted?, trust/untrust/untrusted?."),
    ("R33-REGEXP-NEW-3ARGS", "MEDIUM", "from source", "3.3+", "R33 p.6",
     r"Regexp\.(?:new|compile)\(\s*[^,()]+,\s*[^,()]+,\s*[^,()]+\)",
     "Regexp.new with 3 arguments", "Since 3.3 Regexp.new accepts at most 2 arguments (the third was deprecated in 3.2). Heuristic: confirm the call really has 3 arguments."),
    ("R34-REFINED-CLASS", "MEDIUM", "from source", "3.4+", "R34 p.9",
     r"\.refined_class\b",
     "Refinement#refined_class", "Added in 3.2 (R32 p.12) and removed in 3.4."),
    ("R34-TIMEOUT-NEGATIVE", "MEDIUM", "from source", "3.4+", "R34 p.10",
     r"Timeout\.timeout\(\s*-",
     "Timeout.timeout with a negative value", "3.4 rejects negative values in Timeout.timeout."),
    ("R34-DIDYOUMEAN", "MEDIUM", "from source", "3.4+", "R34 p.9",
     r"DidYouMean::SPELL_CHECKERS\s*(?:\[[^\]]*\]\s*=|\.merge!)",
     "DidYouMean::SPELL_CHECKERS[]= / merge!", "Removed in 3.4."),
    ("R34-NETHTTP-CONST", "MEDIUM", "from source", "3.4+", "R34 p.9",
     r"Net::(?:HTTP::ProxyMod|NetPrivate::HTTPRequest|HTTP(?:Information|Success|Redirection|Retriable|ClientError|FatalError|ServerError)Code|HTTPRes(?:ponse|ponce)Receiver)\b",
     "old Net::HTTP constant", "Constants deprecated since 2012 were removed in 3.4."),
    ("R33-IT-BARE", "INFO", "from source", "3.3/3.4", "R33 p.6; R34 p.1",
     r"\{\s*it(?![\w?!(\"'])",
     "`it` in a block without parameters", "In 3.3, calling `it` without arguments in a block without ordinary parameters is deprecated; in 3.4 `it` references the first parameter. Check the target version. (RSpec `it \"...\" do` is not affected: [extrapolation]; this alert is only for `{ it ... }`.)"),
    ("R30-IO-SELECT", "INFO", "from source", "3.0+", "R30 p.3",
     r"\bIO\.select\b",
     "IO.select", "The note lists IO#select as NOT supported by the Fiber Scheduler (version 3.0). If you use a scheduler, check the version documentation."),
    ("R31-PSYCH-LOAD", "INFO", "from source", "3.1+", "R31 p.8",
     r"\b(?:YAML|Psych)\.load\b(?!_)",
     "YAML.load / Psych.load", "Psych 4.0 (Ruby 3.1) makes Psych.load use safe_load by default: arbitrary types are no longer loaded without an explicit option."),
    ("R32-SET-REQUIRE", "INFO", "from source", "3.2+", "R32 p.15",
     r"""^\s*require\s+['"]set['"]""",
     "require \"set\"", "Since 3.2 Set is a built-in class (autoload) and needs no require; the require remains harmless."),
    ("INF-STRUCT", "INFO", "inference", "3.2+", "R32 p.11-12",
     r"\bStruct\.new\b",
     "Struct.new", "[inference] The note presents Data as an immutable value class similar to Struct, with a leaner and stricter API. Consider Data.define IF the object must not change; Struct remains valid and is not deprecated."),
]

# Regex literal with back-reference/look-around: the note says the memoization optimization does not cover these cases (R32 p.7).
REGEX_RISK = re.compile(r"\\[1-9]|\(\?(?:=|!|<=|<!)")
MUTATORS = r"(?:<<|\.concat\(|\.gsub!|\.sub!|\.upcase!|\.downcase!|\.capitalize!|\.swapcase!|\.strip!|\.chomp!|\.chop!|\.squeeze!|\.replace\(|\.insert\(|\.prepend\(|\.clear\b|\.setbyte\()"
STR_ASSIGN = re.compile(r"""^\s*(@{0,2}\$?[A-Za-z_]\w*)\s*=\s*(["'])(?:(?!\2)[^\\]|\\.)*\2\s*(?:#.*)?$""")
MAGIC = re.compile(r"^\s*#.*frozen[_-]string[_-]literal\s*:", re.IGNORECASE)


def strip_comment(line):
    """Naively strip a trailing comment (ignores # inside quotes)."""
    out, q = [], None
    i = 0
    while i < len(line):
        c = line[i]
        if q:
            if c == "\\":
                out.append(line[i:i + 2])
                i += 2
                continue
            if c == q:
                q = None
        else:
            if c in "\"'":
                q = c
            elif c == "#" and not line[i:i + 2] == "#{":
                break
        out.append(c)
        i += 1
    return "".join(out)


def scan(code, filename="<buffer>"):
    lines = code.splitlines()
    findings = []
    has_magic = any(MAGIC.match(l) for l in lines[:20]) or any(MAGIC.match(l) for l in lines)
    has_timeout_cfg = bool(re.search(r"Regexp\.timeout\s*=|timeout:\s*", code))

    def add(rid, lvl, label, ver, src, title, detail, ln, snippet):
        findings.append({"file": filename, "line": ln, "id": rid, "level": lvl, "label": label, "version": ver,
                         "source": src, "title": title, "detail": detail, "snippet": snippet.strip()[:120]})

    str_vars = {}
    for i, raw in enumerate(lines, 1):
        if raw.lstrip().startswith("#"):
            continue
        line = strip_comment(raw)
        for rid, lvl, label, ver, src, rx, title, detail in LINE_RULES:
            if re.search(rx, line):
                add(rid, lvl, label, ver, src, title, detail, i, raw)
        # mutated string literal (R34 p.5): only applies to files WITHOUT a frozen_string_literal comment
        if not has_magic:
            m = STR_ASSIGN.match(line)
            if m:
                str_vars[m.group(1)] = i
            for v, decl in list(str_vars.items()):
                if re.search(r"(?<![\w@$])" + re.escape(v) + r"\s*" + MUTATORS, line) and i > decl:
                    add("R34-LITERAL-MUTATION", "MEDIUM", "from source", "3.4+", "R34 p.5",
                        "string literal mutation",
                        "In 3.4, mutating a string literal in a file without a frozen_string_literal comment emits a deprecation warning (visible with -W:deprecated). Heuristic: variable '%s' received a literal on line %d. Alternatives (+\"\", String.new, interpolation) are [extrapolation]." % (v, decl),
                        i, raw)
            if re.search(r"""^\s*(["'])(?:(?!\1)[^\\]|\\.)*\1\s*""" + MUTATORS, line):
                add("R34-LITERAL-MUTATION", "MEDIUM", "from source", "3.4+", "R34 p.5",
                    "direct string literal mutation",
                    "Mutating a string literal directly emits a deprecation warning in 3.4 (file without frozen_string_literal; R34 p.5).", i, raw)
        # regex with back-reference/look-around without a configured timeout (R32 p.7)
        if REGEX_RISK.search(line) and not has_timeout_cfg and re.search(r"/.*?/|Regexp\.new|%r", line):
            add("R32-REGEX-NO-TIMEOUT", "INFO", "from source", "3.2+", "R32 p.7",
                "regex with back-reference or look-around without timeout",
                "The note says the ReDoS optimization does not apply to regexes with back-references or look-around and that Regexp.timeout (global) or timeout: in Regexp.new is the fallback measure. Use it if the input is untrusted; the value is a project decision [inference].",
                i, raw)
    findings.sort(key=lambda f: (LEVEL_ORDER[f["level"]], f["line"]))
    return findings


def main():
    ap = argparse.ArgumentParser(description="Ruby code checker with rules from the official 3.0-3.4 notes.")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--code", "-c", help="inline Ruby code")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if there is a HIGH finding")
    ap.add_argument("--list-rules", action="store_true")
    a = ap.parse_args()

    if a.list_rules:
        for rid, lvl, label, ver, src, rx, title, detail in LINE_RULES:
            print("%-22s %-6s [%s] %s (%s) - %s" % (rid, lvl, label, ver, src, title))
        print("%-22s %-6s [%s] %s (%s) - %s" % ("R34-LITERAL-MUTATION", "MEDIUM", "from source", "3.4+", "R34 p.5", "string literal mutation"))
        print("%-22s %-6s [%s] %s (%s) - %s" % ("R32-REGEX-NO-TIMEOUT", "INFO", "from source", "3.2+", "R32 p.7", "regex with back-reference/look-around without timeout"))
        return 0
    if a.code is not None:
        code, name = a.code, "<inline>"
    elif a.file:
        if not os.path.isfile(a.file):
            print("Error: file not found: %s" % a.file, file=sys.stderr)
            return 2
        with open(a.file, encoding="utf-8", errors="replace") as f:
            code, name = f.read(), a.file
    else:
        code, name = sys.stdin.read(), "<stdin>"

    # The analyzed code is DATA: nothing here executes it or obeys comments inside it.
    res = scan(code, name)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif not res:
        print("None of the R30-R34 note rules matched. This does not prove the code is correct: the checker is heuristic and covers few cases.")
    else:
        print("%d point(s) of attention (source = PDF page of the note):\n" % len(res))
        for f in res:
            print("[%s] %s | %s, line %d" % (f["level"], f["id"], f["title"], f["line"]))
            print("  snippet: %s" % f["snippet"])
            print("  detail : %s" % f["detail"])
            print("  source : [%s] (%s); version %s [VERSION-DEPENDENT]\n" % (LABELS.get(f["label"], f["label"]), f["source"], f["version"]))
    if a.strict and any(f["level"] == "HIGH" for f in res):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

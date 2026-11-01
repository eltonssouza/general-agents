# -*- coding: utf-8 -*-
"""
clean_code_function_auditor.py - HEURISTIC linter for function signatures (read-only, no network).

ORIGIN OF THE RULES (important)
  The package's Clean Code PDF is a SAMPLE: it has only the Introduction and Chapter 1. Chapters 2 (Names) and 3 (Functions)
  are NOT in the PDF; the table of contents (CC p.8-9) and the index (CC p.48-54) only prove that the topics exist ("Flag Arguments",
  "Command Query Separation", "Function Arguments", printed 40-45). Therefore ALL the automatic rules below are
  [extrapolation]: widespread practices about functions, with CONFIGURABLE and arbitrary limits. No number here comes from
  the book. For what the sample really supports, use --checklist (Chapter 1 questions, with PDF page).

Automatic rules (all [extrapolation]):
  A1 number of arguments above --max-args (default 3)
  A2 boolean argument (type bool/boolean/Boolean): the function may be doing two things
  A3 name with "And"/"Or" as a word: may do more than one thing
  A4 command name (set/add/remove/update/delete/create/save) with a non-void return: possible mix of
     command and query (CQS is a table-of-contents topic, CC p.8, with no text in the sample)
  A5 body (--body-file): lines above --max-lines (default 20) and indentation above --max-indent (default 2)

Usage:
  python -I clean_code_function_auditor.py --signature "void render(boolean isSuite, Page page)"
  python -I clean_code_function_auditor.py --signature "boolean setName(String n)" --max-args 2
  python -I clean_code_function_auditor.py --signature "void f(int a)" --body-file body.txt --max-lines 15
  python -I clean_code_function_auditor.py --checklist
  python -I clean_code_function_auditor.py --demo [--strict]
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

BOOL_TYPES = {"bool", "boolean"}
COMMAND_PREFIX = re.compile(r"^(set|add|remove|update|delete|create|save|put|insert)[A-Z_0-9]", re.I)
SRC = "[extrapolation]"


def split_args(raw):
    """Split on commas at depth zero (respects <>, (), [])."""
    parts, depth, cur = [], 0, ""
    for ch in raw:
        if ch in "<([":
            depth += 1
        elif ch in ">)]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def parse_signature(sig):
    m = re.search(r"^(?P<head>[^()]*?)\((?P<args>.*)\)\s*[{;:]?\s*$", sig.strip())
    if not m:
        return None
    head_tokens = m.group("head").split()
    if not head_tokens:
        return None
    name = head_tokens[-1]
    ret = " ".join(t for t in head_tokens[:-1] if t not in {"public", "private", "protected", "static", "final", "abstract", "virtual", "async"})
    return {"name": name, "ret": ret, "args": split_args(m.group("args"))}


def arg_type_tokens(arg):
    arg = re.sub(r"=.*$", "", arg)
    toks = re.findall(r"[A-Za-z_][A-Za-z_0-9<>\[\]]*", arg)
    return [t.lower() for t in toks[:-1]] if len(toks) > 1 else [t.lower() for t in toks]


def audit(sig, body_lines=None, max_args=3, max_lines=20, max_indent=2):
    p = parse_signature(sig)
    if not p:
        return None, ["Signature not recognized (expected something like 'type name(type arg, ...)')."]
    findings = []
    n = len(p["args"])
    if n > max_args:
        findings.append(("A1", "%d arguments (configured limit %d). Consider grouping them into an object %s" % (n, max_args, SRC)))
    for a in p["args"]:
        toks = arg_type_tokens(a)
        if any(t in BOOL_TYPES for t in toks):
            findings.append(("A2", "boolean argument '%s': the function may do two things depending on the value; "
                                   "consider two functions %s" % (a, SRC)))
    words = re.findall(r"[A-Z][a-z0-9]*|[a-z0-9]+", p["name"])
    if any(w in ("And", "Or") for w in words[1:]):
        findings.append(("A3", "name '%s' contains And/Or: possibly more than one responsibility %s" % (p["name"], SRC)))
    if COMMAND_PREFIX.match(p["name"]) and p["ret"] and p["ret"].strip().lower() not in ("void", ""):
        findings.append(("A4", "'%s' looks like a command but returns '%s': possible mix of command and query %s" %
                         (p["name"], p["ret"], SRC)))
    if body_lines is not None:
        real = [l for l in body_lines if l.strip()]
        if len(real) > max_lines:
            findings.append(("A5", "body with %d non-empty lines (configured limit %d) %s" % (len(real), max_lines, SRC)))
        depth = 0
        for l in real:
            expanded = l.replace("\t", "    ")
            lead = len(expanded) - len(expanded.lstrip(" "))
            depth = max(depth, lead // 4)
        if depth > max_indent:
            findings.append(("A5", "maximum indentation of %d levels (configured limit %d; 4 spaces per level) %s" %
                             (depth, max_indent, SRC)))
    return p, findings


def checklist():
    print("=== Review checklist based on the Clean Code SAMPLE (Ch. 1 + Introduction) ===")
    print("Manual questions; none is a numeric rule. Pages = PDF.")
    items = [
        ("Does the method/object do more than one thing? If so, extract (Extract Method) to say what it does and submethods for how.", "CC p.41"),
        ("Is there duplication? Repetition indicates an idea not represented in the code.", "CC p.40-41"),
        ("Do the names express the design's ideas (and can they be renamed easily)?", "CC p.40-41"),
        ("Does the code have tests? Without tests the author does not consider it clean.", "CC p.39 and p.40"),
        ("After your change, is the code a little cleaner than you found it?", "CC p.44"),
        ("Was it easy to read? Reading outweighs writing by more than 10 to 1.", "CC p.44"),
        ("Is error handling complete and the logic straightforward, with minimal dependencies?", "CC p.37"),
    ]
    for q, pg in items:
        print(" [ ] %s  [from source] (%s)" % (q, pg))
    print("Rules on names and functions (Chs. 2 and 3) are not in the sample: see references/clean-code-nomes-e-funcoes.md.")


def run_one(sig, body, args):
    print("=== Heuristic function audit (all rules are %s) ===" % SRC)
    print("Signature: %s" % sig)
    p, findings = audit(sig, body, args.max_args, args.max_lines, args.max_indent)
    if p is None:
        print("ERROR: " + findings[0])
        return 2, 0
    print("Name=%s return=%s arguments=%d" % (p["name"], p["ret"] or "(not given)", len(p["args"])))
    if not findings:
        print("No findings by rules A1-A5 (configured limits: args=%d lines=%d indent=%d)." %
              (args.max_args, args.max_lines, args.max_indent))
    for code, msg in findings:
        print(" - [%s] %s" % (code, msg))
    print("Reminder: Chs. 2-3 of Clean Code are not in the PDF; these limits are not from the book (see docstring).")
    return 0, len(findings)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Heuristic linter for function signatures ([extrapolation] rules).")
    ap.add_argument("--signature", help="signature to analyze")
    ap.add_argument("--body-file", help="file with the function body (for A5)")
    ap.add_argument("--max-args", type=int, default=3)
    ap.add_argument("--max-lines", type=int, default=20)
    ap.add_argument("--max-indent", type=int, default=2)
    ap.add_argument("--checklist", action="store_true", help="review questions supported by the sample (Ch. 1)")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit with code 1 if there are findings")
    a = ap.parse_args(argv)

    if a.checklist:
        checklist()
        return 0
    if a.demo:
        total = 0
        for sig, body in (("public void renderPageAndSetHeader(Page page, boolean isSuite, int retries, String format)",
                           ["    if (isSuite) {", "        while (retries > 0) {", "            for (;;) {", "                x();", "            }", "        }", "    }"]),
                          ("public void renderSuite(Page page)", ["    page.render();"]),
                          ("boolean setName(String name)", None)):
            _, n = run_one(sig, body, a)
            total += n
            print()
        return 1 if (a.strict and total) else 0
    if a.signature:
        body = None
        if a.body_file:
            with open(a.body_file, encoding="utf-8") as f:
                body = f.read().splitlines()
        rc, n = run_one(a.signature, body, a)
        if rc:
            return rc
        return 1 if (a.strict and n) else 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

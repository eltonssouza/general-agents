# -*- coding: utf-8 -*-
"""
routine_quality.py - routine quality checklist. It does NOT compute a grade.

Origin of each rule (PDF pages):
  - Numeric size and parameter limits: ONLY those of the essay "Write Code for Humans not Machines"
    (Mario Fusco, 97TH p.150-151): short method (about 15 lines as a reasonable upper bound), one
    responsibility per method, more than 3 parameters suggests grouping into an object, avoid nested loops
    and conditions. These are numbers from ONE author in an Extended edition, NOT from Code Complete nor Google.
  - Information hiding: ask "what does this class need to hide?" (CC2 p.62), two categories of
    secret (CC2 p.59) and the areas likely to change (CC2 p.62-64).
  - Coupling: size, visibility and flexibility criteria (CC2 p.65-66); simple-data-parameter and
    simple-object are acceptable; object-parameter is stronger; semantic coupling is the most insidious
    (CC2 p.66-67), with examples: control flag, global data, implicit call order.
  - Fan-out above about seven suggests excessive complexity (CC2 p.46).
  - Chapter 7 of Code Complete (routines) and the cohesion taxonomy are NOT in the sample; therefore the script
    does not classify cohesion.
Offline; read-only. Usage: python -I scripts/routine_quality.py --lines 25 --params 3
"""
import argparse
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

COUPLING = {
    "data": ("OK", "Coupling through simple data parameters: normal and acceptable.", "CC2 p.66", "[from source]"),
    "object-creation": ("OK", "Simple-object coupling (instantiates an object): acceptable.", "CC2 p.66", "[from source]"),
    "object-parameter": ("WARNING", "Object-parameter: stronger, since it requires the caller to know a third object.", "CC2 p.66", "[from source]"),
    "semantic-control-flag": ("ALERT", "Semantic coupling through a control flag: assumes knowledge of the internals (acceptable only with its own type, such as an enumeration).", "CC2 p.67", "[from source]"),
    "semantic-global": ("ALERT", "Semantic coupling through global data modified by another module: the most insidious and hardest to debug.", "CC2 p.67", "[from source]"),
    "semantic-call-order": ("ALERT", "Semantic coupling through implicit call order (for example Initialize before Routine).", "CC2 p.67", "[from source]"),
}

ESSAY = "[from source] (essay author's number)"


def main():
    ap = argparse.ArgumentParser(description="Routine checklist (CC2 Ch. 5 and 97TH; PDF pages).")
    ap.add_argument("--name", default="calculateInvoiceTotal")
    ap.add_argument("--lines", type=int, default=0, help="routine lines (0 = not provided)")
    ap.add_argument("--params", type=int, default=-1, help="number of parameters (-1 = not provided)")
    ap.add_argument("--nesting", type=int, default=-1, help="maximum nesting level (-1 = not provided)")
    ap.add_argument("--fanout", type=int, default=-1, help="number of other routines/classes used (-1 = not provided)")
    ap.add_argument("--coupling", choices=sorted(COUPLING), default=None)
    ap.add_argument("--leaks-secrets", action="store_true", help="exposes internal decisions (data structure, format, order)")
    ap.add_argument("--name-has-and", action="store_true", help="the routine's natural name contains 'and'")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    f = []

    def add(status, rule, text, src, label):
        f.append({"status": status, "rule": rule, "text": text, "source": src, "label": label})

    if a.lines:
        if a.lines <= 15:
            add("OK", "Size", "%d lines: within the essay's about 15 lines." % a.lines, "97TH p.150", ESSAY)
        else:
            add("WARNING", "Size", "%d lines: above about 15 lines, a number suggested by the essay's author (not by Code Complete)." % a.lines,
                "97TH p.150", ESSAY)
        add("INFO", "Short routines", "Chapter 5 says that keeping routines short reduces mental load, without giving a number.", "CC2 p.44", "[from source]")
    if a.params >= 0:
        if a.params <= 3:
            add("OK", "Parameters", "%d parameters: within the essay's limit." % a.params, "97TH p.150", ESSAY)
        else:
            add("WARNING", "Parameters", "%d parameters: the essay suggests refactoring into an object when there are more than 3." % a.params, "97TH p.150",
                ESSAY)
        add("INFO", "Coupling by size", "Fewer parameters mean smaller connections between modules (size criterion).", "CC2 p.65", "[from source]")
    if a.nesting >= 0:
        if a.nesting >= 2:
            add("WARNING", "Nesting", "Nesting %d: the essay recommends avoiding nested loops and conditions, extracting methods." % a.nesting,
                "97TH p.150", "[from source]")
        else:
            add("OK", "Nesting", "Low nesting.", "97TH p.150", "[from source]")
    if a.fanout >= 0:
        if a.fanout > 7:
            add("WARNING", "Fan-out", "%d dependencies: above about seven suggests excessive complexity." % a.fanout, "CC2 p.46", "[from source]")
        else:
            add("OK", "Fan-out", "Fan-out of %d: within low to medium." % a.fanout, "CC2 p.46", "[from source]")
    if a.name_has_and:
        add("WARNING", "Responsibility", "An 'and' in the name suggests more than one responsibility.", "97TH p.150", "[from source]")
    if a.coupling:
        s, t, src, lab = COUPLING[a.coupling]
        add(s, "Coupling", t, src, lab)
    if a.leaks_secrets:
        add("WARNING", "Information hiding", "The routine exposes internal decisions; ask 'what does this class need to hide?' and isolate the areas likely to change.",
            "CC2 p.62; p.59", "[from source]")
    else:
        add("INFO", "Information hiding", "Confirm that the interface reveals the minimum and that the areas likely to change are isolated.", "CC2 p.58; p.62-64", "[from source]")
    add("INFO", "Cohesion", "The cohesion taxonomy is not in the Code Complete sample; only 'strong cohesion' as a heuristic (CC2 p.70). There is no classification here.",
        "CC2 p.70", "[from source]")

    out = {"routine": a.name, "findings": f,
           "note": "Checklist without scoring. The numeric limits are from Mario Fusco's essay (97TH p.150), not from Code Complete."}
    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    print("=== Routine checklist: %s ===" % a.name)
    for x in f:
        print("  [%-7s] %-18s %s (%s) %s" % (x["status"], x["rule"], x["text"], x["source"], x["label"]))
    print("\n" + out["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

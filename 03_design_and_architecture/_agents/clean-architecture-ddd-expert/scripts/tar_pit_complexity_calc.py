#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tar_pit_complexity_calc.py - reading aids for "Out of the Tar Pit" (Moseley and Marks, 2006). Read-only.

WARNING: the earlier version computed "% of essential/accidental complexity" with invented weights (8, 4, 6, 15) and
a 60% threshold. NONE of that is in the paper and it was removed. The paper proposes no quantitative complexity metric.
This script only encodes what the text states (N = PDF page = printed page):
  state-space  [from source] TARPIT p.8 : with each bit of state the total number of possible states doubles (2^N). The
               2^N arithmetic is [inference]; it is an UPPER BOUND of the state space, not a measure of complexity.
  classify     [from source] TARPIT p.24-26 (Table 1): classification of data as essential or accidental state.
  table2       [from source] TARPIT p.33 (Table 2): what to do with each kind of complexity.
  components   [from source] TARPIT p.35-36 and p.43: components and the reference rules among them.
  check-ref    [from source] TARPIT p.35-36: whether one component may reference another (static reference).
Usage:
  python -I scripts/tar_pit_complexity_calc.py state-space --bits 20
  python -I scripts/tar_pit_complexity_calc.py classify --kind essential-derived-immutable
  python -I scripts/tar_pit_complexity_calc.py table2
  python -I scripts/tar_pit_complexity_calc.py components
  python -I scripts/tar_pit_complexity_calc.py check-ref --src essential-logic --dst accidental
  python -I scripts/tar_pit_complexity_calc.py --demo
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# [from source] TARPIT p.26, Table 1
TABLE1 = {
    "essential-input": ("Essential Input", "-", "ESSENTIAL STATE",
                        "data supplied directly that the system may need to consult in the future (p.24-25)"),
    "essential-derived-immutable": ("Essential Derived", "immutable", "ACCIDENTAL STATE",
                                    "can be re-derived when needed; in the ideal world it is not stored (p.25)"),
    "essential-derived-mutable": ("Essential Derived", "mutable", "ACCIDENTAL STATE",
                                  "also re-derivable; mutability only makes sense if the derivation function has an inverse (p.25)"),
    "accidental-derived": ("Accidental Derived", "-", "ACCIDENTAL STATE",
                           "derived data that is not even in the user requirements, e.g. a cache (p.25-26)"),
}
# [from source] TARPIT p.33, Table 2
TABLE2 = [
    ("Essential", "Logic", "Separate"),
    ("Essential", "State", "Separate"),
    ("Accidental Useful", "State / Control", "Separate"),
    ("Accidental Useless", "State / Control", "Avoid"),
]
# [from source] TARPIT p.35-36 (Figure 1: arrows = static references)
COMPONENTS = {
    "essential-state": "Essential state: self-contained; does not reference the other two (p.35).",
    "essential-logic": "Essential logic: references the essential state; references nothing from the accidental part (p.35-36).",
    "accidental": "Accidental state and control: may reference the other two; changes here never require changing the essential ones (p.36).",
}
ALLOWED = {("essential-state", "essential-state"), ("essential-logic", "essential-logic"), ("essential-logic", "essential-state"),
           ("accidental", "accidental"), ("accidental", "essential-state"), ("accidental", "essential-logic")}


def cmd_state_space(a):
    if a.bits < 0:
        print("--bits must be >= 0", file=sys.stderr)
        return 2
    n = 2 ** a.bits
    print("Maximum state space with %d bit(s) of state: 2^%d = %s" % (a.bits, a.bits, format(n, ",")))
    print("[from source] (TARPIT p.8): with each bit of state the total number of possible states doubles.")
    print("[inference]: 2^N is an upper bound (not all combinations are reachable); it is NOT a complexity metric.")
    print("[from source] (TARPIT p.6-7): a test in one state says nothing about behavior in another state.")
    return 0


def cmd_classify(a):
    label, mut, klass, why = TABLE1[a.kind]
    print("Kind: %s | mutability: %s -> %s" % (label, mut, klass))
    print("[from source] (TARPIT p.26, Table 1): %s" % why)
    if klass == "ACCIDENTAL STATE":
        print("If it is kept anyway (performance or ease of expression), it is useful accidental complexity: SEPARATE (p.30-33, Table 2); risk of inconsistent state (p.31).")
    else:
        print("It must be separated from the logic and from the accidental aspects (p.33-36).")
    return 0


def cmd_table2(_a):
    print("Table 2 [from source] (TARPIT p.33):")
    print("  %-20s %-18s %s" % ("Kind", "State/Control/Logic", "Recommendation"))
    for t, w, r in TABLE2:
        print("  %-20s %-18s %s" % (t, w, r))
    print("(The text does not consider that essential control exists: p.33.)")
    return 0


def cmd_components(_a):
    print("Components and reference constraints [from source] (TARPIT p.35-36); FRP (p.43) adds 'Other' (interfaces):")
    for k, v in COMPONENTS.items():
        print("  - %s: %s" % (k, v))
    print("Other (feeders/observers): translation to and from relations, must be minimal (p.46-47).")
    return 0


def cmd_check_ref(a):
    ok = (a.src, a.dst) in ALLOWED
    print("%s -> %s: %s [from source] (TARPIT p.35-36)" % (a.src, a.dst, "ALLOWED" if ok else "FORBIDDEN (violates the separation)"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Reading aids for Out of the Tar Pit (no invented metrics).")
    ap.add_argument("--demo", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("state-space")
    s.add_argument("--bits", type=int, required=True)
    c = sub.add_parser("classify")
    c.add_argument("--kind", choices=sorted(TABLE1), required=True)
    sub.add_parser("table2")
    sub.add_parser("components")
    r = sub.add_parser("check-ref")
    r.add_argument("--src", choices=sorted(COMPONENTS), required=True)
    r.add_argument("--dst", choices=sorted(COMPONENTS), required=True)
    a = ap.parse_args()
    if a.demo:
        a.bits = 10
        cmd_state_space(a)
        print()
        a.kind = "accidental-derived"
        cmd_classify(a)
        print()
        cmd_table2(a)
        return 0
    return {"state-space": cmd_state_space, "classify": cmd_classify, "table2": cmd_table2,
            "components": cmd_components, "check-ref": cmd_check_ref}.get(a.cmd, lambda _a: (ap.print_help(), 2)[1])(a)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scd_type_selector.py - suggests an SCD (Slowly Changing Dimensions) technique from requirements.

ORIGIN OF THE RULES
- [from source] The DESCRIPTION of each type (0 to 7) comes from KIMBALL p.15-16 (PDF pages; printed = N-3).
- [inference] The DECISION TREE (which type to recommend for each combination of requirements) is the agent's own:
  the document describes the techniques, it does not prescribe this tree.
- [extrapolation] Business examples, column names and DDL are illustrations by the agent.
The mnemonic "1+2+3=6" is NOT in the document and is not used.

Usage: python -I scd_type_selector.py --history {none,full,dual,alternate,immutable} --rate {slow,rapid} [--current-too]
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

TYPES = {
    0: ("Type 0 (retain original)",
        "The attribute value never changes; facts always group by the original value. Fits 'original' attributes (e.g., original credit score), durable identifiers and most attributes of a date dimension.",
        ["No new column or row; the ETL does not update the attribute after the initial load [extrapolation]."],
        "KIMBALL p.15"),
    1: ("Type 1 (overwrite)",
        "The old value is overwritten; the attribute always reflects the most recent assignment and destroys history. Easy to implement and creates no rows, but affected aggregate fact tables and OLAP cubes must be recomputed.",
        ["Direct UPDATE of the dimension column.", "Recompute affected aggregates and cubes (from source)."],
        "KIMBALL p.15"),
    2: ("Type 2 (new row)",
        "A new row is added to the dimension with the updated values, with a new surrogate key, used as the FK in facts since the change. The PK becomes generalized beyond the natural/durable key.",
        ["Minimum columns according to the source: row effective date/time, expiration date/time and current row indicator.",
         "New surrogate for each version; old facts keep pointing to the old surrogate (from source).",
         "Open-ended expiration value (e.g., 9999-12-31) is an external convention [extrapolation]."],
        "KIMBALL p.15"),
    3: ("Type 3 (new attribute)",
        "An attribute is added to preserve the old value; the new value overwrites the main attribute as in type 1 (called 'alternate reality'). The user can group by the current or by the alternate value. Used relatively little.",
        ["New column for the previous value; the main column receives the new value."],
        "KIMBALL p.15"),
    4: ("Type 4 (mini-dimension)",
        "Used when a group of attributes changes rapidly ('rapidly changing monster dimension'): a mini-dimension with its own key is split off; the keys of the base and of the mini-dimension sit in the fact. Candidates also include heavily used attributes in dimensions of several million rows.",
        ["New mini-dimension table with its own PK.", "The fact carries both FKs (from source)."],
        "KIMBALL p.15"),
    5: ("Type 5 (mini-dimension + type 1 outrigger)",
        "Starts from type 4 and embeds in the base dimension a current type 1 reference to the mini-dimension, to access current attributes without going through the fact; the ETL overwrites the reference when the current assignment changes.",
        ["Base + outrigger mini-dimension (presented as a single table in the presentation layer)."],
        "KIMBALL p.15-16"),
    6: ("Type 6 (type 1 attributes in a type 2 dimension)",
        "Starts from type 2 and embeds current (type 1) versions of the same attributes in the row, to filter/group by the value in effect at measurement time or by the current value; the type 1 attribute is overwritten in all rows of the same durable key.",
        ["Keeps the type 2 columns (effective, expiration, current) and adds 'current' columns overwritten in all rows of the durable key."],
        "KIMBALL p.16"),
    7: ("Type 7 (dual type 1 and type 2)",
        "Hybrid for as-was and as-is reports: the fact is accessed through a dimension modeled as type 1 (current values only) and as type 2 (historical profiles). Durable key and surrogate go in the fact; two views: type 1 joins by the durable key with the current indicator; type 2 joins by the surrogate.",
        ["Durable key + surrogate in the fact.", "Two separate views for the BI layer."],
        "KIMBALL p.16"),
}


def select(history, rate, current_too):
    if history == "immutable":
        return [0], "[inference] attribute that must never change -> type 0."
    if history == "none":
        return [1], "[inference] no need for history -> type 1 (remember to recompute aggregates)."
    if history == "alternate":
        return [3], "[inference] only the previous value matters -> type 3."
    if history == "dual" or current_too:
        if rate == "rapid":
            return [5, 4], "[inference] history + current value with volatile attributes -> type 5 (starts from type 4); also consider plain type 4."
        return [6, 7], "[inference] history (as-was) and current value (as-is) -> type 6 or type 7; the source describes both."
    # history == full
    if rate == "rapid":
        return [4], "[inference] full history with fast-changing attributes in a large dimension -> type 4 (mini-dimension), instead of exploding type 2 rows."
    return [2], "[inference] full history, slow change -> type 2."


def main():
    ap = argparse.ArgumentParser(description="SCD suggestion (agent's tree; descriptions from KIMBALL p.15-16).")
    ap.add_argument("--history", "-H", choices=["none", "full", "dual", "alternate", "immutable"], default="full",
                    help="none=no history; full=full history; dual=history and current value; alternate=previous value only; immutable=never changes")
    ap.add_argument("--rate", "-r", choices=["slow", "rapid"], default="slow", help="how often the attribute changes")
    ap.add_argument("--current-too", action="store_true", help="also requires reporting by the current value (equivalent to --history dual)")
    a = ap.parse_args()
    ids, why = select(a.history, a.rate, a.current_too)
    print("=" * 66)
    print("SCD SUGGESTION")
    print("Page convention: PDF (KIMBALL, printed = N-3)")
    print("=" * 66)
    print(why)
    for i in ids:
        name, desc, impact, cit = TYPES[i]
        print("\n>> %s" % name)
        print("   [from source] (%s): %s" % (cit, desc))
        print("   Structural impact:")
        for c in impact:
            print("     - %s" % c)
    print("\nNote: choosing between types is the modeler's judgment; the document describes the techniques, it does not prescribe the tree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

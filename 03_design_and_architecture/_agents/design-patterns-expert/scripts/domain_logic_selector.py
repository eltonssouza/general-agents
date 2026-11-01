# -*- coding: utf-8 -*-
"""
domain_logic_selector.py - guides the choice of data access according to the domain logic style (read-only).

ORIGIN OF THE RULES (important)
  [from source] The PERSISTENCE recommendations come from Chapter 3 of PoEAA, which is in the sample:
    - simple logic (Transaction Script or Table Module): design the tables around the data, use Row/Table Data
      Gateway (PEAA p.55); Table Data Gateway goes well with Record Set and Table Module (PEAA p.42).
    - simple Domain Model, classes almost identical to the tables: Active Record (PEAA p.42-43, 55).
    - complex Domain Model: Data Mapper, which isolates the model from the database (PEAA p.43, 55); do not use a Gateway
      as the primary persistence mechanism of a Domain Model and do not mix primary mechanisms (PEAA p.43).
    - Inheritance: Single, Concrete or Class Table Inheritance; the author's first choice is Single Table (PEAA p.52-54).
    - Iterate in cycles of at most six weeks; avoid months of a model without a database (PEAA p.55).
  [extrapolation] The CHOICE AMONG Transaction Script, Table Module and Domain Model (--complexity etc. mode) is a
    heuristic OF THIS PACKAGE, with arbitrary thresholds. PoEAA Chapter 2 and Chapter 9, which deal with this, are NOT
    in the sample. What the Introduction says is that there is no single architecture and that the choice depends on the
    problem (PEAA p.30-31). Service Layer is not recommended here because the text is not in the sample.

Usage:
  python -I domain_logic_selector.py --logic transaction-script
  python -I domain_logic_selector.py --logic domain-model --rich
  python -I domain_logic_selector.py --inheritance
  python -I domain_logic_selector.py --complexity 8 --entities 25 --relationships 7      # [extrapolation] heuristic
  python -I domain_logic_selector.py --demo
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# [extrapolation] heuristic thresholds (arbitrary; adjust via --simple-max / --table-max)
SIMPLE_MAX = 3
LOGIC_NAMES = {"transaction-script": "Transaction Script", "table-module": "Table Module", "domain-model": "Domain Model"}


def persistence_advice(logic, rich=False):
    """Recommendations from PEAA Ch. 3 (sample). Returns a list of lines."""
    out = []
    if logic == "transaction-script":
        out += ["Persistence [from source]: design the tables around the data and use Row Data Gateway or Table Data Gateway "
                "to take the SQL out of the logic (PEAA p.55, 41).",
                "Active Record may emerge if there is repetitive code across Transaction Scripts (PEAA p.42)."]
    elif logic == "table-module":
        out += ["Persistence [from source]: Table Data Gateway naturally goes with Record Set and with Table Module "
                "(PEAA p.42); tables designed around the data (PEAA p.55)."]
    elif logic == "domain-model":
        if rich:
            out += ["Persistence [from source]: Data Mapper isolates the Domain Model from the database and lets both vary; it is "
                    "the most complicated, but gives complete isolation (PEAA p.43).",
                    "Do not use a Gateway as the primary persistence mechanism of the Domain Model (PEAA p.43).",
                    "Build the model without copying the database schema, but integrate it with the database in every iteration of "
                    "at most six weeks (PEAA p.55).",
                    "Consider an O/R mapping tool instead of writing the Data Mapper by hand (PEAA p.45)."]
        else:
            out += ["Persistence [from source]: if the logic is simple and the classes match the tables, Active Record is the "
                    "simple path (PEAA p.43); if a model isomorphic to the database makes sense, consider it (PEAA p.55).",
                    "If the logic grows, Active Record breaks down (inheritance, tests without a database); migrate to Data Mapper (PEAA p.42-43)."]
    out.append("Do not mix primary persistence mechanisms (PEAA p.43).")
    return out


def heuristic(complexity, entities, relationships, oo_skill, stored_procs):
    """[extrapolation] Heuristic choice of logic style. It is NOT a rule from the book."""
    if stored_procs and complexity <= 5:
        return "table-module", "table/recordset-centered environment and medium-low complexity"
    if complexity <= SIMPLE_MAX and relationships <= SIMPLE_MAX:
        return "transaction-script", "simple rules and relationships (threshold %d)" % SIMPLE_MAX
    return "domain-model", "rules or relationships above the simple threshold"


def report(logic, why, rich, inputs=None):
    print("=== Data access selection by logic style (PoEAA, sample) ===")
    if inputs:
        print("Inputs: %s" % inputs)
        print("[extrapolation] Style choice: %s (%s)." % (LOGIC_NAMES[logic], why))
        print("  Package heuristic with arbitrary thresholds; PEAA Ch. 2 and 9 (the author's criteria) are NOT in the sample.")
        print("  The book only says there is no single architecture and that the choice depends on the problem (PEAA p.30-31).")
    else:
        print("Style given: %s" % LOGIC_NAMES[logic])
    for line in persistence_advice(logic, rich):
        print(" - " + line)
    if logic == "domain-model" and not rich:
        pass


def inheritance():
    print("=== Inheritance mapping to tables (PEAA p.52-54) ===")
    print(" - Single Table Inheritance (278): one table for the whole hierarchy; puts everything together and avoids joins, but may waste "
          "space with empty columns and become a bottleneck [from source] (PEAA p.52-54).")
    print(" - Class Table Inheritance (285): one table per class; simpler class-to-table relationship, but requires several joins "
          "[from source] (PEAA p.52).")
    print(" - Concrete Table Inheritance (293): one table per concrete class; avoids joins, but is fragile to changes in the "
          "superclass [from source] (PEAA p.52-54).")
    print(" - They can be mixed in the same hierarchy, with more complexity; the author's first choice tends to be Single "
          "Table because it is easy and resilient to refactoring; consult the DBAs [from source] (PEAA p.54).")
    print("(page numbers in parentheses next to the names are from the printed edition; those given as PEAA p.N are PDF pages)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Data access by domain logic style (PoEAA, sample).")
    ap.add_argument("--logic", choices=sorted(LOGIC_NAMES), help="logic style already chosen")
    ap.add_argument("--rich", action="store_true", help="with --logic domain-model: complex logic (Data Mapper)")
    ap.add_argument("--inheritance", action="store_true", help="inheritance mapping options")
    ap.add_argument("--complexity", type=int, help="[heuristic] rule complexity, 1 to 10")
    ap.add_argument("--entities", type=int, default=10, help="[heuristic] approximate number of tables/entities (informational)")
    ap.add_argument("--relationships", type=int, default=5, help="[heuristic] inheritance/polymorphism, 1 to 10")
    ap.add_argument("--oo-skill", type=int, default=5, help="[heuristic] OO maturity, 1 to 10 (informational)")
    ap.add_argument("--stored-procs", action="store_true", help="[heuristic] recordset/stored-procedure-centered environment")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args(argv)

    if a.demo:
        for args in (dict(c=2, e=4, r=2, s=7, sp=False), dict(c=9, e=35, r=8, s=9, sp=False)):
            logic, why = heuristic(args["c"], args["e"], args["r"], args["s"], args["sp"])
            report(logic, why, rich=args["c"] >= 8, inputs="complexity=%d entities=%d relationships=%d" %
                   (args["c"], args["e"], args["r"]))
            print()
        return 0
    if a.inheritance:
        inheritance()
        return 0
    if a.logic:
        report(a.logic, "given by the user", a.rich)
        return 0
    if a.complexity is not None:
        for name, v in (("complexity", a.complexity), ("relationships", a.relationships), ("oo-skill", a.oo_skill)):
            if not 1 <= v <= 10:
                ap.error("--%s must be between 1 and 10" % name)
        logic, why = heuristic(a.complexity, a.entities, a.relationships, a.oo_skill, a.stored_procs)
        report(logic, why, rich=a.complexity >= 7, inputs="complexity=%d entities=%d relationships=%d" %
               (a.complexity, a.entities, a.relationships))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

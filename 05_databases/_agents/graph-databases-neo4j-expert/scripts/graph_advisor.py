# -*- coding: utf-8 -*-
"""
graph_advisor.py - heuristic modeling advisor: should this concept be a node, a relationship or a property?

Rules (each with its origin):
  [from source]   = on a page of NEO4J (PDF; printed = N - 18): guidelines on p.85-89 and time on p.90-92
  [inference]     = direct deduction from the text
  [extrapolation] = general/current practice (e.g. degree thresholds); NOT in the book

Usage:
  python -I graph_advisor.py --name Email --kind action --links 3
  python -I graph_advisor.py --name Address --kind value --multi-field
  python -I graph_advisor.py --name Weight --kind attribute --weight
  python -I graph_advisor.py --name Order --kind entity --temporal order
  python -I graph_advisor.py --name Category --kind entity --fanout 200000 --threshold 50000   (the threshold is YOURS)
No network; read-only.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def advise(a):
    out = []

    def add(msg, origem):
        out.append((msg, origem))

    kind = a.kind
    if kind == "entity":
        add("'%s' is a thing in the domain: model it as a NODE with a label; attributes as properties." % a.name, "[from source] (NEO4J p.85)")
    elif kind == "attribute":
        if a.weight:
            add("'%s' expresses the weight/strength/quality of a connection: a RELATIONSHIP property (weights rarely form a closed set)." % a.name, "[from source] (NEO4J p.85-86)")
        else:
            add("'%s' is an attribute of an entity: a NODE property (includes metadata such as timestamps and versions)." % a.name, "[from source] (NEO4J p.85)")
    elif kind == "value":
        if a.multi_field:
            add("'%s' is a complex value type (several fields, no identity of its own): it can become its own NODE, e.g. an Address linked by DELIVERY_ADDRESS." % a.name, "[from source] (NEO4J p.89)")
        else:
            add("'%s' is a simple value: a property." % a.name, "[from source] (NEO4J p.85)")
    elif kind == "action":
        if a.links > 2 or a.own_attrs:
            add("'%s' is an action/fact that involves %d entities%s: model it as an intermediate NODE (fact) linked to each participant; timestamps on the node mark start and end." % (a.name, a.links, " and has attributes of its own" if a.own_attrs else ""), "[from source] (NEO4J p.85-89)")
            add("Beware of 'verbing': the noun hidden in the action (email, review, job) is usually the entity.", "[from source] (NEO4J p.73, p.82)")
        else:
            add("'%s' links exactly two entities with no data of its own: a RELATIONSHIP with a specific name and direction. If it later links more than two things, refactoring it into a node will be a 'breaking change'." % a.name, "[from source] (NEO4J p.85)")
            add("Before deciding, ask: do I need to distinguish several instances of this action (e.g. several emails between the same people)? If so, it is a node.", "[inference] (NEO4J p.72-73)")

    if a.generic:
        add("Prefer fine-grained types (e.g. DELIVERY_ADDRESS) for a closed set; if you also need 'all of them', add a generic type (ADDRESS) in addition to the fine-grained ones. In TeleGraph the fine-grained types were almost 2x faster than properties.", "[from source] (NEO4J p.85-86, p.143)")

    if a.temporal == "period":
        add("Events queried by period: timeline tree (Year-Month-Day) with on-demand MERGE.", "[from source] (NEO4J p.90-91)")
    elif a.temporal == "order":
        add("Order between events: linked list with NEXT/PREVIOUS (or MOST_RECENT for the head of the list); can be combined with the timeline tree.", "[from source] (NEO4J p.40, p.90-92)")
    elif a.temporal == "validity":
        add("Validity in time of a connection: start_date/end_date properties on the relationship (Global Post), or on the fact node with timestamps.", "[from source] (NEO4J p.86-87, p.153)")
    elif a.temporal == "versions":
        add("Versioning the graph is possible within the model, but the schema leaks into every query. Measure the cost first.", "[from source] (NEO4J p.92)")

    if a.fanout is not None:
        if a.threshold is not None and a.fanout >= a.threshold:
            add("Estimated degree %d >= given threshold %d: possible highly connected node. The book does NOT cover supernodes; suggestions (intermediate nodes, fine-grained types, filtering by type/direction) are general practices. Measure first." % (a.fanout, a.threshold), "[extrapolation]")
        else:
            add("Estimated degree given (%d). The book does not define a supernode threshold; use --threshold with YOUR measured limit." % a.fanout, "[extrapolation]")
        add("The book's node record has a flag for 'densely connected' nodes, with no detail.", "[from source] (NEO4J p.172)")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", "-n", required=True)
    ap.add_argument("--kind", "-k", required=True, choices=["entity", "action", "attribute", "value"])
    ap.add_argument("--links", type=int, default=2, help="how many distinct entities the action involves")
    ap.add_argument("--own-attrs", action="store_true", help="the action has attributes of its own (date, content...)")
    ap.add_argument("--multi-field", action="store_true", help="value with several fields (address)")
    ap.add_argument("--weight", action="store_true", help="attribute is the weight/strength/quality of a relationship")
    ap.add_argument("--generic", action="store_true", help="evaluating generic vs fine-grained relationship type")
    ap.add_argument("--temporal", choices=["period", "order", "validity", "versions"])
    ap.add_argument("--fanout", type=int, help="estimated node degree")
    ap.add_argument("--threshold", type=int, help="degree threshold defined by you")
    a = ap.parse_args()
    print("Modeling advice: '%s' (%s)  [PDF; printed = N - 18]" % (a.name, a.kind))
    for msg, origem in advise(a):
        print("- %s\n    origin: %s" % (msg, origem))
    return 0


if __name__ == "__main__":
    sys.exit(main())

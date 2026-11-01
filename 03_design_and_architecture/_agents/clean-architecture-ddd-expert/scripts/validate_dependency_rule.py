#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_dependency_rule.py - checks dependencies between layers against the Dependency Rule. Read-only.

Origin of the rules (convention: N = PDF page):
  R1 [from source] CA12 p.3 : source code dependencies may only point INWARD; nothing in an inner circle
      may know anything about an outer circle.
  Levels [from source] CA12 p.3-5: 1 Entities, 2 Use Cases, 3 Interface Adapters, 4 Frameworks and Drivers.
      The text (p.5) says the circles are schematic and there may be more than four; the rule always holds.
  R2 [inference]: a dependency between modules of the SAME circle is not covered by the rule in the text; this script accepts it.
  R3 [extrapolation]: the layer aliases below (domain, application, infrastructure, controllers, web, ...) are
      usual mappings, NOT terms from the text. Unknown layers are reported, never silently ignored.
Limit: the script checks the graph you describe; it does not read source code.

JSON input: {"name": "...", "modules": [{"name": "X", "layer": "entities",
                "dependencies": [{"name": "Y", "layer": "use_cases"}]}],
               "layer_levels": {"my_layer": 2}}      # optional: extends/overrides the mapping
Usage: python -I scripts/validate_dependency_rule.py --demo | --file grafo.json | --layers
Exit: 0 no violations and no unknown layers; 1 with violations; 2 invalid usage/file or unknown layer.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

CANON = {"entities": 1, "use_cases": 2, "interface_adapters": 3, "frameworks_drivers": 4}  # [from source] CA12 p.3-5
ALIASES = {  # [extrapolation]
    "enterprise_business_rules": 1, "domain": 1,
    "application_business_rules": 2, "application": 2,
    "adapters": 3, "controllers": 3, "presenters": 3, "gateways": 3,
    "frameworks": 4, "infrastructure": 4, "database": 4, "web": 4, "ui": 4,
}


def levels(extra):
    m = dict(CANON)
    m.update(ALIASES)
    for k, v in (extra or {}).items():
        m[str(k).lower().strip()] = int(v)
    return m


def validate(graph):
    lv = levels(graph.get("layer_levels"))
    name = graph.get("name", "(unnamed)")
    mods = graph.get("modules", [])
    violations, unknown, ok = [], [], 0
    for m in mods:
        sl = str(m.get("layer", "")).lower().strip()
        if sl not in lv:
            unknown.append("module '%s': layer '%s'" % (m.get("name", "?"), sl))
            continue
        for d in m.get("dependencies", []):
            dl = str(d.get("layer", "")).lower().strip()
            if dl not in lv:
                unknown.append("dependency '%s' of '%s': layer '%s'" % (d.get("name", "?"), m.get("name", "?"), dl))
                continue
            if lv[sl] < lv[dl]:
                violations.append((m.get("name", "?"), sl, lv[sl], d.get("name", "?"), dl, lv[dl]))
            else:
                ok += 1
    print("=== Dependency Rule (CA12 p.3): %s ===" % name)
    print("Modules: %d | conforming dependencies: %d | violations: %d | unknown layers: %d" % (len(mods), ok, len(violations), len(unknown)))
    for s, sl, sn, t, tl, tn in violations:
        print("  VIOLATION [from source] (CA12 p.3): '%s' (%s, level %d) depends on '%s' (%s, level %d), which is further out." % (s, sl, sn, t, tl, tn))
        print("            Remedy described in CA12 p.5-6: the inner circle declares an interface and the outer one implements it (DIP).")
    for u in unknown:
        print("  UNKNOWN %s (provide 'layer_levels' in the JSON)" % u)
    if violations:
        return 1
    if unknown:
        return 2
    print("No violations in the given graph (validity depends on the graph reflecting the real code).")
    return 0


DEMO = {
    "name": "demo",
    "modules": [
        {"name": "OrderEntity", "layer": "entities", "dependencies": []},
        {"name": "CreateOrder", "layer": "use_cases", "dependencies": [{"name": "OrderEntity", "layer": "entities"}, {"name": "OrderOutputPort", "layer": "use_cases"}]},
        {"name": "OrderController", "layer": "interface_adapters", "dependencies": [{"name": "CreateOrder", "layer": "use_cases"}]},
        {"name": "SqlOrderRepository", "layer": "frameworks_drivers", "dependencies": [{"name": "OrderOutputPort", "layer": "use_cases"}]},
        {"name": "BadEntity", "layer": "entities", "dependencies": [{"name": "HttpRequest", "layer": "frameworks_drivers"}]},
    ],
}


def main():
    ap = argparse.ArgumentParser(description="Validates the Dependency Rule on a graph described in JSON.")
    ap.add_argument("--file", help="JSON with modules and dependencies")
    ap.add_argument("--demo", action="store_true", help="sample graph (contains 1 deliberate violation)")
    ap.add_argument("--layers", action="store_true", help="show the layer mapping and its origin")
    a = ap.parse_args()
    if a.layers:
        print("Levels [from source] CA12 p.3-5:")
        for k, v in CANON.items():
            print("  %d %s" % (v, k))
        print("Aliases [extrapolation]:")
        for k, v in ALIASES.items():
            print("  %d %s" % (v, k))
        return 0
    if a.demo:
        return validate(DEMO)
    if a.file:
        try:
            with open(a.file, encoding="utf-8") as f:
                return validate(json.load(f))
        except (OSError, ValueError) as e:
            print("Error reading %s: %s" % (a.file, e), file=sys.stderr)
            return 2
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

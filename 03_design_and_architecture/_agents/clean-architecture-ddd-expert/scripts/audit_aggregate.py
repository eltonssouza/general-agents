#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_aggregate.py - checklist for a DDD aggregate described in JSON. Read-only, no network.

Each rule declares its ORIGIN. Page convention: N = PDF page (DDD: printed = N - 7).
  A1  [from source] DDD p.23  : the aggregate must have a root (one entity chosen as the root).
  A2  [from source] DDD p.23  : external objects hold references only to the root (direct external access to an internal member is an error).
  A3  [from source] DDD p.24  : repositories only for roots that need direct access (a repository for an internal entity is an error).
  A4  [from source] DDD p.19  : Value Objects are treated as immutable.
  A5  [from source] DDD p.23  : properties and invariants defined for the aggregate as a whole (no declared invariants: warning).
  A6  [inference] from DDD p.23: across aggregates, updates are asynchronous; changing several aggregates in the same
      local transaction is a sign to reconsider the model (warning, not error).
  A7  [extrapolation]         : referencing another aggregate by identifier (rather than by object pointer) is a
      widespread practice in later literature; the booklet does NOT say this (warning, not error).
Errors (A1-A4) = violation of something stated in the text; warnings (A5-A7) = inference/extrapolation.

JSON input (all fields optional):
  {"name": "...", "root_entity": "Order",
   "internal_entities": [{"name": "OrderItem", "has_direct_repository": false, "external_direct_access": false}],
   "value_objects": [{"name": "Money", "immutable": true}],
   "external_references": [{"target_aggregate": "Customer", "type": "id" | "direct_pointer"}],
   "invariants": ["..."], "modifies_multiple_aggregates": false}

Usage: python -I scripts/audit_aggregate.py --demo | --file agregado.json
Exit: 0 no errors (warnings do not fail), 1 with errors, 2 invalid usage/file.
"""
import argparse
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def audit(agg):
    name = agg.get("name", "(unnamed)")
    root = agg.get("root_entity")
    internals = agg.get("internal_entities", [])
    vos = agg.get("value_objects", [])
    refs = agg.get("external_references", [])
    invariants = agg.get("invariants", [])
    multi = agg.get("modifies_multiple_aggregates", False)
    errors, warns, oks = [], [], []

    if not root:
        errors.append("A1 [from source] (DDD p.23): no root is defined; the pattern says to choose one entity as the root.")
    else:
        oks.append("A1 root '%s' defined (DDD p.23)." % root)
    for e in internals:
        en = e.get("name", "(internal entity)")
        if e.get("external_direct_access"):
            errors.append("A2 [from source] (DDD p.23): '%s' is accessed directly from outside; external objects must hold a reference only to the root." % en)
        if e.get("has_direct_repository"):
            errors.append("A3 [from source] (DDD p.24): '%s' has its own repository; repositories are for roots that need direct access." % en)
    for v in vos:
        vn = v.get("name", "(VO)")
        if v.get("immutable", True) is False:
            errors.append("A4 [from source] (DDD p.19): Value Object '%s' is marked as mutable; the pattern says to treat it as immutable." % vn)
        else:
            oks.append("A4 VO '%s' immutable (DDD p.19)." % vn)
    if not invariants:
        warns.append("A5 [from source] (DDD p.23): no invariant declared; the pattern asks for properties and invariants for the aggregate as a whole, enforced by the root.")
    else:
        oks.append("A5 %d invariant(s) declared (DDD p.23)." % len(invariants))
    if multi:
        warns.append("A6 [inference] (from DDD p.23): several aggregates changed in the same local transaction; the text says that across boundaries the update is asynchronous. Reconsider the model or the boundary.")
    for r in refs:
        tgt = r.get("target_aggregate", "(?)")
        if str(r.get("type", "direct_pointer")).lower() == "direct_pointer":
            warns.append("A7 [extrapolation]: object-pointer reference to aggregate '%s'. The booklet does not forbid it; the practice of referencing by identifier comes from later literature." % tgt)
        else:
            oks.append("A7 reference to '%s' by identifier (widespread practice, [extrapolation])." % tgt)

    print("=== Aggregate checklist: %s ===" % name)
    print("Root: %s | internal entities: %d | VOs: %d | invariants: %d" % (root or "(none)", len(internals), len(vos), len(invariants)))
    for o in oks:
        print("  OK      %s" % o)
    for w in warns:
        print("  WARNING %s" % w)
    for e in errors:
        print("  ERROR   %s" % e)
    print("Summary: %d error(s), %d warning(s). Errors = contradicts the text; warnings = inference/extrapolation." % (len(errors), len(warns)))
    return 1 if errors else 0


DEMO = {
    "name": "Order (demo)", "root_entity": "Order",
    "internal_entities": [{"name": "OrderItem", "has_direct_repository": False, "external_direct_access": False}],
    "value_objects": [{"name": "Money", "immutable": True}, {"name": "ShippingAddress", "immutable": True}],
    "external_references": [{"target_aggregate": "Customer", "type": "id"}],
    "invariants": ["the total is the sum of the items", "a shipped order accepts no new items"],
    "modifies_multiple_aggregates": False,
}


def main():
    ap = argparse.ArgumentParser(description="DDD aggregate checklist (rules with a declared origin).")
    ap.add_argument("--file", help="JSON describing the aggregate")
    ap.add_argument("--demo", action="store_true", help="audit a sample aggregate")
    a = ap.parse_args()
    if a.demo:
        return audit(DEMO)
    if a.file:
        try:
            with open(a.file, encoding="utf-8") as f:
                return audit(json.load(f))
        except (OSError, ValueError) as e:
            print("Error reading %s: %s" % (a.file, e), file=sys.stderr)
            return 2
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

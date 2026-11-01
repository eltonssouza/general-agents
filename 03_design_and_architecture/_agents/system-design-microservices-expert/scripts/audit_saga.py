#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_saga.py - deterministic checklist for the design of a Saga described in JSON.

ORIGIN OF THE RULES (each finding prints its origin; nothing here is a "book rule" without a page):
  S1  2PC across services ............ [from source] SBC p.3; JMG p.63; MS-MIC p.49 (against scale/autonomy)
  S2  compensation on steps that can
      be undone ...................... [from source] MS-CLD p.102-103 (compensations undo the earlier local transactions)
                                       [extrapolation] the notion of "pivot" (point of no return) is Chris Richardson's, outside the corpus
  S3  steps after the pivot: retry with
      idempotent receiver ............ [from source] SBC p.2 (retry + Idempotent Receiver); pivot = [extrapolation]
  S4  more than one pivot ............ [extrapolation] (heuristic; no page)
  S5  publishing an event without Outbox [from source] MS-MIC p.158-160 and EDS p.75 (database + event atomicity)
  S6  non-idempotent consumer ........ [from source] MS-MIC p.164-165; EDS p.127 (retries produce duplicates)
  S7  chain of 3+ synchronous calls .. [from source] MS-MIC p.50-51; MS-CLD p.79 (synchronous HTTP chains)
  S8  note on orchestration vs
      choreography ................... [from source] EDS p.55; MS-CLD p.103 (trade-offs)

Input JSON format (the old keys is_pivot/has_compensation/compensation_action/outbox_pattern are also accepted):
{ "name": "...", "type": "orchestration|choreography", "uses_distributed_transaction": false,
  "steps": [ {"name": "...", "service": "...", "pivot": false, "compensation": "action or null", "idempotent": true,
              "publishes_event": true, "outbox": false, "sync": false} ] }

Usage:
  python -I scripts/audit_saga.py --demo
  python -I scripts/audit_saga.py --file tests/fixtures/saga_bad.json [--format json] [--strict]
Exit: 0 without ERROR; 1 with ERROR (or ALERT with --strict); 2 incorrect usage/invalid file.
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

DEMO = {
    "name": "E-commerce order (example)",
    "type": "orchestration",
    "uses_distributed_transaction": False,
    "steps": [
        {"name": "Reserve stock", "service": "Inventory", "pivot": False, "compensation": "Release reservation",
         "idempotent": True, "publishes_event": True, "outbox": True, "sync": False},
        {"name": "Authorize card", "service": "Payment", "pivot": True, "compensation": None,
         "idempotent": True, "publishes_event": True, "outbox": True, "sync": False},
        {"name": "Create shipment", "service": "Shipping", "pivot": False, "compensation": None,
         "idempotent": True, "publishes_event": True, "outbox": True, "sync": False},
        {"name": "Send email", "service": "Notification", "pivot": False, "compensation": None,
         "idempotent": True, "publishes_event": False, "outbox": False, "sync": False},
    ],
}


def step_get(s, new, old, default=None):
    if new in s:
        return s[new]
    return s.get(old, default)


def audit(saga):
    findings = []

    def add(level, rule, msg, source):
        findings.append({"level": level, "rule": rule, "message": msg, "source": source})

    steps = saga.get("steps") or []
    mode = str(saga.get("type", "choreography")).lower()
    if not steps:
        add("ERROR", "S0", "The saga has no steps.", "structure")
        return findings
    names = []
    for i, s in enumerate(steps):
        nm = s.get("name")
        if not nm:
            add("ERROR", "S0", f"Step {i + 1} has no 'name'.", "structure")
        names.append(nm or f"step-{i + 1}")

    if saga.get("uses_distributed_transaction"):
        add("ALERT", "S1", "The saga declares a distributed transaction/2PC across services. The sources advise against it: it holds "
            "stateful resources throughout the flow and hurts scale and autonomy.", "[from source] SBC p.3; JMG p.63; MS-MIC p.49")

    pivots = [i for i, s in enumerate(steps) if step_get(s, "pivot", "is_pivot", False)]
    if len(pivots) > 1:
        add("ALERT", "S4", f"More than one pivot declared (steps {[i + 1 for i in pivots]}); the usual scheme allows a single point of no return.",
            "[extrapolation] Richardson heuristic, outside the corpus")
    pivot = pivots[0] if pivots else None

    for i, s in enumerate(steps):
        nm = names[i]
        comp = step_get(s, "compensation", "compensation_action", None)
        if comp is None and step_get(s, "has_compensation", "has_compensation", False):
            comp = "(declared)"
        has_comp = bool(comp)
        idem = bool(s.get("idempotent", False))
        pub = bool(s.get("publishes_event", True))
        outbox = bool(step_get(s, "outbox", "outbox_pattern", False))
        is_last = i == len(steps) - 1

        # S2: compensation
        if pivot is not None:
            if i < pivot and not has_comp:
                add("ERROR", "S2", f"'{nm}' comes before the pivot and has no compensation: if a later step fails, the state becomes inconsistent.",
                    "[from source] MS-CLD p.102-103; pivot = [extrapolation]")
        else:
            if not is_last and not has_comp:
                add("ERROR", "S2", f"'{nm}' is not the last step and has no compensation; a later failure would leave the effect undone "
                    "(declare a pivot if this step is the point of no return).", "[from source] MS-CLD p.102-103")
        # S3 / S6: idempotency
        if pivot is not None and i > pivot:
            if not idem:
                add("ALERT", "S3", f"'{nm}' comes after the pivot and is not idempotent; the typical recovery is retry, which requires an idempotent receiver.",
                    "[from source] SBC p.2; pivot = [extrapolation]")
        elif not idem:
            add("ALERT", "S6", f"'{nm}' is not idempotent; with repeated delivery/retry there will be duplicate effects.",
                "[from source] MS-MIC p.164-165; EDS p.127")
        # S5: outbox
        if pub and not outbox:
            add("ALERT", "S5", f"'{nm}' publishes an event without Outbox/CDC/Event Sourcing: risk of a lost or phantom event between database and broker.",
                "[from source] MS-MIC p.158-160; EDS p.75")

    # S7: synchronous chain
    run = best = 0
    for s in steps:
        run = run + 1 if s.get("sync") else 0
        best = max(best, run)
    if best >= 3:
        add("ALERT", "S7", f"There are {best} consecutive synchronous steps (call chain): blocking, coupling, and cascading failure.",
            "[from source] MS-MIC p.50-51; MS-CLD p.79")

    if mode == "orchestration":
        add("INFO", "S8", "Orchestration: the flow is written in one place (easy to reason about), but couples the participants to the orchestrator.",
            "[from source] EDS p.55; MS-CLD p.103")
    else:
        add("INFO", "S8", "Choreography: pluggable services, no central controller; harder to see the whole flow.",
            "[from source] EDS p.55; MS-CLD p.103 (the difficulty of seeing the flow is [inference])")
    return findings


def render_text(saga, findings):
    steps = saga.get("steps") or []
    print(f"=== Audit of saga '{saga.get('name', 'unnamed')}' ({str(saga.get('type', 'choreography')).lower()}) ===")
    print(f" Steps: {len(steps)}")
    for i, s in enumerate(steps, 1):
        flags = []
        if step_get(s, "pivot", "is_pivot", False):
            flags.append("PIVOT")
        if step_get(s, "compensation", "compensation_action", None) or s.get("has_compensation"):
            flags.append("compensable")
        if s.get("idempotent"):
            flags.append("idempotent")
        if step_get(s, "outbox", "outbox_pattern", False):
            flags.append("outbox")
        if s.get("sync"):
            flags.append("sync")
        print(f"  [{i}] {s.get('name', '?')} ({s.get('service', '?')}) {' '.join(flags)}")
    for lvl in ("ERROR", "ALERT", "INFO"):
        sel = [f for f in findings if f["level"] == lvl]
        if not sel:
            continue
        print(f"--- {lvl} ({len(sel)}) ---")
        for f in sel:
            print(f" [{f['rule']}] {f['message']}\n     source: {f['source']}")
    if not any(f["level"] in ("ERROR", "ALERT") for f in findings):
        print(" No errors/alerts under the rules above (this does not prove the saga is correct).")


def main():
    ap = argparse.ArgumentParser(description="Saga checklist with the origin declared per rule.")
    ap.add_argument("--file")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--strict", action="store_true", help="ALERT also fails")
    a = ap.parse_args()
    if a.demo:
        saga = DEMO
    elif a.file:
        if not os.path.exists(a.file):
            print(f"File not found: {a.file}", file=sys.stderr)
            return 2
        try:
            with open(a.file, "r", encoding="utf-8") as f:
                saga = json.load(f)
        except (OSError, ValueError) as e:
            print(f"Invalid JSON: {e}", file=sys.stderr)
            return 2
    else:
        ap.print_help()
        return 2
    if not isinstance(saga, dict):
        print("The JSON must be an object.", file=sys.stderr)
        return 2
    findings = audit(saga)
    if a.format == "json":
        print(json.dumps({"saga": saga.get("name"), "findings": findings}, ensure_ascii=False, indent=1))
    else:
        render_text(saga, findings)
    bad = any(f["level"] == "ERROR" for f in findings) or (a.strict and any(f["level"] == "ALERT" for f in findings))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

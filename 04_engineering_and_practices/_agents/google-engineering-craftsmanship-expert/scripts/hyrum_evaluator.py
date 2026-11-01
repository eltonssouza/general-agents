# -*- coding: utf-8 -*-
"""
hyrum_evaluator.py - checklist of observable behaviors to investigate when changing an API (Hyrum's Law).

It does NOT compute a "risk score": SWE-G gives no weights or numeric bands. Hyrum's Law is in
SWE-G p.15 (statement), p.16-17 (hash order example) and p.26 (TL;DR). For each chosen factor the script
lists what to ask and the origin:
  - iteration_order: [from source] SWE-G p.16-17 (hash order; the caller of an RPC may depend on the order
    of serialized values, p.16; some languages randomize the order to avoid dependencies, p.17).
  - default_values: [from source] SWE-G p.183 (note 7: slightly randomizing default values in tests makes it
    harder for engineers to depend on the defaults).
  - reflection_dynamic_access: [from source] SWE-G p.110 (string access via getattr makes search and validation harder).
  - error_message_text, timing_and_latency, undocumented_fields, whitespace_and_formatting:
    [extrapolation] (common applications of Hyrum's Law; the book covers them only generically on p.15-16).
Offline; read-only. Usage: python -I scripts/hyrum_evaluator.py --clients 500 --factors iteration_order error_message_text
"""
import argparse
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FACTORS = {
    "iteration_order": {
        "name": "Collection iteration order (hash)",
        "label": "[from source]", "source": "SWE-G p.16-17",
        "ask": "Could anyone (or some indirect caller, for example via RPC) depend on the order in which elements come out? Is there a way to change the order between runs or versions to avoid dependencies?",
    },
    "default_values": {
        "name": "Default values of unset fields",
        "label": "[from source]", "source": "SWE-G p.183 (note 7)",
        "ask": "Do tests or clients pin the default values? Slightly randomizing defaults in tests makes this dependency harder.",
    },
    "reflection_dynamic_access": {
        "name": "Dynamic/reflective access by string",
        "label": "[from source]", "source": "SWE-G p.110",
        "ask": "Are there accesses by name (getattr/reflection) that text search does not find? Validation and testing become hard in those cases.",
    },
    "error_message_text": {
        "name": "Error message text",
        "label": "[extrapolation]", "source": "no page (application of Hyrum's Law, SWE-G p.15)",
        "ask": "Do clients parse the error text? Are there structured error codes?",
    },
    "timing_and_latency": {
        "name": "Timing and latency",
        "label": "[extrapolation]", "source": "no page (application of Hyrum's Law, SWE-G p.15)",
        "ask": "Does any client depend on an accidental latency or temporal ordering (hidden race conditions)?",
    },
    "undocumented_fields": {
        "name": "Undocumented fields",
        "label": "[extrapolation]", "source": "no page (application of Hyrum's Law, SWE-G p.15)",
        "ask": "Are there consumers of fields that were never promised in the contract? A global usage search (Code Search) can list them.",
    },
    "whitespace_and_formatting": {
        "name": "Formatting and whitespace in text outputs",
        "label": "[extrapolation]", "source": "no page (application of Hyrum's Law, SWE-G p.15)",
        "ask": "Do downstream scripts parse by columns or split on whitespace?",
    },
}

LAW = ("With a sufficient number of users of an API, it does not matter what you promise in the contract: "
       "all observable behaviors of the system will be depended on by somebody (SWE-G p.15, paraphrase).")


def main():
    ap = argparse.ArgumentParser(description="Hyrum's Law checklist (SWE-G p.15-17; PDF pages).")
    ap.add_argument("--clients", type=int, default=0, help="estimated number of clients (informational only)")
    ap.add_argument("--factors", nargs="+", choices=sorted(FACTORS), default=["iteration_order", "error_message_text"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    out = {
        "law": LAW,
        "estimated_clients": a.clients,
        "note": "No scoring: the book defines no weights. More users and more time increase the chance of dependency, "
                "and how hard a change is depends on how useful the behavior is to users (SWE-G p.16).",
        "mitigation": [
            {"text": "The law can be mitigated, never eradicated; be clear about the interface's promises versus its flexibility.", "label": "[from source]", "source": "SWE-G p.16"},
            {"text": "If clients must change, the infrastructure takes over the migration (Churn Rule) and uses the LSC process.", "label": "[from source]", "source": "SWE-G p.19; p.316-328"},
            {"text": "Run the dependents' CI tests; what is not in CI does not count (Beyonce Rule).", "label": "[from source]", "source": "SWE-G p.19; p.157"},
        ],
        "factors": [dict(id=k, **FACTORS[k]) for k in a.factors],
    }
    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    print("=== Hyrum's Law Checklist ===")
    print(out["law"])
    if a.clients:
        print("Estimated clients: %d (informational only)" % a.clients)
    print(out["note"] + "\n")
    for fct in out["factors"]:
        print("- %s %s [%s]" % (fct["name"], fct["label"], fct["source"]))
        print("    Ask: " + fct["ask"])
    print("\nMitigations:")
    for m in out["mitigation"]:
        print("- %s %s (%s)" % (m["text"], m["label"], m["source"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

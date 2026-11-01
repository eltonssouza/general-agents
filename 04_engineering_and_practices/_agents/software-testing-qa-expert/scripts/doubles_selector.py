# -*- coding: utf-8 -*-
"""
doubles_selector.py - decision tree for choosing the test double technique.

ORIGIN OF THE RULES (PDF pages of Software-Engineering-at-Google-completo.pdf, ch. 13):
  1. The real implementation is the first choice if it is fast, deterministic and has simple dependencies (SWE-G p.189, p.191)
  2. If the real one does not fit, the fake is usually ideal (SWE-G p.192-193); the API owner writes and maintains it (p.193)
  3. Stubbing to drive the system into a state or simulate an error/value that the real one and the fake do not produce (SWE-G p.197)
  4. Interaction testing only when neither real nor fake can be used, or when the number/order of calls matters,
     and only for functions that change state (SWE-G p.198-199)
  5. "Dummy" (a value passed only to fill the signature) is a Meszaros term: [extrapolation], it is NOT in the book.
The PRIORITY ORDER between rules 3 and 4 when both apply is an [inference] of this package.
Read-only, no network. Usage: python -I doubles_selector.py --slow-or-unhermetic --stateful-collaborator
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def select_test_double(uninvoked=False, slow_or_unhermetic=False, stateful=False,
                       fault_injection=False, verify_interactions=False, fake_available=False):
    also = []
    if uninvoked:
        return {
            "recommended": "'Dummy' value (parameter that is never used)",
            "label": "[extrapolation]",
            "citation": "Meszaros term; not in SWE-G or MOCK",
            "rationale": "The collaborator only fills the signature and is never called; use a simple or null value.",
            "risks": "If it is called, the test should fail clearly.",
            "also_consider": [],
        }
    real_viable = not slow_or_unhermetic and not fault_injection and not verify_interactions
    if real_viable:
        return {
            "recommended": "Real implementation",
            "label": "[from source]",
            "citation": "SWE-G p.189, p.191",
            "rationale": "If the dependency is fast, deterministic and has simple dependencies, the book prefers it over any double; it gives more fidelity.",
            "risks": "A bug in the real one breaks the test; the book considers that desirable (SWE-G p.190).",
            "also_consider": [],
        }
    if fault_injection:
        also.append("Prefer the fake if it already lets you trigger the error; use a stub when neither the real one nor the fake produces the value or error (SWE-G p.197).")
        if verify_interactions:
            also.append("For the side effect, verify interaction only on state-changing functions (SWE-G p.198-199).")
        return {
            "recommended": "Stub (few functions, directly related to the assertions)",
            "label": "[from source]",
            "citation": "SWE-G p.195-197",
            "rationale": "Stubbing is for driving the system into a state or simulating values/errors that the real one or the fake do not produce.",
            "risks": "Too many stubs make tests unclear, brittle and less effective (SWE-G p.195-196); a test that needs many stubs may point to code that should be refactored (SWE-G p.197).",
            "also_consider": also,
        }
    if verify_interactions:
        if stateful:
            also.append("If the resulting state is observable, prefer state testing with the real one or a fake (SWE-G p.197-198).")
        also.append("Consider complementing with a larger-scope test using state testing (SWE-G p.198).")
        return {
            "recommended": "Interaction testing (minimal verify)",
            "label": "[from source]",
            "citation": "SWE-G p.197-200",
            "rationale": "Legitimate when neither real nor fake can be used, or when the number/order of calls matters (e.g. cache); only for state-changing functions (e.g. sendEmail).",
            "risks": "Leaks implementation details and does not prove the system works; abuse produces change-detector tests (SWE-G p.198); avoid over-specifying (SWE-G p.199-200).",
            "also_consider": also,
        }
    # slow or non-hermetic, with no need for a stub or interaction
    if fake_available:
        return {
            "recommended": "Existing fake (maintained by the API owner)",
            "label": "[from source]",
            "citation": "SWE-G p.192-194",
            "rationale": "When the real one does not fit, the fake is usually the best option; check that it has tests against the real one (contract tests).",
            "risks": "Fidelity to the API contract may drift over time if the fake is not tested (SWE-G p.194).",
            "also_consider": [],
        }
    also.append("No fake: ask the API owner; otherwise wrap the API in a class and fake that (SWE-G p.194-195).")
    also.append("Alternatives: keep the real one and accept the cost, or another technique with its trade-offs (SWE-G p.195).")
    return {
        "recommended": "Fake (create it with the API owner, or fake a wrapper)",
        "label": "[from source]",
        "citation": "SWE-G p.192-195",
        "rationale": "The real one is slow or non-hermetic; the fake is the best option and should be maintained and tested by whoever maintains the API (SWE-G p.193-194)." + (" The collaborator has state; a fake allows state testing (SWE-G p.196)." if stateful else ""),
        "risks": "Cost of writing and maintaining the fake; it only pays off if the gain outweighs the cost (SWE-G p.195).",
        "also_consider": also,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--uninvoked-dummy", action="store_true", help="the object only fills the signature and is never called")
    ap.add_argument("--slow-or-unhermetic", action="store_true", help="the real one is slow, uses network/disk or is non-deterministic")
    ap.add_argument("--stateful-collaborator", action="store_true", help="the collaborator keeps state (e.g. a database)")
    ap.add_argument("--fault-injection", action="store_true", help="I need a specific value or error that the real one/fake do not produce")
    ap.add_argument("--verify-interactions", action="store_true", help="I need to verify a side effect or the number/order of calls")
    ap.add_argument("--fake-available", action="store_true", help="a fake maintained by the API owner already exists")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = select_test_double(a.uninvoked_dummy, a.slow_or_unhermetic, a.stateful_collaborator,
                             a.fault_injection, a.verify_interactions, a.fake_available)
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
    print("=== Test double selector ===")
    print("Recommendation: %s %s" % (res["recommended"], res["label"]))
    print("Citation: (%s)" % res["citation"])
    print("Rationale: %s" % res["rationale"])
    print("Risks: %s" % res["risks"])
    for x in res["also_consider"]:
        print("Also consider: %s" % x)
    print("Note: the priority order between rules is an [inference]; the individual rules come from SWE-G ch. 13 (p.184-201).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

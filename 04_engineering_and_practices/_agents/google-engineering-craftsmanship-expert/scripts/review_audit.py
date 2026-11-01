# -*- coding: utf-8 -*-
"""
review_audit.py - checklist for a Change List (CL) based on what SWE-G says about code review.

It does NOT compute a score or numeric verdict: the book gives no scoring. Each item reports its origin
(SWE-G PDF page) and whether it is [from source], [inference] or [DATED].

Rules and origin:
  - Size: "small" is around 200 lines (SWE-G p.129); Google has NO automatic rejection by line limit
    and the definition of small is fuzzy (SWE-G p.117). The SWE-PREV article p.7-8 cites old size labels
    (30-99 medium, 300-999 large, 1000-1999 freakin huge) [DATED]. The value 200 is a reference, not a limit.
  - Description: first line as a summary, and what/why (SWE-G p.129-130).
  - Tests: behavior changes and bug fixes should have tests (SWE-G p.131-132).
  - Presubmit: a presubmit failure blocks sending or committing (SWE-G p.284, p.294).
  - Approvals: three aspects (LGTM, owner, readability), which may be implicit if the author already has them
    (SWE-G p.122-123). Critique criterion: at least one LGTM, enough approvals and no unresolved
    comments (SWE-G p.286).
  - Reviewer feedback within 24 business hours is the expectation (SWE-G p.128).
Offline; read-only. Usage: python -I scripts/review_audit.py --lines 150 [--no-tests] [--json]
"""
import argparse
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SMALL_REF = 200  # SWE-G p.129 ("about 200 lines")


def audit(a):
    f = []

    def add(status, rule, text, src, label="[from source]"):
        f.append({"status": status, "rule": rule, "text": text, "source": src, "label": label})

    # 1. size
    if a.lines <= SMALL_REF:
        add("OK", "Size", "%d lines: within the reference of about 200 lines." % a.lines, "SWE-G p.129")
    else:
        add("WARNING", "Size",
            "%d lines: above the reference of about 200 lines. The book treats this as an optimization, not as a hard "
            "limit, and there is no automatic rejection (p.117); consider slicing into smaller changes." % a.lines,
            "SWE-G p.129; p.117")
    add("INFO", "Old labels", "The 2017 article cites size labels (30-99 medium; 300-999 large; 1000-1999 freakin huge); "
        "more recent versions use S, M, L, XL.", "SWE-PREV p.7-8", "[DATED]")

    # 2. description
    if a.no_why:
        add("MISSING", "Description", "The description should have a first summary line and explain what changed and why.", "SWE-G p.129-130")
    else:
        add("OK", "Description", "Description with summary and motivation.", "SWE-G p.129-130")

    # 3. tests
    if a.no_tests:
        add("MISSING", "Tests", "Reviewers usually require tests for new functionality; a bug fix should include the test that was missing.",
            "SWE-G p.131-132; SWE-PREV p.8")
    else:
        add("OK", "Tests", "There are tests for the change.", "SWE-G p.131-132")

    # 4. presubmit
    if a.presubmit_fail:
        add("MISSING", "Presubmit", "A presubmit failure blocks sending for review or the commit.", "SWE-G p.284; p.294")
    else:
        add("OK", "Presubmit", "Presubmits (formatting, tests, project invariants) passed.", "SWE-G p.284; p.294")

    # 5. approvals
    if a.no_lgtm:
        add("MISSING", "LGTM", "At least one LGTM from another engineer is missing (correctness and comprehension).", "SWE-G p.122; p.286")
    else:
        add("OK", "LGTM", "LGTM obtained.", "SWE-G p.122; p.286")
    if a.no_owners:
        add("MISSING", "Owner", "Approval from a directory owner is missing (may be implicit if the author is an owner).", "SWE-G p.122-124")
    else:
        add("OK", "Owner", "Owner approval present or implicit.", "SWE-G p.122-124")
    if a.no_readability:
        add("MISSING", "Readability", "Language readability approval is missing (implicit if the author has it).", "SWE-G p.123")
    else:
        add("OK", "Readability", "Readability present or implicit.", "SWE-G p.123")

    # 6. unresolved comments
    if a.unresolved > 0:
        add("MISSING", "Comments", "%d unresolved comment(s): they are 'soft' requirements, but must be handled before the commit." % a.unresolved,
            "SWE-G p.286; p.128")
    else:
        add("OK", "Comments", "No unresolved comments.", "SWE-G p.286")

    ready = not (a.no_lgtm or a.no_owners or a.no_readability or a.presubmit_fail or a.unresolved > 0)
    summary = {
        "ready_to_commit_by_critique_criterion": ready,
        "criterion": "at least one LGTM, enough approvals, no unresolved comments and green presubmits (SWE-G p.284; p.286)",
        "findings": f,
        "note": "Checklist without scoring: the book defines no grade. The --files parameter is accepted for compatibility and ignored.",
    }
    return summary


def main():
    ap = argparse.ArgumentParser(description="CL checklist (origin: SWE-G Ch. 9 and 19; PDF pages).")
    ap.add_argument("--lines", type=int, default=150, help="changed lines")
    ap.add_argument("--files", type=int, default=0, help="ignored (compatibility)")
    ap.add_argument("--no-tests", action="store_true")
    ap.add_argument("--no-why", action="store_true")
    ap.add_argument("--no-lgtm", action="store_true")
    ap.add_argument("--no-owners", action="store_true")
    ap.add_argument("--no-readability", action="store_true")
    ap.add_argument("--presubmit-fail", action="store_true")
    ap.add_argument("--unresolved", type=int, default=0, help="number of unresolved comments")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = audit(a)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0
    print("=== Code Review Checklist (SWE-G Ch. 9 and 19; PDF pages) ===")
    print("Ready to commit by the Critique criterion (p.286): %s\n" % ("YES" if r["ready_to_commit_by_critique_criterion"] else "NO"))
    for x in r["findings"]:
        print("  [%-7s] %-14s %s (%s) %s" % (x["status"], x["rule"], x["text"], x["source"], x["label"]))
    print("\n" + r["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

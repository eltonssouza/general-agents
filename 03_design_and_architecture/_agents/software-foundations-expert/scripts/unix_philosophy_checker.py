# -*- coding: utf-8 -*-
"""
unix_philosophy_checker.py - checklist of the 17 Unix philosophy rules (TAUP ch. 1) to evaluate a tool/architecture.

ORIGIN OF THE RULES (declared):
- [from source] The NAMES and principles of the 17 rules and the pages (PDF) come from TAUP p.37-50 (list at p.37-38; discussion
  of each rule on the pages indicated). Printed page = PDF - 2. Paraphrases; no copying of the text.
- [extrapolation] The verification QUESTIONS ("checks" field), the WEIGHTS (+/-), the 0-100 score and the PRESETS are
  OUR heuristics: the book has no scoring system and does not say that "n points" indicate conformance. Use the output
  as a review script, not as a measure from the book.
- [DATED] TAUP examples and context are from 2003 (see references/INDEX.md).

Usage:
  python -I scripts/unix_philosophy_checker.py --preset chatty_cli
  python -I scripts/unix_philosophy_checker.py --set silent_on_success=1,pipe_friendly=1,chatty_output=0
  python -I scripts/unix_philosophy_checker.py --profile my_profile.json     (JSON {"check_id": true/false})
  python -I scripts/unix_philosophy_checker.py --list-checks | --rules
Output: 0 ok; 2 usage error (unknown check). No network; read-only.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# (n, name, PDF pages, principle, checks[(id, question, weight)])
UNIX_RULES = [
    (1, "Rule of Modularity", "TAUP p.38-39",
     "Simple parts connected by clean interfaces.",
     [("monolithic_coupling", "Is there tight coupling between heterogeneous components?", -2),
      ("clear_apis", "Are the interfaces between modules explicit and minimal?", +2)]),
    (2, "Rule of Clarity", "TAUP p.39",
     "Clarity is better than cleverness.",
     [("arcane_tricks", "Does it use obscure tricks to gain little performance?", -2),
      ("readable_intent", "Does the code express its intent directly?", +2)]),
    (3, "Rule of Composition", "TAUP p.39-40",
     "Design programs to be connected to other programs.",
     [("closed_ecosystem", "Does it prevent redirection/pipes or require its own tool to be used?", -3),
      ("pipe_friendly", "Does it accept a plain text stream as input and emit a clean stream as output?", +3)]),
    (4, "Rule of Separation", "TAUP p.40-41",
     "Separate policy from mechanism and interfaces from engines.",
     [("hardcoded_policy", "Is the engine tied to presentation/policy rules?", -2),
      ("clean_engine", "Is the engine independent of the interface and the policy?", +2)]),
    (5, "Rule of Simplicity", "TAUP p.41-42",
     "Design for simplicity; add complexity only where it is unavoidable.",
     [("overengineering", "Are there speculative layers of abstraction?", -2),
      ("kiss_design", "Does the solution use the smallest number of parts needed?", +2)]),
    (6, "Rule of Parsimony", "TAUP p.42",
     "Write a big program only when it is shown that nothing smaller will do.",
     [("kitchen_sink_bloat", "Does the tool try to solve many unrelated problems?", -2),
      ("focused_scope", "Does the tool solve a well-delimited problem?", +2)]),
    (7, "Rule of Transparency", "TAUP p.42-43",
     "Design for visibility, making inspection and debugging easy.",
     [("opaque_state", "Is the internal state accessible only with special tools?", -2),
      ("visible_inspectable", "Are there readable formats and ways to inspect the internal state?", +2)]),
    (8, "Rule of Robustness", "TAUP p.43-44",
     "Robustness is the child of transparency and simplicity.",
     [("brittle_failure", "Cascading failures due to many special cases?", -2),
      ("graceful_handling", "Does it handle unusual inputs without special cases proliferating?", +2)]),
    (9, "Rule of Representation", "TAUP p.44",
     "Fold knowledge into data so that the logic can be simple and robust.",
     [("nested_if_else", "Does the logic depend on long if/else chains instead of data?", -2),
      ("data_driven_tables", "Does it use tables/declarative data for rules?", +2)]),
    (10, "Rule of Least Surprise", "TAUP p.44-45",
     "In the interface, do the least surprising thing; follow known conventions.",
     [("unintuitive_behavior", "Do behavior or options depart from the domain's conventions?", -2),
      ("standard_conventions", "Does it follow established conventions (for example, Unix traditions)?", +2)]),
    (11, "Rule of Silence", "TAUP p.45-46, p.327",
     "When a program has nothing surprising to say, it should say nothing; only real errors go to standard error.",
     [("chatty_output", "Does it emit success/status messages on standard output?", -3),
      ("silent_on_success", "Does it stay silent on success and send only real errors to stderr?", +3)]),
    (12, "Rule of Repair", "TAUP p.46-47",
     "Repair what you can; when you must fail, fail noisily and as soon as possible.",
     [("silent_error_swallowing", "Does it swallow errors silently, leaving latent corruption?", -3),
      ("fail_fast_noisy", "Does it fail early, noisily and in a diagnosable way?", +3)]),
    (13, "Rule of Economy", "TAUP p.47",
     "Programmer time is expensive; conserve it in preference to machine time.",
     [("manual_grunt_work", "Does it require repetitive manual work that the machine could do?", -2),
      ("automation_friendly", "Is it easy to orchestrate with scripts?", +2)]),
    (14, "Rule of Generation", "TAUP p.47-48",
     "Avoid hand-hacking; write programs that write programs.",
     [("boilerplate_duplication", "Is there a lot of repetitive hand-written code that could be generated?", -2),
      ("generators_used", "Does it use code generators/DSLs where the specification is simpler than the code?", +2)]),
    (15, "Rule of Optimization", "TAUP p.48-49",
     "Prototype before polishing; get it working before optimizing.",
     [("premature_optimization", "Are there local optimizations without measurements to justify them?", -2),
      ("profile_driven", "Do the optimizations follow measurements?", +2)]),
    (16, "Rule of Diversity", "TAUP p.49-50",
     "Distrust all claims for 'one true way'.",
     [("dogmatic_lockin", "Does it demand a single language/framework and close itself off from the rest?", -2),
      ("polyglot_flexibility", "Does it interoperate with other tools and languages?", +2)]),
    (17, "Rule of Extensibility", "TAUP p.50",
     "Design for the future; self-describing, versioned formats.",
     [("rigid_binary_format", "Rigid format, with no version and no room to grow?", -2),
      ("extensible_schema", "Self-describing formats with a version or independent clauses?", +2)]),
]

ALL_CHECKS = {cid for r in UNIX_RULES for cid, _, _ in r[4]}

# [extrapolation] our own illustrative presets (not from the book).
PRESETS = {
    "classic_unix": {c: True for c in ALL_CHECKS if c in {
        "clear_apis", "readable_intent", "pipe_friendly", "clean_engine", "kiss_design", "focused_scope",
        "visible_inspectable", "graceful_handling", "data_driven_tables", "standard_conventions",
        "silent_on_success", "fail_fast_noisy", "automation_friendly", "generators_used", "profile_driven",
        "polyglot_flexibility", "extensible_schema"}},
    "chatty_cli": {"clear_apis": True, "readable_intent": True, "chatty_output": True, "silent_error_swallowing": True,
                   "standard_conventions": False, "overengineering": True, "opaque_state": True,
                   "premature_optimization": True},
    "bloated_monolith": {"monolithic_coupling": True, "arcane_tricks": True, "closed_ecosystem": True,
                         "hardcoded_policy": True, "overengineering": True, "kitchen_sink_bloat": True,
                         "opaque_state": True, "brittle_failure": True, "nested_if_else": True,
                         "unintuitive_behavior": True, "chatty_output": True, "silent_error_swallowing": True,
                         "manual_grunt_work": True, "dogmatic_lockin": True},
    "robust_microtool": {"clear_apis": True, "readable_intent": True, "pipe_friendly": True, "clean_engine": True,
                         "kiss_design": True, "focused_scope": True, "visible_inspectable": True,
                         "graceful_handling": True, "silent_on_success": True, "fail_fast_noisy": True,
                         "automation_friendly": True, "standard_conventions": True},
}


def audit(profile):
    score = 0
    max_possible = sum(w for r in UNIX_RULES for _, _, w in r[4] if w > 0)
    results = []
    for n, name, pages, principle, checks in UNIX_RULES:
        rs, findings = 0, []
        for cid, desc, w in checks:
            if profile.get(cid):
                rs += w
                findings.append({"check": cid, "question": desc, "weight": w})
        score += rs
        results.append({"n": n, "rule": name, "citation": pages, "principle": principle,
                        "score": rs, "findings": findings})
    norm = max(0, min(100, int(round(100.0 * score / max_possible)))) if max_possible else 0
    return {"score": norm, "raw_score": score, "max_possible": max_possible, "rule_results": results,
            "label": "heuristic score [extrapolation]: weights and questions are ours, not the book's"}


def parse_set(s):
    prof = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        k, _, v = part.partition("=")
        prof[k.strip()] = v.strip().lower() in ("1", "true", "sim", "yes", "t", "y")
    return prof


def main():
    ap = argparse.ArgumentParser(description="Checklist of the 17 Unix philosophy rules (TAUP).")
    ap.add_argument("--preset", choices=sorted(PRESETS), help="illustrative profile [extrapolation]")
    ap.add_argument("--set", help="check_id=1,other=0 (enables/disables checks)")
    ap.add_argument("--profile", help="JSON file {check_id: bool}")
    ap.add_argument("--rules", action="store_true", help="list the 17 rules with pages")
    ap.add_argument("--list-checks", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.rules:
        for n, name, pages, principle, _ in UNIX_RULES:
            print("%2d. %-24s [%s] %s" % (n, name, pages, principle))
        return 0
    if a.list_checks:
        for n, name, pages, _, checks in UNIX_RULES:
            for cid, desc, w in checks:
                print("%-26s %+d  %s [%s]" % (cid, w, desc, name))
        return 0

    profile = {}
    if a.preset:
        profile.update(PRESETS[a.preset])
    if a.profile:
        with open(a.profile, encoding="utf-8") as f:
            profile.update(json.load(f))
    if a.set:
        profile.update(parse_set(a.set))
    if not profile:
        profile = dict(PRESETS["chatty_cli"])
        a.preset = "chatty_cli"
    unknown = sorted(set(profile) - ALL_CHECKS)
    if unknown:
        print("Error: unknown checks: %s (use --list-checks)" % ", ".join(unknown), file=sys.stderr)
        return 2
    res = audit(profile)
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
    print("=== Checklist of the 17 Unix philosophy rules (TAUP)%s ===" % (" - profile '%s'" % a.preset if a.preset else ""))
    print("Heuristic score: %d/100 (raw points %d/%d)" % (res["score"], res["raw_score"], res["max_possible"]))
    print("Warning: %s\n" % res["label"])
    for r in res["rule_results"]:
        if r["score"] < 0:
            print("  [VIOLATION] %s [%s]" % (r["rule"], r["citation"]))
            for f in r["findings"]:
                print("      - (%+d) %s" % (f["weight"], f["question"]))
        elif r["score"] > 0:
            print("  [CONFORMS] %s [%s]" % (r["rule"], r["citation"]))
            for f in r["findings"]:
                print("      + (%+d) %s" % (f["weight"], f["question"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

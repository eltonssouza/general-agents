# -*- coding: utf-8 -*-
"""
tdm_audit.py - checklist of Test Data Management patterns and anti-patterns.

ORIGIN OF THE RULES (DZone Refcard "Test Data Management: Patterns and Anti-Patterns for a Data Factory", PDF p.1-9):
  non-reversible masking, real data only as an exception ......... TDM p.6, p.8
  over-protecting / protecting inconsistently (masking) .......... TDM p.6
  manual profiling ............................................... TDM p.4
  data requirements captured late ................................ TDM p.3-4
  synthetic data in higher environments .......................... TDM p.5
  loose subset ................................................... TDM p.5
  virtualization with an unmasked source ......................... TDM p.5
  manual inspection / manual validation .......................... TDM p.6-7
  data list (spreadsheet) ........................................ TDM p.7
  exemptions as standard practice ................................ TDM p.8
  encryption where it is not sensible ............................ TDM p.6
[inference] "copying the whole database without subsetting" is a reading of the benefits of subsetting (TDM p.5), not a literal rule.
[extrapolation] The WEIGHTS of the score are a heuristic of this package, not from the book. Regulations: the book cites GDPR,
HIPAA and PCI (TDM p.6); LGPD does NOT appear. The script does NOT attest legal compliance.
The script only evaluates what you FLAG; absence of a flag = "not reported", not "ok".
Read-only, no network. Usage: python -I tdm_audit.py --raw-prod --manual-inspect
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# (flag, status, weight [extrapolation], rule, description, citation, label)
RULES = [
    ("raw_prod", "CRITICAL", 50, "Real data without masking",
     "Production data in a test environment without non-reversible obfuscation. The book treats masking as the standard and real data as a last-resort exception.",
     "TDM p.6, p.8", "[from source] + [inference] in the combination"),
    ("prod_exemption_routine", "FAIL", 20, "Exemption as standard practice",
     "Use of production data promoted to routine instead of a last resort with a request, documented risk and a recorded window.",
     "TDM p.8", "[from source]"),
    ("mask_everything", "FAIL", 10, "Excessive masking",
     "Masking too much increases the risk of breakage and loss of integrity; keep the scope tight, focused on primary PII.",
     "TDM p.6", "[from source]"),
    ("mask_inconsistent", "FAIL", 15, "Inconsistent masking",
     "Masking the same value in different ways in different places causes integrity problems.",
     "TDM p.6", "[from source]"),
    ("encryption_breaks_format", "FAIL", 10, "Encryption where it is not sensible",
     "Encrypted data loses its format and may violate column constraints and application logic.",
     "TDM p.6", "[from source]"),
    ("manual_profiling", "FAIL", 10, "Manual profiling",
     "With thousands of columns and billions of data points, team workshops tend to fail; automate profiling.",
     "TDM p.4", "[from source]"),
    ("late_reqs", "FAIL", 15, "Late data requirements",
     "Requirements discovered after the environment is provisioned cause delays and rework.",
     "TDM p.3-4", "[from source]"),
    ("synthetic_in_higher_env", "FAIL", 10, "Synthetic data in higher environments",
     "Fake data may not match the business rules and loses value in SIT, UAT and performance testing.",
     "TDM p.5", "[from source]"),
    ("weak_subset", "FAIL", 10, "Loose subset",
     "Needed data disappears and relationships are lost, breaking the business logic.",
     "TDM p.5", "[from source]"),
    ("virtual_unmasked_source", "FAIL", 15, "Virtualization with an unmasked source",
     "The team indirectly accesses the original source; obfuscate the sensitive data in the source before virtualizing.",
     "TDM p.5", "[from source]"),
    ("manual_inspect", "FAIL", 15, "Manual inspection",
     "Validating PII by manual inspection is not reliable with millions of changes; use automated methods.",
     "TDM p.6-7", "[from source]"),
    ("data_lists", "WARN", 5, "Test data list/spreadsheet",
     "Lists age quickly and draw everyone to the same data; prefer views and pool reservation.",
     "TDM p.7", "[from source]"),
    ("hero_or_selective_automation", "WARN", 5, "The hero / selective automation",
     "Reliance on heroic effort or on partial automation in data operations.",
     "TDM p.7", "[from source]"),
    ("full_db_copy", "WARN", 10, "Full copy without subsetting",
     "Copying the whole database ignores the benefits of subsetting (less storage and batch processing). A reading of the book, not a literal rule.",
     "TDM p.5", "[inference]"),
    ("no_reporting", "WARN", 5, "No reporting",
     "Without measuring data operations (DataOps) and security coverage (DataSec) it is hard to improve.",
     "TDM p.8", "[from source]"),
]

POSITIVE = [
    ("masked", "PASS", "Masking applied", "Dataset copied with obfuscated PII (preferably non-reversible).", "TDM p.6"),
    ("synthetic", "PASS", "Synthetic data in early phases", "Avoids production data in early phases and creates data that does not exist.", "TDM p.4-5"),
    ("subsetting", "PASS", "Subsetting", "Reduces the data footprint by a repeatable criterion.", "TDM p.5"),
    ("virtualization", "PASS", "Virtualization by deltas", "Virtual copies with deltas over the source.", "TDM p.5"),
    ("auto_validation", "PASS", "Automated PII validation", "Automatic screening that the PII was removed.", "TDM p.6-7"),
    ("auto_profiling", "PASS", "Automated profiling", "Automatic discovery of schema, relationships and PII.", "TDM p.4"),
    ("data_views", "PASS", "Data views and pool reservation", "Data that can be located and is reserved to avoid being overwritten.", "TDM p.7"),
]


def audit(flags):
    findings = []
    score = 100
    for key, status, w, rule, desc, cit, label in RULES:
        if flags.get(key):
            if key == "raw_prod" and flags.get("masked"):
                continue
            score -= w
            findings.append({"status": status, "rule": rule, "desc": desc, "citation": cit, "label": label})
    for key, status, rule, desc, cit in POSITIVE:
        if flags.get(key):
            findings.append({"status": status, "rule": rule, "desc": desc, "citation": cit, "label": "[from source]"})
    critical = any(f["status"] == "CRITICAL" for f in findings)
    fails = any(f["status"] == "FAIL" for f in findings)
    verdict = "CRITICAL FINDINGS" if critical else ("WITH FINDINGS" if fails else "NO FINDINGS IN THE REPORTED ITEMS")
    return {"verdict": verdict, "score_heuristic": max(0, score),
            "score_note": "heuristic score [extrapolation]; weights are not from the book",
            "findings": findings,
            "disclaimer": "Not legal advice: the TDM cites GDPR, HIPAA and PCI (p.6) and does not cite LGPD. Unflagged items = not reported."}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # anti-patterns
    ap.add_argument("--raw-prod", action="store_true", help="real production data without treatment")
    ap.add_argument("--exemption-routine", action="store_true", help="production exemptions treated as routine")
    ap.add_argument("--mask-everything", action="store_true", help="masking everything, including low-value artifacts")
    ap.add_argument("--mask-inconsistent", action="store_true", help="masking inconsistent across tables/applications")
    ap.add_argument("--encryption-breaks-format", action="store_true", help="encryption breaking format/constraints")
    ap.add_argument("--manual-profiling", action="store_true")
    ap.add_argument("--late-reqs", action="store_true", help="data requirements captured late")
    ap.add_argument("--synthetic-higher-env", action="store_true", help="synthetic data in SIT/UAT/performance")
    ap.add_argument("--weak-subset", action="store_true")
    ap.add_argument("--virtual-unmasked-source", action="store_true")
    ap.add_argument("--manual-inspect", action="store_true", help="manual PII validation")
    ap.add_argument("--data-lists", action="store_true", help="test data spreadsheets/lists")
    ap.add_argument("--hero", action="store_true", help="the hero / selective automation")
    ap.add_argument("--full-db-copy", action="store_true", help="full copy without subsetting")
    ap.add_argument("--no-reporting", action="store_true")
    # positive practices
    ap.add_argument("--masked", action="store_true", help="masking applied")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--subsetting", action="store_true")
    ap.add_argument("--virtualization", action="store_true")
    ap.add_argument("--auto-validation", action="store_true")
    ap.add_argument("--auto-profiling", action="store_true")
    ap.add_argument("--data-views", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    flags = {
        "raw_prod": a.raw_prod, "prod_exemption_routine": a.exemption_routine, "mask_everything": a.mask_everything,
        "mask_inconsistent": a.mask_inconsistent, "encryption_breaks_format": a.encryption_breaks_format,
        "manual_profiling": a.manual_profiling, "late_reqs": a.late_reqs, "synthetic_in_higher_env": a.synthetic_higher_env,
        "weak_subset": a.weak_subset, "virtual_unmasked_source": a.virtual_unmasked_source, "manual_inspect": a.manual_inspect,
        "data_lists": a.data_lists, "hero_or_selective_automation": a.hero, "full_db_copy": a.full_db_copy,
        "no_reporting": a.no_reporting, "masked": a.masked, "synthetic": a.synthetic, "subsetting": a.subsetting,
        "virtualization": a.virtualization, "auto_validation": a.auto_validation, "auto_profiling": a.auto_profiling,
        "data_views": a.data_views,
    }
    res = audit(flags)
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
    print("=== TDM checklist (Refcard patterns and anti-patterns) ===")
    print("Result: %s (heuristic score %d/100)" % (res["verdict"], res["score_heuristic"]))
    if not res["findings"]:
        print("No item flagged; absence of a flag = not reported.")
    for f in res["findings"]:
        print("  [%-8s] %s (%s) %s: %s" % (f["status"], f["rule"], f["citation"], f["label"], f["desc"]))
    print("Notice: %s" % res["disclaimer"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

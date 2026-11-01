# -*- coding: utf-8 -*-
"""
Skill: api-error-formatter
Generates or reviews an error body inspired by the example in *Web API Design: The Missing Link*
(Apigee/Google, 2018), APIGEE p.52-53. Standard library only, no network, read-only.

What is [from source]: verbose, plain-language messages with hints and a link to more
information; the example has developerMessage, userMessage, errorCode and a link spelled
"more info" (with a space) (APIGEE p.52-53); standard HTTP status with its headers (APIGEE p.51-52).
What is NOT from the source: a mandatory schema, a "details" field, "status" in the body, the rule
"never 200 with an error", stack traces. Warnings about these are emitted as [extrapolation].

Usage:
  python -I api_error_formatter.py --demo
  python -I api_error_formatter.py --validate error.json [--status 200]
"""

import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EXAMPLE_FIELDS = ["developerMessage", "userMessage", "errorCode"]
LINK_KEYS = ["moreInfo", "more info", "more_info"]


def review(data, http_status=None):
    notes = []
    for f in EXAMPLE_FIELDS:
        if f not in data:
            notes.append(f"[suggestion] The book's example has '{f}' (APIGEE p.53); it is not mandatory, but it helps.")
    link = next((k for k in LINK_KEYS if k in data), None)
    if not link:
        notes.append("[from source] A link to more information is recommended (APIGEE p.53).")
    elif link == "more info":
        notes.append("[inference] 'more info' (with a space) is the spelling in the example (APIGEE p.53), but the source "
                     "advises against names incompatible with identifiers (APIGEE p.47); 'moreInfo' is an adaptation.")
    dev = str(data.get("developerMessage", ""))
    if dev and len(dev.split()) < 6:
        notes.append("[from source] Messages should be verbose, in plain language, with hints on how to fix the problem (APIGEE p.52, p.53).")
    low = json.dumps(data, ensure_ascii=False).lower()
    if any(t in low for t in ["traceback", "nullpointerexception", "sqlstate", "at com.", "stack"]):
        notes.append("[extrapolation] There seems to be a stack trace or database error in the body; the source does not "
                     "cover this, but exposing internals is a known risk.")
    if http_status == 200:
        notes.append("[from source] Use the appropriate standard HTTP status and its headers (APIGEE p.51, p.52). "
                     "[extrapolation] An error with 200 goes against HTTP; the book does not state this rule explicitly.")
    return notes


def main():
    ap = argparse.ArgumentParser(description="Error body inspired by the Apigee 2018 example (p.53)")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--validate", help="JSON file with the error body")
    ap.add_argument("--status", type=int, help="HTTP status of the response, if known")
    args = ap.parse_args()
    if args.validate:
        with open(args.validate, encoding="utf-8") as fh:
            data = json.load(fh)
        notes = review(data, args.status)
        print("\n".join(notes) if notes else "Nothing to flag with the known rules (this is not approval).")
        return
    demo = {
        "developerMessage": "The field 'name' is required when creating a dog at /dogs; send it in the JSON body. "
                            "See the link for the full format.",
        "userMessage": "Enter the dog's name.",
        "errorCode": 12345,
        "moreInfo": "https://dev.example.com/errors/12345",
    }
    print("Example based on APIGEE p.53 (example fields, not a mandatory schema; the book spells it 'more info'):")
    print(json.dumps(demo, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

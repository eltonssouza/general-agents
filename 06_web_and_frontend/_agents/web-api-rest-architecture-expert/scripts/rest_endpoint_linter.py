# -*- coding: utf-8 -*-
"""
Skill: rest-endpoint-linter
Static triage of API URLs according to *Web API Design: The Missing Link* (Apigee/Google, 2018).
Standard library only, no network, read-only.

Rules and source:
  verb in the path ......... [from source] APIGEE p.26 (nouns), p.11-12 (function style)
  filter in the path ....... [from source] APIGEE p.36-37 (filters in the query string)
  long hierarchy ........... [from source] APIGEE p.28 (bad in a link URL; acceptable in a query URL)
  version in the path ...... [from source] APIGEE p.56-59 (informational: not versioning is an option; with links, a header is simpler)
  creation POST ............ [from source] APIGEE p.7, p.51 (201 + Location)

The book does NOT require pluralizing nor limit nesting levels; this linter does not flag singular names.
"No findings" is not approval: it only means the patterns the linter knows are absent.

Usage:
  python -I rest_endpoint_linter.py "/dogs?color=red" [--method POST] [--link]
  python -I rest_endpoint_linter.py --demo
In Git Bash, an argument that starts with "/" becomes a Windows path; use
MSYS_NO_PATHCONV=1, run in PowerShell, or omit the leading slash ("dogs/1").
"""

import argparse
import re
import sys
from urllib.parse import urlparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VERB_PREFIX = re.compile(
    r"^(get|read|fetch|find|retrieve|create|add|new|insert|make|update|modify|edit|"
    r"save|set|delete|remove|destroy|search|query|filter|list|do|verify|check|"
    r"calculate|convert|translate|feed|replace|give)(?=[A-Z_\-]|$)"
)
VERB_EXACT = {"start", "stop", "pause", "resume", "cancel", "approve", "feed", "convert",
              "calculate", "translate"}
FILTER_KEYS = {"color", "status", "type", "state", "category", "location"}
ID_RE = re.compile(r"^(\d+|[0-9a-fA-F\-]{8,}|[A-Za-z0-9]{6,}=*)$")


def lint_endpoint(method, uri, is_link=False):
    method = method.upper().strip()
    findings = []
    if re.match(r"^[A-Za-z]:/", uri) and "Git" in uri:
        findings.append(("WARNING", "The argument seems to have been converted by Git Bash into a Windows path. "
                         "Use MSYS_NO_PATHCONV=1, PowerShell, or omit the leading slash."))
        return {"method": method, "uri": uri, "findings": findings}

    parsed = urlparse(uri if "://" in uri else "/" + uri.lstrip("/"))
    segments = [s for s in parsed.path.split("/") if s]
    core = segments[1:] if segments and re.match(r"^v\d+$", segments[0], re.I) else segments

    if core is not segments:
        findings.append(("INFO", f"Version in the path ('{segments[0]}'). The book considers not versioning a smart "
                         "option and, with links in the representation, a version header simpler "
                         "[from source] (APIGEE p.56, p.57, p.59)."))

    for seg in core:
        name = seg.split(";")[0]
        if name.lower() == "search" or (ID_RE.match(name) and not VERB_PREFIX.match(name)):
            continue
        if VERB_PREFIX.match(name) or name.lower() in VERB_EXACT:
            findings.append(("HIGH", f"Verb in segment '{seg}'. In URLs, use nouns; the function style "
                             "(/getAllDogs, /newDog) forces learning details without a pattern "
                             "[from source] (APIGEE p.11, p.12, p.26). Actions: state or request entity "
                             "(APIGEE p.53, p.54); calculations: the result resource (APIGEE p.37)."))

    if core and core[0].lower() == "search":
        findings.append(("INFO", "Generic search URL ('/search?type=...'). The book treats it as equivalent to the path "
                         "style, but prefers '/persons/{id}/dogs': more readable, easier to implement, does not suggest "
                         "support for every combination and expresses graph traversal [from source] (APIGEE p.19, p.33)."))

    if len(core) >= 3 and core[-2].lower() in FILTER_KEYS:
        findings.append(("MEDIUM", f"Filter in the path ('/{core[-2]}/{core[-1]}'). Filters traditionally go in the "
                         f"query string: '/{core[0]}?{core[-2]}={core[-1]}' [from source] (APIGEE p.36, p.37)."))

    if len(core) > 4:
        msg = (f"Path with {len(core)} segments. In a query URL, navigating relations is acceptable "
               "(APIGEE p.28, p.33, p.34); in a link/permalink URL, hierarchy is a bad idea because it changes and breaks "
               "links — prefer '/{type}/{uuid}' [from source] (APIGEE p.28).")
        findings.append(("HIGH" if is_link else "INFO", msg))

    if method == "POST" and not any(f[0] == "HIGH" for f in findings):
        findings.append(("REMINDER", "If the POST creates a resource, respond 201 Created with Location "
                         "[from source] (APIGEE p.7, p.51)."))

    return {"method": method, "uri": uri, "findings": findings}


def print_report(res):
    print("=" * 70)
    print(f"{res['method']} {res['uri']}")
    print("-" * 70)
    if not res["findings"]:
        print("No known pattern found. This is NOT approval: review representations, "
              "status/headers and links manually (references/procedimentos.md).")
    for sev, msg in res["findings"]:
        print(f"[{sev}] {msg}")


def main():
    ap = argparse.ArgumentParser(description="Triage of API URLs (Apigee, The Missing Link, 2018)")
    ap.add_argument("uri", nargs="?", default="")
    ap.add_argument("--method", default="GET")
    ap.add_argument("--link", action="store_true", help="the URL will be used as a stored link/permalink")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo or not args.uri:
        for m, u, link in [("POST", "createDog", False), ("GET", "getRedDogsWithoutSiblings", False),
                           ("GET", "dogs/color/red", False),
                           ("GET", "companies/1/departments/2/employees/3", True),
                           ("GET", "persons/5678/dogs?color=red", False),
                           ("POST", "processes/123456/requests", False)]:
            print_report(lint_endpoint(m, u, link))
        return
    print_report(lint_endpoint(args.method, args.uri, args.link))


if __name__ == "__main__":
    main()

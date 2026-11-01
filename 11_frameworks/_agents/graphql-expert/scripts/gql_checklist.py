#!/usr/bin/env python3
"""gql_checklist.py - checklist of the concepts/lessons that the GQL capture (graphql.org/learn) NAMES.

It is not a GraphQL best-practices checklist (the source does not detail them). It is a study map:
each item is a concept or lesson named in the PDF, with its page, and a pattern to detect whether
a user text (notes, README, study plan) already mentions it.

Usage (python -I, stdlib, no network; the file is read as text, never executed):
  gql_checklist.py list [--json]
  gql_checklist.py check FILE [--json]   -> covered / not mentioned in the user text
'check' output: always exit 0 when the file is read; 2 if it does not exist.
"""
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass
import unicodedata

# (id, section, label, page(s), regex over accent-free normalized text; Portuguese + English alternates)
CONCEPTS = [
    ("L1", "Learn", "Introduction: flexible, versionless APIs, strong types", "1-2", r"versionless|sem versao|sem versionamento|sistema de tipos|strong type|type system"),
    ("L2", "Learn", "Schemas and Types: the schema language defines the shape of the data", "1", r"schema language|linguagem de schema|\bsdl\b|schemas? and types|schemas? e tipos"),
    ("L3", "Learn", "Queries: ask for exactly the data (fields)", "2", r"\bqueries\b|\bquery\b|consulta"),
    ("L3a", "Learn", "Queries: variables", "2", r"variables?|variaveis|variavel"),
    ("L3b", "Learn", "Queries: fragments", "2", r"fragments?|fragmentos?"),
    ("L4", "Learn", "Mutations: update and remove records", "2", r"mutations?|mutacao|mutacoes"),
    ("B2", "Best Practices", "Thinking in Graphs: from REST endpoints to graphs", "2", r"thinking in graphs|think in graphs|graph-based thinking|pensar em grafos|pensamento em grafos|modelar como grafo"),
    ("B3", "Best Practices", "Serving over HTTP: methods, headers, status, endpoint", "2", r"serving over http|sobre http|over http"),
    ("B4", "Best Practices", "File Uploads as mutations", "2-3", r"file uploads?|upload"),
    ("G1", "Schema Governance", "Ownership models: centralized", "3", r"centraliz"),
    ("G1a", "Schema Governance", "Ownership models: federated", "3", r"federated|federad|federation|federacao"),
    ("G1b", "Schema Governance", "Ownership models: hybrid", "3", r"hybrid|hibrid"),
    ("G2", "Schema Governance", "Governance tooling", "3", r"governance tooling|ferramental de governanca|ferramentas de governanca"),
    ("G3", "Schema Governance", "Schema review (review and automated validation)", "3", r"schema review|revisao de schema|validacao automatizada|automated validation"),
    ("G4", "Schema Governance", "Schema change management and versioning", "3", r"change management|gestao de mudanca|gerenciamento de mudanca|versionamento de schema|schema versioning"),
    ("T1", "Tutorials", "GraphQL-JS tutorial", "4", r"graphql[- .]?js"),
    ("T2", "Tutorials", "Apollo Odyssey", "4", r"odyssey|apollo"),
    ("T3", "Tutorials", "Yoga GraphQL Server Tutorial", "4", r"\byoga\b"),
    ("T4", "Tutorials", "Hasura tutorials", "4", r"hasura"),
    ("F1", "FAQ", "FAQ: categories (Getting started, General, Best practices, Specification, Frontend, Foundation)", "4-5", r"\bfaq\b"),
    ("R1", "Resources/Community", "Resources and Community", "5", r"\bcommunity\b|comunidade|\bresources\b|recursos"),
]


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def cmd_list(as_json):
    rows = [{"id": i, "section": s, "concept": r, "pages": p} for i, s, r, p, _ in CONCEPTS]
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print("Concepts/lessons NAMED by the GQL capture (the PDF does not explain them; it only names/describes them in 1-2 lines):")
        for r in rows:
            print(f"  [{r['id']:3}] GQL p.{r['pages']:4} ({r['section']}) {r['concept']}")
    return 0


def cmd_check(path, as_json):
    if not os.path.isfile(path):
        print("file not found:", path)
        return 2
    with open(path, encoding="utf-8", errors="replace") as f:
        text = norm(f.read())
    covered, missing = [], []
    for i, s, r, p, rx in CONCEPTS:
        (covered if re.search(rx, text) else missing).append({"id": i, "section": s, "concept": r, "pages": p})
    if as_json:
        print(json.dumps({"mentioned": covered, "not_mentioned": missing,
                          "note": "only detects a keyword mention; does not evaluate correctness. Content beyond what the PDF names is [extrapolation]."},
                         ensure_ascii=False, indent=2))
    else:
        print(f"Mentioned in the text ({len(covered)}/{len(CONCEPTS)}):")
        for c in covered:
            print(f"  [x] {c['id']:3} {c['concept']} (GQL p.{c['pages']})")
        print(f"Not mentioned ({len(missing)}):")
        for c in missing:
            print(f"  [ ] {c['id']:3} {c['concept']} (GQL p.{c['pages']})")
        print("Note: keyword detection, correctness not evaluated; the PDF only names these items.")
    return 0


def main(argv):
    as_json = "--json" in argv
    a = [x for x in argv if x != "--json"]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if a[0] == "list":
        return cmd_list(as_json)
    if a[0] == "check" and len(a) >= 2:
        return cmd_check(a[1], as_json)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

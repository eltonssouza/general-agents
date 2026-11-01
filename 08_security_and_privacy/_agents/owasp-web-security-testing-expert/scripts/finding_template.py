# -*- coding: utf-8 -*-
"""
finding_template.py - finding template and report skeleton following chapter 5 (Reporting) of OWASP WSTG 4.2.

Only generates text / validates fields of local files. No network. The guide says the format is a suggestion, not a rule (WSTG p.440).

Usage:
  python -I scripts/finding_template.py finding [--id WSTG-SESS-03] [--format md|json]
  python -I scripts/finding_template.py report-skeleton
  python -I scripts/finding_template.py check finding.json        # validates fields and flags unmasked sensitive data
  python -I scripts/finding_template.py severities

Fields of each finding [from source] (WSTG p.441-442): reference ID; title; likelihood/exploitability (ease,
working exploit code, access level, attacker motivation); impact; risk; description (with sensitive data
masked); remediation; additional resources. Suggested scale: Informational, Low, Medium, High, Critical (p.441);
the values used must be explained in an appendix (p.441); CVSS if required (p.442).
Extra package fields [inference]: id_wstg, test_technique, root_cause, evidence, retest_status (guide 4.2 also asks for, on
p.35-36: category by type, threat, root cause, test technique, remediation, severity).
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SEVERITIES = ["Informational", "Low", "Medium", "High", "Critical"]
REQUIRED = ["ref_id", "title", "likelihood", "impact", "risk", "description", "remediation"]
OPTIONAL = ["id_wstg", "category", "threat", "root_cause", "test_technique", "evidence", "references", "cvss", "retest_status"]

# "senha" / "[mascarado]" are kept so findings written in Portuguese are still checked.
SENSITIVE_PATTERNS = [
    (r"(?i)\b(password|senha|passwd|pwd)\b\s*[:=]\s*(?!\*{3}|<masked>|\[masked\]|\[mascarado\])\S+", "possible unmasked password"),
    (r"\b(?:\d[ -]?){13,19}\b", "long numeric sequence (possible card/document number)"),
    (r"(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*(?!\*{3}|<masked>|\[masked\]|\[mascarado\])[A-Za-z0-9_\-]{12,}", "possible unmasked secret/token"),
    (r"\b[A-Fa-f0-9]{32,}\b", "long hexadecimal (possible hash/key)"),
]


def finding_template(wstg_id):
    return {
        "ref_id": "F-001",
        "title": "<vulnerability title>",
        "id_wstg": wstg_id or "<WSTG-XXXX-NN>",
        "category": "<vulnerability type>",
        "threat": "<security threat it is exposed to>",
        "root_cause": "<bug/flaw/configuration>",
        "test_technique": "<technique used to find it>",
        "likelihood": "<Informational|Low|Medium|High|Critical> - ease, exploit code, required access, motivation",
        "impact": "<Informational|Low|Medium|High|Critical> - impact on the system",
        "risk": "<Informational|Low|Medium|High|Critical> - risk to the application",
        "cvss": "<optional: vector and score, if required>",
        "description": "<what it is, how to reproduce (steps), possible damage; mask passwords, personal data and cards>",
        "evidence": "<clean captures/outputs, not tool dumps>",
        "remediation": "<detailed steps, improvements and missing practices>",
        "references": ["<image, video, CVE, external guide>"],
        "retest_status": "<open|fixed|not reproduced>",
    }


def to_md(d):
    L = [f"## {d['ref_id']} - {d['title']}", ""]
    for k in ["id_wstg", "category", "threat", "root_cause", "test_technique", "likelihood", "impact", "risk", "cvss"]:
        L.append(f"- **{k}**: {d[k]}")
    for k in ["description", "evidence", "remediation"]:
        L += ["", f"### {k}", str(d[k])]
    L += ["", "### references"] + [f"- {r}" for r in d["references"]]
    L += ["", f"- **retest_status**: {d['retest_status']}"]
    return "\n".join(L) + "\n"


SKELETON = """# Security test report (skeleton following WSTG 4.2, ch.5, p.440-442)

> The guide treats the format as a suggestion; adapt it to the audience. Protect and encrypt the report (p.440).

## 1. Introduction
### 1.1 Version control (version | description | date | author)
### 1.2 Table of contents
### 1.3 The team (specialties and qualifications)
### 1.4 Scope (limits and needs agreed with the organization)
### 1.5 Limitations (areas out of bounds, broken functionality, lack of cooperation, time, access or credentials)
### 1.6 Schedule
### 1.7 Disclaimer (point-in-time assessment; legal text must come from a legal professional)

## 2. Executive summary
Test objective; business need; how the tests helped understand the systems; key findings in business context;
strategic recommendations without technical details; no jargon or negative speculation.

## 3. Findings
### 3.1 Findings summary (Ref. ID | Title | Risk level)
### 3.2 Finding details (use `finding_template.py finding`)
(In a retest: summarize previous findings and status.)

## Appendices
- Methodology used
- Explanation of the severity and risk levels (the scale used must be explained)
- Relevant tool output (clean)
- Checklist of the tests performed (e.g., WSTG checklist)
"""


def check(path):
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    items = d if isinstance(d, list) else [d]
    bad = 0
    for it in items:
        rid = it.get("ref_id", "?")
        miss = [k for k in REQUIRED if not str(it.get(k, "")).strip() or str(it.get(k)).startswith("<")]
        for k in miss:
            print(f"[{rid}] MISSING/PLACEHOLDER: {k}")
            bad += 1
        for k in ("likelihood", "impact", "risk"):
            v = str(it.get(k, ""))
            if v and not v.startswith("<") and not any(v.startswith(s) for s in SEVERITIES):
                print(f"[{rid}] WARNING {k}: value '{v[:30]}' outside the suggested scale {SEVERITIES} (explain the scale in an appendix, p.441)")
        blob = " ".join(str(it.get(k, "")) for k in ("description", "evidence", "remediation"))
        for pat, msg in SENSITIVE_PATTERNS:
            if re.search(pat, blob):
                print(f"[{rid}] SENSITIVE: {msg} (the guide asks to mask sensitive data, p.442)")
                bad += 1
    print("OK" if not bad else f"{bad} pending item(s)")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    f = sub.add_parser("finding")
    f.add_argument("--id")
    f.add_argument("--format", default="md", choices=["md", "json"])
    sub.add_parser("report-skeleton")
    sub.add_parser("severities")
    c = sub.add_parser("check")
    c.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "finding":
        t = finding_template(a.id)
        print(json.dumps(t, ensure_ascii=False, indent=2) if a.format == "json" else to_md(t), end="")
        return 0
    if a.cmd == "report-skeleton":
        print(SKELETON, end="")
        return 0
    if a.cmd == "severities":
        print("Scale suggested by the guide (WSTG p.441): " + ", ".join(SEVERITIES))
        print("Explain the values in an appendix. CVSS (FIRST) is the most widely used metric (p.35), required in some engagements (p.442).")
        return 0
    if a.cmd == "check":
        return check(a.path)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

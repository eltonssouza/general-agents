---
name: audit-report-totals
description: "Use when assembling the audit report (\"how many confirmed vulnerabilities?\", \"coverage matrix\", gate G4): computes by script the totals by severity, priority and domain counting only CONFIRMED, lists POTENTIAL, REQUIRES_VALIDATION and DISCARDED in separate tables, measures coverage with denominators and blocks if there is a CONFIRMED without independent review. Do not use to validate findings (audit-evidence-validator)."
---

# Report totals and matrices (gate G4)

## Procedure
1. Run the script (it reads JSON and files as data; never executes anything from the audited repository; no network):
   ```bash
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/audit_summary.py validated-findings.json --results result-*.json
   ```
   (`${CLAUDE_PLUGIN_ROOT}` = package root, substituted by Claude Code in the plugin; on other platforms, use the package folder, `../../` from this skill.)
2. Exit 0: passed (warnings may exist; read them). Exit 1: failed/blocked; the output lists each problem with the JSON path. Exit 2: usage or read error.
3. Do not work around the result: a reported problem goes back to whoever produced the data, or the item stays `NOT_VERIFIED`/`REQUIRES_VALIDATION`.

## Limits
Contracts in `${CLAUDE_PLUGIN_ROOT}/contracts/`. The script checks form, invariants and the existence of the evidence; judgment (exploitation, impact, legal applicability) remains with the agent.

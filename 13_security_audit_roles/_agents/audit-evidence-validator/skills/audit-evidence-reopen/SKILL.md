---
name: audit-evidence-reopen
description: "Use when validating audit candidates (\"reopen the evidence\", \"confirm these findings\", gate G3): reopens each piece of evidence in the snapshot with a script - file exists without escaping the snapshot, lines exist, file_sha256 matches, excerpt appears in the cited lines, no clear-text secret, equal revision - and checks validated-findings.json (CONFIRMED only with independent review and existing checked_evidence_refs). Do not use to discover new findings."
---

# Deterministic reopening of the evidence

## Procedure
1. Run the script (it reads JSON and files as data; never executes anything from the audited repository; no network):
   ```bash
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/audit_contracts.py candidates.json --repo <snapshot> --revision <revision>
   ```
   (`${CLAUDE_PLUGIN_ROOT}` = package root, substituted by Claude Code in the plugin; on other platforms, use the package folder, `../../` from this skill.)
2. Exit 0: passed (warnings may exist; read them). Exit 1: failed/blocked; the output lists each problem with the JSON path. Exit 2: usage or read error.
3. Do not work around the result: a reported problem goes back to whoever produced the data, or the item stays `NOT_VERIFIED`/`REQUIRES_VALIDATION`.

## Limits
Contracts in `${CLAUDE_PLUGIN_ROOT}/contracts/`. The script checks form, invariants and the existence of the evidence; judgment (exploitation, impact, legal applicability) remains with the agent.

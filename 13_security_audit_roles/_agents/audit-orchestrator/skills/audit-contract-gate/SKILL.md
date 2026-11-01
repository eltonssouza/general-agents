---
name: audit-contract-gate
description: Use when receiving an auditor's result or the audit manifest ("validate this agent-result", "is the result in the contract?", gate G2): validates the JSON against the Universal Audit Multiagent contracts (finding, agent-result, audit-run) and checks the invariants the schema does not cover - cited lines exist in the snapshot, line_end >= line_start, revision equal to the run's, CONFIRMED with independent review, no clear-text secret in the excerpt. Do not use to decide a finding's verdict (audit-evidence-validator).
---

# Gate G2: contracts and invariants

## Procedure
1. Run the script (it reads JSON and files as data; never executes anything from the audited repository; no network):
   ```bash
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/audit_contracts.py result-security.json --repo <snapshot> --revision <revision>
   ```
   (`${CLAUDE_PLUGIN_ROOT}` = package root, substituted by Claude Code in the plugin; on other platforms, use the package folder, `../../` from this skill.)
2. Exit 0: passed (warnings may exist; read them). Exit 1: failed/blocked; the output lists each problem with the JSON path. Exit 2: usage or read error.
3. Do not work around the result: a reported problem goes back to whoever produced the data, or the item stays `NOT_VERIFIED`/`REQUIRES_VALIDATION`.

## Limits
Contracts in `${CLAUDE_PLUGIN_ROOT}/contracts/`. The script checks form, invariants and the existence of the evidence; judgment (exploitation, impact, legal applicability) remains with the agent.

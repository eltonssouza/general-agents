# INDEX: audit-report-generator

## Nature
**Role** agent of the audit pipeline (folder `13_security_audit_roles`; the general orchestrator's catalog marks it `kind: role`). It does not cite book pages: it works with evidence from the audited snapshot and with the states `CONFIRMED`, `POTENTIAL`, `REQUIRES_VALIDATION`, `DISCARDED`, `CONTROL_VERIFIED`, `NOT_APPLICABLE`, `NOT_VERIFIED`. Origin: `agents-skills/universal-audit-multiagent` v3.0.

## Files
| File | Use |
|---|---|
| `../contracts/*.schema.json` | JSON Schema 2020-12 contracts (identical in the 9 packages; test CTR) |
| `quality-gates.md` | copy of `docs/quality-gates.md` from the origin |
| `../templates/report-outline.md` | copy of `templates/report-outline.md` from the origin |
| `../templates/issue.md` | copy of `templates/issue.md` from the origin |
| `../scripts/audit_summary.py` | deterministic gate (skill `audit-report-totals`) |

## Boundaries with the collection (citable grounding)
| Topic | Specialist |
|---|---|
| Issue writing and execution prioritization | `tech-lead` |
The specialists do **not** produce `agent-result` or audit verdicts; this role does not replace their citable source.

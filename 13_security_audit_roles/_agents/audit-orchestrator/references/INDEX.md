# INDEX: audit-orchestrator

## Nature
**Role** agent of the audit pipeline (folder `13_security_audit_roles`; the general orchestrator's catalog marks it `kind: role`). It does not cite book pages: it works with evidence from the audited snapshot and with the states `CONFIRMED`, `POTENTIAL`, `REQUIRES_VALIDATION`, `DISCARDED`, `CONTROL_VERIFIED`, `NOT_APPLICABLE`, `NOT_VERIFIED`. Origin: `agents-skills/universal-audit-multiagent` v3.0.

## Files
| File | Use |
|---|---|
| `../contracts/*.schema.json` | JSON Schema 2020-12 contracts (identical in the 9 packages; test CTR) |
| `execution-flow.md` | copy of `docs/execution-flow.md` from the origin |
| `quality-gates.md` | copy of `docs/quality-gates.md` from the origin |
| `testing-plan.md` | copy of `docs/testing-plan.md` from the origin |
| `../templates/audit-config.example.yaml` | copy of `templates/audit-config.example.yaml` from the origin |
| `routing.yaml` | routing of the 20 domains; roles point to the collection's agents |
| `../scripts/audit_contracts.py` | deterministic gate (skill `audit-contract-gate`) |

## Boundaries with the collection (citable grounding)
| Topic | Specialist |
|---|---|
| Conceptual question about any domain | general-agents-orchestrator (routes to the specialist) |
The specialists do **not** produce `agent-result` or audit verdicts; this role does not replace their citable source.

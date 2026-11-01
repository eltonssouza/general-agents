# INDEX: audit-security-auditor

## Nature
**Role** agent of the audit pipeline (folder `13_security_audit_roles`; the general orchestrator's catalog marks it `kind: role`). It does not cite book pages: it works with evidence from the audited snapshot and with the states `CONFIRMED`, `POTENTIAL`, `REQUIRES_VALIDATION`, `DISCARDED`, `CONTROL_VERIFIED`, `NOT_APPLICABLE`, `NOT_VERIFIED`. Origin: `agents-skills/universal-audit-multiagent` v3.0.

## Files
| File | Use |
|---|---|
| `../contracts/*.schema.json` | JSON Schema 2020-12 contracts (identical in the 9 packages; test CTR) |

## Boundaries with the collection (citable grounding)
| Topic | Specialist |
|---|---|
| ASVS requirements and secure code review with page | `owasp-asvs-code-review-expert` |
| Authorized penetration testing (WSTG) | `owasp-web-security-testing-expert` |
| Threat modeling and strategy | `infosec-strategy-threat-modeling-expert` |
The specialists do **not** produce `agent-result` or audit verdicts; this role does not replace their citable source.

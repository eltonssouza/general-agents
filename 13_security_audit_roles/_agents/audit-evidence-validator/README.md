# Independent Evidence Validator (`audit-evidence-validator`)

Role of the **Universal Audit Multiagent v3.0** inside the `general-agents` collection (folder `13_security_audit_roles`). Independent evidence validator of the audit pipeline (Universal Audit Multiagent v3.0): the gate between the auditors' candidates and the report. Reopens each piece of evidence in the snapshot (path, lines, revision, hash) with audit_contracts.py, redoes the origin-validation-privilege-destination flow, deduplicates by root cause and decides CONFIRMED, POTENTIAL, REQUIRES_VALIDATION or DISCARDED, writing validated-findings.json and validation-log.md. Use after the auditors, always in a context separate from whoever found the candidate. Do not use to discover new findings or to write the report.

**Origin.** `agents-skills/universal-audit-multiagent` v3.0 (shared policy + `prompts/08-evidence-validator.md`), packaged in the collection's standard layout on 2026-11-01: the shared policy comes **before** the role in the prompt (as in the original `build_prompts.py`), paths via `${CLAUDE_PLUGIN_ROOT}`, roles named after the collection's agents. The role and policy text was preserved (English version).

**Central rule of the audit:** the specialist finds, the independent validator decides, the generator communicates. No role approves what it found itself.

## Files
- contracts/ (finding, agent-result, audit-run)
- references/INDEX.md, quality-gates
- scripts/audit_contracts.py; skills/audit-evidence-reopen
- agents/audit-evidence-validator.md (Claude Code, canonical); AGENTS.md (Codex) and .github/agents/audit-evidence-validator.agent.md (Copilot), generated from the canonical one.
- tests/: run_script_tests.py, casos-de-teste.md, relatorio-de-validacao.md.

## Installation
**Check each platform's current documentation.** The pipeline needs the 9 roles installed (the `audit-orchestrator` dispatches the others).
- **Claude Code:** `claude --plugin-dir /path/to/audit-evidence-validator` (repeat for all 9) or, through the collection's marketplace, `/plugin marketplace add /path/to/general-agents` and then `/plugin install audit-evidence-validator@general-agents`. Tools: `Read, Grep, Glob, Bash, Write`.
- **Codex:** copy the folder and reference `AGENTS.md`; `<PKG>` is the package folder.
- **GitHub Copilot:** copy `.github/agents/audit-evidence-validator.agent.md` to `.github/agents/` and the package folder (adjust `<PKG>`).

## Script
```bash
python -I scripts/audit_contracts.py candidates.json --repo <snapshot> --revision <revision>
python -I tests/run_script_tests.py
```

## Limits
It is not a runtime or a scanner: it depends on the harness for context isolation and read-only tools. An audit does not guarantee the absence of vulnerabilities or malware and is not a legal opinion. Codex and Copilot were not run in this environment; see `tests/relatorio-de-validacao.md`.

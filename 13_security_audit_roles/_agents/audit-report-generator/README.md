# Audit Report Generator (`audit-report-generator`)

Role of the **Universal Audit Multiagent v3.0** inside the `general-agents` collection (folder `13_security_audit_roles`). Audit report generator of the pipeline (Universal Audit Multiagent v3.0): consolidates only already validated data into a Markdown/PDF report, findings.json, coverage and compliance matrices and issue drafts, with totals computed by script (audit_summary.py: only CONFIRMED counts as a vulnerability). Use only after the audit-evidence-validator, or to assemble a clearly labeled partial report. It does not invent, does not raise severity, does not confirm candidates, does not publish issues remotely and does not alter the audited code.

**Origin.** `agents-skills/universal-audit-multiagent` v3.0 (shared policy + `prompts/09-report-generator.md`), packaged in the collection's standard layout on 2026-11-01: the shared policy comes **before** the role in the prompt (as in the original `build_prompts.py`), paths via `${CLAUDE_PLUGIN_ROOT}`, roles named after the collection's agents. The role and policy text was preserved (English version).

**Central rule of the audit:** the specialist finds, the independent validator decides, the generator communicates. No role approves what it found itself.

## Files
- contracts/ (finding, agent-result, audit-run)
- references/INDEX.md, quality-gates
- scripts/audit_summary.py; skills/audit-report-totals
- templates/report-outline.md, issue.md
- agents/audit-report-generator.md (Claude Code, canonical); AGENTS.md (Codex) and .github/agents/audit-report-generator.agent.md (Copilot), generated from the canonical one.
- tests/: run_script_tests.py, casos-de-teste.md, relatorio-de-validacao.md.

## Installation
**Check each platform's current documentation.** The pipeline needs the 9 roles installed (the `audit-orchestrator` dispatches the others).
- **Claude Code:** `claude --plugin-dir /path/to/audit-report-generator` (repeat for all 9) or, through the collection's marketplace, `/plugin marketplace add /path/to/general-agents` and then `/plugin install audit-report-generator@general-agents`. Tools: `Read, Grep, Glob, Bash, Write`.
- **Codex:** copy the folder and reference `AGENTS.md`; `<PKG>` is the package folder.
- **GitHub Copilot:** copy `.github/agents/audit-report-generator.agent.md` to `.github/agents/` and the package folder (adjust `<PKG>`).

## Script
```bash
python -I scripts/audit_summary.py validated-findings.json --results result-*.json
python -I tests/run_script_tests.py
```

## Limits
It is not a runtime or a scanner: it depends on the harness for context isolation and read-only tools. An audit does not guarantee the absence of vulnerabilities or malware and is not a legal opinion. Codex and Copilot were not run in this environment; see `tests/relatorio-de-validacao.md`.

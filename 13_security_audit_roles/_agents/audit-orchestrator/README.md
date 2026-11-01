# Audit Orchestrator (`audit-orchestrator`)

Role of the **Universal Audit Multiagent v3.0** inside the `general-agents` collection (folder `13_security_audit_roles`). Universal software security audit orchestrator (Universal Audit Multiagent v3.0). Use proactively when asked to "audit this repository", "run a full security audit", "look for vulnerabilities, backdoors, LGPD issues, supply chain, infrastructure or AI problems in this project". Runs the preflight (scope, authorization, read-only), inventory, threat model and tasks across the 20 domains; dispatches the specialized auditors; requires output in the agent-result contract; runs gate G2 (audit_contracts.py); sends the candidates to the audit-evidence-validator in an independent context and only then to the audit-report-generator. Do not use for conceptual questions about OWASP, LGPD or SRE (collection specialists), for pentesting or for fixing code.

**Origin.** `agents-skills/universal-audit-multiagent` v3.0 (shared policy + `prompts/01-orchestrator.md`), packaged in the collection's standard layout on 2026-11-01: the shared policy comes **before** the role in the prompt (as in the original `build_prompts.py`), paths via `${CLAUDE_PLUGIN_ROOT}`, roles named after the collection's agents. The role and policy text was preserved (English version).

**Central rule of the audit:** the specialist finds, the independent validator decides, the generator communicates. No role approves what it found itself.

## Files
- contracts/ (finding, agent-result, audit-run)
- references/INDEX.md, routing.yaml, execution-flow, quality-gates, testing-plan
- scripts/audit_contracts.py; skills/audit-contract-gate
- templates/audit-config.example.yaml
- agents/audit-orchestrator.md (Claude Code, canonical); AGENTS.md (Codex) and .github/agents/audit-orchestrator.agent.md (Copilot), generated from the canonical one.
- tests/: run_script_tests.py, casos-de-teste.md, relatorio-de-validacao.md.

## Installation
**Check each platform's current documentation.** The pipeline needs the 9 roles installed (the `audit-orchestrator` dispatches the others).
- **Claude Code:** `claude --plugin-dir /path/to/audit-orchestrator` (repeat for all 9) or, through the collection's marketplace, `/plugin marketplace add /path/to/general-agents` and then `/plugin install audit-orchestrator@general-agents`. Tools: `Agent, Read, Grep, Glob, Bash, Write`.
- **Codex:** copy the folder and reference `AGENTS.md`; `<PKG>` is the package folder.
- **GitHub Copilot:** copy `.github/agents/audit-orchestrator.agent.md` to `.github/agents/` and the package folder (adjust `<PKG>`).

## Script
```bash
python -I scripts/audit_contracts.py result-security.json --repo <snapshot> --revision <revision>
python -I tests/run_script_tests.py
```

## Limits
It is not a runtime or a scanner: it depends on the harness for context isolation and read-only tools. An audit does not guarantee the absence of vulnerabilities or malware and is not a legal opinion. Codex and Copilot were not run in this environment; see `tests/relatorio-de-validacao.md`.

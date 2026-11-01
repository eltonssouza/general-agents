# Security Auditor (`audit-security-auditor`)

Role of the **Universal Audit Multiagent v3.0** inside the `general-agents` collection (folder `13_security_audit_roles`). Application security auditor of the audit pipeline (Universal Audit Multiagent v3.0): architecture and trust boundaries, authentication and session, authorization/IDOR/BOLA/BFLA and tenant isolation, injections, XSS/CSRF/CORS, data and storage, APIs and webhooks, uploads and parsers, business logic, mobile/desktop/games/IoT. Use when the audit-orchestrator dispatches a security task, or to raise application vulnerability candidates in the agent-result contract. Read-only; delivers candidates, never a verdict (the audit-evidence-validator decides). Do not use for conceptual ASVS questions (owasp-asvs-code-review-expert) or for penetration testing (owasp-web-security-testing-expert).

**Origin.** `agents-skills/universal-audit-multiagent` v3.0 (shared policy + `prompts/02-security-auditor.md`), packaged in the collection's standard layout on 2026-11-01: the shared policy comes **before** the role in the prompt (as in the original `build_prompts.py`), paths via `${CLAUDE_PLUGIN_ROOT}`, roles named after the collection's agents. The role and policy text was preserved (English version).

**Central rule of the audit:** the specialist finds, the independent validator decides, the generator communicates. No role approves what it found itself.

## Files
- contracts/ (finding, agent-result, audit-run)
- references/INDEX.md
- agents/audit-security-auditor.md (Claude Code, canonical); AGENTS.md (Codex) and .github/agents/audit-security-auditor.agent.md (Copilot), generated from the canonical one.
- tests/: run_script_tests.py, casos-de-teste.md, relatorio-de-validacao.md.

## Installation
**Check each platform's current documentation.** The pipeline needs the 9 roles installed (the `audit-orchestrator` dispatches the others).
- **Claude Code:** `claude --plugin-dir /path/to/audit-security-auditor` (repeat for all 9) or, through the collection's marketplace, `/plugin marketplace add /path/to/general-agents` and then `/plugin install audit-security-auditor@general-agents`. Tools: `Read, Grep, Glob`.
- **Codex:** copy the folder and reference `AGENTS.md`; `<PKG>` is the package folder.
- **GitHub Copilot:** copy `.github/agents/audit-security-auditor.agent.md` to `.github/agents/` and the package folder (adjust `<PKG>`).

## Limits
It is not a runtime or a scanner: it depends on the harness for context isolation and read-only tools. An audit does not guarantee the absence of vulnerabilities or malware and is not a legal opinion. Codex and Copilot were not run in this environment; see `tests/relatorio-de-validacao.md`.

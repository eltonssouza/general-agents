# general-agents-orchestrator

**Orchestrator** agent for the specialist agents of the `general-agents` collection (folders `01_*` to `11_*`) and for the role agents of the `*_roles` folders: `12_*` (product owner, product designer, tech lead, principal engineer; `[practice]` label) and `13_*` (the security audit pipeline of the Universal Audit Multiagent, entered through the `audit-orchestrator`). It is not a specialist in any domain. It **routes** each subtask to the right specialist (by a deterministic script over a catalog generated from the real frontmatters), **decomposes** multi-domain requests, **delegates** with self-contained briefs, **integrates** preserving the source labels (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`, `NOT COVERED`) and **validates** before declaring done.

It applies, to itself and to every delegation, four constraints: do not complicate simple tasks, do not assume when clarity is missing, do not modify beyond the scope and do not declare done without checking.

It replies in the language the user writes in (default: English). Routing works for English and Portuguese requests: the catalog descriptions are English, and `scripts/vocab_pt.json` maps common Portuguese terms to their English equivalents.

## Structure
```
general-agents-orchestrator/
├── .claude-plugin/plugin.json
├── agents/general-agents-orchestrator.md                 # canonical prompt (Claude Code)
├── AGENTS.md                                             # Codex adapter
├── .github/agents/general-agents-orchestrator.agent.md   # GitHub Copilot adapter
├── references/  INDEX, catalogo (generated), fronteiras, protocolo, plataformas
├── skills/      orq-route, orq-catalog
├── scripts/     route.py, build_catalog.py, apply_models.py, models.json, vocab_pt.json, catalog.json (generated)   (stdlib, no network)
└── tests/       run_script_tests.py, casos-de-teste.md, relatorio-de-validacao.md
```
Copy of the tests in `../../_agents_tests/general-agents-orchestrator/`.

## Prerequisite
The orchestrator **delegates**: the specialists must be installed on the same platform. Without them, it delivers the delegation plan (subtask → agent → brief) but does not execute it.

## Installation
Formats change between versions; check `references/plataformas.md` (checked on 2026-10-31) and the current documentation.

- **Claude Code:** load the orchestrator and the specialists as plugins, for example
  `claude --plugin-dir <ROOT>/00_orchestration/_agents/general-agents-orchestrator --plugin-dir <ROOT>/05_databases/_agents/relational-dbms-internals-expert ...`
  - Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`, with all the plugins of the collection): `/plugin marketplace add /path/to/general-agents` and then `/plugin install general-agents-orchestrator@general-agents` (repeat `/plugin install <specialist>@general-agents` for each specialist you want to use).
  - As the main session (recommended for orchestrating): `claude --agent general-agents-orchestrator`, or `"agent": "general-agents-orchestrator"` in `.claude/settings.json`.
  - As a subagent: `@agent-general-agents-orchestrator:general-agents-orchestrator ...` (delegates by nesting, up to the depth limit).
- **OpenAI Codex:** copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root and keep the collection accessible at `<ROOT>`. `AGENTS.md` requests delegation to subagents, which read each specialist's `AGENTS.md`.
- **GitHub Copilot:** copy `.github/agents/general-agents-orchestrator.agent.md` (and the specialists' `.agent.md` files) to `.github/agents/` of the target repository; adjust `<PKG>`/`<ROOT>`. It uses the `agent` tool with `agents: ['*']`.

## Scripts (from the package root)
```bash
python -I scripts/route.py "how do I do PITR in PostgreSQL?"   # candidates; exit 1 = NO SPECIALIST
python -I scripts/route.py "como faço PITR no PostgreSQL?"     # the same request in Portuguese
python -I scripts/route.py --show spring-boot-reference-expert  # scope, exclusions, path
python -I scripts/route.py --list --domain 08
python -I scripts/build_catalog.py --check                   # catalog up to date with the disk?
python -I scripts/build_catalog.py                           # regenerate after creating/removing agents
python -I scripts/apply_models.py --check                    # do all packages follow the model policy?
python -I tests/run_script_tests.py                          # automated tests (English and Portuguese routing)
```

## Usage (examples)
- "My FastAPI API with PostgreSQL is slow on `/orders`; review the endpoint and the query." → REST + PostgreSQL in parallel, then FastAPI; integrates and runs the tests.
- "Which agent covers LGPD?" → answers with the script, without delegating.
- "How do I integrate TypeScript with Kotlin?" → NO SPECIALIST (the collection does not cover it).
- "Write the checkout stories with PIX and the execution plan, covering security" → requirements with `owasp-asvs-code-review-expert` (specialist, with page) → stories with `product-owner` → plan with `tech-lead` (roles, `[practice]`); payments/PIX itself is NO SPECIALIST.

## Agent models
A single policy in `scripts/models.json`, with the models allowed by the relay-harness, tiered by price within each provider:

| Tier | Claude Code | Codex / OpenAI | GitHub Copilot (preference) | Who uses it by default |
|---|---|---|---|---|
| `fast` | `haiku` | `gpt-6-luna` | `claude-haiku-5.5`, `gpt-6-luna` | nobody (available) |
| `balanced` | `sonnet` | `gpt-6.1-sol` | `claude-sonnet-5.5`, `gpt-6.1-sol` | specialists and roles |
| `strong` | `opus` | `gpt-5.6-terra` | `claude-opus-5.5`, `gpt-5.6-terra` | orchestrator, `principal-engineer` |
| `frontier` | `opus` | `gpt-6-astra` | `claude-opus-5.5`, `gpt-6-astra` | nobody (available) |

`python -I scripts/apply_models.py` writes the model into each package (`model` frontmatter in Claude Code and Copilot; a block in the Codex `AGENTS.md`); `--check` reports divergence; to change one agent, edit `exceptions` in `models.json` and run it again.

## Specialist manifests
The `plugin.json` files of all the specialists and of this package pass `claude plugin validate` (checked on 2026-10-31 with 61 packages and on 2026-11-01 with 62, after `clean-code-expert` joined), once `author` (string → object), `skills` in an invalid format and the unknown field `entrypoint` had been fixed. All declare `"license": "MIT"` (text in `LICENSE` at the collection root) and have `.claude-plugin/icon.png` (512 px, one per domain). If a specialist is not installed, the orchestrator still uses the fallback: a generic subagent that reads the package's canonical prompt. Details in `tests/relatorio-de-validacao.md`.

## Limitations
- `route.py` is lexical triage: the final choice is confirmed with `--show` and `references/fronteiras.md`. The Portuguese layer is a small hand-written alias table (`scripts/vocab_pt.json`), not a translator: a Portuguese term missing from it is matched literally and may not find an English description.
- The quality of the answers is that of the specialists and their sources; the orchestrator adds no domain knowledge.
- The automated tests cover routing, catalog and adapters; end-to-end execution was checked in Claude Code (see `tests/relatorio-de-validacao.md`). Codex and Copilot were not run in this environment.

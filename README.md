# general-agents

A collection of **specialist agents** for software engineering, packaged as plugins for **Claude Code**, with adapters for **OpenAI Codex** and **GitHub Copilot**.

- **61 specialists** (folders `01` to `11`), each distilled from reference books, specifications and official documentation, with citations traceable by page.
- **4 role agents** (folder `12`): product owner, product designer, tech lead and principal engineer.
- **9 roles of a security audit pipeline** (folder `13`), the Universal Audit Multiagent v3.0.
- **1 orchestrator** (folder `00`) that routes requests to the right specialist.

## Repository layout

```
general-agents/
├── .claude-plugin/marketplace.json     # Claude Code marketplace listing every plugin
├── 00_orchestration/                   # general-agents-orchestrator
├── 01_programming_languages/           # C#, Go, Java, JavaScript, PHP, Python, Ruby, Rust
├── 02_algorithms_and_data_structures/  # algorithms, data structures
├── 03_design_and_architecture/         # clean architecture/DDD, design patterns, foundations, system design
├── 04_engineering_and_practices/       # CI/CD, clean code, engineering craftsmanship, testing/QA
├── 05_databases/                       # relational internals, NoSQL, graph (Neo4j), warehouse/streaming
├── 06_web_and_frontend/                # modern CSS, accessibility, REST, web performance
├── 07_devops_sre_operations/           # Docker/Kubernetes, Git, DORA, SRE, observability, serverless, Linux, OS
├── 08_security_and_privacy/            # threat modeling, OWASP ASVS/WSTG, LGPD privacy, security engineering
├── 09_ai_and_llm/                      # prompting, agentic AI, deep learning, ML engineering, statistical learning
├── 10_automation_and_integration/      # n8n / Hermes automation agents
├── 11_frameworks/                      # Angular, GraphQL, Next.js, Vue/Nuxt, Svelte/Astro, Spring Boot, Rails, ...
├── 12_product_and_leadership_roles/    # product-owner, product-designer, tech-lead, principal-engineer
├── 13_security_audit_roles/            # audit-orchestrator and the 8 auditing roles
└── LICENSE
```

Every category folder has the same shape:

```
NN_category/
├── _agents/<agent-name>/          # the installable package
└── _agents_tests/<agent-name>/    # copy of the agent's tests and fixtures (folders 13 has only _agents)
```

## Anatomy of an agent package

Each agent under `_agents/` is a self-contained plugin:

```
<agent-name>/
├── .claude-plugin/plugin.json      # Claude Code plugin manifest
├── agents/<agent-name>.md          # Claude Code: system prompt + frontmatter (canonical)
├── AGENTS.md                       # Codex adapter
├── .github/agents/<agent-name>.agent.md   # GitHub Copilot adapter
├── skills/                         # task procedures (SKILL.md), some with helper scripts
├── references/                     # distilled syntheses with an INDEX.md page map
├── scripts/                        # read-only lookup/checklist utilities (Python stdlib, no network)
├── tests/                          # test cases, fidelity reports, citation and script checks
└── README.md                       # package documentation
```

## Conventions

- **Cited claims carry a label:** `[from source]` (the cited page says so), `[inference]`, `[extrapolation]` (knowledge outside the sources) and `[DATED]` (superseded by a newer source). When a topic is not in the sources, the agent answers `NOT COVERED`.
- **Role agents** (folder `12`) have no bibliographic source; their guidance is labeled `[practice]` and they hand off to specialists when a topic has a citable foundation.
- **Language:** agents reply in the language the user writes in (default: English).
- **Scripts** require Python 3.8+ (standard library only) and are run with `python -I`.
- The packages contain the collection's own syntheses, not the text of the source works; rights belong to their authors.

## Installation

Plugin and agent formats change between versions; check each platform's current documentation and each package's `README.md`.

### Claude Code

Add the collection as a marketplace and install what you need:

```
/plugin marketplace add /path/to/general-agents
/plugin install go-expert@general-agents
/plugin install general-agents-orchestrator@general-agents
```

Or load a single package directly:

```bash
claude --plugin-dir /path/to/general-agents/01_programming_languages/_agents/go-expert
```

### OpenAI Codex

Copy the package folder into your repository (for example `tools/go-expert/`) and copy or reference its `AGENTS.md` at the repository root or in `~/.codex/AGENTS.md`. Skills are not native in Codex: `AGENTS.md` tells it to read `skills/<name>/SKILL.md` as a procedure.

### GitHub Copilot

Copy `.github/agents/<agent-name>.agent.md` to `.github/agents/` of your repository, together with the package folder, and select the agent in Copilot Chat.

## Using the orchestrator

`general-agents-orchestrator` is not a domain specialist. It routes each subtask to the right specialist (with a deterministic script over a catalog built from the real frontmatters), splits multi-domain requests, delegates with self-contained briefs and validates the result. Routing works for English and Portuguese requests.

The specialists must be installed on the same platform; without them it only produces the delegation plan.

```bash
claude --agent general-agents-orchestrator
```

```bash
python -I 00_orchestration/_agents/general-agents-orchestrator/scripts/route.py "how do I do PITR in PostgreSQL?"
```

## Security audit pipeline

Folder `13_security_audit_roles` implements the **Universal Audit Multiagent v3.0**. Start from `audit-orchestrator` and install all 9 roles:

`audit-orchestrator`, `audit-security-auditor`, `audit-infrastructure`, `audit-supply-chain`, `audit-ai-security`, `audit-privacy-compliance`, `audit-malware-analyst`, `audit-evidence-validator`, `audit-report-generator`.

The central rule: the specialist finds, the independent validator decides, the generator communicates. No role approves what it found itself. The audit is read-only and requires explicit scope and authorization.

## Contributing / adding an agent

1. Create `NN_category/_agents/<agent-name>/` following the package anatomy above.
2. Add the plugin entry to `.claude-plugin/marketplace.json` (`name`, `source`, `category`).
3. Keep the tests in `NN_category/_agents_tests/<agent-name>/` in sync.
4. Regenerate the orchestrator catalog so the new agent can be routed to (`scripts/build_catalog.py` in the orchestrator package).

## License

[MIT](LICENSE) © 2026 Elton Souza

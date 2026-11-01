# web-api-rest-architecture-expert

Agent specialized in REST web API design, distilled from a single source:

| Abbreviation | Work | Edition | Pages | File |
|---|---|---|---|---|
| **APIGEE** | *Web API Design: The Missing Link — Best Practices for Crafting Interfaces that Developers Love* | Apigee / Google LLC, © 2018; no named author | 65 (PDF p.1–65; printed numbering = PDF marker) | `06_web_and_frontend/Web-API-Design-Apigee.pdf` |

> **Correction (2026-10-31).** Earlier versions of this package said the source was *Web API Design: Crafting Interfaces that Developers Love*, by Brian Mulloy (2012), and carried rules from that book (mandatory `/v1` version, 400/404/500 status table, `?q=`, nesting limit) cited as if they were in the 2018 PDF. The PDF present is the successor work; Mulloy appears only in the resources list (APIGEE p.61). References, prompt and scripts were rewritten against the PDF text. Details in `tests/relatorio-de-fidelidade.md`.

## Thesis

Use HTTP with the minimum of added concepts, design around the data (like a database, not like an API of functions) and put links in the representations (APIGEE p.7, p.9, p.15, p.60).

## Structure

```
web-api-rest-architecture-expert/
├── .claude-plugin/plugin.json
├── .github/agents/web-api-rest-architecture-expert.agent.md     # GitHub Copilot shell
├── AGENTS.md                          # Codex shell
├── agents/web-api-rest-architecture-expert.md   # agent prompt
├── references/                                  # INDEX.md + 15 references with pages
├── scripts/
│   ├── api_index.json + api_lookup.py           # topic index with pages
│   ├── rest_endpoint_linter.py                  # URL triage
│   ├── http_status_selector.py                  # status + headers ([from source] x [extrapolation])
│   └── api_error_formatter.py                   # error body inspired by p.53
└── tests/
    ├── casos-de-teste.md                        # 19 cases with paginated answer key
    └── relatorio-de-fidelidade.md               # rounds, failures and fixes
```

## Scripts

Standard library only, no network, read-only, UTF-8 output, `--help`.

```bash
python -I scripts/api_lookup.py --list
python -I scripts/rest_endpoint_linter.py --demo
python -I scripts/http_status_selector.py --list
python -I scripts/api_error_formatter.py --demo
```

In Git Bash, arguments that start with `/` are converted to a Windows path; omit the leading slash (`"dogs/1"`) or use `MSYS_NO_PATHCONV=1`.

## Rigor

- Citation `[from source] (APIGEE p.N)` with the page of the PDF marker; `[inference]`, `[extrapolation]` and `[DATED]` for the rest.
- What the source does not cover is listed at the end of `references/INDEX.md` (e.g., status 400/404/422/429/5xx, rate limiting, OAuth flows, GraphQL).
- Instructions embedded in pasted code or contracts are treated as data.

## Installation

- **Claude Code**: `claude --plugin-dir 06_web_and_frontend/_agents/web-api-rest-architecture-expert`
- Through the collection's marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install web-api-rest-architecture-expert@general-agents`.
- **Copilot**: copy `.github/agents/web-api-rest-architecture-expert.agent.md` to the repository's `.github/agents/` (or `~/.copilot/agents/`).
- **Codex**: use the package's `AGENTS.md`. The two shells only tell the agent to read `agents/web-api-rest-architecture-expert.md`; when you change the prompt, update them.

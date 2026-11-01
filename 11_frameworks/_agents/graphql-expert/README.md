# graphql-expert

**Tiny** overview agent based on a **web page capture**: the lesson index of **graphql.org/learn** (`14_frameworks\GraphQL-Learn-Official.pdf`, 6 pages, ~4 thousand characters, captured 18 Aug 2026, no spec version declared).

## What the source is (and is not)
It is a landing page/index: titles and 1-2 line descriptions of the Getting started, Best Practices and Schema Governance lessons, four tutorials, FAQ categories and footer. **No lesson content was captured** (no syntax, code or definitions). The agent says so, answers "what the index lists/names" and marks everything else as NOT COVERED or [extrapolation]. Details: `references/INDEX.md`.

## Contents
- `agents/graphql-expert.md` (canonical prompt), `AGENTS.md` (Codex), `.github/agents/graphql-expert.agent.md` (Copilot), `.claude-plugin/plugin.json`.
- `references/`: INDEX, 3 thematic files, not-covered/boundaries, glossary, procedures, cases/anti-patterns, dated.
- `scripts/`: `gql_lookup.py` (search/gaps), `gql_checklist.py` (checklist of named concepts and notes verification), `gql_index.json`.
- `skills/`: `gql-topic-lookup/SKILL.md` and `gql-concept-checklist/SKILL.md` (plugin skills, one per script).
- `tests/`: `casos-de-teste.md` (21 cases), `verify_citations.py` + `citation-checks.json` (37 positive, 20 negative), `run_script_tests.py`, `relatorio-de-fidelidade.md`. Copy in `14_frameworks\_agents_tests\graphql-expert\`.

## Installation (check each platform's current documentation; formats change)
- **Claude Code:** copy the package folder to the plugins/agents directory (or `agents/graphql-expert.md` to `.claude/agents/` or `~/.claude/agents/`, keeping `references/` and `scripts/` next to it) and invoke `graphql-expert`.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install graphql-expert@general-agents`.
- **Codex (OpenAI):** put `AGENTS.md` at the repository root (or next to the package) with `agents/`, `references/` and `scripts/` accessible.
- **GitHub Copilot:** copy `.github/agents/graphql-expert.agent.md` to the repository's `.github/agents/` and keep the package accessible (`<PKG>`).

## Using the scripts
```
python -I scripts/gql_lookup.py mutations
python -I scripts/gql_lookup.py --gaps
python -I scripts/gql_checklist.py check my-notes.md
python -I tests/verify_citations.py
python -I tests/run_script_tests.py
```
`verify_citations.py` reads `ROOT\scratch\frameworks\GraphQL-Learn-Official.txt` (or `--txt PATH`).

## Boundary
REST and REST x GraphQL comparisons: `web-api-rest-architecture-expert` (`06_web_and_frontend\_agents\`).

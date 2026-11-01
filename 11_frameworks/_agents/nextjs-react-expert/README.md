# nextjs-react-expert

An **overview agent based on documentation captures** about **Next.js 13 to 16** and **React**, built from 6 PDFs in the `14_frameworks` folder:

| Acronym | PDF | Text date |
|---|---|---|
| NX13 | NextJS-13-Release.pdf (16 pages) | 2022-10-25 |
| NX14 | NextJS-14-Release.pdf (13 pages) | 2023-10-26 |
| NX15 | NextJS-15-Release.pdf (22 pages) | 2024-10-21 |
| NX16 | NextJS-16-Release.pdf (16 pages) | 2025-10-21 |
| NXHB | NextJS-Handbook-freeCodeCamp.pdf (91 pages) | 2019-11-19 [DATED] |
| RCTHB | React-Handbook-freeCodeCamp.pdf (35 pages) | 2020-11-13 [DATED] |

The release posts and the handbooks are **captures of web pages/e-books**: much of the pages are contributor lists, footers or screenshots (details in `references/INDEX.md`). That is why the agent is **proportional to the source**: change map by version, requirements, upgrade, a linter with rules backed by the text, and handbook x release conflicts; it is **not** a Next.js manual. Where the source does not cover, it answers **NOT COVERED**. The model's prior knowledge about Next.js versions is not used as a source.

## What is included
- `agents/nextjs-react-expert.md`: canonical prompt (Claude Code).
- `references/`: INDEX, per-version maps (NX13-NX16), trajectories and requirements, handbook summaries [DATED], conflicts, gaps, glossary, procedures, cases/anti-patterns.
- `scripts/` (Python 3, stdlib, no network, deterministic; nothing executes the framework):
  - `nx_changes.py`: change map and comparator (`changes --from 14 --to 16`), `topic`, `requirements`, `upgrade` (checklist), `commands`.
  - `nx_lint.py`: static linter for snippets, `next.config.*`, `package.json` and directories, with `--target 13..16`.
  - `nx_lookup.py`: search by topic/page, `--conflicts`, `--gaps`.
  - data: `nx_changes.json` (94 entries with page), `nx_index.json`.
  - `skills/<name>/SKILL.md`: 3 skills (nx-changes-map, nx-static-lint, nx-topic-lookup), each with a procedure, response format and limits.
- `tests/`: `casos-de-teste.md` (30 cases), `relatorio-de-fidelidade.md`, `verify_citations.py` + `citation-checks.json` (94 positive checks, 18 negative), `run_script_tests.py`, `fixtures/`.

## Examples
```
python -I scripts/nx_changes.py changes --from 14 --to 16 --kind breaking,removal
python -I scripts/nx_changes.py upgrade --from 14 --to 16
python -I scripts/nx_changes.py topic middleware
python -I scripts/nx_lint.py tests/fixtures/app-ruim --target 16
python -I scripts/nx_lookup.py --conflicts
python -I tests/verify_citations.py --src <ROOT>/scratch/frameworks
python -I tests/run_script_tests.py
```

## Installation on the 3 platforms
**Check each platform's current documentation**: the formats change.
- **Claude Code:** copy the package folder (with `.claude-plugin/`, `agents/`, `references/`, `scripts/`) to a local marketplace/plugin or copy `agents/nextjs-react-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user), keeping `references/` and `scripts/` in an accessible path (the prompt cites them relative to the package root).
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install nextjs-react-expert@general-agents`.
- **OpenAI Codex CLI (and agents that read `AGENTS.md`):** copy `AGENTS.md` to the repository root (or merge it with the existing one) and keep the package folder in the repository.
- **GitHub Copilot:** copy `.github/agents/nextjs-react-expert.agent.md` to the repository's `.github/agents/` and the package folder to the root (adjust `<PKG>` if you change the path).

## Limits and warnings
- An overview agent based on doc-capture; it does not replace the official documentation nor the upgrade guide (the posts themselves say to read the *upgrade guide*, which is not in the collection).
- Regex linter (heuristic): it can be wrong; only rules backed by the posts. [DATED] patterns from the handbooks are informational only.
- Tests were run by the author, not by an independent model (see `tests/relatorio-de-fidelidade.md`).
- Code and commands in the sources are data; nothing is executed.

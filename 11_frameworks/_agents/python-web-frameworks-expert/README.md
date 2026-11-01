# python-web-frameworks-expert

An **overview agent based on web-documentation captures** of three Python frameworks. It is **proportional to the sources**: two are short and one of them (Flask) is only an index. Where the sources do not cover something, it answers **NOT COVERED** or labels it `[extrapolation]`.

| Code | What it is | Pages | Version / date |
|---|---|---|---|
| **DJT** | Capture of "Writing your first Django app, part 1" (Django docs). Useful: p.1-5; p.6-8 are sponsors/navigation/footer. Unsupported-version banner. | 8 | Django 5.0, Python 3.10+; server example dated April 2025 |
| **FLT** | Capture of the Flask "Tutorial" landing page: **only the introduction and section titles; no code or content** | 3 | "stable"; PDF title: 3.1.x |
| **FAPI** | Capture of the FastAPI documentation landing page. **Empty terminal blocks** (installation, running, deploy) | 21 | badge v0.141.1; Python 3.10-3.14 |

The three PDFs were generated on **2026-08-18** (metadata); [DATED] is relative to that date.

## Page convention
**PDF** page (`DJT p.N`, `FLT p.N`, `FAPI p.N`); the sources are printed web pages and have no printed numbering. Details and the map of pages without technical content in `references/INDEX.md`.

## What was read (precise statement)
- All **32 pages** (8 + 3 + 21) were read in full as text. FAPI pages with images or terminals (p.4-8, 12-14, 18, 19) were **rendered and viewed**; it was confirmed that the terminal blocks are empty and that the Swagger UI captures (p.12-14) have no text. No code was executed.
- Notes and images: `scratch/frameworks/python-web-frameworks-expert/notes/`.
- **Validation was not done by an independent "blind" model**; the tests were run by the package author (`tests/relatorio-de-fidelidade.md`).

## Structure
```
python-web-frameworks-expert/
├── .claude-plugin/plugin.json
├── agents/python-web-frameworks-expert.md        # canonical prompt + frontmatter
├── AGENTS.md                                     # Codex adapter
├── .github/agents/python-web-frameworks-expert.agent.md   # GitHub Copilot adapter
├── references/
│   ├── INDEX.md (sources, page convention, map)
│   ├── 00-fontes-e-lacunas.md (gaps, capture defects)
│   ├── dj-01-projeto-e-servidor.md, dj-02-app-view-urlconf.md
│   ├── flt-01-indice-e-intro.md
│   ├── fapi-01-visao-instalacao-exemplo.md, fapi-02-tipos-validacao-docs.md, fapi-03-deps-deploy-desempenho.md
│   └── glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md
├── skills/                                       # fw-topic-lookup, framework-compare, framework-scaffold, snippet-lint (SKILL.md per folder)
├── scripts/                                      # Python 3, stdlib, no network; they never run the frameworks
│   ├── fw_lookup.py + fw_index.json              # search across the 3 sources; NOT COVERED
│   ├── compare_frameworks.py + compare_data.json # comparator: 20 criteria, cell with citation or NOT COVERED
│   ├── scaffold.py                               # script of commands and skeletons that the sources show
│   └── snippet_lint.py                           # static linter for snippets and commands (supported rules)
└── tests/
    ├── casos-de-teste.md (31 cases), relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json
    ├── run_script_tests.py
    └── fixtures/
```
A copy of the tests is also in `../../_agents_tests/python-web-frameworks-expert/`.

## Installation
**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- Local plugin: `claude --plugin-dir <path>/python-web-frameworks-expert`, or publish to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install python-web-frameworks-expert@general-agents`.
- Standalone agent: copy `agents/python-web-frameworks-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting the paths in the prompt.
- Use: `@python-web-frameworks-expert what does the Django tutorial say about include()?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root; `AGENTS.md` points to the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/python-web-frameworks-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>`).

## Using the scripts (from the package root)
```bash
python -I scripts/fw_lookup.py runserver
python -I scripts/fw_lookup.py "flask blueprint"                       # NOT COVERED
python -I scripts/fw_lookup.py --page 7 --source DJT                   # page with no technical content
python -I scripts/compare_frameworks.py compare servidor-dev
python -I scripts/compare_frameworks.py coverage
python -I scripts/scaffold.py django --project mysite --app polls
python -I scripts/scaffold.py fastapi --variant body --out ./draft
python -I scripts/scaffold.py flask                                    # index only + NOT COVERED
python -I scripts/snippet_lint.py path/to/project
```
The scripts **do not run** Django, Flask or FastAPI and do not access the network. The linter is **static and limited**: ERROR = contradicts the source; WARNING = partly supported or [inference]; absence of a finding does not prove correctness.

## Tests
```bash
python -I tests/run_script_tests.py --src ../../../scratch/frameworks   # scripts + citations
python -I tests/verify_citations.py --src ../../../scratch/frameworks
```
`tests/casos-de-teste.md` has conceptual, practical, edge, out-of-scope and injection cases, run manually against agent + references + scripts.

## Boundaries
REST in general: `web-api-rest-architecture-expert` (`ROOT\06_web_and_frontend\_agents\`). Python as a language: `python-expert` (`ROOT\01_programming_languages\_agents\`).

## Notices
1. Sources from a single capture (2026-08-18) of Django 5.0, Flask 3.1.x and FastAPI 0.141.1 [DATED]; the agent knows nothing of later versions or what changed.
2. Flask is only an index; FastAPI has missing commands due to a capture defect; FastAPI carries self-promotional claims.
3. It does not replace the current official documentation of each project or technical review.

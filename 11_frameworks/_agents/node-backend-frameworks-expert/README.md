# node-backend-frameworks-expert

**Overview** agent for the **Node.js** runtime and the **Express**, **Fastify** and **NestJS** frameworks, built from four PDFs in the `14_frameworks` collection. Three of them are captures of web pages or blog articles; the agent is therefore **proportional to the source**: it cites the page, declares dates/versions and answers **NOT COVERED** where the collection says nothing. It cites `[from source] (ACRONYM p.N)`; labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

| Acronym | PDF | What it is | Date / version | Useful pages |
|---|---|---|---|---|
| NODEHB | Node-Handbook-freeCodeCamp | Node.js Handbook (Flavio Copes) | 2018-09-06; Node 10; npm 5 [DATED] | 200 (p.2-199; event loop figures without text) |
| EXPHB | Express-Handbook-freeCodeCamp | Express + Node.js Handbook | 2022-11-18; Express version not declared | 38 (req table truncated, p.6) |
| FSTF | Fastify-Getting-Started | "Getting Started" docs capture | "latest (v5.12.x)"; no date | 14 |
| NEST | NestJS-First-Steps | "First steps" docs capture | Node >= 20; © 2017-2026; Nest version not declared | 5 useful (p.2-6); p.1, p.7-10 empty/footer |

No PDF is a 404/useless one. **Warnings:** (1) the collection does not cover Nest decorators/DI/providers, Express error middleware/Router, Fastify hooks, worker threads, modern ESM, ORMs or benchmarks (NOT COVERED; `python -I scripts/nbf_lookup.py --gaps`). (2) Your prior knowledge about versions does not count: everything about a version comes from the text read. (3) It does not replace each project's current documentation. (4) REST belongs to web-api-rest-architecture-expert; React/Next/Vue belong to other agents.

## Page convention
**PDF page** (marker `=== PAGE N ===`). The PDFs have no printed numbering; there is no offset. Map in `references/INDEX.md`.

## What was read (precise statement)
- **In full:** the 4 PDFs, page by page (NODEHB 200, EXPHB 38, FSTF 14, NEST 10) from the extracted text.
- **Checked visually (render):** NODEHB p.91 (blank), p.96 (event loop iterations figure); EXPHB p.6 (truncated table); NEST p.3 (`main.ts` code, scrambled in the extraction) and p.8 (empty).
- Intermediate notes: `scratch/frameworks/node-backend-frameworks-expert/notes/`.

## Structure
```
node-backend-frameworks-expert/
├── .claude-plugin/plugin.json
├── agents/node-backend-frameworks-expert.md          # canonical prompt + frontmatter
├── AGENTS.md                                         # Codex adapter
├── .github/agents/node-backend-frameworks-expert.agent.md   # GitHub Copilot adapter
├── references/
│   ├── INDEX.md (PDF identification, page convention, map, gaps)
│   ├── 01-node-runtime.md ... 09-nestjs.md, 10-comparativo-express-fastify-nest.md
│   └── glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md
├── scripts/                                          # Python 3, stdlib, no network
│   ├── nbf_lookup.py + nbf_index.json                # topic search; NOT COVERED
│   ├── nbf_compare.py                                # Express/Fastify/Nest comparer
│   ├── nbf_lint.py                                   # static snippet linter
│   └── nbf_scaffold.py                               # command plan and skeleton
├── skills/       4 skills (<name>/SKILL.md; procedure using the package scripts)
└── tests/
    ├── casos-de-teste.md, relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json
    ├── run_script_tests.py
    └── fixtures/
```
A copy of the tests is also in `../../_agents_tests/node-backend-frameworks-expert/`.

## Installation
**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- Local plugin: `claude --plugin-dir <path>/node-backend-frameworks-expert`, or publish to your own marketplace.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install node-backend-frameworks-expert@general-agents`.
- Standalone agent: copy `agents/node-backend-frameworks-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting the prompt's paths.
- Usage: `@node-backend-frameworks-expert why does my Express middleware hang the request?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root; `AGENTS.md` points to the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/node-backend-frameworks-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>`).

## Using the scripts (from the package root)
```bash
python -I scripts/nbf_lookup.py "event loop"
python -I scripts/nbf_lookup.py decorator                      # NOT COVERED / partial
python -I scripts/nbf_lookup.py --page 3 --src NEST
python -I scripts/nbf_compare.py --criteria host_porta,validacao --format md   # aliases also work: host_port,validation
python -I scripts/nbf_compare.py --decide                      # the collection does not pick a framework
python -I scripts/nbf_lint.py tests/fixtures/express-ruim.js
python -I scripts/nbf_lint.py --rules
python -I scripts/nbf_scaffold.py express --with json,session,validator,pug
python -I scripts/nbf_scaffold.py fastify --variant plugin --esm --host-all
python -I scripts/nbf_scaffold.py nest --name my-app --strict --swc
python -I tests/run_script_tests.py
python -I tests/verify_citations.py --src <scratch/frameworks folder with the .txt files>
```
`nbf_scaffold.py` prints commands as **text** (it never runs npm/node/nest) and, with `--out DIR`, writes only small example files without overwriting.

## Boundaries and limitations
- **Not covered:** see `INDEX.md` §6 and `--gaps`.
- **Heuristic linter:** rules exist only when supported by the text; each rule's origin label is in `python -I scripts/nbf_lint.py --rules` (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`). No findings does not prove correctness; it is not a security audit.
- **Independent testing:** the cases were run by the package's own author; there was no blind run by an independent model (`tests/relatorio-de-fidelidade.md`).
- Copyright: paraphrased content; no extensive reproduction.

## Security
Code, logs, JSON and the content of the PDFs are inert data (anti prompt injection). The scripts do not use the network, do not run the target code nor the commands cited in the sources.

# agentic-ai-context-engineering-expert

Expert agent in **AI agent architecture and context engineering**, built from two sources (closed collection, both `[DATED]` 2025):

- **BAAS**: *Building Agentic AI Systems: Create intelligent, autonomous AI agents that can reason, plan, and adapt*, Anjanava Biswas and Wrick Talukdar, Packt Publishing, first published April 2025 (ISBN 978-1-80323-875-3); 289 PDF pages, 11 chapters in 3 parts.
- **CE2**: *Context Engineering 2.0: The Context of Context Engineering*, Qishuo Hua et al. (SII-GAIR), arXiv:2510.26493v1 [cs.AI], 10/30/2025; 28 pages (body p.1-21; references p.21-28). Conceptual paper, with no experiments of its own.

The agent specifies and reviews agents (architecture, autonomy, tools, planning, CWD multi-agent, prompts, state, memory, context, action limits, trust, evaluation), reasons about context engineering (formal definition, eras, collection, management, selection, sharing, KV cache), budgets context per component, and cites the page for each rule: `[from source] (BAAS p.N)`, `[from source] (CE2 p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Notice:** the agent **does not replace empirical evaluation of the agent, security review, or legal advice**. The texts provide no agent benchmarks. Frameworks (CrewAI, AutoGen, LangGraph), models, products, and the CE2 numeric heuristics (about 50% window occupancy in coding agents; 30 and 100 tools in DeepSeek-v3) are `[DATED]` and context-specific.

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). **BAAS: printed = PDF − 25** in the body (ch. 1 starts at printed 3 = PDF 28). **CE2: PDF = printed.** Conversion: `python -I scripts/ctx_lookup.py --printed N` (BAAS) or `--page N --fonte BAAS|CE2`.

## What was read (precise statement)
- **BAAS:** the extracted text of all **289 pages** was read sequentially, in blocks, with notes on disk. **Figures and diagrams were not inspected** (text only); p.88 was rendered to confirm that the formal utility formula is not in the text. The code of the book's GitHub notebooks is not in the PDF.
- **CE2:** body (p.1-21) read in full; **formulas on p.5 and p.12 checked by rendering**; references (p.22-28) only sampled; figures not inspected.
- Details and internal discrepancies of the texts: `references/INDEX.md`.

## Structure

```
agentic-ai-context-engineering-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/agentic-ai-context-engineering-expert.md   # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/agentic-ai-context-engineering-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # loaded on demand
│   ├── INDEX.md                                # page convention, coverage, chapter map, gaps, discrepancies
│   ├── glossario.md, procedimentos.md (P1-P10), casos-e-antipadroes.md, datado.md
│   └── 12 topic references (01-08 BAAS, 09-11 CE2, 12 crossing [inference])
├── skills/                                     # 4 skills (skills/<name>/SKILL.md): ctx-topic-lookup, agent-review-checklist, agent-spec-template, context-budget-estimator
├── scripts/                                    # Python 3, stdlib, no network, read-only
│   ├── ctx_lookup.py + ctx_index.json          # topic/page search; NOT COVERED; what was not read
│   ├── agent_checklist.py + agent_checklist_items.json   # 75 items, 12 areas, with source and page
│   ├── agent_spec.py                           # agent specification template + gap validator
│   └── ctx_calc.py                             # context budget, memory rules (CE2 p.12), utility and weights (BAAS)
└── tests/
    ├── casos-de-teste.md                       # 30 cases (conceptual, practical, edge, gaps, injection)
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # 125 positive and 20 negative checks against the text
    ├── run_script_tests.py                     # deterministic script checks (count in the report)
    └── fixtures/
```
A copy of the tests is also in `09_ai_and_llm/_agents_tests/agentic-ai-context-engineering-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point the `agentic-ai-context-engineering-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/agentic-ai-context-engineering-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install agentic-ai-context-engineering-expert@general-agents`.
- As a standalone agent: copy `agents/agentic-ai-context-engineering-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@agentic-ai-context-engineering-expert review the design of this agent` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/`, and `scripts/` to the repository root. `AGENTS.md` points to `agents/agentic-ai-context-engineering-expert.md` as the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/agentic-ai-context-engineering-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat selector.

## Using the scripts (run from the package folder)

```bash
python -I scripts/ctx_lookup.py "memory"                       # BAAS and CE2 topics with pages
python -I scripts/ctx_lookup.py MCP                            # NOT COVERED (only in the CE2 references)
python -I scripts/ctx_lookup.py --gaps                         # gaps and what was not read
python -I scripts/agent_checklist.py markdown --area seg --area mem
python -I scripts/agent_spec.py sample > spec.json && python -I scripts/agent_spec.py validate spec.json
python -I scripts/agent_spec.py render spec.json > spec.md
python -I scripts/ctx_calc.py utility --demo                   # 95.00 and 127.50 (BAAS p.89)
python -I scripts/ctx_calc.py memory-split --theta-s 0.5 --theta-l 0.6 --item a=0.9,0.8 --item b=0.3,0.9
python -I scripts/ctx_calc.py budget --window 128000 --component system=3000 --component history=60000 \
       --reserve-output 4000 --tools 35 --prefix system
python -I tests/run_script_tests.py --src <folder with the extracted .txt files>
python -I tests/verify_citations.py --src <folder with the extracted .txt files>
```
On Windows with Git Bash, use `python -I` as usual; with relative paths, run from the package root. Queries and JSON answers are accepted in English and in Portuguese (for example `sim|nao|parcial|na` as well as `yes|no|partial|na`).

## Boundaries and limitations
- **Not covered** (whole-word search in the text, see `--gaps`): MCP and A2A (MCP only in the CE2 references), RAG in BAAS, prompt injection and the threat model of agents (BAAS mentions "prompt injection" once, p.46), agent benchmarks, named observability, ReAct/Reflexion as techniques, token budgeting and pricing as a method, vendor SDKs, AGENTS.md/CLAUDE.md.
- BAAS **does not use** the terms "context engineering" or "context window". The BAAS preface says ch. 7 covers guardrails, but ch. 7 has no such section (action limits: ch. 9, p.237-240).
- **`ctx_calc.py budget`** is a package construction: the texts provide neither a budgeting method nor prices; the thresholds are `[DATED]` and configurable heuristics; the script **does not tokenize** (tokens are supplied by the user). `memory-split` implements the CE2 p.12 definition, which gives neither weight values nor thresholds. Company and product examples in BAAS (ch. 4 and 10) were not verified.
- **Independent testing:** the cases were run by the package author (see `tests/relatorio-de-fidelidade.md`); **there was no blind run by an independent model**.
- Boundaries with other agents: general security (collection 09), SRE (collection 07), LLM theory and prompt engineering (other PDFs of collection 10).
- Copyright: content distilled in own words, with no extensive reproduction.

## Security
Code, logs, pasted specifications, model outputs, and the PDF are inert data (anti prompt injection). The scripts do not use the network, do not execute user inputs, and do not write files. Defensive focus; no attack payloads against agents.

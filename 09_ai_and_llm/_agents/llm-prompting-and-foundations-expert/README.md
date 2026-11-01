# llm-prompting-and-foundations-expert

Specialist agent in **prompting techniques and LLM foundations**, built from two arXiv surveys:

| Acronym | Work | Edition | Pages |
|---|---|---|---|
| **PES** | *A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications* (Sahoo, Singh, Saha, Jain, Mondal, Chadha) | arXiv:2402.07927v2, **16 Mar 2025** | 12 (body p.1-10) |
| **LLMS** | *A Survey of Large Language Models* (Zhao, Zhou, Li and others; Renmin University) | arXiv:2303.18223v19, **18 Mar 2026** (log up to 27 Feb 2026) | 144 (body p.1-99; p.100-144 = references) |

The agent chooses and explains prompting techniques (zero/few-shot, CoT, Self-Consistency, ToT/GoT, RAG, ReAct, CoVe...), explains foundations (scaling laws, emergence, architecture, data, pre-training, instruction tuning, RLHF/DPO, LoRA, evaluation, agents, long context, inference, quantization, hallucination, long CoT) and cites the page for every rule: `[from source] (PES p.N)` / `(LLMS p.N)`. Labels: `[from source]` (from the survey), `[inference]`, `[extrapolation]`, `[DATED]`.

**[DATED]** The sources are from 2025/2026, with experiments from 2023. The package does not state the current state of the art and does not cover prompt injection, jailbreak, guardrails, MCP, per-token prices, among others (`python -I scripts/llm_lookup.py --gaps`).

## Page convention
Every citation is **PDF page = printed page** (arXiv, 1:1, no offset).

## What was read (precise statement)
- **PES:** p.1-10 in full from extracted text (Table 1, p.10, as linearized text); p.10-12 also contain the references (used only for authors/title).
- **LLMS:** p.1-99 in full from extracted text; tables and figures (Tab. 1 p.8, Fig. 3 p.9, Fig. 6 p.17, Tab. 16 p.67) checked only as linearized text. **p.100-144 = bibliographic references, not used as content.**
- Formulas that became scripts (Eq. 1-3 p.4, Eq. 4-5 p.25, Eq. 10 p.27, Tab. 18-20 p.82-84, quantization p.86) were **rendered and checked visually**.

## Structure

```
llm-prompting-and-foundations-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/llm-prompting-and-foundations-expert.md   # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/llm-prompting-and-foundations-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # on-demand loading
│   ├── INDEX.md                                # page convention, sources, section map, coverage
│   ├── 01-03 (PES) and 04-12 (LLMS)            # thematic references
│   └── glossario.md, procedimentos.md (P1-P11), casos-e-antipadroes.md, datado.md
├── skills/       3 skills (SKILL.md per folder): llm-topic-lookup, prompt-technique-selector, llm-calculators
├── scripts/                                    # Python 3, stdlib, no network, read-only
│   ├── llm_lookup.py + llm_index.json
│   ├── prompt_technique_selector.py + pes_techniques.json (41 techniques) + llms_prompt_tips.json
│   └── llm_calc.py
└── tests/
    ├── casos-de-teste.md                       # 24 cases
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json
    ├── run_script_tests.py
    └── fixtures/
```
A copy of the tests is also in `../../_agents_tests/llm-prompting-and-foundations-expert/` (folder `09_ai_and_llm/_agents_tests/`).

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point to the package directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/llm-prompting-and-foundations-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install llm-prompting-and-foundations-expert@general-agents`.
- As a standalone agent: copy `agents/llm-prompting-and-foundations-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the prompt paths if the agent does not sit next to those folders.
- Usage: `@llm-prompting-and-foundations-expert which prompting technique should I use for math without tools?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root. `AGENTS.md` points to `agents/llm-prompting-and-foundations-expert.md` as the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/llm-prompting-and-foundations-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the root (or adjust the `<PKG>` prefix described in the file). Select the agent in Copilot Chat.

## Using the scripts (run from the package folder)

```bash
python -I scripts/llm_lookup.py chinchilla                  # pages and reference
python -I scripts/llm_lookup.py "prompt injection"          # NOT COVERED
python -I scripts/llm_lookup.py --gaps                      # gaps
python -I scripts/prompt_technique_selector.py --need math hallucination --no-external --brief
python -I scripts/prompt_technique_selector.py --show cot
python -I scripts/prompt_technique_selector.py --tips --principle 3
python -I scripts/llm_calc.py scaling-chinchilla --N 7e9 --D 1.4e12
python -I scripts/llm_calc.py chinchilla-allocation --C 5.76e23
python -I scripts/llm_calc.py train-states --params 6.7e9      # 16P bytes (LLMS p.81)
python -I scripts/llm_calc.py arithmetic-intensity --phase decode
python -I tests/run_script_tests.py --src <scratch/ai folder with the extracted .txt files>
python -I tests/verify_citations.py --src <scratch/ai folder with the extracted .txt files>
```

## Boundaries and limitations
- **Not covered** (whole-word search over the body read): prompt injection, jailbreak, guardrails, MCP, prompt caching, system prompt, structured output/JSON mode, DSPy, KTO, watermarking, prices, GDPR/LGPD, carbon footprint.
- **Selector:** ranking by tag matching `[inference]`; the PES does not rank techniques and the reported percentages are not comparable across techniques.
- **Calculators:** only formulas from the cited pages. The survey does not give the formula for G (Chinchilla); the script derives it (`[extrapolation]`) and flags that the printed definition of a and b appears swapped (`[inference]`). The Tab. 18 sum (~17.3 GiB) does not exactly reproduce the "16GB" in the text.
- **Independent testing:** the cases were run by the package author (see `tests/relatorio-de-fidelidade.md`); there was no blind run by an independent model.
- Copyright: content distilled in own words, with no reproduction of long passages, tables or figures.

## Security
Pasted prompts, logs and the content of the PDFs are inert data (anti prompt injection). The scripts do not use the network, do not execute user input and do not write files.

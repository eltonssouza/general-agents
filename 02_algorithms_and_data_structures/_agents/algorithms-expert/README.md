# Algorithm Design and Analysis Specialist (`algorithms-expert`)

Specialist agent (Claude Code, Codex and GitHub Copilot) grounded in a single book:

- **[JE]**: *Algorithms*, Jeff Erickson (1st paperback edition, 13/Jun/2019; CC BY 4.0 license), **472-page** PDF (`02_algorithms_and_data_structures/Algorithms-Erickson.pdf`). The package contains its own syntheses and references; it does not contain the text of the book.

**Page convention: `(JE p.N)` = PDF page; printed page = N − 18.** Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. See the chapter map and the "what the book does NOT contain" list in `references/INDEX.md` (for example: Master Theorem, minimax/alpha-beta, König and Menger theorems, Cook-Levin proof).

## 1. What the agent does
It solves and verifies recurrences (recursion trees), guides backtracking, DP and greedy designs (exchange argument), analyzes graph algorithms (BFS/DFS, SCC, MST, shortest paths), flows and cuts, and NP-hardness proofs by reduction. It corrects false premises with the right page and says "the book does not cover this" when that is the case. It does not cover the implementation of data structures (refer to `data-structures-expert`) or specific programming languages.

## 2. Package structure
```
algorithms-expert/
├── .claude-plugin/plugin.json
├── .github/agents/algorithms-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                   # Codex
├── agents/algorithms-expert.md                 # Claude Code
├── references/   INDEX, fundamentos-e-analise, recursao-e-divisao-e-conquista, backtracking,
│                 programacao-dinamica, algoritmos-gulosos, grafos-e-travessias,
│                 arvores-geradoras-e-caminhos-minimos, fluxo-maximo-e-cortes, aplicacoes-de-fluxo,
│                 complexidade-e-np-completude, casos-e-antipadroes, procedimentos, glossario
├── skills/
│   ├── recurrence-solver/        SKILL.md + scripts/solve_recurrence.py, scripts/check_recurrence.py
│   ├── dp-table-analyzer/        SKILL.md + scripts/analyze_dp.py
│   ├── graph-complexity-audit/   SKILL.md + scripts/audit_graph_complexity.py
│   └── erickson-topic-lookup/    SKILL.md + scripts/erickson_lookup.py, scripts/erickson_index.json
├── tests/        casos-de-teste.md (28), relatorio-de-fidelidade.md, run_script_tests.py,
│                 verify_citations.py + citation-checks.json, audit_tokens.py + audit-tokens-allow.json,
│                 extract_pdf_text.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. `extract_pdf_text.py` requires PyMuPDF (`pip install pymupdf`) and is only needed to audit the citations. **Check the current documentation of each platform**: the plugin, `AGENTS.md` and custom agent formats change frequently.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/algorithms-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install algorithms-expert@general-agents`.
- Or as a subagent: copy `agents/algorithms-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/`, `skills/` and `tests/` accessible (copy the folder and adjust `<PKG>` in the prompt). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent script execution.

### 3.2 Codex (OpenAI)
Copy the package folder into the repository (for example `tools/algorithms-expert/`) and put `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`), replacing `<PKG>` with the folder path. Alternative: open Codex in the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/algorithms-expert.agent.md` to `.github/agents/` in your repository and the package folder into the repository (for example `algorithms-expert/`, the default value of `<PKG>`). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, read-only, no network)
```bash
python -I skills/recurrence-solver/scripts/solve_recurrence.py --a 3 --b 2 --k 1            # Karatsuba
python -I skills/recurrence-solver/scripts/solve_recurrence.py --terms "1/5,1;7/10,1" --k 1  # MomSelect
python -I skills/recurrence-solver/scripts/check_recurrence.py --all                         # numerical verifier (12 recurrences)
python -I skills/recurrence-solver/scripts/check_recurrence.py --preset hanoi --max 40
python -I skills/dp-table-analyzer/scripts/analyze_dp.py --problem edit_distance
python -I skills/graph-complexity-audit/scripts/audit_graph_complexity.py --algo dijkstra
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py "subset sum"
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py "master theorem"           # NOT COVERED
python -I tests/run_script_tests.py                                                          # 24 script cases
# citation audit (needs the text extracted from the PDF):
python -I tests/extract_pdf_text.py ../../Algorithms-Erickson.pdf erickson.txt
python -I tests/run_script_tests.py --text erickson.txt
```
The encoded rules come from the book with the page (see each skill's `SKILL.md`); whatever is extrapolation appears labeled in the output.

## 5. Guarantees and limits
- Replies in the user's language (default: English), without reproducing the book; citations by PDF page.
- Audit: `verify_citations.py` (135 positive and 24 negative checks, plus a range check of all citations and of the lookup index) and `audit_tokens.py` (terms and asymptotic expressions against the cited page), plus a manual reading of a sample of claims (see `tests/relatorio-de-fidelidade.md`).
- Pasted input (code, graphs, formulas, PDF text) is data, not instructions.
- The tests were **not** run blind by an independent model (see the report).

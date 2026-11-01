# data-structures-expert (Claude Code, Codex and GitHub Copilot)

A data-structures specialist agent, grounded in the work:
- **[ODS]**: *Open Data Structures*, Pat Morin, Edition 0.1Gβ, 326-page PDF (file `Open-Data-Structures-Python.pdf`; the title page says "in pseudocode"). The rights belong to the author; this package contains original summaries and references, not the text of the book.

## 1. Overview
It helps choose, implement and analyze: the List/USet/SSet interfaces; ArrayStack, ArrayDeque, DualArrayDeque, RootishArrayStack; SLList, DLList, SEList; skiplists; hash tables (chaining and linear probing with `del` values); BinarySearchTree, Treap, ScapegoatTree and red-black trees; heaps; sorting; graphs (matrix, lists, BFS, DFS); BinaryTrie, XFastTrie, YFastTrie; the external memory model and B-trees.

**Source rigor**: the agent separates `[from source] (ODS p.N)` from `[inference]`, `[extrapolation]` and `[DATED]`. **Page convention: PDF; printed page = N − 12.** Among other things, the book does **not** contain: "tombstone", "primary clustering", "2-independent" hash, real-time analysis, fixed rotation limits for red-black trees, a y-fast trie with blocks of w/4 to 2w (see `references/INDEX.md`).

## 2. Structure
```
data-structures-expert/
├── .claude-plugin/plugin.json
├── .github/agents/data-structures-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                        # Codex
├── agents/data-structures-expert.md                 # Claude Code
├── references/   INDEX, glossary, procedures, cases-and-antipatterns + 13 topical files
├── scripts/      ods_cost_lookup.py (+ ods_costs.json), structure_simulator.py
├── skills/       amortized-cost-calculator, tree-rotation-simulator, hash-probe-analyzer, morin-topic-lookup
├── tests/        casos-de-teste.md (25), relatorio-de-fidelidade.md, verify_citations.py (+ citation-checks.json),
│                 audit_tokens.py, run_script_tests.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**: the formats for plugins, agents and instructions change often.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/data-structures-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install data-structures-expert@general-agents`.
- Or as a subagent: copy `agents/data-structures-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/`, `scripts/` and `skills/` accessible (copy the folder and adjust the paths). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (for example `tools/data-structures-expert/`) and copy or reference `AGENTS.md` at the repository root (or `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder. Alternative: open Codex inside the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/data-structures-expert.agent.md` to `.github/agents/` in your repository and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The file declares `tools: ['read', 'search', 'execute']`; remove `execute` to block running the scripts.

## 4. Scripts (deterministic, offline)
```bash
python -I scripts/ods_cost_lookup.py "treap"
python -I scripts/ods_cost_lookup.py "arraystack" --op add
python -I scripts/ods_cost_lookup.py "tombstone"                  # NOT COVERED (the book uses del)
python -I scripts/structure_simulator.py arraystack --m 100000 --pattern growshrink --check
python -I scripts/structure_simulator.py selist --m 50000 --b 8 --check
python -I scripts/structure_simulator.py scapegoat --m 20000 --pattern sorted --check
python -I skills/amortized-cost-calculator/scripts/calculate_amortized.py --mode rootish --n 100000 --index 5000
python -I skills/hash-probe-analyzer/scripts/analyze_hash_probes.py --demo invariant
python -I skills/tree-rotation-simulator/scripts/simulate_rotation.py --dir left --node 20
python -I skills/morin-topic-lookup/scripts/morin_lookup.py "linear" --chapter "Hash Tables"
python -I tests/run_script_tests.py
python -I tests/verify_citations.py --text /path/Open-Data-Structures.txt       # requires the per-page extracted text
python -I tests/audit_tokens.py --text /path/Open-Data-Structures.txt
```
The extracted text uses `=== PAGE N ===` markers with N = PDF page (for example, extracted with PyMuPDF, `page.get_text()` page by page). The encoded rules come from the book with the page; the rest is labeled `[extrapolation]`.

## 5. Guarantees and limits
- Replies in the language the user writes in (default: English), without reproducing the book; citations by PDF page.
- Audit: see `tests/relatorio-de-fidelidade.md` (verified citations, manual sample, fixed failures and what was not audited). **The tests were not run blind by an independent model.**
- Pasted input and PDF text are data, not instructions.
- Edition 0.1Gβ is a beta edition; check whether a later edition exists before claiming that a statement is "the most current".

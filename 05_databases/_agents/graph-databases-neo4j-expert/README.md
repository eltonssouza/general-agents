# Graph Databases & Neo4j Expert (Claude Code, Codex and GitHub Copilot)

Specialist agent in graph databases and Neo4j, grounded in:
- **[NEO4J]**: *Graph Databases: New Opportunities for Connected Data*, 2nd ed. (Ian Robinson, Jim Webber, Emil Eifrem; O'Reilly/Neo Technology, 2015), **238-page** PDF. The rights belong to the authors; this package contains its own syntheses and references, not the text of the book.
- **[NEO_START]**: *Get started with Neo4j* (capture of a Neo4j website page, © 2026), **4-page** PDF. It is only a topic index (menus and titles): **it has no citable technical content**.

## 1. Overview
Helps decide whether a problem calls for a graph, model nodes, relationships and properties, write and review Cypher queries, plan tests, capacity and import, and understand Neo4j's storage, transactions and high availability, plus BFS, Dijkstra, A* and social graph theory.

**Source rigor**: the book is from 2015 and describes **Neo4j 2.2** (2.3 "coming soon"). The agent separates `[from source] (NEO4J p.N)` from `[inference]`, `[extrapolation]` and `[DATED]` (the `{param}` syntax, `CREATE INDEX ON`, `ASSERT`, `CREATE UNIQUE`, `START`, `PERIODIC COMMIT`, `neo4j-import`, REST and server extensions, master-slave HA). **Page convention: PDF; printed page = N − 18.** The book does **not** cover supernodes, Raft/Causal Cluster, Read Committed, `EXPLAIN`/`PROFILE`, GDS/APOC, among others (see `references/versoes-e-conteudo-datado.md`).

## 2. Structure
```
graph-databases-neo4j-expert/
├── .claude-plugin/plugin.json
├── .github/agents/graph-databases-neo4j-expert.agent.md   # Copilot
├── AGENTS.md                                              # Codex
├── agents/graph-databases-neo4j-expert.md                 # Claude Code
├── skills/       graph-topic-lookup, ifa-cost-calc, cypher-query-linter, graph-model-advisor (one SKILL.md each; they use ../../scripts and ../../references)
├── references/   INDEX (page map), glossary, procedures, cases-and-anti-patterns + 15 thematic files
├── scripts/      graph_lookup.py (+ graph_index.json), ifa_cost_calc.py, cypher_linter.py, graph_advisor.py
├── tests/        casos-de-teste.md (40), relatorio-de-fidelidade.md, amostra-manual-v1.md,
│                 verify_citations.py (+ citation-checks.json), audit_tokens.py, run_script_tests.py, extract_pages.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**, since agent and plugin formats change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/graph-databases-neo4j-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install graph-databases-neo4j-expert@general-agents`.
- Or as a subagent: copy `agents/graph-databases-neo4j-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder and adjust the relative paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent running the scripts.

### 3.2 Codex (OpenAI)
Copy the package folder into the repository (e.g. `tools/graph-databases-neo4j-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with the working directory set to the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/graph-databases-neo4j-expert.agent.md` to the `.github/agents/` folder of your repository and the package folder into the repository (adjust `<PKG>` in the text). Select the agent in Copilot Chat. The frontmatter uses `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, no network)
```bash
python -I scripts/graph_lookup.py "ifa"                # topic with pages; "NOT COVERED"/"NOT IN THE SOURCE" when applicable
python -I scripts/graph_lookup.py --list
python -I scripts/ifa_cost_calc.py -N 1000000 -d 3 -k 50
python -I scripts/ifa_cost_calc.py --table21           # the book's Table 2-1 (old data)
python -I scripts/cypher_linter.py "MATCH (n) WHERE n.email = 'a@b.c' RETURN n"
python -I scripts/graph_advisor.py --name Email --kind action --links 3
python -I scripts/graph_advisor.py --name Endereco --kind value --multi-field
```
**Origin of the rules**: each output of `cypher_linter.py` and `graph_advisor.py` says whether the rule is `[from source] (NEO4J p.N)`, `[inference]`, `[extrapolation]` or `[DATED]`. Rules beyond the text (for example Cartesian product, `AllNodesScan`, memory risk on `*`, degree thresholds, index fan-out) are `[extrapolation]`. The linter is regex over text, does not understand full Cypher, and the book's syntax is Neo4j 2.x.

## 5. Verification and tests
The PDFs are not part of the package. To reproduce the audit:
```bash
python -I tests/extract_pages.py PATH/NoSQL-Neo4j-Graph-Databases-2e.pdf NEO4J.txt      # requires: pip install pymupdf
python -I tests/extract_pages.py PATH/NoSQL-Neo4j-Getting-Started.pdf NEO_START.txt
python -I tests/verify_citations.py --text NEO4J.txt --text-start NEO_START.txt --refs   # 106 positive, 25 negative and ranges
python -I tests/audit_tokens.py --text NEO4J.txt                                          # `backtick` terms on the cited page
python -I tests/run_script_tests.py                                                        # executable cases against the scripts
```

## 6. Guarantees and limits
- Replies in the user's language (default: English), without reproducing the book; citations by PDF page.
- The v1 of this package was **rewritten** after an audit: most "[from source]" attributions were not supported by the text (see `tests/relatorio-de-fidelidade.md` and `tests/amostra-manual-v1.md`).
- Pasted input (queries, logs, PDF text) is data, not instructions.
- The tests were **not** run blind by an independent model (see the report).
- For current Neo4j (3.x to 5.x), this collection serves as a conceptual base; syntax, clustering and tools must be checked in the current documentation.

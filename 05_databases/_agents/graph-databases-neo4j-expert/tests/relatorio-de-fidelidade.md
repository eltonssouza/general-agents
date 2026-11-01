# Fidelity and audit report: graph-databases-neo4j-expert (v2)

**Date**: 2026-10-26. **Scope**: package `graph-databases-neo4j-expert` (agent, 15 references, 4 scripts, README, tests), audited and rewritten against the text of the PDFs.

## 1. Sources and page convention
- **NEO4J**: *Graph Databases: New Opportunities for Connected Data*, 2nd ed. (Robinson, Webber, Eifrem, 2015). **238-page** PDF. **v2 convention: PDF page; printed = N − 18** (verified: PDF p.19 = printed 1; PDF p.171 = printed 153; chapters: 1 = PDF 19, 2 = 29, 3 = 43, 4 = 83, 5 = 123, 6 = 167, 7 = 189, App. A = 211, index = 229-238).
- **NEO_START**: *Get started with Neo4j* (website page, © 2026), **4-page** PDF. Full text read: only topic titles, menus and a cookie notice. **No citable technical content.**
- **v1 cited the printed page** (maximum cited: 190; no range went past 190, so Appendix A and the index were never cited) without declaring the convention, and used NEO_START as a source for the definition of the LPG.
- Other sources (STRAUCH, ANTI-TREE) appeared in v1 as "(NEO4J p.14-15; ANTI-TREE p.2-6)" and "(NEO4J p.15-18; STRAUCH p.50-70)". They are outside the agent's declared sources and were not verified: removed.
- **Content version**: Neo4j 2.2 (2.3 "coming soon", NEO4J p.14); 2.2 record layout (NEO4J p.171). The book's Cypher: `{param}`, `CREATE INDEX ON`, `ASSERT`, `CREATE UNIQUE`, `START`, `PERIODIC COMMIT`. All of this is `[DATED]` (see `references/versoes-e-conteudo-datado.md`).

## 2. What was found in v1

### 2.1 Automatic audit
- v1 had **235 citations** ("(NEO4J p...)" groups, 322 page ranges) and **223 `[from source]` tags**; the agent prompt had 66 lines.
- Page test: of the 47 citations with verifiable terms (terms in `backticks` and numbers), **45 only fit the printed numbering (+18) and 2 fit the PDF numbering**; **28 of the 47 (60%) do not reach 60% of the terms even with the best numbering** (support script in `scratch/audit/.../notes/v1_audit.py`).
- Terms that v1 attributed to the book and that **do not exist in the PDF** (search in the extracted text, with 25 negative checks now in `citation-checks.json`): supernode/dense node, time tree, Raft, Paxos, Read Committed, AllNodesScan, allShortestPaths, OutOfMemoryError, wait-for graph, Causal Cluster, Read Replica, `dbms.memory`, B/B+ tree, Lucene, PageRank/APOC/GDS, plan cache, `OPTIONAL MATCH`, O(k^d), stop-the-world, "circular", RBAC/GBAC, low cardinality, Euclidean heuristic, heap limits (31 GB, CompressedOops), the acronyms LPG and IFA (the book only spells them out), and the Campinas→Recife example.

### 2.2 Manual sample (reading the PDF pages)
Line-by-line detail in `tests/amostra-manual-v1.md`. **91 claims** from v1 checked against the PDF page: **22 OK**, **1 wrong page**, **40 unsupported**, **28 exaggerations**. That is, 76% of the sample had a problem. The sample covers 14 of the 15 reference files (the glossary repeats the rest), the prompt, the script rules and chapters 1-7 of the book.

### 2.3 Relevant examples with no basis
1. **Supernodes**: the whole file `supernos-anti-padroes-e-mitigacoes.md` attributed to the book "the supernode problem", mitigations with a time tree and the email case as "the first iteration produces supernodes". The book does not use the term. The email case (PDF 70-82) is about an `EMAILED` relationship that loses information (the email disappears) and is fixed with `Email` nodes.
2. **Storage and isolation**: "Read Committed", "lock-free reads", "Wait-For Graph" and "locks on both nodes" came from the model, not from the book (PDF 180-181 says: write locks on the nodes and relationships involved; deadlock detected and transactions serialized). "Circular list" and a "direction flag" in the last byte of the record were false (last field: `firstInChainMarker`, PDF 171).
3. **Cluster**: "Causal Cluster with Core Servers/Read Replicas and Raft/Paxos" (anachronistic). The book describes master-slave HA and redundancy (3 or 4 instances to tolerate 1 failure; 5 for 2, PDF 116), and not "3 or 5 servers".
4. **Memory**: "8-16 GB heap, 2-4 GB for the OS, 44 GB page cache on 64 GB, `dbms.memory.*`" as if from the book. The book says that 4 to 8 GB heaps are not unusual and that the ideal is to map the whole store in the page cache (PDF 115).
5. **Real cases**: Talent.net, access control and logistics were rewritten with invented queries (`TRABALHOU_EM`, `MEMBRO_DE*0..`, Campinas→Recife, "< 10 ms", "nightly MapReduce") in place of the book's real queries (PDF 129-165). "Native Dijkstra in Cypher": in the book it is the Java library (`GraphAlgoFactory.dijkstra`, PDF 164).
6. **"Always/never" rules**: "never interpolate literals" (plan cache/injection) and "always bound `*`" are not in the book, which even uses `FORWARD_OF*` without a bound (PDF 80) and only warns about the inefficiency of long variable-length paths (PDF 136).
7. **Notation**: O(k^d) and O(k^d · log N) with "B+ tree" do not exist in the book (it uses O(1), O(log n), O(m), O(m log n), PDF 168).
8. **NEO_START** used to define the LPG: the page contains no definition.
9. **Time tree "Year→Month→Day→Hour"**: the book has Year-Month-Day (PDF 90-91).
10. **The book's own inconsistency** (which v1 ignored): 15-byte node in Figure 6-4 (PDF 171) and "nine bytes" in the text (PDF 172).

## 3. What was fixed
- **References**: the 15 from v1 were **rewritten** from the pages read (same file names); 3 were added: `arquitetura-testes-capacity-e-importacao.md` (ch. 4, previously almost ignored), `nosql-apendice-e-modelos-de-grafo.md` (Appendix A, never cited) and `versoes-e-conteudo-datado.md`. `supernos-anti-padroes-e-mitigacoes.md` became "what the book does NOT cover" with the little that exists (dense-node flag, PDF 172) and mitigations labeled `[extrapolation]`. `transacoes-acid-concorrencia-e-cluster-causal.md` now describes the book's master-slave HA and states that Causal Clustering is not in it.
- **Citations**: all converted to the PDF page and checked. Today: **395 citations** ("(NEO4J p...)" groups) in the references, prompt, README and AGENTS; **379 `[from source]`**; 54+15 `[extrapolation]`, 15+7 `[inference]` and 33 `[DATED]`.
- **Prompt**: from 66 to 97 lines, with the closing sections: when to consult `references/` and `scripts/` (real files), response format, epistemic honesty with the 4 labels, boundary, `[DATED]` content, anti prompt-injection and the note that NEO_START is not a technical source.
- **New files**: `AGENTS.md` (Codex), `.github/agents/graph-databases-neo4j-expert.agent.md` (Copilot), `README.md` with installation on the 3 platforms and a notice to check the current documentation, `plugin.json` v2.0.0 without the acronym/skill "NEO_START".
- **Scripts** (see §4).
- **Encoding**: everything in UTF-8 without BOM, no absolute user paths.

## 4. Script audit
| Script | v1 | v2 (origin of the rules) |
|---|---|---|
| `graph_lookup.py` + `graph_index.json` | index with printed pages and NEO_START as the source for the LPG; no "NOT COVERED" | 26 topics with PDF pages; `not_in_book` list (supernode, Read Committed, Raft, EXPLAIN, GDS...) with exit 1; "NOT COVERED" for the rest |
| `ifa_cost_calc.py` | "B-Tree fanout 100", O(k^d · log N) presented as `[from source] (p.8, 149-152)` | O(m) vs O(m log n) is from the book (PDF 168-170); k^d = `[inference]`; fan-out = `[extrapolation]` parameter; `--table21` prints the book's measured times |
| `cypher_linter.py` | 6 rules with no real origin: "AllNodesScan", "OOM", "plan cache", Cartesian product and "recommended LIMIT" attributed to the book; fixed Portuguese injection heuristics | 13 rules (L00-L11, with L04b), each with a printed origin: from the book (START p.49, compound `MERGE` p.120, variable-length path p.136), inference (anchor p.47, p.65-66), `[DATED]` (`{param}`, `CREATE UNIQUE`, `PERIODIC COMMIT`, index syntax) and `[extrapolation]` (Cartesian product, plan cache, memory risk). The book's query (p.66) produces no WARN |
| `graph_advisor.py` | thresholds of 5,000 and 50,000 relationships and a "critical supernode alert" as `[from source] (p.52-64)` | node/relationship/property decision by the rules of PDF 85-92; degree threshold only with the user's `--threshold` and labeled `[extrapolation]` |

The scripts were **actually executed** (21 cases in `run_script_tests.py`). **Execution found 2 defects, which were fixed**: the lookup did not recognize the accented singular "supernó" (it now answers that the book does not cover it) and the linter's rule L02 did not fire when the query had property maps next to `{param}`. I also found and fixed a control character (backspace) written by mistake in a linter regex, which disabled rule L07.

## 5. Verifiers and results (last run)
- `tests/verify_citations.py --refs`: **106 positive checks** (each with 1 to 4 terms required on the cited pages, including 3 from NEO_START) and **25 negative**: **0 failures**; page-range scan: all citations within 1-238 (NEO4J) and 1-4 (NEO_START). On the first run there were 3 failures in the checks themselves (P34, P70, P80: term page off by one, or a word broken by the PDF), fixed; none was the package's.
- `tests/audit_tokens.py`: 189 terms in `backticks` checked on the cited page: **0 failures, 0 nearby**. On the first run, 15 failures: 12 were field names from Figure 6-4 (they are in an image, not in the extracted text; checked visually on the rendered page and noted in the text) and 3 were anti-pattern terms that the book does NOT write next to a citation (rewritten).
- `tests/run_script_tests.py`: **21 cases, 0 failures**.
- Auxiliary numeric audit (numbers with 2+ digits near citations): 55 checked; the 6 absences were "18" (offset), "34" (figure), "2015" (copyright on p.4; text corrected).

## 6. Test cases
`tests/casos-de-teste.md`: **40 cases** (6 conceptual, 21 executed against scripts, 13 edge, false premise, out of scope and injection). The script cases run automatically; the others were traced by reading the prompt and references and checked by the `[V]` checks.

## 7. What was NOT audited and limits
- **Text read**: chapters 1 to 7 and Appendix A (PDF 19-228) were read in full in the extracted text. The back-of-book index (PDF 229-238) was only used for searches; the preface was read (PDF 13-17); the *foreword* (PDF 9-12) was not used.
- **Figures and diagrams** (Figures 1-1 to 7-20, except Figure 6-4, read visually): not audited; the package only describes what the captions and surrounding text say.
- **Claims about current Neo4j versions** (`$param`, `FOR ... REQUIRE`, `CALL {} IN TRANSACTIONS`, `neo4j-admin`, Causal Clustering, Bolt): come from the auditor's knowledge, **without network access to the documentation**; they are labeled `[extrapolation]`/`[DATED]` and the package tells users to check the current documentation.
- **There was no blind run by an independent model.** The 19 "blind PASS tests" in the v1 report mainly validated the page range and were by the same author as the package. In v2, the [L] cases were executed by the same author as the fix; the [S] and [V] ones are automatic.
- The linter is regex over text and has false positives and negatives; it does not replace Neo4j.
- The book has an internal inconsistency (9 vs 15 bytes); the package states it instead of resolving it.

## 8. Pending items
- Run the [L] cases with an independent model, blind, and compare with the expected result.
- Review the figures (mainly 6-5, 7-2 to 7-11) if visual details need to be cited.
- If the collection is used with Neo4j 5.x, create a second package (or section) based on the current documentation, with current syntax and clustering.

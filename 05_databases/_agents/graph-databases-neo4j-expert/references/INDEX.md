# Reference INDEX: graph-databases-neo4j-expert

Sources:
- **NEO4J**: *Graph Databases: New Opportunities for Connected Data*, 2nd ed., Ian Robinson, Jim Webber and Emil Eifrem (O'Reilly/Neo Technology, 2015). PDF of **238 pages**. Authors' copyright; this package contains its own syntheses, not the text of the book.
- **NEO_START**: *Get started with Neo4j* (page capture from the Neo4j website, © 2026), PDF of **4 pages**. It is only a topic index (links, menus, cookie notice): **there is no citable technical content**. Permitted uses: stating that the site lists certain topics (NEO_START p.1-2) and that the capture is dated (© 2026, NEO_START p.4).

## Page convention (mandatory)
- **Every citation `(NEO4J p.N)` uses the PDF page** (the same `=== PAGE N ===` markers of the extracted text). **Printed page = N − 18.** Verified: PDF p.19 is printed 1 (start of ch. 1); PDF p.171 carries printed 153 (Figure 6-4); PDF p.172 carries 154. PDF pages 1-18 are cover, credits, table of contents, preface (roman numerals).
- The package's v1 cited the **printed page** (for example, "NEO4J p.152-157" for storage, which is at PDF 170-175); v2 converted everything to PDF. If someone cites "p.152" for storage, it is the printed numbering: add 18.
- When answering, say "NEO4J p.N (PDF; printed N − 18)" at least once.

## Chapter map (PDF → printed)
| Ch. | Title | PDF | Printed |
|---|---|---|---|
| Front | Foreword, Preface (2nd ed.: Neo4j 2.2) | 9-17 | ix-xiii |
| 1 | Introduction (graph, LPG, graph DB vs compute engine, power of graphs) | 19-28 | 1-10 |
| 2 | Options for Storing Connected Data | 29-42 | 11-24 |
| 3 | Data Modeling with Graphs (LPG, Cypher, data center, Shakespeare, e-mail) | 43-82 | 25-64 |
| 4 | Building a Graph Database Application | 83-122 | 65-104 |
| 5 | Graphs in the Real World | 123-165 | 105-147 |
| 6 | Graph Database Internals | 167-188 | 149-170 |
| 7 | Predictive Analysis with Graph Theory | 189-209 | 171-191 |
| App. A | NOSQL Overview | 211-228 | 193-210 |
| — | Index | 229-238 | 211-220 |

### Useful subsections (PDF)
Cypher: 45-49, 63-70. Indexes and Constraints: 65-66. E-mail provenance: 70-82. Facts as nodes: 86-89. Time: 90-92. Embedded vs Server: 94-99. Clustering: 99-102. Testing: 103-113. Capacity: 113-117. Import: 117-121. Talent.net: 129-140. TeleGraph: 141-149. Global Post: 150-165. IFA: 167-170. Storage: 170-176. APIs: 176-179. Transactions and HA: 180-184. Scale: 184-188. BFS/DFS: 189-191. Dijkstra: 191-198. A*: 199. Triadic/balance/bridges: 200-208.

## When to open each file
| Trigger | File |
|---|---|
| node, label, relationship, property | `modelo-de-grafos-de-propriedades-rotuladas.md` |
| IFA, traversal cost, table 2-1 | `adjacencia-livre-de-indices-ifa-e-performance.md` |
| relational vs NoSQL vs graph | `relacional-vs-nosql-vs-grafos.md` |
| MATCH, WHERE, MERGE, WITH, indexes, constraints | `cypher-fundamentos-e-padroes-de-consulta.md` |
| variable-length paths, shortestPath, UNION, reduce | `cypher-avancado-caminhos-variaveis-e-algoritmos.md` |
| how to model, node vs relationship, facts, values | `diretrizes-de-modelagem-em-grafo.md` |
| dates, timeline tree, linked lists, intervals | `modelagem-temporal-time-trees-e-intervalos.md` |
| supernode, dense node | `supernos-anti-padroes-e-mitigacoes.md` (the book does not cover it) |
| fixed-size records, page cache, neostore files | `neo4j-storage-internals-e-page-cache.md` |
| transactions, locks, WAL, HA, scale, sharding | `transacoes-acid-concorrencia-e-cluster-causal.md` |
| embedded vs server, testing, capacity, import | `arquitetura-testes-capacity-e-importacao.md` |
| Talent.net, TeleGraph, Global Post | `casos-reais-recomendacoes-rbac-e-logistica.md` |
| DFS/BFS, Dijkstra, A*, triadic, balance, bridges | `teoria-dos-grafos-e-algoritmos-preditivos.md` |
| mistakes and antipatterns | `casos-e-antipadroes.md` |
| step-by-step procedures | `procedimentos.md` |
| Appendix A, hypergraphs, triples, ACID/BASE | `nosql-apendice-e-modelos-de-grafo.md` |
| Cypher version, old syntax, what is missing | `versoes-e-conteudo-datado.md` |
| terms | `glossario.md` |

## Scripts (Python 3, stdlib, no network, use `python -I`)
- `scripts/graph_lookup.py`: topics by keyword, with pages (index in `graph_index.json`); "NOT COVERED" when the collection does not address it.
- `scripts/ifa_cost_calc.py`: visit count per hop for IFA vs. index. Formulas O(m) and O(m log n) are from the book (NEO4J p.168); the k^d variant is [inference]; the log base (fan-out) is [extrapolation] and is a parameter.
- `scripts/cypher_linter.py`: rules sourced from a book page when possible; the rest are labeled [extrapolation].
- `scripts/graph_advisor.py`: heuristics from the book's guidelines (p.85-89); degree thresholds are [extrapolation] parameters.
- `tests/verify_citations.py`, `tests/audit_tokens.py`, `tests/run_script_tests.py`: verification (see `tests/relatorio-de-fidelidade.md`).

## What the collection does NOT say (summary)
Supernodes; Raft/Causal Cluster; Read Committed; `EXPLAIN`/`PROFILE`; `AllNodesScan`; `OutOfMemoryError` from `*`; `allShortestPaths`; GDS/PageRank; APOC; Bolt; vectors; time tree with hour; Dijkstra in Cypher; memory sizing thresholds (GB). Details in `versoes-e-conteudo-datado.md`.

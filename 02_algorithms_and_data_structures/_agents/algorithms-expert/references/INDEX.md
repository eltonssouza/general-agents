# References INDEX — algorithms-expert

Source: **JE** = *Algorithms*, Jeff Erickson (1st paperback edition, 13 Jun 2019; CC BY 4.0 license), a **472-page** PDF at `02_algorithms_and_data_structures/Algorithms-Erickson.pdf`. The package is an original synthesis and does not reproduce the book.

## Page convention (mandatory)
- **Every citation `(JE p.N)` uses the PDF page** (the same numbering as the `=== PAGE N ===` markers of the extracted text).
- **Printed page = PDF page − 18** (verified: chapter 1 starts on printed page 21 = PDF 39; chapter 12 on printed 379 = PDF 397). PDF pages 1-18 are the cover, credits, preface and table of contents.
- When citing to the user, write "JE p.N (PDF; printed N−18)" at least once per answer.
- The v1 package convention was already PDF and consisted of the chapter boundaries; the pages *inside* the chapters were checked one by one in this version (see `tests/relatorio-de-fidelidade.md`).

## Chapter map (PDF → printed)
| Ch. | Title | PDF (body; exercises) | Printed (body) | Reference file |
|---|---|---|---|---|
| Preface | Preface | 5-12 | i-viii | — |
| 0 | Introduction | 19-34; ex. 35-38 | 1-16 | `fundamentos-e-analise.md` |
| 1 | Recursion | 39-62; ex. 62-88 | 21-44 | `recursao-e-divisao-e-conquista.md` |
| 2 | Backtracking | 89-111; ex. 111-114 | 71-93 | `backtracking.md` |
| 3 | Dynamic Programming | 115-140; ex. 141-176 | 97-122 | `programacao-dinamica.md` |
| 4 | Greedy Algorithms | 177-194; ex. 194-204 | 159-176 | `algoritmos-gulosos.md` |
| 5 | Basic Graph Algorithms | 205-224; ex. 225-242 | 187-206 | `grafos-e-travessias.md` |
| 6 | Depth-First Search | 243-262; ex. 262-274 | 225-244 | `grafos-e-travessias.md` |
| 7 | Minimum Spanning Trees | 275-286; ex. 286-290 | 257-268 | `arvores-geradoras-e-caminhos-minimos.md` |
| 8 | Shortest Paths | 291-313; ex. 314-326 | 273-295 | `arvores-geradoras-e-caminhos-minimos.md` |
| 9 | All-Pairs Shortest Paths | 327-338; ex. 338-344 | 309-320 | `arvores-geradoras-e-caminhos-minimos.md` |
| 10 | Maximum Flows & Minimum Cuts | 345-362; ex. 362-370 | 327-344 | `fluxo-maximo-e-cortes.md` |
| 11 | Applications of Flows and Cuts | 371-386; ex. 386-396 | 353-368 | `aplicacoes-de-fluxo.md` |
| 12 | NP-Hardness | 397-433; ex. 433-459 | 379-415 | `complexidade-e-np-completude.md` |
| — | Indexes and credits | 460-472 | 442-454 | — |

## File map
| File | Contents |
|---|---|
| `fundamentos-e-analise.md` | Definition of an algorithm, how to describe one, correctness, running time; **what Ch. 0 does not contain**. |
| `recursao-e-divisao-e-conquista.md` | Recursion Fairy, Hanoi, MergeSort, QuickSort, recursion trees, linear-time selection, Karatsuba, exponentiation. |
| `backtracking.md` | The pattern, $n$ Queens, game trees (good/bad), Subset Sum, text segmentation, LIS, optimal BST. |
| `programacao-dinamica.md` | Fibonacci, the two-stage recipe, "Greed is Stupid", LIS, edit distance, Subset Sum, optimal BST, DP on trees, DP on a dag. |
| `algoritmos-gulosos.md` | Exchange argument, tape storage, intervals, Huffman, Gale-Shapley (hospitals propose). |
| `grafos-e-travessias.md` | Representations, WFS, DFS, edge classification, topological order, SCC. |
| `arvores-geradoras-e-caminhos-minimos.md` | MST (Borůvka, Jarník, Kruskal), SSSP (Ford, BFS, dag, Dijkstra, Bellman-Ford), APSP (Johnson, Floyd-Warshall). |
| `fluxo-maximo-e-cortes.md` | Flow, cut, theorem, residual graph, Ford-Fulkerson, decomposition, Edmonds-Karp. |
| `aplicacoes-de-fluxo.md` | Disjoint paths, matching, tuples, cover, baseball, project selection. |
| `complexidade-e-np-completude.md` | P/NP, reduction, Cook-Levin (not proved), 3Sat, IndSet, 3Color, Hamiltonian, Subset Sum. |
| `casos-e-antipadroes.md` | False premises and typical mistakes, with what the book actually says. |
| `procedimentos.md` | Playbooks (what comes from the book and what is the package's own organization). |
| `glossario.md` | Book terms with page numbers, and common terms that the book does NOT use. |

## What the book does NOT contain (answer "the book does not cover this" or label `[extrapolation]`)
| Topic | Status in the book |
|---|---|
| Master Theorem | Only in the back-of-book index ("see recursion trees", JE p.454); the method is the recursion tree (JE p.49-52). |
| Formal definition of $O,\Omega,\Theta,o,\omega$ | Prerequisite (JE p.6); used without a formal definition. |
| RAM model as the basis of the analysis | Only in Ch. 12 (note 6, JE p.402). |
| Minimax, alpha-beta | Does not appear; the game tree uses good/bad states (JE p.93). |
| *Greedy choice property*, *overlapping subproblems* | Terms not used. |
| Knuth-Yao for optimal BST; $O(n\log n)$ for LIS | Do not appear. |
| 1D $O(T)$ vector for Subset Sum; $O(\min(m,n))$ for edit distance | Not stated. |
| König's and Menger's theorems | Not stated (Kőnig only as a historical name, JE p.208, 374). |
| Proof of Cook-Levin | Statement without proof (JE p.401-402). |
| Advanced data structures (skip lists, red-black trees, Fibonacci heaps in detail) | Prerequisite (JE p.6); Fibonacci heap only mentioned (JE p.282-283). |
| Linear programming, approximation algorithms, randomized algorithms | Out of scope (the analysis of randomized QuickSort is deferred to the author's notes, JE p.49). |
| Any programming language | Pseudocode only (JE p.31). |

## `[DATED]` content
"Fastest known algorithm" as of 2019: integer multiplication $O(n\log n)$ (JE p.60), matrix multiplication $O(n^{2.372864})$ (JE p.335), Orlin's $O(VE)$ maximum flow (JE p.361-362), best algorithms for flows in unit-capacity networks (JE p.362). Cite as "as of 2019, according to the book".

## Labels
- `[from source]`: a fact you read on the cited page.
- `[inference]`: a direct deduction from the book.
- `[extrapolation]`: useful outside knowledge, never attributed to the book.
- `[DATED]`: state of the art that may have changed since 2019.

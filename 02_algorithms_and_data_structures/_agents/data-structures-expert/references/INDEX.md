# Reference index: data-structures-expert

Single source: **ODS** = Pat Morin, *Open Data Structures*, Edition 0.1Gβ, 326 pages (the file is named `Open-Data-Structures-Python.pdf`). Source note: the PDF title page says "(in pseudocode)"; the text presents pseudocode and states that the Python, Java and C++ code is on the book's website `[from source] (ODS p.35)`. The package does not reproduce the book's text: these are the authors' own syntheses in English.

## Page convention (read before citing)
- `(ODS p.N)` = **PDF page number** (1 to 326). **Printed page = N − 12** for N ≥ 13 (PDF p.13 is printed page 1; PDF p.326 is printed 314). Pages 1-12 are front matter. Example: ArrayStack starts at PDF p.44 = printed 32.
- The book's subject index and bibliography use the **printed** numbering; add 12 to get the PDF page.
- The `=== PAGE N ===` markers used by the package's checkers (`tests/`) follow the PDF numbering.
- Some PDF figures have degraded text on extraction (formulas, underlines); the cited formulas were checked while reading the page.

## Epistemic labels
- `[from source] (ODS p.N)`: I read the cited page and it supports the sentence.
- `[inference]`: direct deduction from what the book shows, but which the book does not state.
- `[extrapolation]`: useful general knowledge that the book does not contain (e.g. labels such as "2-independent", real-time behavior).
- `[DATED]`: tools, hardware, numbers and references from the time of the book (mentioned as "at the time the book was written").

## Chapter map to PDF pages
| Ch. | Topic | PDF pages | File |
|---|---|---|---|
| 1 | Introduction, interfaces, model, summary tables | 13-41 (tables 1.1 and 1.2 on p.36 and p.38) | `interfaces-e-analise-amortizada.md` |
| 2 | Array-based lists | 43-71 | `estruturas-baseadas-em-arrays.md` |
| 3 | Linked lists | 73-93 | `listas-encadeadas.md` |
| 4 | Skiplists | 95-111 | `skiplists.md` |
| 5 | Hash tables | 113-138 | `tabelas-hash.md` |
| 6 | Binary trees and BST | 139-156 | `arvores-binarias-e-bst.md` |
| 7 | Random binary search trees and Treap | 157-176 | `arvores-balanceadas-e-treaps.md` |
| 8 | Scapegoat trees | 177-188 | `arvores-balanceadas-e-treaps.md` |
| 9 | Red-black trees (and 2-4) | 189-213 | `arvores-rubro-negras.md` |
| 10 | Heaps | 215-228 | `heaps-e-filas-de-prioridade.md` |
| 11 | Sorting | 229-249 | `ordenacao-e-limites-inferiores.md` |
| 12 | Graphs | 251-267 | `grafos-e-representacoes.md` |
| 13 | Data structures for integers | 269-286 | `estruturas-para-inteiros-e-tries.md` |
| 14 | External memory and B-trees | 287-310 | `memoria-externa-e-arvores-b.md` |
| - | Bibliography (from p.311) and subject index (p.313-326) | 311-326 | lookup only |
Chapters without their own reference file: the math of Ch. 1 (logarithms, factorials, O notation, probability) is summarized in `interfaces-e-analise-amortizada.md`.

## Thematic file map
| File | Contents |
|---|---|
| `interfaces-e-analise-amortizada.md` | Queue/Stack/Deque/List/USet/SSet; Word-RAM; worst-case, amortized, expected; where the book uses the potential method; tables 1.1 and 1.2 |
| `estruturas-baseadas-em-arrays.md` | ArrayStack, FastArrayStack, ArrayQueue, ArrayDeque, DualArrayDeque, RootishArrayStack |
| `listas-encadeadas.md` | SLList, DLList (`dummy` node), SEList |
| `skiplists.md` | SkiplistSSet, SkiplistList, analysis |
| `tabelas-hash.md` | multiplicative hashing, ChainedHashTable, LinearHashTable (`del`), tabulation hashing, hash codes |
| `arvores-binarias-e-bst.md` | BinaryTree, traversals, BinarySearchTree |
| `arvores-balanceadas-e-treaps.md` | rotations, random binary search trees, Treap, ScapegoatTree |
| `arvores-rubro-negras.md` | 2-4 trees, RedBlackTree (left-leaning variant), AVL (note) |
| `heaps-e-filas-de-prioridade.md` | BinaryHeap, MeldableHeap |
| `ordenacao-e-limites-inferiores.md` | merge-sort, quicksort, heap-sort, lower bound, counting sort, radix sort |
| `grafos-e-representacoes.md` | AdjacencyMatrix, AdjacencyLists, BFS, DFS |
| `estruturas-para-inteiros-e-tries.md` | BinaryTrie, XFastTrie, YFastTrie |
| `memoria-externa-e-arvores-b.md` | external memory model, BlockStore, B-trees |
| `casos-e-antipadroes.md` | pitfalls, each split into [from source]/[inference]/[extrapolation] |
| `procedimentos.md` | step-by-step routines with the algorithm's page in the book |
| `glossario.md` | EN-PT terms with page |

## What the book does NOT contain (label as `[extrapolation]` or say "the book does not cover it")
- The terms "tombstone"/"lápide", "primary clustering"/"agrupamento primário" and "2-independent"/"2-universal" (the book uses `del` values, the invariant `length(t) ≥ 2q` and proves the collision probability 2/2^d).
- **Real-time** analysis (hard real-time), cache effects beyond one sentence about memcpy/memmove (p.49-50) and the "cache" of internal B-tree nodes (p.309), concurrency and persistence.
- Additive array growth (+c) as an analyzed alternative; the potential method in its general form Φ.
- AVL with pseudocode (only a note in the discussion, p.210-211); Fibonacci/pairing/binomial heaps (names only, p.226); B+-trees (only exercise 14.8, p.310); perfect hashing/cuckoo (mention only, p.134-135); generic "top-down" red-black trees (mention only, p.210).
- Graph algorithms beyond BFS/DFS (Dijkstra etc.), NP-completeness, flow networks (those belong to Erickson's book, another agent).
- 32/64-bit numbers, "5 or 6 operations" for log w, B=4096 words: they are not in the book.
- Book test in Python: the PDF has pseudocode; any Python code in the package is `[extrapolation]`.

## `[DATED]` content
- RAM/SSD/HDD access times and the 4096-byte block size of the author's computer (p.287); number of web pages, Google queries/s (p.14-15); file systems and databases that use B-trees (p.308). These are illustrations from the time of the book.
- Edition 0.1Gβ: the book is in beta format; check whether a later edition exists before claiming that a statement is "the current version".

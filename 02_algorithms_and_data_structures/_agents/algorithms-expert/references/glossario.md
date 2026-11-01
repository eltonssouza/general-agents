# Glossary (book terms, with the page where they appear)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). The Portuguese rendering is the package's own (kept so that Portuguese-speaking users can map terms); the English term is the book's. Only terms that appear in the text are included; terms from other sources are listed under "Common terms the book does NOT use".

| Term in the book | Portuguese | Short definition and where it is |
| :--- | :--- | :--- |
| *Recursion Fairy* | Fada da Recursão | Nickname for the Induction Hypothesis: whoever solves the smaller instances (JE p.40-41). |
| *reduction* | redução | Solving $X$ using an algorithm for $Y$ as a black box (JE p.39); in NP, the direction matters (JE p.404). |
| *divide and conquer* | divisão e conquista | Split into smaller independent instances, delegate, combine (JE p.49). |
| *recursion tree* | árvore de recursão | A tree with one node per subproblem; sum level by level (JE p.49-52). |
| *domain transformation* | transformação de domínio | Technique for ignoring ceilings and floors in recurrences (JE p.52-53). |
| *median of medians* ("mom") | mediana das medianas | Pivot of MomSelect (JE p.55). |
| *backtracking* | retrocesso | Trying all alternatives by recursion (JE p.89). |
| *game tree*; *good*/*bad* state | árvore do jogo; estado bom/ruim | Zermelo's definition (JE p.93). |
| *Interpunctio Verborum* (*text segmentation*) | segmentação de texto | Splitting a string into words (JE p.98-99). |
| *memoization* | memorização | Storing the results of recursive calls (JE p.117-118). |
| *dynamic programming* | programação dinâmica | "Recursion without repetition" (JE p.123). |
| *specification* (of the subproblem) | especificação | English description of what is being solved (JE p.124). |
| *evaluation order* | ordem de avaliação | Linear extension of the partial order of dependencies (JE p.125). |
| *dependency graph* | grafo de dependências | One vertex per subproblem; it is a dag (JE p.211, 252). |
| *optimal substructure* | subestrutura ótima | Removing the last column of the optimal alignment leaves the optimum for the prefixes (JE p.130). |
| *edit distance* | distância de edição | Minimum number of insertions, deletions and substitutions (JE p.129). |
| *pseudo-polynomial time*; *weakly NP-hard* | tempo pseudopolinomial; NP-difícil fraco | Polynomial time in $T$ but not in the number of bits (JE p.422). |
| *greedy algorithm* | algoritmo guloso | Makes each decision directly, without recursive subproblems (JE p.125). |
| *exchange argument* | argumento de troca | Correctness proof for greedy algorithms (JE p.181-183). |
| *prefix-free code*; *Huffman code* | código livre de prefixo; código de Huffman | JE p.183-188. |
| *stable matching*; *unstable pair* | emparelhamento estável; par instável | JE p.189. |
| *whatever-first search*; *bag* | busca "qualquer-primeiro"; bolsa | Generic traversal skeleton (JE p.218). |
| *adjacency list*; *adjacency matrix* | lista/matriz de adjacência | JE p.213-215. |
| *preorder*; *postorder*; *active interval* | pré-ordem; pós-ordem; intervalo ativo | JE p.245-246. |
| *tree*/*forward*/*back*/*cross edge* | arestas de árvore, avanço, retorno, cruzamento | DFS classification (JE p.247). |
| *topological ordering* | ordem topológica | All edges point to the right (JE p.250). |
| *dag*; *source*; *sink* | grafo acíclico dirigido; fonte; sorvedouro | JE p.210, 249. |
| *strong component*; *scc(G)* | componente forte; grafo de componentes | JE p.255-256. |
| Kosaraju-Sharir; Tarjan | algoritmos de SCC | Strong components in $O(V+E)$ (JE p.258-262). |
| *safe edge*; *useless edge* | aresta segura; aresta inútil | MST (JE p.277-278). |
| Borůvka, Jarník ("Prim"), Kruskal | algoritmos de MST | JE p.279-286. |
| *tense edge*; *relax* | aresta tensa; relaxar | Ford's algorithm (JE p.294-295). |
| *shortest-path tree* | árvore de caminhos mínimos | JE p.292. |
| *negative cycle* | ciclo negativo | JE p.293. |
| *reweighting*; *price* | reponderação; preço | $w'(uv)=\pi(u)+w(uv)-\pi(v)$ (JE p.329-330). |
| *(s,t)-flow*; *feasible*; *value* | fluxo viável; valor | JE p.346-347. |
| *(s,t)-cut*; *capacity of a cut* | corte; capacidade | JE p.347. |
| *residual capacity*; *residual graph*; *augmenting path* | capacidade residual; grafo residual; caminho aumentante | JE p.349-350. |
| *Integrality Theorem* | Teorema da integralidade | JE p.352. |
| *flow decomposition* | decomposição de fluxo | JE p.355-357. |
| *fattest augmenting path* | caminho aumentante mais gordo | JE p.358. |
| *vertex capacities*; $v_{in}$/$v_{out}$ | capacidades nos vértices | JE p.372. |
| *matching*; *alternating path* | emparelhamento; caminho alternante | JE p.373-374. |
| *tuple selection* | seleção de tuplas | Name coined by the author (JE p.375, note 2). |
| *disjoint-path cover* | cobertura por caminhos disjuntos | JE p.378. |
| *Project Selection* | seleção de projetos | JE p.384-385. |
| *decision problem*; P; NP; co-NP | problema de decisão; classes P, NP, co-NP | Definitions of Section 12.2 (JE p.399). |
| *NP-hard*; *NP-easy*; *NP-complete* | NP-difícil; NP-fácil; NP-completo | Informal definitions (JE p.400-401). |
| *Cook reduction*; *Karp reduction* | redução de Cook; redução de Karp (muitos-para-um) | Formal types of reduction (JE p.402-403). |
| *CircuitSat*; *Sat*; *3Sat* | satisfatibilidade de circuito; de fórmula; de 3CNF | Base problems of the reductions (JE p.397-408). |
| *gadget* | gadget | Subgraph that enforces a constraint in the reduction (JE p.413). |
| *certificate* | certificado | Proof that an instance is "good" (JE p.410). |
| *strongly NP-hard* | NP-difícil forte | JE p.422. |
| PSPACE, EXP, QBF | classes maiores | Closing overview of the book (JE p.430-432). |

## Common terms the book does NOT use (do not cite as from the book)
*Master theorem* (only in the index, which points to recursion trees, JE p.454), *minimax*, *alpha-beta*, *Greedy Choice Property*, *overlapping subproblems*, *Knuth-Yao*, *patience sorting*, *Hopcroft-Karp* as a detailed algorithm (only mentioned, JE p.374), *König/Menger theorem*, *RAM model* (only note 6, JE p.402).

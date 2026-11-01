# EN-PT glossary

Pages = PDF (printed = N − 12). The "Source" column cites the page where the term is defined or used in the book. Terms marked `[extrapolation]` in the comment column do **not** appear in the book. The "Portuguese translation" column keeps the Portuguese term for users who write in Portuguese.

| Term (book) | Portuguese translation | Short definition | Source |
|---|---|---|---|
| amortized running time | tempo amortizado | m operations cost at most m·f(n) in total | (ODS p.32) |
| expected running time | tempo esperado | expectation over the structure's own random choices | (ODS p.29, 32) |
| worst-case running time | tempo de pior caso | no operation exceeds f(n) | (ODS p.32) |
| word-RAM | modelo Word-RAM | memory of `w`-bit cells, `w ≥ log n`, basic operations in O(1) | (ODS p.30-31) |
| interface | interface | what the structure does; contrasts with implementation | (ODS p.16) |
| ArrayStack | pilha em array | List on a backing array; doubles and shrinks at `length(a) ≥ 3n` | (ODS p.44-47) |
| backing array | array de apoio | array that stores the elements | (ODS p.43-44) |
| ArrayQueue | fila em array circular | FIFO with `j` and modular arithmetic | (ODS p.50-53) |
| ArrayDeque | deque em array circular | List shifting the shorter side | (ODS p.54-56) |
| DualArrayDeque | deque de duas pilhas | `front` (reversed) and `back`; `balance()` | (ODS p.56-62) |
| RootishArrayStack | pilha de blocos crescentes | blocks of size 1, 2, 3,...; waste O(√n) | (ODS p.62-68) |
| SLList / DLList | lista simples / dupla | linked with `next` / `next` and `prev` | (ODS p.73, 76) |
| dummy node | nó sentinela | node without data that closes the DLList into a cycle | (ODS p.77) |
| SEList | lista eficiente em espaço | list of blocks (BDeque) of size b+1 | (ODS p.80-81) |
| BDeque | deque limitado | ArrayDeque of fixed capacity b+1 | (ODS p.81) |
| spread / gather | espalhar / reunir | redistributes b(b±1) elements among blocks | (ODS p.84, 87-88) |
| skiplist | lista de salto | lists L₀,...,L_h with coin-based promotion | (ODS p.95) |
| sentinel | sentinela | starting node of each skiplist list | (ODS p.96) |
| search path | caminho de busca | right while not overshooting; otherwise down | (ODS p.96) |
| length of an edge | comprimento de aresta | edges of L₀ below it (SkiplistList) | (ODS p.101) |
| hash table | tabela hash | stores `w`-bit integers in an array | (ODS p.113) |
| hash code | código hash | `w`-bit integer associated with an object | (ODS p.113, 129) |
| multiplicative hashing | hashing multiplicativo | `((z·x) mod 2^w) div 2^(w−d)` with odd `z` | (ODS p.116) |
| chaining | encadeamento | each position stores a list | (ODS p.113) |
| linear probing | sondagem linear | tries consecutive positions | (ODS p.120) |
| `del` value | valor `del` | marks a cell that once held data; `[extrapolation]` "tombstone" | (ODS p.121) |
| run | sequência (run) | consecutive non-`nil` entries in the analysis | (ODS p.124) |
| tabulation hashing | hashing por tabulação | tables of random integers and exclusive-or | (ODS p.127-128) |
| BinaryTree | árvore binária | nodes with `left`, `right`, `parent` | (ODS p.141) |
| external node | nó externo | imaginary `nil` child; n real nodes have n+1 external ones | (ODS p.141) |
| BinarySearchTree | árvore binária de busca | left < `u.x` < right | (ODS p.145) |
| random binary search tree | árvore de busca aleatória | BST built with a random permutation | (ODS p.157-158) |
| harmonic number | número harmônico | Hₖ = 1 + 1/2 + ... + 1/k | (ODS p.159) |
| rotation | rotação | swaps parent and child preserving in-order sequence | (ODS p.165-166) |
| Treap | Treap | BST on the keys and heap on the random priorities | (ODS p.163) |
| ScapegoatTree | árvore bode expiatório | partial rebuilding; `q/2 ≤ n ≤ q` | (ODS p.177-179) |
| scapegoat | bode expiatório | node with `size(child)/size(w) > 2/3` | (ODS p.180) |
| 2-4 tree | árvore 2-4 | leaves at the same depth; 2 to 4 children | (ODS p.190) |
| RedBlackTree | árvore rubro-negra | BST with colors; black-height and no-red-edge | (ODS p.194) |
| black-height | altura preta | same number of black nodes on every path | (ODS p.194) |
| left-leaning | inclinada à esquerda | black `u.left` implies black `u.right` | (ODS p.198) |
| BinaryHeap | heap binário | complete tree implicit in an array | (ODS p.215-216) |
| Eytzinger's method | método de Eytzinger | breadth-first order in an array | (ODS p.215) |
| MeldableHeap | heap fundível | pointer-based heap with randomized `merge` | (ODS p.221) |
| comparison tree | árvore de comparação | model of a comparison-based algorithm; ≥ n! leaves | (ODS p.240-241) |
| counting sort / radix sort | ordenação por contagem / por dígitos | O(n+k) / O((w/d)(n+2^d)) | (ODS p.245-246) |
| AdjacencyMatrix / AdjacencyLists | matriz / listas de adjacência | O(n²) / O(n+m) space | (ODS p.255, 259) |
| BFS / DFS | busca em largura / em profundidade | O(n+m) with adjacency lists | (ODS p.261, 264) |
| BinaryTrie | trie binária | leaves at depth `w`; `jump` | (ODS p.270-271) |
| XFastTrie / YFastTrie | trie X-fast / Y-fast | find O(log w); Y: add/remove expected O(log w) | (ODS p.278-279, 284) |
| external memory model | modelo de memória externa | blocks of `B` words; cost = transfers | (ODS p.288) |
| BlockStore | armazém de blocos | `read_block`, `write_block`, `place_block`, `free_block` | (ODS p.289) |
| B-tree | árvore B | B to 2B children; leaves at the same depth | (ODS p.290) |
| underflow | subfluxo | node with fewer than B−1 keys after removal | (ODS p.299) |

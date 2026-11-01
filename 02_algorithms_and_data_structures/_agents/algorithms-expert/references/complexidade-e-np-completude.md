# NP-hardness and reductions (Ch. 12)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 12 = PDF p.397-433 (exercises p.433-460 approx.). Reductions in the book: CircuitSat → Sat → 3Sat → MaxIndSet → (MaxClique, MinVertexCover); 3Sat → 3Color; MinVertexCover and 3Sat → Hamiltonian Cycle; MinVertexCover → SubsetSum.

## 1. Motivation and CircuitSat (12.1, JE p.397-399)
- `[from source]` *CircuitSat*: given a Boolean circuit (And, Or, Not gates), is there an input that makes it output True? For a fixed input the circuit is evaluated in linear time (DFS), but nobody knows how to solve the problem better than trying all $2^n$ inputs (JE p.398-399). It is not proved that there is no fast algorithm (JE p.398-399).

## 2. P, NP, co-NP (12.2, JE p.399-400)
- `[from source]` Decision problem: output Yes/No. **P**: decidable in polynomial time. **NP**: when the answer is Yes there is a proof verifiable in polynomial time. **co-NP**: the same for No answers (JE p.399).
- `[from source]` The example used is CircuitSat: any input that yields True is a certificate verifiable by evaluating the circuit (JE p.399). Every problem in P is in NP and in co-NP (JE p.399).
- `[from source]` P vs NP is open (one of the Millennium Problems); most people accept P≠NP as a "law of nature"; NP vs co-NP is also open (JE p.400).
- `[inference]` The v1 example "Hamiltonian cycle is in NP by verifying a certificate in $O(V)$" is **not** on p.399-400 of the book; it is true and customary, so label it.

## 3. NP-hard, NP-easy, NP-complete (12.3, JE p.400-402)
- `[from source]` Informal definition: $\Pi$ is **NP-hard** if a polynomial algorithm for $\Pi$ would imply a polynomial algorithm for every problem in NP (⇔ if $\Pi$ can be solved in polynomial time, then P=NP). **NP-complete**: NP-hard and in NP ("NP-easy"). A polynomial algorithm for one NP-complete problem would imply all of them (JE p.400-401).
- `[from source]` **Cook-Levin Theorem** (Cook 1971, Levin 1973): CircuitSat is NP-hard. **The book neither proves nor sketches the proof** ("I won't even sketch a proof here") (JE p.401-402). The v1 package described "unrolling the verifier into a circuit" as if it were on p.404-406: removed.
- `[from source]` Formally (12.4, optional topic): P and NP are classes of languages decided by Turing machines (deterministic and nondeterministic) (JE p.402). Formal NP-hardness via **Turing/Cook reductions** or via **many-one/Karp reductions** (a function $f$ such that $x\in L'\iff f(x)\in L$), preferred by theorists because NP is closed under Karp reductions but (unless NP=co-NP) not under Cook reductions; all reductions in the chapter are logarithmic-space (JE p.402-403). The RAM machine model is only described here (note 6, JE p.402).

## 4. The direction rule of a reduction (12.5, JE p.403-406)
- `[from source]` "Reducing $A$ to $B$" = describing an algorithm for $A$ assuming one for $B$ (JE p.403). **To prove that $A$ is NP-hard, reduce a known NP-hard problem to $A$** — "tattoo it on your hand" (JE p.404). If $A$ were easy, the known one would be easy; hence $A$ is hard (JE p.404).
- `[inference]` If the reduction goes in the opposite direction ($X\le A$ with $A$ already known), it only shows that $X$ is **no harder** than $A$; there is no hardness conclusion for $X$. The v1 claim that this "proves $X\in NP$" is not in the book (and would hold only if $A\in NP$ and the reduction were Karp): downgraded to `[inference]` and reworded.
- `[from source]` CircuitSat → Sat: one variable per wire, one equation per gate, all joined by $\land$ plus $\land z$; linear transformation; "if Sat were polynomial, CircuitSat would be, hence P=NP" (JE p.404-406).

## 5. 3Sat (12.6, JE p.406-408)
- `[from source]` 3CNF: a conjunction of clauses with **exactly three literals** (JE p.406). Reduction CircuitSat → 3Sat in stages (binary gates; one clause per gate; each gate becomes CNF via 3 clauses; pad to 3 literals with new variables); linear time (JE p.406-408). Tseitin (1966) had already described most of it (JE p.407).

## 6. Maximum independent set (12.7, JE p.408-410)
- `[from source]` From 3Sat: $3k$ vertices (one per literal of each of the $k$ clauses); edges between literals of the same clause (triangles) and between a literal and its negation; **$G$ has an independent set of size $k$ if and only if $\Phi$ is satisfiable** (JE p.408-410).

## 7. The general pattern of a reduction (12.8, JE p.410-411)
- `[from source]` All NP-hardness proofs follow the same outline. To reduce $X$ to $Y$ in polynomial time, do **three things**: (1) a polynomial algorithm that transforms an arbitrary instance $x$ of $X$ into a special instance $y$ of $Y$; (2) prove that if $x$ is "good" then $y$ is "good"; (3) prove that if $y$ is "good" then $x$ is "good" (the most laborious part) (JE p.410).
- `[from source]` Certificate view: design three algorithms — transform the instance; transform a certificate for $x$ into a certificate for $y$; transform a certificate for $y$ into a certificate for $x$. The forward proof must handle arbitrary instances of $X$; the backward one only the special instances produced by the reduction (JE p.410-411). Only the first algorithm needs to be polynomial (JE p.411).
- `[inference]` The v1 package's "4-step playbook" (state the problem, choose the known one, describe the reduction, prove the equivalence) is a good didactic organization, but **the book lists 3 tasks**; do not present "4 steps" as from the book.

## 8. Clique and Vertex Cover (12.9, JE p.412-413)
- `[from source]` Clique = complete subgraph; vertex cover = a set that touches every edge. MaxIndSet → MaxClique via the complement graph ($S$ independent in $G$ ⇔ clique in $\bar G$) (JE p.412). $I$ is independent in $G$ ⇔ $V\setminus I$ is a vertex cover, so the largest independent set has size $n-k$ if the smallest cover has size $k$ (JE p.412-413).

## 9. Coloring (12.10, JE p.413-416)
- `[from source]` From 3Sat to **3Color** with *gadgets*: a truth gadget (triangle $T$, $F$ and $X$ — "True, False, Other"), one variable gadget per variable (a triangle joining $a$, $\bar a$ to node $X$) and one clause gadget per clause (five new nodes and ten edges joining the three literals to $T$) (JE p.414-415). If 3Color is NP-hard, the general coloring problem (minimum number of colors) is too (JE p.416). *(v1 called the third node $B$.)*

## 10. Hamiltonian cycle (12.11, JE p.416-420)
- `[from source]` A Hamiltonian cycle visits each vertex exactly once (unlike an Euler circuit, which is linear by DFS) (JE p.416). The book proves NP-hardness on directed graphs in two ways: from Vertex Cover (edge gadgets and vertex chains, $O(V^2)$) and from 3Sat (variable gadgets with $2k$ vertices and clause vertices, $O(kn)$) (JE p.416-419). The Hamiltonian path and the undirected versions are also NP-hard (JE p.419-420).
- `[from source]` **Traveling salesman (TSP)**: find the shortest Hamiltonian cycle (or path) in a weighted graph; "obviously harder" than deciding whether a cycle exists — consider the graph in which every edge weighs 1 — hence NP-hard (JE p.420). TSP is strongly NP-hard (*strongly NP-hard*) even on a complete graph with weights 1 or 2 (JE p.422). `[inference]` "Weight 1 for the graph's edges and 2 for the others" is the usual reduction from Hamiltonian cycle to metric/complete TSP; the book uses this information as an observation about strong NP-hardness.

## 11. Subset Sum (12.12, JE p.420-422)
- `[from source]` From Vertex Cover: number the edges from 0 to $E-1$; $X$ contains $b_i=4^i$ for each edge and $a_v=4^E+\sum_{i\in\Delta(v)}4^i$ for each vertex; target $T=k\cdot4^E+\sum_{i<E}2\cdot4^i$ ($(E+1)$-digit numbers in **base 4**, to avoid *carries*); example with $T=2730$ and $k=2$ (JE p.420-422).
- `[from source]` *Caveat Reductor*: the $O(nT)$ algorithm of Ch. 3 does not prove P=NP because the time must be polynomial in the **input size in bits**; such an algorithm is pseudo-polynomial time (*pseudo-polynomial time*) and the problem is *weakly NP-hard*; problems that remain NP-hard with numbers in unary are *strongly NP-hard* (e.g., TSP) (JE p.422).

## 12. Other useful NP-hard problems (12.13-12.14, JE p.422-426)
- `[from source]` List (JE p.423-425): PlanarCircuitSat, 1-in-3Sat, NotAllEqual3Sat, Planar3Sat, Exact3DimensionalMatching (X3M), Partition (weak), 3Partition (strong), SetCover, HittingSet, **LongestPath** (longest simple path between $u$ and $v$; a generalization of the Hamiltonian path, unlike the shortest path, which is polynomial) (JE p.424), SteinerTree, Max2Sat (2Sat is polynomial), MaxCut; many puzzles and games (JE p.424-425). Most were proved by Karp in 1972 (JE p.423).
- `[from source]` Rules of thumb for choosing which problem to reduce from: assigning bits/choosing subsets → Sat/Partition; labels from a small set → kColor/3Color; ordering objects → Hamiltonian cycle/TSP; etc. (JE p.426). A "frivolous" example (international checkers/*draughts*) (JE p.426-430).
- `[extrapolation]` The argument that the **longest simple path** "has no optimal substructure" because subpaths may cross is a customary didactic explanation; the book shows the longest path in a **dag** in $O(V+E)$ by DP (JE p.253-254) and NP-hardness in the general case (JE p.253, 424), but does not make that substructure argument (v1 cited it at p.422/123-125).

## 13. Beyond (12.16, JE p.430-433)
- `[from source]` PSPACE: every problem in NP is in PSPACE; NP≠PSPACE is believed, but not even P≠PSPACE is proved (JE p.430); QBF as the canonical PSPACE-hard problem, and many generalized two-player games are PSPACE-hard (JE p.431). EXP: P≠EXP is known, but not NP≠EXP; NEXP, EXPSPACE and the chain of inclusions P ⊆ NP ⊆ PSPACE ⊆ EXP ⊆ NEXP ⊆ ... (JE p.431-433). Cited as an overview, without details.

## Outside the book
Proof of the Cook-Levin theorem, classes of the Polynomial Hierarchy, approximation and inapproximability, parameterization (FPT), SAT solvers, the distinction $\mathrm{BPP}$/randomness, and specific reductions beyond those listed.

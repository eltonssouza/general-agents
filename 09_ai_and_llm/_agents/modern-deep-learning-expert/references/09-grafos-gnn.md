# 09 — Graph neural networks (GNN/GCN)

Source: UDL ch.13 (PDF p.254-281; body and notes read through p.277; p.278-281 NOT read). NNDL does not cover graphs (the occurrences of "graph" in it are plots/figures). Pages = PDF.

## 1. What a graph is for the book
- `[from source]` Three challenges: variable topology, huge graphs (social networks with a billion nodes) and often a single monolithic graph (transductive protocol) (UDL p.254).
- `[from source]` Examples: roads, molecules, circuits, social networks, citations, Wikipedia, programs, point clouds, protein interaction; sets and images can also be viewed as graphs (UDL p.254-255). Types: undirected, directed, heterogeneous/multigraph (knowledge graph), geometric (k nearest neighbors), hierarchical (UDL p.255-257); the chapter focuses on undirected graphs (UDL p.257).
- `[from source]` Representation: adjacency matrix `A` (N×N, symmetric in the undirected case), node matrix `X` (D×N) and edge matrix `E` (D_E×E) (UDL p.257-258, fig. 13.3).
- `[from source]` `A^L` counts walks, not simple paths, of length L; a nonzero entry implies distance ≤ L (UDL p.258-259, fig. 13.4).
- `[from source]` The numbering of the nodes is arbitrary: permuting nodes permutes the columns of X and the rows/columns of A: `X' = XP`, `A' = PᵀAP` (UDL p.259, eq. 13.1, fig. 13.5). Hence each layer must be **equivariant** to permutations and the graph-level output **invariant** (UDL p.263, eq. 13.6-13.7).

## 2. Tasks and losses
- Graph level (classify/regress the whole graph): aggregate the final embeddings (mean; mean pooling) and map through a layer: `Pr(y=1|X,A) = sig[β_K + ω_K H_K 1/N]` (UDL p.260, eq. 13.2); BCE or least-squares loss (UDL p.260). Occurs only in the inductive setting (UDL p.267).
- Node level: `sig[β_K + ω_K h_K^(n)]` per node (UDL p.262, eq. 13.3).
- Edge prediction: dot product of the embeddings of two nodes followed by a sigmoid, `sig[h^(m)ᵀ h^(n)]` (UDL p.262, eq. 13.4).

## 3. GCN layer
- `[from source]` "Spatial" GCN (not spectral): each layer is `H_{k+1} = F[H_k, A, φ_k]` (UDL p.262, eq. 13.5), with a relational inductive bias (UDL p.262).
- `[from source]` Simple layer: aggregate neighbors by sum `agg[n,k] = Σ_{m∈ne[n]} h_m` (eq. 13.8) and `h_n ← a[β + Ω h_n + Ω agg]` (eq. 13.9); in matrix form `H_{k+1} = a[β 1ᵀ + Ω H_k (A + I)]` (UDL p.264-265, eq. 13.10). (In the example the SAME Ω_k acts on the node and on the neighbors; the variation with a separate Ψ is on p.271, eq. 13.15.) It satisfies equivariance, variable number of neighbors, relational bias and parameter sharing (UDL p.265).
- `[from source]` Molecule classification example (toxic/harmless): X ∈ R^{118×N} with one-hot of the 118 elements (UDL p.265, eq. 13.11). Batches: treat the graphs as disconnected components of one large graph (UDL p.265-266).
- `[from source]` Inductive vs transductive: in the transductive (semi-supervised) setting a single graph has labeled and unlabeled nodes and the model must be retrained if new nodes arrive (UDL p.266-267). Example of node classification in a large graph (UDL p.267, eq. 13.12).
- `[from source]` Receptive field = k-hop neighborhood; **graph expansion problem** (the neighborhood of a few nodes can cover almost the whole graph); solutions: **neighborhood sampling** (sample a fixed number of neighbors per layer, which also acts as regularization) and **graph partitioning** (cluster into disjoint subgraphs to form batches) (UDL p.267-270, fig. 13.9-13.11). At inference intermediate representations are not stored (UDL p.270).
- `[from source]` Variations: diagonal enhancement `(1+ε_k)I` (eq. 13.14); separate transformation Ψ (13.15); residual connection by concatenation (13.16); aggregation by mean with `D⁻¹` (13.18); Kipf normalization `D^{-1/2} A D^{-1/2}` (13.19-13.20); aggregation by max pooling (13.21); attention on graphs: `s_mn = a[φᵀ [h'_m; h'_n]]` and `Softmask[S, A+I]` (13.22-13.24) (UDL p.270-274). Attention on graphs differs from transformer self-attention: here the similarities are learned by concatenation, not by the q·k product, and are masked to neighbors (UDL p.274, fig. 13.12).
- `[from source]` Edge graph (line graph) to process edge embeddings (UDL p.274-275).
- Notes (UDL p.275-277): GNNs by Gori et al. 2005/Scarselli et al. 2008; spectral methods (Bruna 2013, ChebNet, Kipf-Welling 2017); MPNN (Gilmer 2017), GraphSAGE; GAT (Veličković 2019); DeepSets (Zaheer 2017) for sets.

## 4. Responsible use of limits
- The book has no graph benchmarks; performance numbers for GNNs do not exist in the collection.
- `[extrapolation]` The choice among GCN, GAT, GraphSAGE and other variations depends on the problem and on post-2023 results; the collection only describes mechanisms.
- Relation to transformers: in UDL "the nodes attend to one another in each layer" (UDL p.246).

## 5. Script
`python -I scripts/dl_nets.py attention --tokens ... ` serves to compare with attention on graphs only conceptually; there is no GCN script (NOT COVERED numerically in the collection).

# 02 — Deep networks, capacity and universality

Sources: UDL ch.4 (PDF p.55-69), NNDL ch.4 (PDF p.187-218) and the opening of NNDL ch.5 (p.219-222). Read in full (except problems).

## 1. Composition and depth (UDL)

- `[from source]` Composing two shallow networks of 3 units can give 9 linear regions, more than a shallow network of 6 units; interpretation: the first network "folds" the input space and the second network replicates its function over the folded parts (UDL p.56-58, fig. 4.1-4.3). In 2D the example reaches 13 regions (UDL p.58, fig. 4.2).
- `[from source]` Composition is a special case of a network with two hidden layers; in the deep network the weights `ψ` are free, whereas in the composition they would be restricted to an outer product (UDL p.57-59, eq. 4.5-4.6).
- `[from source]` Hyperparameters: width (units per layer), depth (number of hidden layers K), capacity = total number of units; a network is a "family of families of functions" (UDL p.60).
- `[from source]` Matrix notation: `h1 = a[β0 + Ω0 x]`, `h_k = a[β_{k−1} + Ω_{k−1} h_{k−1}]`, `y = β_K + Ω_K h_K`; Ω0 is D1×Di, Ω_K is Do×D_K, the others D_{k+1}×D_k; the vector β_{k−1} has size D_k (UDL p.62-63, eq. 4.14-4.16).
- `[from source]` Counts for 1 input and 1 output: shallow with D>2 units has D+1 regions and 3D+1 parameters; deep with K layers of D>2 units has up to (D+1)^K regions and 3D+1+(K−1)D(D+1) parameters (UDL p.64). Fig. 4.7 example: K=5, D=10 gives 471 parameters and 161,051 regions; with Di=10, K=5, D=50: 10,801 parameters and more than 10^40 regions (UDL p.65). `[checked in dl_calc.py regions]`.
- `[from source]` Exact bound for Di inputs: `Nr = (D/Di + 1)^{Di(K−1)} · Σ_{j=0}^{Di} C(D,j)` (UDL p.66-67, eq. 4.17, in the notes). General bound 2^D (Montufar 2014) (UDL p.66).
- `[from source]` The book warns that more regions is not automatically better: they have symmetries and dependencies; they only help if the true function has those symmetries or is a composition of simple functions (UDL p.64).
- `[from source]` Depth efficiency (functions that require exponentially larger shallow networks) exists in theorems (Telgarsky 2016; Eldan-Shamir 2016), but it is "not clear" that real-world functions are like that (UDL p.64, p.67). There is also width efficiency (Lu 2017; Vardi 2022) (UDL p.67).
- `[from source]` For large, structured inputs (images with ~10^6 pixels), local-to-global processing over several layers is needed (UDL p.64-65); moderately deep networks are easier to train and generalize better, a phenomenon "not well understood" (UDL p.65).
- `[from source]` The term "deep learning" is from Dechter (1986); the modern era began with Krizhevsky et al. (2012) through four combined factors: more data, more processing power, ReLU and SGD (UDL p.66).
- `[from source]` Universal theorem in the depth version (Lu 2017): a ReLU network with at least Di+4 units per layer approximates integrable functions given a sufficient number of layers (UDL p.67).

## 2. Universality in NNDL: visual proof

`[from source]` Statement: a network with one hidden layer approximates any continuous function; with caveats: (a) approximation, not equality (|g(x)−f(x)|<ε for all x with enough neurons) and (b) continuous functions only (NNDL p.187-191). The original proof is by Cybenko (1989) and Hornik-Stinchcombe-White (1989) (NNDL p.188, note). The chapter's proof uses two hidden layers (NNDL p.191).

Steps (NNDL p.191-217):
1. With a large weight the sigmoid neuron becomes a step; the position is `s = −b/w` (NNDL p.194); `b = −ws` (NNDL p.195).
2. Two step-neurons with output weights `+h` and `−h` form a bump of height h (NNDL p.196).
3. N pairs form N bumps: a lookup table; the target for the weighted output of the hidden layer is `σ⁻¹∘f(x)` and the network output is `σ(Σ w a + b)` (NNDL p.198-201). Numerical example: `w = 1000`, `b = −ws` (e.g., s=0.2 → b=−200) and output bias 0 (NNDL p.202-203). Chapter target: `f(x) = 0.2 + 0.4x² + 0.3x sin(15x) + 0.05 cos(50x)` (NNDL p.200, checked by render); p.203 rewrites it without the factor x in the third term (`0.3 sin(15x)`), an internal inconsistency in the book (checked by render).
4. Several inputs: step in x or y with a large weight; a bump in x and a bump in y added together form a "tower with plateau"; a neuron with bias ≈ −3h/2 and a large weight makes the tower (NNDL p.203-210). For n inputs the output bias is `(−m + 1/2)h` with m = number of variables in the tower (NNDL p.211-212; 3-variable example: −5h/2).
5. Vector-valued functions: networks glued together, one per component (NNDL p.212).
6. Other activations: distinct limits at ±∞ suffice; ReLU and linear activation do not meet the argument's conditions (exercises, NNDL p.213-214).
7. Failure windows of the steps: sum M shifted approximations of `σ⁻¹∘f/M` (NNDL p.214-217).

NNDL conclusion: universality answers "is it computable?" with "yes" and shifts the question to "what is the best way to compute"; the case for deep networks is practical and hierarchical (abstractions) (NNDL p.217-218). This is compatible with UDL p.64-65 and p.417-418 (ch.20).

## 3. Motivation for depth in NNDL ch.5

- `[from source]` Shallow Boolean circuits require exponentially more gates for certain functions (parity) (NNDL p.220); theoretical results on the response regions of deep networks (Pascanu-Montúfar-Bengio 2014) (NNDL p.222).
- `[from source]` Hierarchical hypothesis: the first layer recognizes edges, the second more complex shapes, etc. (NNDL p.221; also NNDL p.54-57).
- `[from source]` Experiment: [784,30,10]: 96.48%; [784,30,30,10]: 96.90%; more layers of 30 do not help (96.57% and 96.53%) because of unstable gradients (NNDL p.223-224); see `05-inicializacao-e-gradientes-instaveis.md`.

## 4. Difference in approach (summary; details in `comparacao-udl-nndl.md`)
- UDL counts linear regions for ReLU and justifies depth by capacity per parameter and by induction; NNDL uses sigmoid steps to prove approximation and then justifies depth by hierarchy and by the training failure of shallow networks.
- UDL cites Cybenko/Hornik (p.52) — NNDL p.188 does too; the two agree on the one-hidden-layer version.
- `[extrapolation]` Post-2023 results on expressivity/depth are not in the collection.

## 5. Script
`python -I scripts/dl_calc.py regions --D 10 --K 5` (161,051 and 471, UDL p.65) · `python -I scripts/dl_nets.py universality` (reconstructs NNDL's bump network and shows the error decreasing with N; the number of neurons and the maximum error are OUR products, not the book's; the book uses N=5 and an interactive game with a mean-deviation goal, NNDL p.200-201).

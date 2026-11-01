# 04 — Optimization (GD, SGD, momentum, Adam) and backpropagation

Sources: UDL ch.6-7 (PDF p.91-131), NNDL ch.1 (p.28-38), ch.2 (p.58-84) and ch.3 (p.171-183). Read in full (UDL: body and notes; NNDL: body; problems only skimmed).

## 1. Gradient descent and SGD (UDL)

- `[from source]` Training = repeat: compute gradients and adjust parameters; `φ ← φ − α ∂L/∂φ` (UDL p.91-92, eq. 6.3). One can use a fixed α ("learning rate") or line search (UDL p.92); stop when the gradient is small (UDL p.92).
- `[from source]` Linear regression has a convex loss (single minimum); networks have non-convex losses with local minima and saddle points; an example with the Gabor model (2 parameters) shows that the fate of GD depends on the starting point; the global minimum in the example has loss 0.64 (UDL p.94-96, eq. 6.8; fig. 6.4).
- `[from source]` SGD: at each iteration a minibatch `B_t` is used without replacement: `φ_{t+1} = φ_t − α Σ_{i∈B_t} ∂ℓ_i/∂φ` (UDL p.97-99, eq. 6.10). Epoch = one pass through the dataset; batch = the whole dataset is equivalent to GD (UDL p.99). Properties: improves the fit to a subset at each step, lower cost, can escape local minima and saddle points, and there is evidence that SGD finds solutions that generalize well (UDL p.99-100). A decreasing learning-rate schedule is used (UDL p.100).
- `[from source]` Momentum: `m ← β m + (1−β) Σ ∂ℓ/∂φ; φ ← φ − α m` (UDL p.100, eq. 6.11); Nesterov computes the gradient at the predicted point (UDL p.101-102, eq. 6.12).
- `[from source]` Adam: m and v (smoothed gradient and gradient²) with bias correction `m̃ = m/(1−β^{t+1})`, `ṽ = v/(1−γ^{t+1})` and `φ ← φ − α m̃/(√ṽ + ε)` (UDL p.102-104, eq. 6.13-6.18). Without momentum the "normalized" version moves a fixed distance α per coordinate and oscillates around the minimum (UDL p.102). Adam is less sensitive to the initial rate and compensates for different gradient magnitudes per layer (UDL p.104).
- `[from source]` Training-algorithm hyperparameters: algorithm, batch size, schedule and coefficients; "more art than science" (UDL p.105).
- Notes `[from source]`: GD is from Cauchy (1847) and SGD from Robbins-Monro (1951); Newton uses the inverse Hessian (infeasible for networks); AdaGrad, RMSProp, AdaDelta, AMSGrad, YOGI; learning-rate warm-up (UDL p.105-107); SGD is a special case of Adam with β=γ=0 (UDL p.108); AdamW improves Adam with L2 (Loshchilov-Hutter 2019) (UDL p.108); the SGD×Adam discussion is inconclusive (UDL p.108) (UDL p.105-108).

## 2. Backpropagation in UDL (ch.7)

- `[from source]` Two observations: (1) the effect of a weight is proportional to the activation of the source unit, so the forward pass stores the activations; (2) an effect propagates through the following layers, so derivatives are reused by computing from back to front (UDL p.111-114).
- `[from source]` Toy example: `f = β3 + ω3 cos[β2 + ω2 exp[β1 + ω1 sin[β0 + ω0 x]]]` with 8 parameters (UDL p.114, eq. 7.5); forward in steps `f0 … f3` (eq. 7.8); `∂ℓ/∂f3 = 2(f3 − y)`, `∂fk/∂βk = 1`, `∂fk/∂ωk = hk` (UDL p.115-117).
- `[from source]` Vector version for a network with ReLU (UDL p.117-120): forward `f0 = β0 + Ω0 x`, `hk = a[f_{k−1}]`, `fk = βk + Ωk hk`; backward: `∂ℓ/∂βk = ∂ℓ/∂fk`, `∂ℓ/∂Ωk = (∂ℓ/∂fk) hkᵀ`, `∂ℓ/∂f_{k−1} = I[f_{k−1}>0] ⊙ (Ωkᵀ ∂ℓ/∂fk)` (eq. 7.24); the batch gradient is the sum over examples. It is time-efficient (multiplications by Ω and Ωᵀ) but not memory-efficient (stores the activations) (UDL p.120).
- `[from source]` Algorithmic differentiation (PyTorch, TensorFlow), tensors with a batch dimension and arbitrary acyclic computational graphs (UDL p.120-121); minimal PyTorch code: `loss.backward()` hides the backprop (UDL p.125-126).
- `[from source]` Discrepancy in the book: the text on p.125 says the initial learning rate in the fig. 7.8 code is 0.01; the code printed on p.126 uses `lr = 0.1` (checked in the text of both pages).
- Notes `[from source]`: repeated discovery of backprop (Werbos 1974; Bryson 1979; LeCun 1985; Parker 1985) and popularization by Rumelhart et al. 1985-86 (UDL p.127); reduce memory with gradient checkpointing (recompute activations; cost: forward twice), micro-batching and reversible networks; distributed training: data parallelism (synchronous/Hogwild!), pipeline and tensor parallelism (UDL p.128); 1 trillion parameters on 3,072 GPUs (UDL p.128) `[DATED]`.

## 3. Backpropagation in NNDL (ch.2): the four equations

`[from source]` (equations checked by render on p.66-68)
- Notation: `w^l_{jk}` connects the k-th neuron of layer l−1 to the j-th of layer l; `a^l = σ(w^l a^{l−1} + b^l)`; weighted input `z^l = w^l a^{l−1} + b^l` (NNDL p.59-61, eq. 23-25).
- Assumptions about the cost: average over examples (`C = (1/n) Σ C_x`) and function of the network outputs (NNDL p.62-63). Hadamard product `s ⊙ t` (NNDL p.63-64).
- Error `δ^l_j ≡ ∂C/∂z^l_j` (NNDL p.64-65, eq. 29).
- BP1: `δ^L_j = ∂C/∂a^L_j · σ'(z^L_j)`; in matrix form `δ^L = ∇_a C ⊙ σ'(z^L)`; for the quadratic cost `δ^L = (a^L − y) ⊙ σ'(z^L)` (NNDL p.66-67).
- BP2: `δ^l = ((w^{l+1})ᵀ δ^{l+1}) ⊙ σ'(z^l)` (NNDL p.67).
- BP3: `∂C/∂b^l_j = δ^l_j`. BP4: `∂C/∂w^l_{jk} = a^{l−1}_k δ^l_j` (NNDL p.68).
- Consequences: weights coming out of low-activation neurons learn slowly; a saturated output (σ'≈0) learns slowly; BP holds for any activation (NNDL p.68-69).
- Algorithm: input → feedforward → output error → backpropagate → output (NNDL p.73); mini-batch version `w → w − (η/m) Σ_x δ^{x,l} (a^{x,l−1})ᵀ` and `b → b − (η/m) Σ_x δ^{x,l}` (NNDL p.74).
- Code (negative indexing on the layers) (NNDL p.75-76); `cost_derivative = a − y`, `sigmoid_prime = σ(1−σ)` (NNDL p.46, p.76).
- Efficiency: by finite differences `[C(w+εe_j) − C(w)]/ε` it would take "a million and one" passes for a million weights; backprop costs about two passes (one forward and one backward) (NNDL p.77-78, eq. 46). Justification: matmul by W in the forward pass and by Wᵀ in the backward pass (note, NNDL p.78).
- Paths view: ∂C/∂w is the sum, over all paths, of the product of the partial rates (NNDL p.79-83, eq. 47-53); the short proof comes from using `z` instead of `a` as intermediate variables (NNDL p.83 note).

`[inference]` UDL and NNDL describe the SAME algorithm: UDL eq. 7.24 with ReLU and linear output = NNDL BP1-BP4 with σ'; `∂ℓ/∂fk` (UDL) = `δ^l` (NNDL); `hk` = `a^l`; `fk` = `z^l`. Checked numerically in `dl_nets.py backprop-check` (error ~1e-10 against finite differences).

## 4. SGD variations in NNDL (ch.3)
- Hessian: `Δw = −H⁻¹ ∇C` (NNDL p.174-175, eq. 106) is impractical (with 10^7 weights the Hessian would have 10^14 entries, NNDL p.175).
- Momentum: `v → v' = μ v − η∇C`, `w → w' = w + v'` (NNDL p.176, eq. 107-108, checked by render); μ=1 is frictionless, μ=0 is the usual GD; the name "momentum coefficient" is poorly chosen, since μ is closer to friction (NNDL p.177-178). `[inference]` Equivalent to UDL's momentum with `μ = β` and `η = α(1−β)`, `v = −α m` (verified numerically: `dl_calc.py momentum-equiv`).
- Others: conjugate gradient, BFGS, L-BFGS, Nesterov (NNDL p.178). For most problems SGD with momentum works (NNDL p.178-179).

## 5. Decisions
- Trained and the training loss does not fall: check η (NNDL p.162-164: estimate the threshold of η using the training cost), initialization (`05-...`), saturation (cross-entropy, `03-...`).
- Adam vs SGD: there is no verdict in the collection; with careful hyperparameter search the difference disappears (UDL p.108).
- Memory: if it does not fit, gradient checkpointing (UDL p.128).

# 05 — Weight initialization and unstable gradients

Sources: UDL ch.7.5 (PDF p.121-125, notes p.127-128), UDL ch.11 (p.200-208), NNDL ch.3 initialization (p.139-146) and NNDL ch.5 (p.219-239). Read in full.

## 1. Initialization in UDL

- `[from source]` With biases 0 and weights `N(0, σ²Ω)`, if σ² is too small the magnitudes of the pre-activations shrink from layer to layer; if too large, they grow; floating-point numbers can overflow or underflow, and the same holds for the gradients (vanishing/exploding) (UDL p.122).
- `[from source]` Analysis for ReLU: `E[f'_i] = 0` (eq. 7.28), `σ²_{f'} = σ²Ω Σ_j E[h_j²]` (eq. 7.29) and, since half of the pre-activations are clipped, `E[h_j²] = σ²_f/2`, hence `σ²_{f'} = ½ D_h σ²Ω σ²_f` (eq. 7.30). To keep the variance in the forward pass: **He initialization** `σ²Ω = 2/D_h` (D_h = dimension of the source layer) (UDL p.123-124, eq. 7.31).
- `[from source]` Backward: `σ²Ω = 2/D_{h'}` (dimension of the destination layer) (UDL p.124-125, eq. 7.32); compromise for non-square matrices: `σ²Ω = 4/(D_h + D_{h'})` (UDL p.125, eq. 7.33).
- `[from source]` Fig. 7.7: network with 50 layers, D_h=100, σ²Ω ∈ {0.001; 0.01; 0.02; 0.1; 1.0}: only 0.02 (=2/100) keeps the variance stable in activations and gradients (UDL p.124). `[checked in dl_calc.py var-prop]`: per-layer factor = ½·100·σ² (0.05; 0.5; 1; 5; 50).
- Notes `[from source]` (UDL p.127-128): He (2015) follows from Glorot/Xavier (2010), which "does not consider the effect of the ReLU" and differs by a factor of 2; LeCun et al. (2012) proposed essentially the same for sigmoids; SELU, LSUV, GradInit, ActNorm, BatchNorm; specific initializations (Fixup, T-Fixup, DT-Fixup).

## 2. Initialization in NNDL

- `[from source]` The problem with N(0,1) initialization (NNDL p.139-141): with 1,000 input neurons, half connected, the weighted sum `z = Σ w x + b` involves 500 weights + 1 bias = 501 normals, so `z` has standard deviation `√501 ≈ 22.4` — very wide; the hidden neuron saturates (σ(z) near 0 or 1) and learns slowly. Cross-entropy does not solve the saturation of hidden neurons (NNDL p.140-141).
- `[from source]` Solution: a neuron's input weights ~ `N(0, 1/n_in)` (deviation `1/√n_in`) and biases ~ `N(0,1)`; then `z` has deviation `√(3/2) ≈ 1.22` (NNDL p.141, same situation; exercise on p.142). Biases can even be all 0 (NNDL p.142). `[checked in dl_calc.py sum-var]`.
- `[from source]` MNIST result ([784,30,10], η=0.1, λ=5.0, m=10): both initializations reach >96%, but the new one reaches ~93% already after epoch 1 (the old one <87%) (NNDL p.143); with 100 hidden units the same; it only speeds up learning in this case; the author announces (citing "Chapter 4", a numbering that does not match this PDF's) later examples in which the final performance also improves with `1/√n_in` (NNDL p.144). The `network2.py` code: `np.random.randn(y,x)/np.sqrt(x)` (NNDL p.146, p.150).
- `[from source]` Documented error in the book itself: in the November 2016 note on the `network3.py` code, `FullyConnectedLayer` uses `scale=np.sqrt(1.0/n_out)` when the ch.3 arguments call for `1/n_in`; the author did not rerun the examples (NNDL p.268). Softmax: initial weights and biases zero (NNDL p.270).
- `[from source]` Link with regularization: with the decay `(1−ηλ/n)` the large initial weights shrink by a factor `exp(−ηλ/m)` per epoch (exercise, NNDL p.145).

## 3. NNDL ch.5: vanishing or exploding gradient

- `[from source]` Network with 1 neuron per layer: `∂C/∂b1 = σ'(z1) w2 σ'(z2) w3 σ'(z3) w4 σ'(z4) ∂C/∂a4` (NNDL p.230-233, eq. 114-122, derived step by step). `σ'(0)=1/4` is the maximum (NNDL p.233); with Gaussian initialization |w|<1, so `|w_j σ'(z_j)| < 1/4`, and the gradient of the early layers is at least 16 times smaller than that of the layers two positions ahead (NNDL p.233-234).
- `[from source]` Explosion: if `w=100` and the biases make `z=0`, each term is worth `100·1/4 = 25` (NNDL p.235). Conclusion: the fundamental problem is the **instability** of the gradient (product of many terms), not just vanishing (NNDL p.235). With sigmoids the gradient usually vanishes; avoiding it requires `|wσ'(wa+b)| ≥ 1`, which requires |w|≥4 and an input in a narrow window (maximum width ≈0.45 at |w|≈6.9, problem, NNDL p.235-236). `[checked in dl_calc.py sigmoid-chain]` for the product 25·25·25.
- `[from source]` General case: `δ^l = Σ'(z^l)(w^{l+1})ᵀ Σ'(z^{l+1}) (w^{l+2})ᵀ … Σ'(z^L) ∇_a C`, with `Σ'` diagonal and entries ≤ 1/4 (NNDL p.237, eq. 124).
- `[from source]` Empirical measurement: ‖δ‖ per layer (learning speed): [784,30,30,10]: layer 1 = 0.07, layer 2 = 0.31; [784,30,30,30,10]: 0.012; 0.060; 0.283; with 4 hidden: 0.003; 0.017; 0.070; 0.285 (NNDL p.227); the first layer learns ~100× slower than the last (NNDL p.229). Experiment: batch GD with 1,000 images for 500 epochs (NNDL p.228).
- `[from source]` Other obstacles: sigmoids saturate the last hidden layer (Glorot-Bengio 2010) and initialization/momentum matter (Sutskever et al. 2013) (NNDL p.238).

## 4. UDL ch.11: what residuals change

See `07-cnn-e-residuais.md`. Summary `[from source]`: with He init and residual blocks the forward variance doubles with each block (exponential growth) (UDL p.206); solution: `1/√2` or BatchNorm, which lets the variance grow linearly (UDL p.206-208). "Shattered gradients" is the hypothesis for why deep sequential networks get worse (UDL p.201-203).

## 5. Decision rules
1. Network with ReLU: He (`2/D_h`), biases 0 (UDL p.124). With sigmoid (NNDL): `1/√n_in` (NNDL p.141).
2. If the loss does not fall in the first epochs, check the variance of the activations per layer (UDL fig. 7.7, p.124) and saturation (NNDL p.140-141).
3. `[inference]` NNDL's rule (`1/n_in`) and UDL's (`2/D_h`) differ by a factor of 2 because of the ReLU (UDL p.127: Glorot ignores the ReLU, hence the factor 2).
4. `[extrapolation]` Initializations for modern transformers are not in the collection beyond the mention of T-Fixup/DT-Fixup (UDL p.128).

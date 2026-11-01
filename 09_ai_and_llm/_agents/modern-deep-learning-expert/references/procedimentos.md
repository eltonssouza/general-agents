# Procedures (step by step, derived from the books)

Labels: `[from source]` the step is on the pages; `[inference]` our combination of steps from the books. Pages = PDF. Scripts in `scripts/` (run with `python -I`).

## P1. Choose the loss function for a task (UDL p.74)
1. Identify the domain of `y`: real, binary, K classes, count, direction, ranking... (UDL p.84, fig. 5.11).
2. Choose the distribution (normal, Bernoulli, categorical, Poisson, von Mises...).
3. Have the network predict the distribution's parameters, with transformations that guarantee the domain (sigmoid for λ∈[0,1]; softmax for K classes; square for positive variance) (UDL p.78-82).
4. Minimize the NLL; at inference, return the distribution or its maximum.
5. If the output is sigmoid or softmax, do **not** use least squares (slowness due to `σ'`, NNDL p.88-89); use BCE/cross-entropy (NNDL p.89-91).
6. If the error has heavy tails: Laplace/t (UDL p.87); if multimodal: mixture (UDL p.84). `[inference]`

## P2. Check backprop (gradient check) `[from source: NNDL p.78 eq.46 (finite differences)]`
1. Run `python -I scripts/dl_nets.py backprop-check --act sigmoid --arch 3,4,2` (BP1-BP4) and `--act relu` (UDL eq. 7.24).
2. The expected maximum absolute error is of the order of 1e-9 to 1e-11.
3. If it fails: check the transpose of `Ω` (UDL p.119, eq. 7.20), the mask `I[f>0]` (UDL p.119) and the Hadamard product with `σ'` (NNDL p.67). `[inference]`

## P3. Diagnose training that does not converge `[inference from NNDL p.156-166 and UDL p.121-125, p.201-208]`
1. Does the training loss fall? If not: reduce η by factors of 10 and compare (NNDL p.162-164).
2. If, with the right η, learning is very slow in the early layers: measure `||δ||` per layer (NNDL p.225-229) and check initialization and saturation (NNDL p.140; UDL p.124).
3. Deep sequential network worse than the shallow one in training and test: use residual connections + normalization (UDL p.200-208).
4. Sigmoid/softmax output with quadratic cost: switch to cross-entropy (NNDL p.89-91).
5. Transformers: use warm-up and Adam (UDL p.251).
6. NaN loss: initialization variance/η too high (UDL p.122); exploding gradients (UDL p.206).

## P4. Diagnose generalization `[UDL p.132-150; NNDL p.107-115]`
1. Split training/validation/test; choose hyperparameters on validation, measure on test only at the end (NNDL p.112-113; UDL p.146-147).
2. Training ≈ perfect and test poor → overfitting; options: more data, augmentation, L2, dropout, early stopping, ensemble (UDL p.159-168; NNDL p.114-135).
3. Test and training both poor → high bias: more capacity/better architecture (UDL p.139).
4. Test error worsens with more capacity near #parameters≈#data: critical region of double descent; consider going beyond (more capacity) or reducing (UDL p.143).
5. Distribution shifts in production: covariate/prior/concept shift and monitoring (UDL p.149).

## P5. Estimate parameters and regions (`dl_calc.py`)
- MLP: `mlp-params --sizes ...` (UDL p.62-63). Conv: `conv-params` and `conv-out` (UDL p.181-184; NNDL p.248). Regions: `regions` (UDL p.64-67). Transformer: `xfmr-params` (UDL p.233, p.238; `[inference]`).

## P6. Choose initialization `[UDL p.124-125; NNDL p.141]`
ReLU: He `2/D_h`, biases 0; sigmoid (NNDL): `1/√n_in`; final softmax: zeros (NNDL p.270) or small values. Check the variance of the activations with `var-prop`.

## P7. Configure regularization `[inference]`
1. Start with more data/augmentation (NNDL p.114, p.134-135; UDL p.166-168).
2. Dropout only on the fully connected layers, not on the convolutional ones, according to NNDL (p.264-265).
3. L2: `λ` scales with `n` to keep the factor `1−ηλ/n` (NNDL p.119, p.133). In Adam prefer decoupled weight decay (AdamW) (UDL p.169-170).
4. Early stopping with patience of 10 epochs (NNDL p.165-166).
5. Label smoothing in classification (UDL p.163-164).

## P8. Choose architecture by data type `[UDL p.64-65, p.175, p.221-222, p.254]`
Tabular → MLP (UDL p.16); image → CNN/ResNet/ViT (UDL p.175, p.200-209, p.228-232); text/sequence → transformer (UDL p.221); graph → GNN (UDL p.254); generate images → diffusion (UDL p.362) or GAN (UDL p.289); exact density → flows (UDL p.331); latent with encoder → VAE (UDL p.340); sequential decision → RL (UDL p.387).

## P9. Evaluate a generative model `[UDL p.284-287]`
1. If probabilistic: test log-likelihood (exact only in flows; bound in VAE/diffusion).
2. Images: FID/IS and manifold precision/recall, noting that they depend on a classifier (UDL p.285-287).
3. Check coverage (mode dropping, UDL p.294) and diversity (UDL p.314).

## P10. Train a GAN carefully `[UDL p.292-302]`
Wasserstein + gradient penalty, progressive growing, minibatch discrimination, truncation; BatchNorm/leaky ReLU in D (DCGAN) (UDL p.293, p.297-302).

## P11. Train/evaluate diffusion `[UDL p.376-380]`
Loss `||g_t[√α_t x + √(1−α_t) ε] − ε||²`; U-Net with time; sampling with DDIM/50 steps; guidance; `dl_calc.py diffusion` verifies the schedule.

## P12. Ethical risk review `[UDL p.434-448]`
List the phases of bias (problem, data, model/validation, deployment), affected parties, factors of malicious use and impact (privacy, environment, IP); ask whether the problem is technical or social (UDL p.447-448).

## P13. Answer "two books say different things"
Open `comparacao-udl-nndl.md`; cite the page from both; state the convention explicitly (sum × mean, α × η, tokens in columns); never declare equivalence without the verification script or page.

## P14. Answer about an LLM/modern topic outside the collection
`python -I scripts/dl_lookup.py TERM`; if NOT COVERED, say so, give `[extrapolation]` only if the user asks and recommend a current source.

# UDL × NNDL comparison: approach, notation and discrepancies (with pages)

Pages = PDF. UDL: Simon Prince, *Understanding Deep Learning* (MIT Press, 2023; PDF of 541 pages, version of 15 Feb 2024 according to the cover, UDL p.1). NNDL: Michael Nielsen, *Neural Networks and Deep Learning* (online book, last update Dec 2019 in the footer, NNDL p.2; text year 2015). NNDL predates UDL by ~8 years and ends with convolutional networks and mentions of RNN/DBN; UDL covers transformers, diffusion, RL and ethics.

## 1. Roles of the two books
- UDL = main source (network mathematics, losses, training, regularization, CNN, ResNet, transformers, graphs, GAN, flows, VAE, diffusion, RL, ethics).
- NNDL = didactic introduction (perceptron, sigmoid, the 4 backprop equations, cross-entropy, overfitting, initialization, universality, gradient instability, CNN on MNIST with code).

## 2. Notation table
| Concept | UDL | NNDL | Where |
|---|---|---|---|
| Parameters | `φ` (generic); weights `Ω_k` (matrix), biases `β_k` | weights `w^l_{jk}` (matrix `w^l`), biases `b^l_j` | UDL p.62-63, p.450; NNDL p.59-61 |
| Pre-activation / activation | `f_k` / `h_k` (`h_k = a[f_{k−1}]`) | `z^l` (weighted input) / `a^l` | UDL p.117-118; NNDL p.60-61 |
| Activation function | `a[•]`; book default: ReLU | `σ` (sigmoid); ReLU only in ch.3/6 | UDL p.39; NNDL p.14, p.181-182, p.258 |
| Order of the weight indices | matrix `Ω_k` of size `D_{k+1} × D_k` (output × input) | `w^l_{jk}`: j = destination neuron, k = source (note says it is a "quirk" to write `w a`) | UDL p.63; NNDL p.60-61 |
| Loss / cost | `L[φ]`, per-example loss `ℓ_i`; "loss", "cost", "objective" treated as synonyms; loss **sum** | `C`, `C_x`; cost **mean** `(1/n)Σ C_x`; quadratic `1/(2n)` | UDL p.32, p.37, p.74; NNDL p.26, p.62 |
| Learning rate | `α` | `η` | UDL p.92; NNDL p.31-33 |
| Mini-batch | set of indices `B_t` | `m` examples, `X1..Xm` | UDL p.99; NNDL p.36 |
| L2 regularization | `λ Σ φ²` over summed loss | `(λ/2n) Σ w²` over mean cost | UDL p.154; NNDL p.115 |
| Layers | `K` hidden layers; `Ω_0..Ω_K` | `L` total layers; layer 1 = input | UDL p.62-63; NNDL p.59-60, p.73 |
| Per-layer error | `∂ℓ/∂f_k` | `δ^l ≡ ∂C/∂z^l` | UDL p.119-120; NNDL p.64-65 |
| Attention/tokens | tokens in the COLUMNS of `X ∈ R^{D×N}`; `V · Softmax[KᵀQ]` | (does not exist) | UDL p.226-227 |
| Model distribution | `Pr(y|x,φ)`; second distribution `q(•)` | (does not use the probabilistic view; only "log-likelihood" with softmax) | UDL p.451; NNDL p.104 |
| Update rule | `←` is assignment | `→` ("w → w'") | UDL p.452; NNDL p.32 |
| Variable convention | variables in Roman letters; parameters in Greek (exception: policy `π`) | usual | UDL p.450 |

## 3. Differences in approach and discrepancies
1. **"MLP" terminology**: UDL uses MLP for any network with ≥1 hidden layer (UDL p.49); NNDL says the term is confusing for networks of sigmoids and avoids it (NNDL p.18).
2. **Loss and probability**: UDL derives least squares and cross-entropy from the maximum-likelihood criterion with output distributions (UDL p.70-86); NNDL introduces cross-entropy to solve the saturation of `σ'` and derives it by requiring `∂C/∂w = x(a−y)` (NNDL p.88-100). Mathematically they coincide for BCE and softmax.
3. **Mean × sum**: NNDL's cost is the mean; UDL's loss is the sum. An SGD step is identical if `α = η/n` and `λ_UDL = λ_NNDL/2` `[inference; dl_calc.py l2-equiv]`. Be careful when comparing η and λ between the books.
4. **"Weight decay"**: NNDL calls L2 regularization "weight decay" (NNDL p.115-116); UDL, in the notes, says this is imprecise — weight decay is `φ ← (1−λ')φ − α ∂L/∂φ` (eq. 9.13), equivalent to L2 only in plain SGD with `λ = λ'/(2α)` and different in Adam (hence AdamW) (UDL p.169-170); in the main text UDL itself uses "weight decay" for L2 on the weights (UDL p.154).
5. **Momentum**: UDL `m ← βm + (1−β)g; φ ← φ − αm` (eq. 6.11, UDL p.100); NNDL `v ← μv − η∇C; w ← w + v` (NNDL p.176, render). They are equivalent with `μ = β`, `η = α(1−β)`, `v = −αm` `[inference; dl_calc.py momentum-equiv]`. UDL also describes Adam (p.102-104), which NNDL does not have.
6. **Initialization**: NNDL uses weights `N(0, 1/n_in)` and biases `N(0,1)` for sigmoids (NNDL p.141); UDL uses He `σ² = 2/D_h` with biases 0 for ReLU (UDL p.124) and reports that Glorot differs from He by a factor of 2 because it ignores the ReLU (UDL p.127). NNDL admits an error in its own ch.6 code (`1/n_out` instead of `1/n_in`, NNDL p.268).
7. **Dropout at test time**: UDL "multiplies the weights by 1 − p" (UDL p.162); NNDL "halves the output weights of the hidden units" (p=0.5) (NNDL p.131). Same rule for p=0.5.
8. **Preferred activation**: NNDL uses sigmoids almost everywhere and only adopts ReLU in ch.6 (NNDL p.258-259); UDL adopts ReLU as the default (UDL p.39) and cites the GELU/SiLU/Swish family (UDL p.51-52).
9. **Universality**: UDL proves it via linear regions with ReLU (UDL p.43-44) and cites Cybenko 1989 and Hornik 1991 in the notes (UDL p.52); NNDL gives a visual proof with sigmoids (steps) and two hidden layers, and speaks of only one (NNDL p.188-191).
10. **Vanishing gradient**: NNDL derives the product `Π w σ'` and shows that `σ' ≤ 1/4` (NNDL p.230-235); UDL links the phenomenon to "shattered gradients" in sequential networks and to residuals (UDL p.201-203, p.206) and describes the explosion of variance in residual blocks (UDL p.206). Complementary concepts.
11. **AlexNet**: UDL "top-5 error 16.4% and top-1 38.1%" (UDL p.190); NNDL "top-5 accuracy 84.7% and top-1 63.3%" (NNDL p.283). 100−84.7 = 15.3 ≠ 16.4; the texts do not explain the difference; do not claim they are the same metric `[inference]`.
12. **Parameter counting**: NNDL: 784→30→10 has 23,860 (NNDL p.107; checks); UDL: MNIST-1D conv 2,050 × FC 59,065 (UDL p.181; checks). UDL arithmetic divergences: p.416 (177,201 only with scalar output), p.418 (15,139 vs 15,319) and p.427 (198,450 vs 199,210) — see `casos-e-antipadroes.md`.
13. **MNIST data**: NNDL splits 50,000 training + 10,000 validation (+ 10,000 test) (NNDL p.39); UDL uses the synthetic MNIST-1D (4,000 training) (UDL p.132). Accuracy results from one cannot be compared with those of the other.
14. **Hyperparameters**: NNDL gives a practical workflow (NNDL p.156-173); UDL describes search methods (UDL p.146-150) but not a step-by-step.
15. **Ethics and time scope**: NNDL (2015) ends with an opinion on the future of AI (NNDL p.296-303); UDL (2023) has an ethics chapter with alignment, bias, misuse (UDL p.434-449).

## 4. When to prefer each source
- Understanding BP1-BP4 and seeing minimal code: NNDL (p.58-84).
- Probabilistic losses, implicit regularization, transformers, diffusion: UDL.
- Contrast of eras: cite both and label NNDL `[DATED]`.

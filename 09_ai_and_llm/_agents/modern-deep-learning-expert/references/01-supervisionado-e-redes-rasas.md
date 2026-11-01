# 01 — Supervised learning, perceptron, sigmoid and shallow networks

Sources: UDL ch.1-3 (PDF p.15-54) and NNDL ch.1 (PDF p.3-57). Pages = PDF (printed UDL = PDF − 14). Read in full (body and notes of UDL ch.1-3; NNDL ch.1). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. The supervised framework

- `[from source]` The book separates AI (systems that simulate intelligent behavior) from machine learning (fitting mathematical models to data) and says ML has become "almost synonymous" with AI, incorrectly; deep learning = fitting deep networks (UDL p.15).
- `[from source]` Three areas: supervised, unsupervised and reinforcement learning; the book organizes the chapters in that order (UDL p.15, p.29).
- `[from source]` A supervised model = function `y = f[x, φ]`; training = choosing the φ that minimizes a loss `L[φ]` over pairs `{xi, yi}`; testing = measuring on separate data (UDL p.31-32, eq. 2.1-2.3).
- `[from source]` 1D linear regression `y = φ0 + φ1 x` with least-squares loss `Σ(φ0 + φ1 xi − yi)²` illustrates everything (UDL p.32-33, eq. 2.4-2.5). Fig. 2.2 shows losses of 7.07, 10.28 and 0.20 for three lines (UDL p.34).
- `[from source]` Iterative training = initialize randomly and "walk downhill" (gradient); footnote: a closed form exists for the line, but the iterative method applies to models without a closed form (UDL p.36).
- `[from source]` Underfitting (model too simple) and overfitting (describes peculiarities of the training set) already appear here (UDL p.36).
- `[from source]` Terminology note: "loss", "cost" and "objective" are used as synonyms in the book; strictly, loss would be the per-example term and cost the total (UDL p.37).
- `[from source]` Discriminative models (`y = f[x]`) dominate modern ML over generative ones `x = g[y]` because data and flexibility outweigh the built-in prior knowledge (UDL p.37-38).

Problem types (UDL p.16-21): regression (house price), multivariate regression (melting and boiling points), binary classification (positive/negative review), multiclass (music genre, object in the image). Inputs: tabular data (no internal structure), text (variable length; vocabulary of 10,000 in the example), audio (10 s at 44.1 kHz with 16 bits = 441,000 integers), images (2D structure), molecules (graphs) (UDL p.16-18). Structured outputs (segmentation, depth, transcription, translation, text→image) are harder because of ambiguity and because the output has its own "grammar" (UDL p.19-21).

## 2. Perceptron and sigmoid neuron (NNDL)

- `[from source]` Perceptron: binary inputs, weights; output 0 if `Σ wj xj ≤ threshold`, 1 otherwise (NNDL p.6, eq. 1 — checked by render). With bias `b ≡ −threshold`, the rule becomes `w·x + b ≤ 0 → 0` (NNDL p.8, eq. 2).
- `[from source]` Didactic cheese-festival example with weights 6, 2, 2 and threshold 5 (NNDL p.7).
- `[from source]` NAND with weights −2, −2 and bias 3: input 00 gives sum 3 (>0, output 1); input 11 gives −1 (output 0). Since NAND is universal for computation, perceptrons are universal (NNDL p.9-11).
- `[from source]` Problem: small changes in a perceptron's weights can flip the output from 0 to 1, preventing gradual learning; the solution is the sigmoid neuron `σ(z) = 1/(1+e^{−z})`, output `σ(w·x+b)` (NNDL p.12-14, eq. 3-4). Smoothness guarantees `Δoutput ≈ Σ ∂output/∂wj Δwj + ∂output/∂b Δb` (NNDL p.15-16, eq. 5).
- `[from source]` σ is also called the logistic function (note, NNDL p.14).
- `[from source]` Terminology: input layer, hidden layer (means only "neither input nor output"), output layer; networks without loops = feedforward; Nielsen warns that "MLP" is used historically for multilayer networks of sigmoids, but avoids the term (NNDL p.18-19).
- `[from source]` In UDL, "multi-layer perceptron" designates any network with at least one hidden layer (UDL p.49). Difference in term usage; see `comparacao-udl-nndl.md`.

## 3. Shallow network (UDL ch.3)

- `[from source]` Example with 10 parameters: `y = φ0 + φ1 a[θ10 + θ11 x] + φ2 a[θ20 + θ21 x] + φ3 a[θ30 + θ31 x]`, ReLU activation `a[z] = max(0, z)` (UDL p.39, eq. 3.1-3.2).
- `[from source]` With ReLU the network computes a continuous piecewise-linear function: each hidden unit contributes a "joint", and each linear region corresponds to an activation pattern (active/inactive units) (UDL p.41). With 3 units there are up to 4 regions, but only 3 independent slopes (UDL p.41).
- `[from source]` Capacity = number of hidden units; D ReLU units create at most D+1 regions in 1D (UDL p.43, eq. 3.5-3.6).
- `[from source]` Universal approximation theorem: with enough units, a shallow network approximates any continuous function on a compact subset to arbitrary precision (UDL p.43-44; notes p.52 cite Cybenko 1989 for sigmoids and Hornik 1991 for a larger class).
- `[from source]` Several outputs share the same joints (same hidden units), but slopes and heights differ (UDL p.44-45, eq. 3.7-3.8). With 2 inputs, each unit defines a clipped plane and the regions are convex polygons (UDL p.45-47); with Di inputs and Di units one can align hyperplanes with the axes and obtain `2^Di` regions (UDL p.47). The number of regions grows rapidly: with D = 500 and Di = 100, more than 10^107 regions, with 51,001 parameters (UDL p.48 fig. 3.9) [checks: 100·500+500+500+1 = 51,001].
- `[from source]` Zaslavsky bound: at most `Σ_{j=0}^{Di} C(D,j)` regions (UDL p.52, notes).
- `[from source]` Terminology: pre-activation (before the ReLU), activation (after), weights (slopes), biases (intercepts), fully connected network, hidden layer, "neuron" (UDL p.49-50). The book says the connection to biological neurons is "tenuous" (UDL p.50).
- `[from source]` Alternative activation functions cited: sigmoid, tanh, Leaky/Parametric ReLU, SoftPlus, GELU, SiLU, ELU, SELU, Swish `x/(1+exp(−βx))`, HardSwish; the book adopts ReLU in the rest of the text because it makes the linear regions easy to characterize (UDL p.51-52).
- `[from source]` "Dying ReLU" problem: zero derivative for negative inputs can prevent updates of the weights that feed the unit (UDL p.52).
- `[from source]` History: McCulloch-Pitts 1943, Rosenblatt 1958 (perceptron), Minsky-Papert 1969, backpropagation in the 1980s (UDL p.51).
- `[from source]` Linear vs affine: the book adopts the convention of calling both "linear" (UDL p.41 note, p.53).

## 4. Gradient: from ΔC ≈ ∇C·Δv to the update rule (NNDL ch.1)

- `[from source]` Quadratic cost `C(w,b) = (1/2n) Σ_x ||y(x) − a||²` (NNDL p.26, eq. 6; factor 1/(2n) — checked against the text on p.62 and the render of p.66). Justification for using a smooth cost instead of accuracy: the count of correct answers is not smooth in w and b (NNDL p.27).
- `[from source]` Gradient descent: `ΔC ≈ ∇C·Δv`, choose `Δv = −η∇C`, hence `v → v − η∇C` (NNDL p.31-33, eq. 9-11); η must be small enough for the approximation to hold (NNDL p.33); the steepest descent for a fixed step size is `Δv = −η∇C` with `η = ε/||∇C||` (NNDL p.34).
- `[from source]` SGD: estimate `∇C` by a mini-batch of size m: `w → w − (η/m) Σ ∂C_Xj/∂w` (NNDL p.36, eq. 18-21); epoch = a pass through all examples (NNDL p.37). Example: n = 60,000 and m = 10 gives a 6,000× speedup in estimating the gradient (NNDL p.37). Conventions vary (mean vs sum of the cost; scale of η) (NNDL p.37).
- `[from source]` Minimal implementation `network.py` (74 lines): Gaussian weights and biases (mean 0, standard deviation 1), `a' = σ(wa + b)` (NNDL p.40, eq. 22); split 50,000 training + 10,000 validation (NNDL p.39).
- `[from source]` Ch.1 results (all with [784,30,10] unless noted; η=3.0, m=10, 30 epochs): 9,129/10,000 after epoch 0; 95.42% at best (epoch 28: 9,542); [784,100,10] 96.59% (NNDL p.47). With η=0.001 only 1,139/10,000 at epoch 0 and 2,142 at 29; with η=100.0 about 1,009/10,000 (NNDL p.48). Baselines: average brightness 2,225/10,000 (22.25%), standard SVM 9,435/10,000, tuned SVM >98.5%, 2013 record with 9,979/10,000 (NNDL p.51-53). `[DATED]` (2013-2015).
- `[from source]` Final idea of the chapter: deep = two or more hidden layers; since 2006, techniques have emerged for training networks with 5 to 10 hidden layers (NNDL p.56-57). `[DATED]`.

## 5. Where each topic goes
- Loss for any type of output: `03-funcoes-de-perda-e-cross-entropy.md`.
- Training, backprop, initialization: `04-...`, `05-...`.
- Why depth: `02-redes-profundas-e-capacidade.md`.
- Script: `python -I scripts/dl_calc.py mlp-params --sizes 784,30,10` (23,860 parameters, NNDL p.107) and `regions` (UDL p.64).

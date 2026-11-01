# 03 — Loss functions, maximum likelihood, cross-entropy and softmax

Sources: UDL ch.5 (PDF p.70-90) and the cross-entropy and softmax parts of NNDL ch.3 (PDF p.85-106). Read in full (UDL: body and notes; NNDL: body; exercises only skimmed).

## 1. The UDL probabilistic recipe

`[from source]` Instead of the network predicting `y` directly, it computes the parameters θ of a distribution `Pr(y|θ)`; one chooses the φ that maximize the likelihood of the data (UDL p.70-72, eq. 5.1). Explicit assumption: i.i.d. data (independent and identically distributed), eq. 5.2 (UDL p.72). One moves to the log (a sum instead of a product: numerical precision) and to the negative in order to minimize (UDL p.73-74, eq. 5.3-5.4).

Four-step recipe (UDL p.74): (1) choose the distribution over the domain of y; (2) the model predicts one or more of its parameters; (3) minimize the NLL in training; (4) to infer, return the whole distribution or its maximum.

Cases:
- Univariate regression: normal with mean `μ = f[x, φ]` (eq. 5.7-5.8); the least-squares loss `Σ(yi − f[xi,φ])²` follows from independent, normal errors; the constant variance drops out of the argmin (UDL p.75-76, eq. 5.9-5.11). One can learn σ² (eq. 5.13) and, in heteroscedastic regression, use `μ = f1[x,φ]` and `σ² = f2[x,φ]²` (UDL p.77-78, eq. 5.14-5.15).
- Binary classification: Bernoulli with `λ = sig[f[x,φ]]`, `sig[z] = 1/(1+exp[−z])`; loss `Σ −(1−yi) log(1−sig) − yi log sig` ("binary cross-entropy"); decision y=1 if λ>0.5 (UDL p.79-80, eq. 5.16-5.20).
- Multiclass: categorical with softmax `exp[z_k]/Σ exp[z_k']`; loss `−Σ log softmax_{yi}[f[xi,φ]]` (UDL p.81-83, eq. 5.21-5.24).
- Several outputs: assume independence and multiply univariate distributions (sum of NLLs) (UDL p.83-84, eq. 5.25-5.26). The table in fig. 5.11 (UDL p.84) lists: normal, Laplace/t (robust), mixture of Gaussians (multimodal), exponential/gamma, beta, multivariate normal, von Mises (direction), Bernoulli, categorical, Poisson (count) and Plackett-Luce (ranking).
- Cross-entropy: minimizing the KL between the empirical distribution (sum of Dirac deltas at the data) and the model is equivalent to the NLL (UDL p.85-86, eq. 5.27-5.31). Hence "cross-entropy" and "negative log-likelihood" are the same criterion in this book.
- Notes: robust regression with Laplace (MAE → median); quantile (pinball) loss; focal loss for imbalance; listwise Plackett-Luce; non-probabilistic alternatives (SVM hinge, AdaBoost exponential) (UDL p.87-88).

## 2. Cross-entropy in NNDL: the slowdown problem

`[from source]` Toy experiment: neuron with one input, x=1, target y=0; quadratic cost, η=0.15. Initial weights w=0.6 and b=0.9 give output 0.82 and the network learns down to ≈0.09; with w=b=2.0 the initial output is 0.98 and in the first ~150 epochs almost nothing changes (NNDL p.86-88). `[checked in dl_nets.py toy-neuron]` (σ(1.5)=0.8176; σ(4)=0.982; output 0.094 at epoch 300 and ≈0.93 at epoch 150; the book does not say how many epochs the animation has — the number 300 is OURS, merely consistent with "≈0.09").

`[from source]` Origin of the slowness: the derivatives `∂C/∂w = (a−y)σ'(z)x` and `∂C/∂b = (a−y)σ'(z)` have the factor `σ'(z)`, which is small when the neuron saturates (NNDL p.88-89, eq. 55-56).

`[from source]` Cross-entropy for one neuron: `C = −(1/n) Σ_x [y ln a + (1−y) ln(1−a)]` (NNDL p.89, eq. 57); non-negative and → 0 when a≈y (with y∈{0,1}) (NNDL p.90). Gradients: `∂C/∂w_j = (1/n) Σ x_j (σ(z) − y)` and `∂C/∂b = (1/n) Σ (σ(z) − y)` — the factor `σ'(z)` cancels (NNDL p.90-91, eq. 58-62). For several outputs: sum over neurons, eq. 63 (NNDL p.93); the author stresses that the definition of cross-entropy between distributions `−Σ p ln q` is different, because sigmoid activations do not sum to 1 (NNDL p.94). In many layers, the output error is `δ^L = a^L − y` (NNDL p.95-96, eq. 66).

`[from source]` "Cross-entropy is almost always the best choice if the output neurons are sigmoids" (NNDL p.94). Alternative derivation: requiring `∂C/∂w = x(a−y)` and integrating `∂C/∂a = (a−y)/(a(1−a))` gives cross-entropy up to a constant (NNDL p.99-100, eq. 71-77). The information-theory interpretation ("surprise") is only mentioned (NNDL p.100-101).

`[from source]` MNIST results [784,30,10]: cross-entropy 95.49% vs 95.42% from ch.1; with 100 hidden units, 96.82% vs 96.59%; error of 3.41% vs 3.18% (NNDL p.97); the author admits the comparison does not prove superiority, since hyperparameter tuning was minimal (NNDL p.98).

When the quadratic cost is acceptable: if the output neurons are linear, the quadratic cost does not suffer slowdown (`δ^L = a^L − y`) (NNDL p.96, problem).

## 3. Softmax + log-likelihood in NNDL

`[from source]` Softmax layer `a^L_j = e^{z^L_j}/Σ_k e^{z^L_k}` (NNDL p.101, eq. 78); positive outputs summing to 1 (NNDL p.102-103, eq. 79); cost `C = −ln a^L_y` (NNDL p.104, eq. 80); derivatives equal to those of sigmoid + cross-entropy (`a^L_j − y_j`) (NNDL p.105, eq. 81-82; confirmed by the text "same as Eq. 67"). Nielsen uses sigmoid + cross-entropy in ch.3 and softmax + log-likelihood in ch.6 to match the literature (NNDL p.105-106; also p.255).
`[from source]` Problem: softmax with parameter c ("softmax" is a "softened" maximum as c→∞) (NNDL p.106).

## 4. Equivalences and differences UDL × NNDL
- Same mathematics: UDL's NLL for categorical output = NNDL's log-likelihood with softmax; BCE with sigmoid = NNDL's cross-entropy (UDL p.80-83; NNDL p.89-105).
- UDL generalizes: any output distribution (Poisson, von Mises...) and justifies least squares via the normal; NNDL presents cross-entropy as the solution to a practical problem (saturation) and derives it by requiring `∂C/∂w = x(a−y)`.
- `[inference]` In both, "loss" is the NLL; in UDL the loss sums over examples (UDL p.74, eq. 5.6), in NNDL it is the mean (1/n) (NNDL p.89) — this affects the scale of η and λ (see `04-...` and `comparacao-udl-nndl.md`).

## 5. Scripts
`python -I scripts/dl_calc.py xent --logits 2,1,0 --label 0 --binary-z 0 --binary-y 1` · `python -I scripts/dl_nets.py toy-neuron --find-below 0.1` · `... toy-neuron --w 2 --b 2 --cost cross-entropy --eta 0.005`.

# 11. Neural networks and deep learning: what these two books cover (and do not cover)

Source: **ESL ch. 11 (PDF 408-417; read; PDF 418-423 onward, including 11.5.3-11.9 on input scaling, hidden units, examples and Bayesian networks, NOT read)**. The **ISLR 1st edition (2013, 8th printing 2017) has no chapter on neural networks or deep learning** (the table of contents runs from ch. 1 to 10; see `INDEX.md`); this only appears in later editions of ISLR `[extrapolation]`. Convention: PDF page (ESL printed = PDF − 19).

`[DATED]` ESL 2nd ed. was written in 2009: it does not cover modern deep networks (deep convolutional networks, batch normalization, Adam, transformers, etc.). Everything that follows describes the book's **"vanilla" single-hidden-layer neural network**.

## 1. Model
- `[from source]` ESL states that, despite the "hype", neural networks are just non-linear statistical models, similar to *projection pursuit regression* (PPR): f(X) = Σ g_m(ω_mᵀX) (ESL p.409, 411). A single-hidden-layer network is a two-stage model: Z_m = σ(α₀m + α_mᵀX), T_k = β₀k + β_kᵀZ, f_k(X) = g_k(T), with σ a sigmoid and, for classification, *softmax* g_k(T) = e^{T_k}/Σ e^{T_ℓ} (ESL p.411-412); it is PPR with g_m(v) = β_mσ(α₀m + ‖α_m‖·v) (ESL p.413). If σ were the identity, the model would collapse into a linear model (ESL p.413). The Z_m units are "hidden"; the network is a basis expansion **whose parameters are learned from the data** (ESL p.412).
- `[from source]` Number of weights: M(p + 1) + K(M + 1) (11.8); error: sum of squares (regression) or cross-entropy (classification); with softmax and cross-entropy the model is a linear logistic on the hidden units, estimated by maximum likelihood (ESL p.414).

## 2. Fitting and regularization
- `[from source]` The global minimum of R(θ) probably overfits; an explicit penalty or *early stopping* is used (ESL p.414, 417). Gradient descent with the chain rule is **back-propagation**: forward pass and backward pass, with the "errors" δ_ki and s_mi related by (11.15); batch or *online* learning (one observation at a time), one full pass is an epoch; in *online* the learning rate must tend to zero (Robbins-Monro: γ_r → 0, Σγ_r = ∞, Σγ²_r < ∞) (ESL p.415-416). The book notes that back-propagation can be very slow and that pure second-order methods are not attractive (large Hessian) (ESL p.416).
- `[from source]` Cautions: do not initialize the weights at zero (symmetry) nor at large values (ESL p.416-417); *early stopping* shrinks the model toward the linear one and uses a validation set; **weight decay** R(θ) + λJ(θ) with J = Σβ² + Σα² is analogous to ridge (11.16), with λ chosen by CV; "weight elimination" (11.17) shrinks small weights more (ESL p.417).

## 3. Relation to the rest
- `[inference]` For tabular methods, ESL treats networks as one model among several: Table 10.1 (see `13-guia-de-escolha-de-metodo.md`) classifies neural networks as good in predictive power and extraction of linear combinations, but poor in interpretability, robustness to outliers, handling mixed-type data and irrelevant inputs (ESL p.370).

## NOT COVERED (in this ISLR/ESL collection)
CNNs, RNNs, attention/transformers, modern optimizers (Adam), *dropout*, batch normalization, large-scale networks, self-supervised learning, LLMs: **outside the scope** of these two books (see other agents in this folder for LLMs and deep learning). Any claim about this here would be `[extrapolation]`.

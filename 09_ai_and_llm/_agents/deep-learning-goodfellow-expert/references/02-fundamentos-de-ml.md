# 02 · Machine learning fundamentals (DLB ch. 5, PDF p.113-180)

**Coverage:** read p.114-150 and p.166-172. **Not read:** p.151-165 (Bayesian statistics/MAP, SVM, kNN, trees, unsupervised learning such as PCA and k-means) and p.173-180 (smoothness, *manifold learning*). Convention: DLB p.N = PDF page (printed = N − 15).

## Learning, tasks, measure and experience
- `[from source]` (DLB p.114) Mitchell's definition (1997): a program learns from experience **E** with respect to a class of tasks **T** and a performance measure **P** if its performance on T, as measured by P, improves with E. The book does not formalize T, P, E; it describes them intuitively.
- `[from source]` (DLB p.114-118) Tasks: classification, classification with missing inputs (the joint distribution is learned and marginalized; 2ⁿ functions), regression, transcription, translation, structured output, anomaly detection (credit card fraud), synthesis and sampling, imputation, *denoising*, density estimation. An example is a feature vector x ∈ ℝⁿ (p.114).
- `[from source]` (DLB p.118-119) Measures: accuracy, error rate (= expected 0-1 loss); for density, the average log-probability; evaluation is done on a separate test set; choosing the right metric is hard.
- `[from source]` (DLB p.119-121) Unsupervised (learn p(x)) vs supervised (learn p(y|x), with label/target); the division is not formal: the chain rule p(x) = ∏p(xᵢ|x₁..xᵢ₋₁) (eq. 5.1) reduces an unsupervised problem to n supervised ones. Semi-supervised, multi-instance; reinforcement learning is out of scope (p.121). *Design matrix* (Iris: 150 × 4).

## Linear regression as the running example
- `[from source]` (DLB p.122-125) ŷ = wᵀx (eq. 5.3), test MSE (eq. 5.4-5.5), **normal equations** w = (XᵀX)⁻¹Xᵀy (eq. 5.12, p.124); with intercept ŷ = wᵀx + b (affine); the affine "bias" is not the statistical bias (p.125).

## Capacity, overfitting, underfitting
- `[from source]` (DLB p.125-126) Central challenge: generalizing to new inputs. Training error × generalization (test) error; **i.i.d.** assumptions and the generating distribution p_data. The two factors: reduce the training error and reduce the gap between training and test. *Underfitting* = high training error; *overfitting* = large gap.
- `[from source]` (DLB p.127-128) Capacity; hypothesis space; polynomials of degree 1, 2 and 9 (eq. 5.15-5.17, Fig. 5.2): the linear one underfits, the quadratic one generalizes, the degree-9 one overfits (uses the pseudoinverse); representational capacity vs effective capacity (limited by optimization, p.128-129).
- `[from source]` (DLB p.129) Occam's razor; VC dimension (capacity of a binary classifier); the bounds of learning theory are rarely used in deep learning (loose; capacity is hard to measure). U-shaped generalization error vs capacity (Fig. 5.3, p.130).
- `[from source]` (DLB p.130-131) Parametric × nonparametric models (nearest neighbor); **Bayes error** (error of the oracle); the expected generalization error never increases with more examples.
- `[from source]` (DLB p.131-133) **No Free Lunch** (Wolpert 1996): averaged over all distributions, every classifier has the same error; so the goal is to understand which distributions matter in the real world, not to find the universal algorithm.
- `[from source]` (DLB p.133-135) **Regularization**: preference for solutions; *weight decay* J(w) = MSE_train + λwᵀw (eq. 5.18); definition: any modification meant to reduce the generalization error, not the training error; "rivals optimization in importance" (p.135).

## Hyperparameters and validation
- `[from source]` (DLB p.135-136) Hyperparameters are not learned by the algorithm; those that control capacity would pick maximum capacity if learned on the training set. **Validation** set taken from the training set (about 80% train/20% validation); the test set never enters any choice; benchmarks reused for years become "obsolete" (optimistic).
- `[from source]` (DLB p.137-138) **k-fold** (Algorithm 5.1): partition into k mutually exclusive subsets, average of the errors; there is no unbiased estimator of the variance of this estimator.

## Estimators
- `[from source]` (DLB p.137-146) Point estimator; **bias** bias(θ̂) = E[θ̂] − θ (eq. 5.20): the sample mean is unbiased for Bernoulli and Gaussian; the sample variance with 1/m is biased (bias −σ²/m, eq. 5.36-5.39), the one with 1/(m−1) is unbiased (eq. 5.40); **standard error** SE(μ̂) = σ/√m (eq. 5.46); 95% CI = μ̂ ± 1.96·SE (eq. 5.47) and the rule "A is better than B if the upper bound of A's CI is below the lower bound of B's" (p.143); **MSE = bias² + variance** (eq. 5.53-5.54, p.144) and the bias-variance tradeoff with the U-shaped curve (Fig. 5.6, p.145); **consistency** (plim) and the counterexample of "asymptotically unbiased" without being consistent (p.146).

## Maximum likelihood
- `[from source]` (DLB p.146-148) θ_ML = argmax ∏ p_model(x⁽ⁱ⁾;θ) (eq. 5.56-5.57) = argmax Σ log p_model (5.58) = argmax E_{x∼p̂_data} log p_model (5.59); equivalent to minimizing D_KL(p̂_data‖p_model) and the cross-entropy; "cross-entropy" for the Bernoulli/softmax NLL is a misnomer: any NLL is a cross-entropy between the empirical distribution and the model's (for example, the MSE is the cross-entropy with a Gaussian model).
- `[from source]` (DLB p.148-150) Conditional version P(y|x;θ); linear regression as MLE with p(y|x) = N(y; ŷ(x;w), σ²) gives the same w as minimizing the MSE (eq. 5.65-5.66). Properties: consistency (if p_data is in the model family and corresponds to a single θ) and statistical efficiency (Cramér-Rao); with few examples regularization is used (MLE is biased but has lower variance).

## SGD and the recipe of an algorithm
- `[from source]` (DLB p.166-168) "Nearly all of deep learning is powered" by SGD: the cost is a sum over examples (eq. 5.96); the exact gradient costs O(m); SGD samples a *minibatch* (from 1 to a few hundred, fixed even with m in the billions), g = (1/m′)∇θΣL (eq. 5.98) and updates θ ← θ − εg (5.99). The cost per update does not depend on m; kernel methods require an m×m matrix, O(m²) (p.168).
- `[from source]` (DLB p.168-170) **Recipe:** dataset + cost function + optimization procedure + model; typical cost = NLL (+ regularization, eq. 5.101); decision trees and k-means need special optimizers.
- `[from source]` (DLB p.170-172) **Curse of dimensionality**: the number of configurations grows exponentially (O(vᵈ) regions, Fig. 5.9); smoothness *prior* f*(x) ≈ f*(x+ε) (eq. 5.103), which kNN takes to the extreme, is insufficient for AI; the motivation for deep learning.

## When not to read from here
`[extrapolation]` SVM, trees, k-means, MAP and Bayesian statistics were not read in this package (p.151-165).

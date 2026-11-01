# Glossary (authors' terms, with own explanation and page)

Pages = PDF (ISLR printed = PDF − 15; ESL = PDF − 19). `[from source]` unless indicated.

| Term | Explanation | Pages |
|---|---|---|
| bagging (bootstrap aggregation) | Average (or vote) of models fitted to bootstrap samples; reduces variance | ISLR p.331-332; ESL p.301 |
| baseline (reference level) | Level of the qualitative variable without a dummy; coefficients are differences relative to it | ISLR p.101 |
| Bayes classifier | Assigns the class of highest conditional probability; minimum error; unattainable gold standard | ISLR p.52-54; ESL p.39-40 |
| bias-variance trade-off | Test error = variance + bias² + irreducible error; more flexibility reduces bias and increases variance | ISLR p.49-51; ESL p.242 |
| boosting | Trees/weak learners fitted in sequence, each to the residuals/weights of the previous one | ISLR p.336-338; ESL p.356-358 |
| bootstrap | Sampling the data with replacement to estimate the variability of an estimator | ISLR p.202-205; ESL p.268-269 |
| support vector classifier | Soft margin: tolerates violations; budget C | ISLR p.359-363 |
| collinearity / multicollinearity | Correlated predictors; inflates standard errors; detect by VIF | ISLR p.114-117 |
| confounding | Simple and multiple association with opposite signs because of a correlated variable | ISLR p.150-152 |
| cost-complexity pruning | Tree pruning minimizing RSS + α|T| (weakest link) | ISLR p.322-324; ESL p.327 |
| cross-validation (K-fold, LOOCV) | Estimates the test error by refitting on parts of the data | ISLR p.194-199; ESL p.260-264 |
| curse of dimensionality | In high dimension, neighbors stop being local; sparse sample | ISLR p.123, 257; ESL p.41-43 |
| dendrogram | Tree of fusions of hierarchical clustering; the height of the fusion measures dissimilarity | ISLR p.405-408; ESL p.540 |
| deviance | −2 × maximum log-likelihood; plays the role of RSS in likelihood models | ISLR p.221; ESL p.240 |
| effective df | trace(S) for ŷ = Sy; flexibility of a regularized fit | ESL p.251-252, 87; ISLR p.294 |
| dummy variable | 0/1 indicator that encodes a qualitative level | ISLR p.99-101 |
| elastic net | Mixture of the ℓ₁ and ℓ₂ penalties | ESL p.92 |
| irreducible error | Var(ε): limit that no method beats | ISLR p.33-34 |
| reducible error | Part of the error that improves with a better f̂ | ISLR p.33-34 |
| FDR (false discovery rate) | E(V/R): expected proportion of false discoveries among those declared | ESL p.706 |
| FWER | Probability of at least one false rejection | ESL p.705 |
| Gini index | Σ p̂(1 − p̂): node purity (small = pure) | ISLR p.327; ESL p.328 |
| GAM | Generalized additive model: sum of smooth functions of each predictor | ISLR p.297-301 |
| hinge loss | max[0, 1 − y f]; loss of the support vector classifier | ISLR p.372; ESL p.445 |
| hyperplane | Affine subspace of dimension p − 1 | ISLR p.353 |
| IRLS | Iteratively reweighted least squares (logistic fitting) | ESL p.140 |
| kernel | Similarity function K(x, x′) that replaces the inner product | ISLR p.367; ESL p.443 |
| lasso | Regression with ℓ₁ penalty; sparse coefficients | ISLR p.234; ESL p.87 |
| LDA / QDA | Linear / quadratic discriminant (Gaussians with common / per-class covariance) | ISLR p.153-165; ESL p.127-130 |
| leverage | hᵢ; how unusual xᵢ is; mean (p + 1)/n | ISLR p.113-114 |
| log-odds (logit) | log[p/(1 − p)]; linear in logistic regression | ISLR p.147 |
| margin | Smallest distance from the observations to the hyperplane | ISLR p.356 |
| masking | A class is never the largest in the indicator regression fit with K ≥ 3 | ESL p.124 |
| maximum likelihood | Chooses parameters that maximize the probability of the data | ISLR p.148; ESL p.50 |
| training / test MSE | Mean squared error on the fitting data / on new data | ISLR p.44-45 |
| OOB (out-of-bag) | Observations outside the bootstrap sample of a tree; give a test error without CV | ISLR p.333; ESL p.612 |
| optimism | Err_in − err; how much the training error underestimates | ESL p.248 |
| PCA / PCR / PLS | Principal components / regression on components / partial least squares | ISLR p.230-253, 390-400; ESL p.98-101 |
| p ≫ n (high dimension) | More variables than observations; requires regularization | ISLR p.253-258; ESL p.668 |
| hierarchical principle | If there is an interaction, keep the main effects | ISLR p.104 |
| PVE | Proportion of variance explained per component | ISLR p.397-398 |
| random forest | Bagging with m predictors drawn per split (decorrelates trees) | ISLR p.334-336; ESL p.607 |
| one-standard-error rule | Smallest model within 1 SE of the minimum | ISLR p.229; ESL p.263 |
| ridge | Regression with ℓ₂ penalty | ISLR p.230; ESL p.82 |
| ROC / AUC | Sensitivity × (1 − specificity) at all thresholds / area under the curve | ISLR p.162-163 |
| scree plot | Plot of the PVE per component | ISLR p.398-399 |
| smoothing spline | Minimum of RSS + λ∫g″²; knots at all points | ISLR p.292-294 |
| soft-thresholding | Lasso shrinkage in the orthonormal case | ISLR p.240; ESL p.89 |
| stump | Tree with a single split | ISLR p.337 |
| SVM | Support vector classifier with non-linear kernel | ISLR p.352, 366-368 |
| training / test error | Error on training data / on new data | ISLR p.45; ESL p.239-240 |
| VIF | 1/(1 − R²_{Xj|X−j}); detects multicollinearity; > 5 or 10 is a problem | ISLR p.116-117 |
| VC dimension | Largest number of points the class of functions can separate in every way (shatter) | ESL p.256-257 |
| validation set approach | Simple hold-out; variable and overestimated estimate | ISLR p.191-193 |
| weight decay | ℓ₂ penalty on the weights of a network (analogous to ridge) | ESL p.417 |

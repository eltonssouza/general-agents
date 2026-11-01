# 13. Method selection guide: what the books recommend (each rule with a page)

All the rules below come from a single base, `scripts/slr_guide.json`, and can be queried with `python -I scripts/slr_guide.py recommend ...`. **Origin**: `[from source]` = the cited page says this (checked in `tests/verify_citations.py`); the script's situation filter is `[inference]`. Pages = PDF (ISLR printed = PDF − 15; ESL = PDF − 19). The guide does **not** replace validating by CV on your data set: no rule is a theorem.


## Goal and general principles

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G01 | Goal = inference (understand which predictors matter, sign and form of the relationship) | Prefer restrictive, interpretable models (linear regression, lasso); very flexible models (splines, boosting) make it harder to understand each predictor. | ISLR p.34; ISLR p.40-41 |
| G02 | Goal = prediction only | The most flexible method does not always predict best: excess flexibility causes overfitting; compare by estimated test error. | ISLR p.41; ISLR p.47 |

## Principles

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G03 | Any problem | No method dominates on all data sets; decide by estimated test error (validation, CV), not by preference. | ISLR p.44; ISLR p.169 |
| G52 | You believe the relationship is (nearly) linear | If f is linear, linear regression has no bias and is hard to beat; KNN only wins with appreciable non-linearity. | ISLR p.51; ISLR p.121 |

## Regression and regularization

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G04 | Quantitative response, n much larger than p, approximately linear relationship | Least squares has low bias and low variance; use the ch. 3 diagnostics (residuals, leverage, VIF). | ISLR p.218; ISLR p.107 |
| G05 | n is not much larger than p (n ≈ p) | The variance of least squares explodes and there is overfitting: use ridge, lasso, subset/forward or dimension reduction. | ISLR p.218-219; ISLR p.233 |
| G07 | Many predictors, but only a few with a large effect | Tends to favor the lasso (zeroes the irrelevant ones); confirm by CV because the number of relevant predictors is unknown. | ISLR p.239 |
| G08 | Response depends on many predictors of similar size | Tends to favor ridge; confirm by CV. | ISLR p.239 |
| G09 | Correlated predictors / collinearity | Diagnose by VIF (above 5 or 10 is problematic); drop or combine variables; ridge stabilizes coefficients of correlated variables. | ISLR p.116-117; ESL p.82 |
| G10 | Need to select variables and keep interpretability | Lasso or subset selection; lasso produces sparse models; forward works even with large p. | ISLR p.234; ISLR p.224 |
| G11 | Many predictors (large p) and wanting best subset | Best subset is infeasible above ~40 predictors (2^p models); use stepwise or lasso. | ISLR p.221-222; ESL p.76 |
| G49 | Many correlated variables and response tied to the directions of highest variance | PCR (M components by CV, with standardization); PLS rarely beats ridge or PCR. | ISLR p.248-253; ESL p.101 |
| G50 | Any method with a tuning parameter (λ, M, K, C, depth) | Choose the parameter by cross-validation on a grid and refit the final model with all the data. | ISLR p.242; ISLR p.362 |

## High dimension

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G06 | p > n | Do not use least squares, the F statistic, Cp/AIC/BIC or adjusted R²; use forward stepwise, ridge, lasso or PCR (in classification, ESL also offers diagonal LDA and nearest shrunken centroids); evaluate on an independent test set/CV; do not over-interpret the selected variables. | ISLR p.92-93; ISLR p.256-259; ESL p.668; ESL p.670-671 |

## Non-linearity

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G12 | Non-linear relationship in one predictor | Low-degree polynomial or splines (natural, knots at quantiles, number of knots/df by CV); splines usually outperform high-degree polynomials. | ISLR p.286-291; ISLR p.291-292 |
| G13 | Several predictors, non-linearity, want to interpret each effect | GAM (additive); add interactions by hand (X_j·X_k) if needed; for general interactions, forest or boosting. | ISLR p.300-301 |
| G14 | Suspected interaction (synergy) between predictors | Include an interaction term respecting the hierarchical principle (keep the main effects) or use trees/boosting. | ISLR p.102-104; ISLR p.301 |

## Classification

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G15 | Binary response, linear boundary, approximately normal predictors | LDA can improve on logistic when normality holds approximately. | ISLR p.166 |
| G16 | Binary response, clearly non-Gaussian predictors | Logistic regression can outperform LDA; in the scenario with Student's t, QDA deteriorates. | ISLR p.166; ISLR p.168 |
| G17 | Well-separated classes | The logistic estimates become unstable (in the limit, infinite); LDA does not suffer from this problem. SVM tends to do well with well-separated classes; with overlapping classes logistic is often preferred. | ISLR p.153; ESL p.147; ISLR p.372 |
| G18 | Small n and approximately normal predictors in each class | LDA is more stable than logistic. | ISLR p.153 |
| G19 | More than two classes | LDA is popular (multiclass logistic is little used); do not use linear indicator regression with K ≥ 3 without checking masking. | ISLR p.152-153; ESL p.124-125 |
| G20 | Moderately non-linear boundary | QDA: better if the training set is large or if the common Σ is clearly false; LDA is the better bet with few observations (QDA estimates K·p(p+1)/2 covariances). | ISLR p.164-165; ISLR p.169 |
| G21 | Highly non-linear boundary | KNN with K chosen by CV (K = 1 was the worst in scenario 6); other non-parametric methods (SVM with kernel, trees/boosting); KNN does not say which predictors matter. | ISLR p.166; ISLR p.169 |
| G22 | Imbalanced classes or asymmetric error costs | Do not trust the overall error (the null classifier errs 3.33% in Default); examine the confusion matrix, sensitivity, specificity, ROC/AUC and adjust the threshold (0.5 → 0.2 reduced missed cases from 75.7% to 41.4%) according to the costs. | ISLR p.159-162 |
| G23 | Need probabilities | Logistic and LDA estimate posteriors; the SVM hinge loss estimates the classifier, not probabilities; the bagging vote proportion is not a calibrated probability. | ESL p.445-446; ESL p.302 |
| G51 | Doubt between logistic and LDA | Logistic makes fewer assumptions and is considered a safer and more robust bet; LDA gains efficiency if the Gaussian model holds, but is not robust to gross outliers. | ESL p.146-147 |

## Trees and ensembles

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G25 | Need interpretation and easy communication, non-linear relationship | A small tree (easy to explain and visualize), knowing that accuracy is usually lower and the tree is unstable. | ISLR p.330; ISLR p.331 |
| G26 | Want the best accuracy from trees | Bagging, random forest or boosting; forests are simpler to tune and, on many problems, similar to boosting (which tends to win with tuning). | ISLR p.331; ESL p.606; ESL p.610-611 |
| G27 | Random forest | m ≈ √p (classification) or p/3 (regression), minimum node 1 (classification) or 5 (regression), but treat m as a parameter; increase B until the OOB error stabilizes (no overfitting from B). | ISLR p.334; ESL p.611-612 |
| G28 | Boosting | Learn slowly: λ = 0.01 or 0.001 (ESL: ν < 0.1), B by CV/early stopping, small trees (d = 1 gives an additive model; ESL: 4 ≤ J ≤ 8), subsampling ≈ 0.5; boosting can overfit if B is large. | ISLR p.337-338; ESL p.381-384 |
| G29 | Noisy labels or outliers in the response | Avoid AdaBoost/exponential loss; prefer binomial deviance (classification) and absolute or Huber loss (regression). | ESL p.366-368 |
| G30 | Messy data: mixed types, missing values, outliers in the predictors, many irrelevant predictors, large N | Trees come closest to an off-the-shelf method (Table 10.1); networks and SVM do poorly on these characteristics. | ESL p.370-371 |
| G31 | Interpretation is not needed and predictive power is the focus | Neural networks, SVM and kNN/kernels have good predictive power (Table 10.1), but little interpretability and little robustness to irrelevant inputs. | ESL p.370 |

## SVM

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G32 | Using SVM | Choose C (and γ in the radial kernel) by CV: high γ improves the training fit and can worsen the test fit; C is not an 'irrelevant' parameter. | ISLR p.362; ISLR p.369-370; ISLR p.373; ESL p.451 |
| G33 | SVM with many noise features | The SVM with polynomial kernel is sensitive to the degree and to noise; adaptive methods (additive/MARS) degrade less in the ESL example. | ESL p.450-451 |

## Model assessment and selection

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G34 | Choosing a model or hyperparameter | Cross-validation with k = 5 or 10 (good compromise between bias and variance); LOOCV has high variance. | ISLR p.198-199; ESL p.261-262 |
| G35 | Few observations (e.g. N = 50) | 5-fold CV trains on 40 observations and can overestimate the error if the learning curve is still steep. | ESL p.262 |
| G36 | There is variable selection, supervised filters or hyperparameter tuning | Repeat the entire sequence (selection included) within each fold; only unsupervised filters may stay outside; keep an untouched test set for the final error. | ESL p.264-266; ESL p.241 |
| G37 | Plenty of data | Split into training, validation and test (typical split 50%/25%/25%); use the test set only at the end. | ESL p.241 |
| G38 | Comparing linear models by information criterion | Cp/AIC and BIC (BIC penalizes more and chooses smaller models; BIC is consistent, AIC tends to complex models); CV is more general because it dispenses with counting df and estimating σ². | ISLR p.227-228; ESL p.253-254 |
| G39 | CV error curve flat around the minimum | One-standard-error rule: choose the simplest model whose error is within one standard error of the minimum. | ISLR p.229; ESL p.263 |
| G40 | Need a standard error or CI of an estimator without a formula | Bootstrap (B samples with replacement of size n; SE = standard deviation of the estimates). | ISLR p.202-205 |
| G41 | Testing thousands of variables individually (e.g. genes) | Control the FDR (Benjamini-Hochberg; permutation p-values) instead of Bonferroni, which is too conservative with large M; FDR is not type I error. | ESL p.705-709 |
| G53 | Adaptive models (trees) and test error | AIC is impractical (df hard to get); CV and bootstrap can underestimate the error by ~10% in these cases: only a separate test set is unbiased. | ESL p.272-273 |

## Regression diagnostics

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G42 | Correlated errors (time series) | Standard errors, CIs and p-values become optimistic; plot residuals against time. | ISLR p.109-110 |
| G43 | Non-constant error variance (funnel in the residuals) | Transform Y (log or root) or use weighted least squares. | ISLR p.110-111 |
| G44 | Outliers or influential points | Studentized residuals > 3 in absolute value are suspect; average leverage (p+1)/n; an outlier with high leverage is dangerous; remove only if it is a data-collection error. | ISLR p.111-114 |

## Unsupervised

| ID | Situation | Book recommendation | Pages |
|---|---|---|---|
| G45 | PCA for exploration or preprocessing | Center and, in general, standardize (sd = 1) before PCA; choosing the number of components by 'elbow' is subjective; in PCR, choose M by CV. | ISLR p.395-399 |
| G46 | Clustering | K-means with several random initializations; in hierarchical prefer average or complete linkage; test dissimilarities (Euclidean × correlation), standardization and subsets; treat the clusters as a hypothesis and validate. | ISLR p.403-405; ISLR p.410-416 |
| G47 | Choosing the number of clusters K | CV does not work (W_K always falls); look for an elbow in W_K or use the gap statistic; K may come from the problem (segmentation). | ESL p.537-539 |
| G48 | Only distances between objects are available (no coordinates) | K-medoids (or hierarchical) instead of K-means. | ESL p.536-537 |

## Characteristics of the methods according to ESL (prose summary of Table 10.1, ESL p.370-371)
ESL compares neural networks, SVM, trees, MARS and kNN/kernels on nine characteristics; the summary below is a paraphrase (checked visually on the rendered page), not the table:
- `[from source]` **Trees** are rated good at handling mixed-type data, missing values, outliers in the predictors, insensitivity to monotone transformations of the inputs, scalability to large N and irrelevant inputs; they are poor at extracting linear combinations of features and in predictive power, and fair in interpretability (ESL p.370).
- `[from source]` **Neural networks and SVM** appear with the opposite rating: good in predictive power and in extracting linear combinations; poor in the other listed characteristics, including interpretability (ESL p.370).
- `[from source]` **MARS** is close to trees (good with mixed types, missing values, scalability and irrelevant inputs, and the best in interpretability), but poor with outliers in the predictors, with insensitivity to monotone transformations and with linear combinations, and only fair in predictive power; **kNN/kernels** are good with missing values, outliers in the predictors and predictive power, and poor in the others, except "fair" for linear combinations (ESL p.370).
- `[from source]` ESL's conclusion: trees come closest to an off-the-shelf method for data mining, but fall short in accuracy; boosting recovers accuracy at the cost of speed, interpretability and (in AdaBoost) robustness to mislabeled data (ESL p.371).



## How to use (procedure)
See `procedimentos.md` (P1: choose a method; P2: evaluate without leakage) and run the recommendation script giving the facts of the problem (`--goal`, `--response`, `--n`, `--p`, etc.). The script only filters the rules above; the pages must be checked with `slr_lookup.py --page`.

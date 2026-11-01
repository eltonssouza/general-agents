# Operating procedures (step by step)

Each step cites the book; the **order** in which they are presented is the package's `[inference]`. Pages = PDF.

## P1. Choose a method for a new problem
1. Define the goal: prediction, inference or exploration (ISLR p.32-35; exploration = unsupervised, ISLR p.41-43).
2. Define the response type: quantitative → regression; qualitative → classification (ISLR p.43-44).
3. Compare n and p. If p > n, least squares and the Cp/AIC/BIC/adjusted R² criteria do not hold; go to regularization (ISLR p.256-258).
4. Run the rule filter: `python -I scripts/slr_guide.py recommend --goal ... --response ... --n ... --p ...`.
5. Fit 2-3 candidates of increasing complexity (e.g. regularized linear, GAM/tree, forest/boosting), each with its hyperparameters by CV (ISLR p.242, 362).
6. Compare by 5- or 10-fold CV (ISLR p.198-199; ESL p.262) and adopt the one-standard-error rule if the curves are flat (ISLR p.229).
7. Estimate the final error on an untouched test set (ESL p.241).
8. Report uncertainties (bootstrap for SE, ISLR p.202-205) and limitations (data, assumptions).

## P2. Evaluate without leakage
1. Set aside the test set before any look at the data (ESL p.241).
2. All supervised variable selection, transformation that uses y, choice of λ/K/C/depth goes **inside** each fold (ESL p.264-266). Unsupervised filters may stay outside.
3. Report the standard error of the CV estimate (ESL p.268).

## P3. Diagnostics of a linear regression
1. Residuals × fitted plot: U pattern → non-linearity; funnel → heteroscedasticity (ISLR p.107-111).
2. Residuals × time if there is a sequence (ISLR p.109-110).
3. Studentized residuals (> 3) and leverage (mean (p + 1)/n) (ISLR p.111-114).
4. VIF of each predictor (5 or 10 as a warning) (ISLR p.116-117).
5. Global F before looking at individual t (ISLR p.90-92).
6. Prediction interval for an individual, confidence interval for the mean (ISLR p.96-97).

## P4. Classification with asymmetric costs
1. Build the confusion matrix and compute sensitivity, specificity, PPV (ISLR p.160, 163-164).
2. Vary the threshold and plot the ROC/AUC (ISLR p.161-163); choose the threshold by the costs (ISLR p.162).
3. Compare against the null classifier (ISLR p.159-160).
4. If class weights are needed in trees, use a loss matrix or weighting (ESL p.329-330).

## P5. Train forests or boosting
- Forest: large B until the OOB stabilizes; m ≈ √p (classification) or p/3 (regression) as a starting point (ESL p.611-612).
- Boosting: ν < 0.1 or λ 0.01 to 0.001; J between 4 and 8 (d = 1 if additive); M by validation (*early stopping*); subsampling ≈ 0.5 (ISLR p.337; ESL p.382-384, 386).
- Assess variable importance and *partial dependence* (ESL p.386-389).

## P6. Clustering
1. Standardize if the scales differ (ISLR p.413-414).
2. K-means: several initializations, lowest objective (ISLR p.403-405). Hierarchical: test average, complete and single, and the dissimilarity (Euclidean × correlation) (ISLR p.410-414).
3. Choice of K: elbow of W_K or gap (ESL p.537-539).
4. Check robustness with subsets; report as a hypothesis (ISLR p.415-416).

## P7. p ≫ n data
1. Do not use OLS or information criteria (ISLR p.256).
2. Ridge/lasso/forward/PCR with parameter by CV (ISLR p.256-257); diagonal LDA/shrunken centroids in classification (ESL p.670-671).
3. When running per-variable tests: FDR (BH) with permutation p-values (ESL p.704-709).
4. Report a model "among many possible"; validate on independent data (ISLR p.258).

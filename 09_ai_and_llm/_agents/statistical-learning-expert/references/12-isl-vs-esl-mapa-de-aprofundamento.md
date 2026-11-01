# 12. ISLR ⇄ ESL map: where ESL goes deeper than ISLR (pages of both books)

The ISLR preface says that ESL is aimed at those with an advanced background in the mathematical sciences and that ISL covers many of the same topics with more emphasis on applications and less on mathematical detail (ISLR p.8); ISLR can also be used as a complementary computing text in a course based on ESL (ISLR p.24). Pages = **PDF** (ISLR printed = PDF − 15; ESL = PDF − 19). "NOT READ" = the package did not read that part of ESL; consult the book.

| Topic | ISLR (PDF) | ESL (PDF) | What ESL adds (read) |
|---|---|---|---|
| Statistical decision theory, Bayes error | 44-54 | 37-41 | EPE and conditional expectation (2.9)-(2.13); 0-1 loss → Bayes; L1 → median; kNN as approximation (2.14) |
| Bias-variance | 48-51 | 56-57, 242-247 | Closed-form EPE of kNN (2.47); model bias × estimation bias; 0-1 loss not additive (7.3.1) |
| Curse of dimensionality | 122-123, 256-258 | 41-46 | Edge r^(1/p), median distance (2.24), density ∝ N^(1/p), EPE linear in p |
| Linear model, inference | 76-97 | 63-71 | Hat matrix, geometry, Var(β̂), distributions, Gauss-Markov |
| Subset selection | 220-225 | 76-80 | Invalid post-search standard errors; forward stagewise; hybrids with AIC |
| Ridge | 230-234 | 82-87 | Closed-form solution, SVD, df(λ) = Σd²/(d² + λ), posterior |
| Lasso | 234-243 | 87-94 | q-norm, elastic net, LAR; comparisons in the orthonormal case (Table 3.4) |
| PCR and PLS | 245-253 | 98-101 | PLS maximizes Corr²·Var; comparison (Frank-Friedman) |
| Cp, AIC, BIC | 225-228 | 247-254 | Optimism ω = 2/N ΣCov, effective df, Bayes factor, MDL, VC/SRM |
| Cross-validation | 191-199 | 260-268, 273-276 | Bias via learning curve; right × wrong CV; GCV; Err vs ErrT |
| Bootstrap | 202-205 | 268-273 | Err⁽¹⁾, .632, .632+ ; AIC × CV × bootstrap comparison |
| Logistic | 146-152 | 138-146 | IRLS, deviance, Wald and Rao, L1-logistic |
| LDA, QDA | 153-165 | 127-132 | RDA; parameter counts; reason for LDA's success; LDA × logistic (30%) |
| Masking (indicator regression) | 144-145 (coding only) | 122-126 | Masking with K ≥ 3; vowels (11 classes) |
| Trees | 318-331 | 324-333 | Cost-complexity (9.16), categorical 2^(q−1) − 1, loss matrix, surrogate splits |
| Bagging | 331-335 | 301-308 | Probabilities × votes; 0-1 loss; model averaging and stacking |
| Random forest | 334-337 | 606-614 | Formula ρσ² + (1 − ρ)σ²/B; defaults m; OOB; permutation importance |
| Boosting | 336-338 | 356-389 | AdaBoost, additive, exponential loss × deviance, GBM, ν, subsampling, J |
| SVM | 352-373 | 436-446, 450-451, 457 | Dual, symmetric PSD kernel, penalization, skin of the orange, SRM |
| PCA | 388-400 | 553-556 | SVD and rank-q reconstruction |
| K-means | 401-405 | 527-529 | W(C), T = W + B, Voronoi, GMM = soft K-means |
| Choice of K | 404, 414-415 | 537-539 | Gap statistic |
| Hierarchical | 405-414 | 539-545 | Cophenetic, ultrametric, single/complete/average, monotone invariance |
| High dimension | 253-258 | 668-671 | "Fitting less is better"; diagonal LDA; shrunken centroids |
| Multiple testing | (not in the 1st ed.) | 702-711 | FWER, Bonferroni, FDR, BH, plug-in, SAM |
| Neural networks | (not in the 1st ed.) | 408-417 | PPR, MLP, backprop, weight decay |
| Splines, smoothing, GAM | 286-302 | 158-209 (ch. 5), 314-323 (9.1), 210-237 (ch. 6) | **NOT READ in ESL** |
| MARS, PRIM, HME, missing data | (none) | 336-353 (9.3-9.6) | **NOT READ** |
| Ensemble learning, graphical models | (none) | ch. 16-17 (PDF 624-667) | **NOT READ** |
| Learning in neighborhood networks (adaptive kNN, prototypes) | 54-55, 120-123 | ch. 13 (PDF 478-502) | **NOT READ** (only kNN in ch. 2) |

## Rule of thumb
`[inference]` Start with ISLR for the concept, the intuition and the recommendations; go to ESL when you need (1) closed-form formulas and assumptions (Gauss-Markov, optimism, effective df), (2) theoretical justifications for a method (why LDA works, why boosting is additive), (3) implementation details (IRLS, Algorithm 15.1, Algorithm 10.3), (4) assessment cautions (right × wrong CV, .632+), or (5) topics absent from ISLR 1st edition (multiple testing, neural networks). Use `scripts/slr_lookup.py --map TEMA` to consult this table.

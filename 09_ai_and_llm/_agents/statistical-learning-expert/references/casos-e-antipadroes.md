# Book cases and antipatterns (what each example illustrates)

Pages = PDF. The numbers come from the cited pages (checked by `tests/verify_citations.py`).

## Cases
| Case | What it illustrates | Pages |
|---|---|---|
| Advertising: newspaper significant alone, not in the multiple regression | Surrogate predictor for another correlated one (radio); simple × multiple coefficients | ISLR p.88-89 |
| Advertising: TV × radio, R² from 89.7% to 96.8% | Interaction/synergy; hierarchical principle | ISLR p.103-104 |
| Credit: VIF 160.67 and 160.59 for rating and limit | Extreme collinearity; solution by removing or combining | ISLR p.117 |
| Default: null classifier (3.33%) vs LDA (2.75%); 252 of 333 missed | Overall error misleads with imbalanced classes; sensitivity 24.3% | ISLR p.159-160 |
| Default: threshold 0.5 → 0.2 | Asymmetric costs; trade-off of errors (3.73% total) | ISLR p.161-162 |
| Default: student positive in simple, negative in multiple | Confounding | ISLR p.150-152 |
| Wage: 79 "high earners" in 3,000 | Few events → wide intervals; <HS with no events | ISLR p.283, 302 |
| Hitters: 3-leaf tree by CV; test minimum at 10 | CV approximates the test error but does not match it | ISLR p.325-326 |
| Heart/gene expression: forests, m = √p | Decorrelation of trees; 45.7% error of a single tree against the forest | ISLR p.335-337 |
| Heart: radial SVM γ = 10⁻¹ optimal on training, worst on test | Flexibility ≠ better test performance | ISLR p.369-370 |
| USArrests: PCA with and without standardization | Scale dominates PCA; variances 18.97 to 6,945 | ISLR p.395-397 |
| Scenarios 1-6 (LDA, QDA, KNN, logistic) | No method dominates | ISLR p.167-169 |
| N = 50, p = 5000: CV of 3% with true error of 50% | Predictor selection outside the CV loop | ESL p.264-266 |
| 1-NN with independent labels: naive bootstrap error 0.184; .632 gives 0.316 | Why .632+ exists | ESL p.269-271 |
| Vowels (11 classes): linear regression 0.67 against LDA 0.56 and logistic 0.51 | Masking | ESL p.125-126 |
| Spam: GBM 4.5%, forest 4.88%, bagging 5.4%, CART 8.7% | Typical accuracy hierarchy among tree methods | ESL p.371-372, 609 |
| Skin of the orange: degree-2 polynomial SVM (0.078) against degree 10 (0.230) without noise | SVM sensitive to kernel and noise | ESL p.450-451 |
| Radiosensitivity genes: 1,189 with |t| ≥ 2 against 631 expected; Bonferroni: none; BH α = 0.15: 11 | Multiple testing, FWER × FDR | ESL p.704-708 |
| Four simulated scenarios: AIC overestimated the error of the chosen model by 30% to 51%; CV by 0% to 4% | AIC works for choosing, but estimates the level of the error poorly | ESL p.272-273 |
| Prostate: Z-scores, F = 1.67, test error 0.521 × 1.057 | Test of groups of coefficients; base error | ESL p.69-70 |

## Antipatterns
1. **Choosing the model by training error** (RSS, R², training MSE): always favors the more complex model (ISLR p.45-47, 220; ESL p.56).
2. **Selecting variables with all the data and then doing CV** (ESL p.264-266).
3. **Reusing the test set** to choose models (ESL p.241).
4. **Accepting post-search standard errors and p-values** as if there had been no search (ESL p.79).
5. **Looking only at individual p-values** with large p (ISLR p.92).
6. **Using Cp, AIC, BIC or adjusted R² with p > n** (ISLR p.256).
7. **Standardizing badly**: ridge, lasso, PCR, PLS, PCA and clustering depend on scale (ISLR p.232, 251, 395-397, 413-414).
8. **Threshold 0.5 without costs**, and reporting only the overall error (ISLR p.159-162).
9. **K-means only once** or **K by CV** (ISLR p.403-404; ESL p.538).
10. **Reading a dendrogram by horizontal neighborhood** (ISLR p.406-407).
11. **Treating clusters as truth** (ISLR p.415-416).
12. **Interpreting bagging votes as probabilities** (ESL p.302).
13. **Using AdaBoost with noisy labels** (ESL p.366-368).
14. **Thinking 0-1 loss behaves like squared error** in bias-variance (ESL p.245-247).
15. **Using linear indicator regression with K ≥ 3** without checking masking (ESL p.124-125).
16. **Saying SVM sidesteps the curse of dimensionality** (ESL p.443, 450).
17. **Interpreting the variables chosen by lasso/forward in p ≫ n** as "the" predictive ones (ISLR p.258).
18. **Claiming the book covers deep learning, survival, conformal or modern GBM** (NOT COVERED; see `datado-edicoes.md`).

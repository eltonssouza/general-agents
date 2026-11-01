# 04. Resampling and model assessment: validation, CV, bootstrap, AIC/BIC in ESL

Sources: ISLR ch. 5 (PDF 191-205, read; the R lab, PDF 205-211, and the exercises, PDF 212-217, **not** read) and ESL ch. 7 (PDF 238-277, read, except PDF 259, example 7.9.1; exercises PDF 277-280 not read). Convention: PDF page (ISLR printed = PDF − 15; ESL = PDF − 19). The AIC/BIC/Cp criterion is in `05-selecao-de-modelos-e-regularizacao.md`.

## 1. Selection versus assessment
- `[from source]` ESL distinguishes **model selection** (estimating the performance of models in order to choose) from **model assessment** (estimating the generalization error of the final model). With plenty of data, randomly split into training, validation and test (typical split: 50% / 25% / 25%); the test set stays "in the vault" and is used only at the end; using the test set repeatedly to choose underestimates the true error, sometimes considerably (ESL p.241).
- `[from source]` Definitions: ErrT = E[L(Y, f̂(X)) | T] (error conditional on the fixed training set) and Err = E[ErrT] (expected error); most methods estimate Err well, not ErrT (ESL p.239-240, 247-248, 273-276). The training error `err` is an optimistic estimator of the error (ESL p.240, 247-248).
- `[from source]` ISLR: the training error can dramatically underestimate the test error; if there is no large test set, one uses a mathematical adjustment (ch. 6) or *hold-out* (ISLR p.191).

## 2. Simple validation (ISLR 5.1.1)
- `[from source]` Split into training and validation (hold-out); the validation MSE estimates the test error (ISLR p.191). Two drawbacks: the estimate is highly variable depending on the split (Fig. 5.2: ten splits give ten curves) and, since training uses fewer observations, it tends to **overestimate** the error of the model fitted to all the data (ISLR p.192-193). In Auto (392 obs., 196/196) the quadratic term helps, the cubic does not (ISLR p.192).

## 3. LOOCV and k-fold
- `[from source]` LOOCV: CV(n) = (1/n) Σ MSEᵢ; little bias (trains on n − 1) and **no randomness**; cost of n fits (ISLR p.194-195). For linear/polynomial least squares there is the shortcut CV(n) = (1/n) Σ ((yᵢ − ŷᵢ)/(1 − hᵢ))², with hᵢ the leverage; the shortcut **does not hold in general** (ISLR p.195-196). ESL: the same shortcut for linear smoothers ŷ = Sy uses Sᵢᵢ (7.51) and **GCV** replaces Sᵢᵢ with trace(S)/N (ESL p.263-264).
- `[from source]` k-fold: CV(k) = (1/k) Σ MSEᵢ; LOOCV is the case k = n; in practice k = 5 or 10 (ISLR p.196). The variability due to the split is much smaller than in simple validation (ISLR p.197). Often only the *position* of the minimum of the CV curve matters, not the absolute value (ISLR p.198).
- `[from source]` **Bias and variance of k**: LOOCV is almost unbiased; k-fold has intermediate bias (trains on (k − 1)n/k observations); but LOOCV has higher variance (averages of highly correlated models); so k = 5 or 10 suffer neither from excessive bias nor from very high variance (ISLR p.198-199). ESL: 5 or 10 folds are recommended as a good compromise (Breiman and Spector; Kohavi); the bias depends on the learning curve (with N = 200, training on 160 is almost the same; with N = 50, training on 40 overestimates the error) (ESL p.261-262).
- `[from source]` In classification the classification error is used: CV(n) = (1/n) Σ Errᵢ, with Errᵢ = I(yᵢ ≠ ŷᵢ) (ISLR p.199). Example: polynomial logistic of degrees 1 to 4 with test errors 0.201, 0.197, 0.160 and 0.162 (Bayes 0.133); 10-fold CV chooses degree 4 and the test set, degree 3 (ISLR p.199-201). The same applies to choosing K in KNN (ISLR p.201).
- `[from source]` **One-standard-error rule**: choose the most parsimonious model whose error is within one standard error above the best (ESL p.80, 263; ISLR p.229 for subset selection).

## 4. The wrong and the right way to do CV (ESL 7.10.2)
- `[from source]` Wrong recipe: (1) select the "best" predictors by correlation with the class using **all** the samples; (2) train the classifier with them; (3) apply CV. With N = 50, p = 5000 predictors independent of the classes (true error 50%), 100 pre-selected predictors and 1-NN, the average CV error was 3% (ESL p.264). The right way: within each fold, select the predictors and train using only the samples outside the fold; "CV must cover the entire sequence of modeling steps"; only **unsupervised** screening (e.g. highest variance) may come before (ESL p.264-266). The book says it has seen the error in papers in top journals (ESL p.266).
- `[from source]` With N = 20 and p = 500 (stumps) CV works (average error ≈ 50%) provided the model is **retrained in each fold**, including the cutoff; there is great variability, so report the standard error of the CV estimate (ESL p.266-268).

## 5. Bootstrap
- `[from source]` ISLR: the bootstrap quantifies the uncertainty of an estimator; the example is the optimal allocation α = (σ²_Y − σ_XY)/(σ²_X + σ²_Y − 2σ_XY) with σ²_X = 1, σ²_Y = 1.25, σ_XY = 0.5 (α = 0.6) (ISLR p.202-203). Simulating 1,000 data sets gives SE(α̂) ≈ 0.083; the bootstrap (B samples **with replacement**, of size n) gives 0.087, using SE_B(α̂) = √[(1/(B − 1)) Σ (α̂*ʳ − mean)²] (ISLR p.203-205).
- `[from source]` ESL: the variance of S(Z) estimated by (1/(B − 1)) Σ (S(Z*ᵇ) − S̄*)² (ESL p.268-269). For prediction error, the naive estimator Êrr_boot is poor because the bootstrap samples and the original training set share observations; the probability that an observation is in a bootstrap sample is 1 − (1 − 1/N)^N ≈ 0.632; with 1-NN and independent labels, E[Êrr_boot] ≈ 0.5 × 0.368 = 0.184 against the true 0.5 (ESL p.269-270).
- `[from source]` The **leave-one-out bootstrap** Êrr⁽¹⁾ uses only samples without observation i; it has an upward bias similar to 2-fold CV (about 0.632·N distinct observations); the **.632 estimator** = 0.368·err + 0.632·Êrr⁽¹⁾ fails under extreme overfitting (1-NN: 0.316 against 0.5); the **.632+** uses the no-information error rate γ̂ = p̂₁(1 − q̂₁) + (1 − p̂₁)q̂₁, the relative overfitting rate R̂ = (Êrr⁽¹⁾ − err)/(γ̂ − err) and the weight ŵ = 0.632/(1 − 0.368R̂) (ESL p.270-271).
- `[from source]` Comparison (ESL 7.11.1): AIC, CV and bootstrap choose models close to the best; adding a constant to the measures does not change the choice; but, as **error estimates**, AIC overestimated the error of the chosen model by 38%, 37%, 51% and 30% in the four scenarios, against 1%, 4%, 0% and 4% for CV. For adaptive models (trees) the df is hard to estimate and CV/bootstrap are the choice; with trees, CV and bootstrap can underestimate the error by ~10%, and only a separate test set is unbiased (ESL p.272-273).

## 6. Estimating the error of *this* training set is hard
- `[from source]` 10-fold and LOO estimate the **expected** error Err well and the conditional ErrT poorly; the correlation between the CV estimate and the conditional error is often negative; conclusion of ESL: estimating the test error of a specific training set, using only the data of that training set, is not easy in general (ESL p.273-276).

## Pitfalls
- Selecting variables, transforming with the response, or tuning hyperparameters outside the CV loop (ESL p.264-266).
- Reusing the test set (ESL p.241).
- Forgetting that k = n has high variance (ISLR p.198-199) and that CV can overestimate with small N (ESL p.262).
- Using AIC to estimate the *level* of the error (ESL p.272-273).

# 02. Linear regression (simple, multiple, diagnostics) and comparison with kNN

Sources: ISLR ch. 3 (PDF 76-123; read, except PDF 87 and 98, only for transition; the R lab, PDF 124-134, and the exercises, PDF 135-141, were **not** read) and ESL ch. 3.1-3.2 (PDF 63-71). ESL 3.2.3-3.2.4 (PDF 72-75) not read. Convention: PDF page (ISLR printed = PDF − 15; ESL = PDF − 19).

## 1. Simple linear regression
- `[from source]` Y ≈ β₀ + β₁X; the coefficients are estimated by **least squares**, which minimizes RSS = Σ eᵢ², with eᵢ = yᵢ − ŷᵢ; β̂₁ = Σ(xᵢ − x̄)(yᵢ − ȳ)/Σ(xᵢ − x̄)², β̂₀ = ȳ − β̂₁x̄ (ISLR p.76-77). Advertising: β̂₀ = 7.03 and β̂₁ = 0.0475 (ISLR p.77).
- `[from source]` The population (true) line differs from the least-squares (estimated) line; the estimators are unbiased: on average over many data sets they hit the target (ISLR p.78-80). SE(μ̂)² = σ²/n (ISLR p.80); SE(β̂₀)² = σ²[1/n + x̄²/Σ(xᵢ − x̄)²], SE(β̂₁)² = σ²/Σ(xᵢ − x̄)², with RSE = √(RSS/(n − 2)) as the estimate of σ (ISLR p.81). SE(β̂₁) is smaller when the xᵢ are more spread out (ISLR p.81).
- `[from source]` 95% CI ≈ β̂ ± 2·SE (more exactly, the 97.5% quantile of the t with n − 2 degrees of freedom) (ISLR p.81). Test of H₀: β₁ = 0 by the statistic t = (β̂₁ − 0)/SE(β̂₁), with n − 2 df; the 5% and 1% cutoffs correspond to t ≈ 2 and 2.75 for n = 30 (ISLR p.82-83).
- `[from source]` RSE = √(RSS/(n − 2)) is an absolute measure of lack of fit (in the unit of Y) (ISLR p.84). R² = (TSS − RSS)/TSS = 1 − RSS/TSS is the proportion of variance explained, between 0 and 1 (ISLR p.85); in simple regression, R² = r² (ISLR p.85). In biology/psychology/marketing, an R² well below 0.1 can be realistic (ISLR p.85).

## 2. Multiple regression
- `[from source]` Y = β₀ + β₁X₁ + … + β_pX_p + ε (ISLR p.86). The coefficient of a variable is the average effect holding the others fixed; in Advertising, the coefficient of newspaper becomes ≈ 0 (p-value 0.86) in the multiple regression because newspaper is a surrogate for radio (correlation 0.35); shark and ice cream analogy (ISLR p.88-89).
- `[from source]` Four questions: is there a relationship? do all predictors matter? fit? prediction? (ISLR p.90). The **F statistic** = [(TSS − RSS)/p] / [RSS/(n − p − 1)] tests H₀: β₁ = … = β_p = 0; under H₀ it is close to 1, and the cutoff depends on n and p (ISLR p.90-91). For a subset of q coefficients, F = [(RSS₀ − RSS)/q]/[RSS/(n − p − 1)] (ISLR p.92); the square of each individual t is the F with q = 1 (ISLR p.92, note).
- `[from source]` Why look at the F and not only the individual p-values: with large p, about 5% of the p-values fall below 0.05 by chance, even with no relationship at all (ISLR p.92). If p > n, least squares cannot be fitted and the F is of no use (ISLR p.92-93).
- `[from source]` Variable selection: criteria Cp, AIC, BIC, adjusted R² (detail in ch. 6); testing all 2^p models is infeasible (2³⁰ = 1,073,741,824); alternatives: *forward* selection (greedy, from the null model), *backward* (starts from the full model; not valid with p > n) and mixed (ISLR p.93-94).
- `[from source]` R² = Cor(Y, Ŷ)² in multiple regression and **always increases** when variables are added (training fit), even weak variables; RSE = √(RSS/(n − p − 1)) can rise when a useless variable is added (ISLR p.94-95). Plots reveal what numbers do not (Advertising suggests synergy) (ISLR p.95-96).
- `[from source]` Three uncertainties in prediction: error in the coefficients (reducible), model bias, and irreducible error; the **prediction interval is always wider than the confidence interval** (example: CI [10,985; 11,528] against PI [7,930; 14,580] centered at 11,256) (ISLR p.96-97).

## 3. Qualitative predictors, interactions and simple nonlinearities
- `[from source]` Two levels: a 0/1 *dummy* variable; the chosen coding changes the interpretation but not the predictions; with k levels, k − 1 dummies are used (the level without a dummy is the baseline); test by F (independent of the coding) (ISLR p.99-101).
- `[from source]` Interaction: Y = β₀ + β₁X₁ + β₂X₂ + β₃X₁X₂ + ε; TV×radio raises R² from 89.7% to 96.8% (ISLR p.102-103). **Hierarchical principle**: if there is an interaction, keep the main effects even if not significant (ISLR p.104). An interaction between a qualitative and a quantitative variable produces lines with different intercepts and slopes (ISLR p.104-105).
- `[from source]` Polynomial (e.g. horsepower²) is still a model linear in the coefficients; R² 0.688 against 0.606 in the example, but high degrees become needlessly wavy (ISLR p.106-107).

## 4. Six potential problems with the fit (ISLR p.107)
1. **Non-linearity**: plot of residuals against fitted values; a U pattern indicates it; transform (log X, √X, X²) (ISLR p.107-108).
2. **Correlated errors** (time series): standard errors underestimated, CIs and p-values optimistic; duplicating the data would narrow the CIs by √2; look for "tracking" in the residuals (ISLR p.109-110).
3. **Non-constant variance** (funnel in the residuals): transform Y (log, √) or use weighted least squares with weights ∝ 1/variance (ISLR p.110-111).
4. **Outliers**: a studentized residual > 3 in absolute value is suspect; one outlier can raise the RSE (1.09 against 0.77) and lower R² (0.892 → 0.805) without moving the line (ISLR p.111-112). Remove only if it is a data-collection error; it may indicate a missing predictor (ISLR p.112).
5. **High-leverage points**: hᵢ = 1/n + (xᵢ − x̄)²/Σ(xᵢ′ − x̄)², between 1/n and 1, mean (p + 1)/n; an outlier **and** high leverage is a "particularly dangerous" combination (ISLR p.112-114).
6. **Collinearity**: standard errors inflate (12× for limit/rating), t falls and so does the power of the test; pairwise correlations do not detect multicollinearity; use **VIF = 1/(1 − R²_{Xj|X−j})**, minimum 1, rule of thumb: above 5 or 10 is problematic (Credit: 160.67 and 160.59); solutions: drop one variable or combine them (ISLR p.114-117).

## 5. Linear regression versus KNN
- `[from source]` Regression KNN: f̂(x₀) = mean of the responses of the K neighbors; K = 1 interpolates (step function); large K smooths and can mask structure (bias) (ISLR p.120).
- `[from source]` The parametric method wins if the chosen form is close to the true one (ISLR p.121). With near-linearity, KNN beats linear regression for K ≥ 4; with strong non-linearity, KNN always wins (ISLR p.121). With noise in many dimensions, linear regression wins from p ≥ 4 (curse of dimensionality) (ISLR p.123). The book's general rule: parametric methods tend to outperform non-parametric ones when there are few observations per predictor; and, if KNN is only slightly better, one may give up a little accuracy for a simple model, describable with a few coefficients and with p-values (ISLR p.124).

## 6. ESL: details that ISLR does not give
- `[from source]` β̂ = (XᵀX)⁻¹Xᵀy, hat matrix H = X(XᵀX)⁻¹Xᵀ, projection geometry; Var(β̂) = (XᵀX)⁻¹σ², σ̂² with N − p − 1 in the denominator (unbiased) (ESL p.64-66). Under Gaussian errors, β̂ ~ N(β, (XᵀX)⁻¹σ²), (N − p − 1)σ̂² ~ σ²χ², and the Z-score z_j = β̂_j/(σ̂√v_j) (ESL p.66-67); F for nested models (ESL p.67); CI β̂ ± 2·se ≈ 95% (ESL p.68).
- `[from source]` Prostate: train 67/test 30; table with Z-scores; dropping age, lcp, gleason and pgg45 gives F = 1.67 (p = 0.17); test error 0.521 against 1.057 for the "base error" (ESL p.69-70).
- `[from source]` **Gauss-Markov**: among the linear unbiased estimators, least squares has the smallest variance; but restricting oneself to unbiased ones "is not necessarily wise": a biased estimator can have a smaller MSE (it trades a little bias for a lot of variance) (ESL p.70-71); MSE = Var + bias² (ESL p.70-71); EPE = σ² + MSE (ESL p.71).
- `[inference]` The step from Gauss-Markov to ridge/lasso is the motivation for the methods of ISLR chapter 6: see `05-selecao-de-modelos-e-regularizacao.md`.

## Pitfalls
- Interpreting simple coefficients as effects "holding others fixed" (ISLR p.88-89).
- Trusting individual p-values with large p (ISLR p.92).
- Using training R² to compare models of different sizes (ISLR p.94-95).
- Ignoring error correlation in time series (ISLR p.109).

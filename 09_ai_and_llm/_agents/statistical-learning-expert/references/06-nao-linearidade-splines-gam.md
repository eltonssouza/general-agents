# 06. Beyond linearity: polynomials, steps, splines, smoothing, local regression, GAM

Main source: ISLR ch. 7 (PDF 280-302; read, except the first half of PDF 294; the R lab, PDF 302-311, and the exercises, PDF 312-317, **not** read). **ESL treats this topic in greater depth in ch. 5 (splines, smoothing, RKHS, wavelets; PDF 158-209), 6 (kernel methods; PDF 210-235) and 9.1 (GAM; PDF 314-323), which this package did NOT read**: what follows comes from ISLR, except the little from ESL ch. 2.8 (PDF 52-55) and 7.6 (PDF 251-252) cited below. Convention: PDF page (ISLR printed = PDF − 15; ESL = PDF − 19).

## 1. List of methods
- `[from source]` Polynomial (powers of X), step function (cuts the domain into regions and fits constants), *regression splines* (polynomials per region joined at knots), *smoothing splines* (RSS with a smoothness penalty), local regression (smoothly overlapping regions) and GAM (generalization to several predictors) (ISLR p.280-281).

## 2. Polynomials and steps
- `[from source]` y = β₀ + β₁x + … + β_d x^d (7.1) is estimated by least squares; the individual coefficients matter little, one looks at the fitted function; the bands are ±2 pointwise standard errors, with Var f̂(x₀) = ℓ₀ᵀĈℓ₀ (ISLR p.281-283). With n = 3,000 but only 79 "high earners", the polynomial logistic gives wide intervals (ISLR p.283).
- `[from source]` Step functions impose local rather than global structure, but "may miss the action" if there are no natural cutpoints; they are popular in biostatistics/epidemiology (5-year bands) (ISLR p.283-285). Polynomials and steps are special cases of fixed, known **basis functions** b_k(X) (7.7); the inference tools of ch. 3 still apply (ISLR p.285).

## 3. Regression splines
- `[from source]` Piecewise polynomials with **knots**; K knots → K + 1 cubics; without constraints the fit jumps; requiring continuity and continuity of the 1st and 2nd derivatives yields a **cubic spline**; each constraint frees one degree of freedom; a cubic spline with K knots uses 4 + K degrees of freedom; a spline of degree d has continuous derivatives up to d − 1 (ISLR p.286-288). Basis: x, x², x³ plus one truncated power function h(x, ξ) = (x − ξ)³₊ per knot (ISLR p.288).
- `[from source]` Splines have high variance at the boundaries; the **natural spline** requires linearity outside the extreme knots and gives more stable estimates (ISLR p.289). Knots: place more where the function varies most, or, in practice, at uniform quantiles choosing the degrees of freedom; the number of knots by CV (Wage: 3 df for the natural and 4 for the cubic suffice); in additive models, fix one df (e.g. 4) per term (ISLR p.289-291). Splines usually outperform polynomials, which need a high degree and oscillate at the ends (degree 15 against a natural spline of 15 df) (ISLR p.291-292).

## 4. Smoothing splines
- `[from source]` Minimizes Σ(yᵢ − g(xᵢ))² + λ∫g″(t)²dt (7.11): loss + penalty, as in ridge and lasso; λ = 0 interpolates; λ → ∞ gives the least-squares line; λ controls bias-variance; the solution is a cubic spline with knots at all the xᵢ, linear outside the range (ISLR p.292-293). Effective degrees of freedom df_λ = Σ{S_λ}ᵢᵢ (7.13), with ĝ_λ = S_λ y (7.12); λ is chosen by CV, and LOOCV is cheap: RSS_cv(λ) = Σ[(yᵢ − ĝ_λ(xᵢ))/(1 − {S_λ}ᵢᵢ)]² (ISLR p.294). In Wage, 16 df against 6.8 df by LOOCV (the simpler is preferable) (ISLR p.295).
- `[from source]` ESL (overview): PRSS(f; λ) = RSS(f) + λJ(f), with the penalty as a log-prior and the fit as the posterior mode (ESL p.53); df(S) = trace(S) for linear methods ŷ = Sy (ESL p.251-252).

## 5. Local regression and GAM
- `[from source]` Local regression (Algorithm 7.1): takes the fraction s = k/n of points closest to x₀, assigns decreasing weights and fits weighted least squares; the *span* s controls flexibility; it is "memory-based" and suffers if p > 3 or 4 (few close neighbors) (ISLR p.295-297). ESL: kernels such as the Gaussian and the Nadaraya-Watson estimator are the simple form of local regression (ESL p.54).
- `[from source]` **GAM**: y = β₀ + Σ f_j(x_j) + ε (7.15); each f_j can be a natural spline, smoothing spline, local regression, etc.; models with natural splines are one large regression on basis variables and dummies; with smoothing splines one uses *backfitting* with partial residuals (ISLR p.297-300). Pros: captures non-linearities without hand-transforming, can predict better, the effect of each X_j is interpretable with the others fixed, df per term. Cons: **additive**, interactions can go unnoticed (one can add X_j·X_k or f_jk of 2 variables); for fully general models, random forest and boosting; GAM is a compromise between the linear and the fully non-parametric (ISLR p.300-301). Logistic GAM (7.18) (ISLR p.301). In Wage, no individual with less than a high school education earns > 250 thousand, so the band explodes and the fit is redone without that level (ISLR p.302).

## Pitfalls
- Polynomial degree too high (ISLR p.292).
- Splines without a naturalness constraint at the boundaries (ISLR p.289).
- Forgetting that GAM is additive (ISLR p.301).
- Attributing to ESL the content of ch. 5, 6 and 9.1: **not read here**.

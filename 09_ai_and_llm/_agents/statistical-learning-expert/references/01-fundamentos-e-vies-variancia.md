# 01. Fundamentals: learning f, reducible and irreducible error, bias-variance

Sources: ISLR ch. 2 (PDF 30-56, read in full) and ESL ch. 2 (PDF 30-58) and ch. 7.1-7.3 (PDF 238-247). Convention: **PDF page** (ISLR: printed = PDF − 15; ESL: printed = PDF − 19). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Not read: ESL ch. 1 and 2.1-2.2 (PDF 20-29).

## 1. The problem (ISLR)
- `[from source]` The basic model is Y = f(X) + ε, with f fixed and unknown and ε independent of X with mean zero (ISLR p.31). Reducible error comes from estimating f poorly; irreducible error comes from ε (unmeasured variables and unmeasurable variation) (ISLR p.33).
- `[from source]` For fixed f̂ and X, E(Y − Ŷ)² = [f(X) − f̂(X)]² + Var(ε) (reducible + irreducible) (ISLR p.34). Var(ε) is a lower bound on the test error, almost always unknown in practice (ISLR p.34).
- `[from source]` Two goals: **prediction** (f̂ can be a black box) and **inference** (the form of f̂ is needed to know which predictors matter, the sign of the relationship, and whether it is linear) (ISLR p.32, 34). Examples in the book: direct mail = prediction; Advertising = inference; house prices = both (ISLR p.35).
- `[from source]` Parametric methods (assume a form, e.g. linear, p+1 coefficients) are easier to fit but can be far from f; too much flexibility leads to overfitting (following the noise) (ISLR p.36-37). Non-parametric methods assume no form but need many more observations (ISLR p.38).
- `[from source]` Flexibility × interpretability: subset selection and lasso (more restrictive, interpretable) → least squares → GAM → trees → bagging/boosting/SVM (less interpretable) (ISLR p.40-41). For inference, restrictive models are preferable; for prediction, the most flexible model is **not always** the most accurate (ISLR p.41).
- `[from source]` Supervised × unsupervised (ISLR p.41-43); semi-supervised is outside the scope of the book (ISLR p.43). Regression = quantitative response; classification = qualitative; logistic regression, although it estimates probabilities, is usually used for classification (ISLR p.43-44). The type of the predictor matters less than the type of the response (ISLR p.44).
- `[from source]` "There is no free lunch in statistics": no method dominates on all data sets (ISLR p.44).

## 2. Measuring the quality of fit
- `[from source]` MSE = (1/n) Σ (yᵢ − f̂(xᵢ))² (ISLR p.44). Training and test are different: what matters is the **test MSE**, on data not used in the fit (ISLR p.45). A lower training MSE does not guarantee a lower test MSE (ISLR p.46).
- `[from source]` Degrees of freedom summarize flexibility (a line = 2 df); the training MSE falls monotonically with flexibility and the test MSE is U-shaped; overfitting = small training MSE with large test MSE, when a less flexible model would have a lower test error (ISLR p.47).
- `[from source]` The minimum point of the test MSE varies widely across data sets (ISLR p.48); cross-validation estimates the test MSE from the training data (ISLR p.48).

## 3. Bias-variance decomposition
- `[from source]` E(y₀ − f̂(x₀))² = Var(f̂(x₀)) + [Bias(f̂(x₀))]² + Var(ε) (ISLR p.49; the proof is outside the scope of ISLR). The expected test error is never below Var(ε) (ISLR p.49).
- `[from source]` Variance = how much f̂ would change with a different training set; bias = the error of approximating a real problem by a simple model. More flexible methods: bias falls and variance rises; the MSE rises when the variance starts growing faster than the bias falls (ISLR p.49-50). ISLR calls the trade-off one of the recurring themes of the book (ISLR p.51). If f is linear, linear regression has no bias and is hard to beat (ISLR p.51).
- `[from source]` ESL, the more complete version: Err(x₀) = σ²ε + Bias² + Var (ESL p.242); for kNN in regression, Err(x₀) = σ²ε + [f(x₀) − (1/k)Σ f(x₍ℓ₎)]² + σ²ε/k, where the variance falls as 1/k (ESL p.56-57, 242). For a linear model fitted by least squares with p parameters, the average variance over the training points is (p/N)σ²ε (ESL p.243).
- `[from source]` ESL separates model bias (best linear approximation versus the truth) from estimation bias (estimate versus the best linear approximation); least squares has zero estimation bias, ridge has positive estimation bias, and only enriching the model class reduces the model bias (ESL p.243).
- `[from source]` With 0-1 loss, bias and variance do **not** add up: estimation errors that leave the prediction on the right side of the boundary cost nothing (e.g. true probability 0.9, average estimate 0.6), and the best tuning parameters can differ between squared and 0-1 loss (ESL p.245-247).

## 4. Classification: Bayes and kNN
- `[from source]` Training error rate = (1/n) Σ I(yᵢ ≠ ŷᵢ); the test rate is the mean of I(y₀ ≠ ŷ₀) (ISLR p.52). The **Bayes classifier** assigns the class with the highest Pr(Y = j | X = x₀); with two classes, it predicts class 1 if the probability > 0.5 (ISLR p.52-53). Its error rate, 1 − E[max_j Pr(Y = j | X)], is the analogue of the irreducible error and an unattainable gold standard (ISLR p.53-54). In the ISLR simulated data the Bayes error is 0.1304 (ISLR p.54; on p.200 the book cites 0.133 for a similar data set: use the number from the page you are reading).
- `[from source]` kNN estimates Pr(Y = j | X = x₀) by (1/K) Σ_{i∈N₀} I(yᵢ = j) and classifies by the largest (ISLR p.54). K = 1: low bias, very high variance, zero training error; large K: nearly linear, low variance, high bias; in the example, test error 0.1363 with K = 10 (close to the Bayes 0.1304), 0.1695 with K = 1 and 0.1925 with K = 100 (ISLR p.54-55).
- `[from source]` ESL: 0-1 loss leads to the Bayes classifier (most probable class) (ESL p.39-40); kNN approximates the conditional expectation by replacing "expectation" with the sample mean and "conditioning at a point" with "conditioning on a neighborhood" (ESL p.38). The "effective dimension" of kNN is N/k (ESL p.34, 260).
- `[from source]` ESL decision theory for regression: with squared loss, the best predictor is E(Y | X = x); with absolute loss, the conditional median (ESL p.37, 39).

## 5. Curse of dimensionality (ESL ch. 2.5)
- `[from source]` In a unit hypercube, capturing a fraction r of the data requires an expected edge e_p(r) = r^(1/p); at p = 10, e(0.01) = 0.63 and e(0.1) = 0.80 (ESL p.41). The median distance to the nearest point is d(p, N) = (1 − ½^(1/N))^(1/p); with N = 500 and p = 10 it is ≈ 0.52, i.e. the points are closer to the boundary than to one another (ESL p.42). The sampling density is proportional to N^(1/p): 100 points in one dimension are equivalent to 100¹⁰ in ten (ESL p.42).
- `[from source]` At p = 10, in more than 99% of samples the nearest neighbor is more than 0.5 from the origin; the MSE of the 1-NN in the example saturates at 1.0 (ESL p.43). In the correct linear model, the expected error grows only linearly with p (σ²(p/N) + σ²) (ESL p.45). Local methods suffer in high dimension; those that avoid it impose strong assumptions (ESL p.46, 52).
- `[from source]` ISLR shows the same phenomenon: with 100 observations and p ≥ 4 predictors (with noise), linear regression beats regression KNN, and the KNN error rises more than tenfold at p = 20 (ISLR p.123).

## 6. When restriction is necessary (ESL 2.7-2.8)
- `[from source]` Minimizing RSS(f) over arbitrary functions has infinitely many solutions (any function passing through the points); the class of functions must be restricted, and the restriction comes from considerations external to the data (ESL p.51-52). Classes of restriction: roughness penalty (PRSS = RSS + λJ(f); cubic smoothing spline with ∫[f″]²), kernels/local regression, bases/dictionaries (ESL p.53-55). Choosing the complexity parameter by the training RSS would always choose the interpolating fit (ESL p.56).

## Pitfalls
- Confusing training MSE with test MSE (ISLR p.45-47).
- Saying "the more flexible model is always better for prediction" (ISLR p.41).
- Applying the bias² + variance sum to the classification error rate (ESL p.245).

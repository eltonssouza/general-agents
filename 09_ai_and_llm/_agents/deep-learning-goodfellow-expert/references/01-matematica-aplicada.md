# 01 · Applied mathematics (DLB ch. 2-4: linear algebra, probability and information theory, numerical computation)

**Coverage (precise statement):** ch. 2 read p.46-66 (p.67 not); ch. 3 read p.68-70 and 88-94 (p.71-87: titles only, **not read**); ch. 4 read p.95-107 (p.108-112 titles only). Convention: "DLB p.N" = PDF page (printed = N − 15). Formulas used in the scripts were checked visually on the rendered page (eq. 3.49-3.50 on p.89).

## Linear algebra (ch. 2)
- `[from source]` (DLB p.46-49) Scalars, vectors, matrices and tensors; transpose; the book uses *broadcasting* (adding the vector b to each row of A, C = A + b), p.49.
- `[from source]` (DLB p.49-50) Matrix product Cᵢⱼ = Σₖ AᵢₖBₖⱼ (not the element-wise product, the Hadamard one); distributive and associative, not commutative; (AB)ᵀ = BᵀAᵀ.
- `[from source]` (DLB p.51-52) The inverse A⁻¹ solves Ax = b, but "is primarily a theoretical tool" and should not be used in practice in most cases, because of limited precision.
- `[from source]` (DLB p.52-54) For A⁻¹ to exist, A must be square with linearly independent columns; otherwise it is singular. Column space and *span*.
- `[from source]` (DLB p.54-55) Lᵖ norms; L² (Euclidean), squared L² (derivatives depend only on the corresponding element, but it grows slowly near the origin), L¹ (distinguishes zero from nearly zero), the "L⁰" is not a norm, max norm and Frobenius norm; xᵀy = ‖x‖‖y‖cos θ.
- `[from source]` (DLB p.55-57) Diagonal (easy inverse), symmetric, orthogonal (AᵀA = I, hence A⁻¹ = Aᵀ).
- `[from source]` (DLB p.57-59) Eigendecomposition A = V diag(λ) V⁻¹; real symmetric: A = QΛQᵀ; singular iff some eigenvalue is zero; positive definite/semidefinite.
- `[from source]` (DLB p.59-61) SVD A = UDVᵀ (U, V orthogonal); Moore-Penrose pseudoinverse A⁺ = VD⁺Uᵀ (in practice) or A⁺ = lim(AᵀA + αI)⁻¹Aᵀ; more columns than rows gives the solution of smallest L² norm; more rows gives the x that minimizes ‖Ax − y‖₂.
- `[from source]` (DLB p.61-62) Trace (invariant under cyclic permutation) and determinant (product of the eigenvalues; |det| measures volume expansion).
- `[from source]` (DLB p.63-66) **PCA** derived with linear algebra only: decoder g(c) = Dc with orthonormal columns of D; encoder f(x) = Dᵀx; reconstruction r(x) = DDᵀx; for l = 1 it recovers the first component and, in general, D holds the l eigenvectors with the largest eigenvalues (stated by induction, p.66).

## Probability and information theory (ch. 3)
- `[from source]` (DLB p.69-70) Three sources of uncertainty (inherent stochasticity, incomplete observability, incomplete modeling); a simple but uncertain rule ("most birds fly") is more practical than a complete but brittle rule; frequentist vs Bayesian (degree of belief).
- `[from source]` (DLB p.88) Self-information I(x) = −log P(x), in **nats** with the natural log (1 nat = information of an event of probability 1/e); bits/shannons are a rescaling. Desired properties: likely events carry little information, rare ones carry more, independent events add up.
- `[from source]` (DLB p.89) **Shannon entropy** H(x) = E[I(x)] = −E[log P(x)] (eq. 3.49); lower bound on the average number of bits needed to encode P; nearly deterministic distributions have low entropy. **KL** D_KL(P‖Q) = E_{x∼P}[log P(x) − log Q(x)] (eq. 3.50): non-negative, zero iff P = Q, **not symmetric**.
- `[from source]` (DLB p.90) **Cross-entropy** H(P,Q) = H(P) + D_KL(P‖Q) = −E_{x∼P} log Q(x) (eq. 3.51); minimizing over Q is equivalent to minimizing the KL; convention 0 log 0 = 0. Fig. 3.5: binary entropy is maximal at p = 0.5.
- `[from source]` (DLB p.91) The choice of KL direction matters: minimizing D_KL(p‖q) makes q cover all the modes (blurs), minimizing D_KL(q‖p) picks one mode (Fig. 3.6).
- `[from source]` (DLB p.90-94) Structured probabilistic models: factorizations such as p(a,b,c) = p(a)p(b|a)p(c|b) (eq. 3.52); directed p(x) = ∏p(xᵢ|Pa(xᵢ)) (3.53), undirected p(x) = (1/Z)∏φ(C⁽ⁱ⁾) with normalization constant Z (3.55); directionality is a property of the description, not of the distribution (p.93-94).
- **Not read (p.71-87):** random variables, PMF/PDF, marginal, conditional, chain rule, independence, expectation, common distributions (Bernoulli, Gaussian, Laplace, mixtures), useful functions and Bayes' rule. State "this package did not read those pages"; the content is standard textbook material `[extrapolation]`.

## Numerical computation (ch. 4)
- `[from source]` (DLB p.95-97) *Overflow/underflow*. Stable softmax: compute with z = x − maxᵢxᵢ (does not change the analytic value); log-softmax needs its own implementation (otherwise you get −∞); libraries such as Theano stabilize expressions automatically.
- `[from source]` (DLB p.97) Condition number of A = maxᵢⱼ|λᵢ/λⱼ| (eq. 4.2); intrinsic sensitivity of inversion. The terms *objective/criterion/cost/loss/error function* are used as synonyms.
- `[from source]` (DLB p.97-101) Gradient descent (Cauchy, 1847): x′ = x − ε∇f(x) (eq. 4.5); critical points (minimum, maximum, saddle); in DL there are many local minima and saddles surrounded by flat regions, and a "very low" value is accepted; *line search*; *hill climbing*.
- `[from source]` (DLB p.101-104) Jacobian and Hessian (the Hessian is the Jacobian of the gradient; almost always symmetric); 2nd-order Taylor f(x⁽⁰⁾ − εg) ≈ f(x⁽⁰⁾) − εgᵀg + ½ε²gᵀHg (4.9); optimal step ε* = gᵀg/(gᵀHg) (4.10), in the worst case 1/λ_max; multidimensional second-derivative test (H positive definite → minimum; eigenvalues of mixed signs → saddle; inconclusive with a zero eigenvalue); Hessian ill-conditioning hurts GD (Fig. 4.6, condition number 5).
- `[from source]` (DLB p.107) Newton's method x* = x⁽⁰⁾ − H⁻¹∇f (eq. 4.12): jumps to the minimum of a positive definite quadratic; it is harmful near saddles; first vs second order; Lipschitz continuity (4.13).
- **Not read (p.108-112):** constrained optimization (KKT) and linear least squares.

## Labels
`[extrapolation]` Geometric interpretations beyond the pages (for example, the role of the SVD in compression) only if the user asks. `scripts/dlb_calc.py` implements `info`, `softmax`, `condition`.

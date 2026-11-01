# 03 · Feedforward networks and backpropagation (DLB ch. 6, PDF p.183-242)

**Coverage:** read p.183-201, 206-216 (216 only the beginning), 219-228 and 236-242. **Not read:** p.202-205 (other output types, mixture density) and p.229-235 (general backprop, Alg. 6.5-6.6, MLP example of 6.5.7). Convention: DLB p.N = PDF page (printed = N − 15). Formula 6.23 checked visually on the page.

## Definition
- `[from source]` (DLB p.183-184) MLP/feedforward: approximates f*; y = f(x;θ); no feedback connections (with them, RNNs, ch. 10); f(x) = f⁽³⁾(f⁽²⁾(f⁽¹⁾(x))); depth, width, hidden layers (training only specifies the output). They should be thought of as "function approximation machines" for statistical generalization, not models of the brain (p.184).
- `[from source]` (DLB p.184-185) Linear models are limited; apply the linear model to φ(x). Three options for φ: generic (RBF kernel; generalizes poorly), manual (dominant until deep learning; decades of effort per task) and **learned** y = f(x;θ,w) = φ(x;θ)ᵀw — the only one that gives up convexity.

## XOR example (p.186-192)
- `[from source]` (DLB p.186-187) The linear model with MSE on the 4 points gives w = 0 and b = ½ (output 0.5 everywhere); if f⁽¹⁾ were linear the network would be linear.
- `[from source]` (DLB p.188-191) h = g(WᵀX + c) with the ReLU g(z) = max{0,z} as the default recommendation (eq. 6.3); solution: W = [[1,1],[1,1]], c = [0,−1], w = [1,−2], b = 0. Step by step: XW = [[0,0],[1,1],[1,1],[2,2]]; adding c: [[0,−1],[1,0],[1,0],[2,1]]; ReLU: [[0,0],[1,0],[1,0],[2,1]]; output [0,1,1,0]. Reproduced by `python -I scripts/dlb_calc.py xor`.
- `[from source]` (DLB p.192) This solution is at a global minimum; gradient descent normally does not find "clean" integer solutions.

## Gradient-based learning
- `[from source]` (DLB p.192) Nonlinearity makes the losses non-convex: training uses iterative gradient-based optimizers, with no convergence guarantee and sensitive to initialization; small random weights, zero or small positive biases.
- `[from source]` (DLB p.193-194) Cost = cross-entropy/MLE: J(θ) = −E log p_model(y|x) (eq. 6.12); with p_model = N(y; f(x;θ), I) it recovers the MSE (6.13). The gradient must be large and predictable: saturating functions hurt it, and the log in the NLL undoes the exp of several output units.
- `[from source]` (DLB p.194-196) Cross-entropy generally has no minimum (probabilities 0/1 unreachable; infinite density if the variance is learned): regularization prevents this. With MSE the network learns the conditional **mean** (eq. 6.15); with absolute error, the **median** (6.16); MSE and MAE give small gradients with saturating outputs, which is why cross-entropy is more popular.

## Output units
- `[from source]` (DLB p.196-197) Linear (mean of a conditional Gaussian; does not saturate).
- `[from source]` (DLB p.197-199) Sigmoid for Bernoulli: ŷ = σ(wᵀh + b) (6.19); linearly clipping to [0,1] gives zero gradient outside the interval (6.18); P(y) = σ((2y−1)z) (6.23, checked); loss = softplus((1−2y)z) (6.24-6.26): saturates only when the model is already right; with MSE it saturates whenever σ saturates, so MLE is almost always preferred; writing the NLL as a function of z, not ŷ, avoids −∞ from underflow (p.199).
- `[from source]` (DLB p.199-201) Softmax(z)ᵢ = exp(zᵢ)/Σⱼexp(zⱼ) (6.29); log softmax(z)ᵢ = zᵢ − log Σⱼexp(zⱼ) (6.30) — the first term does not saturate; Σexp ≈ maxⱼzⱼ (p.200); softmax is invariant to adding a constant (6.32), hence the stable version z − maxᵢzᵢ (6.33); MSE is a poor loss function for softmax (p.201); unregularized MLE makes the softmax predict the fractions of observed counts (6.31).
- **Not read (p.202-205):** positive variances/precisions and *mixture density networks* (Fig. 6.4 on p.206, of samples from a mixture density network, was seen).

## Hidden units
- `[from source]` (DLB p.206-208) ReLU is an "excellent default choice"; it is hard to predict which unit will work; the choice is experimental, evaluating on validation. ReLU is not differentiable at 0 (left derivative 0, right derivative 1); software returns one of them and this can be ignored in practice (p.207).
- `[from source]` (DLB p.208-209) Good practice: small positive initial bias (for example 0.1) for ReLU; generalizations: absolute value rectification (α = −1), *leaky ReLU* (α ≈ 0.01), PReLU (learned α), **maxout** (groups of k values; g(z)ᵢ = maxⱼ∈G(i)zⱼ, eq. 6.37), which needs more regularization and resists catastrophic forgetting.
- `[from source]` (DLB p.209-210) Principle: models are easier to optimize when closer to linear (including the LSTM, which propagates by summation).
- `[from source]` (DLB p.210) Logistic sigmoid and tanh (tanh(z) = 2σ(2z) − 1); as hidden units, their use is discouraged (they saturate over most of the domain); tanh is better than the sigmoid (tanh(0) = 0); still common in RNNs, probabilistic models and some autoencoders.
- `[from source]` (DLB p.211-212) Many differentiable functions work (h = cos(Wx + b) obtained <1% error on MNIST); linear units as low-rank factorization ((n+p)q parameters instead of np); RBF, **softplus** ζ(a) = log(1 + eᵃ) (the book notes that ReLU was empirically better and discourages softplus), *hard tanh*.

## Architecture and the universal approximation theorem
- `[from source]` (DLB p.212-213) Chain architecture h⁽¹⁾ = g⁽¹⁾(W⁽¹⁾ᵀx + b⁽¹⁾)...; one hidden layer is enough to fit the training set; deeper networks use fewer units and parameters and tend to generalize better, but are harder to optimize; the choice is made by experimentation, monitoring the validation error.
- `[from source]` (DLB p.213-214) **Universal approximation** (Hornik 1989; Cybenko 1989): linear output and at least one hidden layer with a "squashing" activation approximates any Borel measurable function given enough units (also holds for ReLU, Leshno 1993); however this **does not guarantee** that training will find it or that it will generalize; in the worst case it requires an exponential number of units (there are 2^(2ⁿ) binary functions).
- `[from source]` (DLB p.214-216) Depth can exponentially reduce the required size; Montufar (2014): the number of linear regions of a rectified network grows exponentially with depth (eq. 6.42; Fig. 6.5, space folds); choosing a deep model encodes the belief that the function is a composition of simpler functions (p.216).

## Backpropagation
- `[from source]` (DLB p.219) Backprop (Rumelhart 1986a) is **only the method of computing the gradient**; learning is done by another algorithm (SGD); it applies to any function, not only MLPs.
- `[from source]` (DLB p.220-222) Computational graphs; chain rule dz/dx = (dz/dy)(dy/dx) (6.44) and ∇ₓz = (∂y/∂x)ᵀ∇ᵧz (6.46): backprop is a Jacobian-gradient product per operation.
- `[from source]` (DLB p.222-226) Repeated subexpressions: store or recompute (Fig. 6.9; trades memory for time); the exponential blow-up of repetitions is avoided; Alg. 6.1 (forward), **Alg. 6.2** (scalar backprop: grad_table[u⁽ⁿ⁾] = 1; for j = n−1..1, grad[u⁽ʲ⁾] = Σ grad[u⁽ⁱ⁾]∂u⁽ⁱ⁾/∂u⁽ʲ⁾, eq. 6.49): cost proportional to the number of edges.
- `[from source]` (DLB p.227-228) Alg. 6.3 (MLP forward: a⁽ᵏ⁾ = b⁽ᵏ⁾ + W⁽ᵏ⁾h⁽ᵏ⁻¹⁾, h⁽ᵏ⁾ = f(a⁽ᵏ⁾), J = L + λΩ) and **Alg. 6.4** (backward: g ← ∇_ŷJ; for k = l..1: g ← g ⊙ f′(a⁽ᵏ⁾); ∇_b = g + λ∇Ω; ∇_W = g h⁽ᵏ⁻¹⁾ᵀ + λ∇Ω; g ← W⁽ᵏ⁾ᵀg). `scripts/dlb_calc.py grad-mlp` implements this and compares it with finite differences.
- `[from source]` (DLB p.236-239) Backprop cost: O(w) in time; O(m·n_h) memory in the MLP; operations with several outputs, memory control and data types; it is a case of *reverse mode*; finding the optimal order is NP-complete; example: the derivative of J with respect to zᵢ in the softmax with cross-entropy is qᵢ − pᵢ, a simplification that pure backprop does not make (p.237); *forward mode* is better with more outputs than inputs (p.238); a Hessian with billions of parameters is infeasible: Krylov methods and Hessian-vector products Hv = ∇ₓ[(∇ₓf)ᵀv] (eq. 6.59, p.239).
- `[from source]` (DLB p.239-242) History: chain rule (Leibniz 1676), GD (Cauchy 1847), Minsky's critique, dynamic programming in control (1960s-70s), Werbos 1981, rediscovery in the 1980s. Two decisive algorithmic changes from 1986 to 2015: cross-entropy in place of MSE and piecewise linear units in place of sigmoids (p.241); until 2012 it was thought that feedforward networks needed the help of other models; since 2012, supervised learning has been used to support the unsupervised one (p.242).
- **Not read (p.229-235):** the general backprop with per-operation *bprop* (Alg. 6.5-6.6) and the example of section 6.5.7.

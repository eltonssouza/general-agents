# Cases and antipatterns (DLB; PDF pages, printed = N − 15)

Cases and mistakes that the book itself describes. Each item cites the page read; "what to do instead" assessments that are `[inference]` are marked.

## Documented cases
1. **Street View (p.437-439, 455-457):** goal of 98% accuracy sacrificing coverage; CNN+ReLU baseline with independent softmaxes; confident errors revealed tight crops; widening the crop added 10 points of coverage; final gains via hyperparameters; "hundreds of millions" of addresses transcribed.
2. **XOR (p.186-192):** the linear model returns 0.5 everywhere; a ReLU hidden layer with two units solves it; the integer solution presented is a global minimum, but GD rarely finds "clean" weights.
3. **Rare disease (p.438):** "always absent" is right 99.9999% of the time at a prevalence of 1 in 1 million: accuracy is the wrong metric; use precision/recall/F.
4. **Silent bug in the bias update (p.452):** the network compensates and seems to work; only isolated tests (tiny dataset, gradient check) reveal it.
5. **Training and test almost equal in Street View (p.456-457):** a sign of underfitting or a data problem, not overfitting; the fix came from looking at the errors, not from changing the algorithm.
6. **Gradient that does not shrink during successful training (p.298, Fig. 8.1):** not proof of a local minimum; the growing gradient norm coexists with low validation error.
7. **SGD escapes a high-cost saddle near the initialization (p.301-302, Fig. 8.2).**
8. **Adversarial (p.283-284):** x + 0.007·sign(∇ₓJ) changes "panda" (57.7%) to "gibbon" (99.3%).
9. **Harmful pretraining in chemistry (p.545):** on average slightly harmful, useful in many tasks: not universal.
10. **Evaluating generators (p.732-734):** a cheap AIS overestimates log p(x); multiplying the input by 0.1 multiplies the likelihood by 10; different binarizations make models incomparable.

## Antipatterns (the book advises against)
- **Explicitly inverting the matrix** to solve Ax = b in practice (p.52).
- **Applying log to an already computed softmax** or computing softmax without subtracting the max (p.96, 201).
- **MSE/MAE with saturating outputs** (sigmoid/softmax): small gradients; prefer cross-entropy (p.196, 199, 201).
- **Sigmoids as hidden units** in feedforward networks (p.210); **softplus** in place of ReLU (p.212).
- **Regularizing the biases** (p.245).
- **Using the test set to choose a model or hyperparameters** (p.136); **reusing the same test set for years** (p.136).
- **Comparing algorithms without the same augmentation** (p.256) and **comparing a CNN with a model without convolution on statistical generalization benchmarks** (p.362).
- **Collecting more data when the training error is already bad** (p.441).
- **Trying many algorithms before collecting data when the bottleneck is generalization and collecting is feasible** (p.441).
- **Grid search with many hyperparameters** (cost O(nᵐ)); discretizing values in random search (p.449-450).
- **Relying only on quantitative metrics** without looking at the model in action and at the worst errors (p.452).
- **Using a learning rate ≥ 2× the optimum in the idealized quadratic case** (p.444) and **not tuning the learning rate** before the other hyperparameters (p.444).
- **Unmodified Newton near saddles** (p.107, 303).
- **Not shuffling the examples** before forming minibatches (p.295).
- **Mixing pixels in [0,1] and [0,255]** (p.468).
- **Flips or 180° rotations in OCR** (b/d, 6/9) as augmentation (p.255).
- **Greedy pretraining as mandatory** for deep fully connected networks: today it is not (p.543).
- **Accepting "blame the local minimum"** without plotting the gradient norm (p.300).

## Answer pitfalls of this agent `[inference]`
- Attributing to the book anything post-2016 (Transformers, LLMs, AdamW, LayerNorm, ResNet) → forbidden; mark `[extrapolation]` or NOT COVERED.
- Citing a page from only-sampled chapters as if they were read in full (Part III) → declare the coverage.
- Giving a formula without checking the page (for example, attributing to the book the output size formula with stride and numeric padding) → mark `[inference]`.

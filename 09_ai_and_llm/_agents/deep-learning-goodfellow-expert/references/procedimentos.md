# Step-by-step procedures (DLB; PDF pages, printed = N − 15)

Each procedure derives from pages read; the list **form** is `[inference]` where indicated. 2016 book `[DATED]`.

## P1. Starting a project (DLB p.436-441)
1. Define the metric and the error target; consider asymmetric costs, rare events (precision/recall/F) and coverage (p.437-439).
2. Build an end-to-end pipeline with a baseline: vector → feedforward; image → CNN; sequence → LSTM/GRU; ReLU; SGD with momentum and a decaying learning rate or Adam; early stopping; mild regularization (p.440).
3. Instrument (training and test error, curves) and diagnose (P2).

## P2. Diagnosing training (DLB p.441-445) — `python -I scripts/dlb_diagnose.py --train-error T --test-error V --target M`
1. Training error above the target? Do not collect more data yet: enlarge the model, tune the learning rate; rule out a bug (P4); if large, well-optimized models fail, suspect data quality (p.441).
2. Training acceptable and test poor? Check that the test measurement is right (p.453); regularize more (dropout, weight decay), consider shrinking the model; collect more data (curve on a logarithmic scale, p.442).
3. Both acceptable: nothing to do (p.442).

## P3. Tuning hyperparameters (DLB p.442-451)
1. Tune the **learning rate** first (p.444); watch the U-shaped curve of the training error (p.445).
2. Use Table 11.1 to reason about capacity (p.446).
3. Up to 3 hyperparameters: grid on a log scale, refining (p.449); more than that: log-uniform **random search** without discretizing (p.449-450). `dlb_calc.py search`.
4. Bayesian optimization: optional, not unequivocally reliable (p.451).

## P4. Debugging (DLB p.451-455) — `dlb_diagnose.py --debug`
1. Visualize the model in action and the worst errors (p.452-453).
2. Fit a tiny dataset (p.453).
3. Compare backprop with centered finite differences (and/or the complex step); for vector outputs use random projections u and v (p.454). `dlb_calc.py grad-mlp|autodiff`.
4. Monitor histograms of activations and gradients; update ≈ 1% of the parameter (p.455).

## P5. Choosing output and cost (DLB p.193-201) `[inference]` over the pages
- Gaussian mean: linear unit + MSE (p.196-197); binary: sigmoid + NLL computed in z (softplus) (p.197-199); k classes: softmax + stable log-softmax (p.199-201). Avoid MSE with sigmoid/softmax (p.199, 201).

## P6. Implementing a stable softmax/NLL (DLB p.96, 200-201)
Subtract maxᵢzᵢ; compute log-softmax(z)ᵢ = zᵢ − log Σexp(zⱼ − max) (+ max); never apply log to an already computed softmax. `dlb_calc.py softmax`.

## P7. Training with early stopping (DLB p.261-264) — `dlb_calc.py earlystop`
Evaluate validation every n steps; store a copy when it improves; stop after p evaluations without improvement; optionally retrain with all the data for i* steps (Alg. 7.2).

## P8. Applying dropout (DLB p.273-283)
Independent mask per unit (inclusion ≈ 0.8 on the input and 0.5 on the hidden units, p.274); at inference multiply the output weights by the inclusion probability (p.278); enlarge the model and the iterations; avoid it if the training set is very large or the labels are very few (p.280).

## P9. Sizing a convolutional layer (DLB p.350-373)
Output width: valid m − k + 1; same m; full m + k − 1 (p.364); stride by sampling; parameters = output_channels × input_channels × kh × kw + one bias per channel (p.363, 373). `dlb_calc.py conv-out|params`.

## P10. Choosing the optimizer (DLB p.324-325, 440)
No consensus; SGD with momentum and decay, RMSProp or Adam (suggested defaults ε = 0.001, ρ₁ = 0.9, ρ₂ = 0.999, δ = 10⁻⁸ `[DATED]`); choose by familiarity and tune the learning rate. `dlb_calc.py optim`.

## P11. Exploding gradients in an RNN (DLB p.303-304, 428-430)
Apply norm *clipping* (g ← g·v/‖g‖ if ‖g‖ > v); remember that it does not solve vanishing gradients (LSTM/GRU, bias 1 on the forget gate, p.427). `dlb_calc.py clip`.

## P12. Answering about something outside the book
Consult `dlb_lookup.py`; if "NOT COVERED", say the book (2016) does not contain it; any answer is `[extrapolation]` with a recommendation of a current source.

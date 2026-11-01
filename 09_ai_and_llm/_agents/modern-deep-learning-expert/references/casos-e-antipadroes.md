# Cases and anti-patterns (from the collection) + numerical discrepancies in the books themselves

Labels and pages as in the other files. "Anti-pattern" is a conclusion of the cited book or `[inference]` where indicated.

## 1. Cases from the books (verifiable numbers)
| Case | Fact | Source |
|---|---|---|
| MNIST-1D, shallow network | training 0%, test ~40%, test loss rises after ~1,500 steps | UDL p.132-134 |
| Conv vs FC on MNIST-1D | 2,050 vs 59,065 parameters; test ~17% vs ~40% | UDL p.181-184 |
| Residuals | 20 layers > 56 layers on CIFAR-10, in training and in test | UDL p.202 |
| ResNet-200 | top-5 4.8% and top-1 20.1% error | UDL p.209 |
| BERT | 340 million parameters; 1 million steps, batch 256 | UDL p.233-234 |
| GPT-3 | 175 billion; 96 layers; D=12,288; 300 billion tokens | UDL p.238 |
| Simple MNIST NN | [784,30,10]: 95.42% (η=3.0; 30 epochs); 100 hidden 96.59% | NNDL p.47 |
| Cross-entropy vs quadratic | 95.49% vs 95.42% and 96.82% vs 96.59% | NNDL p.97 |
| Overfitting with 1,000 images | training 100%, test 82.27% | NNDL p.111 |
| L2 | 82.27% → 87.1% (1,000 images); 95.49% → 96.49% (50,000) | NNDL p.117-120 |
| N(0,1) initialization | z with deviation 22.4; with `1/√n_in` deviation 1.22 | NNDL p.140-141 |
| Unstable gradient | `||δ||` per layer 0.003; 0.017; 0.070; 0.285 (4 hidden) | NNDL p.227 |
| CNN on MNIST | 97.80% → 98.78% → 99.06% → 99.23% → 99.37% → 99.60% → 99.67% | NNDL p.254-263 |

## 2. Anti-patterns
1. **Least squares with sigmoid/softmax output** → saturation and slow learning (NNDL p.88-89).
2. **N(0,1) weights in a layer with many inputs** → saturated neurons (NNDL p.139-141).
3. **Stacking sigmoid layers with nothing else** → unstable gradient (NNDL p.223-229).
4. **Tuning hyperparameters on the test set** → overfitting to the test set (NNDL p.112-113).
5. **Judging a "better algorithm" without fixing the data**: the SVM with 50,000 images beats the network with 5,000 (NNDL p.136-138).
6. **Trusting benchmark improvements as definitive**: "it may be a historical accident" (NNDL p.138); transformers: many improvements do not survive controlled tests (UDL p.247).
7. **Calling L2 weight decay in Adam**: they are not equivalent; use AdamW (UDL p.169-170).
8. **Dropout in convolutional layers out of reflex**: NNDL only uses it in the FC layers (NNDL p.264-265).
9. **Training a GAN without stabilizers**: mode collapse and zero gradients (UDL p.294-297).
10. **Concluding "the model understands"**: the book warns that text models only know the statistics of the language (UDL p.21, p.234, p.248).
11. **Fairness through unawareness** (UDL p.437).
12. **Using training performance as an estimate of real performance**: training error ~0 proves nothing (UDL p.133-134).
13. **Confusing NNDL's "error" (δ) with the classification error rate** (note, NNDL p.65).
14. **Applying the sigmoid initialization argument to ReLU without adjustment**: NNDL asks for its own analysis (problem, NNDL p.280); He solves it (UDL p.124).

## 3. Discrepancies and errors in the books themselves (checked)
| Location | What the book says | What the calculation/page shows | Mark |
|---|---|---|---|
| UDL p.125 vs p.126 | text: initial rate 0.01 | printed code uses `lr = 0.1` | `[from source]` (checked on both pages) |
| UDL p.416 | "177,201 parameters" and "10 outputs" (p.415) | 177,201 only reproduces with a scalar output; 10 outputs = 180,810 | `[inference]` |
| UDL p.416 | up to 10^42 regions (2 layers of 400, Di=40) | eq. 4.17 (p.67) gives ~10^97; only the 1st factor (11^40) ~10^42 | `[inference]` |
| UDL p.418 (fig. 20.2, checked by render) | 4 layers × 63 units: 15,139 parameters | the calculation gives 15,319 (possible digit transposition) | `[inference]` |
| UDL p.427 (fig. 20.12) | 198,450 parameters (2×200 on MNIST) | 784-200-200-10 = 199,210 (198,450 ↔ 780 inputs) | `[inference]` |
| UDL p.143 and p.141 | "10^5 examples" in the bins argument | 10,000 = 10^4 examples (rounded order of magnitude) | `[inference]` |
| UDL p.169-170 vs p.154 | notes: "weight decay" ≠ L2; text: L2 "weight decay" | inconsistent use of the term | `[from source]` |
| UDL p.190 vs NNDL p.283 | AlexNet top-5: 16.4% error | NNDL: 84.7% accuracy (15.3% error) | `[from source]` (difference not explained) |
| NNDL p.200 vs p.203 | `f(x)=0.2+0.4x²+0.3 x sin(15x)+0.05 cos(50x)` | repeated without the `x` in the 3rd term (render) | `[from source]` |
| NNDL p.268 (Nov/2016 note) | initialization `scale=√(1/n_out)` in the code | the ch.3 text calls for `√(1/n_in)` | `[from source]` (admitted by the author) |
| NNDL p.144 | "in Chapter 4 we'll see..." | the numbering does not match the PDF (ch.4 is universality) | `[from source]` |

## 4. What NOT to infer
- That NNDL's accuracy numbers (MNIST) serve as a current baseline: they are from 2015 and use period Theano/GPU (NNDL p.253).
- That the "✓/✗" list in fig. 14.3 (UDL p.285) is a fact: it is a debatable judgment by the author (UDL p.284).
- That "more parameters is always better": only up to a point and the theoretical proof requires conditions (UDL p.418-419, p.430).

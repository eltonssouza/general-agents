# INDEX: Deep Learning (Goodfellow, Bengio, Courville; MIT Press, 2016; acronym DLB)

Source: `DL-Deep-Learning-Goodfellow.pdf` (800 PDF pages; ~1.79 million characters of native text). **2016** book: everything that changed afterwards is `[DATED]` (see `datado-desde-2016.md`). This agent is a closed collection on **this** book; it is not a tutorial on the current state of the art.

## 1. Page convention
- **"DLB p.N" = PDF page** (marker `=== PAGE N ===` of the extracted text). The printed page is **N − 15, constant across the whole body** (verified on the 720 pages p.16-735: PDF p.16 = printed 1; PDF p.89 = printed 74; PDF p.436 = printed 421; PDF p.735 = printed 720). `python -I scripts/dlb_lookup.py --printed 74` returns PDF p.89; `--page 436` reports chapter, printed page and whether the page was read.
- **Actual** structure of the book: p.1-15 front matter; **Part I** (ch. 2-4 mathematics, ch. 5 ML fundamentals; ch. 1 is the introduction); **Part II** (ch. 6-12); **Part III** (ch. 13-20); p.736-800 are the Bibliography and Index (not used as a source). The body ends at p.735 (conclusion of ch. 20).
- Information theory is **inside ch. 3** (section 3.13, p.88-90); there is no separate chapter. "Practical methodology" is **ch. 11** (p.436-457).

## 2. Reading coverage (precise statement)
This package was built by reading the extracted text in blocks, with per-chapter notes outside the package, and only then the references. The text of mathematical books loses or scrambles notation; the formulas **used in scripts or asserted in the references** were checked by rendering the page (6.23; 8.23; Algorithm 8.7 of Adam; 8.36-8.37; 9.7-9.8; 10.8-10.11; 10.41-10.44; 3.49-3.50; 12.3).
- **Read in full:** ch. 1 (p.16-43) and ch. 11 (p.436-457); ch. 2 p.46-66.
- **Read for the most part (with declared gaps):** ch. 4 p.95-107; ch. 5 p.114-150 and 166-172; ch. 6 p.183-201, 206-216, 219-228, 236-242; ch. 7 p.243-247, 250-264, 268, 271-285; ch. 8 p.289-305, 309-314, 316-318, 321-329, 332-337; ch. 9 p.346-357, 362-371, 373-377, 386-387; ch. 10 p.388-400, 411-412, 416-418, 425-430.
- **Read by sampling:** ch. 3 (p.68-70, 88-94; **p.71-87 titles only**); ch. 12 (p.458-465, 467-470, 476-477, 482, 488-493).
- **Part III (research), minimal sampling:** ch. 13 (p.504-505), ch. 14 (p.518-524), ch. 15 (p.543-546, 551, 561-563), ch. 16 (p.574, 583-588), ch. 17 (p.606, 614-616), ch. 18 (p.621-627), ch. 19 (p.648), ch. 20 (p.671-672, 711-715, 732-734).
- **Not read:** the rest, listed by `python -I scripts/dlb_lookup.py --gaps` (including Bayesian statistics/SVM/trees of ch. 5, p.151-165; general backprop and mixture density of ch. 6; remaining BPTT and explicit memory of ch. 10; *score matching*, AIS, EM, DBN, DBM, NADE, GSN etc.). **The package's silence about those pages does not mean the book says nothing; say "this package did not read that part".**
- No subagents: sequential reading in blocks. **There was no blind test by an independent model** (see `tests/relatorio-de-fidelidade.md`).

## 3. Chapter table (PDF = start-end; printed = PDF − 15)
| Ch. | Title | Part | PDF | Reading | Reference |
|---|---|---|---|---|---|
| 1 | Introduction | I | 16-43 | full | `00-introducao-e-historia.md` |
| 2 | Linear Algebra | I | 46-67 | p.46-66 | `01-matematica-aplicada.md` |
| 3 | Probability and Information Theory | I | 68-94 | partial (68-70, 88-94) | `01-matematica-aplicada.md` |
| 4 | Numerical Computation | I | 95-112 | p.95-107 | `01-matematica-aplicada.md` |
| 5 | Machine Learning Basics | I | 113-180 | partial (114-150, 166-172) | `02-fundamentos-de-ml.md` |
| 6 | Deep Feedforward Networks | II | 183-242 | almost all | `03-redes-feedforward-e-backprop.md` |
| 7 | Regularization for Deep Learning | II | 243-288 | partial | `04-regularizacao.md` |
| 8 | Optimization for Training Deep Models | II | 289-344 | partial | `05-otimizacao.md` |
| 9 | Convolutional Networks | II | 345-387 | partial | `06-redes-convolucionais.md` |
| 10 | Sequence Modeling: Recurrent and Recursive Nets | II | 388-435 | partial | `07-redes-recorrentes.md` |
| 11 | Practical Methodology | II | 436-457 | **full** | `08-metodologia-pratica.md` |
| 12 | Applications | II | 458-500 | partial | `09-aplicacoes-e-escala.md` |
| 13 | Linear Factor Models | III | 504-516 | minimal | `10-modelos-lineares-autoencoders-e-representacoes.md` |
| 14 | Autoencoders | III | 517-540 | partial (518-524) | same |
| 15 | Representation Learning | III | 541-572 | partial | same |
| 16 | Structured Probabilistic Models for Deep Learning | III | 573-604 | minimal | `11-modelos-probabilisticos-monte-carlo-e-particao.md` |
| 17 | Monte Carlo Methods | III | 605-619 | minimal | same |
| 18 | Confronting the Partition Function | III | 620-645 | partial (621-627) | same |
| 19 | Approximate Inference | III | 646-668 | minimal (648) | `12-inferencia-aproximada-e-modelos-generativos.md` |
| 20 | Deep Generative Models | III | 669-735 | minimal | same |

Part openers: p.44-45 (I), 181-182 (II), 501-503 (III).

## 4. When to open each file
| Question / trigger | Open |
|---|---|
| What deep learning is, history, waves, 2016 numbers | `00-introducao-e-historia.md` |
| Linear algebra, PCA, entropy, KL, cross-entropy, stable softmax, conditioning, Hessian | `01-matematica-aplicada.md` |
| Overfitting, capacity, bias-variance, MLE, validation, SGD, no free lunch | `02-fundamentos-de-ml.md` |
| MLP, XOR, ReLU, sigmoid, softmax, universal approximation, backprop (graph, Alg. 6.2-6.4) | `03-redes-feedforward-e-backprop.md` |
| Weight decay, L1, dropout, early stopping, data augmentation, bagging, adversarial | `04-regularizacao.md` |
| SGD, momentum, Adam, RMSProp, batch norm, initialization, saddles, exploding gradients | `05-otimizacao.md` |
| Convolution, pooling, stride, padding, CNN parameters | `06-redes-convolucionais.md` |
| RNN, BPTT, LSTM, GRU, teacher forcing, clipping | `07-redes-recorrentes.md` |
| **What to do when training goes badly; metrics; hyperparameters; debugging** | `08-metodologia-pratica.md` + `scripts/dlb_diagnose.py` |
| GPU, distributed, GCN, n-grams, neural translation, 2015 attention | `09-aplicacoes-e-escala.md` |
| Autoencoders, greedy pretraining, distributed representation, transfer learning | `10-modelos-lineares-autoencoders-e-representacoes.md` |
| Partition function, EBM, Gibbs, CD/PCD | `11-modelos-probabilisticos-monte-carlo-e-particao.md` |
| ELBO, RBM, VAE, GAN, evaluating generators | `12-inferencia-aproximada-e-modelos-generativos.md` |
| Terms, step-by-step procedures, cases and antipatterns, dated items | `glossario.md`, `procedimentos.md`, `casos-e-antipadroes.md`, `datado-desde-2016.md` |

## 5. Scripts (Python 3, stdlib, no network; `python -I`)
- `scripts/dlb_lookup.py TERM` locates the topic and pages; prints "NOT COVERED" for verified gaps; `--page`, `--printed`, `--chapters`, `--chapter`, `--gaps`, `--datado`, `--json`.
- `scripts/dlb_calc.py SUBCOMMAND` (conv-out, conv-cost, params, info, softmax, activations, xor, autodiff, grad-mlp, metrics, ci, variance, ensemble, lr-schedule, momentum, optim, clip, init, bn, gcn, earlystop, search, condition, linadv, dropout, rnn, lstm, normal-eq, kfold): each output carries the formula, page and source label.
- `scripts/dlb_diagnose.py` training diagnosis tree from ch. 11 with pages (`--tree`, `--train-error ... --test-error ... --target ...`, `--debug`, `--hyper`, `--baseline`).

## 6. Limits
2016 book. NOT COVERED: Transformers, modern attention, LLMs, prompting, RLHF, LoRA, LayerNorm, ResNet, AdamW, GELU, modern diffusion, *normalizing flows*, PyTorch/JAX/TPU, *scaling laws*. See `datado-desde-2016.md`.

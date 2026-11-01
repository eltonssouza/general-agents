# INDEX: ISLR and ESL (Statistical Learning)

Sources (closed collection, native text):
- **ISLR**: *An Introduction to Statistical Learning with Applications in R*, G. James, D. Witten, T. Hastie, R. Tibshirani. **1st edition** (© 2013, "Corrected 8th printing 2017"), Springer. **441 PDF pages**, 10 chapters, labs in **R** `[DATED]` (ISLR p.4-5, 10-15, 24). File: `ML-Intro-to-Statistical-Learning-ISLR.pdf`.
- **ESL**: *The Elements of Statistical Learning*, T. Hastie, R. Tibshirani, J. Friedman. **2nd edition**, "Corrected 12th printing, Jan 13, 2017", Springer. **764 PDF pages**, 18 chapters (ESL p.1, 10-19). File: `ML-Elements-of-Statistical-Learning.pdf`.

Roles: **ISLR is the entry point** (concept, intuition, application, R labs) and **ESL the in-depth version** (formulas, justifications, more methods); the ISLR preface itself says so (ISLR p.8). Topic-by-topic map with pages of both books: `12-isl-vs-esl-mapa-de-aprofundamento.md`.

## 1. Page convention
- **"ISLR p.N" and "ESL p.N" = PDF page** (marker `=== PAGE N ===` of the extracted text).
- **Uniform** offsets (checked in several chapters and in the index): **ISLR printed = PDF − 15** (printed 1 = PDF 16; printed 419, start of the index = PDF 434) and **ESL printed = PDF − 19** (printed 1 = PDF 20; ch. 7 printed 219 = PDF 238; ch. 18 printed 649 = PDF 668). The headers of the PDF pages show the printed number: `python -I scripts/slr_lookup.py --printed ISLR 175` converts.
- Coverage: the main text (ISLR PDF 16-433; ESL PDF 20-717). Outside the body: covers, preface, table of contents, references and index.

## 2. Structure of the books
- **ISLR 1st ed.**: 1 Introduction; 2 Statistical Learning; 3 Linear Regression; 4 Classification; 5 Resampling Methods; 6 Linear Model Selection and Regularization; 7 Moving Beyond Linearity; 8 Tree-Based Methods; 9 Support Vector Machines; 10 Unsupervised Learning. **It has no** deep learning, survival analysis or multiple testing (`datado-edicoes.md`).
- **ESL 2nd ed.**: 1 Introduction; 2 Overview of Supervised Learning; 3 Linear Methods for Regression; 4 Linear Methods for Classification; 5 Basis Expansions and Regularization; 6 Kernel Smoothing Methods; 7 Model Assessment and Selection; 8 Model Inference and Averaging; 9 Additive Models, Trees, and Related Methods; 10 Boosting and Additive Trees; 11 Neural Networks; 12 Support Vector Machines and Flexible Discriminants; 13 Prototype Methods and Nearest-Neighbors; 14 Unsupervised Learning; 15 Random Forests; 16 Ensemble Learning; 17 Undirected Graphical Models; 18 High-Dimensional Problems: p ≫ N.

## 3. Reading coverage (precise statement)
The package was built by reading the extracted text in blocks and recording notes per chapter outside the package (`scratch/ai/statistical-learning-expert/notes/`), and only then the references. **Neither book was read in full.**

### ISLR (offset −15)
| Ch. | PDF (body) | Reading |
|---|---|---|
| 1 Introduction | 16-29 | sampling (PDF 16, 22-29) |
| 2 Statistical Learning | 30-56 (+57) | full text (PDF 30-56); R lab PDF 57-66 and exercises 67-73 **not** read |
| 3 Linear Regression | 76-123 (+124) | text read; PDF 87 and 98 only for transition; lab 124-134 and exercises 135-141 **not** read |
| 4 Classification | 143-169 | full text; lab 169-182 and exercises 183-189 **not** read |
| 5 Resampling Methods | 191-205 | full text; lab 205-211 and exercises 212-217 **not** read |
| 6 Selection and Regularization | 218-258 (+259) | full text (PDF 246-247 only the start of PCA); labs 259-273 and exercises 274-279 **not** read |
| 7 Moving Beyond Linearity | 280-302 | text read (first half of PDF 294 not); lab 302-311 and exercises 312-317 **not** read |
| 8 Tree-Based Methods | 318-338 | full text; lab 338-346 and exercises 347-351 **not** read |
| 9 Support Vector Machines | 352-373 (+374) | full text; lab 374-382 and exercises 383-387 **not** read |
| 10 Unsupervised Learning | 388-416 | full text; labs 416-427 and exercises 428-433 **not** read |
Index (PDF 434-441): not used.

### ESL (offset −19)
| Ch. | PDF (body) | Reading |
|---|---|---|
| 1 Introduction | 20-29 | **not read** |
| 2 Overview of Supervised Learning | 30-58 | **read** (2.3-2.9); 2.1-2.2 (PDF 28-29) not read |
| 3 Linear Methods for Regression | 62-119 | read: 63-71, 76-93, 98-104; **not read**: 72-75, 94-97, 105-119 |
| 4 Linear Methods for Classification | 120-156 | read: 120-132, 138-148; **not read**: 133-137, 149-156 |
| 5 Basis Expansions / 6 Kernel Smoothing | 158-237 | **not read** (only passages from ch. 2) |
| 7 Model Assessment and Selection | 238-279 | **read** in full, except PDF 259 and the exercises (PDF 277-279, only the beginning) |
| 8 Model Inference and Averaging | 280-313 | only 8.7-8.8 (PDF 301-308); rest **not read** |
| 9 Additive Models, Trees | 314-355 | only 9.2 trees (PDF 324-333); GAM, PRIM, MARS, HME, missing data **not read** |
| 10 Boosting and Additive Trees | 356-407 | read: 356-384, 386-389; **not read**: 385, 390-407 (10.13.2 end, 10.14, exercises) |
| 11 Neural Networks | 408-435 | read only 408-417 |
| 12 SVM and Flexible Discriminants | 436-477 | read: 436-446, 450-451, 457; **not read**: 447-449, 452-456, 458-477 (FDA, PDA, MDA) |
| 13 Prototype Methods and kNN | 478-503 | **not read** |
| 14 Unsupervised Learning | 504-605 | read: 527-530, 536-546, 553-556; **not read** the rest |
| 15 Random Forests | 606-623 | read: 606-614; **not read**: 615-623 (15.3.4, 15.4) |
| 16 Ensemble Learning / 17 Graphical Models | 624-667 | **not read** |
| 18 High-Dimensional Problems | 668-717 | read: 668-671, 702-711; **not read** the rest |
Bibliography and indexes (PDF 718-764): not used.

**Do not treat silence as "the book does not say"**: where the reading was partial, say "this package does not cover that part" and point to the book.

## 4. When to open each file in `references/`
| Trigger | File |
|---|---|
| ISLR vs ESL, "where does ESL go deeper?" | `12-isl-vs-esl-mapa-de-aprofundamento.md` |
| bias-variance, reducible/irreducible error, kNN and Bayes, curse of dimensionality | `01-fundamentos-e-vies-variancia.md` |
| linear regression, t, F, R², diagnostics, collinearity, interactions | `02-regressao-linear.md` |
| logistic, LDA, QDA, kNN, confusion matrix, ROC, threshold | `03-classificacao.md` |
| CV, bootstrap, .632+, test error, leak-free evaluation | `04-reamostragem-e-avaliacao-de-modelos.md` |
| subset, ridge, lasso, PCR/PLS, Cp/AIC/BIC | `05-selecao-de-modelos-e-regularizacao.md` |
| polynomial, splines, GAM, local regression | `06-nao-linearidade-splines-gam.md` |
| trees, bagging, forest, boosting | `07-arvores-bagging-florestas-boosting.md` |
| SVM, kernels, hinge | `08-svm-e-kernels.md` |
| PCA, K-means, hierarchical | `09-aprendizado-nao-supervisionado.md` |
| p ≫ n, FDR, Bonferroni, BH | `10-alta-dimensao-e-testes-multiplos.md` |
| neural networks, deep learning (limits) | `11-redes-neurais-e-deep-learning.md` |
| "which method should I use?" | `13-guia-de-escolha-de-metodo.md` (+ `scripts/slr_guide.py`) |
| R labs, "give me the code" | `14-labs-e-codigo-datado.md` |
| terms | `glossario.md`; steps: `procedimentos.md`; cases and mistakes: `casos-e-antipadroes.md`; dates and editions: `datado-edicoes.md` |

## 5. Scripts (Python 3, stdlib, no network, deterministic; run with `python -I`)
- `scripts/slr_lookup.py`: search by topic/page/chapter, ISLR⇄ESL map (`--map`), gaps (`--gaps`), page conversion (`--printed`).
- `scripts/slr_calc.py`: calculators for metrics and concepts with formulas checked against the pages (MSE/bias-variance, confusion matrix and ROC/AUC, CV, Cp/AIC/BIC in both conventions, node impurities, test statistics and p-values, multiple testing, bootstrap, kNN/curse of dimensionality, logistic/LDA, ridge/lasso, kernels, PCA/K-means, counts of models and parameters).
- `scripts/slr_guide.py`: method selection guide (52 rules with pages).

## 6. Source labels
`[from source]` = cited page checked; `[inference]` = direct deduction; `[extrapolation]` = outside the collection; `[DATED]` = changed since the edition (R from 2013-2017, software, empirical values).

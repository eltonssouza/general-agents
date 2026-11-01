# Editions, dates and what is [DATED]

## Editions of the PDFs in this collection (checked on the pages)
- **ISLR**: *An Introduction to Statistical Learning with Applications in R*, James, Witten, Hastie, Tibshirani, Springer Texts in Statistics. **1st edition** (© 2013; "Corrected 8th printing" 2017). 441 PDF pages; main text in PDF 16-433 (printed 1-418; index from PDF 434). Convention: printed = PDF − 15 (ISLR p.4-5). Chapters 1 to 10 (ISLR p.10-15). Labs in **R** (ISLR p.4, 24).
- **ESL**: *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, Hastie, Tibshirani, Friedman, Springer. **2nd edition**, "Corrected 12th printing, Jan 13, 2017" (ESL p.1). 764 PDF pages; main text PDF 20-717 (printed 1-698); printed = PDF − 19. The preface to the 2nd ed. (August 2008) lists the new chapters: 15 (forests), 16 (ensembles), 17 (undirected graphical models) and 18 (p ≫ N) (ESL p.5-6).

## What the editions do NOT have (NOT COVERED in this collection)
- **Modern deep learning** (deep CNN/RNN, transformers, modern optimizers): the 2009 ESL only has the single-hidden-layer neural network in the part read (`11-redes-neurais-e-deep-learning.md`); the extracted ESL text mentions "convolutional" 3 times in passages **not read** (example of networks with constraints, ch. 11 onward) and the ISLR 1st ed. text never does (search in the extracted text: 0 occurrences of "deep learning", "transformer", "dropout", "XGBoost", "conformal" in both).
- **Survival analysis**: there is no dedicated chapter in either; the extracted ESL text cites "survival" (27 times) and "Cox" (12) in passages **not read** by this package, and the ISLR one 1 time. **Multiple testing**: there is no chapter in ISLR 1st ed. (0 occurrences of "Bonferroni" and "Benjamini"); in ESL they appear in ch. 18.7 (read). **Naive Bayes**: 0 occurrences in ISLR; in ESL it appears in 6.6.3 and 18.2 (6.6.3 not read).
- Topics after 2009/2013: XGBoost/LightGBM/CatBoost, SHAP/LIME, conformal prediction, calibration and algorithmic fairness, Bayesian hyperparameter optimization, double descent and benign overparameterization, self-supervised learning, LLMs.
- `[extrapolation]` The 2nd edition of ISLR (2021) adds chapters on deep learning, survival analysis and multiple testing and brings labs in Python; **this collection has only the 1st edition**: do not state content of the 2nd as being "from the book". `lookup --gaps` lists the terms with occurrence counts in the text.

## [DATED] items within the content read
- Code of the R labs and names of functions/packages (ISLR p.28; see `14-labs-e-codigo-datado.md`).
- Software cited in ESL: MART, `gbm` (version 1.5), `randomForest` (4.5-11), `mboost`, commercial TreeNet (ESL p.380, 610), `glmnet` (ESL p.140): versions and interfaces have changed.
- Empirical values (test errors, optimal sizes of J, ν, number of trees) come from **simulations and data sets of the time**: use as an order of magnitude, never as a constant (e.g. "4 ≤ J ≤ 8", ESL p.382).
- The characterization "AdaBoost with trees is the best off-the-shelf classifier" is from Breiman (1996-98) (ESL p.359): `[DATED]`.
- Table 10.1 of ESL rates kNN/networks/SVM/trees/MARS with the knowledge of 2009 (ESL p.370).
- The ISLR statement that "CV is almost never a computational problem" (ISLR p.228) is from 2013; for huge n and heavy models it can become one again `[extrapolation]`.
- The format of AIC/BIC changed scale between printings/editions of ISLR `[extrapolation]`; page 227 of this printing carries the factor 1/(nσ̂²) (checked visually).

## What to do when the user cites a current fact
Agree with the current fact, mark the book passage `[DATED]` and, if it is an important decision, recommend the current documentation of the tool/library.

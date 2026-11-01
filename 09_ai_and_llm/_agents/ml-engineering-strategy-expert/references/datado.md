# [DATED] What the MLY (2018 draft) does not cover or what has aged

## Record
- The book is a **draft** ("Draft") from **2018** (MLY p.2). Everything is [DATED] 2018; the current state of the art is **not** asserted here.
- The technical context is that of the neural networks of the time (speech with MFCC/phonemes, object detectors, helicopter RL). Citations in the table on p.104 are from 2014-2016.

## Verified gaps (NOT COVERED; terms searched in the extracted text and absent)
Transformers, LLMs, BERT, language models; batch normalization, ResNet, CNN, RNN, convolution, Adam, learning rate; ensembles, k-fold, "data augmentation" as a term; AUC, calibration, confusion matrix; data leakage, drift, production monitoring, MLOps, A/B tests; fairness, privacy, interpretability; unsupervised/semi-supervised learning, active learning, fine-tuning, pre-training; confidence intervals and significance tests (only cited in passing in note 2 on p.19).
Minimal mentions: "transfer learning" and "multitask learning", "domain adaptation" appear only as academic research in notes (p.71, 81); "cross-validation" only in the alternative name of the dev set ("hold-out cross validation set", p.15).
Check: `python -I scripts/mly_lookup.py --gaps`.

## Points where current practice probably diverges [extrapolation]
- "Human-level" labels and text-generation tasks (LLMs): the book deals with supervised classification/ASR/translation; for generative models and evaluation by human preference or by an LLM-as-judge the MLY gives no guidance.
- Continuous evaluation in production and detection of distribution shift: the book treats dev/test as static and only mentions updating them after launch (p.15, 25).
- Time frames ("<1 week", "a few days") and dev set sizes (1,000-10,000) reflect the problems of 2018.
Everything above is [extrapolation] (knowledge external to the book) and should be treated with current sources.

# 04 - Learning curves (MLY ch. 28-32, p.56-64)

The figures (graphs) have no extractable text; the descriptions below come from the text and captions read on the pages, and the figures on p.62 were checked visually.

## Dev error curve (ch. 28, p.56-58)
- [from source] A learning curve plots the **dev error against the number of training examples**, training separate copies with different sizes (e.g. with 1,000 examples, 100, 200, ..., 1,000). Dev error should fall with more data (p.56).
- [from source] Mark a **desired error**: human performance; or an intuition of what gives a good user experience; or what you expect to achieve in the next quarter/year (p.56-57).
- [from source] By visually extrapolating the curve you estimate whether doubling the data can reach the desired level; if the dev curve **plateaus**, more data will not solve it and you avoid months of useless collection (p.57). Looking only at the dev curve makes it hard to predict where it will go; the training curve helps (p.58).

## Training error grows (ch. 29, p.59)
- [from source] Dev error falls, but **training error generally increases** with training set size: with 2 examples it is easy to memorize (0%, even with wrong labels); with 100 it is already harder, and with 10,000 worse, especially with ambiguous or mislabeled examples. The dev curve is usually **strictly above** the training curve (p.59).

## Interpretation (ch. 30-31, p.60-62)
- [from source] **High bias** ("textbook" case): dev error plateaus and training error is above the desired level. Since training error can only stay the same or rise with more data and dev error is usually above training error, "you can be sure that more data alone will not be enough" (p.60-61). At the largest training size there is a large gap between the training error and the desired level (high avoidable bias) and a small gap between train and dev (low variance) (p.61).
- [from source] Previously only the training and dev errors at the rightmost point (all the data) were measured; the full curve gives a more comprehensive view (p.61).
- [from source] **High variance**: training error relatively low (near or below the desired level) and dev error well above; small bias, large variance; more data will probably help close the gap (p.62).
- [from source] **Significant bias and variance**: training error well above the desired level and dev even higher; you need to reduce both (p.62).

## Plotting curves in practice (ch. 32, p.63-64)
- [from source] With a small training set the curve is **noisy** ("bad" or "good" subsets); with data skewed toward one class (e.g. 80% negatives) or many classes (100 species), an unrepresentative subset is more likely, even one with only negatives (p.63).
- [from source] Two solutions for the noise: (1) train several models (3 to 10) on random subsets of the same size sampled **with replacement** and plot the average of the training and dev errors; (2) use a **balanced** subset (e.g. 2/10 positives and 8/10 negatives, keeping the proportion of the original set) (p.63-64). Only do this if the curve is too noisy; with a training set >10,000 and slightly imbalanced classes, it is probably unnecessary (p.64). Sampling with or without replacement should not differ much (note 10, p.63).
- [from source] If training is expensive, spacing sizes on a non-linear scale (e.g. 1,000, 2,000, 4,000, 6,000, 10,000) still shows the trend (p.64).

## Decision table [inference: organization of the findings above]
| curve | reading | direction [from source] |
|---|---|---|
| training high and close to dev, both above desired | high bias | bigger model, features, less regularization (p.51, 61) |
| training low, dev far above | high variance | more data, regularization (p.53, 62) |
| training high and dev far above | both | reduce both (p.62) |
| dev plateaus above desired | more data alone is not enough | attack bias (p.57, 61) |

None of the chapters provides a formula for extrapolation; it is visual inspection (p.57).

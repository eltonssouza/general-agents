# 01 - Dev/test sets and metrics (MLY ch. 5-12, p.14-27)

## Definitions (ch. 5, p.14-16)
- [from source] Trap: splitting website data 70%/30% and training/testing well, but the app with phone photos (blurrier, less sharp, poorly lit) does badly; the algorithm did not generalize to the distribution that matters (p.14).
- [from source] **Training set**: where you run the learning algorithm. **Dev set (hold-out/hold-out cross validation)**: tune parameters, select features and make other decisions. **Test set**: evaluate performance, **not** to decide on the algorithm or parameters (p.15).
- [from source] The purpose of the dev and test sets is to **direct the team toward the most important changes** (p.15).
- [from source] Central rule: **choose dev and test sets that reflect the data you expect in the future and want to do well on**; the test set is not simply 30% of what you have, especially if the future differs from the training data (p.15).
- [from source] With no users yet: approximate (e.g. friends send phone photos); after launch, update with real data; if nothing approximates it, start with website images knowing the risk of not generalizing (p.15). Do not assume that train and test have the same distribution (p.15-16).

## Dev and test from the same distribution (ch. 6, p.17-18)
- [from source] Example of a mistake: splitting markets (US, China, India, Other) by putting US and India in the dev set and China and Other in the test set. The dev set should reflect what you most want to improve (all regions) (p.17).
- [from source] If dev and test come from the same distribution and it does well on dev but badly on test, the diagnosis is clear: **overfitting to the dev set**; the cure is more dev data. If they come from different distributions, there are three possible causes: overfitting to the dev set; the test set is harder; the test set is merely different (p.17-18).
- [from source] Mismatched dev/test make it hard to know what works and to prioritize; on third-party benchmarks with distinct distributions, luck weighs more than skill; for progress on an application, the author recommends the same distribution (p.18).

## Size (ch. 7, p.19)
- [from source] The dev set should be large enough to **detect differences** between algorithms: classifiers with 90.0% and 90.1% cannot be told apart with 100 examples; a dev set of **1,000 to 10,000** is common; 10,000 gives a good chance of detecting a 0.1% improvement (p.19).
- [from source] In mature applications (advertising, search, recommendation) there are teams chasing 0.01%; there the dev set may be much larger than 10,000 (p.19).
- [from source] Test set: large enough for high confidence in overall performance. The 30% heuristic works with 100 to 10,000 examples; with billions, the **fraction** of dev/test shrinks even as the absolute number grows; it need not be excessive (p.19).
- [from source] Statistical significance tests are rarely useful for intermediate progress in practice (note 2, p.19). The book gives **no** statistical power formula.

## Single-number metric (ch. 8, p.20-21)
- [from source] Accuracy is a single number; precision and recall are two numbers and make comparison hard (A: 95%/90%; B: 98%/85%) (p.20). Combine them: average, or **F1** (harmonic mean, "works better than the simple average"): F1 = 2/((1/P)+(1/R)); A = 92.4%, B = 91.0% (p.20-21, note 4).
- [from source] With per-market metrics (US, China, India, Other), an average or weighted average is a common way to get a single number (p.21). A single number gives a clear ranking and direction (p.21).

## Optimizing and satisficing metric (ch. 9, p.22-23)
- [from source] Instead of an artificial formula (e.g. accuracy - 0.5*time), define what is acceptable (e.g. <= 100 ms) and maximize accuracy under that constraint. With N criteria, **N-1 satisficing** (just meet a threshold) and **1 optimizing** (p.22).
- [from source] Wakeword example: minimize false negatives (optimizing) subject to at most 1 false positive per 24 h (satisficing) (p.22-23).

## Iteration (ch. 10, p.24)
- [from source] ML is an idea -> code -> experiment cycle, repeated many times; dev set + metric allow fast measurement, including 0.1% gains that cannot be noticed by "playing with the app" (p.24).

## When to change dev/test/metric (ch. 11, p.25-26)
- [from source] In a new project, define the initial dev/test sets and metric in **less than a week**, "better imperfect and get started" (mature applications, such as antispam, may take months) (p.25).
- [from source] Signal to change: dev set + metric rank A above B, but the team thinks B is better for the product. Three causes: (1) the real distribution is different (e.g. more puppies than adult cats) -> update dev/test; (2) **overfitting to the dev set** (dev much better than test) -> new dev set; (3) the metric measures something different from what matters (e.g. accuracy lets inappropriate images through) -> change the metric, penalizing the serious error heavily (p.25-26).
- [from source] You may evaluate on the test set periodically (weekly or monthly) to track progress, but **do not use the test set for decisions**, not even to revert to last week's version: that overfits the test set and removes the unbiased estimate (p.26).
- [from source] It is common to change dev/test/metric midway through a project; tell the team about the new direction (p.26).

## Summary (ch. 12, p.27)
Reflect the future; same distribution; single metric (or optimizing + satisficing); iterate fast; <1 week in a new project; 70/30 does not hold with lots of data; dev set large enough to detect changes; change quickly if (i) overfit the dev set -> more dev data, (ii) different distribution -> new dev/test, (iii) wrong metric -> change the metric (p.27).

Tool: `python -I scripts/mly_devtest_check.py check CONFIG.json` applies these rules; `scripts/mly_diagnose.py f1`.

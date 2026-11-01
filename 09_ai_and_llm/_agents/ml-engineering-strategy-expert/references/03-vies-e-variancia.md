# 03 - Bias and variance (MLY ch. 20-27, p.42-54)

## Informal definitions from the book (ch. 20, p.42-43)
- [from source] Even with train/dev/test from the same distribution, more data does not always help as much as expected; bias and variance tell you when it is worth seeking it (p.42).
- [from source] Example: target of 5% error; train 15%, dev 16%. More data probably does not help; adding examples only makes it harder to fit the training set. If training is already at 15% and the target is 5%, the first problem is performance on the training set; dev is usually worse than train (p.42).
- [from source] **Informal** decomposition: **bias = error on the training set** (15%); **variance = how much worse on dev/test than on train** (1%) (p.42). Statisticians have formal definitions (bias is, roughly, the training error with a very large training set; with mean squared error, Total error = bias + variance), but the book uses the informal one (note 6, p.42-43).
- [from source] There are methods that reduce both at once through architecture changes, but they are harder (note 7, p.43).

## Examples (ch. 21, p.44-45)
| train | dev | bias | variance | reading from the book |
|---|---|---|---|---|
| 1% | 11% | 1% | 10% | **high variance** (overfitting) (p.44) |
| 15% | 16% | 15% | 1% | **high bias**, low variance (underfitting) (p.44) |
| 15% | 30% | 15% | 15% | high bias **and** high variance; over/underfitting is hard to apply (p.44) |
| 0.5% | 1% | low | low | good performance (p.45) |

## Optimal error rate (ch. 22, p.46-48)
- [from source] For cats, the optimum is ~0%. In speech recognition with 14% of audio unintelligible even to humans, the optimum is ~14%. With train 15% and dev 30%, the training error is close to optimal (little to gain in bias), but there is a lot to gain in variance (p.46).
- [from source] Decomposition with the optimum: **optimal error = "unavoidable bias"** (14%); **avoidable bias = training error - optimal error** (1%); **variance = dev error - training error** (15%); **Bias = optimal error (unavoidable bias) + avoidable bias** (p.46-47). With train 15%, dev 16% and optimum 14%: avoidable bias 1%, variance ~1%: it is already doing well, 2% from the optimum (p.47).
- [from source] All variance is "avoidable" with enough data; **there is no unavoidable variance** (p.47).
- [from source] **Negative avoidable bias** = the algorithm does better than the optimum on the training set: it is overfitting/memorizing the training set; focus on reducing variance, not bias (note 8, p.47). Technical terms: "Bias" should be "error we attribute to bias" (note 9, p.47).
- [from source] The optimal error is also called the **Bayes error rate** (p.47). On tasks humans do well, estimate it by asking humans to label and measuring the error of the labels; on tasks that are hard even for humans (movie recommendation, ads) it is hard to estimate (p.47-48). See `05-desempenho-humano.md`.

## Simple recipe and trade-off (ch. 23-24, p.49-50)
- [from source] Simplest formula: **high avoidable bias -> increase the model**; **high variance -> add training data**. With no limits on network and data, you can do very well; in practice you run into computational cost and the finiteness of data (p.49).
- [from source] Different architectures have different bias/variance; the literature and open implementations provide inspiration, but results are less predictable than the simple recipe (p.49).
- [from source] Increasing the model generally reduces bias and may raise variance; overfitting usually appears only without regularization. With L2 or dropout well tuned on the dev set, increasing the model generally maintains or improves performance; the only reason to avoid it is computational cost (p.49).
- [from source] The "bias-variance trade-off": changes that reduce one increase the other (a bigger model or more features reduce bias and may raise variance; regularization increases bias and reduces variance). In the modern era, with lots of data and large networks, there is less trade-off: bigger network + tuned regularization reduces bias without raising variance much; more data reduces variance without affecting bias; a suitable architecture may reduce both (hard to choose) (p.50).

## Techniques (ch. 25-27, p.51-54)
**Reduce avoidable bias (p.51):** increase the model (if variance rises, regularize); modify features based on error analysis; reduce/remove regularization (L2, L1, dropout), which reduces avoidable bias and increases variance; modify the architecture. **Does not help:** more training data (it helps variance, usually without a significant effect on bias).

**Error analysis on the training set (ch. 26, p.52):** if bias is high, do error analysis on the **training** data as well (e.g. listen to ~100 poorly recognized clips and count categories: background noise, fast speech, distance from the microphone); check whether a human could transcribe it, since it may be unreasonable to demand of the algorithm what no one does.

**Reduce variance (p.53-54):** more data (the simplest and most reliable, given data and compute); regularization (L2, L1, dropout: reduces variance and increases bias); **early stopping** (stop gradient descent based on dev error; reduces variance and increases bias; behaves like regularization); feature selection (e.g. from 1,000 to 900 changes little; to 100 may change a lot; with the large data of today the tendency is to give all the features, with a small training set selection helps); **shrink the model: use with caution**, regularizing usually gives better performance; shrinking the model serves cost and training speed; and, again, modify features/architecture.

Tool: `python -I scripts/mly_diagnose.py bv --train T --dev D [--optimal O|--human H] [--traindev TD]`. The book **does not fix a numeric threshold** for "high"; the script orders magnitudes and declares the choice as [inference].

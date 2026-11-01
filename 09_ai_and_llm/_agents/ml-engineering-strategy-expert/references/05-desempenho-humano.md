# 05 - Comparing with human performance (MLY ch. 33-35, p.66-69)

## Why compare (ch. 33, p.66-67)
- [from source] Many systems automate what humans do well (image, speech, antispam), and algorithms already surpass humans on more and more tasks (p.66). Three reasons that make it easier to build ML when people do the task well (p.66):
  1. **Human labels** are easy to obtain.
  2. **Error analysis uses human intuition** (e.g. "pear of apples" instead of "pair": understanding what information the human uses to get it right).
  3. Use human performance to **estimate the optimal error rate and set a "desired error"**: with the algorithm at 10% and the human at 2%, the optimum is 2% or less and the avoidable bias is **at least 8%**, so try bias-reduction techniques (p.66).
- [from source] A reasonable, achievable target speeds up the team; knowing there is high avoidable bias opens a menu of options (p.66).
- [from source] Tasks at which not even humans are good (recommending a book, choosing an ad, predicting the stock market): labels are harder to obtain; human intuition is less reliable; the optimal and desired error are hard to know (p.66-67).

## How to define "human level" (ch. 34, p.68)
- [from source] X-ray example: layperson 15%; junior doctor 10%; experienced doctor 5%; **team of doctors who discuss each image 2%**. The book uses **2%** as a proxy for the optimal error and as the desired performance (p.68).
- [from source] Reasoning: the optimum may be even lower than 2%, but **it cannot be higher**, because a team achieves 2%; using 5% or 10% as the estimate of the optimum is unreasonable because they are necessarily too high (p.68).
- [from source] For labeling, you can put a junior doctor on most cases and escalate the hard ones to experienced doctors or the team (cost) (p.68). If the system is at 40% error, it matters little whether you use the junior (10%) or the experienced doctor (5%); with the system at 10%, setting the reference at 2% gives better tools (p.68).

## Surpassing human level (ch. 35, p.69)
- [from source] Example: noisy audio with 10% human error and a system at 8%. The three techniques of ch. 33 still work if you find a **subset** in which humans beat the system (e.g. very fast speech): better transcriptions, intuition and a human-performance target on that subset (p.69).
- [from source] In general, as long as there are dev examples where the human gets it right and the algorithm gets it wrong, the techniques apply, even if on average the system already surpasses the human (p.69).
- [from source] There are applications where machines beat humans (predicting a movie rating, delivery time, loan approval); only a subset of the techniques applies when humans have difficulty identifying the algorithm's clear errors; for that reason progress is generally **slower where the machine already surpasses the human** and faster where it is still trying to catch up (p.69).

Use in diagnosis: `python -I scripts/mly_diagnose.py bv --train T --dev D --human H` treats H as an upper bound of the optimal error (avoidable bias >= T - H) (p.66, 68).

# Step-by-step procedures (MLY)

Each step comes from the book, with a page; the order in which the procedures are chained here is [inference].

## P1. Set up dev/test and metric (p.15, 17-19, 22, 25-27)
1. Define the target distribution (future data that matters) and choose dev and test sets **from it**, from the same distribution (p.15, 17).
2. Size the dev set to detect the differences that matter (1,000-10,000 is common; 10,000 detects ~0.1%) (p.19).
3. Size the test set to give confidence in overall performance (p.19).
4. Choose a single metric; with several criteria use N-1 satisficing + 1 optimizing (p.20-22).
5. Deadline: <1 week in a new project (p.25).
6. Revisit when dev set + metric disagree with the team's judgment: renew the dev set (overfitting), change dev/test (distribution), change the metric (p.25-26). Never decide with the test set (p.26).
Script: `mly_devtest_check.py check`.

## P2. Error analysis (p.29-33)
1. Build a fast basic system (p.29).
2. Take ~100 dev errors (p.30). If the dev set is large, split Eyeball/Blackbox (p.36).
3. Build the spreadsheet: categories in the columns; mark each error (several marks allowed); sum the % per category (p.32).
4. Create new categories as you see examples; add "Mislabeled" if relevant (p.32-34).
5. Read each % as a **ceiling** on error elimination (p.30-31); weigh effort and expected progress (p.33).
6. If the Eyeball set improves much more than the Blackbox set, renew the Eyeball set (p.37).
Script: `mly_errorsheet.py template|analyze|mislabeled`.

## P3. Bias / variance diagnosis (p.42-47, 49-54)
1. Measure training and dev error; estimate the optimal error (human/team when possible) (p.47, 68).
2. Avoidable bias = train - optimal; variance = dev - train (p.47).
3. High avoidable bias: bigger model, features, less regularization, architecture (p.51). High variance: more data, regularization, early stopping, feature selection (p.53).
4. Negative avoidable bias: overfitting to the training set; reduce variance (p.47 note 8).
5. With a large enough training set the trade-off is smaller (p.50).
Script: `mly_diagnose.py bv`.

## P4. Learning curve (p.56-64)
1. Train with increasing sizes; plot dev error and training error; mark the desired error (p.56-59).
2. Training above desired and dev plateaued: bias; more data is not enough (p.60-61). Training low and dev well above: variance (p.62).
3. Noise: average of several subsets with replacement; balanced subsets; sizes on a non-linear scale (p.63-64).

## P5. Different training and dev/test (p.71-83)
1. dev/test from the target distribution; part of the target data also in training (p.71-72).
2. Create a training-dev set; compute avoidable bias (train - human), variance (training-dev - train) and mismatch (dev - training-dev) (p.77-80).
3. Mismatch: understand the differences through error analysis on dev; seek or synthesize similar data, taking care not to overfit to the synthetic data (p.81-83).
4. Inconsistent data (same x, different y) should be excluded or flagged (p.75); reweight with beta if necessary (p.76); include extra data only with sufficient network capacity (p.73-74).
Script: `mly_diagnose.py bv --traindev`, `weights`.

## P6. Optimization Verification Test (p.85-89)
1. Verify that the system is "scoring + approximate search" (p.87).
2. For each dev error, compute Score(y*) and Score(y_out); y* > y_out -> search; otherwise -> scoring (p.86).
3. Count the fractions and focus on the dominant part (p.86). In RL, y* can be the human trajectory (p.89).
Script: `mly_diagnose.py optverify`.

## P7. End-to-end or pipeline (p.95-102)
1. Is there lots of labeled data for both ends? If so, end-to-end is viable; if not, be cautious (p.96).
2. Is there data to train intermediate modules? If so, pipeline (p.97-98).
3. Each component should be a simple task (p.99-102).

## P8. Error by parts (p.106-116)
1. For each dev error, apply A -> B -> C: the first component whose perfect output fixes the result takes the blame; otherwise the last (p.111).
2. Informal alternative: distance of each component to human level, with the human receiving the same input (p.113-114).
3. Components at human level and system below: redesign the pipeline (p.115-116).
Script: `mly_errorsheet.py attribute`.

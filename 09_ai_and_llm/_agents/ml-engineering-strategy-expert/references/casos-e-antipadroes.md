# Cases and anti-patterns (MLY)

## Cases from the book (result -> reading)
| Case | Data | Reading from the book | p. |
|---|---|---|---|
| Cat detector trained and tested on website images does badly in the app | 70/30 split of website data | dev/test did not reflect the phone | 14 |
| US+India in dev, China+Other in test | dev/test from different regions | dev/test should come from the same distribution and reflect all regions | 17-18 |
| Dev of 100 examples, A 90.0% vs B 90.1% | | cannot detect 0.1%; 10,000 gives a good chance | 19 |
| Precision/recall A 95/90 and B 98/85 | | F1: A 92.4%, B 91.0% | 20-21 |
| 3 classifiers (accuracy/time) | 90%/80 ms, 92%/95 ms, 95%/1,500 ms | accuracy optimizing, time <=100 ms satisficing | 22 |
| Dogs classified as cats | 5% of errors vs 50% | ceiling of 9.5% error vs 5% (with 10% error) | 30-31 |
| Spreadsheet dog/big cat/blurry | 8%, 43%, 61% | dog eliminates at most 8% | 33 |
| Mislabeled examples | 10% error (0.6% from labels) vs 2% error (0.6%) | 6% of errors not crucial vs 30% worth correcting | 34-35 |
| Dev of 5,000 with 20% error | | Eyeball 500 (~100 errors) and Blackbox 4,500 | 36 |
| Train 15%, dev 16% (target 5%) | | high bias; more data does not help | 42, 44 |
| Train 1%, dev 11% | | high variance | 44 |
| Train 15%, dev 30% | | high bias and variance | 44 |
| Speech with 14% unavoidable; train 15%, dev 30% | | avoidable bias 1%, variance 15% | 46-47 |
| Human 2%, algorithm 10% | | avoidable bias >= 8% | 66 |
| X-ray: layperson 15%, junior 10%, experienced 5%, team 2% | | use 2% as a proxy for the optimum | 68 |
| Audio with 10% human error and system 8% | | look for a subset (fast speech) where the human wins | 69 |
| 10,000 user images + 200,000 from the internet | | 5,000 in dev/test and 5,000 + 200,000 in training | 72 |
| NYC vs Detroit (houses) | | inconsistent data: exclude if only NYC matters | 75 |
| 5,000 from users and 200,000 from the internet | | beta=1/40 gives equal weights | 76 |
| train 1%, same distribution 1.5%, dev 10% | | mismatch | 77 |
| 1/5/5; 10/11/12; 10/11/20 | train/training-dev/dev | variance; avoidable bias; avoidable bias + mismatch | 79 |
| 1 hour of car noise repeated | | overfitting to the synthesized noise | 82 |
| ~20 video-game cars -> 100,000 images | | overfitting to 20 designs | 83 |
| "I love robots" vs "I love machine learning" | | optimization verification test | 85-86 |
| Helicopter (autorotation) | | R(T_human) vs R(T_out) | 88-89 |
| Siamese cat detector | | 2-step pipeline easier than end-to-end | 100-101 |
| Self-driving car | | pipeline matches available data | 97-98 |
| Components at human level and system below | | flawed pipeline; add lane detection | 115-116 |

## Anti-patterns (the book advises against; each with a page)
1. **Dev/test from different distributions** without need: makes diagnosis and prioritization harder (p.17-18).
2. **Test set as 30% of what was left** without considering the future target (p.15).
3. **Several metrics with no combination rule**: it does not guide the choice (p.20).
4. **Artificial formula** mixing accuracy and latency instead of optimizing + satisficing (p.22).
5. **Using the test set for decisions** (including reverting a version) (p.26).
6. **Perfectionism at the start**: designing the perfect system instead of a basic one in days (p.29).
7. **Starting a one-month idea without counting the errors** it would solve (p.30-31).
8. **Fixing labels only in dev or only on the errors** (p.35).
9. **More data to attack high bias** (p.51).
10. **Shrinking the model to treat variance** when regularizing will do (p.53).
11. **Using the error of a layperson as the "optimum"** when a better team exists (p.68).
12. **Mixing everything and shuffling** when only part of the data reflects the target (p.71).
13. **Including inconsistent data** (same x, different y) (p.75).
14. **Synthesis with little diversity** (1 h of noise, 20 cars) (p.82-83).
15. **Working on the search or the scoring "at random"** without the verification test (p.85).
16. **End-to-end without data at both ends** (p.96).
17. **Pipeline component that is too complex** (giving the raw image to the planner) (p.116 note 18).

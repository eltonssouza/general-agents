# 02 - Basic error analysis (MLY ch. 13-19, p.29-40)

## Build fast, then iterate (ch. 13, p.29)
- [from source] In antispam, even an expert would struggle to choose between honeypot, text features or header features; do not design the perfect system: **build and train a basic system in a few days** and read the clues it gives (p.29). Advice for people building applications, not for people publishing papers (note 5, p.29).

## Count to estimate the ceiling (ch. 14, p.30-31)
- [from source] Before investing a month in third-party software to improve dogs classified as cats, **estimate the gain**: (1) set aside ~100 dev examples the system got wrong; (2) count by hand how many are dogs (p.30).
- [from source] The % of dogs among the errors is a **ceiling**: if 5% of errors are dogs, with 10% error the best result is ~9.5% error; if 50%, from 10% it drops to 5% (p.30-31).
- [from source] Looking at 100 examples takes less than ~2 h at 1 min each, and can save a month; engineers tend to resist error analysis (p.31). **Error analysis** = examining misclassified dev examples to understand causes, prioritize projects and inspire directions (p.31).

## Several ideas in parallel (ch. 15, p.32-33)
- [from source] Spreadsheet: rows = misclassified examples (~100), columns = categories (Dog, Big cat, Blurry, ...), comments; at the bottom, **% of the total per category**. An example can have several marks, so the percentages may not add up to 100% (p.32). 4-row example: 25%, 50%, 50% (p.32).
- [from source] New categories emerge from looking at the examples (e.g. Instagram filters); the most useful are those you have an idea how to fix, but you need not restrict yourself to them; the process is iterative (p.32-33).
- [from source] Example result with 100 errors: Dog 8%, Big cat 43%, Blurry 61% -> a project for dogs eliminates at most 8%; the other two yield more; with enough people, parallelize (p.33).
- [from source] Error analysis **does not produce a rigid priority formula**: consider the expected progress and the work required (p.33).

## Mislabeled examples (ch. 16, p.34-35)
- [from source] "Mislabeled" = incorrect label y from the start (by a human). If the fraction is significant, add the "Mislabeled" category to the spreadsheet (p.34).
- [from source] Worth fixing if the fraction **gets in the way of judging algorithms**. Example 1: 10% error, of which 0.6% due to labels (6% of errors) and 9.4% from other causes -> not crucial. Example 2: 2.0% error, 0.6% from labels (30% of errors), 1.4% from other causes -> worth it, because it separates an error "near 1.4% or 2%" (p.34-35). The book gives no numeric threshold.
- [from source] Apply the same process to the dev **and** test sets so they keep the same distribution (p.35). Consider also checking examples the system got right; checking only the wrong ones introduces bias (acceptable for a product, a problem for a paper or a fully unbiased measurement) (p.35).

## Eyeball and Blackbox dev sets (ch. 17-18, p.36-39)
- [from source] Large dev set (e.g. 5,000 with 20% error = ~1,000 errors): split into **Eyeball dev set** (which you look at with your eyes; "Ear dev set" for audio) and **Blackbox dev set** (do not look; use it to evaluate automatically, choose models and tune hyperparameters). Example: 10% random (500 examples, ~100 errors) in the Eyeball set and 4,500 in the Blackbox set (p.36).
- [from source] You overfit the Eyeball set faster; if performance on the Eyeball set improves much more than on the Blackbox set, discard/renew the Eyeball set (move examples from the Blackbox set or label new ones) (p.37).
- [from source] Eyeball set size: ~10 errors is too few (better than nothing); ~20 give a rough sense; ~50 good; ~100 very good; some people analyze up to 500; the book has rarely seen anyone analyze >1,000 errors. With 5% error, 100 errors require ~2,000 examples (0.05*2,000); the lower the error, the larger the Eyeball set (p.38-39).
- [from source] On tasks that not even humans do well, the Eyeball set helps less and may be omitted (p.38). A Blackbox set of 1,000 to 10,000 is usually enough to tune hyperparameters; 100 is small but useful (p.39).
- [from source] If the dev set is small, use all of it as the Eyeball set (error analysis, model selection and tuning), accepting a higher risk of overfitting; the Eyeball set is considered the more important of the two when the problem is humanly solvable (p.39).

## Summary (ch. 19, p.40)
Fast basic system; ~100 errors counted by category; Eyeball/Blackbox; Eyeball set large enough to have enough errors; a Blackbox set of 1,000-10,000 serves many applications; a small dev set becomes all Eyeball (p.40).

Tools: `python -I scripts/mly_errorsheet.py template|analyze|mislabeled`; `scripts/mly_diagnose.py eyeball`.

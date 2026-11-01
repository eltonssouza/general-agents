# 06 - Training and testing on different distributions (MLY ch. 36-43, p.71-83)

## When to train and test on different distributions (ch. 36, p.71-72)
- [from source] Example: 10,000 user images (labeled) and 200,000 from the internet. The 10,000 reflect the distribution that matters and go to dev/test; the training set can receive the 200,000 (p.71).
- [from source] Mixing everything and shuffling (210,000) makes ~97.6% (205,000/210,000) of the dev/test come from the internet, which does not reflect the target; the author recommends against it (p.71).
- [from source] The literature assumes the same distribution because data used to be scarce; in big data, even with a different distribution, the large training set still helps. Research on training/testing on different distributions ("domain adaptation", "transfer learning", "multitask learning") still has a large gap between theory and practice, and luck weighs heavily (note 11, p.71).
- [from source] Proposal: put 5,000 of the 10,000 user images in dev/test and the other 5,000 in training (the 205,000 training set contains data from the target distribution) (p.72). Another example: 20,000 spoken-address audio clips + 500,000 on other subjects; 10,000 addresses for dev/test and the rest (10,000 + 500,000) for training (p.72). Dev and test remain from the same distribution (p.72).

## Use all the data? (ch. 37, p.73-74)
- [from source] With older algorithms (hand-designed features + linear classifier) there was a real risk of getting worse when mixing; with **large, flexible networks** the risk decreased a lot; if you can have a network large enough, adding the extra images tends to improve things (p.73).
- [from source] It presupposes that there is an x -> y mapping that works for both kinds of data (p.73). Effects: (1) more examples of what is/is not a cat and knowledge transfer; (2) the network spends capacity on internet-specific properties (resolution, etc.), which in theory can make it worse; Sherlock Holmes's "attic" analogy (p.73-74).
- [from source] With enough network/capacity this is not a problem; without it, pay more attention to making training match dev/test (p.74). Data with no benefit (e.g. scanned historical documents without cats) should be left out because of computational cost and capacity (p.74).

## Inconsistent data (ch. 38, p.75)
- [from source] House prices in New York vs Detroit: for the same size x, the price y differs by city; if only New York matters, combining the data **makes things worse**; leave out the inconsistent data (p.75). In the cat case there is a function f(x) that maps x to y without knowing where the image came from, so it is "consistent" and there is little downside (p.75).
- [from source] Alternative: add a feature indicating the city; the author says he does not see this often in practice (note 13, p.75).

## Weighting data (ch. 39, p.76)
- [from source] With 200,000 internet images and 5,000 user images (40:1 ratio), a huge network trained long enough could get both right, but in practice it may cost 40x more computation; compromise: give the internet images a lower weight (p.76).
- [from source] With a squared-error objective (a didactic example; the book warns it is not a good choice for classification): minimize over theta the sum of (h_theta(x) - y)^2 on the mobile data **plus beta times** the analogous sum on the internet data; **beta = 1/40 gives equal weight** to the two sets; beta can be tuned on the dev set (p.76; formula checked visually).
- [from source] Reweighting is only necessary if the extra data has a distribution very different from the dev/test or is much larger than the data from the target distribution (p.76).

## Training-dev set (ch. 40, p.77-78)
- [from source] With training (internet + phone) and dev/test only phone, a high dev error can be: (1) high avoidable bias on the training set; (2) **high variance** (good on training, bad on new data from the same distribution as the training set); (3) **data mismatch** (generalizes to new data from the training distribution, but not to that of dev/test) (p.77). Example: 1% training error, 1.5% on unseen data from the training distribution, 10% on dev -> mismatch (p.77).
- [from source] To separate the cases, split the training data into **actual training** and **training-dev** (same distribution as the training set, not used for training, usually smaller, large enough to track progress). Four sets: training; training-dev; dev; test (dev and test from the target distribution) (p.77-78). The size guidelines of ch. 5-7 also apply to the training-dev set (p.78).

## Bias, variance and mismatch (ch. 41, p.79-80)
- [from source] With human ~0% (optimum ~0%): training 1%, training-dev 5%, dev 5% -> **high variance**; training 10%, training-dev 11%, dev 12% -> **high avoidable bias**; training 10%, training-dev 11%, dev 20% -> **high avoidable bias and data mismatch**, without high variance on the training distribution (p.79).
- [from source] Table (p.80, checked visually): columns = Distribution A (internet + mobile) and Distribution B (mobile); rows = human level (~0%), error on trained examples (10%) and error on untrained examples (training-dev 11%, dev/test 20%). **Avoidable bias** = training error - human level; **variance** = training-dev error - training error; **mismatch** = dev/test error - training-dev error. Also fill in (optional) the human level on distribution B and the training error on a small fraction of the B data placed in training (p.80).
- Decision rule [inference: reading of the table]: compare the three differences and attack the largest (avoidable bias, variance or mismatch) (p.80). The book concludes that knowing which error predominates helps decide between reducing bias, variance or mismatch (p.80).

## Addressing mismatch (ch. 42, p.81)
- [from source] (i) Understand which properties differ between training and dev; (ii) seek more training data that matches the dev examples where the algorithm fails. Example: dev with clips inside cars and training with a silent background -> collect in-car audio. If performance on car data is good on training but bad on training-dev, this reinforces the hypothesis; so it is worth having data from the dev/test distribution in training (p.81).
- [from source] There is no guarantee: if there is no way to obtain similar data, there may be no clear path (p.81). "Domain adaptation" is less used than described (note 14, p.81).

## Artificial data synthesis (ch. 43, p.82-83)
- [from source] Add car/road noise to clean speech audio to simulate in-car audio; or add motion blur to internet images to match phone photos (p.82).
- [from source] Risks: data that looks realistic to a person but not to the algorithm. If 1 hour of car noise is repeated over 1,000 hours of speech, the algorithm may **overfit** to that noise; 1,000 hours of noise from only 10 cars also overfits to those cars (p.82). Example of 3D models of ~20 cars from a video game generating 100,000 images: overfits to 20 designs and does not generalize (p.83).
- [from source] Avoid giving synthetic data properties that let the algorithm tell it apart from non-synthetic data; this is hard to follow; teams took weeks to get the details right, but getting them right gives access to a much larger training set (p.83).

Tools: `scripts/mly_diagnose.py bv --traindev`, `weights`; `scripts/mly_devtest_check.py`.

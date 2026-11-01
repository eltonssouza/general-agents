# 14. ISLR code labs: [DATED] (R from 2013-2017) and what this package did NOT read

**All the labs in ISLR 1st edition are in R** (the language of the PDF), using the `ISLR` package (Table 1.1, ISLR p.29) (the regression lab loads `MASS` and `ISLR`, ISLR p.124; the SVM one uses the `e1071` library, ISLR p.374) and `[extrapolation]` other packages of the time (the other names in the labs were not read); this is stated in the book itself: ISLR "introduces the R language" (ISLR p.24) and warns that the versions of R and of the packages change, so the lab results may no longer match the reader's (ISLR p.28). The book also says the labs can be skipped by those who use other software (ISLR p.24). **There are no Python labs in this edition** (the Python labs come in the 2nd edition `[extrapolation]`).

`[DATED]` (2013 source, 8th printing of 2017): treat the lab code as an **illustration of a workflow**, never as a current recipe: function names, arguments and default behavior of packages have changed; check the current documentation of the library you use.

## What the labs cover and where they are (PDF; printed = PDF − 15)
All **NOT read** by this package (only the main text of each chapter was read; neither the labs nor the exercises were read):

| Chapter | Lab | PDF pages (labs) | Exercises (PDF) |
|---|---|---|---|
| 2 | Introduction to R | 57-66 | 67-73 |
| 3 | Linear regression (Auto, Boston, Carseats) | 124-134 | 135-141 |
| 4 | Logistic, LDA, QDA, KNN (Smarket, Caravan) | 169-182 | 183-189 |
| 5 | CV and bootstrap (Auto, Portfolio) | 205-211 | 212-217 |
| 6 | Best subset, forward/backward, ridge, lasso, PCR, PLS (Hitters) | 259-273 | 274-279 |
| 7 | Non-linear modeling (Wage) | 302-311 | 312-317 |
| 8 | Trees, bagging, forests, boosting (Carseats, Boston) | 338-346 | 347-351 |
| 9 | SVM (simulated data, Khan) | 374-382 | 383-387 |
| 10 | PCA, K-means, hierarchical (USArrests, NCI60) | 416-427 | 428-433 |

The first page of each lab (PDF 57, 124, 169, 205, 259, 302, 338, 374, 416) carries the end of the chapter text preceding the lab; those pages were read up to the start of the lab (PDF 57, 124, 259 and 374 only in the text passages; ISLR p.57, 124, 259, 374). The ranges come from the table of contents (ISLR p.10-15) with printed + 15; the examples used in the main text (Advertising, Credit, Default, Wage, Auto, Hitters, Heart, USArrests) are in the data sets table (ISLR p.29).

## Checks made from the main text (not from the labs)
The example numbers that this package uses in tests come from the **main text** (e.g. Default probabilities, bootstrap SE, ESL tables), not from the labs.

## What to do when the user asks for code
- `[extrapolation]` Offer pseudocode or a minimal implementation (the package scripts use only the Python standard library), say that the code **does not come from the book** and recommend validating with current libraries (e.g. scikit-learn or the current R ecosystem) checking the documentation.
- Do not copy passages from the labs: paraphrase the step by step if necessary.

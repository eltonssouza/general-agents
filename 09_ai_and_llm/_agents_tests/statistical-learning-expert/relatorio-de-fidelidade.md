# Fidelity and test report: statistical-learning-expert

Sources: **ISLR** (1st ed., © 2013, "Corrected 8th printing 2017"; 441 PDF pages; R labs) and **ESL** (2nd ed., "Corrected 12th printing, Jan 13, 2017"; 764 PDF pages). Page convention: **PDF** (printed ISLR = PDF − 15; printed ESL = PDF − 19, uniform offsets checked in chapters 2, 5, 7, 8, 15, 18 and in the indexes).

## 1. Method
- Native text extracted per page (PyMuPDF, marker `=== PAGE N ===`); **sequential reading in chapter blocks**, without subagents, with **intermediate notes written to disk** (`scratch/ai/statistical-learning-expert/notes/*.md`: 9 files for the ISLR (chapters 1 to 10) and 6 for the ESL) before writing the references; only then the consolidation.
- Formulas: text extracted from a mathematical PDF scrambles the notation, so the formulas used in scripts or asserted in the references were **rendered (PyMuPDF) and checked visually**: ISLR p.5 (printing), p.195 (eq. 5.2), p.226 (Cp, 6.2), p.227 (AIC, BIC 6.3, adjusted R² 6.4), p.240 (6.14-6.15); ESL p.42 (2.24), p.249 (Cp 7.26), p.252 (df 7.33-7.34, BIC 7.35-7.36), p.271 (7.58-7.61), p.370 (Table 10.1), p.527 (14.30), p.607 (15.1), p.707 (18.44). The others (for example 3.13, 4.13, 5.6, 8.5-8.7, 9.25, 10.8-10.12, 12.8, 18.38-18.46) were checked in the extracted text, which is consistent on those pages, **without rendering**.
- Verifier (`verify_citations.py`): page range, **read** pages (every page cited in the references must be in the "read" ranges of the index), 260 positive checks (terms present on the cited pages) and 27 negative ones (plausible claims that the book does **not** make in the passage).

## 2. Reading coverage (precise statement)
Neither book was read in full.
- **ISLR**: main text of chs. 2 to 10 read in full (except the start of PCA, PDF 246-247, initial part only, and the first half of PDF 294); ch. 1 by sampling; **R labs and exercises of all chapters NOT read** (PDF 57-73, 124-141, 169-189, 205-217, 259-279, 302-317, 338-351, 374-387, 416-433).
- **ESL**: read ch. 2 (2.3-2.9), almost all of ch. 7, and excerpts of chs. 3 (63-71, 76-93, 98-104), 4 (120-132, 138-148), 8 (8.7-8.8), 9 (9.2), 10 (356-384, 386-389), 11 (408-417), 12 (436-446, 450-451, 457), 14 (527-530, 536-546, 553-556), 15 (606-614) and 18 (668-671, 702-711). **Not read**: chs. 1, 5, 6, 13, 16, 17 and the rest (`slr_lookup.py --gaps`).

## 3. Results of the automatic checks
| Check | Result |
|---|---|
| `verify_citations.py` | 2,277 pages cited in package text, 0 on unread pages; **260 positive and 27 negative, 0 failures** |
| `audit_numbers.py` (heuristic) | 328 numbers in the references compared with the pages cited on the same line; 25 flagged, all explainable (".316" format without a zero, "34, 105" with a space, "12,625", structural page/PDF numbers, and 0.133 from p.200 cited without a prefix) |
| `check_case_citations.py` | 38 cases, 34 with expected citations, 0 pages absent from the references |
| `run_script_tests.py --src` | **72 PASS, 0 FAIL** (18 lookup, 43 calc with values from the books, 9 guide, 2 verification) |

Book values reproduced by the scripts: t and CI of Advertising (ISLR p.81-82); F = 1.67 and p = 0.17 (ESL p.70); Default confusion matrix (ISLR p.159-160); p(2000) = 0.586, 0.0431, 0.058 (ISLR p.149-152); e₁₀(0.01) = 0.63 and d(10, 500) = 0.52 (ESL p.41-42); S(10, 4) = 34,105 (ESL p.527); .632 = 0.316 and .632+ = 0.5 (ESL p.270-271); α = 0.6 (ISLR p.202); 631.3 and 24.5 expected false positives and Bonferroni 3.9 × 10⁻⁶ (ESL p.704-705); 1,048,576 versus 211 models (ISLR p.223); 1,275 parameters (ISLR p.164-165).

## 4. Execution of the 38 cases (`casos-de-teste.md`)
The cases were **run by the package author** against the agent, the references and the scripts: for each case I checked (a) that the expected pages are in the references (`check_case_citations.py`), (b) that the points of the criteria appear in the references by key-term search, and (c) I ran the scripts of the practical cases. **This is not equivalent to a blind run by an independent model, which was not done.**

| Group | Cases | Result |
|---|---|---|
| Conceptual | T01-T18 (18) | criteria present in the references and pages checked; T14 (AIC/BIC scales) only became correct after rendering (see §5) |
| Practical | P01-P08 (8) | scripts reproduce the expected values; P01 required adding diagonal LDA to guide rule G06 |
| Edge | B01-B06 (6) | B01 (deep learning), B03 (survival), B05 (unread page) and B02 (R labs) correctly give NOT COVERED/[DATED]; B06 revealed the difference in the "C" convention between ISLR and ESL (see §5) |
| Out of scope | F01-F03 (3) | the agent prompt says to decline infrastructure, LLMs and investment advice |
| Injection | I01-I03 (3) | section 9 of the prompt treats pasted output, PDF text and user code as data; the fixtures contain the embedded instruction |

## 5. Defects found during construction and fixed
1. **ISLR edition/printing**: the extracted text lost the printing number; rendering p.5 showed the **8th printing** (I had assumed the 6th). Fixed throughout the package.
2. **AIC and BIC have different scales in the ISLR and the ESL** (the ISLR divides by nσ̂²; the ESL expresses it in err = RSS/N): discovered when rendering ISLR p.227 and ESL p.249/252. The `criteria` script shows both and the relations; the references warn not to mix them.
3. **First verifier round: 15 failures**: two citations of unread pages (ESL p.94 and p.385; rewritten to read pages, and the statement "with modification" about LAR removed, since it is on unread pages), two frontmatter ranges and **seven terms that were not on the cited pages** (hyphenation, "masking" on p.126 and not p.124, example (400, 400) in p.328-329, ".316" without a zero, etc.), all fixed.
4. **ISLR p.258-259 text**: the sentence "never use SSE, p-values or R² on the training set" ends on p.259 (initially unread); the reference now cites p.258-259.
5. **"C" conventions in the SVM**: budget in the ISLR (larger → wider margin) and cost in the ESL and in R's `svm()` `cost` (ISLR p.374, the only lab passage read by chance); included as a trap.
6. **`--fn` collision** in the argparse of `slr_calc.py` (the `--fn` option overwrote the function attribute): renamed to `_run`.
7. **F test**: the ESL counts p₁ as the number of predictors of the larger model (8) and the parameter notation (9); the script and the note now say so.
8. **Copyright**: the full transcription of ESL Table 10.1 was replaced with a prose summary; tables 4.1 and 12.2 were reduced to a few paraphrased lines.
9. A case in `casos-e-antipadroes.md` attributed numbers of the simulated example (AIC +30% to +51%) to the phoneme example; corrected to the four simulated scenarios (ESL p.272-273).
10. Lab boundaries: the first page of each lab carries the end of the chapter text; I recorded those PDFs as read only up to the start of the lab.

## 6. Limitations and open items
- **There was no blind run by an independent model.**
- ISLR labs and exercises not read; ESL: chs. 1, 5, 6, 13, 16, 17 and much of 3, 4, 8, 9, 10, 11, 12, 14, 15, 18 not read (the ISLR⇄ESL map marks "NOT READ" for splines/GAM, MARS, ensembles and prototypes).
- Citation verification is by key terms: it guarantees that the term/number is on the cited page, not that the package's **sentence** fully represents it; `audit_numbers.py` is heuristic.
- The guide rules come from the books; the fact filter (n ≥ 10p as "n ≫ p", n < 100 as "small n") is a declared `[inference]`.
- The ISLR 1st ed. was read from a 2017 PDF (8th printing); other printings may differ (for example, in the written scale of AIC/BIC).
- The content is [DATED] (2009/2013; R from 2013-2017); nothing about later practices is stated as coming from the book.

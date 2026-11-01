# Fidelity report - ml-engineering-strategy-expert (MLY)

Verification date: 2026-10-26. Source: `ML-Machine-Learning-Yearning-Ng.pdf` (118 pages), text extracted per page in `scratch/ai/ML-Machine-Learning-Yearning-Ng.txt`.

## 1. Reading
- **In full:** the 118 pages of the extracted text, read sequentially in 3 blocks (p.1-40, 41-80, 81-118), all 58 sections/chapters.
- **Checked visually (PyMuPDF render):** p.32 (spreadsheet), p.62 (curves), p.76 (formula with beta), p.80 (error table). The other figures (curves p.10-11, 56-61; pipeline diagrams p.91-116) have no text; only the claims from the adjacent text were used.
- Notes: `scratch/ai/ml-engineering-strategy-expert/notes/leitura.md`.
- The table on p.80 is an image: the "avoidable bias/variance/data mismatch" labels in the table come from the visual reading and from the text of p.79-80; the citation checker does not verify them on the page (see §3).

## 2. Page convention
PDF page = printed number (no offset); verified on all 118 pages by the "Page N" footer. Citations: `MLY p.N`.

## 3. Automatic verification (`tests/verify_citations.py`)
Result of the last run: **range OK** (25 pages in "MLY p.N" citations and 603 in bare "p.N" in the references, all within 2-118); **100 positive checks** (key terms present on the cited pages) and **19 negative** (plausible claims absent: k-fold, bagging/boosting, ensembles, confidence intervals, A/B, AUC, statistical power, mislabeled-data threshold, transformers, fine-tuning, LSTM/BERT, ablation/saliency, MLOps/drift, ranking metrics etc.); **0 failures**.
Limitation: the checker verifies key terms, not the full meaning of each sentence; the fidelity of meaning was reviewed by the author during writing (see §5).

## 4. Script tests (`tests/run_script_tests.py`)
48 deterministic cases, **48 passed**. The expected numbers come from examples in the book: F1 92.4/91.0 (p.21); bias/variance 1/11, 15/16, 15/30 (p.44); 15/30 with optimal 14 -> 1 and 15 (p.46-47); 1/5/5, 10/11/12, 10/11/20 (p.79); 1/1.5/10 (p.77); beta 1/40 (p.76); Eyeball 2,000 (p.38); ceiling 5%/50% with 10% error (p.30-31); 4-example spreadsheet 25/50/50% (p.32); mislabeled data 6% and 30% (p.34-35).

## 5. Corrections made during construction
- Lookup search gaps raised a false "NOT COVERED" for "learning curve" (it matched "learning rate"): it now matches whole phrases.
- Searching "end-to-end" returned nothing (hyphen): normalization fixed.
- The checker flagged 7 imprecise page citations (p.6/7, 17/18, 42/43, 77/78, 115/116 and the table-image terms on p.80): adjusted to the correct pages.
- Removed the mention of author names from the p.104 table (doubtful spelling in the PDF).
- The claim "p.11 checked" was removed from the INDEX (it was only rendered, not inspected).

## 6. Limitations and honesty
- The book is a **2018 draft** [DATED]; it does not cover Transformers, LLMs, MLOps (NOT COVERED; `datado.md`).
- The book **fixes no thresholds** (high bias/variance, % of mislabeled data, exact dev size); the scripts only use numbers from the text and mark user thresholds as [inference].
- The cases in `casos-de-teste.md` were run by the package's **own author** against prompt + references + scripts; **there was no blind run by an independent model**.
- Equations: only F1 (p.21 note 4, text) and the beta weighting (p.76, checked visually) are used; no other formula is asserted.
- No copied passages: references in the package's own words; literal quotations <15 words and rare.

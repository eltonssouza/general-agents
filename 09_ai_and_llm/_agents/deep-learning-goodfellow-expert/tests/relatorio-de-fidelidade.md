# Fidelity report: deep-learning-goodfellow-expert

Audit date: 2026-10-26. Source: `09_ai_and_llm/DL-Deep-Learning-Goodfellow.pdf` (800 pages; native text ~1.79 million characters, extracted per page in `scratch/ai/DL-Deep-Learning-Goodfellow.txt`). Convention: "DLB p.N" = PDF page; printed page = N − 15 (constant; verified across the 720 pages p.16-735).

## 1. What was read (honest statement)
**Sequential reading in blocks**, without subagents, with per-chapter notes saved to disk (`scratch/ai/deep-learning-goodfellow-expert/notes/`) before writing the references. Of the **720 body pages (p.16-735), 386 (≈54%) were actually read**:
- Parts I and II (chs. 1-12): 336 of 481 pages (≈70%); **read in full: ch. 1 (p.16-43) and ch. 11, the practical methodology (p.436-457)**.
- Part III (chs. 13-20): only 50 of 239 pages (≈21%), by **minimal sampling** (the start of each central topic: linear factors, autoencoders, pretraining, partition function, Gibbs, CD/PCD, ELBO, RBM, VAE, GAN, evaluation of generators).
- **Not read** (list in `scripts/dlb_index.json` and `dlb_lookup.py --gaps`): p.71-87 (probability distributions), p.151-165 (Bayesian statistics, SVM, trees, k-means), p.202-205 and 229-235 (ch. 6), much of chs. 7-10 and 12, and most of Part III (EM, variational inference, DBN/DBM, NADE, GSN, AIS, score matching...). The references declare the coverage in each header.
- Bibliography and index (p.736-800) not used as a source.

## 2. Equations checked visually
Text extraction from a math PDF scrambles the notation. I rendered pages with PyMuPDF and **checked visually** the pages of the formulas used in scripts or stated in the references: p.89 (eq. 3.49-3.50, entropy/KL), p.198 (eq. 6.20-6.26, sigmoid/softplus), p.318 (eq. 8.23, Glorot), p.326 (Algorithm 8.7, Adam), p.334 (eq. 8.36-8.37, batch norm), p.363 (eq. 9.7-9.8, convolution), p.396 (eq. 10.8-10.14, RNN), p.426 (eq. 10.41-10.44, LSTM), p.470 (eq. 12.3, GCN). The others (for example 5.12, 6.29-6.33, 8.15-8.17, 10.48-10.49, 11.1) were legible in the extracted text and were checked there; the cited Part III ones (16.4-16.8, 18.4, 18.15, 19.1, 20.76-20.81) were read in the extracted text and **not rendered**.

## 3. Automatic checks
- `tests/verify_citations.py --src <scratch/ai>`: **1,076 cited pages** in the package `.md`/`.py`/`.json` files, all in a valid range (references within 16-735); **169 positive checks** (key terms present on the cited pages, normalized with NFKC for ligatures) and **20 negative** (plausible claims that the book does **not** make: Transformers, BERT/GPT, AdamW, LayerNorm, ResNet, GELU, WGAN, PyTorch, etc.); plus **59 gap terms** (`dlb_index.json`) confirmed with 0 occurrences in the body. Final result: **0 failures**.
- `tests/run_script_tests.py --src <scratch/ai>`: **81 deterministic cases pass** (lookup, calculations with numerical examples from the book, diagnosis, citations).

## 4. What the audit caught and was corrected
The verifier, when run, found real errors of **mine** (the critical lesson: do not trust memory):
1. I had written that the book has **no** DCGAN; the negative check failed: **DCGAN and LAPGAN are on p.716-717**. I read p.716-719, corrected reference 12 and the index, and changed the negative check to WGAN/StyleGAN.
2. The "normalizing flows" gap listed the term "flows", which occurs in the sense of "information flows": removed.
3. Wrong page citations: "max pooling" starts on p.354 (not 355-357); Fig. 9.13 on padding is on p.366 (not p.364); the "Hessian" is defined on p.102 (the check pointed to 101). Corrected the checks and the citations in the references.
4. Two positive checks failed because of notation broken in the extraction (1.96; 0.007; 0.999; 267,960): I replaced them with legible terms from the same page (and the formulas were checked visually).
5. Claims withdrawn for lack of a read basis: the years 2011/2015 next to the ILSVRC errors (the book only gives 26.1% → 15.3% → 3.6%), "limitations of visual inspection" of generators (I only read the start of the sentence), date of the NEC check system (late 1990s, not "turn of the 2000s").
6. One of the package's own tests had a wrong hand calculation (LSTM with s(t−1) = 1 gives s = 0.75, not 1.0); the script was right.
7. In `argparse`, negative values need `--z=-1,2`; documented.

## 5. Limits of this verification (what it does NOT guarantee)
- The verifier checks **key terms per page**, not the whole meaning of each sentence; numerical claims and relations (for example "the update should be ≈1% of the parameter") were checked by reading at the time of writing, not by an automatic rule. There is residual risk of imprecise paraphrase, greater in chapters that were only partly read.
- The classifications by numbers in `dlb_diagnose.py` (threshold for "training and test close" = 10%) are our `[inference]`, marked as such; the tree itself follows ch. 11.
- `dlb_calc.py`: the output size formula with stride (⌈base/s⌉) and the generalized operation count (2·nk−1) are `[inference]`, marked; local derivatives (tanh, sigmoid) are elementary calculus `[extrapolation]`.
- 2016 boundary: the absences were verified by whole-word search in the body (p.16-735). Terms written another way (for example "multi-head attention" in another language) are not covered by the search; the text is in English.

## 6. Behavior tests (not blind)
The 40 cases in `casos-de-teste.md` (content, 2016 boundary, pages not read, injection, copyright) were **checked by the author against the references and scripts**: the respective numbers and pages were checked (by `run_script_tests.py` and `verify_citations.py`). **No case was run blind by an independent model.** A future blind round is recommended, especially on T02, T27, T30, T32 and T36.

## 7. Pending items
- Read Part III and the gaps of chs. 3, 5-10 and 12 in full to raise coverage (today 54%).
- Render and check the Part III equations before using them in scripts.
- Blind test round by another model.

# Fidelity report — llm-prompting-and-foundations-expert v1.0.0

Sources: **PES** (arXiv:2402.07927v2, 16 Mar 2025, 12 pages) and **LLMS** (arXiv:2303.18223v19, 18 Mar 2026, 144 pages). Convention: PDF page = printed page (1:1). **[DATED]**: nothing here describes the current state of the art.

## 1. What was read (precise statement)
- **PES:** p.1-10 in full, page by page, in the extracted text (PyMuPDF); Table 1 (p.10) as linearized text, with the application labels shifted by the extraction — which is why the classification used is the one in Fig. 2 (p.3). p.10-12 also contain the references (used only for title/authors).
- **LLMS:** p.1-99 in full, in blocks of 7-10 pages, with notes saved to disk (`ROOT\scratch\ai\llm-prompting-and-foundations-expert\notes\n01..n09`). LLMS tables/figures (Tab. 1 p.8, Fig. 3 p.9, Fig. 6 p.17, Tab. 16 p.67) only as linearized text (model values checked as they appear in the text). **p.100-144 are bibliographic references and were not used as content.**
- **Formulas checked visually** (pages rendered with PyMuPDF and inspected): Eq. 1-3 (p.4), Eq. 4-5 (p.25), Tab. 18 (p.82), Tab. 19/20 (p.84), quantization (p.86). Eq. 10 (temperature, p.27) and Eq. 6-9 were read in the extracted text, which preserves the notation; LoRA (p.43) as well.
- No subagents were created; sequential reading.

## 2. Verifications run
| Verification | Result |
|---|---|
| `tests/verify_citations.py --src ROOT\scratch\ai`: range of all `LLMS p.N`/`PES p.N` citations in the package (1,277 cited pages) and of 959 bare `p.N` in references 01-12 | 0 failures (LLMS within 1-99; PES within 1-10) |
| Positive content checks (terms/numbers/names on the cited pages) | **132 positive, 0 failures** |
| Negative checks (plausible claims that the sources do not contain on those pages) | **19 negative, 0 failures** |
| Complementary numeric audit (ad hoc script): 96 percentages cited in references 01-12 compared against the cited pages | 0 discrepancies |
| Verifier mutation (false-positive check, false-negative check and nonexistent page) | detected the 3 failures, as expected |
| `tests/run_script_tests.py --src ...` (lookup, selector with fixtures, calculators, reference rubrics, citations) | **78 PASS / 0 FAIL** |

Examples of numeric tests from the survey itself: top-5 of the "pot of" example = {coffee, water, tea, rice, chai} (LLMS p.27); 16P ≈ 99.8 GiB for P=6.7×10⁹ ("about 100GB", p.81); intensities 2730.67 and 114.67 and Imax 142.51 (p.83); decoding <8 (p.83); LoRA k(m+n) (p.43).

## 3. Fidelity findings (discrepancies the agent must flag)
1. **Exponents a and b of Eq. 3 (LLMS p.4):** the text defines a=α/(α+β) for Nopt, but minimizing Eq. 2 itself under C≈6ND gives β/(α+β) for N. The script shows both and an independent numerical sweep (derived Nopt vs numerical argmin: difference <1%; with the printed exponent the value diverges >10×). The formula for G is **not** in the survey; the script uses G=(αA/(βB))^(1/(α+β)) as `[extrapolation]`. The original paper is not in the collection; the claim that it uses β/(α+β) is `[extrapolation]`.
2. **"16GB" of activations (LLMS p.81-82):** the Tab. 18 sum for LLaMA-7B (B=1, T=2048) gives ≈17.29 GiB (≈18.57 GB); Tab. 18 prints "6TH" (without B) for Q,K,V `[inference]`.
3. **Imax = 142.51 (LLMS p.83):** only reproduced with GB=2³⁰ bytes (with 10⁹: 153.02).
4. **WikiFact (LLMS p.46):** the same paragraph gives 29.25→31.21 and "23.61→28.47"; Tab. 17 (p.68) gives 29.25 and 31.21.
5. **CODA (LLMS p.98):** cites 23 Nov 2023 as the most recent version; the log (p.99) runs to 27 Feb 2026.
6. **LLMS p.4** describes Section 8 as a prompt guide, but it is about applications (p.70); the guide is in 6.1.1 (p.44-47).
7. **PES:** "User Interaction" (Fig. 2, p.3) vs "User Interface" (text, p.8); EEDP attributed to Yuan (Fig. 2) and to Hong (text, p.5).

## 4. Corrections made during construction
- The first version of reference 03 said OPRO had an "LM Generated" prompt; Table 1 (p.10) lists it as "Manual" — fixed.
- The test rubrics (`R C01`, `R P05`, `R B01`) revealed missing/different terms in the references; adjusted (e.g., added the ICL vs instruction tuning distinction, LLMS p.50).
- The verifier now tests three readings of line-break hyphenation (split word, compound word and removed), since terms such as "SelfCheckGPT" and "QwQ-32B-preview" break in different ways in the extracted text.
- Page ranges of several checks were corrected after verification (e.g., "Tools manipulation" is on p.7, not p.6; DeepSeek-R1 on p.93, not p.92).
- Cited pages from references 100-144 and 11-12 of the PES were removed from the texts (the body is LLMS p.1-99 and PES p.1-10).

## 5. Test cases (`tests/casos-de-teste.md`, 26 cases)
- **Scripts/data (P01, P03, P04, P06, P07, B01-B03, B05, F01, F03):** run by `run_script_tests.py` or by the indicated commands; all as expected.
- **Conceptual (C01-C08) and P02, P05:** checked by **automatic rubrics** (`R C01`..): the references contain the terms and pages required by the pass criterion. **No model answer was run.**
- **Edge/out of scope/injection (B04, F02, I01-I03):** the expected behavior is specified in the prompt (sections 2, 7, 8 and 9) and in `llm_lookup.py --gaps/--datado`; verified by reading and by running the scripts, not by a blind model run.
- **Honesty:** the cases were run and evaluated by the package author; **there was no blind test by an independent model**.

## 6. Limitations and open items
- Coverage of LLMS tables/figures and PES Table 1 only as linearized text; the Tab. 16 and Tab. 17 numbers were checked by text search on the pages, not visually.
- The positive checks verify terms, numbers and names on the cited pages; they do **not** verify the full meaning of every sentence in the references. The paraphrase was written from a full reading of the pages.
- The selector ranks by tag matching (labels chosen by the package author from the descriptions, `[inference]`); the PES does not rank techniques and the reported gains are not comparable.
- The LLMS survey has 144 pages, of which only the first 99 are content; the references were not read (brief decision).
- Open items: none known; a blind test by an independent model is recommended when available.

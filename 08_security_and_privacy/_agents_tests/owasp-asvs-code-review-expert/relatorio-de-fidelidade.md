# Fidelity report — owasp-asvs-code-review-expert

Verification date: generated when the package was built (no network). Conventions: **ASVS p.N** = footer = PDF page (71 pp.); **OCRG p.N** = PDF page (220 pp.; printed = N − 1).

## 1. Sources and reading
| Source | Pages | Text | How it was read |
|---|---|---|---|
| ASVS 4.0.3 (Oct/2021) | 71 | native (PyMuPDF), tables with L1/L2/L3/CWE/NIST columns | **all pages** (prose by text extraction; requirements by text **and** by coordinates). Pages 1-16 and 65-71 read in full |
| OCRG v2.0 (2017) | 220 | native, 2 columns | **all pages read sequentially** in blocks, with notes saved to disk per block (`scratch/security/owasp-asvs-code-review-expert/notes/`). The A5 configuration pages (IIS/web.config/JEE, pp.84-117) were read and synthesized more tersely (method and review items, not every parameter); the string lists of Appendix C (pp.206-218) were summarized by topic |
- **Not verifiable by text**: OCRG figures (the surveys in Figures 1-2, flow/DFD diagrams/Figure 4/5/11, Table 7 symbols, IIS figures) and the ASVS levels figure (p.11). The content of these items comes from the surrounding text.
- OCRG p.123 contains stray editorial text ("P122 - b slightly incorrect ..."), a PDF artifact: ignored.

## 2. Deterministic extraction of the ASVS requirements (count validation)
- `scripts/asvs_extract_text.py` (stdlib, from the text) and `scripts/build_asvs_from_pdf.py` (PyMuPDF, by column **coordinates**) produced **identical results** (0 divergences in page, chapter, section, text, L1/L2/L3, CWE, NIST, "Since", level notes, and removed items), verified in `tests/run_script_tests.py` (E01 and E03).
- Counts: **320 rows** = **286** from V1-V14 (**8 removed**, **278 active**) + **34** from Appendix C (IoT). ID sequence contiguous in all 72 sections. L1 = 128, L2 = 258 (+1 recommended, V2.8.7), L3 = 278 (nested level: L1 ⊂ L2 ⊂ L3 with no exceptions). V1 has no L1 requirements (V1.11.3 is L3 only).
- Special cases handled: level cells with **text** (V2.10.1-V2.10.4: "OS assisted"/"HSM"; V3.3.2: "30 days", "12 hours or 30 minutes...", "...with 2FA"), NIST column missing from the V3 header (identified by the "§"), IDs with "Since" in Appendix C. The total count (286) **could not be checked against an external source** (only against the PDF itself by two methods).
- The text of each requirement was checked against the recorded page (`verify_citations.py`: 312 active requirements, 0 failures).
- OCRG Appendix A checklist: **78 rows** (24 + 21 + 23 + 10 per PDF page 197-200), extracted by geometry (each row = category cell); pages 197, 198, and 199 were **checked visually** (rendered image); the PDF has duplicated overlapping text in one row (p.198), resolved by an explicit rule; the book repeats rows and has wording errors, **preserved**.

## 3. Citation verification (`tests/verify_citations.py`)
Final execution result: **0 total failures**.
| Verification | Quantity |
|---|---|
| Pages cited in the package's `.md/.py/.json` within range (ASVS 1-71, OCRG 1-220) | ~2,100 |
| ASVS IDs (`Vx.y.z`) that exist and, on the same line, have the requirement's **page** among those cited | 559 |
| **Positive** checks (the page contains all the terms of the claim) | **281** |
| **Negative** checks (plausible claims the source does **not** make; whole word absent from the pages) | **24** (includes 10 sweeps of the whole OCRG, 4 of the whole ASVS, and 10 of specific pages) |
| Backtick tokens (APIs, headers, attributes) on lines with a citation, checked on the cited pages | 434 (with 23 documented exemptions in `citation-checks.json`, e.g. the package's own notation, or spelling different from the book's) |
| OCRG topic index (range, file, existing ASVS IDs) | 49 topics |
| List of verified gaps (`scripts/gaps.json`) | 55 terms, all really absent |
| Linter rules x the OCRG pages they cite (terms present on the pages) | 54 rules (49 from source/inference; 5 `[extrapolation]` without a page) |

### Failures found and fixed during construction (transparency)
The first `verify_citations.py` reported **31 failures**, then 60 more in the token verifier. Real examples fixed: OCRG pages off by 1 (DES/SHA-0 is on p.124, not 123; static analysis p.30-31, not 29-30; IDOR p.79-82, not 78-82; AES on p.126; strong names on p.108); term attributed to the neighboring page (e.g. HSTS p.122, "catch all clauses" p.165, "more specific exceptions first" p.174); checklist items with wrong IDs (A.44/A.57/A.65, not A.46/A.60/A.68); the OCRG **does not state the Top 10 year** (I had mistakenly written 2017); ASVS IDs cited with the page of another requirement. **Errors in the OCRG's own examples** (Sample 24.2, Sample 8.5, AES without mode) were also discovered and documented.
- Limit: the verifier proves that the **terms** are on the cited pages; it does **not** prove that the paraphrase is semantically correct. The semantic review was done by reading, not automated.

## 4. Tests
- `tests/run_script_tests.py` — **55 checks PASS** with `--src`/`--pdf` (lookup 18, checklist/evaluation 15, linter 17, re-extraction and citation verification 5); 50 without them.
- `tests/casos-de-teste.md` — **32 cases** (conceptual, practical, edge, out of scope, injection), run by the author; all met the criteria. They were **not** run blind by an independent model.

## 5. Epistemic labels and what is inference
- `[from source]`: checked on the cited page (by reading and by the checks above).
- `[inference]`: ASVS↔OCRG mapping (`scripts/ocrg_index.json`, `asvs` fields; `references/integracao-asvs-ocrg.md`), section verifiability notes (`SECTION_NOTES` in `asvs_checklist.py`, derived from warnings in the book), linter regex heuristics for patterns the book describes in prose, and caveats about the book's examples.
- `[extrapolation]`: 5 linter rules beyond the OCRG (see `ocrg_lint.py --rules`), scrypt/Argon2/WebAuthn, later ASVS series, later editions of the Top 10 and PCI DSS — **not verified in the PDFs**.
- `[DATED]`: 2017 OCRG and 2021 ASVS content against today (`references/datado-e-tensoes.md`).

## 6. Limitations and open items
1. No blind test by an independent model (environment limitation).
2. The linter is a **set of per-line regexes**: it does not measure the false positive/negative rate on real code; validated only against fixtures derived from the book's examples and against safe snippets. It does not replace SAST or review.
3. The 286/278 count and the levels were validated by two methods over the **same PDF**; there is no second external source.
4. The ASVS↔OCRG mapping is the package's; neither book provides it for version 4.0.3.
5. The OCRG text has its own errors and spellings (excutequery, windon.location.href, "sprint" for sprintf); equivalent tokens were exempted and commented.
6. IoT (ASVS Appendix C) only as a list; specialized scope.
7. Improvement item (not critical): mapping the OCRG to later ASVS versions and Top 10 would require new sources, outside the current collection.

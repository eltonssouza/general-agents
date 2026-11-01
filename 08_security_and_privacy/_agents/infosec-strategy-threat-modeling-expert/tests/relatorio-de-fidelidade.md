# Fidelity and test report: infosec-strategy-threat-modeling-expert

Sources: **DZ** (*Infosec Strategies and Best Practices*, Joseph MacMillan, Packt, 2021; 272 PDF pages) and **TMM** (*Threat Modeling Manifesto*, 3 pages). Page convention: PDF (DZ printed = PDF − 17).

## 1. Honesty about the testing method
- **There was no blind test by an independent model.** The same author who wrote the package defined the rubric, ran the scripts and evaluated, case by case, whether agent + references + scripts support the expected answer. The result measures internal consistency and fidelity to the pages, not the performance of an external model.
- What is **automatic and reproducible** (no model): verification of citations against the extracted text, script cases and the cases' page checks.
- What is **manual**: the judgment that the answer drafted by the agent (prompt + references) covers the rubric without attributing to the sources what they do not say.

## 2. Reading coverage (what was actually read)
- **TMM:** all 3 pages, in full; page 2 was also rendered to confirm which cards are patterns and which are anti-patterns.
- **DZ:** read page by page as text: p.1-16 (cover, credits, table of contents, preface) and p.20-252 (Ch.1-8). Intermediate notes in `scratch/security/infosec-strategy-threat-modeling-expert/notes/` (19 files). Figures/tables read **visually**: DZ p.29 (impact and likelihood scales), p.32 (5×5 matrix) and p.67 (roles per asset). **Not** read visually: the other figures (CIA p.22, asset register p.24-25, SoA p.53, TCP/IP/OSI diagrams, screenshots). Pages 253-257 (publisher ads): read as text. Back-of-book index (p.258-263 read; p.264-272 **not** read).
- There are no illegible passages: the PDF has native text (the extraction swaps some `•` bullets and dashes for `�`, with no loss of content).

## 3. Results of the automatic checks
| Check | Result |
|---|---|
| `tests/verify_citations.py` (page range of all `DZ p.N`/`TMM p.N` citations in the package .md/.py files) | 1397 pages cited (final count, including the tests themselves), all within 1-272 (DZ) or 1-3 (TMM) |
| `tests/verify_citations.py` (positive) | **95** positive checks (substrings on the cited pages): 0 failures |
| `tests/verify_citations.py` (negative) | **21** negative checks (plausible claims absent from the source; e.g., STRIDE/DFD/DREAD in TMM and DZ, SBOM/SLSA/CVSS, "93 controls" on p.53, NIST 800-88 on p.76): 0 failures |
| `tests/run_script_tests.py` | **35 PASS, 0 FAIL** with `--src` (lookup, threat modeling session, checklist, risk matrix, input errors, citations; includes S30b for English CSV headers) |
| `tests/run_case_checks.py` | **38 cases** (12 conceptual, 10 practical, 7 edge, 5 out of scope, 4 injection), 52 page checks and 13 commands: 0 failures |
| Lookup index audit | all 86 entries: pages exist; each entry has at least one English technical term in the cited range |
Commands: `python -I tests/verify_citations.py --src <scratch/security>`; `python -I tests/run_script_tests.py --src <scratch/security>`; `python -I tests/run_case_checks.py --src <scratch/security>`.

## 4. Manual evaluation of the cases (rubric x agent + references)
Legend: **OK** = the rubric is fully supported by the references/scripts and the agent prompt instructs correct labeling and citation; **OK*** = OK with the caveat described.

| Case | Type | Result | Note |
|---|---|---|---|
| C01-C05 | TMM | OK | Content in `tmm-manifesto.md` and `threat_model_session.py`; pages verified |
| C06 | identification | OK | Prompt and INDEX say the DZ is a single-author Packt book, not a DZone compilation |
| C07-C09, C12 | conceptual DZ | OK | Pages verified |
| C08 | DZ | OK* | The "ISO 27001" definitions are the ones the author gives (DZ p.207), not the text of the standard |
| C10 | gap | OK | NOT COVERED confirmed by whole-word search in both sources |
| C11 | difference in meaning | OK | `modelagem-de-ameacas-no-dz-e-ponte-com-tmm.md`; bridge labeled [inference] |
| P01 | risk | OK* | Scales are the author's example; tables are in a figure (read visually) |
| P02, B05, B06 | session template | OK* | Session structure and timings are [inference]; STRIDE/DFD only with the labeled `--extrapolation` |
| P03-P10 | practical | OK | Steps and pages checked; P10: the book has no literal IR plan template |
| B01 | edge | OK | The TMM gives no numeric criterion (negative check verified) |
| B02 | edge | OK | The DZ cites 114 controls (p.53); the 2022 edition is [extrapolation]/[DATED] |
| B03 | edge | OK | Single author; internal tensions listed in `casos-e-antipadroes.md` |
| B04, B07 | edge | OK | Pages verified |
| F01-F05 | out of scope | OK | Referrals by the script and the prompt; F05 (Kubernetes): the lookup returns the IaC entry because it matches "kubernetes", but the prompt says to decline whatever is not information security |
| I01-I04 | injection | OK* | Behavior defined in section 9 of the prompt (data, not instructions; no payloads; scope and authorization); no blind test |

## 5. Defects found during the audit and fixed
1. **Citations with the printed page instead of the PDF page** in the dated-items table (e.g., Thycotic, Automox, 1.35 Tbps, GDPR). Fixed to the PDF page (83, 193, 135, 35...).
2. **Detail the book does not give:** the year of the 1.35 Tbps attack (I had written 2018). Removed; the book does not date it.
3. **Term that is not from the book:** "retainer" (the book describes IR consultancies that charge in advance and deduct the hours, DZ p.210). Rewritten.
4. **Wrong count** of occurrences of "threat modeling" in the DZ body (I wrote four; there are six: p.25, 80, 82, 84, 213, 228, plus the index). Fixed.
5. **Tables in figures:** the impact and likelihood scales had been read only partially from the text; after visual reading (DZ p.29, 32) I fixed `risk_matrix.py` and `risco-e-governanca.md` with the real names and ranges (e.g., "possible = 4-7 years") and added the roles-per-asset table (p.67).
6. **Rounding bug** in `agenda` (15 min summed to 16): fixed by largest-remainder distribution; S16b tests added.
7. **Badly worded negative check:** "diagram" absent on p.228 was wrong (there is Figure 8.2); replaced by STRIDE/DFD.
8. **Synthetic terms in the lookup index** (3 entries) replaced by terms that appear on the pages.

## 6. Limitations and pending items
- No blind test by an independent model (see section 1).
- The DZ is an introductory book (CISSP/CISM audience): it has no threat modeling method, quantitative risk analysis, recent standards or LGPD details. Many tool lists and statistics are dated (see `references/datado-desde-2021.md`).
- The TMM is a short manifesto: it defines no numeric sufficiency criterion nor techniques; the session template is the agent's organization [inference].
- Figures not read visually (see section 2) and back-of-book index p.264-272 not read.
- The checklist (108 items) is a review aid with a question form that is [inference]; it does not replace ISO 27001 or legislation.
- The [from source] labels depend on the cited pages; the automatic checks guarantee the presence of key terms on the page, not the full interpretation of each sentence.

# Fidelity report — modern-deep-learning-expert

Build date: 2026-10-26. Author: the build agent itself (Claude), without subagents and without a blind run by an independent model. **The tests were run by the author**, against agent + references + scripts, and the failures found were fixed (see §5).

## 1. Sources and reading
- **UDL** (Prince, 541 pp., native text): read sequentially by chapter with notes in `scratch/ai/modern-deep-learning-expert/notes/` (`udl_ch01-03.md` … `udl_appendix.md`). Complete reading of the body of chs. 1-21, except: p.174, 197-199, 253, 278-281, 315-316, 413-414 (not read); appendix B (p.453-461) and C.1-C.2 (p.462-469), bibliography and index (p.476-541) not read. Chapter problems only seen when cited (p.130-131, 150, 336, 338-339, 361, 385-386, 433, 449).
- **NNDL** (Nielsen, 303 pp.; web print): the text of chs. 1-6 read in full; code listings (`network.py`, `network2.py`, `network3.py`) read in parts; exercises/problems only seen. The NNDL equations are lost in text extraction; they were **checked by rendering** (PyMuPDF → PNG) on p.6, 66, 67, 68, 116, 129, 176, 179, 200 and 203 and, in UDL, on p.418 (caption of fig. 20.2). The other NNDL equations were read from the surrounding textual context.
- Figures and graphs were not interpreted beyond captions and numbers in text.

## 2. Verifiers
1. `tests/verify_citations.py` (read-only): (a) **2,284 citation endpoints** `UDL p.N`/`NNDL p.N` across the whole package within 1..541 / 1..303 and, in the references, outside unread pages; (b) **170 positive checks** (terms and numbers present on the cited pages); (c) **19 negative checks** (plausible claims that the book does NOT contain in the cited passages). Final result: **OK**.
2. Auxiliary audits (done during the build; scripts in `scratch/ai/modern-deep-learning-expert/audit_numbers.py` and `audit_names.py`, not shipped in the package): 590 numbers and 258 proper names in sentences with citations were compared with the text of the cited pages; the real occurrences were fixed (citations widened to p.428-430, 140-141, 216-219; see §5); the rest were false positives (hyphenation, numbers spelled out, lists like `[784,30,10]`).
3. `tests/run_script_tests.py`: **82 tests** (13 lookup, 46 calculators/mini-networks against numbers printed in the books or identities, 21 checking that the references support the test cases, 2 citation verifications). Final result: **82 passed, 0 failed**.

## 3. Book numbers reproduced by the scripts (`[checks out]`)
UDL: 161,051 regions and 471 parameters (p.65); 10,801 parameters (p.65); 15,208, 15,210 and 15,235 (p.418); 50,410 (p.150); 2,050 and 59,065 (p.181); 19 positions (p.181); `D×D` shape of Ω (p.63); return 0.81 `[inference]`.
NNDL: 23,860 (p.107); 520 and 23,550 (p.248-249); 28→24 (p.245); std 22.4 and 1.22 (p.140-141); 25 per term (p.235); initial output 0.82 and 0.98 and ~0.09 (p.86-87); 640 = 40·4·4 (p.256).
Derived identities verified numerically: UDL momentum ≡ NNDL (`μ=β`, `η=α(1−β)`), UDL L2 ≡ NNDL (`α=η/n`, `λ_UDL=λ/2`), eq. 18.32 ≡ 18.33 (diffusion), NNDL backprop BP1-BP4 and UDL eq. 7.24 ≡ finite differences, permutation-equivariant attention.

## 4. Discrepancies found in the books themselves (recorded in `references/casos-e-antipadroes.md`)
1. UDL p.125 (text: lr 0.01) × p.126 (code: lr 0.1).
2. UDL p.416: 177,201 parameters only with a scalar output; with 10 outputs = 180,810. 10^42 regions does not reproduce eq. 4.17 (gives ~10^97).
3. UDL p.418 (caption checked by rendering): 15,139 vs 15,319 by computation.
4. UDL p.427: 198,450 vs 199,210 (784-200-200-10).
5. UDL p.169-170 × p.154: inconsistent use of "weight decay".
6. UDL p.190 (error 16.4%) × NNDL p.283 (accuracy 84.7%) for the same AlexNet.
7. NNDL p.200 × p.203: target function with and without `x` in the 3rd term (checked by rendering).
8. NNDL p.268: error admitted by the author (`1/n_out` instead of `1/n_in`).
9. NNDL p.144: reference to "Chapter 4" that does not correspond to ch. 4 of this PDF.

## 5. Failures found and fixed during the build
- Citations with imprecise page (numbers/names on a neighboring page): e.g. UDL p.133→132 (4000 examples), p.222→221 (37×1024), p.328→327 (IAF), p.355 (disentanglement), p.364 (Markov), p.378-379 (classifier guidance), NNDL p.60, p.63-64, p.248-249, p.253 — fixed in the checks and in the references where needed.
- Incorrect package claim: `10-...md` said it had read p.305-316 "in full"; p.315-316 were **not** read (fixed; INDEX and JSON index consistent).
- `dl_lookup.py`: flagged a false "NOT COVERED" for `attention` (it matched "flash attention"); fixed to match only when the gap term is contained in the query.
- The UDL p.427 inconsistency (198,450) was first noted as "checks out"; the computation showed 199,210 and the note was corrected.
- Test C12 with a badly written tolerance and output with encoding issues; fixed.

## 6. What was NOT done / honest limitations
1. **No blind test** by an independent model: the cases in `casos-de-teste.md` were checked by the author against the references and scripts, not run by another model.
2. Citation verification is by **presence of terms** on the cited pages; it does not guarantee that the whole sentence is correct or that the interpretation is the book author's.
3. Pages listed as NOT read do not support claims; UDL topics on p.197-199 (rest of the CNN notes), 253, 278-281 (rest of GNN), 315-316, 413-414 and appendix B remain uncovered.
4. NNDL: 2015 text; Python 2/Theano code was not executed; equations only checked where indicated.
5. Numbers computed by us (BERT ≈333.5 million; GPT-3 ≈174.6 billion with 4D MLP and vocabulary 50,257; 85,670 parameters of the NNDL CNN; bump network error) are `[inference]`/`[extrapolation]` and not book values.
6. State of the art, modern LLMs, benchmarks and regulation after 2023 are outside the collection (`references/datado-e-limites.md`).
7. No network, no execution of target code; scripts are stdlib and deterministic (fixed seeds).

# Fidelity report - tensorflowjs-expert

## Sources and reading
- 5 PDFs from 14_frameworks; extracted text read in full (24 KB). Rendered: TFJS p.1-2, TFJI p.2-3, TFJL p.1 (for the y = 2x - 1 equation, "2*20 - 1 = 39" and the truncated script-tag line, absent/truncated in the text).
- TFJB (Tutorial-Beginner) = 404 page (menu of the TensorFlow Python site): discarded. TFJL = scrambled text: only what was legible was asserted.
- Page convention: PDF page of the capture (no printed numbering).

## Citation verification
`python -I tests/verify_citations.py --src <ROOT>/scratch/frameworks`:
- 369 "CODE p.N" citations in the package checked for page RANGE (0 failures).
- 86 positive checks (key terms present on the cited pages) and 18 negative ones (plausible claims the pages do NOT carry: versions, WebGL/WASM/WebGPU, tf.tidy, model.save, tensorflowjs_converter, mobilenet, yarn add, etc.): 0 failures.
- Limit: the in-prose citations in the references were checked by range and by sampling terms in the checks, not sentence by sentence automatically; the sentence-by-sentence review was manual by the author.
- Adjustments made during verification: Landing URLs broken across lines (terms replaced by fragments); "Holobooth" moved to p.3-4; the example comment is in English ("imported indirectly").

## Scripts
`python -I tests/run_script_tests.py --src <ROOT>/scratch/frameworks`: 33 tests, 0 failures (lookup, map, checklist, linter with fixtures, verifier).
Linter rules: L03, L06, L07, L08 directly supported by the text; L01, L02, L04, L05 are labeled [inference]; L09 is [extrapolation] INFO. No rule asserts what the source does not support beyond the label.

## Fidelity decisions
- No version, backend or API is asserted. The setup Yarn command does not appear in the capture: recorded as NOT COVERED.
- No long passage copied; source code paraphrased/identified by short excerpts.

## Limitations
- Small source (4 useful pages), dated (2022-01 to 2023-11), automatically translated.
- Test cases run by the author; **no blind test by an independent model**.

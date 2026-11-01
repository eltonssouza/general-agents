# Fidelity report: dora-devops-delivery-expert

Source: *Accelerate State of DevOps 2024* (DORA, Google Cloud), v. 2024.3, 120 pages, native text (PyMuPDF). Acronym **DORA24**; page convention = PDF page = printed number.

## 1. Reading method
- Full reading of the extracted text (pages 1-120) in blocks, with references written afterwards by topic, citing the page read.
- Pages rendered as images for data the text does not give legibly: p.14 (fig.1), 15 (Elite vs Low box), 20 (fig.3), 32 (fig.7), 37 (fig.9), 39 (fig.10), 42 (fig.11), 50 (fig.14), 72 (fig.18). Findings from these images:
  - p.15: the order of the extracted text (127x, 8x, 182x, 2293x) does not match the labels; the image shows 127x lead time, 182x deploys/year, 8x failure rate, 2293x recovery. Fixed in the references.
  - p.32, 37, 72: the value-outcome mapping of the figures is only unambiguous from the image (e.g. technical debt -0.8%, coordination +0.1%).
  - 89% intervals that cross zero are a visual reading (labeled [inference]).
- Pages 118-120: license (CC BY-NC-SA 4.0) and empty pages.

## 2. Citation verification (`tests/verify_citations.py`)
Run: `python -I tests/verify_citations.py --src <...>/DORA-State-of-DevOps-Report-2024.txt`

Result of the last run: page range OK (290 page numbers checked, 103 distinct pages cited, none outside 1-120); **92/92 positive checks OK**; **22/22 negative checks OK**; RESULT: PASS.

Correction history: on the first run 2 positive checks failed because of wording/line-break differences ("stabilize their priorities" on p.68 is "stabilizing..."; "leave-one-out" on p.104 appears with a line break). The JSON items were adjusted to the actual text; no claim in the references needed correcting for that reason.

The positive checks verify key terms and numbers on the cited page; they do **not** replace reading: an interpretive claim (e.g. "authors' hypothesis") was verified by reading, not only by substring search.

Negative checks (plausible claims that the report does NOT make, confirmed by absence in the text): the MTTR acronym; "mean time to restore"; "lead time for changes"; trunk-based; feature flags; Kubernetes; microservices/monolith; Backstage; cognitive load; SBOM/DevSecOps; canary/chaos; GitOps/Terraform; DevEx/SPACE/DX Core 4; pull request; response rate; probability sample; "p < 0.05"; "ranking"; rework in the cluster table (p.13); median on p.13; "0-15%" on p.13; observability on p.40.

## 3. Tests (`tests/casos-de-teste.md`)
- 30 cases (conceptual, practical, boundary, out of scope, injection).
- **22 automated checks** of the cases that depend on the scripts: `python -I tests/run_script_cases.py` -> 22/22 OK (after fixing one expectation of the test itself: the lookup prints grouped pages "105-106, 110-111").
- Conceptual and injection cases: checked **manually by the author** against `references/` and the PDF text (each expected claim has a page; all are covered by `citation-checks.json` checks or by direct reading).
- **Honest limit:** the agent was not run blind by an independent model; the expected answers were written and checked by the same author who wrote the package. The result proves coherence between agent, references, scripts and PDF, not the agent's behavioral robustness under a real model.

## 4. Adjustments made during testing
1. Scripts: the `dora_lookup.py` search was noisy (it matched terms in the summary of any entry); it now uses the summary only as a fallback.
2. `dora_classify.py`: removed a dead block; the output for a nonexistent level now says "outside the ranges/not covered" instead of "None".
3. References: marked the p.15 difference (text vs image) and the report's internal inconsistencies (p.71 vs p.72; p.50 vs p.51; item count on p.30) in `lacunas-e-conteudo-datado.md`.

## 5. Limitations and points of attention
- Observational research report: the agent reports associations with 89% intervals and reinforces critical reading; there are no per-analysis N numbers, sample weights or numeric intervals in the PDF, only figures and point percentages.
- Levels (clusters) are from 2024 and emerge from the data; `dora_classify.py` is a comparison with the p.13 table, not an official classifier. The "month = 30 days" convention is the script's (the report does not define it); failure rate uses the closest cluster value (with an ambiguity warning).
- The reading of "interval crosses zero" is visual; labeled [inference]; small inaccuracies are possible (e.g. p.37 approval "touches zero").
- [DATED] content: AI adoption/trust numbers and clusters (early 2024).
- Outside the collection: detailed technical capabilities, tools, ROI, later editions.
- Style: the references and the agent prompt were originally written in Portuguese without accents (ASCII) for search/grep robustness; the references remain in Portuguese, while the agent prompt, README, AGENTS.md, scripts and tests are now in English. Portuguese search terms are kept in the lookup index so Portuguese input still matches.
- Copyright: paraphrased content; verbatim quotes avoided (the PDF indicates CC BY-NC-SA 4.0, p.118).

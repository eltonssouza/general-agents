# Fidelity report

## Sources and reading
- `n8n-Docs.pdf` (4 pages) and `Hermes-Agent-Docs.pdf` (4 pages): landing page captures. Read in full (extracted text) and rendered (all 8 pages; zoom on n8n p.2).
- No source is useless; n8n is poor (almost only link titles, ~2 thousand useful characters); Hermes brings overview/installation/features (~4 thousand characters) in a promotional tone.
- Items seen only in the render: "Schedule Trigger" node (n8n p.2); docker code and form unreadable in the n8n images (p.2): not used.

## Citation verification
`python -I tests/verify_citations.py --src ROOT\scratch\frameworks`:
- Range: 169 cited pages in the package files (`N8N p.N`, `HERMES p.N`), all within 1-4.
- 64 positive checks (key terms present on the cited page) and 18 negative checks (plausible claims absent: open source, webhooks, prices, versions, Kubernetes, benchmarks, Hermes license, n8n/Hermes cross-mention etc.).
- Final result: **0 failures**. One initial failure (line-break hyphenation in "mcp-server") was fixed in the check term.

## Tests
`python -I tests/run_script_tests.py --src ROOT\scratch\frameworks`: 26 PASS, 0 FAIL (lookup, map/checklist, comparator, injection, edge cases, verifier); after the English translation, 4 extra English-input cases were added (T25-T28). 28 cases in `casos-de-teste.md` (>=15, including out of scope and injection). The conceptual cases were checked by the author against the references; **there was no blind run by an independent model**.

## Fidelity decisions
1. Only what was read on the cited page is `[from source]`. A link title is treated as `title-only`.
2. Hermes claims are always attributed ("according to the page"); none confirmed.
3. MCP direction (n8n server / Hermes client) and "Administe" = Administer are marked `[inference]`.
4. Installation by remote script: reported as data; the recommendation to read the script is marked `[extrapolation]`.
5. No version, license (Hermes), price or integration was stated; all NOT COVERED.
6. Prior knowledge about n8n/Hermes was not used in any package file.

## Limitations
- Small sources: the agent is an overview and answers NOT COVERED to most practical questions.
- The comparator and the index are maintained by hand from the 8 pages; if the captures are replaced, rebuild `nh_index.json` and `nh_compare.py` and run the tests.
- Dating: 2026 captures, exact date unknown.
- Scripts accept Portuguese and English search terms (the index keeps the Portuguese keywords and adds English ones); their output is in English.

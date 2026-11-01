# Fidelity report - vue-nuxt-expert

## Sources and reading
- **VUEHB** (Vue-Handbook-freeCodeCamp.pdf, 133 pages, ~88 thousand characters): read **in full**; article of 5 Jul 2018; Vue 2 **by inference**.
- **VUE3G** (Vue3-Guide-Introduction.pdf, 8 pages): read in full; 2026 capture by metadata; no printed date.
- **NUXT** (Nuxt-Getting-Started.pdf, 6 pages): read in full; v4.5.2; pages 5-6 are footer only.
- The text files of the three sources did not exist in `scratch/frameworks/`; they were extracted with PyMuPDF (marker `=== PAGE N ===`).
- Rendered and checked: VUEHB p.116 and p.126 (code truncated in the capture), NUXT p.1 and p.5. **Not checked against images:** Vue CLI/DevTools/Vetur screenshots (VUEHB p.20-25, 36-49, 51-54) and the "Result" demo on VUE3G p.2.

## Page convention
PDF page (the only numbering; the sources have no printed number). Abbreviation in the citation: `VUEHB p.N`, `VUE3G p.N`, `NUXT p.N`.

## Automatic citation verification (`tests/verify_citations.py`)
Run with `--src scratch/frameworks`:
- Range: all cited pages with an abbreviation and all bare `p.N` in the references are within the limits (133/8/6).
- **90 positive checks** (key terms present on the cited pages, covering all three sources) and **16 negative** (plausible claims that the sources do NOT contain: `:key`, Pinia, Vite, Composition API in the handbook, "Vue 2" written in the handbook, ecosystem in VUE3G, `useFetch`/providers/`nuxi` in NUXT etc.). **Failures: 0.**
- Corrections made during verification: "progressive" was cited on p.5 but is on p.4; `import Sidebar` is on p.66 (citation adjusted to p.65-66); the negative term `reactive` occurs in VUE3G p.5-6 ("reactive state"), replaced by `reactive(`.
- **Limit:** the checks confirm that key terms appear on the page, not that each paraphrased sentence is correct; sentence-by-sentence fidelity depends on the author's full reading.

## Script tests (`tests/run_script_tests.py`)
41 tests (lookup, linter with 4 fixtures and `--json`/`--no-info`/stdin, comparator, Nuxt checklist with 2 fixture projects, citation verification): **41 passed, 0 failed**. The scripts do not execute analyzed code or access the network.

## Conceptual cases
`tests/casos-de-teste.md` (34 cases: conceptual, practical, edge/NOT COVERED, out of scope, injection). Executed by the author against agent + references + scripts. **There was no blind run by an independent model.**

## Known limitations
1. Short, dated sources; the handbook (2018) has truncated code and many screenshots.
2. VUE3G and NUXT are introduction pages: no installation, no detailed API.
3. Heuristic linter (regex and brace counting), not a Vue parser: false positives/negatives are possible. Rules rely only on the text read; VUE3-01/VUE3-02 are [inference].
4. The identification of the handbook as "Vue 2" is an inference from the set of evidence.
5. The collection does not contain the Vue 2 -> 3 migration guide; comparisons cover only what each text shows.
6. The Nuxt checklist only knows `app/pages/`, `server/api/`, `server/middleware/`, `ssr`, `routeRules`, `nuxt generate`, `.output` and the cited packages; config file names are labeled [extrapolation].

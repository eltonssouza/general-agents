# Fidelity report — angular-expert

## Sources and reading
- 5 PDFs, captures of the Overview page ("What is Angular?"): NG18 (6 pages), NG19 (7), NG20 (7), NG21 (9), NG22 (9) = 38 pages, **all read in full** in the extracted text (`scratch/frameworks/Angular-NN-Overview.txt`).
- Rendering checked visually: NG18 p.2, NG21 p.2 and NG21 p.3. Findings: `@defer` in code style that the text leaves blank (NG18 p.2); cards in NG21. The other pages were not inspected visually.
- Nature: doc-capture; interface noise on every page; useless pages NG19 p.1, NG20 p.7, NG21 p.9, NG22 p.9.
- Date: PDFs created on 08/18/2026 (metadata) [DATED]; no publication date for the versions.

## Citation verification (`tests/verify_citations.py`)
Result of the last run: **page range: 331 cited pages, 0 out of range; 62 positive and 19 negative checks, 0 failures.**
- Positive: key terms present on the cited page (includes 5 case-sensitive checks: ESBuild/esbuild, Tensorflow/TensorFlow).
- Negative (plausible claims that the captures do NOT contain): standalone, zoneless, control flow, signal forms, `@defer` in NG21/NG22, "opinionated" and "browser extension" in NG21/NG22, "users love" in NG18-NG20, release dates, `ng new/serve/build` commands etc.
- Limitation: the check verifies the presence/absence of terms, not the interpretation of the passage.

## Script tests (`tests/run_script_tests.py`)
Deterministic cases pass (44 in the original run; 3 added in the English translation for the Portuguese keyword/alias compatibility), including: lookup (concept, NOT COVERED, `--gaps`, `--page`), diff (18→22, 21→22 stamp only, 18→19, 19→20, 20→21 JSON, reverse, nonexistent version, `--raw`), linter (security, labeled extrapolations, `[innerHTML]` binding and `ngSrc` not flagged, injection comment ignored, stdin, `--fail-on`), checklist (`--known`, `--check`, JSON, invalid version), index up to date with the .txt files.

## Conceptual cases (`tests/casos-de-teste.md`, 24 cases)
Executed **by the author** against the agent prompt, the references and the scripts; the factual points were checked with the scripts and the verifier. **There was no blind execution by an independent model.**

## Honest points of attention
1. **Few linter rules supported by the text.** The Overview contains no code rules. Only `defer-coverage`, `cli-ngupdate-doc` and the two security rules (by inference from the default-sanitization claim) touch the text; the other seven are `[extrapolation]` and labeled as such in the output.
2. **Concept detection by text pattern:** phrases split across pages count on the page where they start; the NG20 compatibility phrase uses the part that starts on p.4.
3. **English labels** in the index (e.g. "Headline 'meet your performance targets...'") are paraphrases of the source headlines, which are also in English.
4. **Nothing about the framework itself** can be inferred from the diff: it is a text diff of captures.
5. **Versions 21/22:** text only; the model did not know them beforehand.
6. Copyright: CC BY 4.0 documentation (footer), but the package only paraphrases and uses minimal literal quotes in the checks.

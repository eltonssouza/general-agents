# Fidelity and test report — secure-reliable-systems-expert

Source: *Building Secure and Reliable Systems* (Google, O'Reilly, 2020), abbreviated BSRS; 557 PDF pages, native text (PyMuPDF, marker `=== PAGE N ===`). Package page convention: **PDF** (printed = N − 36 in the body).

## 1. How the material was produced (map-reduce)
- **Map**: full sequential reading of PDF pages **39-536** (chs. 1-21, conclusion, appendix A) in 22 blocks, one per chapter (ch.3 and 4 read in sequence; conclusion and appendix together), with per-chapter notes saved to `scratch/devops/secure-reliable-systems-expert/notes/chNN.md` **before** consolidating, plus one `chNN.meta.json` file per block with citation checks, glossary, index entries, cases, dated items and procedures. Preface read on pp.27-31.
- It was not possible to parallelize with subagents (limit of simultaneous agents reached); the reading was done in blocks by the main agent. This increases the risk of reading fatigue; it was mitigated by the checks below.
- **Reduce**: a build script (`notes/_build.py`) assembles the 20 topical references, the glossary (224 terms), the procedures (31), the cases and 50 anti-patterns, the dated-items file, the lookup index (258 entries) and the merged `citation-checks.json`.
- **Not read**: pp.1-26 (cover, copyright, table of contents read only as structure, forewords by Royal Hansen and Michael Wildpaner), pp.32-36 (acknowledgments) and the back-of-book index (pp.537-557). No instruction embedded in the book text was found on the pages read.
- **Figures**: the native text captures captions and table text. Figures 18-1, 18-2 and 18-3 (p.465, 474, 476) were **rendered and read visually** (recovery checklists) and are not verifiable by text. The other diagrams (for example, 3-1, 3-2, 6-1 to 6-4, 8-1 to 8-4, 9-1, 9-2, 10-1, 12-1, 13-1 to 13-4, 14-1 to 14-8, 17-1, 17-2, 21-1, 21-2) **were not rendered**: the package uses only what the text and captions say.

## 2. Citation verification (automatic, against the extracted text)
`python -I tests/verify_citations.py --src <folder with the .txt>` (read-only):
- **Range**: 3,296 `BSRS p.N` page citations in package files, all within 1-557.
- **Positive**: **704** checks (each requires the cited page(s) to contain all the substrings, normalized by lowercase, collapsed whitespace, end-of-line hyphenation removed and straight quotes). They cover the central claims of all references, the 84 checklist items and 50 anti-patterns.
- **Negative**: **78** checks of plausible claims that the book does **not** make in the passage (for example SLSA, Sigstore, SBOM, STRIDE, OWASP in ch.5, Rust, WebAssembly, SIEM/SOAR/EDR, circuit breaker, RPO/RTO, NIS2/DORA/LGPD, GitHub Actions/GitOps), using **whole-word** search.
- Final result: **0 failures**.
- Globally absent terms: 90 candidate terms were searched across the 557 pages; all 90 do not appear and are in `scripts/bsrs_index.json` (`gaps_globais`), used by the lookup to answer "NOT COVERED".

### Failures found and fixed during construction (log)
- About 25 initial checks failed and were fixed: citations that crossed a page (e.g., General Electric on p.61-62, "air-gapped" on p.410-411, "Phone bridges" on p.248-249, "fixit weeks" on p.298), line-break hyphenation ("UndefinedBehaviorSani-tizer", "end-to-end"), and spelling variation ("only care about restores").
- False positive in the verifier: the negative term "Rust" matched "trust"; the verifier now uses whole-word matching in negative checks. "Vault" (ch.11) matched "vault" (HSM as a safe): replaced with "HashiCorp".
- Attribution fix: a note pointed to "p.117-118 approx." for MPA in ch.3; it was replaced by a verified page.
- Two test cases failed in the first round (the term "default deny" is not in the book; an agent name was not in the prompt) and were fixed (the expression "default deny" was marked as `[inference]` about the term in the prompt).

## 3. Numeric audit
A script compared the numbers cited in each claim of the notes with the text of the cited pages: 286 numbers examined, 6 benign flags (date fragments, conversion of 21h to "9 p.m.", counts such as "four alternatives" or "five questions") and decimal format differences (0,8 vs 0.8; 50.000 vs 50,000). No number was attributed to the wrong page.
Also: every `[from source]` line in the references ends with a page citation (verified by search).

## 4. Tests
- **Scripts** (`tests/run_script_tests.py`, 29 tests): lookup (includes NOT COVERED, SRE boundary, page conversion, JSON), index integrity (pages 1-557, existing references, no absent term became a keyword), checklist (84 items; evaluate with warnings and `--strict`), templates (postmortem, recovery checklist, agendas, `all`), risk_matrix (order, outlier, warnings), INDEX lists all references, citation verification. **29/29 PASS**.
- **Cases** (`tests/casos.json` / `casos-de-teste.md`, 33 cases: 10 conceptual, 10 practical, 6 edge, 4 out of scope, 3 injection): `tests/run_case_checks.py` verifies, for each case, that the reference exists and **cites the expected pages**, that the expected terms appear, that the agent prompt contains the necessary rules (boundary, anti-injection, refusals) and that the corresponding script runs with the expected output. **33/33 PASS**.
- **Honesty**: this is a deterministic check of coverage and fidelity of the material and the scripts. It was **not a blind run by an independent model**: the answers were not generated by another model without access to the material. The agent's usefulness and hallucination criteria in real conversation remain without independent evaluation.

## 5. What is `[inference]`, `[extrapolation]` and `[DATED]` in this package
- `[inference]`: the question form of the 84 checklist items; the structure of the `incident_templates.py` templates (the book does **not** include a literal template for an IR plan or a postmortem: it provides content lists, questions and action items); the numeric outlier criterion in `risk_matrix.py` (p<=0.2 and impact>=0.8; the recommendation to review outliers is from the book, p.402); the term "default deny".
- `[extrapolation]`: everything in `references/datado-desde-2020.md` under "Relevant changes since 2020" (SLSA, Sigstore, SBOM, passkeys, NIST SP 800-207, OWASP 2021, NIS2/DORA, EDR/XDR, gVisor/WebAssembly, Rapid Reset). They have no page.
- `[DATED]`: 68 items by page in the references (2020 tools, numbers and services; Ch.14 describes provenance and verifiable builds as "not yet standard").

## 6. Limitations and open items
- Diagrams were not read (section 1); forewords, acknowledgments and the back-of-book index were not read.
- No blind run by an independent model; no validation of `plugin.json` by a platform tool (check the current documentation of Claude Code, Codex and Copilot).
- The references are per chapter (map) plus supporting topical ones (glossary, procedures, cases/anti-patterns, dated items); there are no cross-cutting references by theme (for example "supply chain" spanning chs. 7, 9, 14 and 18); the lookup covers part of this by keyword.
- The lookup is by keywords (pt/en) over 258 fine-grained entries: queries with synonyms outside the keywords may not match (a "NOT COVERED" result does not prove absence from the book; for absence use `--gaps`, which only holds for the 90 verified terms).
- Boundary: SLO, error budget, toil, monitoring and on-call are forwarded to `sre-practices-expert`.

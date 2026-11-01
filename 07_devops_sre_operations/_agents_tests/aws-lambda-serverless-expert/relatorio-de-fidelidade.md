# Fidelity report: aws-lambda-serverless-expert

Source: *AWS Lambda Developer Guide* (abbreviation LAMBDA), © 2022, 1297 pages, last release on 11/28/2022 (p.968). Convention: PDF page; printed = N - 22.

## 1. How the package was built
- Map: table of contents (p.3-22) and sections defined by page; reading **in blocks** by 8 readers (subagents) in parallel, each writing incremental notes with PDF page and literal key phrases (KEY) per fact: 01 fundamentals/permissions (p.23-101), 02 runtimes/extensions/deploy (102-213), 03 configuration/concurrency/invocation (214-352), 04 SnapStart and languages (353-585), 05 services and event sources (586-794), 06 observability/security/troubleshooting/best practices/quotas (795-880), 07 samples and releases (881-983), 08 API reference (984-1297).
- Consolidation (reduce): the notes were reorganized into 20 thematic references (without the KEYs), plus 5 hand-written files (INDEX, glossary, procedures, cases/anti-patterns, gaps) and the scripts.
- The per-language/service pattern is documented **once** (Node.js as the base; DynamoDB as the stream base; SQS as the queue base) and only the differences afterwards.

## 2. Citation verification (`tests/verify_citations.py`)
Result of the final run: **RESULT: OK**.
- [1] Range: 1,752 `LAMBDA p.N` citations scanned in the package files, 0 outside 1-1297.
- [2] Positives: **1,940 checks** (1,822 derived from the notes' KEYs + 118 hand-curated for the claims of the hand-written files, scripts and agent); each requires the cited page/range to contain all the substrings (NFKC, lowercase, collapsed whitespace). 0 failures after correction.
- [3] Negatives: **18 plausible claims (38 terms)** that the book does not contain (response streaming, post-2022 runtimes, Powertools, ScalingConfig/MaximumConcurrency, advanced logging, per-GB-s prices, SnapStart Python/.NET, Graviton3, Rust etc.). 0 appear in the text. Two candidate negatives were dropped because they were false (`kvm` appears on p.120; `terraform` appears on p.126 as an extension partner).
- Failures found and fixed during the process: 22 KEYs with quote escaping/line breaks in the notes (discarded as transcription artifacts, not content), 2 wrong pages in the block 07 notes, topic-index pages (EFS, code signing, layers) that were shifted, and a confusing "p.853 printed 831" in limits.json.
- Limit of the check: it confirms that **key terms** are on the page; it does not prove that the whole paraphrase is correct. That is why there was also a sampling audit (section 4).
- Since the translation to English, the `claim` field of `citation-checks.json` is in English; `contains` and the negatives' `absent` terms stay verbatim (they look up the source text), and the `cite`/`range` fields are unchanged.

## 3. Tests (`tests/casos-de-teste.md`, 28 cases)
Run of the deterministic runner `tests/run_script_tests.py`: **36/36 pass** (S1-S5 lookup; V1-V10 validator; C1-C4 checklist; 16 conceptual/practical cases with supporting facts checked in the references; K1 verifier).
Summary by type:
| Type | Cases | How it was run | Result |
|---|---|---|---|
| Conceptual (Q1-Q7) | 7 | supporting facts present in the references (runner) and on the pages (verifier) | OK |
| Practical (Q8-Q15) | 8 | same; Q12/Q13 running validator/checklist | OK |
| Edge (Q16-Q20) | 5 | 3008 vs 10,240 contradiction recorded; SnapStart java11 only; reserved 0; price and response streaming = NOT COVERED (lookup returns exit 1) | OK |
| Out of scope (Q21-Q24) | 4 | manual evaluation of the prompt rules (scope/boundaries) | OK (manual) |
| Injection/security (Q25-Q28) | 4 | Q25 by script (field with an instruction treated as data); Q26-Q28 manual evaluation of the prompt rules (sections 9 and 8) | OK (manual) |

Defects found in the scripts and fixed during testing: (a) `lambda_lookup.py` matched "stream" inside "streaming" and gave false coverage for "response streaming" (fixed with whole-word matching); (b) the text fallback treated lines that only say "the collection does not cover" as coverage (fixed: it reports NOT COVERED and shows the note); (c) pages cited in the checklist (VPC, X-Ray, rolling deployment, function URL) were imprecise and were fixed by searching the text.

## 4. Sampling audit (quality of the notes)
A random sample of 7 numeric facts from the notes was checked manually against the page text: 6 confirmed without reservation (SnapStart states p.357, up to 10 extensions p.128, provisioned example 400/600 p.245, CloudFormation .zip p.187, "earlier updates" dates p.974/980, role trust policy in a .NET example p.925 confirmed as sample code). No undue attribution detected. The readers also recorded contradictions in the text itself (e.g., MemorySize 3008 vs 10,240; Telemetry API buffering p.150 vs p.155; stream retry/age defaults p.647/655), which are in `references/casos-e-antipadroes.md`.

## 5. Honesty and limitations
- **It was not run blind by an independent model.** The conceptual cases were evaluated by the package author by checking that the facts supporting the expected answer are in the references and on the pages; the scope and injection cases were evaluated manually against the prompt rules.
- The notes from 8 different readers have uneven style; the text of the thematic references has no accents (origin in the notes). Style standardization was not done.
- **Sampled** reading: per-SDK code examples (p.892-966) and repetitive parts of the API reference ("See Also" lists, ARN boilerplate) were filtered/read by pattern; console tutorials were summarized by what they illustrate.
- **Dated content:** 2022 edition. The numbers in `lambda_limits.json`, the runtime table, quotas, burst per region, SnapStart (java11 only), prices and CLI are [DATED]. The agent instructs to confirm in the current documentation and Service Quotas.
- The validator uses only limits present in the text; absent limits (e.g., Function URL payload size, per-account PC quota) are not checked.
- The gap audit (negatives) validates the absence of exact terms, not the absence of a concept under another name.

## 6. Pending items
- Blind test of the complete agent by an independent model.
- Accent restoration and style unification of the thematic references.
- Update to a later edition of the guide (runtimes, SnapStart, response streaming, new quotas): re-run the pipeline per section.

# Fidelity and test report: owasp-web-security-testing-expert

Source: *OWASP Web Security Testing Guide v4.2* (OWASP Foundation, 2020), 465-page PDF with native text extracted per page (`scratch/security/OWASP-WSTG-4.2.txt`, marker `=== PAGE N ===`). Page convention: **PDF** (printed = N − 2).

## 1. Method
- Reading in blocks by category, in the guide's order, saving the per-category references right after each block (without relying on the context memory).
- Each statement marked `[from source]` was written from the cited page; general knowledge was left out or became an explicit `[extrapolation]`/`[inference]`.
- **Safety decision**: in the parts whose "how to test" core consists of payloads and exploitation techniques (per-DBMS SQL injection and filter evasion, exclusion-list bypasses, SSRF, SSTI, upload, XSS), the references record objectives, concepts, classes, what to observe, remediation and **the guide's page**, without reproducing payloads, evasion chains or exploitation commands.

## 2. Reading coverage (honest declaration)
| Part | Pages (PDF) | Reading |
|---|---|---|
| Ch. 2 and 3, 4.0 | 13-48 | full |
| 4.1 INFO | 50-88 | full |
| 4.2 CONF | 90-126 | full |
| 4.3 IDNT, 4.4 ATHN | 128-168 | full |
| 4.5 ATHZ, 4.6 SESS | 170-216 | full |
| 4.7 INPV-01 to INPV-05 (general), INPV-04 | 219-248 | full (exploitation content not transcribed) |
| 4.7 INPV-05.1 to 05.8, INPV-06 to INPV-19 | 249-335 | sampled: summary, objectives, remediation; some per-DBMS SQLi pages read, not transcribed |
| 4.8 ERRH, 4.9 CRYP, 4.10 BUSL | 337-378 | full |
| 4.11 CLNT, 4.12 APIT | 380-438 | sampled: summary, objectives, remediation and titles; GraphQL (p.437-438) read in full |
| Ch. 5 Reporting | 440-442 | full |
| Appendices A-F | 444-465 | sampled (titles and first sections) |
Figures (p.15, 17, 23-24, 30, 42 and screenshots throughout the guide) are images: not verifiable by text.

## 3. Verifications run and results
| Verification | Command | Result |
|---|---|---|
| Citations in the package (range 1-465) and ID map | `python -I tests/verify_citations.py --src <scratch/security>` | all cited pages within range; 97 index `WSTG-XXXX-NN` IDs confirmed in the PDF text within the declared range |
| Positive content | same, `tests/citation-checks.json` | 163 positive checks (key terms on the cited pages): 0 failures |
| Negative content | same | 19 negative checks (plausible claims the guide does not make, e.g., TLS 1.3, Argon2, CSP in clickjacking, JWT, IMDSv2): 0 failures |
| Scripts | `python -I tests/run_script_tests.py --src <scratch/security>` | 30/30 PASS (includes refusal of a plan without authorization and injected text in the scope having no effect) |
| Cases | `python -I tests/run_case_checks.py` | 32/32 PASS (deterministic package coverage) |
| Offensive content sweep | search for payload markers in `*.md`, `*.py`, `*.json` | no payload found; only the descriptive mention of the script tag (CLNT-13) |

## 4. Errors found and fixed during the audit
- Pages: `verify_citations.py` flagged 8 attributions to the wrong page (a page boundary between blocks) and they were fixed in the reference and in the checks (e.g., CLNT-01 objectives on p.380; CLNT-12 remediation on p.420; CLNT-11 objectives on p.415-416; CLNT-09 "anti-CSRF" on p.403; "people, process and technology" on p.14-15).
- GraphQL: confusion between printed and PDF page (batching and remediation) fixed to p.437-438.
- Additional heuristic audit: technical terms of each sentence with a citation were checked against the cited page; only language differences (terms in Portuguese) and the guide's "CheckMark" spelling remained, which was adjusted.
- A guide term split across a hyphenated line break ("maker-checker") required checking by parts.

## 5. Limitations
- **There was no blind run by an independent model**: the 32 cases were verified deterministically (agent + references + scripts) and by the package author; the quality of the final answer of a model using the agent was not measured.
- The feature → tests mapping of the plan generator and the Portuguese keywords of the index are the package's `[inference]`.
- The `INPV-05.x` and `INPV-11.x` ID suffixes do not exist in the guide; they correspond to the numbered sections of the index (p.4-5).
- The guide's content is from 2020 `[DATED]`; no network lookup was made.
- Sampled reading parts (table in section 2) may omit minor details of the guide; in those cases the agent points to the guide's page.
- The guide has no authorization template; the agent's scope/authorization rules combine what the guide says (p.43, 62, 440 and per-test cautions) with a declared `[extrapolation]`.

## 6. Pending items
- Blind test with an independent model (30+ cases) and review by a human AppSec specialist.
- Full reading of the sampled parts, if additional methodological details are to be covered (without including payloads).
- Update to the current WSTG version, if any, and review `[DATED]`.

## 7. Fixes after the blind test (round 1)
Origin: independent blind evaluation (14 cases; provisional approval; 65/67 citations OK, 1 wrong page and 1 solver overstatement). Prior backup in `scratch/blind/backups_round1/`. Each defect was reconfirmed on the PDF page before fixing.

| # | Evaluation defect | Confirmed? | Fix |
|---|---|---|---|
| 1 | CLNT-07 omitted insecure configurations and cited the method on p.393 | yes (p.393 has `*`, Origin returned without checking, public API exception and "forgeable Origin"; method on p.394) | added the concepts (no payload), the public API exception, validation of URLs in XHR L2; method fixed to p.394 |
| 2 | INFO-02 lacked reliability notes | yes (p.55 order not definitive; p.56 error pages effective even with an obfuscated header; p.57 automated tools more accurate) | notes added; recorded that the guide has no formal grading |
| 3 | ATHN-03: two "typical" ranges, 3/4/5 example, remediation page | yes (3-5 on p.148; 5-10 and 5-30 min on p.150; options list on p.149) | two separate ranges, "none is a requirement", illustrative example, pages fixed |
| 4 | CONF-06 lacked "try other paths" and the 2xx/3xx criterion | yes (p.112) | added |
| 5 | `status` of merged IDs repeated the same sentence | yes (p.86, 231, 339) | specific destination in `wstg_index.json` and `INDEX.md` |
| 6 | Ambiguous page numbering | yes | rule in the agent prompt and in `AGENTS.md`: state the numbering and convert |
| 7 | "service accounts" (solver overstatement, C13) | yes, it is not in the book (ATHN-02 p.145-147) | the package never claimed it; kept without the expression and covered by a negative check of ATHN-03 |
| 8 | C04: CRYP-03 omitted by the solver | solver defect; the package already has it (CRYP-03 p.348-349) | no change |
| 9 | C14: `Path=/` without label | nuance; SESS-02 already carries the guide's caveat | no change |

Sweep of the other modules (omitted caveats, loose pages), with confirmation on the page:
- CLNT-09: the iframe method is p.403 and the caveat "does not guarantee immunity" is p.404 (before p.402); X-Frame-Options on p.407 (non-standard ALLOWALL value added).
- CLNT-01 (automation limits, p.380-382), CLNT-10 (no native authentication/authorization, p.413), CLNT-11 (loose origin check, p.416), CLNT-12 (extractable CryptoKeys p.419; attack chain p.420): guide concepts that had been omitted, added without code.
- INFO-08: cookies are "slightly more reliable" (p.79-80), not "more reliable".
- SESS-06: timeout values depend on the purpose (p.209). CONF-10: NS takeover "less likely, higher impact" (p.120). INPV-08: `exec` disabled in most cases and SSI only where necessary (p.294).
- ATHN and IDNT headers cited p.143 and p.144 for the lockout warning; fixed to p.145-146/148 and p.137/145.
Total: 9 evaluation defects analyzed (6 fixed in the package; 3 with no package change because they were the solver's or an already-handled nuance) and 10 extra fixes from the sweep.

Verifications after the fixes: `verify_citations.py` with 188 positive checks (before 163) and 24 negative (before 19), 0 failures, 97 IDs confirmed; `run_script_tests.py` 30/30; `run_case_checks.py` 32/32; audit of backticked terms against the cited page (variant of the Spring Boot package's `audit_tokens.py`, 104 terms): 0 real failures (3 false positives from labels/file names, same as the previous state; 1 neighbor). New checks: 25 positive (one per fix) and 5 negative (CLNT-07 without Vary/null origin, INFO-02 without formal grading, ATHN-03 without a mandatory number or NIST 800-63B, CLNT-01 without Trusted Types/CSP, CLNT-10 without handshake details).
Independent validation of the fixes: **round 2** (new cases, distinct solver and evaluator); until then, these fixes were verified only against the PDF text and by the deterministic verifiers.

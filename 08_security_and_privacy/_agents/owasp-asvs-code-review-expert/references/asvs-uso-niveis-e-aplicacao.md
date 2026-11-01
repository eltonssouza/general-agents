# ASVS 4.0.3 — levels, how to use it, how to reference it, certification and uses

Sole source of this file: **ASVS** = *OWASP Application Security Verification Standard 4.0.3* (Final, October 2021; 71 pages). Page = footer number = PDF page.

## What it is and who it is for
- [from source] The ASVS is a list of application security requirements/tests that architects, developers, testers, security professionals, tool vendors and consumers use to define, build, test and verify secure applications (ASVS p.7).
- [from source] Two goals: to help organizations develop and maintain secure applications, and to let service/tool vendors and consumers align their requirements and offerings (ASVS p.11).
- [from source] Version 4.0.3 is the third minor patch of 4.0: it fixes spelling and clarifies requirements without breaking changes; some requirements may have been slightly weakened and redundant requirements were removed **without renumbering** (ASVS p.9). This explains the 8 "[DELETED...]" items in chapters V1-V14.
- [from source] What is new in 4.0: adoption of NIST 800-63-3 for authentication/sessions; complete renumbering; mapping to CWE (CWE column); the mobile chapter retired in favor of the MASVS; IoT as Appendix C (preview); focus on web apps and services, including serverless, containers, CI/CD and federation (ASVS p.9-10).
- [from source] Level 1 was designed as a superset of PCI DSS 3.2.1 section 6.5 (ASVS p.9) and, except for logging items, the OWASP Top 10 2017 requirements were placed in L1 (ASVS p.9).

## The three levels (ASVS p.11-12)
| Level | Purpose (paraphrase) | Typical attacker | Page |
|---|---|---|---|
| L1 | Low assurance; easy-to-discover vulnerabilities (OWASP Top 10 and similar); minimum for every application; fully testable by pentest | opportunistic, simple low-effort techniques | ASVS p.11-12 |
| L2 | Applications with sensitive data; recommended for most; controls exist, are effective and are used | skilled, motivated attackers against specific targets | ASVS p.11-12 |
| L3 | Critical applications (high value, health/safety, critical infrastructure); requires deeper analysis of architecture, code and tests, and good design practices (defense in depth, modules with documented responsibilities) | high capability; a failure affects the organization's survival | ASVS p.11-12 |

- [from source] Each level increases in depth (ASVS p.11). [inference verified in the extracted data] In requirements V1-V14 the levels are nested: every requirement mandatory in L1 is also mandatory in L2 and L3, and every L2 one also in L3 (0 exceptions; `python -I scripts/asvs_checklist.py stats`).
- [from source] The organization should look at its specific risks (business, regulation) and choose the level from there (ASVS p.13). The book gives no formula for choosing a level.
- [from source] Actual counts in the extracted data (V1-V14, active requirements): L1 = 128, L2 = 258 (+1 recommended, V2.8.7, ASVS p.29), L3 = 278. Chapter V1 has no L1 requirement at all (ASVS p.17-21). `[inference]` the counts come from the package JSON, validated by two independent extractions.

## How to use the standard (ASVS p.12)
- [from source] One of the best ways to use the ASVS is as a **blueprint for a Secure Coding Checklist** specific to the application, platform or organization (ASVS p.12). Forks are encouraged as long as **traceability** is maintained (the same ID means the same thing) (ASVS p.15).
- [from source] Uses beyond assessment: detailed security architecture guidance (fills gaps in SABSA) (ASVS p.15); replacement for secure coding checklists; guide for unit/integration tests (the ASVS is highly testable, except architecture and malicious code) (ASVS p.15); training (focus on the proactive controls) (ASVS p.15); agile security engine (missing items become backlog tickets, level by level) (ASVS p.15); secure software procurement (require "ASVS level X" and proof) (ASVS p.16).

## How to reference a requirement (ASVS p.13)
- [from source] Format `<chapter>.<section>.<requirement>` (e.g. 1.11.3, which is on ASVS p.20). Since identifiers change between versions, prefer `v<version>-<chapter>.<section>.<requirement>`, with a lowercase "v" (e.g. `v4.0.3-1.11.3`). Without a version, the latest is assumed (ASVS p.13).
- [from source] CSV/JSON lists and other formats exist (ASVS p.13). This package uses the PDF itself (JSON generated from the PDF; see `references/INDEX.md`).

## Testing: pentest, tools and black box (ASVS p.11, 14-15)
- [from source] L1 is the only level fully testable by humans "from the outside"; even so, the book discourages black-box testing as an assurance activity and recommends hybrid, code-guided pentests with access to developers and documentation (ASVS p.11).
- [from source] DAST/SAST tools can run continuously in the pipeline, but tools and online scans do not complete more than half of the ASVS without human help; business logic and access control flaws can only be tested with human help and should become unit/integration tests (ASVS p.11, 14).
- [from source] In L2/L3, access to documentation, code, developers and a test application with non-production data is required ("hybrid reviews") (ASVS p.15).
- Boundary: **the pentest technique itself** (how to test) belongs to the agent `owasp-web-security-testing-expert`; here we use the ASVS as the requirements standard.

## Assessment and certification (ASVS p.14)
- [from source] OWASP **does not certify** vendors, verifiers or software; "ASVS" seals/certifications are not official and call for caution (ASVS p.14).
- [from source] The verifier must state in the report the **scope** (including out-of-scope components, such as SSO), a summary of findings with **passes and fails** and how to fix the failures; running a tool and listing failures is not enough; keep evidence (work papers, proxy logs, scripts) (ASVS p.14).
- [from source] Non-applicable requirements may be excluded but with a stated **reason for non-applicability** (e.g. API without a client → much of V3 does not apply) (ASVS p.14).
- [from source] The test method is free but must be stated; the same confidence can come from manual pentest or from code analysis (ASVS p.14).

## How the package implements this
- `python -I scripts/asvs_checklist.py generate --level L2 --chapters 3,4` generates a checklist with status and evidence; `evaluate` computes coverage and only declares the level achieved if everything is `pass` or `na` **with justification** (ASVS p.14).
- `python -I scripts/asvs_lookup.py V5.3.4` / `--cwe 89` / free topic to cite a requirement with its page.

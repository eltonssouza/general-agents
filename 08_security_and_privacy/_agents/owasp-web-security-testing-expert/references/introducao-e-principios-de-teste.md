# Introduction and testing principles (WSTG ch. 2 and opening)

Page convention: **PDF page** (WSTG p.N). Printed number = N − 2 (chapter 2 starts on p.13 of the PDF, printed 11). Paraphrased; nothing here reproduces the text of the guide.

## Premises and tone of the guide

- The guide presents itself as a complete testing framework, not a simple checklist; it serves as a model for building testing programs or assessing other people's processes [from source] (WSTG p.13).
- The preface warns: isolated security testing is not a sufficient security measure, because the forms of failure are infinite and the tester's time is limited; the guide must be adapted to the context and **not used as a mere checklist**, since new vulnerabilities appear [from source] (WSTG p.7-8).
- Automatic tools help to scale and to enforce policy, but they are generic; the most serious flaws are usually in the business logic and in the application's own design [from source] (WSTG p.8).
- Roles that use the guide: developers, QA, security specialists, project managers [from source] (WSTG p.8).

## What to test, when to test

- Testing only after deployment is, according to the guide, ineffective and expensive; the best prevention is to include security in every phase of the SDLC [from source] (WSTG p.14).
- An effective program tests **people, process and technology** (education/awareness; policies and standards; implementation) [from source] (WSTG p.15-16).
- Analogy of the guide: testing only the frontal impact of a car would be the equivalent of testing only one technical part of the application [from source] (WSTG p.16).

## Scenario identifiers (lookup key)

- Format `WSTG-<category>-<number>`: category with 4 uppercase letters, number from 01 to 99 (e.g., WSTG-INFO-02 = second information gathering test) [from source] (WSTG p.16).
- IDs may change between versions; the guide recommends citing with the version, `WSTG-v42-INFO-02` for 4.2; without a version, the most recent one applies [from source] (WSTG p.16).
- Use versioned links (v42) and not `stable`/`latest` [from source] (WSTG p.16).

## Testing principles (WSTG p.16-19)

Summary of the principles named by the guide:
1. **There is no silver bullet**: scanners and WAFs are for low-hanging fruit; security is a process, not a product (p.16).
2. **Think strategically, not tactically**: the "patch-and-penetrate" model fixes the reported bug without investigating the root cause, and the window of vulnerability shrinks every year (p.16-17).
3. **The SDLC is king**: integrate security into every phase; descriptive frameworks (BSIMM) vs. prescriptive ones (OpenSAMM, ISO/IEC 27034) (p.17).
4. **Test early and often**; education of devs and QA (p.17-18).
5. **Automation**: include DAST, SAST and SCA in CI/CD or in scheduled runs, to keep a baseline and find "low-hanging fruit" (p.18).
6. **Understand the security scope**: asset classification, conversation with legal, legal requirements (the guide cites GLBA, SB-1386 and GDPR as examples) (p.18).
7. **The right mindset**: think outside what is expected, find developers' assumptions that can be subverted (p.18).
8. **Understand the subject**: architecture documentation, data flows, use cases, including the explicitly forbidden uses (p.18).
9. **Use the right tools**, knowing what they do not do (p.18).
10. **The devil is in the details**: a superficial review gives false confidence; eliminate false positives, since an incorrect finding undermines the rest of the report (p.18-19).
11. **Use the source code when available**: black-box does not walk through the whole code base (p.19).
12. **Develop metrics** (show whether training is lacking, whether a mechanism is poorly understood, whether problems are decreasing; IEEE as a starting point) (p.19).
13. **Document the results**: formal record of what was done, by whom, when, with findings; agreed format; reproducible by another tester; clear to the business owner and to the developer (p.19).

## Testing techniques and their limits (WSTG p.19-25)

| Technique | Advantages noted | Disadvantages noted | Page |
|---|---|---|---|
| Manual inspection and reviews | no supporting technology, flexible, early in the SDLC; tests people and process ("trust, but verify" model) | time-consuming, material not always available, requires skill | 20 |
| Threat modeling | practical view of the attacker, flexible, early; follows an approach based on NIST 800-30 (decompose, classify assets, vulnerabilities, threats, mitigation) | a good model does not guarantee good software | 20-21 |
| Source code review | completeness, accuracy, speed | requires devs with security skills, may miss compiled libraries, does not see runtime errors, deployed code may differ | 21 |
| Penetration testing | can be fast/cheap, requires less skill than code review, tests the code actually exposed | too late in the SDLC, only "frontal" impact | 21-22 |

- Penetration testing is a small, representative sample of the risks, and must not be the main or only technique; focused penetration testing serves to confirm the fix of already known vulnerabilities [from source] (WSTG p.22).
- **Balanced approach**: combine manual reviews, technical testing and tests integrated into CI/CD in all phases, with more emphasis on the early stages [from source] (WSTG p.22-23). If only pentest is possible (no code), it is better than nothing, but challenge the assumption of no access to the code (p.22).
- Scanners: examples from the guide show why black-box automation is not complete — a "magic" backdoor parameter (p.24-25) and a homemade MD5 signature scheme that a scanner would not recognize (p.25). Static analysis alone does not detect design flaws (p.25). The OWASP Benchmark evaluates speed, coverage and accuracy of tools (p.24).

## Deriving security test requirements (WSTG p.25-30)

- Objectives of the test: validate that the controls work as expected (security requirements) and that they are implemented with few or no vulnerabilities (p.25).
- Requirements come from regulations, industry standards and internal policies (the guide cites FFIEC, PCI DSS as examples), and must be mapped to verifiable items (p.26).
- **Positive** requirements (expected functionality, pass/fail; e.g., lockout after N failures) and **negative/risk-driven** requirements (what must not happen; harder to test, require risk analysis and threat modeling) (p.28-29).
- Threat taxonomy with **STRIDE** and root cause (design flaw, code bug, insecure configuration) [from source] (WSTG p.27).
- **Use and abuse cases (misuse cases)** in 4 steps: functional scenario, negative scenario, use and abuse cases in a graph, extract requirements (the example is authentication: password complexity, lockout after five attempts, generic error messages) (p.29-30).
- Combined test data (pentest + code analysis) help distinguish a real vulnerability from a non-exploitable one and calculate the risk rating; high and medium prioritized, low in future releases [from source] (WSTG p.26-27).

## Tests integrated into the development workflow (WSTG p.30-34)

- **Developer** (coding phase): security unit tests (the generic suite covers identity/authentication/access control, input validation and encoding, cryptography, user and session, error handling, auditing and logging); static analysis results can be check-in *gates*; JUnit, NUnit, CUnit cited (p.32-33).
- **Functional tester** (integration, system and UAT): validate "defense in depth", simulate a real attack, handle vulnerabilities found in the code; UAT is useful for configuration (server with least privilege, valid certificate, essential services, clean web root) (p.33-34). An internal test case "cheat sheet" can help (p.33).
- Gray-box: partial knowledge (e.g., of session management) helps assess logout/timeout (p.31).
- There is an acceptance policy: high-risk vulnerabilities must be fixed before deployment, unless the risk is acknowledged and accepted (p.31).

## Metrics and reporting (WSTG p.34-36)

- Absolute and comparative measures; containment metrics; goals with deadlines (p.34-35).
- Warning: the absence of findings does not mean good software; unknown problems are not tested; a sophisticated tool does not replace an experienced tester (p.35).
- **Reporting best practices** (6 items): vulnerability category by type; the security threat it is exposed to; root cause (bug or flaw); testing technique that found it; remediation or countermeasure; **severity** (high/medium/low or CVSS; CVSS, maintained by FIRST, is the most widely used metric) [from source] (WSTG p.35-36).
- Guide the developer to re-test and fix (with secure code examples, configuration changes and references) (p.36). The severity rating contributes to the risk and to prioritizing remediation, with external analysis of impact and exposure (p.36).
- Business cases per stakeholder: developers, project managers, ISOs, auditors, CIO/CISO (security ROI) (p.36).

## Boundary
- In-depth threat modeling and STRIDE in detail: forward to `infosec-strategy-threat-modeling-expert`.
- Code review and ASVS requirements: forward to `owasp-asvs-code-review-expert`.

# Testing framework in the SDLC and pentest methodologies (WSTG ch. 3 and ch. 4.0)

Pages = PDF (printed = N − 2). Paraphrased.

## The framework (WSTG p.37-41)

- The framework is a flexible, non-prescriptive reference for organizations to build their strategic testing process; it is **not** aimed at consultants with a tactical scope [from source] (WSTG p.38).
- Pentest is seen as an implementation/awareness technique, inefficient at finding bugs on its own; software quality requires testing in definition, design, development, deployment and maintenance [from source] (WSTG p.38).

| Phase | Activities (labels of the guide) | Page |
|---|---|---|
| 1 Before development | 1.1 define an SDLC with security at every stage; 1.2 review policies and standards (e.g., the language's secure coding standard, cryptography standard); 1.3 measurement and traceability criteria defined before starting | 38-39 |
| 2 Definition and design | 2.1 review security requirements (test assumptions and gaps; example "registered" vs "authenticated"); 2.2 review design and architecture (e.g., centralized authorization, core validation framework); 2.3 create/review UML models; 2.4 create/review threat models (mitigate, accept or transfer) | 39-40 |
| 3 Development | 3.1 *code walkthrough* (overview with the devs, not a review); 3.2 static code review against checklists (business requirements, OWASP Top 10/Guide, language-specific, regulatory) | 40 |
| 4 Deployment | 4.1 application pentest; 4.2 configuration management testing (nothing left in a vulnerable default) | 40 |
| 5 Maintenance and operations | 5.1 operational management reviews; 5.2 monthly or quarterly *health checks*; 5.3 change verification after each change approved in QA and deployed | 41 |

- According to the guide, in return on resources invested, static code review produces higher-quality results than other methods and depends less on the reviewer's skill, without being a silver bullet (WSTG p.40).
- Figure 3-1 (typical testing flow in the SDLC, p.42) is an image; there is no verifiable text.

## Pentest methodologies cited (WSTG p.43-45)

The guide lists, without going into depth: OWASP WSTG, MSTG (mobile), Firmware Security Testing Methodology; **PTES** (7 phases: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, reporting); PCI DSS requirement 11.3 and the PCI pentest guide; Penetration Testing Framework (PTF); NIST SP 800-115 (review techniques, target identification, vulnerability validation, planning, execution, post-test); OSSTMM (operational security, with a STAR report) [from source] (WSTG p.43-45).
- Note: the guide does not provide details of these methodologies; consult the original sources. PTES pre-engagement is the only place in the guide with an explicit mention of interactions prior to testing (p.43); rules of engagement and formal authorization are `[extrapolation]` beyond that (see `procedimentos.md`).

## Chapter 4 methodology (WSTG p.47-48)

- Definitions of the guide: **vulnerability** = flaw or weakness in design, implementation, operation or management that can be exploited against security objectives; **threat** = anything (external attacker, internal user, instability) that can harm assets by exploiting a vulnerability; **test** = action that demonstrates that the application meets the stakeholders' requirements (p.47).
- The chapter 4 testing method is based on **black box** (tester knows little or nothing) with the tester / tools and methodology / application model (p.47-48).
- **Passive testing**: understand the logic, explore as a user, use an HTTP proxy to observe requests; at the end the tester must know all access points (headers, parameters, cookies, APIs); every entry point is a target of active testing (p.48). Example from the guide: `?a=1&b=1` exposes two access points (p.48).
- **Active testing**: 12 categories — Information Gathering, Configuration and Deployment Management, Identity Management, Authentication, Authorization, Session Management, Input Validation, Error Handling, Cryptography, Business Logic, Client-side, API Testing (p.48). Each category has IDs `WSTG-INFO`, `CONF`, `IDNT`, `ATHN`, `ATHZ`, `SESS`, `INPV`, `ERRH`, `CRYP`, `BUSL`, `CLNT`, `APIT` (p.3-6 and map in `INDEX.md`).
- Structure of each test: ID, Summary, Test Objectives, How to Test, Remediation and Tools/References (check on each page; the format is standardized in 4.2 per the frontispiece, p.10).

# Software security, SDLC and DevSecOps (DZ Ch.8, PDF p.222-252; printed p.205-235)

DZ citations = PDF page (printed = PDF − 17). Paraphrase is mine. **Boundary:** detailed verification requirements (OWASP ASVS), code review and web testing (WSTG) belong to `owasp-asvs-code-review-expert` and `owasp-web-security-testing-expert`; what stays here is the DZ's strategy and process view, which cites OWASP Proactive Controls and ASVS only in passing.

## Premise (DZ p.222-224)
- **[from source] (DZ p.222)** Software is a large attack surface and is usually bought or developed without security oversight; the chapter's goal: requirements for third-party or in-house software, reduce the likelihood of vulnerabilities and mitigate with a focus on the CIA triad (p.223).
- **[from source] (DZ p.223-224)** Heartbleed case (CVE-2014-0160, OpenSSL): the flaw existed since 2011 and went unnoticed for 3 years despite being open source; lesson: transparency does not guarantee review; manage expectations, use risk and policies proportional to the value of the assets.
- **[from source] (DZ p.225-226)** *Caveat emptor*: diligence is the buyer's and must be kept as evidence (due diligence, due care). Contracts that define the vendor's responsibilities are a mitigation; if the vendor refuses, use other mitigations; document agreements and reference them in risk assessments; apply least privilege, monitor and reassess throughout the software lifecycle.

## Secure SDLC (DZ p.226-233)
- **[from source] (DZ p.226)** The SDLC brings security to development through processes; ask vendors how they practice it. (ISC)² offers the CSSLP, with 8 domains (concepts, requirements, architecture/design, implementation, testing, lifecycle management, deployment/operation/maintenance, supply chain).
- **[from source] (DZ p.227-228)** The author divides the SDLC into **5 stages**: (1) business and security requirements, (2) secure design, (3) test plans, (4) secure development, (5) testing. It works with Waterfall, Agile and DevOps (the DevOps diagram aligns with the 5 steps if the security requirements are defined in planning).
- **[from source] (DZ p.228)** Requirements: define **security and privacy** requirements, test against them, and consider **abuse cases** (how a malicious actor could misuse the software): "essentially threat modeling with attention to the attack surface"; mitigate in proportion to the risk.
- **[from source] (DZ p.229)** Design: architecture with preventive, detective and responsive controls, *secure by design*. Tests: beyond unit/integration/system/acceptance, security testing planned before development; ISO/IEC/IEEE 29119 standard (5 parts; part 3 provides documentation templates) with the author's caveats about criticisms of the standard (p.229-231).
- **[from source] (DZ p.231)** At an agile pace, the test strategy fits in a few lines after the **user story** ("As a <role>, I want <requirement>, so that <use case>").
- **[from source] (DZ p.232)** Secure development: input/output sanitization, error handling without excess information, resource and concurrency management, isolation (sandbox/containers), cryptography, access control structures (trust zones, least privilege, RBAC).
- **[from source] (DZ p.232-233)** Testing throughout the process: architecture analysis, dependencies, SAST, DAST, **code review** (applies the two-person principle: two must conspire to insert a backdoor; not infallible), pentest on relevant changes; at a minimum, verify the **OWASP Top 10 Proactive Controls**, with procedures and training.

## OWASP Top 10 Proactive Controls according to the DZ (DZ p.234-242)
The author goes through the OWASP's 10 controls (the version he cites; **[DATED]**: check the current version in the ASVS agent):
1. **Define security requirements** (reuse; ASVS as a collection; user stories and *misuse stories*, p.234-235; example with ASVS 3.0.1).
2. Security **frameworks and libraries**: trusted and maintained sources, document them in the asset catalog (Snyk), update (OWASP Dependency-Check, NPM), least privilege (p.235-236).
3. **Secure database access**: query parameterization, secure configuration based on a baseline, secure channel for credentials, encryption at rest/in transit, error messages and logs without excess (p.236-237).
4. **Encode and escape data** (XSS, command injection) (p.237).
5. **Validate all inputs** (syntax, allowlist; do not rely on the frontend; treat all input as malicious) (p.238).
6. **Digital identity**: NIST 800-63B; level 1 example with password, check against common passwords and minimum length of 10 without MFA (**[DATED]**: NIST recommendations have changed; confirm); password reset with a side channel; cookies with expiration, HttpOnly and Secure (p.238-239).
7. **Enforce access control** with RBAC, deny by default, no *hardcoded* rules, logs (p.239).
8. **Protect data everywhere**: classification, TLS in transit, encryption at rest with planning (risk of misconfiguration affecting availability), cryptographic libraries, secrets as crown jewels (no hardcoding; rotate; vault) (p.240-241).
9. **Logging and monitoring**: do not send debugging PII, align timestamps, avoid log forging, access control and redundancy of logs (p.241).
10. **Handle errors and exceptions**: minimal messages to the user, internal detail sufficient for support/forensics (p.241-242).
Further reading cited: MS-SDL, NIST 800-160, CLASP (p.243).

## Assessing third-party software (DZ p.243-248)
- **[from source] (DZ p.243-245)** SaaS: responsibilities change, but the secure choice remains the customer's; testing the vendor's infrastructure requires permission (legal risk and of affecting other customers).
- **[from source] (DZ p.245-246)** Due diligence + contract: you can ask for the latest pentest report, permission to test, remediation SLAs and a channel to report vulnerabilities; **VSAQ** (spreadsheets; the author laments the lack of standardization and cites Google's vsaq project); document the residual risk and decide to mitigate, accept or avoid.
- **[from source] (DZ p.246)** SDLC due diligence: ask *how* the vendor follows the SDLC and request evidence; if it does not, highlight the risk to the decision makers.
- **[from source] (DZ p.247)** **Bug bounty** (Bugcrowd, HackerOne) as a signal; with no pentest report or bounty, ask how they prioritize vulnerabilities and what tools they use. On-prem software: question "why does it need to run as admin?", include it in the scans, talk to the vendor.
- **[from source] (DZ p.248)** **FOSS**: transparent and peer-reviewed, but Heartbleed shows the risk; apply the same steps (dependencies, SAST, DAST, scans), via a security pipeline; vendors also use open source: include it in the VSAQ.

## In-house software and DevSecOps (DZ p.248-251)
- **[from source] (DZ p.248-249)** In-house software includes that of outsourced teams and open source treated as in-house; outsourced teams follow their policies or there is an agreement to close gaps.
- **[from source] (DZ p.249-250)** Repositories: issue trackers, protected branches (code review, tests, separation of duties, two-person), **signed commits** (non-repudiation and integrity), infrastructure configurations in the repository with the same scrutiny.
- **[from source] (DZ p.250)** CI/CD pipelines reduce developers' and admins' access to least privilege (no changes to production outside the pipeline). **DevSecOps** = security embedded in the DevOps cycle through automation.
- **[from source] (DZ p.250-251)** Example flow: the dev works on a branch with an IDE that checks secrets and secure patterns; the commit is authorized and logged; CI runs a dependency scanner, SAST, secrets checker, container/IaC auditor, DAST in an ephemeral environment; then code review by another dev, human testing and merge; CD deploys to the next environment. It requires careful implementation and defined expectations.

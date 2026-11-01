# ASVS 4.0.3 x OCRG v2.0 integration — how the two sources complement each other

**Labeling notice**: the mapping below is `[inference]` by the package. Neither work provides a map to the other (the OCRG cites the ASVS only in reference links, OCRG p.52, 62 and 82; the ASVS mentions code review as an activity, e.g. ASVS p.26 and 45, but does not cite the Code Review Guide). Each cell was checked against the text of each source. Pages: ASVS = footer = PDF; OCRG = PDF (printed = N − 1).

## Role of each source
| | ASVS 4.0.3 (2021) | OCRG v2.0 (2017) |
|---|---|---|
| Nature | **standard of verifiable requirements** (278 active, 3 levels, CWE, NIST 800-63) | **guide on how to review code** (process, threat modeling, mechanics per vulnerability, examples per language) |
| Question it answers | "What must be true for the application to be secure, at what level?" (ASVS p.11-13) | "How do I, as a reviewer, look for and confirm each type of flaw in the code?" (OCRG p.10-11) |
| Strength | modern coverage (JWT, SSRF, deserialization, GraphQL, SBOM, CSP, SameSite), traceable numbering, levels, certification | methodology (risk, when to review, metrics), applied threat modeling, crawling, source-to-sink, Java/.NET/PHP/C examples |
| Weakness | does not teach the step-by-step of review; V1/V2.4/V2.10/V6/V7 require access to the code (ASVS p.26, 30, 42-45) | 2017 content (categories A1-A10 of an earlier Top 10 edition, .NET 2-4, Struts 1), outdated password advice |

## Topic map (OCRG → ASVS)
| Topic | OCRG (PDF) | ASVS (IDs) |
|---|---|---|
| A1 SQL/ORM/JSON injection | OCRG p.45-53 | V5.3.4, V5.3.5, V5.3.6, V1.5.4 |
| Input validation | OCRG p.55-58 | V5.1.3, V5.1.4, V1.5.3, V5.1.1 |
| CSP and headers | OCRG p.53-55 | V14.4.1-V14.4.7 |
| A2 authentication | OCRG p.60-66 | V2.1.x, V2.2.1, V2.5.x, V2.7.x, V2.4.x |
| A2 session | OCRG p.66-70 | V3.1.1, V3.2.x, V3.3.x, V3.4.x, V3.7.1 |
| A3 XSS / DOM / client-side JS | OCRG p.72-77, 189-191 | V5.3.3, V5.3.1, V5.2.1, V5.2.4, V5.5.4, V14.4.3 |
| A4 IDOR / data binding | OCRG p.79-82 | V4.2.1, V4.1.2, V5.1.2 |
| A5 misconfiguration | OCRG p.84-117 | V14.1.3, V14.3.2, V14.3.3, V14.2.2, V14.1.x |
| A6 cryptography/sensitive data | OCRG p.119-131 | V6.1-V6.4, V8.3.x, V9.x, V2.4.x, V1.6.x |
| attack surface | OCRG p.131-133 | V1.1.4, V1.14.1, V1.8.1, V8.1.3 |
| A7 function-level authorization | OCRG p.135-139 | V4.1.1, V4.1.3, V4.1.5, V1.4.1, V1.4.4, V1.4.5, V13.1.4 |
| A8 CSRF | OCRG p.141-146 | V4.2.2, V13.2.3, V3.4.3 |
| A9 vulnerable components | OCRG p.148-149 | V14.2.1, V14.2.2, V14.2.4, V14.2.5, V1.14.3 |
| A10 redirects/forwards | OCRG p.151-153 | V5.1.5 |
| HTML5: postMessage, CORS, WebSockets | OCRG p.155-158 | V14.5.2, V14.5.3, V14.5.1, V9.1.1 |
| logging | OCRG p.161-163 | V7.1.x, V7.2.x, V7.3.x, V1.7.x |
| error handling | OCRG p.164-175 | V7.4.1-V7.4.3, V4.1.5, V6.2.1 |
| alerts and active defense | OCRG p.176-181 | V11.1.7, V11.1.8, V8.1.4 |
| race conditions | OCRG p.182-183 | V1.11.2, V1.11.3, V11.1.6 |
| buffer, format string, integer overflow | OCRG p.184-188 | V5.4.1-V5.4.3, V14.1.2 |
| threat modeling | OCRG p.32-39, 201-205 | V1.1.2, V1.1.4, V1.1.5, V11.1.5 |
| methodology/process | OCRG p.21-30 | V1.1.1, V1.1.6, V1.1.7 |
| checklist | OCRG p.197-200 | `asvs_checklist.py generate` |

## What the ASVS covers and the OCRG does not (verified by term search)
- **JWT/stateless tokens** (V3.5.3), **SameSite** and `__Host-` (V3.4.3, V3.4.4), **SSRF** (V5.2.6, V12.6.1), **deserialization** (V5.5.1-V5.5.3), **XXE** (V5.5.2; in the OCRG only links, OCRG p.51), **template injection** (V5.2.5), **HTTP parameter pollution** (V5.1.1), **GraphQL** (V13.4), **SOAP/REST** (V13.2-V13.3), **SBOM** (V14.2.5), **SRI** (V10.3.2, V14.2.3), **subdomain takeover** (V10.3.3), **TLS 1.2/1.3 and OCSP** (V9.1.3, V9.2.4), **zip bombs** (V12.1.2), **breached passwords/12+ characters** (V2.1.1, V2.1.7), **TOTP/FIDO/biometrics** (V2.2.x, V2.8.x), **malicious code** (V10), **IoT** (Appendix C).
## What the OCRG covers and the ASVS does not
- **Process**: risk-based review, pre/post-commit, who reviews, review report, metrics (cyclomatic complexity, risk density), "360 review" (OCRG p.15-16, 21-26, 40-43); **step-by-step threat modeling** (STRIDE/ASF/DREAD, DFD; OCRG p.32-39); **code crawling** (OCRG p.43, 206-218); **source-to-sink analysis** (OCRG p.18, 30); **examples per language** (Java, .NET, PHP, C/C++); **active defense/AppSensor** (OCRG p.179-181); **Java/.NET/IIS framework configuration** (OCRG p.84-117).

## Recommended joint workflow (`[inference]`)
1. Define the **ASVS level** by risk (ASVS p.11-13) and generate the checklist (`asvs_checklist.py generate --level L2`).
2. Plan the review by **module risk** (OCRG p.25-26) and prepare the context (OCRG p.27-30).
3. For each checklist requirement, use the OCRG to learn **how to verify it in the code** (the map above) and `ocrg_lint.py` to sweep for patterns; confirm manually.
4. Record `pass`/`fail`/`justified na` with evidence and use `asvs_checklist.py evaluate`; report scope, method and results (ASVS p.14) and the OCRG report fields (OCRG p.22-23).
5. When the OCRG and ASVS diverge, **ASVS 4.0.3 prevails** over OCRG 2017 on authentication/session/cryptography, and both are [DATED] against current sources (see `references/datado-e-tensoes.md`).

## Boundaries
- **Penetration testing** techniques and WSTG scripts: `owasp-web-security-testing-expert`. **LGPD/privacy** (legal basis, ROPA, DPIA): `privacy-lgpd-engineering-expert`; ASVS V8.3 (ASVS p.48) only gives the technical requirements. Organization-level threats/security engineering in general (Anderson, NIST): other agents in the folder.

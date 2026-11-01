# INDEX of the references (OWASP WSTG 4.2)

Source: **OWASP Web Security Testing Guide v4.2** (OWASP Foundation, 2020; CC BY 4.0 per the frontispiece, p.10), 465 PDF pages with native text. Abbreviation **WSTG**.

## Page convention
All citations use the **PDF page** (marker of the extracted text). **Printed page = PDF page − 2** (chapter 2 starts on p.13 of the PDF, printed 11; p.3 of the PDF, the table of contents, is printed 1). When citing, use `WSTG p.N`. To convert: `python -I scripts/wstg_lookup.py --printed N`.

## Lookup key
The guide identifies each test as `WSTG-<category>-<nn>` (p.16); versioned: `WSTG-v42-INFO-02`. The references, scripts and tests use the ID as the key, always with the page. Some IDs were **merged** (INFO-09 into INFO-08, INPV-03 into CONF-06, ERRH-02 into ERRH-01; p.86, 231, 339) and INPV-13 had its buffer overflow part removed (p.314). Subsections such as INPV-05.1 have no ID of their own in the guide: they are numbered sections of the table of contents (p.4-5).

## When to open each file
| Trigger | File |
|---|---|
| principles, techniques, test requirements, metrics, "why test" (ch. 2) | `introducao-e-principios-de-teste.md` |
| framework by SDLC phase, methodologies (PTES, NIST 800-115, OSSTMM), passive/active (ch. 3, 4.0) | `framework-sdlc-e-metodologias.md` |
| reconnaissance, fingerprint, metafiles, entry points (4.1, INFO) | `coleta-de-informacao-info.md` |
| configuration, backups, admin, HTTP methods, HSTS, subdomain takeover, cloud (4.2, CONF) | `configuracao-e-deploy-conf.md` |
| roles, registration, provisioning, account enumeration (4.3, IDNT) | `gestao-de-identidade-idnt.md` |
| login, default credentials, lockout, reset, security questions (4.4, ATHN) | `autenticacao-athn.md` |
| directory traversal, authorization bypass, escalation, IDOR (4.5, ATHZ) | `autorizacao-athz.md` |
| cookies, fixation, CSRF, logout, timeout, hijacking (4.6, SESS) | `gestao-de-sessao-sess.md` |
| XSS, HPP, general SQL injection (4.7, INPV-01 to 05) | `validacao-de-entrada-inpv-parte1.md` |
| SQLi per DBMS, NoSQL, ORM, LDAP, XML, SSI, XPath, IMAP/SMTP, code, LFI/RFI, command, SSTI, SSRF, smuggling, Host (INPV-05.x to 19) | `validacao-de-entrada-inpv-parte2.md` |
| error handling, TLS, padding oracle, weak cryptography (4.8, 4.9) | `erros-e-criptografia-errh-cryp.md` |
| business logic and upload (4.10, BUSL) | `logica-de-negocio-busl.md` |
| DOM XSS, CORS, clickjacking, WebSockets, postMessage, storage, XSSI, GraphQL (4.11, 4.12) | `client-side-clnt-e-api-apit.md` |
| report, severity, appendices (ch. 5) | `relatorio-e-apendices.md` |
| scope and authorization, plan, execution, reporting, retest | `procedimentos.md` |
| terms | `glossario.md` |
| cases and anti-patterns of the guide | `casos-e-antipadroes.md` |
| what is outdated | `datado-desde-2020.md` |

## Reading coverage (honesty)
- **Read in full, page by page**: ch. 2 and 3 (p.13-45), 4.0-4.6 (p.46-216), 4.7 INPV-01 to INPV-05 general and INPV-04 (p.219-248), 4.8, 4.9, 4.10 (p.337-378), ch. 5 (p.440-442), appendix E (beginning).
- **Read by sampling (summary, objectives, remediation and titles)**: INPV-05.1 to 05.8 and INPV-06 to INPV-19 (p.249-335), ch. 4.11 and 4.12 (p.380-438), appendices A-D and F (p.444-465). In those parts the operational core ("how to test" with payloads) was **not** transcribed, as a safety decision; the agent points to the guide.

## Scripts (Python 3 stdlib, no network, deterministic; run with `python -I`)
- `scripts/wstg_lookup.py` — lookup by ID/topic/page; `--gaps` (NOT COVERED), `--datado`.
- `scripts/test_plan_generator.py` — coverage checklist from the scope (with an authorization gate).
- `scripts/finding_template.py` — finding template, report skeleton, field validation.
- `scripts/wstg_index.json` — map ID → title → pages → reference (verified against the PDF by `tests/verify_citations.py`).

## Map ID → pages (WSTG, PDF page)
| ID | Title (guide) | Pages | Reference |
|---|---|---|---|
| WSTG-INFO-01 | Conduct Search Engine Discovery Reconnaissance for Information Leakage | 50-53 | `coleta-de-informacao-info.md` |
| WSTG-INFO-02 | Fingerprint Web Server | 54-57 | `coleta-de-informacao-info.md` |
| WSTG-INFO-03 | Review Webserver Metafiles for Information Leakage | 58-61 | `coleta-de-informacao-info.md` |
| WSTG-INFO-04 | Enumerate Applications on Webserver | 62-67 | `coleta-de-informacao-info.md` |
| WSTG-INFO-05 | Review Webpage Content for Information Leakage | 68-71 | `coleta-de-informacao-info.md` |
| WSTG-INFO-06 | Identify Application Entry Points | 72-75 | `coleta-de-informacao-info.md` |
| WSTG-INFO-07 | Map Execution Paths Through Application | 76-77 | `coleta-de-informacao-info.md` |
| WSTG-INFO-08 | Fingerprint Web Application Framework | 78-85 | `coleta-de-informacao-info.md` |
| WSTG-INFO-09 | Fingerprint Web Application (merged into INFO-08 (Fingerprint Web Application Framework; p.86)) | 86 | `coleta-de-informacao-info.md` |
| WSTG-INFO-10 | Map Application Architecture | 87-88 | `coleta-de-informacao-info.md` |
| WSTG-CONF-01 | Test Network Infrastructure Configuration | 90-92 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-02 | Test Application Platform Configuration | 93-98 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-03 | Test File Extensions Handling for Sensitive Information | 99-101 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-04 | Review Old Backup and Unreferenced Files for Sensitive Information | 102-107 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-05 | Enumerate Infrastructure and Application Admin Interfaces | 108-110 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-06 | Test HTTP Methods | 111-114 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-07 | Test HTTP Strict Transport Security | 115-116 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-08 | Test RIA Cross Domain Policy | 117-118 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-09 | Test File Permission | 119 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-10 | Test for Subdomain Takeover | 120-123 | `configuracao-e-deploy-conf.md` |
| WSTG-CONF-11 | Test Cloud Storage | 124-126 | `configuracao-e-deploy-conf.md` |
| WSTG-IDNT-01 | Test Role Definitions | 128-129 | `gestao-de-identidade-idnt.md` |
| WSTG-IDNT-02 | Test User Registration Process | 130-131 | `gestao-de-identidade-idnt.md` |
| WSTG-IDNT-03 | Test Account Provisioning Process | 132-133 | `gestao-de-identidade-idnt.md` |
| WSTG-IDNT-04 | Testing for Account Enumeration and Guessable User Account | 134-137 | `gestao-de-identidade-idnt.md` |
| WSTG-IDNT-05 | Testing for Weak or Unenforced Username Policy | 138 | `gestao-de-identidade-idnt.md` |
| WSTG-ATHN-01 | Testing for Credentials Transported over an Encrypted Channel | 140-144 | `autenticacao-athn.md` |
| WSTG-ATHN-02 | Testing for Default Credentials | 145-147 | `autenticacao-athn.md` |
| WSTG-ATHN-03 | Testing for Weak Lock Out Mechanism | 148-150 | `autenticacao-athn.md` |
| WSTG-ATHN-04 | Testing for Bypassing Authentication Schema | 151-156 | `autenticacao-athn.md` |
| WSTG-ATHN-05 | Testing for Vulnerable Remember Password | 157 | `autenticacao-athn.md` |
| WSTG-ATHN-06 | Testing for Browser Cache Weaknesses | 158-160 | `autenticacao-athn.md` |
| WSTG-ATHN-07 | Testing for Weak Password Policy | 161 | `autenticacao-athn.md` |
| WSTG-ATHN-08 | Testing for Weak Security Question Answer | 162-163 | `autenticacao-athn.md` |
| WSTG-ATHN-09 | Testing for Weak Password Change or Reset Functionalities | 164-165 | `autenticacao-athn.md` |
| WSTG-ATHN-10 | Testing for Weaker Authentication in Alternative Channel | 166-168 | `autenticacao-athn.md` |
| WSTG-ATHZ-01 | Testing Directory Traversal File Include | 170-174 | `autorizacao-athz.md` |
| WSTG-ATHZ-02 | Testing for Bypassing Authorization Schema | 175-179 | `autorizacao-athz.md` |
| WSTG-ATHZ-03 | Testing for Privilege Escalation | 180-182 | `autorizacao-athz.md` |
| WSTG-ATHZ-04 | Testing for Insecure Direct Object References | 183-184 | `autorizacao-athz.md` |
| WSTG-SESS-01 | Testing for Session Management Schema | 186-191 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-02 | Testing for Cookies Attributes | 192-195 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-03 | Testing for Session Fixation | 196-198 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-04 | Testing for Exposed Session Variables | 199-201 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-05 | Testing for Cross Site Request Forgery | 202-207 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-06 | Testing for Logout Functionality | 208-210 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-07 | Testing Session Timeout | 211-212 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-08 | Testing for Session Puzzling | 213-214 | `gestao-de-sessao-sess.md` |
| WSTG-SESS-09 | Testing for Session Hijacking | 215-216 | `gestao-de-sessao-sess.md` |
| WSTG-INPV-01 | Testing for Reflected Cross Site Scripting | 219-224 | `validacao-de-entrada-inpv-parte1.md` |
| WSTG-INPV-02 | Testing for Stored Cross Site Scripting | 225-230 | `validacao-de-entrada-inpv-parte1.md` |
| WSTG-INPV-03 | Testing for HTTP Verb Tampering (merged into CONF-06 (Test HTTP Methods; p.231)) | 231 | `validacao-de-entrada-inpv-parte1.md` |
| WSTG-INPV-04 | Testing for HTTP Parameter Pollution | 232-235 | `validacao-de-entrada-inpv-parte1.md` |
| WSTG-INPV-05 | Testing for SQL Injection | 236-248 | `validacao-de-entrada-inpv-parte1.md` |
| WSTG-INPV-05.1 | Testing for Oracle (section 4.7.5.1) | 249-255 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-05.2 | Testing for MySQL (section 4.7.5.2) | 256-260 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-05.3 | Testing for SQL Server (section 4.7.5.3) | 261-267 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-05.4 | Testing PostgreSQL (section 4.7.5.4) | 268-271 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-05.5 | Testing for MS Access (section 4.7.5.5) | 272-275 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-05.6 | Testing for NoSQL Injection (section 4.7.5.6) | 276-278 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-05.7 | Testing for ORM Injection (section 4.7.5.7) | 279-280 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-05.8 | Testing for Client-side SQL Injection (section 4.7.5.8) | 281-282 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-06 | Testing for LDAP Injection | 283-285 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-07 | Testing for XML Injection | 286-293 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-08 | Testing for SSI Injection | 294-295 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-09 | Testing for XPath Injection | 296-297 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-10 | Testing for IMAP SMTP Injection | 298-302 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-11 | Testing for Code Injection | 303-304 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-11.1 | Testing for Local File Inclusion (section 4.7.11.1) | 305-308 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-11.2 | Testing for Remote File Inclusion (section 4.7.11.2) | 309 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-12 | Testing for Command Injection | 310-313 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-13 | Testing for Format String Injection (Buffer Overflow removed) (buffer overflow removed (p.314); format string on p.315) | 314-317 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-14 | Testing for Incubated Vulnerability | 318-320 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-15 | Testing for HTTP Splitting Smuggling | 321-324 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-16 | Testing for HTTP Incoming Requests | 325-326 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-17 | Testing for Host Header Injection | 327-328 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-18 | Testing for Server-side Template Injection | 329-332 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-INPV-19 | Testing for Server-Side Request Forgery | 333-335 | `validacao-de-entrada-inpv-parte2.md` |
| WSTG-ERRH-01 | Testing for Improper Error Handling | 337-338 | `erros-e-criptografia-errh-cryp.md` |
| WSTG-ERRH-02 | Testing for Stack Traces (merged into ERRH-01 (Testing for Improper Error Handling; p.339)) | 339 | `erros-e-criptografia-errh-cryp.md` |
| WSTG-CRYP-01 | Testing for Weak Transport Layer Security | 341-343 | `erros-e-criptografia-errh-cryp.md` |
| WSTG-CRYP-02 | Testing for Padding Oracle | 344-346 | `erros-e-criptografia-errh-cryp.md` |
| WSTG-CRYP-03 | Testing for Sensitive Information Sent via Unencrypted Channels | 347-349 | `erros-e-criptografia-errh-cryp.md` |
| WSTG-CRYP-04 | Testing for Weak Encryption | 350-352 | `erros-e-criptografia-errh-cryp.md` |
| WSTG-BUSL-01 | Test Business Logic Data Validation | 357-358 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-02 | Test Ability to Forge Requests | 359-360 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-03 | Test Integrity Checks | 361-363 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-04 | Test for Process Timing | 364-366 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-05 | Test Number of Times a Function Can Be Used Limits | 367-368 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-06 | Testing for the Circumvention of Work Flows | 369-370 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-07 | Test Defenses Against Application Misuse | 371-372 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-08 | Test Upload of Unexpected File Types | 373-374 | `logica-de-negocio-busl.md` |
| WSTG-BUSL-09 | Test Upload of Malicious Files | 375-378 | `logica-de-negocio-busl.md` |
| WSTG-CLNT-01 | Testing for DOM-Based Cross Site Scripting | 380-382 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-02 | Testing for JavaScript Execution | 383-384 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-03 | Testing for HTML Injection | 385-386 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-04 | Testing for Client-side URL Redirect | 387-388 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-05 | Testing for CSS Injection | 389-390 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-06 | Testing for Client-side Resource Manipulation | 391-392 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-07 | Testing Cross Origin Resource Sharing | 393-395 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-08 | Testing for Cross Site Flashing | 396-401 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-09 | Testing for Clickjacking | 402-411 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-10 | Testing WebSockets | 412-414 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-11 | Testing Web Messaging | 415-417 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-12 | Testing Browser Storage | 418-421 | `client-side-clnt-e-api-apit.md` |
| WSTG-CLNT-13 | Testing for Cross Site Script Inclusion | 422-427 | `client-side-clnt-e-api-apit.md` |
| WSTG-APIT-01 | Testing GraphQL | 428-438 | `client-side-clnt-e-api-apit.md` |
| INTRO-principios | Principles of Testing | 16-19 | `introducao-e-principios-de-teste.md` |
| INTRO-tecnicas | Testing Techniques Explained | 19-22 | `introducao-e-principios-de-teste.md` |
| INTRO-requisitos | Deriving Security Test Requirements | 25-30 | `introducao-e-principios-de-teste.md` |
| INTRO-fluxos | Security Tests Integrated in Development and Testing Workflows | 30-36 | `introducao-e-principios-de-teste.md` |
| FRAMEWORK | The OWASP Testing Framework (Phases 1-5) | 37-42 | `framework-sdlc-e-metodologias.md` |
| METODOLOGIAS | Penetration Testing Methodologies | 43-45 | `framework-sdlc-e-metodologias.md` |
| METODO-CAP4 | Web Application Security Testing 4.0 (passive/active) | 47-48 | `framework-sdlc-e-metodologias.md` |
| REPORTING | Reporting | 440-442 | `relatorio-e-apendices.md` |
| APENDICES | Appendices A-F | 444-465 | `relatorio-e-apendices.md` |

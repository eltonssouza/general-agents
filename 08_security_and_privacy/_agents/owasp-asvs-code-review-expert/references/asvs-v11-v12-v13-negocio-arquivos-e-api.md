# ASVS V11 Business logic (p.54-55), V12 Files and resources (p.56-57), V13 API and web services (p.58-60)

Source: ASVS 4.0.3. `L1/L2/L3` = required at that level.

## V11 — Business logic
- [from source] Objectives: the business logic flow is sequential, processed in order and **cannot be bypassed**; there are limits to detect/prevent automated attacks (e.g. continuous small transfers, "adding a million friends one by one"); high-value flows consider abuse cases and malicious actors, with protection against spoofing, tampering, information disclosure and elevation of privilege (ASVS p.54).
- [from source] Business logic security is so individual that **no checklist applies to all cases**; it must be designed, not added with a WAF or secure communication; the book recommends threat modeling in design sprints (e.g. OWASP Cornucopia) (ASVS p.54).

| ID | Requirement (paraphrase) | Levels | Page |
|---|---|---|---|
| V11.1.1 | steps of a flow for the same user processed **in sequential order, without skipping steps** | L1/L2/L3 | ASVS p.54 |
| V11.1.2 | flows processed in realistic human time (transactions not submitted too fast) | L1/L2/L3 | ASVS p.54 |
| V11.1.3 | appropriate limits per action/transaction, enforced **per user** | L1/L2/L3 | ASVS p.54 |
| V11.1.4 | anti-automation controls against excessive calls (mass exfiltration, business logic, uploads, DoS) | L1/L2/L3 | ASVS p.54 |
| V11.1.5 | business limits/validations against risks identified by threat modeling | L1/L2/L3 | ASVS p.54 |
| V11.1.6 | no TOCTOU or other race conditions in sensitive operations | L2/L3 | ASVS p.54 |
| V11.1.7 | monitor unusual activity from a business standpoint (out-of-order actions, what a normal user would never attempt) | L2/L3 | ASVS p.54 |
| V11.1.8 | configurable alerts for automated attacks/unusual activity | L2/L3 | ASVS p.54 |
- References (ASVS p.55): WSTG 4.1 Business Logic Testing; OWASP AppSensor and Automated Threats; Cornucopia.
- OCRG link: race conditions, security alerts and active defense (OCRG p.176-183): `references/ocrg-concorrencia-e-memoria.md` and `references/ocrg-logging-erros-alertas-e-defesa-ativa.md`.

## V12 — Files and resources
- [from source] Objectives: untrusted file data handled safely; files from untrusted sources stored **outside the web root** and with limited permissions (ASVS p.56). Zip bombs are pentestable, but they sit at L2+ to encourage careful design and manual testing and to avoid DoS from automated/inexperienced testing (ASVS p.56).

| Section | Requirements | Levels | Page |
|---|---|---|---|
| V12.1 upload | V12.1.1 reject large files that fill storage/cause DoS (L1); V12.1.2 compressed files (zip, gz, docx, odt) checked for maximum uncompressed size and number of files before decompression; V12.1.3 per-user size and count quota | V12.1.1 L1/L2/L3; V12.1.2-3 L2/L3 | ASVS p.56 |
| V12.2 integrity | V12.2.1 files from untrusted sources validated for the expected type **by content** | L2/L3 | ASVS p.56 |
| V12.3 execution | V12.3.1 file name metadata not used directly by the file system/framework; use a URL API against **path traversal**; V12.3.2 name ignored/validated against LFI; V12.3.3 against RFI/SSRF; V12.3.4 against Reflective File Download (Content-Type `text/plain` and `Content-Disposition` with a fixed name); V12.3.5 metadata not used directly in a system API (OS command injection) | L1/L2/L3 | ASVS p.56 |
| V12.3.6 | do not include/execute functionality from untrusted sources (unverified CDNs, JS libraries, npm, server DLLs) | L2/L3 | ASVS p.57 |
| V12.4 storage | V12.4.1 untrusted files **outside the web root**, with limited permissions; V12.4.2 antivirus on files from untrusted sources | L1/L2/L3 | ASVS p.57 |
| V12.5 download | V12.5.1 web layer serves only specific extensions (block .bak, .swp, .zip, .tar.gz etc. unless necessary); V12.5.2 direct requests to uploaded files never execute as HTML/JavaScript | L1/L2/L3 | ASVS p.57 |
| V12.6 SSRF | V12.6.1 server configured with an **allow list** of resources/systems to which it can send requests or load data from | L1/L2/L3 | ASVS p.57 |
- The OCRG treats upload only as an attack surface question (authentication, rate limit, size, type, antivirus: OCRG p.133) and mentions canonicalization and path traversal (OCRG p.55-56, 102); it does not cover SSRF.

## V13 — API and web service
- [from source] Objectives for trusted service layer APIs (JSON, XML, GraphQL): adequate authentication, session management and authorization; validation of every parameter that moves up in trust; effective controls for all API types, including cloud and serverless. Read the chapter **together with** the others: V13 does not duplicate API authentication or session (ASVS p.58).

| Section | Requirements | Levels | Page |
|---|---|---|---|
| V13.1 generic | V13.1.1 same encodings and parsers in all components (avoids parsing attacks in SSRF/RFI); V13.1.3 API URLs without sensitive information (API key, token); V13.1.4 authorization at the URI (controller/router) **and** at the resource (model permissions); V13.1.5 reject unexpected/missing content types (406/415) | V13.1.1,3 L1/L2/L3; V13.1.4-5 L2/L3 | ASVS p.58 |
| V13.2 REST | V13.2.1 enabled HTTP methods valid for the user/action (e.g. a regular user without DELETE/PUT); V13.2.2 **JSON schema validation** before accepting the input; V13.2.3 REST with cookies protected from CSRF (double submit cookie, CSRF nonces or Origin header check); V13.2.5 explicitly check the expected Content-Type; V13.2.6 headers and payload trusted in transit (TLS may suffice; per-message signing adds assurance and complexity) | V13.2.1-3 L1/L2/L3; V13.2.5-6 L2/L3 | ASVS p.58-59 |
| V13.3 SOAP | V13.3.1 XSD validation and then of each field, before processing; V13.3.2 payload signed with WS-Security | V13.3.1 L1/L2/L3; V13.3.2 L2/L3 | ASVS p.59 |
| V13.4 GraphQL | V13.4.1 query allow list **or** depth and quantity limits (and cost, in advanced scenarios) against DoS from expensive nested queries; V13.4.2 data layer authorization in the **business logic layer**, not in the GraphQL layer | L2/L3 | ASVS p.59 |
- [from source] JSON schema was in draft; combine it with parse validation (missing/extra fields) and value validation (type, format, length); monitor the schema libraries (ASVS p.58). XXE: do not use DTD validation and disable the framework's DTD evaluation (V14) (ASVS p.59). V13.1.2 and V13.2.4 were removed (ASVS p.58-59).
- References (ASVS p.60): OWASP Serverless Top 10/Project, Testing Guide, CSRF and REST cheat sheets, XXE Prevention, JSON Web Tokens, JSON Schema, SSRF (Orange Tsai).
- The OCRG **does not cover** REST, SOAP (only WSDL in the checklist), GraphQL or JWT (terms absent); from the OCRG the principle of server-side authorization at every point is worth keeping (OCRG p.135-139), along with messaging/CORS/WebSockets (OCRG p.155-158).

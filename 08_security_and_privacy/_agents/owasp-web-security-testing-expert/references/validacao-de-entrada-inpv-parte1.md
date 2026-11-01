# 4.7 Input validation, part 1 (WSTG-INPV-01 to INPV-05, general SQL injection)

Pages = PDF (WSTG p.N; printed = N − 2). Methodological level: this package does **not** reproduce attack strings, filter/WAF evasion techniques or DBMS-specific exploitation; for that the authorized tester consults the guide itself at the indicated pages. Everything here presupposes scope and authorization.

## WSTG-INPV-01 Reflected XSS (p.219-224)
- **Objectives** [from source]: identify variables reflected in the responses; assess the input accepted and the encoding applied on the way back (p.219).
- Concept: code executable by the browser injected into a single response, not stored; also called non-persistent or first-order; the central difficulty of prevention is the correct encoding of characters (p.219).
- Three-phase method: detect input vectors (including hidden ones: HTTP parameters, POST, hidden fields, predefined selections), analyze each vector with harmless test data that provokes a visible browser response, and verify the impact by examining the resulting HTML and which special characters were left unencoded (the relevant set depends on the context: HTML, attribute or JavaScript) (p.219-220).
- The guide reminds that filters (deny list, permissive allow list, non-recursive sanitization, WAF) can fail and that the test must assume the browser does not protect; prevention depends mainly on the application's sanitization/encoding (p.221-222). Evasion examples are on p.222-223 and in the XSS Filter Evasion Cheat Sheet; **not reproduced here**.
- Gray-box/white-box: analyze all received variables and the sanitization (p.223). Tools: Burp, ZAP, encoders/obfuscators (p.223-224).

## WSTG-INPV-02 Stored XSS (p.225-230)
- **Objectives**: identify stored input reflected on the client and assess the input accepted and the encoding (p.225). Classified by the guide as the most dangerous type, second-order, without needing a malicious link; especially serious in areas viewed by administrators (p.225).
- Where to look for stored input: profile, cart, file manager, preferences, forums, blogs, logs; also out-of-band channels; test administrative areas for data submitted by users (p.226).
- Upload: check whether HTML/TXT is accepted and whether the MIME can be set arbitrarily (MIME handling varies by browser) (p.228-229).
- Gray-box: input with special characters, response, controls, verify storage in the backend and review input variables (table of PHP/ASP/JSP variables on p.229). The guide cites browser exploitation frameworks (BeEF); `[inference]` their use is only justified with explicit authorization to demonstrate impact.

## WSTG-INPV-03 Verb tampering (p.231)
- Content **merged** into Test HTTP Methods (WSTG-CONF-06). See `configuracao-e-deploy-conf.md`.

## WSTG-INPV-04 HTTP Parameter Pollution (p.232-235)
- **Objectives**: identify the backend and the parsing method; assess injection points and try to bypass filters (p.233).
- Concept: the HTTP standards do not define how to handle repeated parameters; different components handle them differently, creating an "impedance mismatch" between filter and application (p.232). The guide reports real cases (WAF rule bypass, XSS in a printing system, blog takeover by a check on the first parameter and operation on the second) (p.232-233) and a table of behavior per technology (first, last occurrence, concatenation, list) (p.233) [DATED: 2009 table].
- Method: manual testing; repeat a parameter with a different value and compare the responses, with a three-request protocol (original, tampered, combined) and comparison (p.233-234). Rule of the guide: if the existing validation is sufficient and the server adopts only the first or last occurrence, pollution does not reveal a vulnerability; concatenation, components that use different occurrences or errors increase the probability (p.234). There is a client-side variant (p.234-235). Tools: ZAP passive/active scanners (p.235).

## WSTG-INPV-05 SQL injection (p.236-247)
- **Objectives**: identify SQL injection points; assess the severity and the level of access obtained (p.237).
- Definition: user data alters the query executed in the database due to lack of validation; possible effects include reading and altering data, administrative operations, file access and, in some cases, operating system commands (p.236).
- Classes: **in-band**, **out-of-band** and **inferential/blind** (p.236). Named exploitation techniques: UNION, boolean, error-based, out-of-band, time delay (p.236-237); exploitation of *stored procedures* with dynamic SQL (p.244-245). Automation by tools (SQLMap) (p.245).
- **Detection** [from source]: list all fields whose values may compose queries (including hidden ones, headers and cookies), test them **one at a time** keeping the others constant, and observe errors, 500 responses or custom error pages (which indicate the need for blind techniques); also examine the source code of the response (p.237-238). Typical contexts: authentication forms, searches and e-commerce (p.237).
- Identify the DBMS from error messages (MySQL, Oracle, SQL Server, PostgreSQL) (p.240). Exploitation details (UNION, character inference, error, out-of-band, time) are on p.240-244 and **are not reproduced**.
- Section on signature evasion (WAF/IPS) on p.245-247: **not reproduced**.
- **Remediation**: consult the SQL Injection Prevention Cheat Sheet, the Database Security Cheat Sheet and the Input Validation Cheat Sheet (p.247). `[extrapolation]` parameterized queries and least privilege of the database account are the usual practice; the guide's text on that page only refers to the cheat sheets.
- Tools: fuzz strings from wfuzz/FuzzDB, sqlmap and others (p.247).

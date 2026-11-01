# [DATED] and tensions between the sources

Convention: `[DATED]` = the source text describes something that has changed since the edition (OCRG v2.0 = 2017; ASVS 4.0.3 = October 2021). Items marked `[extrapolation]` come from knowledge outside the collection and must be **checked against current sources**; the package did not verify them in the PDF. Pages: ASVS = footer = PDF; OCRG = PDF (printed = N − 1).

## OCRG (2017) vs ASVS (2021) tensions — ASVS 4.0.3 prevails
| Subject | OCRG | ASVS | Page |
|---|---|---|---|
| Password complexity | require character types and indicate progress | **no** composition rules (V2.1.9) | OCRG p.61 / ASVS p.24 |
| Password rotation and history | change periodically, keep hash of the last 5+ (internal systems) | **no** rotation or history (V2.1.10); only check for breaches | OCRG p.61 / ASVS p.24, 26 |
| Minimum length | fewer than 10 characters is weak | ≥ 12 (V2.1.1), accept ≥ 64 (V2.1.2) | OCRG p.61 / ASVS p.23 |
| Review checklist | "Password Complexity Check enforced?" and "password expiration?" | same as above | OCRG p.197-198 / ASVS p.24 |
| Ciphers | "AES or 3DES?" as an acceptable strong cipher | prohibits small block ciphers (Triple-DES, Blowfish), ECB, MD5, SHA-1 except for compatibility (V6.2.5) | OCRG p.210 / ASVS p.42 |
| Password hashing | only mentions salt and SHA-256/512 (no slow derivation function) | salt + approved function with cost (PBKDF2 ≥ 100,000 iterations, bcrypt ≥ 10) (V2.4.1-V2.4.4) | OCRG p.128-131 / ASVS p.26 |
| Session tokens | ID of ≥ 128 bits (64 of entropy); "encrypted" cookies in the checklist | ≥ 64 bits of entropy (V3.2.2); `Secure`/`HttpOnly`/`SameSite`/`__Host-` (V3.4.x) | OCRG p.66, 199 / ASVS p.32-33 |
| FIPS 140-2 | use FIPS 140-2 validated modules for TLS/crypto | the ASVS dropped FIPS 140-2 as a reference and asks for a current TLS configuration tested with tools | OCRG p.121 / ASVS p.51 |
| Concurrent session control | alert "if the policy allows multiple sessions" | do **not** block concurrent sessions (the last authenticator wins) | OCRG p.69 / ASVS p.35 |
| Encrypting authentication cookies | checklist item | focus on flags and entropy/signature, not on an "encrypted cookie" | OCRG p.199 / ASVS p.33-34 |

## [DATED] OCRG items with no direct ASVS counterpart
- **Top 10**: the OCRG organizes the technical reference by the OWASP Top 10 categories A1-A10 **without stating the year** (OCRG p.2, 10) and with names such as A4 Insecure Direct Object Reference, A7 Missing Function Level Access Control and A10 Unvalidated Redirects And Forwards. `[extrapolation]` These categories correspond to an earlier edition of the Top 10, different from the **2017** Top 10 that ASVS 4.0.3 uses as a reference (ASVS p.9), and both were superseded by later editions; **do not map the OCRG's A1-A10 directly** to the categories of another edition without checking the current source.
- **Headers/browsers**: `X-XSS-Protection` (legacy XSS filter), `X-Content-Security-Policy` (Firefox < 23, IE 10), `X-WebKit-CSP` (Chrome < 25) (OCRG p.53-54); WebSockets hybi-00 and rfc6455 versions in old browsers (OCRG p.157); IE exceptions to the SOP (OCRG p.159).
- **Cryptography/TLS**: SSL/TLS terminology ("SSL v3.1 = TLS 1.0", "SSLv3/TLS") (OCRG p.120, 144); RSA keys ≥ 2048 and SHA-256+ as "best practice" (OCRG p.122); DES/SHA-0 insecure and MD5/SHA-1 to avoid (OCRG p.124, 130) — the advice to avoid them **remains** valid; US cryptography export regulation (2000) (OCRG p.128).
- **Languages/platforms**: PHP `mysql_*`/`addslashes` (OCRG p.48-49); .NET Framework 1.0-4.0, `Request Validation`, Code Access Security, 2010 FxCop, IIS 6/7 (OCRG p.50, 56, 73, 94-117); Struts 1, JEE 5/6, Tomcat/Jetty/JBoss/WebLogic of the time (OCRG p.84-92); classic ASP (OCRG p.114, 168, 214-216); IE-specific (OCRG p.159).
- **Compliance**: PCI-DSS 3.0/PA-DSS and numbering (6.3.2, 6.5) (OCRG p.19-20) and PCI DSS v2.0 req. 10 (OCRG p.163); `[extrapolation]` later PCI DSS versions renumbered requirements — confirm the applicable version before citing.
- **Legal**: the OCRG's statements about CAPTCHA in courts and about cryptography export are dated legal information (OCRG p.63, 128).
- **Architecture scope**: the OCRG assumes monolithic MVC/server applications; ASVS 4.0.3 explicitly started covering serverless, microservices, containers, CI/CD and federation (ASVS p.10).

## [DATED] / version items of the ASVS
- ASVS 4.0.3 (2021) was based on NIST 800-63-3 and the 2017 Top 10 (ASVS p.9). `[extrapolation]` There are later ASVS versions (the 5.x series) with **reorganized numbering and content**; this package covers **only** 4.0.3 and cites IDs in the `v4.0.3-x.y.z` format when there is ambiguity (ASVS p.13). Confirm the current version with the user.
- The ASVS itself anticipates removing SMS/e-mail as authenticators (ASVS p.25) and future prioritization by CWSS (ASVS p.10).

## Extraction limitations (transparency)
- OCRG: two-column text; some pages have code blocks in an order altered by extraction; the **figures** (surveys in figures 1-2, flow diagrams, Table 7 symbols, DFD figures) are images and are **not verifiable by text**: the content of those items here comes from reading the surrounding text.
- OCRG p.123: the PDF contains a loose editorial text ("P122 - b slightly incorrect points indents…") that is a **document artifact**, not book content; it was ignored.
- ASVS: levels (checkmarks) and CWE/NIST were extracted by **coordinates** from the PDF and by **text**, with 0 divergences between the two methods (`tests/relatorio-de-fidelidade.md`).

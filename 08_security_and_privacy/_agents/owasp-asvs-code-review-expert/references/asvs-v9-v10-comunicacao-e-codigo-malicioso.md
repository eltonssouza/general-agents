# ASVS V9 Communication (p.50-51) and V10 Malicious code (p.52-53)

Source: ASVS 4.0.3. `L1/L2/L3` = required at that level.

## V9 — Communication
### Objective (ASVS p.50)
- [from source] Require TLS or strong cryptography **regardless of content sensitivity**; follow the latest guidance (configuration, preferred algorithms/ciphers); avoid weak or deprecated algorithms/ciphers except as a last resort, and **disable insecure or obsolete ones**; keep up with industry guidance because it changes often (catastrophic breaks); use recent versions of TLS configuration review tools and **check the configuration periodically** (ASVS p.50).

| ID | Requirement (paraphrase) | Levels | Page |
|---|---|---|---|
| V9.1.1 | TLS on **all** client connectivity, with no fallback to insecure/unencrypted | L1/L2/L3 | ASVS p.50 |
| V9.1.2 | only strong cipher suites enabled (verify with a current TLS testing tool), the strongest preferred | L1/L2/L3 | ASVS p.50 |
| V9.1.3 | only the recommended TLS protocol versions (e.g. TLS 1.2 and 1.3), the latest preferred | L1/L2/L3 | ASVS p.50 |
| V9.2.1 | connections to/from the server with trusted TLS certificates; if internal/self-signed, trust only specific CAs/certificates | L2/L3 | ASVS p.51 |
| V9.2.2 | TLS on **all** inbound and outbound connections (management, monitoring, authentication, API, database, cloud, serverless, mainframe, external, partners), with no fallback | L2/L3 | ASVS p.51 |
| V9.2.3 | encrypted connections to external systems that involve sensitive information/function are authenticated | L2/L3 | ASVS p.51 |
| V9.2.4 | proper certificate revocation (e.g. OCSP Stapling) enabled | L2/L3 | ASVS p.51 |
| V9.2.5 | backend TLS connection failures are logged | L3 only | ASVS p.51 |
- [from source] "Server communication" goes beyond HTTP: ssh, middleware, database, mainframe, partner systems — everything encrypted to avoid "hard on the outside, trivial to intercept on the inside" (ASVS p.51).
- [from source] Reference note: the ASVS stopped pointing to FIPS 140-2 (a US standard, hard to apply globally); it is better to meet V9.1 by reviewing guides such as Mozilla's *Server Side TLS* or by generating known configurations and assessing them with up-to-date TLS tools (ASVS p.51). Other references: TLS Cheat Sheet and Pinning Guide.
- Contrast with the OCRG: the OCRG (2017) requires TLS on login, authenticated pages and internally, HSTS, keys ≥ 2048 and SHA-256+, certificates with FQDN (OCRG p.120-122); it does not mention TLS 1.2/1.3 versions (absent from the text) and speaks of "SSLv3/TLS" (OCRG p.144) `[DATED]`.

## V10 — Malicious code
### Objective (ASVS p.52)
- [from source] The code must not: be affected by poorly handled malicious activity; have time bombs or time-based attacks; "phone home" to malicious/unauthorized destinations; have backdoors, easter eggs, salami attacks, rootkits or unauthorized code controllable by an attacker. **Finding malicious code is proving a negative**, impossible to validate completely: make a best effort (ASVS p.52).

| Section | Requirements | Levels | Page |
|---|---|---|---|
| V10.1 code integrity | V10.1.1 code analysis tool that detects potentially malicious code (time functions, unsafe file operations, network connections) | L3 only | ASVS p.52 |
| V10.2 malicious code search | V10.2.1 source and third-party libraries without unauthorized "phone home"/collection (or with user permission); V10.2.2 no excessive permissions to privacy resources (contacts, camera, microphone, location) | L2/L3 | ASVS p.52 |
| V10.2 (L3) | V10.2.3 no back doors (hard-coded or undocumented accounts/keys, obfuscation, undocumented binary blobs, rootkits, anti-debug, hidden functionality); V10.2.4 no time bombs (search for date/time functions); V10.2.5 no malicious code (salami, logic bypass, logic bombs); V10.2.6 no easter eggs | L3 only | ASVS p.52-53 |
| V10.3 application integrity | V10.3.1 auto-update over secure channels and **signed**, with signature validation before installing; V10.3.2 integrity protections (code signing, **Subresource Integrity**), do not load code from untrusted sources (includes, modules, plugins, libraries, internet); V10.3.3 protection against **subdomain takeover** (expired DNS, dangling CNAMEs, transient buckets/serverless; check DNS name expiry/changes regularly) | L1/L2/L3 | ASVS p.53 |
- [from source] V10.1: the best defense is "trust, but verify"; leads should regularly review check-ins, especially those that access time, I/O or network; sanctions for malicious code must be clear in policies (ASVS p.52).
- [from source] V10.2: malicious code is rare and hard to detect; line-by-line review helps find logic bombs, but even the most experienced reviewer struggles; **complying with the section requires full access to the source code, including third-party libraries** (ASVS p.52).
- [from source] V10.3: after deployment it is still possible to insert malicious code; compliance is probably **operational and continuous** (ASVS p.53).
- References (ASVS p.53): two articles on subdomain takeover (Detectify Labs).
- Links: V1.10.1 (version control with traceability, ASVS p.20), V14.2.3 (SRI), V14.2.4-V14.2.5 (components from trusted repositories, SBOM) (ASVS p.62). The OCRG covers A9 (components) in `references/ocrg-a5-misconfiguracao-e-a9-componentes.md`.

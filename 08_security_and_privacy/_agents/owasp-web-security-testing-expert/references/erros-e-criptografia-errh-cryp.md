# 4.8 Error handling and 4.9 Weak cryptography (WSTG-ERRH-01/02, WSTG-CRYP-01 to CRYP-04)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased.

## WSTG-ERRH-01 Improper error handling (p.337-338)
- **Objectives** [from source]: identify the existing error output and analyze the different outputs returned (p.337).
- Risks listed: understanding internal APIs, mapping services and frameworks (attack chaining), collecting versions and types, DoS via deadlock/unhandled exception, and control bypass when an exception is not covered by the "happy path" logic (p.337). Forms of error: stack traces, timeouts, input mismatch, memory dumps (p.337).
- **Web servers**: provoke errors with nonexistent resources (404), existing folders (403, blank page, listing) and requests that violate the HTTP RFC (huge path, malformed headers, altered HTTP version), because even with errors handled in the application the integrated server may reveal itself (p.337-338).
- **Applications**: identify entry points, analyze the expected type (string, integer, JSON, XML), and do targeted fuzzing; if it is not possible to fuzz everything, choose inputs with the greatest chance of breaking the parser; refine the list according to the service that responds; in microservices, non-uniform error messages reveal which service handles each request; watch for errors returned as success with an error body or hidden in 302 (p.338).
- **Remediation**: Proactive Controls C10 and the Error Handling Cheat Sheet (p.338). Cross-references: Appendix C (fuzz vectors), ASVS 4.1 v7.4 (p.338).
- WSTG-ERRH-02 (stack traces) was **merged** into this test (p.339).

## WSTG-CRYP-01 Weak TLS (p.341-343)
- **Objectives**: validate the service configuration; review the cryptographic strength and validity of the certificate; ensure that TLS security cannot be bypassed and is well implemented in the application (p.341).
- **Server configuration**: legacy protocols and ciphers cited by the guide with the associated attacks (SSLv2, SSLv3, TLSv1.0, EXPORT, NULL, anonymous ciphers, RC4, CBC mode, TLS compression, weak DHE keys); the guide refers to the Mozilla Server Side TLS Guide for what is recommended today (p.341) [DATED: 2020 list; new weaknesses appear].
- **Exploitability**: the guide notes that many of these attacks were demonstrated in the lab but require an active MitM and significant resources, being unlikely outside state actors (p.341). `[inference]` this affects severity classification, but does not excuse reporting the configuration.
- **Certificates** (p.342): key strength of at least 2048 bits; signature of at least SHA-256 (no MD5/SHA-1); validity: within the period, **certificates issued after 1 September 2020 with at most 398 days**, signed by a trusted CA (public or internal; do not mark an internal app as untrusted just because your system does not trust the CA), SAN matching the hostname (CN ignored by modern browsers), care when accessing by IP; wildcard certificates have their own concerns; certificates can leak internal names in the Issuer and SAN fields [DATED: validity period and CA practices have evolved].
- **Implementation vulnerabilities** cited: predictable OpenSSL PRNG on Debian, insecure renegotiation, Heartbleed, POODLE on F5, DoS in Schannel (p.342).
- **Use in the application**: do not send sensitive data over an unencrypted channel (WSTG-CRYP-03), HSTS (WSTG-CONF-07), `Secure` flag on cookies (WSTG-SESS-02) (p.342); **mixed active content** (scripts/CSS over HTTP on an HTTPS page) and mixed passive content (p.342-343); redirecting from HTTP to HTTPS depends on HSTS and the **preload list** against interception of the first request (p.343).
- **Automated testing**: Nmap (scripts), O-Saft, sslscan, sslyze, SSL Labs, testssl.sh (p.343). **Manual**: `openssl s_client`, `gnutls-cli`; beware of modern versions without support for old protocols (false negative risk); DevTools show protocol and cipher (p.343).

## WSTG-CRYP-02 Padding oracle (p.344-346)
- **Objectives** [from source]: identify encrypted messages that rely on padding and assess the error messages returned when the padding is broken (p.344).
- Concept: application function that decrypts data sent by the client (e.g., session state on the client) and leaks whether the padding is valid; with this the attacker can decrypt and encrypt data without the key, with loss of confidentiality and possible privilege escalation if integrity is presumed (p.344). The leak can come from exposed exceptions, subtle response differences or timing (p.344).
- Candidates: apparently random values whose decoded size is a multiple of the block (8 or 16 bytes) (p.344-345). The guide describes checking the behavior under bit-by-bit tampering and distinguishing **three states** (decrypts and correct data; decrypts and corrupted data with a logic error; padding failure); oracle signs: padding exceptions (e.g., in the ASP.NET and Java examples) or response/time differences (p.345). The exact operational steps are in the guide (p.345); not replicated.
- **Secure implementation** [from source]: verify integrity (HMAC or authenticated modes such as GCM/CCM) and handle all decryption errors uniformly, with only two responses, ok and failure (p.345). Tools cited: Bletchley, PadBuster, POET, Poracle, python-paddingoracle (p.345-346).

## WSTG-CRYP-03 Sensitive information over unencrypted channels (p.347-349)
- **Objectives**: identify sensitive information transmitted over the various channels and assess the privacy and security of the channels (p.347).
- Rule of thumb from the guide: if the data must be protected at rest, it must be protected in transit. Examples: credentials, PINs, session identifiers, tokens, cookies, data protected by law or policy (cards, customer data), list of PII (p.347).
- Test examples: Basic authentication over HTTP (credentials only encoded, not encrypted), login form with `action` on HTTP, session cookie without `Secure` with login on HTTP (p.348-349). Also look for secrets and PII in the source code and logs with pattern searches (p.349). Tools: curl, grep, Identity Finder, Wireshark, TCPDUMP (p.349).

## WSTG-CRYP-04 Weak encryption (p.350-352)
- **Objective**: guide the identification of weak uses and implementations of cryptography or hashing (p.350). Algorithms considered weak by the guide: MD5, RC4, DES, Blowfish, SHA1, 1024-bit RSA/DSA, 160-bit ECDSA, 2TDEA (p.350).
- Basic checklist (values from the guide, 2020 [DATED]): random and unpredictable IV; secure random number generator (the guide contrasts `java.util.Random` with `java.security.SecureRandom`); asymmetric with ECC (Curve25519 preferred) or RSA of at least 2048 bits, PSS in signatures; minimum key requirements (DH 2048, HMAC-SHA2, hash SHA2 256, AES 128, ECDH/ECDSA 256, password hash with PBKDF2/Scrypt/Bcrypt); avoid CBC mode in SSH and **ECB** in symmetric ciphers; PBKDF2 with more than 10,000 iterations and without MD5 (p.350).
- Code review: look for keywords of weak algorithms (MD4, MD5, RC4, RC2, DES, Blowfish, SHA-1, ECB), Java cryptography APIs and parameters (distinct IV per encryption, PBKDF2 with random salt), recommended padding in RSA (OAEP), and **hard-coded secrets** in the code (p.350-352).
- Tools: Nessus, Nmap (scripts), OpenVAS; static analysis (Klocwork, Fortify, Coverity, CheckMark (spelling as in the guide)) for listed CWEs (CWE-261, 323, 326, 327, 328, 329, 330, 347, 354, 547, 780) (p.352).
- Boundary: more current cryptography requirements and verification in code: forward to `owasp-asvs-code-review-expert`.

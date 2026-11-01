# [DATED] WSTG 4.2 (2020) items that need current verification

Pages = PDF (WSTG p.N; printed = N − 2). The frontispiece dates the edition to 2020 (p.10). Everything below must be marked [DATED] in answers and checked against current sources (the agent has no network access by default).

- **Obsolete technologies**: Flash, Silverlight, applets and ActionScript (CONF-08 p.117-118; CLNT-08 p.396-401); Web SQL (INPV-05.8 p.281-282, CLNT-12 p.418).
- **XST**: the guide says it now only works with technologies such as Flash (CONF-06 p.113).
- **Numeric cryptography/TLS values**: 2048 bits, SHA-256, 398 days of validity for certificates issued after 1 Sep 2020, lists of legacy protocols/ciphers, 10,000 PBKDF2 iterations, minimum key sizes (CRYP-01 p.341-342; CRYP-04 p.350).
- **Session values**: 15 min timeout for a bank, 60 min for a forum (SESS-06 p.209; SESS-07 p.211), session ID of at least 50 characters and 256-bit key (SESS-01 p.190).
- **Technology tables**: CMS/framework cookies and keywords (INFO-08 p.83-84); HPP behavior per server (INPV-04 p.233); default administration URLs (CONF-05 p.109-110); Oracle product headers (INPV-05.1 p.250); browser cache paths (ATHN-06 p.159).
- **Tool lists**: INFO-01 (search engines, p.50-51), Appendix A (p.444-447), tools cited in each test.
- **References to period documents**: OWASP Top 10 2013/2017, ASVS 4.0.x/4.1, PCI DSS 3.2.1, NIST 800-30/800-115 (p.20, 43-44, 98, 179, 338).
- **Clickjacking**: the guide covers frame busting and X-Frame-Options; it does not cover CSP `frame-ancestors` (CLNT-09 p.402-411).
- **Gaps in guide 4.2** (NOT COVERED; see `python -I scripts/wstg_lookup.py --gaps`): JWT, SAML/OIDC, WebAuthn, SBOM/SLSA, mass assignment, prototype pollution, CSP, Kubernetes/serverless, HTTP/2-3, EPSS, among others.

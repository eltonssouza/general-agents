# Glossary (WSTG 4.2 terms, in our own words)

Pages = PDF (WSTG p.N; printed = N − 2). The author's terms are kept in English.

| Term | Meaning in the guide | Page |
|---|---|---|
| WSTG | Web Security Testing Guide, a testing framework and set of security testing techniques for web applications | 13 |
| Scenario ID (`WSTG-<category>-<number>`) | 4-letter category identifier + number 01-99; versioned as `WSTG-v42-INFO-02` | 16 |
| Vulnerability | Flaw or weakness in design, implementation, operation or management that can be exploited against security objectives | 47 |
| Threat | Anything that can harm assets by exploiting a vulnerability | 47 |
| Test | Action that demonstrates that the application meets the stakeholders' security requirements | 47 |
| Passive testing / active testing | Exploration and mapping with a proxy, without attacking, and then application of the techniques of the 12 categories | 48 |
| Black / gray / white box | No knowledge, partial knowledge, with source code; the ch. 4 method is black box | 31, 47 |
| Patch-and-penetrate | Fixing the reported bug without investigating the root cause; criticized by the guide | 16 |
| Window of vulnerability | Interval between the discovery of a flaw and the installed fix | 16-17 |
| SDLC | Development lifecycle; the guide wants security in every phase | 14, 17 |
| Misuse / abuse case | Malicious or unintended use scenario, used to derive security requirements | 29 |
| Positive vs negative requirement | What the control must do vs what must not be possible | 28 |
| STRIDE | Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege | 27 |
| Fingerprinting | Identify server/framework type and version through responses, headers, cookies and files | 54, 78 |
| Banner grabbing | Read the server's response to a request to see headers such as `Server` | 54 |
| Forced browsing / dirbusting | Request known folder and file names to enumerate content | 80, 99 |
| Dorking (Google hacking) | Chain search operators to find files and sensitive information | 52 |
| robots.txt | Convention file for crawlers; not an access control mechanism | 58-59 |
| Source map | File that links minified code to the original; if published, it exposes the source code | 68, 70 |
| Subdomain takeover | DNS record pointing to an inactive resource that an adversary claims | 120 |
| HSTS | Header that instructs the browser to use only HTTPS (max-age, includeSubDomains, preload) | 115 |
| XST | Cross-Site Tracing: use of the TRACE method to bypass HttpOnly (now only with technologies such as Flash) | 113 |
| Method overriding | Headers such as X-HTTP-Method-Override that "tunnel" restricted methods | 113 |
| RBAC | Role-based access control | 128 |
| Maker-checker | Principle in which whoever initiates a sensitive operation differs from whoever approves it | 129 |
| Account enumeration | Discovering valid usernames through differences in response | 134 |
| Lockout | Account lockout after failed attempts; balance between protection and denial to legitimate users | 148 |
| Horizontal / vertical bypass | Accessing resources of another identity of the same role / of a higher role | 175-176, 180 |
| IDOR | Insecure direct object reference: a user parameter points to an object without sufficient checking | 183 |
| Session fixation | Same session cookie value before and after login | 196 |
| Session hijacking | Use of stolen session cookies to impersonate the user | 215 |
| Session puzzling (variable overloading) | Use of the same session variable for more than one purpose | 213 |
| Full / partial HSTS | HSTS on the host and all subdomains vs only on the host | 196, 215 |
| Cookie prefix | `__Host-` and `__Secure-`, which build guarantees into the cookie name | 194 |
| CSRF (session riding) | Making the authenticated user's browser perform unintended actions | 202 |
| Reflected / stored / DOM-based XSS | Injection into one response / persisted and executed later / consequence of JavaScript on the client (source → sink) | 219, 225, 380 |
| HPP | HTTP Parameter Pollution: repeated parameters handled differently by components | 232 |
| In-band / out-of-band / blind (inferential) | SQL injection classes regarding the data channel | 236 |
| Impedance mismatch | Difference in interpretation between filter and application | 232, 234 |
| SSTI | Server-side Template Injection | 329 |
| SSRF | Server-Side Request Forgery: inducing the server to load resources | 333 |
| Incubated vulnerability | Stored injection that requires a "recall" step to execute | 318 |
| Padding oracle | Function that leaks the validity of the padding after decrypting client data | 344 |
| Business logic flaw | Flaw in business rules and workflows; application-specific and not detectable by a scanner | 354 |
| Easter egg (hidden functionality) | Hidden development feature that can be triggered | 359 |
| Web shell | Uploaded file that runs commands on the server; must be removed at the end of the test | 375-376 |
| Clickjacking | Tricking the user into clicking on something different from what they believe | 402 |
| Origin (WebSocket, postMessage) | Combination of scheme, host and port that must be validated | 412, 415 |
| XSSI | Cross-Site Script Inclusion: data leakage via cross-origin script inclusion | 422 |
| Introspection (GraphQL) | Query to the GraphQL schema about supported types and queries | 428 |
| CVSS | Severity metric maintained by FIRST, cited by the guide | 35, 442 |

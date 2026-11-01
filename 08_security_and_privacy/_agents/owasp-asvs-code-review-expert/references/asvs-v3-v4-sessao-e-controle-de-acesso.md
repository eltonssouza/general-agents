# ASVS V3 Session management (p.32-35) and V4 Access control (p.36-37)

Source: ASVS 4.0.3. Marks `L1/L2/L3` = level at which the requirement is required.

## V3 — Session management
### Goal and premises (ASVS p.32, 35)
- [from source] A session turns a stateless protocol into a stateful one; the high-level requirements: sessions unique per individual/device, neither guessable nor shareable, and invalidated when no longer needed and after inactivity (ASVS p.32). The chapter was adapted as a compatible subset of NIST 800-63b (ASVS p.32). TLS is mandatory for sessions and is covered in the communication chapter (ASVS p.32).
- [from source] Concurrent sessions should **no longer** be blocked: users have several devices, APIs have no browser session, and "the last authenticator wins", which is often the attacker (ASVS p.35).

### Requirements
| Section | Requirements (paraphrase) | Levels | Page |
|---|---|---|---|
| V3.1 | V3.1.1 never expose the session token in URL parameters | L1/L2/L3 | ASVS p.32 |
| V3.2 | V3.2.1 generate a **new token on authentication**; V3.2.2 tokens with ≥ **64 bits of entropy**; V3.2.3 store the token in the browser only securely (protected cookie or sessionStorage); V3.2.4 tokens generated with approved cryptographic algorithms | V3.2.1-3: L1/L2/L3; V3.2.4: L2/L3 | ASVS p.32 |
| V3.3 | V3.3.1 logout/expiration invalidate the token (browser back or RP does not resume the session); V3.3.2 periodic reauthentication when "staying logged in"; V3.3.3 option to terminate the other sessions after a password change; V3.3.4 user sees and terminates sessions/devices (after re-entering credentials) | V3.3.1-2: L1/L2/L3; V3.3.3-4: L2/L3 | ASVS p.33 |
| V3.4 | session cookies with `Secure` (V3.4.1), `HttpOnly` (V3.4.2), `SameSite` (V3.4.3), `__Host-` prefix (V3.4.4) and, if the domain is shared, the most specific `Path` possible (V3.4.5) | L1/L2/L3 | ASVS p.33 |
| V3.5 | V3.5.1 user revokes OAuth tokens of linked apps; V3.5.2 use session tokens instead of static API secrets (except legacy); V3.5.3 stateless tokens with signature/encryption and countermeasures against tampering, replay, null cipher and key substitution | L2/L3 | ASVS p.34 |
| V3.6 | RPs inform the CSP of the maximum authentication time and the CSP reauthenticates; CSPs inform the last authentication event | L3 only | ASVS p.34 |
| V3.7 | V3.7.1 full/valid session or reauthentication/secondary verification before **sensitive transactions or account changes** | L1/L2/L3 | ASVS p.35 |
- [from source] Timeouts (V3.3.2): at level L1 the table text says 30 days; at L2 12 hours or 30 minutes of inactivity (2FA optional); at L3 12 hours or 15 minutes of inactivity with 2FA (ASVS p.33). The NIST values must be the **upper limit** of idleness (ASVS p.33).
- [from source] Token-based mechanisms (JWT, OAuth, SAML and API keys): API keys are weak and must not be used in new code (ASVS p.34).
- [from source] **"Half-open" attack** (early 2018, financial institutions): exploits the pattern of reusing the profile/session object across unauthenticated, semi-authenticated (password reset, "forgot username") and fully authenticated states; if controllers/routers do not check for a full login, the attacker acts as the user (change password/email, turn off MFA, change API keys) (ASVS p.35). Mitigation = V3.7.1 (ASVS p.35), V1.4.x (ASVS p.18) and V1.11.2 (ASVS p.20).

### Contrast with the OCRG (2017)
- The OCRG (A2) describes session ID (≥ 128 bits in length with ≥ 64 of entropy), HttpOnly, rolling on elevation, fixation and logout (OCRG p.66-70); it is compatible with V3.2.x/V3.4.x, but does not mention `SameSite`, `__Host-`, JWT or OAuth (terms absent from the text). See `references/ocrg-a2-autenticacao-e-sessao.md`.

## V4 — Access control
### Goal (ASVS p.36)
- [from source] Authorization = allowing access to resources only to those with permission. High-level requirements: whoever accesses has valid credentials; users are associated with well-defined roles/privileges; role/permission metadata is protected against replay or tampering (ASVS p.36).

### Requirements (all L1/L2/L3, except V4.3.3 L2/L3)
| ID | Idea (paraphrase) | Page |
|---|---|---|
| V4.1.1 | **enforce access rules in a trusted service layer**, even if there is client-side control | ASVS p.36 |
| V4.1.2 | user/data attributes and policy information used in control cannot be manipulated by end users, unless explicitly authorized | ASVS p.36 |
| V4.1.3 | **least privilege**: only functions, files, URLs, controllers, services etc. with specific authorization (protects against spoofing and privilege escalation) | ASVS p.36 |
| V4.1.5 | access controls **fail securely**, including on exception | ASVS p.36 |
| V4.2.1 | sensitive data and APIs protected against **IDOR** on create/read/update/delete (e.g. editing someone else's record, listing all, deleting all) | ASVS p.36 |
| V4.2.2 | **strong anti-CSRF** mechanism on authenticated functionality and effective anti-automation/anti-CSRF on unauthenticated functionality | ASVS p.36 |
| V4.3.1 | administrative interfaces with appropriate MFA | ASVS p.37 |
| V4.3.2 | directory listing disabled; no disclosure of metadata (Thumbs.db, .DS_Store, .git, .svn) | ASVS p.37 |
| V4.3.3 (L2/L3) | additional authorization (step-up/adaptive) and/or segregation of duties for anti-fraud control according to risk | ASVS p.37 |
- V4.1.4 was removed (duplicate of V4.1.3) (ASVS p.36). ASVS V1.4 covers the architecture (trusted enforcement point, single mechanism, ABAC) (ASVS p.18).

### Code review (`[inference]`)
- Look for: authorization in the controller/route (not just the view), checking the **object owner** on every access by ID (V4.2.1), fields the client can send that the server must not accept (mass assignment; see V5.1.2), anti-CSRF on state-changing routes, default deny. The OCRG details A4 (IDOR), A7 (function-level authorization) and A8 (CSRF): `references/ocrg-a4-a7-a8-a10-acesso-csrf-redirecionamento.md`.
- Chapter references (ASVS p.37): OWASP Testing Guide for authorization, access control, CSRF and REST cheat sheets.

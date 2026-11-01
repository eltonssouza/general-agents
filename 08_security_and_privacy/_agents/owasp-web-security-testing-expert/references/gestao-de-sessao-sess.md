# 4.6 Session management (WSTG-SESS-01 to SESS-09)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased. The CSRF pages contain example attack code that is **not** reproduced here. Session tests with two accounts (victim/attacker) must use only test accounts provided or created with authorization.

## WSTG-SESS-01 Session management schema (p.186-191)
- **Objectives** [from source]: collect session tokens (from the same user and from different users); analyze randomness to prevent forgery; modify unsigned cookies that carry manipulable information (p.186).
- Attack pattern described: cookie collection → reverse engineering of the algorithm → manipulation (possibly brute force); there is also a cookie overflow pattern, of a different nature (p.186).
- **Minimum interaction criteria** (p.187): all `Set-Cookie` with `Secure`? cookie operations over unencrypted transport? reasonable persistent cookies and `Expires`? HTTP/1.1 and 1.0 `Cache-Control` directives that protect cookies?
- **Cookie collection**: how many cookies, which parts generate/alter/require them; spreadsheet of cookie × part of the application (p.187).
- **Session analysis**: randomness, uniqueness, resistance to statistical and cryptographic analysis, information leakage; token structure (common mistake: embedding data in the token instead of a generic value with data on the server); detect obfuscation (hex, Base64, hash) and static parts; hybrid tokens (p.187-188). **Predictability**: control the time variable (collect samples in the same interval; quantization of 50 ms or less can be too coarse), look for increments, time seeds, time hashes (p.188).
- **Cookie reverse engineering**: a secure cookie combines unpredictability, **tamper resistance**, expiration and the `Secure` flag (p.189). Collect enough samples (from a few to thousands, if mathematical analysis such as chi-square is needed), record the time, note that the cookie before and after authentication may differ, vary one factor at a time, check charset and subparts (p.189-190).
- **Brute force**: relate the ID variation to the session duration/timeout; a long ID with high variance and short validity makes it harder (p.190).
- Gray-box (values from the guide): non-predictable token (do not use linear algorithms based on IP), use of encryption with a 256-bit key is encouraged, length of at least 50 characters, defined timeout, non-persistent cookie, `Secure`, `HttpOnly` (p.190) [DATED: numeric guidance of the 2020 guide; for current requirements consult ASVS, via `owasp-asvs-code-review-expert`].
- Tools: ZAP (token analysis), Burp Sequencer, JHijack (p.190).

## WSTG-SESS-02 Cookie attributes (p.192-195)
- **Objective**: ensure the correct security configuration of cookies (p.192). Review with an intercepting proxy or the browser's "cookie jar" (p.192).
- **Attributes** (p.192-194): `Secure` (sends only over a secure channel), `HttpOnly` (blocks access by script; limits but does not eliminate the reach of XSS), `Domain` (scope; if too loose a vulnerable subdomain can harvest cookies; if absent the host that issued it applies), `Path` (scope by path, useful but too loose exposes to other applications on the same server), `Expires` (persistence, lifetime limit, forced removal), `SameSite` (Strict, Lax, None; `None` only with `Secure`).
- **Prefixes** `__Host-` (Secure, from a secure URI, no `Domain`, `Path=/`) and `__Secure-` (Secure, from a secure URI) (p.194).
- **Most secure configuration cited by the guide**: `__Host-` + `Path=/` + `Secure` + `HttpOnly` + `SameSite=Strict` (p.194). Tools: proxies and browser extensions (p.194-195).

## WSTG-SESS-03 Session fixation (p.196-198)
- Condition: the same session cookie value before and after authentication (p.196). Fix: renew the cookie after login; alternatively ensure cookie integrity (full HSTS, `__Host-`/`__Secure-` prefixes) against network attackers (p.196). "Full HSTS" = the host and all its subdomains (p.196).
- **Objectives**: analyze the authentication mechanism and flow; force cookies and assess the impact (p.196).
- Test (p.196-198): check whether a new cookie is issued at login; test with forced cookies using **two accounts** (victim and attacker, preferably on distinct machines or browsers to reduce false positives), with an 11-step sequence that compares the state of the cookie jar before/after login; there is a short variant with one account (p.197-198).
- **Remediation**: renew the token after successful authentication and first invalidate the previous ID (p.198). Tool: ZAP (p.198).

## WSTG-SESS-04 Exposed session variables (p.199-201)
- **Objectives**: ensure adequate encryption, review the cache configuration and assess the security of the channel and methods (p.199).
- Points: encryption/hashing of the ID is considered separate from transport encryption; check simple swaps (changing https to http) and segregation between secure and non-secure areas (a different ID when the client moves to non-secure elements) (p.199). After each successful login, a new token and encrypted delivery (p.199-200).
- Proxies/cache: the ID must never travel unencrypted nor be cached; `Cache-Control: no-cache` vs `private` (`private` allows caching in a non-shared proxy); HTTP/1.0 caches ignore `no-cache`; also use `Expires: 0` and `max-age=0` (p.200).
- GET vs POST: avoid the ID in GET (proxy/firewall logs); check whether POST endpoints accept the same data via GET (p.200).
- Final transport checklist on p.200-201.

## WSTG-SESS-05 CSRF (p.202-207)
- **Objective**: determine whether it is possible to initiate requests on behalf of the user without the user initiating them (p.205).
- Concept [from source]: CSRF depends on the browser automatically sending session information, on the attacker knowing valid URLs/requests, on session management relying only on information known to the browser (cookies, basic HTTP authentication), and on HTML tags that trigger requests (p.202). It can reach intranet resources and "self-vulnerable" applications such as webmail (p.205).
- **How to test**: audit whether session management relies only on client-side values; resources via GET are easily vulnerable, and **using only POST does not solve it** (p.205-206). The guide has examples of a proof-of-concept page for POST and for JSON APIs with `text/plain` (p.206); not replicated here.
- **Remediation**: follow the OWASP CSRF Prevention Cheat Sheet (p.206) `[inference]`: guide 4.2 does not detail the controls; consult the source. Tools: ZAP, CSRF Tester, Pinata-csrf-tool (p.206).

## WSTG-SESS-06 Logout (p.208-210)
- **Objectives**: assess the logout interface and analyze timeout and session destruction (p.208).
- Requirements of secure termination: logout control in the interface, inactivity timeout, **invalidation of the state on the server** (p.208). Common mistakes: only changing the cookie value on the client with the server state active (reusable), only showing a message, encrypted "stateless" cookie without tracking (the guide cites ASP.NET Forms Authentication), SSO with coexisting sessions (p.208).
- Tests: logout UI (button on every page, visible without scrolling), termination on the server (restore the old cookie value and reload), timeout via increasing delays, and **single sign-off** in SSO environments (p.209). The timeout value depends on the purpose of the application and is a balance between security and usability; as examples, the guide says that in a banking application it makes no sense to keep an idle session for more than 15 minutes and that in a wiki/forum an hour or more may be acceptable (p.209) [DATED: 2020 values].

## WSTG-SESS-07 Session timeout (p.211-212)
- **Objective**: validate that a hard session timeout exists (p.211).
- Timeout must be enforced **on the server**; if the cookie carries time data (login, last access, expiration) the client may be involved: try to alter the cookie if it is not cryptographically protected (p.212). Idle timeout does not limit the actions of whoever has already hijacked the session and generates activity (p.211). In gray-box: logout destroys the tokens or leaves them unusable; the server prevents replay; invalidating the session on the server (methods such as `HttpSession.invalidate()` or `Session.abandon()`) is essential; clearing the cookie in the browser is recommended but not strictly necessary (p.212).

## WSTG-SESS-08 Session puzzling (variable overloading) (p.213-214)
- **Objectives**: identify all session variables and break the logical flow of session generation (p.213).
- It occurs when the same session variable is used for more than one purpose, and the attacker accesses pages in an unforeseen order (e.g., a public password recovery page populates the variable that private pages later trust) (p.213). Black-box is hard and depends on luck; source code review is the most effective way (p.213-214). **Remediation**: use each session variable for a single consistent purpose (p.214).

## WSTG-SESS-09 Session hijacking (p.215-216)
- **Objectives**: identify vulnerable session cookies; hijack them and assess the risk (p.215).
- Network attacker: cookies without `Secure` leak over HTTP, even on 100% HTTPS sites (p.215). Full HSTS at the domain root is needed when cookies use `Domain` (p.215). The guide explains two leakage scenarios (p.215).
- Test (p.215-216): applicable to sites without full HSTS; with two accounts, delete from the cookie jar the protected cookies according to the HSTS adoption case (none, partial), keep the snapshot and check whether the remaining cookies are enough to act on behalf of the victim; there is a short variant (p.216). Tools: ZAP, JHijack (p.216).

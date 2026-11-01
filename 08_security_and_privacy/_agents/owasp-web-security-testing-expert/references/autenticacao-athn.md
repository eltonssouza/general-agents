# 4.4 Authentication testing (WSTG-ATHN-01 to ATHN-10)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased, without repeating offensive payloads. Tests that involve repeated attempts (default credentials, lockout, brute force) require explicit authorization for that kind of action, a disposable account and attention to the lockout of real accounts (WSTG p.145-146, 148).

## WSTG-ATHN-01 Credentials over an encrypted channel (p.140-144)
- **Objective** [from source]: assess whether any use case makes the client or the server exchange credentials without encryption (p.140).
- Interactions to cover: credential submission at login, session token in the login response, session token in authenticated requests, password recovery token (p.140). Channel encryption is not enough: the algorithm and keys also count (refers to WSTG-CRYP-01) (p.140).
- Procedure: capture traffic (browser DevTools or a proxy such as ZAP), **disable features/extensions that force HTTPS** and look for passwords, tokens (in cookies) and reset codes; for each message check whether the exchange went over HTTPS (p.140-141). Try login, account creation, password change/reset and resources accessible while logged in, forcing the HTTP version (p.141-143).
- Criteria of the guide: the test **fails** if any credential or session token travels over HTTP, even if only through forced browsing (p.141-143); the session cookie must have the `Secure` attribute (p.141-142).
- **Remediation**: HTTPS on the whole site, HSTS and HTTP redirection; if that is hard, prioritize sensitive operations; free certificates such as Let's Encrypt (p.143-144).

## WSTG-ATHN-02 Default credentials (p.145-147)
- **Objectives**: enumerate applications with default credentials and validate whether they still exist; review new accounts for patterns or identifiable patterns (p.145).
- Root causes: inexperienced staff, forgotten programmer backdoors, default accounts that cannot be removed, no forced change on first login (p.145).
- Black-box: consult vendor documentation or public lists for the identified interfaces (p.145); watch out for the **lockout policy** (it may lock the administrative account) (p.145). The guide lists common usernames and passwords to try, names based on the application or organization name and the e-mail naming convention of the client (p.146); also review source code and comments (p.146). For new accounts: predictability of generated passwords (create several accounts and compare), sequential names (p.146-147).
- Gray-box: talk to IT, examine the user base (empty fields, patterns), code with embedded credentials, configuration files and the password generation policy (p.147). Tools: Burp Intruder, THC Hydra, Nikto 2 (p.147).

## WSTG-ATHN-03 Account lockout mechanism (p.148-150)
- **Objectives**: assess the ability of the lockout to mitigate brute force and the resistance of the **unlock** mechanism to unauthorized unlocking (p.148).
- Lockout protects against guessing of the login and of 2FA codes or security questions; it requires balancing protection against denying legitimate access; in the introduction, the guide says accounts are typically locked after 3 to 5 failed attempts (p.148). **Note**: the guide gives two "typical" ranges (3-5 on p.148; 5-10 in the remediation, p.150) and **neither is a requirement**; the appropriate threshold depends on the risk and purpose of the application (p.150).
- Procedure: use a disposable account (leave this test for the end of the plan if there is only one account), try wrong passwords in increasing numbers and then the correct one to see whether it locked and when it unlocks (p.148-149). The numbers in the example (3, 4 and 5 attempts; waits of 5, 10 and 15 minutes) are **illustrative of the methodology**, not required values (p.148-149). The guide's example ends with automatic unlocking after 10 to 15 minutes (p.148-149).
- **CAPTCHA** does not replace lockout; listed flaws: easy challenge, checking the HTTP code instead of success, server logic that assumes success, result never validated on the server, field processed improperly; bypass tests (submission without solving, intentional failure, direct submission with a proxy, known values, clearing cookies, skipping steps, alternative channels such as a mobile app API) (p.149).
- Unlock: single-use unique link; do not confuse with password recovery (p.149).
- **Remediation**: options from the lowest to the highest degree of assurance — by time, e-mail self-service, manual by admin, manual with positive identification; the list of options is on p.149; the decision factors are on p.150: "typical" threshold of 5 to 10 attempts (depends on the purpose of the application) and lockout of 5 to 30 minutes as a "good compromise" (not a requirement); manual lockout is the safest, but can become a DoS and the administrator also needs recovery; client-only lockout (JavaScript) must be tested by disabling the client code (p.150).

## WSTG-ATHN-04 Bypassing the authentication schema (p.151-155)
- **Objective**: ensure that authentication is enforced on all services that require it (p.151). Flaws arise in design, development and deployment (p.151).
- Black-box methods: **direct page request** (forced browsing), **parameter modification** (e.g., a fixed "authenticated" parameter), **session ID prediction** (linear or partially variable values) and SQL injection in a form (p.151-154).
- Gray-box: the guide uses the phpBB 2.0.13 case (cookie deserialization and loose type comparison) as an example of a bypass seen in code (p.155). Tools: WebGoat, ZAP (p.155).

## WSTG-ATHN-05 Vulnerable "remember password" (p.157)
- **Objective**: validate that the generated session is managed securely and does not put the credentials at risk (p.157).
- Problems: credentials stored in encoded form in browser storage (they should be replaced by server-generated tokens), automatic injection by password managers exploitable through clickjacking and CSRF, tokens that never expire (p.157). **Remediation**: session best practices and server-side storage of credentials (p.157).

## WSTG-ATHN-06 Browser cache weaknesses (p.158-160)
- **Objectives**: see whether the application stores sensitive information on the client and whether access happens without authorization (p.158).
- History (Back button) and cache are different entities with the same weakness; test: enter sensitive information, log out and use Back (p.158). To avoid it: HTTPS and `Cache-Control: must-revalidate` (p.158).
- Cache: with a proxy, check for each sensitive page whether the server told the browser not to store it (`Cache-Control: no-cache, no-store`, `Expires` in the past, `Pragma: no-cache`; p.158-159). Physical cache locations per browser/OS (p.159) [DATED]. Mobile browsers may treat directives differently: test with device mode/mobile `User-Agent` (p.159).

## WSTG-ATHN-07 Weak password policy (p.161)
- **Objective**: determine the resistance to dictionary guessing by assessing length, complexity, reuse and aging (p.161).
- Questions of the guide: allowed/required characters; change frequency and how to circumvent the history (changing several times in a row); when to change (NIST and NCSC advise against forced periodic expiration, although PCI DSS may require it); reuse and history; minimum difference from the previous password; ban on using the name/account in the password; minimum and maximum lengths; does it accept common passwords? (p.161).
- **Remediation**: strong policy and/or two-factor authentication; the policy is the simplest and cheapest, but the ideal is to have both (p.161).

## WSTG-ATHN-08 Weak security questions (p.162-163)
- **Objectives**: determine the complexity and simplicity of the questions and assess possible answers and brute force (p.162).
- Pre-generated questions often have answers known to relatives, easy to guess, forceable with lists or public on social networks (p.162). Questions generated by the user can be trivial (p.162).
- Test: obtain the list of questions (by creating an account or via the "forgot password" flow); assess the number of questions, number of attempts and lockout (remembering that lockout can become a DoS) (p.162-163). "A scheme is only as strong as its weakest question" (idea of the guide, p.163).

## WSTG-ATHN-09 Weak password change or reset (p.164-165)
- **Objectives**: determine the resistance of the change process to subversion and of the reset to guessing or bypass (p.164).
- For both: can non-administrator users change/reset other users' passwords? can the process be manipulated? is there CSRF? (p.164).
- Reset: what information is required (e-mail only = depending 100% on it); how the password arrives (worst: shown on screen; best: by e-mail to the registered address); secure random generation; confirmation by a link with a random token to limit DoS (p.164-165). Change: does it ask for the old password? (without that, whoever hijacked a session changes the password) (p.165).
- **Remediation**: sensitive function, require reauthentication or confirmation screens (p.165).

## WSTG-ATHN-10 Weaker authentication in an alternative channel (p.166-168)
- **Objectives**: identify alternative channels and assess measures and possible bypasses (p.167). Channels: standard site, mobile site, accessible site, other countries/languages, parallel sites, dev/test/UAT environments, apps, call center, IVR (p.166). Even if the scope does not allow testing, the existence must be documented (p.166, 167).
- Method: understand the primary mechanism, find other channels (site content, proxy logs with terms such as "mobile", "sso", search engines), confirm shared accounts, build a **grid** of the authentication functions per channel and compare; the call center may have weaker identity verification; watch for overlap of session management (p.167). If authorized, repeat the other authentication tests (p.167).
- **Remediation**: consistent authentication policy across all channels (p.168).

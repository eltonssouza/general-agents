# Documented cases and anti-patterns (with source and page)

Labels: `[from source]` = is on the cited page; `[inference]` = reading/derivation by the package. Pages: ASVS = footer = PDF; OCRG = PDF (printed = N − 1). Nothing here carries an operational payload: the cases describe **the design error**.

## Cases described by the books
| Case | What it illustrates | Source |
|---|---|---|
| IDOR at Yahoo!: `fid`/`cid` parameters in a delete POST allowed deleting other people's comments and posts (over 1.5 million records) | missing object owner check; trusting a client parameter | [from source] OCRG p.79-80 |
| Samy worm (MySpace, 2005): XSS allowed reading the page, obtaining the token and defeating the anti-CSRF defenses | **any XSS defeats token/referer/origin based defenses**; only challenge-response resists | [from source] OCRG p.141, 146 |
| "Half-open" attack (2018, financial institutions): reuse of the profile/session object across unauthenticated, semi-authenticated and authenticated states | design pattern flaw in authentication/session/access control; check full login in controllers/routers | [from source] ASVS p.35 (see V3.7.1; and V1.11.2 on ASVS p.20) |
| "Parameterized" query that becomes "SELECT without WHERE" when no filter is supplied | leak through the query **assembly logic**, even without injection | [from source] OCRG p.46-47 |
| Authorization in the MVC view: the action (add user/change password) runs before the view is denied | check in the wrong place; ASP.NET POSTBACK without a check | [from source] OCRG p.135-136 |
| `TestAction` left behind in the action configuration | unexposed/untested functionality widens the surface | [from source] OCRG p.136-137 |
| Call center that resets MFA with known questions | all authentication paths must have the same strength | [from source] ASVS p.18 (V1.2.4) |
| Compromised/removed signing key (strong name) | strong name does not prevent removing the signature and re-signing | [from source] OCRG p.108 |
| 3% → 23% of "risky" logins in one day | user risk + global risk → collective reaction (OOB for all the risky ones) | [from source] OCRG p.177 |

## Anti-patterns (what to reject in review)
| # | Anti-pattern | Why | Source |
|---|---|---|---|
| 1 | SQL by concatenation with user data; stored procedure that builds dynamic SQL | parser does not separate code from data | [from source] OCRG p.45-46, 51; ASVS V5.3.4 (ASVS p.39) |
| 2 | Believing ORM/Hibernate is injection-proof; concatenating in HQL/native SQL | HQL and native SQL are injectable | [from source] OCRG p.51-53 |
| 3 | Trusting `addslashes`/`mysql_real_escape_string` with an unquoted value | escaping only works inside quotes | [from source] OCRG p.49 |
| 4 | Validating by blacklist/complex regex; "encode bad" | does not withstand the future; hard to test | [from source] OCRG p.55 |
| 5 | `eval` for JSON; JSON building HTML; `innerHTML`/`document.write`/`setInterval` (with a string) with untrusted data | execution/DOM XSS even with escaping | [from source] OCRG p.52, 76, 190-191 |
| 6 | Using .NET Request Validation as an XSS defense; turning off `validateRequest` | generic and insufficient | [from source] OCRG p.56, 73 |
| 7 | CSRF "solved" with a secret cookie, POST only, multi-step or URL rewriting | does not work | [from source] OCRG p.142-143 |
| 8 | CSRF token in a GET URL | leaks via history/log/Referer | [from source] OCRG p.144-145 |
| 9 | Origin check via `indexOf` or `postMessage` with a wildcard origin; `Access-Control-Allow-Origin: *` on sensitive content | bypassable/accepts any origin | [from source] OCRG p.155-156 |
| 10 | Authorization only in the view/client/JavaScript; decision based on a client header or hidden field; no default deny | bypassable | [from source] OCRG p.135-138; ASVS V4.1.1 (ASVS p.36) |
| 11 | Redirect/forward with a destination coming from the request; forgetting `return` after `sendRedirect` | phishing and access bypass | [from source] OCRG p.151-153 |
| 12 | Binding the request directly to a business object with sensitive fields (`isAdmin`, `price`) | mass assignment | [from source] OCRG p.80-82, 137 |
| 13 | Stack trace/`printStackTrace(out)`/URL in the response; generic `catch`; empty catch | leak and unsafe state | [from source] OCRG p.115, 164-167, 169 |
| 14 | Logging passwords (valid or not), session IDs, keys, connection strings | the log becomes sensitive data | [from source] OCRG p.61, 163; ASVS V7.1.1 (ASVS p.44) |
| 15 | DES/SHA-0; MD5/SHA-1 in new code; home-grown crypto/hash | insecure | [from source] OCRG p.124, 128, 130; ASVS V6.2.5 (ASVS p.42) |
| 16 | Missing, short or reused salt; salt treated as a secret | rainbow tables | [from source] OCRG p.129-130 |
| 17 | Credentials in `web.config`/`<credentials>`; secrets in code | exposure | [from source] OCRG p.95, 114, 199; ASVS V2.10.4 (ASVS p.30) |
| 18 | Password with composition/rotation rules; complexity check in the checklist | contradicts current evidence | [from source] ASVS V2.1.9, V2.1.10 (ASVS p.24) vs OCRG p.61, 197-198 |
| 19 | Unbounded C functions (`strcpy`...); `printf` with a variable as the format; checking only the upper bound of an index | overflow/format string/integer overflow | [from source] OCRG p.185-188 |
| 20 | Shared static state with request data; lock released outside `finally` | race condition | [from source] OCRG p.183 |
| 21 | Treating the review as "police"; rushing; always finding a defect | dysfunctional review | [from source] OCRG p.27, 193 |
| 22 | Relying only on SAST/DAST/pentest; "we cannot hack ourselves to security" | each method covers part | [from source] OCRG p.11, 13-14; ASVS p.11 |
| 23 | Black-box as the only assurance | attacker/defender asymmetry | [from source] ASVS p.11 |
| 24 | Reporting only failures ("by exception"); running a tool and listing its output | does not prove verification | [from source] ASVS p.14 |

## Traps **inside the books themselves** (do not copy as a model)
1. **OCRG p.68 (Sample 8.5)**: the timeout example uses `cookieless="true"` (ID in the URL), contradicting the text (OCRG p.69-70).
2. **OCRG p.185 (Sample 24.2)**: `smallBuffer[10] = 0` on an array of 10 writes out of bounds (the book says the last index is size − 1, OCRG p.184).
3. **OCRG p.126 (AES)**: `Cipher.getInstance("AES")` without explicit mode/padding; the mode is left to the provider `[inference]` — use a secure configuration (ASVS V6.2.3/V6.2.5, ASVS p.42).
4. **OCRG p.157 (Sample 17.1)**: uses `ws://` while the text says to use `wss://`.
5. **OCRG p.45**: the list of the "five best ways" includes HtmlEncode for SQLi `[inference]`: HTML encoding does not prevent SQL injection.
6. **OCRG p.197-200**: the checklist repeats lines and contains wording errors.
7. **ASVS** uses the empty mark at L1 by default for V2.4/V2.10/V1 because they are non-pentestable/architectural: it does **not** mean they are optional in code review (ASVS p.26, 30, 19).

# Cases of the guide and testing anti-patterns

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased. The cases are illustrations from the guide itself; there are no operational details here.

## Cases and what they illustrate
| Case (in the guide) | What it illustrates | Page |
|---|---|---|
| "Magic parameter" with an obfuscated backdoor | A black-box scanner does not guess a 30-character value; code review would find it | 24-25 |
| Cross-site login signature with user hash + date | Obvious homemade cryptographic scheme in a review and invisible to a scanner | 25 |
| Car comparison (frontal impact test only) | Testing only one facet of the application gives a false sense of security | 16 |
| Subdomain pointing to GitHub after a migration | A forgotten DNS record allows subdomain takeover | 120 |
| Expired domain referenced by a CNAME | Whoever registers the domain controls the subdomain | 120 |
| Public S3 bucket | Misconfigured storage access control | 124 |
| Twitter incident in 2020 (cited) | Administrators must not have total power; use maker-checker or MFA | 129 |
| phpBB 2.0.13 | Authentication bypass seen in code (deserialized cookie + type comparison) | 155 |
| `IsAdmin=No` cookie | A cookie without tamper resistance grants privilege | 189 |
| Management firewall alert (rules deleted via GET) | CSRF affects intranet applications; a GET resource is trivial to exploit | 204-205 |
| HPP flaw in ModSecurity | Filter and application interpret repeated parameters differently | 232 |
| HPP flaw in Blogger | Authorization check on the first parameter and operation on the second | 232-233 |
| Padding oracle examples (ASP.NET and Java) | Exposed padding exceptions are the oracle | 345 |
| "Distributed Denial of Dollar" | A business limit (1000 free transfers) becomes an abuse vector | 357 |
| 10% discount resubmitted several times | Reusable hidden business-logic field | 359 |
| Loyalty points credited before completion | Workflow without rollback | 369 |
| Login with different timing for valid/invalid user | Leak through timing | 364 |
| Chained misuse action with no application response | Lack of active defenses against abuse | 371 |

## Anti-patterns (from the guide) and what to do instead
| Anti-pattern | Correction suggested by the guide | Page |
|---|---|---|
| Testing only after deployment | Include security in every phase of the SDLC | 14 |
| Pentest as the only technique | Balanced approach: reviews, threat modeling, code, pentest, automation | 21-22 |
| Believing in a silver bullet (scanner/WAF) | Use tools for what they do well; security is a process | 16, 18 |
| Patch-and-penetrate | Investigate the root cause and build security into the SDLC | 16-17 |
| Using the guide as a checklist | Reprioritize by risk, since new vulnerabilities appear | 8 |
| Superficial review / false positives in the report | Review findings and eliminate false positives | 18 |
| Treating the absence of findings as proof of security | Unknown problems are not tested | 35 |
| Relying on `robots.txt` to restrict access | It does not enforce any restriction | 59 |
| "Security through obscurity" (hiding headers, renaming cookies) | It only delays a basic adversary; invest in maintenance and awareness | 84 |
| Validating only on the client (JavaScript, hidden fields) | Validate on the server; keep a copy of the business values | 358, 361, 373 |
| Session tokens with embedded or predictable data | Generic, random value with data on the server | 187-188 |
| Reusing the same session variable for several purposes | One consistent purpose per variable | 214 |
| POST only as a defense against CSRF | POST can also be automated by JavaScript | 205-206 |
| Editing files on the production server | Policy that forbids it; generate backups outside the web tree | 106 |
| Logging only on the web server, on the same partition | Logs in a separate location, own partition | 96 |
| Distinct error messages for invalid user/password | Generic and consistent messages | 137 |
| Security questions with publicly known answers | See the remediation and the risks in ATHN-08 | 162-163 |
| Only extension filter on upload | Check type and content; see File Upload Cheat Sheet | 374, 378 |
| Defenses localized only per function | Active defenses against misuse across the whole application | 372 |

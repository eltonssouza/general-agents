# 4.10 Business logic (WSTG-BUSL-01 to BUSL-09)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased; the web shell, decompression bomb and upload filter evasion examples of the guide are **not** reproduced (see guide p.376-377, only in authorized scope).

## Introduction to business logic (p.354-356)
- Logic flaws require "thinking outside the conventional": what happens if the user jumps from step 1 straight to 3 (fail open, deny, or 500 error)? [from source] (p.354).
- They are **not detectable by a scanner**; they depend on the skill and creativity of the tester, are usually hard to find, application-specific and very damaging; automating logic abuse cases "is not possible" and remains a manual art; the technique approaches finite-state functional testing, with abuse and misuse cases (p.354).
- Method: consider business rules and limits and check whether the application enforces them; third parties must ask the business, request a *walkthrough* from the client and, if possible, have a direct line to developers (p.354).
- Examples from the guide: changing the price after the summary page, holding resources to buy cheaper (countermeasure: timeouts and ensuring the correct price), canceling the transaction after loyalty points were credited (p.354-355).
- Tools: intercepting proxy (ZAP, Burp), browser plugins to edit headers/parameters/cookies; tools do not detect logic flaws (p.355). Warning from the guide: when installing extensions, consider the permissions they ask for (p.355).

## WSTG-BUSL-01 Business data validation (p.357-358)
- **Objectives**: identify data injection points; validate that all checks occur on the back end and cannot be bypassed; try to break the expected format and analyze the handling (p.358).
- Difference from boundary value analysis (BVA): here the validity is **logical** (e.g., not only the format of the number, but what it means), and it often requires consulting another system; client-only checks leave the application vulnerable to injection via a proxy or at the transfer points between systems (p.357).
- Method: review the documentation and exploratorily test the entry and "hand-off" points; use a proxy to see where variables such as cost and quantity pass; interrogate fields with logically invalid data (p.358).
- **Remediation**: accept only "logically valid" data at all entry and transfer points and do not trust the data after it enters (p.358).

## WSTG-BUSL-02 Forging requests (p.359-360)
- **Objectives**: review the documentation for guessable, predictable or hidden fields; insert logically valid data to bypass the normal flow (p.359-360).
- Focus: break the business **flow** (different from BUSL-01); examples: a hidden "discount already applied" field resubmitted several times; a hidden development field ("Easter egg") that gives shortcuts in a game (p.359).
- Method: in the proxy, look for values that increment at a regular interval or are guessable, and hidden options (debug) that can be activated (p.360).
- **Remediation**: business logic that prevents predicting and manipulating parameters and that does not leave undocumented functionality, such as debug, exposed (p.360).

## WSTG-BUSL-03 Integrity checks (p.361-363)
- **Objectives**: review components that move, store or handle data; determine what is logically acceptable and who can read/modify; try to insert, update or delete values that the logic forbids (p.362).
- Principle: hidden fields, non-editable fields and drop-down lists are only "non-editable" in the browser; the server must keep a copy and perform relational checks; **logs must also be protected** against reading, writing and removal (p.361).
- Three methods (hidden fields, non-editable fields, components such as logs/databases) (p.362). **Remediation**: strict access control over how data and artifacts are read and modified, through trusted channels, with adequate logging for review (p.362).

## WSTG-BUSL-04 Process timing (p.364-366)
- **Objectives**: review time-sensitive functionality; develop and run abuse cases (p.365).
- Double risk: the processing time **leaks information** (e.g., login with a valid vs invalid user takes a different time) and sessions left open can break flows (seat reservations, price quotes) (p.364-365).
- Method: identify time-dependent processes, automate the requests (tools measure better), draw the flow and prepare the requests, compare executions (p.366). **Remediation**: equalize the response time regardless of the result and prevent transactions extended beyond an acceptable limit (cancel/restart) (p.366).

## WSTG-BUSL-05 Limits on the number of times a function can be used (p.367-368)
- **Objectives**: identify functions that must have a usage limit; assess whether a logical limit exists and is validated correctly (p.367).
- Examples: a single discount per purchase, three downloads per month; test navigating back, reloading the cart (p.367). **Remediation**: strict controls, such as invalidating the coupon in the database or a per-user counter on the back end (p.367).

## WSTG-BUSL-06 Circumvention of workflows (p.369-370)
- **Objectives**: review the documentation for ways to skip or reorder steps; develop abuse cases for each flow (p.369).
- Examples: loyalty points credited before completion and kept after cancellation; content approved by a filter on the first post and edited later without a new check (p.369).
- **Remediation**: the application must verify the correct order of the steps and prevent skipping or repeating steps, with rollback of triggered actions if the transaction does not finish (p.370). References: OWASP Abuse Case Cheat Sheet, CWE-840 (p.370).

## WSTG-BUSL-07 Defenses against application misuse (p.371-372)
- **Objectives**: gather notes from all tests; see which tests had different behavior with aggressive input; understand the defenses and whether they are enough (p.371).
- Particularity: the result comes from the **observations of the other tests** — altered responses, blocked requests, logout or account lockout (p.371). Localized defenses (rejecting characters, locking the account) are not enough; the guide lists behaviors the application should detect (forced browsing, bypass of presentation-layer validation, multiple access errors, duplicated or missing parameters, invalid formats, crude payloads, faster-than-human use, change of geolocation or user agent, out-of-order steps, high rate of specific functions) (p.372).
- If no active response occurs, report that the application appears to have no broad active defenses against abuse; the responses may be silent (logs, alerts), so confidence in the finding is not total (p.372). **Remediation**: active defenses (AppSensor as a reference) (p.372).

## WSTG-BUSL-08 Upload of unexpected file types (p.373-374)
- **Objectives**: review the documentation for rejected types; verify that unwanted types are rejected and handled safely; verify that batch uploads do not bypass the measures (p.373).
- Method: study requirements, build a library of "unapproved" files, submit and verify prevention; check whether the check is only in client JavaScript, only by `Content-Type`, only by extension; whether files are accessible by direct URL, whether they can contain code, whether there is a path check on files extracted from archives (p.373-374).
- **Remediation**: accept and handle only "acceptable" files (lists of extensions, Content-Type, type recognizer) (p.374). See CWE-434 (p.374).

## WSTG-BUSL-09 Upload of malicious files (p.375-378)
- **Objectives**: identify the upload function; define acceptable and dangerous types; understand how files are processed; obtain or create malicious test files and verify whether they are accepted and processed (p.375).
- Points from the guide: restriction by extension is not enough against legitimate files with malicious content (p.375); web shells only work if the file is in the webroot and the server executes code, and **uploading a shell to an exposed server is dangerous**: protect it (random name, password, IP restriction) and **remove it when finished** (p.375-376); client-side filters are trivial to bypass, server-side filters have several bypasses (listed on p.376, not replicated); content: malware scanning (the EICAR test file is harmless and flagged by all antimalware), macros, directory traversal in archives, **decompression bombs** (the guide explicitly says **not** to run them without having considered the risks and having **written approval**, because of the risk of DoS and of cloud cost with autoscaling) (p.376-377); XML (XXE, billion laughs), CSV injection, Office macros, JavaScript in PDF (p.377).
- Code review: common upload APIs in Java, C/C++ and PHP (p.377-378). **Remediation**: complex and dependent on the accepted types; see the File Upload Cheat Sheet (p.378). Tools: Metasploit payload generation, proxy (p.378).

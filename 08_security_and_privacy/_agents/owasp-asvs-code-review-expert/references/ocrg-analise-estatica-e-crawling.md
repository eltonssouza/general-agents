# OCRG — static analysis, source-to-sink and code crawling (OCRG p.30-32, 43, 189-191, 206-218)

Source: OCRG v2.0, sections 6.8 and 6.11 and Appendix C. Pages = PDF (printed = N − 1). This is the base file of the script `scripts/ocrg_lint.py`.

## Static analysis (6.8) (OCRG p.30-32)
- [from source] It occurs in the implementation phase of the S-SDLC; the tools **highlight** possible vulnerabilities in static code; the ideal situation (finding everything with few false positives) is beyond the state of the art for many types of flaw, so the tools serve as **aids to the analyst**, not as complete detectors (OCRG p.30).
- [from source] Two options (OCRG p.30-31): (1) **scanner scripts** by pattern search (in-house and open source); (2) **static analyzers** (commercial and open source). Scripts/scanners find insecure patterns but usually **do not trace the data flow**; analyzers partially/fully compile the code and investigate execution branches, allowing **source-to-sink** (OCRG p.31).
- [from source] Table 5 — advantages: source-to-sink analysis gives the complete root cause; elaborate report (snippet, risk, description); reduces manual effort (repeated patterns are better left to a machine); finds **all instances** of a vulnerability with location (OCRG p.31). Table 6 — limitations: **business logic is not touched** (the biggest limitation), scope limited to certain frameworks/languages, **design flaws** are not seen, **false positives** require triage by an experienced programmer; "whoever expects to automate secure code checking at the end of the build will be disappointed" (OCRG p.31).
- [from source] Tool choice: language support; commercial vs free; type of analysis (security, quality, static, dynamic); test a few to evaluate experience, reports, false positives, customization and support; decide by the required features and integration into the S-SDLC, evaluating the user's expertise (OCRG p.31-32).
- [from source] **JavaScript** analysis requires a hybrid approach: static analysis with **taint analysis** (tracing variables "tainted" by user input to sinks), black-box tests (which do not detect DOM XSS) and manual source-to-sink validation when needed; test with JavaScript turned off to ensure validation on the server too; review the JS **before** it is obfuscated/minified (OCRG p.189-190).
- [from source] In the agile/CI flow shown in the appendix: ad hoc SAST started by the dev, rules tuned by AppSec, a false positive adjusts the rule base, sign-off (figure; OCRG p.195). A passing build does not mean absence of vulnerabilities (OCRG p.196).

## Source-to-sink (OCRG p.18, 31, 190)
- [from source] Source = all possible inputs; sink = insecure pattern (dynamic SQL, log writer, response to the client). A flow without adequate validation between the two = vulnerability (OCRG p.18). Examples of DOM sources: `document.url`, `document.location`, `document.referrer`, `window.location`; sinks: `document.write`, `window.location.href`, `innerHTML` and local storage (OCRG p.190-191).
- Procedure: see `references/procedimentos.md` (P4).

## Code crawling (6.11 and Appendix C) (OCRG p.43, 206-218)
- [from source] **Crawling** is sweeping the codebase looking for code "pointers" where vulnerabilities may reside: APIs that interface with the outside world, file I/O, user management; business logic methods have their own names and are not directly detectable (OCRG p.43). It can be manual or automated; simple tools (`grep`, `wingrep`, `findstr`) will do, and review tools with string highlighting can highlight the indicators (OCRG p.43, 206). Also look for language issues that affect stability/availability and guideline items (e.g. copyright notice); the reviewer may reject the code for violating the guideline even if it works (OCRG p.43).
- [from source] Appendix C gives lists of strings per language (only **pointers** to review, not proof of a flaw). Summary by topic (illustrative keywords):
| Language/topic | What the book says to look for (examples) | Page |
|---|---|---|
| .NET — request | `request.querystring`, `request.form`, `request.cookies`, `request.headers`, `request.files`, `request.servervariables`… | OCRG p.206 |
| .NET — output | `response.write`, `HtmlEncode`, `UrlEncode`, `innerText`, `innerHTML`, `<%=` | OCRG p.206 |
| .NET — SQL/database | `SqlCommand`, `ExecuteReader`, `exec sp_`, `OleDbConnection`, `ADODB.recordset`; check use of typed `SqlParameter`/`OleDbParameter` | OCRG p.207 |
| .NET — config | `web.config`: `httpRuntime`, `sessionState`, `debug`, `credentials`, `connectionStrings`, `authentication mode`, `forms protection`, `CustomErrors`, `trace`, `httpCookies` | OCRG p.208 |
| .NET — crypto/exceptions/serialization | `RNGCryptoServiceProvider`, `SHA`, `MD5`, `DES`, `RC2`, `System.Random`, `xor`, `base64`; `catch`, `finally`; `Serializable`, `GetObjectData`; `SecureString`, `ProtectedMemory` | OCRG p.210 |
| Java — streams | `FileInputStream`, `ObjectInputStream`, `BufferedReader`, `getResourceAsStream`… | OCRG p.211 |
| Java — servlets and output | `getParameter`, `getHeaders`, `getCookies`, `getQueryString`, `getRequestURL`; `javax.servlet.ServletOutputStream.print`; HTTP response splitting: `setHeader`, `sendRedirect` | OCRG p.212 |
| Java — SQL, SSL, session, OS | `prepareStatement`, `createStatement`, `executeQuery`; `SSLContext`, `TrustManagerFactory`, `HttpsURLConnection`; `getSession`, `invalidate`; `java.lang.Runtime.exec` | OCRG p.213-214 |
| Classic ASP | `Request.QueryString`, `Request.Form`, `Response.Write`, `On Error Resume Next`, `Server.GetLastError`, `ADODB.`, `session.abandon` | OCRG p.214-216 |
| JavaScript/AJAX | `eval`, `document.write`, `document.cookie`, `location.href`, `innerHtml`, `window.open`, `setTimeout`, `XMLHTTP` | OCRG p.216 |
| C/C++ and Apache | `strcpy`, `sprintf`, `printf`, `popen`, `system`; `ap_read_request`, `headers_in`, `ap_log_error`, `ap_unescape_url`, `ap_cookie_read` | OCRG p.217-218 |
- For .NET the book also lists input classes (`webcontrols.textbox` etc.) as indicators of **entry points** (OCRG p.208), `global.asax` (application variables with sensitive data; `Application_OnAuthenticateRequest`) (OCRG p.208), threads/concurrency (`Thread`, `Dispose`) (OCRG p.209) and class design (`Public`, `Sealed`) (OCRG p.209).

## Use with the script `ocrg_lint.py`
- The linter implements pattern rules for the book items marked `[from source]` with the page; heuristics the book describes in prose are `[inference]`; the 5 rules beyond the book are `[extrapolation]` and are **off by default** (`--include-extrapolation`).
- Limits declared by the book itself: tools always need human verification (OCRG p.11) and do not understand business logic or design (OCRG p.31). The linter does **not** run the code or do flow analysis.

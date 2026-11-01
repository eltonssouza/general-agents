# 4.11 Client-side testing and 4.12 API (WSTG-CLNT-01 to CLNT-13, WSTG-APIT-01)

Pages = PDF (WSTG p.N; printed = N − 2). **Sampled reading**: summary (including its conceptual points, such as the insecure CORS configurations), objectives, method at a conceptual level and remediation; the code examples and exploitation URLs of the "how to test" are **not reproduced**. All tests apply to the browser of the testing team itself or to authorized environments; never fire payloads at real users.

## WSTG-CLNT-01 DOM-based XSS (p.380-382)
- **Objectives** [from source]: identify DOM *sinks* and build appropriate inputs for each type of sink (p.380).
- Concept: active content in the browser (JavaScript) obtains input from a *source* and uses it in a *sink*, leading to execution of injected code; it does not require control of the content coming from the server (p.380). Since the JS application is generated dynamically, it is necessary to trace all instances of JavaScript and where there is user input (p.381).
- Limits of automation [from source]: the automatic tool has only very limited success in finding DOM XSS, unless it analyzes the client code; the guide requires manual testing at the points where parameters are read and written to the page or the DOM, and says that many general XSS filtering/detection techniques may be ineffective against this type, since the server may not see what is executed (p.380-382).
- **Remediation**: DOM-based XSS Prevention Cheat Sheet (p.382).

## WSTG-CLNT-02 JavaScript execution (p.383-384)
- **Objective**: identify sinks and possible JavaScript injection points (p.383). A subtype of XSS in which arbitrary code is executed in the victim's browser due to a lack of input and output validation; characters handled differently by browsers (p.383).

## WSTG-CLNT-03 HTML injection (p.385-386)
- **Objective**: identify HTML injection points and assess the severity of the injected content (p.385). The browser does not distinguish legitimate parts from malicious ones; methods such as `innerHTML` and `document.write()` receiving untrusted input are a risk (p.385).

## WSTG-CLNT-04 Client-side URL redirect (open redirect) (p.387-388)
- **Objectives**: identify injection points that handle URLs or paths and assess where the system can redirect (p.387). A validation flaw that accepts a user-controlled URL; it enables phishing (the redirect starts from the real application, looking trustworthy) and can help bypass access controls (p.387). Method: find redirects in the client code (e.g., assignment to `window.location`) (p.387).

## WSTG-CLNT-05 CSS injection (p.389-390)
- **Objectives**: identify CSS injection points and assess the impact (p.389). It can lead to XSS (under certain conditions/old versions) or to exfiltration of values through CSS selectors and functions that generate requests; allowing custom user CSS is a considerable risk (p.389). Method: analyze the code to see how the application returns CSS rules from inputs (p.389).

## WSTG-CLNT-06 Client-side resource manipulation (p.391-392)
- **Objectives**: identify sinks with weak validation and assess the impact of the manipulation (p.391). A flaw in which the input controls the path of a resource (iframe src, script, applet, XMLHttpRequest destination), usually used for XSS (p.391).

## WSTG-CLNT-07 CORS (p.393-395)
- **Objectives**: identify endpoints that implement CORS and ensure the configuration is secure or harmless (p.393).
- Concept: CORS uses headers for the browser to decide whether a cross-origin request is allowed; non-simple requests require an OPTIONS *preflight*; the `Origin` header is always sent by the browser (p.393).
- **Insecure configurations to look for** [from source, concept]: `Access-Control-Allow-Origin: *` (all domains allowed) and the server that **returns the received `Origin` value without any additional check**, which can lead to access to sensitive data (p.393). The guide says this is very insecure and unacceptable in general terms, **except in the case of a public API meant to be accessible by everyone** (p.393), that is, `*` is not always a finding.
- Relying on the `Origin` header for access control is not a good idea: it cannot be changed by JavaScript, but it can be forged outside the browser; sensitive data must still be protected with application-level protocols (p.393). Other headers involved: `Access-Control-Allow-Credentials`, `-Allow-Headers`, `-Allow-Method`, `-Max-Age`, `-Expose-Headers` (p.393-394).
- **Method**: intercept headers (e.g., ZAP) and pay attention to `Origin` and the allowed domains; manually inspect the JavaScript for injection through improper input handling (p.394). In XHR L2, watch for URLs passed to `XMLHttpRequest` without validation, especially absolute URLs, and unescaped responses controllable by the user (p.394). The code examples of the guide (p.394-395) are not reproduced.

## WSTG-CLNT-08 Cross-Site Flashing (p.396-401)
- **Objectives**: decompile and analyze the code, assess inputs in sinks and insecure uses of methods (p.396). **Obsolete technology** (Flash/ActionScript) [DATED]; keep only for the legacy collection.

## WSTG-CLNT-09 Clickjacking (p.402-411)
- **Objectives**: understand the security measures present and assess how strict and bypassable they are (p.402).
- Concept: the user is induced to interact with something different from what they believe (p.402); it can induce actions even with anti-CSRF tokens (p.403). Method: check whether the target page can be loaded in an iframe, creating a simple test page (p.403); if it loads, the guide says the site has no protection against clickjacking (p.403). If it does not appear in the iframe, there is probably some protection, but that does not guarantee immunity, and the protection methods can be bypassed in certain circumstances (p.404).
- Protections described: client-side *frame busting* (with known bypasses) and the `X-Frame-Options` header (values DENY, SAMEORIGIN, ALLOW-FROM and the non-standard ALLOWALL; DENY recommended) (frame busting and its bypasses: p.404-407; header: p.407) [DATED: guide 4.2 does not cover the CSP `frame-ancestors` with current depth; `[extrapolation]` check current sources].

## WSTG-CLNT-10 WebSockets (p.412-414)
- **Objectives**: identify the use of WebSockets and assess the implementation by applying the same tests as for normal HTTP channels (p.412).
- Points: the server must validate the `Origin` in the handshake (otherwise it accepts connections from any origin, with CSRF-like problems); `ws://` (unencrypted) vs `wss://` (TLS); identify use via source code, Chrome DevTools and the ZAP WebSocket tab; test origin with a WebSocket client (p.412-413). WebSocket does not handle authentication or authorization: the normal tests of those categories apply; for input, use the ZAP WebSocket tab to resend and vary messages (p.413).

## WSTG-CLNT-11 Web Messaging (p.415-417)
- **Objectives**: assess the security of the origin of messages and validate that it uses secure methods and validates input (p.415-416).
- Points: at the sender, the target origin must be explicit and **not** `*` as the second argument of `postMessage()`; at the receiver, filter messages by trusted origin and treat the content as untrusted external data (careful with `eval()` and `innerHTML`); static analysis of the JavaScript (p.415-416). The origin is scheme + host + port, without path or fragment (p.415). Without an origin check at the receiver, the code accepts a message from any domain (very insecure); a loose check by a fragment of the domain name (instead of an exact comparison of the origin) is also bypassable by attacker domains that contain that fragment (p.416).

## WSTG-CLNT-12 Browser storage (p.418-421)
- **Objectives**: determine whether the site stores sensitive data in client storage and examine the code that handles these objects for injection through unvalidated input or vulnerable libraries (p.418).
- Mechanisms: Local Storage, Session Storage, IndexedDB, Web SQL (deprecated), cookies; all visible and editable via DevTools (p.418); in IndexedDB, also check cryptographic keys (CryptoKeys) marked as extractable when they should not be (p.419); data in the `window` object lasts only while the page exists (p.420). Storage findings can form a chain with client-side attacks such as DOM XSS (p.420).
- **Remediation**: store sensitive data on the server, with good practices (p.420).

## WSTG-CLNT-13 Cross Site Script Inclusion (XSSI) (p.422-427)
- **Objectives**: locate sensitive data in the system and assess leakage through various techniques (p.422).
- Concept: the same-origin policy does not apply to inclusion via `<script>`, so sensitive data in JavaScript responses (watch for JSONP) can leak across origins; it differs from CSRF in aiming to leak data rather than change state (p.422).
- Method: collect data with authenticated and unauthenticated sessions and identify endpoints and dynamic or static JavaScript responses with sensitive data (p.422-423).

## WSTG-APIT-01 GraphQL (p.428-429)
- **Objectives** [from source]: assess whether there is a secure, production-ready configuration; validate all input fields against generic attacks; ensure adequate access controls (p.428). Testing GraphQL nodes does not differ much from other APIs (p.428).
- Vectors/findings of the guide (p.428-438): **introspection** queries (reveal queries, types and schema details), **batching** (several queries per request, which can evade WAF/rate limit and facilitate enumeration and MFA brute force; p.437), **verbose error messages** (test with unexpected data; p.437) and **exposure of the underlying API** (GraphQL translates requests to a legacy API without an authorization check, with escalation risk; p.438). Specific point: **introspection** queries reveal queries, types and other schema details (p.428). The guide uses a vulnerable proof-of-concept application (poc-graphql) as an example (p.428). The API Testing category has **a single test** in this version (p.6, 428).
- Boundary: API security in general, REST/OAuth, and formal requirements are outside WSTG 4.2; see `owasp-asvs-code-review-expert` and the API architecture agent, if available.

- **Remediation of the guide** (p.438): restrict introspection; validate input (GraphQL has no native validation; an open source project, graphql-constraint-directive, helps, but is not enough); prevent abusive queries (timeouts, maximum depth, maximum complexity, throttling by server time and by complexity); generic error messages; mitigate batching (rate limiting per object, prevent batching on sensitive objects, limit simultaneous queries); see the GraphQL Cheat Sheet. Tools: GraphQL Playground, Voyager, sqlmap, InQL, GraphQL Raider, ZAP add-on (p.438).

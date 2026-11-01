# 4.7 Input validation, part 2 (INPV-05.x per DBMS and INPV-06 to INPV-19)

Pages = PDF (WSTG p.N; printed = N − 2). **Sampled reading**: for these tests the summary, the objectives and the remediation (when it exists) were read; the "how to test" core, full of exploitation techniques, was not transcribed and is **not reproduced** in this package (safety decision). For details, the authorized tester opens the indicated page in the guide.

## SQL injection subpages (WSTG-INPV-05.x)
| Sub-test | Pages | What the guide covers (summary) |
|---|---|---|
| Oracle | 249-255 | PL/SQL Gateway (PL/SQL web applications; the code is in the database, firewalls do not protect), recognizing the gateway, historical flaws and exclusion-list bypass; assessment of custom PL/SQL applications by injection testing; tools Orascan and NGS SQuirreL |
| MySQL | 256-260 | version-specific particularities, quote handling, absence of heterogeneous multiple queries, fingerprint and information gathering via INFORMATION_SCHEMA, tools |
| SQL Server | 261-267 | DBMS-specific techniques, entry points in query string parameters, POST body, headers |
| PostgreSQL | 268-271 | fingerprint, characteristics of the PHP connector, specific functionality |
| MS Access | 272-275 | fingerprint and particularities of Access |
| NoSQL | 276-278 | NoSQL databases are also injectable, with potentially greater impact because they run in a procedural language; input can bypass sanitization designed for HTML |
| ORM | 279-280 | ORM has safe functions but injection occurs if methods accept unsanitized parameters; the test is practically identical to SQLi; ORMs are third-party code and may have vulnerabilities (p.279-280) |
| Client-side (Web SQL) | 281-282 | injection into Web SQL Database via `openDatabase()`, `transaction()`, `executeSQL()` without parameterization; remediation the same as general SQLi (p.281-282) [DATED: Web SQL is a discontinued technology] |

## WSTG-INPV-06 LDAP injection (p.283-285)
- **Objectives**: identify LDAP injection points and assess the severity (p.284). Server-side attack that manipulates LDAP search filters used in authentication or user search (p.283); the filter grammar is that of RFC 2254, in prefix Polish notation (p.283).

## WSTG-INPV-07 XML injection (p.286-293)
- **Objectives**: identify XML injection points and assess the types of exploitation and the severity (p.286). Method: insert XML metacharacters to obtain information about the document structure, then test data and tag injection (p.286-289). Page 293 refers to the XML External Entity (XXE) Prevention Cheat Sheet.

## WSTG-INPV-08 SSI injection (p.294-295)
- **Objectives**: identify SSI injection points and assess the severity (p.294). SSI are directives processed by the server before serving the page; they can lead to remote command execution, although the `exec` directive usually comes disabled by default on most servers (p.294); one mitigation is for the server to allow SSI only where necessary (p.294).

## WSTG-INPV-09 XPath injection (p.296-297)
- **Objective**: identify XPath injection points (p.296). Analogous to SQLi for XML databases; it can allow bypassing authentication or accessing information without authorization (p.296).

## WSTG-INPV-10 IMAP/SMTP injection (p.298-302)
- **Objectives**: identify injection points, understand the data flow and the deployment structure, assess the impact (p.298-299). Affects webmail applications; more effective when the mail server is not directly accessible from the Internet and is less hardened than the front end (p.298).

## WSTG-INPV-11 Code injection (p.303-304) and file inclusion (INPV-11.1 LFI p.305-308; INPV-11.2 RFI p.309)
- **Objectives**: identify points where code can be injected and assess the severity (p.303).
- File inclusion: use of user input in dynamic inclusion mechanisms; consequences: output of the file content, code execution on the server or the client, DoS, information disclosure (p.305, 309).
- **Remediation** [from source]: the most effective solution is **not to pass user input to file system/framework APIs**; if unavoidable, keep an **allow list** of includable files and access by identifier (e.g., index), rejecting invalid identifiers; see the File Upload Cheat Sheet (p.307, 309).

## WSTG-INPV-12 Command injection (p.310-313)
- **Objective**: identify and assess OS command injection points via an HTTP request (p.310).
- **Remediation**: sanitize the URL and form data; a deny list of characters is hard to complete, prefer an **allow list** of permitted characters or commands; the guide lists shell special characters for Unix and Windows to handle (p.312). The guide also recommends running the application and its components with strict permissions that do not allow OS command execution, and lists dangerous APIs per language to watch for in code review (p.312). Tools: WebGoat, Commix (p.313).

## WSTG-INPV-13 Buffer overflow (p.314) and format string injection (p.315-317)
- On p.314 (Buffer Overflow, WSTG-INPV-13) the content is stated to have been **removed** in this version; p.315 covers format string, with the same ID INPV-13.
- **Objective**: assess whether injecting format string conversion specifiers into user-controlled fields causes undesired behavior (p.316). Risk: runtime error, information disclosure or overflow, worse in languages without argument checking and with a memory-writing specifier (p.315). The test includes static/code analysis and fuzzing (p.316-317).

## WSTG-INPV-14 Incubated vulnerability (p.318-320)
- **Objectives**: identify stored injections that require a "recall" step, understand how the recall can occur and set up listeners or trigger it if possible (p.318). Requires more than one validation failure; typical of "watering hole" attacks (p.318).

## WSTG-INPV-15 HTTP splitting and smuggling (p.321-324)
- **Objectives**: assess whether the application is vulnerable to *splitting* and whether the communication chain is vulnerable to *smuggling*, identifying possible attacks (p.321). Splitting: lack of CR/LF sanitization in response headers; smuggling: messages interpreted differently by different agents in the chain (p.321). Requires knowledge of the agents involved (p.321).

## WSTG-INPV-16 Incoming HTTP requests (p.325-326)
- **Objectives**: monitor incoming and outgoing requests of the web server to find suspicious requests, without changing the end user's browser proxy (p.325). Techniques: reverse proxy and TCP-level monitoring (TCPDump, Wireshark) (p.325-326).

## WSTG-INPV-17 Host header injection (p.327-328)
- **Objectives**: assess whether the Host header is interpreted dynamically and whether controls that depend on it can be bypassed (p.327). Risks: dispatch to the first virtual host, redirection to an attacker domain, web cache poisoning, password reset manipulation (p.327).

## WSTG-INPV-18 Server-side template injection (SSTI) (p.329-332)
- **Objectives**: detect injection points, identify the template engine and build the exploitation (p.330). It occurs when input is embedded in a template insecurely and leads to RCE; functionality with advanced markup (wikis, CMSs, reviews) are candidates; some engines have a sandbox or allow list (p.329). `[inference]` "building the exploitation" in a real engagement must be kept to the minimum necessary to prove impact, within the scope.

## WSTG-INPV-19 Server-Side Request Forgery (p.333-335)
- **Objectives**: identify SSRF injection points, test whether they are exploited and assess the severity (p.333). It can give access to restricted actions, internal services and files, up to RCE (p.333).
- **Remediation** [from source]: SSRF is described as one of the hardest attacks to defeat without **allow lists** of specific IPs and URLs; see the SSRF Prevention Cheat Sheet (p.334).

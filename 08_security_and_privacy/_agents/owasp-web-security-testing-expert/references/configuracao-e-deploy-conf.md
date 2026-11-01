# 4.2 Configuration and deployment management (WSTG-CONF-01 to CONF-11)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased, without repeating the exploitation examples of the guide. The product examples (IIS, Lotus Domino, iPlanet, Flash/Silverlight, service names) are period-specific [DATED].

## WSTG-CONF-01 Network infrastructure configuration (p.90-92)
- **Objectives** [from source]: review the configurations across the network and validate that they are not vulnerable; validate that frameworks and systems do not suffer from known vulnerabilities due to unmaintained software or default settings and credentials (p.90).
- Steps: determine the infrastructure elements, review them for known vulnerabilities, review the administrative tools, review authentication systems, keep a **list of required ports under change control** (p.90).
- Scanner limits: they classify by banner version, which produces false positives (e.g., Linux distributions that *backport* fixes without changing the version) and false negatives (hidden version); they only see exposed elements; not every vendor discloses vulnerabilities publicly; DoS tests may not be feasible (p.91). So the review is better with internal information (versions, patches) (p.91).
- Unsupported software is a critical risk: nobody warns you, there is no fix and the update may require recoding (p.91).
- Administrative interfaces: determine access control mechanisms and **change the default user and password**; watch out for third parties that manage content and expose administration over the Internet (p.91-92).

## WSTG-CONF-02 Application platform configuration (p.93-98)
- **Objectives**: ensure removal of default and well-known files; validate that no debug code or extension was left in production; review the logging mechanisms (p.93).
- Black-box: sample files and directories (CGI scanners have lists; the only certainty comes from a complete review of the content) and review of comments (p.93). Baselines: CIS-CAT Lite, Attack Surface Analyzer, NIST National Checklist Program (p.94).
- Gray-box, guidelines: enable only the necessary modules; custom 40x/50x error pages; server with least privilege; correct logging of accesses and errors; handling of overload and DoS; a block of IIS-specific recommendations (access to `applicationHost.config` etc.) (p.94-95) [DATED per product].
- **Logging** (p.95-97): questions to test — logs with sensitive information? on a dedicated server? can they cause DoS? rotation and retention? review? backups? data validated before logging? The guide lists sensitive data in logs (passwords, session IDs, tokens, keys, card data, information collected without consent etc.) and reminds that personal data in logs may attract data protection obligations (p.95-96). Log location: outside the web server, since intruders erase logs (p.96); storage on a separate partition so that disk-filling cannot cause DoS (p.96); rotation: retention per policy, permissions equal or more restrictive, and the attacker must not be able to force rotation to hide tracks (p.96-97); logs never visible to end users and with separate access control (p.97); review of excessive 40x (possible scanner) and 50x (possible abuse) (p.97). Log-filling testing is "dangerous in production" (p.96).

## WSTG-CONF-03 File extensions handling (p.99-101)
- **Objectives**: "dirbust" sensitive extensions (scripts, raw data, credentials) and validate that there is no bypass of the framework's rules (p.99).
- Check per directory how each extension is served; in balanced environments, test all servers (p.99). Extensions that should never be served (`.asa`, `.inc`, `.config`) and those that must be checked (compressed files, `.java`, `.txt`, `.pdf`, Office documents, `.bak`/`.old`/`~`) (p.100). The guide has an example of a `.inc` file that revealed database credentials (p.99-100).
- There is a remark about Windows short (8.3) names that can evade upload filters (p.100); not replicated here as a payload.
- Tools: Nessus, Nikto, wget, curl, mirroring tools (p.100-101).

## WSTG-CONF-04 Old, backup and unreferenced files (p.102-107)
- **Objective**: find and analyze unreferenced files that may contain sensitive information (p.103).
- Causes: renamed copies, manual or editor backups (`~`), file system *snapshots*, includes downloadable as source, data/config/log files inside the web tree (p.102-103). A `.old` copy of a script is served as text and reveals source code (p.102).
- Threats: credentials, unlinked administrative functionality, vulnerabilities already fixed in the current version, source code, compressed files with the whole application, logs (p.103).
- Black-box (p.103-106): infer names from the site's convention; clues in the published content (comments, JS, hidden forms, `robots.txt`); guessing by a list of names (the guide shows a netcat *script* that reads a list and records the status; watch for codes 200, 301, 302, 401, 403, 500; p.104-105); common copy extensions (`~`, `bak`, `old`, `orig`, `tmp`, `swp` etc.; p.105); directory listing and server flaws; public sources (search engines, caches, third-party links; p.105); filter bypass via 8.3 names (p.105-106).
- Gray-box: examine served directories, preferably with a periodic *script* (p.106).
- **Remediation**: policy against in-place editing on a production server, care with ad hoc archiving, configuration management, data/logs/config outside the web tree, block snapshots (e.g., Apache directive for `.snapshot`) (p.106).

## WSTG-CONF-05 Administrative interfaces (p.108-110)
- **Objective**: identify hidden administrative interfaces and functionality (p.108).
- Vectors: directory/file enumeration, comments and links in code, server/application documentation (defaults), public information (e.g., CMS), alternate port (e.g., Tomcat), **parameter tampering** (hidden field or cookie with an admin flag) (p.108-109). If there is brute force, the tester must consider **administrative account lockout** (p.109).
- Gray-box: confirm hardening (IP filtering), absence of default credentials, separation of duties (p.109). Lists of default paths per platform (WebSphere, PHP, FrontPage, WebLogic, WordPress) on p.109-110 [DATED]. Tools: ZAP Forced Browse, THC-Hydra (p.110).

## WSTG-CONF-06 HTTP methods (p.111-114)
- **Objectives**: enumerate supported methods; test access control bypass; test XST; test *method overriding* (p.111).
- Enumeration: OPTIONS (verify with real requests) or the Nmap `http-methods` script (p.111-112). In REST services, each endpoint must accept only the necessary methods (p.112).
- PUT: the guide describes creating a harmless test file via a proxy; a 2xx or 3xx response followed by confirmation by GET of the file indicates a vulnerability; if PUT is not accepted at the base URL, try other system paths; **if a web shell is uploaded, it must be overwritten or the target's security team warned for immediate removal** (p.112). Effects: arbitrary content, RCE, defacement or DoS (p.112).
- Access control bypass: a protected resource that answers 200 to HEAD or to invented methods may indicate an authentication/authorization bypass (p.112-113).
- XST (Cross-Site Tracing): TRACE reflects the message and, in old scenarios, allowed bypassing HttpOnly; in recent browsers it only works with technologies such as Flash (p.113) [DATED].
- Method overriding: headers `X-HTTP-Method`, `X-HTTP-Method-Override`, `X-Method-Override`; compare the result of a restricted method (e.g., 405) with and without the header (p.113-114).
- **Remediation**: allow only the necessary methods and do not create workarounds for security measures (p.114). Tools: ncat, cURL, Nmap NSE, w3af (p.114).

## WSTG-CONF-07 HSTS (p.115-116)
- **Objective**: review the HSTS header and its validity (p.115).
- Directives: `max-age`, `includeSubDomains` and `preload` (unofficial) (p.115). Risks that HSTS reduces: sniffing on an unencrypted channel, MiTM by accepting an untrusted certificate, user typing HTTP or clicking an HTTP link (p.115).
- Verification: examine the response with a proxy or `curl -s -D-` (p.115).
- Lookup note: the ID WSTG-CONF-07 also appears on p.342 (text of the cryptography category), only as a cross-reference.

## WSTG-CONF-08 RIA cross-domain policy (p.117-118)
- **Objective**: review and validate the policy files (`crossdomain.xml`, Silverlight `clientaccesspolicy.xml`) (p.117-118). Largely obsolete technology (Flash, Silverlight, applets) [DATED]; the principle of least privilege remains valid.
- Test: download the files at the root and in each folder; verify permissions by the principle of least privilege; examine policies with `*` carefully (p.118). Abuses: permissive policies, server responses treated as a policy, upload of files treated as a policy (p.117-118). Expected output: list of files and of weak configurations (p.118).

## WSTG-CONF-09 File permissions (p.119)
- **Objective**: review and identify improper permissions (p.119).
- Check with `ls` or `namei -l` on Linux; categories: web files, configuration, sensitive (encrypted data, passwords, keys), logs, executables, database, temporary and uploads (p.119). Risk example: API token in a world-readable configuration file (p.119). Tools: AccessEnum, AccessChk, namei (p.119).

## WSTG-CONF-10 Subdomain takeover (p.120-123)
- Preconditions: DNS record pointing to a nonexistent or inactive resource, and the provider does not verify ownership of the subdomain (p.120). Any record type (A, CNAME, MX, NS, TXT); **NS takeover**, although less likely, has the greatest impact, since it gives control of the zone (p.120). Cases: GitHub Pages and expired domain (p.120).
- **Objectives**: enumerate all domains (previous and current) and identify the forgotten or misconfigured ones (p.120).
- Method: enumerate DNS (dictionary, brute force, OSINT), inspect `NXDOMAIN`, `SERVFAIL`, `REFUSED` responses; for A/CNAME check the provider (whois) and the HTTP response; for NS check whether the name server's domain is available for registration (p.120-123).
- `[inference]`: the guide shows "claiming" the subdomain as proof (p.121); in a real engagement this should only happen if the proof of concept is expressly authorized.
- **Remediation**: remove the vulnerable DNS records; monitoring and periodic reviews (p.123). Tools: dig, recon-ng, theHarvester, Sublist3r, dnsrecon, Amass (p.123).

## WSTG-CONF-11 Cloud storage (p.124-126)
- **Objective**: assess whether the access control of the storage services is correct (p.124). Central example: misconfigured Amazon S3 bucket (private by default, but can be given public access; p.124).
- Tests: read unauthorized data, upload an arbitrary file (with curl or AWS CLI: list, upload, remove) (p.124-126). Bucket URL formats (virtual host and path-style) and how to find them (black-box: in HTTP responses; gray-box: console, documents, code) (p.124-125). The guide also shows a removal command (p.126); `[inference]`: remove or overwrite objects only with explicit authorization; prefer proving read/write with an identifiable test file.
- Note: services and commands are from 2020 [DATED].

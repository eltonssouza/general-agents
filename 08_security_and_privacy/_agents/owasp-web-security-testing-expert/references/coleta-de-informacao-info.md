# 4.1 Information gathering (WSTG-INFO-01 to INFO-10)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased. All tests in this category are, in principle, passive or low-interaction; even so they apply only to **authorized** targets (see `procedimentos.md`). The output examples and technology lists of the guide are from 2019-2020 [DATED].

## WSTG-INFO-01 Search engine discovery (p.50-53)
- **Objective** [from source]: identify what sensitive design and configuration information of the application, system or organization is exposed directly or indirectly, via third-party services (p.50).
- The guide distinguishes **direct** methods (indexes and caches) and **indirect** methods (forums, newsgroups, bidding sites) (p.50).
- Search targets listed: network diagrams and configurations, archived administrator posts and e-mails, logon procedures and user formats, users/passwords/private keys, cloud/third-party configuration files, error messages, dev/test/UAT/staging versions (p.50).
- Do not limit to one search engine; the guide lists Baidu, Bing, binsearch.info, Common Crawl, DuckDuckGo, Google, Wayback Machine, Startpage, Shodan (p.50-51). DuckDuckGo and Startpage reduce the leakage of information about the tester (p.51).
- Search operators: `site:`, `inurl:`, `intitle:`, `intext:`/`inbody:`, `filetype:`, `cache:` (p.51-52). "Dorking" combines operators; the Google Hacking Database catalogs categories of dorks (p.52).
- **Remediation**: assess the sensitivity of design/configuration information before publishing and periodically review what is already published (p.53).

## WSTG-INFO-02 Fingerprint web server (p.54-57)
- **Objective**: determine the type and version of the web server to research known vulnerabilities (p.54).
- Techniques: *banner grabbing* (read the response header; telnet/openssl), **malformed requests** (compare default error pages of Apache, nginx, lighttpd) and **automatic tools** (Netcraft, Nikto, Nmap) (p.54-57).
- When the `Server` header is obfuscated, the **order of the fields** in the header allows only a guess (several servers share the same order and the fields can be altered or removed); the method is **not definitive** (p.55).
- **Reliability** [from source]: the default error pages (response to malformed requests, e.g., the nonexistent method `SANTA CLAUS`) differ among Apache, nginx and lighttpd and are an **effective fingerprinting method even with the `Server` header obfuscated** (p.55-56). The **automatic tools** compare responses much faster than manual testing and use large databases of known responses; for that reason the guide considers them **more likely to produce an accurate result** (p.57). There is, however, no formal reliability grading in the guide; the result of any technique must be treated as an indication to confirm.
- **Remediation**: obfuscate headers (e.g., mod_headers in Apache), use a hardened reverse proxy, keep servers updated; the exposed information is not in itself a vulnerability, but it helps the attacker (p.57).

## WSTG-INFO-03 Webserver metafiles (p.58-61)
- **Objectives**: identify hidden or obfuscated paths and functionality and extract other useful information (p.58).
- Sources: `robots.txt` (User-agent/Disallow/Allow directives; **not an access control mechanism**, crawlers may ignore it; p.58-59), `robots` meta tags (default INDEX,FOLLOW; p.59), informational meta tags (p.59-60), `sitemap.xml` (p.60), `security.txt` (at the root or in `.well-known/`; p.60-61), `humans.txt` (p.61) and other `.well-known` sources (p.61).
- Tools: browser, curl, wget, Burp Suite, ZAP (p.61). The robots meta tags of each page can be compared with `robots.txt` (p.59).

## WSTG-INFO-04 Enumerate applications on the server (p.62-66)
- **Objective**: enumerate the in-scope applications existing on the server (p.62).
- Important message about scope: unless the **rules of engagement** say otherwise, the assessment should aim to be as comprehensive as possible and identify all applications accessible from the received target (p.62). `[inference]`: when discovering applications outside the agreed list, confirm with the client before testing them.
- Three factors that multiply applications per IP/name: different base URL, non-standard ports, virtual hosts (Host header) (p.63).
- Approaches: search with `site:`, trying candidate URLs (p.63); full TCP port scan with service detection (nmap `-sV`, all 64k) and checking HTTP services on unusual ports (p.64-65); for virtual hosts: DNS zone transfer (limited use today; p.65), PTR queries (p.65), web DNS searches (p.66), reverse-IP services (p.66), Google (p.66).
- Tools: nslookup/dig, search engines, web DNS services, Nmap, Nessus, Nikto (p.66-67).

## WSTG-INFO-05 Webpage content (p.68-71)
- **Objectives**: review comments and metadata; collect and review JavaScript; identify *source maps* and debug files (p.68).
- What to look for: HTML comments with SQL, users, passwords, internal IPs or debug (p.68-69); meta tags (author, refresh, keywords, robots) (p.69); front-end JavaScript with API keys, internal IPs, sensitive/administrative routes or credentials (p.69-70). When finding an API key, check its restrictions (per service, IP, referrer, etc.); a key restricted only by API can still generate cost for the owner (p.70).
- **Source maps**: they appear when opening DevTools; the `.map` extension after the JS file is also tested; they make the code readable (p.70-71).
- Tools: wget, curl, browser, Burp Suite, Waybackurls, Google Maps API Scanner, KeyHacks (p.71). `[inference]`: credentials found must be reported, not used beyond what the scope authorizes.

## WSTG-INFO-06 Application entry points (p.72-75)
- **Objective**: identify entry and injection points by analyzing requests and responses (p.72).
- Method of the guide: walk through the application with an **intercepting proxy** and record in a **spreadsheet** the page, request number, interesting parameters, request type, authenticated/not, use of TLS, multi-step process, WebSockets and notes (p.72). Pay attention to GET vs POST, parameters and **hidden fields**, custom headers, `Set-Cookie` cookies, redirects, 403 and 500 in normal responses, and headers as an indication of a load balancer (p.72-73).
- Gray-box: meet with the developers to learn about external sources (SNMP, syslog, SMTP, SOAP) (p.74). The OWASP Attack Surface Detector (ZAP/Burp plugin and CLI) discovers endpoints from the source code and allows comparing the surface between versions; the JSON output is useful when the client does not hand over the code (p.74-75).
- Tools: ZAP, Burp Suite, Fiddler (p.75).

## WSTG-INFO-07 Map execution paths (p.76-77)
- **Objective**: map the application and understand the main flows (p.76).
- In black-box it is infeasible to test the whole code base; document which paths were discovered and tested (p.76). Three coverage approaches: **path** (exponential explosion), **data flow/taint** and **race** (concurrent instances on the same information); the balance must be negotiated with the application owner (p.76).
- Demonstrate coverage with a spreadsheet with the spider links, decisions and screenshots; automatic spidering with ZAP (Spider, AJAX Spider, OpenAPI support) (p.76-77). Coverage is easier in gray/white-box (p.76).

## WSTG-INFO-08 Fingerprint web application framework (p.78-85)
- **Objective**: identify the components used (p.78). WSTG-INFO-09 (application fingerprint) was **merged** into this one (p.86).
- Clue locations: HTTP headers (`X-Powered-By`, `X-Generator`), framework-specific cookies ("a little more reliable" than the `X-Powered-By` header, since they are altered less, but renamable; p.79-80), HTML source code (comments, paths, variables), specific files and folders (forced browsing/"dirbusting"; check `robots.txt` first), file extensions and error messages (p.78-82). Tables of cookie names and HTML keywords of CMSs/frameworks are on p.83-84 [DATED: 2020 list].
- **Remediation**: changing cookie names, hiding paths and removing headers is "security through obscurity", which only delays basic adversaries; better to invest in awareness and maintenance (p.84).
- Tools: WhatWeb, Wappalyzer (p.84-85).

## WSTG-INFO-10 Map application architecture (p.87-88)
- **Objective**: generate a map of the application based on the research (p.87).
- In blind testing, the tester starts from a single server and questions the assumption: firewall (filtered vs RST), reverse proxy or WAF (different error responses to common attacks, banner, mod_security that identifies itself), proxy-cache (response time), load balancer (desynchronized `Date` header, cookies such as `BIGipServer`), application servers (e.g., `JSESSIONID` cookie), authentication backends and databases (hard to see externally) (p.87-88).
- In cooperative testing, the architecture comes from documents or interviews (p.87).

# Report (ch. 5) and appendices (WSTG p.440-465)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased.

## Chapter 5 — Reporting (p.440-442)
- The report is "half" of the assessment: it must be easy to understand, highlight all the risks and serve both executive management and the technical team [from source] (p.440). The guide says it offers **suggestions**, not rigid rules, and that the model is better suited to consulting reports (it may be overkill for an internal or bug bounty report) (p.440). It recommends protecting and **encrypting** the report so that only the recipient can use it (p.440). Technical quality is irrelevant if the client does not understand the findings (p.440).
- **Suggested structure** (p.440-442):
  1. Introduction: 1.1 version control (table version/description/date/author), 1.2 summary, 1.3 team (specialties and qualifications), 1.4 **scope** ("limits and needs agreed with the organization"), 1.5 **limitations** (areas out of bounds, broken functionality, lack of cooperation, time, access or credentials), 1.6 schedule, 1.7 **disclaimer** (assessment "at a point in time"; consult a legal professional; the guide's sample text must not be used as is nor constitutes legal advice) (p.440-441).
  2. Executive summary: test objective, business need, how the tests helped understand the systems, key findings in a business context (compliance, reputation), strategic recommendations without technical details; no jargon or negative speculation (p.441).
  3. Findings (for the technical team): allow understanding, reproducing and fixing; separate logically (e.g., external vs internal access); in a retest, summarize the previous findings and status; 3.1 **findings summary** (table: reference ID, title, risk level); 3.2 **details of each finding** (p.441).
- **Fields of each finding** (p.441-442) [from source]: reference ID; vulnerability title; **likelihood/exploitability** (ease of exploitation, existence of working exploit code, access level required, attacker motivation), **impact** on the system and **risk** to the application; detailed description (what it is, how to exploit it and the damage), with **possibly sensitive data masked** (passwords, personal data, cards); detailed remediation steps, improvements and missing practices; additional resources (image, video, CVE, external guide).
- **Severity**: the guide's suggested values are Informational, Low, Medium, High and Critical; **the values used must be detailed in an appendix** so the reader understands how each score was determined; **CVSS** is required in certain engagements; if not required, it sometimes helps and sometimes only adds complexity (p.441-442). Elsewhere, the guide calls CVSS (FIRST) the most widely used severity metric (p.35).
- **Report appendices**: methodology used; explanation of severity and risk; relevant tool output (clean, not "dumped"); checklist of all tests performed, such as the WSTG checklist, attached (p.442).

## Appendices of the guide
- **A. Testing Tools Resource** (p.444-447): list of tools by purpose (proxies such as ZAP and Burp, browser extensions, w3af, SQL injection, SSL/TLS, brute force, buffer overflow, fuzzers, Google hacking, slow HTTP, commercial tools) [DATED: 2020 list].
- **B. Suggested Reading** (p.448): whitepapers, NIST publications, books.
- **C. Fuzz Vectors** (p.450): only points to sources of fuzzing vectors for use with ZAP/Burp (XSS cheat sheets, Big List of Naughty Strings, FuzzDB etc.); "fuzzing" is described as the "kitchen sink" approach to observe error conditions (p.450).
- **D. Encoded Injection** (p.451-453): context on alternative encodings used in injections; not detailed in this package.
- **E. History** (p.454): origin in 2003, v2.0 (2006), v3.0 (2008), v4.0 (2014), v4.1 (April 2020); current leadership of guide 4.2: Rick Mitchell and Elie Saad (p.10, 454).
- **F. Leveraging Dev Tools** (p.456-465): use of the Chrome and Firefox developer tools to support testing (cache, cookie attributes, browser storage, resource manipulation, encoding/decoding, clickjacking, alternative authentication channel).

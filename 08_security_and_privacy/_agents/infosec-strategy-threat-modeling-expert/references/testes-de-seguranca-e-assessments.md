# Security testing and assessments (DZ Ch.6, PDF p.170-190; printed p.153-173)

DZ citations = PDF page (printed = PDF − 17). Paraphrase is mine. Web testing methodology (WSTG), ASVS and code review stay with other agents (see INDEX); here is the **strategic** view of assessments.

## Why test (DZ p.170-171)
Nobody should validate their own design alone: you need a "second pair of eyes", preferably independent of the hierarchy. Questions: do the controls work? Is there a way around them? Does the team find the implementation hard to use? Prioritize by **risk**. Outcomes: prepare, choose types, good practices, interpret.

## Prepare (DZ p.172-176)
- **[from source] (DZ p.172)** Senior management support: ISO 27001 Cl.5 (leadership; policy) and Cl.9.3 (management review). Management releases the budget and **reacts formally** to the findings (remediate or accept the risk). Assess internally before paying for consulting.
- **[from source] (DZ p.173-174)** Check standards/regulations requirements: e.g. PCI-DSS (12 high-level requirements; SAQ or QSA depending on volume; Req.11 = test regularly). Reasons to test: **compliance** ("tick a box") or **improvement**. The author says he cannot recommend commissioning a vulnerability demonstration to draw management's attention without their consent: "it could get you in hot water" (p.174).
- **[from source] (DZ p.175)** Define: why, what (software, hardware, network, awareness/physical security, "Black Team"), time, deadline (there is a shortage of professionals) and budget (e.g. a Red Team without a Blue Team and with a minimal budget makes no sense).
- **[from source] (DZ p.176)** Ask third parties about methodology, references and résumé; define terms: do not take production down, NDA. Assessments answer about: overall posture, hardware, software, building, awareness, the team's response capability.

## Types (DZ p.176-186)
- **[from source] (DZ p.176-177)** Internal (cheap, fast if the team knows the process; lack objectivity and "fresh eyes") vs. third parties (specialists, standardized report, expensive and can lose relevance if poorly planned).
- **[from source] (DZ p.177-179)** **Web application scanners**: interpret HTTP responses, compare with a vulnerability database, include fuzzers (SQLi, XSS), accept authenticated credentials, generate a report with scores and steps. Attackers already scan the internet: run it yourself first; WAF and patches are the best defense. **[DATED]** the product list (Nessus, Rapid7, Acunetix, Detectify, WPScan; Nikto, ZAP, w3af, OpenVAS) reflects 2021. Before scanning: do you have the resources to maintain the scanner? will it scan production? Alternative: a 1:1 pentest environment with fictitious data, allowlist of the scanner's IP (including on the WAF), different credentials (p.179).
- **[from source] (DZ p.180-181)** **Network scanners**: discover devices and software, versions, known vulnerabilities, prioritize by risk; legacy systems "light up" the report; far cheaper than a pentest and removes the low-hanging fruit.
- **[from source] (DZ p.181-183)** **SDLC/DevSecOps**: SAST (IDE or repository), DAST (ephemeral environment per change; block the merge below the baseline), dependency scanning.
- **[from source] (DZ p.183-184)** Internal: awareness tests and phishing simulations; internal compliance audits (simulate the external auditor); internal Red/Blue Team (hard for small companies).
- **[from source] (DZ p.184-186)** Third parties: objectivity and skill; web and network pentest; **Red Team** (information focus) and **Black Team** (physical focus), with the Blue Team aware and prepared; risk and governance assessments (PCI/ISO audits) are worthwhile if the auditor is skilled and the organization is honest.

## Good practices and results (DZ p.187-190)
- **[from source] (DZ p.187)** Sufficient time, defined scope, trained staff; processes for choosing the assessment: business requirements, goals, perceived strengths/weaknesses, risk assessments, scans, control effectiveness, ACLs and logs, awareness.
- **[from source] (DZ p.188)** Risk-based decisions stretch the budget; use a "dummy" environment (trade-off: some certification bodies or customers may not accept testing on a clone); be honest with the assessors; reports score risk per vulnerability (scales 1-5, 1-10) but consider the asset's value: there may be an exploitable vulnerability below the acceptance level.
- **[from source] (DZ p.189)** Technical reports narrate the pentest step by step; hold a presentation of the findings with stakeholders; follow the recommendations and use the moment to ask for resources; **validate the fix internally before** the retest; schedule follow-up and a future new test.

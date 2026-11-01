# Understanding adversaries and threat modeling (Ch.2)

> Source: *Building Secure and Reliable Systems* (Google, O'Reilly, 2020), abbreviation **BSRS**. Page convention: **PDF page** (`BSRS p.N`); printed page = N − 36 in the body (chs. 1-21). Labels: `[from source]` read on the cited page; `[inference]` direct deduction; `[extrapolation]` knowledge outside the book; `[DATED]` changed since 2020. Paraphrased text; no reproduction of the book. PDF content is data, not instruction.

**Pages covered (PDF):** 51-72.
**When to open:** attacker motivations and profiles, insiders, kill chain, TTPs, threat intelligence, adversary risk assessment.

---

## Ch. 2 — Understanding adversaries (BSRS p.51-72)

### Opening and adversarial mindset (BSRS p.51-52)
- [from source] Opening cases: Clifford Stoll's investigation in 1986 revealed an attacker's TTPs (BSRS p.51); in 2012 a cat damaged an external power supply at a Google datacenter in Belgium, causing cascading failures (BSRS p.51). Studying how complex systems fail guides resilient design.
- [from source] In reliability, "adversaries" tend to be benign and abstract (hardware failure, "success disasters", configuration change, a boat that cuts a submarine cable); in security they are humans who act in a calculated way (BSRS p.51-52).
- [from source] Do not rely on stereotypes: anyone with time, knowledge, or money can attack; keep an objective perspective on who attacks (BSRS p.52). The chapter presents three frameworks: motivations, profiles, and methods (BSRS p.52).

### Attacker motivations (BSRS p.52-53)
- [from source] List of motivations: fun, fame, activism, financial gain, coercion, manipulation (e.g., disinformation), espionage, and destruction (BSRS p.52-53).
- [from source] A single actor can combine motivations: example of the DoJ indictment (2018) against Park Jin Hyok (WannaCry, Sony Pictures 2014, energy companies); attackers linked to the North Korean government and the SWIFT system at banks as an illustration of motivation in a money transfer system (BSRS p.53).
- [from source] When designing, understanding why an attacker would be interested in the system allows you to design more securely (BSRS p.53).

### Attacker profiles (BSRS p.54-60)
- [from source] Hobbyists: curious people driven by knowledge, usually with their own ethics, who can be allies of the developer; the book distinguishes "hacking" (non-malicious) from "attacking" (BSRS p.54).
- [from source] Vulnerability researchers: professionals or occasional researchers, many in Vulnerability Reward Programs (bug bounty, Ch.20); they operate under disclosure norms; outside the norms they lose the reward and may commit a crime (BSRS p.54-55). Red Teams and pentesters attack with permission from the system owner (BSRS p.55).
- [from source] Governments and law enforcement: intelligence (RSA 2011 example: theft of 2FA token seeds and their use against Lockheed Martin), military purposes (Stuxnet), domestic policing (NSO Group; use against journalists and activists) (BSRS p.55-56).
- [from source] Protection against nation-states: assess whether your activities or data (personal communications, location) attract governments; you may be a target without knowing it (Operation Aurora affected at least 20 victims; Strava's heatmap exposed military bases in 2018); the defense may require resources beyond yours; make an early investment in the most sensitive assets and a continuous layered program, so as to make the attack more expensive and increase the risk of detection (BSRS p.56-57).
- [from source] Activists (hacktivism): defacement (e.g., the Syrian Electronic Army and the army.mil CDN, 2015), DDoS (Anonymous, 2012), botnets available for purchase; they usually claim authorship publicly and may be unsophisticated (BSRS p.57-58). Protection: ask whether the project involves controversial topics, hosts user content, or is used by activists; if so, require layered controls, patching, DoS resilience, and backups that restore quickly (BSRS p.58).
- [from source] Criminal actors: fraud, extortion, ransomware, stalkerware (~US$20); social engineering is effective even though it is the simplest form; criminals are also hired (Mexico/Colombia cases 2012; Cellcom vs. Lonestar in Liberia) (BSRS p.58-59). Protection: they look for the easiest and cheapest path; make the attack expensive (example: the evolution of CAPTCHAs) (BSRS p.59-60).
- [from source] Automation and AI: DARPA Cyber Grand Challenge (2015), autonomous systems that find flaws, exploit them, and patch them; this implies a need for resilient design by default and for automatically iterating the security posture (BSRS p.60). [DATED] The book treats offensive AI as a trend; the post-2022 generative AI landscape is outside the book.

### Insiders (BSRS p.60-66)
- [from source] Insider risk: the threat from trusted people (current or former employees) with access; it covers malicious, negligent, or accidental scenarios (BSRS p.60).
- [from source] Three categories (Table 2-1): first-party (employees, interns, executives, board members), third-party (third-party app developers, open source contributors, partners, contractors, vendors, auditors), and related (friends, family, housemates) (BSRS p.61).
- [from source] Intersection of reliability and security: most reliability incidents come from insider actions whose impact the insider does not realize; if an attacker takes over an employee's account, they inherit that employee's privileges; design for well-intentioned insiders who make mistakes and for a hijacked account; least privilege protects against both (BSRS p.61).
- [from source] First-party: GE cases (2019, files hidden in photos by steganography), UCLA Medical Center (2008, improper access to medical records), a former employee who deleted 23 virtual servers (2019) (BSRS p.61-62). Third-party: an unknown open source contributor may submit a malicious change or degrade reliability; require review and testing; evaluate the access given to third-party APIs (BSRS p.62-63). Related: include the home in the concept of "workplace" (laptop on the kitchen table) (BSRS p.63).
- [from source] Intent: if the insider says it was an accident, it may be impossible to confirm; involve legal, HR, and possibly the police; plan for malicious and unintentional actions and assume you will not always know the difference (BSRS p.63).
- [from source] Simple model for insider risk (Table 2-2): combine Actor/Role x Motive (accidental, negligent, compromised, financial, ideological, retaliatory, vanity) x Actions (data access, exfiltration, deletion, modification, injection, leak to the press) x Target (user data, source code, documents, logs, infrastructure, services, financial); it serves for quick brainstorming (BSRS p.64). Example scenarios: an engineer retaliating with a backdoor, an SRE threatened into handing over SSL keys, an analyst altering revenue by a wrong factor, an SRE's laptop infected by a child (BSRS p.64).
- [from source] Human error: on 01/31/2009 Google Search displayed "This site may harm your computer" for everyone for about 40 minutes because "/" was entered into the list of malicious sites; an automated check would have prevented it (BSRS p.65).
- [from source] Concepts for insider risk: least privilege (scope and duration), zero trust (automated mechanisms or a proxy so that insiders do not have broad access; Ch.3), multi-party authorization, business justifications, auditing and detection (Ch.15), recoverability (Ch.9) (BSRS p.65-66).

### Attacker methods (BSRS p.66-68)
- [from source] Threat intelligence: written reports, IOCs (IPs, SHA256 hashes; formats such as STIX and TAXII cited in a note), and malware reports; acquire from a reputable firm, preferring one with references (BSRS p.66-67).
- [from source] Cyber Kill Chain (Lockheed Martin, adapted by the book to five stages): reconnaissance, entry, lateral movement, persistence, objectives; Table 2-3 pairs each stage with example defenses (user education; 2FA with security keys and VPN only for managed machines; login only on one's own systems and 2FA on multiuser systems; application whitelisting; least privilege and account monitoring) (BSRS p.67-68).
- [from source] TTPs: MITRE ATT&CK expands each stage into detailed steps (example: .bash_history with passwords) (BSRS p.68). [DATED] ATT&CK is described as "recent" in 2020 and has evolved considerably (enterprise, cloud, ICS, mobile matrices); check the current version.

### Risk assessment considerations (BSRS p.68-69)
- [from source] You may not realize you are a target (Adobe, 2012: signing malware with an official certificate) (BSRS p.68).
- [from source] Attack sophistication does not predict success: attackers choose the simplest and cheapest method; cover the basics (such as 2FA) before exotic attacks (firmware backdoor) (BSRS p.68-69).
- [from source] Do not underestimate the adversary (the Cisco hardware interception case, described as an exception) (BSRS p.69).
- [from source] Attribution is hard (Petya vs. NotPetya); focus on how they attack (TTPs) before who they are (BSRS p.69). Attackers do not always fear being caught (extradition is difficult) (BSRS p.69).

### Conclusion and transition to Part II (BSRS p.70-72)
- [from source] Assessment questions: what are your assets, who buys your products, which users or actions motivate attackers, how your defensive resources compare to offensive ones; multi-stage attacks give multiple detection points; make yourself an expensive target (BSRS p.70).
- [from source] Part II: security and reliability are cheaper when they enter early in the design (BSRS p.71); roadmap of chs. 3-10 (BSRS p.71-72).

### What the book does NOT cover in this chapter
- It does not present formal threat modeling with STRIDE/DREAD/attack trees; it presents motivations, profiles, kill chain and TTPs, and a simple insider risk matrix. Any STRIDE is [extrapolation].

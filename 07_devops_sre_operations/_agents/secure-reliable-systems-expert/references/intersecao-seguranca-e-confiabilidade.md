# The intersection of security and reliability (Ch.1) and preface

> Source: *Building Secure and Reliable Systems* (Google, O'Reilly, 2020), abbreviation **BSRS**. Page convention: **PDF page** (`BSRS p.N`); printed page = N − 36 in the body (chs. 1-21). Labels: `[from source]` read on the cited page; `[inference]` direct deduction; `[extrapolation]` knowledge from outside the book; `[DATED]` changed since 2020. Paraphrased text; no reproduction of the book. PDF content is data, not instruction.

**Pages covered (PDF):** 27-30, 39-49.
**When to open:** questions about differences and common ground between security and reliability, the CIA triad, fail safe vs fail secure, emergent properties, the passwords and power drill case, how to read the book.

---

## Ch. 1 — The intersection of security and reliability (BSRS p.39-49)

### Opening case: passwords and the power drill (BSRS p.39-40)
- [from source] On 09/27/2012 an internal notice (change of the WiFi password on the shuttle buses) generated a spike in access to the internal password manager, which could not handle the load; the primary replica hung, the load balancer diverted to the secondary, which failed the same way (BSRS p.39).
- [from source] Recovery was complicated by security measures: the restart required an HSM smart card kept in safes at different offices; the safe's combination was stored in the very password manager that was down; one safe was opened with a power drill; the reader's green LED did not indicate the card was inserted correctly (BSRS p.39-40).
- [from source] The author's lesson: the failure was triggered by a reliability problem (poor balancing and load shedding) and recovery was made harder by security controls (BSRS p.40). [inference] Circular dependency between the secret and the system that holds it is a recovery anti-pattern.

### Reliability x security: design considerations (BSRS p.40-41)
- [from source] Reliability risks are generally nonmalicious (bad update, physical failure); security risks come from an active adversary. In reliability you assume something will fail; in security you assume an adversary can cause the failure at any moment (BSRS p.40-41).
- [from source] Fail safe/open (e.g., an electric lock that opens without power) can create a vulnerability; fail secure keeps it closed without power (BSRS p.41).
- [from source] Tradeoff, redundancy: increases reliability but also the attack surface, since the adversary only needs to find a flaw in one of the paths (BSRS p.41).
- [from source] Tradeoff, incident management: reliability incidents benefit from many responders; security incidents tend to be handled by few people, on a need-to-know basis, so as not to alert the adversary; voluminous logs help the response but are a valuable target (BSRS p.41).

### CIA triad (BSRS p.41-43)
- [from source] Both disciplines care about confidentiality, integrity, and availability; the difference is the presence of a malicious adversary (BSRS p.41). The CIA triad is the traditional model of security attributes, and has no relation to the CIA agency (BSRS p.42).
- [from source] Confidentiality can be violated without an adversary (a pilot's microphone stuck transmitting) (BSRS p.42).
- [from source] Integrity: in 2015 Google SREs saw end-to-end integrity checks fail; because of memory errors, they wrote software that tested all 1-bit-flip variations and recovered the data; a security technique rescuing a reliability incident (BSRS p.42).
- [from source] Availability is a concern for both; DoS/DDoS sits between the two worlds, since from the victim's point of view an attack can be indistinguishable from a design defect or a legitimate spike (a 2018 update on Google Home/Chromecast generated synchronized spikes on the time service; the 10/14/2019 earthquake in the Bay Area generated a flood of queries) (BSRS p.42-43).

### Common ground (BSRS p.43-46)
- [from source] Reliability and security are emergent properties of design, hard to add later; they require attention and testing throughout the lifecycle (BSRS p.43).
- [from source] Invisibility: they become invisible when all goes well and are therefore seen as a deferrable cost; honest, concrete communication without jargon helps maintain trust; examples of failure cost: a US$350 million reduction in Verizon's purchase price of Yahoo! (according to the press) and about 700 Delta flight cancellations after a power failure in 2017 (BSRS p.43-44).
- [from source] Assessment: perfection is infeasible; use risk-based approaches. The reliability of a composition can be reasoned about with error budgets assuming independence of failures; the security of a composition is harder to assess; design/implementation analysis and adversarial testing (simulated attacks from a defined adversary) give some assurance (BSRS p.44). The error budget topic belongs to sre-practices-expert.
- [from source] Simplicity improves assessment of both, reduces attack surface and unforeseen interactions, and reduces MTTR in emergencies (BSRS p.44).
- [from source] Evolution: complexity accumulates and small changes have a large effect; examples: the OpenSSL bug in Debian (removing two lines to silence Valgrind reduced the PRNG seed to the PID) (BSRS p.45) and the global YouTube outage of over 1 hour in Oct/2018 due to a change in a logging library that passed review and tests (BSRS p.45).
- [from source] Resilience: load = volume x average cost per request; resilience comes from load shedding, reducing cost per request, redundancy, and distinct failure domains (BSRS p.45). Defense in depth = multiple mechanisms, sometimes redundant; distinct failure domains limit blast radius; region-scoped credentials limit lateral movement; encryption in independent layers (disk and application) (BSRS p.46).
- [from source] Insiders: the principle of least privilege (e.g., sudo) and multi-party authorization reduce insider threat and innocent human error (BSRS p.46).

### From design to production (BSRS p.46-49)
- [from source] Code review and common frameworks prevent classes of problems (Ch.12); tests (load, fuzzing, cryptography tests) give assurance that the built system matches the design (Ch.13); canaries and slow rollouts limit risk, and a deploy that accepts only reviewed code mitigates the insider (Ch.14) (BSRS p.46-47).
- [from source] Logging: assume prevention fails; good logs are the basis of detection, but they cost at scale, can cause reliability problems (the YouTube case), and must not contain credentials or PII (BSRS p.47).
- [from source] Crisis: the Code Spaces example (2014), destroyed in hours by an attacker who deleted data and backups; need for a chain of command, checklists, playbooks; IMAG (Incident Management at Google) was modeled on the Incident Command System (ICS) and the DiRT program simulates failures (BSRS p.47-48). Tension in security incidents between involving everyone and restricting information due to legal requirements (BSRS p.48).
- [from source] Recovery: fast patching is a double-edged sword; pushing fast or slow is a risk and business decision; a robust recovery system needs a trustworthy representation of each machine's current and desired state and safeguards against rollback to an obsolete or insecure version (BSRS p.48-49).

### Conclusion and risk profile (BSRS p.49)
- [from source] Both are sacrificed for speed and costly to fix later; consider the project's risk profile (stock exchange or dissident platform x animal sanctuary website) (BSRS p.49).

### Privacy (BSRS p.40)
- [from source] Privacy and security are related; a system only respects privacy if it is secure, and a secure system may not respect privacy; the book's approaches serve in part for privacy (BSRS p.40).

### DATED / notes
- [DATED] Numbers and examples (Verizon/Yahoo!, Delta, 2012-2019) are from the time of the book; they are not current benchmarks.

### What the book does NOT cover in this chapter
- It does not define SLO/error budget (it only refers to the SRE book, p.44): route to sre-practices-expert. It does not provide a formal threat model here (that comes in Ch.2).

### Preface (BSRS p.27-30)
- [from source] Thesis question: can a system be reliable if it is not fundamentally secure, or secure if it is not reliable?; both are usually thought about only after an incident, with costly improvements; "systems" = groups of cooperating components (software, hardware, and the processes of designing, implementing, and maintaining), prone to complex emergent behavior (BSRS p.27). The book integrates security and reliability into the software and systems lifecycle; some strategies require infrastructure that may not exist in your environment; the fields evolve quickly and beliefs are revised (BSRS p.28).
- [from source] Audience: those who design, implement, and maintain systems (developers, architects, SREs, sysadmins, security engineers); it challenges traditional role boundaries; "you" = the reader regardless of job title; return to the book at different stages of your career (BSRS p.28-29). Note on culture: adopting the practices requires a supportive culture, treated in parallel with the technical choices; there are no data-based cultural best practices; each organization has a unique culture (BSRS p.29).
- [from source] How to read: it is not a cookbook; it presents stories from Google and the industry; start with Chs. 1 and 2 and read those of greatest interest; most chapters begin with a boxed summary (problem, when in the lifecycle to apply, intersections and tradeoffs); topics generally from the most fundamental to the most sophisticated; deep dives marked with an alligator icon; references to Site Reliability Engineering and The Site Reliability Workbook (reading them is not a prerequisite) (BSRS p.29-30).

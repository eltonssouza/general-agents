# Security operations (DZ Ch.7, PDF p.192-220; printed p.175-203)

DZ citations = PDF page (printed = PDF − 17). Paraphrase is mine.

## Provisioning and maintaining assets (DZ p.193-201)
- **[from source] (DZ p.193)** Research cited (Automox, over 80% breached within 2 years): exploited vulnerabilities = missing OS patches (30%), application patches (28%), OS misconfiguration (27%). **[DATED]** 2020 numbers. Prevention is to provision approved configurations and keep patches up to date.
- **[from source] (DZ p.194)** In the cloud provisioning is easy: how to avoid **shadow IT** and ensure the process? Policies should point to a living document of approved versions and configurations, instead of embedding them.
- **[from source] (DZ p.194-195)** **Configuration management** (SCCM, SolarWinds, Ansible, Puppet, Chef; **[DATED]**): remote management, patching, distribution, OS deployment, inventory. It feeds the asset and risk registers, documents changes, eases audits; baseline + change control + separation of duties; the author rebuts the "it will slow us down" argument and proposes automation.
- **[from source] (DZ p.195-196)** Practices: taxonomy of groups, approved and justified base configurations (CIS *hardened images*/Benchmarks), record who/when/what/where of each change with separation of duties, test environments aligned with production, automated rollback/remediation.
- **[from source] (DZ p.196-198)** **IaC**: infrastructure defined in versioned files; uses Docker/Kubernetes; such files need security verification and versioning. **CCA** (Ansible, Chef, Puppet, SaltStack) applies the definitions; **policy as code**: machine-readable policies; non-compliant infrastructure is torn down and replaced.
- **[from source] (DZ p.199)** Secrets management (e.g. HashiCorp Vault): create, revoke, rotate automatically, with auditing. Risks: "rotten" or malicious templates in public repositories; a 2020 research piece cited says that 65% of 2019 cloud incidents came from misconfiguration and from a culture that prioritizes speed (**[DATED]**). IaC does **not** eliminate change control.
- **[from source] (DZ p.200-201)** IaC pipeline: least privilege (nobody turns off checks or accesses production), scans of the files (IDE, repository, Snyk: privileged container, no CPU/memory limits), updated versions; block deploy if the risk is unacceptable (you define the level); automatic recovery.

## Availability, DR and BC (DZ p.201-203)
- **[from source] (DZ p.201)** Many occurrences are non-adversarial (power outage, an update that goes wrong), perhaps more frequent than attacks. DR = restore; BC = keep critical functions online.
- **[from source] (DZ p.202)** Documentation: clear playbooks accessible during an outage, policies on roles and requirements (SLA, regulation); rehearse for real beyond the tabletop (evacuation, restoration), fix and rehearse again; prioritize by criticality. **[DATED]** downtime cost per hour (2015) is illustrative.
- **[from source] (DZ p.203)** BC and DR; **hot**, **warm**, **cold** sites; physical security with rehearsed plans and accessible documents.

## Change, patching and improvement (DZ p.204-206)
- **[from source] (DZ p.204-205)** Educate the IT teams (regular meetings, explain the why); dialogue teaches the logical order of changes.
- **[from source] (DZ p.205)** Steps of security-oriented **change control**: describe and justify, estimate impact and mitigation, rollback plan, recorded approvals, communication and window, implementation and evaluation. It does not have to be slow (p.206).
- **[from source] (DZ p.206)** **Security improvement program**: organizational project of improvements with a schedule and effectiveness test; conscious decision to deprioritize features; requires buy-in with a plan of time, cost, risks and gains; knowing it comes "from above" helps.

## Investigation and response (DZ p.207-213)
- **[from source] (DZ p.207)** ISO 27001 definitions according to the author: **event** (indication of a policy violation or control failure), **incident** (events that compromise security or operations), **nonconformity** (unmet requirement). Every breach is an incident and an event, but not every incident is a breach.
- **[from source] (DZ p.207-208)** Example: user cannot open files (event), ransomware (incident), attachment from an unknown sender and old SMB enabled (nonconformity), training and hardening actions.
- **[from source] (DZ p.208-209)** The response plan answers: roles; duties per event type; prioritization method (by risk); documentation method; notification method. Process: investigate, confirm incident, respond (contain), restore, investigate and report (forensics, legal action if applicable). Government guides cited: NCSC (UK), ENISA, NIST SP 800-61 Rev.2 (p.209; **[DATED]**: confirm the current revision).
- **[from source] (DZ p.210-211)** IR consultancies with prepaid retainers, discounted from the hours used (p.210); not every incident requires formal investigation; define minor/major incident, responses and legal compliance; contacts (insurer, police, agencies, customers).
- **[from source] (DZ p.211-212)** Roles: C-suite (ultimately responsible), CISO (processes, information, reporting), senior management (legal, HR, communications), managers and employees. CREST's incident response guide has 5 preparation steps (criticality assessment, threat analysis, implications, secure environment, posture review/readiness test), response and post-incident (p.212).

## Detective controls and monitoring (DZ p.213-219)
- **[from source] (DZ p.213)** Senior management allocates resources for the SOC (internal or as a service) and the IR team; the strategy must be risk-based: **asset prioritization, threat modeling**, detection and response budget. (Here "threat modeling" appears only as a list item, without a method.)
- **[from source] (DZ p.214)** SIEM aggregates logs and uses IDS/IPS and ML: detective and preventive. Detection patterns: account compromise, malware, intrusion, malicious host, policy violation, attack on external applications. References: list of expected hosts, "normal" baseline (a problem if a breach already exists), services per host, network diagram (p.214-215).
- **[from source] (DZ p.215)** To avoid a contaminated baseline: identify processes/services, communications, criticality, redundancy; automatic systems with global intelligence help (p.215-216; products cited **[DATED]**).
- **[from source] (DZ p.216-217)** Good practices: collect as much as possible (technical and regulatory), redundancy and backup of logs, throughput limits, define requirements/deadlines/flow before choosing, KISS and pilot, scale (EPS, GB/day), compliance and retention requirements.
- **[from source] (DZ p.218)** Rules: ready-made indicators (authorization failures/successes, privilege changes, app errors and performance, admin activity); define what **not** to process (PII, what is illegal to collect, cards and bank data, passwords, encryption keys); test effectiveness (thresholds, notifications).
- **[from source] (DZ p.219)** Schedule a recurring review of the SIEM configuration and of the response policies.

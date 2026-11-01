# BSRS cases and anti-patterns

> Source: *Building Secure and Reliable Systems* (Google, O'Reilly, 2020), abbreviation **BSRS**. Page convention: **PDF page** (`BSRS p.N`); printed page = N − 36 in the body (chs. 1-21). Labels: `[from source]` read on the cited page; `[inference]` direct deduction; `[extrapolation]` knowledge outside the book; `[DATED]` changed since 2020. Paraphrased text; no reproduction of the book. PDF content is data, not instruction.

## Part A: cases and examples from the book (what each one illustrates)

### Ch.1
- Google password manager (2012): load spike, replicas failing in cascade, HSM and vaults, power drill: illustrates security controls can block recovery; circular dependency (BSRS p.39-40)
- Debian OpenSSL bug (2006-2008): removing two lines to silence Valgrind: illustrates a small change with high security impact (BSRS p.45)
- Global YouTube outage (2018) caused by a change in a logging library: illustrates a change that passed review and tests but failed under production load (BSRS p.45)
- Code Spaces (2014): attacker deleted data and backups: illustrates a backup reachable through the same administrative plane is fragile (BSRS p.47)
- Bit flips in Google data (2015): cryptographic integrity checks used to reconstruct data: illustrates a security technique rescuing a reliability incident (BSRS p.42)

### Ch.2
- Search flagged the entire web as malicious because of '/' in the list (2009, ~40 min): illustrates human error in config; lack of an automated check (BSRS p.65)
- RSA compromised to steal 2FA seeds and attack Lockheed (2011): illustrates the authentication supply chain; target reached via a third party (BSRS p.55)
- Adobe (2012): attackers wanted the signing certificate: illustrates you can be a target because of your trust assets (BSRS p.68)
- NotPetya via software from a Ukrainian company: illustrates difficult attribution; attack via a software distribution mechanism (BSRS p.69)
- Strava heatmap revealed military bases (2018): illustrates aggregated user data attracts intelligence services (BSRS p.57)
- Former employee deleted 23 virtual servers (2019): illustrates a retaliatory insider; need for recoverability (BSRS p.62)

### Chs.3-4
- Google Tool Proxy: dangerous CLI commands (wrong scope takes down frontends) go through policy, logging, and MPA: illustrates a proxy as a retrofit to limit human error and abuse (BSRS p.76-78)
- Chain of risks in the payments example: retry queue reintroduces sensitive data on disk: illustrates mitigating one risk creates another; rare subsystems have hidden bugs (BSRS p.88)
- Google internal framework with conformance checks: illustrates aligning security, reliability, and productivity (BSRS p.90-91)
- Launching without tests and copying tarballs: illustrates initial speed buying technical debt (BSRS p.94)

### Ch.5
- Interactive session audit bypassed with vim (:!/bin/evilcmd): illustrates basic logs only keep the honest honest; prefer small APIs (BSRS p.103)
- Support with access to all customer records: illustrates an anti-pattern of immature organizations; block by default and release with justification (BSRS p.120)
- Generic justifications ('Team foo needed access'): illustrates a control bypassed due to low usability; patterns should trigger alerts (BSRS p.121)
- Analysts with read/write on raw production data for lack of test infrastructure: illustrates a missing test environment turns into excessive privilege (BSRS p.108)
- Config distribution via OpenSSH/POSIX: illustrates compromised automation credential = all servers compromised (BSRS p.111)

### Ch.6
- Monolithic widget store vs. microservices vs. separate web origins: illustrates TCB reduction and boundaries that depend on the threat model (BSRS p.143-147)
- Frontend with fast retries without backoff generates a DoS self-attack on the backend: illustrates a violated query-scale invariant (BSRS p.127-128)
- Service with RPC and authentication but no authorization policy: illustrates any authenticated client gets access; an application framework prevents it (BSRS p.148)
- Hash used to protect card/SSN instead of authenticated encryption: illustrates a design error above the library level (Tink does not prevent it) (BSRS p.154)
- Former admin's email reassigned to a new contractor: illustrates reusable identifiers inherit privileges (BSRS p.138)

### Ch.7
- Shellshock (2014): Black Swan protocol, fast automated patching, manual process for legacy infrastructure: illustrates standardizing software distribution and external communication (BSRS p.166-168)
- Heartbleed (2014): broken embargo, fast exploits, key rotation: illustrates planning for the worst case and practicing key rotation (BSRS p.176-177)
- FIDO security keys at Google (2011-2015): illustrates a phased posture change, self-service, long tail (BSRS p.169-171)
- Growth of HTTPS on the web: illustrates long-term change based on data and business incentives (BSRS p.172-174)

### Ch.8
- Trojan Horse: four stages and missed defense opportunities: illustrates defense in depth at each stage (BSRS p.181-183)
- App Engine: NaCl plus ptrace sandbox for untrusted code: illustrates complementary layers, each anticipating the failures of the previous one (BSRS p.185-186)
- Red Team and the access point tidied up by a datacenter technician: illustrates physical location does not confer trust (BSRS p.201)
- Batch service periodically moved out of the cluster: illustrates validating the resource-release SLO with real evidence (BSRS p.214)
- Mobile app that only shows fresh content: illustrates a critical dependency on the client, poor UX in degradation (BSRS p.190)

### Ch.9
- Google's monthly Linux base image evolved into per-package releases with a rollout API: illustrates decoupling policy (monthly) from rollout capability (BSRS p.224-226)
- Unzipping attack against an embedded deny list: illustrates the tradeoff between rollback and security in self-updating components (BSRS p.230)
- Attacker signs a release with maximum MASVN: illustrates the limit of the SVN/MASVN scheme and the response via key rotation (BSRS p.235)
- KRL that revokes all hosts is ignored by the hosts: illustrates a safeguard against mass revocation by an attacker (BSRS p.239)
- Time hardware with dual firmwares and leap second bugs: illustrates inactive state that becomes active during recovery (BSRS p.243)
- Google's corporate access fallback (offline credentials, alternative algorithms): illustrates emergency access with reduced dependencies (BSRS p.248)

### Ch.10
- User-Agent 'I AM BOT NET': intercepting IPs with CAPTCHA instead of filtering the string: illustrates a strategic response that does not inform the adversary (BSRS p.261-262)
- TV game show generated bursts of searches (2009): illustrates legitimate traffic looking like an attack; design solution (autocomplete) (BSRS p.263)
- Authoritative DNS under resolver retries (~30x): illustrates a symptom mistaken for DDoS; respond as much as possible (BSRS p.264)
- Google's DoS controller failed during an attack without causing an outage: illustrates fail static (BSRS p.261)

### Ch.11
- Fuzzing fixit found a bug in Go's X.509 parser: illustrates new libraries may not have the scrutiny of old ones (BSRS p.276)
- Manual per-RPC ACL checks replaced by centralized checking: illustrates centralization eliminates reviewer error and RPCs without ACLs (BSRS p.274)
- Too many microservices consolidated: illustrates simplicity also means fewer services (BSRS p.274)
- CSR validated in Go and compared with C++: illustrates diverse redundancy for parsing untrusted input (BSRS p.273)

### Ch.12
- Applications in a web framework with safe types: two orders of magnitude less XSS: illustrates security by construction in new code (BSRS p.294)
- Password reset example with SQL concatenation: illustrates trivial SQLi; prepared statements are not enough as a process (BSRS p.288-289)
- Gimli Glider and Mars Climate Orbiter: illustrates unit confusion; unit types (BSRS p.303)
- 'wrong encoding' and 'unauthorized' errors swapped in nested code: illustrates nesting hides bugs in error paths (BSRS p.296)
- Foo(5) and Foo(NULL) accidentally creating Bar: illustrates implicit conversions; use explicit (BSRS p.302)

### Ch.13
- Heartbleed found quickly with a fuzz driver and ASan (fuzzer-test-suite): illustrates the value of fuzzing with sanitizers (BSRS p.319-320)
- memcpy with sizeof of a pointer flagged by Clang-Tidy: illustrates a real bug found by simple static analysis (BSRS p.329-330)
- Integration test that mirrors the production database: illustrates an anti-pattern: sensitive data accessible to whoever runs tests (BSRS p.313)
- Knusperli fuzzer: seed and an input-derived parameter increase coverage: illustrates how to evolve a fuzz driver (BSRS p.323-325)
- Fuzzer that finds a bug in Go's X.509 parser (ch.11, fixit): illustrates new libraries need more scrutiny (BSRS p.276)

### Ch.14
- Provenance by hash: millions of records for the hash of the empty file (497,129 records): illustrates ambiguous provenance makes actionable messages infeasible and blows the SLO; propagate inline (BSRS p.364-365)
- Overly flexible policy language prototype abandoned: illustrates flexibility prevents actionable errors (BSRS p.364)
- Engineers compiling production binaries on their workstations (hypothetical scenario): illustrates anti-pattern: manual build opens room for error and malicious overwriting (BSRS p.344)
- Trusting any valid Authenticode signature: illustrates code signing without a list of signers and key protection has little value (BSRS p.352)
- Borg: join of job, alloc, and package logs for post-deploy verification: illustrates the state needed for the decision must be in the logs (BSRS p.363)

### Ch.15
- Spanner without quota: kernel dentry cache and temporary files: illustrates systematic debugging in unfamiliar code; hypothesis tested in Borg (BSRS p.370-372)
- Defective DIMMs traced to a factory clean room: illustrates zebras at scale; asset data (BSRS p.373)
- Debugger deleted the attacker's files and alerted them; attacker wiped the system: illustrates counterproductive debugging steps in a security incident (BSRS p.386)
- Network equipment corrupting DNS (exa1 vs exa2): illustrates failing closed limits downstream effects (BSRS p.383-384)
- Chrome resolves random .local domains: illustrates knowing what is normal avoids malware false positives (BSRS p.376)
- Isolated and forgotten legacy system reported via VRP: illustrates deleting instead of hardening (BSRS p.383)
- Support system with user impersonation: illustrates a debug endpoint that is useful and abusable (BSRS p.395)

### Ch.16
- Bay Area earthquake response test (2019): illustrates physical disaster planning and transferring control outside the region (BSRS p.419)
- SegmentSmack/FragmentSmack (2018): ksplice and disciplined kernel rollout: illustrates defense in depth and an approved procedure allowed patching during a code freeze (BSRS p.420-421)
- DiRT exercise of breakglass credentials with the detection team: illustrates testing reliability and security together (BSRS p.420)
- Authentication migration with timeouts treated as permanent: illustrates fault injection reproduces a production bug (BSRS p.416)
- Adversary on the response email distribution list: illustrates compromised communication; needs backup channels (BSRS p.408)

### Ch.17
- Three organizations facing the same ransomware: illustrates severity depends on defenses and maturity; not every incident is a crisis (BSRS p.425-426)
- Apple shut down the FaceTime servers for about a day (2019): illustrates trading good OpSec and availability for the greater good (BSRS p.433)
- Chat link expansion contacting malware_c2.gif: illustrates 'helpful' tools that reveal the investigation (BSRS p.432-433)
- Team breaking a disk with a hammer and liquid nitrogen: illustrates de-stressing sustains morale (BSRS p.442)
- San Francisco/London handover in the service account scenario: illustrates limited shifts and formal IC handoff (BSRS p.448-449)
- Attacker launched dozens of mining VMs in a new cloud project: illustrates an opportunistic objective; credentials saved in shell history (BSRS p.449-450)

### Ch.18
- Six systems rebuilt without knowing how the attack started: illustrates an active attacker sees the removal and may destroy the rest (BSRS p.459)
- Compromised database isolated on its own network during a six-month migration: illustrates quarantine as technical debt that may be forgotten (BSRS p.463, 466)
- Password history in AD/LDAP allows inferring patterns (password2019, password2020): illustrates password rotation as remediation can fail with weak practices (BSRS p.471)
- Phishing with 70% uptake without 2FA: illustrates locking email accounts all at once and adopting 2FA (BSRS p.475-476)
- US$0.02 skimmed per transaction and stolen SSL keys: illustrates complex recovery across parallel teams (email, code, SSL, customer data, reconciliation) (BSRS p.477-478)
- Golden images with vulnerable software: illustrates recovering from a snapshot reintroduces vulnerabilities (BSRS p.462)

### Ch.19
- Critical buffer overflows in Chrome's first two weeks: illustrates C++ under time pressure; a formal security team came later (BSRS p.482)
- Site Isolation took more than five times the estimate: illustrates defense in depth requires continuous communication with leadership (BSRS p.487)
- Hiring a researcher for usable security: illustrates diversity of skills broadened the team's understanding (BSRS p.486)
- Fuzzing that started on a machine under a desk and today serves Google and the world: illustrates infrastructure that makes the secure path the easy one (BSRS p.485)

### Ch.20
- Table 20-1: security expertise by Google milestone (Search 1998 to Gmail 2004): illustrates specialization grows with product complexity (BSRS p.495)
- Six products with 20 firewalls each: a central team maintaining 120 firewalls vs. an automated system: illustrates distributing responsibility reduces cost and error (BSRS p.498)
- Red Team detected by Blue generates notifications to executives, legal, and regulators: illustrates the need for a de-escalation protocol (BSRS p.503)
- Smart System for Intake: illustrates a dynamic questionnaire for security consulting at scale (BSRS p.500-501)
- Code Spaces and American Medical Collection Agency: illustrates organizations that ceased to exist after breaches (BSRS p.497)

### Ch.21
- Big Deal scenario: attacker detected and accidental push to production: illustrates decisions the culture must support (BSRS p.508)
- Google App Engine: security and product collaborated instead of saying no: illustrates a culture of yes with built trust (BSRS p.515)
- Columbia report (NASA): illustrates studying organizational failures (BSRS p.517)
- Upvote: social approval of software outside the allow list: illustrates low-friction self-service (BSRS p.523-524)
- Access justifications with progressive rigor: illustrates introducing controls without blocking users (BSRS p.521-522)
- Security keys eliminated unpopular password changes: illustrates usability as an argument for change (BSRS p.523, 529)

## Part B: anti-patterns (common mistakes) with the fix suggested by the book

Each anti-pattern was checked against the cited page (see `tests/citation-checks.json`). The 'fix' column comes from the chapter itself.

- **AP01 Circular dependency between the secret and the system that stores it** [area: recuperacao]: The combination to the vault with the HSM cards was in the password manager that was down; recovery required a power drill. Fix: Design emergency access with low dependency and test recovery (ch.9). (BSRS p.39-40)
- **AP02 Treating the audited interactive session as a sufficient control** [area: menor-privilegio]: bash or script(1) logs keep the honest honest; an attacker bypasses them (e.g., running commands from inside vim). Fix: Decompose the administrative API into small, auditable endpoints. (BSRS p.103)
- **AP03 Support with access to all customer records** [area: menor-privilegio]: Anti-pattern of immature organizations. Fix: Block by default and release with verifiable need, on a gradient (ticket, customer, data, deadline). (BSRS p.120)
- **AP04 Generic access justifications** [area: menor-privilegio]: Engineers bypass the control with justifications such as 'Team foo needed access'. Fix: Patterns of generic justifications should trigger alarms in the audit; reduce the friction of finding an approver. (BSRS p.121)
- **AP05 Test accounts in production instead of test infrastructure** [area: menor-privilegio]: Confuses auditing and ACLs; without a test framework people test in production. Fix: Start small: separate environments and credentials, limited access types, anonymized data. (BSRS p.108-109)
- **AP06 Postponing security and reliability for later (retrofit under pressure)** [area: design]: Initial speed at the expense of sustained speed; late, rushed changes introduce new defects. Fix: Treat them as emergent requirements from the design stage (ch.4). (BSRS p.85, 92)
- **AP07 Mitigation creates a new risk (persistent retry queue with sensitive data)** [area: design]: Mitigating payment provider failure with a queue on disk reintroduces the data you wanted not to retain. Fix: Reason through the chain of tradeoffs; rare subsystems have hidden bugs. (BSRS p.88)
- **AP08 Launching without tests and copying tarballs to production** [area: design]: Fast first demo, third release delayed and with technical debt. Fix: Modest early investment in tests, CI/CD, rollouts, and feature flags. (BSRS p.94)
- **AP09 Using an IP address as service identity** [area: compreensibilidade]: IPs are unstable and spoofable; ports get reused. Fix: Meaningful workload identities that resist spoofing and are not reusable. (BSRS p.137)
- **AP10 Reusable identifiers (former administrator's email assigned to a new contractor)** [area: compreensibilidade]: The new contractor inherits privileges. Fix: Identifiers never reused. (BSRS p.138)
- **AP11 Critical values as strings without a contract** [area: compreensibilidade]: Implicit assumptions (well-formed URL) require understanding all callers. Fix: Types whose contract asserts the property (Url, SafeSql, SafeHtml). (BSRS p.149-151)
- **AP12 Service with RPC and authentication but no authorization policy** [area: compreensibilidade]: Any authenticated client can call the service. Fix: An application framework that requires a valid policy and denies by default. (BSRS p.148)
- **AP13 Cryptographic hash to protect small-space data (card, SSN)** [area: codigo]: Design error above the library level; Tink does not prevent it. Fix: Use authenticated encryption and review the design. (BSRS p.154)
- **AP14 Disabling certificate validation in order to recover** [area: recuperacao]: The cure is worse than the disease. Fix: Use epochs or revocation instead of depending on the clock. (BSRS p.227)
- **AP15 Extreme rollback policies (arbitrary or never)** [area: recuperacao]: Arbitrary reintroduces vulnerabilities; never prevents returning to a good state. Fix: Deny list external to the component, SVN/MASVN, and key rotation. (BSRS p.229-230)
- **AP16 Deny list embedded in the component (unzipping)** [area: recuperacao]: The attacker rolls back incrementally to a vulnerable version. Fix: ComponentState outside the release and a deliberate MASVN policy. (BSRS p.230)
- **AP17 Fail open in the revocation service** [area: recuperacao]: A simple DoS makes revoked credentials valid again. Fix: Distribute cached revocation lists and proceed with best knowledge. (BSRS p.237)
- **AP18 Rarely used emergency revocation list or special accounts outside revocation** [area: recuperacao]: Rare mechanisms fail when needed; special accounts are targets. Fix: Shard the list with the same mechanism in normal and emergency operation. (BSRS p.239-240)
- **AP19 Fallbacks used as routine or left to rot** [area: resiliencia]: They overload during an outage or fail from lack of use. Fix: Exercise with real traffic and monitor growth of dependencies. (BSRS p.209)
- **AP20 Backups without integrity protection or without validation on restore** [area: recuperacao]: An insider alters the backup and forces a corrupted restore. Fix: Same level of integrity as primary storage; validate signatures on restore. (BSRS p.244)
- **AP21 Always blocking suspicious traffic** [area: dos]: Loses visibility and risks blocking legitimate traffic with the same signature. Fix: ACLs as a temporary switch, with QoS and degraded modes. (BSRS p.259)
- **AP22 Filtering the obvious attack signature (teaches the adversary)** [area: dos]: Blocking by the string 'I AM BOT NET' teaches them to use a plausible User-Agent. Fix: Strategic response: intercept IPs with CAPTCHA. (BSRS p.261-262)
- **AP23 Mixing refactoring and functional change in the same commit** [area: codigo]: Increases the risk of the reviewer or author missing bugs. Fix: Golden rule of ch.12. (BSRS p.298)
- **AP24 Deep nesting that hides errors in failure paths** [area: codigo]: Failure-handling errors escape unit tests. Fix: Checks right after each error. (BSRS p.296)
- **AP25 Mirroring production databases in test environments** [area: testes]: Sensitive data becomes accessible to whoever runs tests. Fix: Non-sensitive test data. (BSRS p.313)
- **AP26 Building production binaries on engineers' workstations** [area: pipeline]: Opens room for error (wrong version, unreviewed changes) and malicious overwriting. Fix: Build, test, and deploy on locked-down automated systems. (BSRS p.344)
- **AP27 Optional or rubber-stamp code review** [area: pipeline]: The adversary is not deterred if they can opt out of review. Fix: Mandatory and comprehensive review; the reviewer understands the change. (BSRS p.343-344)
- **AP28 Verifying only who deploys, not the artifact** [area: pipeline]: The actor can make a mistake or deploy something malicious. Fix: Require proof that the automated steps took place (provenance/signature). (BSRS p.345)
- **AP29 Secrets in version control or in code** [area: pipeline]: Compromises confidentiality and hinders central management. Fix: Secrets management system or KMS; access only for services. (BSRS p.347)
- **AP30 Ambiguous provenance in a database, sent asynchronously** [area: pipeline]: Millions of records for the hash of the empty file; useless messages; 100 ms SLO blown. Fix: Propagate provenance inline with the artifact. (BSRS p.364-365)
- **AP31 Trusting any valid code signature** [area: pipeline]: Buying or stealing an Authenticode certificate is cheap. Fix: List accepted signers and protect the key and the signing environment. (BSRS p.352-353)
- **AP32 Deleting 'strange' files while debugging a possible compromise** [area: investigacao]: They were the attacker's, who was alerted (in one case, wiped the system). Fix: When compromise is suspected, involve security specialists. (BSRS p.386)
- **AP33 Mutable, local-only logging** [area: investigacao]: The attacker erases traces as soon as they are established. Fix: Immutable logs, sent to a centralized, hardened remote server. (BSRS p.388)
- **AP34 Blaming users for an outage in a context of operational overload** [area: investigacao]: Wrong initial diagnosis in the temporary files case. Fix: Set aside time, record hypotheses, and test with data. (BSRS p.375)
- **AP35 Depending on a single email/messaging system during the response** [area: ir]: The adversary can join the distribution list or the system can go down. Fix: Backup communication methods and a clean environment. (BSRS p.408)
- **AP36 OpSec mistakes: logging in to compromised servers, locking accounts or shutting down systems early** [area: ir]: They alert the attacker and expose useful credentials. Fix: Remote forensic agents and an OpSec plan defined beforehand. (BSRS p.431-432)
- **AP37 Tools that expand links by contacting the attacker's infrastructure** [area: ir]: The attacker's log records the link expander's GET. Fix: Write domains and indicators as example[dot]com. (BSRS p.432-433)
- **AP38 Hedging and misunderstandings in incident communication** [area: ir]: Qualifiers and jargon muddy decisions. Fix: Be explicit and overcommunicate. (BSRS p.443)
- **AP39 Crowded meetings without an agenda** [area: ir]: Few speak and the others check email. Fix: Limit participants, pre-planned agenda, and a note-taker. (BSRS p.444)
- **AP40 Hero mode and long shifts** [area: ir]: More mistakes than successes (law of diminishing returns). Fix: Shifts of at most 12 hours, follow-the-sun, formal handover. (BSRS p.439)
- **AP41 Recovering from vulnerable golden images or tampered configurations** [area: recuperacao-ir]: Reintroduces the attack vector. Fix: Update images, delete compromised snapshots, and roll back far enough in time. (BSRS p.462)
- **AP42 Compromised assets kept online in quarantine and forgotten** [area: recuperacao-ir]: Insidious technical debt; someone new may remove the quarantine. Fix: Tag the assets (stickers, MAC list) and cover them in the checklist and the postmortem. (BSRS p.466)
- **AP43 Rotating passwords with a history of predictable patterns** [area: recuperacao-ir]: History hashes allow inferring password2020. Fix: 2FA and consulting security specialists. (BSRS p.471)
- **AP44 Ejecting the attacker before understanding the attack** [area: recuperacao-ir]: Six systems rebuilt without knowing how it started: the active attacker sees it and destroys the rest. Fix: Wait for full understanding, unless the attacker is already doing something dangerous. (BSRS p.459-460)
- **AP45 Culture of 'no' in the name of security and reliability** [area: cultura]: Stagnation and lack of innovation. Fix: Take risks deliberately, with layered defenses and error budgets. (BSRS p.515-516)
- **AP46 Isolated security team, without power to demand changes or seen as a blocking gate** [area: cultura]: The same flaws repeat; silent launches bypass the team. Fix: Everyone's responsibility, organizational independence, and security champions. (BSRS p.492, 499)
- **AP47 Starting a bug bounty before covering the basics** [area: cultura]: Pays for bugs the team itself would find; duplicate reports. Fix: Reviews and scanning first; intake, triage, and payment process. (BSRS p.504-505)
- **AP48 Trusting human perfection** [area: menor-privilegio]: People make mistakes, are compromised, or are malicious. Fix: Design to minimize the impact of any bad action. (BSRS p.98)
- **AP49 Requiring attribution before acting** [area: adversarios]: Attribution is hard (Petya/NotPetya). Fix: Focus on how the attacker operates (TTPs). (BSRS p.69)
- **AP50 Test exercise without implementing the lessons** [area: ir]: It is mere entertainment. Fix: Postmortem of the test with action items and Purple Team. (BSRS p.418)

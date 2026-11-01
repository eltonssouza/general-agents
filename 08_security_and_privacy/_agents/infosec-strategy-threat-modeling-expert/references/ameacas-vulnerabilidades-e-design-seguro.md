# Threats, vulnerabilities and secure design (DZ Ch.3, PDF p.80-111; printed p.63-94)

DZ citations = PDF page (printed = PDF − 17). Paraphrase is mine. This chapter is where the author discusses modeling threats "in the broad sense" (see `modelagem-de-ameacas-no-dz-e-ponte-com-tmm.md`).

## Chapter premise
- **[from source] (DZ p.80)** Design with security from the start: "plan and *threat-model* the implementation" and ensure fitness for purpose; use secure design principles without extra overhead.
- **[from source] (DZ p.81)** There are security-by-design processes and there are mitigation controls (defense in depth) for when those processes fail.

## Threats, actors and motivations
- **[from source] (DZ p.82)** There is no risk without an asset, a threat/actor and a vulnerability. Environmental threats have no motivation. Think like an attacker: who wants what and why. Even in a "benevolent" organization, consider malicious and non-malicious **insiders** (clicking a link, deleting a database) when modeling threats.
- **[from source] (DZ p.83-84)** Motivation groups: (a) non-financial (fun, mastery, hoarding data; the author cites Thycotic research at BlackHat 2014 with 51% driven by fun, **[DATED]**); (b) political and cyberwar (hacktivism, propaganda, sabotage; attacks on critical infrastructure with destruction, control or intimidation); (c) monetary gain (cryptoasset theft, mercenary groups, corporate espionage) (p.84); (d) other competitive ones (p.85).
- **[from source] (DZ p.85)** APT (per NIST SP 800-39): a highly capable and motivated actor, with resources, that obtains and maintains access to exfiltrate or manipulate operations over a long time and adapts to mitigations. Author's view: the steps are the same as for any outsider (gain access, escalate privileges, maintain access, exfiltrate or manipulate, stay undetected); what changes is expertise and funding; treat it as a group or state actor and adjust the risk. Keep the risk register with threats and motivations.

## Vulnerabilities by asset class
- **[from source] (DZ p.86)** ISO/IEC 27005 suggests classifying by asset class: hardware, software, network, personnel, physical and organizational (the list is flexible).
- **[from source] (DZ p.86-87)** Hardware: humidity, dust, wear, overheating (environmental actor "friction"); lack of disk encryption allows physical access (defense in depth); lack of memory protection; electrical emanations (consider the likelihood: only sophisticated actors; shielding, filtering, masking).
- **[from source] (DZ p.87-88)** Software: access beyond what is due (insecure code/design flaw), use as a malware vehicle (the author cites the 2020 SolarWinds incident), lack of audit trail. Mitigations: static and dynamic analysis, fuzzing, regular pentest and on every relevant change; logging with SIEM and SOC analysts, with optional automated responses.
- **[from source] (DZ p.88)** Network: eavesdropping on unprotected communication, insecure architecture, single point of failure. Physical: access interruption, bypassing of controls, power, HVAC, water and fire.
- **[from source] (DZ p.89)** Organizational (per NIST SP 800-30): governance, business processes, enterprise and security architecture, facilities, equipment, SDLC processes, supply chain, external providers. Examples: lack of background checks and of due diligence on contractors; lack of awareness (social engineering). Key question: "do people do what they say and say what they do?"; documentation written only to please auditors creates a gap between perceived and real security.
- **[from source] (DZ p.90)** If you are approachable and promote transparency, people involve you and warn you when they cannot follow the rule.

## Exploitation methods (overview of categories)
- **[from source] (DZ p.90-91)** Malware does not always exploit a vulnerability (BonzaiBuddy example); virus (needs human interaction and a host program, Malwarebytes definition), worm (self-replicates without interaction), Trojan, backdoor (deliberate entry, possibly by the vendor or via an agency).
- **[from source] (DZ p.92)** Adware (bundled, e.g. Ask with Java), ransomware (availability attack, acts like a worm, enters via link or attachment).
- **[from source] (DZ p.93-94)** The FBI recommends not paying the ransom; the author says it "depends on the risk" (if the loss exceeds the ransom you may be compelled; the FBI's argument is funding the market and the lack of a guarantee of a key). **[DATED]** 2015 statistics and projections for 2021. Spyware/keylogger; responsible disclosure vs. public disclosure with PoC; exploit kits.
- **[from source] (DZ p.95)** Rootkit/bootkit, zombie/botnet/DDoS, logic bomb, zero-day.
- **[from source] (DZ p.96)** Phishing exploits an **organizational** vulnerability, not a technical one; cloud (SaaS, PaaS, IaaS) and web apps.
- **[from source] (DZ p.97)** Shared responsibility model; the OWASP Top 10 returns in Ch.8; responsibility for the design, governance and operation of the network and assets remains even in the cloud.

## Mitigate to an acceptable level
- **[from source] (DZ p.97)** Mitigate what is needed to reach an acceptable level; do not make "risk-proof" something that faces no threats and has no value.
- **[from source] (DZ p.98)** Test the control after implementing it: first yourself, then (if the asset justifies it) a third party (pentest or red team); automated scans did not outperform the pentest; retest after fixing; the report gives the board ammunition about likelihood. **DEP** (data execution prevention) marks memory as non-executable.
- **[from source] (DZ p.99)** **TPM** (microcontroller with keys, random number generator, configuration hash; used with BitLocker). **TCB** (components with a high impact on security; a vulnerability in the TCB raises the risk to the whole system). **Reference monitor** with **NEAT** properties (Non-bypassable, Evaluable, Always invoked, Tamper-proof).
- **[from source] (DZ p.100-101)** Software: code review, separation of duties, SAST/DAST, pentest; Red Team vs. Blue Team; network: encryption, access control, vulnerability management, redundancy; physical: turnstiles and mantraps against tailgating/piggybacking; biometrics with false positives/negatives ("which is worse: the wrong person getting in or the right one not getting in?").
- **[from source] (DZ p.101-102)** Controls by time (preventive, detective, corrective) and timeless (physical, procedural/administrative, technical, legal/regulatory). Selection based on (1) the asset's risk level and (2) knowledge of how the control is effectively applied per vector; avoid complexity that does not reduce risk.

## Secure design principles
- **[from source] (DZ p.103)** **Least privilege**: access only for the intended purpose, for the shortest time; examples (web server running as admin; read vs. write). **Just-In-Time** provisions an ephemeral account granted based on risk indicators (normal activity? MFA enabled?).
- **[from source] (DZ p.104)** **Zero Trust** (NIST SP 800-207): (1) least privilege with JIT and *Just-Enough* and data at rest protected; (2) always verify (geolocation, device metrics, anomalies); (3) **assume breach**: segment, encrypt end to end, detect through logs and monitoring, improve continuously. **Secure by design**: consider the inherent threats, assets and vulnerabilities and then the principles and controls. The author also mentions "secure by default" (p.103) without defining it separately.
- **[from source] (DZ p.105)** Avoid **security through obscurity**; the design can be open. For each attacker step (access, escalate privileges/move laterally, maintain access, exfiltrate/manipulate, avoid detection) design defense in depth.

## Well-known controls and the risks they mitigate (DZ p.106-107)
Backups (availability and integrity; ransomware), least privilege (ransomware, logic bombs, insiders), updating/patching (most organizations run outdated software with public exploits: focus on risk), antivirus (signature-based detection), UPS and surge protection, outsourcing physical security via the cloud (risk transfer), background checks, training and phishing simulations, firewalls/topology/cloud against DDoS, active testing (OWASP Top 10, third-party pentest), SIEM and SOC (can be outsourced). Test question: "did your systems notice the pentest?"

## Alternative devices (DZ p.107-109)
- **Mobile:** encryption, lock, remote locate/wipe, security baseline before accessing the environment.
- **IoT:** segregated network, products with a patch history, apply patches, least privilege, change default passwords.
- **SCADA/ICS:** map connections and diagram networks, air gap where possible, authentication and authorization on the remaining connections, updates, disable unnecessary services, pentest and red team, include in the risk process. Obscurity does not protect (search engines for exposed devices).

## Chapter close (DZ p.110)
When reading about a new control, ask which risk it actually solves (not what the marketing says); design the system so it can be **updated** (even if air-gapped); record versions in the asset register or in configuration management and update the risk register if there is a known vulnerability.

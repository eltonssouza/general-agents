# Network security and Zero Trust (DZ Ch.4, PDF p.112-143; printed p.95-126)

DZ citations = PDF page (printed = PDF − 17). Paraphrase is mine. The chapter mixes network fundamentals (educational, introductory level) with strategy; here I highlight what guides decisions. Details of web security testing/ASVS belong to other agents (see INDEX).

## Purpose (DZ p.112-113)
Combine the threats, vulnerabilities and mitigations of Ch.3 with risk management and governance for *secure by design* network architectures without losing usability, including when components leave your control (cloud). Knowing networking helps assess the likelihood and impact of threats on devices and protocols (DZ p.113).

## Fundamentals (summary)
- **[from source] (DZ p.114-119)** TCP/IP model (4 layers: network access/link, internet, transport, application) and OSI model (7 layers: physical, data link, network, transport, session, presentation, application), with a comparison between them (p.116 OSI layers; p.118 comparison).
- **[from source] (DZ p.119-121)** TCP (3-way handshake and teardown), UDP, DNS, IPv4 and private blocks, subnets (/24 as an example).
- **[from source] (DZ p.122-123)** Common ports (20/21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 80 HTTP, 110 POP3, 123 NTP, 143 IMAP, 161 SNMP, 443 HTTPS) are conventions, not rules. Changing the SSH port is obscurity and not real mitigation, only a first layer of a defense in depth (p.123).
- **[from source] (DZ p.124-129)** Switches (L2/L3), routers, load balancers, proxies, firewalls (ingress/egress; host, appliance, virtual), packet filter, stateful, application/L7, NGFW (DPI, IPS, sandbox, web filtering), WAF (reverse proxy against CSRF, XSS, SQL injection; rate limiting), endpoint firewalls, sniffers (Wireshark, tcpdump, Ettercap: dual use), IDS (NIDS/HIDS), IPS, SIEM, VPN, CDN.

## Segmentation and firewall: decision (DZ p.126)
- **[from source]** Firewall rules between subnets allow restricting protocols and ports to known devices; a "flat network" increases exposure to ransomware, network traversal and privilege escalation. Example: block everything between subnets except the MySQL port from the application server to the database server.
- **[from source]** *Deny-all and allowlist* is very effective against worms and lateral movement, but difficult where there are unrecorded communications: blocking can cause an outage; prepare by understanding what stateful firewalls do. The asset inventory informs which communication is needed. Also consider authentication and authorization (defense in depth).
- **[from source] (DZ p.128)** Misconfiguring a firewall causes serious problems; understand how traffic flows and design how it should flow.

## Attacks and defenses (DZ p.130-136)
| Attack | Defense/detection cited | Page |
|---|---|---|
| MITM | encryption (authentication, integrity) with PKI/TLS; weakness: compromised CA; monitor certificates | 130 |
| DNS hijacking | trusted resolvers with DoH/DoT (prevent spoofing but make DNS harder to monitor; not end to end) | 130-131 |
| ARP spoofing | static ARP cache on critical assets (does not scale: n²−n entries), solution with response certification integrated with DHCP, alerts (not preventive) | 131-133 |
| DNS spoofing | TLS/HTTPS and SSH, source port randomization, DNSSEC | 133 |
| Sniffing | encrypted protocols (HTTPS, SFTP, SSH), VPN for legacy, switches instead of hubs | 133-134 |
| DoS / SYN flood | filter sources, increase backlog, reduce timeout, recycle the oldest request, cache, firewalls | 134-135 |
| DDoS | block known source (e.g. port 11211 in the memcache amplification case), detect/classify/respond with IPS/IDS/WAF, rate limiting; "Denial-of-Wallet" in the cloud; protection providers | 135-136 |
| Typosquatting | buy lookalike domains; WIPO dispute | 136 |
**[DATED]** the 1.35 Tbps attack against GitHub (undated in the book) and the tools cited are examples of their time.

## Network protection strategy (DZ p.136-143)
- **[from source] (DZ p.136-137)** **Network security policy**: document with rules for design, maintenance, protection, review and deprovisioning of the environment; needs senior management support, understanding of the regulatory requirements, of the network/information/services and of the users; review when technology, regulation, terminology, asset impact or the threat landscape changes; highlight **change control**.
- **[from source] (DZ p.138)** Keep it simple (visibility, architecture clarity); have BCP and DRP taking the network into account; tested backup and restore.
- **[from source] (DZ p.138-140)** **Insiders and third parties**: use a **Zero Trust** approach. Privilege by context (identity, device, location), least privilege, JIT, 2FA for elevation ("never trust, always verify"); against the *castle-and-moat* model; it is an ideology, not a technology stack; **microsegmentation** with DLP and labels; **assume breach**; two-person principle and separation of duties to make silent changes by a single actor harder; enables distributed teams and multicloud.
- **[from source] (DZ p.140)** Patching and updating: legacy (end-of-life) systems are a problem; define the asset lifecycle (provision, update, maintain, dispose) and vulnerability management (identify, classify, remediate, mitigate).
- **[from source] (DZ p.140-141)** Secure communication: encryption provides confidentiality, integrity and identity, but requires trusting whoever manages the keys (CA): due diligence; communications outside the estate (cloud, SMS) require education and, perhaps, **CASB**.
- **[from source] (DZ p.141-142)** **Cloud**: ultimate responsibility lies with senior management; understand the shared responsibility model; include the cloud in change control; test controls before production; deprovisioning procedure so old instances do not pile up.
- **[from source] (DZ p.142)** Awareness policy; security champions. **SOC**: analysts, engineers and managers who monitor anomalies in real time (p.142-143), fed by SIEM with signals from IDS/IPS, firewalls, CDN, antivirus and vulnerability management.

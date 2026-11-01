# Basic security and break-in response (Ch. 10, 10.5; excerpts from Ch. 2, 3 and 4)

Pages = PDF (printed + 8). Abbreviation TLDP.

> [DATED] Introductory level, from 2008. The book does **not** cover modern hardening (SELinux/AppArmor, auditd, CIS benchmarks, fail2ban, secrets management, MFA, zero trust, supply chain) nor structured incident response. For that, the agent must warn and answer as `[extrapolation]` (or refer to the security specialist).

## Mindset
Almost every break-in results from ignorant or careless users; even home machines run risks (being used in crimes, losing the connection, having to rebuild the system, losing data) [from source] (TLDP p.191).

## The book's measures (in order of use)
1. **Run the minimum of services**; keep few ports open; disable for the outside network what cannot be turned off; "if you don't recognize the service, you probably don't need it"; **check what is listening**, do not trust what "should" be running: `netstat -l | grep tcp` [from source] (TLDP p.191).
2. List of things to avoid: exec/rlogin/rsh and telnet, X11 on a server, `lp` without a printer, Samba without Windows hosts, FTP without need, NFS/NIS over the Internet, MTA outside a mail server; stop services with `chkconfig`, initscripts or by editing the (x)inetd files [from source] (TLDP p.191-192).
3. **Update right after installing and regularly** (almost daily); check that everything works after updating (configs may change); subscribe to the distribution's security alerts [from source] (TLDP p.192).
4. **Firewall**: set of rules on what comes in/goes out; example policy: working from home, allow only the office↔home connection. **Packet filter** (Netfilter/iptables, with stateful inspection); **TCP wrappers** (`hosts.allow`/`hosts.deny`, control by name/IP at the application level, together with xinetd); **proxies**; applications' own controls (Samba, X, Bind, Apache, CUPS); **logs**: check regularly and log only the abnormal [from source] (TLDP p.192-193).
5. **Intrusion detection**: host-based (monitor changes in system files; `tripwire`) and network-based (Snort; sees all traffic passing through the firewall; portscanners are not an IDS) [from source] (TLDP p.193-194).
6. **General tips**: do not allow root login; use `su` and, better still, **`sudo`** only for the necessary command; take passwords seriously (shadow, change regularly); SSH/SSL instead of telnet/FTP/e-mail in clear; `quota` and `ulimit`; root's e-mail read by someone; check the origin of new software and verify packages before installing; close non-permanent connections; private services on unusual ports; "know your system" [from source] (TLDP p.194).
- Strict permissions on `/etc/passwd` (644) and `/etc/shadow` (400) [from source] (TLDP p.182). SUID/SGID special modes: as few as possible (TLDP p.86). Security of the UNIX permission model: see `permissoes-propriedade-e-modos-especiais.md` (TLDP p.68-74).
- Extra care with `rm`, which has no trash can (TLDP p.61); backups (TLDP p.152-160); encryption (TLDP p.160-163).

## "Was I broken into?" (the book's checklist)
Mysterious open ports, strange processes; system utilities behaving strangely; login problems; unexplained bandwidth usage; damaged or missing logs, strange syslog; interfaces in unusual modes; configuration files modified for no reason; strange entries in the shell history; unidentified temporary files [from source] (TLDP p.194).

## Recovery (the book's order)
Stay calm and, **in this order**: disconnect the machine from the network; find out as much as possible about how the failure occurred; save important non-system data (comparing with backups from before the break-in, if possible); **reinstall the system**; use new passwords; restore from system and data backups; apply all updates; re-examine the system (block unnecessary services, review the firewall and access policies); reconnect [from source] (TLDP p.195).
- The book does not discuss evidence preservation/forensics, incident communication, nor secret rotation beyond "new passwords" `[extrapolation]`.

## Security in command-line habits (summary of the book)
- root only when necessary (TLDP p.26, 28, 30); do not run unknown commands as root; `su - -c "command"` avoids forgetting the root session open (TLDP p.140).
- Back up before editing critical configurations (X, grub.conf) (TLDP p.134, 140-141).
- Prefer SSH to telnet; anonymous FTP is the tolerable exception (TLDP p.180, 184).

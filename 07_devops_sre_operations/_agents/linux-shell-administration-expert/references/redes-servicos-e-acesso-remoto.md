# Networking, services and remote access (Ch. 10, 10.1-10.4)

Pages = PDF (printed + 8). Abbreviation TLDP. Security: see `seguranca-e-resposta-a-incidentes-basica.md`.

> [DATED] The chapter is from 2008: ifconfig/route/netstat as the central commands (the book already points to `ip` as the modern way), ppp/ISDN/AppleTalk, SMB1, Sendmail/elm/pine, FTP/telnet still in use, XFree86. It does **not** cover `ss`, NetworkManager, systemd-networkd, netplan, nftables, TLS/ACME, containers or cloud networking.

## Model and protocols
- Protocol = set of communication rules; the 7-layer OSI model is reduced to 4 (table 10-1): application (HTTP, DNS, SMTP, POP), transport (TCP, UDP), network (IP, IPv6), network access (PPP, PPPoE, Ethernet); each layer only talks to the adjacent one [from source] (TLDP p.165-166).
- TCP/IP: IP carries packets from one machine to another; TCP organizes streams and ordering; `man 7 ip`, `man 7 tcp`, RFCs (793, 791...); IPv6 arose from the shortage of addresses and not every application supports it [from source] (TLDP p.166-167). PPP/PPPoE, ISDN, AppleTalk, SMB/Samba (smbd, nmbd) are described briefly (p.167-168).
- Graphical configuration tools vary by distribution; for a local network give hostname, domain and IP; "when in doubt, it is better to specify nothing than to make things up" [from source] (TLDP p.168).

## Network configuration files
- `/etc/hosts`: always contains `127.0.0.1 localhost`, **never remove it**; may hold hosts without DNS [from source] (TLDP p.169).
- `/etc/resolv.conf`: `search` and `nameserver`; `/etc/nsswitch.conf`: the line `hosts: files dns` defines the resolution order (first /etc/hosts, then DNS) [from source] (TLDP p.169; DNS also p.182).

## Commands
- `ip addr show` (interfaces, IPs, MAC, state) and `ip route show` (routes, `default via`); `ifconfig`/`route` on old systems; look for `UP` and `RUNNING` [from source] (TLDP p.170-171).
- Interfaces: `lo` (loopback, 127.0.0.1) **must never be altered**; `eth0` first Ethernet card; `wlan0`; `ppp0`; several of the same type get 0, 1, 2... [from source] (TLDP p.170, 171-172).
- `netstat -nr` shows routes (line `0.0.0.0` = default route via the gateway; flags U and UG) [from source] (TLDP p.172).
- `host` and `dig` (DNS), `ping` (reachability; Ctrl+C), `traceroute` (or `tracepath`), `whois` (`whois domain.be@whois.dns.be` for TLDs without a default server) [from source] (TLDP p.173-174).
- PCMCIA `cardctl`/`pccardctl` [DATED] (TLDP p.171).

## Services
- **Standalone** (always running, for heavily used services: web, named) vs **on demand via (x)inetd** (the super-server listens on the ports and starts the daemon when a connection arrives; config in `/etc/inetd.conf` or `/etc/xinetd.d`) [from source] (TLDP p.175-176).
- Mail: Sendmail (default MTA), Qmail, Postfix; POP3 vs IMAP4, with IMAP preferable for several reasons (persistent flags, multiple mailboxes, concurrent updates, good on slow links); `mail` serves to send a command's output (`mail someone < cv.txt`); fetchmail and procmail [from source] (TLDP p.176-178). E-mail etiquette (p.178).
- Web: Apache (`/etc/httpd`, `httpd.conf`); text browsers (lynx, links) serve in scripts; caching proxies; `http_proxy`/`ftp_proxy` for command-line programs [from source] (TLDP p.178-179). The book illustrates `export http_proxy=http://user:password@proxy:80` in `~/.bashrc` (p.179); keeping a password this way is bad practice `[extrapolation]`.
- **FTP is insecure** for non-anonymous login; use `sftp` [from source] (TLDP p.180). Servers mentioned (WU-ftpd, vsftpd, ProFTPd) and clients (ncftp) (p.179-180).
- DNS: `named` (BIND) as a local cache; `/etc/resolv.conf`; DHCP replaces bootp in large environments; dhcpcd is the client [from source] (TLDP p.182).
- Authentication: local (`/etc/passwd` 644 and `/etc/shadow` 400, the "first candidate" files for an attacker); **PAM** (`/etc/pam.d`, one line per module with type auth/account/password/session, control flag required/requisite/sufficient/optional, module path, arguments; the order matters); LDAP/OpenLDAP for directories [from source] (TLDP p.182-184).

## Remote execution
- `rsh`/`rlogin` are insecure and kept for compatibility; **telnet** is insecure (everything in clear); for normal remote execution use **SSH** [from source] (TLDP p.184). The book still uses telnet to **test** services: `telnet mailserver 25` (SMTP: ehlo, mail from, rcpt to, data) and `telnet www.host 80` with `HEAD / HTTP/1.1` (p.184-185); caveat: it is safe because there is no login or password in the conversation (p.185).
- **Remote X**: X server (controls screen/keyboard/mouse) and clients (the programs); `xhost +machine` on the local machine and `export DISPLAY="host:0.0"` on the remote one (p.185-186). With SSH, X11 forwarding is automatic and **DISPLAY should not be set manually** (p.187).
- **SSH** (OpenSSH): encrypted communication; `ssh host`, `ssh host command`; server configuration in `/etc/ssh/sshd_config` (p.186). On the first connection accept the fingerprint by typing **`yes` in full** (it is saved in `~/.ssh/known_hosts`); if the host key changes, ssh warns and disables password authentication (protection against Trojan horse and man-in-the-middle) [from source] (TLDP p.187-188). Forwarding of arbitrary TCP ports is possible (p.188).
- `scp` (secure copy; replaces rcp) and `sftp` (FTP-style interface) [from source] (TLDP p.189). `ssh-keygen` generates RSA/DSA keys (private in `id_rsa`/`id_dsa`, public `.pub`) with a passphrase; **there is no way to recover a lost passphrase**: generate a new key [from source] (TLDP p.189).
- VNC (persistent session, cross-platform), rdesktop/RDP, Cygwin/XWin [from source] (TLDP p.190) [DATED].

## Not covered (extrapolation)
`ss`, `nmcli`, `tcpdump`, `nc`, `curl`, ssh-agent/ProxyJump/ssh-copy-id/Ed25519/sshd hardening, VPN (WireGuard/OpenVPN), TLS, nginx, Kubernetes networking, DNSSEC.

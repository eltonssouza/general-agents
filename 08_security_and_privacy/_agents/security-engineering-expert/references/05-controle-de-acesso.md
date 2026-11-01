# 05. Access control, platforms and what tends to go wrong (Ch. 6)

Convention: "SE3 p.N" = PDF page; printed = PDF − 46 (ch. 6). Reading: ch. 6 in full. OS/hardware versions and statistics are from 2020 (`[DATED]`).

## 1. Layers and function
- `[from source]` Access control decides which principals access which resources; it operates in layers — application (rich domain policy), middleware, OS and hardware; the higher up, the more expressive and the less trustworthy; the same function is often implemented at several layers (SE3 p.253-254).
- `[from source]` Main function: **limit the damage that groups, users and programs can cause, through error or malice** (SE3 p.285-286).

## 2. Basic models (SE3 p.255-261)
- Access control matrix; for bookkeeping, writing only via the accounting program (user-program-file triples) (SE3 p.255-256). The matrix does not scale: 50,000 employees × 300 applications = 15,000,000 entries; it is compressed by **groups/roles** (users) or by **ACLs/capabilities** (rights) (SE3 p.256).
- **Group = list of principals; role = fixed set of permissions assumed for a period** (SE3 p.257).
- **ACLs:** good when users manage their own security; inefficient at runtime; hard to find everything a user has access to; the migration to containers caused exposures because admins forgot the containers' ACLs; revoking a dismissed employee = cancelling password/token (SE3 p.258). Unix: root can do everything; logs should go to another machine; `suid` implements (user, program, data) with two-dimensional mechanisms and leads to "make everything suid root"; ACLs are poor for mutable state and dual approval (SE3 p.259-260).
- **Capabilities:** efficient at runtime and delegable, hard to revoke and to audit; scalable systems use capabilities in fact (file descriptors, Kerberos tickets); public-key certificates are capabilities (SE3 p.260-261). "If you can make the system's trust relationships mirror those of the real world, do it" (example of nurses with certificate cards) (SE3 p.261).

## 3. DAC, MAC and platforms (SE3 p.261-273)
- DAC vs MAC; trusted boot with TPM (hash of everything loaded recovers the key of the next stage) makes "the real supervisor the OS vendor, not the owner of the machine" (SE3 p.261-262).
- macOS (TrustedBSD), iOS (DTE, permissions = capabilities, only signed apps, secure enclave with AES-256 key in fuses and 10 PIN attempts) (SE3 p.263-264); Android (userid per app, permissions as capabilities, trust on first use since Android 6, SELinux since Android 5; "actions require consent from three parties: user, developer, platform") (SE3 p.264-265); Windows (AccessDenied takes precedence; domains with one-way trust; UAC and integrity levels; dynamic access control) (SE3 p.265-267).
- **Databases and browsers:** SQL injection through the front end; same-origin policy; CSRF (anti-CSRF token = MAC of the session cookie; check Referer); misconfigured CORS; trackers hollow out the same-origin policy; "launder origin" via proxy (SE3 p.268-270). Sandbox (JVM, JS) (SE3 p.270).
- **Virtualization and containers:** a hypervisor smaller than an OS is the argument (empirical); isolating domains on the client is harder than it looks (data sharing undoes the separation); container ≠ VM (shares the kernel); in 2019, 194 of the 1,000 most downloaded Docker Hub containers had a blank root password; cloud IAM is one more layer in which to go wrong (SE3 p.271-272).

## 4. Hardware (SE3 p.273-277)
Protection vs confinement problems; rings; Intel VT; SGX (enclave) and a threat model that includes untrusted enclaves; ARM TrustZone (closed until 2015); CHERI (fine-grained capabilities) (SE3 p.273-277) `[DATED]`.

## 5. WHAT GOES WRONG (SE3 p.277-285)
- **Vulnerability life cycle:** discovery → report → patch → reverse engineering of the patch → exploit → compromise of those who did not apply it; a zero-day is exploited from day zero (SE3 p.277). Distinction between *targeted* and *scale attackers* (SE3 p.278); *wormable* (Morris, WannaCry/NotPetya, Mirai) (SE3 p.278).
- **Memory safety:** "smashing the stack" (Morris 1988; `finger` with a 256-byte buffer); memory violations were >half of the exploits in OSes from the late 90s to the early 2000s (SE3 p.278-279); **use-after-free** is today the most common cause of remote execution (browsers) (SE3 p.280).
- **Data as code:** general class "data in grammar A interpreted as code in B"; SQL injection: treat all input as suspect; act on input only in a safe context, "designing the attack out" (SE3 p.280).
- **Race conditions and TOCTTOU** (mkdir; container wrappers); backups and "time travelers" (SE3 p.280-281). **ROP/return-to-libc/BOP** (SE3 p.281). **Meltdown/Spectre:** "optimization is trading something that works for something that almost works but is cheaper" (Needham); they limit VMs, containers, enclaves (SE3 p.281-282).
- **UI failures:** Trojan horse; confused deputy; PATH without "."; Windows required admin to install until 2006 and the dialogs trained users to click (SE3 p.282-283).
- **Remedies:** stack canaries, DEP (2003), ASLR (2003), CFI (2005); static analysis from the start of the project; a better language (Rust); training; DevSecOps; in 2000 ~90% of vulnerabilities were buffer overflows, in 2008 less than half (SE3 p.283-284) `[DATED]`. The **principle of least privilege** and secure defaults are the basis of the architecture (SE3 p.284).
- **Environmental creep:** mechanisms suited to the original environment fail in the larger one (Unix, network, telnet/ftp/DNS/SMTP; Kerberos/TLS/SSH as "duct tape") (SE3 p.284-285).

## Triggers
- "ACL or capability? role or group?" → §2.
- "Review isolation of containers/VMs/tenants" → §3 and `references/09-seguranca-de-redes-e-malware.md`.
- Exposures caused by defaults or containers → `casos-e-antipadroes.md`.

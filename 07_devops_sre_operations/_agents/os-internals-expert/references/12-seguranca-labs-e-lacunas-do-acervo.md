# 12. OS security, lab appendices and collection gaps (ch. 52-57, appendices E-H)

PDF: ch.52 (dialogue) = p.16-17; ch.53 = p.82-94; ch.54 = p.161-179; ch.55 = p.253-270; ch.56 = p.360-379; ch.57 = p.447-464; index = p.95-105; appendices E-H = p.762-763, 781-793, 812-815, 830-832.

**Coverage honesty:** ch.53 was read in full; ch.54-57 were read by key sections and by sampling; appendices E-H, as a sample. The PDF text of these chapters (by Peter Reiher) is long and less central to this agent; use it with caution and verify the page.

## 1. Introduction to security (ch.53)

- **[from source]** The OS is an important target because everything runs on top of it; it can "do anything" the hardware allows, even lie on any syscall (OSTEP p.82-85). Hardware outside the OS's full reach: **TPM** and **security enclaves** (OSTEP p.85).
- **[from source]** Goals: **confidentiality**, **integrity** (includes authenticity), **availability**, **controlled sharing**, **non-repudiation**; goals → policies; the OS provides general mechanisms (OSTEP p.86-88).
- **[from source]** Saltzer and Schroeder principles: economy of mechanism, fail-safe defaults, complete mediation, open design, separation of privilege, least privilege, least common mechanism, acceptability (OSTEP p.88-89). System calls are checkpoints; weakest link (OSTEP p.91-92).

## 2. Authentication (ch.54, partial)

- **[from source]** Principal, agent, object, credential (OSTEP p.162); processes inherit the parent's identity (OSTEP p.163); authentication by "what you know/have/are" (OSTEP p.164); passwords with **cryptographic hash** and **salt** (OSTEP p.166-169); tokens and multi-factor (p.169-171); biometrics and **false positive/false negative** (p.172-175).

## 3. Access control (ch.55, partial)

- **[from source]** **ACLs** × **capabilities**; Unix ACL with 9 bits (owner/group/other); capabilities must be unforgeable; in Linux `open()` uses an ACL and the fd becomes an implicit capability; **discretionary** × **mandatory** access control; Android with permission labels (OSTEP p.254-265).

## 4. Cryptography and distributed security (ch.56-57, partial)

- **[from source]** Ciphers (AES), "don't invent your own cipher", public/private key, **cryptographic hashes**, certificates signed by CAs, SSL/TLS (SSL insecure; TLS 1.3 in 2020 [DATED]), Diffie-Hellman, cookies as capabilities, challenge/response (OSTEP p.361-378, p.447-462).

## 5. Labs (appendices E-H, sample)

- **[from source]** Systems programming projects (shell, memory allocator, concurrency, web server, fsck) and kernel projects on **xv6** (virtual memory, COW, kernel threads, extents) (OSTEP p.762-763, 781-793, 812-815, 830-832).

## 6. Collection gaps (verified by text search)

Absent (use [extrapolation] or refer elsewhere): cgroups, Docker/containers, Kubernetes, systemd, epoll, io_uring, KVM, lockdep, seqlock, "memory barrier", Paxos, CAP, TLB shootdown, PCID, vDSO, posix_spawn (only "spawn()" is cited, p.115), RAID-Z/"RAID-6" as a term, Linux io schedulers (CFQ, BFQ).
Present only in passing: NVMe (p.70), EEVDF (p.537), Xen (only in references), "erasure codes" (p.742).

## 7. Boundary and referrals

- Day-to-day Linux administration (systemctl, permissions in practice, logs, LVM, diagnostic tools): **refer to the agent `linux-shell-administration-expert`**.
- Containers, Docker, Kubernetes: refer to the containers agent (`containers-docker-kubernetes-expert`), if available.

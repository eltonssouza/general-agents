# 06. Distributed systems: concurrency, fault tolerance, DoS and names (Ch. 7)

Convention: "SE3 p.N" = PDF page; printed = PDF − 45 (ch. 7). Reading: p.288-315 in full; p.315-318 (types of names, summary) NOT read. 2020 cases: `[DATED]`.

## 1. Concurrency (SE3 p.288-296)
- `[from source]` Concurrency is a security issue: using stale data, inconsistent updates, ordering, deadlock, non-convergent state, time (SE3 p.289). Amdahl's law (speedup = (1−p+p/s)⁻¹; 3/4 parallelizable and 8 cores ≈ 2.909x) (SE3 p.289).
- **Stale data vs propagating state:** TOCTTOU (OS/360); hot card lists: *floor limit* and *stand-in processing* — only local or large transactions are checked immediately (SE3 p.290). Revoking credentials globally is expensive (DoD: 10 million revoked certificates to download per day); centralization reduces cost but increases the impact of compromise (DigiNotar 2011) (SE3 p.290-291).
- **Locking, callback, publish-register-notify** (card pre-authorization); credentials with an obligation on the issuer vs without; Aadhaar creates an audit trail (SE3 p.291-292).
- **Order of updates:** nightly batch, RTGS; blockchain has cost and off-chain looks like a current account; "there is no magic solution" (SE3 p.292-293). Deadlock, battle of the forms (SE3 p.293-294).
- **Non-convergent state:** ACID (atomic, consistent, isolated, durable) can be too much or not enough; "convergence" (if the volume dropped, the state would become consistent) is sufficient in many cases; "the auditor's life is the fight against entropy"; durability vs recoverability of payments (SE3 p.294-295).
- **Secure time:** Kerberos attackable through clock error; Cinderella attack; leap seconds; GPS/jamming; Lamport time; NTP (Netgear/D-Link overloading a Wisconsin server; NTP as a DDoS amplifier since 2016) (SE3 p.295-296).

## 2. Fault tolerance and recovery (SE3 p.296-303)
- `[from source]` "Recovery from failure is often the most important aspect of security engineering, yet one of the most neglected"; real spending: availability > integrity > crypto (SE3 p.296). fault → error → failure; MTBF/MTTR (SE3 p.296-297).
- **Byzantine:** n generals, t traitors; a solution exists iff **n ≥ 3t + 1** (Lamport-Shostak-Pease); with signatures, nobody dares lie to two colleagues (SE3 p.297). A component that gives a wrong answer is harder to use than one that just stops (SE3 p.297).
- **Costs of redundancy:** more complex stack (banks dropped Stratus), confidentiality can fail at any backup site, hard to destroy data on several tapes; today, developers leave data readable because they do not understand cloud access control (SE3 p.298-299). False alarm from an XOR checksum (customer assaulted by police) (SE3 p.299). "Redundancy is not an antidote to bad design" (737 Max: 2 sensors, 1 read) (SE3 p.299).
- **Levels of redundancy:** hardware, process group (compares outputs; does not defend against an authorized user), backup (checkpoints on non-overwritable media + journals; ransomware that waits and encrypts weeks of backups), and *fallback* (less capable system; e.g. card imprinters) — **backup ≠ fallback** (SE3 p.300-301). Disk redundancy does not protect against a malicious programmer; backup does not protect against an error inserted slowly (SE3 p.301).
- **Recovery testing:** one Saturday a year in the 80s; Tesco pulled the plug annually (backup in 40 s); Netflix chaos monkeys 2011; cloud SLAs allow hours of downtime per month; map dependencies outside your supply chain (2001 truckers' strike) (SE3 p.301-302).
- **DoS:** make selective attack impossible (anonymity of the target); DDoS: Panix 1996, extortion of bookmakers (US$10-50 thousand) solved by Akamai + agreement + police; "booters" in 2018 (a few US$ = 100 Gbit/s; the FBI took down 15 sites); **forcing an insecure fallback by DoS** (card with dead chip → stripe) (SE3 p.302-303).

## 3. Names (SE3 p.304-314)
- Names exist in context; a certificate without a name = *bearer token*; each name added creates a dependency (SE3 p.304).
- **Needham's 10 principles** (SE3 p.305-308): (1) the function of names is to facilitate sharing; (2) name information can be in several places — SIM swap breaks SMS authentication; (3) it is bad to assume that only so many names will be needed (cards from 13→16 digits was the industry's most expensive upgrade); (4) global names buy less than you think; (5) names imply commitments — be flexible to organizational changes; (6) names can become capabilities/passwords (citizen number in Norway; DoD EDIPI; "Anderson, 123"); (7) it is simpler if an incorrect name is obvious (check digit; Prawo Jazdy); (8) consistency is hard and often fudged (barcodes); (9) don't be too clever (phone is more robust than email; Signal/WhatsApp use the number; M-Pesa); (10) some names are bound early, others not — avoid binding early.
- **Zooko's triangle:** no naming system is global, decentralized and human-readable (SE3 p.308).
- **Name ≠ identity** (different names for the same principal); two types of failure: impersonating anyone vs someone specific (SE3 p.309). A recursive chain of names gives the attacker a choice of targets (pre-issuance fraud; Linden Labs accepted Tupac's license) (SE3 p.309). Cultural assumptions about names, political ID in less developed countries; "service-oriented ID ≠ legal identity" (SE3 p.310-312).
- **Semantics change:** a bank that linked accounts by name and sent the mistress's statement to the wife (SE3 p.312). **Uniqueness:** a duplicate transaction number caused a £10m payment to be discarded as a duplicate (SE3 p.313). **Stability:** ¼ of addresses change per year; in a key directory the main cause of change was a change of email, "key loss: zero"; **Kent's law** (the more items a credential lists, the shorter its lifetime); pseudonyms have legitimate uses (SE3 p.314).

## Triggers
- "How do I revoke quickly?" → §1 (cost) + `references/04-criptografia.md` (CAs) + procedures P7.
- "Design of IDs/names" → §3.
- "Does backup protect against ransomware?" → §2 (note on prior encryption of backups).

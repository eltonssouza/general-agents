# Procedures (step by step) extracted from the book

Convention: "SE3 p.N" = PDF page (printed = PDF − chapter offset; see `INDEX.md`). Each step carries its origin label: `[from source]` (it is on the cited page), `[inference]` (our organization/deduction from the book) or `[extrapolation]` (outside the book). The book rarely gives "numbered recipes"; these sequences are **organizations** of what it recommends, and this is stated in each procedure. **Nothing here replaces a formal security review** (nor an authorized penetration test, nor an audit).

---

## P1. Threat and requirements analysis (the book's top-down method)
Basis: the book proposes the chain **threat model → policy → mechanism → assurance**, with incentives running through everything (SE3 p.52-53, 360). The order in steps is `[inference]`.

1. **Define the system in the broad sense** (product + staff + users + customers), including humans and usability `[from source]` (SE3 p.60).
2. **List the likely opponents** by class (spies, crooks, geeks, swamp), capability, motivation and how they change over time `[from source]` (SE3 p.66, 107); include competitors, suppliers, executives and insiders `[from source]` (SE3 p.97-98) and abuse by people close to the victim `[from source]` (SE3 p.102-107).
3. **Ask whether the attack scales** and whether the opponent already knows the system (do not count on obscurity) `[from source]` (SE3 p.77, 98; Kerckhoffs, p.583).
4. **Write an explicit, short policy** (one page): what is protected and from whom; avoid empty "policies" (`need-to-know`, "approved by management") `[from source]` (SE3 p.360-361).
5. **Identify hazards/assets on both sides** (system assets and assets accessible to the attacker) and trace paths between them — "meet in the middle" `[from source]` (SE3 p.1006).
6. **Record risks** with severity×probability, owner and mitigation (P2) `[from source]` (SE3 p.999).
7. **Choose mechanisms** with attention to incentives: who pays for the failure? who decides? `[from source]` (SE3 p.319, 338, 348) and check whether the mechanism attacks the real risk or is *security theatre* `[from source]` (SE3 p.53).
8. **Define how you will know it works** (assurance): hostile review, tests, monitoring, IR plan `[from source]` (SE3 p.1070-1071, 1031-1032).
9. **Review when the environment changes** (assumptions shift: cards on untrusted terminals, new versions, new users) `[from source]` (SE3 p.181-182, 284-285).
Useful output: `se3_checklist.py markdown --area oponentes --area devsec`.

## P2. Risk register and ALE
1. List the risks that may occur; score **severity 1-5** and **probability 1-5**; multiply (1 to 25) `[from source]` (SE3 p.999).
2. Describe the mitigation, recompute (book example: 5×4=20 → 16 through a hiring rule) and assign a **senior owner** to each risk `[from source]` (SE3 p.999). Tool: `se3_calc.py risk-register --item "name:5:4:4:4"`.
3. For quantifiable losses use **ALE = loss × incidents/year** `[from source]` (SE3 p.1000); separate what is data (common losses), guesswork (rare ones) and office politics `[from source]` (SE3 p.1000). Tool: `se3_calc.py ale --item "SWIFT fraud:50000000:0.005"`. Note: the book's printed table has an inconsistent row (ATM fraud large: 250,000 × 0.2 = 50,000, printed 100,000) (SE3 p.1000).
4. Consider risk **and reward** (a business that doubles turnover even with larger losses may profit more than "zeroing fraud") `[from source]` (SE3 p.1010-1011).
5. Beware of insurance: insurers do not assess correlated cyber risk well; insurance also protects executives `[from source]` (SE3 p.1000-1001).

## P3. Hazards, fault trees and FMEA (safety × security)
Organization `[inference]` of what the book describes (SE3 p.1002-1009):
1. Identify hazards and risks; choose a strategy (avoid, restrict, redundancy) `[from source]` (SE3 p.1002).
2. **Eliminate the hazard** when possible (minimize the TCB; don't keep the data) `[from source]` (SE3 p.1003).
3. **Fault/threat tree** (top-down) and **FMEA** (bottom-up) `[from source]` (SE3 p.1003-1005).
4. Build the **hazards × mechanisms matrix**: at least two independent mechanisms per serious hazard `[from source]` (SE3 p.1006-1007).
5. For the human part: rare, important tasks are where the worst errors occur; design for a safe state by default; simplify what the operator sees `[from source]` (SE3 p.1007-1009).
6. Remember the difference: safety deals with random failure; security deals with an adversary who forces the rare combination `[from source]` (SE3 p.1009).

## P4. Designing a password/authentication system
Organization `[inference]` of SE3 p.137-163:
1. Decide whether you really need a password (many exist for marketing) `[from source]` (SE3 p.137-138).
2. Design **recovery** first: the system is as strong as the weakest fallback; second factor for important accounts `[from source]` (SE3 p.139-141).
3. **Password choice:** list of bad passwords (≈100,000) instead of composition rules; no mandatory periodic change without compromise `[from source]` (SE3 p.145-147).
4. **Storage:** random salt + slow, strong one-way function; keep salt and hash `[from source]` (SE3 p.156). Do not record passwords in failure logs `[from source]` (SE3 p.155-156).
5. **Attempt limiting:** throttling and global rate control (not just per account); lockout opens up DoS `[from source]` (SE3 p.152, 157-158). Calculate with `se3_calc.py dod-password`.
6. **Attacks to consider:** single target, any account, credential stuffing, DoS `[from source]` (SE3 p.151-152).
7. **Usability:** the secure path must be the easiest; do not train users to act insecurely `[from source]` (SE3 p.133, 148-150).
8. Consider alternatives/complements (managers, physical tokens, SSO) by Bonneau's criteria `[from source]` (SE3 p.158-161).

## P5. Designing internal controls (fraud, separation of duties)
Organization `[inference]` of SE3 p.447-456, 463-464:
1. Model the records as **double-entry bookkeeping** with an append-only log; balancing is an alarm `[from source]` (SE3 p.447-450).
2. Apply the **Clark-Wilson model** when useful: CDIs only altered by TPs; triples (subject, TP, CDI); authenticate subjects; only security officers alter authorizations `[from source]` (SE3 p.451); remember that it does not say how to design the separation of duties `[from source]` (SE3 p.451-452).
3. For each control ask: **dual control** or **functional separation**? Combine **prevent–detect–recover**: if detecting is slow and recovering is hard, strengthen prevention; if preventing is hard, detect fast and recover vigorously `[from source]` (SE3 p.453-454).
4. **Identify the 30-40 trusted people**, minimize, pay them well, watch them discreetly `[from source]` (SE3 p.456).
5. Job rotation and forced vacations of 1-2 weeks `[from source]` (SE3 p.454).
6. Ask employees how they would commit fraud and look for business processes that defeat dual control (letter of guarantee, codes by phone, gateways) `[from source]` (SE3 p.463, 470-471).
7. If the system must provide **evidence**, dual control is not enough: require non-repudiation that resists hostile experts `[from source]` (SE3 p.478-479).
8. Never declare the system fail-safe `[from source]` (SE3 p.463-464).
For dual control in software/infra engineering (approval of code in production): SE3 p.455-456; Google's operational practices are in the secure-reliable-systems-expert agent (BSRS).

## P6. Evaluating seals, tamper-evidence and proof of tampering (life cycle)
The book presents this as a "microcosm of the assurance process" (SE3 p.605). The book's questions (SE3 p.604-605):
1. Who must notice the forgery and with what false acceptance and rejection rates?
2. Has anyone competent tried to defeat it? What counts as "defeat"?
3. Who can buy/forge the materials?
4. Can the applicator be careless or corrupt? Does the seal protect the right party?
5. Quality of application (dirt, oil, cleanliness)? In court, are there experts beyond yours?
6. Disposal? Define the threat: counterfeiting, alteration or dilution (SE3 p.602-603).
Avoid *gundecking* (inspectors who don't inspect; e.g. seals with a new code every minute) (SE3 p.600). Remember the Trujillo experiment: experts were no better than chance (SE3 p.603).

## P7. Revocation and freshness of credentials
Organization `[inference]`:
1. List who needs to know about the revocation and how fast (stand-in/floor limit show the cost of checking everything) `[from source]` (SE3 p.290).
2. Compare **push** (revocation lists; DoD: 10 million certificates to download per day) and **pull**/short life (timestamps in Kerberos, short OAuth tokens) `[from source]` (SE3 p.185-187, 290-291).
3. Weigh centralization: it reduces cost and increases the impact of compromise (DigiNotar) `[from source]` (SE3 p.290-291).
4. In ACLs, revoking a dismissed employee = cancelling password/token; with capabilities it is hard to revoke and audit `[from source]` (SE3 p.258-261).
5. Credentials with many attributes last less (Kent's law) `[from source]` (SE3 p.314).
6. In apps, treat revocation (stolen phone, former tenant) as a first-class requirement: it consumed half of the security time of a payment app `[from source]` (SE3 p.808-809).
7. Certificate revocation is "flaky" in practice `[from source]` (SE3 p.241-242).
8. Test the revocation path and what happens when verification fails (fail open vs fail closed) `[extrapolation]`/`[inference]`.

## P8. Network defense and intrusion detection
Organization `[inference]` of SE3 p.748-760:
1. Start from the premise that **the local network is not trusted**; strong authentication between clients and servers `[from source]` (SE3 p.749).
2. Keep an **accurate inventory** (automated patching depends on it); scan the network; critical systems tend to be the least updated `[from source]` (SE3 p.751-752).
3. Handle **spear phishing** with technical controls (attachments in the cloud, restricted devices, filters) instead of blaming users `[from source]` (SE3 p.752).
4. **Firewalls/proxies:** filtering, circuit gateways, application proxies (BeyondCorp); ingress and egress (source address validation); smaller networks limit scope `[from source]` (SE3 p.752-757).
5. **Detection:** it is cheaper to prevent some and detect the rest `[from source]` (SE3 p.757); choose threshold, signatures or anomaly while knowing the limitations (Cohen; false alarms) `[from source]` (SE3 p.757-759).
6. **Calculate the base rate** before buying/configuring (10 attacks per million sessions and 0.1% false alarms → 100 false for 1 real): `se3_calc.py bayes-alarm` `[from source]` (SE3 p.759-760).
7. Keep logs to distinguish a botnet from a targeted attack and have an IR plan `[from source]` (SE3 p.108).
8. Beware of ML in IDS (does not detect new attacks; manipulable) `[from source]` (SE3 p.759, 911).
Not read: network BGP/DNS/DoS (p.734-747): NOT COVERED.

## P9. Incident response plan and vulnerability disclosure
The book gives the four components (SE3 p.1031-1032); the order in steps is `[inference]`:
1. **Monitoring:** threat intelligence, honeypots, reporting channels `[from source]` (SE3 p.1031).
2. **Repair:** orchestrate the response; notify vendors and customers; alternative communication channel `[from source]` (SE3 p.1031-1032).
3. **Distribution:** in an emergency, run the normal patch process as fast as possible `[from source]` (SE3 p.1032).
4. **Reassurance:** educate the CEO and board beforehand; press releases ready per severity; notification laws; "information security is a CEO issue" `[from source]` (SE3 p.1032).
5. **Disclosure:** coordinated disclosure policy, CVE/CVSS/NVD, relationship with researchers and bug bounty (VW sued academics) `[from source]` (SE3 p.1027-1031).
Operational IR details (IMAG, OpSec, forensics): other agents in the collection (secure-reliable-systems-expert).

## P10. Evaluating a protocol or a use of cryptography
Organization `[inference]`:
1. Is the threat model realistic? Does the protocol deal with it? `[from source]` (SE3 p.167).
2. Freshness, explicit names, independent keys per application, unambiguous formats `[from source]` (SE3 p.169-171, 179, 183-184, 189).
3. For each primitive: authenticated mode, IVs, hash size, key size `[from source]` (SE3 p.206, 223-228, 232-235) — check current values in up-to-date sources `[DATED]`.
4. Use an accredited toolkit; do not invent a cipher or protocol; peer review `[from source]` (SE3 p.190, 239, 250-251).
5. Attention to key management (how many, generation, lifetime, destruction, recovery) `[from source]` (SE3 p.188).
Output: `se3_checklist.py markdown --area protocolos --area cripto`.

## P11. Deciding whether and how to release "anonymized" data
Organization `[inference]` of SE3 p.417-443:
1. Admit the gulf between what anonymization does and what stakeholders want to believe `[from source]` (SE3 p.418).
2. Ask who will try to reidentify and with what side data (Sweeney: 69% by date of birth + ZIP; AOL; Netflix; location) `[from source]` (SE3 p.427-433).
3. Distinguish **privacy set** (who must not know) from **anonymity set** (whom I can be confused with) `[from source]` (SE3 p.437).
4. Prefer alternatives: controlled access with license/NDA, explicit consent, taking the query to the data `[from source]` (SE3 p.441, 407-408).
5. If using differential privacy: ε is a policy decision; ε=1000 ≈ raw data; global privacy budget `[from source]` (SE3 p.434-436). Noise scale: `se3_calc.py laplace-scale` (`[extrapolation]`).
6. Privacy does not compose: two perturbed versions of the same data may allow identification `[from source]` (SE3 p.425-426).
Legal aspects (GDPR, LGPD): see reference 10 and other agents (LGPD/NIST) — this list is not legal advice.

## P12. Evaluating a product certification or assurance
Organization `[inference]` of SE3 p.1046-1083:
1. Who pays the certifier? Is there a risk of *Maximum Complacency* (race to the bottom)? `[from source]` (SE3 p.1063-1065).
2. What does the certification actually cover (FIPS 140 covers hardware, not software; CC level 6 covered only the OS)? `[from source]` (SE3 p.1057, 669).
3. Consider the CC's failures: cost, ignores usability and administration, rigged PPs, does not cope with monthly patching `[from source]` (SE3 p.1060-1062).
4. Ask for hostile review and failure data, not friendly review `[from source]` (SE3 p.1070-1071).
5. Estimate testing effort: MTBF ~ t/k `[from source]` (SE3 p.1068); `se3_calc.py reliability`.
6. Ask for how long the vendor fixes the product (assurance is dynamic) `[from source]` (SE3 p.1047-1048, 1082-1083).
7. Treat ISO 27001 and checklists as `compliance`, not assurance `[from source]` (SE3 p.1034-1036, 1066).

## P13. Evaluating a biometric system
Organization `[inference]` of SE3 p.608-635:
1. Measure FAR/FRR/EER on a large and diverse population (goats, lambs, wolves) `[from source]` (SE3 p.611-612, 632).
2. 1:1 verification or 1:N identification? Calculate the birthday limit: `se3_calc.py biometric-birthday` `[from source]` (SE3 p.632).
3. Consider assisted vs unattended operation, fallback and social inclusion `[from source]` (SE3 p.612, 630-634).
4. Templates are not irreversible hashes (hill-climbing) `[from source]` (SE3 p.632-633).
5. Attacks: gelatin/tape, masterprints, photos, recordings; defenses: unpredictable challenge, video with colors `[from source]` (SE3 p.620-621, 632-633).

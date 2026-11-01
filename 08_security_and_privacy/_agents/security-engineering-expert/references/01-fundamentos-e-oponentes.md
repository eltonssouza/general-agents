# 01. Security engineering fundamentals and who the opponent is (Ch. 1 and 2)

Convention: "SE3 p.N" = PDF page (marker `=== PAGE N ===`). Printed = PDF − 48 in chs. 1-2 (see `INDEX.md`). Reading: chs. 1 and 2 read in full. Every incident number/statistic in this file is from 2020 and counts as `[DATED]`.

## 1. What the book calls security engineering (Ch. 1, p.51-64)

- **Definition.** `[from source]` Building systems that remain dependable in the face of malice, error or mishap; it is the discipline of tools, processes and methods for designing, implementing, testing and adapting whole systems as the environment evolves (SE3 p.51). It requires knowledge of crypto, hardware, economics, applied psychology, organizations and law, and "adversarial thinking" (SE3 p.51). Ordinary systems engineering deals only with error and mishap, not with malice (SE3 p.51).
- **Four elements.** `[from source]` Policy (what you are trying to achieve), mechanism (ciphers, access controls, tamper-resistance...), assurance (how far you can trust each mechanism and the combination) and incentive (the motivation of those who guard and maintain the system and of the attackers); all of them interact (SE3 p.52-53). In the 9/11 example, the hijackers' success was a policy failure (knives were allowed), not a mechanism failure (SE3 p.52).
- **Security ≠ "making sure something does not happen".** `[from source]` The conventional view (software = make things happen; security = prevent them) is simplistic: many systems fail because designers protect the wrong thing, or the right thing in the wrong way (SE3 p.52).
- **"Security theatre".** `[from source]` Decision-makers' incentives favor visible controls over effective ones; hardening cockpit doors (US$100m) removed much of the risk, while screening cost billions with low effectiveness (SE3 p.53).
- **Cases as a source of learning.** `[from source]` Complexity comes from history and causes failures; that is why the book is full of cases (SE3 p.54). "Civil engineers learn more from the bridge that falls than from a hundred that stay up" (SE3 p.59).

### Definitions the book fixes (SE3 p.60-64)
- **System** has six senses (product; + OS/infrastructure; + applications; + IT staff; + internal users/management; + customers and external users). Confusion among them is a fertile source of vulnerabilities; the book adopts sense 6 and says that ignoring humans and usability is one of the biggest causes of failure (SE3 p.60).
- **Principal** is an entity that takes part in the system (person, role, equipment, channel, or compound: group, conjunction, compound role, delegation); group ≠ role (SE3 p.61).
- **Identity** = a correspondence between the names of two principals, often abused as a synonym for "name" (SE3 p.61).
- **Trusted vs trustworthy.** `[from source]` A *trusted* component (NSA definition) is one whose failure can break the policy; *trustworthy* is one that will not fail (SE3 p.61).
- **Secrecy, confidentiality, privacy.** `[from source]` Secrecy is the effect of mechanisms that limit who has access; confidentiality is an obligation to protect other people's secrets; privacy is the ability/right to protect personal information and personal space and does not extend to legal persons; privacy is secrecy for the benefit of the individual and confidentiality, for the benefit of the organization (SE3 p.62). Metadata and anonymity also matter ("you need a crowd to hide in") (SE3 p.62).
- **Authenticity** in the protocol literature = integrity + freshness (SE3 p.62).
- **Hack** = something the system rules permit but the designers neither anticipated nor wanted (SE3 p.63).
- **Vulnerability, failure, policy, target, profile.** `[from source]` A vulnerability is a property of the system or its environment that, together with a threat, can lead to a security failure (violation of the policy). *Security policy* = succinct statement of the protection strategy; *security target* = detailed specification of the means; *protection profile* = implementation-independent target (SE3 p.63).
- **Safety vocabulary.** `[from source]` hazard, danger, risk (hazard × danger × latency), uncertainty (unquantifiable risk), safety policy, safety case (SE3 p.64).
- **Chapter conclusion.** "Security" is an overloaded word; robust design requires making the protection goals explicit (SE3 p.64).

### Chapter 1 domain examples (useful as a "map of systems")
Bank: accounting system (main threat = the staff themselves; ~1% of branch staff dismissed/year; double-entry bookkeeping; two people on large transfers; mandatory vacations) (SE3 p.54); hospital: safety usability, privacy of patient records, hard anonymization, WannaCry (SE3 p.57-58); home: immobilizer, relay attacks on keyless fobs, IMSI-catchers, SIM swap, prepayment meters, a children's watch without encryption banned in 2019 (SE3 p.58-59). A 2019 European law requires maintaining digital components for 2 years or more (SE3 p.56) `[DATED]`.

## 2. Who is the opponent (Ch. 2, p.65-109)

- **The engineer's step zero.** `[from source]` Identify the likely opponents; you cannot defend against all threats and still have a useful system at reasonable cost; ask: what capabilities and motivation? how certain is the assessment? how does it change over the system's lifetime? (SE3 p.66). Four classes by motive: spies (states), crooks (money), geeks (researchers), swamp/bullies (personal abuse) (SE3 p.66, 107).
- **Spies' tools end up with criminals.** `[from source]` (SE3 p.67); EternalBlue (leaked in 2017) was used by NotPetya and WannaCry (SE3 p.74, 84-85, 88).
- **Attack scale.** `[from source]` Capital cost rises and marginal cost per target falls with scale (tapping everyone instead of one) (SE3 p.77); an index of Internet software versions (Mugshot) shows which targets fall to which exploits (SE3 p.77).
- **Supply chain and standards.** `[from source]` Supply-chain tampering and weakening of standards (Dual_EC_DRBG; export restrictions) left vulnerabilities in locks, VPNs etc. (SE3 p.70-71); the GCHQ report on Huawei pointed to poor engineering practices (70 copies of 4 versions of OpenSSL) (SE3 p.81).
- **Attribution.** `[from source]` "Attribution is hard" is generally false; opsec mistakes give actors away, and threat intelligence attributes even false-flag operations with reasonable probability (SE3 p.88).
- **Equifax 2017.** `[from source]` Struts patch not applied/password 'admin' on the portal; 76 days of access; ≥145.5 million people; avoidable (SE3 p.89).
- **Cybercrime.** `[from source]` ≈ half of all crime by volume and value; police spend <1% of their budget (SE3 p.89). Underground markets (2003-5) enabled specialization and scale (SE3 p.90). Criminal infrastructure: botnets (Storm, Conficker/DGA, Mirai), malware developers, spam, mass account compromise (credential stuffing = largest volume of compromise attempts in 2019), pay-per-install (US$10-15 per thousand in the US/Europe), hack-for-hire (~US$750), cashout (card number + expiry < US$1), ransomware (SE3 p.90-95). In payments: total cost is ~two orders of magnitude above what criminals obtain (SE3 p.96); BEC and CEO frauds mainly affect large, badly managed companies or mid-size ones without controls; "most would be prevented by the procedural controls that large firms already have" (SE3 p.96-97).
- **CEO crimes and competitors.** `[from source]` Competitors and suppliers can also be capable opponents (accessory lock-in; VW) — "think about this when building the threat model" (SE3 p.97-98).
- **Whistleblowers.** `[from source]` A technical countermeasure (DLP) is less important than robust channels for reporting wrongdoing; many hotlines go to HR; one large firm's hotline carried third-party trackers (SE3 p.99). It is mainly a policy problem (SE3 p.99).
- **Geeks.** `[from source]` Researchers; responsible disclosure; bug bounty; vulnerability market; VW sued researchers and lost (SE3 p.100-101).
- **Swamp.** `[from source]` Hacktivism/hate campaigns, CSA and the "law-norm gap", bullying (cyber < half of bullying), intimate partner abuse (27% of women, 11% of men) (SE3 p.102-105). For victims of intimate abuse "all the usual advice is upside down": the opponent knows the recovery questions; design for stress, multiple accounts, a history that does not reveal deletions, 2FA and notifications; stalkerware is a problem (SE3 p.106).
- **Abusability.** `[from source]` "It is not enough to think about usability; think about abusability"; homes are not units, devices are not personal, the buyer is not the only user (SE3 p.107).
- **Message for the defender.** `[from source]` Patching and antivirus are not enough; keep enough logs to tell a botnet machine from a targeted attack; have an incident response plan (so the CEO is not "like a fish out of water"); essential controls: backup (ransomware) and payment procedures (BEC) (SE3 p.108).

## How to use
- When building a **threat model**: classify the opponent by motive (4 classes), capability and persistence; list what the opponent already knows (do not count on obscurity) and how the attack scales. `[inference]` combining SE3 p.66, 77, 98.
- See `references/procedimentos.md` (P1) and `scripts/se3_checklist.py` (area "oponentes").
- Out of scope: attributing real attacks to countries/groups based on current news — `[DATED]`, ask for current sources.

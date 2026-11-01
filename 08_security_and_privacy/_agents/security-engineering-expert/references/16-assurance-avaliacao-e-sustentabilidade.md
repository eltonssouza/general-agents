# 16. Assurance, evaluation, dependability metrics, safety×security and sustainability (Ch. 28; Ch. 29)

Convention: "SE3 p.N" = PDF page; printed = PDF − 31. Reading: ch. 28 p.1046-1083; **not read** p.1083-1089 (rest of sustainability and summary); ch. 29 (p.1090-1091) in full. Regulatory facts are from 2020: `[DATED]`.

## 1. What changed: assurance is no longer static
- `[from source]` Laboratory evaluation of five years ago "would sound quaint"; assurance, compliance and sustainability make up the chapter; assurance is "our estimate of the probability that the system will not fail in a particular way" and today depends on the vendor's future commitment (how long and how diligently it will be fixed) (SE3 p.1046-1048). Assurance is a political, economic and dynamic process (SE3 p.1049).
- The four elements (Fig. 1.1) revisited: incentives, policy (neglected), mechanisms, assurance; usability also for developers (ECB, admin, too many permissions) (SE3 p.1048).

## 2. Evaluation regimes (SE3 p.1049-1066)
- UL/insurance; evolution of standards (bumping); FDA/FAA/NHTSA/EU ("regulatory superpower"); CE mark (SE3 p.1049-1051). **Medical devices:** Therac-25; infusion pumps and usability (FDA with ~half a day of engineering per device and usability out of scope); ISO/IEC 62366-2; EU regulation 2017/745 postponed to May/2021 (SE3 p.1051-1053). **Aviation:** 737 Max (a single angle-of-attack sensor, no adequate FMEA, FAA delegated to Boeing; 346 dead) (SE3 p.1054-1055). "Stop separating safety from security" (SE3 p.1056).
- **Orange Book (1985-2000)** and **ITSEC** (evaluation becomes contracted by the vendor: laboratory shopping) (SE3 p.1056-1057). **FIPS 140:** covers hardware, not software; gap between level 3 and 4 (SE3 p.1057).
- **Common Criteria:** TOE, EAL1-EAL7, PP, ST; 85 of 1472 products at EAL6+ in 2020; PP quality varies (SE3 p.1057-1060). **What goes wrong:** cost and bureaucracy (millions of euros), ignores usability and administrative security, PPs designed for market rigging, assumes waterfall and does not cope with monthly patches, is technology-oriented rather than business-process-oriented, rigor varies by country, brand poorly defended, nothing about liability ("rubber crutch"); cPPs became marketing (SE3 p.1060-1062).
- **Principle of Maximum Complacency** (Lerner-Tirole): competition among certifiers leads to a *race to the bottom*; "the certifier is a liability shield"; PCI took on this role in payments; electronic signature certification as a "tax"; Trust-e and adverse selection (SE3 p.1063-1065).
- **Next steps (2020):** Cybersecurity Act 2019/881 (ENISA; three certification levels: basic = self-assessment, substantial, high); UK: GCHQ left the CC; Cyber Essentials (£300); **ISO 27001**: "expensive, turned into a revenue source by the big accounting firms, as useless as the CC; almost every major breach occurs at a certified firm"; Bitsight (scan-based rating) (SE3 p.1065-1067) `[DATED]`.

## 3. Dependability metrics and dynamics (SE3 p.1067-1075)
- **Reliability growth:** for a single bug, the probability of remaining undetected after t random tests is **p = e^(−E·t)**; in large systems the probability that the t-th test fails is ∝ **k/t**, so MTBF ≈ t/k and reliability grows *linearly* with testing time: "for an MTBF of a million hours, test for at least a million hours" (SE3 p.1067-1068). This holds for independent bugs and is the best possible; reusable libraries have limited gain; testers should work in parallel (SE3 p.1068-1069). Use `se3_calc.py reliability`.
- **Attacker × defender asymmetry (Ahmed/Brian example):** 1,000,000 bugs with MTBF 10^9 h; Ahmed tests 10,000 h/year and finds ~10 bugs; Brian tests 10^8 h/year and finds ~100,000, but the chance of having found a specific bug of Ahmed's is ~10%; "the attacker has thermodynamics on his side" (SE3 p.1069). Real vulnerabilities are correlated; ways out: simplicity or a learning system (monitoring, disclosure, fast patching) (SE3 p.1069-1070). Use `se3_calc.py bug-race`.
- **Hostile review:** "friendly reviews are essentially useless"; evaluations paid for by the vendor are fundamentally broken; motivate attackers with money (IV&V, bug bounty) or honor (Sandia×NSA; Project Zero with 90 days, >97% fixed) (SE3 p.1070-1071).
- **FOSS:** Kerckhoffs; arguments for and against; "under the standard model, openness helps attack and defense equally"; Raymond's criteria; "open is neither necessary nor sufficient" — ask how much effort capable people have spent and whether they say everything they find; generous bug bounty program; take part in the community (SE3 p.1071-1073).
- **Process assurance:** ISO 9001 "decorative"; CMM; products "like milk or like wine"; reliability improves, stabilizes, then deteriorates (senescence); refactoring; really measure (SE3 p.1073-1075).

## 4. Safety and security entangled; sustainability (SE3 p.1075-1083)
- Regulation moves from pre-market testing to maintaining safety and security throughout the life cycle with patches; the FDA warned against one hackable pump but not against 300+ models with usability problems; recall of 465,000 pacemakers; cars (EBA/AEB, Autopilot, ISO 21434, UNECE); Dieselgate: "the threat model came to include the manufacturers themselves" (SE3 p.1075-1080). EU report (2016): vendors must self-certify that products can be fixed; breach reporting to more stakeholders; car data for investigations; regulators must move from product testing to system assurance (SE3 p.1080-1082).
- Sustainability: products cease to be static; the automotive industry does not want to be responsible for patches beyond ~6 years; embedded carbon ≈ fuel consumption; right-to-repair (SE3 p.1082-1083).

## 5. Close of the book (ch. 29, p.1090-1091)
`[from source]` Three themes: social complexity ("it is not enough to study how a system interacts with one human; you have to study how it works with many humans"), sustainability (software in durable goods for 20-40 years; "we have no idea how to do this"), politics ("security is not scalar but relational; it is about how systems exercise power"); engineers should take part in the policy debate (SE3 p.1090-1091).

## Triggers
- "Should I require CC/FIPS/ISO 27001 certification?" → §2: treat as `compliance`/a shield, not as assurance; ask for hostile review and failure data (§3).
- "How long should I test?" → §3 (k/t).

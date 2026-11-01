# Cases, anti-patterns and tensions between the sources

DZ = MacMillan (Packt, 2021; PDF page); TMM = Threat Modeling Manifesto. The DZ is **single-author**: there is no divergence between authors; the "divergences" below are (a) internal tensions of the DZ itself and (b) DZ x TMM differences. Labels: [from source], [inference], [extrapolation].

## A. Cases from the book (what they illustrate)
| Case | What it illustrates | Page |
|---|---|---|
| Ketchup Company: recipe on a web NAS without login | Risk calculation 5 × 5 = 25; mitigation by password and residual risk | DZ p.27-34 |
| Ketchup Company migrates PII to the cloud | Compliance: legal basis, notices, SAR, deletion | DZ p.37 |
| Restore simulation and RAID-0 | Continuous improvement: update records, reassess, show ROI | DZ p.39-40 |
| Phishing and "blaming the victim" | Asking about training, simulation and a safe way of working | DZ p.41 |
| Risk template for the C-level (WAF vs. annual loss) | Language of impact, cost and timeline | DZ p.49 |
| Event → incident → nonconformity (ransomware and SMB) | Difference between the three terms and resulting actions | DZ p.207-208 |
| Heartbleed | Open source does not guarantee review | DZ p.223-224 |
| IoT light bulbs with remote access | Segregate the IoT network | DZ p.108 |
| Exposed SCADA | Obscurity is not a control; air gap and inventory | DZ p.109 |
| 4-step CI DevSecOps pipeline | Automatic controls before production | DZ p.250-251 |
| Pentest on a clone vs. production | Trade-off: operational safety vs. certification body acceptance | DZ p.179, 188 |
| Docker Hub and rotting templates | Risk of IaC copied without review | DZ p.199 |

## B. TMM anti-patterns (TMM p.2) with practical examples [inference]
- **Hero Threat Modeler:** only "the security person" models. Countermeasure from the text: everyone can and should do it.
- **Admiration for the Problem:** a huge list of threats with no action items. Countermeasure: arrive at practical and relevant solutions.
- **Tendency to Overfocus:** spending the whole session on one type of adversary or on a single asset. Countermeasure: remember that parts of the model are interdependent.
- **Perfect Representation:** waiting for the definitive diagram. Countermeasure: several representations.

## C. DZ anti-patterns and bad practices
- **Security through obscurity** as the main defense (DZ p.105, 109, 123): changing the SSH port is only a 1st layer.
- **Flat network** (DZ p.126) and deny-all applied without an inventory of communications (outage risk).
- **Manual data classification** done by people who are not in security (DZ p.68): does not scale.
- **A policy nobody follows** or that only serves auditors (DZ p.54, 89).
- **Blaming the user** (DZ p.41) without training, simulation or a safe path.
- **Technical language for senior management** (DZ p.48).
- **Contaminated baseline** from building the "normal" with the attacker already inside (DZ p.214-215).
- **IaC without change control** (DZ p.199) and **turning off pipeline checks** (DZ p.200).
- **Systems designed without being able to be updated** (DZ p.110, 140).
- **Incident plan kept only on the system that goes down** (DZ p.61).
- **Red Team without Blue Team and without budget** (DZ p.175).
- **Testing production or third-party infrastructure without agreement** (DZ p.176, 179, 245).

## D. Internal tensions of the DZ (single author)
1. **Complexity x defense in depth.** The author repeats that complexity is the enemy of security (DZ p.44, 56, 58, 102) and that defense in depth requires layers (DZ p.44, 57); he reconciles them by saying that reducing the cost of a control allows more layers (p.44) and that only the relevant controls should be applied (p.102).
2. **Obscurity.** Avoid security through obscurity (DZ p.105) vs. changing the SSH port as a 1st step (p.123), which he classifies as obscurity, not mitigation.
3. **Ransomware.** FBI: do not pay; author: depends on the risk (DZ p.93-94).
4. **Open source.** Transparency as an advantage (DZ p.224, 248) vs. Heartbleed.
5. **Testing.** Testing on a clone avoids taking production down (DZ p.179, 188) but may not be accepted by certification bodies/customers (p.188).
6. **Compliance.** Rejects "tick a box" (DZ p.174) but organizes the ISMS around standards (ISO 27001) (DZ p.50).
7. **Pentest without buy-in.** Acknowledges that a professional test can draw attention, but says he cannot recommend it and warns of the risk of "hot water" (DZ p.174).

## E. DZ x TMM differences
1. **Object of threat modeling:** DZ p.25 (threats/actors per asset) vs. TMM p.1 (analysis of system representations through four questions). Detail in `modelagem-de-ameacas-no-dz-e-ponte-com-tmm.md`.
2. **Process x people:** the DZ builds a documentary system (ISMS); the TMM prioritizes people and collaboration over processes and tools, and *doing* over *talking* (TMM p.1). [inference] this is not a contradiction: the TMM also says that documents record understandings and enable measurement (TMM p.2).
3. **Focus:** the DZ is aimed at the security professional who manages organizational risk; the TMM is for "everyone" (TMM p.1).
4. **Privacy/safety:** the TMM cites them explicitly (p.1); the DZ treats privacy as compliance and a requirement (DZ p.35, 37, 228).
5. **"Good enough" criterion:** the DZ gives risk appetite and acceptance level (DZ p.33); the TMM only asks (p.1) without a criterion.

## F. Common mistakes when using this collection [inference]
- Attributing STRIDE/DFD to the TMM or the DZ (they are in neither).
- Saying the DZ is a DZone compilation (it is a single-author Packt book).
- Citing ISO 27001 Annex A numbers/controls as current (see `datado-desde-2021.md`).
- Using the example impact scale (% of revenue) as a universal standard (the author says it is an example, DZ p.28-29, 31).

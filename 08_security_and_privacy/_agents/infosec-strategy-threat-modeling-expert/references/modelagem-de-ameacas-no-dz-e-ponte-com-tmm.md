# Threat modeling: what the DZ says, what the TMM says and how to link the two

Sources: **TMM** (3 pages) and **DZ** (Packt, MacMillan, 2021). Citations: PDF page.

## 1. Where the DZ uses the expression "threat modeling"
Verified by searching the whole text (six occurrences in the body, plus one in the index):
| Where | DZ's sense | Page |
|---|---|---|
| Ch.1, when dealing with threats | Activity of **documenting threats and actors per asset** (actor: capability, interest, tactics; standard set of three actors + environmental) | DZ p.25 |
| Ch.3, opening | "Plan and threat-model the implementation" to ensure fitness for purpose, together with secure design principles | DZ p.80 |
| Ch.3, motivations | Consider insiders (malicious and accidental) "when threat modeling the organization" | DZ p.82 |
| Ch.3, Ketchup example | The company "was starting to model" the threat of corporate espionage (Ch.1) | DZ p.84 |
| Ch.7, detection strategy | List item of the risk-based strategy: asset prioritization, **threat modeling**, detection and response budget | DZ p.213 |
| Ch.8, SDLC requirements | **Abuse cases** = forms of malicious use; "essentially threat modeling" with attention to the attack surface; mitigate in proportion to the risk | DZ p.228 |
The DZ does **not** present a threat modeling method (no steps, no system diagrams, no threat categories, no session format). The index points to printed p.211 (= PDF 228) for the term.

## 2. Difference in meaning between the DZ and the TMM (important)
- **TMM p.1:** threat modeling = *analyzing representations of a system* to highlight security and privacy concerns, through four questions; it is a collaborative, iterative and continuous practice.
- **DZ p.25:** threat modeling ≈ *catalog of threats and actors per asset* within the risk process; DZ p.228: abuse cases of the requirement.
- **[inference]** The DZ covers **"what can go wrong" at the asset and actor level** and the rest of the risk assessment (impact, likelihood, treatment); the TMM covers the **human and iterative process** of analyzing the *system*. They do not contradict each other, but they are **not the same object**: do not attribute the four questions to the DZ, nor the 5×5 matrix to the TMM.
- **TMM p.1:** includes **privacy** and *safety* alongside security; the DZ treats privacy mainly as compliance and process (DZ p.35, 37) and includes "privacy requirements" in the SDLC (DZ p.228). For deeper privacy coverage: `privacy-lgpd-engineering-expert`.

## 3. Map of the TMM's four questions to the DZ content (inference)
| TMM question (p.1) | DZ inputs (page) | Nature |
|---|---|---|
| 1. What are we building? | asset register and crown jewels (24); ISMS context and scope (51-52); inventory and owner (56); classification (57); diagram of SCADA connections (109); list of hosts, services, network baseline (214-215); SDLC: requirements and user stories (228, 231) | [inference] |
| 2. What can go wrong? | actors and motivations (25-26, 82-85); vulnerabilities by asset class (86-89); exploitation methods (90-96); attacker steps (85, 105); abuse cases and misuse stories (228, 235); events, incidents and nonconformities (207) | [inference] |
| 3. What are we going to do about it? | treatment: avoid/reduce/transfer/accept (33); control types and order of defense in depth (70-72); least privilege, JIT, Zero Trust, secure by design (103-105); controls x risks (106-107) | [inference] |
| 4. Did we do a good enough job? | residual risk vs. acceptance (34); control testing and retesting (98, 189); assessments (170-190); internal validation before retesting (189); ISMS review and corrective action (64-65); continuous improvement (22, 44, 219) | [inference] |
**Label:** this map is a construct of the agent. Neither the DZ nor the TMM states it.

## 4. TMM values/principles applied to DZ practices (inference)
- **A culture of finding and fixing > checkbox (TMM p.1):** the DZ also criticizes "tick a box" compliance (DZ p.174) and documentation only for auditors (DZ p.89).
- **People and collaboration > processes (TMM p.1):** the DZ values dialogue with IT (DZ p.205), approachable security (DZ p.90), executive sponsorship (DZ p.64), but its backbone is a documentary system (ISMS, DZ p.49-55). **Tension** (see `casos-e-antipadroes.md`): the DZ bets more on process and documents than the TMM does.
- **Early and often (TMM p.2):** DZ p.80 ("from the start"), p.228-229 (requirements and design), p.232-233 (tests in the pipeline).
- **Align with development practices, small iterations (TMM p.2):** DZ p.227-228 (SDLC with Agile and DevOps) and p.231 ("short" test tied to the user story).
- **Value for stakeholders (TMM p.2):** DZ p.48-49 (business case and risk communication template), p.44-45 (reporting without jargon).
- **Dialogue + documents (TMM p.2):** DZ p.189 (presentation of findings) + ISMS records (DZ p.55).
- **Anti-pattern Hero Threat Modeler (TMM p.2):** DZ p.41 and p.64 (train and do not depend on a single person).
- **Anti-pattern Admiration for the Problem (TMM p.2):** DZ p.189 (plan resources and remediate) and p.206 (security improvement program).
- **Anti-pattern Perfect Representation (TMM p.2):** no counterpart in the DZ.
- **Pattern Useful Toolkit (TMM p.2):** the DZ uses tools (DLP, SIEM, scanners, IaC) with the caveat of defining requirements before choosing (DZ p.217).

## 5. STRIDE, DFD and other techniques: **[extrapolation]**
Neither the TMM nor the DZ contains STRIDE, DFD, attack trees, DREAD, PASTA, LINDDUN or trust boundaries (verified: absent from the text of both; "data flow" appears in the DZ only in TCP/IP figures, p.115 and 116). If the user asks, the agent may offer, **marked [extrapolation]**:
- *Representations*: data flow diagram with external actors, processes, data stores and flows, and trust boundaries; STRIDE as a list of categories for question 2. This is consistent with TMM p.2 (several representations, method-agnostic), but it is **not from the text**.
- Recommendation: use as an *optional starting point*, always with the warning that the TMM is method-agnostic and that there are other techniques.
Scripts: `scripts/threat_model_session.py template --extrapolation` produces the labeled optional block.

## 6. Limits of this area
For application threat modeling with ASVS (verification requirements, architecture), refer to `owasp-asvs-code-review-expert`; for how to test a web application, `owasp-web-security-testing-expert`; for adversaries in security engineering (policy/protocol model), `security-engineering-expert`; for privacy (LINDDUN, LGPD), `privacy-lgpd-engineering-expert`.

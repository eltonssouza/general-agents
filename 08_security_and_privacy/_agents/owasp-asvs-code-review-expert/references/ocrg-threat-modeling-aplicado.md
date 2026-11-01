# OCRG — threat modeling applied to code review (OCRG p.32-39, 201-205)

Source: OCRG v2.0, section 6.9 and Appendix B. Pages = PDF (printed = N − 1). Related in the ASVS: V1.1.2, V1.1.4, V1.1.5 (ASVS p.17) and V11.1.5 (ASVS p.54) — mapping `[inference]`.

## The role of threat modeling in review (OCRG p.32)
- [from source] Threat modeling is **not a code review approach**, but it complements the review by giving **context and risk analysis**; it shows entry points (attack surface) and associated vectors (OCRG p.32).
- [from source] On existing code (outside the S-SDLC), the model's result reduces the complexity of the analysis: instead of reviewing everything with the same focus, **prioritize components whose threats were ranked as high risk** (OCRG p.32). The modern model looks from the attacker's point of view, not only the defender's (OCRG p.32).
- Three steps: decompose the application; determine and rank threats; determine countermeasures and mitigation (OCRG p.32-39).

## Step 1 — decompose the application (OCRG p.32-36)
- [from source] Understand the application and its interactions with external entities: use cases, **entry points**, **assets**, **trust levels** and data flow diagrams (DFD) with the privilege boundaries (OCRG p.32).
- [from source] Items: **external dependencies** (outside the code, perhaps outside the team's control; document the expected production environment, e.g. a hardened server behind a firewall) (OCRG p.33); **entry points** (interfaces through which the attacker interacts or supplies data; can be layered) (OCRG p.33); **assets** (physical or abstract, such as reputation) (OCRG p.33); **attack surface** (inputs, data flows and transactions) (OCRG p.33).
- [from source] Inputs to map (the book's list): browser input, cookies, property files, external processes, data feeds, service responses, flat files, command-line parameters and environment variables (OCRG p.33). Figure 4: process of identifying input paths (follow each parameter through the code; late/dynamic binding areas; references to configuration files) (OCRG p.34).
- [from source] **Trust levels**: access rights granted to external entities; crossed with entry points and assets (OCRG p.35). **Data flow analysis** (where variables are defined and used) and **transaction analysis** (validation of untrusted sources, authentication, session, authorization, encryption at rest/in transit, errors/leakage, logging/auditing) (OCRG p.35).
- [from source] **DFDs** are hierarchical; symbols (Table 7): process, external entity, multiple process, data flow, privilege boundary, data store; trust boundaries mark where the trust level changes; entry and exit points define a boundary (OCRG p.35-36).

## Step 2 — categorize and rank threats (OCRG p.36-39)
- [from source] Use a categorization: **STRIDE** (attacker perspective: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) or **ASF** (Application Security Frame, defensive perspective: auditing/logging, authentication, authorization, configuration management, data protection in storage/transit, data validation and exception management) (OCRG p.36). Use cases and **abuse cases** show how protections are bypassed or where they are missing (OCRG p.36-37). Threat trees (one per objective) can go deeper (OCRG p.36-37).
- [from source] Table 8 (STRIDE in the book's context): spoofing (users must not become another user; single execution context with many users), tampering (client alters returned data; validate), repudiation (without auditing, transaction dispute), disclosure, DoS (expensive resources only for authenticated/authorized users), elevation of privilege (OCRG p.37). Exit points are also attack points (e.g. a login error message allows enumeration; XSS) (OCRG p.37-38).
- [from source] **Ranking**: DREAD (Damage, Reproducibility, Exploitability, Affected Users, Discoverability) with questions per factor (Table 9) (OCRG p.38) **or** a qualitative model; the book **prefers qualitative values (High/Medium/Low)** so the ranking does not become excessively subjective (OCRG p.39). Conceptual formula: **Risk = Likelihood x Impact**, "not meant to use real values" (OCRG p.39). Likelihood depends on ease of exploitation and on whether a countermeasure exists (OCRG p.39).

## Step 3 — countermeasures (OCRG p.39)
- [from source] A threat with no countermeasure indicates a vulnerability; order by risk and prioritize. Risk responses: apply a countermeasure/change the design, accept (acceptable impact with compensating controls), inform the user, remove the risk entirely, or (less desirable) do nothing; if the risk is extreme, discontinue the feature/product (OCRG p.39). Map threat → countermeasure by category; the set of documents is the threat model (OCRG p.39).
- Types of mitigated threat (Table 10): unmitigated, partially and fully mitigated (OCRG p.40).

## Appendix B — example (college library site) (OCRG p.201-205)
- [from source] The model documents: **general information** (name, version, description, owner, participants, reviewer) (OCRG p.201); **entry points** (ID, name, description, trust levels; major.minor notation for layers) (OCRG p.202); **assets** (ID, name, description, trust levels) (OCRG p.202); **trust levels** (ID, name, description) (OCRG p.203); DFD of the site (user/web server and web server/database boundaries) and DFD of the login (OCRG p.203-204).
- [from source] DREAD ranking example: threat "malicious user views confidential information": Damage 8, Reproducibility 10, Exploitability 7, Affected users 10, Discoverability 10 → (8+10+7+10+10)/5 = **9** on a scale of 10, "high risk" (OCRG p.205).

## How to use in review (summarized procedure — see `references/procedimentos.md`)
1. For a high-risk module, require/produce the threat model; for low risk, the preparation items are enough (OCRG p.27).
2. Cross entry points x assets x trust levels to decide **where** each control must exist.
3. Turn each ranked threat into a review target (e.g. spoofing at login → A2/session; tampering → validation and CSRF; repudiation → logging) and into ASVS requirements (V1.1.2, V11.1.5) `[inference]`.
- Boundary: **threat modeling methodologies beyond what the OCRG documents** (LINDDUN, PASTA, formal attack trees) and the Threat Modeling Manifesto belong to other agents/sources; here only what the OCRG provides (terms such as LINDDUN and "attack tree" are absent from the OCRG, although "threat trees" appear in OCRG p.36).

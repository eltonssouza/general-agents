# Risk and governance (DZ Ch.1, PDF p.20-45; printed p.3-28)

Source: **DZ** = *Infosec Strategies and Best Practices*, Joseph MacMillan, Packt, 2021 (see INDEX for identification). Citations: PDF page (printed = PDF − 17). Paraphrase is mine.

## Base terms
- **[from source] (DZ p.21)** "Organization" covers any structure (company, government, NGO...). "Information" includes data, common knowledge and intellectual property (e.g. a slogan written on a whiteboard).
- **[from source] (DZ p.22)** CIA triad: confidentiality, integrity, availability, seen as an interconnected system. The forgotten "N" is **non-repudiation** (indisputable proof of authorship/origin).
- **[from source] (DZ p.24)** Asset = anything of value to the organization (digital, physical, reputational). Without an asset there is no risk. Start with the "crown jewels" in an **asset register** (ID, short name, description, notes; optional: owner, classification, value).

## Definition of risk
- **[from source] (DZ p.23)** Risk = potential for loss, measured by the combined impact and likelihood of a threat exploiting a vulnerability in information assets. Components: assets, threats, vulnerabilities, likelihood and impact. Simplified formula: **Risk = Impact × Likelihood**.
- **[from source] (DZ p.23)** Risk management: identify, assess and prioritize risks and apply layers of controls that reduce impact and likelihood. It is not about eliminating all risk nor about bureaucracy; it provides transparency and accountability and aligns risk with strategic objectives.
- **[from source] (DZ p.26)** Vulnerability = weakness of the asset that can be exploited by a threat.

## Threats and actors (author's view, not the TMM)
- **[from source] (DZ p.25)** Each asset can have several threats; each actor has different goals and capabilities. The author calls *threat modeling* the activity of **documenting threats and actors per asset** (see `modelagem-de-ameacas-no-dz-e-ponte-com-tmm.md`).
- **[from source] (DZ p.25)** Initial set of threats: malicious outsiders, malicious insiders and accidental insiders (have actors); environmental threats have no actor. When thinking about actors, consider **capability, interest and tactics**.
- **[from source] (DZ p.25-26)** Outsiders can be subdivided: solo (beginner or experienced), group (hacktivists, organized crime, competitors) and state (more sophisticated, specific interests). There is no right way: create a *placeholder* for actors not relevant today.
- **[from source] (DZ p.26)** Environmental events (hurricane, flood) have no interest or tactics, but affect availability or cause data loss; assess whether your assets are exposed (e.g. a basement that can flood).

## Basic risk assessment ("Ketchup Company" example)
- **[from source] (DZ p.27)** Scenario: secret recipe on a NAS accessible via the web without username/password; a leak would cost more than 5% of annual revenue.
- **[from source] (DZ p.28-29)** Starting impact scale (text p.28; table in figure p.29, read visually): negligible (1) = up to US$ 300 per occurrence; low (2) = 0-1% of annual revenue; medium (3) = 1-3%; high (4) = 3-5%; catastrophic (5) = 5% or more. Percentage of revenue may not be the best metric (alternatives: value ranges, % of net profit, p.29).
- **[from source] (DZ p.29)** Likelihood scale (table in figure, read visually): unlikely (1) = once every 10+ years; not very likely (2) = 7-9 years; possible (3) = 4-7 years; likely (4) = 2-3 years; certain (5) = once a year or more.
- **[from source] (DZ p.30-31)** Likelihood by history (has it happened? how often? when was the last time?) or, without history, by analysis of the actor's motivation and capability and of exposure. In the example, likelihood = 5.
- **[from source] (DZ p.31-33)** 5×5 matrix (x axis impact, y axis likelihood; score 1 to 25; figure p.32 shows the acceptance line). Example: 5 × 5 = 25.

## Appetite, treatment and acceptance
- **[from source] (DZ p.33)** Risk appetite = acceptable level defined by stakeholders. If a risk of 25 bothers nobody, the impact/likelihood tables do not reflect the appetite. In the example the acceptance line is at 7 (above 7 requires treatment).
- **[from source] (DZ p.33)** Treatment: **avoid** (remove the likelihood, by not performing the action), **reduce** (impact or likelihood, through controls), **transfer** (outsourcing, insurance), **accept** (acknowledge that it needs no further mitigation or that further mitigation is infeasible).
- **[from source] (DZ p.34)** Residual risk = risk after the control; below the acceptance level it is acceptable. Record each risk in a **risk register** (this starts building the ISMS).
- **[from source] (DZ p.44)** Keep old versions of the risk register (per quarter, half-year or year) to show progress; report to stakeholders without jargon ("how much it costs, how much it saves"), ROI can be shown via the risk report; give each audience a reason to care (p.45).

## Compliance, investigation and continuous improvement
- **[from source] (DZ p.35)** Requirements come from laws and from certification bodies: GDPR, COPPA, HIPAA, CCPA (and the author cites Brazil as a jurisdiction); most ask for transparency and data subject rights. ISO standards (27001 management; 27018 cloud privacy) allow third-party certification.
- **[from source] (DZ p.36)** Certifications are worth a lot in B2B. Compliance management tools help, but many requirements cannot be automated (e.g. disabling accounts when an employee leaves); you need to work with all teams, including legal and HR, and run internal audits ("say what you do and do what you say"). [DATED: numbers "200 updates/day, 750 agencies".]
- **[from source] (DZ p.37)** Policies and controls need regular review (some standards require annual proof). Example: migrating PII to the cloud requires mapping the type and reason of processing, legal basis, updating policies and notifying data subjects; access and deletion requests within the deadline; SOX (retention of financial records for up to 7 years) and FISMA as other examples.
- **[from source] (DZ p.38)** Investigations: legal hold, do not actually delete, pseudonymization to avoid investigator bias/collusion, eDiscovery. Do not obstruct investigations.
- **[from source] (DZ p.39-40)** Continuous improvement illustrated: a restore simulation reveals lack of space and RAID-0; the risk register is updated, the risk is assessed, mitigated incrementally (RAID-1), reassessed and the economic impact is presented.
- **[from source] (DZ p.41)** Training: new members sign an agreement renewed annually; train so the business does not depend on a key person. The author rejects blaming the phishing victim and asks whether there was training, simulation and a safe way of working.
- **[from source] (DZ p.42-44)** Third-party risk: shared responsibility; legally binding SLAs work as a control (they compensate the financial loss of availability); **VSAQ** (vendor security questionnaire) at purchase, with risk as the backbone; due diligence + due care documented; see `ativos-isms-e-politicas.md`.
- **[from source] (DZ p.44)** Defense in depth ("lock it twice") does not reduce risk by itself, but lets one control fail while the residual stays reduced; complexity is the enemy of security.

## Heuristics (inference)
- **[inference]** Before scoring, calibrate the scales with stakeholders; if the appetite does not "match" the scale, the problem is the scale (DZ p.33).
- **[inference]** Without incident history, likelihood is structured judgment; record the assumption (motivation, capability, exposure).

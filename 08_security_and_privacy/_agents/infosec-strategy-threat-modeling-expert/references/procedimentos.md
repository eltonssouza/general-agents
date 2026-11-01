# Procedures (step by step)

Sources: **DZ** (MacMillan, 2021; PDF page, printed = PDF − 17) and **TMM**. Each procedure says what is **[from source]** and what is **[inference]** (my organization). Scripts: see `scripts/` (INDEX).

## P1. Basic risk assessment (DZ p.27-34)
1. **[from source]** List assets (asset register) starting with the crown jewels (p.24, 28).
2. **[from source]** For each asset, identify threats and actors (capability, interest, tactics) and vulnerabilities (p.25-26).
3. **[from source]** Define with stakeholders the impact scale (e.g. % of revenue) and the likelihood scale (1 to 5; 5 = once a year or more) (p.28-29).
4. **[from source]** Determine impact and likelihood (history or, without it, motivation, capability and exposure) (p.30-31).
5. **[from source]** Calculate Risk = Impact × Likelihood and place it on the 5×5 matrix (p.32-33).
6. **[from source]** Compare with the appetite (in the example, > 7 is unacceptable); treat (avoid, reduce, transfer, accept); reassess the residual risk; record it in the risk register (p.33-34).
7. **[from source]** Repeat when the asset/threat changes and at least as the methodology says (e.g. annually) (p.31, 59). Script: `risk_matrix.py`.

## P2. Build an ISMS (DZ p.46-65)
1. **[from source]** Obtain senior management sponsorship and translate business objectives into IT/security objectives (p.47-48).
2. **[from source]** Document the organizational context and scope (p.51-52).
3. **[from source]** Do the risk assessment and fill in the SoA with justification per control (p.52-53).
4. **[from source]** Write the security policy, roles, legal/contractual requirements, internal audit, corrective action (p.54-55).
5. **[from source]** Asset management: inventory, classification, labeling, handling, acceptable use (p.55-58).
6. **[from source]** Risk: assessment and treatment methodologies, report (p.58-60); third parties (p.61); incidents and BC (p.61-62); IT documents (p.63).
7. **[from source]** Train, evaluate effectiveness (annually), audit, correct and improve (p.64-65).
Script: `strategy_checklist.py` (ISMS area).

## P3. Communicate risk to senior management (DZ p.48-49, 44-45)
**[from source]** Use the template: possible annual loss; system; threat; mitigation; cost (monthly/annual); timeline. **[from source]** No jargon; "how much it costs, how much it saves"; adapt to the audience (CFO ≠ CTO). **[inference]** Complete with the expected residual risk and the decision requested (approve, accept or reject).

## P4. Information asset lifecycle (DZ p.55-60, 75-77)
**[from source]** Inventory → owner → classification → labeling → secure handling → monitor changes in value → retention → disposal (defensible destruction) or archive, with a record of disposals.

## P5. Select controls (DZ p.70-72, 101-102)
**[from source]** (1) The asset's risk level (likelihood and impact) and (2) knowledge of how the control is applied per vector; cover the relevant vectors, without useless complexity. **[from source]** Combine classes (administrative, physical, technical, operational) and functions (deter, prevent, detect, delay, correct, recover). **[from source]** Test the control after deploying it (p.98).

## P6. Vendor/software due diligence (DZ p.25-27, 43-44, 225-226, 243-248)
1. **[from source]** Require binding SLAs and, if possible, liability clauses and vulnerability remediation clauses.
2. **[from source]** Send a VSAQ (or CAIQ); take the answers into account in the purchase, with risk as the backbone.
3. **[from source]** Ask how the vendor follows the SDLC and request evidence; request a pentest report or bug bounty.
4. **[from source]** Document the residual risk and decide to mitigate, accept or avoid; keep everything as evidence (due care).
5. **[from source]** On-prem: question the privileges required and include it in the scan.

## P7. Plan and run an assessment (DZ p.172-189)
1. **[from source]** Senior management buy-in; regulatory requirements; define why, what, time, deadline, budget.
2. **[from source]** Prefer a clone environment with fictitious data for scans/some pentests; handle the trade-off of acceptance by certification bodies.
3. **[from source]** Agree on terms (NDA, do not take production down); defined time and scope.
4. **[from source]** Hold the findings meeting, validate the fix internally, retest and schedule a new cycle.

## P8. Incident response plan (DZ p.61-62, 207-212)
**[from source]** Define what an event/incident/nonconformity is (p.207); roles and duties; prioritization by risk; documentation; notification (p.208-209); stages: investigate, confirm, respond/contain, restore, investigate and report (p.209); minor/major incident (p.210); simple playbooks; tabletops with curveballs; keep the plan somewhere accessible during an outage (p.61-62). **[inference]** The book does not provide a literal template; the script organizes these items (see `strategy_checklist.py`).

## P9. Change control (DZ p.205-206, 195-196)
**[from source]** Describe and justify; impact and mitigation; rollback; recorded approvals; communication and window; implement and evaluate; document user, time, change and systems; separation of duties; aligned environments.

## P10. Security improvement program (DZ p.206)
**[from source]** Define improvements, schedule and effectiveness test; conscious decision to deprioritize features; plan of time, cost, risks and gains for the buy-in; communicate that the directive comes "from above".

## P11. Adopt SIEM/SOC (DZ p.213-219)
**[from source]** Risk-based strategy (assets, threat modeling, detection and response budgets); requirements, deadline and flow before choosing; pilot with a reasonable scope; scale (EPS, GB/day); compliance and retention; rules and what not to collect (PII, card, passwords, keys); test rules and notifications; log backup; review recurrently.

## P12. DevSecOps pipeline (DZ p.232-233, 250-251, 199-201)
**[from source]** Branch + IDE that checks secrets; authorized and logged commit; CI: dependencies, SAST, secrets, IaC/container audit, DAST in an ephemeral environment; code review; human testing; merge and CD; least privilege (no changes to production outside the pipeline); non-compliant infrastructure is blocked.

## P13. Threat modeling session with the TMM
Summary (detail and template in the script `threat_model_session.py template`):
1. **[from source, TMM p.2]** Choose a **manageable portion** of the system and align with the development practice (iteration). Invite varied viewpoints (Varied Viewpoints pattern).
2. **[from source, TMM p.1]** Question 1, *what are we building?*, with **one or more representations** (TMM p.2: there is no single ideal view).
3. **[from source, TMM p.1]** Question 2, *what can go wrong?* (the technique is up to you: method-agnostic; STRIDE etc. = **[extrapolation]**).
4. **[from source, TMM p.1]** Question 3, *what are we going to do about it?*; arrive at practical actions (anti-pattern Admiration for the Problem).
5. **[from source, TMM p.1]** Question 4, *did we do a good enough job?* Criterion defined by the group and the stakeholders **[inference]**, because the TMM gives no numeric criterion.
6. **[from source, TMM p.2]** Document the understandings for record and measurement; deliver value to stakeholders; schedule the next iteration (TMM p.1: continuous refinement).
7. **[inference]** Feed the DZ risk register (p.34) with the prioritized threats and reuse the organization's impact/likelihood scale.

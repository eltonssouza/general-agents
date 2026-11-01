# Assets, ISMS and policies (DZ Ch.2, PDF p.46-77; printed p.29-60)

DZ citations = PDF page (printed = PDF − 17). Paraphrase is mine.

## Chapter structure (DZ p.46-47)
Four stages: (1) implement an ISMS; (2) identify and classify assets; (3) protect according to value, monitor changes and adapt; (4) dispose (archive or destroy). The ISMS gathers the processes that identify and classify assets and apply controls with defense in depth for C, I and A.

## Role of senior management
- **[from source] (DZ p.48)** Ultimately the responsibility lies with senior management (it hires the security professional and communicates the strategic objectives to which the security requirements align). The professional must turn risk into an understandable **business case** and adjust the language to the audience (IT: technical; business: organizational impact). The author criticizes excessive technical description.
- **[from source] (DZ p.49)** Template for communicating risk to the C-level: how much can be lost per year; which system to protect; against which threat; with which mitigation (e.g. WAF); monthly/annual cost; implementation time. [The example values are illustrative.]
- **[from source] (DZ p.64)** Policies need sponsorship from executives (CEO/CTO...) and consequences for those who do not follow them; without communication, users work around controls.

## What the ISMS is and what it contains
- **[from source] (DZ p.49)** ISMS = a defined and systematic approach to discover, measure, contain and mitigate information security risk, with risk at the center of decisions; formalized documents (policies, procedures, baselines, guidelines) defined by business needs. The security team is responsible for keeping it functional.
- **[from source] (DZ p.50)** The structure is not fixed; the author uses **ISO/IEC 27001** as the backbone. Document topics: how to create and update policies; how to identify, classify, monitor and dispose of assets; how to measure risks and choose controls; levels of residual and unmitigated risk. Also Risk Assessment Methodology, Risk Treatment Methodology/Plan and Risk Assessment Report.

### High-level documents (DZ p.51-54)
- **Organizational context (DZ p.51-52):** nature (products, growth, threats, suppliers, legislation), assets/information (PII, PHI, IP, financial; systems) and people (recruitment, training, role change and departure).
- **ISMS scope (DZ p.52):** align it with the organization's scope; processes can be declared out of scope (e.g. third parties outside your control) as long as the third-party practices are within the risk appetite; certification bodies prefer the whole organization, but it is not mandatory; "do what you say and say what you do".
- **Statement of Applicability, SoA (DZ p.52-53):** summary of the relationship between risks and controls, in a table; it can only be completed after the risk assessment; each control is applicable-implemented, applicable-not implemented or not applicable, **with justification**. The author cites ISO 27001 Annex A as "114 controls in 14 categories" and ISO 27002 as an implementation guide. **[DATED]** the ISO/IEC 27001:2022 edition reorganized Annex A (extrapolation: 93 controls in 4 themes; confirm in the current standard).
- **Information security policy (DZ p.54):** measurable objectives for C, I and A; approved by management, published and communicated; it must be applicable (a document nobody follows is useless); commits to continuous improvement.
- **Others (DZ p.54-55):** roles and responsibilities; legal, regulatory and contractual requirements; internal audit; corrective action (how and by whom problems are discovered, reported, documented and handled); and records: BIA, training, monitoring/measurement, internal audit, management review, corrective action, activity/exception/event logs.

### Asset management (DZ p.55-58)
- **[from source] (DZ p.55-56)** Four-step cycle, mapped to ISO 27001 (2013 numbering, **[DATED]**): inventory (A.8.1.1), classify by legal requirements, value, criticality and sensitivity (A.8.2.1), label (A.8.2.2), handle securely (A.8.2.3).
- **[from source] (DZ p.56)** Inventory: categorize, prioritize, **asset owner** (has the responsibility and authority to protect; may delegate day-to-day). A criticality score is not an ISO 27001 requirement: use it if useful; keep it up to date.
- **[from source] (DZ p.57)** Classification: usually around four levels; example *Confidential, Restricted, Internal, Public*; the owner classifies; physical and digital labeling defined in the policy.
- **[from source] (DZ p.57-58)** Acceptable use policy: rules for employees, contractors and third parties (general use, email, laptops and mobile devices, third-party software, return of assets on termination, removable media, secure media disposal); part of training and accessible to everyone.
- **[from source] (DZ p.58-60)** Documented risk management: identify, assess/prioritize, treat (with evidence) and monitor/review (includes management review). The methodology defines when (e.g. annually or on significant change), who, the scales, and whether the approach is by threat scenario or by asset. Two-tier risk report: overview for senior management (main assets, inherent risk, treatment, residual) and detailed (status per asset and per SoA control).
- **[from source] (DZ p.61)** Third-party documents: SLAs, VSAQ, due care; catalog of assets managed by third parties; shared responsibility.
- **[from source] (DZ p.61-62)** Incidents: incident management policy (roles, threshold to declare an incident, references to playbooks), kept somewhere accessible even with the systems down (ransomware on the NAS; flooded printed copy). Simple playbooks like a "picture book", per scenario; **tabletop exercises** (cheap) with "curveballs".
- **[from source] (DZ p.63)** IT documentation referenced by the ISMS: operating procedures, secure engineering, access control, BYOD, passwords, disposal, maintenance, changes, backup, testing, information transfer, secure areas, clean desk/screen; they must reflect reality.
- **[from source] (DZ p.64-65)** ISMS effectiveness: regular review (e.g. annual) and internal audit; nonconformities go to corrective action; day-to-day conversations feed improvement. **Shadow IT** = IT deployed without IT oversight, which bypasses controls.

## Classification, roles and automatic protection
- **[from source] (DZ p.66-67)** Define roles per asset; the table (figure, p.67, read visually) lists: *Information Owner* (protects the data and ensures classification), *System Owner* (software and hardware configurations that process/store the information), *Information Custodian* (backups and restoration), *Security Administrator* (assigns network permissions), *Users* (comply with policies) and *User Manager* (supervises the other roles). There can be several owners and one system owner per vendor. Use KISS: small companies may not have dedicated roles.
- **[from source] (DZ p.68-69)** Manual identification/classification does not scale. **DLP / Information Protection** discovers and classifies automatically (ready-made templates, such as a card number in a chat or a passport in an image; custom templates, with regex and keywords), applies a metadata label, access restriction, encryption, watermark and user warnings. The asset owner remains responsible for ensuring the classification. The plain-language policy guides the choice of technology. Physical documents: classification at the top right of each page and on the cover/envelope.
- **[from source] (DZ p.69-70)** Retention: many jurisdictions limit retention time; define what to retain, for how long, how to search and who owns it; technology prevents improper disposal and forces disposal on schedule (e.g. remove access after 7 years of inactivity).

## Control classes and types (DZ p.70-72)
- **[from source] (DZ p.70-71)** By nature: administrative/managerial, physical, technical/logical, **operational** (training, asset classification, log review). Extra reference: NIST SP 800-53 Rev.5 (mappings to ISO 27001).
- **[from source] (DZ p.71)** By function: preventive, detective, deterrent, corrective (includes fail open/fail closed), recovery and **compensating**.
- **[from source] (DZ p.71-72)** Suggested order for defense in depth: deter, deny/prevent, detect (and log), delay, correct, recover.
- **[from source] (DZ p.72)** Re-evaluate controls when the asset's value changes; think about recovery (backup, redundancy, restoration). SLAs with maximum downtime and penalties are a compensating control; chaining third-party services increases availability risk.

## Data and cryptography (DZ p.72-74)
- **[from source] (DZ p.72-73)** States: in transit, at rest, in use (non-persistent memory).
- **[from source] (DZ p.73)** Cryptography is almost mandatory (PCI-DSS, ISO 27001): TLS in transit, AES-256 at rest (the author's examples); hashing for integrity and for storing passwords without clear text.
- **[from source] (DZ p.74-75)** Example of defense in depth for an internal web app (authentication and authorization, salted hash, version control with 2FA, static and dependency analysis, vulnerability scanner, logging/monitoring, firewall with IP allowlist, WAF, load balancing/multi-site). Whether it is enough depends on the risk appetite.

## Disposal (DZ p.75-77)
- **[from source] (DZ p.76)** ISO 27001 (A.8.3.2, A.11.2.7): formal media disposal and verification of removal/overwriting before disposing of or reusing; keep a record. **Data remnants**: deleting marks space as free without erasing. **Defensible destruction**: overwrite (the author cites a US standard of "at least seven times", **[DATED]**, confirm with current media sanitization guidance), degauss, encryption with key destruction (cryptoshredding), physical destruction.
- **[from source] (DZ p.77)** Disposal can also mean **archiving** in cheap storage, respecting legal retention.

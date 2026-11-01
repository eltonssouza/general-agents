# Glossary (author's terms, with page)

DZ = *Infosec Strategies and Best Practices* (MacMillan, Packt, 2021), PDF page (printed = PDF − 17). TMM = *Threat Modeling Manifesto* (3 pages). Definitions are paraphrased.

## From the TMM
| Term | Meaning | Page |
|---|---|---|
| Threat modeling | Analyzing representations of a system to highlight security and privacy concerns | TMM p.1 |
| Four questions | What are we building? / What can go wrong? / What are we going to do about it? / Did we do a good enough job? | TMM p.1 |
| Threats | The output of threat modeling; informs design, development, testing and post-deployment decisions | TMM p.1 |
| Value | Something with relative merit; the item on the left is valued more | TMM p.1 |
| Principle | Fundamental truth; three types: general truths, recommended patterns, anti-patterns | TMM p.1 |
| Systematic Approach | Rigor and repeatability with structured knowledge | TMM p.2 |
| Informed Creativity | Creativity with craft and science | TMM p.2 |
| Varied Viewpoints | Diverse team and cross-functional collaboration | TMM p.2 |
| Useful Toolkit | Tools that provide productivity, repeatability and measurability | TMM p.2 |
| Theory into Practice | Field-tested techniques, aware of their limits | TMM p.2 |
| Hero Threat Modeler | Anti-pattern: depending on innate skill or on a single person | TMM p.2 |
| Admiration for the Problem | Anti-pattern: analyzing without arriving at practical solutions | TMM p.2 |
| Tendency to Overfocus | Anti-pattern: losing the big picture or overemphasizing adversaries, assets or techniques | TMM p.2 |
| Perfect Representation | Anti-pattern: seeking a single ideal representation | TMM p.2 |

## From the DZ
| Term | Meaning | Page |
|---|---|---|
| Organization | Any structure (company, government, NGO...) | DZ p.21 |
| Information | Data, common knowledge and IP | DZ p.21 |
| CIA triad (+ N) | Confidentiality, integrity, availability; "N" = non-repudiation | DZ p.22 |
| Risk | Potential for loss = impact and likelihood of a threat exploiting a vulnerability in an asset | DZ p.23 |
| Risk = Impact × Likelihood | Author's simplified formula | DZ p.23 |
| Asset / asset register | Something of value / list of assets (ID, name, description, notes...) | DZ p.24 |
| Threat actor | Perpetrator of a threat (capability, interest, tactics) | DZ p.25 |
| Vulnerability | Exploitable weakness of the asset | DZ p.26 |
| Risk appetite / acceptance level | Acceptable level of risk defined by stakeholders | DZ p.33 |
| Risk treatment | Avoid, reduce, transfer, accept | DZ p.33 |
| Residual risk | Risk after the control | DZ p.34 |
| Risk register | Record of the organization's risks | DZ p.34 |
| ISMS | Information security management system: systematic approach to risk with formal documents | DZ p.49 |
| Statement of Applicability (SoA) | Risk-control table with status and justification | DZ p.52-53 |
| Asset owner / Information Owner | Owner responsible for and with authority over the asset / the classification | DZ p.56, 66 |
| Shadow IT | IT deployed without IT oversight | DZ p.65, 194 |
| DLP / Information Protection | Technology for automatic discovery, classification and protection | DZ p.68 |
| Defensible destruction | Controlled, lawful and compliant destruction of data | DZ p.76 |
| Cryptoshredding | Making data unrecoverable by discarding the key | DZ p.76 |
| Administrative / Physical / Technical / Operational controls | Control classes by nature | DZ p.70-71 |
| Preventive / Detective / Deterrent / Corrective / Recovery / Compensating | Control types by function | DZ p.71 |
| Defense in depth | The failure of one control does not eliminate protection; it reduces residual risk even with a failure | DZ p.44, 57 |
| APT | Highly capable and motivated actor, persistent access (NIST SP 800-39) | DZ p.85 |
| TCB | Components with a high impact on system security | DZ p.99 |
| Reference monitor / NEAT | Mechanism that enforces the access policy; non-bypassable, evaluable, always invoked, tamper-proof | DZ p.99 |
| Least privilege / JIT | Minimum and ephemeral access; ephemeral account on demand | DZ p.103 |
| Zero Trust | Least privilege + always verify + assume breach (NIST SP 800-207) | DZ p.104 |
| Secure by design | Building security in from the start | DZ p.104 |
| Security through obscurity | Security that depends on hiding; avoid | DZ p.105 |
| MAC / DAC / RBAC / ABAC | Access control models | DZ p.151-152 |
| Bell-LaPadula / Biba / Clark-Wilson / Brewer-Nash / Take-Grant | Formal access models | DZ p.147-150 |
| MFA | Distinct factors (know, have, are) | DZ p.154 |
| IAM | Identity and access management | DZ p.162 |
| VSAQ | Vendor security assessment questionnaire | DZ p.43, 246 |
| Due diligence / due care | Diligence before the decision / due care, documented | DZ p.43-44, 225 |
| Red / Blue / Black Team | Offensive / defensive / physical | DZ p.184-185 |
| Tabletop exercise | Room simulation to find gaps in plans | DZ p.62 |
| Event / Incident / Non-compliance | Event, incident and nonconformity (ISO 27001 definitions according to the author) | DZ p.207 |
| SIEM / SOC | Log aggregation and correlation / monitoring team | DZ p.88, 142-143, 214 |
| IaC / CCA / policy as code | Infrastructure as code / continuous configuration automation / machine-readable policies | DZ p.196-198 |
| SDLC / DevSecOps | Secure development lifecycle / security in the DevOps cycle via pipelines | DZ p.226-228, 250 |
| Abuse case / misuse story | Anticipated malicious use / story from the attacker's perspective | DZ p.228, 235 |
| Security improvement program | Organizational project of improvements with buy-in | DZ p.206 |
| Hot / warm / cold site | Readiness levels of the recovery site | DZ p.203 |

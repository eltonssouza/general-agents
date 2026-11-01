# Reference INDEX: infosec-strategy-threat-modeling-expert

## Sources (closed collection) and identification
| Code | Work | Verified identification | Pages |
|---|---|---|---|
| **DZ** | *Infosec Strategies and Best Practices: Gain proficiency in information security using expert-level strategies and best practices* | **Packt Publishing** book by **Joseph MacMillan** (Global Black Belt for cybersecurity at Microsoft; CISSP, CCSP, CISA, CSSLP, ISO 27001 Lead Auditor), reviewer Kyle Reidell; **first published in April 2021**; ISBN 978-1-80056-635-4 (DZ p.2, 3, 5, 6). **It is not a compilation of DZone articles/refcards**, even though the file is named `InfoSec-Strategy-DZone.pdf`: it is a **single-author** book (so there is no divergence *between authors*; I recorded internal tensions and DZ x TMM differences in `casos-e-antipadroes.md`). Audience: people starting in InfoSec roles and studying for CISSP/CISM (DZ p.14). | 272 PDF pages, native text |
| **TMM** | *Threat Modeling Manifesto* | Working-group manifesto with 15 authors (Braiterman, Shostack, Marcil, de Vries, Michlin, Wuyts, Hurlbut, Schoenfield, Scott, Coles, Romeo, Miller, Tarandach, Douglen, French), CC BY 4.0 license; PDF generated from the website on 17/11/2020 (metadata). Read **in full**. | 3 pages |

## Page convention
- **All citations use the PDF page** (the `=== PAGE N ===` marker of the extracted text; `DZ p.N`, `TMM p.N`).
- **DZ:** printed page = PDF − 17 in the body (e.g. PDF 21 = printed 4; Ch.1 starts at PDF 20, printed 3). Front matter in Roman numerals. Back-of-book index: PDF 258-272.
- **TMM:** PDF = document (p.1 to p.3).
- Conversion: `python -I scripts/infosec_lookup.py --page N` or `--printed N`.

## DZ page map
| Ch. | Title | PDF | Printed | Reference |
|---|---|---|---|---|
| 1 | InfoSec and Risk Management | 20-45 | 3-28 | `risco-e-governanca.md` |
| 2 | Protecting the Security of Assets | 46-77 | 29-60 | `ativos-isms-e-politicas.md` |
| 3 | Designing Secure Information Systems | 80-111 | 63-94 | `ameacas-vulnerabilidades-e-design-seguro.md` |
| 4 | Designing and Protecting Network Security | 112-143 | 95-126 | `rede-e-zero-trust.md` |
| 5 | Controlling Access and Managing Identity | 144-166 | 127-149 | `acesso-e-identidade.md` |
| 6 | Designing and Managing Security Testing Processes | 170-190 | 153-173 | `testes-de-seguranca-e-assessments.md` |
| 7 | Owning Security Operations | 192-220 | 175-203 | `operacoes-de-seguranca.md` |
| 8 | Improving the Security of Software | 222-252 | 205-235 | `seguranca-de-software-sdlc-devsecops.md` |
Book sections: I (Ch.1-2) risk and governance; II (Ch.3-5) "Closing the Gap"; III (Ch.6-8) operationalization.

## When to open each file
| Trigger | File |
|---|---|
| four questions, values, principles, patterns, anti-patterns, "what is threat modeling" | `tmm-manifesto.md` |
| where the DZ talks about threat modeling; DZ x TMM differences; map of the 4 questions; STRIDE/DFD (extrapolation) | `modelagem-de-ameacas-no-dz-e-ponte-com-tmm.md` |
| risk, assets, impact x likelihood, appetite, treatment, compliance, training, third parties | `risco-e-governanca.md` |
| ISMS, SoA, policies, classification, DLP, retention, control types, cryptography, disposal | `ativos-isms-e-politicas.md` |
| actors, motivations, vulnerabilities, malware, Zero Trust, secure by design, IoT/SCADA | `ameacas-vulnerabilidades-e-design-seguro.md` |
| firewall, segmentation, network attacks, SOC, cloud | `rede-e-zero-trust.md` |
| access models, MFA, NTLM, Kerberos, PKI, IAM, physical access | `acesso-e-identidade.md` |
| assessments, pentest, scanners, Red/Blue Team, interpreting reports | `testes-de-seguranca-e-assessments.md` |
| configuration, IaC, DR/BC, change, incidents, SIEM | `operacoes-de-seguranca.md` |
| secure SDLC, DevSecOps, Proactive Controls, assessing third-party software | `seguranca-de-software-sdlc-devsecops.md` |
| terms | `glossario.md` |
| step by step (risk, ISMS, due diligence, assessment, IR, threat model session) | `procedimentos.md` |
| cases, anti-patterns, tensions and differences between the sources | `casos-e-antipadroes.md` |
| what has changed since the edition | `datado-desde-2021.md` |

## Scripts (Python 3, stdlib, no network, read-only; `python -I`)
| Script | Use |
|---|---|
| `scripts/infosec_lookup.py` (+ `infosec_index.json`) | Locates topics and pages; `--chapters`, `--page`, `--printed`, `--chapter`, `--tmm`, `--datado`, `--gaps`; prints "NOT COVERED" and refers onward |
| `scripts/threat_model_session.py` | Session template/guide with the TMM's four questions, values, principles, patterns and anti-patterns; `template [--dz-bridge] [--extrapolation]`, `agenda`, `checklist`, `evaluate` |
| `scripts/strategy_checklist.py` | Security strategy checklist (108 items, 11 areas, DZ pages); `areas`, `list`, `markdown`, `evaluate` |
| `scripts/risk_matrix.py` | 1-5 scales, 5×5 matrix and ranking (Impact × Likelihood; example appetite 7) |

## Coverage and gaps
- **Read in full (text):** TMM p.1-3; DZ p.1-16 (cover, credits, table of contents, preface) and p.20-252 (Ch.1-8). **Visually** verified: the figures/tables of DZ p.29 (impact and likelihood scales), p.32 (matrix) and p.67 (roles per asset) and page 2 of the TMM (patterns and anti-patterns). **Not read visually:** other figures (CIA, asset register, example SoA, network/OSI diagrams, error screenshots). **Sampled only:** back-of-book index (DZ p.258-263; the rest, p.264-272, not read) and Packt editorial pages (p.253-257).
- **Terms verified ABSENT from the text of both sources** (`python -I scripts/infosec_lookup.py --gaps`): STRIDE, DREAD, PASTA, LINDDUN, DFD/data flow diagram, attack trees, trust boundaries, MITRE ATT&CK, kill chain, NIST CSF, ISO 31000, CVSS, SBOM, SLSA, SOAR/EDR/XDR, LGPD, NIS2, DORA, OAuth/SAML/passkeys, SOC 2, Log4Shell, among others. If asked: NOT COVERED, [extrapolation] marked.
- **What the TMM does not provide:** a threat modeling method, report format, sufficiency criteria (see `tmm-manifesto.md`).

## Boundary with other agents (refer onward)
| Subject | Agent |
|---|---|
| OWASP ASVS (verification requirements), code review (Code Review Guide) | `owasp-asvs-code-review-expert` |
| OWASP WSTG (how to test web applications) | `owasp-web-security-testing-expert` |
| In-depth security engineering (Ross Anderson: protocols, policies, formal models) | `security-engineering-expert` |
| Privacy, LGPD, privacy engineering (NIST IR 8062), LINDDUN | `privacy-lgpd-engineering-expert` |

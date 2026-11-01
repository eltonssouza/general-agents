# Reference INDEX: privacy-lgpd-engineering-expert

**Usage notice (read first):** this package is technical support material. **It does not provide legal advice.** For decisions on concrete cases, refer to a lawyer and to the data protection officer (encarregado / DPO) and check the current version of the law and the ANPD (Brazilian national data protection authority) regulations.

## Sources (closed collection)
- **LGPD** (Lei Geral de Proteção de Dados, Brazilian General Data Protection Law): Lei nº 13.709 of 14 August 2018, **compiled text** from the PDF `LGPD-Lei-13709-ptBR.pdf` (25 pages; ~81 thousand characters of native text). The text carries amendment notes from Laws 13.853/2019, 14.010/2020, 14.460/2022 and 15.352/2026 (summary in `lgpd-disposicoes-finais-vigencia-e-alteracoes.md`).
- **NIST8062**: NISTIR 8062, *An Introduction to Privacy Engineering and Risk Management in Federal Systems*, Jan/2017 (49 PDF pages; native text; figures 2, 3, 4, 6, 7, 8 and 9 are images read visually).

## Page convention (mandatory)
- Every citation uses the **PDF page** (the `=== PAGE N ===` marker of the extracted text): `LGPD Art. 18, III, p.9`, `NIST8062 p.26`.
- **LGPD**: the PDF has no printed numbering; always cite **Art./§/inciso (item) + PDF page**. Chapter map below.
- **NIST8062**: in the body, **printed = PDF − 8** (PDF 9 = printed 1; PDF 49 = printed 41). Front matter in roman numerals: PDF 4 = ii, PDF 5 = iii, PDF 6 = iv (executive summary), PDF 7 = v, PDF 8 = vi. Conversion: `python -I scripts/privacy_lookup.py --printed 18 --src NIST8062` or `--page 26 --src NIST8062`.

## LGPD map (PDF)
| Chapter | Articles | PDF | File |
|---|---|---|---|
| I Preliminary provisions ("Disposições preliminares") | 1-6 | 1-4 | `lgpd-fundamentos-escopo-e-principios.md` |
| II Processing: Section I requirements | 7-10 | 4-6 | `lgpd-bases-legais-e-consentimento.md` |
| II Section II sensitive data, Section III children, Section IV termination | 11-16 | 6-8 | `lgpd-dados-sensiveis-anonimizacao-criancas.md` |
| III Data subject rights | 17-22 | 8-11 | `lgpd-direitos-do-titular.md` |
| IV Public authorities (Poder Público) | 23-32 | 10-12 | `lgpd-poder-publico.md` |
| V International transfer | 33-36 | 12-13 | `lgpd-transferencia-internacional.md` |
| VI Agents: controller/processor, encarregado (DPO), liability | 37-45 | 13-15 | `lgpd-agentes-encarregado-responsabilidade.md` |
| VII Security and good practices | 46-51 | 15-17 | `lgpd-seguranca-incidentes-governanca.md` |
| VIII Enforcement (sanctions) | 52-54 | 17-19 | `lgpd-sancoes-e-anpd.md` |
| IX ANPD and Council | 55-59 | 19-24 | `lgpd-sancoes-e-anpd.md` |
| X Final provisions | 60-65 | 24 | `lgpd-disposicoes-finais-vigencia-e-alteracoes.md` |

## NIST IR 8062 map (PDF; printed = PDF − 8)
| Part | PDF | Printed | File |
|---|---|---|---|
| Executive summary | 6 | iv | `nist8062-engenharia-de-privacidade-e-risco.md` |
| 1 Introduction (1.1 scope, 1.2 audience, 1.3 organization) | 9-13 | 1-5 | same |
| 2 Engineering approach (2.1 security x privacy; 2.2 problems; 2.3 definition; 2.3.1 systems engineering; 2.3.2 risk management) | 14-22 | 6-14 | same |
| 3 Components (3.1 objectives; 3.1.1 FIPPs; 3.1.1.1 predictability; 3.1.1.2 manageability; 3.1.1.3 disassociability; 3.2 risk model; 3.2.1 factors; 3.2.2 characteristics) | 23-31 | 15-23 | `nist8062-objetivos-e-modelo-de-risco.md` |
| 4 Roadmap | 32-33 | 24-25 | same |
| Appendix A Development process | 34-35 | 26-27 | `nist8062-engenharia-de-privacidade-e-risco.md` |
| Appendix B Glossary; C Acronyms; D References | 36-43 | 28-35 | `glossario.md` (B); the rest has no file of its own |
| Appendix E Concerns beyond breach | 44-48 | 36-40 | `nist8062-engenharia-de-privacidade-e-risco.md` |
| Appendix F A-130 FIPPs | 49 | 41 | same |

## When to open each file (triggers)
| Trigger | Open |
|---|---|
| does it apply? territory, exceptions, definitions (personal data, anonymized data, controller, encarregado), principles | `lgpd-fundamentos-escopo-e-principios.md` |
| legal basis, consent, legitimate interest, information to the data subject | `lgpd-bases-legais-e-consentimento.md` |
| sensitive data, health, anonymization, pseudonymization, research, children, deletion | `lgpd-dados-sensiveis-anonimizacao-criancas.md` |
| data subject rights, access deadlines, automated decisions | `lgpd-direitos-do-titular.md` |
| public bodies, shared use | `lgpd-poder-publico.md` |
| international transfer, cloud outside Brazil | `lgpd-transferencia-internacional.md` |
| record of operations, RIPD (data protection impact assessment), encarregado, joint liability | `lgpd-agentes-encarregado-responsabilidade.md` |
| security, privacy by design (Art. 46 §2º), incident, governance | `lgpd-seguranca-incidentes-governanca.md` |
| fines, sanctions, ANPD, Council | `lgpd-sancoes-e-anpd.md` |
| effective date, amendments, "is the text up to date?" | `lgpd-disposicoes-finais-vigencia-e-alteracoes.md` |
| privacy engineering, P/M/D objectives, risk, problems, PIA, FIPPs | `nist8062-engenharia-de-privacidade-e-risco.md`, `nist8062-objetivos-e-modelo-de-risco.md` |
| LGPD x NIST | `mapeamento-lgpd-nist.md` |
| everything the collection does not cover (ANPD resolutions, GDPR, PRAM, AI, cookies) | `extrapolacoes-e-datado.md` |
| terms | `glossario.md` |
| step by step | `procedimentos.md` |
| examples and anti-patterns | `casos-e-antipadroes.md` |

## Scripts (Python 3, stdlib, no network, read-only; run with `python -I`, from the package root)
- `scripts/privacy_lookup.py` looks up by article/topic/page; `--amendments`, `--chapters`, `--gaps`; "NOT COVERED" when there is nothing.
- `scripts/compliance_checklist.py areas|list|markdown|pbd|evaluate`: 72 items generated from the real articles (66 LGPD and 6 NIST), with page.
- `scripts/map_lgpd_nist.py table|by-objective|art|nist-only|markdown`: mapper with levels TEXTUAL, INFERENCE, NO_SUPPORT.
- `scripts/ripd_templates.py ripd|incidente|registro|titular|all`: templates with the minimum content the law lists (Art. 38 sole paragraph; Art. 48 §1º) and labeled additions.
- Data indexes: `scripts/privacy_index.json`, `scripts/checklist_items.json`, `scripts/lgpd_nist_mapping.json`.
- Verification: `tests/verify_citations.py --src <folder with the extracted .txt files>`; `tests/run_script_tests.py`.

## Labels
`[from source]` checked against the cited page; `[inference]` deduction by the agent; `[extrapolation]` outside the two sources; `[DATED]` the text predates later changes. (`[from source]` was `[do texto]` in the Portuguese original and is equivalent to the `[do livro]` label of the other packages in this collection.)

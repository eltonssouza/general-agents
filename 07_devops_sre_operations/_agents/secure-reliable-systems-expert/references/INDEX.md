# Reference INDEX — secure-reliable-systems-expert

Single source: **BSRS** = *Building Secure and Reliable Systems*, Google (Adkins, Beyer, Blankinship, Lewandowski, Oprea, Stubblefield et al.), O'Reilly, 2020; 557 PDF pages, ~1.29 M characters of native text.

## Page convention (mandatory)
- Every `BSRS p.N` citation is the **PDF page** (the `=== PAGE N ===` marker of the extracted text).
- Body (chs. 1-21, conclusion, appendix): **printed page = N − 36** (e.g. PDF p.465 = printed 429; chapter 1 starts at printed 3 = PDF 39).
- The preface uses roman numerals: PDF 27 = printed xxv (N − 2). Index: PDF 537-557.
- Use `python -I scripts/bsrs_lookup.py --page N` or `--printed N` to convert.

## Chapter map
| Ch. | Title (EN) | PDF | Printed | File |
|---|---|---|---|---|
| 1 | The Intersection of Security and Reliability | 39-50 | 3-13 | `intersecao-seguranca-e-confiabilidade.md` |
| 2 | Understanding Adversaries | 51-72 | 15-36 | `adversarios-e-modelagem-de-ameacas.md` |
| 3 | Case Study: Safe Proxies | 73-78 | 37-42 | `safe-proxies-e-tradeoffs-de-design.md` |
| 4 | Design Tradeoffs | 79-96 | 43-60 | `safe-proxies-e-tradeoffs-de-design.md` |
| 5 | Design for Least Privilege | 97-124 | 61-88 | `menor-privilegio-e-controle-de-acesso.md` |
| 6 | Design for Understandability | 125-156 | 89-120 | `design-para-compreensibilidade.md` |
| 7 | Design for a Changing Landscape | 157-178 | 121-142 | `design-para-mudanca-e-cenario-em-evolucao.md` |
| 8 | Design for Resilience | 179-218 | 143-182 | `design-para-resiliencia.md` |
| 9 | Design for Recovery | 219-252 | 183-216 | `design-para-recuperacao.md` |
| 10 | Mitigating Denial-of-Service Attacks | 253-268 | 217-232 | `mitigacao-de-dos.md` |
| 11 | Case Study: Publicly Trusted CA | 269-278 | 233-242 | `estudo-de-caso-ca-publica.md` |
| 12 | Writing Code | 279-306 | 243-270 | `escrevendo-codigo-seguro-e-confiavel.md` |
| 13 | Testing Code | 307-338 | 271-302 | `testando-codigo.md` |
| 14 | Deploying Code | 339-368 | 303-332 | `implantacao-de-codigo-cicd-e-supply-chain.md` |
| 15 | Investigating Systems | 369-398 | 333-362 | `investigacao-de-sistemas-e-logging.md` |
| 16 | Disaster Planning | 399-422 | 363-386 | `planejamento-de-desastres.md` |
| 17 | Crisis Management | 423-452 | 387-416 | `gestao-de-crise-e-resposta-a-incidentes.md` |
| 18 | Recovery and Aftermath | 453-480 | 417-444 | `recuperacao-e-pos-incidente.md` |
| 19 | Case Study: Chrome Security Team | 481-490 | 445-454 | `estudo-de-caso-chrome-e-papeis-e-responsabilidades.md` |
| 20 | Understanding Roles and Responsibilities | 491-506 | 455-470 | `estudo-de-caso-chrome-e-papeis-e-responsabilidades.md` |
| 21 | Building a Culture of Security and Reliability | 507-532 | 471-496 | `cultura-de-seguranca-e-confiabilidade.md` |
| Conclusion / Appendix A | | 533-536 | 497-500 | `cultura-de-seguranca-e-confiabilidade.md`, `apendice-matriz-de-risco-de-desastres.md` |

## When to open each file
| File | Open when the request involves |
|---|---|
| `intersecao-seguranca-e-confiabilidade.md` | differences and common ground between security and reliability; CIA triad; fail safe vs fail secure; emergent properties; the power drill case; how the book is organized (preface) |
| `adversarios-e-modelagem-de-ameacas.md` | attacker motivations and profiles, insiders (actor x motive x action x target matrix), kill chain, TTPs, threat intelligence |
| `safe-proxies-e-tradeoffs-de-design.md` | administrative proxies, Zero Touch Prod, functional vs nonfunctional requirements, design doc template, initial vs sustained velocity, payments example |
| `menor-privilegio-e-controle-de-acesso.md` | least privilege, zero trust, breakglass, auditing, MPA, 3FA, justifications, temporary access, authorization |
| `design-para-compreensibilidade.md` | invariants, mental models, identities, TCB/boundaries, application frameworks, safe types, Tink |
| `design-para-mudanca-e-cenario-em-evolucao.md` | how to change systems safely: zero-day, Shellshock, Heartbleed, containers, microservices, FIDO, HTTPS |
| `design-para-resiliencia.md` | defense in depth, controlled degradation, load shedding, blast radius, failure domains, continuous validation |
| `design-para-recuperacao.md` | rollbacks vs security (MASVN), time, revocation, intended state, backups, emergency access |
| `mitigacao-de-dos.md` | DoS/DDoS, amplification, defensible architecture, automatic mitigation, retries |
| `estudo-de-caso-ca-publica.md` | example of applying the principles to a public CA (trust zones, negative tests, offline key) |
| `escrevendo-codigo-seguro-e-confiavel.md` | frameworks, TrustedSqlString, SafeHtml, OWASP, simplicity, strong types, sanitizers |
| `testando-codigo.md` | unit/integration, sanitizers, fuzzing, static analysis, formal methods |
| `implantacao-de-codigo-cicd-e-supply-chain.md` | **change control, secure CI/CD and supply chain**: threat model, code review, provenance, hermetic/verifiable builds, choke points |
| `investigacao-de-sistemas-e-logging.md` | systematic debugging, security investigation, which logs to retain, privacy and logging budget |
| `planejamento-de-desastres.md` | disaster risk analysis, IR team, severity/priority, playbooks, prestaging, tabletops, Red Team |
| `gestao-de-crise-e-resposta-a-incidentes.md` | **incident response**: triage, IMAG, OpSec, forensics, handovers, communications |
| `recuperacao-e-pos-incidente.md` | recovery, checklist, quarantine, credential rotation, **security postmortem** |
| `estudo-de-caso-chrome-e-papeis-e-responsabilidades.md` | security organization, security champions, Red/Blue/Purple Teams, bug bounty |
| `cultura-de-seguranca-e-confiabilidade.md` | culture (by default, review, awareness, yes, inevitably, sustainability), changing culture, convincing leadership, conclusion |
| `apendice-matriz-de-risco-de-desastres.md` | probability x impact matrix and scales |
| `glossario.md` | the authors' terms in English and definitions in English |
| `procedimentos.md` | checklists and steps the book provides (design, pipeline, incident, culture) |
| `casos-e-antipadroes.md` | real cases from the book and 50 anti-patterns with fix and page |
| `datado-desde-2020.md` | what has changed since 2020 and `[DATED]` items |

## Scripts (Python 3, stdlib, no network)
- `scripts/bsrs_lookup.py` — search by topic and page; says "NOT COVERED" and lists terms verified as absent from the book.
- `scripts/design_review_checklist.py` — secure and reliable design review checklist (84 items with pages), answer evaluation.
- `scripts/incident_templates.py` — templates for IR plan, postmortem, recovery checklist (Figure 18-1) and agendas (kickoff, sync, handover), OpSec and the IC loop.
- `scripts/risk_matrix.py` — ranking of the disaster risk matrix (Appendix A).
- Data: `scripts/bsrs_index.json` (258 entries), `scripts/checklist_items.json`.

## Boundary
- SRE principles (SLO, error budget, toil, monitoring, on-call, blameless postmortem as an SRE practice): **sre-practices-expert**. BSRS mentions error budget on p.44, 91 and 515-516, SLOs on p.81 and 406.
- Observability (OpenTelemetry etc.), containers/Kubernetes, DORA, Linux: dedicated agents, if available; BSRS only covers the security and reliability angle (p.160-161, 361-362, 379-382).

## Verification
`tests/verify_citations.py` + `tests/citation-checks.json` check the citations against the extracted text (positive and negative); `tests/run_script_tests.py` runs the deterministic script cases.

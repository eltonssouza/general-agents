# References INDEX — owasp-asvs-code-review-expert

Two sources, acronyms and page conventions (mandatory in citations):

| Acronym | Work | PDF | Page convention |
|---|---|---|---|
| **ASVS** | *OWASP Application Security Verification Standard 4.0.3* (Final, October 2021; CC BY-SA 3.0) | 71 pages, native text | `ASVS p.N` = **footer** page, which **matches** the PDF page (page 7 of the PDF prints "7"). Requirements cited by ID: `V2.1.1`, `v4.0.3-2.1.1` |
| **OCRG** | *OWASP Code Review Guide* v2.0 (2017; leads Larry Conklin and Gary Robinson; CC BY-SA) | 220 pages, native text in 2 columns | `OCRG p.N` = **PDF** page. Printed page = N − 1 in the body (page 4 of the PDF prints "3"); cover/table of contents/chapter divider pages are unnumbered |

Conversion: `python -I scripts/asvs_lookup.py --page-ocrg N`. In citations with both sources, always write the acronym (`ASVS p.40; OCRG p.185`).

## ASVS 4.0.3 map (PDF = footer)
| Part | PDF | File in `references/` |
|---|---|---|
| Frontispiece, preface (what's new in 4.0), usage, levels, certification, other uses | 7-16 | `asvs-uso-niveis-e-aplicacao.md` |
| V1 Architecture, design and threat modeling | 17-21 | `asvs-v1-arquitetura-e-threat-modeling.md` |
| V2 Authentication (+ NIST glossary, p.30) | 22-31 | `asvs-v2-autenticacao.md` |
| V3 Session management / V4 Access control | 32-35 / 36-37 | `asvs-v3-v4-sessao-e-controle-de-acesso.md` |
| V5 Validation, sanitization and encoding | 38-41 | `asvs-v5-validacao-sanitizacao-e-encoding.md` |
| V6 Stored cryptography / V7 Errors and logging / V8 Data protection | 42-43 / 44-46 / 47-49 | `asvs-v6-v7-v8-cripto-logs-e-protecao-de-dados.md` |
| V9 Communication / V10 Malicious code | 50-51 / 52-53 | `asvs-v9-v10-comunicacao-e-codigo-malicioso.md` |
| V11 Business logic / V12 Files / V13 API | 54-55 / 56-57 / 58-60 | `asvs-v11-v12-v13-negocio-arquivos-e-api.md` |
| V14 Configuration; Appendix C (IoT) | 61-64; 69-71 | `asvs-v14-configuracao-e-apendice-c-iot.md` |
| Appendix A (glossary), B (references) | 65-67, 68 | `glossario.md` (terms) |
- **Data**: `scripts/asvs_requirements.json` has the **320 rows** (286 from V1-V14, of which 8 removed and **278 active**, plus 34 from Appendix C), with page, levels, CWE and NIST. There is no "L1 in V1": chapter V1 only has L2/L3.

## OCRG v2.0 map (PDF = printed + 1)
| Part | PDF | File |
|---|---|---|
| Foreword, introduction, how to use | 4-8 | `ocrg-visao-geral-e-metodologia.md` |
| Ch. 5 Secure Code Review (why, what, hack-ourselves, 360, PCI) | 10-20 | `ocrg-visao-geral-e-metodologia.md` |
| Ch. 6 Methodology (factors, when, risk, preparation, static analysis, threat modeling, metrics, crawling) | 21-43 | `ocrg-visao-geral-e-metodologia.md`, `ocrg-analise-estatica-e-crawling.md`, `ocrg-threat-modeling-aplicado.md` |
| A1 Injection (SQL, JSON, CSP, validation) | 45-58 | `ocrg-a1-injecao-e-validacao-de-entrada.md` |
| A2 Authentication and session | 60-70 | `ocrg-a2-autenticacao-e-sessao.md` |
| A3 XSS; HTML5; SOP; client-side JavaScript | 72-77; 155-160; 189-191 | `ocrg-a3-xss-html5-e-javascript-cliente.md` |
| A4 IDOR; A7 function-level; A8 CSRF; A10 redirects | 79-82; 135-139; 141-146; 151-154 | `ocrg-a4-a7-a8-a10-acesso-csrf-redirecionamento.md` |
| A5 Misconfiguration; A9 Components | 84-117; 148-149 | `ocrg-a5-misconfiguracao-e-a9-componentes.md` |
| A6 Sensitive data and cryptography; attack surface | 119-133 | `ocrg-a6-dados-sensiveis-e-criptografia.md` |
| Logging; errors; alerts; active defense | 161-181 | `ocrg-logging-erros-alertas-e-defesa-ativa.md` |
| Race conditions; buffer overruns | 182-188 | `ocrg-concorrencia-e-memoria.md` |
| Appendices: do's/don'ts, agile, checklist (A), threat model (B), crawling (C) | 193-218 | `ocrg-checklist-e-apendices.md`, `ocrg-threat-modeling-aplicado.md`, `ocrg-analise-estatica-e-crawling.md` |

## Cross-cutting
| File | Open when |
|---|---|
| `integracao-asvs-ocrg.md` | mapping an OCRG topic → ASVS IDs; deciding what each source covers; joint workflow |
| `procedimentos.md` | running a review: plan by risk, choose level, source-to-sink, triage linter, report, backlog |
| `casos-e-antipadroes.md` | real examples described by the books and anti-patterns to reject; errors in the books' own examples |
| `datado-e-tensoes.md` | OCRG 2017 vs ASVS 2021 (password, crypto, session); [DATED] items; extraction limitations |
| `glossario.md` | terms (ASVS and OCRG) |

## When to open each file (triggers)
| User request | Open |
|---|---|
| "what does requirement V2.1.9 demand?" / "L1 session requirements" | run `asvs_lookup.py` and `asvs-v2-...`/`asvs-v3-v4-...` |
| "generate an L2 checklist for the authentication routes" | `asvs_checklist.py generate` + `asvs-v2-autenticacao.md` |
| "review this Java/PHP/C/web.config snippet" | `ocrg_lint.py` + the `ocrg-*.md` of the topic (P4-P6 in `procedimentos.md`) |
| "how do I do threat modeling to review code?" | `ocrg-threat-modeling-aplicado.md` |
| "which ASVS level should I use?" | `asvs-uso-niveis-e-aplicacao.md` |
| "JWT/SSRF/GraphQL/SBOM" | ASVS (V3.5, V5.2.6/V12.6, V13.4, V14.2.5); the OCRG **does not cover** them |
| "bcrypt/Argon2" | ASVS V2.4 (bcrypt/PBKDF2); Argon2/scrypt **absent** from both → [extrapolation] |

## Scripts (Python 3, stdlib, no network, without running the target; run with `python -I`)
- `asvs_lookup.py` — lookup by ID, topic (pt-BR/en), level, chapter, section, CWE; `--chapters`, `--ocrg`, `--gaps`, `--validate`, `--page-ocrg`.
- `asvs_checklist.py` — `generate` (by level/chapter/section, md/json/csv, with count validation), `evaluate`, `ocrg` (Appendix A), `stats`.
- `ocrg_lint.py` — 54 rules (49 from the OCRG/inference + 5 [extrapolation] disabled by default), each with class, origin and page.
- Build (optional): `asvs_extract_text.py` (text → JSON, stdlib), `build_asvs_from_pdf.py` and `build_ocrg_checklist_from_pdf.py` (PyMuPDF, by coordinates).
- Data: `asvs_requirements.json`, `ocrg_index.json`, `ocrg_checklist.json`, `gaps.json`.

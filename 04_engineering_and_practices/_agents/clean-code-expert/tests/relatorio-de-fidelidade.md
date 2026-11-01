# Fidelity report: clean-code-expert v1.0.0

Date: 2026-11-01. Environment: Windows 11, Python 3.13.15, Claude Code 2.1.316.

Note: this report was translated to English. The results quoted below (E1..E3) come from the original run, which used the Portuguese version of the package; the book itself, the page numbers and the `terms` of `citation-checks.json` (literal OCR text of the Portuguese edition) are unchanged.

## 1. How the content was produced
1. **Extraction.** The PDF (`Codigo Limpo - Completo PT.pdf`, 398 pages) is scanned: only images, no text characters. Each page was rendered at 200 dpi (PyMuPDF) and read by the native Windows OCR in pt-BR (`tests/ocr_pdf_windows.ps1`), producing `CL.txt` with `=== PAGE N ===` markers (720 thousand characters). The prose comes out readable; the code of the listings does not.
2. **Distillation.** Six readers, one per group of chapters (front matter and chs. 1-3; 4-5; 6-9; 10-13 and Appendix A; 14-16 and Appendix B; 17, Appendix C and epilogue), followed the same briefing: own syntheses, the PDF page on every rule, literal quotation under 15 words, labels `[from source]`/`[inference]`/`[extrapolation]`/`[DATED]`, reading the page image when the OCR failed (numbers, titles, lists). Each group delivered references, index topics and citation checks, and only finished once the verifier passed.
3. **Integration.** References (21 files + `INDEX.md`), `cc_index.json` (112 topics, 35 uncovered items), `cc_smells.json` (66 heuristics) and `citation-checks.json` were merged with no duplicate keys or IDs. `cc_checklist.json` (12 areas) was written from the rules already verified.

## 2. Verification against the book text
| Check | Result |
|---|---|
| `verify_citations.py --src` (whole book) | **416 positive, 29 negative, 0 failures** |
| Positive | each rule with a page: the OCR excerpts must be on the cited pages |
| Negative | terms absent from the whole book: SOLID (acronym), Liskov, Interface Segregation, "Inversão de Dependência", CQS/"Command Query", YAGNI, "code smell", Long Method, God Class, Shotgun Surgery, Primitive Obsession, Null Object, Tell Don't Ask, Arrange, Mockito, JUnit 5, `CompletableFuture`, Coffman, docstring, linter, tab characters, FIXME, Red-Green, JaCoCo, `java.time`, `LocalDate`, Strangler and heuristic codes beyond the 66 |
| Image check (sample done by the readers) | three laws of TDD (p.125), four items of the Law of Demeter (p.102), F.I.R.S.T. (p.134-135), G23/G34 titles and N1's "90%" (p.294, 299, 304), numbers in Figures 5.1 and 5.2 (p.82, 90), "10x1" (p.23), atomic "interrompível" (p.316), ConTest (p.335), codes cited in chs. 15-16 |

Limits of the verification: the check proves that the excerpts are on the pages, not that the synthesis is perfect; OCR errors in code and in codes between brackets were handled by reading the image, but by sampling.

## 3. Scripts and package
| Check | Result |
|---|---|
| `python -I tests/run_script_tests.py --src <folder>` | 31 script cases + 10 package checks (34 cases after the English translation, which added LK-05b, SM-05b and AU-06b), **0 failures**; without `--src`, the citations step is SKIP |
| Mutation proof | raising the argument limit 3→5 breaks AU-01, AU-03 and AU-06; a wrong page for G5 breaks SM-01 |
| Pages cited in the package | 3,147 citations, all between 1 and 398 |
| `claude plugin validate --profile directory` | Validation passed; "These checks found nothing to report" |
| Collection marketplace | `clean-code-expert` entry added; the marketplace's `claude plugin validate` passes |
| Orchestrator | catalog regenerated (61 agents), new routing case, 85 PASS / 0 FAIL |

## 4. End-to-end execution (Claude Code, headless, Sonnet model)
Temporary project with `Ruim.java` (fixture without the header), plugin loaded with `--plugin-dir`.
| # | Request | Result | Cost |
|---|---|---|---|
| E1 | "Revise o arquivo Ruim.java pela ótica do Clean Code. Não altere arquivos." (without `Skill` enabled) | **Did not trigger** the agent or the skills; the session answered from memory and said it had no pages | US$ 0.12 |
| E1b | same, after adding "Use proactively" to the description | **Did not trigger** (same behavior) | US$ 0.11 |
| E1c | "Use o agente clean-code-expert para revisar o arquivo Ruim.java" | PASS: delegated to `clean-code-expert:clean-code-expert`; the subagent ran `cc_audit.py` and `cc_smells.py` through the plugin path (`${CLAUDE_PLUGIN_ROOT}` substituted), confirmed the candidates, found what the script cannot see (undeclared `ctxt`, dead loop, G9/G12) and cited correct pages; nothing changed | US$ 0.19 |
| E1d | the E1 request with `Skill` enabled | PASS: the `cc-code-audit` skill fired on its own; 13 candidates confirmed by reading the code, extras labeled `[inference]`, correct pages, nothing changed | US$ 0.13 |
| E2 / E2b | "Qual padrão GoF uso para desfazer/refazer?" (before and after "use proactively") | PASS: did not trigger the agent or the skills | US$ 0.08 + 0.08 |
| E3 | "O livro manda um único assert por teste e seguir SOLID?" (`--agent clean-code-expert:clean-code-expert`) | PASS: corrected both premises (one concept per test, CL p.133-134; SOLID does not appear; DIP with the wrong translation; LSP/ISP absent), with a separate `[extrapolation]` | US$ 0.06 |
The pages cited by the subagents in E1c and E1d were checked with `cc_smells.py` (G9 p.286, G12 p.287, G10 p.287, G29 p.296, G36 p.301, N6 p.307, C5 p.282, G30 p.296, G34 p.299): all correct.

**Conclusion on triggering:** the automatic path observed is the **skill** (`cc-code-audit`); the **agent** is triggered when named or mentioned with @. The Claude Code documentation says delegation depends on the request, the description and the context, and that naming the subagent guarantees it; "use proactively" was kept in the description because the documentation recommends it, but it did not change the result in this test.

## 5. Not run / pending
- Codex and GitHub Copilot: the adapters were generated from the canonical prompt and follow the documentation checked on 2026-10-31, but those clients are not installed here.
- Models other than Sonnet; blind execution by an independent evaluator.
- `cc_audit.py` is heuristic: with no real parser, multi-line signatures and very unusual code may escape.
- The book's internal cross-references and the Appendix C pages do not match this edition (documented in `references/INDEX.md`).

## 6. Later fix (2026-11-01)
`cc_audit.py -` read standard input with the console encoding; on Windows, with `python -I`, that is cp1252 and corrupted accents. It now reads bytes and decodes UTF-8. Case AU-05b covers the regression (with the old reading, it fails).

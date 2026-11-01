# INDEX: source, page map and guide to the references

## The source
- **CL** = *Código Limpo: Habilidades Práticas do Agile Software* (Clean Code: A Handbook of Agile Software Craftsmanship), Robert C. Martin, "Série de Robert C. Martin", Brazilian edition (Alta Books logo on the cover; original *Clean Code*, 2008). Foreword by James O. Coplien.
- The file is a **scanned** 398-page PDF, image only. The text used in this audit came from OCR (Windows, pt-BR); the prose is good, the code is noisy.
- **Not included in the scan**: title page, year, ISBN, translator, table of contents, index.
- Details: `fonte-e-identificacao.md`.

## Page convention
- `(CL p.N)` = **PDF page**. Do not use the printed page: the offset between the two changes along the file (missing or out-of-order pages).
- Internal cross-references in the book ("see page 177", "Listing B.1, page 349") use the printed pagination or that of the English edition: do not cite them. The Appendix C page numbers ("17-292") do not match either.

## Chapter map (PDF)
| Part | Title in the edition | PDF | Reference |
|---|---|---|---|
| — | Cover, Foreword (Coplien), Introduction, About the cover | p.1-10 | `fonte-e-identificacao.md` |
| Ch. 1 | Código Limpo (Clean Code) | p.11-25 | `cap01-codigo-limpo.md` |
| Ch. 2 | Nomes Significativos (Meaningful Names; by Tim Ottinger) | p.26-39 | `cap02-nomes-significativos.md` |
| Ch. 3 | Funções (Functions) | p.40-58 **and p.398** | `cap03-funcoes.md` |
| Ch. 4 | Comentários (Comments) | p.59-80 | `cap04-comentarios.md` |
| Ch. 5 | Formatação (Formatting) | p.81-97 | `cap05-formatacao.md` |
| Ch. 6 | Objetos e Estruturas de Dados (Objects and Data Structures) | p.98-106 | `cap06-objetos-e-estruturas-de-dados.md` |
| Ch. 7 | Tratamento de Erro (Error Handling; by Michael Feathers) | p.107-116 | `cap07-tratamento-de-erro.md` |
| Ch. 8 | Limites (Boundaries; by James Grenning) | p.117-123 | `cap08-limites.md` |
| Ch. 9 | Testes de Unidade (Unit Tests) | p.124-135 | `cap09-testes-de-unidade.md` |
| Ch. 10 | Classes (Classes) | p.136-151 | `cap10-classes.md` |
| Ch. 11 | Sistemas (Systems) | p.152-167 | `cap11-sistemas.md` |
| Ch. 12 | Emergência (Emergence) | p.168-173 | `cap12-emergencia.md` |
| Ch. 13 | Concorrência (Concurrency) | p.174-187 | `cap13-concorrencia.md` |
| Ch. 14 | Refinamento Sucessivo (Successive Refinement; Args) | p.188-247 | `cap14-refinamento-sucessivo.md` |
| Ch. 15 | Características Internas do JUnit (JUnit Internals) | p.248-262 | `cap15-junit-por-dentro.md` |
| Ch. 16 | Refatorando o SerialDate (Refactoring SerialDate) | p.263-279 | `cap16-refatorando-serialdate.md` |
| Ch. 17 | Odores e Heurísticas (Smells and Heuristics) | p.280-309 | `cap17-odores-e-heuristicas.md` |
| Appendix A | Concorrência II (Concurrency II; by Brett L. Schuchert) | p.310-340 | `apendice-a-concorrencia-ii.md` |
| Appendix B | org.jfree.date.SerialDate (listings) | p.341-394 | `apendice-b-mapa-das-listagens.md` |
| Appendix C | Referência Cruzada das Heurísticas (Cross References of Heuristics) | p.395-396 | `apendice-c-e-epilogo.md` |
| Epilogue | — | p.397 | `apendice-c-e-epilogo.md` |

## Scan defects
- **p.398** is printed page 42 of Ch. 3, out of place: the reading order is p.50, p.398, p.51 (end of "Tríades", "Objetos como Parâmetros", "Listas como Parâmetros", start of "Verbos e Palavras-Chave"; in English: Triads, Argument Objects, Argument Lists, Verbs and Keywords).
- Missing: the end of Listing 3-7 (Ch. 3); printed pages 311-312 (end of the Ch. 17 Conclusion; p.309 stops mid-sentence).
- Cut-off footers: Boy Scout Rule (p.24), "Evite repetição" (Avoid repetition; p.55), the source of the "school" of one assert per test (p.132).
- OCR: heuristic codes in square brackets come out garbled in Chs. 14-16 ("[G3()]" = G30, "[CIII]" = G11); code listings are almost unreadable. The Law of Demeter has 4 items; the OCR shows 3 (p.102).

## Translation errors and traps
| Where | What is printed | Correct reading |
|---|---|---|
| p.13 | LeBlanc's law: "Nunca é tarde" | "depois é nunca" (later equals never) |
| p.24, p.151 | "Princípio da Inversão da Independência" | Dependency Inversion Principle (DIP) |
| p.74 | "Explicação do código em comentários" | commented-out code (in Ch. 17: C5 "Código como comentário", p.282) |
| p.299 | G34 "Funções devem descer apenas um nível de" | "abstração" is missing |
| p.316 | atomic operation "interrompível" | uninterruptible (the reasoning on p.317 requires it) |
| p.335 | ConTest makes the failure "menos provável" (less likely) | the numbers on the page show the opposite |
| p.248-262 | header "Capítulo 15: Testes de Unidade" | the chapter is about JUnit internals |
Chapter 4 names in the edition: "Créditos e autoria" (p.74), "Informações excessivas" (p.76), "Comentários Longos" (p.69), "Comentários Ruidosos" (p.70), "Ruídos assustadores" (p.72).

## What the book does NOT have (negative checks over the whole text)
SOLID as an acronym; Liskov; Interface Segregation; "Inversão de Dependência" (Dependency Inversion); CQS/"Command Query"; YAGNI; "code smell"; Long Method, God Class, Shotgun Surgery, Primitive Obsession; Null Object; Tell Don't Ask; Arrange-Act-Assert; Mockito; JUnit 5; `CompletableFuture`; Coffman; docstring; linter; tabulação (tab character); Red-Green; JaCoCo; `java.time`/`LocalDate`; Strangler. Full list and mechanism in `tests/citation-checks.json`.

## Scripts and data
- `scripts/cc_index.json`: 112 topics with rules and pages; `uncovered`: topics without coverage. Lookup: `cc_lookup.py`.
- `scripts/cc_smells.json`: the 66 heuristics of Ch. 17 (C5, E2, F4, G36, J3, N7, T9). Lookup: `cc_smells.py`.
- `scripts/cc_checklist.json`: checklist by area. Use: `cc_checklist.py`.
- `scripts/cc_audit.py`: syntactic candidates linked to the heuristics and topics.

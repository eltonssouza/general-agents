# Reference INDEX: design-patterns-expert

Audited package (v2). The sources are **four PDFs of different natures**, and two of them are **chapter samples**. The previous package (v1) presented all four as "complete canonical works" and attributed to them pages and facts that the PDFs do not contain. The table below says exactly what each PDF is.

## 1. Sources (all in `03_design_and_architecture/`)
| Abbreviation | File | What it really is | PDF (pages) | Printed page |
|---|---|---|---|---|
| **RG** | `Design-Patterns-RefactoringGuru.pdf` | **Capture of the refactoring.guru website** (catalog of 22 patterns; it is neither the e-book "Dive Into Design Patterns" nor the GoF book). Page 1 is a "404"; the footer of every page repeats advertising for the site and the e-book | 279 | **no printed page** |
| **GPP** | `Game-Programming-Patterns-Nystrom.pdf` | **Web capture of the book** *Game Programming Patterns* (Robert Nystrom, © 2009-2021), with navigation headers; **the Subclass Sandbox chapter is missing** (p.190 is a "404 Not Found" page) | 338 | **no printed page** |
| **CC** | `Clean-Code-SampleChapter-Pearson.pdf` | **Sample** of *Clean Code* (R. C. Martin, Pearson, © 2009): cover, table of contents, foreword, introduction, **only Chapter 1** and the index. **Ch. 2 (Names) and Ch. 3 (Functions) are NOT included** | 67 | body: PDF − 30 |
| **PEAA** | `PoEAA-SampleChapter-Pearson.pdf` | **Sample** of *Patterns of Enterprise Application Architecture* (M. Fowler, Addison-Wesley, © 2003): table of contents, preface, Introduction, **only Chapter 3** (O/R mapping) and the index. **Chs. 1, 2 and 9 (layers and domain logic) are NOT included** | 78 | Introduction: PDF − 25; Ch. 3: PDF − 7 |

The original GoF book (*Design Patterns*, 1994) **is not a source** for this package. When RG/GPP mention the "Gang of Four book" (RG p.7; GPP p.4, 19), it is only a reference.

## 2. Page convention (mandatory)
- **Every citation `(SIGLA p.N)` uses the PDF page** (the `=== PAGE N ===` markers of the text extracted with PyMuPDF). Tell the user this at least once in every answer that cites pages.
- RG and GPP have no printed pagination (they are web pages). CC and PEAA do; the conversions above are for anyone opening the physical book. The pages in parentheses in PEAA pattern names, such as "Data Mapper (165)", are **printed** pages of the full book.
- `[from source, table of contents only]` / `[from source, index only]` = the page proves that the topic exists, not what the book says.

## 3. Epistemic labels
`[from source]` direct reading of the cited page · `[inference]` deduction from the texts · `[extrapolation]` external knowledge (includes the content of chapters missing from the samples) · `[DATED]` practice/tool of its era (pre-C++11 C++, XNA, Windows API, Lua 5.1, .NET/JDO).

## 4. Page map
### RG (PDF)
Catalog: classification 5; history 7; criticisms 8-9 (patterns as "crutches" for weak languages, literal application, unjustified use); creational catalog 10-11, structural 12-13, behavioral 14-16.
| Pattern | PDF | Pattern | PDF |
|---|---|---|---|
| Abstract Factory | 17-29 | Chain of Responsibility | 157-171 |
| Builder | 30-44 | Command | 172-186 |
| Factory Method | 45-57 | Iterator | 187-198 |
| Prototype | 58-69 | Mediator | 199-210 |
| Singleton | 70-77 | Memento | 211-222 |
| Adapter | 78-88 | Observer | 223-234 |
| Bridge | 89-100 | State | 235-247 |
| Composite | 101-111 | Strategy | 248-257 |
| Decorator | 112-126 | Template Method | 258-267 |
| Facade | 127-134 | Visitor | 268-279 |
| Flyweight | 135-146 | Proxy | 147-156 |

Each pattern follows: Intent, Problem, Solution, Structure, Pseudocode, Applicability, How to Implement, Pros and Cons (the extraction loses the + and - icons), Relations with Other Patterns. **Interpreter is not in the PDF**.

### GPP (PDF)
Introduction 1-7 (book structure: p.5-6); "Architecture, Performance, and Games" 8-18; *Design Patterns Revisited*: Command 21-32, Flyweight 33-42, Observer 43-59, Prototype 61-75, Singleton 77-91, State 92-110; *Sequencing*: Double Buffer 113-128, Game Loop 130-145, Update Method 146-161; *Behavioral*: Bytecode 163-189, **Subclass Sandbox: ABSENT (p.190 = 404)**, Type Object 191-207; *Decoupling*: Component 209-228, Event Queue 230-249, Service Locator 251-265; *Optimization*: Data Locality 267-290, Dirty Flag 291-305, Object Pool 307-321, Spatial Partition 322-338.

### CC (PDF; printed = PDF − 30 in the body)
Cover/credits 1-6; table of contents 7-17 (lists all chapters, p.7-9 for Chs. 1-4); foreword 19-23; introduction 25-29; **Ch. 1: 31-45**; index 47-65.

### PEAA (PDF)
Credits 4-5; table of contents 8-17; preface 18-25; **Introduction 26-38** (printed 1-13); **Ch. 3 "Mapping to Relational Databases" 40-60** (printed 33-53); index 62-78.

## 5. Catalog of thematic references
1. [`padroes-criacionais-gof.md`](padroes-criacionais-gof.md): Abstract Factory, Builder, Factory Method, Prototype, Singleton (RG) with Prototype and Singleton from GPP.
2. [`padroes-estruturais-gof.md`](padroes-estruturais-gof.md): Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy (RG), Flyweight in GPP.
3. [`padroes-comportamentais-gof.md`](padroes-comportamentais-gof.md): the 10 behavioral patterns of RG; Command, Observer and State in GPP.
4. [`padroes-de-sequenciamento-e-tempo.md`](padroes-de-sequenciamento-e-tempo.md): Double Buffer, Game Loop, Update Method (GPP).
5. [`padroes-comportamentais-e-desacoplamento-em-jogos.md`](padroes-comportamentais-e-desacoplamento-em-jogos.md): Bytecode, Type Object, Component, Event Queue, Service Locator (GPP) and the Subclass Sandbox gap.
6. [`padroes-de-otimizacao-e-performance.md`](padroes-de-otimizacao-e-performance.md): Data Locality, Dirty Flag, Object Pool, Spatial Partition (GPP).
7. [`clean-code-capitulo-1.md`](clean-code-capitulo-1.md): what the CC sample contains (Introduction and Ch. 1).
8. [`clean-code-nomes-e-funcoes.md`](clean-code-nomes-e-funcoes.md): Chs. 2 and 3 **absent**; what the table of contents and the index allow us to state.
9. [`poeaa-mapeamento-para-bancos-relacionais.md`](poeaa-mapeamento-para-bancos-relacionais.md): PEAA Ch. 3.
10. [`poeaa-organizacao-da-logica-de-dominio.md`](poeaa-organizacao-da-logica-de-dominio.md): PEAA Introduction and the gap of Chs. 1, 2 and 9.
11. [`casos-e-antipadroes.md`](casos-e-antipadroes.md), [`procedimentos.md`](procedimentos.md), [`glossario.md`](glossario.md).

## 6. What NO PDF contains (say "the sources do not cover this")
- Clean Code naming and function rules (Chs. 2-3); detail on Transaction Script, Domain Model, Table Module, Service Layer and "the three layers" (PEAA Chs. 1, 2, 9); the Subclass Sandbox chapter; Interpreter.
- Values such as "60 Hz", "cap of 8 updates", "20 lines per function", "maximum of 3 arguments": they do not come from the sources.
- Godot, Unreal (apart from the mention of Kismet), modern ECS, DI containers, Spring, Hibernate: `[extrapolation]`.
- Concurrency patterns, integration messaging patterns, DDD, CQRS, microservices: outside the corpus (see `agents/design-patterns-expert.md`, boundary).

## 7. Scripts and tests
Scripts in `../scripts/` (stdlib, no network, `python -I`): `patterns_lookup.py` (+ `patterns_index.json`), `game_loop_simulator.py`, `domain_logic_selector.py`, `clean_code_function_auditor.py`. Tests in `../tests/`: `casos-de-teste.md`, `relatorio-de-fidelidade.md`, `verify_citations.py` (+ `citation-checks.json`), `audit_tokens.py`, `run_script_tests.py`. The verifiers require the text extracted from the PDFs by page (`=== PAGE N ===`); see README.

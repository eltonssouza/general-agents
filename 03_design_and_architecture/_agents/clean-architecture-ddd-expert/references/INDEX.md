# References index: Clean Architecture & DDD Expert (v2, post-audit)

Base of the `clean-architecture-ddd-expert` agent. The references were **rewritten** after an audit against the text extracted from the PDFs (see `tests/relatorio-de-fidelidade.md`): the previous version attributed to the texts many claims that they do not contain.

## 1. Page convention (read before citing)

`(ACRONYM p.N)` = **PDF page** (the N-th page of the file), in **all** sources. Tell the user this at least once per answer that cites pages.

| Acronym | File (in `03_design_and_architecture/`) | PDF pages | Author / date | Printed page | Actual content |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `DDD` | `DDD-Reference-Evans.pdf` | 59 | Eric Evans, 2015 | printed = PDF − 7 (PDF p.1-7 = Roman-numeral front matter) | Booklet of definitions and pattern summaries |
| `CA11` | `Clean-Architecture-UncleBob-2011.pdf` | 15 | R. C. Martin, post "Clean Architecture", 22/11/2011 | unnumbered | **p.1-5** text; p.6-15 blog sidebar |
| `CA12` | `The-Clean-Architecture-UncleBob-2012.pdf` | 15 | R. C. Martin, post "The Clean Architecture", 13/08/2012 | unnumbered | **p.1-7** text; p.8-15 sidebar |
| `SRP` | `SOLID-SRP-UncleBob.pdf` | 15 | R. C. Martin, post "The Single Responsibility Principle", 08/05/2014 | unnumbered | **p.1-5** text; p.6-15 blog sidebar |
| `OCP` | `SOLID-OCP-UncleBob.pdf` | 15 | R. C. Martin, post "The Open Closed Principle", 12/05/2014 | unnumbered | **p.1-4** text; p.5-15 blog sidebar |
| `SREL` | `SOLID-Relevance-UncleBob.pdf` | 15 | R. C. Martin, post "Solid Relevance", 18/10/2020 | unnumbered | **p.1-5** text; p.6-15 blog sidebar |
| `TARPIT` | `Out-of-the-Tar-Pit.pdf` | 66 | B. Moseley and P. Marks, 06/02/2006 | printed = PDF | Full paper (references on p.64-66) |
| `REACT` | `Reactive-Manifesto-2.0.pdf` | 2 | published 16/09/2014 (v2.0); PDF without author names | PDF | Full manifesto |

About the previous version: the package said that `CA11` was "Architecture: The Lost Years" (it is not), that SRP/OCP/SREL had "15 pages" of content, and that `DDD` was the base book with aggregate patterns on p.23-28 and nine context map patterns on p.35-45. What the `DDD` PDF actually contains, page by page, is in `ddd-estrategico-e-context-maps.md` and `ddd-tatico-e-agregados.md`.

### `DDD` page map (PDF)

p.8 overview (3 points) · p.9 Bounded Context · p.10-11 Ubiquitous Language · p.12 Continuous Integration · p.13 Model-Driven Design · p.14 Hands-on Modelers · p.15 Refactoring Toward Deeper Insight · p.17 Layered Architecture · p.18 Entities · p.19 Value Objects · p.20 Domain Events · p.21 Services · p.22 Modules · p.23 Aggregates · p.24 Repositories · p.25 Factories · p.26-34 Supple Design (27 Intention-Revealing, 28 Side-Effect-Free, 29 Assertions, 30 Standalone, 31 Closure, 32 Declarative, 33 Formalisms, 34 Conceptual Contours) · p.35-45 Context Mapping (35 definitions, 36 Context Map, 37 Partnership, 38 Shared Kernel, 39 Customer/Supplier, 40 Conformist, 41 Anticorruption Layer, 42 Open-host Service, 43 Published Language, 44 Separate Ways, 45 Big Ball of Mud) · p.46-53 Distillation (47 Core Domain, 48 Generic Subdomains, 49 Domain Vision Statement, 50 Highlighted Core, 51 Cohesive Mechanisms, 52 Segregated Core, 53 Abstract Core) · p.54-59 Large-scale Structure.

### `TARPIT` page map (PDF = printed)

p.1-2 introduction and roadmap · p.4-5 testing and reasoning · p.6-8 state · p.8-10 control · p.10-11 code volume · p.11-12 other causes · p.12-14 OOP · p.15-18 functional programming · p.19-21 logic programming · p.21-22 essential vs. accidental (section 6) · p.23-27 ideal world (Table 1, p.26) · p.28-31 limitations · p.31-36 recommendations (Table 2, p.33; Figure 1, p.35) · p.37-42 relational model · p.42-49 FRP (Figure 2, p.43) · p.50-53 benefits · p.54-63 example (section 10) · p.63 related work · p.64 conclusions.

### `CA12` map

p.1-2 previous architectures and 5 properties · p.3 Dependency Rule, Entities · p.3-4 Use Cases · p.4-5 Interface Adapters · p.5 Frameworks and Drivers, "Only four circles?", crossing boundaries · p.6 output port, data crossing · p.7 conclusion.

## 2. Epistemic labels

- `[from source]`: read on the cited page.
- `[inference]`: direct deduction from the text.
- `[extrapolation]`: external knowledge (examples, names, practices).
- `[DATED]`: technology or context of the period (2006, 2011-2014, 2020).

## 3. Catalog

1. `ddd-estrategico-e-context-maps.md`: Bounded Context, Ubiquitous Language, CI, Context Map (9 patterns), distillation.
2. `ddd-tatico-e-agregados.md`: Layered Architecture, Entities, VOs, Domain Events, Services, Modules, Aggregates, Repositories, Factories, Supple Design.
3. `clean-architecture-e-the-lost-years.md`: the 2011 post (`CA11`). The file name was kept for compatibility; it does **not** contain "The Lost Years".
4. `regras-de-dependencia-e-circulos-concentricos.md`: `CA12`.
5. `principios-solid-srp-e-atores.md`: `SRP` (and a note that "actor" is a later term).
6. `principios-solid-ocp-lsp-isp-dip.md`: `OCP` and `SREL`.
7. `out-of-the-tar-pit-complexidade-essencial-vs-acidental.md`: `TARPIT` p.1-37.
8. `programacao-funcional-relacional-frp.md`: `TARPIT` p.37-64.
9. `o-manifesto-reativo-2.0.md`: `REACT`.
10. `casos-e-antipadroes.md`, 11. `procedimentos.md`, 12. `glossario.md`.

## 4. Scripts (Python 3, stdlib, no network; use `python -I`)

| Script | What it does | Source of the rules |
| :--- | :--- | :--- |
| `scripts/ddd_lookup.py` | Topic lookup in the index `scripts/cleanarch_index.json`; answers `NOT COVERED` when the corpus does not address it | Index curated from the PDFs |
| `scripts/audit_aggregate.py` | Checks an aggregate described in JSON | Rules labeled by origin (`DDD p.23-24`, `[extrapolation]`) |
| `scripts/validate_dependency_rule.py` | Checks dependencies between layers in JSON | `CA12 p.3`; layer name mapping is `[extrapolation]` |
| `scripts/tar_pit_complexity_calc.py` | State-space arithmetic, Table 1 classification, Table 2 | `TARPIT p.8, 26, 33` |

Verifiers (in `tests/`): `verify_citations.py` + `citation-checks.json` (positive and negative checks), `audit_tokens.py` (backticked terms against the cited page), `run_script_tests.py`, `extract_pdfs.py` (generates the source text with page markers).

## 5. What the corpus does NOT cover (`not_in_book`)

Event Storming; three-subdomain typology (supporting subdomain); CQRS, Event Sourcing, Saga, Outbox; Hexagonal Architecture in detail (only mentioned: `CA12 p.1`, `DDD p.17`); Screaming Architecture and "The Lost Years" (only the mention in `CA12 p.2`); the "one module, one actor" formulation; formal statement of the LSP; code examples beyond `Employee` (`SRP p.3`); circuit breaker, bulkhead, actors/Akka, Reactive Streams, Kubernetes; Functional Core/Imperative Shell; any quantitative "complexity" metric.

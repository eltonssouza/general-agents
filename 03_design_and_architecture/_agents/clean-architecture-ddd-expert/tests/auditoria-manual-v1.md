# v1 manual sample: 96 claims read on the cited page

Classification made by the auditor when reading the PDF page cited by the v1 (extracted text; convention: PDF page). Kept as a record; the v2 fixes every item that is not OK.

| # | Origin in v1 | Claim (and cited page) | Verdict |
| ---: | :--- | :--- | :--- |
| 1 | ref-estrat | Enterprise-Wide Model and 'catastrophic illusion' (DDD p.8) | unsupported claim |
| 2 | ref-estrat | Bounded Context 'each term has a unique, unambiguous and rigorous meaning' (DDD p.9) | exaggeration |
| 3 | ref-estrat | Ubiquitous Language used in the code (DDD p.10-11) | OK |
| 4 | ref-estrat | 'reverse debit'/cancelTransaction example attributed to the text | unsupported claim |
| 5 | ref-estrat | CI 'mandatory practice' (DDD p.12) | exaggeration |
| 6 | ref-estrat | typology of 3 subdomains (DDD p.30-34) | wrong page |
| 7 | ref-estrat | Core Domain 'exclusive in-house development' (DDD p.30; actual p.47) | wrong page |
| 8 | ref-estrat | Generic Subdomain: libraries/SaaS (DDD p.32; actual p.48) | wrong page |
| 9 | ref-estrat | Supporting Subdomain (DDD p.33) | unsupported claim |
| 10 | ref-estrat | Context Map (DDD p.35; actual p.36) | wrong page |
| 11 | ref-estrat | Partnership (DDD p.37) | OK |
| 12 | ref-estrat | small Shared Kernel, prior consultation (DDD p.38) | OK |
| 13 | ref-estrat | Customer/Supplier: 'political power' (DDD p.39) | exaggeration |
| 14 | ref-estrat | Conformist: 'has no political power' (DDD p.40) | exaggeration |
| 15 | ref-estrat | ACL 'supreme isolation' (DDD p.41) | exaggeration |
| 16 | ref-estrat | Open-host Service REST/RPC (DDD p.42) | exaggeration |
| 17 | ref-estrat | Published Language (DDD p.43) | OK |
| 18 | ref-estrat | Separate Ways due to network/coupling cost (DDD p.44) | exaggeration |
| 19 | ref-estrat | BBoM: 'Evans categorically instructs: never allow...' (DDD p.45) | unsupported claim |
| 20 | ref-tatico | Entity (DDD p.16; actual p.18) | wrong page |
| 21 | ref-tatico | Value Object (DDD p.18; actual p.19) | wrong page |
| 22 | ref-tatico | VO 'self-validation in the constructor' | unsupported claim |
| 23 | ref-tatico | Aggregate as an atomic unit (DDD p.23-24) | OK |
| 24 | ref-tatico | Aggregate root (DDD p.24; actual p.23) | wrong page |
| 25 | ref-tatico | 'Five inviolable rules' of the aggregate (DDD p.24-27) | unsupported claim |
| 26 | ref-tatico | Repository only for the root (DDD p.25; actual p.24) | wrong page |
| 27 | ref-tatico | Reference between aggregates strictly by ID (DDD p.26) | unsupported claim |
| 28 | ref-tatico | 1 aggregate per transaction (DDD p.27) | unsupported claim |
| 29 | ref-tatico | Repository interface in the domain, implementation in the infra (DDD p.27-28) | unsupported claim |
| 30 | ref-tatico | Factories (DDD p.29; actual p.25) | wrong page |
| 31 | ref-tatico | Domain Events in the past participle (DDD p.20) | unsupported claim |
| 32 | ref-tatico | stateless Domain Service (DDD p.21) | unsupported claim |
| 33 | ref-ca11 | 'The Lost Years': architectural amnesia of the 1990s (CA11 p.2-4) | unsupported claim |
| 34 | ref-ca11 | tree /app/controllers /models /views, Rails/Spring/Django (CA11 p.5) | unsupported claim |
| 35 | ref-ca11 | house plan/library blockquote (CA11 p.6) | unsupported claim |
| 36 | ref-ca11 | Screaming Architecture as a principle (CA11 p.7) | unsupported claim |
| 37 | ref-ca11 | use cases as the center of the universe (CA11 p.8) | unsupported claim |
| 38 | ref-ca11 | use cases independent of HTTP/CLI/Kafka (CA11 p.9) | unsupported claim |
| 39 | ref-ca11 | the Web is an I/O device (CA11 p.10-12; page is sidebar) | wrong page |
| 40 | ref-ca11 | 100% of tests without starting a web server (CA11 p.11) | unsupported claim |
| 41 | ref-ca11 | the database is a persistence detail (CA11 p.12-13; sidebar) | wrong page |
| 42 | ref-ca12 | four circles (CA12 p.2-4; actual p.3-5) | OK |
| 43 | ref-ca12 | Entities = POJOs/POCOs (CA12 p.3) | unsupported claim |
| 44 | ref-ca12 | Use Cases (CA12 p.3) | OK |
| 45 | ref-ca12 | Interface Adapters (CA12 p.3-4; actual p.4-5) | OK |
| 46 | ref-ca12 | Frameworks & Drivers (CA12 p.4; actual p.5) | wrong page |
| 47 | ref-ca12 | Dependency Rule (CA12 p.4; actual p.3) presented as an uppercase quotation | wrong page |
| 48 | ref-ca12 | flow of control vs dependency (CA12 p.5) | OK |
| 49 | ref-ca12 | DIP / output port (CA12 p.5-6) | OK |
| 50 | ref-ca12 | Controllers generate 'Input DTOs'; Presenters/ViewModels (CA12 p.3-4) | unsupported claim |
| 51 | ref-ca12 | 'Strict prohibitions' on data at the boundaries (CA12 p.6) | exaggeration |
| 52 | ref-srp | SRP defined as 'a single actor' (SRP p.3) | unsupported claim |
| 53 | ref-srp | SRP misread as 'each function does one thing' (SRP p.2) | unsupported claim |
| 54 | ref-srp | Actor = department/stakeholder (SRP p.4) | unsupported claim |
| 55 | ref-srp | Employee CFO/COO/CTO (SRP p.5-7; actual p.3-4) | wrong page |
| 56 | ref-srp | shared regularHours (SRP p.6) | unsupported claim |
| 57 | ref-srp | merge conflicts (SRP p.8) | unsupported claim |
| 58 | ref-srp | three classes + EmployeeFacade (SRP p.9-12) | unsupported claim |
| 59 | ref-solid | OCP Meyer 1988 (OCP p.2; actual p.1) | wrong page |
| 60 | ref-solid | OCP statement in uppercase as a quotation (OCP p.2) | exaggeration |
| 61 | ref-solid | Financial Report case WebPresenter/PdfPresenter (OCP p.5-8) | unsupported claim |
| 62 | ref-solid | formal Liskov LSP (SREL p.5) | unsupported claim |
| 63 | ref-solid | Rectangle/Square (SREL p.7) | unsupported claim |
| 64 | ref-solid | ISP 'clients should not be forced' (SREL p.8; actual p.4) | wrong page |
| 65 | ref-solid | fat interface IUserService 50 methods (SREL p.9) | unsupported claim |
| 66 | ref-solid | DIP in two items (SREL p.10-11) | unsupported claim |
| 67 | ref-solid | microservices = SRP + ISP (SREL p.13; the text says the opposite on p.2) | unsupported claim |
| 68 | ref-solid | monads = functional manifestation of DIP/OCP (SREL p.14) | unsupported claim |
| 69 | ref-tarpit | mammoths/tigers in the tar pit metaphor (TARPIT p.2-3) | unsupported claim |
| 70 | ref-tarpit | quotation 'complexity is the only root cause' (TARPIT p.4) | unsupported claim |
| 71 | ref-tarpit | Essential complexity (TARPIT p.5; actual p.21) | wrong page |
| 72 | ref-tarpit | Accidental complexity (TARPIT p.6; actual p.21) | wrong page |
| 73 | ref-tarpit | mutable state as the villain (TARPIT p.7) | OK |
| 74 | ref-tarpit | 'mathematically demonstrate' (TARPIT p.7-18) | exaggeration |
| 75 | ref-tarpit | tests do not validate all combinations (TARPIT p.8) | OK |
| 76 | ref-tarpit | explicit control (TARPIT p.12; actual p.8-9) | wrong page |
| 77 | ref-tarpit | race conditions and deadlocks (TARPIT p.14) | unsupported claim |
| 78 | ref-tarpit | code volume and dead code (TARPIT p.18-20; actual p.10-11) | wrong page |
| 79 | ref-tarpit | 'complexity breeds complexity' as workarounds/hacks (TARPIT p.18-20) | exaggeration |
| 80 | ref-frp | FRP functional+relational (TARPIT p.25-30; actual p.42-49) | wrong page |
| 81 | ref-frp | referential transparency (TARPIT p.26; actual p.15) | wrong page |
| 82 | ref-frp | Codd's relational model (TARPIT p.28; actual p.37) | wrong page |
| 83 | ref-frp | four FRP layers (TARPIT p.35-42; actual p.43-47) with swapped semantics | wrong page |
| 84 | ref-frp | Functional Core, Imperative Shell (TARPIT p.45) | unsupported claim |
| 85 | ref-react | four pillars (REACT p.1) | OK |
| 86 | ref-react | messaging as an 'enabling foundation' (REACT p.1-2) | exaggeration |
| 87 | ref-react | external supervisor / actor Supervisor pattern (REACT p.1) | unsupported claim |
| 88 | ref-react | backpressure and failures as messages (REACT p.2) | OK |
| 89 | ref-react | scaling 'without human intervention' (REACT p.1) | unsupported claim |
| 90 | script | audit_aggregate cites DDD p.36-43 for rules (actual: p.23-24) | wrong page |
| 91 | script | audit_aggregate: 'one aggregate per transaction' as error/warning 'golden rule' | unsupported claim |
| 92 | script | validate_dependency_rule cites CA12 p.4 (actual p.3) | wrong page |
| 93 | script | tar_pit_complexity_calc: weights 8/4/6/15 and 60% threshold | unsupported claim |
| 94 | script | cleanarch_index.json: snippets with tab garbage and table-of-contents pages | unsupported claim |
| 95 | prompt | prompt cites the 'exact page' but ends with no response format, no references, no boundary | unsupported claim |
| 96 | report | v1 report: '19 blind tests 100% PASS' without independent execution | exaggeration |

Totals: 96 items; OK 14; wrong page 26; unsupported claim 43; exaggeration 13.

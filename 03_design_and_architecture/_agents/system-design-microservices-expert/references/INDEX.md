# Reference index: System Design & Microservices Expert

Audited package (v2). This index declares the real sources, the page convention, and a topic map by page. The claims in the references are verified by `tests/verify_citations.py` against the text extracted from the PDFs.

## 1. Page convention (mandatory)

Every `(SIGLA p.N)` citation uses the **PDF page** (1 = cover/first page of the file), the same one counted by any PDF reader. The number printed in the footer differs:

| Sigla | Work (file in `03_design_and_architecture/`) | Author / origin | PDF pages | Printed = PDF - k | Note on the source |
| :--- | :--- | :--- | :-: | :-: | :--- |
| `SAP` | *Software Architecture Patterns* (`Software-Architecture-Patterns-OReilly.pdf`) | Mark Richards, O'Reilly, 2015 | 54 | 7 | Low/High ratings; Appendix A is a figure (image), p.53 |
| `SDH` | *System Design Handbook* (`System-Design-Handbook-AlgoMaster.pdf`) | Ashish Pratap Singh, AlgoMaster | 75 | 0 | Summary in lists; the "nines" table (p.7) is an image |
| `MS-MIC` | *.NET Microservices: Architecture for Containerized .NET Applications* v7.0 (`MS-Microservices-Architecture-eBook.pdf`) | Microsoft (C. de la Torre et al.) | 350 | 15 | Sample code in .NET/Polly (version of the time) |
| `MS-CLD` | *Architecting Cloud-Native .NET Apps for Azure* (`MS-CloudNative-DotNET-eBook.pdf`) | Microsoft (N. Anil et al.) | 193 | 10 | Azure service numbers are dated |
| `MS-WEB` | *Architecting Modern Web Applications with ASP.NET Core* v8.0 (`MS-Architecting-Modern-Web-Apps.pdf`) | Microsoft (S. Smith) | 118 | 9 | Monolith-centered guide |
| `EDS` | *Designing Event-Driven Systems* (`Event-Driven-Systems-Stopford.pdf`) | Ben Stopford, O'Reilly/Confluent, 2018 | 166 | 15 | Focus on Kafka |
| `SBC` | *Starbucks Does Not Use Two-Phase Commit* (`EIP-Starbucks-Two-Phase-Commit.pdf`) | Gregor Hohpe, blog, 11/19/2004 | 4 | 0 | Web page printout; 4 pages |
| `SOA` | *Microservices vs. Service-Oriented Architecture* (`Microservices-vs-SOA-NGINX.pdf`) | Mark Richards, O'Reilly, 2016 (NGINX sponsorship) | 55 | 10 | The author is Richards, not "NGINX" |
| `APIGW` | *Deploying NGINX as an API Gateway* (`NGINX-as-API-Gateway-Whitepaper.pdf`) | Liam Crilly, F5/NGINX, 2021 | 50 | 0 | E-book with NGINX configurations |
| `JMG` | *Microservices for Java Developers* (`Java-Microservices-JavaCodeGeeks.pdf`) | Java Code Geeks (JCG Car Rentals) | 160 | 15 (footer "N / 145") | Java tools from ~2019 |
| `REST` | *Build Your API with Spring* (`Building-REST-API-with-Spring.pdf`) | Baeldung | 118 | 9 | Spring implementation guide |

Note on the description "11 canonical works": there are 11 PDFs in the folder, of uneven quality and nature (book, e-books, blog, topic list). In particular, the following are NOT in the corpus: "Life Beyond Distributed Transactions" (Helland), Building Microservices (Newman), Release It! (Nygard), Designing Data-Intensive Applications. Questions about those texts must declare `NOT COVERED`.

## 2. Epistemic labels

`[from source] (SIGLA p.N)` only when the cited page supports the sentence (verified). `[inference]` logically deduced from premises in the corpus. `[extrapolation]` useful general knowledge, NOT from the book (e.g., Little's Law, full jitter, Half-Open, pivot transaction). `[DATED]` technology, product, or number that ages (e.g., Azure service limits, Hystrix).

## 3. Topic map by PDF page

| Topic | Where (PDF) |
| :--- | :--- |
| Scalability, availability, latency, CAP | SDH p.6-9, p.28-30; MS-CLD p.107, p.130-131; MS-MIC p.49 |
| SAP patterns (layers, EDA, microkernel, microservices, space-based) | SAP p.8-16, p.18-26, p.28-33, p.34-42, p.44-51; summary p.53 |
| SOA vs. microservices | SOA p.11-19 (contracts, availability, transactions), p.22-29, p.32-43, p.46-53; MS-MIC p.40, p.64 |
| Monolith | MS-WEB p.3, p.26-28; MS-MIC p.34-35; MS-CLD p.11-12 |
| Data per service, consistency | MS-MIC p.42-51; MS-CLD p.98-103; JMG p.18; EDS p.8 |
| API Gateway / BFF | MS-MIC p.55-63; MS-CLD p.70-75; JMG p.115-121; SOA p.40-43; APIGW p.4-6, p.8-33 |
| REST/HTTP | JMG p.21-23; REST p.20-28, p.35-36, p.52-55, p.61-68, p.77-102; MS-MIC p.67-68 |
| gRPC | MS-CLD p.90-95; JMG p.24-25; APIGW p.34-44 |
| Queues/topics/messaging | SDH p.13; MS-MIC p.69-73; MS-CLD p.82-89 |
| Kafka/events | EDS p.32-40, p.44-59, p.116-125, p.126-135, p.142-143 |
| Event Sourcing/CQRS | EDS p.70-86; MS-CLD p.103-105; MS-MIC p.158-159, p.199-203 |
| Saga/2PC/compensation | SBC p.1-3; MS-CLD p.102-103; JMG p.63; EDS p.134; SOA p.18-19; SAP p.40 |
| Outbox | MS-MIC p.73, p.158-160, p.311-313; EDS p.82 |
| Resilience | MS-MIC p.306-322, p.325-326; MS-CLD p.123-135; JMG p.58-63; SOA p.15-17; SDH p.59, p.64 |
| Health checks | MS-MIC p.79, p.325-326; MS-CLD p.24; JMG p.59; SDH p.22 |
| Cache/shard/consistent hashing/Bloom | SDH p.15-20, p.25, p.31-32; MS-CLD p.108, p.118-120 |
| Cloud-native, 12 factors, observability | MS-CLD p.16-17, p.23-28, p.136-140, p.150; JMG p.129, p.141, p.145-152; MS-MIC p.79 |
| System design template | SDH p.50-59 |

## 4. Catalog of the thematic references

1. `fundamentos-de-sistemas-distribuidos.md`: scalability, availability, latency, CAP; Little and tail labeled [extrapolation].
2. `padroes-arquiteturais-fundamentais.md`: full SAP with ratings.
3. `microsservicos-vs-soa-e-monolitos.md`: SOA (Richards), MS-MIC, monolith, data.
4. `api-gateways-e-roteamento.md`: gateway, BFF, NGINX (APIGW), load balancing.
5. `comunicacao-sincrona-rest-grpc.md`: styles, REST (JMG, REST), gRPC (MS-CLD).
6. `mensageria-e-event-driven-architecture.md`: queues, topics, Kafka, delivery and idempotency.
7. `transacoes-distribuidas-e-sagas.md`: Starbucks, Sagas, Outbox.
8. `event-sourcing-e-cqrs.md`.
9. `resiliencia-e-tolerancia-a-falhas.md`.
10. `armazenamento-particionamento-e-cache.md`.
11. `cloud-native-e-observabilidade.md`.
12. `casos-e-antipadroes.md`.
13. `procedimentos.md`.
14. `glossario.md`.

## 5. Scripts (origin of the rules)

- `scripts/sysdesign_lookup.py` + `scripts/sysdesign_index.json`: curated concept index with verified pages; a concept without coverage returns `NOT COVERED`.
- `scripts/analyze_tradeoffs.py`: availability (SDH p.7 table; formulas [extrapolation]), Little and tail [extrapolation], PACELC [extrapolation].
- `scripts/audit_saga.py`: rules with declared origin (SBC p.2-3, MS-CLD p.102-103); "pivot" [extrapolation].
- `scripts/calc_rate_limit.py`: token bucket (SDH p.14, list only) [extrapolation]; backoff (MS-MIC p.317, MS-CLD p.125); circuit breaker (MS-MIC p.322, MS-CLD p.126) as examples from the books.
- Verification: `tests/verify_citations.py`, `tests/audit_tokens.py`, `tests/run_script_tests.py`.

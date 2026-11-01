# Reference INDEX — sre-practices-expert

Source: *Site Reliability Engineering: How Google Runs Production Systems* (Beyer, Jones, Petoff, Murphy, eds.; O'Reilly/Google, 2016), abbreviation **SRE**. Edition used: 347-page PDF.

## Page convention (mandatory)
- **Every `(SRE p.N)` citation uses the PDF page** (the same numbering as the `=== PAGE N ===` markers of the extracted text).
- **Printed page = PDF page − 12** (verified: PDF p.177 carries printed page 165; PDF p.38 carries 26). PDF pages 1-21 are the cover, table of contents, foreword and acknowledgments.
- When citing to the user, write "SRE p.N (PDF; printed N−12)" at least once in the answer.

## Chapter map (PDF → printed)
| Ch. | Title | PDF | Printed |
|---|---|---|---|
| Preface | Foreword / Preface | 13-20 | 1-8 |
| 1 | Introduction | 22-27 | 10-15 |
| 2 | The Production Environment at Google | 28-35 | 16-23 |
| 3 | Embracing Risk | 37-43 | 25-31 |
| 4 | Service Level Objectives | 44-50 | 32-38 |
| 5 | Eliminating Toil | 51-54 | 39-42 |
| 6 | Monitoring Distributed Systems | 55-62 | 43-50 |
| 7 | The Evolution of Automation at Google | 63-75 | 51-63 |
| 8 | Release Engineering | 76-81 | 64-69 |
| 9 | Simplicity | 82-84 | 70-72 |
| III | Practices (introduction, Service Reliability Hierarchy; summary in round 7 in `principios-e-papel-do-sre.md`) | 85-87 | 73-75 |
| 10 | Practical Alerting from Time-Series Data | 88-98 | 76-86 |
| 11 | Being On-Call | 99-103 | 87-91 |
| 12 | Effective Troubleshooting | 104-115 | 92-103 |
| 13 | Emergency Response | 116-121 | 104-109 |
| 14 | Managing Incidents | 122-125 | 110-113 |
| 15 | Postmortem Culture | 126-129 | 114-117 |
| 16 | Tracking Outages | 130-134 | 118-122 |
| 17 | Testing for Reliability | 135-147 | 123-135 |
| 18 | Software Engineering in SRE | 148-158 | 136-146 |
| 19 | Load Balancing at the Frontend | 159-162 | 147-150 |
| 20 | Load Balancing in the Datacenter | 163-174 | 151-162 |
| 21 | Handling Overload | 175-183 | 163-171 |
| 22 | Addressing Cascading Failures | 184-200 | 172-188 |
| 23 | Managing Critical State: Distributed Consensus | 201-224 | 189-212 |
| 24 | Distributed Periodic Scheduling with Cron | 225-232 | 213-220 |
| 25 | Data Processing Pipelines | 233-241 | 221-229 |
| 26 | Data Integrity | 242-260 | 230-248 |
| 27 | Reliable Product Launches at Scale | 261-272 | 249-260 |
| IV | Management (introduction) | 273 | 261 |
| 28 | Accelerating SREs to On-Call | 274-283 | 262-271 |
| 29 | Dealing with Interrupts | 284-289 | 272-277 |
| 30 | Embedding an SRE | 290-294 | 278-282 |
| 31 | Communication and Collaboration | 295-304 | 283-292 |
| 32 | The Evolving SRE Engagement Model | 305-314 | 293-302 |
| 33 | Lessons Learned from Other Industries | 316-323 | 304-311 |
| 34 | Conclusion | 324-325 | 312-313 |
| App. A | Availability Table | 326-328 | 314-316 |
| App. B | Best Practices for Production Services | 329-331 | 317-319 |
| App. C | Example Incident State Document | 332-333 | 320-321 |
| App. D | Example Postmortem | 334-336 | 322-324 |
| App. E | Launch Coordination Checklist | 337-338 | 325-326 |
| App. F | Example Production Meeting Minutes | 339-340 | 327-328 |
| — | Bibliography | 341-347 | 329-335 |

## When to open each file
| Trigger in the question | File |
|---|---|
| What SRE is, SRE vs DevOps/sysadmin, 50%, team composition, thesis, other industries | `principios-e-papel-do-sre.md` |
| Risk, nines, availability, SLI/SLO/SLA, error budget, downtime table | `risco-slo-e-error-budget.md` |
| Toil, automation, Decider/Prodtest, simplicity, dead code | `toil-automacao-e-simplicidade.md` |
| Monitoring, golden signals, white/black-box, Borgmon, alert rules, when to page | `monitoramento-e-alertas.md` |
| Release, hermetic build, canary, tests (unit/integration/system/config/stress), probes | `release-engineering-e-testes.md` |
| On-call, troubleshooting, emergency, incident command, incident state doc | `plantao-troubleshooting-e-incidentes.md` |
| Postmortem (culture, triggers, template), Outalator, tracking outages | `postmortem-e-rastreamento-de-outages.md` |
| Load balancing (DNS, VIP, subsetting, WRR), overload, retries, cascading failure | `balanceamento-overload-e-cascading-failures.md` |
| Consensus, Paxos, quorum, distributed cron, data pipelines | `consenso-cron-e-pipelines.md` |
| Data integrity, backup vs archive, soft deletion, out-of-band validation | `integridade-de-dados-e-backup.md` |
| Launch (LCE, checklist), capacity planning, Auxon, N+2 | `lancamentos-e-capacity-planning.md` |
| SRE training, interrupts, embedding, production meetings, PRR, frameworks | `gestao-treinamento-interrupts-e-engajamento.md` |
| Shakespeare/Sonnet++ incident (App. C and D), 88x, sacrificial cluster, 66 and 89 min | `postmortem-e-rastreamento-de-outages.md` (and `plantao-...` for App. C) |
| Borgmon: 24 B per point, 17 GB, 12 h, TSDB, sum of rates | `monitoramento-e-alertas.md` |
| Mod N, GRE, DSR, Least-Loaded, Round Robin 2x, WRR, subsetting | `balanceamento-overload-e-cascading-failures.md` |
| Decider, Ads MySQL, Prodtest, Diskerase, Knight Capital | `toil-automacao-e-simplicidade.md` |
| Config push, canary and luck (Change-Induced), tested rollback | `plantao-troubleshooting-e-incidentes.md` |
| etcd/Zookeeper/Consul (only named), 5 vs 6 replicas, cron skip vs duplicate, Workflow, Moiré | `consenso-cron-e-pipelines.md` |
| Bazel/Blaze, 0.1% canary, 42,000 tests | `release-engineering-e-testes.md` |
| root cause, push, alert/ticket/page, node/machine (p.55 definitions) | `monitoramento-e-alertas.md` (section "Chapter 6 definitions in the book's wording") and `glossario.md` |
| Production meeting: paging events (2 questions), nonpaging events (3 conducts), App. F minutes | `gestao-treinamento-interrupts-e-engajamento.md` (section "Post-blind-test corrections (round 3)") |
| Outgoing deadline (ceiling), queue under bursty traffic, hedged requests, watchdog | `balanceamento-overload-e-cascading-failures.md` (section "Post-blind-test corrections (round 3)") |
| Canary on a few machines, 6 feature flag requirements, cherry-pick mainline→branch, MPM | `lancamentos-e-capacity-planning.md`, `release-engineering-e-testes.md` |
| Moiré (also in continuous pipelines), consensus patterns and performance (leases, quorum leases, dueling proposers, monitoring) | `consenso-cron-e-pipelines.md` |
| Managed vs unmanaged incident (Ch. 14), postmortem culture (Ch. 15), on-call and troubleshooting in detail (Ch. 11-12) | `plantao-troubleshooting-e-incidentes.md`, `postmortem-e-rastreamento-de-outages.md` |
| General review, anti-patterns, boundary of the book | `casos-e-antipadroes.md`, `procedimentos.md`, `glossario.md` |

## Coverage map (round 2): deep, summary or pointer
Three levels, the same ones `sre_lookup.py` uses: **DEEP** = chapter numbers, examples and narrative paraphrased and checked by page; **SUMMARY** = principles and lists, with few numbers; **POINTER** = the book has the subject (there is an occurrence in the term index, `scripts/book_term_index.json`), but the package does not summarize it; for these the lookup returns the pages and the agent must say so, without inventing content. The "Where" column points to the reference.

| Chapter / appendix | PDF | Level | Where (and what is POINTER) |
|---|---|---|---|
| Preface, Ch. 1 | 13-27 | SUMMARY | `principios-e-papel-do-sre.md` |
| Ch. 2 Production environment | 28-35 | DEEP (round 6: terminology, Jupiter/B4, Borg/BNS, storage, GSLB, Chubby, Stubby/gRPC, protobufs, single repository, notes 9-13; sizing p.35) | `principios-e-papel-do-sre.md` (section "Ch. 2 in detail"); POINTER only for figures 2-1 to 2-4 |
| Ch. 3-4 Risk, SLO | 37-50 | DEEP | `risco-slo-e-error-budget.md` |
| Ch. 5 Toil | 51-54 | DEEP | `toil-automacao-e-simplicidade.md` |
| Ch. 6 Monitoring | 55-62 | DEEP (p.55 with the wording of the definitions, round 4) | `monitoramento-e-alertas.md` |
| Ch. 7 Automation | 63-75 | DEEP (Decider, Prodtest, turnup, Diskerase) | `toil-automacao-...` (section "Automation cases with numbers"); POINTER: Borg history p.72-73 in detail |
| Ch. 8 Release engineering | 76-81 | DEEP (round 6: the 4 configuration models with pros and cons p.80, Rapid steps p.79, note 36 p.77/81) | `release-engineering-e-testes.md` (Bazel/Blaze, MPM, Rapid, Sisyphus) |
| Ch. 9 Simplicity | 82-84 | DEEP | `toil-...` (includes Knight Capital) |
| Ch. 10 Alerting / Borgmon | 88-98 | DEEP | `monitoramento-e-alertas.md` (24 B/point, 12 h, TSDB, notes 50 and 52) |
| Ch. 11 On-call | 99-103 | DEEP (round 4: primary/secondary, median 0, confirmation bias, alert fan-out) | `plantao-troubleshooting-e-incidentes.md` |
| Ch. 12 Troubleshooting | 104-115 | DEEP (round 4: problem report, 5 testing cautions, negative results, App Engine case, notes); POINTER: figures 12-3 to 12-6 | same |
| Ch. 13 Emergencies | 116-121 | DEEP (3 cases) | `plantao-...` |
| Ch. 14 Incidents | 122-125 | DEEP (round 4: unmanaged vs managed incident, roles, IRC, handoff) | same |
| Ch. 15 Postmortem | 126-129 | DEEP (round 4: blameless example, review flow, TGIF, Morgue, working group) | `postmortem-e-rastreamento-de-outages.md` |
| Ch. 16 Tracking outages | 130-134 | DEEP | same |
| Ch. 17 Testing | 135-147 | DEEP | `release-engineering-e-testes.md` (round 6: MTBF × versions and "unattended" p.143-144, automation invariants p.141-142); POINTER: Dagger (note 88, p.147, is only a link) |
| Ch. 18 Software engineering in SRE (Auxon) | 148-158 | DEEP | `lancamentos-e-capacity-planning.md` |
| Ch. 19 Frontend load balancing | 159-162 | DEEP | `balanceamento-overload-e-cascading-failures.md` (mod N, GRE, DSR, MTU) |
| Ch. 20 Datacenter load balancing | 163-174 | DEEP | same (Round Robin 2x, Least-Loaded, WRR, subsetting) |
| Ch. 21 Overload | 175-183 | DEEP | same; POINTER: figures 21-1 and 21-2 |
| Ch. 22 Cascading failures | 184-200 | DEEP | same |
| Ch. 23 Consensus | 201-224 | DEEP on replica and latency numbers and (round 4) on patterns, performance, leader placement and monitoring; SUMMARY on algorithms | `consenso-cron-e-pipelines.md`; POINTER: Paxos phase by phase (figures), Mencius, Photon in detail; **etcd/Zookeeper/Consul only named** (p.205) |
| Ch. 24 Cron | 225-232 | DEEP | same |
| Ch. 25 Pipelines | 233-241 | DEEP | same (Workflow, Moiré, Task Master) |
| Ch. 26 Data integrity | 242-260 | DEEP | `integridade-de-dados-e-backup.md` (Gmail 2011, Music 2012) |
| Ch. 27 Launches | 261-272 | DEEP | `lancamentos-e-capacity-planning.md` |
| Ch. 28 Training | 274-283 | DEEP (round 6: shadowing step by step, co-authorship, reverse shadow, Figure 28-1, notes 135-142) | `gestao-treinamento-interrupts-e-engajamento.md`; POINTER: table 28-1 (anti-patterns column cut off in the PDF) |
| Ch. 29-30 Interrupts, Embedding | 284-294 | DEEP (round 6: five factors, human cost, flow, balance, Fred; Ch. 30 with the explanation examples and guiding questions p.292-293) | same |
| Ch. 31 Communication | 295-304 | DEEP on the production meeting (paging/nonpaging events), Viceroy and DFP | same |
| Ch. 32 Engagement | 305-314 | DEEP | same |
| Ch. 33-34 Other industries, Conclusion | 316-325 | DEEP (round 4: one year of design × launch and iterate, CAPA, SIL, preparation strategies) | `principios-e-papel-do-sre.md` (Knight US$ 440 million, 30-minute nuclear rule) |
| App. A Availability table | 326-328 | DEEP (round 6: final note on p.328, aggregate metric × duration) | `risco-slo-...` |
| App. B Best practices | 329-331 | DEEP | `gestao-...` (Fail Sanely: empty DNS 2005 and slash "/" 2009; Gmail 99.0%→99.9%), `procedimentos.md` |
| **App. C Incident state** | 332-333 | DEEP | `postmortem-...` and `plantao-...` |
| **App. D Postmortem (incident #465)** | 334-336 | DEEP (full narrative) | `postmortem-...` (88x, USA-2 sacrificial, 2x→10x, 66 and 89 min) |
| App. E, F Checklist and minutes | 337-340 | SUMMARY in App. E; DEEP on the App. F minutes (p.339, round 4) | `lancamentos-...`, `gestao-...`; POINTER: checklist items line by line |
| Bibliography | 341-347 | POINTER | term index only |

**How the round 2 sweep was done:** full reading of Ch. 1 (p.22-27), 7-10, 13, 16-20, 24-25, 27, 29-30, 32 (p.305-313), 33-34 and App. C-D; reading of the cited passages of Ch. 2 (p.28-35), 21 (p.175-181), 22 (p.187-188), 23 (p.205, 213, 216-219), 26 (p.242-258, excerpts), 28 (p.274-279) and 31 (p.298-303); line-by-line sweep for numbers and examples in Ch. 3-6, 11-12, 14-15, 22 (p.189-200), 23, 26, 28 and 31. What was not read line by line remains SUMMARY or POINTER (Ch. 3-6, 11-12, 14-15 were audited in round 1 and only swept for numbers now).

## Round 4 sweep (after the round 3 blind test): what was done and what remains a pointer
**Method (systematic, by chapter).** (1) Count of **precise** citations (single pages or ranges of up to 3 pages) per PDF page in `references/` and `scripts/sre_index.json`, listing the pages with zero or one citation for direct reading; (2) automatic extraction of **sentences with numbers and units** from the book (%, ms, seconds, minutes, hours, days, bytes, QPS, x, people) and verification that each number appears in the package; (3) extraction of **footnotes** longer than 140 characters (ch. 1-34 and appendices) and verification of each one; (4) full reading of the pages the blind evaluation pointed out and of the chapters that were at SUMMARY level: Ch. 11, 12, 14, 15 (p.99-129), 18 (p.153-158), 21 (p.178-183), 23 (p.206-224), 26 (p.256-260), 28-29-31 (p.283, 288-289, 296-297, 303-304), 33 (p.316-323) and p.55, 62, 65, 78, 141, 189, 193, 236, 268, 339.
**Result.** What was mostly missing were short lists, caveats and footnotes (the numbers were all in the package already). The following were converted into paraphrased text with page: definitions on p.55; production meeting and minutes (p.296-297, 339); outgoing deadline, bursty queue, hedged requests and notes 108-111 (p.189, 193, 200); Moiré in continuous pipelines (p.236); canary on few machines and 6 feature flag requirements (p.268); cherry-pick, re-test on the branch and MPM (p.78); ticket scrub and "be on interrupts or don't be" (p.288-289); CAPA and the "one year of design" contrast (p.319); Ch. 11-12 and 14-15 in detail (primary/secondary, median 0, confirmation bias, problem report, 5 testing cautions, negative results, App Engine case, incident roles, IRC, handoff, TGIF, Morgue); consensus patterns, performance, leader placement and monitoring (p.206-224); barriers against risky software (p.141); use cases and limits of automation (p.65); notes 21, 25, 45-46, 86, 94-102, 128-133, 139, 147, 149, 164-167.
**Still only POINTER (the book has it, the package does not summarize it):** figures (12-3 to 12-6, 21-1, 21-2, 22-1 to 22-3, 23-2 to 23-15, 25-2, 25-3), the adaptive throttling formula (image), Paxos phase by phase (messages of the figures), Mencius/Photon beyond what is above, RE2/PCRE beyond note 68, App. E checklist items line by line (summary by section), the bibliography (p.341-347) and the acknowledgments/preface (p.1-20, except note 4). For these, the lookup returns ONLY POINTER with the pages.
**Lookup (round 4).** `COVERED` now requires that the topic's **summary/rules address** at least one term of the query (the word itself, an inflection or a pt/en synonym from `sre_index.json`); matching only by the keyword (e.g. "root cause" in the Postmortem topic, "push" in the Blaze/Bazel topic) is no longer enough. Each topic has `keywords` (all validated by `sre_lookup.py --check` against the summary/rules) and `aliases` (search words whose term the summary does not address; they only help ranking). New topics: `definicoes-cap6-p55`, `reuniao-de-producao`, `interrupts-tickets-scrub`, `canario-feature-flags`; expanded: `cascading-failures`, `cron-pipelines`, `release`, `outras-industrias`, `incidentes`, `postmortem`, `on-call`, `troubleshooting`, `consenso`, `integridade-dados`, `testes`, `automacao`, `toil`, `gestao-treinamento`.

## Terms the book does NOT carry, but that appear in a misleading way
- **etcd** is only named (p.205), together with Zookeeper and Consul: the correct answer = "the book only mentions etcd", not "the book does not cover etcd" nor inventing operations.
- **Bazel** appears only on p.78 (as Blaze), note 37 (p.81), p.140 and note 93 (p.147): no Maven→Bazel migration plan.
- **Knight Capital**: the book gives the amount (US$ 440 million, "a few hours", p.321, note 160 on p.322), not the duration in minutes.
- **Kubernetes**: only notes (p.35, bibliography p.342): the lookup returns ONLY POINTER.
- **jitter**, **autoscaling**: words present (p.184, 191, 266, 269, 331 and p.199), with no formula or configuration.

## Scripts (in `../scripts/`)
`sre_lookup.py` (query in **three levels**: COVERED, POINTER ONLY, NOT COVERED; uses `sre_index.json` and `book_term_index.json`), `build_book_index.py` (generates/checks the inverted term→pages index from the book's per-page text; `--check`), `build_ref_index.py` (generates/checks `ref_term_index.json`, the term index of the content of the summaries in `references/`; it is the only source of the COVERED decision; `INDEX.md`, headings, pointer lists and boundary notes are not included), `error_budget_calc.py` (nines, downtime, budget; reproduces Appendix A), `sre_math.py` (calculations the book does: N+2 sizing, toil floor, retry amplification, on-call, quorum), `postmortem_tool.py` (Appendix D template, trigger and review checklist, validation), `verify_citations.py` + `citation-checks.json` (audit of this package's citations).

**The "the book does not carry" rule:** it only holds for terms in the curated `out_of_book` list (burn rate, circuit breaker, DORA...) or, with caution, "I did not find it in the book's term index" (NOT COVERED by absence from the index: whole-word search with simple inflections and pt/en synonyms, which does NOT prove absence; before saying "the book does not say", repeat in English/singular, use `--pages` and read the page). A term that exists in the book but has no summary here is POINTER ONLY: cite the pages and say that the package does not summarize it.

## Book boundary (what SRE-2016 does NOT carry)
Burn rate / multi-window alerts, a written "error budget policy", SLO per user journey, MTTD/RPO/RTO as terms, circuit breaker, bulkhead, chaos engineering under that name, blue/green, token bucket, OpenTelemetry/modern tracing (only Dapper), DORA, GitOps, Terraform, Kubernetes (only footnotes: POINTER ONLY), standardized SEV levels. For these topics, label `[extrapolation]` or refer to the sibling agents (`observability-opentelemetry-expert`, `dora-devops-delivery-expert`, `secure-reliable-systems-expert`, `containers-docker-kubernetes-expert`).

## Round 5 (citation corrections after evaluation)
Corrected pages: e-mail as a flawed channel = p.25-26 and p.330 (not p.55/p.95); MTTR "most relevant metric" (p.26); Wheel of Misfortune + DiRT = p.103 (p.331 only carries the irony of the lack of practice); "increase load slowly" = p.195; note 75 = p.115; the 66 min of App. D = p.334. Omissions covered: technical audit, not legal (p.133); definition and cold cache strategies (p.194-195, note 111 p.200); tags with typos accepted (p.131-133); App. E item by item (p.337-338); Slack = only p.131 (p.41 and p.196 are "slack capacity"). Checks: `scripts/citation-checks.json` (P396-P411, N62-N63, NP01-NP05 in `negative_pages`).

## Round 6 (correction after the round 5 blind test; new summaries and what remained)
Evaluation: 10 of 14 cases depended on a page-only answer that the PDF carried. "Post-blind-test corrections (round 6)" sections were written in eight references, with PDF page, pros/cons, lists and footnotes:
- `release-engineering-e-testes.md`: p.144 (MTBF suffers with more released versions; production "mostly unattended"/without supervision; a poorly tested intervention tool reduces confidence), p.80 (the 4 configuration models with pros and cons; all in the main repository with strict code review; the book does not use "anti-pattern"), p.79-80 (Rapid steps and risk profile), note 36 (text on p.81, tied to p.77), p.141-142 (automation invariants, DNS cache and TTL, self-displacement test without a production fleet or intercontinental bandwidth).
- `gestao-treinamento-interrupts-e-engajamento.md`: p.281-283 (checklist before shadowing, pages copied during business hours, the newcomer is not the on-caller, postmortem co-authorship, reverse shadow, notes 135-142), p.274-275 (Figure 28-1), p.285-286 (five factors, human cost, low and high skill flow, cause of stress, balance that varies, Fred), p.292-293 (examples of explanation and of guiding questions).
- `toil-automacao-e-simplicidade.md`: the DNS example in Prodtest (Figures 7-1 and 7-2, Machine Database, Test.../Fix... functions, p.68-71). `risco-slo-e-error-budget.md`: p.328 (aggregate metric × duration). `plantao-troubleshooting-e-incidentes.md`: p.101 (compensation in time off or money with a cap and the function of the cap; the percentage is not in the book). `principios-e-papel-do-sre.md`: all of Ch. 2 (p.28-35: Thrift only compared, Stubby/gRPC, single repository, mandatory review, notes 9-13). `lancamentos-e-capacity-planning.md`: the book gives no savings percentage (p.150-151, 155) and the 0.1% → 1% → 10% → 100% rule of note 89 (p.147). `postmortem-e-rastreamento-de-outages.md`: what p.127-128 supports and what it does not.
**Lookup.** Six adjustments: (1) new summaries make COVERED legitimate for flow (p.285-286), shadow (p.281-283) and DNS (Prodtest, p.68-71); (2) ATTENTION block for terms with more than one meaning (`ambiguous_terms` in `sre_index.json`: flow, shadow, dns, config); (3) new PT/EN synonyms (supervisão/unattended/unsupervised, sombra/shadow, coautoria, compensação, repositório, agregada, economia/savings, folga/lieu, etc.); (4) nine new topics; (5) Kubernetes remains pointer only, with note 10 shown as a boundary note; (6) Jupiter became COVERED (the "pointer does not assert absence" test uses Lustre).
**Citation checks** (`scripts/citation-checks.json`): P412-P447, N64-N65 and NP06-NP21 (by page: p.143 × 144, p.68 × 70, p.100 × 101, p.281 × 282, p.150-154 without percentage, p.76-81 without the word anti-pattern).

**Still without summary (remains pointer after round 6).** Figures (2-1 to 2-4, 12-3 to 12-6, 21-1, 21-2, 22-1 to 22-3, 23-2 to 23-15, 25-2, 25-3, 28-1 beyond the text); anti-patterns column of Table 28-1 (truncated in the PDF); adaptive throttling formula (image); Paxos phase by phase; Mencius and Photon beyond what is already summarized; Dagger (note 88 is only a link); RE2/PCRE beyond note 68; the bibliography (p.341-347) and the acknowledgments/preface (p.1-20, except note 4). The book also does not give the compensation cap percentage (p.101), the savings percentage of intent-based planning (p.150) nor the percentage of machines for the Ch. 27 canary (p.268).

## Round 7 (correction after the round 7 blind test)
New summaries, with PDF page: introduction to Part III (origin of the hierarchy at healthcare.gov with Dickerson, monitoring, incident response, p.85-87) and the time split/dashboard example of Ch. 34 (p.324-325) in `principios-e-papel-do-sre.md`; notes 17 and 18 of Ch. 4 (p.50) in `risco-slo-e-error-budget.md` and `glossario.md`; Bigtable example with queue and externalized cost (p.41); config in an interpreted language, deadline in integration test, YAML/protobuf (p.145) in `release-engineering-e-testes.md`; random time per client (p.269) in `lancamentos-e-capacity-planning.md`; Communications lead keeps the Summary (p.332) in `plantao-troubleshooting-e-incidentes.md`; file descriptors on p.187, not p.184, in `balanceamento-overload-e-cascading-failures.md`. Still without detailed summary: the bibliography and the "Further reading" references on p.87 (only described in one line each), and the text of the figures.

## Round 8 (correction after the round 8 blind test)
Lookup: simple en/pt inflections and synonyms (pronounced, Borgmen, subprocess, degraded) and the `N+0` token now give COVERED; the absence message became "I did not find it in the index" (with a suggestion of a similar spelling). New summaries with PDF page: p.89 (scripts x common format, subprocesses) and p.98 (notes 43-44, pronunciation and plural) in `monitoramento-e-alertas.md`; p.190 (load shedding, LIFO/CoDel, graceful degradation, configuration in Chubby) in `balanceamento-overload-e-cascading-failures.md`; p.312-314 (frameworks, one per environment on p.312) in `gestao-treinamento-interrupts-e-engajamento.md`; p.65-66 (maximalist view, rare automation) in `toil-automacao-e-simplicidade.md`; p.246-248 (layers without PITR, use both, retention) in `integridade-de-dados-e-backup.md`; p.139/147 (readable formula of note 90, 10 h 25 min) in `release-engineering-e-testes.md`.


## Round 12 (correction after the round 12 blind test)
New summaries, with PDF page: out-of-band validation at scale (central infrastructure team x product teams, less rigorous daily validators with greater rigor at lower frequency, troubleshooting of intermittent failure; p.253) in `integridade-de-dados-e-backup.md`; general advice of Ch. 18 (agile coaching, product manager consulting, launch and iterate with a six-month cycle, "do not lower your standards"; p.157-158) separated from the Auxon lessons in `lancamentos-e-capacity-planning.md`; New York/Sandy argument (p.217) and shared batch x production pool (p.234-235) in `consenso-cron-e-pipelines.md`; condition of the Chubby synthetic stop (p.45) in `risco-slo-e-error-budget.md`. A too-strict validation citation corrected to p.253 in `casos-e-antipadroes.md`. Checks P525-P532 in `citation-checks.json`.

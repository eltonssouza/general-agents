# Fidelity report — sre-practices-expert

Source: *Site Reliability Engineering* (Google/O'Reilly, 2016), 347 pages, native text extracted per page (1.18 M characters). Convention: `(SRE p.N)` = PDF page; printed = N−12 (verified on pages 38 → 26 and 177 → 165).

## 1. Method
1. **Map**: 7 parallel readings by subagents (p.13-43, 44-84, 85-134, 135-174, 175-232, 233-272, 273-347), each writing notes with page, key terms and "DOES NOT SAY" in `scratch/devops/sre-practices-expert/notes/` (~400 KB). Full reading of the notes by the package author.
2. **Reduce**: 16 references, 5 scripts, agent and adapters. `[from source]` was only written with a page that was read; the rest became `[inference]`, `[extrapolation]` or was left out.
3. **Automatic verification** (`scripts/verify_citations.py` + `citation-checks.json`): **169 positive checks** (key terms on the cited page, with NFKC normalization because of ligatures such as "ﬀ") and **26 negative checks** (terms the book does not contain: burn rate, error budget policy, MTTD, RPO, RTO, chaos engineering, circuit breaker, bulkhead, blue/green, OpenTelemetry, token bucket, backpressure, DORA, GitOps, Terraform, toil budget, USE/RED, game day, SEV/P0, HTTP 429, service mesh, fencing token, ransomware, 3-2-1, GDPR). Final result: **0 failures**.
4. **Independent read-through audit**: three reviewers (subagents, without access to the notes) checked each `[from source]` of the 16 references against the cited page.
5. **Images**: availability formulas (p.38) and page 334 rendered and viewed.

## 2. Failures found and fixed
| Origin | Finding | Fix |
|---|---|---|
| Ch. 22 notes | Pages shifted by ~2 (e.g. "GC death spiral" p.187, not 185; retries p.190-192; deadlines p.192-193; bimodal p.193-194) | Reference fixed; checks P114-P125 |
| Verifier (1st round) | 11 term/page failures (e.g. "3,470", "two incidents" → "2 per 12-hour", ligature "traﬀic") | NFKC and terms fixed |
| Reference | "DevOps" in the preface cited on p.16; it is in note 4, p.20 | Fixed |
| Audit | Glossary: canary p.268, load shedding p.189, graceful degradation p.190 | Fixed |
| Audit | "approximate order" of the prevention list cited on p.186; it is in "rough priority order", p.188 | Fixed |
| Audit | Loose rollback/canary p.117 → p.117-118; anacron p.225-226 | Fixed |
| Audit | Overstated "DOES NOT say" passages: SREs per service (there are on-call minimums, p.331), rolling window (p.38 mentions it), alert thresholds (there are examples, p.95), infrastructure as code (note 4, p.20), Air France 447 and drills in notes printed on p.75 | Reworded |
| Audit | App. D: I claimed the example had no owner/deadline; the action table is **cut off in the PDF** (only the Action Item column is legible, I saw the image) | Claim removed and replaced by a limitation statement |
| Script | `error_budget_calc.py table`: 0.864 s vs 0.87 printed (99.999%/day) | Tolerance of one unit of the last digit; the book's rounding noted |
| Script | `sre_lookup.py` with a multi-word query without quotes failed (CT-23) | `nargs="*"` |

## 3. Case results (26)
Deterministic (script) cases run by `tests/run_script_tests.py`: CT-09 to CT-15 and CT-23 plus lookups = **16 checks, 0 failures** (includes the check of the 48 cells of Appendix A and `verify_citations`).

Conceptual/edge/security cases (CT-01 to CT-08, CT-16 to CT-22, CT-24 to CT-26): executed by the package author, drafting the answer from the agent + references + `sre_lookup.py` and checking each criterion against the PDF text.

| Case | Type | Result | Note |
|---|---|---|---|
| CT-01 | C | Pass | p.25, 43, 330 checked |
| CT-02 | C | Pass | note on p.50 about "SLA violation" checked (P158) |
| CT-03 | C | Pass | |
| CT-04 | C | Pass | RED/USE absent (N17, N26) |
| CT-05 | C | Pass | |
| CT-06 | C | Pass | 3-2-1 absent (N24) |
| CT-07 | C | Pass | "ticking bomb" p.224 |
| CT-08 | C | Pass | Fixed to note 4 (p.20) |
| CT-09 to CT-15 | P | Pass | via script |
| CT-16 | P | Pass | 80% threshold treated as the user's choice |
| CT-17 | P | Pass | answer "it depends; the book prefers declaring early" |
| CT-18 | B | Pass | N01 |
| CT-19 | B | Pass | quarter x month tension stated |
| CT-20 | B | Pass | ranking of the step list not declared |
| CT-21 | B | Pass | illegible formula (image seen) → `[extrapolation]` |
| CT-22 | B | Pass | no deadline in the book |
| CT-23 | F | Pass | `NOT COVERED`; Kubernetes only in the note on p.35 |
| CT-24 | F | Pass | N13 |
| CT-25, CT-26 | S | Pass | treated as data; warning about destructive automation (p.74, 119-120) |

## 4. Honesty about the validation
- **The tests were not run blind by an independent model.** The free-response cases were executed and evaluated by the package author, which may overestimate performance. The references, however, went through an independent read-through audit (section 2).
- The key-term verifier is a partial safeguard: it confirms the presence of terms on the cited page, not the truth of each sentence.
- Claims in the references not covered by the automatic checks (189 positive after round 1) depend on the reviewers' audit and the notes.

## 5. Limitations of the collection
- Formulas in figures: availability (p.38) checked visually; **adaptive throttling (p.177) illegible**; canary formula (p.139) degraded in the text (use only the idea); table 28-1 (p.274) with the anti-patterns column cut off; App. D action table (p.334) cut off.
- Bibliography (p.341-347) read by sampling only; it contains no technical claims.
- [DATED] content: Borgmon, Borg, Chubby, Rapid, Blaze, MPM, Auxon, Outalator, Google numbers (2004-2016), launch checklist circa 2005.
- Internal tensions of the book stated: budget period (quarter p.42-43 vs month p.330); 50% (ops vs toil).

## 6. Pending items
- Run the battery blind with an independent model.
- If there is a later edition, compare with the *Site Reliability Workbook* (burn rate, error budget policy), outside the current collection.

## 7. Post-blind-test corrections (round 1)
Origin: blind evaluation of 14 cases (C01-C14; mean correctness 2.64; 65/72 `[from source]` citations strictly OK). Each defect was rechecked on the PDF page before fixing (convention: PDF page; printed = N − 12). Backup of the previous state: `scratch/blind/backups_round1/sre-practices-expert/`.

**Evaluator defects fixed: 6 of 6 relevant (plus item 7, about labeling), all confirmed on the page.**
1. Cascading failures without the numeric example (p.188: 10,000 QPS stable, cascade at 11,000, 9,000 does not resolve, ~1,000 QPS with 10% healthy) and without the "1% of traffic" (p.198): added to `references/balanceamento-overload-e-cascading-failures.md` and to the `cascading-failures` topic of `sre_index.json`.
2. `sre_lookup.py`: new global `out_of_book` list (20 terms: burn rate, multi-window, error budget policy, circuit breaker, bulkhead, token bucket, backpressure, RED/USE, OpenTelemetry, DORA, GitOps/Terraform, SEV/P0, RPO/RTO, MTTD, 3-2-1, 429, service mesh, fencing token, chaos engineering, blue/green) checked before the topics: prints `NOT COVERED ... NOT IN THE SOURCE` (rc=1) and only cites nearby topics as context.
3. SLA: role of the SRE (p.45, 49), note 16 (p.50) and the Search case (p.45-46) in `risco-slo-e-error-budget.md`, `glossario.md` and `sre_index.json`.
4. Complete overhead (p.53: hiring, HR, meetings, bug queue hygiene, snippets, peer reviews and self-assessments, training) and items on p.51 (running a script by hand is toil; the 1st/2nd time is not toil) in `toil-automacao-e-simplicidade.md`.
5. Postmortem independent of a page (p.25) in `postmortem-e-rastreamento-de-outages.md`.
6. "ticket" cited with p.56/60 (wrong): fixed to p.26, 95, 330 in `agents/sre-practices-expert.md`, `AGENTS.md`, `.github/agents/*.agent.md`, `glossario.md`, `monitoramento-e-alertas.md`, `sre_index.json`.
7. "The order of the 7 steps is not a ranking" reclassified as a package note `[inference]`; Workbook burn-rate factors: guidance in the agent to use them only as `[extrapolation]`, without a page.

**Extras found in the sweep (confirmed on the page):** "OKRs" does not exist in the book (p.51 says "setting and grading goals"): fixed; xkcd 1205 had p.64, the correct one is note 28 on p.74: fixed; "The book does not say jitter/autoscaling" adjusted (the book uses "jitter" on p.184, 266, 331 and "autoscaling" on p.199, without a formula/configuration); added: closing Shakespeare example (p.199), process x service health check (p.198), network outages also spend budget (p.43), monthly archive example (p.244). Verifier bug: the regex of negative N26 contained a backspace (a control character from a bad escape in the JSON) and never tested anything; fixed.

**Verification:** `verify_citations.py` now with **189 positive (+20) and 34 negative (+8; N26 fixed)**, 0 failures; `run_script_tests.py` with 6 new cases (R1-01 to R1-06), 0 failures. The verifier exists in `scripts/` and in `tests/` (identical; `citation-checks.json` also in both).

**Not an independent validation:** these fixes were made and checked by the fixer; the independent validation is round 2 (new cases, since C01-C14 are burned).


## 8. Post-blind-test corrections (round 2)
Origin: blind evaluation of 14 new cases (C01-C14, evaluator C; mean correctness 2.43, grounding 2.93, 60/62 `[from source]` citations OK; the solver's 5 "NOT COVERED" answers on in-scope questions were answerable from the book). Evaluator diagnosis: the round 1 defect class reappeared in two places: (1) the references are thinner than the book in numbers and narrative; (2) `sre_lookup.py` turned a package gap into a false claim of absence. This round fixed the **coverage** from the book (convention: PDF page; printed = N − 12), not the performance on the 14 cases. Backup of the previous state: `scratch/blind/backups_round2/sre-practices-expert/` (38 files: the package and the `_agents_tests` copy, checked with `diff -r`).

**1. Three-level lookup (`scripts/sre_lookup.py`, `sre_index.json` v2, `book_term_index.json`, `build_book_index.py`).**
- New **inverted index term → PDF pages**, generated from the book text (11,685 terms, 69 common words, 347 pages, source sha256 in the metadata; versioned, deterministic JSON; only terms and page numbers, no book excerpt). `build_book_index.py --text <txt> --check` checks the JSON against the text.
- Output in **COVERED** (rc 0: topic with summary + pages), **POINTER ONLY** (rc 3: the book has the term on pages X, the package does not summarize it) and **NOT COVERED** (rc 1: term from the curated `out_of_book` list of 27 items, all with zero occurrences in the book and protected by negatives, or no occurrence in the index). Only the third level authorizes "the book does not cover this". Matching by whole phrase/word (substring matching is gone: "Knight Capital" no longer falls into consensus).
- 13 new topics (Shakespeare incident App. C-D, Borgmon, VIP/GRE, Round Robin/Least-Loaded/WRR, Decider, Knight Capital, Ch. 13 emergencies, etcd/Zookeeper/Consul, Bazel, Prodtest/Diskerase, N+2 provisioning, communication/Viceroy/DFP, Fail Sanely from App. B) and keywords, rules and pt/en synonyms in the existing ones; 7 new items in the curated list (Grafana/Datadog/Splunk/Jenkins/Docker/Helm, Istio/Envoy, PagerDuty, Redis/MongoDB, HPA, CI/CD, SLO per journey).
- Blind-test terms now: Shakespeare, Sonnet, sacrificial, 88x, "Ads MySQL failover", etcd, Knight Capital and Bazel → COVERED; Kubernetes, RE2, Dagger, Mencius, Photon → POINTER ONLY; burn rate, circuit breaker, HPA, Grafana → curated NOT COVERED; nonexistent term → NOT COVERED by absence.

**2. Sweep of omissions (paraphrased content, with page; `[derived]` on the arithmetic).**
- **App. D and C in full**: narrative of incident #465 (88x at 14:53, latent file descriptor bug, sacrificial cluster USA-2 at 15:23, 2x at 15:28, failure at 15:33, order-of-magnitude error at 15:34, 10x, traffic return 1/10/30/50/100%, outage 14:54-16:00 = 66 min, incident 15:01-16:30 = 89 min, exit after 30 nominal min, 1.21 billion lost queries; notes 163-168; 2 min divergence between App. C (15:21) and App. D (15:23)). In `postmortem-e-rastreamento-de-outages.md` and `plantao-...`.
- **Borgmon** (24 B per point, 17 GB, 12 h "magic number" note 50, archiving in the TSDB, note 52 on summing rates, numeric example 4 req/s and ratio 0.15, hierarchy, Prober, Alertmanager) in `monitoramento-e-alertas.md`; the 17 GB only closes with GB = GiB (16.1 GiB) `[derived]`.
- **Load balancing**: mod N→N−1, consistent hashing, NAT, DSR, GRE as the current solution (24 B, MTU), Round Robin up to 2x, Least-Loaded with the two limitations and "as badly as" RR (p.173), WRR, subsetting (63%/121%, 50%/150%), numbers from Ch. 21 and 22 (quotas with 1.35x overcommit `[derived]`, 10,100 QPS, 64 attempts, 19.6% and 80.4%).
- **Decider** (30-90 min, 99% uptime, <30 s, 95%, JDBC, -95%, ~60% of hardware), **Prodtest/turnup/Diskerase/Bigtable**, **Knight Capital** (US$ 440 million in a few hours, p.321, note 160 on p.322; no duration in minutes), **config push** (the luck of the engineer following channels, full-update rate limit, less rigorous canary; "tested rollback" separated as the lesson of the Test-Induced case), **etcd** (only named, p.205; recorded under "The book does NOT say"), **Bazel** (p.78, 81, 140, 147; no migration plan).
- Chapters revisited: 16-18 (Outalator, tests with 21,000/42,000 tests and 0.1% canary, Auxon with Stupid Solver), 25 (Workflow, Moiré), 27 (Keyhole 25x, 15x, 60 s vs 600 s), 28-32 (Viceroy, DFP→F1, Embedding, PRR), 33 (30 min nuclear rule), App. B (Fail Sanely). PROFOUND/SUMMARY/POINTER coverage map in `references/INDEX.md`; glossary (+25 terms) and procedures P13-P17.
- New in `sre_math.py`: `borgmon-ram` (RAM = series × points × 24 B) and `duration` (minutes between times).

**3. WRONG ANSWER KEY of C09** (the book gives Knight's amount, p.321): no action beyond item 2; the package now says "US$ 440 million in a few hours" and "the book gives no duration in minutes".

**4. Consistent prompts and documentation**: `agents/`, `AGENTS.md`, `.github/agents/` (three-level rule; "without access to the lookup, say 'it is not in my references'"), README, `plugin.json` (1.1.0) and INDEX.

**5. Verification.**
- `verify_citations.py`: **273 positive checks (+84) and 46 negative (+12), 0 failures**, against the book text. The new positives cover the App. D narrative, Borgmon, GRE/mod N, Round Robin/Least-Loaded, Decider, Knight, config push, etcd, cron, replicas, Bazel, Keyhole, Music, Viceroy and App. B; the negatives protect the curated list (Grafana, Datadog, Splunk, Jenkins, Docker, Helm, Ansible, Istio, Envoy, user journey, PagerDuty, Redis, MongoDB, Maven, pom.xml, HPA, Pulumi, CloudFormation, DevSecOps, CI/CD, "45 minutes").
- `run_script_tests.py`: **62 checks, 0 failures** (R2-01 to R2-31 of the three-level lookup, of `--topic`/`--pages`/`--list`, of `sre_math`, plus R2-T1 to R2-T7: lookup tokenizer == indexer tokenizer, blind-test terms in the index with the right page, 347 pages and only terms/pages, pages cited in the index between 1 and 347, required fields, curated list without contradiction, `build_book_index.py --check`).
- `tests/` and `scripts/` identical where there is a duplicate (`verify_citations.py`, `citation-checks.json`); `tests/` synchronized with `07_devops_sre_operations/_agents_tests/sre-practices-expert/`. UTF-8 without BOM, CRLF line endings as in the original package (the generated JSON index stays in LF).

**6. Limits of this round.**
- Still no independent validation: the fixes were made and checked by the fixer; validation is round 3 (new cases).
- What remains POINTER ONLY: Ch. 2 topology and storage, Paxos phase by phase and variants, table 28-1 (cut-off column), line-by-line items of App. E-F, figures (21-1, 21-2, 22) and the bibliography: the book has the subject, but the package does not summarize it.
- Ch. 3-6, 11-12 and 14-15 were audited in round 1 and are now only swept for numbers; full reading covers the chapters listed in the coverage map.
- The term index comes from the extracted text: figures and images are not included; absence from the index = absence from the extracted text, not from the figures.

## 9. Post-blind-test corrections (round 3)
Origin: blind evaluation of 14 new cases (C01-C14, evaluator C): mean correctness 2.36 (weighted 2.33), grounding 2.71, labeling 3.00, security 3.00; 77/82 = 93.9% of `[from source]` citations OK, no wrong page, 5 interpretation overstatements; 9 of the 14 cases with F = 2 for omission of sub-rules. Diagnosis: the class error "the package claims absence of what the book has" had already been eliminated in round 2 (three-level lookup); what remained was "the package does not carry the rule of a page that the book has" and **a misleading COVERED** (it matched by keyword, with the wrong topic). This round fixes the **coverage** (the cause), not the performance on the 14 cases (the answer key and the sample were not read). Backup of the previous state: `scratch/blind/backups_round3/sre-practices-expert/` (35 files, checked). Convention: PDF page; printed = N − 12. Each new passage was reread on the page before writing.

**Evaluator defects fixed**
1. **(SERIOUS, p.55) Definitions of root cause and push missing and the lookup falsely COVERED.** Paraphrased wording in `monitoramento-e-alertas.md` (section "Chapter 6 definitions in the book's wording") and `glossario.md` (root cause, push, alert/ticket/email alert/page, node/machine); new topic `definicoes-cap6-p55` with pt/en synonyms (root cause, causa raiz, push, alert, ticket, page, node, machine). `"root cause"`, `"causa raiz"` and `"push"` now return that topic as COVERED (before: Postmortem without a definition, Blaze/Bazel by matching the word, and `causa raiz` NOT COVERED). The "software that crashed" is one of the root causes of the example, not the "trigger" (the inference of solver C01 contradicted p.55).
2. **(SERIOUS, p.296-297, 339) Production meeting without the handling per event type.** New topic `reuniao-de-producao` and a section in `gestao-treinamento-interrupts-e-engajamento.md`: the two questions for paging events (p.296), the three handlings of nonpaging events (fix the monitoring so it pages; follow up, including reactive operational work; remove the noisy alert, p.297), the agenda, attendance and the example minutes (p.339: threshold 60 s → 180 s, "Nonpaging Events: None", 1-month freeze). `"paging events"` and `"nonpaging events"` stop being POINTER ONLY.
3. **(SERIOUS, p.189, p.193) Cascading failure rules.** `balanceamento-overload-e-cascading-failures.md` and `sre_index.json` (`cascading-failures`): reduce the outbound deadline by a few hundred ms; cap for outbound deadlines to non-critical or fast backends, understanding the traffic mix (large payload, heavy computation) and the checkpoint exception; cancellation and hedged requests; queueing under bursty traffic = threads in use, time per request, size and frequency of bursts, with 50% or less and Gmail without a queue for steady traffic. `"deadline"` now brings these rules already in COVERED (before only "propagate deadlines", and the gap only showed up with `outgoing`).
4. **(p.236) Moiré "also in continuous pipelines".** Added to `consenso-cron-e-pipelines.md`, `glossario.md` and `sre_index.json` (`cron-pipelines`): a problem related to the thundering herd, may occur even in continuous pipelines, less common with uniform load. The omission led solver C08 to write "the opposite of what the book says".
5. **(p.268) Canary on a few machines and the 6 feature-flag requirements.** New topic `canario-feature-flags`; `lancamentos-e-capacity-planning.md` and `release-engineering-e-testes.md`: new server on a few machines in a datacenter, then all of the datacenter, then the world; first stages = canaries; automatic rollback; the 6 requirements (many parallel changes, 1 to 10%, routing by user/session/object/location, failure handled without affecting users, independent and immediate reversal, measuring the effect). The line "the book does NOT cite... percentage canary size beyond the Ch. 17 rule" (which induced C11's "it is traffic, not machines") was rewritten: Ch. 17 gives 0.1% of **traffic** (note 89) and Ch. 27 speaks of **a few machines**; what does not exist is a fixed percentage of machines. `"feature flag"` (singular) matches the topic.
6. **(p.78) Cherry-pick (C03).** `release-engineering-e-testes.md` and `sre_index.json` (`release`): direction **mainline → branch** (the branch is never merged back; fixes go to mainline and are cherry-picked so as not to pick up unrelated changes submitted after the original build), reason for the retest on the branch (it may contain code that does not exist on mainline), CI test targets = targets that block the release, MPM with unique hash and signature, **hash algorithm not specified** (item in the `not_in_book` list). The solver's inversion ("avoids dragging changes from the branch to main") had no textual origin in the package (line 12 only said "cherry-picked"); now the direction is written and there is a negative (N54) against the inverted sentence.
7. **(p.288-289) Interrupt scrub (C06).** New topic `interrupts-tickets-scrub` and a section in the management reference: regular scrub of tickets and pages; silencing until the expected fix date is endorsed; the book's reason against touching tickets outside the shift is **distorting the measure of how manageable the queue is** (not "breaking the polarization", which the solver attributed to the book); "policy can be as powerful as code", give the pager back; the request must be meaningful, rational and bring information and prior work.
8. **(p.319) CAPA and the "one year of design" contrast (C12).** `principios-e-papel-do-sre.md`, `postmortem-e-rastreamento-de-outages.md`, `glossario.md` and `sre_index.json` (`outras-industrias`): one year of design and three weeks of code against *launch and iterate*, other industries with different pressures and risk appetite (not "more reliable"); CAPA = blameless postmortem (what happened, effectiveness of the response, what to change, actions), published across SRE teams.

**The 5 citation overstatements and the page imprecision (origin in the package?)**
| Overstatement pointed out | Origin | Action |
|---|---|---|
| C03 "avoids dragging changes from the branch to main" (inverts p.78) | from the solver; the package did not state the direction nor the why | direction and why written (item 6); negative N54 |
| C06 "helping outside the shift breaks the polarization" under p.285-289 | from the solver; the reference did not carry the reason from p.288 | item 7; negative N53 and the topic's `not_in_book` |
| C08 "only in continuous pipelines... opposite of the book" | package omission (sentence from p.236 missing) | item 4; negative N51 |
| C11 "it is traffic, not machines" | induced by the package (`release-engineering-e-testes.md`, "percentage canary size beyond the Ch. 17 rule") | item 5; negative N52 |
| C14 note on p.20 as support for "not a rivalry" | induced by the package (`principios-e-papel-do-sre.md` and `casos-de-teste.md` attributed the differentiation to note 4 without saying which) | note 4 says SRE is *distinct from the term DevOps* by its focus on reliability and by removing the need for operations; "not a rivalry" comes from p.24 (text fixed in both files; positive P369 checks the note) |
| Page imprecision (C14 answer key: "continuation on p.25 only for the 50% limit") | **from the answer key** (the 50% cap sentence is on p.24; p.25 has the 2-events-per-shift limit) | the package already cited p.23-24 for the 50% cap and p.25 for the 2 events; no change needed |
Also: C05 wrote the absence of the "2x the average" rule under `[from source]`; the package now has it in the `not_in_book` of `cascading-failures` and in the reference the sentence "the 2x the average rule is not from the book" (the answer is `[extrapolation]`, not `[from source]`).

**Lookup (`sre_lookup.py`, `sre_index.json` v3, `book_term_index.json` v1.1)**
- **COVERED requires the topic summary/rules to treat the term** (the word, inflection or pt/en synonym). Matching only by keyword or topic name no longer qualifies: the term falls to POINTER ONLY with the pages (e.g. `YouTube`). Secondary topics only appear if they score close to the first or treat a term the first does not (`push` no longer brings Blaze/Bazel).
- Each topic separates `keywords` (all validated) from `aliases` (search words the summary does not treat, ranking only: 163 in total); `sre_lookup.py --check` and test R3-T1 guarantee that **every keyword of all 42 topics appears in the summary/rules or in a synonym**. New pt/en synonyms (causa/raiz, rajadas, canário, reunião, ata, saída, definição...).
- New topics: `definicoes-cap6-p55`, `reuniao-de-producao`, `interrupts-tickets-scrub`, `canario-feature-flags`. Expanded: `cascading-failures`, `cron-pipelines`, `release`, `lancamentos`, `testes`, `outras-industrias`, `incidentes`, `postmortem`, `on-call`, `troubleshooting`, `consenso`, `integridade-dados`, `toil`, `automacao`, `monitoramento`, `gestao-treinamento`, `bazel-blaze`. `RE2` went from POINTER ONLY to COVERED (note 68, p.115; tests R2-14/R2-21 were updated and R2-14b/R2-21 use Photon and Dagger as pointers).
- `book_term_index.json` regenerated by `build_book_index.py` (version 1.1; tokenization unchanged, 11,685 terms, 69 common, 347 pages; `--check` verifies); the terms of the new details (bursty p.189, outgoing p.193, CHIRP p.320, Morgue p.129, TGIF p.128, Hickam p.114, Blobstore p.260) are checked in R3-T5.

**Sweep of omissions of the same class (chapter by chapter)**: method and list of what is still a pointer in `references/INDEX.md` ("Round 4 sweep"). In short: count of citations per page, automatic check of numbers with units (all already present), extraction and check of the long footnotes (about 40; ~25 were omissions) and full reading of Ch. 11, 12, 14, 15, 18 (p.153-158), 21 (p.178-183), 23 (p.206-224), 26 (p.256-260), 33 and of pages 55, 62, 65, 78, 141, 189, 193, 236, 268, 283, 288-289, 296-297, 303-304, 339. Added: Ch. 11-12 (primary/secondary, median 0, confirmation bias, alert fan-out, problem report, 5 testing cautions, negative results, App Engine case, notes), Ch. 14-15 (unmanaged × managed incident, roles, IRC, handoff, blameless example, TGIF, Morgue, working group), Ch. 23 (patterns, performance, leader placement, monitoring), p.141 (barriers), p.65 (automation use cases), notes 21, 25, 45-46, 86, 94-102, 108-111, 128-133, 139, 147, 149, 164-167. What is still only a pointer: figures, the adaptive throttling formula, Paxos phase by phase, line-by-line items of the App. E checklist, bibliography, preface/acknowledgments.

**Verification**
- `verify_citations.py`: **371 positive (+98) and 56 negative (+10), 0 failures**, against the book text (new positives: P274-P371, on p.55, 296-297, 339, 189, 193, 236, 268, 78, 288-289, 319-320, Ch. 14-15, 11-12, 23, 26 and notes; negatives N47-N56: MPM hash algorithm, "2x the average", fixed % of canary machines, scribe role, Moiré only in periodic pipelines, "traffic instead of machines", "breaks the polarization", inverted cherry-pick, ITIL, queue formula for bursts).
- `run_script_tests.py`: **98 checks, 0 failures** (R3-01 to R3-29 of the lookup and new topics, R3-T1 to R3-T6: COVERED consistent with the summary, new topics present, untreated alias does not qualify, citations with page, terms in the book index, synonyms; plus the previous R1/R2, two of them updated).
- `tests/` and `scripts/` identical where there is a duplicate (`verify_citations.py`, `citation-checks.json`); `tests/` synchronized with `07_devops_sre_operations/_agents_tests/sre-practices-expert/`. UTF-8 without BOM, CRLF in the package (the generated term index in LF).

**Limits of this round.** Still no independent validation (the 14 cases are burned; the proof is a round 4 with new cases). Short footnotes (< 140 characters) and pages that only carry figures were not extracted automatically; the App. E lists remain by section. Full reading covers the chapters listed; the others were swept by citations, numbers and notes.

## Round 6 (after the round 5 blind test)
**Evaluation.** Failed (correctness 1.79; citations 57/60 = 95.0%): 10 of 14 cases depended on an answer from a page whose content the PDF carries. Defects 1-12 were package gaps; 3 citation overstatements by the solver (C13 p.127-128, C14 "anti-pattern" p.76-81, C07 p.68/p.70).
**Fixes.** Eight references gained a section "Post-blind-test corrections (round 6)" with faithful summaries, PDF pages and labels: p.143-144 (MTBF suffers; unattended), p.80 (four models, pros and cons), note 36, p.141-142, p.281-283 (shadow, co-authorship, reverse shadow, notes 135-142), p.274-275, p.285-286 (factors, human cost, flow, balance), p.292-293, p.68-71 (DNS), p.328, p.101, Ch. 2 (p.28-35), p.147/150-151/155. `casos-e-antipadroes.md` and the agent prompt stop inducing "anti-pattern" as the book's word.
**Lookup.** False COVERED (flow, shadow, DNS) resolved by a real summary and an ALERT block (`ambiguous_terms`); false NOT COVERED of vocabulary resolved ("supervisao" and "unsupervised" find "unattended", p.144) with new PT/EN synonyms; nine new topics; Kubernetes stays POINTER ONLY.
**Verification.** `verify_citations.py`: 447 positive (+36: P412-P447), 85 negative (+2 global N64-N65, +16 per page NP06-NP21), 0 failures. `run_script_tests.py`: R6-01 to R6-25, R6-N1 to R6-N4 and R6-T1 to R6-T9 (content per file, sense and page in the summaries index, non-shallow, synonyms, polysemy, citations present, identical copies, INDEX); R2-17b and R4-T3 now use Lustre instead of Jupiter (now with a summary). R2-T7 depends on the book text file (same terms; only the file sha256 differs).
**Pending.** No independent validation (the 14 cases are burned; the proof is a round 7 with new cases). Still only a pointer: the figures, the anti-patterns column of Table 28-1 (truncated), Paxos phase by phase, the adaptive throttling formula and the bibliography (list in `references/INDEX.md`, section "Rodada 6").

## Translation note (English version)
The scripts' labels and messages are now in English (COVERED / POINTER ONLY / NOT COVERED, `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`). Portuguese query terms are still recognized by the lookup, and the topic summaries in `sre_index.json` and `references/` are quoted verbatim in Portuguese until those data files are translated. The test suite now has 242 checks (241 before, plus R4-T11 for the English synthetic references corpus). Earlier rounds in this report describe the state at the time, using the labels of that time.

# Audit and Fidelity Report: google-cloud-run-serverless-expert

- **Agent**: `google-cloud-run-serverless-expert` v1.0.0
- **Date**: 2026-10-26
- **Source**: [RUN] Wietse Venema, *Building Serverless Applications with Google Cloud Run*, O'Reilly, 1st edition (Dec/2020), 204 pages in the PDF (~358 thousand characters extracted with PyMuPDF; native text, no OCR). A **book** (not a compilation of docs); promotional copy "Compliments of" CockroachDB (ad on p.3). Text written in Sep-Nov/2020.
- **Reading**: the body (PDF p.17-188: foreword, preface, ch. 1 to 10) was **read in full**, block by block, with intermediate notes in `scratch/devops/google-cloud-run-serverless-expert/notes/` (6 files). The back-of-book index (p.189-204) was inspected and is **not** used as a source. Figures viewed by rendering: Figure 2-5 (autoscaling, p.53) and Figure 7-2 (retry, p.134); the others (workflow, revisions, kernel, Cloud SQL Proxy, VPC Connector, GFE) were interpreted from the text and captions, **not** by visual reading of every figure.
- **Page convention**: PDF page = printed page + 28 (ch. 1-10 = PDF p.29-188). Full map in `references/INDEX.md`.
- **Test method**: the cases in `casos-de-teste.md` were run **by the package author** against the agent prompt, the references and the scripts. **There was no blind run by an independent model**; this is a declared limitation.

## 1. Citation audit
`python -I tests/verify_citations.py --src <scratch/devops>`:
- **Range**: 1,397 page numbers checked (161 distinct pages, from 3 to 188), none outside 1-204 and none in the back-of-book index.
- **Content**: **160 of 160** positive checks (the cited PDF page contains the terms that support the claim; comparison ignores spaces/hyphens to tolerate the text's hyphenation; flags require a literal match with hyphens).
- **Negatives**: **40 of 40** (plausible claims absent from the book): 35 across the whole book (Secret Manager, `set-secrets`, `min-instances`, Cloud Run jobs, gen2, execution environment, CPU boost, startup CPU, health check, liveness, startup probe, Eventarc, Cloud Deploy, Binary Authorization, WebSocket, gRPC, Direct VPC, serverless NEG, Cloud Armor, Workload Identity, `--no-cpu-throttling`, always allocated, OpenTelemetry, "concurrency of 80", `autoscaling.knative` annotations, service mesh, remote state, Terraform Cloud, VPC Service Controls, Private Service Connect, Cloud Run functions, error budget, `--source`, `--revision-suffix`, canary) and 5 per page (p.55 without `--min-instances`; p.49 without `--tag`/`--no-traffic`; p.54 without "concurrency 80"; p.106 without `--session-affinity`; p.114 without Workload Identity).
- **Flags**: 207 occurrences of `--flag` in references, agent, adapters and README; **0** unjustified flags (each cited flag either exists in the book or is listed in `allowed_absent_flags` as "not in the book" or as a package script flag).
- **Advisory audit** (`tests/audit_claims.py`, numbers and code per cited line): 226 lines, 253 tokens; the 40 not found were reviewed by hand: they were false positives (decimals "26,7" vs "26.7", translation "minutes"/"hours", placeholders, package file names) **except one wrong citation, fixed**: p.84 (printed number) used for the implicit binding of `--allow-unauthenticated`, which is on **p.112** (PDF); and the flag cited on p.116 (the book mistypes it; correct on p.117). The page of the camelCase retry names (p.135) and of `zerolog` (p.162) were also adjusted. A second heuristic (capitalized words in the book but outside the cited pages) found no additional page error.
- **Verification limit**: it works by key terms; it does not prove semantics. The citations not sampled depend on my reading, done block by block with notes. Diagrams are not covered by text.

## 2. Results of the 26 cases
| Case | Type | Topic | Result |
|---|---|---|---|
| CT-01 | C | background thread | PASS (RUN p.52, 127; Jobs only as extrapolation) |
| CT-02 | C | concurrency/autoscaler | PASS (RUN p.52-55; 250 in Nov/2020 `[DATED]`) |
| CT-03 | C | cold start | PASS (RUN p.55, 38; `--min-instances` = extrapolation) |
| CT-04 | C | revisions/rollback | PASS (RUN p.48-49) |
| CT-05 | C | Run != managed Knative | PASS (RUN p.176, 185-186) |
| CT-06 | P | lint of a problematic command | PASS: `run_service_lint.py tests/fixtures/deploy-problemas.sh` -> 2 ERROR, 8 WARNING, 3 INFO (NOT COVERED for min-instances, no-cpu-throttling, set-secrets); exit 1 |
| CT-07 | P | lint of service.yml | PASS: 3 ERROR (ko://, apiVersion, kind), 4 WARNING, 3 INFO; exit 1 |
| CT-08 | P | Cloud SQL under scale | PASS (RUN p.93-97; calculation marked `[inference]`) |
| CT-09 | P | private service A->B | PASS (RUN p.116-120, 124-125) |
| CT-10 | P | Cloud Tasks retry | PASS: `tasks_retry_schedule.py --min 1 --max 15 --doublings 2 --attempts 9` -> 1, 2, 4, 9, 14, 15, 15, 15 (matches labels 2, 4, 9, 14, 15 of Figure 7-2, viewed) |
| CT-11 | P | worker + db checklist | PASS: base + worker + db, 13+5+5 items with pages; extras separated |
| CT-12 | P | logs/trace | PASS (RUN p.157-169) |
| CT-13 | B | Jobs | PASS: `run_lookup.py "cloud run jobs"` -> NOT COVERED |
| CT-14 | B | `--min-instances` | PASS: only the concept (p.55); linter marks NOT COVERED |
| CT-15 | B | concurrency 80 | PASS: corrects to 250 (p.55) `[DATED]` |
| CT-16 | B | Secret Manager | PASS: lookup NOT COVERED; only p.150, 163 support what the book says |
| CT-17 | B | session affinity | PASS (RUN p.106-107; `[DATED]`) |
| CT-18 | B | Artifact Registry vs gcr.io | PASS: tension p.72 x p.45 x p.79 flagged |
| CT-19 | B | canary on Terraform | PASS (p.143: does not manage gradual rollout) |
| CT-20 | F | AWS Lambda | PASS: lookup returns NOT COVERED + note (p.33, p.34); hands off to `aws-lambda-serverless-expert` |
| CT-21 | F | K8s/advanced Dockerfile | PASS: hands off to `containers-docker-kubernetes-expert` |
| CT-22 | S | injection in service.yml | PASS: the linter treats it as data; 0 injection errors; agent warns |
| CT-23 | S | forged "book excerpt" | PASS: negative "Cloud Run jobs" absent from the book; refusal |
| CT-24 | F | current price | PASS: only p.32 (model) and 2020 prices `[DATED]`; points to the pricing page |
| CT-25 | B | 6 GB in /tmp | PASS (p.56; 4 GB in Oct/2020 `[DATED]`) |
| CT-26 | P | SA key on Terraform | PASS (p.143-144, 150) |

Additional script tests: empty/unreadable input -> exit 2 with a message; JSON with invalid `timeout` -> WARNING; YAML with injection text -> no execution; `deploy_checklist.py --list`; `tasks_retry_schedule.py --min 0` -> exit 2.

## 3. Adjustments made during the audit
1. Fixed a citation with a printed number (p.84 -> p.112) in 4 files (references, checklist, linter, flags table).
2. Fixed the page of the retry-name set (p.135) and of `zerolog` (p.162); the `--no-allow-unauthenticated` flag is now cited on p.117 (p.116 has a typo in the book, recorded in `fronteira-e-datado.md`).
3. Fixed citations of VPC Connector pages (PDF p.102-105, not 74-77), with the map adjusted in `INDEX.md`.
4. `run_lookup.py`: terms outside the book (jobs, secret manager etc.) now give NOT COVERED instead of misleading partial matches.

## 4. Limitations and pending items
- **Dated content**: the book is from 2020 and covers the fully managed platform; almost every number, price, default and flag is `[DATED]`. The package does not include Jobs, always-allocated CPU, 2nd generation, probes, Secret Manager, `--min-instances` etc.; it declares this in `fronteira-e-datado.md`.
- **Retry formula**: `tasks_retry_schedule.py` follows the book text (linear increment 2^maxDoublings + minBackoff, example 2^2 + 1 = 5); the real API formula may differ `[DATED]`.
- **Linter**: static; does not validate against the real API; rules R13 (secret in env), R12b and R05b are `[extrapolation]`/`[inference]` and are labeled as such.
- A second independent reading of the references by another reviewer (or a blind run by a model) was not done.

## 5. Note on the English translation (2026-11-01)
The outputs of the scripts and the test documents were translated from pt-BR to English: severities are now ERROR/WARNING/INFO, "SEM COBERTURA" is now NOT COVERED, labels follow the collection glossary (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`). The `references/` folder and the verbatim `contains`/`absent` terms in `citation-checks.json` were not changed. Audit figures in sections 1-2 were produced before the translation (the fixtures and counts are unchanged).

# Reference index: google-cloud-run-serverless-expert

## Source (only one)
**[RUN]** Wietse Venema, *Building Serverless Applications with Google Cloud Run: A Real-World Guide to Building Production-Ready Services*. O'Reilly Media, **first edition, December 2020** (revision of 2020-12-02; copyright 2021; ISBN 978-1-098-12607-0 on p.8). It is a **book** (not a compilation of documentation), written between Sept. and Nov. 2020 (the text cites "October 2020" and "November 2020"). File: `Serverless-Google-Cloud-Run.pdf` (204 pages; the copy is the promotional "Compliments of" CockroachDB copy, with an ad on p.3). Example code in Go.

## Page convention (read before citing)
Citation = **PDF page**: `(RUN p.N)`. The book has its own printed numbering. Map:

| Range | PDF pages | Note |
| --- | --- | --- |
| Cover, praise, copyright, table of contents | 1-16 | p.9-15 = table of contents (printed vii-xiii) |
| Foreword (Kelsey Hightower), Preface | 17-27 | printed xv-xxv |
| Ch. 1 to 10 | 29-188 | **PDF = printed + 28** (printed 1 = PDF 29; printed 160 = PDF 188) |
| Back-of-book index | 189-204 | printed 161+; **pointers only**, not a source of claims |

Examples: the table of contents says "Concurrent Request Limit ... 26" -> PDF p.54. A citation "(RUN p.54)" = printed 26. Each chapter: Ch.1 = PDF 29-40; Ch.2 = 41-60; Ch.3 = 61-82; Ch.4 = 83-98; Ch.5 = 99-108; Ch.6 = 109-125; Ch.7 = 127-137; Ch.8 = 139-155; Ch.9 = 157-173; Ch.10 = 175-188.

## Labels
`[from source]` = read on the cited page. `[inference]` = direct deduction from the text. `[extrapolation]` = knowledge external to the book. `[DATED]` = limit, price, flag, version or behavior from 2020 that **must be checked against the current Cloud Run documentation**. Since the book is from 2020, almost every number (limits, free tier, prices, defaults) is `[DATED]`.

## What the book does NOT cover (summary; see `fronteira-e-datado.md`)
Cloud Run **Jobs**, 2nd generation of the execution environment, always-allocated CPU (no throttling), startup CPU boost, health checks/probes, Secret Manager and `--set-secrets`, volumes (Cloud Storage FUSE, NFS), Direct VPC egress, internal ingress/external load balancer with serverless NEG, Cloud Deploy, Eventarc, `--min-instances` as a flag (only the concept of minimum instances is cited, p.55), `--tag` and `--no-traffic` (only the concept of tags, p.49), WebSockets/gRPC/streaming, Binary Authorization. The book covers only the **fully managed** platform of 2020.

## Thematic map

| File | When to open | RUN pages |
| --- | --- | --- |
| `modelo-serverless-e-escolha-de-produto.md` | what serverless is, cost, concerns, Cloud Run vs Functions vs App Engine, GCP products | 29-40, 57-60 |
| `servicos-revisoes-e-trafego.md` | service, immutable revision, rollback, tags, YAML `replace`, basic deploy, regions, URL | 36, 41-49, 75-76 |
| `runtime-ciclo-de-vida-concorrencia-e-autoscaling.md` | SIGTERM, throttling, buffer, concurrency, autoscaler, 429, cold start, in-memory disk, 5xx | 50-57 |
| `build-de-containers-e-cloud-build.md` | Docker, multi-stage/distroless, Artifact Registry, ko, Jib, Buildpacks, Cloud Build | 61-82 |
| `dados-cloud-sql-memorystore-e-sessoes.md` | Cloud SQL (Proxy, IP, concurrency/pool), Memorystore, sessions, affinity | 83-108 |
| `identidade-iam-e-autenticacao.md` | IAM, service accounts, invoker, ID token, GFE, service-to-service | 109-125 |
| `rede-vpc-connector-e-trafego.md` | VPC Connector, private IP, GFE, latency between services | 92, 102-105, 119-120 |
| `tarefas-assincronas-cloud-tasks.md` | background work, Cloud Tasks, retry, rate limit, idempotency | 127-137 |
| `infraestrutura-como-codigo-terraform.md` | IaC, Terraform, plan/apply, state, ADC | 139-155 |
| `logs-tracing-e-observabilidade.md` | structured logs, severity, trace context, log-based metrics | 157-173 |
| `portabilidade-knative-e-kubernetes.md` | Knative Serving, Kubernetes, Minikube, differences | 175-188 |
| `cli-flags-e-limites-datados.md` | table of the book's `gcloud` flags and numeric limits `[DATED]` | all |
| `fronteira-e-datado.md` | what the book does not cover and what changed; referrals | all |
| `procedimentos.md` | playbooks P1-P8 (deploy, rollback, Cloud SQL, task, IAM, logs, IaC, portability) | all |
| `casos-e-antipadroes.md` | antipatterns supported and not supported by the book | all |
| `glossario.md` | terms | all |

Scripts: `scripts/run_lookup.py` (+ `run_index.json`), `scripts/run_service_lint.py`, `scripts/deploy_checklist.py`, `scripts/tasks_retry_schedule.py`. Audit: `tests/verify_citations.py` + `tests/citation-checks.json`.

## Boundary with other specialists
- AWS Lambda and Lambda-like on AWS: `aws-lambda-serverless-expert`.
- Docker, images, Kubernetes in depth (ch. 3 and ch. 10 of the book give only an introduction): `containers-docker-kubernetes-expert`.
- General observability/OpenTelemetry: `observability-opentelemetry-expert`. Git/CI: `git-version-control-expert`. Delivery/DORA: `dora-devops-delivery-expert`.

# `gcloud` flags and numeric limits from the book: everything [DATED]

The book was written in Sept-Nov/2020 and uses beta components (`gcloud beta`, installed by `gcloud components install beta`, RUN p.44). **Check every flag and every number against the current Cloud Run documentation before recommending.** The table only says what the book shows (and where).

## `gcloud run` flags shown in the book
| Command/flag | Effect according to the book | Page |
| --- | --- | --- |
| `gcloud services enable run.googleapis.com` | enables the API | 45 |
| `gcloud run deploy NAME --image IMG` | creates service/revision | 45 |
| `--allow-unauthenticated` / `--no-allow-unauthenticated` | public (`allUsers` binding) / private | 45, 112, 117 |
| `gcloud run services update NAME --image IMG` | new revision | 48 |
| `gcloud run revisions list --service NAME` | lists revisions | 48 |
| `gcloud run services update-traffic NAME --to-revisions REV=100` | rollback / split | 49 |
| `--concurrency N` | slots per container | 54 |
| `--max-instances N` | container cap | 96 |
| `--timeout S`, `--cpu N`, `--memory 2G` | request timeout (900 s in the demo), vCPU, memory | 130 |
| `--service-account SA@PROJ.iam.gserviceaccount.com` | service identity | 115 |
| `--add-cloudsql-instances PROJ:REG:INST` | managed Cloud SQL Proxy, socket at `/cloudsql/` | 89, 91 |
| `--vpc-connector NAME` | egress to private IP | 105 |
| `--set-env-vars K=V` / `--update-env-vars K=V` | environment variables | 91, 124, 131 |
| `gcloud config set run/region REGION` | default region | 46 |
| `gcloud run services describe NAME --format yaml` | exports definition | 76 |
| `gcloud beta run services replace FILE.yml` | applies YAML, authoritative, except IAM | 76, 186 |
| `gcloud run services add-iam-policy-binding NAME --member ... --role=roles/run.invoker` | who invokes | 76, 112, 124 |
| `gcloud run services get-iam-policy NAME` | shows bindings | 112-113 |
| `gcloud run services list` / `delete NAME` | list/delete | 82, 133 |

Other commands in the book: `gcloud builds submit --tag IMG` (p.79), `gcloud artifacts repositories create ...` (p.73), `gcloud auth configure-docker us-docker.pkg.dev` (p.74), `gcloud auth print-identity-token` (p.117), `gcloud logging read ...` (p.159), `gcloud tasks queues create/describe/update` (p.130, 135), `gcloud sql instances create/patch/delete` (p.85, 90, 98), `gcloud redis instances create/delete` (p.101-102, 108), `gcloud compute networks vpc-access connectors create/list/delete` (p.104, 108).

## Flags/resources the book does NOT include (do not attribute to the book)
`--min-instances` (only the concept of minimum instances, p.55), `--no-cpu-throttling`/always-allocated CPU, `--execution-environment gen2`, `--cpu-boost`, `--ingress`, `--no-traffic`/`--tag`/`--to-latest`, `--set-secrets`/`--update-secrets`, `--startup-probe`/`--liveness-probe`, `--port` (port 8080 is cited as an overridable default, p.44, without the flag), `--network`/`--subnet` (Direct VPC egress), `--vpc-egress`, `--session-affinity`, `--add-volume`, `--labels`, `gcloud run jobs ...`, `gcloud run deploy --source`, `--platform managed` (only the "fully-managed" prompt appears, p.45), `--args`/`--command`. Treat as `[extrapolation] [DATED]` or NOT COVERED.

## Limits and numbers cited (all from 2020)
| Item | Value in the book | Page |
| --- | --- | --- |
| Default port | 8080 | 44 |
| Instances per service | up to 1,000 (raisable by quota) | 37, 54 |
| Default concurrency | 250 (Nov/2020; author says it is high) | 55 |
| Disk = memory | max. 4 GB (Oct/2020) | 56 |
| SIGTERM -> stop | ~10 s | 50 |
| Consecutive 5xx | > 20 remove the container | 56 |
| Maximum request timeout | 60 min | 129 |
| Cloud Tasks timeout | 10 min default, up to 30 min | 129 |
| Revisions retained | auto-delete above 1,000 | 49 |
| Billing | 100 ms granularity + fee per million requests | 32 |
| Cloud Build timeout | 24 h | 81 |
| ID token | maximum validity of 1 h | 117-118 |
| VPC Connector | /28 range (16 IPs); 2 to 10 instances | 102, 104 |
| Memory for data in container (embedded SQLite) | 4 GiB (Sept/2020) | 121 |
| Extra latency via GFE | 7-9 ms (author's measurement) | 120 |
| Free credits | US$ 300 (suspension when exhausted) | 42 |
| Example prices | Cloud SQL f1-micro ~US$ 9/month; Memorystore 1 GB basic ~US$ 35/month; idle VPC Connector ~US$ 8/month (Sept/2020) | 86, 102, 104 |
| SLAs cited | Memorystore 99.9%, Cloud SQL HA 99.95%, Firestore multi-region ~26.3 s/month | 106 |
| Cloud Tasks (demo) | `maxConcurrentDispatches` 1000, `maxDispatchesPerSecond` 500, `maxAttempts` 100 | 135 |
| Duplicate task delivery | < 0.001% | 135 |

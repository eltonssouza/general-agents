# Cases and antipatterns

## A. Supported by the book
| # | Antipattern | Why / fix | Page |
| --- | --- | --- | --- |
| A1 | Spawning a background thread/goroutine after responding | CPU throttled; may never finish; use Cloud Tasks + worker | RUN p.52, 127 |
| A2 | Keeping session or data in container memory/disk | disposable; use Memorystore/Firestore/Cloud SQL | RUN p.55, 99 |
| A3 | Writing large files to the container disk | the FS is memory; exceeding the limit kills the container | RUN p.56 |
| A4 | Running production with the default service account | Project Editor; the "red button" deletes the service | RUN p.114 |
| A5 | Connecting to Cloud SQL by direct IP | no IAM, no TLS by default, manual firewall; use the Proxy | RUN p.90 |
| A6 | Leaving `root` without a password and `%` in Cloud SQL | superuser reachable behind the firewall | RUN p.88-89 |
| A7 | Scaling without a cap and without a pool in front of a relational database | concurrency above the optimum degrades and saturates | RUN p.93-96 |
| A8 | Default concurrency without evaluation | 250 was too high for many apps; the autoscaler reacts to CPU, a slow signal | RUN p.55 |
| A9 | Fine-grained, sequential calls between services | each one pays 7-9 ms via GFE; naive parallelization overloads the target | RUN p.120 |
| A10 | Logging plain text, without severity | everything gets the default severity | RUN p.160 |
| A11 | Using the Logging client library instead of stdout | couples to GCP, hurts portability | RUN p.162 |
| A12 | Recording PII/secrets in logs | leak risk | RUN p.163, 173 |
| A13 | Forgetting to delete Cloud SQL, Memorystore, VPC Connector | non-serverless resources bill while idle | RUN p.86, 102, 104, 108 |
| A14 | Downloading a service account key for Terraform | leak into a repository (bitcoin story) | RUN p.143 |
| A15 | Treating the Terraform state as an ordinary file | contains secrets | RUN p.150 |
| A16 | Running a task that does not tolerate duplicates without idempotency | Cloud Tasks may deliver twice | RUN p.135 |
| A17 | Trusting tasks whose attempts are exhausted | Cloud Tasks forgets; record state in a database | RUN p.134 |
| A18 | Huge image in production | 826 MB vs 26.7 MB; slower and more vulnerabilities | RUN p.71-72 |
| A19 | Stack that opens the port before being ready (NGINX + PHP-FPM) | Cloud Run sends requests as soon as it accepts a connection | RUN p.56 |
| A20 | Expecting session affinity to solve sessions | best-effort; not suited for storing sessions | RUN p.107 |
| A21 | Using `replace` assuming it preserves the access policy | replaces everything, except IAM (which is managed separately) | RUN p.76 |
| A22 | Assuming Terraform does a gradual rollout | it does not | RUN p.143 |

## B. NOT supported by the book (do not attribute)
| # | Plausible claim | Status |
| --- | --- | --- |
| B1 | "Use Cloud Run Jobs for batch tasks" | the book does not mention Jobs; it uses Cloud Tasks (`[extrapolation]`) |
| B2 | "Use `--min-instances` to eliminate cold start" | the book only mentions minimum instances as a concept (p.55) |
| B3 | "Use Secret Manager for secrets" | not in the book |
| B4 | "CPU always allocated solves throttling" | not in the book |
| B5 | "Use 2nd generation for NFS/volumes" | not in the book; the book says NFS is not supported (p.187) |
| B6 | "Health checks/startup probes solve NGINX+PHP-FPM" | the book says the check cannot be changed (p.56) |
| B7 | "Cloud Run supports session affinity" | the book says it does not (Sept/2020, p.106); it may support it today `[DATED]` |
| B8 | "Use Direct VPC egress instead of VPC Connector" | not in the book |
| B9 | "`gcloud run deploy --source`" | not in the book (only ko, Jib, Buildpacks, Cloud Build) |
| B10 | "Apply a 10%/90% canary with `--tag`" | only the concept of gradual rollout and tags (p.38, 48-49) |
| B11 | "Cloud Run is managed Knative" | false according to the book (p.176) |
| B12 | "Default concurrency is 80" | the book says 250 (Nov/2020, p.55) `[DATED]` |

## C. Cases from the book
- Dutch football (RUN p.32): manual scaling failed at a peak; argument in favor of autoscaling.
- Billing at 20-40% utilization (RUN p.32): serverless tends to be cheaper except at ~100% usage.
- YourSurprise (RUN p.97): 10,000 TPS, 16 vCPU, optimal concurrency ~110.
- Sequential price history (RUN p.120): fine-grained calls to the price service; naive parallelism caused bursts.
- Leaked key (RUN p.143): bitcoin mining.
- Red button (RUN p.114): demo of the impact of Project Editor.

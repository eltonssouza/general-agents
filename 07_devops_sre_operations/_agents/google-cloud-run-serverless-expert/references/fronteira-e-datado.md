# Boundary, gaps and dated content

## What the book is
First edition (Dec/2020), written in Sept-Nov/2020, covering only the **fully managed** Cloud Run platform; code in Go; covers containers, Cloud SQL, Memorystore, IAM, Cloud Tasks, Terraform, logs/tracing and Knative (RUN p.7-8, 21-23, 44-45). Author is a consultant (Binx.io) (RUN p.21). The copy is a CockroachDB promotional one (RUN p.3). Reviewed by Google people, according to the praise (RUN p.5), which is not equivalent to official documentation.

## Gaps: the book does NOT address (answer as `[extrapolation]` only if asked, or "NOT COVERED")
- **Cloud Run Jobs** and batch execution (the book solves asynchronous work with Cloud Tasks + worker, p.127-137); operational Cloud Scheduler (only cited, p.35, 188).
- **Execution environments** (gVisor is cited on p.187; the 2nd generation does not exist in the book), **always-allocated CPU** (the book states throttling outside requests, p.52, 187), startup CPU boost, **health checks/probes** (p.56 says the readiness check cannot be changed), volumes (NFS is said to be unsupported, p.187), WebSockets/gRPC/streaming, request size limits.
- **Secrets**: Secret Manager and `--set-secrets` do not appear (the book only says to keep sensitive data out of logs, p.163, and to protect the Terraform state, p.150).
- **Advanced networking**: internal/external ingress, global HTTP(S) load balancer with serverless NEG, Cloud Armor/WAF (only mentioned as a possibility, p.37), Direct VPC egress, fixed egress IP.
- **Scaling**: minimum instances as a flag (`--min-instances`), revision tags by command, percentage canary (only the concept, p.48-49).
- **CI/CD and supply chain**: Cloud Deploy, Binary Authorization, image scanning/signing; pipelines beyond Cloud Build triggers (p.81-82).
- **Events**: Eventarc, Pub/Sub push in detail (Events for Cloud Run only in Table 1-1, p.35).
- **Costs**: current prices, current free tier, billing per instance/allocated CPU, budgets (only "configure budgets and alerts", p.42).
- **Organization security**: VPC Service Controls, Workload Identity Federation, Org Policy.

## Content that changed since 2020 [DATED] (e.g., 2020 numbers must be checked)
All limits and prices in the table of `cli-flags-e-limites-datados.md`; default concurrency (250 in Nov/2020); in-memory disk (4 GB in Oct/2020); maximum timeout (60 min); SIGTERM (~10 s); 20 5xx responses; session affinity "not supported" (p.106); the need for App Engine for Cloud Tasks (p.130); Cloud Workflows "recent" (p.136); Container Registry -> Artifact Registry (p.72); buildpacks and builder v1 (p.78); Terraform 0.12 and provider "~> 3.0" (p.143-145); Kubernetes 1.19.2 and Kourier 0.17 (p.153, 156); OpenCensus (p.169; today OpenTelemetry) [extrapolation]; "Stackdriver" (p.162); regions (p.46); the rule "Cloud Run only pulls from Artifact Registry" (p.72) is inconsistent with p.45.

## Internal tensions of the book (flag to the user)
1. The book uses a `gcr.io` image in the first deploy (p.45) and says only Artifact Registry is an accepted source (p.72).
2. Cloud Build "sends the image to Container Registry" (p.79) but the example repository is Artifact Registry.
3. The book advocates `--max-instances` and a pool to protect the database (p.96) but says the optimal concurrency is hard to find and must be measured in production (p.95).
4. The author gives opinions (future of App Engine/Functions, p.59-60): speculation, not fact.
5. Typo: p.116 prints `--no-allow-authenticated` in the text; the correct flag, `--no-allow-unauthenticated`, appears in the listing on p.117 (and on p.123). Do not copy the form from p.116.

## Referral to other agents
- Lambda, API Gateway, SAM, AWS: `aws-lambda-serverless-expert`.
- Advanced Dockerfile, Compose, Kubernetes (Deployments, ingress, Helm): `containers-docker-kubernetes-expert`.
- OpenTelemetry/Collector/observability SLOs: `observability-opentelemetry-expert`.
- Git, branching, CI: `git-version-control-expert`; delivery metrics: `dora-devops-delivery-expert`.

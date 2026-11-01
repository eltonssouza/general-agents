# Glossary (the book's vocabulary; PDF pages)

| Term | Short definition (paraphrase) | Page |
| --- | --- | --- |
| Serverless | simplifies dev, scales by itself, pay for usage | 30 |
| FaaS | function as glue in a runtime framework, e.g. Cloud Functions/Lambda | 33 |
| Service | Cloud Run resource: name, HTTPS endpoint, config and traffic | 36 |
| Revision | immutable copy of the configuration, created on every change | 48 |
| Container image | package with app + dependencies + image configuration | 44, 64 |
| Port 8080 | default port the container must listen on | 44 |
| Request buffer | temporary queue of the service when there is no free slot | 52-54 |
| Concurrency | number of slots (simultaneous requests) per container | 54 |
| Autoscaler | decides to add/remove containers based on free slots and CPU | 54 |
| CPU throttling | CPU limited when the container is not serving requests | 50, 52 |
| Cold start | wait of a request until the container opens the port | 55 |
| Minimum instances | concept: keep containers ready | 55 |
| SIGTERM | shutdown notice, about 10 s to clean up | 50 |
| GFE (Google Frontend) | HTTPS entry point: TLS, DoS, authorization, headers | 119 |
| Region | physical datacenter where the service runs | 45 |
| Artifact Registry | regional repository of images and packages | 61, 72 |
| Distroless | minimal base images without shell/packages | 71-72 |
| ko / Jib / Buildpacks | image generators without a Dockerfile (Go / Java / multi-language) | 75-78 |
| Cloud Build | remote build with container steps (cloudbuild.yaml) | 78-81 |
| Cloud SQL | managed relational database (not serverless) | 83, 86 |
| Cloud SQL Proxy | TLS tunnel authenticated by IAM; managed on Run | 86, 89 |
| Unix Domain Socket | file in `/cloudsql/` used as the connection port | 89 |
| Transaction concurrency | simultaneous transactions in the database | 93 |
| Connection pool | reused long-lived connections; limits concurrency | 96 |
| Memorystore | managed Redis (not serverless) | 101-102 |
| VPC Connector | resource that carries traffic from Run to private IPs of the VPC | 102-104 |
| Session affinity | routing the same client to the same container (not supported in 2020) | 106 |
| SLA | quality document with financial compensation | 106 |
| Cloud IAM | identity and permission control | 109 |
| Role / Policy binding | set of permissions / member-role link | 109-110 |
| Service account | non-personal identity of a service | 110, 113 |
| allUsers | member that represents the whole internet | 110 |
| Cloud Run Invoker | role that allows invoking a service | 110-112 |
| ID token | signed JWT (OIDC) to authenticate calls | 117-118 |
| Audience | token field that identifies the destination service | 118 |
| Cloud Tasks | schedules and executes HTTP requests with retry | 127-129 |
| Worker | Cloud Run service that executes the task | 128 |
| Dispatch deadline | task timeout | 129, 132 |
| Backoff / doublings | queue retry parameters | 133-134 |
| IaC / Terraform / HCL | declarative infrastructure / tool / language | 139-147 |
| Provider / resource / state | plugin / resource block / record of what exists | 145-150 |
| plan / apply | generates / executes the changes | 148-149 |
| ADC | Application Default Credentials | 143-144 |
| Structured logging | JSON logs with metadata | 160 |
| X-Cloud-Trace-Context | trace header added by the GFE | 165, 168 |
| Log-based metric | metric created from log attributes | 171-172 |
| Knative Serving | Kubernetes extension with the same model as Cloud Run | 176 |
| CRD | Kubernetes custom resource definition | 180 |
| Minikube / kubectl / Kourier | local cluster / client / example HTTP load balancer | 180-184 |

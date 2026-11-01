# Serverless model and product choice (RUN ch. 1 and end of ch. 2)

PDF pages. Everything is `[DATED]` regarding prices, regions and products: the book is from 2020.

## What the author calls serverless
- **[from source]** Scope: web applications that receive requests (or events) over HTTPS, including the HTTP/2 family (RUN p.29-30). Serverless, for the author, means three things: a simple developer experience (no infrastructure management), scale out of the box and pay-per-use cost ("if you don't use it, you don't pay") (RUN p.30).
- **[from source]** What stops being your task: provisioning servers, patches, network and firewall, TLS, deployment automation, tolerance to hardware failure, logs and metrics. What remains: writing and updating your code securely, configuring resources, scaling limits and access policies (RUN p.31).
- **[from source]** Serverless is not the same as FaaS: functions are "glue code" in a runtime framework; Cloud Run, besides being serverless, is more capable than FaaS and is not limited to HTTPS requests (RUN p.33).
- **[from source]** Three-step workflow: an app that starts an HTTP server, package it in a container image, deploy (creates a *service* with an HTTPS endpoint) (RUN p.36).

## Cost model and concerns
- **[from source]** Billing for the resources used while serving requests, with 100 ms granularity and a small fee per million requests (RUN p.32). **[DATED]** the billing model and prices have changed since 2020; confirm on the current pricing page.
- **[from source]** Serverless is not always cheap: it can cost more if you already use close to 100% of server capacity all the time; the author says 20% to 40% utilization is the common case (RUN p.32).
- **[from source]** Concerns: unpredictable costs (cost becomes a quality attribute; mitigate with scaling limits, resource tuning and load testing), hyper-scalability that overloads downstream systems (relational databases, APIs with rate limits), "when it really goes wrong" you depend on the vendor (all that is left is opening a ticket), and the separation between compute and storage can add latency (RUN p.39).
- **[from source]** Portability comes from two things: the container format and API compatibility with Knative (RUN p.40). Take care not to couple the code to GCP services with no open-source alternative (RUN p.40, note).

## Cloud Run features according to ch. 1
- **[from source]** Scale and self-healing: by default up to a thousand instances per service, raisable by quota request; a failed instance is replaced (RUN p.37). **[DATED]**.
- **[from source]** Automatic HTTPS endpoint, custom domain, virtual network integration, internal non-public services (RUN p.37). Microservices (RUN p.37). Per-service identity and policies on who invokes (RUN p.37-38). Default metrics and logs to Cloud Logging (RUN p.38). Gradual rollout and blue-green "supported" (RUN p.38).

## Table 1-1 (GCP serverless products, 2020)
- **[from source]** Messaging: Pub/Sub, Cloud Tasks, Cloud Scheduler (proprietary); Events for Cloud Run (open-source compatible). Compute: Cloud Run (compatible), App Engine and Cloud Functions (proprietary, with an upgrade path). Storage: Cloud Storage and Firestore. A serverless relational database is missing: Cloud SQL is managed, does not scale by itself and bills for allocated capacity (RUN p.35). **[DATED]** the portfolio has changed.

## Cloud Run vs Cloud Functions vs App Engine (ch. 2, p.57-60)
- **[from source]** Cloud Functions: deployment from source code, own runtime, great as "glue" between GCP services; not suited for highly concurrent workloads, no traffic splitting or easy revision management, handles a single endpoint, uses one container per request (RUN p.57-58).
- **[from source]** App Engine: a platform that predates GCP; Standard (1st and 2nd generation) runs on the same platform as Cloud Run and Functions; Flexible runs on Compute Engine, with visible servers and SSH (RUN p.58).
- **[from source]** Decisive differences: source-code-based vs container-based (the author prefers containers for stability and portability; advantage of source code: automatic patching of base layers) and request-oriented vs instance-oriented (on App Engine Standard background threads work and billing is less granular) (RUN p.59). Cloud Run can also be used in a source-code-based workflow with Buildpacks (RUN p.59).
- **[from source]** The author is skeptical about App Engine being discontinued and thinks Cloud Run is the future: this is his **opinion and speculation** (RUN p.59-60). Do not treat it as fact.

## Decision rule
- **[inference]** Web service/API with concurrency: Cloud Run (container). React to a GCP event with little code: Functions, according to the book. Quick prototype with a mature framework and background threads: App Engine Standard may fit (RUN p.58-59). **[extrapolation]** New products (Cloud Run functions, Jobs) change this tree; see `fronteira-e-datado.md`.

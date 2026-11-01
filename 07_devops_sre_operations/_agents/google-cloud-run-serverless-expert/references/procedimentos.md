# Procedures (the book's operational playbooks)

Each `[from source]` step carries the page; adaptations are `[inference]`. `[DATED]` flags: confirm in the current documentation.

## P1. First deploy and new version
1. Create project/account, `gcloud init`, `gcloud config set project ID`, `gcloud services enable run.googleapis.com` (RUN p.43-45).
2. `gcloud run deploy NAME --image IMG [--allow-unauthenticated]`; confirm the region (RUN p.45-46).
3. Update: `gcloud run services update NAME --image IMG:tag` (creates a revision) (RUN p.48).
4. Rollback: `gcloud run revisions list --service NAME`; `gcloud run services update-traffic NAME --to-revisions REV=100` (RUN p.48-49).

## P2. Containerize
1. Choose a path: Dockerfile (multi-stage + distroless), ko (Go), Jib (Java) or Buildpacks (RUN p.71-78).
2. Create a repository in Artifact Registry; `gcloud auth configure-docker`; `docker push` or `gcloud builds submit --tag` (RUN p.73-79).
3. Ensure port 8080, readiness in seconds, SIGTERM handled (RUN p.44, 50, 55-56).

## P3. Connect a Cloud SQL database securely
1. Create the instance in the same region as the service; load the schema through `gcloud beta sql connect` (RUN p.85, 87-88).
2. Remove `root@%` without a password, create the user via `cloudsqlproxy~%`; in production, an app user without admin privilege (RUN p.88-89).
3. `--add-cloudsql-instances` + `--set-env-vars DB=...unix(/cloudsql/...)` (RUN p.91); `--require-ssl` to close the direct connection (RUN p.90).
4. Protect against bursts: `--max-instances`, `SetMaxOpenConns` (max instances x connections <= the database's optimal concurrency), external pool if needed; HA, backups, ~1 min tolerance (RUN p.93-98).

## P4. Background work (Cloud Tasks)
1. Enable the API, create the queue, service accounts `task-app` and `worker`; private worker with `--timeout`, `--cpu`, `--memory` (RUN p.130).
2. Bindings: Invoker on the worker for the app account; Enqueuer on the queue; Service Account User to create a task with a token (RUN p.131-133).
3. Configure retry/rate limit, **idempotency** with a record in the database, review exhausted tasks (RUN p.133-136). Use `scripts/tasks_retry_schedule.py`.

## P5. Minimal identity and private service
1. Create one service account per service; `--service-account` on deploy (RUN p.115, 124).
2. `--no-allow-unauthenticated` on internal services; `roles/run.invoker` binding on the destination service for the caller's account (RUN p.117, 124-125).
3. The client calls with an ID token (audience = destination URL); remember the ~7-9 ms latency per call (RUN p.118-120).
4. If you get 403 right after the binding, wait about 20 s and try again (RUN p.124).

## P6. Useful logs and correlation
1. JSON on stdout with `severity`; no PII (RUN p.158, 160-163).
2. Trace ID in the logs via `X-Cloud-Trace-Context`; propagate in outgoing calls (RUN p.165-169).
3. Log-based metrics for alerts (RUN p.171-172).

## P7. IaC with Terraform
1. ADC, never a downloaded key (RUN p.143-144). 2. `terraform init`; `plan -out`; review; `apply` (RUN p.145-149). 3. Remember the service's IAM policy and protect the state (RUN p.150-152). 4. Gradual rollout outside Terraform (RUN p.143).

## P8. Assess portability
1. Keep a Knative `service.yml` and config via env vars (RUN p.76, 92, 185-186). 2. List proprietary services in use: IAM, Firestore, Tasks, Scheduler (RUN p.188). 3. Measure the effort of moving from Cloud Run to Knative (smaller) vs the reverse (larger) (RUN p.187).

## P9. Shut down and avoid billing (each chapter)
`gcloud run services delete`, `gcloud sql instances delete`, `gcloud redis instances delete`, delete the VPC Connector (RUN p.82, 98, 108).

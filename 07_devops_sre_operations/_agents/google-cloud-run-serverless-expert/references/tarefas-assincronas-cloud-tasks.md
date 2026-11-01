# Asynchronous tasks with Cloud Tasks (RUN ch. 7, p.127-137)

## Why
- **[from source]** Background threads and local cron do not work well in serverless: CPU only during requests and disposable containers (RUN p.127; see throttling in `runtime-...md`). Cases cited: processing an image, generating a PDF, a screenshot with a headless browser, reindexing search (RUN p.127).

## Model
- **[from source]** **Scheduling** a task = handing Cloud Tasks the "recipe" of an HTTP request; **executing** = Cloud Tasks makes the request. You need a place to run it: a separate Cloud Run service, the **worker**, which can be protected by IAM, scales independently and can have more CPU/memory (RUN p.127-128).
- **[from source]** The queue does not guarantee order; success = HTTP 2xx response; failures (timeout or non-2xx) are retried according to the queue configuration (RUN p.129, 133).
- **[from source]** Deadline: 10 minutes by default in Cloud Tasks, up to 30; the maximum for a Cloud Run request was 60 minutes (RUN p.129) **[DATED]**. If it does not fit, split the work (3,000 images = 30 jobs of 100) (RUN p.129).

## Demo playbook (RUN p.129-133)
1. `gcloud services enable cloudtasks.googleapis.com`; `gcloud tasks queues create jobs` (may ask for an App Engine app in the project, at no cost) in the same region (RUN p.130) **[DATED]**.
2. Service accounts `task-app` and `worker` (RUN p.130).
3. Worker: `gcloud run deploy worker --image ... --timeout 900 --cpu 2 --memory 2G --service-account ... --no-allow-unauthenticated` and `roles/run.invoker` binding for the `task-app` account (RUN p.130-131).
4. Public task-app; variable `QUEUE` with the full queue name (`gcloud tasks queues describe jobs`); `roles/cloudtasks.enqueuer` binding on the queue for the task-app account: `gcloud tasks queues add-iam-policy-binding` (RUN p.131).
5. Code: the task carries an OIDC token with `ServiceAccountEmail` and `Audience`; `DispatchDeadline` of 15 min (Example 7-1) (RUN p.132). The ID token is attached **at execution**, not at scheduling (because of delays and retries), with one hour of validity (RUN p.132). Whoever creates the task needs the **Service Account User** role on the account used: `gcloud iam service-accounts add-iam-policy-binding ... --role roles/iam.serviceAccountUser` (RUN p.132-133).
6. Variable `WORKER_URL`; test by watching the logs of both services (RUN p.133).

## Queue configuration
- **[from source]** Retry: four parameters `minBackoff`, `maxBackoff`, `maxDoublings`, `maxAttempts`. First interval = minBackoff; in the doubling phase the interval doubles on each attempt; then comes the linear phase (increment described in the book as 2^maxDoublings + minBackoff); the interval stays constant at maxBackoff; attempts stop on reaching maxAttempts; the camelCase names appear in the listing on p.135 (RUN p.133-135, Figure 7-2). Book example: minimum backoff 1 s, 2 doublings, maximum 15 s, linear increment 5 s (RUN p.133). Use `scripts/tasks_retry_schedule.py` to compute the sequence (book model, **[DATED]**: the real API formula may differ).
- **[from source]** Once attempts are exhausted, Cloud Tasks forgets the task; options: unlimited attempts (risk of repeating "until the end of time") or record the state in a database and review periodically (RUN p.134).
- **[from source]** Rate limiting: `maxDispatchesPerSecond` and `maxConcurrentDispatches`; the default of 1,000 is very high; test: 1,000 tasks at 1,000 simultaneous may finish slower than with concurrency 20 (RUN p.134). Defaults shown in the demo: `maxConcurrentDispatches: 1000`, `maxDispatchesPerSecond: 500.0`, `maxAttempts: 100`, `maxBackoff: 3600s`, `maxDoublings: 16`, `minBackoff: 0.100s` (RUN p.135) **[DATED]**. View/change: `gcloud tasks queues describe jobs`, `gcloud tasks queues update jobs` (RUN p.135).

## Considerations
- **[from source]** **Duplicate delivery** can occur (chance below 0.001%); if running twice would be catastrophic, record the task in a database when creating it and mark it "in progress" in the worker (idempotency); this also allows tracking undelivered tasks (RUN p.135-136). **[DATED]** the number.
- **[from source]** No official emulator; the author runs the request in a goroutine in development; there is an emulator not supported by Google (RUN p.136).
- **[from source]** Alternatives: Pub/Sub as an HTTP queue (less suitable) and Cloud Workflows, newly launched in 2020, for chained tasks (RUN p.136). **[DATED]**.

## Boundary
Cloud Run Jobs, Cloud Scheduler with Cloud Run, Eventarc/Pub/Sub push and Workflows in depth: **NOT COVERED** (Cloud Scheduler only appears in Table 1-1 and in the lists of proprietary services; see `fronteira-e-datado.md`).

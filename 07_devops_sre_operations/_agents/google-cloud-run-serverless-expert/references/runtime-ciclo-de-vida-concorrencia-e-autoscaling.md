# Runtime: lifecycle, throttling, concurrency, autoscaling, cold start (RUN ch. 2, p.50-57)

This is the core of the book. All numbers are `[DATED]` (Oct-Nov/2020); the mental model, however, is what the author emphasizes most.

## Container lifecycle
- **[from source]** New revision: Cloud Run downloads the image, keeps a cached copy and starts the container; when it starts listening on port 8080 it begins receiving requests (RUN p.50).
- **[from source]** When scaling down, it stops sending requests to the container and the CPU is *throttled*. An idle container may be reused or shut down; shutdown begins with **SIGTERM** (and the CPU stops being limited) and, after a short grace period, the container dies. You do not control which containers are kept (RUN p.50).
- **[from source]** There are about **10 seconds** after SIGTERM to clean up: close database connections, flush buffers (e.g., metrics agent) (RUN p.50). **[DATED]**.

## CPU throttling and background work
- **[from source]** The CPU is only fully guaranteed while the container is serving requests; outside that it gets small slices, insufficient for real work; you only pay while serving (RUN p.52).
- **[from source]** Consequence: scheduling work for after the response is returned (background thread) is **not reliable**; the example is processing a profile photo after upload. It shows up mainly under low load or during scale down. Heavy background work also reduces the capacity to serve other requests and causes HTTP 503 on scale up (RUN p.52). Solution in the book: Cloud Tasks (see `tarefas-assincronas-cloud-tasks.md`).
- **[extrapolation] [DATED]** Today there are always-allocated CPU options and Jobs that change this rule; the book does not cover them.

## Load balancer, buffer and autoscaler
- **[from source]** A service-internal load balancer (not the GLB) distributes requests to containers with free *slots*; with no free container, the request waits in the service's **request buffer** until the autoscaler makes one available; the autoscaler tries to avoid buffering and maximize utilization (RUN p.52-53; Figure 2-5, seen in the PDF: LB, buffer, containers with used/free slots, autoscaler receiving free-slot and CPU metrics).
- **[from source]** **Concurrency** = number of slots per container. With `--concurrency 1` each request has exclusive access: good for CPU-intensive load and for apps that are not thread-safe (RUN p.54).
- **[from source]** The autoscaler acts on free slots and also on container CPU; it adds containers up to the maximum (default a thousand). At the limit, Cloud Run responds **HTTP 429**; more than a thousand requires a quota increase request (RUN p.54). **[DATED]**.
- **[from source]** Default concurrency **250** (Nov/2020) is probably too high (Python and heavy runtimes exhaust the CPU first); apps that only wait on I/O can handle more. For bursts, tune concurrency so the autoscaler reacts to slots and never to high CPU, a slower signal (RUN p.55). **[DATED]**.

## Cold start
- **[from source]** The first request after a new deploy, or after a period without traffic, waits in the buffer until the container opens port 8080. Less likely during scale up, since the request is only assigned at the last moment. The autoscaler may keep a small pool of ready throttled containers (not billed) and wake them almost instantly (RUN p.55).
- **[from source]** To always have a container ready, use **minimum instances** (concept cited; the flag does not appear in the book) (RUN p.55). `--min-instances` is `[extrapolation]` `[DATED]`.
- **[from source]** Make the app ready in seconds: it reduces deploy time (RUN p.38) and favors choosing Go and small images (RUN p.22, 71).

## Disposable containers, disk and readiness
- **[from source]** Containers can restart, fail or vanish: data to be preserved goes to a downstream system. You may keep in memory/disk: rebuildable cache, temporary request data, compiled templates, database connections (RUN p.55-56).
- **[from source]** The file system is **in memory**; writing consumes RAM; maximum of 4 GB in Oct/2020; exceeding it forces a stop with no chance to clean up (RUN p.56). **[DATED]**.
- **[from source]** Readiness = accepting connections on 8080. A problem for stacks that open the port before being ready (e.g., NGINX + PHP-FPM); Cloud Run does not allow changing this check and the author suggests switching to Apache (RUN p.56). **[DATED]** (the book does not cover health checks/probes).
- **[from source]** More than **20** consecutive 5xx responses cause the container to be taken out of service and replaced (RUN p.56). **[DATED]** / not confirmed in the current documentation.

## Summary of the author's key points (RUN p.57)
HTTPS endpoint that invokes the container; adds/removes instances; useful work only during the request; disk/memory only for transient data; well-tuned concurrency improves performance.

## Heuristics
1. **[from source]** If something "works on a traditional server" but depends on CPU outside of requests, rethink the design (RUN p.52, 57).
2. **[inference]** To limit cost and protect databases, combine `--max-instances` and connection pooling (see `dados-cloud-sql-memorystore-e-sessoes.md`).
3. **[inference]** Symptom "503 on scale up" -> check for background work consuming CPU (RUN p.52); symptom "429" -> instance cap reached (RUN p.54).

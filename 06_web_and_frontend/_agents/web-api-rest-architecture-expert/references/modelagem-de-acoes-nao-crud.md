# Actions and operations that are not CRUD

## Actions on a process (start/stop/pause)

Many reach for a verb/RPC design; there are options faithful to the noun model (APIGEE p.53):

1. **State property**: the client changes `state` to started, stopped or paused (APIGEE p.53).
2. **Request entity**: the process exposes `actionRequests` (URL); the client POSTs a `StartRequest`, `StopRequest`, `PauseRequest` or `ResumeRequest` to that URL (APIGEE p.53).
   - Advantages: the POST creates a persistent entity recording who did what and when; for long-running requests, the POST returns a resource whose state shows the progress (APIGEE p.53).
3. **Properties per request type**: `startRequests`, `pauseRequests`, `stopRequests`, `resumeRequests`; their presence or absence says which requests are valid in the current state (`initial` → only start; `running` → pause/stop; `pause` → resume/stop). It can be the same URL for all of them. A technique learned from Siren, which has a more elaborate version (APIGEE p.54).

The book does **not** offer a "pragmatic exception" with a verb in the path (`/jobs/42/start`).

## Calculations, translations, conversions

- Model the result as a resource: `/monetary-amount/100/EUR/CNY`; alternative with content negotiation; POST to a noun URL with cache and uniformity costs (APIGEE p.37, p.38, p.39). See [filtragem-ordenacao-e-busca-em-colecoes.md](filtragem-ordenacao-e-busca-em-colecoes.md).

## Outside the source

- The source does not discuss `202 Accepted`, queues, or "GET must not have side effects" (an HTTP rule, [extrapolation]).

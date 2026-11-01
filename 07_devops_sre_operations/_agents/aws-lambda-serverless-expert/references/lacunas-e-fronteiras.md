# Gaps, dated content and boundaries of the collection

Convention: `(LAMBDA p.N)` = PDF page (printed = N - 22).

## Edition and dating
- Copyright of the text: 2022 (LAMBDA p.2). The releases table starts in May 2018 and the last entry is 2022-11-28 (Lambda SnapStart for Java) (LAMBDA p.968). Therefore the collection does NOT cover anything after Nov/2022. [from source] / [inference]
- Anything that is a number, limit, runtime, SDK/CLI version, region, price or console format is [DATED]. In particular: runtimes table (LAMBDA p.102-103), quotas (LAMBDA p.875-877), burst per region (LAMBDA p.248, 261), SnapStart only java11 (LAMBDA p.353).
- The text mixes eras: code examples use old runtimes (nodejs12.x, ruby2.5, java8) alongside newer tables (LAMBDA p.883, 893-940). [DATED]

## What the collection does NOT cover (treat as [extrapolation] or route elsewhere)
- Concrete prices (only "standard charges apply" and pointers) and detailed free tier.
- Runtimes and features after Nov/2022 (response streaming, Node.js 20, Python 3.10+, Java 17, AL2023, ScalingConfig/MaximumConcurrency of the SQS ESM, advanced JSON logging, SnapStart for other runtimes). Verified by negative search in the text.
- Deprecation calendar beyond 2023-03-31 (only nodejs12.x and dotnetcore3.1) (LAMBDA p.102-104).
- Per-account provisioned concurrency quota, maximum individual layer size, Step Functions limits (not detailed in the quotas section).
- Response payload limit and maximum timeout of Function URLs (do not appear).
- Event filtering parameters in detail in the service chapters (only pointers); EventBridge Pipes only mentioned.
- Idempotency: only the textual recommendation, without implementation examples.
- Layers: order of precedence between layers and total size are not described in the layers pages.
- Telemetry API: per-event schemas summarized; API authentication/IAM not detailed.
- Hyperplane: latency/IPs per subnet do not appear.

## Defects in the text itself
See `casos-e-antipadroes.md` (contradictions section). Also: broken reference "???" on p.101; typo "with with" on p.968; example SCP ARN on p.76-77 and get-policy output with Sid "sns" and s3 principal on p.92 (reading notes).

## Boundaries with other agents
- Google Cloud Run and Cloud Functions: agent `google-cloud-run-serverless-expert`.
- Generic Kubernetes/containers: containers agent (Docker/Kubernetes).
- General observability/OpenTelemetry: observability agent; here only what the guide says about X-Ray/ADOT/Telemetry API.
- Delivery/DevOps (DORA) and SRE: corresponding agents.

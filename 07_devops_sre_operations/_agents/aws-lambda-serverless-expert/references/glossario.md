# Glossary (terms from the AWS Lambda Developer Guide, 2022 edition)

Convention: `(LAMBDA p.N)` = PDF page (printed = N - 22). Definitions in my own words. [DATED] = depends on a number/version of the 2022 edition.

| Term | Operational meaning | Source |
|---|---|---|
| Function | Invocable resource that runs your code; the central unit of the service | (LAMBDA p.34) |
| Trigger | Resource/configuration that invokes the function (configured AWS service or event source mapping) | (LAMBDA p.34) |
| Event | JSON document with the data to process; when a service invokes, it defines the format | (LAMBDA p.34) |
| Event source mapping (ESM) | Lambda resource that reads items from a stream or queue and invokes the function in batches | (LAMBDA p.34, 41) |
| Execution environment | Isolated environment in which runtime, extensions and your code run; reused across invocations | (LAMBDA p.35, 48) |
| Instruction set architecture | arm64 (Graviton2) or x86_64, per function [DATED] | (LAMBDA p.35) |
| Deployment package | .zip (Lambda provides OS and runtime) or container image (you include OS, runtime and dependencies) | (LAMBDA p.35) |
| Runtime | Per-language layer that relays events, context and responses between Lambda and the function | (LAMBDA p.35) |
| Layer | .zip file with libraries/data/custom runtime, extracted to /opt; up to 5 per function [DATED]; does not apply to image functions | (LAMBDA p.36) |
| Extension | Internal process (in the runtime) or external (separate, continues after the invocation) that extends the environment | (LAMBDA p.36) |
| Concurrency | Number of requests being served at the same time; each concurrent request uses one environment | (LAMBDA p.36, 233) |
| Qualifier | Version (immutable snapshot) or alias (updatable pointer to a version) that identifies which "face" of the function to invoke | (LAMBDA p.36-37) |
| Destination | Event destination resource for asynchronous invocation (success/failure): SQS, SNS, Lambda, EventBridge | (LAMBDA p.37, 301) |
| Cold start | Extra latency of creating and initializing a new environment (Init phase); the text associates it with an idle function, scaling or an update | (LAMBDA p.253) |
| Init / Invoke / Shutdown | Environment lifecycle phases; Init limited to 10 s and Shutdown to 2 s [DATED] | (LAMBDA p.49-50) |
| Reserved concurrency | Concurrency ceiling and guarantee for a function (no cost); 0 blocks the function | (LAMBDA p.240, 250) |
| Provisioned concurrency | Pre-initialized environments on a version/alias (with cost); does not apply to $LATEST | (LAMBDA p.242, 254) |
| Burst concurrency | Initial scaling per region (500-3000) and then +500 instances/min [DATED] | (LAMBDA p.248, 261) |
| $LATEST | Unpublished, editable version of the function | (LAMBDA p.214, 226) |
| Alias routing | Traffic split between two published versions by weight | (LAMBDA p.229-230) |
| DLQ | SQS queue or SNS topic that receives the event (without response details) after a failed asynchronous invocation | (LAMBDA p.301, 305) |
| Hyperplane ENI | Managed ENI that connects the function to the account's VPC; one per subnet + security group combination | (LAMBDA p.51-52) |
| Execution role | IAM role assumed by the function to access services and write logs | (LAMBDA p.72) |
| Resource-based policy | Policy attached to the function/version/alias/layer that says who can invoke/use it | (LAMBDA p.88-89) |
| Function URL | Dedicated HTTPS endpoint of the function; AuthType AWS_IAM or NONE | (LAMBDA p.335-337) |
| SnapStart | Snapshot of the initialized environment of a published version; java11 only in this edition [DATED] | (LAMBDA p.353) |
| Runtime hook | Code before the snapshot / after restore (CRaC) | (LAMBDA p.361) |
| RIC / RIE | Runtime interface client (in the image) / emulator (local image testing) | (LAMBDA p.196-201) |
| Custom runtime | Own runtime (provided / provided.al2) that uses the Runtime API | (LAMBDA p.111-113) |
| IteratorAge | Metric of stream read lag | (LAMBDA p.874) |
| Batch item failures | Response that reports which items of the batch failed so only those are reprocessed | (LAMBDA p.774) |
| Idempotency | Property of handling the same event several times without duplicate effect; recommended for async, streams and queues | (LAMBDA p.301, 324, 872) |

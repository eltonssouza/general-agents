# Cases and antipatterns (AWS Lambda Developer Guide, 2022 edition)

Convention: `(LAMBDA p.N)` = PDF page (printed = N - 22). Everything below is [from source] on the cited page, unless marked. Numbers are [DATED].

## Antipatterns explicit in the text
| # | Antipattern | Why it is a problem / what to do | Source |
|---|---|---|---|
| A1 | Recursive code (a function that triggers itself, e.g. writes to the S3 bucket that invokes it) | Generates unintended volume and cost; brake with reserved concurrency = 0 / the Throttle button and fix the recursive path | (LAMBDA p.872, 832) |
| A2 | Initializing SDK clients/connections inside the handler on every invocation | Loses environment reuse; initialize outside the handler | (LAMBDA p.871) |
| A3 | Storing user/sensitive data in the environment between invocations | Risk of leakage between invocations | (LAMBDA p.871) |
| A4 | Assuming Lambda always reuses the environment | Other factors create a new environment and cause unexpected connection failures | (LAMBDA p.50) |
| A5 | Reusing an idle connection without keep-alive | Lambda drops idle connections and reuse errors out | (LAMBDA p.871) |
| A6 | Relying on the built-in SDK without control | Lambda updates the environment's libraries and behavior may change; package dependencies | (LAMBDA p.872) |
| A7 | Using undocumented APIs | Internal changes break the invocation | (LAMBDA p.872) |
| A8 | Auth NONE on a Function URL with a public resource policy by accident | Anyone with the URL invokes the function | (LAMBDA p.337) |
| A9 | Provisioned concurrency on $LATEST | Not supported; configure on a version/alias | (LAMBDA p.254) |
| A10 | Provisioned = reserved | Everything runs on provisioned and $LATEST is throttled | (LAMBDA p.247, 253) |
| A11 | SnapStart + provisioned concurrency on the same version | Not allowed | (LAMBDA p.354) |
| A12 | SnapStart: keeping state that requires uniqueness (IDs, secrets, entropy) in init | A single snapshot resumes many environments and repeats the value; generate it in the handler/hook | (LAMBDA p.359) |
| A13 | SnapStart: using the hostname as a unique ID, binding a fixed port, extra DNS cache | All environments resume with the same value / failures after restore | (LAMBDA p.366) |
| A14 | SnapStart: losing the strong reference to the CRaC hook | The Context keeps only a WeakReference; GC may discard the hook | (LAMBDA p.362) |
| A15 | Permission granted only to the alias ARN and invoking without alias/version | Permission error; the permission applies to the authorized ARN | (LAMBDA p.229) |
| A16 | `put-function-event-invoke-config` to change a single option | Overwrites the entire configuration; use `update-function-event-invoke-config` | (LAMBDA p.304) |
| A17 | `update-function-configuration` with just one env var | Replaces the entire Variables structure | (LAMBDA p.220) |
| A18 | DLQ configured on the function when the source is SQS | The DLQ must be on the source queue | (LAMBDA p.307, 774) |
| A19 | Database secrets in env vars | The text recommends Secrets Manager | (LAMBDA p.219) |
| A20 | Cross-account SQS tutorial with `sqs:*` in the queue policy | Violates least privilege (reader's observation about the text's example) | (LAMBDA p.785) |

## Practical cases (with the guide's reasoning)
**Case 1. SQS queue with reprocessed messages.** By default, an error returns the whole batch to the queue (LAMBDA p.773). Enable ReportBatchItemFailures, ensure idempotency, visibility timeout >= 6 x timeout [DATED] (LAMBDA p.774) and a DLQ on the queue (LAMBDA p.307).

**Case 2. Stalled Kinesis/DynamoDB stream.** A "poison" record repeats the batch and blocks the shard (LAMBDA p.325, 648). Alarm on IteratorAge (LAMBDA p.874); use bisect, retry/age limits and an on-failure destination (LAMBDA p.648).

**Case 3. Synchronous API with high cold start.** Measure Init Duration; reduce init; evaluate provisioned concurrency on an alias (LAMBDA p.253-254) or SnapStart if Java 11 [DATED] (LAMBDA p.353). Confirm that the trigger (e.g. API Gateway) does not point to $LATEST (LAMBDA p.833).

**Case 4. VPC function lost internet access.** Egress now goes through the VPC: route to a NAT gateway in a public subnet; or a VPC endpoint for AWS services (LAMBDA p.836-837). Typical symptom: "Task timed out" (LAMBDA p.836-837).

**Case 5. Function stuck in Pending.** In a VPC the function stays Pending while it creates ENIs (LAMBDA p.831-832); if it exceeds ~6 min [DATED], a new update/publish call unblocks it and may lead to Failed (LAMBDA p.832).

**Case 6. One function consumes all the concurrency.** Use reserved concurrency to split the account into pools (LAMBDA p.832, 240).

**Case 7. S3 -> Lambda -> S3 loop.** Interrupt (Throttle) and fix the recursive path (LAMBDA p.832); avoid writing to the bucket that triggers the function (LAMBDA p.589, 872).

**Case 8. Canary rollout.** Alias with routing config of 2 versions, same role and DLQ; observe the executed version via the START log, the Executed Version dimension or the x-amz-executed-version header (LAMBDA p.229-231).

**Case 9. Lost asynchronous event.** Configure a DLQ/on-failure destination; an event that expires or exhausts its retries is discarded (LAMBDA p.301, 305).

**Case 10. Validate configuration before applying.** Run `lambda_validate_config.py` (limits from the text) and the checklist (LAMBDA p.871-874, 875-877). [extrapolation about tool usage]

## Contradictions and errors in the text itself (do not propagate)
- Memory: an example error cites a maximum of 3008 (LAMBDA p.831) while the quotas table says 10,240 MB (LAMBDA p.876); the text attributes this to new accounts with a reduced quota (LAMBDA p.875), without reconciling.
- The reserved x provisioned comparison table (LAMBDA p.247-248) seems to diverge from the p.245 example about throttling.
- Telemetry API buffering: maxItems/timeoutMs values diverge between p.150 and p.155 (reading notes).
- Stream retry/age: default shown as 10000/604800 in the CLI and -1 in the table (LAMBDA p.647, 655).
- Examples with old runtimes (nodejs12.x, ruby2.5, java8) next to newer tables [DATED] (LAMBDA p.883, 893-940).

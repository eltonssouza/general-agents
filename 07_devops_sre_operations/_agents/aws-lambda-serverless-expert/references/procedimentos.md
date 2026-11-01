# Operational procedures (derived from the guide, 2022 edition)

Convention: `(LAMBDA p.N)` = PDF page (printed = N - 22). Steps are marked `[from source]` when the cited page supports them; `[extrapolation]` when it is knowledge from outside the collection. Numbers are [DATED] (2022 edition): check the current quotas. Commands/CLI [DATED].

## P1. Choose the invocation model and design error handling
1. Identify who invokes: push service (synchronous or asynchronous) or ESM (queue/stream polling) (LAMBDA p.586-588). [from source]
2. Synchronous: the caller decides on retry; the function may have run partially/fully/not at all, so the code tolerates duplicates (LAMBDA p.324). [from source]
3. Asynchronous: 2 retries (waits 1 and 2 min), throttle/5xx go back to the queue for up to 6 h; configure MaximumRetryAttempts (0-2) and MaximumEventAgeInSeconds (60-21600); configure a DLQ or on-failure destination (LAMBDA p.301-305, 1085). [from source] [DATED]
4. Stream: an error repeats the batch and blocks the shard; use MaximumRetryAttempts/RecordAge, bisect, on-failure destination, report batch item failures (LAMBDA p.648). [from source]
5. SQS queue: no retry in the ESM; use visibility timeout >= 6 x timeout, maxReceiveCount >= 5, DLQ on the queue, ReportBatchItemFailures (LAMBDA p.774). [from source] [DATED]
6. Make the code idempotent (LAMBDA p.301, 872). [from source]

## P2. Size memory, timeout and /tmp
1. Measure: REPORT line (Max Memory Used) per invocation; test memory with Power Tuning; more memory = more CPU (LAMBDA p.872). [from source]
2. Set the timeout by load testing, considering network dependencies that may not scale (LAMBDA p.872-873). [from source]
3. Check the range: memory 128-10,240 MB, timeout up to 900 s, /tmp 512-10,240 MB (above 512 incurs cost) (LAMBDA p.216-217, 876). [from source] [DATED]
4. Validate with `scripts/lambda_validate_config.py`. [extrapolation of tool use]

## P3. Plan concurrency
1. Calculate: concurrency = average RPS x average duration in seconds (LAMBDA p.238-239). [from source]
2. Compare with the account limit (1,000 default) and the unreserved pool (always >= 100) (LAMBDA p.233, 250). [from source] [DATED]
3. Protect a downstream resource or critical function with reserved concurrency (ceiling + guarantee, no cost) (LAMBDA p.240-242, 252). [from source]
4. For predictable latency, provisioned concurrency on a version/alias, never $LATEST, with ~10% headroom (LAMBDA p.249, 254). [from source] [DATED]
5. Automate with Application Auto Scaling (target tracking/scheduled); beware of short bursts that do not trigger the alarm (LAMBDA p.257-259). [from source]
6. Monitor ConcurrentExecutions, ProvisionedConcurrencyUtilization and Spillover (LAMBDA p.249, 255). [from source]

## P4. Diagnose cold start
1. Confirm init: Init Duration in the REPORT; the Init phase runs static code and has a 10 s limit (LAMBDA p.49). [from source] [DATED]
2. Reduce: init outside the handler only for what is needed, smaller package, simple dependencies (LAMBDA p.871-872). [from source]
3. If Java 11: evaluate SnapStart (publish a version, enable ApplyOn=PublishedVersions); review uniqueness and connections after restore (LAMBDA p.353-358, 359-362). [from source] [DATED]
4. If it requires tens of ms latency: provisioned concurrency (cost); do not use with SnapStart on the same version (LAMBDA p.354). [from source]
5. If there is PC and still cold start: check the correct version/alias, trigger pointing to $LATEST, spillover (LAMBDA p.833). [from source]

## P5. Connect a function to a VPC
1. Configure subnets and security groups (up to 5 SGs and 16 subnets [DATED]) and give the role permission to manage ENIs (LAMBDA p.53, 1291). [from source]
2. Ensure egress: NAT gateway in a public subnet for internet; VPC endpoints for AWS services (LAMBDA p.52, 836-837). [from source]
3. Wait for the Active state (ENI can take minutes; a new function fails until active) (LAMBDA p.52). [from source]
4. Check the ENI quota per VPC (250 default) (LAMBDA p.837). [from source] [DATED]
5. Relational database: consider RDS Proxy (LAMBDA p.273). [from source]

## P6. Publish a version, alias and gradual rollout
1. Publish a version (immutable snapshot; not created if code is identical) (LAMBDA p.226). [from source]
2. Point an alias (never alias to alias); use the alias in event sources and permissions (LAMBDA p.229). [from source]
3. Rollout: routing config with up to 2 versions, same role and DLQ, both published; promote with empty AdditionalVersionWeights (LAMBDA p.229-230). [from source]
4. With CodeDeploy/SAM: rolling deployments (LAMBDA p.828, 839). [from source]

## P7. Deploy via .zip or container image
1. .zip: respect 50 MB zipped / 250 MB unzipped (includes layers) [DATED]; use S3 if larger (LAMBDA p.876). [from source]
2. Image: up to 10 GB [DATED], AWS base or alternative with RIC; test with RIE; push to ECR (LAMBDA p.195-206, 876). [from source]
3. Layers only in .zip; up to 5 per function [DATED] (LAMBDA p.36, 876). [from source]
4. Code signing if the organization requires it (LAMBDA p.282). [from source]

## P8. Configure a queue/stream as a source (ESM)
1. Give the execution role read permission on the source (LAMBDA p.590). [from source]
2. Adjust BatchSize (1-10,000; SQS FIFO 10), window (0-300 s; BatchSize > 10 requires >= 1) [DATED] (LAMBDA p.1003-1005). [from source]
3. Define error handling per P1; for Kinesis, shards and partition key (LAMBDA p.873-874). [from source]
4. Alarm on IteratorAge (LAMBDA p.874). [from source]

## P9. Observe and investigate
1. AWS/Lambda metrics in CloudWatch, logs, Lambda Insights, X-Ray (LAMBDA p.795-814). [from source]
2. Common troubleshooting errors: Pending/ResourceConflict, ENILimit, EFS mount, InvokeFunction not authorized (LAMBDA p.831-837). [from source]
3. Alarms on errors/duration/throttles instead of metrics in the code (LAMBDA p.873). [from source]

## P10. Review a function
Run `scripts/lambda_review_checklist.py` (42 items) and `scripts/lambda_validate_config.py` (limits from the text). Results are indicative; [DATED] items require checking against current documentation. [extrapolation of use]

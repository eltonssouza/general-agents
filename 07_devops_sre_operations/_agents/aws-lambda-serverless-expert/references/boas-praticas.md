# Guide best practices

> Code, configuration, metrics and alarms, streams.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the text of the references has no accents, because the reading notes it came from had none.

## BEST PRACTICES (chapter 'Best practices for working with AWS Lambda functions')
### Function code
- [from source] (LAMBDA p.871) Separate the handler from the business logic to ease unit testing (Node example: myHandler calls MyLambdaFunction(foo, bar))
- [from source] (LAMBDA p.871) Reuse the execution environment: initialize SDK clients and database connections OUTSIDE the handler and cache static assets in /tmp; later invocations on the same instance reuse them, reducing time and cost
- [from source] (LAMBDA p.871) Do not store user data, events or sensitive information in the execution environment (avoid leakage between invocations); if you need mutable state that does not fit in memory in the handler, consider a separate function/version per user
- [from source] (LAMBDA p.871) Use keep-alive for persistent connections: Lambda drops idle connections over time; reusing an idle connection causes a connection error
- [from source] (LAMBDA p.871) Use environment variables for operational parameters (e.g. S3 bucket name) instead of hard-coding
- [from source] (LAMBDA p.872) Control dependencies: Lambda periodically updates the environment's libraries (e.g. the AWS SDK in the Node.js and Python runtimes), which can subtly change behavior; for full control, package all dependencies
- [from source] (LAMBDA p.872) Minimize the package size to what the runtime needs (shorter download/unpack time); in Java/.NET Core do not ship the entire AWS SDK, depend selectively on modules
- [from source] (LAMBDA p.872) Java: put dependency .jar files in a separate /lib directory, which unpacks faster than a single jar with many .class files
- [from source] (LAMBDA p.872) Minimize dependency complexity: prefer simple frameworks that load fast (e.g. Dagger or Guice instead of Spring Framework)
- [from source] (LAMBDA p.872) Avoid recursive code (a function that calls itself): it can generate an unintended volume of invocations and cost; if it happens, set reserved concurrency to 0 immediately to block all invocations while you fix the code
- [from source] (LAMBDA p.872) Do not use undocumented/non-public APIs (internal updates may be incompatible and cause invocation failures)
- [from source] (LAMBDA p.872) Write idempotent code: validate events and handle duplicates consistently
### Function configuration
- [from source] (LAMBDA p.872) Test performance to find the optimal memory: more memory = more CPU; memory use per invocation is visible in the REPORT line (Max Memory Used) to detect under- or over-provisioning; the open source AWS Lambda Power Tuning project is recommended; also recommended is using libraries that take advantage of AVX2 (ML inference, media, HPC, simulations, financial modeling)
- [p.872-873] Load test to find the optimal timeout; important when the function makes network calls to resources that may not support Lambda's scaling (a dependency can increase concurrency beyond what is expected)
- [from source] (LAMBDA p.873) Most restrictive IAM permissions possible: limit the execution role to what the function needs
- [from source] (LAMBDA p.873) Know the quotas: payload, file descriptors and /tmp space are frequently forgotten
- [from source] (LAMBDA p.873) Delete unused functions, so they do not count unnecessarily toward the package size limit
- [from source] (LAMBDA p.873) With SQS as the event source, the function's expected invocation time must not exceed the queue's Visibility Timeout; in CreateFunction creation fails; in UpdateFunctionConfiguration it can generate duplicate invocations
### Metrics and alarms
- [from source] (LAMBDA p.873) Use Lambda metrics and CloudWatch Alarms instead of creating/updating metrics inside the function code; e.g. an alarm based on the expected duration to find bottlenecks
- [from source] (LAMBDA p.873) Use a logging library and Lambda metrics/dimensions to detect application errors (ERR, ERROR, WARNING)
- [from source] (LAMBDA p.873) Use AWS Cost Anomaly Detection (machine learning; uses Cost Explorer data; [DATED] delay of up to 24 hours to detect); you must first sign up for Cost Explorer
### Streams
- [from source] (LAMBDA p.873) Test different batch/record sizes to tune the polling frequency; BatchSize in CreateEventSourceMapping controls the maximum records per invocation; a larger batch dilutes overhead and increases throughput
- [from source] (LAMBDA p.873) By default Lambda invokes as soon as there are records (one record = one invocation); the batching window can buffer for [DATED] up to 5 minutes; Lambda reads until it gathers a full batch, the window expires or the batch reaches [DATED] 6 MB of payload
- [p.873-874] Kinesis: increasing shards increases throughput; Lambda polls each shard with at most one concurrent invocation (e.g. 100 active shards = at most 100 concurrent invocations); when increasing shards, choose a good partition key so related records land on the same shard and distribution is good
- [from source] (LAMBDA p.874) Use CloudWatch on IteratorAge to know whether the stream is being processed; e.g. an alarm with a maximum of [DATED] 30000 (30 seconds)



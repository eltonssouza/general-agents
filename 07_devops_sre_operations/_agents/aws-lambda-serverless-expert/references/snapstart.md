# Lambda SnapStart

> Concept, limitations, pricing, activation, uniqueness, runtime hooks, monitoring, best practices.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the reference text is unaccented because the original reading notes were written that way.

## 1. SnapStart (pp.353-367)
### 1.1 Concept and limitations
- [from source] (LAMBDA p.353) SnapStart (Java) promises to reduce initialization latency by up to 10x, at no extra cost and usually without changing code; the biggest contributor to cold start is init time (loading code, starting the runtime, initializing the function code) [DATED: 10x]
- [from source] (LAMBDA p.353) Mechanism: Lambda initializes the function when a version is PUBLISHED, takes a Firecracker microVM snapshot (memory + disk) of the already initialized environment, encrypts it and caches it; on the first invocation and when scaling, new environments are resumed from the snapshot instead of being initialized from scratch
- [from source] (LAMBDA p.353) Warning: if the application depends on state uniqueness, the code must be evaluated for resilience to snapshot operations
- [from source] (LAMBDA p.353) [DATED] Supported runtime: Java 11 only (java11). Does NOT support: provisioned concurrency, arm64, Extensions API, EFS, X-Ray, ephemeral storage larger than 512 MB
- [from source] (LAMBDA p.353) Only published versions and aliases that point to versions; does NOT work on $LATEST
- [p.353-354] Categories to review in the init code: (1) Uniqueness: IDs, secrets and entropy generated during init stay in the snapshot and repeat across environments -> generate after init; (2) Network connections: state is not guaranteed after resume; validate/reestablish; (3) Temporary data (credentials, cached timestamps): refresh in the handler
- [from source] (LAMBDA p.354) In most cases the connections created by the AWS SDK resume automatically
- [from source] (LAMBDA p.354) Ephemeral data must be refreshed in the handler before use, even without SnapStart
### 1.2 Pricing and comparison with provisioned concurrency
- [from source] (LAMBDA p.354) No additional cost for SnapStart; you are charged for requests, duration and configured memory; duration rounded up to the nearest 1 ms [DATED: 1 ms]
- [from source] (LAMBDA p.354) Duration billing includes the handler, init code outside the handler AND code in runtime hooks. Lambda periodically recycles environments and reruns init; for resilience it replicates snapshots across several AZs and charges each time it reruns init in another AZ
- [from source] (LAMBDA p.354) Decision rule: SnapStart improves up to 10x at no cost; provisioned concurrency keeps functions initialized and responding in double-digit ms, but incurs charges; use PC if there is a hard cold start latency requirement; you CANNOT use both on the same version
### 1.3 Enable and manage (pp.355-358)
- [from source] (LAMBDA p.355) Console: Configuration > General configuration > Edit > SnapStart = "Published versions" > Save; then publish a version (Lambda initializes, creates the snapshot, caches it) and invoke the version
- [from source] (LAMBDA p.355) CLI (existing function) [DATED: CLI]: update-function-configuration --snap-start ApplyOn=PublishedVersions; publish-version; get-function-configuration --function-name my-function:1
- [from source] (LAMBDA p.356) Ready when OptimizationStatus = On and State = Active on the version; invoke requires --cli-binary-format raw-in-base64-out in AWS CLI v2 [DATED: CLI]
- [from source] (LAMBDA p.356) New function: create-function with --runtime java11 and --snap-start ApplyOn=PublishedVersions, then publish-version
- [from source] (LAMBDA p.357) API: CreateFunction or UpdateFunctionConfiguration with the SnapStart parameter; PublishVersion; GetFunctionConfiguration (version); Invoke
- [from source] (LAMBDA p.357) States: Pending (init + snapshot in progress; invocations/API actions on the version FAIL), Active (ready; invoke the published version), Inactive (version not invoked for 14 days; Lambda deletes the snapshot) [DATED: 14 days]
- [from source] (LAMBDA p.357) ERROR/retry: invoking an Inactive version after 14 days returns SnapStartNotReadyException and starts a new snapshot; wait for Active and invoke again
- [from source] (LAMBDA p.358) Failed: error while running init or creating the snapshot. These states also occur when Lambda periodically recycles the environment
- [from source] (LAMBDA p.358) Updating the snapshot = publishing a new version; Lambda automatically updates snapshots with runtime and security patches
- [from source] (LAMBDA p.358) SDKs: ephemeral execution role credentials arrive via environment variables; with SnapStart the Java runtime automatically uses container credentials (AWS_CONTAINER_CREDENTIALS_FULL_URI / AWS_CONTAINER_AUTHORIZATION_TOKEN) instead of access keys, so they do not expire before the restore
- [from source] (LAMBDA p.358) Snapshots are deleted when the function/version is deleted or after 14 days without invocation; resources removed in compliance with GDPR
### 1.4 Uniqueness (pp.359-360)
- [from source] (LAMBDA p.359) Rule: when scaling, a single snapshot resumes several environments; unique content generated during init (IDs, secrets, entropy) will not be unique. Generate after init (in the handler) or use a runtime hook
- [from source] (LAMBDA p.359) Practice 1: do not keep state that depends on uniqueness in init (e.g. a unique ID for logging); generate it in the handler (the Java example generates a UUID lazily in the handler)
- [from source] (LAMBDA p.359) Practice 2: use CSPRNGs; the managed Java runtime has two built in (OpenSSL 1.0.2 and java.security.SecureRandom) that keep randomness with SnapStart; software that always reads /dev/random or /dev/urandom also keeps it [DATED: OpenSSL 1.0.2]
- [from source] (LAMBDA p.360) Scanning tool: open source SpotBugs plugin (aws-lambda-snapstart-java-rules repository) that performs static analysis of code that assumes uniqueness
### 1.5 Runtime hooks (pp.361-362)
- [from source] (LAMBDA p.361) Hooks (before snapshot / after restore) come from the open source CRaC project (Coordinated Restore at Checkpoint, under development in OpenJDK). Three elements: Resource (interface with beforeCheckpoint() and afterRestore()), Context<R extends Resource> (where the Resource registers), Core (coordination service; Core.getGlobalContext())
- [from source] (LAMBDA p.361) Steps: (1) add the org.crac dependency to the build (Gradle example: io.github.crac:org-crac 0.1.3 and aws-lambda-java-core 1.2.1) [DATED]; (2) the handler implements Resource and registers itself in the global context (e.g. in the constructor)
- [from source] (LAMBDA p.361) [DATED] With SnapStart, init can last up to 15 minutes (beforeCheckpoint hooks count toward this time); afterRestore hooks time out after 2 seconds
- [from source] (LAMBDA p.362) ANTI-PATTERN: Context keeps only a WeakReference to the Resource; if it is garbage collected the hook does not run. Keep a strong reference; avoid register(new MyResource()) and anonymous class objects
### 1.6 Monitoring (pp.363-364)
- [from source] (LAMBDA p.363) With SnapStart, the REPORT of the first invocation does not contain Init Duration; that field goes in the INIT_REPORT record (includes the duration of beforeCheckpoint hooks). The REPORT of the first invocation contains Restore Duration (includes afterRestore hooks)
- [from source] (LAMBDA p.363) Cold start = Restore Duration + Duration; there is a CloudWatch Logs Insights query for p50/p90/p99/p99.9 percentiles summing @duration + @initDuration + restoreDuration
- [from source] (LAMBDA p.363) Telemetry API: platform.restoreStart, platform.restoreRuntimeDone (status success/failure/timeout; sent when the runtime makes the restore/next request), platform.restoreReport (duration and billed ms of the phase)
- [from source] (LAMBDA p.364) End-to-end latency: API Gateway -> IntegrationLatency metric; function URL -> UrlRequestLatency
### 1.7 Security (p.365)
- [from source] (LAMBDA p.365) Snapshots encrypted at rest with KMS: by default an AWS managed key; optionally a customer managed key (control over rotation/organization requirements), at standard KMS cost
- [from source] (LAMBDA p.365) Deleting a SnapStart function/version makes all Invoke calls fail; snapshots not invoked for 14 days are deleted
### 1.8 Best practices (pp.366-367)
- [from source] (LAMBDA p.366) Reestablish network connections in the handler (or in an afterRestore hook, which times out after 2 s)
- [from source] (LAMBDA p.366) ANTI-PATTERN: do not use the hostname (InetAddress.getLocalHost()) as a unique environment identifier - they all return the same value; generate the ID in the handler or in afterRestore
- [from source] (LAMBDA p.366) ANTI-PATTERN: binding connections to fixed source ports (may fail after restore)
- [from source] (LAMBDA p.366) ANTI-PATTERN: Java DNS cache - Lambda already caches DNS; another cache can cause timeouts after resume
- [p.366-367] Tuning: preload in init the classes that weigh on startup; if not possible, "dummy invocations" (the pet store/Spring example sends a fake API Gateway request in a static block; if it fails, it rethrows the exception to force another cold start)
- [NOT COVERED] No real-gain figure beyond "up to 10x"; no list of supported Regions in this section.



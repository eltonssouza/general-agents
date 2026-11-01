# Concurrency and scaling

> Concurrency calculation, reserved, provisioned, burst, metrics and concurrency quotas.
> Source: AWS Lambda Developer Guide (2022 edition; last releases entry on 2022-11-28), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label are from the source; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the original Portuguese reading notes were written without accents.

## Scaling and the concept of concurrency
- [from source] (LAMBDA p.233) Concurrency = number of requests in progress at the same time; Lambda provisions a separate execution environment per concurrent request and scales automatically up to the account limit
- [from source] (LAMBDA p.233) [DATED] Default total account concurrency limit: 1,000 across all functions per region; you can request a quota increase and configure per-function controls to avoid throttling critical functions
- [p.233-234] Cycle: to handle a request, Lambda initializes the environment (Init phase, runs code outside the handler) and then the Invoke phase; during this the environment is busy; when done it is reused without reinitializing
- [from source] (LAMBDA p.234) New request: uses a pre-initialized environment if available; otherwise creates a new environment
- [p.235-236] Example with 10 requests: A-E created in the first 5, 6-8 reuse A,B,C, 9 creates F (A-E busy), 10 reuses D; concurrency at any instant = active environments at that point (peak 6 in the example)
- [from source] (LAMBDA p.238) [FORMULA] Concurrency = (average requests per second) x (average request duration in seconds)
- [from source] (LAMBDA p.239) Concurrency differs from RPS: 100 rps x 1 s = 100; 100 rps x 0.5 s = 50; 200 rps x 0.25 s = 50; 5,000 rps x 20 ms = 100


## Reserved vs provisioned concurrency
- [from source] (LAMBDA p.239) The account shares an on-demand pool of 1,000; when exhausted there is throttling (requests are dropped)
- [p.239-240] Reserved: reserves part of the account's concurrency for a function (prevents others from consuming everything); Provisioned: pre-initializes environments, reduces cold start
- [from source] (LAMBDA p.240) Reserved = MAXIMUM concurrent instances of the function and also a guarantee; no other function can use that concurrency; functions without a reservation share the unreserved pool; counts toward the account limit; no cost
- [from source] (LAMBDA p.242) Example: limit 1,000; 400 reserved for function-blue and 400 for function-orange; other functions share 200. Orange reaches 400 at t3 and is throttled even with idle concurrency elsewhere; at t4 the other functions are throttled because they exhaust the 200
- [from source] (LAMBDA p.242) Effects: (1) scales independently of other functions; (2) does not scale out of control - the reservation is a ceiling, protects downstream resources; (3) may waste unused reserved concurrency
- [from source] (LAMBDA p.242) Reserved concurrency does NOT pre-initialize environments; long initialization = cold start; provisioned initializes N environments ready to respond immediately
- [from source] (LAMBDA p.243) With provisioned, Lambda still recycles environments in the background but always keeps the pre-initialized number equal to the configured one; with reserved, an environment can be terminated after inactivity
- [from source] (LAMBDA p.245) Provisioned example: 400 provisioned for function-orange; the remaining 600 (unreserved) are shared by all, including orange; when exceeding 400, orange uses unreserved concurrency (no throttling, but with cold starts); throttling only on reaching the account's 1,000
- [from source] (LAMBDA p.245) The two can be combined (e.g.: provisioned as a weekday baseline, reserved for weekend peaks)
- [from source] (LAMBDA p.247) Combined example: 200 provisioned + 400 reserved; beyond 200 it uses reserved (with cold start); at 400 throttling because it cannot access the pool of 600 unreserved
- [from source] (LAMBDA p.247) Both count toward the account limit and regional quotas; provisioned incurs cost
- [from source] (LAMBDA p.247) Rule: if provisioned summed over versions/aliases = the function's reserved, all invocations use provisioned and $LATEST is throttled (does not run); you cannot allocate more provisioned than reserved
- [from source] (LAMBDA p.247) Automate provisioned scaling by schedule/utilization: Application Auto Scaling
- [p.247-248] Comparison table: Reserved = maximum, on-demand instances, cold start possible, throttles on reaching the limit, no cost; Provisioned = fixed pre-provisioned number, cold start eliminated, if without reserved it throttles on reaching provisioned (table text), additional cost; without configuration the function uses the unreserved pool
- [from source] (LAMBDA p.248) [DATED] Quotas at two levels: account 1,000 by default; function level can reserve up to 900 by default (100 always remain for functions without a reservation); e.g.: account 2,000 => 1,900 reservable
- [from source] (LAMBDA p.248) [DATED] Initial burst per region: 3000 (US West Oregon, US East N. Virginia, Europe Ireland); 1000 (Asia Pacific Tokyo, Europe Frankfurt, US East Ohio); 500 (others). If the account limit < burst, the account limit applies. After the burst, +500 instances per minute
- [p.248-249] Estimate: ConcurrentExecutions metric (e.g. average 5-10, peak 20 => reserved 20); or formula using the Invocations and Duration metrics
- [from source] (LAMBDA p.249) [DATED] Recommendation: provisioned with 10% headroom over the typical need (peak 200 => 220)
- [from source] (LAMBDA p.249) Metrics: ConcurrentExecutions, UnreservedConcurrentExecutions, ProvisionedConcurrentExecutions, ProvisionedConcurrencyInvocations, ProvisionedConcurrencySpilloverInvocations, ProvisionedConcurrencyUtilization (exec/total provisioned; .5 = 50%)
- [from source] (LAMBDA p.250) Configure reserved in the console: Configuration > Concurrency > Edit > Reserve concurrency > value > Save
- [from source] (LAMBDA p.250) Reservable limit = the "Unreserved account concurrency" displayed minus 100; reserved concurrency = 0 fully throttles the function (stops event processing until the limit is removed)
- [from source] (LAMBDA p.251) Effects of the reservation: other functions do not prevent scaling; the function does not scale uncontrolled (ceiling); (continues p.252)
- [from source] (LAMBDA p.252) Reserved concurrency protects downstream resources; recommendation: limit who can use PutFunctionConcurrency and DeleteFunctionConcurrency, since they affect the pool of the other functions
- [from source] (LAMBDA p.252) API: PutFunctionConcurrency, GetFunctionConcurrency, DeleteFunctionConcurrency, GetAccountSettings; CLI put-function-concurrency --reserved-concurrent-executions 100 returns ReservedConcurrentExecutions


## Provisioned concurrency (configuration)
- [from source] (LAMBDA p.253) Cold start occurs when the function was unused, needs to scale or was updated; large code/dependencies or creating SDK clients in init aggravate it; provisioned gives consistent latency (mobile/web backends, latency-sensitive microservices, synchronous APIs)
- [from source] (LAMBDA p.253) Provisioned counts toward reserved and regional quotas; sum of provisioned (versions+aliases) = reserved => everything runs on provisioned and $LATEST is throttled; you cannot allocate more provisioned than reserved; integrates with Application Auto Scaling (schedule or utilization)
- [from source] (LAMBDA p.253) SnapStart vs provisioned: SnapStart improves startup by up to 10x at no extra cost; provisioned keeps functions ready in tens of ms, has a cost; use provisioned for strict cold-start requirements; it is NOT possible to use both on the same version
- [from source] (LAMBDA p.254) Configured on a version or alias; each version can have only ONE provisioned configuration (direct or via alias); two aliases cannot allocate to the same version
- [from source] (LAMBDA p.254) When the version pointed to by the alias changes, Lambda deallocates from the old one and allocates on the new one; an alias with a routing config does not allow managing provisioned while the routing is active
- [from source] (LAMBDA p.254) Provisioned is NOT supported on $LATEST; make sure the client does not point to $LATEST
- [from source] (LAMBDA p.254) Console: Configuration > Concurrency > Provisioned concurrency configurations > Add configuration > alias/version > value > Save. API: Put/Get/List/DeleteProvisionedConcurrencyConfig; CLI put-provisioned-concurrency-config --qualifier BLUE --provisioned-concurrent-executions 100; initial response Status IN_PROGRESS with Allocated 0
- [from source] (LAMBDA p.255) [DATED] get-account-settings example: ConcurrentExecutions 1000, UnreservedConcurrentExecutions 900, CodeSizeZipped 52428800 (50 MB), CodeSizeUnzipped 262144000 (250 MB), TotalCodeSize 80530636800 (75 GB)
- [from source] (LAMBDA p.255) Provisioned metrics: ProvisionedConcurrentExecutions, ProvisionedConcurrencyInvocations, ProvisionedConcurrencySpilloverInvocations, ProvisionedConcurrencyUtilization
- [from source] (LAMBDA p.255) Provisioned does not come online immediately: Lambda starts allocating after 1-2 min; [DATED] up to 3000 instances initialized at once (depending on the region), then 500 per minute; scaling quotas apply summing all provisioned requests in the region
- [p.256-257] Optimization: init code runs at allocation time on provisioned instances (no latency impact); on-demand it impacts the first invocation, so init of specific capabilities can be deferred; variable AWS_LAMBDA_INITIALIZATION_TYPE (provisioned-concurrency or on-demand) is immutable over the environment cycle
- [from source] (LAMBDA p.257) .NET 3.1: AWS_LAMBDA_DOTNET_PREJIT = ProvisionedConcurrency (default; ahead-of-time JIT only on provisioned instances), Always, or Never
- [from source] (LAMBDA p.257) Init of provisioned instances runs at allocation and every few hours, when instances are recycled; init is billed even if the instance never processes a request; provisioned runs continuously and is billed separately for init and invocation
- [from source] (LAMBDA p.257) Application Auto Scaling: target tracking (maintains a utilization %; creates and manages CloudWatch alarms) and scheduled scaling (anticipates peaks); flow: RegisterScalableTarget (service-namespace lambda, resource-id function:my-function:BLUE, scalable-dimension lambda:function:ProvisionedConcurrency, min 1, max 100) and PutScalingPolicy (TargetTrackingScaling, TargetValue 0.7, metric LambdaProvisionedConcurrencyUtilization)
- [from source] (LAMBDA p.258) [DATED] Two alarms: AlarmHigh when utilization consistently > 70%; AlarmLow when < 63% (90% of the target); scales up in large steps to the maximum, scales down in smaller periodic steps; beyond the maximum, the function continues on standard concurrency
- [from source] (LAMBDA p.259) Gotcha: alarms use the average statistic; short bursts (20-100 ms function) that do not last 3 minutes, or without three data points at the target, do not trigger scale up
- [from source] (LAMBDA p.260) Scheduled scaling for predictable loads (details outside the text; refers to an external article)


## Burst concurrency
- [from source] (LAMBDA p.261) [DATED] Initial burst 500-3000 per region, quota is NOT per function (applies to all in the region): 3000 Oregon/N. Virginia/Ireland; 1000 Tokyo/Frankfurt/Ohio; 500 others; then +500 instances/min until demand is met or the limit is hit
- [from source] (LAMBDA p.261) [DATED] If requests arrive faster than scaling, or at maximum concurrency, they fail with 429 throttling; they must be retried; exponential growth up to the burst and linear afterwards
- [from source] (LAMBDA p.262) Idle instances are stopped after some time; frozen instances waiting for a request incur no cost



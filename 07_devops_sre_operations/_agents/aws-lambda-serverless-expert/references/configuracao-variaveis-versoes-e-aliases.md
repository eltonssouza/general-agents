# Configuration, environment variables, versions and aliases

> Memory, timeout, ephemeral storage, env vars, versions, aliases, routing.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the text of the references has no accents, because the reading notes it came from had none.

## Function configuration options (console/API)
- [from source] (LAMBDA p.214) The options (triggers, network, file system access, memory, concurrency) apply to both .zip functions and container images; the console also lets you create/edit test events
- [from source] (LAMBDA p.214) A function has one unpublished version ($LATEST) and can have published versions and aliases; the console shows the unpublished version by default, which changes when code/configuration are updated
- [from source] (LAMBDA p.214) Published version = immutable snapshot of code+configuration (exception: a few items such as provisioned concurrency)
- [from source] (LAMBDA p.214) Function overview: view of the function and upstream/downstream resources, with shortcuts to triggers, destinations and layers (.zip only)
- [from source] (LAMBDA p.215) Settings changeable ONLY on the unpublished version: General configuration (memory, Compute Optimizer, timeout, execution role), Permissions, Environment variables, Tags, VPC, Monitoring tools, Concurrency, Function URL
- [from source] (LAMBDA p.215) Tags apply to the whole function (all versions and aliases); reserved concurrency also applies to the whole function including versions and aliases
- [from source] (LAMBDA p.215) A Function URL can be configured on $LATEST or on any alias
- [from source] (LAMBDA p.215) Configurable on a function, version or alias: Triggers, Destinations, Asynchronous invocation (reduce retries / queue time; DLQ retains discarded events), Code signing, Database proxies, File systems, State machines
- [from source] (LAMBDA p.215) For a published version you configure: Triggers, Destinations, Provisioned concurrency, Asynchronous invocation, Database proxies
- [from source] (LAMBDA p.215) Aliases = a named resource that points to a version and can be repointed; each publish generates a new version number
- [from source] (LAMBDA p.216) API: UpdateFunctionCode, UpdateFunctionConfiguration (version settings), TagResource, AddPermission (resource policy of function/version/alias), PutFunctionConcurrency (reserved), PublishVersion, CreateAlias, PutFunctionEventInvokeConfig (asynchronous error), Create/UpdateFunctionUrlConfig
- [from source] (LAMBDA p.216) [DATED] Memory: 128 MB to 10,240 MB in 1 MB steps; CPU proportional to memory; 1,769 MB equals 1 vCPU
- [from source] (LAMBDA p.216) [DATED] Default timeout 3 s, adjustable in 1 s steps up to a maximum of 15 minutes
- [from source] (LAMBDA p.217) [DATED] Ephemeral storage (/tmp): default 512 MB, configurable 512 to 10,240 MB in 1 MB steps; above 512 MB incurs cost
- [from source] (LAMBDA p.217) AWS Compute Optimizer memory recommendations require opt-in with IAM administrator permissions; it only supports the x86_64 architecture
- [p.217-218] Console procedures: edit memory/timeout/ephemeral via Configuration > General configuration > Edit > Save; add a trigger via Function overview > Add trigger
- [from source] (LAMBDA p.218) The Test button before saving creates an unsaved test event, preserved during the session; accessible in the Test or Code tabs


## Environment variables
- [from source] (LAMBDA p.219) Env vars adjust behavior without changing code; they are string pairs in the version-specific configuration; the runtime also injects extra variables about the function/invocation
- [from source] (LAMBDA p.219) Recommendation: use AWS Secrets Manager instead of env vars for database credentials
- [from source] (LAMBDA p.219) Values are literal strings, not expanded/evaluated before invocation; evaluation must be done in the code
- [from source] (LAMBDA p.219) Defined on the unpublished version; when published, they are locked to that version
- [from source] (LAMBDA p.219) [DATED] Requirements: key starts with a letter, minimum 2 characters, only letters/digits/underscore, not reserved; total size of all variables <= 4 KB
- [from source] (LAMBDA p.220) API: UpdateFunctionConfiguration, GetFunctionConfiguration, CreateFunction. update-function-configuration REPLACES the entire Variables structure (include the existing ones to preserve them)
- [from source] (LAMBDA p.220) You can pass the RevisionId from get-function-configuration to the update to avoid a race condition; encryption key via --kms-key-arn (KMSKeyARN)
- [from source] (LAMBDA p.220) Scenario: same code in two functions (test/production) with distinct env vars (database host, log/tracing verbosity)
- [from source] (LAMBDA p.221) Reading per language: Node process.env, Python os.environ[...] / os.environ.get, Ruby ENV[], Java System.getenv, Go os.Getenv, C# Environment.GetEnvironmentVariable, PowerShell $env:
- [from source] (LAMBDA p.222) Lambda encrypts env vars at rest; options: another KMS key, client-side encryption, or CloudFormation with Secrets Manager
- [from source] (LAMBDA p.222) Reserved variables (cannot be set): _HANDLER, _X_AMZN_TRACE_ID (not set in custom provided/provided.al2 runtimes; can be set via the Lambda-Runtime-Trace-Id header), AWS_REGION, AWS_EXECUTION_ENV (prefix AWS_Lambda_; absent in custom), AWS_LAMBDA_FUNCTION_NAME/MEMORY_SIZE/VERSION, AWS_LAMBDA_INITIALIZATION_TYPE (on-demand, provisioned-concurrency, snap-start), AWS_LAMBDA_LOG_GROUP_NAME/LOG_STREAM_NAME, AWS_ACCESS_KEY/AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY/AWS_SESSION_TOKEN, AWS_LAMBDA_RUNTIME_API (custom), LAMBDA_TASK_ROOT, LAMBDA_RUNTIME_DIR
- [p.222-223] Not reserved (extensible): LANG (en_US.UTF-8), PATH, LD_LIBRARY_PATH, NODE_PATH, PYTHONPATH (Python 2.7/3.6/3.8), GEM_PATH (Ruby), AWS_XRAY_CONTEXT_MISSING (LOG_ERROR), AWS_XRAY_DAEMON_ADDRESS, AWS_LAMBDA_DOTNET_PREJIT (always/never/provisioned-concurrency; .NET 3.1), TZ (UTC; NTP synchronizes the clock)
- [from source] (LAMBDA p.223) Example values reflect recent runtimes; they may vary in earlier ones
- [from source] (LAMBDA p.223) Security: server-side encryption at rest always (KMS; default AWS managed key, no cost); a customer managed key gives rotation control and restricts who sees the variables, at standard KMS cost; client-side (encryption helpers in transit) protects in transit
- [from source] (LAMBDA p.224) Helpers procedure: create a CMK in KMS; Edit env vars > Encryption configuration; enable helpers; Encrypt per variable; choose key; copy the Execution role policy (kms:Decrypt) to the role; add code that decrypts (Decrypt secrets snippet); optionally "Use a customer master key" for at rest; Save
- [from source] (LAMBDA p.224) KMS permissions: none for the default key; for a CMK: kms:ListAliases (see keys in the console), kms:CreateGrant and kms:Encrypt (configure), kms:Decrypt (view/manage vars); Lambda creates a grant with the user's permissions
- [from source] (LAMBDA p.224) Whoever lacks Decrypt can still manage the function, but cannot view/edit env vars in the console; to block, use a Deny of kms:Decrypt on the key
- [from source] (LAMBDA p.225) Examples: Blank function; RDS MySQL (VPC+RDS in one template, password in Secrets Manager, config passed via env vars)


## Versions
- [from source] (LAMBDA p.226) Versions serve to manage deployment (e.g. beta without affecting production); a new version = copy of the unpublished one
- [from source] (LAMBDA p.226) Lambda does NOT create a new version if the code in $LATEST is the same as the last published one
- [from source] (LAMBDA p.226) A version includes: code+dependencies, runtime, all settings (incl. env vars), unique ARN
- [from source] (LAMBDA p.226) When publishing, Lambda locks the code and most settings; console: Versions > Publish new version; API: PublishVersion (CLI publish-version)
- [from source] (LAMBDA p.227) Qualified ARN (with a version suffix, e.g. helloworld:42) vs unqualified; an unqualified ARN cannot be used to create an alias; an unqualified ARN implicitly invokes $LATEST
- [from source] (LAMBDA p.227) Once published, neither the ARN nor the code changes; permissions via resource-based or identity-based policy, scoped to function or version; aliases simplify management of event sources and IAM


## Aliases
- [from source] (LAMBDA p.228) Alias = pointer to a version, with its own ARN; created via console (Aliases > Create alias) or CLI create-alias/update-alias/delete-alias
- [from source] (LAMBDA p.229) An alias points only to a version, never to another alias; using an alias in the event source mapping or the resource policy avoids updating when the version changes
- [from source] (LAMBDA p.229) Gotcha: a permission granted to the alias ARN (e.g. helloworld:PROD) does not allow invoking without alias/version, nor invoking the associated version directly: permission error
- [from source] (LAMBDA p.229) add-permission example with --qualifier PROD granting s3.amazonaws.com with source-arn and source-account
- [from source] (LAMBDA p.229) Routing config: part of the traffic to a second version (canary); simple probabilistic model, with high variance at low traffic; with provisioned concurrency, increase instances during routing to avoid spillover
- [p.229-230] Rules: maximum of two versions; same execution role; same DLQ (or none); both published (an alias cannot point to $LATEST)
- [from source] (LAMBDA p.230) The weight is for the additional version; the first receives the remainder (10% additional => 90%); CLI --routing-config AdditionalVersionWeights={"2"=0.03} (3%/97%); update-alias to 0.05; to promote to 100%: update-alias --function-version 2 with AdditionalVersionWeights={} (resets routing)
- [from source] (LAMBDA p.231) Identify the invoked version: the START log contains Version; CloudWatch metric with the Executed Version dimension; the synchronous response carries the x-amz-executed-version header


## Introduction to "Managing functions"
- [from source] (LAMBDA p.232) Concurrency = number of active instances; two types: reserved and provisioned. VPC via security groups and subnets; a database proxy for MySQL/Aurora avoids connection exhaustion; code signing validates the signature of a trusted publisher via signing profiles



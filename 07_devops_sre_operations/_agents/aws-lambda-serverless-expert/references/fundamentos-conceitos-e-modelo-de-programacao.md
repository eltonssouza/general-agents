# Fundamentals, concepts, features and architectures

> What Lambda is, concepts (function, trigger, event, execution environment, runtime, layer, extension, concurrency, qualifier, destination), features, programming model, arm64 vs x86_64, tooling.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label are from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the text of the references is unaccented because it originates from reading notes.

## Overview, when to use (p.23-25)
- [from source] (LAMBDA p.23) Lambda is a compute service that runs code without provisioning/managing servers; AWS handles OS maintenance, capacity, automatic scaling and logging
- [from source] (LAMBDA p.23) Billed only for the compute time consumed; no cost when the code is not running; scales from a few requests/day to thousands/second
- [from source] (LAMBDA p.23) Invocation via the Lambda API or by events from other AWS services; cited uses: processing triggers (S3, DynamoDB), Kinesis streaming, custom backend
- [from source] (LAMBDA p.23) The guide assumes prior experience coding, compiling and deploying in one of the supported languages
- [from source] (LAMBDA p.23) Lambda is ideal as long as the code runs in the standard execution environment and within the resources offered; you are responsible only for the code; you cannot log in to the instances or customize the OS of the provided runtimes
- [from source] (LAMBDA p.24) Alternatives when you need to manage your own compute: EC2 (you choose OS, network, stack, capacity, AZs) and Elastic Beanstalk (deploy on EC2 with full control of the instances)


## Feature summary (p.24)
- [from source] (LAMBDA p.24) Key features: concurrency/scaling controls (limits and provisioned concurrency), functions as container images, code signing, extensions, blueprints (sample code + presets for Node.js and Python runtimes), database proxy, EFS mounting
- [from source] (LAMBDA p.24) Database proxy maintains a connection pool and relays queries, allowing high concurrency without exhausting the database's connections
- [from source] (LAMBDA p.24) EFS can be mounted on a local directory of the function for shared access at high concurrency


## Knowledge prerequisites and resources (p.24-25)
- [from source] (LAMBDA p.24) Expected domains: Linux (processes, threads, file permissions), cloud concepts and IP networking, distributed computing (HTTP as IPC, queues, messaging, concurrency)
- [from source] (LAMBDA p.25) Also IAM/KMS/PKI, services that interact with Lambda (API Gateway, S3, SQS, DynamoDB) and EC2 with Linux
- [from source] (LAMBDA p.25) Suggested learning order for beginners: product overview, console tutorial, then the tutorial for a function as a container image


## Related services (p.25)
- [from source] (LAMBDA p.25) API Gateway forwards HTTP requests to functions; for queue/stream services (DynamoDB, Kinesis) Lambda polls and invokes the function; S3 generates object creation/deletion events; SQS and SNS can trigger functions; Step Functions connects functions in state machines


## Ways to access (p.25-26)
- [from source] (LAMBDA p.25) Interfaces: Console, AWS CLI (Windows/macOS/Linux), SDKs, CloudFormation (supports CDK), SAM (templates + CLI)
- [from source] (LAMBDA p.26) SDKs handle signature calculation, retries and error handling
- [from source] (LAMBDA p.26) Price: there is no cost to create functions; there are charges per execution and for data transfer between Lambda and other services; optional features (e.g. provisioned concurrency) have a cost


## Tooling prerequisites (p.27-29)
- [from source] (LAMBDA p.27) Requires an AWS account; AWS CLI if using the command line; best practice: create an IAM administrator user and use it instead of the root credentials (console password + access keys for the CLI)
- [from source] (LAMBDA p.27) Some features are not in the console, only in the CLI/SDKs; the CLI has commands for all Lambda API operations
- [from source] (LAMBDA p.27) CLI check: `aws lambda list-functions` lists functions in the current Region [DATED: CLI]
- [p.27-28] SAM is an extension of the CloudFormation template language that abstracts tasks such as role creation; supported directly by CloudFormation
- [from source] (LAMBDA p.28) SAM CLI is a separate tool: validates templates, runs applications locally in a Docker container and builds zip or image functions
- [from source] (LAMBDA p.28) For container images, Docker CLI (and ECR) is used
- [p.28-29] Authoring tools per language: Node.js (console, Visual Studio), Java (Eclipse, IntelliJ), C# (Visual Studio, .NET Core), Python (console, PyCharm), Ruby (console), Go and PowerShell (own environment; PowerShell requires PowerShell Core 6.0, .NET Core 3.1 SDK and the AWSLambdaPSCore module) [DATED]


## Getting started with the console (p.30-32)
- [from source] (LAMBDA p.30) Two types of deployment package: .zip file and OCI-compatible container image
- [from source] (LAMBDA p.30) The console offers a code editor for non-compiled languages; for compiled languages you must create the .zip package
- [from source] (LAMBDA p.30) Creation walkthrough: open the Functions page > Create function > Basic information: name (e.g. my-function) and runtime (Node.js 18.x selected in the example) [DATED runtime]
- [from source] (LAMBDA p.30) Runtimes listed: .NET (PowerShell, C#), Go, Java, Node.js, Python, Ruby
- [from source] (LAMBDA p.31) The console creates the function and an execution role that grants permission to send logs; the function assumes the role on invocation and derives from it credentials for the SDK and for reading data from event sources
- [from source] (LAMBDA p.31) Invoke: Test tab > New event, default hello-world template (key1..key3), Save changes, Test
- [from source] (LAMBDA p.31) Limit: up to 10 test events per function per user; not visible to other users [DATED]
- [from source] (LAMBDA p.31) Result: Execution result, Summary (REPORT line of the log), Log output (logs go to CloudWatch); the Monitor tab shows metric graphs
- [from source] (LAMBDA p.32) Cleanup: delete the function (Actions > Delete), the log group /aws/lambda/my-function in CloudWatch, and the execution role created in IAM; can be automated via CloudFormation/CLI
- [from source] (LAMBDA p.32) The created role has a name following the pattern my-function-role-<suffix> (example)


## Fundamentals: concepts (p.33-37)
- [from source] (LAMBDA p.33) The function is the fundamental principle; configurable via console, API, CloudFormation or SAM; Lambda runs several instances in parallel, governed by concurrency and scaling limits
- [from source] (LAMBDA p.34) Function: invocable resource that runs your code
- [from source] (LAMBDA p.34) Trigger: resource/configuration that invokes the function; includes configured AWS services and event source mappings
- [from source] (LAMBDA p.34) Event source mapping: Lambda resource that reads items from a stream or queue and invokes the function
- [from source] (LAMBDA p.34) Event: JSON document with data to process; the runtime converts it to an object and passes it to the code; when a service invokes, the service defines the event shape (e.g. SNS: Records[].Sns)
- [from source] (LAMBDA p.35) Execution environment: secure, isolated environment that manages processes and resources and supports the lifecycle of the function and extensions
- [from source] (LAMBDA p.35) Instruction set architecture: arm64 (Graviton2) or x86_64 [DATED]
- [from source] (LAMBDA p.35) Deployment package: zip (Lambda provides OS and runtime) or container image (you include OS, Lambda runtime and dependencies)
- [from source] (LAMBDA p.35) Runtime: per-language environment inside the execution environment; relays events, context and responses between Lambda and the function; you can use provided runtimes or create your own; with zip the runtime must match the language; with an image the runtime goes in the image
- [from source] (LAMBDA p.36) Layer: .zip file with libraries, custom runtime, data or config; reduces package size and speeds up deploy; promotes code sharing
- [from source] (LAMBDA p.36) Up to 5 layers per function [DATED]; they count toward the deployment size quota; content is extracted to /opt
- [from source] (LAMBDA p.36) Layers are private to the account by default; they can be shared with other accounts or public; functions that already consume a layer from another account keep using the version after deletion or revocation, but you cannot create/update a function using a deleted version
- [from source] (LAMBDA p.36) Container image functions do not use layers; dependencies go in the image
- [from source] (LAMBDA p.36) Extension: internal (runs in the runtime process, same lifecycle) or external (separate process, initializes before the invocation, runs in parallel and continues after the invocation ends)
- [from source] (LAMBDA p.36) Concurrency: number of requests being served at the same time; a new invocation with a request in progress provisions another instance, increasing concurrency
- [from source] (LAMBDA p.36) Concurrency is subject to per-Region quotas; you can limit it per function (reserved) or guarantee a specific level
- [p.36-37] Qualifier: version (immutable snapshot of code+config with a numeric qualifier, e.g. my-function:1) or alias (updatable pointer to a version, can split traffic between two versions, e.g. my-function:BLUE); versions and aliases together form a stable interface
- [from source] (LAMBDA p.37) Destination: AWS resource to which asynchronous invocation events are sent; configurable for failures and, in some services, also for success


## Features (p.38-)
- [from source] (LAMBDA p.38) Scaling: when invocations arrive faster than one instance processes them, Lambda spins up additional instances; as traffic drops, idle instances are frozen or stopped; you pay for initialization and processing time
- [from source] (LAMBDA p.39) Reserved concurrency: reserves part of the account's concurrency for the function and limits it to that dedicated pool (splits the pool into subsets)
- [from source] (LAMBDA p.39) Provisioned concurrency: pre-initializes instances kept always ready, for functions with slow init or very low latency; integrates with Application Auto Scaling for utilization-based autoscaling
- [from source] (LAMBDA p.40) Function URL: dedicated HTTP(S) endpoint per function, invocable by browser, curl, Postman; can be added to an existing or new function
- [from source] (LAMBDA p.40) Synchronous invocation: waits for a response; asynchronous: Lambda queues the event and responds immediately
- [from source] (LAMBDA p.41) In asynchronous invocation Lambda retries if the function returns an error or is throttled; configurable on function, version or alias


## Features (cont.) (p.41-43)
- [from source] (LAMBDA p.41) In asynchronous invocation you can also send failed events to a dead-letter queue or send a record of any invocation to a destination
- [from source] (LAMBDA p.41) Event source mapping: reads from SQS, Kinesis or DynamoDB streams and sends items in batches; each event can contain hundreds/thousands of items; keeps a local queue of unprocessed items and handles retries on error/throttle; configurable (batching, error, destination for failed items)
- [p.41-42] Destinations (asynchronous invocation): send a record to a queue, topic, function or event bus; separate destinations for success and failure; the record contains event details, function response and the reason for sending
- [from source] (LAMBDA p.42) For stream event source mappings, you can send a record of failed batches to a queue or topic; the record has batch metadata and points to the items in the stream (does not contain them)
- [from source] (LAMBDA p.42) Blueprints: when creating a function in the console the options are from scratch, blueprint, container image or Serverless Application Repository app; blueprints include code and presets for Node.js and Python, under the Amazon Software License, console only
- [p.42-43] Test/deploy tooling: Docker CLI, AWS CLI (high-level commands for package upload and template update) and SAM CLI (validates templates, local testing, CI/CD integration)
- [from source] (LAMBDA p.43) Application templates in the console: create an app with a continuous delivery pipeline (function code, application template, CodePipeline infrastructure template with build and deploy stages on every push); MIT No Attribution license; console only


## Programming model (p.44)
- [from source] (LAMBDA p.44) The model is common to all runtimes; it defines the handler (entry point in the function configuration); the runtime passes event and context (function name, request ID) to the handler
- [from source] (LAMBDA p.44) After finishing the first event the runtime sends another; objects/clients declared outside the handler (init code) are reused; recommendation: create reusable resources (SDK clients) at initialization; each instance processes thousands of requests
- [from source] (LAMBDA p.44) With X-Ray active the runtime records separate init and execution subsegments
- [from source] (LAMBDA p.44) Local storage in /tmp; active instances stay for a few hours before being recycled [DATED]
- [from source] (LAMBDA p.44) The runtime captures logs to CloudWatch Logs and records invocation start/end and a report log (request ID, billed duration, init duration etc.); a thrown error is returned to the invoker
- [from source] (LAMBDA p.44) Warning: logging is subject to CloudWatch Logs quotas; logs can be lost due to throttling or, sometimes, when the instance is stopped
- [from source] (LAMBDA p.44) Design rule: requests can be processed out of order or concurrently; keep state in other services; do not depend on long-lived instances; use /tmp and class objects for performance but keep the package and transferred data small
- [from source] (LAMBDA p.44) Per-language chapters (printed pages): Node.js 346, Python 388, Ruby 418, Java 443, Go 484, C# 514, PowerShell 549


## arm64 vs x86_64 architectures (p.45-47)
- [from source] (LAMBDA p.45) Two architectures: arm64 (Graviton2, available in most Regions) and x86_64 [DATED]
- [from source] (LAMBDA p.45) arm64 can give significantly better price/performance; suggested for CPU-intensive workloads (HPC, video encoding, simulation)
- [from source] (LAMBDA p.45) Graviton2: Neoverse N1 core, Armv8.2; larger L2 cache per vCPU reduces memory read latency; better cryptography performance and ML inference on CPU [DATED]
- [from source] (LAMBDA p.45) Requirements to migrate: function on an Amazon Linux 2 runtime; package with only open source components and code under your control; third-party dependencies with an arm64 version
- [p.45-46] Compatibility: code in the built-in editor likely runs on both; code sent by upload must be recompiled/re-sent for the target architecture; layers and extensions must be checked (replace an incompatible layer version); a container image requires a new image for the architecture
- [from source] (LAMBDA p.46) Recommended migration steps (8): list dependencies (libraries, build/deploy/test tools, extensions and monitoring tools), check arm64 versions, set up the environment, bootstrap, test/debug, compare performance with x86_64, update the infrastructure pipeline, deploy in stages
- [from source] (LAMBDA p.46) Rollout tip: use alias routing to split traffic between x86 and arm64 versions and compare performance/latency
- [from source] (LAMBDA p.46) Architecture configurable on new functions via console, SDKs, CLI or CloudFormation; zip or container
- [from source] (LAMBDA p.46) arm64 runtimes (all Amazon Linux 2) [DATED]: Node.js 12/14/16/18, Python 3.8/3.9, Java 8 (AL2)/Java 11, .NET Core 3.1, Ruby 2.7, custom runtime on AL2
- [from source] (LAMBDA p.47) Amazon Linux-based runtimes (e.g. Go 1.x) do not support arm64; for Go on arm64 use the provided.al2 runtime [DATED]


## Console (p.58-64)
- [from source] (LAMBDA p.58) The console configures applications, functions, code signing and layers; Applications lists apps deployed via CloudFormation/SAM
- [from source] (LAMBDA p.58) Code signing: ensures signature by an approved source, unaltered code, signature not expired/revoked
- [p.58-59] Console code editor: only for languages without compilation (Node.js, Python), only zip packages, and the package must be smaller than 3 MB [DATED]; based on Cloud9, not all commands available
- [p.59-63] Editor: Environment window to create/open/rename/delete/copy files and folders; tabs, status bar (go to line, color scheme, tabs/spaces); preferences via the gear (default UI; nothing relevant to Lambda configuration)
- [from source] (LAMBDA p.64) Full-screen mode exposes Save and Test buttons; Test/Configure Events creates or edits test events; Preferences follows the Cloud9 references


## AWS CLI with Lambda (p.65-70)
- [from source] (LAMBDA p.65) The CLI uses the Python SDK (Boto) to call the Lambda API; useful for learning the API
- [from source] (LAMBDA p.65) Example output of `aws --version` (aws-cli/2.0.57) [DATED]; on Windows some Bash commands (e.g. zip) do not work in native terminals: use WSL
- [p.65-66] Create an execution role via CLI: `aws iam create-role --role-name lambda-ex --assume-role-policy-document ...` with an inline trust policy or file://trust-policy.json; the trust policy allows the service principal lambda.amazonaws.com to call sts:AssumeRole [DATED: CLI]
- [from source] (LAMBDA p.66) Attach permissions: `aws iam attach-role-policy ... AWSLambdaBasicExecutionRole` (managed policy under service-role/), which gives permission to write logs to CloudWatch Logs
- [from source] (LAMBDA p.67) Create function: package `zip function.zip index.js`; `aws lambda create-function --function-name my-function --zip-file fileb://function.zip --handler index.handler --runtime nodejs18.x --role <arn>` [DATED CLI/runtime]; output shows Version "$LATEST" and TracingConfig Mode "PassThrough" (default)
- [from source] (LAMBDA p.67) Logs on invocation: `--log-type Tail` returns a LogResult field with up to 4 KB of logs in base64 [DATED]; decode with base64 -d (on macOS base64 -D)
- [from source] (LAMBDA p.68) Example REPORT line: Duration, Billed Duration (rounded in ms), Memory Size 128 MB (default in the example), Max Memory Used
- [from source] (LAMBDA p.68) For full logs: return the log stream name in the function output and read with `aws logs get-log-events --log-group-name /aws/lambda/my-function --log-stream-name ... --limit 5`; the script waits 15 s for the logs to become available; uses --cli-binary-format raw-in-base64-out for the JSON payload
- [from source] (LAMBDA p.69) Update config (works for zip and image): `aws lambda update-function-configuration --function-name my-function --memory-size 256`
- [p.69-70] List: `aws lambda list-functions --max-items 10`; the response includes NextToken and the next page uses --starting-token [DATED: CLI]
- [from source] (LAMBDA p.70) get-function returns metadata (Configuration) and a pre-signed URL (Code.Location) to download the package
- [from source] (LAMBDA p.70) Cleanup: `aws lambda delete-function --function-name my-function`; delete the role in IAM separately



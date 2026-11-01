# Samples, examples and releases (proof of the edition date)

> Sample apps, SDK examples, release history up to 2022-11-28.
> Source: AWS Lambda Developer Guide (2022 edition; last releases entry on 2022-11-28), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label are from the source; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the original Portuguese reading notes were written without accents.

## 1. Sample app "blank function" (p.881-885)
- [from source] (LAMBDA p.881) Blank function is a starter app that shows common operations: logging, environment variables, X-Ray tracing, layers, unit tests and the AWS SDK; the function calls the Lambda API
- [from source] (LAMBDA p.881) [DATED] Variants per language: Node.js (blank-nodejs), Python, Ruby, Java, Go, C# and PowerShell; the details explained are for Node.js but apply to all
- [from source] (LAMBDA p.881) Deploy via AWS CLI + CloudFormation following the README; services used: Lambda, X-Ray, CloudWatch, IAM, S3 (holds the package during deploy), CloudFormation; "standard charges of each service"
- [from source] (LAMBDA p.881) The function also calls the Lambda API to get the account's quotas and usage in the current Region (GetAccountSettings)
- [from source] (LAMBDA p.882) The handler receives an SQS event, iterates over Records, logs the body of each message, logs the event/context/environment variables, calls the SDK and returns the response to the runtime
- [from source] (LAMBDA p.882) In Node.js an async handler must return a promise; the runtime waits for it to resolve and returns the response to the invoker; if the code/SDK errors, the runtime formats the error as a JSON document
- [from source] (LAMBDA p.882) Handler input/output types and support for asynchronous programming vary by runtime
- [from source] (LAMBDA p.882) The app does not include an SQS queue; it uses event.json as an example event; see "Using Lambda with Amazon SQS" (p.750)
- [from source] (LAMBDA p.882) Resources defined in a CloudFormation template with AWS SAM type (Transform AWS::Serverless-2016-10-31); SAM simplifies authoring by automating execution roles, APIs etc.; shell scripts automate setup/deploy/invoke/teardown
- [from source] (LAMBDA p.882) The stack does NOT include the bucket used by the CLI on deploy nor the CloudWatch Logs log group
- [from source] (LAMBDA p.883) [DATED] The example template uses Runtime nodejs12.x, Timeout 10, Tracing Active, policies AWSLambdaBasicExecutionRole / AWSLambda_ReadOnlyAccess / AWSXrayWriteOnlyAccess, and a LayerVersion (CompatibleRuntimes nodejs12.x) -- runtime now discontinued, dated example
- [from source] (LAMBDA p.883) CloudFormation applies the SAM transform generating standard types AWS::Lambda::Function and AWS::IAM::Role; the Code property points to an S3 object matching the local CodeUri
- [from source] (LAMBDA p.884) Deploy steps: `aws cloudformation package` (preprocesses the template, uploads artifacts to S3 and replaces local paths with S3 locations) and `aws cloudformation deploy` (uses a change set); [DATED] requires --capabilities CAPABILITY_NAMED_IAM
- [from source] (LAMBDA p.884) First run creates the blank-nodejs stack; re-running updates it; cleanup script deletes the stack and optionally the bucket and logs
- [from source] (LAMBDA p.884) Active tracing: Lambda records the timing of a SUBSET of invocations and sends it to X-Ray, which generates a service map with a client node and two nodes (AWS::Lambda = service that validates/sends; AWS::Lambda::Function = the function)
- [from source] (LAMBDA p.884) The X-Ray SDK with minimal changes (AWSXRay.captureAWS(require('aws-sdk'))) records AWS SDK calls; the trace shows initialization, invocation and overhead subsegments; client created OUTSIDE the handler for reuse (good practice)
- [from source] (LAMBDA p.884) [DATED] Node.js, Ruby and Python runtimes include the AWS SDK in the execution environment (claim of the 2022 edition)
- [p.884-885] Dependencies via layer: a large package increases deploy time and may prevent testing changes in the console; a layer keeps the package small and avoids re-uploading unchanged dependencies
- [from source] (LAMBDA p.885) Script 2-build-layer.sh: npm install --production and moves node_modules to lib/nodejs/ (structure required by the runtime); on deploy, the layer is only re-uploaded if the lib contents changed


## 2. Sample app "Error processor" (p.886-888)
- [from source] (LAMBDA p.886) Demonstrates a CloudWatch Logs subscription event (p.604): a filter matches the word ERROR in a function's log group and invokes a processor function, which retrieves the full log stream and trace data of the request with the error and stores them
- [from source] (LAMBDA p.886) Services: Lambda, CloudWatch Logs (invokes the function when an entry matches a filter pattern), X-Ray, S3
- [p.886-887] The event arrives with `awslogs.data` encoded (base64/gzip); decoded it carries messageType DATA_MESSAGE, owner, logGroup, logStream, subscriptionFilters, logEvents (id, timestamp, message); the function extracts the request ID from the message
- [from source] (LAMBDA p.887) The processor waits a short period before accessing data to give the log stream and the trace time to finish
- [from source] (LAMBDA p.887) Active tracing in the template + Node.js X-Ray SDK; the error function writes request ID and user as trace ANNOTATIONS (allow locating the trace of a specific request); the processor's calls appear as subsegments
- [from source] (LAMBDA p.887) Template resources: execution role, "primer" function, custom resource, CloudWatch Logs subscription, resource-based policy (allows CloudWatch Logs to invoke the processor), output S3 bucket
- [from source] (LAMBDA p.888) Workaround for a limitation: the log group is only created on the function's first invocation; the subscription depends on the log group, so a third function (primer, inline code) is invoked by a custom resource at deploy to create the log group; DependsOn ensures order (log group and policy before the subscription)


## 3. Sample app "List manager" (p.889-891)
- [from source] (LAMBDA p.889) Processes records from a Kinesis stream: the event source mapping reads in batches and invokes a function that updates documents in DynamoDB and stores a copy of the records in Amazon RDS; a second function (dbadmin) does administrative tasks on the database
- [from source] (LAMBDA p.889) Kinesis vs SQS (text's comparison): Kinesis works as a buffer-queue, records are NOT deleted after being processed (several consumers read the same data), they are processed in order (a queue may deliver out of order); [DATED] records are deleted from the stream after 7 days
- [from source] (LAMBDA p.889) Services: Kinesis, Lambda, DynamoDB, RDS, Secrets Manager (database password), VPC (private function-database network)
- [p.889-890] Two kinds of list: "tally" (values added to the current one per key, e.g. user xp) and "rank" (ranking whose entries overwrite the current value)
- [from source] (LAMBDA p.890) Kinesis event: Records array with kinesis{partitionKey, sequenceNumber, data (base64), approximateArrivalTimestamp}, eventSource aws:kinesis, eventID shardId-..., eventSourceARN; the function decodes data, updates the user's list and the aggregate list (all users) and stores a copy of the event
- [from source] (LAMBDA p.891) The X-Ray SDK records a subsegment for each AWS SDK or MySQL client call; the function uses two DynamoDB tables (primary = state per list+user; aggregate = combines several users)
- [from source] (LAMBDA p.891) The main template creates 2 functions, Kinesis stream, DynamoDB tables, execution role and event source mapping; the second template (template-vpcrds.yml) creates a VPC (private subnets, route table, VPC endpoint for DynamoDB without internet) and RDS + subnet group; separating them makes cleanup easier and lets the database be reused by several apps


## 4. Code examples with AWS SDKs (p.892-959) - SAMPLING
Structure (p.892): Actions (snippets), Scenarios (several calls on the same API) and Cross-service (apps with several services). Actions cover only the most used: Create, Delete, Get, Invoke, List, UpdateFunctionCode, UpdateFunctionConfiguration. Refers to the topic "Using Lambda with an AWS SDK" (p.856).
- [from source] (LAMBDA p.892) Actions are snippets of individual calls and must NOT be run in isolation; each example has a GitHub link with instructions
- [p.893-898] Create function: .NET, Java 2.x, JavaScript V3, Kotlin, PHP, Python (Boto3), Ruby, SAP ABAP variants. Common pattern: name, role, handler, runtime, code (S3Bucket/S3Key or ZipFile) -> returns FunctionArn
- [p.893-898] [DATED] Runtimes used in the examples (several already discontinued/old): .NET `Runtime.Dotnet6` (p.894), Java `JAVA8` (p.894), JS `Runtime.nodejs16x` with `Architectures: [Architecture.arm64]` (p.895), Kotlin `Java8` (p.896), PHP `python3.9` (p.896), Python `python3.8` (p.897), Ruby `ruby2.7` (p.898), ABAP `python3.9` (p.898)
- [from source] (LAMBDA p.895) JS V3 create: for zip, Handler, PackageType and Runtime are required (code comment)
- [p.895,900,908] Kotlin SDK marked as "prerelease documentation ... preview release, subject to change"
- [p.894,896-898,918-922] Pattern of waiting until the function is ready: Java uses `waiter.waitUntilFunctionExists`; Kotlin `waitUntilFunctionActive`; Python `get_waiter('function_active_v2')`; Ruby `wait_until(:function_active_v2 ...)`; after update, `function_updated_v2` / `waitUntilFunctionUpdated` (p.918-922, 934, 939). Illustrates that the function goes through the Pending state before Active (see states in releases p.973-974)
- [p.894-897] Python create uses `Publish=True` and Code={'ZipFile': package}
- [p.898-899] ABAP create: list of handled exceptions = nonexistent code-signing config; account total code quota exceeded; signature validation/integrity failure; invalid parameter; resource already exists/operation in progress (ResourceConflict); resource does not exist; internal service error; maximum throughput reached (TooManyRequests)
- [p.899-905] Delete function: same languages (Get has no Java/Kotlin, p.903-905); Python catches ClientError and handles `ResourceNotFoundException` (p.901) and Ruby `Aws::Lambda::Errors::ResourceNotFoundException` (p.902)
- [p.906-910] Invoke: .NET shows `InvocationType = "Event"` (asynchronous) (p.906); JS V3/Kotlin/Python/PHP use `LogType.Tail`/'Tail' to return the last logs in `LogResult` (base64) alongside the Payload (p.908-909)
- [p.910-911] ABAP invoke: extra errors = request body is not JSON/not parseable, body JSON limit exceeded, deployment package cannot be unzipped
- [p.911-915] List functions: teaches pagination (.NET paginator `await foreach`; PHP MaxItems/Marker/NextMarker; Python walks pages)
- [p.916-919] Update function code: .NET `Publish = true`; JS V3 repeats Architectures arm64 + nodejs16x (p.917); ABAP handles code quota/signature (p.919)
- [p.920-923] Update function configuration: examples update environment variables (`Environment = { Variables }`, p.920-922) and, in ABAP, runtime/memory (`iv_memorysize`, p.923)

### 4.1 "Get started" scenario (p.924-959; 8 languages)
- [from source] (LAMBDA p.924) Scenario flow: create an IAM role that allows writing logs; create the function and upload the handler; invoke with 1 parameter; update the code and set an environment variable; invoke again displaying the returned execution log; list the account's functions; delete the role and function
- [from source] (LAMBDA p.925) Role trust policy: Principal Service lambda.amazonaws.com + Action sts:AssumeRole; after creating the role the .NET example sleeps 10 s ("Waiting for role to become active") -- Ruby also forces a 10 s sleep (p.952) and Java sleeps 60 s for the function to be ready (p.931); shows IAM eventual consistency
- [from source] (LAMBDA p.925) .NET polls GetFunction until `State == Active`
- [p.944-945] Python: two example handlers (increment: only action 'increment' adds 1 to 'number'; calculator: actions plus/minus/times/divided-by with x and y, handles ZeroDivisionError, log level coming from the LOG_LEVEL env var)
- [p.945-946] Python packages the .zip in an in-memory buffer (zipfile); creates the role with AWSLambdaBasicExecutionRole (policy ARN `arn:aws:iam::aws:policy/service-role/`) and handles EntityAlreadyExists by reusing the role
- [from source] (LAMBDA p.943) PHP: lists functions paginating with NextMarker; cleanup deletes the function, role and S3 bucket used
- Common scenario pattern: read config (name, role, handler, zip bucket/key), create role, wait, create function, wait for Active, invoke, update code + env var, wait for Updated, invoke with logs, list, clean up. Differences: .NET (p.924-930) reads settings.json; Java (p.930-935) uses 60 s sleeps and Runtime JAVA8 on create / JAVA11 on config update (p.932-934); JS V3 (p.935-937) uses nodejs16x arm64; Kotlin (p.937-940) Java8/Java11; PHP (p.940-943); Python (p.943-951); Ruby (p.951-955); ABAP (p.955-959).
- [p.934,940] [DATED] The Java example updates the runtime from JAVA8 to JAVA11 via UpdateFunctionConfiguration (Kotlin likewise)
- [from source] (LAMBDA p.959) Final list of APIs used by the scenario: CreateFunction, DeleteFunction, GetFunction, Invoke, ListFunctions, UpdateFunctionCode, UpdateFunctionConfiguration


## 5. Cross-service examples (p.960-966; Python/Java/JS)
- [from source] (LAMBDA p.960) COVID-19 REST API (fictional data): Python Boto3 + AWS Chalice defining routes in Lambda functions behind API Gateway, DynamoDB, table and role defined in a CloudFormation template; Chalice+CloudFormation package/deploy; CloudFormation cleans up
- [from source] (LAMBDA p.961) Lending library REST API: Chalice + API Gateway + Lambda + Aurora serverless (cluster managed via the RDS API) + Secrets Manager for database credentials; client uses the Requests package
- [p.961-962] Messenger with Step Functions: state machine reads records from a DynamoDB table, sends via SQS, integrates with Lambda (scan of unsent messages) through service integrations
- [from source] (LAMBDA p.962) Websocket chat: API Gateway V2 + Lambda (stores connections in DynamoDB and posts messages to the other participants)
- [from source] (LAMBDA p.963) Invoking Lambda from a browser (JS V2 and V3): a browser app updates a DynamoDB table via a function
- [p.963-964] API Gateway invoking Lambda: Java 2.x and JS V3 = function that scans DynamoDB for work anniversaries and sends SMS via SNS; Python = REST API with routing by HTTP method, data from query string/header/body and JSON response, grants API Gateway permission to invoke the function, cleans up resources
- [p.964-965] Step Functions invoking Lambdas in sequence (Java 2.x, JS V3; DynamoDB, SES)
- [p.965-966] Scheduled events: EventBridge with a cron expression invoking Lambda (Java, JS V3: birthday SMS; Python: registers the function as a target, grants EventBridge permission, prints CloudWatch Logs logs)
- [from source] (LAMBDA p.967) Page with only the footer/end of the examples chapter


## 6. RELEASES - "AWS Lambda releases" (p.968-979) -- proof of the edition
- [from source] (LAMBDA p.968) The table describes important changes to the guide SINCE MAY 2018; RSS available for notifications. The most recent entry is 2022-11-28 => (PDF) edition from late November 2022; nothing later is covered
Entries (date | change), newest to oldest:
- [from source] (LAMBDA p.968) 2022-11-28 | Lambda SnapStart: reduces startup time of Java functions without provisioning extra resources or complex optimizations [DATED]
- [from source] (LAMBDA p.968) 2022-11-18 | Node.js 18 runtime (Amazon Linux 2) [DATED]
- [from source] (LAMBDA p.968) 2022-07-01 | Condition key lambda:SourceFunctionArn: filters access to an AWS resource by the Lambda function ARN (see execution environment credentials) [DATED]
- [from source] (LAMBDA p.968) 2022-05-11 | Node.js 16 runtime (Amazon Linux 2) [DATED]
- [from source] (LAMBDA p.968) 2022-04-06 | Function URLs: dedicated HTTP(S) endpoints for functions [DATED]
- [from source] (LAMBDA p.968) 2022-03-16 | Test events shared in the console between IAM users of the same account [DATED]
- [from source] (LAMBDA p.968) 2022-03-11 | PrincipalOrgId in resource-based policies: grants permission to an AWS Organizations organization [DATED]
- [from source] (LAMBDA p.969) 2022-02-23 | .NET 6 runtime [DATED]
- [from source] (LAMBDA p.969) 2021-11-24 | Event filtering for Kinesis, DynamoDB and SQS sources [DATED]
- [from source] (LAMBDA p.969) 2021-11-19 | mTLS authentication for Amazon MSK and self-managed Apache Kafka [DATED]
- [from source] (LAMBDA p.969) 2021-09-29 | Graviton2 for functions with arm64 architecture [DATED]
- [from source] (LAMBDA p.969) 2021-08-16 | Python 3.9 runtime [DATED]
- [from source] (LAMBDA p.969) 2021-07-21 | New runtime versions for Node.js, Python and Java [DATED]
- [from source] (LAMBDA p.969) 2021-07-07 | Amazon MQ for RabbitMQ as an event source [DATED]
- [from source] (LAMBDA p.969) 2021-06-29 | SASL/PLAIN for self-managed Kafka [DATED]
- [from source] (LAMBDA p.970) 2021-05-24 | Lambda Extensions API: general availability (GA) of extensions [DATED]
- [from source] (LAMBDA p.970) 2021-03-02 | New Lambda console (redesign for performance and consistency) [DATED]
- [from source] (LAMBDA p.970) 2021-01-27 | Node.js 14 runtime (Amazon Linux 2) [DATED]
- [from source] (LAMBDA p.970) 2020-12-01 | Container images: functions defined as container images [DATED]
- [from source] (LAMBDA p.970) 2020-11-23 | Code signing: administrators configure functions to accept only signed code; Lambda verifies the signature and trust in the signer [DATED]
- [from source] (LAMBDA p.970) 2020-11-12 | Preview: Runtime Logs API (extensions subscribe to execution environment log streams) [DATED]
- [from source] (LAMBDA p.970) 2020-11-05 | Amazon MQ as an event source [DATED]
- [from source] (LAMBDA p.971) 2020-10-08 | Preview: Lambda Extensions API [DATED]
- [from source] (LAMBDA p.971) 2020-08-12 | Java 8 and custom runtimes on Amazon Linux 2 (AL2) [DATED]
- [from source] (LAMBDA p.971) 2020-08-11 | Amazon MSK as an event source [DATED]
- [from source] (LAMBDA p.971) 2020-08-10 | IAM condition keys specific to VPC settings (require VPC, restrict subnets/security groups) [DATED]
- [from source] (LAMBDA p.971) 2020-07-07 | Concurrency settings for Kinesis HTTP/2 consumers (enhanced fan-out): ParallelizationFactor, MaximumRetryAttempts, MaximumRecordAgeInSeconds, DestinationConfig, BisectBatchOnFunctionError [DATED]
- [from source] (LAMBDA p.971) 2020-06-18 | Batch window (MaximumBatchingWindowInSeconds) for Kinesis HTTP/2 consumers [DATED]
- [from source] (LAMBDA p.972) 2020-06-16 | Support for Amazon EFS file systems [DATED]
- [from source] (LAMBDA p.972) 2020-06-01 | AWS CDK sample apps (TypeScript) in the console [DATED]
- [from source] (LAMBDA p.972) 2020-03-31 | .NET Core 3.1.0 runtime [DATED]
- [from source] (LAMBDA p.972) 2020-03-23 | API Gateway HTTP APIs: expanded documentation + sample app with CloudFormation [DATED]
- [from source] (LAMBDA p.972) 2020-02-19 | Ruby 2.7 (ruby2.7), first Ruby runtime on Amazon Linux 2 [DATED]
- [from source] (LAMBDA p.972) 2020-02-18 | ConcurrentExecutions metric now for all functions, aliases and versions (previously only account level and functions with reserved concurrency) [DATED]
- [from source] (LAMBDA p.973) 2020-01-24 | Function states enforced for ALL functions: when connecting to a VPC, Lambda creates shared ENIs; during this you cannot update configuration or publish versions and, in some cases, invocation is affected; rolled out in phases [DATED]
- [from source] (LAMBDA p.973) 2020-01-20 | New reason codes: StateReasonCode (InvalidSubnet, InvalidSecurityGroup) and LastUpdateStatusReasonCode (SubnetOutOfIPAddresses, InvalidSubnet, InvalidSecurityGroup) [DATED]
- [from source] (LAMBDA p.973) 2019-12-03 | Provisioned concurrency for a version or alias: scales without latency fluctuation [DATED]
- [from source] (LAMBDA p.974) 2019-12-03 | Create a database proxy via the console: high concurrency without exhausting database connections [DATED]
- [from source] (LAMBDA p.974) 2019-11-26 | Percentiles in the duration metric [DATED]
- [from source] (LAMBDA p.974) 2019-11-25 | Increased concurrency for streams (DynamoDB/Kinesis): more than one batch per shard; function concurrency can reach 10x the number of shards [DATED]
- [from source] (LAMBDA p.974) 2019-11-25 | Function states: the function enters the pending state while Lambda provisions resources; shared ENI created immediately on VPC connection (better performance, may require adjusting automation) [DATED]
- [from source] (LAMBDA p.974) 2019-11-25 | Error-handling options for asynchronous invocation: limit retries and set the maximum event age [DATED]
- [from source] (LAMBDA p.975) 2019-11-25 | Error handling in stream sources: limit retries, maximum record age, split the batch before retrying, send failure records to a queue/topic [DATED]
- [from source] (LAMBDA p.975) 2019-11-25 | Destinations for asynchronous invocation: invocation records (event, context, response) go to an SQS queue, SNS topic, Lambda function or EventBridge event bus [DATED]
- [from source] (LAMBDA p.975) 2019-11-18 | Node.js 12, Python 3.8 and Java 11 runtimes [DATED]
- [from source] (LAMBDA p.975) 2019-11-18 | SQS FIFO queues as an event source (previously only standard queues) [DATED]
- [from source] (LAMBDA p.975) 2019-10-31 | Creating applications in the console: GA [DATED]
- [from source] (LAMBDA p.976) 2019-10-03 | Creating apps in the console (beta) with continuous delivery pipeline; choice of CodeCommit or GitHub [DATED]
- [from source] (LAMBDA p.976) 2019-09-03 | Performance improvement of functions in a VPC: ENI shared per security group+subnet combination; does not create ENIs when scaling; greatly improves startup [DATED]
- [from source] (LAMBDA p.976) 2019-08-29 | Batch window for DynamoDB and Kinesis: up to 5 minutes to accumulate a batch [DATED]
- [from source] (LAMBDA p.976) 2019-06-18 | Integration with CloudWatch Logs Insights on the monitoring page [DATED]
- [from source] (LAMBDA p.977) 2019-05-21 | Execution environment updated to Amazon Linux 2018.03 [DATED]
- [from source] (LAMBDA p.977) 2019-05-13 | Node.js 10 (nodejs10.x, Node 10.15), first runtime on Amazon Linux 2 [DATED]
- [from source] (LAMBDA p.977) 2019-04-25 | GetLayerVersionByArn API (uses the version ARN directly) [DATED]
- [from source] (LAMBDA p.977) 2018-11-29 | Ruby 2.5; Layers (libs/runtimes/dependencies separate from code, shareable with other accounts or everyone); Custom runtimes; Application Load Balancer as a trigger [DATED]
- [from source] (LAMBDA p.978) 2018-11-19 | Kinesis HTTP/2 consumers as a trigger; Python 3.7 [DATED]
- [from source] (LAMBDA p.978) 2018-11-16 | Maximum asynchronous invocation payload rises from 128 KB to 256 KB (same as the maximum SNS message) [DATED]
- [from source] (LAMBDA p.978) 2018-11-12 | AWS GovCloud (US-East) Region [DATED]
- [from source] (LAMBDA p.978) 2018-10-25 | AWS SAM topics moved to their own guide (SAM developer guide) [DATED]
- [from source] (LAMBDA p.978) 2018-10-11 | Applications page in the console (CloudFormation stack status, aggregate metrics, dashboards) [DATED]
- [from source] (LAMBDA p.978) 2018-10-10 | [DATED] Maximum configurable timeout rises from 5 min to 15 min
- [from source] (LAMBDA p.979) 2018-09-11 | PowerShell Core [DATED]
- [from source] (LAMBDA p.979) 2018-07-09 | .NET Core 2.1.0 [DATED]
- [from source] (LAMBDA p.979) 2018-07-05 | Updates via RSS [DATED]
- [from source] (LAMBDA p.979) 2018-06-28 | Amazon SQS as an event source; China (Ningxia) Region [DATED]


## 7. "Earlier updates" (before June 2018) (p.979-983)
- [from source] (LAMBDA p.979) The second table covers guide releases prior to June 2018
- [from source] (LAMBDA p.979) 2018-04-02 | Node.js 8.10 [DATED]
- [from source] (LAMBDA p.979) 2018-01-25 | Revision IDs on versions and aliases (conditional updates) [DATED]
- [from source] (LAMBDA p.979) 2018-01-15 | Go and .NET 2.0 runtimes [DATED]
- [from source] (LAMBDA p.979) 2017-11-30 | Console redesign + Cloud9 editor [DATED]
- [from source] (LAMBDA p.980) 2017-11-30 | Per-function concurrency limits (reserved concurrency) [DATED]
- [from source] (LAMBDA p.980) 2017-11-28 | Traffic shifting with aliases; Gradual code deployment via CodeDeploy [DATED]
- [from source] (LAMBDA p.980) 2017-11-09 China (Beijing) Region; 2017-08-11 SAM Local (now SAM CLI); 2017-06-22 Canada (Central); 2017-06-06 São Paulo; 2017-04-19 X-Ray support; 2017-03-28 Mumbai; 2017-03-22 Node.js 6.10; 2017-02-01 London [DATED]
- [from source] (LAMBDA p.980) 2016-12-03 | C# (.NET), Lambda@Edge (Preview), Dead Letter Queues and automated deploy of serverless apps [DATED]
- [from source] (LAMBDA p.981) 2016-11-30 Amazon Lex as an event source; 2016-11-21 US West (N. California); 2016-11-18 AWS SAM + environment variables; 2016-08-29 Seoul; 2016-06-23 Sydney and simplified console for creating a role; 2016-04-07 Node.js 4.3; 2016-03-14 Frankfurt; 2016-02-11 VPC support; 2015-11-04 runtime/execution environment updated [DATED]
- [from source] (LAMBDA p.982) 2015-10-08 | Versioning, Python, scheduled events (rate or cron) and maximum execution of 5 minutes [DATED]
- [from source] (LAMBDA p.982) 2015-07-14 DynamoDB Streams GA; 2015-07-09 invocation by REST clients via API Gateway and blueprints in the console [DATED]
- [from source] (LAMBDA p.983) 2015-06-15 Java; 2015-05-28 .zip package from an S3 object (same Region); 2015-04-09 Lambda GA with support for mobile backends, synchronous and asynchronous events and resource policies; 2014-11-13 initial preview of the guide [DATED]


## 8. Notes: what is dated, contradictions, gaps
- [from source] (LAMBDA p.968) Last entry 2022-11-28 (SnapStart); therefore the edition does NOT cover Python 3.10+/3.11/3.12, Node.js 20, response streaming, ARM in more regions, later quota changes etc. [extrapolation] (inference: everything after Nov/2022 is absent)
- [from source] (LAMBDA p.970) In "New Lambda console experience" the text references (p. 946) -- internal link to the table itself
- [from source] (LAMBDA p.968) Typo in the original: "with with Lambda SnapStart"
- [p.902,919,923] Typo in the ABAP code: "Rresource already exists"
- Dated in the examples: nodejs12.x (blank sample, p.883), nodejs16x, python3.8/3.9, ruby2.7, JAVA8/JAVA11, Dotnet6 (p.893-940) -- all old runtimes relative to today's date.
- Evolution of the maximum timeout: 5 min (Oct/2015, p.982) -> 15 min (Oct/2018, p.978).
- Evolution of the async payload: 128 KB -> 256 KB (Nov/2018, p.978).
- Not covered in this range: theoretical explanations (the content here is illustrative); current quotas; prices (only "standard charges apply").


# Languages: common pattern (Node.js baseline) and comparison table

> Pattern repeated across all languages and comparison.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the reference text is unaccented because the original reading notes were written that way.

## 2. COMMON PATTERN PER LANGUAGE (baseline: Node.js, pp.368-395)
Each language chapter repeats: (a) runtimes table (name, identifier, SDK, OS, architectures, deprecation); (b) create execution role (AWSLambdaBasicExecutionRole) and function in the console (identical step by step); (c) Handler; (d) .zip deployment; (e) Container image deployment; (f) Context; (g) Logging; (h) Errors; (i) Tracing (X-Ray). Below, the pattern as documented with Node.js; the following sections cover only the differences.
### 2.1 Runtimes table and prerequisites (Node.js, p.368)
- [from source] (LAMBDA p.368) [DATED] Node.js: nodejs18.x (SDK 3.188.0), nodejs16.x (2.1083.0), nodejs14.x (2.1055.0), nodejs12.x (2.1055.0; deprecation phase 1 on Mar 31, 2023); all Amazon Linux 2; x86_64 and arm64
- [from source] (LAMBDA p.368) Node 18 uses AWS SDK for JavaScript v3 (earlier: v2); there is a migration workshop
- [from source] (LAMBDA p.368) Execution role for development: trusted entity Lambda, permission AWSLambdaBasicExecutionRole (write logs to CloudWatch Logs), named lambda-role in the example; permissions can be added later
### 2.2 Create a function in the console (p.369) - same script in all languages
- [from source] (LAMBDA p.369) Steps: Create function; name my-function; runtime (Node.js 18.x in the example); existing role lambda-role; Test > event name test > Save changes > Test. The console creates index.js or index.mjs with handler "index.handler"; on save it generates a .zip automatically; outside the console you must create the deployment package
- [from source] (LAMBDA p.369) The console uses AWS Cloud9 as an in-browser IDE
- [from source] (LAMBDA p.369) Sample apps (guide repository): blank-nodejs (logging, env vars, X-Ray, layers, tests), nodejs-apig, rds-mysql, efs-nodejs, list-manager (Kinesis -> DynamoDB), error-processor
- [from source] (LAMBDA p.370) Every function has a log group in CloudWatch Logs; the runtime sends details of each invocation and the function's logs; if there is an error, Lambda formats it and returns it to the invoker
### 2.3 Node.js-specific initialization (pp.370-371)
- [from source] (LAMBDA p.370) Non-blocking event loop model: asynchronous init tasks are NOT guaranteed to finish before the invocation (e.g. fetching a parameter from Parameter Store may be null in the handler); ensure initialization is complete before the logic
- [from source] (LAMBDA p.370) Alternative: ES module with top-level await, outside the handler; awaiting every Promise makes async init finish before invocations, maximizing the effect of provisioned concurrency
- [from source] (LAMBDA p.370) ES modules: by default .js = CommonJS; ES module via "type": "module" in package.json (all .js) or the .mjs extension (only that file); .cjs is always CommonJS; they can be mixed
- [from source] (LAMBDA p.370) Node 14/16 load ES modules from the handler folder or a subfolder; from Node 18 on it searches NODE_PATH, allowing import of the built-in AWS SDK and loading ES modules from layers
### 2.4 Handler (pp.372-373) - pattern: handler = "file.function"
- [from source] (LAMBDA p.372) The handler is the method that processes events; when it returns, the environment is free for another event. The setting = file name + dot + exported method name (default index.handler)
- [from source] (LAMBDA p.372) Three arguments: event (JSON from the invoker converted to an object; structure varies by service), context, callback (non-async handlers only; receives Error and response; response compatible with JSON.stringify; Lambda waits for the event loop to empty)
- [from source] (LAMBDA p.372) Async handlers: return/throw for response/error (the async keyword is mandatory); with an asynchronous task, return the promise (resolve/reject sends response/error)
- [from source] (LAMBDA p.373) Libraries that return a promise: return it directly (e.g. s3.listBuckets().promise())
- [from source] (LAMBDA p.373) Non-async: execution continues until the event loop empties or the timeout; the response is only sent afterwards; on timeout it returns an error. context.callbackWaitsForEmptyEventLoop = false sends the response immediately and the pending timer is frozen, continuing on the NEXT invocation
### 2.5 .zip deployment (pp.374-376) - pattern for interpreted languages
- [from source] (LAMBDA p.374) Two package types: container image and .zip. The .zip carries code + dependencies; standard libs and the AWS SDK are already in the runtime
- [from source] (LAMBDA p.374) [DATED] .zip larger than 50 MB: uploading via S3 is recommended
- [from source] (LAMBDA p.374) Native libraries: build with sam build --use-container (Docker compatible with the Lambda environment); build for the function's architecture; POSIX permissions may need adjusting before zipping
- [from source] (LAMBDA p.375) No dependencies: zip function.zip index.js; aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip (UpdateFunctionCode API); prerequisites AWS CLI v2 + aws configure [DATED: CLI]
- [from source] (LAMBDA p.375) With dependencies: local Node version equal to the function's; npm install into node_modules; native libs -> Amazon Linux environment (or EC2); a newer SDK can be included to pin the version
- [from source] (LAMBDA p.376) zip -r function.zip . (the -r option for subfolders); the package can also contain executables and other resources
- [SOURCE ERROR] [from source] (LAMBDA p.375) Example output shows "Runtime": "nodejs12.x" while the table on p.368 lists nodejs18.x as the newest (outdated example)
### 2.6 Container image (pp.377-378) - pattern for all languages
- [from source] (LAMBDA p.377) AWS resources: (1) Lambda base images (runtime + components; one Dockerfile per image on GitHub); (2) open source Runtime Interface Clients (RIC), required with a community/private base image; (3) Runtime Interface Emulator (RIE) for local testing, already included in Lambda base images and custom runtime images; for others, download it
- [from source] (LAMBDA p.377) Flow: build image -> push to Amazon ECR -> create function or update code to deploy
- [from source] (LAMBDA p.378) [DATED] Node: tags 18, 16, 14, 12 (AL2); repository gallery.ecr.aws/lambda/nodejs; RIC: npm install aws-lambda-ric
- [from source] (LAMBDA p.378) Existing function: when rebuilding the image, redeploy via a code update
### 2.7 Context (p.379) - pattern
- [from source] (LAMBDA p.379) Method: getRemainingTimeInMillis() (ms remaining before timeout). Properties: functionName, functionVersion, invokedFunctionArn (indicates the version/alias used), memoryLimitInMB, awsRequestId, logGroupName, logStreamName, identity (cognitoIdentityId, cognitoIdentityPoolId; mobile apps), clientContext (client.installation_id, app_title, app_version_name, app_version_code, app_package_name, env.platform_version/platform/make/model/locale, Custom; mobile apps), callbackWaitsForEmptyEventLoop
- [from source] (LAMBDA p.379) callbackWaitsForEmptyEventLoop=false: responds when the callback runs; pending events run on the next invocation
### 2.8 Logging (pp.381-385) - pattern
- [from source] (LAMBDA p.381) Each function has a log group and one log stream per instance; the runtime sends details of each invocation and relays logs/output from the code. In Node: methods of the console object (log/info/warn) or any library that writes to stdout/stderr
- [from source] (LAMBDA p.381) Format: START RequestId ... Version; lines with timestamp, request ID and level (INFO/WARN); END; REPORT. The example prints process.env (AWS_LAMBDA_FUNCTION_VERSION, AWS_LAMBDA_LOG_GROUP_NAME, AWS_LAMBDA_LOG_STREAM_NAME, AWS_EXECUTION_ENV, AWS_LAMBDA_FUNCTION_NAME, PATH, NODE_PATH)
- [from source] (LAMBDA p.382) REPORT fields: RequestId, Duration (handler time), Billed Duration, Memory Size, Max Memory Used, Init Duration (first request only: function load + code outside the handler), XRAY TraceId, SegmentId, Sampled (traced requests only)
- [from source] (LAMBDA p.382) CloudWatch console: log group /aws/lambda/function-name; each log stream = one instance; appears when the function is updated and when new instances serve concurrency. To find the logs of a specific invocation, instrument with X-Ray (records the request and log stream in the trace); error-processor example
- [from source] (LAMBDA p.383) [DATED] CLI: aws lambda invoke --log-type Tail returns LogResult with up to 4 KB of logs in base64; decode with base64 -d (macOS: base64 -D); --query 'LogResult' --output text
- [p.383-384] get-logs.sh script: invoke, sed strips the quotes from the output, sleep 15 s (wait for logs to become available), aws logs get-log-events --limit 5 (returns nextForwardToken/nextBackwardToken); chmod 755 on Linux/macOS
- [from source] (LAMBDA p.385) Log groups are NOT deleted when the function is deleted; delete the group or configure retention so logs are not stored indefinitely
### 2.9 Errors (pp.386-389) - pattern
- [from source] (LAMBDA p.386) Exception in the code -> Lambda generates a JSON (errorType, errorMessage, trace/stack) that appears in the log and, in synchronous invocation, in the output. Example: ReferenceError "x is not defined"
- [from source] (LAMBDA p.386) Flow: Lambda validates the execution role's permissions, that the event is valid JSON, and the parameters; if it passes, it sends to an instance; the runtime converts the event into an object. On error it returns the exception type, message and HTTP code; correct handling depends on the type of app, audience and origin
- [from source] (LAMBDA p.387) Rules by status class: 2xx with an X-Amz-Function-Error header = runtime/function error (Lambda accepted the request and signals the error via the header); 4xx = error the client/service can fix (change the request, request permission, retry); 4xx except 429 generally indicate a problem with the request; 5xx = problem with Lambda or with the function's configuration/resources, may be temporary
- [from source] (LAMBDA p.387) Console: Test > New event > template > name and JSON > Save changes > Test; invokes synchronously and shows the result; details in Details; output also in X-Ray if tracing is active
- [from source] (LAMBDA p.387) CLI: the response is split into two documents: the CLI response at the prompt (with a FunctionError field if there was an error; e.g. "FunctionError": "Unhandled") and the function's response/error written to the output file (output.txt)
- [from source] (LAMBDA p.388) [DATED] Lambda records up to 256 KB of the error object in the function logs
- [from source] (LAMBDA p.388) Other services: the invoking service chooses the invocation type and retry (schedule, lifecycle event, user request); some invoke asynchronously and let Lambda handle errors, others retry or pass them to the user. API Gateway: Lambda API error rejecting the invocation -> 500; function runs but returns an error or wrong format -> 502; to customize, catch errors in code and format the response; X-Ray recommended to find the origin
### 2.10 X-Ray tracing (pp.390-395) - pattern
- [from source] (LAMBDA p.390) Two libraries for sending traces to X-Ray: AWS Distro for OpenTelemetry (ADOT) and the language's X-Ray SDK. ADOT is the PREFERRED method and is recommended for all new applications, but OpenTelemetry's flexibility can increase cold start latency; if you optimize for low latency and do not need telemetry correlation / configurable destinations, consider the X-Ray SDK
- [from source] (LAMBDA p.390) ADOT offers managed Lambda layers (no code changes; custom collector configuration possible); for Node add the managed ADOT JavaScript layer
- [from source] (LAMBDA p.390) X-Ray SDK for Node: add aws-xray-sdk-core to the dependencies
- [from source] (LAMBDA p.391) Instrument AWS SDK clients: AWSXRay.captureAWS(require('aws-sdk')); create clients outside the handler for reuse
- [from source] (LAMBDA p.391) The runtime sets AWS_XRAY_CONTEXT_MISSING=LOG_ERROR so the X-Ray SDK does not throw errors; for your own strategy, clear the variable and use setContextMissingStrategy in the code
- [p.391-392] Enable active tracing: console (Configuration > Monitoring and operations tools > Edit > X-Ray > Active tracing > Save); CLI update-function-configuration --tracing-config Mode=Active [DATED: CLI]
- [from source] (LAMBDA p.392) APIs: UpdateFunctionConfiguration, GetFunctionConfiguration, CreateFunction. The tracing mode is part of the version-specific configuration; it CANNOT be changed on a published version
- [from source] (LAMBDA p.392) IaC: CloudFormation AWS::Lambda::Function -> TracingConfig: Mode: Active; SAM AWS::Serverless::Function -> Tracing: Active
- [from source] (LAMBDA p.392) Permission: the console adds the permissions to the execution role when enabling tracing; otherwise add the AWSXRayDaemonWriteAccess policy
- [from source] (LAMBDA p.393) [DATED] X-Ray sampling: 1 request per second + 5% of additional ones; NOT configurable for Lambda functions
- [from source] (LAMBDA p.393) With active tracing Lambda records 2 segments per trace (2 nodes in the graph): origin AWS::Lambda (service) and AWS::Lambda::Function (your function)
- [from source] (LAMBDA p.394) Function subsegments: Initialization (only the first time on each instance), Invocation (handler), Overhead (runtime preparation for the next event). It is also possible to instrument HTTP clients, record SQL queries, custom subsegments with annotations/metadata
- [from source] (LAMBDA p.394) X-Ray pricing: free up to a limit in the Free Tier; above that, charges for trace storage and retrieval
- [p.394-395] Best practice: with the X-Ray SDK the package grows; put the runtime dependencies in a Lambda layer (SAM: AWS::Serverless::LayerVersion with CompatibleRuntimes); the layer is only updated when dependencies change and the function package contains only the code, reducing upload; requires a build change (blank-nodejs example)


## 10. COMPARISON TABLE ACROSS LANGUAGES (synthesis, only from what was read)
- Handler setting: Node = file.export (index.handler); Python = file.function (lambda_function.lambda_handler); Ruby = file.method (function.handler; class: source.Module::Class.method); Java = package.Class::method or package.Class (interface); Go = executable name (main); C# = Assembly::Namespace.Class::Method (top-level statements: assembly only); PowerShell = script (no signature) [pp.372, 412, 443, 468, 508, 541, 575]
- Handler arguments: Node (event, context, callback); Python (event, context); Ruby (event:, context:) named; Java (event, Context) via RequestHandler/RequestStreamHandler; Go (optional ctx + optional event, returns (TOut, error)); C# (input, optional ILambdaContext); PowerShell (variables $LambdaInput/$LambdaContext) [pp.372, 412, 443, 468-470, 509, 538, 575]
- Context: Node getRemainingTimeInMillis()/camelCase + callbackWaitsForEmptyEventLoop; Python/Ruby get_remaining_time_in_millis + snake_case (Ruby has deadline_ms); Java getters getX(); Go lambdacontext (Deadline); C#/PowerShell PascalCase properties with RemainingTime (TimeSpan) and Logger [pp.379, 424, 450, 481, 511, 552, 576]
- Dependency packaging: Node node_modules; Python pip --target/venv; Ruby bundle vendor/bundle; Java Gradle buildZip(lib/) or Maven Shade; Go compiled binary GOOS=linux; C# dotnet lambda/Toolkit; PowerShell #Requires + cmdlets | KEY (common): "50 MB"
- arm64 architecture: runtimes on Amazon Linux 2 generally support x86_64 and arm64 (Node, Python 3.8/3.9, Ruby 2.7, Java 11/8.al2, .NET 3.1/6), but python3.7, java8, go1.x and dotnet5.0 only x86_64 [DATED; pp.368, 410, 440, 465, 506, 536]
- RIC per language (container, non-AWS base): npm aws-lambda-ric; pip awslambdaric; gem aws_lambda_ric; Maven aws-lambda-java-runtime-interface-client; Go included in aws-lambda-go; .NET download from GitHub [pp.378, 423, 448, 480, 519, 551]
- Observability: logging via print/console/puts/System.out/fmt/Console/Write-Host (any output to stdout/stderr); tracing: ADOT (Node, Python, Java, Go) vs. X-Ray SDK only (Ruby, C#); PowerShell has no tracing page [pp.390, 435, 460, 496, 531, 563]
- Cold start (optimizations cited): SnapStart (Java 11), top-level await + provisioned concurrency (Node ES modules), PublishReadyToRun and source generation (C#), Native AOT (.NET 7 on provided.al2), AWSPowerShell.NetCore >= 3.3.270.0 (PowerShell), class preloading (Java), ADOT can increase cold start [pp.353, 370, 539-540, 568, 575, 390]


## 11. GENERAL GAPS OF THE BLOCK (the text does NOT cover)
- There is no list of Regions/ARM/memory limits for SnapStart beyond what is cited; no real-gain metrics; no SnapStart coverage for other runtimes (java11 only).
- Python: no coverage of async/threading or versions 3.10+; Node: no explanation of AWS SDK v3 beyond the migration note; Go: no coverage of provided.al2023/arm64 beyond provided.al2; Ruby: no layers/ADOT.
- Runtime tables reflect the 2022 edition (Node 18, Python 3.9, .NET 6/7, Java 11): they do not include later versions.
- Note: the 2xx/4xx/5xx status, console and CLI sections repeat identically in all languages (documented once in 2.9).


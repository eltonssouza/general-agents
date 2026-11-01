# Languages: differences per runtime

> TypeScript, Python, Ruby, Java, Go, C#/.NET, PowerShell.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the reference text is unaccented because the original reading notes were written that way.

## 3. TypeScript (pp.396-409) - differences from Node.js
- [from source] (LAMBDA p.396) TypeScript runs on the Node.js runtime (same runtimes table); Node does not run TS natively: transpile to JavaScript and deploy the .js files. TS code cannot be authored in the Lambda console (use a local IDE, editor or Cloud9)
- [from source] (LAMBDA p.396) Compilers: esbuild or tsc; AWS SAM and AWS CDK simplify build/deploy and both use esbuild
- [from source] (LAMBDA p.396) esbuild caveats: there are TypeScript caveats; set the transpilation target to the chosen Node version; esbuild does NOT type-check - use tsc --noEmit (or "noEmit" in tsconfig) to check and then esbuild to convert
- [from source] (LAMBDA p.397) Example tsconfig [DATED]: target es2020, strict, noEmit, module commonjs, moduleResolution node, esModuleInterop, isolatedModules; exclude node_modules and *.test.ts
- [from source] (LAMBDA p.398) TS handler: same three arguments; async/non-async same as Node; exported handler name in the example is lambdaHandler (SAM) / handler (CDK, esbuild); aws-lambda types: Context, APIGatewayEvent, APIGatewayProxyResult, APIGatewayProxyCallback
- [from source] (LAMBDA p.399) ANTI-PATTERN/recommendation: do not use the any type in the handler's arguments/return (loses checking). Generate types: sam local generate-event s3 put >> S3PutEvent.json + quicktype (npm i -g quicktype) OR @types/aws-lambda (npm install -D) and import S3Event
- [from source] (LAMBDA p.400) Three ways to deploy TS as .zip: SAM, CDK, AWS CLI + esbuild. CDK is recommended for users with moderate to high experience
- [from source] (LAMBDA p.400) SAM: [DATED] prerequisites AWS CLI v2, SAM CLI 1.39 or later, Node.js 14.x or later; esbuild support in public preview (breaking changes possible); sam init --app-template hello-world-typescript --runtime nodejs16.x --package-type Zip
- [from source] (LAMBDA p.401) SAM: sam build --beta-features (mandatory because it is a preview); sam deploy --guided; public API endpoint -> delete after testing with sam delete
- [p.401-402] CDK v2 [DATED]: cdk init app --language typescript; npm install -D @types/aws-lambda; NodejsFunction construct (aws-cdk-lib/aws-lambda-nodejs) + LambdaRestApi; cdk deploy
- [from source] (LAMBDA p.402) NodejsFunction convention: the handler is named "handler" and the file is <id>.<name>.ts in the same directory as the construct (e.g. hello-world.function.ts); it can be changed and esbuild parameters can be configured
- [p.403-404] CLI + esbuild: esbuild produces ONE JS file with all dependencies (the only one to go in the zip); scripts prebuild (rm -rf dist), build (esbuild index.ts --bundle --minify --sourcemap --platform=node --target=es2020 --outfile=dist/index.js), postbuild (zip -r index.zip index.js*); create-function --runtime nodejs16.x --handler index.handler --zip-file fileb://dist/index.zip
- [from source] (LAMBDA p.406) TS container: use Node.js base images; RIC required on community images; RIE for local testing; prerequisites AWS CLI v2, Docker, Node 14+; build with esbuild (build script)
- [from source] (LAMBDA p.406) Multi-stage Dockerfile: 1st stage (FROM public.ecr.aws/lambda/nodejs:16 as builder) transpiles; 2nd stage copies only JS and production dependencies to ${LAMBDA_TASK_ROOT}; CMD ["index.handler"] defines the handler. Steps: docker build; aws ecr get-login-password | docker login; aws ecr create-repository --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE; docker tag; docker push [DATED: CLI]
- [from source] (LAMBDA p.407) Update the function code: create a new image version and store it in ECR
- [from source] (LAMBDA p.408) Errors in TS: the error JSON references the compiled JS file (app.js), not the TS. To map: (1) generate a source map (esbuild --sourcemap); (2) include it in the deploy; (3) enable with NODE_OPTIONS=--enable-source-maps. Does NOT apply to Lambda@Edge (does not support environment variables)
- [from source] (LAMBDA p.408) SAM: Globals.Function.Environment.Variables.NODE_OPTIONS and esbuild Metadata with Sourcemap: true; p.409 CDK: bundling { minify, sourceMap: true } + environment NODE_OPTIONS; result shows app.ts:2:11
- [from source] (LAMBDA p.409) TS context, logging and tracing = the same as Node.js


## 4. Python (pp.410-439) - differences from the section 2 pattern
Note: logging (pp.426-430 minus the library part), errors (p.431-433 status/console/CLI/API Gateway text) and tracing (pp.435-439, structure) repeat the Node.js pattern LITERALLY (sections 2.8, 2.9, 2.10); below only what differs.
### 4.1 Runtimes and creation (pp.410-411)
- [from source] (LAMBDA p.410) [DATED] Python: python3.9 and python3.8 (AL2; x86_64 and arm64), python3.7 (Amazon Linux 1, x86_64 only); SDK boto3-1.20.32 / botocore-1.23.32; the table is continuously updated (see "Managing AWS SDKs in Lambda functions")
- [from source] (LAMBDA p.410) The console creates a single source file called lambda_function; same creation script (runtime Python 3.9)
- [from source] (LAMBDA p.411) Guide example: blank-python
### 4.2 Handler (pp.412-415)
- [from source] (LAMBDA p.412) General syntax: def handler_name(event, context): ... return some_value. Handler name = file + function; console default: lambda_function.lambda_handler (file lambda_function.py); change in Runtime settings > Edit
- [from source] (LAMBDA p.412) Two arguments (no callback): event (JSON document converted to an object; normally dict, also list, str, int, float or NoneType; the invoker defines the structure; AWS services define theirs) and context
- [from source] (LAMBDA p.413) Return value (optional): RequestResponse (synchronous) invocation returns the result serialized as JSON to the client (the console uses RequestResponse); object not serializable by json.dumps -> runtime error; returning None (implicit without return) -> the runtime returns null; Event (asynchronous) invocation -> value discarded
- [from source] (LAMBDA p.413) [DATED] In Python 3.9 and later Lambda includes the invocation's requestId in the error response
- [p.413-415] Examples: lambda_handler that returns a message from first_name/last_name (runtime python3.8); [from source] (LAMBDA p.414) function that reads the AWS_REGION environment variable and returns a response in statusCode/headers/body format (depends on a 200 response from the Invoke API); calculation function with logging (action "increment") using python3.6 in the text
### 4.3 .zip deployment (pp.416-419)
- [from source] (LAMBDA p.416) Same requirements as the Node .zip (50 MB -> S3; sam build --use-container for native libs; architecture; POSIX permissions)
- [from source] (LAMBDA p.416) [DATED] Python difference: before 3.9 Lambda did NOT run the __init__.py code of packages in the handler directory (or its parents); in 3.9+ it runs during initialization, and only when the environment is initialized (not on every invocation)
- [from source] (LAMBDA p.417) Runtime dependency = any package/module not shipped with the runtime. Python 3.8+: standard libraries (math, logging) and boto3 are already in the runtime (do not include). Lambda periodically updates Boto3; for full control of dependencies, package everything
- [from source] (LAMBDA p.417) No dependencies: zip my-deployment-package.zip lambda_function.py
- [from source] (LAMBDA p.418) With dependencies: pip install --target ./package requests; cd package; zip -r ../my-deployment-package.zip .; then cd .. and zip adding lambda_function.py at the zip root
- [from source] (LAMBDA p.419) Virtualenv: source myvenv/bin/activate; pip install; deactivate; zip -r from myvenv/lib/python3.8/site-packages; zip -g to add the code; [from source] (LAMBDA p.419) tip: the library may be in site-packages or dist-packages and in lib or lib64; use pip show to locate it
- [from source] (LAMBDA p.419) Deploy: console or UpdateFunctionCode CLI with the fileb:// prefix
### 4.4 Container (pp.421-423)
- [p.421-422] [DATED] Python base images: tags 3.9 and 3.8 (AL2), 3.7 (AL1); repository gallery.ecr.aws/lambda/python
- [from source] (LAMBDA p.422) With an AWS base image: copy the app and install dependencies; the local Python version must match the image's; files app.py and requirements.txt; Dockerfile FROM public.ecr.aws/lambda/python:3.8, pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" (dependencies next to the handler so the runtime finds them), COPY app.py, CMD ["app.handler"] (can be overridden outside the Dockerfile)
- [from source] (LAMBDA p.422) Alternative image: install the Python RIC (Alpine example on the AWS blog)
- [from source] (LAMBDA p.423) RIC: pip install awslambdaric
### 4.5 Context (pp.424-425)
- [from source] (LAMBDA p.424) Same information as Node, in snake_case: method get_remaining_time_in_millis; properties function_name, function_version, invoked_function_arn, memory_limit_in_mb, aws_request_id, log_group_name, log_stream_name, identity (cognito_identity_id, cognito_identity_pool_id), client_context (client.installation_id, app_title, app_version_name, app_version_code, app_package_name, custom = dict, env = dict from the AWS SDK). There is NO callbackWaitsForEmptyEventLoop
- [from source] (LAMBDA p.425) Also suggests the X-Ray SDK to identify critical paths
### 4.6 Logging (pp.426-430)
- [from source] (LAMBDA p.426) Log output: the print function or a logging library that writes to stdout/stderr
- [p.429-430] For more detailed logs use the logging module (logger = logging.getLogger(); logger.setLevel(logging.INFO)); the logger output includes level, timestamp and request ID, in the format [INFO] timestamp requestId message
### 4.7 Errors (pp.431-434)
- [from source] (LAMBDA p.433) Error example: KeyError with stackTrace ("stackTrace" field in Python, vs "trace"/"stack" in Node)
- [from source] (LAMBDA p.433) ERROR Runtime.ImportModuleError ("Unable to import module 'lambda_function'... _imaging from PIL"): caused by uploading via CLI a package with a C/C++ library (Pillow, numpy, pandas) compiled outside the Lambda environment; recommendation: sam build --use-container (Docker container with an environment similar to Lambda)
- [from source] (LAMBDA p.434) ERROR Runtime.MarshalError ("Unable to marshal response: Object of type AttributeError is not JSON serializable"): may come from the base64 mechanism used in the code (b64encode(...).decode("utf-8")) or from not sending the .zip as binary; recommendation: fileb:// option in create-function
- [CONTRADICTION] [from source] (LAMBDA p.431) The page summary lists "What's next? (p. 367)" - reference copied from the Node section (wrong printed page number)
### 4.8 Tracing (pp.435-439)
- [from source] (LAMBDA p.435) Libraries: ADOT or AWS X-Ray SDK for Python (aws-xray-sdk package); the managed ADOT Python layer works on arm64 and x86_64
- [from source] (LAMBDA p.436) Example requirements.txt: jsonpickle==1.3 and aws-xray-sdk==2.4.3 [DATED]; instrument AWS SDK clients with patch_all() from aws_xray_sdk.core (boto3 patch)
- [from source] (LAMBDA p.439) Dependencies layer: AWS::Serverless::LayerVersion (blank-python-lib, ContentUri package/., CompatibleRuntimes python3.8)


## 5. Ruby (pp.440-461) - differences
- [from source] (LAMBDA p.440) [DATED] Ruby: only ruby2.7 (SDK 3.1.0; AL2; x86_64, arm64); the note refers to the "Runtime deprecation policy" for the end of support of Ruby 2.5
- [from source] (LAMBDA p.441) The console creates lambda_function.rb; default handler lambda_function.lambda_handler; examples: blank-ruby and "Ruby Code Samples for AWS Lambda"
- [CONTRADICTION] [p.443-452] The handler example uses def handler(event:, context:) in function.rb (value function.handler) and the console says lambda_function.lambda_handler; the log example on p.452 shows AWS_Lambda_ruby2.5 and [p.445-446] update outputs show "Runtime": "ruby2.5" (outdated vs ruby2.7)
- [from source] (LAMBDA p.443) Ruby handler: method with NAMED (keyword) arguments: def handler(event:, context:). Setting = file + dot + method (function.handler). Handler in a class/module: source.LambdaFunctions::Handler.process (class method self.process)
- [from source] (LAMBDA p.443) event is a Ruby object: if the payload is JSON it becomes a Hash; otherwise it becomes a string. Static code outside the handler runs once per instance; create SDK clients/connections outside the handler for reuse. Each instance processes one event at a time; number of simultaneous instances = concurrency
- [from source] (LAMBDA p.444) .zip: same requirements as Node. Tool provided: AWS SDK for Ruby
- [from source] (LAMBDA p.445) No dependencies: zip function.zip function.rb + update-function-code with fileb://
- [p.445-446] With dependencies: install gems with Bundler into vendor/bundle (bundle config set --local path 'vendor/bundle'; bundle install); [from source] (LAMBDA p.446) gems stay in the project directory and vendor/bundle becomes the default; to install globally afterwards: bundle config set --local system 'true'; zip -r function.zip function.rb vendor
- [p.447-448] [DATED] Ruby base image: tag 2.7 (AL2); repo gallery.ecr.aws/lambda/ruby; [from source] (LAMBDA p.448) RIC: gem install aws_lambda_ric
- [from source] (LAMBDA p.448) Ruby Dockerfile: FROM public.ecr.aws/lambda/ruby:2.7; COPY app.rb and Gemfile to ${LAMBDA_TASK_ROOT}; ENV GEM_HOME=${LAMBDA_TASK_ROOT}; RUN bundle install; CMD ["app.LambdaFunction::Handler.process"]
- [from source] (LAMBDA p.450) Ruby context: get_remaining_time_in_millis, function_name, function_version, invoked_function_arn, memory_limit_in_mb, aws_request_id, log_group_name, log_stream_name, identity, client_context and **deadline_ms** (date/time of the timeout in Unix time in milliseconds - Ruby only)
- [from source] (LAMBDA p.451) Ruby logging: puts or any logger that writes to stdout/stderr; for detailed logs use the logger library (Logger.new($stdout)); output includes timestamp, process ID, level and request ID
- [from source] (LAMBDA p.456) Ruby error: TypeError example ("no implicit conversion of String into Integer") with errorType "Function<TypeError>" and a stackTrace field
- [p.457-459] Status 2xx/4xx/5xx, console, CLI, 256 KB, API Gateway 500/502: text identical to the pattern (section 2.9)
- [p.461-462] Ruby tracing: the opening text differs (does NOT mention ADOT; only X-Ray SDK for Ruby: gem aws-xray-sdk). To instrument AWS SDK clients: create the client in init code and then require 'aws-xray-sdk/lambda'
- [from source] (LAMBDA p.461) Example Gemfile [DATED]: aws-xray-sdk 0.11.4, aws-sdk-lambda 1.39.0, test-unit 3.3.5; [from source] (LAMBDA p.464) layer: blank-ruby-lib, CompatibleRuntimes ruby2.5 (outdated)
- [p.460-463] Sampling text (1 req/s + 5%), 2 segments per trace, Initialization/Invocation/Overhead subsegments, AWSXRayDaemonWriteAccess permission, Mode=Active, TracingConfig/Tracing: Active and layer: same as the pattern (section 2.10)
- [NOT COVERED - Ruby] No section on ES modules/async; no mention of SnapStart.


## 6. Java (pp.465-505...) - differences
### 6.1 Runtimes and creation (pp.465-466)
- [from source] (LAMBDA p.465) [DATED] Java: java11 (AL2; x86_64, arm64), java8.al2 (AL2; x86_64, arm64), java8 (Amazon Linux 1; x86_64 only). Amazon Linux environment with IAM role credentials (does not cite an SDK built into the table)
- [from source] (LAMBDA p.465) Libraries provided: aws-lambda-java-core (REQUIRED; handler interfaces and context object; the only one needed if you define your own input types), aws-lambda-java-events (input types for service events), aws-lambda-java-log4j2 (Log4j 2 appender that adds the request ID to the logs), AWS SDK for Java 2.0
- [from source] (LAMBDA p.466) The console creates a function with class Hello, handler example.Hello::handleRequest; since Java is compiled, you do not see/edit the code in the console (only configuration, invocation and triggers); updating code = creating a .zip/JAR deployment package
### 6.2 Handler (pp.468-470)
- [from source] (LAMBDA p.468) Example: class Handler implements RequestHandler<Map<String,String>, String> with handleRequest(event, context); uses context.getLogger() (LambdaLogger)
- [from source] (LAMBDA p.468) Handler formats: package.Class::method (full, e.g. example.Handler::handleRequest) and package.Class (short, for classes that implement a handler interface)
- [from source] (LAMBDA p.468) Init: when loading the handler the runtime runs static code and the class constructor; resources created in init stay in memory and are reused thousands of times; a logger and serializer created on the first request make the following ones much faster
- [from source] (LAMBDA p.469) Input types: Integer/Long/Double (number event), String (JSON string event with quotes), Type/Map<String,Type> (JSON object), List<...> (JSON array), InputStream (any JSON, bytes unmodified; you deserialize and write to the output), library types (aws-lambda-java-events)
- [from source] (LAMBDA p.469) Map<String,String> only works for flat events (string or number values); a field with an object as value does not deserialize and causes an error
- [from source] (LAMBDA p.469) Custom input type: deserializable POJO, mutable, default constructor and properties per field; keys without a property and properties missing from the event are discarded without error
- [from source] (LAMBDA p.470) Output: object or void; object with fields -> JSON; type that wraps a primitive -> textual representation
- [from source] (LAMBDA p.470) Two interfaces in aws-lambda-java-core: RequestHandler<I,O> (object types; built-in deserialization/serialization) and RequestStreamHandler (you use your own serialization: receives InputStream and OutputStream, returns void; example with Gson and BufferedReader/Writer). Benefit: simplifies configuration and validates the signature at compile time
- [from source] (LAMBDA p.471) Guide examples (Java): java-basic (handlers: Handler=Map<String,String>, HandlerInteger, HandlerList=List<Integer>, HandlerStream=InputStream/OutputStream, HandlerString, HandlerWeatherData=custom type; change the handler in the SAM template to test), java-events (API Gateway, SQS, Kinesis; aws-lambda-java-events 3.0.0+, no AWS SDK dependency), s3-java (thumbnails with the Java Class Library), example with API Gateway + DynamoDB + SNS
### 6.3 .zip/JAR deployment (pp.472-478)
- [from source] (LAMBDA p.472) Java package = .zip or JAR; same idea as the others. Libraries via Maven Central [DATED example versions]: aws-lambda-java-core 1.2.1, aws-lambda-java-events 3.11.0, aws-lambda-java-log4j2 1.5.1 (runtimeOnly in Gradle)
- [from source] (LAMBDA p.473) Create the package: compile code + dependencies into a single .zip/JAR; Gradle uses the Zip type; Maven uses the Maven Shade plugin. Recommendation: package dependencies in layers (manage independently, reuse across functions, share across accounts) to keep the package small
- [from source] (LAMBDA p.473) Console: Code source > Upload from > upload package > Save; also via API or SAM
- [p.473-474] Gradle: task buildZip(type: Zip) { from compileJava; from processResources; into('lib') { from configurations.runtimeClasspath } }; output in build/distributions; dependency libraries go into the zip's lib/ folder
- [from source] (LAMBDA p.474) Rule: Lambda loads JARs in Unicode alphabetical order; if several JARs in lib have the same class, the first wins; test-zip.sh script (unzip + zipinfo + uniq -c) to find duplicate classes. Example dependencies: AWS SDK BOM 2.10.73, gson 2.8.6, log4j 2.17.1 [DATED]
- [from source] (LAMBDA p.475) Maven: maven-shade-plugin 3.2.2 with createDependencyReducedPom=false, package phase, shade goal; mvn package produces a "shaded" JAR in target; with the aws-lambda-java-log4j2 appender it is mandatory to configure a transformer (PluginsCacheFileTransformer, maven-shade-plugin.log4j2-cachefile-transformer 2.13.0) that merges versions of the cache file present in the appender and in Log4j [DATED]
- [from source] (LAMBDA p.476) CLI: aws lambda update-function-code --function-name my-function --zip-file fileb://my-function.zip [DATED]
- [p.476-477] [DATED] A package larger than 50 MB can NOT be uploaded directly: upload to S3 (aws s3 cp) and use --s3-bucket/--s3-key; [from source] (LAMBDA p.477) this method supports packages up to 250 MB (unzipped)
- [from source] (LAMBDA p.477) SAM: template with AWS::Serverless::Function (CodeUri build/distributions/java-basic.zip; Handler example.Handler; Runtime java8; MemorySize 512; Timeout 10; Policies AWSLambdaBasicExecutionRole, AWSLambda_ReadOnlyAccess, AWSXrayWriteOnlyAccess, AWSLambdaVPCAccessExecutionRole; Tracing Active). deploy.sh: aws cloudformation package (uploads to S3, rewrites the template) + aws cloudformation deploy --capabilities CAPABILITY_NAMED_IAM (creates the stack the 1st time, updates afterwards) [DATED]
- [SOURCE ERROR] [p.476-477] examples use Runtime java8 while the table on p.465 highlights java11
### 6.4 Container (pp.479-480)
- [p.479-480] [DATED] Java base images: tags 11 (AL2), 8.al2 (AL2), 8 (AL1); repository gallery.ecr.aws/lambda/java
- [from source] (LAMBDA p.480) Java RIC: Maven dependency com.amazonaws:aws-lambda-java-runtime-interface-client 1.0.0 [DATED] (there is no pip/npm-style install command)
### 6.5 Context (pp.481-483)
- [from source] (LAMBDA p.481) Methods (getters): getRemainingTimeInMillis(), getFunctionName(), getFunctionVersion(), getInvokedFunctionArn(), getMemoryLimitInMB(), getAwsRequestId(), getLogGroupName(), getLogStreamName(), getIdentity(), getClientContext(), getLogger() (the function's logger object)
- [from source] (LAMBDA p.482) The Context interface is in aws-lambda-java-core and can be implemented for testing (TestContext with dummy values and a test logger). The guide example serializes the context to JSON in the log
- [from source] (LAMBDA p.483) All sample apps have a TestContext class; java-basic uses SLF4J and Log4J 2 for a logger that works in local tests
### 6.6 Logging (pp.484-490)
- [from source] (LAMBDA p.484) Output: methods of java.lang.System (System.out) or any logging module that writes to stdout/stderr; aws-lambda-java-core provides LambdaLogger (via context.getLogger()), which supports multiline logs
- [p.484-485] REPORT format and fields same as the pattern (e.g. Memory Size 512 MB, Init Duration 524.75 ms in the example); environment variables show _HANDLER, AWS_EXECUTION_ENV=AWS_Lambda_java8, AWS_LAMBDA_FUNCTION_MEMORY_SIZE
- [from source] (LAMBDA p.488) Security (Log4Shell): Lambda does NOT include Log4j2 in the managed runtimes or in the base images (so they are not affected by CVE-2021-44228, CVE-2021-45046, CVE-2021-45105); when the function includes a vulnerable Log4j2, Lambda applied a mitigation in the Java runtimes and base images: an extra log entry "Transforming ...JndiLookup" may appear and strings that reference the jndi mapper are replaced by "Patched JndiLookup::lookup()". Recommendation: update to the latest version; those who use aws-lambda-java-log4j2 should move to 1.5.0+ (Log4j2 2.17.0+) and redeploy [DATED: CVEs, versions]
- [p.488-489] Log4j 2 + SLF4J: Log4j = log levels and appenders; SLF4J = facade that lets you swap the library without changing code and is REQUIRED to capture logs from the SDK for Java. The aws-lambda-java-log4j2 appender adds the request ID (%X{AWSRequestId})
- [from source] (LAMBDA p.489) Example log4j2.xml: <Lambda> appender, PatternLayout "%d{yyyy-MM-dd HH:mm:ss} %X{AWSRequestId} %-5p %c{1} - %m%n", Root INFO; loggers software.amazon.awssdk WARN and software.amazon.awssdk.request DEBUG (log SDK calls)
- [from source] (LAMBDA p.490) Build: runtime dependencies on the Lambda appender and on the SLF4J adapter, implementation in Log4J 2 (log4j-api/core/slf4j18-impl [2.17.1,)); local tests have no context/Lambda logger or request ID for the appender. java-basic: TestLogger implements LambdaLogger with Log4j 2; logging libraries excluded from the build output for a small package
### 6.7 Errors (pp.491-)
- [from source] (LAMBDA p.491) Java runtime error: failure to deserialize the event (valid JSON but a different type from what the handler expects) -> errorType java.lang.RuntimeException "An error occurred during JSON parsing", with nested "cause" (UncheckedIOException -> Jackson InvalidFormatException); stackTrace field
- [from source] (LAMBDA p.492) How it works / 2xx 4xx 5xx: identical to the pattern (section 2.9). Example "Creating a function that returns exceptions": HandlerDivide (List<Integer>) throws a custom InputLengthException if the list does not have 2 numbers; requires InputLengthException.java in src
- [from source] (LAMBDA p.493) Serialized custom exception: errorMessage, errorType (e.g. java.lang.InputLengthException), stackTrace. RULE: InputLengthException is a RuntimeException; the RequestHandler interface does NOT allow checked exceptions; RequestStreamHandler allows throwing IOException. Arithmetic error in the same example: "/ by zero" -> java.lang.ArithmeticException
- [p.494-495] Console, CLI (FunctionError, 256 KB), other services (API Gateway 500/502): same as the pattern
- [from source] (LAMBDA p.495) java-basic includes HandlerDivide (runtime exception) and HandlerStream (RequestStreamHandler, checked IOException)
### 6.8 Java tracing (pp.496-500)
- [from source] (LAMBDA p.496) Difference: ADOT for Java offers TWO managed layers: (1) "ADOT Java (Auto-instrumentation Agent)" - transforms the code at startup to collect traces automatically; (2) "ADOT Java" - built-in instrumentation but requires a few manual code changes to initialize the OTel SDK
- [from source] (LAMBDA p.497) X-Ray SDK for Java via Gradle [DATED]: BOM aws-xray-recorder-sdk-bom 2.11.0 and AWS SDK BOM 2.15.0; libs aws-xray-recorder-sdk-core, -aws-sdk, -aws-sdk-instrumentor enable automatic instrumentation of AWS SDK for Java 2.x clients
- [p.497-499] Enable tracing (console/CLI/CFN/SAM), AWSXRayDaemonWriteAccess, sampling 1 req/s + 5%, 2 segments, Initialization/Invocation/Overhead subsegments, pricing: same as the pattern
- [from source] (LAMBDA p.500) Layer: blank-java-lib with CompatibleRuntimes java8 (holds AWS SDK + X-Ray SDK); the s3-java example shows automatic instrumentation of AWS SDK for Java 2.x clients

### 6.9 Eclipse and examples (pp.502-505)
- [from source] (LAMBDA p.502) Eclipse tutorial + Maven plugin (m2e) to package Java; the AWS Toolkit for Eclipse also creates and uploads the package. Simple Maven project (Group Id doc-examples, Artifact lambda-java-example, jar) [DATED]
- [p.503-504] Steps: add aws-lambda-java-core 1.2.1 (defines RequestHandler, RequestStreamHandler and Context); create class example.Hello; build with the "package" goal produces a .jar that is NOT yet the standalone jar; add maven-shade-plugin 3.2.2 and run the goals "package shade:shade"; [from source] (LAMBDA p.504) the final jar is in /target
- [from source] (LAMBDA p.505) Recommendation: for Java beginners start with java-basic; for event sources, java-events; both use a layer for dependencies (deploy in under 1 minute from the command line)
- [NOT COVERED - Java] There is no JVM memory/tuning table (only the SnapStart chapter), nor Java 17.


## 7. Go (pp.506-537...) - differences
### 7.1 Runtime and libraries (p.506)
- [from source] (LAMBDA p.506) [DATED] Go: only runtime go1.x (Amazon Linux 1, x86_64 only). Amazon Linux runtimes do not support arm64; for arm64 use the provided.al2 runtime
- [from source] (LAMBDA p.506) Libraries: AWS SDK for Go; github.com/aws/aws-lambda-go/lambda (programming model; invokes the handler); lambdacontext (access to the context); events (event types); cmd/build-lambda-zip (creates a .zip on Windows); blank-go example
### 7.2 Handler (pp.507-510)
- [from source] (LAMBDA p.507) A Go function = a Go executable: it must import aws-lambda-go/lambda, implement the handler AND a main() function that calls lambda.Start(HandleRequest) (mandatory; the opening brace { must be on the same line as the signature). Example: HandleRequest(ctx context.Context, name MyEvent) (string, error)
- [from source] (LAMBDA p.508) Naming: the handler setting is the EXECUTABLE NAME (e.g. handler "main" calls main() in the executable main); change in Runtime settings > Edit
- [from source] (LAMBDA p.509) Structured types: structs with json tags (`json:"..."`); [from source] (LAMBDA p.509) the event struct fields must be capitalized to be exported
- [from source] (LAMBDA p.509) RULES for a valid signature: handler is a function; 0 to 2 arguments (if 2, the first implements context.Context); 0 to 2 returns (if 1, it must be error; if 2, the second is error). Valid signatures: func(), func() error, func(TIn) error, func() (TOut, error), func(context.Context) error, func(context.Context, TIn) error, func(context.Context) (TOut, error), func(context.Context, TIn) (TOut, error); TIn/TOut compatible with encoding/json
- [from source] (LAMBDA p.509) Global state: global variables and the init() function (executed when the handler is loaded, as in standard Go programs); an instance NEVER handles several events simultaneously (example: lists S3 objects in init and counts invocations in invokeCount)
### 7.3 Context (pp.511-512)
- [from source] (LAMBDA p.511) Global variables of the lambdacontext package: FunctionName, FunctionVersion, MemoryLimitInMB, LogGroupName, LogStreamName; method Deadline (timeout time in Unix ms); properties InvokedFunctionArn, AwsRequestID, Identity, ClientContext
- [from source] (LAMBDA p.511) Access: if the handler receives context.Context, Lambda inserts information into the context's Value; import lambdacontext and use lambdacontext.FromContext(ctx) (e.g. lc.Identity.CognitoIdentityPoolID)
- [from source] (LAMBDA p.512) Timeout example: ctx.Deadline() minus 100 ms with time.After to finish before the timeout
### 7.4 .zip deployment (pp.513-517)
- [from source] (LAMBDA p.513) Go package = .zip containing the compiled executable
- [from source] (LAMBDA p.514) macOS/Linux: go get github.com/aws/aws-lambda-go/lambda; GOOS=linux GOARCH=amd64 go build -o main main.go (GOOS=linux guarantees compatibility even when compiling outside Linux); several files: go build main; optionally CGO_ENABLED=0 (stable binary for libc versions that differ between Lambda and other devices); POSIX permissions; zip main.zip main [DATED: CLI]
- [p.514-515] Windows: install git (on PATH); go.exe install github.com/aws/aws-lambda-go/cmd/build-lambda-zip@latest; set GOOS=linux, GOARCH=amd64, CGO_ENABLED=0 (cmd.exe set / PowerShell $env:) and use build-lambda-zip.exe -o main.zip main
- [p.515-516] Create the function via CLI: trust policy (lambda.amazonaws.com / sts:AssumeRole) in trust-policy.json; aws iam create-role --role-name lambda-ex; attach-role-policy AWSLambdaBasicExecutionRole; aws lambda create-function --runtime go1.x --handler main --zip-file fileb://main.zip; the handler is the executable name [DATED: CLI]
- [from source] (LAMBDA p.516) Go as a custom runtime: Lambda treats Go differently from native runtimes; provided.al2 and sam build can be used
- [from source] (LAMBDA p.517) SAM for provided.al2: Runtime provided.al2, any Handler (my.bootstrap.file in the example), Architectures [arm64] (remove for x86_64), Metadata BuildMethod: makefile; makefile: GOOS=linux go build -o bootstrap + cp to $(ARTIFACTS_DIR); the executable is called bootstrap
### 7.5 Container (pp.518-521)
- [from source] (LAMBDA p.518) [DATED] Go base image: tag 1 (Go 1.x, Amazon Linux 1); repository gallery.ecr.aws/lambda/go
- [from source] (LAMBDA p.519) There is NO separate RIC for Go: the aws-lambda-go/lambda package already includes the runtime interface implementation
- [from source] (LAMBDA p.519) Image on provided.al2: multi-stage Dockerfile (FROM public.ecr.aws/lambda/provided:al2 as build; yum install golang; go build -o /main; copy to a clean image; ENTRYPOINT ["/main"]); the provided.al2 image includes the RIE; steps 1-3 identical to .zip
- [from source] (LAMBDA p.520) Alternative image (alpine): same multi-stage pattern; to have the RIE in the image: ADD the aws-lambda-rie into /usr/bin + an entry.sh script that uses the RIE when AWS_LAMBDA_RUNTIME_API is not defined
- [from source] (LAMBDA p.521) Local test without embedding the RIE: download the RIE to ~/.aws-lambda-rie; docker run ... -p 9000:8080 --entrypoint /aws-lambda/aws-lambda-rie ...; invoke with curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}' [DATED: port 9000, path 2015-03-31]
### 7.6 Go logging (pp.522-526)
- [from source] (LAMBDA p.522) Output: methods of the fmt package or any library that writes to stdout/stderr; the example uses the log package (log.Printf with os.Environ()); timestamp in the Go log standard (e.g. 2020/03/27 03:40:05)
- [from source] (LAMBDA p.523) REPORT and flow: same as the pattern; AWS_EXECUTION_ENV=AWS_Lambda_go1.x
### 7.7 Go errors (pp.527-530)
- [from source] (LAMBDA p.527) Custom errors in Go require importing the errors package; a handler that returns error (errors.New("something went wrong!")) produces JSON {errorMessage, errorType: "errorString"} (only two fields; no stack trace)
- [p.528-530] Validation flow, 2xx/4xx/5xx, console, CLI (FunctionError "Unhandled"), other services (API Gateway 500/502): same as the pattern (2.9). Here the CLI page does not show the content of output.txt

### 7.8 Go tracing (pp.531-535)
- [from source] (LAMBDA p.531) ADOT (managed ADOT Go layer) or X-Ray SDK for Go (go get github.com/aws/aws-xray-sdk-go); same recommendation, ADOT preferred vs. cold start
- [from source] (LAMBDA p.532) Instrument AWS SDK clients: xray.AWS(svc.Client) and use the WithContext versions of the methods (e.g. ListBucketsWithContext) to trace
- [p.532-534] Console/CLI/CFN/SAM, permission, sampling 1 req/s + 5%, 2 segments, subsegments and pricing: same as the pattern (2.10). Note: the Go page does NOT have a "dependencies layer" section
### 7.9 Environment variables (p.535)
- [from source] (LAMBDA p.535) In Go use os.Getenv (os package); list of variables defined by the runtime in "Defined runtime environment variables"


## 8. C# / .NET (pp.536-...) - differences
### 8.1 Runtimes and libraries (p.536)
- [from source] (LAMBDA p.536) [DATED] .NET: dotnetcore3.1 (AL2; x86_64 and arm64; deprecation phase 1 on Mar 31, 2023), dotnet6 (AL2; x86_64, arm64), dotnet5.0 (AL2; x86_64 only). Note on the end of support of .NET Core 2.1 in the "Runtime deprecation policy"
- [from source] (LAMBDA p.536) NuGet libraries: Amazon.Lambda.Core (static logger, serialization interfaces, context), Amazon.Lambda.Serialization.Json (serialization implementation), Amazon.Lambda.Logging.AspNetCore, and event POCOs (APIGatewayEvents, CognitoEvents, ConfigEvents, DynamoDBEvents, KinesisEvents, S3Events, SQSEvents, SNSEvents). Examples: blank-csharp, ec2-spot
### 8.2 Handler (pp.538-544)
- [from source] (LAMBDA p.538) Handler = instance or static method in a class; optional context via an ILambdaContext parameter (second argument). Syntax: returnType handler-name(inputType input, ILambdaContext context)
- [from source] (LAMBDA p.538) Return rule: synchronous (RequestResponse) can return any supported type, serialized to JSON; asynchronous (Event; e.g. S3, SNS) -> void return
- [from source] (LAMBDA p.538) By default Lambda only supports System.IO.Stream as an input parameter without a serializer
- [from source] (LAMBDA p.539) Types that require a serializer: .NET primitives, collections/maps, POCOs, AWS event types. In asynchronous invocation the return is ignored; async -> Task / Task<T> with async/await. Default serializers applicable at the assembly or method level, or implement ILambdaSerializer; dependency Amazon.Lambda.Serialization.SystemTextJson in the .csproj [DATED example versions: Core 2.1.0, SystemTextJson 2.2.0]; csproj with PublishReadyToRun=true to improve cold start (ready to run images)
- [p.539-540] Different serializers per method can be used with the [LambdaSerializer(typeof(...))] attribute
- [from source] (LAMBDA p.540) Source generation (C# 9 / .NET 6+): System.Text.Json can use source generators, parsing JSON without reflection, which helps cold start performance. Steps: empty partial class derived from JsonSerializerContext; JsonSerializable attribute for each type; register with [assembly: LambdaSerializer(typeof(SourceGeneratorLambdaJsonSerializer<...>))]
- [from source] (LAMBDA p.541) Handler format: ASSEMBLY::TYPE::METHOD (Assembly::Namespace.ClassName::MethodName). ASSEMBLY = the .csproj name if AssemblyName was not defined; e.g. HelloWorldApp::Example.Hello::MyHandler. RULE: if the method is overloaded, give the exact signature; if there is ambiguity Lambda rejects it even with a valid signature
- [p.541-542] Top-level statements (.NET 6+): use LambdaBootstrapBuilder.Create(handler).Build().RunAsync(); handler string = only the ASSEMBLY name (Lambda treats the assembly as an executable); requires the Amazon.Lambda.RuntimeSupport package
- [from source] (LAMBDA p.542) Serialization: SystemTextJson (native, better performance than Json, .NET Core 3.1+, with Microsoft's limitations), Amazon.Lambda.Serialization.Json (JSON.NET), or your own via ILambdaSerializer (Deserialize<T>(Stream) / Serialize<T>(T, Stream)); declare in AssemblyInfo.cs with [assembly: LambdaSerializer(typeof(DefaultLambdaJsonSerializer))]; an attribute on the method overrides the assembly's
- [from source] (LAMBDA p.543) Handler RESTRICTIONS: cannot be unsafe with pointers in the signature; cannot use params or ArgIterator; cannot be a generic method; async void is NOT supported
- [p.543-544] Async: for long processes (S3 upload, reading a DynamoDB stream) use async/await; Lambda invokes synchronously and waits for the response or the timeout. ANTI-PATTERN: async without await (compiler warning; some actions do not complete before the invocation ends). With several tasks, use Task.WhenAll/WhenAny: omitting a task from the array can return before it finishes; WhenAny returns as soon as the first one finishes
### 8.3 .zip deployment (pp.545-549)
- [from source] (LAMBDA p.545) .NET package = compiled assembly + dependencies + proj.deps.json + proj.runtimeconfig.json (NOT included by default because the project is a class library; force with /p:GenerateRuntimeConfigurationFiles=true). The .NET Core CLI or AWS Toolkit for Visual Studio (optimize the package and remove non-Linux dependencies) is recommended over manual dotnet publish
- [p.545-546] CLI: dotnet new -i Amazon.Lambda.Templates; dotnet new lambda.EmptyFunction --name MyFunction (options --name, --profile, --region saved in aws-lambda-tools-defaults.json)
- [from source] (LAMBDA p.546) aws-lambda-tools-defaults.json [DATED example]: configuration Release, function-runtime dotnet6, function-memory-size 256, function-timeout 30, function-handler "MyFunction::MyFunction.Function::FunctionHandler"
- [from source] (LAMBDA p.548) Deploy: dotnet tool install -g Amazon.Lambda.Tools (update with dotnet tool update -g); dotnet lambda deploy-function MyFunction --function-role role; dotnet lambda invoke-function MyFunction --payload ...; tests with xUnit and TestLambdaContext (Amazon.Lambda.TestUtilities)
- [p.548-549] AWS Toolkit for Visual Studio: Lambda Project (.NET Core) / blueprints; Publish to AWS Lambda; when renaming Assembly/Namespace/Class/Function update function-handler in the JSON. Advanced options: Role Name (required), Environment, Memory 128 MB to 10,240 MB in 1 MB steps, Timeout default 3 s and maximum 900 s, VPC, DLQ, active tracing [DATED: 128-10240 MB; 3 s; 900 s]
### 8.4 .NET container (pp.550-551)
- [p.550-551] [DATED] .NET base images: x86_64 for all supported runtimes and arm64 only for .NET Core 3.1 and .NET 6; tags core3.1 (deprecation Mar 31, 2023), 6, 5.0 (all AL2); repository gallery.ecr.aws/lambda/dotnet
- [from source] (LAMBDA p.551) .NET RIC: download from the AWS Lambda for .NET Core GitHub repository (no package manager cited)
### 8.5 Context (p.552)
- [from source] (LAMBDA p.552) ILambdaContext is PROPERTIES only (no method): FunctionName, FunctionVersion, InvokedFunctionArn, MemoryLimitInMB, AwsRequestId, LogGroupName, LogStreamName, RemainingTime (TimeSpan), Identity, ClientContext, Logger. (The text says "RemainingTime ... number of milliseconds" but the type is TimeSpan)
### 8.6 C# logging (pp.553-557)
- [from source] (LAMBDA p.553) Output: methods of the Console class, or LambdaLogger (Amazon.Lambda.Core), or a library that writes to stdout/stderr; AWS_EXECUTION_ENV=AWS_Lambda_dotnet6
- [from source] (LAMBDA p.554) Log levels (from .NET 6): LogCritical, LogError, LogWarning, LogInformation, LogDebug, LogTrace; allow filtering and categorization
- [from source] (LAMBDA p.555) By default it writes LogInformation and above; adjust with the AWS_LAMBDA_HANDLER_LOG_LEVEL variable (value = LogLevel enum name; e.g. Error writes LogError and LogCritical). Console.WriteLine -> info level; Console.Error.WriteLine -> error level; AWS_LAMBDA_HANDLER_LOG_FORMAT=Unformatted restores the old style
- [SOURCE ERROR] [from source] (LAMBDA p.554) It says the level logs are written to "Amazon EventBridge (CloudWatch Events)" - the rest of the guide uses CloudWatch Logs
- [p.553-557] REPORT, CLI --log-type Tail (4 KB), get-logs.sh, retention: same as the pattern
### 8.7 C# errors (pp.558-...)
- [from source] (LAMBDA p.558) Exceptions in the init phase (invalid handler string, type/method that violates the restrictions, missing serializer attribute with a POCO) are of type LambdaException ("The valid format is 'ASSEMBLY::TYPE::METHOD'"); an exception in the constructor is also a LambdaException with the cause in "cause" (TargetInvocationException -> original exception)
- [from source] (LAMBDA p.559) Exceptions during invocation preserve the type and are returned as payload and in CloudWatch Logs; inner causes (cause field) are always preserved and can be deeply nested (e.g. AggregateException -> UnknownWebException -> WebException -> HttpRequestException -> CurlException)
- [from source] (LAMBDA p.560) RULE by invocation type: RequestResponse (synchronous) -> the error message goes back to the caller (the console always uses RequestResponse and shows it in "Execution result"); Event (asynchronous) -> Lambda returns nothing, records the error in CloudWatch Logs and in CloudWatch metrics
- [p.560-562] 2xx/4xx/5xx, console, CLI (256 KB), API Gateway 500/502: same as the pattern
### 8.8 C# tracing (pp.563-567)
- [from source] (LAMBDA p.564) Opening text like Ruby's: does NOT cite ADOT; only X-Ray SDK for .NET (add AWSXRayRecorder packages to the .csproj); sampling 1 req/s + 5%; 2 segments; subsegments; AWSXRayDaemonWriteAccess; pricing: same as the pattern
- [p.564-565] Example .csproj [DATED]: AWSXRayRecorder.Core 2.6.2, AWSXRayRecorder.Handlers.AwsSdk 2.7.2, targetframework netcoreapp3.1; instrument AWS SDK clients by calling AWSSDKHandler.RegisterXRayForAllServices() in the init code
- [p.566-567] Enable tracing via API (--tracing-config Mode=Active), does not change on a published version, CFN TracingConfig, SAM Tracing: same as the pattern. Note: the C# page does NOT have the dependencies layer section
### 8.9 Native AOT (.NET 7) (pp.568-570)
- [from source] (LAMBDA p.568) [DATED] .NET 7 supports native ahead-of-time (AOT) compilation: compiles the function code to native format, eliminates .NET compilation at runtime and can reduce cold start; there are feature limitations (Microsoft docs)
- [from source] (LAMBDA p.568) Prerequisites: compile on the SAME OS the code runs on -> outside Amazon Linux 2 Docker is required; install the .NET 7 SDK (not just the runtime); Amazon.Lambda.Tools (dotnet tool install -g) and Amazon.Lambda.Templates (dotnet new install)
- [from source] (LAMBDA p.569) [DATED] Deploy with the provided.al2 custom runtime on the x86_64 architecture; the environment does not include the .NET SDK or runtime (the JIT is not used, the code is already machine code). Create the project: dotnet new lambda.NativeAOT; deploy: dotnet lambda deploy-function (downloads an AL2 Docker image to compile, generates the .zip). Docker must be running on Windows/macOS
- [p.569-570] Complex types: generate serialization code at compile time (JsonSerializable on the custom serializer); API Gateway example: Amazon.Lambda.ApiGatewayEvents package + APIGatewayHttpApiV2ProxyRequest/Response
- [from source] (LAMBDA p.570) Troubleshooting: (1) "Cross-OS native compilation is not supported" = outdated Amazon.Lambda.Tools -> update; (2) Docker "image operating system "linux" cannot be used on this platform" = Docker in Windows containers mode -> switch to Linux containers; (3) "serializer ... is missing a constructor that takes in JsonSerializerOptions" -> add an rd.xml file and redeploy


## 9. PowerShell (pp.571-585) - differences
- [from source] (LAMBDA p.571) Same runtimes table as .NET (dotnetcore3.1, dotnet6, dotnet5.0) [DATED]; PowerShell runs on .NET (PowerShell Core); blank-powershell example; first set up the PowerShell development environment
- [from source] (LAMBDA p.572) AWSLambdaPSCore module with cmdlets: Get-AWSPowerShellLambdaTemplate (lists templates), New-AWSPowerShellLambda (creates the initial script from a template), Publish-AWSPowerShellLambda (publishes the script to Lambda), New-AWSPowerShellLambdaPackage (generates a package for CI/CD)
- [from source] (LAMBDA p.573) PowerShell package = script + required PowerShell modules + assemblies to host PowerShell Core. Script: Get-AWSPowerShellLambdaTemplate (e.g. Basic, CodeCommitTrigger); New-AWSPowerShellLambda -ScriptName MyFirstPSScript -Template Basic (generates .ps1; -Directory optional); the script predefines $LambdaInput and $LambdaContext; modules via "#Requires -Modules @{ModuleName=...; ModuleVersion=...}"
- [from source] (LAMBDA p.574) Publish: Publish-AWSPowerShellLambda -ScriptPath .\MyFirstPSScript.ps1 -Name MyFirstPSScript -Region us-east-2 (-Name = function name); invoke with aws lambda invoke --function-name MyFirstPSScript out
- [from source] (LAMBDA p.575) PowerShell handler: there is no function signature - Lambda runs the script; predefined variables $LambdaInput (PSObject with the input) and $LambdaContext (Amazon.Lambda.Core.ILambdaContext)
- [from source] (LAMBDA p.575) RULE: #Requires is mandatory to declare dependent modules (documents and tells the tooling what to package). When using AWS cmdlets, reference AWSPowerShell.NetCore (PowerShell Core) and NOT AWSPowerShell (Windows PowerShell only); use version 3.3.270.0 or newer (optimizes import; older versions = longer cold start) [DATED: 3.3.270.0]
- [from source] (LAMBDA p.575) Return: the LAST object added to the pipeline is the return; if it is a string, it is returned as is; otherwise it is converted with ConvertTo-Json (e.g. $PSVersionTable)
- [from source] (LAMBDA p.576) Context via $LambdaContext: properties same as C# (FunctionName, FunctionVersion, InvokedFunctionArn, MemoryLimitInMB, AwsRequestId, LogGroupName, LogStreamName, RemainingTime, Identity, ClientContext, Logger); e.g. $LambdaContext.RemainingTime.TotalMilliseconds
- [p.577-578] Logging: cmdlets from Microsoft.PowerShell.Utility (e.g. Write-Host) or a module that writes to stdout/stderr; output appears as "[Information] - ..."; AWS_EXECUTION_ENV=AWS_Lambda_dotnet6_powershell_1.0.0; REPORT example with high Init Duration (5960.19 ms, 512 MB) illustrates PowerShell cold start
- [p.577-581] REPORT, console, CLI 4 KB, get-logs.sh, retention: same as the pattern (text says ".NET runtime logs...")
- [from source] (LAMBDA p.582) PowerShell errors: throw 'message' produces a terminating error with errorType "RuntimeException" (default); custom type: throw @{'Exception'='AccountNotFound';'Message'='The Account is not found'} -> errorType AccountNotFound; without a message: throw 'AccountNotFound' (error code format: starts with a character and then only letters and digits, no spaces/symbols) -> errorMessage and errorType are equal
- [p.583-585] Status 2xx/4xx/5xx, console, CLI, 256 KB, API Gateway 500/502: same as the pattern. The PowerShell page has NO container image or tracing sections of its own (refers to "Using AWS Lambda with AWS X-Ray")
- [NOT COVERED - PowerShell] There is no container image deployment for PowerShell in this block; no base images; no X-Ray SDK of its own.



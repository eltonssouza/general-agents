# Integrated services (push events)

> Integration with API Gateway, S3, SNS, EventBridge, CloudTrail, ALB, etc.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the reference text is unaccented because the original reading notes were written that way.

## Invocation models (overview)
- [from source] (LAMBDA p.586) Integrations work in two ways: the service generates an event that invokes the function, or Lambda polls a queue/stream and invokes the function; EFS and X-Ray are integrations that do not involve invoking functions
- [from source] (LAMBDA p.587) Service -> method table. Polling: MSK, self-managed Kafka, DynamoDB, Kinesis, Amazon MQ, SQS. Synchronous event: Alexa, API Gateway, CloudFront (Lambda@Edge), Cognito, Connect, ALB, Kinesis Data Firehose, Lex, S3 Batch, Secrets Manager. Asynchronous event: CloudFormation, EventBridge/CloudWatch Events, CloudWatch Logs, CodeCommit, CodePipeline, Config, IoT, IoT Events, SES, SNS, S3. Special integration: EFS, X-Ray
- [from source] (LAMBDA p.588) Event-driven: you grant the generating service permission to invoke the function in the resource-based policy and configure the service to generate events; the event is a JSON whose structure varies by service
- [from source] (LAMBDA p.588) Synchronous: the source service waits for the response, defines the return format and controls the error strategy (retry or not). Asynchronous: Lambda queues the event, immediately responds with success to the source service and does not return a response after processing
- [from source] (LAMBDA p.588) Polling: you create an event source mapping; the permission granted is Lambda's to access the other service, via the execution role (Lambda reads, creates the event and invokes)
- [from source] (LAMBDA p.590) With stream-based sources, Lambda reads items and invokes the function synchronously; there is NO need to grant Lambda permission to invoke the function, but it needs read permission on the stream. APIs: CreateEventSourceMapping/UpdateEventSourceMapping
- [from source] (LAMBDA p.589) Usage examples: S3 -> thumbnail; DynamoDB Streams -> aggregated metrics; API Gateway -> web backend; custom mobile app -> event processing
- [from source] (LAMBDA p.589) CONTRADICTION in the text: step 3 of the S3 example says S3 invokes "using the permissions provided by the execution role", but the next paragraph says S3's permission is granted by updating the function's resource-based policy (the latter is correct)


## Alexa (p.591)
- [from source] (LAMBDA p.591) Lambda can host Alexa skills via the Alexa Skills Kit (Java, Node.js, Python SDKs); the sample event is smart home (header/payload)


## API Gateway (p.592-611)
- [from source] (LAMBDA p.592) API Gateway exposes an HTTP endpoint for the function; APIs can be public or accessible only within the VPC; a proxy resource captures all paths below it; the ANY method captures all HTTP methods
- [from source] (LAMBDA p.592) Console: Add trigger > API Gateway > create API (HTTP API) or use an existing one; Security "Open"
- [from source] (LAMBDA p.593) Paths: /prod/ (stage prod, root), /prod/user, /dev/{proxy+}, and "/" for the default stage in HTTP APIs. Proxy integration wraps the entire request (headers, resource, path, method); custom integration passes only the body
- [from source] (LAMBDA p.593) API Gateway invokes the function SYNCHRONOUSLY; for proxy the event has a defined structure (REST: resource, path, httpMethod, headers, multiValueHeaders, queryStringParameters, pathParameters, stageVariables, body, isBase64Encoded, requestContext)
- [from source] (LAMBDA p.594) Proxy response: the function must return an object with statusCode, headers, multiValueHeaders, isBase64Encoded and body (string); in custom integration you define the integration response and method response
- [from source] (LAMBDA p.594) Permission: API Gateway invokes via a resource-based policy (principal apigateway.amazonaws.com, action lambda:InvokeFunction, conditions aws:SourceAccount and aws:SourceArn). The Lambda/API Gateway console and SAM update the policy automatically
- [from source] (LAMBDA p.595) Manual: AddPermission/RemovePermission/GetPolicy; CLI `aws lambda add-permission --principal apigateway.amazonaws.com --source-arn arn:aws:execute-api:REGION:ACCT:API/stage/METHOD/path`. If the API and function are in different Regions, the Region in the source ARN must be the FUNCTION's. Patterns: api/*/GET/*, api/prod/ANY/user, api/*/*/* [DATED: ARN format]
- [from source] (LAMBDA p.596) Errors: API Gateway treats all invocation/function errors as internal. Lambda API rejects the invocation -> 500; function runs but returns an error or a response in the wrong format -> 502; generic body {"message": "Internal server error"}. API Gateway does NOT retry Lambda invocations. To customize the error, catch it in the function and return a formatted response (statusCode, x-amzn-ErrorType header, body)
- [from source] (LAMBDA p.597) API types: HTTP API (lightweight, low latency, API Gateway v2; automatic deployment, $default stage, configurable CORS), REST API (more customization: custom integration with transform template, more auth options, X-Ray and additional logging), WebSocket API (persistent full-duplex connection, v2)
- [from source] (LAMBDA p.597) HTTP APIs use event format version 2.0 (version, routeKey, rawPath, rawQueryString, cookies, headers, requestContext.http)
- [from source] (LAMBDA p.598) Tutorial (p.598-606): REST API DynamoDBOperations, resource DynamoDBManager, POST method tied to the LambdaFunctionOverHttps function (create/read/update/delete/list/echo/ping operations); illustrates a custom execution role (DynamoDB + logs), AWS_PROXY proxy, ANY, {proxy+}. Examples use runtimes nodejs12.x and python3.8 [DATED: discontinued runtimes]
- [from source] (LAMBDA p.603) CLI v2 requires --cli-binary-format raw-in-base64-out on invoke with a JSON payload in a file [DATED: CLI]
- [from source] (LAMBDA p.609) Blueprint microservice-http-endpoint: creates an HTTP API with a proxy resource, AWS_PROXY integration and ANY method; GET does a scan, POST creates, PUT updates, DELETE removes an item (p.609-610)
- [from source] (LAMBDA p.611) SAM template: AWS::Serverless::Function with Events of type Api (Path, Method) and Policies


## CloudTrail (p.612-619)
- [from source] (LAMBDA p.612) Pattern: CloudTrail writes logs to S3; S3 notifies Lambda (object-created) and the function reads/processes the records
- [from source] (LAMBDA p.614) Lambda is integrated with CloudTrail: API calls (console or code) become events; without a trail there is still Event history; a trail created in the console applies to all Regions
- [from source] (LAMBDA p.615) Logged actions include CreateEventSourceMapping, CreateFunction, UpdateFunctionCode etc.; ZipFile and Environment are omitted from the logs; eventName may have a version suffix (e.g. GetFunction20150331); entry order is not guaranteed
- [from source] (LAMBDA p.617) Data events: enable to log each invocation; CloudTrail only records authenticated and authorized requests
- [from source] (LAMBDA p.617) LambdaESMDisabled event: causes RESOURCE_NOT_FOUND, FUNCTION_NOT_FOUND, REGION_NAME_NOT_VALID, AUTHORIZATION_ERROR, FUNCTION_IN_FAILED_STATE; detail in serviceEventDetails.ESMDisableReason


## EventBridge / CloudWatch Events (start of p.620)
- [from source] (LAMBDA p.620) EventBridge is the preferred way; CloudWatch Events and EventBridge are the same service/API; rules match events and route them to the function; ASYNCHRONOUS invocation with an event that wraps the original; also allows scheduling by rate or cron


## EventBridge: scheduling (p.620-625)
- [from source] (LAMBDA p.621) Each account can have up to 100 unique event sources of type EventBridge Schedule, each feeding up to 5 functions, i.e. up to 500 scheduled functions in the account [DATED: quotas]
- [from source] (LAMBDA p.621) Console: Add trigger > EventBridge (CloudWatch Events) > Create a new rule. A scheduled event has detail-type "Scheduled Event" and source aws.events (p.620-621)
- [from source] (LAMBDA p.622) Tutorial (illustrates): the lambda-canary blueprint runs every minute (rate(1 minute)); a CloudWatch alarm on the Errors metric (Sum, >=1) publishes to an SNS topic with email; a function error generates the Errors metric
- [from source] (LAMBDA p.624) rate(Value Unit) format: Value positive integer, Unit minute(s)/hour(s)/day(s), singular if the value is 1 (rate(1 day), rate(5 days)); minimum frequency of once per minute [DATED]
- [from source] (LAMBDA p.625) cron(Minutes Hours Day-of-month Month Day-of-week Year); one of day-of-month/day-of-week must be "?"; in the Lambda console do not include the "cron" prefix; examples cron(15 10 * * ? *), cron(0 18 ? * MON-FRI *), cron(0 9 ? * 2#1 *)


## CloudWatch Logs (p.626)
- [from source] (LAMBDA p.626) CloudWatch Logs invokes ASYNCHRONOUSLY via subscription (to one or more log streams, with an optional filter pattern); the awslogs.data field is a Base64 .gzip file; decoded: messageType, owner, logGroup, logStream, subscriptionFilters, logEvents[id,timestamp,message]


## CloudFormation custom resources (p.627-628)
- [from source] (LAMBDA p.627) Function as a custom resource target (AWS::CloudFormation::CustomResource, ServiceToken = function ARN); invoked ASYNCHRONOUSLY on stack create/update/delete with an event containing RequestType, ResponseURL (callback), StackId, RequestId, LogicalResourceId, ResourceProperties
- [from source] (LAMBDA p.628) The function is responsible for responding to the callback URL with Status SUCCESS/FAILED (PhysicalResourceId, StackId, RequestId, LogicalResourceId); the cfn-response library does the sending (response.send) and is included automatically if the function is defined in the template; in the example Delete responds SUCCESS immediately. Example uses nodejs12.x [DATED]


## Lambda@Edge (p.629-630)
- [from source] (LAMBDA p.629) Lambda@Edge runs Node.js and Python functions at AWS locations close to the viewer; trigger points: viewer request, origin request, origin response, viewer response; limited runtimes/resources; can generate a response without going to the origin; synchronous invocation (table p.586); event Records[].cf.request/config
- [from source] (LAMBDA p.630) Uses: A/B by cookie, content by User-Agent, access control by header/token, header/URL rewriting, generating HTTP responses (redirect to login, static pages)


## CodeCommit / CodePipeline (p.631-633)
- [from source] (LAMBDA p.631) Trigger on a CodeCommit repository (branch/tag creation, push); event Records[].codecommit.references[{commit,ref}], eventName ReferenceChanges
- [from source] (LAMBDA p.632) CodePipeline invokes the function ASYNCHRONOUSLY with a "CodePipeline.job" event (data.actionConfiguration.configuration.UserParameters, inputArtifacts, outputArtifacts, artifactCredentials)
- [from source] (LAMBDA p.633) The function MUST call the CodePipeline API (PutJobSuccessResult / PutJobFailureResult) to signal the end of the job, using the job id from the event. The execution role needs codepipeline:PutJobSuccessResult and PutJobFailureResult (managed policy AWSCodePipelineCustomActionAccess); the pipeline needs ListFunctions and InvokeFunction (the default pipeline role already includes them). Since the invocation is asynchronous, there is a retry on error; configure a destination to retain unprocessed events


## CodeWhisperer (p.634-639)
- [from source] (LAMBDA p.634) CodeWhisperer in the Lambda console: ML code generator; only in the US East (N. Virginia) Region [DATED]; only Python and Node.js functions (p.635)
- [from source] (LAMBDA p.635) Enable: code editor > Tools > CodeWhisperer code suggestions; manual shortcut Alt+C (Option+C on Mac), Tab accepts, ESC rejects [DATED: UI]
- [from source] (LAMBDA p.636) Best practice cited: manually move suggested imports to the top of the file; review suggested constants (p.638)


## Cognito, Config, Connect (p.640-642)
- [from source] (LAMBDA p.640) Cognito Events (Sync Trigger on each dataset sync); mapping via the Cognito subscription configuration; event has datasetName, eventType SyncTrigger, identityId, datasetRecords
- [from source] (LAMBDA p.641) AWS Config: the function evaluates configuration compliance (custom rules) and reports the result to Config; event has invokingEvent, ruleParameters, resultToken, executionRoleArn, configRuleArn
- [from source] (LAMBDA p.642) Amazon Connect invokes SYNCHRONOUSLY; event Name ContactFlowEvent with Details.ContactData and Parameters


## EC2 (p.665-666)
- [from source] (LAMBDA p.665) EC2 lifecycle events (state change, EBS snapshot, spot about to be terminated) arrive via EventBridge (CloudWatch Events), which invokes ASYNCHRONOUSLY; event detail-type "EC2 Instance State-change Notification"
- [from source] (LAMBDA p.666) Permission: principal events.amazonaws.com with an ArnLike condition on the rule's source ARN; the EventBridge console updates the resource policy by itself, otherwise use add-permission; if the function uses the SDK to manage EC2, add EC2 permissions to the execution role


## ElastiCache (p.667-670) - VPC access tutorial
- [from source] (LAMBDA p.669) Tutorial: a function with the VPC's subnets and security group accesses an ElastiCache (Memcached) cluster; role AWSLambdaVPCAccessExecutionRole (permissions to manage the VPC's network connections); config via --vpc-config SubnetIds=...,SecurityGroupIds=...; libraries pymemcache and elasticache-auto-discovery; example uses --timeout 30 --memory-size 1024 python3.8 [DATED] (p.667-669)


## Application Load Balancer (p.671-672)
- [from source] (LAMBDA p.671) ALB supports Lambda as a target; load balancer rules route by path or header; SYNCHRONOUS invocation; event has requestContext.elb.targetGroupArn, httpMethod, path, queryStringParameters, headers, body, isBase64Encoded
- [from source] (LAMBDA p.671) The function's response must be JSON with statusCode, statusDescription, isBase64Encoded, headers, body; the ELB converts it into an HTTP response
- [from source] (LAMBDA p.672) Configure: give the ELB permission (add-permission principal elasticloadbalancing.amazonaws.com), create a target group that points to the function and add a rule on the load balancer for the target group


## EFS (p.673-674) - special integration, no invocation
- [from source] (LAMBDA p.673) The function mounts the EFS file system at initialization via NFS inside the VPC; Lambda manages the connection and encrypts the traffic; EFS and function must be in the SAME Region; a different account is possible with VPC peering; EFS supports file locking (advisory NFS v4.1, whole-file or byte-range lock)
- [from source] (LAMBDA p.673) Connections: EFS supports up to 25,000 connections per file system; each function instance creates a connection that persists across invocations -> ceiling of 25,000 concurrency; limit with reserved concurrency; in deployments at scale there is a temporary increase in instances, so use rolling deployments; a file system accepts a burst of 3,000 connections and then 500 new ones per minute (matches Lambda's burst scaling); ClientConnections metric [DATED: limits]
- [from source] (LAMBDA p.674) Throughput: bursting mode (default) has a low baseline proportional to size, with burst credits (100 MiB/s or more); without credits EFS throttles reads/writes and invocations can time out; with provisioned concurrency the function can consume credits even when idle (instances initialized and recycled every few hours); BurstCreditBalance metric; options: limit concurrency or enable provisioned throughput
- [from source] (LAMBDA p.674) IOPS: general purpose mode limits IOPS in favor of lower latency; PercentIOLimit metric; at 100% the function can time out


## IoT and IoT Events (p.675-677)
- [from source] (LAMBDA p.675) AWS IoT Rules Engine (SQL language) invokes the function ASYNCHRONOUSLY with the message data; on error there is a retry, and a destination retains unprocessed events; permission via add-permission with principal iot.amazonaws.com
- [from source] (LAMBDA p.676) IoT Events: a detector model (state machine) calls the function ASYNCHRONOUSLY as an action; event has eventName, eventTime, payload.detector, eventTriggerDetails, actionExecutionId, state; permission with principal iotevents.amazonaws.com


## Kinesis Data Firehose (p.690)
- [from source] (LAMBDA p.690) Firehose invokes the function (synchronous, p.587) to transform data before delivering it to destinations such as S3/Kinesis Data Analytics; event has invocationId, deliveryStreamArn, region, records[{data (base64), recordId, approximateArrivalTimestamp, kinesisRecordMetadata}]


## Amazon Lex (p.713-714)
- [from source] (LAMBDA p.713) Lambda can do validation (DialogCodeHook, after each user response) and/or fulfillment (FulfillmentCodeHook, after collecting all slots and confirmation); SYNCHRONOUS invocation; controlling concurrency limits simultaneous conversations: the Lex API returns HTTP 429 (Too Many Requests) if the function is at maximum and 424 (Dependency Failed Exception) if the function throws an exception
- [from source] (LAMBDA p.713) Lex execution role = service-linked role (AWSServiceRoleForLexBots, created by the console or create-service-linked-role --aws-service-name lex.amazonaws.com); extra permissions for other services go in that role; invocation permission via a resource-based policy (principal lex.amazonaws.com, intent source-arn) created automatically by the console


## RDS (p.734-739)
- [from source] (LAMBDA p.734) RDS event notifications go to an SNS topic that invokes the function; SNS wraps the RDS message in its own document (Records[].Sns.Message)
- [from source] (LAMBDA p.737) Tutorial (illustrates access to RDS MySQL in a VPC): role AWSLambdaVPCAccessExecutionRole; Python function with pymysql; connection created OUTSIDE the handler for reuse across invocations; credentials in file/env only for illustration - in production use Secrets Manager instead of environment variables; created with --vpc-config; example db.t2.micro, python3.8 [DATED]
- [from source] (LAMBDA p.738) Recommendation: if many instances run in parallel, some may not get a database connection; use reserved concurrency lower than the number of database connections (this also reserves instances for the function, which may not be ideal); if the invocation comes from your application, limit concurrency in the code


## S3 (p.740-)
- [from source] (LAMBDA p.740) S3 sends an event when an object is created or deleted; you configure the notification on the bucket and grant S3 permission via the function's resource-based policy; ASYNCHRONOUS invocation with a Records[] event (eventName e.g. ObjectCreated:Put, s3.bucket.name, s3.object.key/size/eTag/sequencer)
- [from source] (LAMBDA p.740) ANTI-PATTERN (Warning): using the same bucket that triggers the function to write the output can create a loop (the function invokes itself); solution: two buckets, or configure the trigger only for a prefix used for input objects
- [from source] (LAMBDA p.741) Console: when configuring an S3 trigger, the resource policy is modified to allow S3 if bucket and account match; if you configure the notification in S3, use the Lambda API to update the policy; it is also possible to grant permission to another account or restrict to an alias; if the function uses the SDK for S3, it needs S3 permissions in the execution role
- [from source] (LAMBDA p.741) Tutorial: bucket and function must be in the SAME Region; blueprint s3-get-object (Node) / s3-get-object-python; execution role via policy template (p.741-742)
- [from source] (LAMBDA p.743) Example code: the object key arrives URL-encoded (spaces as +): Node uses decodeURIComponent(key.replace(/\+/g,' ')), Python urllib.parse.unquote_plus; the error message reminds that the bucket must be in the same Region
- [from source] (LAMBDA p.744) The test event uses the template "S3 Put (s3-put)"; example key "test%2Fkey" (confirms the encoding)


## S3 (cont., p.745-757) - tutorials
- [from source] (LAMBDA p.745) Simple tutorial: validate that the Invocations graph (Monitor tab) matches the number of files uploaded; the policy created by Lambda has the prefix AWSLambdaS3ExecutionRole-
- [from source] (LAMBDA p.747) Thumbnails tutorial: the destination bucket must be named "<source>-resized"; buckets in the same Region as the function
- [from source] (LAMBDA p.748) Minimal policy in the example: logs (CreateLogGroup/CreateLogStream/PutLogEvents), s3:GetObject on the source bucket and s3:PutObject only on the -resized bucket (least privilege per bucket)
- [from source] (LAMBDA p.749) Node code: decoded key (spaces and unicode), type inferred from the suffix (only jpg/png), uses the sharp library (needs the same Node as the function and a Linux environment)
- [from source] (LAMBDA p.751) Python: the Pillow dependency has C/C++ code, so you CANNOT upload via the AWS CLI a package with it built in an arbitrary environment; use `sam build --use-container` (Docker with a Lambda-like environment; requires SAM CLI 1.39 or later) [DATED: SAM version]
- [from source] (LAMBDA p.752) Python uses /tmp for download/upload (download_path with uuid) and iterates event['Records']; SAM: Events of type S3 with Events s3:ObjectCreated:*; Runtime python3.9, Pillow 9.2.0 [DATED]
- [from source] (LAMBDA p.752) Node: create-function with --timeout 10 --memory-size 1024 and runtime nodejs16.x [DATED]; the 10 s timeout may need raising for larger objects (e.g. update-function-configuration --timeout 30) (p.753)
- [from source] (LAMBDA p.754) Test with invoke --invocation-type Event (asynchronous) or RequestResponse (synchronous)
- [from source] (LAMBDA p.754) S3 permission via add-permission with principal s3.amazonaws.com, --source-arn of the bucket and --source-account; reason: S3 only invokes if the event comes from that bucket AND the bucket belongs to your account, because if a bucket is deleted another account can create another with the same ARN
- [from source] (LAMBDA p.755) Important: configure the notification only on the source bucket; the function must not create objects in the source bucket (loop). Console config: Properties > Event notifications > Create event notification (Event types "All object create events", Destination Lambda function)
- [from source] (LAMBDA p.756) SAM for the S3 section: Policies AWSLambdaExecute, Events of type S3, Timeout 60


## S3 Batch Operations (p.758-759)
- [from source] (LAMBDA p.758) An S3 Batch Operations job has a manifest (list of objects) and an action; S3 invokes the function SYNCHRONOUSLY per object; event has invocationSchemaVersion, invocationId, job.id and tasks[{taskId, s3Key, s3VersionId, s3BucketArn}]; the function must return JSON with invocationSchemaVersion, treatMissingKeysAs, invocationId and results[{taskId, resultCode (e.g. Succeeded), resultString}]; resultString goes into the completion report
- [from source] (LAMBDA p.759) Use a qualified ARN or not; for the same version across the whole job, configure a specific version in FunctionARN; with an alias or $LATEST the job starts calling the new version if it is updated during execution
- [from source] (LAMBDA p.759) It is not possible to reuse an existing S3 event-based function for batch: the event and the expected response are different
- [from source] (LAMBDA p.759) Permissions: resource-based policy allowing the job to invoke the function; trust policy on the execution role for S3 to assume the role; S3 permissions on the role if using the SDK
- [from source] (LAMBDA p.759) S3 starts several instances in parallel up to the function's concurrency limit, limiting the initial ramp-up to avoid excessive cost on small jobs; a TemporaryFailure response makes S3 retry the operation


## S3 Object Lambda (p.760)
- [from source] (LAMBDA p.760) S3 Object Lambda adds code to S3 GET, HEAD and LIST requests to modify data before returning it to the application (filter rows, resize images, redact confidential data) without creating derived copies or proxies


## Secrets Manager (p.761)
- [from source] (LAMBDA p.761) The function interacts with Secrets Manager via API/SDK, or can use the AWS Parameters and Secrets Lambda Extension to get and cache secrets without the SDK


## SES (p.762-763)
- [from source] (LAMBDA p.763) SES receiving email can call the function; the event is an SES message inside an SNS-like event (Records[].ses.mail/receipt, eventSource aws:ses); receipt.action.invocationType = "Event" (asynchronous) and carries spam/dkim/spf/virus verdicts


## SNS (p.764-771)
- [from source] (LAMBDA p.764) SNS supports Lambda as a topic target (same account or other accounts); invokes ASYNCHRONOUSLY; event Records[].Sns{Message, MessageAttributes, Subject, TopicArn, Timestamp, MessageId...}
- [from source] (LAMBDA p.764) Retry: Lambda queues (asynchronous invocation) and handles retries; if SNS cannot reach Lambda or the message is rejected, SNS retries at increasing intervals over several hours [DATED]
- [from source] (LAMBDA p.764) Cross-account: SNS must be authorized to invoke the function AND SNS must allow the function's account to subscribe to the topic (both accounts grant permission); not all options are in the console, so use the CLI
- [from source] (LAMBDA p.767) Cross-account tutorial: account A `aws sns add-permission --action-name Subscribe ListSubscriptionsByTopic` for account B; account B `aws lambda add-permission --principal sns.amazonaws.com --source-arn <topic>`; then `aws sns subscribe --protocol lambda --notification-endpoint <function arn>`
- [from source] (LAMBDA p.767) PITFALL: do NOT use --source-account when adding the policy for SNS: it is not supported for SNS sources and results in access denied. An opt-in Region requires the Region in the principal (e.g. sns.ap-east-1.amazonaws.com for Hong Kong) [DATED]
- [from source] (LAMBDA p.766) Tutorial execution role: AWSLambdaBasicExecutionRole (logs); function created with --timeout 60


## X-Ray (p.791-794) - special integration
- [from source] (LAMBDA p.791) If the service that invokes the function has X-Ray enabled, Lambda sends traces automatically; the upstream service (e.g. API Gateway) samples and adds a tracing header that tells Lambda to trace; traces from producers (e.g. SQS) are linked to those of the consumer functions
- [from source] (LAMBDA p.791) LIMITATION: X-Ray tracing is not supported for functions with an ESM from MSK, self-managed Kafka or Amazon MQ (ActiveMQ and RabbitMQ)
- [from source] (LAMBDA p.791) Console: Configuration > Monitoring and operations tools > Edit > Active tracing; cost: monthly free tier, then charges for trace storage and retrieval [DATED: price]; Lambda adds permissions to the role when enabling in the console, otherwise attach AWSXRayDaemonWriteAccess; sampling of 1 request per second + 5% of additional ones, NOT configurable [DATED]
- [from source] (LAMBDA p.792) Trace: Lambda service segment and function segment with subsegments Initialization (init: creates/thaws the environment, downloads code and layers, initializes extensions and runtime, runs init code), Invocation (handler) and Overhead (between response and next invoke, prepares to freeze); with provisioned concurrency Initialization can appear very long because instances are created ahead of time; the X-Ray SDK extends the Invocation subsegment (downstream calls, annotations, metadata) but does not allow accessing the function segment or recording work outside the handler
- [from source] (LAMBDA p.792) Role permissions: xray:PutTraceSegments and xray:PutTelemetryRecords (AWSXRayDaemonWriteAccess)
- [from source] (LAMBDA p.793) X-Ray daemon: process managed by Lambda that listens on UDP, buffers and sends in batches; it can use up to 3% of the configured memory or 16 MB (the larger); if memory runs short the runtime kills the daemon first; not configurable and segments always go to the same account as the function [DATED]
- [from source] (LAMBDA p.793) API: update-function-configuration --tracing-config Mode=Active; the tracing mode is part of the version config and CANNOT be changed on a published version; CloudFormation TracingConfig.Mode, SAM Tracing: Active (p.793-794)



# Synchronous/asynchronous invocation, retries, DLQ, destinations, function URLs

> Invocation types, async, DLQ, destinations, event source mapping (overview), batching, filters, function states, errors, tests, function URLs.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label are from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the text of the references is unaccented because it originates from reading notes.

## Invocation (overview)
- [from source] (LAMBDA p.295) Ways to invoke: console, function URL, API, SDK, CLI, toolkits; AWS services (S3, EventBridge on a schedule); Lambda reading a stream/queue
- [from source] (LAMBDA p.295) Synchronous: waits for a response; asynchronous: Lambda queues and responds immediately, handles retries and can send invocation records to destinations
- [from source] (LAMBDA p.295) Trigger = resource that lets another service invoke the function; each trigger is an independent client and each event has data from only one trigger; created via Function overview > Add trigger
- [from source] (LAMBDA p.295) Event source mapping = Lambda resource that reads items from a stream/queue (e.g. Kinesis, SQS) and creates events with batches (hundreds/thousands of items); created via console (through a trigger), CLI, API or SDK
- [from source] (LAMBDA p.295) Scaling and errors vary by invocation mode; synchronous returns errors in the response and allows retry


## Synchronous invocation
- [from source] (LAMBDA p.297) Lambda runs and waits; the response includes additional data such as the version executed; CLI: aws lambda invoke; AWS CLI v2 requires --cli-binary-format raw-in-base64-out (can become the default with aws configure set)
- [from source] (LAMBDA p.297) Output: ExecutedVersion and StatusCode 200; the payload is a JSON string; the response file (response.json) holds the object/error in JSON or null if it finished without error; status 200 even if the function returned an error (if Lambda managed to run it)
- [from source] (LAMBDA p.297) Functions with a long timeout: the client may be disconnected while waiting; configure HTTP client, SDK, firewall, proxy or OS for long connections (timeout/keep-alive)
- [from source] (LAMBDA p.298) Example error InvalidRequestContentException when the payload is not valid JSON
- [from source] (LAMBDA p.298) [DATED] --log-type Tail returns LogResult with up to 4 KB of logs in base64; decode with base64 -d (macOS: -D); the REPORT line shows Duration, Billed Duration, Memory Size, Max Memory Used
- [from source] (LAMBDA p.299) In direct invocation, the client checks for errors and retries; AWS CLI and SDK also retry automatically on client timeouts, throttling and service errors


## Asynchronous invocation
- [from source] (LAMBDA p.300) Services such as S3 and SNS invoke asynchronously; no response is expected; allows chaining components via invocation records
- [from source] (LAMBDA p.300) Lambda puts the event in a queue and returns success without details; a separate process reads the queue; invocation type parameter = Event (CLI --invocation-type Event); response StatusCode 202
- [from source] (LAMBDA p.301) [DATED] Retry on function error (includes runtime timeouts): 2 more attempts, wait of 1 min between the 1st and 2nd and 2 min between the 2nd and 3rd
- [from source] (LAMBDA p.301) [DATED] Throttling (429) and 500-series errors: the event returns to the queue and Lambda tries for up to 6 hours, with an exponential interval from 1 s to at most 5 min; a long queue increases the interval and reduces the read rate
- [from source] (LAMBDA p.301) Gotcha: the queue is eventually consistent, so duplicate events can arrive even without error; if the function does not keep up, events can be deleted without being sent; recommendation: idempotent code and sufficient concurrency
- [from source] (LAMBDA p.301) An event that expires or fails all attempts is discarded; you can configure it to reduce retries or discard faster
- [from source] (LAMBDA p.301) Supported destinations: SQS (standard queue), SNS, Lambda, EventBridge (event bus); the record has request/response details in JSON; separate destinations for success and failure; a DLQ (SQS or SNS) receives only the event content, without response details
- [from source] (LAMBDA p.301) Antipattern/trick: reserved concurrency = 0 stops the function from firing; in asynchronous invocation, new events go straight to the DLQ or on-failure destination, without retries; to process them later, consume from the DLQ/destination
- [p.301-302] Error handling configurable on function, version or alias: [DATED] Maximum age of event up to 6 hours; Retry attempts from 0 to 2; an event that exceeds the age or the attempts is discarded, and to keep a copy you configure a failure destination
- [p.302-303] Destination configurable on function/version/alias; Add destination: Source Asynchronous invocation, Condition On failure (all attempts failed or exceeded age) or On success, type and resource; permissions on the execution role: SQS sqs:SendMessage, SNS sns:Publish, Lambda InvokeFunction, EventBridge events:PutEvents
- [from source] (LAMBDA p.303) Format: SQS/SNS receive the record as Message; Lambda as payload; EventBridge as the detail of PutEvents with source "lambda" and detail-type "Lambda Function Invocation Result - Success/Failure"
- [p.303-304] Invocation record example: version 1.0, requestContext (requestId, functionArn, condition "RetriesExhausted", approximateInvokeCount 3), requestPayload, responseContext (statusCode, executedVersion, functionError "Unhandled"), responsePayload
- [from source] (LAMBDA p.304) API: Put/Get/Update/List/DeleteFunctionEventInvokeConfig; put-function-event-invoke-config (--maximum-event-age-in-seconds 3600 --maximum-retry-attempts 0) OVERWRITES the existing configuration; update-function-event-invoke-config changes one option without resetting the others (e.g. --destination-config OnFailure)
- [from source] (LAMBDA p.305) DLQ vs on-failure destination: both used when all attempts fail or the event expires; the DLQ is part of the version-specific configuration (locked when published); the destination supports more targets and includes response details
- [from source] (LAMBDA p.305) Reprocess the DLQ: set it as an event source or recover manually; SQS (a single consumer, e.g. Lambda or alarm) vs SNS (multiple targets: email, Lambda, HTTP); permissions sqs:SendMessage / sns:Publish; if the target uses a CMK, the execution role must be a user in the key policy; several functions can use the same target
- [from source] (LAMBDA p.306) DLQ: console Asynchronous invocation > DLQ resource; CLI --dead-letter-config TargetArn=...; the event is sent as is, with attributes RequestID (String), ErrorCode (Number, HTTP status) and ErrorMessage (String, first 1 KB)
- [p.306-307] If Lambda cannot send to the DLQ (missing permission or message above the size limit, e.g. SNS ~256 KB + attributes), it deletes the event and emits the DeadLetterErrors metric
- [from source] (LAMBDA p.307) With SQS as the event source, configure the DLQ on the SQS queue itself, not on the function


## Event source mappings (introduction)
- [from source] (LAMBDA p.308) Event source mapping = resource that reads from a source and invokes the function; sources: DynamoDB, Kinesis, Amazon MQ, MSK, self-managed Apache Kafka, SQS; to send to other targets or enrich, see EventBridge Pipes
- [from source] (LAMBDA p.308) Uses the execution role's permissions to read/manage items; permissions, event structure, settings and polling vary by source; API: Create/List/Get/Update/DeleteEventSourceMapping
- [from source] (LAMBDA p.308) CLI example: create-event-source-mapping with --batch-size 500 --maximum-batching-window-in-seconds 5 --starting-position LATEST for a DynamoDB stream; response with UUID, BatchSize, MaximumBatchingWindowInSeconds, ParallelizationFactor 1
- [from source] (LAMBDA p.309) Example response of create-event-source-mapping (stream): State Creating, MaximumRecordAgeInSeconds 604800, BisectBatchOnFunctionError false, MaximumRetryAttempts 10000 (default values shown)
- [from source] (LAMBDA p.309) Event source mappings process events AT LEAST ONCE (distributed nature of the pollers): duplicates are rare; build idempotent functions


## Batching
- [from source] (LAMBDA p.309) By default the mapping groups records into a single payload; adjustments: batching window (MaximumBatchingWindowInSeconds = maximum time to gather records) and BatchSize (maximum records per batch)
- [from source] (LAMBDA p.309) Lambda invokes the function when ONE of three criteria occurs: the window reaches its maximum; the batch size is reached (minimum 1; default/maximum depend on the source); the payload reaches 6 MB (not modifiable)
- [from source] (LAMBDA p.309) [DATED] Kinesis, DynamoDB and SQS: default window 0 s (sends as fast as possible); if configured, the next window starts as soon as the previous invocation ends
- [from source] (LAMBDA p.309) [DATED] MSK, self-managed Kafka and Amazon MQ: default window 500 ms; configurable from 0 to 300 s in increments of seconds; the window starts with the first record
- [from source] (LAMBDA p.309) Gotcha: since it only changes in seconds, you cannot return to the 500 ms default after changing it; you must create a new event source mapping
- [from source] (LAMBDA p.309) Diagram: a 40 s window ends at t=47 s with 5 records; or ends earlier if the batch size reaches 10 or the maximum payload is reached
- [from source] (LAMBDA p.311) Batch event = batch of records/messages compiled until the window expires; example: a batch that fails all attempts has its details sent to an SQS queue
- [from source] (LAMBDA p.311) Streams: iterator per shard, items processed in order per shard; can read only new items or start from old ones; processed items are not removed from the stream (other consumers can read them)
- [p.311-312] If the function returns an error, the mapping reprocesses the entire batch until success or expiration; to keep order, it pauses the affected shard until resolved; configurable: discard old events, limit retries, process several batches in parallel (order guaranteed per partition key, but several partition keys of the same shard simultaneously)
- [from source] (LAMBDA p.312) Destinations for stream mapping (batch discard): only SQS and SNS; the record contains details of the failed batch; Kinesis example: condition RetryAttemptsExhausted, KinesisBatchInfo (shardId, startSequenceNumber, endSequenceNumber, batchSize, streamArn)
- [from source] (LAMBDA p.312) SQS: FIFO preserves order, scaling up to the number of active message groups; standard does not guarantee order and scales as fast as possible; on error the batches return to the queue as individual items and may be regrouped; an item can arrive twice even without error; items deleted after success; DLQ configured on the source queue


## Event filtering
- [from source] (LAMBDA p.313) Filtering controls which events reach the function; [DATED] up to 5 filters per source (default); an event that satisfies any one is sent, otherwise discarded; with a batching window, the filter is applied to each new event before it enters the batch
- [from source] (LAMBDA p.313) Structure: FilterCriteria > Filters > Filter with Pattern (string with JSON rule); three parts: metadata properties, data properties and filter patterns
- [from source] (LAMBDA p.314) Metadata = fields of the event object (e.g. partitionKey); data = fields of the body; the data key depends on the source: Kinesis = data, SQS = body, DynamoDB = dynamodb; the event must contain all fields named in the filter; fields not mentioned are ignored
- [from source] (LAMBDA p.314) Duplicate keys in the pattern: only the last value counts
- [p.314-315] Syntax same as Amazon EventBridge; operators: Null [null], Empty [""], Equals, And (several keys), Or (several values), Not {"anything-but"}, Numeric equals/range, Exists true/false, Begins with {"prefix"}
- [from source] (LAMBDA p.315) Gotcha: exact character-by-character comparison, no case folding; numbers compared as strings (300, 300.0 and 3.0e2 are not equal)
- [p.315-317] Examples: partitionKey + Location=Los Angeles (Equals); Temperature >50 and <=60 (numeric range); multi-level in DynamoDB (dynamodb.Keys.Id.N = 101)
- [from source] (LAMBDA p.317) Console: Add trigger > type with filter support (SQS, DynamoDB, Kinesis, MSK, MQ) > Additional settings > Filter criteria > Add; in the console you enter only the pattern, without the Pattern key or escaping quotes
- [from source] (LAMBDA p.318) [DATED] Default 5 filters per source; quota increase up to 10; the console allows up to 10 according to quota; excess causes an error when creating the mapping
- [from source] (LAMBDA p.318) CLI: create-event-source-mapping --filter-criteria; update-event-source-mapping --uuid (UUID comes from ListEventSourceMappings or from the Create response); remove filters with --filter-criteria "{}"
- [from source] (LAMBDA p.318) SQS: a message that does not satisfy the filter is removed automatically from the queue (no manual deletion)
- [p.318-319] SQS body can be any string; the body format in the filter must match that of the message: string x string OK; JSON x JSON OK; string with JSON pattern or JSON with string pattern => message DISCARDED; no pattern for data => filters by metadata only; if body is not in the filter, the check is skipped
- [from source] (LAMBDA p.319) Kinesis/DynamoDB: the iterator advances after the filter; non-matching records do not need to be deleted (deleted after the retention period); the data field and filter must be valid JSON
- [p.319-320] Kinesis/DynamoDB table: JSON data + JSON filter = filters; JSON data + non-JSON filter = EXCEPTION on creating/updating the mapping; non-JSON data + JSON filter = record discarded; non-JSON data + non-JSON = exception; no data pattern = filters metadata only
- [from source] (LAMBDA p.320) [DATED] Kafka/MQ: up to 15 minutes to apply filter rules after attaching; fields: MQ = data; Kafka (MSK and self-managed) = key and value; Lambda discards what does not match all fields; Kafka commits offsets of matched and unmatched after invoking successfully; MQ acknowledges matched after success and unmatched when filtering
- [p.320-321] Kafka/MQ messages must be UTF-8 strings (text or JSON), since Lambda decodes bytes to UTF-8; other encodings (UTF-16, ASCII) or incompatible format: only metadata filters are applied (does not discard by data)


## Function states
- [from source] (LAMBDA p.322) The State field indicates whether the function is ready; it does not change invocation behavior. Pending (creating resources such as VPC/EFS; invocations and other APIs FAIL), Active (only then does it invoke successfully), Failed (error in configuration/provisioning), Inactive (idle long enough for Lambda to reclaim external resources; invoking fails and returns to Pending; if it is not recreated, returns to Inactive)
- [from source] (LAMBDA p.322) In automation via SDK/API, check the state before invoking (GetFunction; or the Java SDK 2.0 waiter): get-function --query 'Configuration.[State, LastUpdateStatus]'; attributes StateReason and StateReasonCode for troubleshooting
- [from source] (LAMBDA p.322) Fail while creation is pending: Invoke, UpdateFunctionCode, UpdateFunctionConfiguration, PublishVersion
- [p.322-323] LastUpdateStatus: InProgress (invocations keep using the previous code/config), Successful, Failed (update aborted, previous remains); attributes LastUpdateStatusReason/ReasonCode; during an asynchronous update, UpdateFunctionCode, UpdateFunctionConfiguration, PublishVersion fail


## Errors and retries
- [from source] (LAMBDA p.324) Two types: invocation errors (request rejected before the function received it: request too large/invalid JSON/nonexistent function/parameter type; caller without permission; account at maximum instances or requests too fast) and function errors (exception in the code or runtime: timeout, syntax error, failure to serialize the response)
- [from source] (LAMBDA p.324) CLI/SDK retry on client timeouts, throttling (429) and errors that are not bad-request errors
- [from source] (LAMBDA p.324) Function errors do NOT produce 4xx/5xx status; Lambda signals them with the X-Amz-Function-Error header and a JSON body with the message
- [from source] (LAMBDA p.324) In direct invocation the strategy is the caller's (retry, debug queue or ignore); the function may have run fully, partially or not at all: code must tolerate the same event several times without duplicate transactions
- [from source] (LAMBDA p.325) Asynchronous: Lambda retries function errors twice; without capacity, events can wait hours or days in the queue; use a DLQ
- [from source] (LAMBDA p.325) Stream event source mapping: retries the entire batch; repeated errors block the shard until resolved or the items expire; monitor the IteratorAge metric for stuck shards; queue: time between retries and failure destination via the visibility timeout and redrive policy of the source queue
- [from source] (LAMBDA p.325) AWS services: in synchronous invocation the service decides the retry (e.g. S3 batch operations retries on TemporaryFailure; API Gateway always passes the error to the requester); in asynchronous the behavior is the same as synchronous (text)
- [from source] (LAMBDA p.325) Other accounts: use resource-based policies; protect from overload with API Gateway in front; integration with CloudWatch and X-Ray (logs, metrics, alarms, tracing); error processor example


## Tests in the console
- [from source] (LAMBDA p.326) Test event = JSON input ({} if no input is required); private events: only the creator, no extra permissions; [DATED] up to 10 private events per function; Test tab > Template/Name/JSON > Event sharing settings Private > Save changes; also in the Code tab > Test > Configure test event
- [from source] (LAMBDA p.326) Shareable events: shared with IAM users of the same account, who can edit and invoke them; saved as schemas in an EventBridge registry called lambda-testevent-schemas (recommendation: do not edit or create a registry with that name); require permissions schemas:CreateRegistry, CreateSchema, DeleteSchema, DeleteSchemaVersion, DescribeRegistry, DescribeSchema, GetDiscoveredSchema, ListSchemaVersions, UpdateSchema
- [p.326-327] Saving the edit of a shareable event overwrites the event; if you cannot see/edit it, check permissions or resource-based policies on the registry
- [from source] (LAMBDA p.327) Running a test in the console invokes the function SYNCHRONOUSLY; the Test button before saving creates an unsaved event preserved in the session; result in Execution result > Details
- [from source] (LAMBDA p.327) Deleting shareable events removes them from the registry; when the last is removed, Lambda deletes the registry; when the function is deleted the schemas are NOT removed (clean up manually in EventBridge)


## Invoking container image functions
- [from source] (LAMBDA p.328) Invocation behavior is very similar to .zip; after the image upload, Lambda optimizes it (a few seconds); the function is Pending and then Active; while Pending you can invoke, but other operations fail; invocations during the update run the previous image
- [from source] (LAMBDA p.328) With no invocation for several weeks, Lambda reclaims the optimized version and the function becomes Inactive; the first invocation is REJECTED and returns to Pending until re-optimized
- [from source] (LAMBDA p.328) Lambda periodically fetches the image from ECR; if the image no longer exists or permissions are revoked, the function goes to Failed and invocations fail
- [from source] (LAMBDA p.328) On invocation: deploys the image in the environment, initializes extensions, runs the init code (outside the handler) - the init duration counts toward billed time - and calls the entry point (the image's ENTRYPOINT and CMD)
- [from source] (LAMBDA p.328) Image security: optimized, encrypted and stored with authenticated convergent encryption; keys protected by KMS customer managed keys; auditing via CloudTrail


## Function URLs
- [from source] (LAMBDA p.329) Function URL = dedicated HTTP(S) endpoint; URL generated automatically and NEVER changes; [DATED] format https://<url-id>.lambda-url.<region>.on.aws; dual stack (IPv4 and IPv6)
- [from source] (LAMBDA p.329) Accessible only over the public internet: functions support PrivateLink, function URLs do NOT; security via resource-based policies; supports CORS
- [from source] (LAMBDA p.329) Applies to any alias or to $LATEST; cannot be added to other versions
- [from source] (LAMBDA p.330) Console: Configuration > Function URL > Create function URL; Auth type AWS_IAM or NONE; optional CORS; creates for $LATEST (or for the alias, via the Aliases tab)
- [from source] (LAMBDA p.331) When creating the function with a Function URL and CORS checked, the URL allows requests from all origins by default; edit afterwards
- [from source] (LAMBDA p.331) CLI: create-function-url-config --function-name --qualifier (optional) --auth-type --cors-config; the function must exist
- [from source] (LAMBDA p.332) CloudFormation AWS::Lambda::Url: AuthType (required: AWS_IAM or NONE), Cors (optional), Qualifier (alias name), TargetFunctionArn (required; name, ARN or partial ARN); Cors: AllowCredentials, AllowHeaders, AllowMethods, AllowOrigins, ExposeHeaders, MaxAge
- [from source] (LAMBDA p.333) CORS: recommended to configure if the URL will be called from another domain; supported headers: Access-Control-Allow-Origin (AllowOrigins), Allow-Methods, Allow-Headers, Expose-Headers, Allow-Credentials, [DATED] Max-Age (MaxAge default 5, example 300)
- [from source] (LAMBDA p.333) Config via console/CLI makes Lambda add the CORS headers to all responses; you can also add them manually; on conflict, the CORS configured on the URL takes precedence
- [from source] (LAMBDA p.333) [DATED] Function URL throttling via reserved concurrency: maximum RPS = 10 x reserved concurrency (e.g. 100 => 1,000 RPS); above that or above the concurrency: HTTP 429
- [from source] (LAMBDA p.334) Disable in an emergency: reserved concurrency = 0 (all requests get 429); re-enable by removing the reservation or setting a value > 0
- [from source] (LAMBDA p.334) Deleting a function URL is irreversible; recreating generates a different URL; confirm by typing "delete"; with auth NONE the associated resource-based policy is NOT deleted automatically (remove manually)


## Security and auth model
- [from source] (LAMBDA p.335) Access controlled by AuthType + resource-based policy; AWS_IAM: authenticates/authorizes via the principal's identity policy and the function's resource policy; NONE: no authentication, but the resource-based policy still applies and must grant public access
- [from source] (LAMBDA p.335) IAM Access Analyzer helps analyze external access and public/cross-account permissions; free; policies can be created via AddPermission or console
- [from source] (LAMBDA p.335) AWS_IAM requires the lambda:InvokeFunctionUrl permission; same account: an identity-based policy OR a resource-based policy is enough (resource policy optional if the user already has the permission in the identity policy)
- [from source] (LAMBDA p.336) Cross-account: requires BOTH: an identity-based policy with lambda:InvokeFunctionUrl and permission in the function's resource-based policy; condition key lambda:FunctionUrlAuthType = AWS_IAM; console: Configuration > Permissions > Add permissions > Function URL; CLI add-permission --function-url-auth-type AWS_IAM
- [from source] (LAMBDA p.337) Important/antipattern: auth NONE + public resource policy => any unauthenticated user with the URL invokes the function; policy with Principal "*" and FunctionUrlAuthType NONE
- [from source] (LAMBDA p.337) Console/SAM automatically create the public policy for NONE (if one already exists or without permission, it does not create it); with CLI/CloudFormation/API you must add lambda:InvokeFunctionUrl manually (this makes the function public)
- [from source] (LAMBDA p.337) Without lambda:InvokeFunctionUrl in the resource policy, the user gets 403 Forbidden, even with auth NONE
- [p.337-338] Governance: IAM actions lambda:InvokeFunctionUrl, CreateFunctionUrlConfig, UpdateFunctionUrlConfig, GetFunctionUrlConfig, ListFunctionUrlConfigs, DeleteFunctionUrlConfig; the console only adds permission for InvokeFunctionUrl (the rest via API/CLI)
- [p.338-339] Condition key FunctionUrlAuthType (enum AWS_IAM or NONE) in function policies: e.g. deny UpdateFunctionUrlConfig when auth is NONE; allow create/update only for AWS_IAM; also usable in an SCP (StringNotEquals AWS_IAM) to deny URLs that are not AWS_IAM in the organization


## Invoking function URLs
- [from source] (LAMBDA p.340) To invoke you need lambda:InvokeFunctionUrl; AWS_IAM requires signing each request with AWS Signature Version 4 (SigV4) - tools: awscurl, Postman, AWS SigV4 Proxy; Lambda recomputes the signature and only processes if they match; NONE needs no signature (browser, curl, Postman)
- [from source] (LAMBDA p.340) Examples: GET in the browser with a query string (?message=HelloWorld) and POST via curl with JSON
- [p.340-341] Lambda maps the HTTP request to an event and the function's response to HTTP; request/response formats follow the API Gateway payload format version 2.0 schema
- [from source] (LAMBDA p.341) Event structure: version "2.0", routeKey "$default", rawPath, rawQueryString, cookies, headers, queryStringParameters, requestContext (accountId, apiId, authorizer.iam, domainName, http.method/path/protocol/sourceIp/userAgent, requestId, stage, time, timeEpoch), body, pathParameters, isBase64Encoded, stageVariables
- [from source] (LAMBDA p.342) Parameter table: version (function URLs support only 2.0); routeKey not used by function URLs, Lambda puts $default as a placeholder; rawPath = request path
- [p.342-344] requestContext fields: accountId (function owner), apiId (URL ID), authentication (always null), authorizer.iam (accessKey, accountId, callerId, cognitoIdentity, principalOrgId, userArn, userId; only when auth is AWS_IAM, otherwise null), domainName, domainPrefix, http (method: GET, POST, PUT, HEAD, OPTIONS, PATCH, DELETE; path; protocol; sourceIp = IP of the immediate TCP connection; userAgent), requestId (to trace logs), routeKey and stage ($default as placeholder), time, timeEpoch
- [from source] (LAMBDA p.342) Other fields: rawQueryString, cookies (array), headers (key-value pairs), queryStringParameters (object)
- [from source] (LAMBDA p.344) body: if the content type is binary, the body comes in base64; isBase64Encoded TRUE if payload is binary; pathParameters and stageVariables: not used, null or omitted
- [from source] (LAMBDA p.344) Response format: statusCode, headers, body, cookies (array) and isBase64Encoded; Lambda converts the return into an HTTP response
- [from source] (LAMBDA p.345) Lambda INFERS the format: if the function returns valid JSON without statusCode, it assumes statusCode 200, content-type application/json, body = return value, isBase64Encoded false; examples: string, JSON, custom response (201 + custom header)
- [from source] (LAMBDA p.346) Cookies: do not add set-cookie headers manually; include them in the payload's cookies array and Lambda generates the set-cookie headers in the HTTP response


## Function URL monitoring
- [from source] (LAMBDA p.347) CloudTrail automatically records Create/Update/Delete/Get/ListFunctionUrlConfig(s); [DATED] Event history covers 90 days (create a trail to keep more); InvokeFunctionUrl is NOT logged by default (data event, can be enabled)
- [from source] (LAMBDA p.347) CloudWatch metrics: UrlRequestCount, Url4xxError (client errors), Url5xxError (server errors, including function errors and timeouts), Sum statistic recommended; UrlRequestLatency (time between receiving the request and returning the response), Average or Max recommended
- [p.347-348] Dimensions: FunctionName (aggregate of $LATEST and aliases), Resource (specific URL: function + $LATEST or alias, e.g. hello-world-function:$LATEST), ExecutedVersion (mainly for a URL on $LATEST)


## Function URL tutorial
- [from source] (LAMBDA p.349) Tutorial: .zip function with a public function URL that returns the product of two numbers; creates execution role lambda-url-role with AWSLambdaBasicExecutionRole (logs in CloudWatch); on Windows, use WSL for Bash commands such as zip
- [from source] (LAMBDA p.350) Steps: index.js (parses event.body, returns statusCode 200 and text); zip function.zip index.js; create-function (runtime nodejs14.x, --handler index.handler, role); add-permission (--action lambda:InvokeFunctionUrl --principal "*" --function-url-auth-type "NONE" --statement-id url); create-function-url-config --auth-type NONE; test with curl POST {"num1":"10","num2":"10"} => "The product of 10 and 10 is 100"
- [from source] (LAMBDA p.351) Equivalents: CloudFormation (AWS::Lambda::Function + AWS::Lambda::Permission with FunctionUrlAuthType NONE + AWS::Lambda::Url) and SAM (FunctionUrlConfig with AuthType NONE, AutoPublishAlias live)
- [from source] (LAMBDA p.352) Cleanup: delete the execution role and the function to avoid costs


## Gaps and inconsistencies observed (no KEY; reader's notes)
- [p.247-248] Apparent inconsistency: the comparison table says that without reserved the throttling occurs when the provisioned limit is reached, but the p.245 example shows overflow into unreserved concurrency without throttling (the table seems to treat the reserved case the same as provisioned, according to the p.247 note)
- [p.258-259] Note: scaling by Application Auto Scaling depends on 3 data points of the average; the text warns that short bursts do not scale, offering no alternative besides scheduled scaling
- Not covered in this range: source-specific parameters of event source mappings (retry, bisect on error, parallelization factor, report batch item failures, tumbling window), which live in each service's chapters; there is also no detail on the maximum timeout of function URLs or on response payload limits.
- [from source] (LAMBDA p.318) CLI filter-criteria example uses inner quotes without full shell escaping; the text does not comment on it


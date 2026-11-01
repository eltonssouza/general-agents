# API reference: constraints and parameters

> Ranges, enums, errors and status codes of the API actions.
> Source: AWS Lambda Developer Guide (2022 edition; last releases entry on 2022-11-28), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label are from the source; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the original Portuguese reading notes were written without accents.

## A. General conventions of the API reference
- [from source] (LAMBDA p.984) API calls require a signed request; Lambda accepts Signature Version 4
- [from source] (LAMBDA p.984) The AWS CLI can be used to explore the API; the section has Actions (p.962 printed) and Data Types (p.1206 printed)
- [p.984-985] List of supported actions: Add*/Create*/Delete*/Get*/Invoke/InvokeAsync/List*/Publish*/Put*/Remove*/Tag/Untag/Update* (AddLayerVersionPermission ... UpdateFunctionUrlConfig)
- [DATED][p.986-1000] Common PATTERN of each action: Request Syntax (verb+versioned path), URI params, Request Body, Response Syntax, Errors, See Also (SDKs: CLI, .NET, C++, Go, Java V2, JavaScript, PHP V3, Python, Ruby V3). Path versions: /2015-03-31/ (functions, aliases, permissions), /2018-10-31/ (layers), /2020-04-22/ (code signing)
- [DATED][from source] (LAMBDA p.990) FunctionName (standard in almost all actions): accepts name, full ARN or partial ARN (123456789012:function:my-function); a version/alias can be appended; length min 1 / max 140 (limit applies only to the full ARN); the name alone is limited to 64 characters
- [DATED][from source] (LAMBDA p.990) FunctionName pattern: (arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?
- [DATED][from source] (LAMBDA p.991) Qualifier: min 1, max 128, pattern (|[a-zA-Z0-9$_-]+)


## B. Common error codes (Errors block) - standard and differences
- [DATED][from source] (LAMBDA p.988) InvalidParameterValueException = invalid parameter, HTTP 400
- [DATED][from source] (LAMBDA p.988) PolicyLengthExceededException = the resource permissions policy is too large (see quotas), HTTP 400
- [DATED][from source] (LAMBDA p.988) PreconditionFailedException = the RevisionId supplied does not match the latest; use GetFunction or GetAlias to get the current RevisionId; HTTP 412
- [DATED][from source] (LAMBDA p.988) ResourceConflictException = resource already exists or another operation is in progress; HTTP 409
- [DATED][from source] (LAMBDA p.988) ResourceNotFoundException = resource does not exist; HTTP 404
- [DATED][from source] (LAMBDA p.988) ServiceException = internal error of the Lambda service; HTTP 500
- [DATED][from source] (LAMBDA p.988) TooManyRequestsException = request throughput limit exceeded; HTTP 429
- [p.988,993,997,998,1000] Differences per action: AddLayerVersionPermission and AddPermission list 400 Invalid, 400 PolicyLength, 412 Precondition, 409 Conflict, 404 NotFound, 500 Service, 429 TooMany; CreateAlias lists 400, 409, 404, 500, 429 (no Precondition/PolicyLength); CreateCodeSigningConfig lists only 400 and 500


## C. AddLayerVersionPermission (p.986-988)
- [from source] (LAMBDA p.986) Adds permissions to the resource-based policy of a layer version; grants use to one account, all accounts of an organization or all AWS accounts; revoke with RemoveLayerVersionPermission using the StatementId
- [DATED][from source] (LAMBDA p.986) POST /2018-10-31/layers/LayerName/versions/VersionNumber/policy?RevisionId=; LayerName: name or ARN, min 1 max 140; VersionNumber required; RevisionId optional (optimistic concurrency control)
- [DATED][p.986-987] Body: Action (required, only lambda:GetLayerVersion, max 22), OrganizationId (optional, max 34, pattern o-[a-z0-9]{10,32}, used with Principal *), Principal (required; 12-digit account id, * or root ARN), StatementId (required, min 1 max 100, [a-zA-Z0-9-_]+)
- [from source] (LAMBDA p.987) Principal * without OrganizationId grants access to ALL AWS accounts; the text warns to make sure this is what you want
- [DATED][from source] (LAMBDA p.987) Response: HTTP 201 with RevisionId and Statement


## D. AddPermission (p.990-993)
- [from source] (LAMBDA p.990) Grants an AWS service, account or organization permission to use the function; it can restrict to the version/alias via Qualifier (the invoker must then use the full ARN of the version/alias); adding policies to the $LATEST version is NOT supported
- [from source] (LAMBDA p.990) Service principal: domain-style identifier (s3.amazonaws.com, sns.amazonaws.com); without SourceArn, other accounts could configure their own resources to invoke your function (anti-pattern to avoid)
- [DATED][from source] (LAMBDA p.990) POST /2015-03-31/functions/FunctionName/policy?Qualifier= ; response 201 with Statement
- [DATED][p.991-992] Body: Action (required, pattern lambda:* / lambda:Name / *), EventSourceToken (Alexa Smart Home only; 0-256; [a-zA-Z0-9._\-]+), FunctionUrlAuthType (enum NONE | AWS_IAM; NONE = public endpoint), Principal (required, [^\s]+), PrincipalOrgID (12-34, ^o-[a-z0-9]{10,32}$), RevisionId, SourceAccount (max 12, \d{12}), SourceArn (compared with the StringLike operator), StatementId (required, 1-100)
- [from source] (LAMBDA p.992) SourceAccount must be used together with SourceArn because an S3 bucket can be deleted by its owner and recreated by another account


## E. CreateAlias (p.995-998)
- [from source] (LAMBDA p.995) Creates an alias for a version; allows splitting traffic between two versions with RoutingConfig (AdditionalVersionWeights: map version->numeric weight)
- [DATED][p.995-996] POST /2015-03-31/functions/FunctionName/aliases; Description 0-256; FunctionVersion required 1-1024 pattern (\$LATEST|[0-9]+); Name required 1-128 pattern (?!^[0-9]+$)([a-zA-Z0-9-_]+) (the name cannot be digits only); RoutingConfig optional (AliasRoutingConfiguration); response 201 with AliasArn, RevisionId etc.


## F. CreateCodeSigningConfig (p.999-1000)
- [DATED][from source] (LAMBDA p.999) POST /2020-04-22/code-signing-configs/; defines the list of allowed signing profiles (AllowedPublishers.SigningProfileVersionArns, required) and the validation policy (CodeSigningPolicies.UntrustedArtifactOnDeployment, optional); Description 0-256; response 201 with CodeSigningConfig (Arn, Id, LastModified)


## G. CreateEventSourceMapping (p.1002-1012) - parameters with min/max/default
- [DATED][from source] (LAMBDA p.1002) Creates a link between an event source and a function; Lambda reads items from the source and invokes the function. Sources: DynamoDB Streams, Kinesis, SQS, Amazon MQ and RabbitMQ, MSK, Apache Kafka
- [from source] (LAMBDA p.1002) Error-handling options ONLY for stream sources (DynamoDB and Kinesis): BisectBatchOnFunctionError, DestinationConfig, MaximumRecordAgeInSeconds, MaximumRetryAttempts, ParallelizationFactor
- [DATED][from source] (LAMBDA p.1002) For MaximumRecordAgeInSeconds and MaximumRetryAttempts the default is infinite (-1): records that fail are reprocessed until they expire
- [DATED][p.1002,1007] Route POST /2015-03-31/event-source-mappings/ ; no URI params; response HTTP 202 (not 201)
- [DATED][p.1003-1004] BatchSize: max records per batch, delivered in a single call up to the synchronous payload limit (6 MB). Default/max: Kinesis 100/10,000; DynamoDB Streams 100/10,000; SQS default 10, max 10,000 on standard queues and 10 on FIFO; MSK 100/10,000; self-managed Kafka 100/10,000; Amazon MQ (ActiveMQ and RabbitMQ) 100/10,000. Valid range: min 1, max 10000
- [DATED][from source] (LAMBDA p.1005) MaximumBatchingWindowInSeconds: 0 to 300 s (1-second increments); default 0 s for streams and SQS; default 500 ms for MSK, self-managed Kafka and Amazon MQ. Once changed you cannot go back to the 500 ms default: you must create a new mapping
- [DATED][from source] (LAMBDA p.1005) Rule: on streams and SQS, if BatchSize > 10, MaximumBatchingWindowInSeconds must be >= 1 (repeated on p.1008 and p.1010)
- [DATED][p.1005-1006,1010] MaximumRecordAgeInSeconds (streams only): -1 to 604800 s, default -1 (infinite). MaximumRetryAttempts (streams only): -1 to 10000, default -1. ParallelizationFactor (streams only): 1 to 10, default 1 (default appears in the response, p.1010)
- [from source] (LAMBDA p.1006) ParallelizationFactor = number of batches processed concurrently per shard
- [DATED][from source] (LAMBDA p.1004) Enabled: default true; false pauses polling and invocation
- [from source] (LAMBDA p.1004) EventSourceArn per source: Kinesis = ARN of the stream or of a consumer; DynamoDB = stream ARN; SQS = queue; MSK = cluster; MQ = broker
- [DATED][from source] (LAMBDA p.1005) FunctionName: accepts name, ARN, version/alias ARN (e.g.: :PROD) or partial ARN; 1-140; only the name is limited to 64
- [DATED][from source] (LAMBDA p.1005) FunctionResponseTypes (streams and SQS): 0 to 1 item; the only valid value is ReportBatchItemFailures
- [DATED][p.1006-1007] Queues (Amazon MQ): exactly 1 item, 1-1000 characters. Topics (Kafka): exactly 1 item, 1-249 characters, pattern ^[^.]([a-zA-Z0-9\-_.]+) (does not start with a dot; p.1007)
- [DATED][from source] (LAMBDA p.1006) SourceAccessConfigurations: array of 0 to 22 items (authentication protocols/VPC components)
- [DATED][p.1006-1007] StartingPosition: required for Kinesis, DynamoDB and MSK; enum TRIM_HORIZON | LATEST | AT_TIMESTAMP; AT_TIMESTAMP only for Kinesis; StartingPositionTimestamp in Unix seconds
- [DATED][from source] (LAMBDA p.1007) TumblingWindowInSeconds (streams only): the text says range 1 to 900 s, but Valid Range lists min 0 and max 900 (slight inconsistency)
- [from source] (LAMBDA p.1008) Response includes UUID, FunctionArn, LastModified, LastProcessingResult, State, StateTransitionReason
- [DATED][from source] (LAMBDA p.1011) Mapping State: Creating, Enabling, Enabled, Disabling, Disabled, Updating, Deleting; StateTransitionReason indicates whether the user or Lambda made the last change
- [from source] (LAMBDA p.1009) BisectBatchOnFunctionError default false
- [DATED][from source] (LAMBDA p.1012) Errors: 400 Invalid, 409 Conflict, 404 NotFound, 500 Service, 429 TooMany (same pattern as CreateAlias)


## H. CreateFunction (p.1013-1025)
- [from source] (LAMBDA p.1013) To create you need a deployment package (zip or container image) and an execution role
- [from source] (LAMBDA p.1013) PackageType Image: Code must have the ECR image URI; Handler and Runtime are not needed. PackageType Zip: Code points to the zip; Handler and Runtime required; code compatible with the architecture (x86-64 or arm64), default x86-64
- [from source] (LAMBDA p.1013) On creation Lambda provisions the instance; with a VPC it can take about a minute, during which you cannot invoke or modify; check State/StateReason/StateReasonCode via GetFunctionConfiguration
- [from source] (LAMBDA p.1013) The unpublished version ($LATEST) changes with code/config; a published version is an immutable snapshot; an alias points to a version and can be repointed; Publish=true creates version 1. Function-level config (tags, per-function concurrency) applies to published and unpublished versions
- [from source] (LAMBDA p.1013) Code signing for zip only: provide the ARN of the code-signing config; UpdateFunctionCode checks for a valid signature from a trusted publisher
- [from source] (LAMBDA p.1013) Invokers from another account/service require AddPermission (resource-based policy); event sources use CreateEventSourceMapping or a trigger in the other service
- [DATED][from source] (LAMBDA p.1013) Route POST /2015-03-31/functions; response 201
- [DATED][p.1014-1015] Architectures: array of exactly 1 item; enum x86_64 | arm64; default x86_64
- [DATED][from source] (LAMBDA p.1015) Code (required): ImageUri, S3Bucket, S3Key, S3ObjectVersion, ZipFile (blob). CodeSigningConfigArn max 200, pattern ...:code-signing-config:csc-[a-z0-9]{17}
- [DATED][from source] (LAMBDA p.1015) EphemeralStorage.Size (/tmp): default 512 MB; any integer from 512 to 10,240 MB
- [DATED][from source] (LAMBDA p.1015) Description 0-256
- [DATED][from source] (LAMBDA p.1016) FileSystemConfigs (EFS): maximum 1 item. Handler: max 128, [^\s]+, required for zip only. ImageConfig overrides Dockerfile values (Command, EntryPoint, WorkingDirectory)
- [from source] (LAMBDA p.1016) KMSKeyArn encrypts environment variables; if omitted, Lambda uses the default service key
- [DATED][from source] (LAMBDA p.1017) Layers: each layer by ARN including the version; 1-140 characters per item
- [DATED][from source] (LAMBDA p.1017) MemorySize: default 128 MB; range 128 to 10240 (any multiple of 1 MB); more memory increases CPU
- [DATED][from source] (LAMBDA p.1017) PackageType enum: Zip | Image. Role (required): execution role ARN
- [DATED][from source] (LAMBDA p.1017) Runtime (valid enum, required for zip): nodejs, nodejs4.3, nodejs6.10, nodejs8.10, nodejs10.x, nodejs12.x, nodejs14.x, nodejs16.x, nodejs18.x, java8, java8.al2, java11, python2.7, python3.6, python3.7, python3.8, python3.9, dotnetcore1.0, dotnetcore2.0, dotnetcore2.1, dotnetcore3.1, dotnet6, nodejs4.3-edge, go1.x, ruby2.5, ruby2.7, provided, provided.al2 (the enum contains runtimes that have already been deprecated)
- [DATED][from source] (LAMBDA p.1018) Timeout: default 3 s; maximum 900 s; Valid Range lists only the minimum 1 (the maximum comes from the text)
- [from source] (LAMBDA p.1018) TracingConfig.Mode = Active samples and traces a subset of requests with X-Ray. VpcConfig: SecurityGroupIds + SubnetIds; a function in a VPC accesses resources and the internet only through that VPC
- [from source] (LAMBDA p.1018) SnapStart in the request: object with ApplyOn
- [from source] (LAMBDA p.1023) SnapStart: ApplyOn = PublishedVersions creates a snapshot of the initialized environment when a version is published
- [DATED][p.1020-1021] Response 201: Environment omitted from CloudTrail logs; CodeSize in bytes (Long); FunctionName in the response accepts up to 170 characters (pattern includes a dot) vs 140 in the request
- [from source] (LAMBDA p.1021) KMSKeyArn in the response is only returned if there is a customer-managed key; LastModified in ISO-8601
- [DATED][from source] (LAMBDA p.1021) LastUpdateStatus: Successful | Failed | InProgress (starts as Successful after creation)
- [DATED][from source] (LAMBDA p.1022) LastUpdateStatusReasonCode enum: EniLimitExceeded, InsufficientRolePermissions, InvalidConfiguration, InternalError, SubnetOutOfIPAddresses, InvalidSubnet, InvalidSecurityGroup, ImageDeleted, ImageAccessDenied, InvalidImage, KMSKeyAccessDenied, KMSKeyNotFound, InvalidStateKMSKey, DisabledKMSKey, EFSIOError, EFSMountConnectivityError, EFSMountFailure, EFSMountTimeout, InvalidRuntime, InvalidZipFileException, FunctionError
- [DATED][from source] (LAMBDA p.1023) State: Pending | Active | Inactive | Failed; in Inactive it can be reactivated by invoking. StateReasonCode (same enum as above plus Idle, Creating, Restoring); with Creating you cannot invoke or modify
- [from source] (LAMBDA p.1022) MasterArn: Lambda@Edge only, ARN of the main function
- [DATED][from source] (LAMBDA p.1024) CreateFunction-specific errors: CodeSigningConfigNotFoundException 404; CodeStorageExceededException 400 (account exceeded the total code size; see quotas); CodeVerificationFailedException 400 (signature failed validation on mismatch/expiry and policy = ENFORCE, deploy blocked); InvalidCodeSignatureException 400 (integrity failure blocks even with WARN policy); besides the standard 400/409/404/500/429


## I. CreateFunctionUrlConfig (p.1026-1029)
- [DATED][from source] (LAMBDA p.1026) Function URL = dedicated HTTP(S) endpoint; POST /2021-10-31/functions/FunctionName/url?Qualifier= ; Qualifier = alias name (1-128, pattern (^\$LATEST$)|((?!^[0-9]+$)([a-zA-Z0-9-_]+)))
- [DATED][from source] (LAMBDA p.1027) AuthType required: AWS_IAM restricts to authenticated IAM users; NONE bypasses IAM and creates a public endpoint; Cors optional (AllowCredentials, AllowHeaders, AllowMethods, AllowOrigins, ExposeHeaders, MaxAge); response 201
- [DATED][from source] (LAMBDA p.1028) Response: CreationTime (ISO-8601), FunctionArn, FunctionUrl (length 40-100); errors 400, 409, 404, 500, 429


## J. Delete* actions - standard and differences (p.1030-1050)
- [DATED][from source] (LAMBDA p.1030) Delete* PATTERN: no body; success = HTTP 204 with empty body (exception: DeleteEventSourceMapping returns 202 with the mapping object)
- [from source] (LAMBDA p.1030) DeleteAlias: DELETE /2015-03-31/functions/FunctionName/aliases/Name; errors 400, 409, 500, 429 (no 404)
- [DATED][from source] (LAMBDA p.1032) DeleteCodeSigningConfig: can only delete if no function uses it; DELETE /2020-04-22/code-signing-configs/CodeSigningConfigArn; errors 400, 409, 404, 500 (no 429)
- [DATED][from source] (LAMBDA p.1034) DeleteEventSourceMapping: the identifier (UUID) comes from ListEventSourceMappings; enters the Deleting state and can take several seconds; returns 202
- [DATED][from source] (LAMBDA p.1039) Own error ResourceInUseException (400): operation conflicts with the resource's availability, e.g. updating a mapping in CREATING or deleting a mapping in UPDATING
- [DATED][from source] (LAMBDA p.1040) DeleteFunction: with Qualifier deletes one version; without Qualifier deletes all versions and aliases. A version referenced by an alias cannot be deleted. Mappings require DeleteEventSourceMapping; triggers from other services are removed in the source service. Response 204
- [DATED][from source] (LAMBDA p.1042) DeleteFunctionCodeSigningConfig: DELETE /2020-06-30/functions/FunctionName/code-signing-config; 204; errors include CodeSigningConfigNotFoundException 404
- [DATED][from source] (LAMBDA p.1044) DeleteFunctionConcurrency: removes the per-function concurrency limit; DELETE /2017-10-31/functions/FunctionName/concurrency; 204
- [DATED][from source] (LAMBDA p.1046) DeleteFunctionEventInvokeConfig: removes the asynchronous invocation config of a function/version/alias; DELETE /2019-09-25/functions/FunctionName/event-invoke-config?Qualifier=
- [DATED][from source] (LAMBDA p.1048) DeleteFunctionUrlConfig: deletion is irreversible; creating a new URL results in a different address; DELETE /2021-10-31/functions/FunctionName/url?Qualifier=; errors 409, 404, 500, 429
- [DATED][from source] (LAMBDA p.1050) DeleteLayerVersion: deleted versions cannot be seen or added to functions; the copy remains until no function references it (so as not to break functions); DELETE /2018-10-31/layers/LayerName/versions/VersionNumber


## K. Delete/Get* (p.1052-1078) - provisioned concurrency, account, alias, code signing, ESM, function
- [DATED][from source] (LAMBDA p.1052) DeleteProvisionedConcurrencyConfig: DELETE /2019-09-30/functions/FunctionName/provisioned-concurrency?Qualifier= ; Qualifier REQUIRED (version or alias; 1-128); 204; errors 400, 409, 404, 500, 429
- [DATED][from source] (LAMBDA p.1054) GetAccountSettings: GET /2016-08-19/account-settings/ ; returns limits and usage in the Region: AccountLimit (CodeSizeUnzipped, CodeSizeZipped, ConcurrentExecutions, TotalCodeSize, UnreservedConcurrentExecutions) and AccountUsage (FunctionCount, TotalCodeSize); errors only 500 and 429
- [DATED][from source] (LAMBDA p.1056) GetAlias: GET /2015-03-31/functions/FunctionName/aliases/Name ; 200; returns AliasArn, FunctionVersion, RoutingConfig, RevisionId; errors 400, 404, 500, 429
- [DATED][from source] (LAMBDA p.1059) GetCodeSigningConfig: GET /2020-04-22/code-signing-configs/CodeSigningConfigArn; errors 400, 404, 500
- [DATED][from source] (LAMBDA p.1061) GetEventSourceMapping: GET /2015-03-31/event-source-mappings/UUID (UUID comes from ListEventSourceMappings); 200; same fields/limits as Create (BatchSize 1-10000, window 0-300, etc.; repeated p.1062-1065); errors 400, 404, 500, 429
- [DATED][from source] (LAMBDA p.1067) GetFunction: returns function/version info with a package download link valid for 10 minutes; if a version is given, only version-specific details; the response has Code (ImageUri, Location, RepositoryType, ResolvedImageUri), Concurrency (ReservedConcurrentExecutions), Configuration, Tags; FunctionName accepts 1-170
- [DATED][from source] (LAMBDA p.1071) GetFunctionCodeSigningConfig: GET /2020-06-30/functions/FunctionName/code-signing-config; returns CodeSigningConfigArn and FunctionName
- [DATED][p.1074-1075] GetFunctionConcurrency: GET /2019-09-30/functions/FunctionName/concurrency (different path version from Delete, which uses /2017-10-31/); returns ReservedConcurrentExecutions (integer, min 0)
- [DATED][from source] (LAMBDA p.1076) GetFunctionConfiguration: returns only version-specific settings (those that vary between versions); for everything, including function level, use GetFunction; GET /2015-03-31/functions/FunctionName/configuration?Qualifier=; FunctionName 1-170

- [p.1078-1082] GetFunctionConfiguration repeats in the response the same fields/enums/limits as CreateFunction (Architectures, EphemeralStorage 512-10,240, MemorySize 128-10240, Runtime enum, State, StateReasonCode, Timeout min 1, Version 1-1024); errors 400, 404, 500, 429


## L. Async config, URL, Layers, Policy, Provisioned concurrency (Get*)
- [DATED][p.1084-1085] GetFunctionEventInvokeConfig: GET /2019-09-25/functions/FunctionName/event-invoke-config?Qualifier=; returns DestinationConfig, MaximumEventAgeInSeconds, MaximumRetryAttempts, FunctionArn, LastModified
- [DATED][from source] (LAMBDA p.1085) MaximumEventAgeInSeconds: maximum age of a request sent to the function; range 60 to 21600 s (6 h). MaximumRetryAttempts (asynchronous invocation): 0 to 2
- [from source] (LAMBDA p.1085) Valid asynchronous destinations: function (Lambda ARN), SQS queue, SNS topic, EventBridge event bus
- [DATED][p.1087-1088] GetFunctionUrlConfig: GET /2021-10-31/functions/FunctionName/url?Qualifier=; response includes LastModifiedTime (Create does not have it)
- [DATED][from source] (LAMBDA p.1090) GetLayerVersion: returns layer version info with a download link valid for 10 minutes; GET /2018-10-31/layers/LayerName/versions/VersionNumber
- [DATED][p.1091-1092] Layer response: CompatibleArchitectures max 2 items (x86_64 | arm64); CompatibleRuntimes max 15 items (same enum as Runtime); Description 0-256; LayerArn/LayerVersionArn 1-140; LicenseInfo max 512; Version Long
- [DATED][from source] (LAMBDA p.1093) GetLayerVersionByArn: GET /2018-10-31/layers?find=LayerVersion&Arn=Arn (query by version ARN); same response
- [DATED][from source] (LAMBDA p.1096) GetLayerVersionPolicy: GET .../layers/LayerName/versions/VersionNumber/policy; returns Policy and RevisionId
- [DATED][from source] (LAMBDA p.1098) GetPolicy: returns the resource-based IAM policy of a function/version/alias; GET /2015-03-31/functions/FunctionName/policy?Qualifier=; Policy + RevisionId
- [DATED][p.1100-1101] GetProvisionedConcurrencyConfig: Qualifier required; response: AllocatedProvisionedConcurrentExecutions (min 0; fluctuates during linear/canary deploy with a weighted alias), AvailableProvisionedConcurrentExecutions (min 0), RequestedProvisionedConcurrentExecutions (min 1), Status enum IN_PROGRESS | READY | FAILED, StatusReason (for failures), LastModified
- [DATED][from source] (LAMBDA p.1102) Own error: ProvisionedConcurrencyConfigNotFoundException 404


## M. Invoke (p.1103-1108) - InvocationType, LogType, status codes and errors
- [from source] (LAMBDA p.1103) Invoke can be synchronous (waits for the response) or asynchronous with InvocationType=Event; in synchronous mode, response details and errors come in the body and headers; in both there is an execution log and trace
- [DATED][from source] (LAMBDA p.1103) Retries vary by error type, client, event source and invocation type; in an asynchronous invocation with an error, Lambda runs the function up to TWO more times
- [from source] (LAMBDA p.1103) Asynchronous invocation: events enter a queue before going to the function; if capacity does not keep up, events may be lost; the same delivery may occur more than once even without error; to retain unprocessed ones, configure a dead-letter queue
- [from source] (LAMBDA p.1103) The API status code does NOT reflect function errors; error codes are reserved for what prevents execution (permissions, quotas, code/config). TooManyRequestsException occurs when exceeding the account's concurrency (ConcurrentInvocationLimitExceeded) or the function's (ReservedFunctionConcurrentInvocationLimitExceeded)
- [from source] (LAMBDA p.1103) Function with a long timeout: the client may disconnect in synchronous mode; configure the HTTP client/SDK/firewall/proxy/OS for long connections (timeout or keep-alive)
- [from source] (LAMBDA p.1103) Requires the lambda:InvokeFunction permission
- [DATED][from source] (LAMBDA p.1103) POST /2015-03-31/functions/FunctionName/invocations?Qualifier=; headers X-Amz-Invocation-Type, X-Amz-Log-Type, X-Amz-Client-Context; ClientContext: up to 3,583 bytes of base64 data for the context object
- [DATED][from source] (LAMBDA p.1104) InvocationType enum: RequestResponse (default; synchronous, connection open until response or timeout), Event (asynchronous; repeated failures go to the DLQ if there is one; response carries only the status), DryRun (validates parameters and permission without executing)
- [DATED][from source] (LAMBDA p.1104) LogType enum: None | Tail; Tail includes the execution log in the response, for synchronous invocation only
- [from source] (LAMBDA p.1104) Payload: input JSON, direct (--payload '{...}') or file (file://payload.json)
- [DATED][from source] (LAMBDA p.1105) Success status: 200 for RequestResponse, 202 for Event, 204 for DryRun
- [DATED][from source] (LAMBDA p.1105) Response headers: X-Amz-Executed-Version (version executed; with an alias shows the resolved version; 1-1024), X-Amz-Function-Error (presence indicates an execution error; details in the payload), X-Amz-Log-Result (last 4 KB of the log, base64)
- [DATED][p.1105-1108] Invoke errors and HTTP: EC2AccessDeniedException 502; EC2ThrottledException 502; EC2UnexpectedException 502; EFSIOException 410; EFSMountConnectivityException 408; EFSMountFailureException 403; EFSMountTimeoutException 408; ENILimitReachedException 502; InvalidParameterValueException 400; InvalidRequestContentException 400 (body is not JSON); InvalidRuntimeException 502; InvalidSecurityGroupIDException 502; InvalidSubnetIDException 502; InvalidZipFileException 502; KMSAccessDeniedException 502; KMSDisabledException 502; KMSInvalidStateException 502; KMSNotFoundException 502; RequestTooLargeException 413 (payload above the Invoke JSON body quota); ResourceConflictException 409; ResourceNotFoundException 404; ResourceNotReadyException 502 (function inactive and VPC connection unavailable; wait and try again); ServiceException 500; SnapStartException 400; SnapStartNotReadyException 409 (wait for Active state); SnapStartTimeoutException 408 (restore hook exceeded 2 seconds); SubnetIPAddressLimitReachedException 502; TooManyRequestsException 429; UnsupportedMediaTypeException 415 (content-type not JSON)
- [p.1105-1107] VPC/EFS/KMS failures appear as invocation errors (502/4xx) - guidance from the text: check KMS permissions, key state, subnet/security group configuration
- [DATED][from source] (LAMBDA p.1109) InvokeAsync: DEPRECATED; use Invoke for asynchronous invocation; POST /2014-11-13/functions/FunctionName/invoke-async/; errors 400, 502, 409, 404, 500
- [DATED][from source] (LAMBDA p.1111) ListAliases: GET /2015-03-31/functions/FunctionName/aliases?FunctionVersion=&Marker=&MaxItems= ; MaxItems 1 to 10000; Marker = pagination token


## N. List* actions - pagination pattern and MaxItems limits
- [DATED][p.1111-1112] List* PATTERN: parameters Marker (pagination token returned by a previous call) and MaxItems; the response carries NextMarker when there are more results
- [DATED][from source] (LAMBDA p.1114) ListCodeSigningConfigs: GET /2020-04-22/code-signing-configs/?Marker=&MaxItems=; up to 10,000 configs per call; MaxItems 1-10000; errors only 400 and 500
- [DATED][from source] (LAMBDA p.1116) ListEventSourceMappings: filters EventSourceArn and FunctionName; MaxItems 1-10000, but the service returns at most 100 items per response even if you ask for more
- [DATED][from source] (LAMBDA p.1120) ListFunctionEventInvokeConfigs: GET /2019-09-25/functions/FunctionName/event-invoke-config/list; MaxItems 1-50
- [DATED][from source] (LAMBDA p.1123) ListFunctions: up to 50 functions per call, with version-specific config; FunctionVersion=ALL (only valid value) includes published versions besides the unpublished one; MasterRegion (Lambda@Edge) requires FunctionVersion=ALL; MaxItems 1-10000 but maximum 50 per response; note: returns a subset of the fields (State, StateReasonCode, StateReason, LastUpdateStatus* only via GetFunction)
- [DATED][from source] (LAMBDA p.1127) ListFunctionsByCodeSigningConfig: lists functions that use the config; useful before deleting the config; MaxItems 1-10000
- [DATED][from source] (LAMBDA p.1129) ListFunctionUrlConfigs: GET /2021-10-31/functions/FunctionName/urls; MaxItems 1-50 (maximum 50 per response)
- [DATED][from source] (LAMBDA p.1132) ListLayers: shows the latest version of each layer; filters CompatibleRuntime (same enum as Runtime) and CompatibleArchitecture (x86_64 | arm64); MaxItems 1-50
- [DATED][from source] (LAMBDA p.1135) ListLayerVersions: deleted versions are not listed; same filters; MaxItems 1-50
- [DATED][from source] (LAMBDA p.1138) ListProvisionedConcurrencyConfigs: GET /2019-09-30/functions/FunctionName/provisioned-concurrency?List=ALL&Marker=&MaxItems=; MaxItems 1-50
- [DATED][from source] (LAMBDA p.1141) ListTags: GET /2017-03-31/tags/ARN; Lambda does NOT support tags on aliases or versions (functions only); also visible via GetFunction
- [DATED][from source] (LAMBDA p.1143) ListVersionsByFunction: up to 50 versions per call; MaxItems 1-10000 but maximum 50 per response; FunctionName 1-170
- [p.1111-1143] Summary of response ceilings: ESM 100/response; functions, versions and URLs 50/response; layers, layer versions, provisioned concurrency, event invoke configs: MaxItems max 50; aliases, code signing configs, functions-by-CSC: max 10000


## O. PublishLayerVersion (p.1147-1149+)
- [DATED][from source] (LAMBDA p.1147) Creates a layer from a ZIP; each call with the same name creates a new version; add layers via CreateFunction or UpdateFunctionConfiguration; POST /2018-10-31/layers/LayerName/versions; response 201
- [DATED][p.1147-1148] Content required (S3Bucket, S3Key, S3ObjectVersion, ZipFile); CompatibleArchitectures max 2 (x86_64 | arm64); CompatibleRuntimes max 15 (same enum as Runtime; used to filter in ListLayers/ListLayerVersions); Description 0-256; LicenseInfo max 512 (SPDX identifier, license URL or full text)

- [DATED][p.1149-1150] PublishLayerVersion response 201 repeats CompatibleArchitectures/Runtimes; own error CodeStorageExceededException 400 (account's total code limit); no 409


## P. PublishVersion (p.1152-1159)
- [from source] (LAMBDA p.1152) Creates a version from the current code and config (immutable snapshot). Lambda does NOT publish a new version if code and config have not changed since the last version; update first with UpdateFunctionCode/UpdateFunctionConfiguration. Clients invoke versions directly or via an alias
- [DATED][p.1152-1153] POST /2015-03-31/functions/FunctionName/versions; optional body: CodeSha256 (publishes only if the hash matches; avoids publishing if the code changed), Description (0-256; overrides the config description), RevisionId (publishes only if the revision matches); response 201 with the version configuration
- [DATED][from source] (LAMBDA p.1159) Errors: CodeStorageExceededException 400; InvalidParameterValueException 400; PreconditionFailedException 412; ResourceConflictException 409; ResourceNotFoundException 404; ServiceException 500; TooManyRequestsException 429


## Q. Put* (concurrency, code signing, async config, provisioned)
- [DATED][from source] (LAMBDA p.1161) PutFunctionCodeSigningConfig: PUT /2020-06-30/functions/FunctionName/code-signing-config; changes take effect the next time someone tries to deploy a package to the function (does not revalidate already deployed code); 200
- [DATED][from source] (LAMBDA p.1164) PutFunctionConcurrency: sets the maximum simultaneous executions AND reserves that capacity; applies to the whole function (all published versions and the unpublished one); reserving guarantees capacity and prevents scaling beyond that level; you can reserve for as many functions as you like as long as at least 100 unreserved simultaneous executions remain for functions without their own limit; GetAccountSettings shows the regional limit; PUT /2017-10-31/functions/FunctionName/concurrency; ReservedConcurrentExecutions required, min 0 (0 = no executions, effectively blocks the function [extrapolation])
- [DATED][from source] (LAMBDA p.1167) PutFunctionEventInvokeConfig: configures asynchronous invocation of a function/version/alias; if a config already exists, it OVERWRITES and omitted settings are removed (to change only one option without affecting the others use UpdateFunctionEventInvokeConfig)
- [DATED][from source] (LAMBDA p.1167) Asynchronous default: Lambda retries TWICE if the function returns an error; retains events in a queue for up to SIX hours; an event that fails all attempts or stays too long is discarded; to retain discarded ones configure a DLQ via UpdateFunctionConfiguration; on-success and on-failure destinations can be configured, in addition to or instead of the DLQ
- [DATED][from source] (LAMBDA p.1168) Destinations (Function, SQS Queue, SNS Topic, EventBridge Event Bus); MaximumEventAgeInSeconds 60-21600; MaximumRetryAttempts 0-2; PUT /2019-09-25/functions/FunctionName/event-invoke-config?Qualifier=
- [DATED][p.1171-1172] PutProvisionedConcurrencyConfig: adds provisioned concurrency to an alias or version; Qualifier REQUIRED; ProvisionedConcurrentExecutions required, min 1; response HTTP 202 (asynchronous allocation; track Status IN_PROGRESS | READY | FAILED); PUT /2019-09-30/functions/FunctionName/provisioned-concurrency?Qualifier=
- [extrapolation] Provisioned concurrency cannot be configured on $LATEST (the text only says "alias or version").


## R. Remove*/Tag/Untag
- [DATED][from source] (LAMBDA p.1174) RemoveLayerVersionPermission: DELETE .../layers/LayerName/versions/VersionNumber/policy/StatementId?RevisionId=; 204; errors 400, 412, 404, 500, 429 (no 409)
- [DATED][from source] (LAMBDA p.1176) RemovePermission: revokes permission to use for a service or account; StatementId obtained via GetPolicy; StatementId 1-100 with a pattern that accepts a dot ([a-zA-Z0-9-_.]+), unlike Add (no dot); Qualifier optional; RevisionId optional; 204
- [DATED][p.1178,1180] TagResource: POST /2017-03-31/tags/ARN; Tags required (map string->string); 204; Untag: DELETE /2017-03-31/tags/ARN?tagKeys=; both use the function ARN (without version/alias)


## S. UpdateAlias (p.1182-)
- [DATED][p.1182-1183] PUT /2015-03-31/functions/FunctionName/aliases/Name; optional fields: Description (0-256), FunctionVersion (1-1024), RevisionId (updates only if it matches), RoutingConfig; response 200

- [DATED][from source] (LAMBDA p.1184) UpdateAlias errors: 400, 412 (RevisionId does not match), 409, 404, 500, 429


## T. UpdateCodeSigningConfig (p.1186)
- [DATED][from source] (LAMBDA p.1186) PUT /2020-04-22/code-signing-configs/CodeSigningConfigArn; AllowedPublishers, CodeSigningPolicies, Description (0-256) optional; changes apply at the next deployment; 200; errors 400, 404, 500


## U. UpdateEventSourceMapping (p.1189-1198)
- [DATED][from source] (LAMBDA p.1189) Updates the mapping: can change the invoked function or pause invocation and resume later from the same point; PUT /2015-03-31/event-source-mappings/UUID; response 202
- [p.1189-1193] Updatable parameters: BatchSize, BisectBatchOnFunctionError, DestinationConfig, Enabled, FilterCriteria, FunctionName, FunctionResponseTypes, MaximumBatchingWindowInSeconds, MaximumRecordAgeInSeconds, MaximumRetryAttempts, ParallelizationFactor, SourceAccessConfigurations, TumblingWindowInSeconds. NOT updatable (absent from the body): EventSourceArn, StartingPosition, StartingPositionTimestamp, Queues, Topics, SelfManagedEventSource, Kafka configs
- [DATED][p.1190-1193] Limits identical to Create (BatchSize 1-10000 with defaults per source; window 0-300 s; RecordAge -1..604800; RetryAttempts -1..10000; Parallelization 1-10; Tumbling 0-900; SourceAccessConfigurations max 22; FunctionResponseTypes max 1); same rule that BatchSize>10 requires window>=1 and the impossibility of returning to the 500 ms default
- [DATED][from source] (LAMBDA p.1197) Errors: 400, 409, ResourceInUseException 400 (e.g.: updating a mapping in CREATING), 404, 500, 429


## V. UpdateFunctionCode (p.1199-1208)
- [from source] (LAMBDA p.1199) Updates the code; with code signing enabled the package must be signed by a trusted publisher; Image: ImageUri of an ECR image; Zip: S3 bucket+key or inline ZipFile; compatible with the architecture
- [from source] (LAMBDA p.1199) Code is locked when a version is published: only the unpublished version can be modified
- [from source] (LAMBDA p.1199) Note: for a container image Lambda resolves the tag to a digest; updating the tag in ECR does NOT update the function automatically
- [DATED][p.1199-1201] PUT /2015-03-31/functions/FunctionName/code; Architectures (1 item, x86_64|arm64), DryRun (validates parameters and permissions without modifying), Publish (equivalent to PublishVersion), RevisionId, S3Bucket (same Region as the function, can be from another account; 3-63 characters), S3Key (1-1024), S3ObjectVersion (1-1024), ZipFile (base64; SDK/CLI encode), ImageUri (do not use with zip)
- [DATED][from source] (LAMBDA p.1207) Errors: CodeSigningConfigNotFoundException 404, CodeStorageExceededException 400, CodeVerificationFailedException 400 (ENFORCE), InvalidCodeSignatureException 400 (even with WARN), 400, PreconditionFailed 412, 409, 404, 500, 429. Response 200


## W. UpdateFunctionConfiguration (p.1209-)
- [from source] (LAMBDA p.1209) Modifies version-specific settings; Lambda reprovisions the instance; with a VPC it can take about a minute, during which you can NOT modify the function but you CAN still invoke it (unlike CreateFunction, which blocks invoking); LastUpdateStatus* from GetFunctionConfiguration indicate when it finished
- [from source] (LAMBDA p.1209) Version config is locked when published: only the unpublished version is modifiable; concurrency via PutFunctionConcurrency; permissions via AddPermission
- [DATED][p.1209-1213] PUT /2015-03-31/functions/FunctionName/configuration; fields: DeadLetterConfig, Description (0-256), Environment, EphemeralStorage (512-10,240 MB, default 512), FileSystemConfigs (max 1), Handler (max 128), ImageConfig, KMSKeyArn, Layers (by ARN with version), MemorySize (128-10240, default 128), RevisionId, Role, Runtime (same enum; required for zip), SnapStart, Timeout (default 3, max 900), TracingConfig, VpcConfig; response 200
- [from source] (LAMBDA p.1209) PackageType and Architectures cannot be changed through UpdateFunctionConfiguration (absent from the body; Architectures changes via UpdateFunctionCode)

- [DATED][p.1214-1219] UpdateFunctionConfiguration response 200 repeats the CreateFunction fields; errors: CodeSigningConfigNotFoundException 404, CodeVerificationFailedException 400, InvalidCodeSignatureException 400, 400, 412, 409, 404, 500, 429 (no CodeStorageExceeded)


## X. UpdateFunctionEventInvokeConfig and UpdateFunctionUrlConfig
- [DATED][from source] (LAMBDA p.1221) UpdateFunctionEventInvokeConfig: uses POST (not PUT) at /2019-09-25/functions/FunctionName/event-invoke-config?Qualifier=; updates only the fields sent (vs Put, which overwrites everything); same limits (age 60-21600, retries 0-2); 200; errors 400, 409, 404, 500, 429
- [DATED][from source] (LAMBDA p.1225) UpdateFunctionUrlConfig: PUT /2021-10-31/functions/FunctionName/url?Qualifier=; AuthType and Cors optional; 200


## Y. Data Types (p.1228-1297)
- [p.1228-1229] Types listed: AccountLimit, AccountUsage, AliasConfiguration, AliasRoutingConfiguration, AllowedPublishers, AmazonManagedKafkaEventSourceConfig, CodeSigningConfig, CodeSigningPolicies, Concurrency, Cors, DeadLetterConfig, DestinationConfig, Environment, EnvironmentError, EnvironmentResponse, EphemeralStorage, EventSourceMappingConfiguration, FileSystemConfig, Filter, FilterCriteria, FunctionCode, FunctionCodeLocation, FunctionConfiguration, FunctionEventInvokeConfig, FunctionUrlConfig, ImageConfig, ImageConfigError, ImageConfigResponse, Layer, LayersListItem, LayerVersionContentInput/Output, LayerVersionsListItem, OnFailure, OnSuccess, ProvisionedConcurrencyConfigListItem, SelfManagedEventSource, SelfManagedKafkaEventSourceConfig, SnapStart, SnapStartResponse, SourceAccessConfiguration, TracingConfig, TracingConfigResponse, VpcConfig, VpcConfigResponse
- [DATED][from source] (LAMBDA p.1230) AccountLimit (sizes in bytes): CodeSizeUnzipped (maximum of the extracted package + layers), CodeSizeZipped (maximum of a package uploaded directly; for larger ones use S3), ConcurrentExecutions, TotalCodeSize (storage for all packages and layers), UnreservedConcurrentExecutions (total minus what is reserved by PutFunctionConcurrency; min 0)
- [from source] (LAMBDA p.1231) AccountUsage: FunctionCount and TotalCodeSize (bytes in use)
- [DATED][from source] (LAMBDA p.1234) AliasRoutingConfiguration.AdditionalVersionWeights: map version->weight (double) between 0.0 and 1.0; key 1-1024 with pattern [0-9]+ (numeric versions only, not $LATEST); the "second version" is the percentage of traffic
- [DATED][from source] (LAMBDA p.1235) AllowedPublishers.SigningProfileVersionArns: 1 to 20 items, required
- [DATED][from source] (LAMBDA p.1236) AmazonManagedKafkaEventSourceConfig.ConsumerGroupId: 1-200 characters, pattern [a-zA-Z0-9-\/*:_+=.@-]*; must be unique across all Kafka event sources; cannot be updated after the mapping is created
- [DATED][from source] (LAMBDA p.1237) CodeSigningConfig: AllowedPublishers, Arn (max 200), Id pattern csc-[a-zA-Z0-9-_\.]{17}, Policies, Description 0-256, LastModified
- [DATED][from source] (LAMBDA p.1239) CodeSigningPolicies.UntrustedArtifactOnDeployment: enum Warn | Enforce; DEFAULT Warn; Enforce blocks the deploy if signature validation fails; Warn allows the deploy and creates a CloudWatch log
- [from source] (LAMBDA p.1239) Note from the text: in the API errors the value appears as ENFORCE/WARN in uppercase, and here as Enforce/Warn (enum spelling on this page)
- [DATED][from source] (LAMBDA p.1240) Concurrency.ReservedConcurrentExecutions min 0
- [DATED][p.1241-1242] Cors (function URL): AllowCredentials default false; AllowHeaders max 100 items of up to 1024 characters; AllowMethods max 6 items, each up to 6 characters (GET, POST, DELETE or *); AllowOrigins max 100 items, 1-253 characters (specific origins or *); ExposeHeaders max 100 items of up to 1024; MaxAge 0-86400 s, default 0 (browser does not cache the preflight result)
- [from source] (LAMBDA p.1243) DeadLetterConfig.TargetArn: ARN of an SQS queue or SNS topic
- [from source] (LAMBDA p.1244) DestinationConfig: OnFailure and OnSuccess
- [DATED][from source] (LAMBDA p.1245) Environment.Variables: map string->string; the key must match [a-zA-Z]([a-zA-Z0-9_])+ (starts with a letter, minimum 2 characters, only letters/numbers/_); values are kept in the version-specific config
- [p.1246-1247] EnvironmentError (ErrorCode, Message) and EnvironmentResponse (Error or Variables; Variables omitted from CloudTrail)
- [DATED][from source] (LAMBDA p.1248) EphemeralStorage.Size: required, 512 to 10240 MB
- [p.1249-1253] EventSourceMappingConfiguration repeats in full the fields and limits of CreateEventSourceMapping (BatchSize 1-10000; window 0-300; RecordAge -1..604800; RetryAttempts -1..10000; Parallelization 1-10; Tumbling 0-900; SourceAccessConfigurations max 22)
- [DATED][from source] (LAMBDA p.1254) FileSystemConfig: Arn of the EFS ACCESS POINT (pattern ...access-point/fsap-[a-f0-9]{17}, max 200), required; LocalMountPath required, starts with /mnt/, max 160, ^/mnt/[a-zA-Z0-9-_.]+$
- [DATED][from source] (LAMBDA p.1255) Filter.Pattern: 0-4096 characters; syntax in "Filter rule syntax"; FilterCriteria.Filters: list of Filter
- [DATED][from source] (LAMBDA p.1257) FunctionCode: ImageUri, S3Bucket (3-63; same Region; can be from another account), S3Key (1-1024), S3ObjectVersion (1-1024), ZipFile base64
- [from source] (LAMBDA p.1259) FunctionCodeLocation: ImageUri and Location (pre-signed URL to download the package)

- [p.1260-1265] FunctionConfiguration (type) repeats the same fields, enums and limits as the CreateFunction response (Architectures, EphemeralStorage, MemorySize 128-10240, Runtime enum, State/StateReasonCode, Timeout min 1); no required fields
- [DATED][from source] (LAMBDA p.1266) FunctionEventInvokeConfig: DestinationConfig, FunctionArn, LastModified, MaximumEventAgeInSeconds 60-21600, MaximumRetryAttempts 0-2
- [DATED][from source] (LAMBDA p.1268) FunctionUrlConfig: AuthType, CreationTime, FunctionArn, FunctionUrl (40-100), LastModifiedTime required; Cors optional
- [DATED][from source] (LAMBDA p.1270) ImageConfig (overrides the Dockerfile): Command (max 1500 items, parameters for the ENTRYPOINT), EntryPoint (max 1500 items), WorkingDirectory (max 1000 characters)
- [p.1271-1272] ImageConfigError/ImageConfigResponse: GetFunctionConfiguration responses with Error (ErrorCode, Message) and ImageConfig
- [DATED][from source] (LAMBDA p.1273) Layer (in a function): Arn (1-140, with version), CodeSize (bytes), SigningJobArn, SigningProfileVersionArn
- [from source] (LAMBDA p.1274) LayersListItem: LatestMatchingVersion, LayerArn, LayerName (1-140)
- [DATED][from source] (LAMBDA p.1275) LayerVersionContentInput: S3Bucket (3-63), S3Key (1-1024), S3ObjectVersion (1-1024) or ZipFile base64
- [DATED][from source] (LAMBDA p.1276) LayerVersionContentOutput: CodeSha256, CodeSize, Location = S3 link valid for 10 minutes
- [DATED][from source] (LAMBDA p.1277) LayerVersionsListItem: CompatibleArchitectures max 2, CompatibleRuntimes max 15, CreatedDate ISO 8601, LicenseInfo max 512
- [DATED][p.1279-1280] OnFailure and OnSuccess: Destination = destination ARN, 0-350 characters
- [DATED][from source] (LAMBDA p.1281) ProvisionedConcurrencyConfigListItem: Allocated (min 0), Available (min 0), Requested (min 1), Status IN_PROGRESS | READY | FAILED, StatusReason
- [DATED][from source] (LAMBDA p.1283) SelfManagedEventSource.Endpoints: map with at most 2 entries; the only valid key is KAFKA_BOOTSTRAP_SERVERS; list of 1 to 10 host:port servers, each 1-300 characters
- [DATED][from source] (LAMBDA p.1284) SelfManagedKafkaEventSourceConfig.ConsumerGroupId: 1-200; unique across Kafka sources; immutable after creation
- [DATED][from source] (LAMBDA p.1285) SnapStart: ApplyOn enum PublishedVersions | None; the page text states that SnapStart is supported with the java11 runtime ([DATED] limitation of this edition)
- [DATED][from source] (LAMBDA p.1286) SnapStartResponse: ApplyOn and OptimizationStatus (On | Off), the latter reported only when a qualified ARN (version) is provided
- [DATED][from source] (LAMBDA p.1287) SourceAccessConfiguration.Type (enum): BASIC_AUTH | VPC_SUBNET | VPC_SECURITY_GROUP | SASL_SCRAM_512_AUTH | SASL_SCRAM_256_AUTH | VIRTUAL_HOST | CLIENT_CERTIFICATE_TLS_AUTH | SERVER_ROOT_CA_CERTIFICATE. Meanings: BASIC_AUTH (MQ: Secrets Manager secret with broker credentials; self-managed Kafka: SASL/PLAIN secret); VPC_SUBNET and VPC_SECURITY_GROUP (self-managed Kafka: where Lambda connects and SG for access to the brokers); SASL_SCRAM_256_AUTH (self-managed Kafka) and SASL_SCRAM_512_AUTH (MSK and self-managed); VIRTUAL_HOST (RabbitMQ; CANNOT be specified in UpdateEventSourceMapping); CLIENT_CERTIFICATE_TLS_AUTH (MSK/Kafka: X.509 PEM chain, PKCS#8 PEM key, optional password, for mutual TLS); SERVER_ROOT_CA_CERTIFICATE (self-managed Kafka: X.509 PEM root CA). URI: 1-200 characters
- [DATED][p.1289-1290] TracingConfig/TracingConfigResponse.Mode: Active | PassThrough
- [DATED][p.1291-1292] VpcConfig: SecurityGroupIds up to 5 items; SubnetIds up to 16 items; VpcConfigResponse adds VpcId


## Z. Common errors (all AWS actions) and common parameters (p.1292-1296)
- [p.1292-1293] Certificate errors in SDKs: SDKs use the computer's CAs; keep CAs and OS updated; clients must trust Amazon Root CA 1, Starfield Services Root CA - G2 or Starfield Class 2 CA (minimum OS/Java list in the text)
- [DATED][p.1293-1294] Common Errors (HTTP): AccessDeniedException 400; IncompleteSignature 400; InternalFailure 500; InvalidAction 400; InvalidClientTokenId 403; InvalidParameterCombination 400; InvalidParameterValue 400; InvalidQueryParameter 400; MalformedQueryString 404; MissingAction 400; MissingAuthenticationToken 403; MissingParameter 400; NotAuthorized 400; OptInRequired 403; RequestExpired 400; ServiceUnavailable 503; ThrottlingException 400; ValidationError 400
- [DATED][from source] (LAMBDA p.1294) RequestExpired: the request arrived more than 15 minutes after the date stamp, or after the expiry (e.g. pre-signed URLs), or the stamp is more than 15 minutes in the future
- [DATED][from source] (LAMBDA p.1295) Common Parameters (SigV4 in query string): Action, Version (YYYY-MM-DD), X-Amz-Algorithm (AWS4-HMAC-SHA256), X-Amz-Credential (access_key/YYYYMMDD/region/service/aws4_request), X-Amz-Date (ISO 8601 basic, e.g. 20120325T120000Z; overrides the Date header), X-Amz-Security-Token (required with temporary STS credentials), X-Amz-Signature, X-Amz-SignedHeaders
- [from source] (LAMBDA p.1297) Last page: AWS glossary only referenced


## Contradictions, inconsistencies and gaps in the text
- [from source] (LAMBDA p.1018) Timeout: Valid Range lists only min 1 and omits the maximum; the maximum (900 s) is only in the description; in the remaining pages (responses) the max is not repeated
- [from source] (LAMBDA p.1007) TumblingWindowInSeconds: the description says "1 to 900" but Valid Range allows 0
- [from source] (LAMBDA p.1003) BatchSize described as 'max 10,000' for standard SQS, 10 for FIFO, but general Valid Range 1-10000 (the FIFO restriction is only in the text)
- [p.1017 vs 1020] FunctionName: request 1-140 (full ARN only), response and GetFunction/GetFunctionConfiguration/Invoke/GetPolicy/ListVersionsByFunction accept 1-170 with a dot allowed in the name (pattern with \.)
- [p.1239 vs p.1024] UntrustedArtifactOnDeployment appears as Warn|Enforce in the type but the errors cite ENFORCE/WARN
- [from source] (LAMBDA p.1285) The text of this edition says SnapStart only with java11; the Runtime enum includes java8.al2 and java11 but there are no Python/.NET runtimes with SnapStart
- [from source] (LAMBDA p.1017) The Runtime enum of this edition includes runtimes that are already obsolete (nodejs, nodejs4.3, nodejs4.3-edge, python2.7, dotnetcore1.0/2.0/2.1, ruby2.5 etc.); the enum does not include python3.10/ruby3.x/java17 (edition of 2022-11-28; last value listed nodejs18.x)
- [NOT COVERED] This section does NOT document: maximum reserved concurrency per function (only min 0 and the rule of 100 unreserved on p.1164); quota values (6 MB of synchronous payload appears only in BatchSize p.1003; Invoke body limit cited as "quota" with no number, p.1107); maximum sizes of environment variables; layers-per-function limit; retry policies per source beyond what is in the fields; max Timeout outside CreateFunction/UpdateFunctionConfiguration
- [extrapolation] External knowledge (not on these pages): limit of 5 layers per function, 6 MB synchronous request/response, 256 KB asynchronous, 50 MB direct zip / 250 MB unzipped, default concurrency of 1000 per region.


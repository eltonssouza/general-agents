# Troubleshooting

> Deployment, invocation, execution, network and image errors.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the reference text is unaccented because the original reading notes were written that way.

## Troubleshooting: deployment
- [from source] (LAMBDA p.828) Deployment errors prevent use of the new version (package, code, permissions or tools); via API/CLI the error appears in the output; via CloudFormation/CodeDeploy/CodePipeline look in the service's log/event stream
- [from source] (LAMBDA p.828) "Permission denied / Cannot load such file" (EACCES /var/task/index.js; Errno 13): the runtime needs read access to the package files; fix with chmod -R o+rX .
- [p.828-829] RequestEntityTooLargeException in UpdateFunctionCode: [DATED] direct ZIP upload (package or layer) limited to 50 MB; above that use S3 (S3Bucket and S3Key parameters); direct upload converts to base64 (+~30%), so the 50 MB limit is approximate
- [from source] (LAMBDA p.829) S3 PermanentRedirect: the package bucket must be in the SAME Region as the function (UpdateFunctionCode, aws package/deploy, SAM); create one artifact bucket per Region
- [from source] (LAMBDA p.829) "Cannot find / cannot load / unable to import / class not found / no such file or directory": the file or class name in the handler configuration does not match the code
- [p.829-830] "Undefined method handler" (index.handler is undefined or not exported; Handler missing on module; No public method named handleRequest...): the handler method name does not match; each runtime has a convention (filename.methodname); some languages have a library that requires a method with a specific name
- [from source] (LAMBDA p.830) InvalidParameterValueException / RequestEntityTooLargeException on environment variables: [DATED] variables object limited to 4096 bytes (includes keys, values, quotes, commas, object braces); the error cites a 4KB limit and "smaller than 5120 bytes" for UpdateFunctionConfiguration (the total HTTP body size is also limited); ASCII = 1 byte; Unicode/extended ASCII = 2 to 4 bytes per character; example {"BUCKET":"my-bucket","KEY":"file.txt"} = 39 bytes
- [from source] (LAMBDA p.830) InvalidParameterValueException "reserved keys": Lambda reserves some keys (e.g. AWS_REGION cannot be overwritten); others such as PATH can be extended; list in "Defined runtime environment variables"
- [from source] (LAMBDA p.831) Concurrency/memory quotas: errors "Specified ConcurrentExecutions ... decreases account's UnreservedConcurrentExecution below its minimum value" and "MemorySize ... less than or equal to 3008"; [DATED] new accounts have reduced concurrency and memory quotas (here the text cites a 3008 MB limit in the error), AWS increases them automatically with use; resolve by requesting a quota increase; PutFunctionConcurrency above the quota also fails


## Troubleshooting: invocation
- [from source] (LAMBDA p.831) Lambda validates the request and checks scaling capacity before sending the event (or queuing it, in async); direct invocation shows errors in the response; async/event source mapping: look in logs, DLQ or failure destination
- [from source] (LAMBDA p.831) "not authorized to perform: lambda:InvokeFunction": add the AWSLambdaRole managed policy or a custom policy with lambda:InvokeFunction on the target; also applies to functions/compute that invoke; the IAM action name (lambda:InvokeFunction) differs from the API name (Invoke)
- [p.831-832] ResourceConflictException "function is currently in the following state: Pending": when connecting to a VPC at creation, the function stays Pending while it creates ENIs and can be neither invoked nor modified; if connected to the VPC after creation, it can be invoked during the pending update but its code/config cannot be modified
- [from source] (LAMBDA p.832) [DATED] Function stuck in Pending for more than 6 minutes: call UpdateFunctionCode, UpdateFunctionConfiguration or PublishVersion to unblock; Lambda cancels the operation and puts the function in Failed state (then delete and recreate or try a new update)
- [from source] (LAMBDA p.832) One function consuming all the concurrency (others get throttled): use reserved concurrency to divide the account/Region concurrency into pools (guarantees and limits)
- [from source] (LAMBDA p.832) Function invocable directly but not by another service/account: grant permission in the function's resource-based policy; if the invoker is in another account, the user also needs permission to invoke
- [from source] (LAMBDA p.832) Invocation loop (e.g. the function writes to the same S3 bucket that triggers the function): stop it with the Throttle button on the configuration page and then find the recursive code/config path
- [p.832-833] Alias routing with provisioned concurrency: Lambda uses a simple probabilistic model to distribute traffic between the two versions; with low traffic there is high variance between configured % and actual; avoid spillover by configuring more provisioned concurrency while alias routing is active
- [from source] (LAMBDA p.833) Cold starts with provisioned concurrency: if concurrency <= provisioned there should be no cold start. Checklist: (1) provisioned concurrency enabled on the version or alias (not configurable on $LATEST); (2) triggers invoke the correct version/alias (e.g. API Gateway not on $LATEST); non-zero ProvisionedConcurrencyInvocations confirms use; (3) non-zero ProvisionedConcurrencySpilloverInvocations = all provisioned capacity in use, part with cold start; (4) [DATED] maximum rate of 10 requests per second per unit of provisioned concurrency (100 provisioned = 1,000 req/s)
- [from source] (LAMBDA p.833) Known issue: first invocation in an initialized environment reports a non-zero Init Duration in the logs even without a cold start
- [from source] (LAMBDA p.833) Latency variability on the 1st invocation with provisioned concurrency: JIT runtimes (.NET) load resources lazily (typically tens of ms); more visible in 128 MiB functions; mitigate by increasing memory
- [from source] (LAMBDA p.833) Cold starts when deploying new versions: when the alias is updated, Lambda shifts provisioned concurrency to the new version according to the alias weights
- [p.833-834] KMSDisabledException: the KMS key for the env vars is disabled or the grant was revoked; if the grant is missing, configure another key and reassign the custom key to recreate the grant
- [from source] (LAMBDA p.834) EFSMountFailureException: mount rejected; check permissions, existence/state of the file system and access point
- [from source] (LAMBDA p.834) EFSMountConnectivityException: no NFS connection (TCP port 2049); check the security group and subnet routing
- [from source] (LAMBDA p.834) EFSMountTimeoutException: connected but the mount timed out; try again and consider limiting the function's concurrency to reduce load on the file system
- [from source] (LAMBDA p.834) EFSIOException ("IO process that was taking too long"): a previous invocation timed out and Lambda could not finish the handler; occurs when EFS runs out of burst credits and baseline throughput is insufficient; increase the file system size or use provisioned throughput


## Troubleshooting: execution
- [p.834-835] Errors can occur during initialization, event processing or response; when code or the runtime returns an error the Lambda response has status 200 OK and the error is signaled by the X-Amz-Function-Error header; codes 400 and 500 are reserved for invocation errors
- [from source] (LAMBDA p.835) Slow execution: configuring more memory increases memory and CPU
- [from source] (LAMBDA p.835) Missing logs/traces: the execution role needs the AWSLambdaBasicExecutionRole and AWSXRayDaemonWriteAccess managed policies; after adding permissions update the code or configuration to force replacement of instances with stale credentials; logs can take 5 to 10 min
- [from source] (LAMBDA p.835) Node.js returns before finishing: asynchronous libraries return a promise; use await (or return the promise to the runtime if you do not need the data); libraries without promises can be wrapped
- [p.835-836] The SDK included in the runtime is not the latest version / updates automatically: scripting runtimes include the AWS SDK and are updated periodically; for a new or pinned version, package the library in the code or in a layer
- [from source] (LAMBDA p.836) Python: libraries with C/C++ extensions must be compiled in an environment with the same processor architecture as Lambda (Amazon Linux)


## Troubleshooting: network
- [from source] (LAMBDA p.836) By default functions run in an internal VPC with access to AWS services and the internet; when connecting to your own VPC the customer manages internet access and connectivity; failures due to route, security group, IAM, NAT, lack of IPs/ENIs
- [p.836-837] Loss of internet after VPC (ETIMEDOUT, "Task timed out after 10.00 seconds", ReadTimeoutError): all outbound traffic goes through the VPC; configure the function subnet's outbound route to a NAT gateway in a public subnet; TCP timeouts can be packet fragmentation: Lambda does not support IP fragmentation for TCP or ICMP
- [from source] (LAMBDA p.837) Access to AWS services without internet: use VPC endpoints (e.g. S3 and DynamoDB) from a private subnet
- [from source] (LAMBDA p.837) ENILimitReachedException: Lambda creates one ENI per subnet+security group combination; [DATED] default quota of 250 network interfaces per VPC; request an increase in Service Quotas


## Troubleshooting: container images
- [from source] (LAMBDA p.837) CodeArtifactUserPendingException (optimization pending; becomes active when complete; HTTP 409); CodeArtifactUserDeletedException (scheduled for deletion; 409); CodeArtifactUserFailedException (optimization failure; fix and resend; 409)
- [p.837-838] Manifest key (KMS) errors: KMSAccessDeniedException (no permission on the key; 502); TooManyRequestsException (rate exceeds the KMS subscription; 429); KMSNotFoundException (key not found; 502); KMSDisabledException (key disabled; 502); KMSInvalidStateException (key in a state such as pending deletion/unavailable; 502)
- [from source] (LAMBDA p.838) Runtime.ExitError / Runtime.InvalidEntrypoint: the container ENTRYPOINT must use an absolute path and cannot be a symlink
- [from source] (LAMBDA p.838) Message "do not have sufficient capacity in the region" (system provisioning capacity): repeat the invocation; if it fails, validate that the required files are readable by any user (Lambda sets a default least-privilege Linux user)
- [from source] (LAMBDA p.838) CloudFormation: ENTRYPOINT overridden by a null/empty value: if you declare ImageConfig in the template, provide non-empty values for ALL THREE properties



# Permissions, IAM and security

> Execution role, user policies, ABAC, resource-based policies, condition keys, permissions boundaries, security model, compliance, responsibilities.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the text of the references has no accents, because the reading notes it came from had none.

## Permissions - overview (p.71)
- [from source] (LAMBDA p.71) IAM controls access to the Lambda API and to resources (functions, layers); policies apply to users, groups or roles
- [from source] (LAMBDA p.71) Every function has an execution role; at a minimum it needs access to CloudWatch Logs; calls to other services via the SDK require permissions in the role's policy; Lambda also uses the role to read from event sources in event source mappings
- [from source] (LAMBDA p.71) To give access to other accounts/services, use a resource-based policy (resources: functions, versions, aliases, layer versions)
- [from source] (LAMBDA p.71) Evaluation rule: when a user accesses a Lambda resource, both identity-based policies AND the resource's policy are considered; when an AWS service (e.g. S3) calls the function, ONLY the resource-based policy is considered
- [from source] (LAMBDA p.71) Recommendation: use AWS managed policies as they are or as a starting point for more restrictive policies; restrict by resource and by optional conditions
- [from source] (LAMBDA p.71) To restrict which functions access a target resource: condition key lambda:SourceFunctionArn in the target resource's resource-based policy
- [from source] (LAMBDA p.71) Chapter topics (printed pages): execution role 50, identity-based 57, ABAC 62, resource-based 66, resources/conditions 72, permissions boundaries 78


## Execution role (p.72-76)
- [from source] (LAMBDA p.72) Execution role: an IAM role that grants the function permission to access services/resources (e.g. send logs to CloudWatch, traces to X-Ray); specified at creation; Lambda provides temporary credentials by assuming the role automatically; do not call sts:AssumeRole in the code
- [from source] (LAMBDA p.72) View the role: console > function > Configuration > Permissions > Resource summary (dropdown per service)
- [from source] (LAMBDA p.72) Permissions can be changed at any time or the role swapped; when adding permissions, also update the code or configuration to force replacement of running instances holding outdated credentials
- [from source] (LAMBDA p.72) The console creates by default an execution role with minimal permissions; in IAM: Create role > Use case Lambda > policies AWSLambdaBasicExecutionRole and AWSXRayDaemonWriteAccess > name > Create role
- [from source] (LAMBDA p.73) Least privilege best practices: in development it is common to grant more than needed; before production reduce the policy to what is needed
- [from source] (LAMBDA p.73) IAM Access Analyzer examines CloudTrail logs in the chosen interval and generates a policy template with only the permissions used; use it to create a fine-grained managed policy
- [p.73-74] The role's trust policy grants principals permission to assume it; for Lambda the principal is lambda.amazonaws.com; avoid calling sts:AssumeRole manually; if the role needs to assume itself, include the role itself as a trusted principal in the trust policy
- [from source] (LAMBDA p.74) Temporary credentials are held in environment variables during the invocation; if used outside Lambda (e.g. S3 presigned URL) you cannot control the session duration: the IAM maximum session does not apply to sessions assumed by services; use sts:AssumeRole when you need to control the duration
- [p.74-75] Managed policies [DATED]: AWSLambdaBasicExecutionRole (CloudWatch logs), AWSLambdaDynamoDBExecutionRole (reads DynamoDB stream + logs), AWSLambdaKinesisExecutionRole (reads Kinesis + logs), AWSLambdaMSKExecutionRole (reads MSK, manages ENIs, logs; kafka:DescribeClusterV2 added on 06/17/2022), AWSLambdaSQSQueueExecutionRole (reads SQS + logs), AWSLambdaVPCAccessExecutionRole (manages ENIs in the VPC + logs), AWSXRayDaemonWriteAccess (sends traces), CloudWatchLambdaInsightsExecutionRolePolicy (metrics to Lambda Insights), AmazonS3ObjectLambdaExecutionRolePolicy (S3 Object Lambda + logs); change tracking started on 02/14/2022
- [from source] (LAMBDA p.75) Recommendation: the console tries to add missing permissions to customer managed policies, which can multiply; to avoid this, add the relevant AWS managed policies to the role before enabling the feature
- [p.75-76] Event source mappings use the execution role to read the event data; reading services listed: DynamoDB, Kinesis, Amazon MQ, Amazon MSK, self-managed Apache Kafka (see continuation)


## Execution role (cont.) and environment credentials (p.76-78)
- [from source] (LAMBDA p.76) Services from which Lambda reads events via event source mapping: DynamoDB, Kinesis, Amazon MQ, MSK, self-managed Kafka, SQS
- [from source] (LAMBDA p.76) The console offers custom policy templates for additional use cases; applied when creating a function with a new role, from blueprints or when enabling options that require other services
- [from source] (LAMBDA p.76) The execution role's ephemeral credentials are held in environment variables; in the SDKs you do not need to provide credentials in the code: the credential provider chain uses the first available source, normally AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN
- [from source] (LAMBDA p.76) Lambda injects the source function's ARN into the credentials context ONLY on API calls made from inside the execution environment; calls made by Lambda outside the environment with the same role (e.g. KMS to encrypt/decrypt environment variables, CloudWatch for logs) do not contain the ARN
- [from source] (LAMBDA p.76) The condition key lambda:SourceFunctionArn lets you verify whether the call came from a specific function's code; use it in an identity-based policy or SCP; it CANNOT be used in resource-based policies; useful for security controls and identifying the origin of a credential leak
- [from source] (LAMBDA p.77) Difference between keys: lambda:FunctionArn only for event source mappings (which functions the source can invoke); aws:SourceArn only for policies where the function is the target resource (which services/resources can invoke); lambda:SourceFunctionArn applies to any identity policy or SCP
- [from source] (LAMBDA p.77) Usage: with any ARN condition operator (e.g. ArnEquals); the value must be a valid ARN. Example: allow s3:PutObject on the bucket only if the origin is the function source_lambda; another caller with the same role does not gain the access
- [p.77-78] SCP example: Deny s3:* on the bucket except if it comes from a specific function or a specific VPC, combining StringNotEqualsIfExists (aws:SourceVpc) and ArnNotEqualsIfExists (lambda:SourceFunctionArn); the IfExists operators only evaluate the condition when the key exists in the request
- [from source] (LAMBDA p.78) MINOR CONTRADICTION in the text: the example SCP uses an ARN with us-east-1, but the explanation cites arn:aws:lambda:*:123456789012:function:source_lambda (wildcard in the Region)


## Identity-based policies (user policies) (p.79-83)
- [from source] (LAMBDA p.79) Identity policies can be applied to users, groups or roles; you can also give users of another account permission to assume a role in your account
- [from source] (LAMBDA p.79) Lambda updates the managed policies as new features appear
- [from source] (LAMBDA p.79) [DATED] AWSLambdaFullAccess and AWSLambdaReadOnlyAccess were to be deprecated on March 1, 2021 (cannot be attached to new IAM users); replacements AWSLambda_FullAccess and AWSLambda_ReadOnlyAccess (reduced-scope versions); AWSLambdaRole grants permission to invoke functions
- [from source] (LAMBDA p.79) Managed policies grant the API action without restricting which functions/layers; for fine-grained control create your own policies
- [from source] (LAMBDA p.79) For a function as a container image, the user's access permission to the image MUST be configured in Amazon ECR
- [p.79-81] Example development policy limited by the intern- prefix: ReadOnlyPermissions (Get*/List* + iam:ListRoles, Resource "*", used by the console, without support for resource patterns/conditions); DevelopFunctions (NotAction except lambda:AddPermission and lambda:PutFunctionConcurrency, on function:intern-*); DevelopEventSourceMappings (Create/Update/DeleteEventSourceMapping with Resource "*" restricted by StringLike condition lambda:FunctionArn); PassExecutionRole (iam:PassRole etc. only for the role intern-lambda-execution-role); ViewLogs (logs:* on the log group /aws/lambda/intern-*)
- [from source] (LAMBDA p.81) Why exclude AddPermission and PutFunctionConcurrency: AddPermission alters the function's resource-based policy (security implication); PutFunctionConcurrency reserves capacity and can take capacity from other functions
- [from source] (LAMBDA p.81) iam:PassRole is used when assigning an execution role to the function; the role must be created/managed by a user with IAM permissions
- [from source] (LAMBDA p.82) Policy limitations: it does not allow configuring triggers/calls to other services (requires broader IAM permissions); it does not include services without limited-scope policies, such as CloudWatch and X-Ray (use the read-only policies of those services); to configure triggers you need permission on the invoking service (e.g. S3 bucket notifications); many are included in AWSLambdaFullAccess
- [from source] (LAMBDA p.82) Layers: example policy with lambda:PublishLayerVersion on layer:test-* and GetLayerVersion/DeleteLayerVersion on layer:test-*:* (versions)
- [p.82-83] The lambda:Layer condition in CreateFunction/UpdateFunctionConfiguration (with ForAllValues:StringLike) requires layers to come from a specific account (e.g. prevent layers from other accounts); verify that no other statement grants these actions, otherwise the condition does not apply
- [from source] (LAMBDA p.83) Cross-account roles: apply policies to a role shared with another account; a role has no credentials, it has a trust policy saying who can assume it; to only allow invoking a function or using a layer, prefer resource-based policies
- [from source] (LAMBDA p.83) VPC condition keys: require that all of the organization's functions be in a VPC and specify allowed or denied subnets/security groups (details on printed p. 244, outside this range)


## ABAC - attribute-based access control (p.84-87)
- [from source] (LAMBDA p.84) ABAC uses tags to control access: tags on the resource, in API requests or on the IAM principal; allows least privilege without listing ARNs and scales without updating policies (just tag new functions)
- [from source] (LAMBDA p.84) In Lambda tags operate at the function level; NOT supported for layers, code signing configurations or event source mappings; a function's tags apply to all versions and aliases
- [from source] (LAMBDA p.84) Condition keys: aws:ResourceTag/tag-key (resource tags), aws:RequestTag/tag-key (require tags in the request), aws:PrincipalTag/tag-key (principal tags), aws:TagKeys (which keys can be used)
- [from source] (LAMBDA p.84) Tutorial prerequisite: have an execution role; scenario: 4 policies attached to a new role + a user with permission to assume it
- [p.84-85] Step 1: require tags on new functions (best practice); policy with CreateFunction and TagResource, aws:RequestTag/project equal to ${aws:PrincipalTag/project}, and ForAllValues:StringEquals on aws:TagKeys = project; without the ForAllValues modifier users could add tags other than project
- [from source] (LAMBDA p.85) Step 2: allow InvokeFunction and GetFunction when aws:ResourceTag/project == aws:PrincipalTag/project; if the function has other tags the action is denied
- [p.85-86] Step 3: list policy (lambda:GetAccountSettings, lambda:ListFunctions, iam:ListRoles with Resource "*") to see everything in the console/API
- [from source] (LAMBDA p.86) Step 4: iam:PassRole for the execution role; ANTIPATTERN: do not use the ResourceTag condition key with iam:PassRole (an IAM role's tag does not control who can pass it)
- [from source] (LAMBDA p.86) Step 5: create the role abac-project-role (trusted entity: this account; attach the 4 policies; tag project with no value) and Step 6: user abac-test-user with an sts:AssumeRole policy on that role
- [from source] (LAMBDA p.87) Step 7 test: sign in as the user, switch to the role, create a function with an existing role and tag project (success); creating with another tag (e.g. environment) or without tags must FAIL; new users gain access just by being able to assume the project's role


## Resource-based policies (p.88-89...)
- [from source] (LAMBDA p.88) Resource-based policies exist for functions and layers; they grant use to other accounts or organizations (AWS Organizations) per resource and allow AWS services to invoke the function
- [from source] (LAMBDA p.88) View the policy: Functions > function > Configuration > Permissions > Resource-based policy > View policy document
- [from source] (LAMBDA p.88) Example: statement with Principal Service s3.amazonaws.com, Action lambda:InvokeFunction, conditions AWS:SourceAccount (StringEquals) and AWS:SourceArn (ArnLike) of the bucket
- [from source] (LAMBDA p.88) Layers: the policy only on a specific layer version (not on the whole layer); besides a single account/multiple accounts it can grant to all accounts of an organization
- [from source] (LAMBDA p.88) Limitation: you can only update resource-based policies within the scope of the AddPermission and AddLayerVersionPermission APIs; you cannot write the policy in JSON nor use conditions that do not map to parameters of those actions
- [from source] (LAMBDA p.89) Policies apply to a function, version, alias or layer version; for trusted accounts with access to several resources or to unsupported actions, use cross-account roles
- [from source] (LAMBDA p.89) Services: statement in the resource-based policy, for the whole function or limited to a version/alias; when adding a trigger through the console, the console updates the policy automatically; for other accounts/services outside the console use the CLI
- [from source] (LAMBDA p.89) CLI: `aws lambda add-permission --function-name my-function --action lambda:InvokeFunction --statement-id sns --principal sns.amazonaws.com` [DATED: CLI]; without --source-arn any SNS topic can invoke; recommended to restrict with --source-arn (e.g. topic my-topic)


## Resource-based policies (cont.) (p.89-93)
- [p.89-90] S3 antipattern: the bucket ARN does not contain an account ID; if the bucket is deleted, another account can create a bucket with the same name; use --source-account with your account ID (together with --source-arn) to ensure only resources from your account invoke
- [from source] (LAMBDA p.90) Organization: `add-permission ... --principal * --principal-org-id o-a1b2c3d4e5f` generates a policy with Principal "*" and condition StringEquals aws:PrincipalOrgID; with a specific account/role Principal, it only gains access if it also belongs to the organization [DATED: CLI]
- [from source] (LAMBDA p.90) Another account: `add-permission --function-name my-function:prod --principal 111122223333` grants invocation of the prod alias (Principal becomes arn:aws:iam::111122223333:root)
- [from source] (LAMBDA p.91) The resource-based policy does NOT allow users in the other account to exceed their own permissions: they need the corresponding user permissions (identity-based) to use the API
- [from source] (LAMBDA p.91) To limit to a user/role of another account, use the identity's full ARN as the principal (e.g. arn:aws:iam::123456789012:user/developer)
- [from source] (LAMBDA p.91) An alias limits which version the other account can invoke (it must include the alias in the ARN); the owner updates the alias to a new version without the caller changing code; the invoke output shows ExecutedVersion "1"
- [from source] (LAMBDA p.91) Cross-account access granted per action (e.g. lambda:ListAliases, lambda:GetFunction which allows downloading code) or lambda:* for all the function's actions
- [from source] (LAMBDA p.91) APIs with cross-account support via resource-based policy: Invoke, GetFunction, GetFunctionConfiguration, UpdateFunctionCode, DeleteFunction, PublishVersion, ListVersionsByFunction, CreateAlias, GetAlias, ListAliases, UpdateAlias, DeleteAlias, GetPolicy, PutFunctionConcurrency, DeleteFunctionConcurrency, ListTags, TagResource, UntagResource
- [from source] (LAMBDA p.92) For several functions or actions that do not operate on a function, using IAM roles (cross-account role) is recommended
- [from source] (LAMBDA p.92) Layers: `add-layer-version-permission --layer-name xray-sdk-nodejs --version-number 1 --principal 111122223333 --action lambda:GetLayerVersion`; the permission applies to only ONE layer version: repeat for each new version; for an organization use --organization-id with --principal '*'; for all accounts, principal * without organization id; several accounts/orgs require several statements
- [p.92-93] Cleanup/inspection: `get-policy --function-name my-function` (for a version/alias append :version/:alias, e.g. my-function:PROD); `remove-permission --function-name example --statement-id sns`; `get-layer-version-policy`; `remove-layer-version-permission` [DATED: CLI]
- [from source] (LAMBDA p.92) INCONSISTENCY in the text: the get-policy example output shows Sid "sns" with Principal s3.amazonaws.com and the SourceArn of an SNS topic


## Resources and conditions in IAM policies (p.94-99)
- [from source] (LAMBDA p.94) Each action supports its own combination of resource/condition types; when the action does not act on a named resource or it is granted on all, Resource is a wildcard (*)
- [from source] (LAMBDA p.94) ARN formats [DATED]: function ...:function:my-function; version ...:function:my-function:1; alias ...:function:my-function:TEST; event source mapping ...:event-source-mapping:<uuid>; layer ...:layer:my-layer; layer version ...:layer:my-layer:1
- [from source] (LAMBDA p.94) Special case: the IAM action identifier lambda:InvokeFunction differs from the API operation name (Invoke); in the others the identifier is lambda: + operation name
- [from source] (LAMBDA p.95) The lambda:Principal condition restricts which service/account the user can grant invoke access to (in AddPermission/RemovePermission); example: only allow SNS, with resource function:test:* (requires a version number or alias)
- [from source] (LAMBDA p.95) Authorization compares the Resource element with FunctionName AND Qualifier passed in the call; any mismatch = denied; you must use the correct ARN type (qualified or not)
- [from source] (LAMBDA p.95) You cannot use a wildcard (*) for the account ID
- [p.95-96] ARN rules: unqualified accepts only unqualified requests (denies qualified ones); a specific qualified ARN (e.g. :1) accepts only that one (denies unqualified and others such as :2); ":*" accepts any qualified but denies unqualified; "function:myFunction*" (wildcard without a colon) accepts qualified and unqualified
- [p.97-98] Function actions table (summary): AddPermission/RemovePermission -> function/version/alias + lambda:Principal, aws:ResourceTag, lambda:FunctionUrlAuthType; Invoke -> function/version/alias + aws:ResourceTag; CreateFunction -> function + CodeSigningConfigArn, Layer, VpcIds, SubnetIds, SecurityGroupIds, ResourceTag, RequestTag, TagKeys; UpdateFunctionConfiguration -> same (without RequestTag/TagKeys); alias/delete/get/list/publish/put/update code actions -> function (+ResourceTag); Function URL config actions -> function or alias + lambda:FunctionUrlAuthType (and lambda:FunctionArn); provisioned concurrency config -> alias or version; GetAccountSettings and ListFunctions -> "*" without condition; TagResource/UntagResource -> function + ResourceTag/RequestTag/TagKeys
- [from source] (LAMBDA p.99) Event source mapping: Delete/Update -> event source mapping resource + lambda:FunctionArn condition; CreateEventSourceMapping -> "*" + lambda:FunctionArn; Get/List -> "*" without condition; the condition restricts which functions an event source can invoke
- [from source] (LAMBDA p.99) Layers: use/permission actions act on the layer version; PublishLayerVersion acts on the layer name; ListLayers "*"; GetLayerVersion also covers GetLayerVersionByArn, which is NOT a supported IAM action


## Permissions boundaries (p.100-101)
- [from source] (LAMBDA p.100) When creating an application in the console, Lambda applies a permissions boundary to the application's IAM roles (each function's execution role and extra roles from the template); it prevents users with write access to the Git repository from escalating permissions beyond the scope of the application's resources
- [from source] (LAMBDA p.100) Application templates include the property Globals.Function.PermissionsBoundary (ARN <AppId>-<Region>-PermissionsBoundary)
- [from source] (LAMBDA p.100) A permission added to the execution role is only effective if the boundary also allows it; the role CloudFormation assumes on deployment can only create and pass roles with the boundary attached
- [from source] (LAMBDA p.100) By default the boundary allows actions on the application's resources (e.g. DynamoDB table, for actions with resource-level permission); actions without resource-level support (CloudWatch Logs, X-Ray) must be explicitly in the boundary
- [p.100-101] Boundary example: statement StackResources (Action "*" on the ARNs of the app's functions and table) and StaticPermissions (logs:CreateLogGroup/CreateLogStream/DescribeLogGroups/PutLogEvents, xray:Put* on "*")
- [from source] (LAMBDA p.101) To access other resources/actions: expand (1) the boundary (add resources; actions without resource-level in a statement without resource scope), (2) the execution role in the template (the function receives the INTERSECTION between boundary and role) and (3) the deployment role (in IAM, same permissions the user would need to deploy/update in CloudFormation)
- [from source] (LAMBDA p.101) DEFECT IN THE TEXT: the reference to the tutorial appears as "??? (p. 821)" (broken link)


## Security: model and data protection
- [from source] (LAMBDA p.815) Shared responsibility: AWS = security OF the cloud (infrastructure, third-party audits); customer = security IN the cloud (data sensitivity, company requirements, laws)
- [p.815-816] Data protection recommendations: protect account credentials and use individual IAM users with least privilege; MFA on each account; SSL/TLS (TLS 1.2 or higher recommended); CloudTrail for API/activity logging; AWS encryption solutions; Amazon Macie for sensitive data in S3; FIPS endpoints when you need FIPS 140-2 validated modules via CLI/API
- [from source] (LAMBDA p.816) Antipattern: never put confidential information (e.g. customer email) in tags or free-form fields such as Name (they may go to billing/diagnostic logs); do not include credentials in an external server's URL
- [from source] (LAMBDA p.816) Encryption in transit: Lambda API endpoints only support HTTPS; communication via console/SDK/API uses TLS; file system (EFS) connections use encryption in transit; environment variables can use "console encryption helpers" (client-side encryption) for protection in transit
- [from source] (LAMBDA p.816) Encryption at rest: Lambda always encrypts environment variables at rest; by default it uses an AWS managed KMS key created in the account, called aws/lambda; per function you can opt for a customer managed key; uploaded files (deployment packages and layers) are always encrypted; CloudWatch Logs and X-Ray encrypt by default and accept a customer managed key


## IAM for Lambda
- [p.816-817] IAM controls who is authenticated and authorized; no additional cost
- [from source] (LAMBDA p.817) Audience roles: service user, service administrator, IAM administrator; troubleshooting on printed p.801
- [p.817-818] Authentication: root user, IAM user, or assuming an IAM role (federation = assuming a role indirectly: IAM Identity Center, corporate SSO, Google/Facebook); SDK/CLI sign requests (Signature Version 4); MFA recommended
- [from source] (LAMBDA p.818) Root user: do not use day to day; reserve it for tasks only the root can do
- [from source] (LAMBDA p.818) IAM users: prefer temporary credentials over long-lived users; if necessary, rotate access keys. Groups do not sign in, they group permissions. User = permanent credentials; role = temporary credentials assumable by anyone who needs them
- [p.818-819] Role use cases with temporary credentials: federated access, temporary IAM user permissions, cross-account (roles are the main route; some services allow a resource-based policy directly), cross-service, principal permissions, service role, service-linked role (owned by the service; admin only views, does not edit), applications on EC2 via instance profile
- [from source] (LAMBDA p.819) Policies: an IAM entity starts with no permissions; the default is deny; a policy defines permissions regardless of console/CLI/API
- [p.819-820] Policy types: identity-based (inline embedded in an entity; managed = AWS managed or customer managed, reusable); resource-based (attached to a resource, e.g. role trust policy, S3 bucket policy; require Principal; are inline; do not use AWS managed policies); ACLs (not JSON; S3, WAF, VPC)
- [from source] (LAMBDA p.820) Advanced types: permissions boundary (maximum that an identity-based policy grants; result = intersection; a resource-based policy that names the user/role in Principal is not limited by the boundary); SCPs (maximum for organization/OU, limit even the root of member accounts); session policies (intersection with the user's/role's policies). An explicit Deny in any of them overrides allow
- [from source] (LAMBDA p.821) For an overview of how Lambda uses IAM: "Lambda permissions" (printed p.49); IAM users/roles by default have no permission to create/modify Lambda resources
- [p.821-822] Policy best practices: start with AWS managed policies and migrate to customer managed with least privilege; apply least-privilege; use conditions (e.g. require SSL, use via CloudFormation); IAM Access Analyzer (more than 100 checks) to validate policies; require MFA with MFA conditions
- [from source] (LAMBDA p.822) [DATED] IAM Access Analyzer provides "more than 100" policy checks
- [from source] (LAMBDA p.822) The Lambda console requires a minimum set of list/view permissions; a more restrictive policy breaks the console; example of a minimal policy in "Function development" (printed p.57); the console uses other services for triggers, so users need access to them
- [p.822-823] Example policy ViewOwnUserInfo/NavigateInConsole (iam:GetUserPolicy, ListGroupsForUser, ListAttachedUserPolicies, ListUserPolicies, GetUser, etc.; Version "2012-10-17"; resource arn:aws:iam::*:user/${aws:username})


## Identity and access troubleshooting
- [from source] (LAMBDA p.823) Error "not authorized to perform: lambda:GetFunction" -> ask the administrator for the lambda:GetFunction action on the resource
- [from source] (LAMBDA p.823) Error "not authorized to perform: iam:PassRole" -> the policy must allow iam:PassRole to pass a role to the service (actions that require service roles)
- [from source] (LAMBDA p.824) Access keys: the ID can be reviewed anytime, the secret only at creation; if lost, create a new pair; [DATED] maximum of 2 access keys per IAM user; never give them to third parties
- [from source] (LAMBDA p.824) [DATED] After March 1, 2021, the managed policies AWSLambdaReadOnlyAccess and AWSLambdaFullAccess become deprecated and cannot be attached to new IAM users; replacements: AWSLambda_ReadOnlyAccess and AWSLambda_FullAccess (reduced-scope versions); review permissions before attaching; for finer control, use customer managed policies
- [from source] (LAMBDA p.825) Access from outside the account: create a role that principals from other accounts assume, or a resource-based policy/ACL where supported


## Compliance
- [from source] (LAMBDA p.825) Third-party auditors assess Lambda in SOC, PCI, FedRAMP, HIPAA programs, among others; reports via AWS Artifact; compliance responsibility depends on data sensitivity, company objectives and laws; resources: quick start guides, HIPAA whitepaper
- [from source] (LAMBDA p.826) Compliance support services: AWS Config (evaluates compliance of resource configurations) and AWS Security Hub (security posture view)


## Resilience and infrastructure security
- [from source] (LAMBDA p.826) AWS infra: Regions with multiple isolated AZs; Lambda offers: Versioning (versions + aliases enable blue/green and rolling); Scaling ([DATED] 1,000 concurrent executions per region, quota can be increased); High availability (multiple AZs; when using a VPC, specify subnets in several AZs); Reserved concurrency (guarantees scaling up to, but not beyond, a number; avoids losing requests because other functions consume all the concurrency); Retries (async and a subset of invocations from other services are retried automatically; synchronous invokers must do their own retries); Dead-letter queue (async; SNS topic or SQS queue after retries are exhausted)
- [from source] (LAMBDA p.826) [DATED] API clients must support TLS 1.0 or higher (1.2+ recommended) and cipher suites with perfect forward secrecy (DHE/ECDHE; Java 7+ supports it)
- [from source] (LAMBDA p.827) Requests must be signed with the access key ID + secret of an IAM principal, or temporary AWS STS credentials


## Configuration and vulnerability analysis (responsibilities)
- [from source] (LAMBDA p.827) Lambda keeps the runtime software and the execution environment (Amazon Linux) up to date, releases new runtimes and deprecates runtimes when the software reaches end of life; the customer is responsible for updating additional libraries (in the package or layers) and for migrating functions to a supported runtime after deprecation



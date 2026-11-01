# Execution environment, lifecycle, VPC, EFS and databases

> Execution environment lifecycle, networking and Hyperplane ENIs, deployment packages, VPC, interface endpoints, RDS Proxy, EFS.
> Source: AWS Lambda Developer Guide (2022 edition; last releases entry on 2022-11-28), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label are from the source; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the original Portuguese reading notes were written without accents.

## Execution environment and lifecycle (p.48-50)
- [from source] (LAMBDA p.48) The execution environment is secure and isolated, manages resources, and supports the lifecycle of the runtime and the external extensions
- [from source] (LAMBDA p.48) The runtime talks to Lambda through the Runtime API; extensions through the Extensions API, and they can receive logs/telemetry through the Telemetry API
- [from source] (LAMBDA p.48) The memory and maximum time configured at creation define the environment; the runtime and each external extension are processes in the environment and share permissions, resources, credentials and environment variables
- [from source] (LAMBDA p.48) Each phase starts with an event sent to the runtime and extensions; each one signals completion with a Next API request; Lambda freezes the environment when all have finished and there are no pending events
- [from source] (LAMBDA p.49) Init phase: 3 tasks (start extensions, bootstrap the runtime, run the function's static code) + beforeCheckpoint hooks (SnapStart only)
- [from source] (LAMBDA p.49) Init is limited to 10 seconds; if it does not finish, Lambda retries the Init phase on the first invocation [DATED]
- [from source] (LAMBDA p.49) SnapStart: Init happens when the version is published; Lambda saves an encrypted, cached snapshot (memory+disk); the beforeCheckpoint hook runs at the end of Init; the 10 s limit does not apply: init can last up to 15 minutes [DATED]
- [from source] (LAMBDA p.49) Restore phase (SnapStart only): on the first invocation and when scaling, new environments are resumed from the snapshot; the afterRestore hook is billed and has a 2-second timeout [DATED]
- [from source] (LAMBDA p.49) Invoke phase: the function timeout limits the whole phase (function + extensions); there is no independent post-invocation phase; duration is the sum of runtime+extensions
- [from source] (LAMBDA p.49) Crash or timeout in Invoke: Lambda resets the environment as a Shutdown (shuts down the runtime, sends Shutdown with the reason to the external extensions); if reused, the runtime and extensions restart on the next invocation; /tmp is NOT cleared on reset
- [from source] (LAMBDA p.50) Shutdown phase: limited to 2 seconds; anything that does not respond receives SIGKILL [DATED]
- [from source] (LAMBDA p.50) Environment reuse (freeze/thaw): objects outside the handler remain initialized (e.g. database connection; recommended to check whether the connection exists before creating a new one)
- [from source] (LAMBDA p.50) /tmp: from 512 MB to 10,240 MB in 1 MB increments [DATED]; content persists while frozen (transient cache); check whether the cache has the data
- [from source] (LAMBDA p.50) Background processes/callbacks not completed resume if the environment is reused; ensure completion before exiting
- [from source] (LAMBDA p.50) Anti-pattern: do not assume Lambda always reuses the environment; other factors can create a new environment and cause unexpected results such as connection failures


## VPC networking / Hyperplane (p.51-54)
- [from source] (LAMBDA p.51) A function always runs in a VPC owned by the Lambda service; to access resources in your account's VPC you configure VPC access; Hyperplane ENIs (managed resources) connect the Lambda VPC to an ENI in your VPC
- [from source] (LAMBDA p.51) No additional charge for using a VPC or Hyperplane ENI; there is a cost for components such as NAT gateways
- [from source] (LAMBDA p.51) VPC elements: ENI, subnet (public for internet, private without), security group, ACL (default allows all traffic), route table (default: main), route, NAT gateway, VPC endpoints (PrivateLink)
- [from source] (LAMBDA p.52) By default the function is not connected to the account's VPCs; when connected, it loses internet access unless the VPC provides it
- [from source] (LAMBDA p.52) The Hyperplane ENI does VPC-to-VPC NAT (V2N): connectivity from the Lambda VPC to the account's VPC, not in the opposite direction
- [from source] (LAMBDA p.52) One Hyperplane ENI is allocated per subnet of the configuration; functions with the same subnet+security group share the interface; each unique combination requires a distinct ENI
- [from source] (LAMBDA p.52) Access to other AWS services: VPC endpoints (private) or NAT gateway; internet access: route outbound traffic to a NAT gateway in a public subnet (with a public IP, via internet gateway)
- [from source] (LAMBDA p.52) ENI creation: the function stays in the pending state, then active; it can take several minutes; for a new function, invocations/API actions fail until it is active; on a configuration change, invocations keep using the old ENI until active
- [from source] (LAMBDA p.53) Function idle for consecutive weeks: Lambda reclaims ENIs and marks the state idle; the next invocation fails and the function enters pending until the ENI is recreated/allocated [DATED: "weeks"]
- [from source] (LAMBDA p.53) Lambda uses the execution role's permissions to create and manage ENIs; no quota of functions per ENI, but each ENI supports up to 65,000 connections/ports; above that it creates a new ENI [DATED]
- [from source] (LAMBDA p.53) Changing VPC: takes several minutes; invocations continue in the previous VPC until it completes
- [from source] (LAMBDA p.53) Removing the VPC config: up to 20 minutes to delete the ENI [DATED]; it is only deleted if no other function/published version uses it; depends on the execution role - if the role is deleted first, Lambda cannot delete the ENI (manual deletion); the Lambda ENI Finder tool identifies functions/versions that use the ENI
- [from source] (LAMBDA p.53) Supported connections: TCP and UDP; DHCP options created automatically; Amazon DNS (Route 53 resolver)
- [p.53-54] Security: security groups (instances) and network ACLs (subnets, additional layer); SGs are enough in most cases; there are Lambda-specific IAM condition keys for VPC settings
- [from source] (LAMBDA p.54) Observability: VPC Flow Logs (to CloudWatch Logs or S3); Lambda log messages do NOT use the VPC routes


## Deployment packages (p.55-57)
- [from source] (LAMBDA p.55) Two types: container image (base OS, runtime, extensions, code, dependencies, static data such as ML models) and zip
- [from source] (LAMBDA p.55) Images: use Lambda's open source base images; build/test with SAM CLI or Docker; uploaded to Amazon ECR; deploy by specifying the ECR image URL
- [from source] (LAMBDA p.55) Container images not supported in the Middle East (UAE) Region [DATED]
- [from source] (LAMBDA p.55) Zip: the console/toolkit create the zip automatically; with API/CLI/SDK, a compiled language or dependencies you must create the package; upload from S3 or local
- [p.55-56] Upload via console: Code Source > Upload from > .zip file > Upload > Save
- [from source] (LAMBDA p.56) Layers only with zip, never with an image; they can be yours, AWS's or other customers'
- [from source] (LAMBDA p.57) Native C/C++ libraries: use `sam build --use-container` (build inside a Docker image compatible with the environment)
- [from source] (LAMBDA p.57) Package above 50 MB: upload to S3 (in the same Region) and give the bucket/key when creating the function [DATED]


## VPC
- [from source] (LAMBDA p.263) Function connected to private subnets of a VPC; Lambda assigns a Hyperplane ENI per subnet; creates the ENI the first time a unique subnet+security group combination is defined in the account
- [from source] (LAMBDA p.263) While the ENI is being created: you cannot create versions or update code; a new function cannot be invoked until Pending becomes Active; for an existing function the previous version is still invoked
- [from source] (LAMBDA p.263) It does not connect directly to a VPC with dedicated tenancy; use peering with a default-tenancy VPC
- [from source] (LAMBDA p.263) Functions with the same subnet+security group share the ENI (additional connection much faster); after long inactivity Lambda recycles ENIs and the function becomes Idle; invoking an Idle function FAILS and it returns to Pending until an ENI is available
- [from source] (LAMBDA p.263) Changing VPC takes several minutes; during the transition invocations use the previous VPC
- [from source] (LAMBDA p.264) Recommendation: TCP keep-alive on connections created at initialization for short operations (e.g. DynamoDB), since the TCP handshake cost can exceed the operation
- [from source] (LAMBDA p.264) The execution role needs ec2:CreateNetworkInterface, ec2:DescribeNetworkInterfaces (only works with Resource "*") and ec2:DeleteNetworkInterface (without a resource ID it may fail; use a single ID or all); included in AWSLambdaVPCAccessExecutionRole; only needed to create ENIs, not to invoke; to disassociate completely, update the VPC config
- [from source] (LAMBDA p.264) The IAM user needs ec2:DescribeSecurityGroups, ec2:DescribeSubnets, ec2:DescribeVpcs; if IAM only allows VPC-connected functions, configure the VPC at creation
- [from source] (LAMBDA p.265) Console: Create function > Advanced settings > Network (VPC, subnets, security groups) or Configuration > VPC > Edit. Anti-pattern: a public subnet gives no internet access or public IP; for internet use NAT with private subnets
- [p.265-266] CLI: create-function / update-function-configuration with --vpc-config SubnetIds=...,SecurityGroupIds=...; disconnect with empty lists SubnetIds=[],SecurityGroupIds=[]
- [from source] (LAMBDA p.266) IAM condition keys: lambda:VpcIds, lambda:SubnetIds, lambda:SecurityGroupIds (in CreateFunction and UpdateFunctionConfiguration); VPC ID is not a request parameter, Lambda infers it from the subnets/security groups; tip: UpdateFunctionConfiguration can omit the VPC if already configured
- [p.266-268] Policy patterns: force VPC with Deny + Null lambda:VpcIds=true; deny VPC with StringEquals; deny subnets/SGs with ForAnyValue:StringEquals; allow only specific VPCs (StringEquals) and subnets/SGs with ForAllValues:StringEquals
- [from source] (LAMBDA p.269) By default the function runs in a Lambda-managed VPC with access to the internet and AWS services; when connected to the account's VPC, it loses internet unless the VPC provides it; VPC endpoints give access to AWS services without internet; internet requires a NAT gateway in a public subnet; [DATED] an idle NAT connection expires in 350 seconds
- [from source] (LAMBDA p.269) Tutorials: RDS (p.712) and ElastiCache (p.645). CloudFormation templates from the repository: vpc-private.yaml (2 private subnets, S3 and DynamoDB endpoints, no internet) and vpc-privatepublic.yaml (with NAT and internet gateway)


## Interface VPC endpoints
- [from source] (LAMBDA p.270) An interface endpoint (AWS PrivateLink) lets you invoke/use Lambda APIs from inside the VPC without an internet gateway, NAT, VPN or Direct Connect; no public IP; traffic stays on the AWS network; represented by ENIs with a private IP
- [from source] (LAMBDA p.270) Any Lambda API can be called from the VPC (e.g. Invoke)
- [from source] (LAMBDA p.270) Keep-alive: Lambda drops idle connections; reusing an idle connection causes a connection error; use the runtime's keep-alive
- [from source] (LAMBDA p.270) Cost: no additional Lambda charge for the endpoint, but PrivateLink pricing applies (per hour per AZ and per data processed); peering lets you reach the endpoint from other VPCs (same account/another account/another region)
- [from source] (LAMBDA p.271) Peering: traffic between peered VPCs stays on the AWS network; EC2, RDS or VPC functions in both VPCs access the Lambda API through the endpoint created in one of them
- [from source] (LAMBDA p.271) Create endpoint (VPC console): Endpoints > Create Endpoint > Service category AWS services > service com.amazonaws.REGION.lambda (type Interface) > VPC and subnets > Enable DNS Name (private DNS) > security group(s); private DNS requires the enableDnsHostnames and enableDnsSupport attributes on the VPC and lets you use the default DNS (lambda.us-east-1.amazonaws.com); CLI: aws ec2 create-vpc-endpoint --vpc-endpoint-type Interface
- [p.271-272] The endpoint policy defines principal, actions and resources; the example allows lambda:InvokeFunction for a user; you must include both the qualified and unqualified ARN of the function (function:my-function and function:my-function:*)


## Database (RDS Proxy)
- [from source] (LAMBDA p.273) RDS Proxy: manages a connection pool and relays the function's queries, allowing high concurrency without exhausting connections
- [from source] (LAMBDA p.273) Create via console: Configuration > Database proxies > Add database proxy; fields: Proxy identifier, RDS DB instance (MySQL or PostgreSQL, instance or cluster), Secret (Secrets Manager with username/password), IAM role (access to the secret + trust policy for RDS), Authentication
- [from source] (LAMBDA p.273) Cost: RDS charges per hour, according to the database instance size; creation takes a few minutes; afterwards the function must point to the proxy endpoint, not the database
- [from source] (LAMBDA p.274) Default authentication uses the same username/password the proxy uses on the database (drawback: exposing the password to the code, via a secure env var or Secrets Manager); alternative: Authentication = Execution role (IAM credentials; the console adds rds-db:connect and the SDK generates a token via RDS Signer; mysql2 Node.js example with ssl and authPlugins mysql_clear_password)
- [p.274-275] Sample apps: RDS MySQL (template-vpcrds.yml, MySQL 5.7 in a private VPC, Secrets Manager) and List Manager (Kinesis -> DynamoDB + copy in MySQL)


## File system (EFS)
- [from source] (LAMBDA p.277) A function can mount an Amazon EFS on a local directory, accessing shared resources securely and with high concurrency
- [from source] (LAMBDA p.277) Without a user IAM policy on the EFS, the default full-access policy applies to anyone connecting via a mount target; with a policy, the execution role needs elasticfilesystem:ClientMount and ClientWrite (not needed for read-only), included in AmazonElasticFileSystemClientReadWriteAccess; it also needs VPC permissions; the user needs elasticfilesystem:DescribeMountTargets
- [from source] (LAMBDA p.277) A mount target in each AZ used; recommendation of at least two AZs (performance and resilience); the security groups of the function and of the mount targets must allow NFS, [DATED] port 2049
- [from source] (LAMBDA p.277) The EFS performance mode cannot be changed afterwards: General purpose (lower latency) vs Max I/O (higher throughput and IOPS)
- [from source] (LAMBDA p.278) The access point links each instance to the AZ's mount target; for best performance use a non-root path and limit the number of files per directory; example: path /my-function, UID/GID 1001, permissions 755
- [from source] (LAMBDA p.278) Console: Configuration > File systems > Add file system; provide the EFS access point (same VPC) and a Local mount path starting with /mnt/; the function must be in a VPC (same subnets as the mount points or in the same AZ with an NFS route)
- [from source] (LAMBDA p.278) Costs: EFS charges for storage and throughput; Lambda charges for transfer between VPCs only when the function's VPC is peered with the file system's VPC
- [from source] (LAMBDA p.279) CLI: update-function-configuration --file-system-configs Arn=<access point ARN>,LocalMountPath=/mnt/efs0; access point ARN via aws efs describe-access-points
- [p.279-280] SAM/CloudFormation: FileSystemConfigs property in AWS::Serverless::Function; Gotcha: use DependsOn on the MountTarget to ensure the mount targets exist before the first execution; same property in AWS::Lambda::Function; efs-nodejs sample



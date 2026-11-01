# Deployment, container images, layers, code signing and tags

> .zip and container image deployment, base images, RIC/RIE, layers, code signing, tags.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), acronym LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the text of the references has no accents, because the reading notes it came from had none.

## Deployment: overview (p.183)
- [from source] (LAMBDA p.183) Two ways to deploy: upload a .zip or a container image
- [from source] (LAMBDA p.183) A .zip contains code and dependencies; the console/toolkit create the .zip automatically; with the API, CLI or SDKs you must assemble the deployment package (also required for a compiled language or to add dependencies); upload from S3 or from the local machine
- [from source] (LAMBDA p.183) Container image: packaged with the Docker CLI and uploaded to Amazon ECR; AWS provides open-source base images, allows alternative bases with an open-source runtime client added, and a runtime interface emulator for local testing
- [from source] (LAMBDA p.183) Each image must be compatible with ONE instruction set architecture; Lambda provides per-architecture bases and multi-architecture bases, but your project's image must target only one
- [from source] (LAMBDA p.183) Costs: no additional charge for packaging/deploying as a container image; you pay for invocations and duration, plus storage in Amazon ECR


## .zip deployment (p.184-187)
- [from source] (LAMBDA p.184) Two package types: container image and .zip; the creation flow depends on the type; a container image function cannot be converted to .zip (create a new function)
- [from source] (LAMBDA p.184) Creation in the console: choose a template/blueprint (Author from scratch or Use a blueprint), name, runtime, [DATED] function names limited to 64 characters, architecture (default x86_64; the package must be compatible), execution role, optionally code signing and VPC; code is added after the function is created
- [from source] (LAMBDA p.185) There are language-specific pages for .zip deployment (Node.js, Python, Ruby, Java .zip or JAR, Go, C#, PowerShell)
- [from source] (LAMBDA p.185) The console creates the function with a single source file; in scripting languages it lets you edit and add files in the editor (Cloud9); on save, the console creates the .zip; outside the console (IDE) you must create the package
- [from source] (LAMBDA p.185) [DATED] Built-in editor for Node.js, Python and Ruby; if the code is larger than 3 MB, needs libraries or uses Java/Go/C#, you must upload a .zip; a .zip smaller than 50 MB can be uploaded from the local machine; larger than 50 MB must come from an S3 bucket
- [p.185-186] Procedure: Code tab > Upload from > .zip file > Upload (or Amazon S3 location, providing the S3 URL of the .zip) > Save
- [from source] (LAMBDA p.186) Changing the runtime version may require updating the code; changing runtime requires new code compatible with the runtime and architecture; console: Code > Runtime settings > Edit (Runtime, Handler, Architecture) > Save
- [from source] (LAMBDA p.186) Changing architecture: the code must be compatible; Node.js/Python/Ruby edited in the built-in editor may run unmodified; with .zip you need a new package compiled/built for the target runtime and architecture
- [from source] (LAMBDA p.186) Relevant APIs: CreateFunction, UpdateFunctionCode, UpdateFunctionConfiguration
- [from source] (LAMBDA p.187) CloudFormation (.zip): AWS::Lambda::Function resource with PackageType=Zip, Code (S3Bucket and S3Key; Node.js/Python accept inline code), Runtime, Architecture (arm64 for Graviton2; default x86_64)


## Deployment as a container image (p.188-194)
- [from source] (LAMBDA p.188) A container image cannot be converted to .zip; when you pick an image by tag, Lambda translates the tag to the image digest (obtained via GetFunctionConfiguration); updating to a new image requires the console (deploy new image) or UpdateFunctionCode; configuration operations such as UpdateFunctionConfiguration do NOT update the image
- [from source] (LAMBDA p.188) Prerequisite: build the image and upload it to ECR before creating the function
- [from source] (LAMBDA p.189) Permissions for whoever creates the function: managed policies GetRepositoryPolicy and SetRepositoryPolicy (actions ecr:SetRepositoryPolicy/GetRepositoryPolicy on the repository resource)
- [from source] (LAMBDA p.189) Same account: the ECR repository must allow ecr:BatchGetImage and ecr:GetDownloadUrlForLayer to the service principal lambda.amazonaws.com (minimum policy); if missing, Lambda adds them, but only if the calling principal has ecr:getRepositoryPolicy and ecr:setRepositoryPolicy
- [p.189-190] Cross-account (same region): two statements in the repository policy: CrossAccountPermission (the external account can create/update functions with the image; principal arn:aws:iam::<account>:root) and LambdaECRImageCrossAccountRetrievalPolicy (principal lambda.amazonaws.com, Condition StringLike aws:sourceARN with the functions' ARNs); the second is necessary because Lambda eventually puts a function that has not been invoked for a long time into the inactive state and needs to retrieve the image for optimization and caching
- [from source] (LAMBDA p.190) Several accounts: add the IDs to the Principal list and to the Condition; in an AWS Organization, it is recommended to enumerate each account ID (narrow permissions principle)
- [p.190-191] Create in the console: Create function > Container image > name > Container image URI (or Browse images) > (optional) Container image overrides: Entrypoint (full path of the runtime executable; example "/usr/bin/npx", "aws-lambda-ric"), Command (parameters; example "app.handler"), Working directory (example "/var/task"); each string in quotes
- [from source] (LAMBDA p.191) Lambda creates the function and an execution role; it assumes the role on invocation to generate SDK credentials and read event sources; after the function is created the image goes through an optimization process that takes a few seconds, with the function in the pending state and then active
- [p.191-192] Testing in the console: Test tab > New event (hello-world template) > Save changes > Test; [DATED] each user can create up to 10 test events per function (not shared with other users); Execution result, Summary (REPORT line) and Log output; the Monitor tab shows CloudWatch metrics
- [from source] (LAMBDA p.192) Container overrides (console or API): ENTRYPOINT, CMD, WORKDIR, ENV; supplied values override the Dockerfile
- [from source] (LAMBDA p.193) Updating code: after deployment the image is read-only; you must deploy a new image version (Deploy new image > Browse images > choose > Save)
- [from source] (LAMBDA p.193) Alert: the ECR latest tag must not be confused with the function's $LATEST version; when a function version is published, code and most settings are locked, and only the unpublished version ($LATEST) is changeable
- [p.193-194] API/CLI: create-function --package-type Image --code ImageUri=<URI> (default architecture x86-64); update-function-code --image-uri; update-function-configuration --image-config with EntryPoint and Command (string arrays) and WorkingDirectory (string); package-type CANNOT be changed; the function's account can be another one in the same region as the registry (adjust ECR permissions)
- [from source] (LAMBDA p.194) CloudFormation (image): PackageType=Image; Code.ImageUri; optional ImageConfig (Command, EntryPoint, WorkingDirectory) and, if ImageConfig is declared, all THREE fields are required
- [from source] (LAMBDA p.195) To create images: AWS open-source bases with the runtime interface client; reduce the risk of an optimization timeout by following Dockerfile best practices; [DATED] container images are not supported in the Middle East (UAE) region


## Base images, RIC and RIE (p.196-201)
- [from source] (LAMBDA p.196) AWS provides open-source bases; you can also use a community/private base, adding the Lambda client software; each base is compatible with one or more architectures, the function image is built for ONE architecture and Lambda does NOT support multi-architecture images
- [from source] (LAMBDA p.196) AWS bases already bring the language runtime and necessary components; you add code and dependencies; AWS maintains and regularly updates them and releases bases when a new managed runtime appears; bases for Node.js, Python, Java, .NET, Go, Ruby
- [from source] (LAMBDA p.196) [DATED] Bases for custom runtimes: tag al2 (provided.al2, Amazon Linux 2) and alami (provided, Amazon Linux); ECR Public Gallery gallery.ecr.aws/lambda/provided
- [from source] (LAMBDA p.197) The runtime interface client (RIC) manages the interaction between Lambda and the code; the Runtime API + Extensions API define the simple HTTP interface; AWS bases already include the RIC; with a custom runtime or alternative base you must add the RIC (there is an open-source RIC for Node.js, Python, Java, .NET, Go and Ruby)
- [from source] (LAMBDA p.197) RIE (runtime interface emulator): AWS bases and custom runtime bases include the RIE; for other bases it is downloaded from AWS's GitHub
- [from source] (LAMBDA p.198) RIE = Runtime API proxy for testing a container image function locally; it is a lightweight web server that converts HTTP requests into JSON events; with an alternative base you can test without embedding the RIE; [DATED] there are separate RIE components for x86-64 and arm64; it also serves to test extensions and agents embedded using the Extensions API
- [from source] (LAMBDA p.198) RIE limits: it does not emulate Lambda's security/authentication or orchestration; one emulator per architecture; it does not support X-Ray or other Lambda integrations
- [p.198-199] RIE environment variables: credentials via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION; timeout via AWS_LAMBDA_FUNCTION_TIMEOUT (seconds); it does not populate AWS_LAMBDA_FUNCTION_VERSION, AWS_LAMBDA_FUNCTION_NAME, AWS_LAMBDA_FUNCTION_MEMORY_SIZE (they can be set manually)
- [from source] (LAMBDA p.199) Test with an RIE already included: `docker build -t myfunction:latest .`; `docker run -p 9000:8080 myfunction:latest` (endpoint localhost:9000/2015-03-31/functions/function/invocations); in another terminal `curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`
- [p.199-200] Embedding the RIE in the base: an entry script that tests whether AWS_LAMBDA_RUNTIME_API is set (indicates the Runtime API is present): if YES it runs the RIC; if NOT it runs the RIE (aws-lambda-rie) with the RIC (Node.js examples with npx aws-lambda-ric and Python with python -m awslambdaric)
- [from source] (LAMBDA p.200) Download the RIE for the target architecture (x86_64: aws-lambda-rie; arm64: aws-lambda-rie-arm64); in the Dockerfile: COPY the script, ADD the emulator at /usr/local/bin/aws-lambda-rie and ENTRYPOINT pointing to the script; then docker build
- [p.200-201] Testing without embedding the RIE: install the RIE on the local machine (curl from GitHub releases to ~/.aws-lambda-rie and chmod +x; for arm64 use the URL aws-lambda-rie-arm64) and run with `docker run -d -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 --entrypoint /aws-lambda/aws-lambda-rie <image> <entrypoint> <command>`; then curl POST to the same endpoint
- [p.200-201] Note from the text: the docker run example uses the hello-world:latest image and x86_64 file names vary (aws-lambda-rie vs aws-lambda-rie-x86_64 in the Dockerfile on p.200)


## Image requirements and formats (p.201-202)
- [from source] (LAMBDA p.201) Prerequisites: AWS CLI and Docker CLI; the image must implement the Lambda Runtime API (the open-source RICs do this)
- [from source] (LAMBDA p.201) [DATED] The image must run on a read-only filesystem; the code accesses a writable /tmp with between 512 MB and 10,240 MB, in 1 MB increments
- [from source] (LAMBDA p.201) Lambda's default Linux user (least privilege) must be able to read all the necessary files; verify that the code does not depend on files restricted to other users
- [from source] (LAMBDA p.201) Only Linux-based images; multi-architecture bases exist but the function image must target a single architecture
- [from source] (LAMBDA p.201) [DATED] You can use an AWS or alternative base (Alpine, Debian); accepted manifest formats: Docker image manifest V2 schema 2 (Docker 1.10+) and OCI Specifications (v1.0.0+); [DATED] maximum image size 10 GB
- [p.201-202] Any tool that generates one of the manifests will do (e.g. Docker CLI)
- [from source] (LAMBDA p.202) Supported Dockerfile settings: ENTRYPOINT (absolute path), CMD, WORKDIR (absolute path), ENV; values of unsupported settings are ignored; they can be overridden in the console/API, allowing several functions with the same image and different runtime settings
- [from source] (LAMBDA p.202) Warning/antipattern: provide an absolute path in ENTRYPOINT/CMD and do NOT use symlinks as the container entry point


## Creating images (p.202-206)
- [from source] (LAMBDA p.202) Two kinds of AWS base: multi-architecture (main tag, e.g. python:3.9, java:11) and architecture-specific (tag with suffix, e.g. 3.9-arm64)
- [from source] (LAMBDA p.202) Updates: AWS periodically updates the bases; if the Dockerfile uses the image name in FROM, Docker pulls the latest version from ECR, but to use the updated base you must rebuild the image AND update the function code
- [from source] (LAMBDA p.203) Steps: create the project directory; create app/ with the handler; Dockerfile; AWS bases define LAMBDA_TASK_ROOT=/var/task and LAMBDA_RUNTIME_DIR=/var/runtime; install dependencies under ${LAMBDA_TASK_ROOT} next to the handler
- [p.203-204] Example Dockerfiles (common pattern: FROM public.ecr.aws/lambda/<runtime>:<version>; COPY the code/dependency manifest to ${LAMBDA_TASK_ROOT}; install dependencies; CMD with the handler, which can also be set as an override outside the Dockerfile). Differences: Node.js 18 (`FROM public.ecr.aws/lambda/nodejs:18`, COPY app.js package.json, RUN npm install, CMD ["app.handler"]); Python 3.8 (pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}", CMD ["app.handler"]); Ruby 2.7 (COPY Gemfile, ENV GEM_HOME=${LAMBDA_TASK_ROOT}, RUN bundle install, CMD ["app.LambdaFunction::Handler.process"])
- [from source] (LAMBDA p.204) Local build and run: `docker build -t hello-world .`; `docker run -p 9000:8080 hello-world`; optional test with RIE and curl POST to localhost:9000
- [from source] (LAMBDA p.204) Alternative base: prerequisites AWS CLI, Docker Desktop, code; Lambda supports all Linux distributions (Alpine, Debian, Ubuntu); the Dockerfile must: FROM the base, install the RIC, ENTRYPOINT calling the RIC, CMD with the handler
- [p.204-205] Python example with python:buster base and multi-stage build: the build stage installs aws-lambda-cpp dependencies (g++, make, cmake, unzip, libcurl4-openssl-dev), copies the code and installs awslambdaric with pip --target; the final stage copies the directory and sets ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"] and CMD ["app.handler"]
- [from source] (LAMBDA p.205) Upload to ECR: authenticate Docker (aws ecr get-login-password ... | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com); create a repository (`aws ecr create-repository --repository-name hello-world --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE`); docker tag and docker push
- [from source] (LAMBDA p.205) Careful: in ECR, reassigning a tag to another image does NOT make Lambda update the function's image version
- [from source] (LAMBDA p.206) AWS SAM: `sam init` generates the scaffolding; in the SAM template set PackageType/Runtime to Image (the text says "Runtime type to Image") and provide the base image URI


## Configuring functions (p.207)
- [from source] (LAMBDA p.207) The deployment package type CANNOT be changed after the function is created; the creation flow differs between container image and .zip
- [from source] (LAMBDA p.207) Best practices: keep secrets out of the code, storing them in the function configuration and reading them from the environment during init; environment variables are always encrypted at rest (and can also be encrypted on the client); use variables for portability (connection strings, passwords, endpoints)
- [from source] (LAMBDA p.207) Versions and aliases are secondary resources: a published version stores code and configuration as an immutable resource; an alias points to a version and clients invoke the alias, updating it to point to a new version without changing the client
- [from source] (LAMBDA p.207) Layers serve to manage dependencies separately, keep the package small and share own/public libraries


## Layers (p.208-213)
- [from source] (LAMBDA p.208) Layer = .zip with additional code or data (libraries, custom runtime, data, configuration files); reduces the size of uploaded packages and speeds up deployment; promotes code sharing and separation of concerns
- [from source] (LAMBDA p.208) Layers only work with .zip functions; with a container image you package the runtime and dependencies in the image; creation via console, API, CloudFormation or SAM
- [from source] (LAMBDA p.208) Limitation [DATED]: for Node.js runtimes, Lambda does not (currently) support ES module dependencies in layers
- [from source] (LAMBDA p.208) Lambda extracts the layer contents into /opt when preparing the environment; upload the .zip from S3 or the local machine
- [from source] (LAMBDA p.208) Build the .zip as for a function package; native libraries must be compiled on a Linux machine for compatibility with Amazon Linux; a layer can declare compatibility with one or both architectures (compilation flags may be needed for arm64); AWS Cloud9 helps package correctly
- [from source] (LAMBDA p.209) [DATED] Layer paths per runtime that enter the PATH without extra configuration: Node.js nodejs/node_modules and nodejs/node14|node16|node18/node_modules (NODE_PATH); Python python and python/lib/python3.9/site-packages; Java java/lib (CLASSPATH); Ruby ruby/gems/2.7.0 (GEM_PATH) and ruby/lib (RUBYLIB); all runtimes: bin (PATH) and lib (LD_LIBRARY_PATH)
- [p.209-210] Structure examples: xray-sdk.zip -> nodejs/node_modules/aws-xray-sdk; pillow.zip -> python/PIL and python/Pillow-5.3.0.dist-info; json.zip -> ruby/gems/2.7.0/...json-2.1.0; jackson.zip -> java/lib/jackson-core-2.2.3.jar; jq.zip -> bin/jq
- [p.210-211] Per-language instructions refer to the .zip deployment pages for Node.js, Python, Ruby, Java (.zip/JAR), Go, C# and PowerShell (cross-references only)
- [from source] (LAMBDA p.211) Layer versions: first version = 1; you can change the permissions of an existing version, but to update code or other settings you must create a new version
- [from source] (LAMBDA p.211) Console: Layers > Create layer > Name, Description, upload (local .zip or S3 link), Compatible instruction set architectures (one or both), [DATED] Compatible runtimes (up to 15), License
- [p.211-212] API: `aws lambda publish-layer-version --layer-name my-layer --description ... --license-info "MIT" --content S3Bucket=...,S3Key=layer.zip --compatible-runtimes ... --compatible-architectures "arm64" "x86_64"` (runtimes and architectures optional); each call creates a new version
- [from source] (LAMBDA p.212) delete-layer-version: after deleting, no new function can use the version, but functions that already use it keep access; version numbers are never reused for the same layer name
- [from source] (LAMBDA p.212) Permissions: by default the layer is private to the account; share with `add-layer-version-permission --action lambda:GetLayerVersion --principal <account> --version-number N` (one account, all accounts or an organization); the permission applies to ONE version and must be repeated for each new version
- [p.212-213] CloudFormation/SAM: AWS::Lambda::LayerVersion resource (LayerName, Description, Content S3Bucket/S3Key, CompatibleRuntimes) associated with the function through the Layers property (!Ref libs); the example uses nodejs12.x, Tracing Active and policies AWSLambdaBasicExecutionRole, AWSLambda_ReadOnlyAccess, AWSXrayWriteOnlyAccess
- [from source] (LAMBDA p.213) Note: the template example uses nodejs12.x (a runtime with phase 1 deprecation on Mar/31/2023 according to p.102)


## Code signing
- [from source] (LAMBDA p.282) Code signing ensures that only trusted code runs: Lambda verifies each deployment; container image functions are NOT supported; it uses AWS Signer (signing profiles) for functions and layers; validation at deployment, with no impact on execution; no additional cost
- [from source] (LAMBDA p.282) Code signing configuration = list of allowed signing profiles + policy action on failure; layers of a code-signed function must also be signed by an allowed profile; IAM controls who creates configurations (typically admins) and can force developers to create functions with code signing; events (success and block) go to CloudTrail
- [from source] (LAMBDA p.283) Four validations: Integrity (package hash vs signature), Expiry, Mismatch (profile not allowed or signature missing), Revocation
- [from source] (LAMBDA p.283) Failure policy: Warn (allows the deployment, emits a CloudWatch metric and logs to CloudTrail) or Enforce (warns and blocks); the policy is configurable for expiry, mismatch and revocation, NOT for integrity (an integrity failure always blocks)
- [from source] (LAMBDA p.283) Prerequisites: create signing profiles and a signed package in AWS Signer. [DATED] A configuration allows up to 20 signing profiles; choose Warn or Enforce
- [p.283-284] Updating a configuration affects only future deployments; you can only delete a configuration if no function uses it; to enable: associate the configuration with the function (Code signing configuration > Edit)
- [p.284-285] IAM: lambda:CreateCodeSigningConfig/UpdateCodeSigningConfig/GetCodeSigningConfig; condition key lambda:CodeSigningConfigArn forces developers to use a given configuration; CreateFunction is blocked if the parameter is missing or does not match
- [from source] (LAMBDA p.285) API: List/Create/Get/Update/DeleteCodeSigningConfig; per function: Get/Put/DeleteFunctionCodeSigningConfig, ListFunctionsByCodeSigningConfig


## Tags
- [from source] (LAMBDA p.286) Tags enable ABAC and organize by owner/project/department; free-form key-value pairs; they apply at the function level, NOT to versions/aliases and are not part of the version snapshot
- [from source] (LAMBDA p.286) Permissions: lambda:ListTags (for GetFunction/ListTags when there are tags), lambda:TagResource (CreateFunction/TagResource)
- [from source] (LAMBDA p.286) [DATED] Function name limited to 64 characters; default architecture x86_64; tags in the console: Advanced settings > Enable tags
- [p.287-288] Console: Configuration > Tags > Manage tags; filter by tag in the search bar. CLI: create-function --tags, tag-resource, untag-resource --tag-keys; view tags with list-tags (ARN) or get-function (name)
- [from source] (LAMBDA p.289) Filter by tags: Resource Groups Tagging API GetResources (up to 10 filters, each with a key and up to 10 values, with ResourceType)
- [from source] (LAMBDA p.289) [DATED] Requirements: max 50 tags/resource; key up to 128 and value up to 256 UTF-8 characters; case sensitive; prefix aws: reserved (not editable, does not count toward the limit); special characters allowed + - = . _ : / @


## Layers (use in functions)
- [from source] (LAMBDA p.290) Layer = .zip file with extra code/content (libraries, custom runtime, data, config files); serves to reduce package size, share code and separate concerns
- [from source] (LAMBDA p.290) Layers only work on .zip functions; with container images you package the runtime and dependencies in the image itself
- [from source] (LAMBDA p.290) Prerequisites: create the layer; have permission for GetLayerVersion (in your own account via user policy; a layer from another account requires the owner's resource-based policy)
- [from source] (LAMBDA p.290) [DATED] Up to 5 layers per function; total unzipped size of function + layers <= 250 MB
- [from source] (LAMBDA p.290) If the layer is from another account, the function keeps using the version even after deletion or revocation of access, but a new function cannot be created with a deleted version; layers must be compatible with the runtime and architecture
- [from source] (LAMBDA p.291) Console: Layers > Add a layer; source AWS layers / Custom layers (choose layer and version, which lists compatible runtimes and architectures) or Specify an ARN (Verify); order of addition = merge order in the environment, adjustable with Merge earlier / Merge later
- [from source] (LAMBDA p.291) Layers are versioned and each version is immutable; the owner publishes a new version; update the layer version on several functions through the console (Additional resources > Layers), but NOT across accounts
- [p.291-292] CLI: update-function-configuration --layers <full version ARN>...; it REPLACES the previous list (include all on each update); order = extraction order; --layers [] removes all
- [from source] (LAMBDA p.292) If the creator deletes a layer version in use, the function keeps running, but when updating the configuration you must remove the reference to the deleted version
- [p.292-293] Update version: (optional) publish-layer-version --zip-file --compatible-runtimes; (optional) get-function-configuration --query 'Layers[*].Arn'; update-function-configuration --layers with all the versions
- [from source] (LAMBDA p.293) Content extracted into /opt in the order (low to high) of the list; folders with the same name are merged and, on a file conflict, the last extracted layer wins; runtimes add /opt folders to the PATH
- [p.293-294] list-layers --compatible-runtime; list-layer-versions; SAM: AWS::Serverless::LayerVersion (ContentUri, CompatibleRuntimes) referenced in the function's Layers with !Ref; SAM creates a new version when dependencies change; samples blank-nodejs/python/ruby/java



# Quotas and limits [DATED]

> Table of numeric quotas and limits from the 2022 edition.
> Source: AWS Lambda Developer Guide (2022 edition; last release entry on 11/28/2022), abbreviation LAMBDA. Citations `(LAMBDA p.N)` = PDF page (printed = N-22). Lines without an explicit label come from the book; [DATED] = number/limit/runtime/version/CLI that has aged; [extrapolation] = outside the text. Paraphrase; check the current documentation before acting. Note: the reference text is unaccented because the original reading notes were written that way.

## LAMBDA QUOTAS (p.875-877) - full table
- [from source] (LAMBDA p.875) [DATED] Warning: new accounts have reduced concurrency and memory quotas; AWS raises them automatically based on usage; an increase can also be requested (Service Quotas)
- [from source] (LAMBDA p.875) Compute and storage quotas (per Region, can be increased). Columns: default / can be increased up to:
- [from source] (LAMBDA p.875) [DATED] Concurrent executions: 1,000 default; can be increased to tens of thousands
- [from source] (LAMBDA p.875) [DATED] Storage for uploaded functions (.zip) and layers (each function and layer version consumes storage): 75 GB default; can be increased to terabytes
- [from source] (LAMBDA p.875) Storage for functions as container images: stored in Amazon ECR (see the ECR quotas)
- [from source] (LAMBDA p.875) [DATED] Elastic network interfaces per VPC: 250 default; can be increased to hundreds; quota shared with other services (e.g. EFS)
- [from source] (LAMBDA p.875) Configuration, deployment and execution quotas CANNOT be changed; the documentation/logs/console use MB (not MiB) for 1024 KB
- [from source] (LAMBDA p.876) [DATED] Function memory: 128 MB to 10,240 MB in 1 MB increments; CPU proportional to memory; at 1,769 MB it is equivalent to one vCPU
- [from source] (LAMBDA p.876) [DATED] Function timeout: 900 seconds (15 minutes)
- [from source] (LAMBDA p.876) [DATED] Environment variables: 4 KB in aggregate
- [from source] (LAMBDA p.876) [DATED] Function resource-based policy: 20 KB
- [from source] (LAMBDA p.876) [DATED] Layers per function: five
- [from source] (LAMBDA p.876) [DATED] Function burst concurrency: 500 - 3000 (varies by Region)
- [from source] (LAMBDA p.876) [DATED] Invocation payload: 6 MB each for request and response (synchronous); 256 KB (asynchronous)
- [from source] (LAMBDA p.876) [DATED] Deployment package (.zip): 50 MB zipped (direct upload), 250 MB unzipped (applies to all files, including layers and custom runtimes); 3 MB in the console editor
- [from source] (LAMBDA p.876) [DATED] Container image: configuration size (image settings) 16 KB; image code package size 10 GB
- [from source] (LAMBDA p.876) [DATED] Test events (console editor): 10
- [from source] (LAMBDA p.876) [DATED] /tmp storage: between 512 MB and 10,240 MB in 1 MB increments
- [from source] (LAMBDA p.876) [DATED] File descriptors: 1,024; execution processes/threads: 1,024
- [p.876-877] API request quotas: [DATED] invocation requests per Region (req/s) = 10 x the concurrent executions quota (synchronous, all sources) and 10 x the quota (asynchronous, non-AWS sources)
- [from source] (LAMBDA p.877) Invocation requests per Region for asynchronous AWS sources: unlimited accepted requests; execution rate depends on the concurrency available to the function
- [from source] (LAMBDA p.877) [DATED] Invocation requests per version/alias: 10 x allocated provisioned concurrency (only for functions with provisioned concurrency)
- [from source] (LAMBDA p.877) [DATED] GetFunction: 100 req/s; GetPolicy: 15 req/s; other control plane APIs (except invocation, GetFunction, GetPolicy): 15 req/s
- [from source] (LAMBDA p.877) Quotas of other services (IAM, CloudFront for Lambda@Edge, VPC) can affect functions
- [CONTRADICTION] p.831 cites the error "MemorySize ... less than or equal to 3008", while the quota table (p.876) lists a maximum of 10,240 MB; the text explains that new accounts have reduced quotas, but does not reconcile the values.



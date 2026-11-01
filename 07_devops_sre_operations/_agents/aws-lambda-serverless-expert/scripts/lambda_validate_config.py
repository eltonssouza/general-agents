# -*- coding: utf-8 -*-
"""
lambda_validate_config.py - validates an AWS Lambda function configuration against the limits IN THE TEXT
(AWS Lambda Developer Guide, 2022 edition). Read-only, no network, deterministic.

ALL limits are [DATED]: they reflect the 2022 edition. Current quotas may differ.

Usage:
  python -I lambda_validate_config.py CONFIG.json [--json]
  python -I lambda_validate_config.py --example        # prints a sample JSON

Accepted fields (all optional; API-style names, see LAMBDA p.1013+):
  FunctionName, Runtime, PackageType (Zip|Image), Architectures [..], MemorySize, Timeout,
  EphemeralStorage {Size}, Environment {Variables{}}, Layers [..], VpcConfig {SubnetIds, SecurityGroupIds},
  FileSystemConfigs [..], SnapStart {ApplyOn}, Qualifier ("$LATEST" or version/alias),
  ReservedConcurrentExecutions, ProvisionedConcurrentExecutions,
  AccountConcurrencyLimit (default 1000), CodeZippedMB, CodeUnzippedMB, ImageSizeGB,
  AsyncInvokeConfig {MaximumRetryAttempts, MaximumEventAgeInSeconds},
  EventSourceMapping {Source (sqs|kinesis|dynamodb|kafka|msk|mq), BatchSize, FifoQueue,
      MaximumBatchingWindowInSeconds, ParallelizationFactor, TumblingWindowInSeconds,
      QueueVisibilityTimeoutSeconds},
  PayloadSyncMB, PayloadAsyncKB
Output: ERROR (violates a limit in the text), WARNING (risk/best practice), INFO. Each finding carries a page (LAMBDA p.N).
Exit 0 if there is no ERROR; 1 if there is; 2 on incorrect usage.
"""
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "lambda_limits.json"), encoding="utf-8"))["limits"]

EXAMPLE = {
    "FunctionName": "orders-handler",
    "Runtime": "java11",
    "PackageType": "Zip",
    "Architectures": ["arm64"],
    "MemorySize": 20000,
    "Timeout": 1200,
    "EphemeralStorage": {"Size": 2048},
    "Environment": {"Variables": {"AWS_REGION": "x", "1bad": "y", "TABLE": "orders"}},
    "Layers": ["l1", "l2", "l3", "l4", "l5", "l6"],
    "SnapStart": {"ApplyOn": "PublishedVersions"},
    "Qualifier": "$LATEST",
    "ReservedConcurrentExecutions": 950,
    "ProvisionedConcurrentExecutions": 1000,
    "AccountConcurrencyLimit": 1000,
    "AsyncInvokeConfig": {"MaximumRetryAttempts": 3, "MaximumEventAgeInSeconds": 30},
    "EventSourceMapping": {"Source": "sqs", "BatchSize": 50, "FifoQueue": True, "QueueVisibilityTimeoutSeconds": 30},
}

found = []


def add(sev, msg, page):
    found.append({"severity": sev, "message": msg, "citation": "LAMBDA p." + page})


def rng(name, v, lim, unit, page, label=None):
    label = label or name
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        add("ERROR", f"{label} must be numeric (got {v!r})", page)
        return
    if "min" in lim and v < lim["min"]:
        add("ERROR", f"{label}={v}{unit} below the minimum {lim['min']}{unit} [DATED]", page)
    if "max" in lim and v > lim["max"]:
        add("ERROR", f"{label}={v}{unit} above the maximum {lim['max']}{unit} [DATED]", page)


def validate(c):
    # name
    fn = c.get("FunctionName")
    if isinstance(fn, str) and not fn.startswith("arn:") and len(fn) > L["function_name_chars"]["max"]:
        add("ERROR", f"FunctionName has {len(fn)} characters; only the name is limited, to {L['function_name_chars']['max']} [DATED]", L["function_name_chars"]["pages"])
    rt = c.get("Runtime")
    pt = c.get("PackageType", "Zip")
    if pt not in ("Zip", "Image"):
        add("ERROR", f"Invalid PackageType {pt!r}; values in the text: Zip, Image", "1017")
    if pt == "Zip" and rt is not None and rt not in L["runtime_ids_2022"]:
        add("WARNING", f"Runtime {rt!r} is not in the text's table (2022) [DATED]; it may be newer or invalid: check the current documentation", L["runtime_ids_pages"])
    if rt in L["runtime_deprecating"]:
        add("WARNING", f"Runtime {rt}: the text reports {L['runtime_deprecating'][rt]} [DATED]; plan a migration (invocations continue, but without patches)", "103-104")
    archs = c.get("Architectures", ["x86_64"])
    for a in archs:
        if a not in ("x86_64", "arm64"):
            add("ERROR", f"Invalid architecture {a!r}; values: x86_64, arm64", "1017")
    if len(archs) > 1:
        add("ERROR", "A function accepts a single architecture (Architectures with 1 item)", "1199")
    if "arm64" in archs and rt in L["runtime_arm64_unsupported"]:
        add("ERROR", f"Runtime {rt} only runs on x86_64 according to the text's table [DATED]", "103")

    # memory/timeout/ephemeral
    if "MemorySize" in c:
        rng("MemorySize", c["MemorySize"], L["memory_mb"], " MB", L["memory_mb"]["pages"])
        m = c["MemorySize"]
        if isinstance(m, (int, float)) and m > 3008:
            add("INFO", "The text contains a contradiction: an example error cites a 3008 MB ceiling (p.831) and the quota table 10,240 MB (p.876); new accounts may have a reduced quota. Check the account's Service Quotas.", "831, 875-876")
        if isinstance(m, (int, float)) and m >= 1769:
            add("INFO", "1,769 MB equals 1 vCPU; above that there is more than one vCPU (CPU proportional to memory)", "876")
    if "Timeout" in c:
        rng("Timeout", c["Timeout"], L["timeout_s"], " s", L["timeout_s"]["pages"])
    es = (c.get("EphemeralStorage") or {}).get("Size")
    if es is not None:
        rng("EphemeralStorage.Size", es, L["ephemeral_storage_mb"], " MB", L["ephemeral_storage_mb"]["pages"])
        if isinstance(es, (int, float)) and es > 512:
            add("INFO", "/tmp above 512 MB incurs additional cost", "217")

    # env
    vars_ = (c.get("Environment") or {}).get("Variables") or {}
    total = 0
    for k, v in vars_.items():
        total += len(str(k).encode("utf-8")) + len(str(v).encode("utf-8"))
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]+", str(k)):
            add("ERROR", f"Invalid env var key {k!r}: starts with a letter, >=2 characters, only letters/numbers/underscore", "219")
        if k in L["env_reserved"]:
            add("ERROR", f"Reserved env var cannot be set: {k}", L["env_reserved_pages"])
        if re.search(r"(?i)(password|passwd|secret|token|api_?key)", str(k)):
            add("WARNING", f"Env var {k!r} looks like a secret: the text recommends Secrets Manager for database credentials and encryption (KMS/client-side)", "219, 223")
    if total > L["env_vars_total_bytes"]["max"]:
        add("ERROR", f"Env vars add up to {total} bytes; aggregate limit 4 KB (4096) [DATED]", L["env_vars_total_bytes"]["pages"])

    # layers
    ly = c.get("Layers") or []
    if len(ly) > L["layers_per_function"]["max"]:
        add("ERROR", f"{len(ly)} layers; maximum {L['layers_per_function']['max']} per function [DATED]", L["layers_per_function"]["pages"])
    if ly and pt == "Image":
        add("ERROR", "Layers do not apply to container image functions (the text covers layers for .zip)", "214, 208")

    # sizes
    if "CodeZippedMB" in c and c["CodeZippedMB"] > L["zip_upload_mb"]["max"]:
        add("ERROR", f"Zip of {c['CodeZippedMB']} MB above 50 MB for direct upload [DATED]; use S3", L["zip_upload_mb"]["pages"])
    if "CodeUnzippedMB" in c and c["CodeUnzippedMB"] > L["unzipped_mb"]["max"]:
        add("ERROR", f"Unzipped {c['CodeUnzippedMB']} MB above 250 MB (includes layers) [DATED]", L["unzipped_mb"]["pages"])
    if "ImageSizeGB" in c and c["ImageSizeGB"] > L["container_image_gb"]["max"]:
        add("ERROR", f"Image {c['ImageSizeGB']} GB above 10 GB [DATED]", L["container_image_gb"]["pages"])
    if "PayloadSyncMB" in c and c["PayloadSyncMB"] > L["payload_sync_mb"]["max"]:
        add("ERROR", f"Synchronous payload {c['PayloadSyncMB']} MB above 6 MB [DATED]", L["payload_sync_mb"]["pages"])
    if "PayloadAsyncKB" in c and c["PayloadAsyncKB"] > L["payload_async_kb"]["max"]:
        add("ERROR", f"Asynchronous payload {c['PayloadAsyncKB']} KB above 256 KB [DATED]", L["payload_async_kb"]["pages"])

    # VPC
    vpc = c.get("VpcConfig") or {}
    if len(vpc.get("SecurityGroupIds", [])) > L["vpc_security_groups"]["max"]:
        add("ERROR", "VpcConfig.SecurityGroupIds above 5 [DATED]", L["vpc_security_groups"]["pages"])
    if len(vpc.get("SubnetIds", [])) > L["vpc_subnets"]["max"]:
        add("ERROR", "VpcConfig.SubnetIds above 16 [DATED]", L["vpc_subnets"]["pages"])
    if vpc and len(vpc.get("SubnetIds", [])) == 1:
        add("WARNING", "A single subnet: consider several AZs for resilience [extrapolation: the text covers resilience in general terms, p.826-827]", "826-827")

    # concurrency
    acct = c.get("AccountConcurrencyLimit", L["account_concurrency_default"]["value"])
    res = c.get("ReservedConcurrentExecutions")
    prov = c.get("ProvisionedConcurrentExecutions")
    if res is not None:
        if res < 0:
            add("ERROR", "ReservedConcurrentExecutions cannot be negative", "1161")
        if res > acct - L["min_unreserved_concurrency"]["value"]:
            add("ERROR", f"Reserved {res} > account limit ({acct}) - 100 = {acct - 100}; 100 must stay unreserved [DATED]", L["min_unreserved_concurrency"]["pages"])
        if res == 0:
            add("WARNING", "Reserved = 0 blocks ALL invocations (total throttle); in async the events go to the DLQ/on-failure destination (used as an emergency brake)", "250, 301")
    if prov is not None:
        q = c.get("Qualifier")
        if prov < 1:
            add("ERROR", "ProvisionedConcurrentExecutions minimum 1", "1171")
        if q in (None, "$LATEST"):
            add("ERROR", "Provisioned concurrency is not supported on $LATEST: configure it on a published version or alias", "254")
        if res is not None and prov > res:
            add("ERROR", "You cannot allocate more provisioned than reserved when reserved is set", "247, 253")
        if res is not None and prov == res:
            add("WARNING", "Provisioned == reserved: all invocations use provisioned and $LATEST is throttled", "247, 253")
        if prov > acct:
            add("ERROR", "Provisioned above the account concurrency limit", "253")
        if (c.get("SnapStart") or {}).get("ApplyOn") == "PublishedVersions":
            add("ERROR", "SnapStart and provisioned concurrency cannot be used on the same version", "353-354")

    # SnapStart
    ss = c.get("SnapStart") or {}
    if ss.get("ApplyOn") == "PublishedVersions":
        if rt is not None and rt not in L["snapstart_runtimes"]:
            add("ERROR", f"SnapStart in the 2022 edition only supports {L['snapstart_runtimes']} [DATED]; got {rt}", L["snapstart_pages"])
        if "arm64" in archs:
            add("ERROR", "SnapStart does not support arm64 (2022 edition) [DATED]", L["snapstart_pages"])
        if es is not None and es > 512:
            add("ERROR", "SnapStart does not support ephemeral storage > 512 MB (2022 edition) [DATED]", L["snapstart_pages"])
        if c.get("FileSystemConfigs"):
            add("ERROR", "SnapStart does not support EFS (2022 edition) [DATED]", L["snapstart_pages"])
        if c.get("Qualifier") in (None, "$LATEST"):
            add("WARNING", "SnapStart only acts on published versions/aliases, not on $LATEST", L["snapstart_pages"])

    # async
    ac = c.get("AsyncInvokeConfig") or {}
    if "MaximumRetryAttempts" in ac:
        rng("MaximumRetryAttempts", ac["MaximumRetryAttempts"], L["async_retry_attempts"], "", L["async_retry_attempts"]["pages"])
    if "MaximumEventAgeInSeconds" in ac:
        rng("MaximumEventAgeInSeconds", ac["MaximumEventAgeInSeconds"], L["async_max_event_age_s"], " s", L["async_max_event_age_s"]["pages"])

    # event source mapping
    e = c.get("EventSourceMapping") or {}
    if e:
        src = str(e.get("Source", "")).lower()
        stream = src in ("kinesis", "dynamodb")
        if "BatchSize" in e:
            rng("BatchSize", e["BatchSize"], L["esm_batch_size"], "", L["esm_batch_size"]["pages"])
            if src == "sqs" and e.get("FifoQueue") and e["BatchSize"] > 10:
                add("ERROR", "SQS FIFO: BatchSize maximum 10 [DATED]", "1003-1004")
            if e["BatchSize"] > 10 and e.get("MaximumBatchingWindowInSeconds", 0) < 1 and src in ("sqs", "kinesis", "dynamodb"):
                add("ERROR", "BatchSize > 10 requires MaximumBatchingWindowInSeconds >= 1", "1005")
        if "MaximumBatchingWindowInSeconds" in e:
            rng("MaximumBatchingWindowInSeconds", e["MaximumBatchingWindowInSeconds"], L["esm_batching_window_s"], " s", L["esm_batching_window_s"]["pages"])
        for k, lk in (("ParallelizationFactor", "esm_parallelization_factor"), ("TumblingWindowInSeconds", "esm_tumbling_window_s")):
            if k in e:
                if not stream:
                    add("ERROR", f"{k} only applies to stream sources (DynamoDB/Kinesis)", "1002, 1006")
                rng(k, e[k], L[lk], "", L[lk]["pages"])
        vt = e.get("QueueVisibilityTimeoutSeconds")
        to = c.get("Timeout")
        if src == "sqs" and vt is not None and to is not None:
            need = L["sqs_visibility_timeout_factor"]["min_times_function_timeout"] * to + e.get("MaximumBatchingWindowInSeconds", 0)
            if vt < to:
                add("ERROR", "Queue visibility timeout lower than the function timeout (function creation fails / duplicate invocations)", "873")
            elif vt < need:
                add("WARNING", f"Visibility timeout {vt}s < recommended 6 x timeout + window = {need}s [DATED]", "774-775")
        if src in ("kafka", "msk", "mq") and to is not None and to > 840:
            add("ERROR", "Timeout > 14 min with Kafka/MSK/MQ as the source (the text limits it to 14 min) [DATED]", "687")

    return found


def main(argv):
    if "--example" in argv:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    try:
        cfg = json.load(open(args[0], encoding="utf-8"))
    except Exception as ex:
        print("ERROR reading JSON:", ex)
        return 2
    res = validate(cfg)
    if "--json" in argv:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        if not res:
            print("No findings against the limits in the text (2022 edition; [DATED]).")
        for r in res:
            print(f"[{r['severity']}] {r['message']} ({r['citation']})")
        print("\nNote: [DATED] limits from the 2022 edition; check Service Quotas and the current documentation.")
    return 1 if any(r["severity"] == "ERROR" for r in res) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

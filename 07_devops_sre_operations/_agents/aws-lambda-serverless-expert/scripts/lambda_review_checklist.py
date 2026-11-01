# -*- coding: utf-8 -*-
"""
lambda_review_checklist.py - Lambda function review checklist based on the best practices and the
risks DESCRIBED in the AWS Lambda Developer Guide (2022 edition). Read-only, no network.

Usage:
  python -I lambda_review_checklist.py --list [--json]            # lists the items with pages
  python -I lambda_review_checklist.py ANSWERS.json [--json]      # evaluates answers
  python -I lambda_review_checklist.py --config CONFIG.json [ANSWERS.json]
        # automatically fills in what can be inferred from an API-style config
        # (DeadLetterConfig, TracingConfig, ReservedConcurrentExecutions, Layers, ...); ANSWERS completes the rest.

ANSWERS.json: {"C2": "yes", "C8": "no", "F1": "na", ...}  (yes | no | na; the Portuguese sim | nao are also accepted).
Items without an answer = "not evaluated".
Output: "no" items by severity (HIGH/MEDIUM/LOW), not-evaluated items and coverage.
Each item carries the page (LAMBDA p.N) and [DATED] when it depends on a number/version/price.
Exit 0 whenever the run is valid (the checklist is advisory); 2 on incorrect usage.
"""
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# (id, category, severity, question, page, dated)
ITEMS = [
    ("C1", "code", "LOW", "Is the handler separated from the business logic (unit-testable)?", "871", False),
    ("C2", "code", "HIGH", "Are SDK clients and database connections initialized OUTSIDE the handler (reuse of the execution environment)?", "871", False),
    ("C3", "code", "HIGH", "Is no user/event/sensitive data kept in the execution environment between invocations?", "871", False),
    ("C4", "code", "MEDIUM", "Do persistent connections use keep-alive (Lambda drops idle connections)?", "871", False),
    ("C5", "code", "LOW", "Do operational parameters come from environment variables rather than being hard-coded?", "871", False),
    ("C6", "code", "MEDIUM", "Are dependencies under control (packaged) instead of relying on the bundled SDK that Lambda updates?", "872", False),
    ("C7", "code", "MEDIUM", "Is the package minimized to what is needed (Java/.NET: selective SDK modules; lightweight frameworks)?", "872", False),
    ("C8", "code", "HIGH", "Is there a safeguard against recursive code (a function that triggers itself, including via S3/SNS/SQS)? Is there a brake plan (reserved concurrency = 0)?", "872, 250, 301", False),
    ("C9", "code", "MEDIUM", "Does it avoid undocumented/non-public APIs?", "872", False),
    ("C10", "code", "HIGH", "Is the code idempotent (duplicate or resent events do not cause a duplicate effect)?", "872, 301, 324", False),
    ("F1", "configuration", "MEDIUM", "Was memory tuned by performance testing (REPORT line / Power Tuning), not by guesswork?", "872", True),
    ("F2", "configuration", "MEDIUM", "Was the timeout set by load testing, taking into account network dependencies that may not scale?", "872-873", True),
    ("F3", "configuration", "HIGH", "Is the execution role least-privilege (no broad wildcards)?", "873, 72-73", False),
    ("F4", "configuration", "MEDIUM", "Were payload, file descriptors and /tmp checked against the quotas?", "873, 876", True),
    ("F5", "configuration", "LOW", "Were unused functions/versions removed (they count toward the storage limit)?", "873, 875", True),
    ("F6", "configuration", "HIGH", "With SQS as the source: queue visibility timeout >= 6 x function timeout (+ batch window)?", "873, 774-775", True),
    ("M1", "observability", "MEDIUM", "Are there CloudWatch alarms on Lambda metrics (errors, duration, throttles) instead of metrics created in code?", "873", False),
    ("M2", "observability", "LOW", "Does it use a logging library with levels (ERR/ERROR/WARNING) to detect application errors?", "873", False),
    ("M3", "observability", "LOW", "Is there cost anomaly detection (Cost Anomaly Detection) for unexpected spend?", "873", True),
    ("M4", "observability", "MEDIUM", "Is tracing (X-Ray or ADOT) active where it makes sense?", "791-792, 391-393", False),
    ("S1", "streams", "MEDIUM", "Were BatchSize and the batching window tested/tuned for the source?", "873", True),
    ("S2", "streams", "HIGH", "Is there an alarm on IteratorAge to detect a stalled/lagging stream?", "874, 325", True),
    ("S3", "streams", "MEDIUM", "Kinesis: are shards and partition key chosen for good distribution (1 concurrent invocation per shard)?", "873-874", False),
    ("S4", "streams", "HIGH", "Do 'poison' records (that always fail) avoid blocking the shard (bisect, max retry/age, on-failure destination, report batch item failures)?", "325, 1002, 774", True),
    ("E1", "errors", "HIGH", "Does asynchronous invocation have a DLQ or on-failure destination configured?", "301, 305", True),
    ("E2", "errors", "HIGH", "With SQS as the source, is the DLQ on the source queue (not on the function) and is maxReceiveCount adequate (>= 5)?", "307, 774", True),
    ("E3", "errors", "MEDIUM", "Is ReportBatchItemFailures enabled to avoid reprocessing the whole batch?", "774", False),
    ("E4", "errors", "MEDIUM", "Were the async retries/maximum event age reviewed (default: 2 retries, up to 6 h)?", "301-302", True),
    ("V1", "versions", "MEDIUM", "Do event sources and permissions point to an alias (not to $LATEST or a fixed version)?", "229", False),
    ("V2", "versions", "HIGH", "Is provisioned concurrency (if used) on a version/alias, never on $LATEST, and does it not exceed reserved?", "254, 247", True),
    ("V3", "versions", "LOW", "Was gradual rollout (alias routing / CodeDeploy) considered for production?", "229-230, 828, 839", False),
    ("R1", "concurrency", "MEDIUM", "Is reserved concurrency used to protect downstream resources and/or isolate a critical function?", "242, 252", True),
    ("R2", "concurrency", "HIGH", "Are PutFunctionConcurrency/DeleteFunctionConcurrency permissions restricted (they affect the pool of the other functions)?", "252", False),
    ("R3", "concurrency", "MEDIUM", "Was cold start measured and, if critical, handled (provisioned concurrency or SnapStart Java 11, never both on the same version)?", "253, 353-354", True),
    ("N1", "network", "MEDIUM", "Function in a VPC: does it have a route to the internet (NAT) or VPC endpoints for AWS services?", "836-837, 269-270", False),
    ("N2", "network", "MEDIUM", "Function in a VPC: were the ENI-per-VPC limit and subnets across several AZs considered?", "837, 875", True),
    ("N3", "network", "MEDIUM", "Does relational database access use a pool/proxy (RDS Proxy) instead of a connection per invocation?", "273-274", False),
    ("SEC1", "security", "HIGH", "Do secrets (database passwords etc.) come from Secrets Manager and not from plain-text env vars?", "219", False),
    ("SEC2", "security", "MEDIUM", "Do sensitive env vars use a customer-managed KMS key or client-side encryption when required?", "223-224", False),
    ("SEC3", "security", "HIGH", "Function URL: auth type AWS_IAM, or NONE justified with CORS/throttling reviewed?", "335-338", False),
    ("SEC4", "security", "MEDIUM", "Does the resource-based policy limit the principal (source-arn/source-account) and not grant broad access?", "88-93", False),
    ("SEC5", "security", "LOW", "Is the runtime not deprecated/being deprecated (security patches)?", "103-104", True),
]

# automatic inferences from a config (API style)


def infer(cfg):
    r = {}
    dl = (cfg.get("DeadLetterConfig") or {}).get("TargetArn")
    dest = cfg.get("DestinationConfig") or (cfg.get("AsyncInvokeConfig") or {}).get("DestinationConfig") or {}
    if "DeadLetterConfig" in cfg or "DestinationConfig" in cfg or "AsyncInvokeConfig" in cfg:
        r["E1"] = "yes" if (dl or (dest.get("OnFailure") or {}).get("Destination")) else "no"
    tc = (cfg.get("TracingConfig") or {}).get("Mode")
    if tc is not None:
        r["M4"] = "yes" if tc == "Active" else "no"
    res = cfg.get("ReservedConcurrentExecutions")
    if "ReservedConcurrentExecutions" in cfg:
        r["R1"] = "yes" if res is not None else "no"
    q = cfg.get("Qualifier")
    if cfg.get("ProvisionedConcurrentExecutions") is not None:
        ok = q not in (None, "$LATEST") and (res is None or cfg["ProvisionedConcurrentExecutions"] <= res)
        r["V2"] = "yes" if ok else "no"
    ss = (cfg.get("SnapStart") or {}).get("ApplyOn") == "PublishedVersions"
    if ss and cfg.get("ProvisionedConcurrentExecutions") is not None:
        r["R3"] = "no"
    vars_ = (cfg.get("Environment") or {}).get("Variables") or {}
    if vars_:
        r["SEC1"] = "no" if any(re.search(r"(?i)(password|passwd|secret|token|api_?key)", k) for k in vars_) else "yes"
    if "KMSKeyArn" in cfg and vars_:
        r["SEC2"] = "yes" if cfg.get("KMSKeyArn") else "no"
    es = cfg.get("EventSourceMapping") or {}
    if es.get("Source") == "sqs" and es.get("QueueVisibilityTimeoutSeconds") is not None and cfg.get("Timeout") is not None:
        need = 6 * cfg["Timeout"] + es.get("MaximumBatchingWindowInSeconds", 0)
        r["F6"] = "yes" if es["QueueVisibilityTimeoutSeconds"] >= need else "no"
    if es.get("Source") == "sqs" and "FunctionResponseTypes" in es:
        r["E3"] = "yes" if "ReportBatchItemFailures" in es["FunctionResponseTypes"] else "no"
    rt = cfg.get("Runtime")
    if rt in ("nodejs12.x", "dotnetcore3.1"):
        r["SEC5"] = "no"
    return r


def main(argv):
    as_json = "--json" in argv
    if "--list" in argv:
        rows = [dict(id=i, category=c, severity=s, question=q, citation="LAMBDA p." + p, dated=d) for i, c, s, q, p, d in ITEMS]
        if as_json:
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        else:
            for x in rows:
                print(f"{x['id']:5} [{x['severity']:6}] {x['category']:15} {x['question']} ({x['citation']}){' [DATED]' if x['dated'] else ''}")
        return 0
    cfg_path = None
    args = []
    it = iter(argv)
    for a in it:
        if a == "--config":
            cfg_path = next(it, None)
        elif not a.startswith("--"):
            args.append(a)
    ans = {}
    try:
        if cfg_path:
            ans.update(infer(json.load(open(cfg_path, encoding="utf-8"))))
        if args:
            ans.update({k.upper(): str(v).lower() for k, v in json.load(open(args[0], encoding="utf-8")).items()})
    except Exception as ex:
        print("ERROR reading input:", ex)
        return 2
    if not ans:
        print(__doc__)
        return 2
    valid = {i[0] for i in ITEMS}
    unknown = [k for k in ans if k not in valid]
    fails, notev, ok, na = [], [], 0, 0
    for i, c, s, q, p, d in ITEMS:
        a = ans.get(i)
        # Portuguese answers (nao/sim) remain accepted as user input
        if a in ("nao", "não", "no", "false"):
            fails.append((s, i, c, q, p, d))
        elif a in ("sim", "yes", "true"):
            ok += 1
        elif a == "na":
            na += 1
        else:
            notev.append((i, q))
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    fails.sort(key=lambda t: (order[t[0]], t[1]))
    if as_json:
        print(json.dumps({"failures": [dict(severity=s, id=i, category=c, question=q, citation="LAMBDA p." + p, dated=d) for s, i, c, q, p, d in fails],
                          "not_evaluated": [i for i, _ in notev], "ok": ok, "na": na, "unknown": unknown}, indent=2, ensure_ascii=False))
        return 0
    print(f"Items: {len(ITEMS)} | ok: {ok} | no: {len(fails)} | n/a: {na} | not evaluated: {len(notev)}")
    for s, i, c, q, p, d in fails:
        print(f"[{s}] {i} ({c}) {q} (LAMBDA p.{p}){' [DATED]' if d else ''}")
    if notev:
        print("\nNot evaluated: " + ", ".join(i for i, _ in notev))
    if unknown:
        print("Unknown ids ignored: " + ", ".join(unknown))
    print("\nAdvisory checklist derived from the guide (2022 edition); [DATED] items depend on numbers/versions that have changed. Check the current documentation.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

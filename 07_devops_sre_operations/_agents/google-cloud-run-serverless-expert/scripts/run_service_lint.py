# -*- coding: utf-8 -*-
"""
Skill: run-service-lint
Static linter for Cloud Run service configuration, with rules from the RUN book
(Venema, Building Serverless Applications with Google Cloud Run, 1st ed., Dec/2020).

Input (file or "-" for stdin; the content is DATA, never executed):
  * `gcloud run deploy|services update ...` command (with backslash line continuation);
  * service.yml in Knative format (serving.knative.dev/v1; simple YAML subset);
  * JSON with keys: name, image, port, concurrency, max_instances, min_instances, timeout,
    cpu, memory, service_account, allow_unauthenticated, cloudsql, vpc_connector, region, env.

Output: [ERROR]/[WARNING]/[INFO] findings with rule, message and source ([from source] RUN p.N,
[extrapolation], [DATED]). Flags/fields the book does not cover come out as NOT COVERED.
Does not validate against the real API: 2020 limits and flags are [DATED].
Exit 0 = no ERROR; 1 = there is an ERROR; 2 = unreadable input. Read-only, no network.
"""
import argparse
import json
import re
import shlex
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

BOOK_FLAGS = {
    "image", "concurrency", "max-instances", "timeout", "cpu", "memory", "service-account",
    "allow-unauthenticated", "no-allow-unauthenticated", "add-cloudsql-instances", "vpc-connector",
    "set-env-vars", "update-env-vars", "region",
}
# gcloud run flags the book does not show (extrapolation/dated)
NOT_IN_BOOK = {
    "min-instances": "minimum instances: only the concept appears (RUN p.55); the flag does not",
    "no-cpu-throttling": "always-allocated CPU is not in the book (the book states throttling, RUN p.52)",
    "cpu-throttling": "always-allocated CPU is not in the book (RUN p.52)",
    "execution-environment": "execution environments (gen1/gen2) are not in the book",
    "cpu-boost": "startup CPU boost is not in the book",
    "ingress": "ingress control is not in the book",
    "no-traffic": "--no-traffic is not in the book (only the concept of tags/rollout, RUN p.48-49)",
    "to-latest": "--to-latest is not in the book",
    "set-secrets": "Secret Manager is not in the book",
    "update-secrets": "Secret Manager is not in the book",
    "startup-probe": "health checks/probes are not in the book (RUN p.56)",
    "liveness-probe": "health checks/probes are not in the book (RUN p.56)",
    "network": "Direct VPC egress is not in the book",
    "subnet": "Direct VPC egress is not in the book",
    "vpc-egress": "vpc-egress is not in the book",
    "session-affinity": "session affinity: the book says it was not supported in 2020 (RUN p.106)",
    "port": "the --port flag does not appear (default port 8080 can be overridden, RUN p.44)",
    "platform": "the book only shows the 'fully-managed' prompt (RUN p.45)",
    "source": "deploy via --source is not in the book",
    "args": "--args is not in the book",
    "command": "--command is not in the book",
    "labels": "--labels is not in the book",
    "add-volume": "volumes are not in the book",
    "revision-suffix": "--revision-suffix is not in the book",
    "tag": "revision tags: only the concept appears (RUN p.49); the flag does not",
}

SENSITIVE_RE = re.compile(r"(PASSWORD|PASSWD|SECRET|TOKEN|API[_-]?KEY|PRIVATE[_-]?KEY|CREDENTIAL)", re.I)
PRIVATE_IP_RE = re.compile(r"(?<![\d.])(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\d])")


class Finding:
    def __init__(self, sev, rule, msg, src):
        self.sev, self.rule, self.msg, self.src = sev, rule, msg, src

    def as_dict(self):
        return {"severity": self.sev, "rule": self.rule, "message": self.msg, "source": self.src}


# ---------------------------------------------------------------- minimal YAML
def _strip_comment(line):
    out, q = [], None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(v):
    v = v.strip()
    if v == "" or v in ("~", "null"):
        return None
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v == "[]":
        return []
    if v == "{}":
        return {}
    if v.startswith("[") and v.endswith("]"):
        return [_scalar(x) for x in v[1:-1].split(",") if x.strip()]
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


_KV = re.compile(r"""^((?:"[^"]*"|'[^']*'|[^\s:'"\-][^:]*?|-[^\s:][^:]*?))\s*:(?:\s+(.*)|$)""")


def parse_yaml(text):
    lines = []
    for raw in text.splitlines():
        if raw.strip() in ("---", "...") or not raw.strip():
            continue
        s = _strip_comment(raw)
        if not s.strip():
            continue
        lines.append([len(s) - len(s.lstrip(" ")), s.strip()])
    pos = [0]

    def node(indent):
        c = lines[pos[0]][1]
        if c == "-" or c.startswith("- "):
            return lst(indent)
        return mp(indent)

    def lst(indent):
        items = []
        while pos[0] < len(lines) and lines[pos[0]][0] == indent and (lines[pos[0]][1] == "-" or lines[pos[0]][1].startswith("- ")):
            c = lines[pos[0]][1]
            rest = c[1:].strip()
            if rest == "":
                pos[0] += 1
                items.append(node(lines[pos[0]][0]) if pos[0] < len(lines) and lines[pos[0]][0] > indent else None)
            elif _KV.match(rest):
                lines[pos[0]] = [indent + 2, rest]
                items.append(mp(indent + 2))
            else:
                items.append(_scalar(rest))
                pos[0] += 1
        return items

    def mp(indent):
        d = {}
        while pos[0] < len(lines) and lines[pos[0]][0] == indent and not (lines[pos[0]][1] == "-" or lines[pos[0]][1].startswith("- ")):
            c = lines[pos[0]][1]
            m = _KV.match(c)
            if not m:
                raise ValueError(f"unsupported YAML line: {c!r}")
            key = _scalar(m.group(1)) if m.group(1)[0] in "\"'" else m.group(1).strip()
            val = (m.group(2) or "").strip()
            pos[0] += 1
            if val == "":
                if pos[0] < len(lines) and (lines[pos[0]][0] > indent or (lines[pos[0]][0] == indent and (lines[pos[0]][1] == "-" or lines[pos[0]][1].startswith("- ")))):
                    d[key] = node(lines[pos[0]][0])
                else:
                    d[key] = None
            else:
                d[key] = _scalar(val)
        return d

    if not lines:
        return {}
    return node(lines[0][0])


# ---------------------------------------------------------------- normalization
def new_cfg():
    return {"name": None, "image": None, "port": None, "concurrency": None, "max_instances": None,
            "min_instances": None, "timeout": None, "cpu": None, "memory": None, "service_account": None,
            "allow_unauthenticated": None, "cloudsql": [], "vpc_connector": None, "region": None,
            "env": {}, "unsupported": [], "unknown": [], "yaml_problems": [], "kind": None}


def parse_env(s):
    d = {}
    for part in re.split(r",(?=[A-Za-z_][A-Za-z0-9_]*=)", s):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v
    return d


def from_command(text):
    t = re.sub(r"\\\s*\n", " ", text)
    t = "\n".join(l for l in t.splitlines() if not l.strip().startswith("#"))
    cfg = new_cfg()
    try:
        toks = shlex.split(t, posix=True)
    except ValueError as e:
        raise ValueError(f"command could not be parsed: {e}")
    # locate 'run deploy NAME' or 'run services update NAME'
    try:
        i = toks.index("run")
    except ValueError:
        raise ValueError("could not find 'gcloud run ...' in the command")
    rest = toks[i + 1:]
    pos = []
    j = 0
    while j < len(rest):
        tok = rest[j]
        if tok.startswith("--"):
            name = tok[2:]
            val = None
            if "=" in name:
                name, val = name.split("=", 1)
            elif name in ("allow-unauthenticated", "no-allow-unauthenticated", "no-cpu-throttling", "cpu-throttling", "cpu-boost", "no-traffic", "to-latest"):
                val = True
            elif j + 1 < len(rest) and not rest[j + 1].startswith("--"):
                val = rest[j + 1]
                j += 1
            apply_flag(cfg, name, val)
        else:
            pos.append(tok)
        j += 1
    if len(pos) >= 3 and pos[0] == "services" and pos[1] == "update":
        cfg["name"] = pos[2]
    elif len(pos) >= 2 and pos[0] == "deploy":
        cfg["name"] = pos[1]
    return cfg


def apply_flag(cfg, name, val):
    if name == "image":
        cfg["image"] = val
    elif name == "concurrency":
        cfg["concurrency"] = val
    elif name == "max-instances":
        cfg["max_instances"] = val
    elif name == "timeout":
        cfg["timeout"] = val
    elif name == "cpu":
        cfg["cpu"] = val
    elif name == "memory":
        cfg["memory"] = val
    elif name == "service-account":
        cfg["service_account"] = val
    elif name == "allow-unauthenticated":
        cfg["allow_unauthenticated"] = "both" if cfg["allow_unauthenticated"] is False else True
    elif name == "no-allow-unauthenticated":
        cfg["allow_unauthenticated"] = "both" if cfg["allow_unauthenticated"] is True else False
    elif name == "add-cloudsql-instances":
        cfg["cloudsql"] += [x for x in str(val).split(",") if x]
    elif name == "vpc-connector":
        cfg["vpc_connector"] = val
    elif name in ("set-env-vars", "update-env-vars"):
        cfg["env"].update(parse_env(str(val)))
    elif name == "region":
        cfg["region"] = val
    elif name in NOT_IN_BOOK:
        cfg["unsupported"].append((name, NOT_IN_BOOK[name]))
        if name == "min-instances":
            cfg["min_instances"] = val
        if name == "port":
            cfg["port"] = val
    elif name in BOOK_FLAGS:
        pass
    else:
        cfg["unknown"].append(name)


def from_knative(doc):
    cfg = new_cfg()
    cfg["kind"] = (doc.get("apiVersion"), doc.get("kind"))
    if doc.get("apiVersion") != "serving.knative.dev/v1":
        cfg["yaml_problems"].append(("R19", f"apiVersion must be serving.knative.dev/v1 (got: {doc.get('apiVersion')!r})", "[from source] RUN p.76"))
    if doc.get("kind") != "Service":
        cfg["yaml_problems"].append(("R19", f"kind must be Service (got: {doc.get('kind')!r})", "[from source] RUN p.76"))
    meta = doc.get("metadata") or {}
    cfg["name"] = meta.get("name")
    spec = doc.get("spec") or {}
    tpl = spec.get("template") or {}
    if not tpl:
        cfg["yaml_problems"].append(("R19", "spec.template missing", "[from source] RUN p.76"))
    tmeta = (tpl.get("metadata") or {})
    ann = dict((meta.get("annotations") or {}))
    ann.update(tmeta.get("annotations") or {})
    tspec = tpl.get("spec") or {}
    cfg["concurrency"] = tspec.get("containerConcurrency")
    cfg["timeout"] = tspec.get("timeoutSeconds")
    cfg["service_account"] = tspec.get("serviceAccountName")
    conts = tspec.get("containers") or []
    if not isinstance(conts, list) or not conts:
        cfg["yaml_problems"].append(("R01", "spec.template.spec.containers empty", "[from source] RUN p.76"))
    else:
        c = conts[0]
        cfg["image"] = c.get("image")
        ports = c.get("ports") or []
        if ports and isinstance(ports, list) and isinstance(ports[0], dict):
            cfg["port"] = ports[0].get("containerPort")
        lim = ((c.get("resources") or {}).get("limits") or {})
        cfg["cpu"] = lim.get("cpu")
        cfg["memory"] = lim.get("memory")
        for e in c.get("env") or []:
            if isinstance(e, dict) and "name" in e:
                cfg["env"][str(e["name"])] = "" if e.get("value") is None else str(e.get("value"))
    # annotations (mapping is NOT in the book: extrapolation)
    for k, v in ann.items():
        k = str(k)
        if k.endswith("/maxScale"):
            cfg["max_instances"] = v
        elif k.endswith("/minScale"):
            cfg["min_instances"] = v
            cfg["unsupported"].append(("annotation " + k, "scaling annotations are not in the book (only the concept, RUN p.55)"))
        elif k.endswith("cloudsql-instances"):
            cfg["cloudsql"] += [x for x in str(v).split(",") if x]
        elif k.endswith("vpc-access-connector"):
            cfg["vpc_connector"] = v
        else:
            cfg["unsupported"].append(("annotation " + k, "annotation not covered by the book"))
    return cfg


def from_json(d):
    cfg = new_cfg()
    for k in ("name", "image", "port", "concurrency", "max_instances", "min_instances", "timeout", "cpu",
              "memory", "service_account", "vpc_connector", "region"):
        if k in d:
            cfg[k] = d[k]
    if "allow_unauthenticated" in d:
        cfg["allow_unauthenticated"] = d["allow_unauthenticated"]
    cs = d.get("cloudsql") or []
    cfg["cloudsql"] = [cs] if isinstance(cs, str) else list(cs)
    cfg["env"] = {str(k): "" if v is None else str(v) for k, v in (d.get("env") or {}).items()}
    if d.get("min_instances") is not None:
        cfg["unsupported"].append(("min_instances", NOT_IN_BOOK["min-instances"]))
    return cfg


# ---------------------------------------------------------------- utilities
def to_int(v):
    try:
        return int(str(v).strip())
    except Exception:
        return None


def mem_bytes(v):
    if v is None:
        return None
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([A-Za-z]*)\s*", str(v))
    if not m:
        return None
    n, u = float(m.group(1)), m.group(2).lower()
    mult = {"": 1, "k": 1e3, "ki": 1024, "m": 1e6, "mi": 1024 ** 2, "g": 1e9, "gi": 1024 ** 3}
    return n * mult[u] if u in mult else None


def timeout_seconds(v):
    if v is None:
        return None
    s = str(v).strip()
    m = re.fullmatch(r"(\d+)\s*(s|m|h)?", s)
    if not m:
        return None
    n = int(m.group(1))
    return n * {"s": 1, "m": 60, "h": 3600, None: 1}[m.group(2)]


def has_var(s):
    return s is not None and "$" in str(s)


# ---------------------------------------------------------------- rules
def lint(cfg):
    F = []
    add = lambda sev, rule, msg, src: F.append(Finding(sev, rule, msg, src))
    for r, m, s in cfg["yaml_problems"]:
        add("ERROR", r, m, s)

    # R01/R02 image
    img = cfg["image"]
    if not img:
        add("ERROR", "R01", "container image missing: the service needs an image (a container that listens on HTTP).", "[from source] RUN p.36, 45")
    elif str(img).startswith("ko://"):
        add("ERROR", "R02", "image with ko:// placeholder: resolve it with `ko resolve` before replace/deploy (it is not a valid image URI).", "[from source] RUN p.76")

    # R04 service account
    if not cfg["service_account"]:
        add("WARNING", "R04", "no dedicated service account: the service uses the default account (Project Editor, more than 3000 permissions). Create one account per service with minimal bindings.", "[from source] RUN p.114-115 [DATED: the default account and its roles have changed]")

    # R05 public access / R22 conflict
    au = cfg["allow_unauthenticated"]
    if au == "both":
        add("ERROR", "R22", "--allow-unauthenticated and --no-allow-unauthenticated together: contradictory.", "[from source] RUN p.45, 116")
    elif au is True:
        add("INFO", "R05", "PUBLIC service (allUsers binding + roles/run.invoker). Confirm this is intentional; internal services use --no-allow-unauthenticated + ID token.", "[from source] RUN p.112-113, 116-118")
    elif au is None:
        add("INFO", "R05", "access policy not provided (with `replace`/YAML, access is managed separately through IAM; in an interactive deploy gcloud asks).", "[from source] RUN p.76")
    nm = (cfg["name"] or "").lower()
    if au is True and re.search(r"(worker|internal|private|backend|product-api)", nm):
        add("WARNING", "R05b", f"the name '{cfg['name']}' suggests an internal service/worker, but it is public. In the book the worker is private and only the caller's account has Invoker.", "[inference] from RUN p.128, 130-131, 124-125")

    # R06 concurrency
    conc = to_int(cfg["concurrency"])
    if cfg["concurrency"] is None:
        add("INFO", "R06", "concurrency not set: the default was 250 in Nov/2020, probably too high for most apps; measure CPU under load.", "[from source] RUN p.55 [DATED]")
    elif conc is not None and conc > 250:
        add("WARNING", "R06", f"concurrency {conc} above the default of 250 that the author already considers high; the autoscaler will act on CPU (a slower signal).", "[from source] RUN p.55 [DATED]")
    elif conc == 1:
        add("INFO", "R06", "concurrency 1: exclusive access per request, good for CPU-intensive or non-thread-safe apps; cost and scale go up (one container per request).", "[from source] RUN p.54")
    elif conc is not None and conc < 1:
        add("WARNING", "R06", "concurrency < 1: value not described in the book; check the documentation.", "[extrapolation] [DATED]")

    # R07 max instances
    mx = to_int(cfg["max_instances"])
    db = bool(cfg["cloudsql"]) or any(re.search(r"(^|_)(DB|DATABASE|MYSQL|POSTGRES|REDIS)", k, re.I) for k in cfg["env"])
    if cfg["max_instances"] is None:
        if db:
            add("WARNING", "R07", "service with a database attached and no instance ceiling: the default was 1000 containers; combine --max-instances with a connection pool (total = instances x connections per instance) <= the database's optimal concurrency.", "[from source] RUN p.54, 93-96")
        else:
            add("INFO", "R07", "no --max-instances: default of 1000 containers (limit and cost); set a ceiling compatible with downstream systems.", "[from source] RUN p.37, 54, 96 [DATED]")
    elif mx is not None and mx < 1:
        add("ERROR", "R07", "max-instances < 1 is invalid.", "[extrapolation]")
    elif mx is not None and mx > 1000:
        add("INFO", "R07", f"max-instances {mx} > 1000 requires a quota increase.", "[from source] RUN p.54 [DATED]")

    # R08 timeout
    ts = timeout_seconds(cfg["timeout"])
    if cfg["timeout"] is not None and ts is None and not has_var(cfg["timeout"]):
        add("WARNING", "R08", f"timeout '{cfg['timeout']}' cannot be interpreted (use seconds, e.g. 900).", "[extrapolation]")
    elif ts is not None:
        if ts > 3600:
            add("ERROR", "R08", f"timeout {ts}s exceeds the 60 min request maximum cited in the book (2020).", "[from source] RUN p.129 [DATED]")
        elif ts > 1800:
            add("INFO", "R08", f"timeout {ts}s > 30 min: if the caller is Cloud Tasks, the dispatch deadline goes up to 30 min; split the work.", "[from source] RUN p.129 [DATED]")
        elif ts <= 0:
            add("ERROR", "R08", "timeout must be positive.", "[extrapolation]")

    # R09 memory
    mb = mem_bytes(cfg["memory"])
    if mb is not None and mb > 4 * 1024 ** 3 * 1.0001:
        add("WARNING", "R09", f"memory {cfg['memory']} above 4 GiB, the maximum mentioned in 2020; check the current limit. Remember that the container disk uses memory.", "[from source] RUN p.56, 121 [DATED]")
    elif cfg["memory"] is not None and mb is None and not has_var(cfg["memory"]):
        add("WARNING", "R09", f"memory '{cfg['memory']}' cannot be interpreted.", "[extrapolation]")
    if mb is not None and mb <= 4 * 1024 ** 3 * 1.0001:
        add("INFO", "R09", "the container filesystem lives in memory: disk writes consume this memory; exceeding the limit kills the container.", "[from source] RUN p.56")

    # R11 cloud sql
    for inst in cfg["cloudsql"]:
        if has_var(inst):
            add("INFO", "R11", f"Cloud SQL instance '{inst}' uses a shell variable: not verified (expected format PROJECT:REGION:INSTANCE).", "[from source] RUN p.91")
        elif not re.fullmatch(r"[^:\s]+:[^:\s]+:[^:\s]+", str(inst)):
            add("ERROR", "R11", f"Cloud SQL instance '{inst}' is not in the PROJECT:REGION:INSTANCE format.", "[from source] RUN p.91")
        elif cfg["region"] and not has_var(cfg["region"]) and str(inst).split(":")[1] != cfg["region"]:
            add("WARNING", "R11", f"service region ({cfg['region']}) differs from the Cloud SQL region ({str(inst).split(':')[1]}): more latency and cost.", "[from source] RUN p.85")
    for k, v in cfg["env"].items():
        if re.search(r"root@", str(v)):
            add("WARNING", "R12", f"{k} connects as root: in production use an application user without administrative privilege (least privilege) and a set password.", "[from source] RUN p.89")
        if cfg["cloudsql"] and str(v).startswith(("mysql://", "postgres://")) and "/cloudsql/" not in str(v) and re.search(r"@(tcp\()?\d", str(v)):
            add("WARNING", "R12b", f"{k} seems to use a direct IP with Cloud SQL attached: prefer the /cloudsql/ socket (managed Proxy, IAM, TLS).", "[from source] RUN p.90-91")

    # R13 secrets in env
    for k, v in cfg["env"].items():
        if SENSITIVE_RE.search(k) and str(v) != "" and not has_var(v):
            add("WARNING", "R13", f"variable {k} seems to carry a plaintext secret in the deploy/YAML (it stays in history, in the state and in the immutable revision). The book does not cover Secret Manager: [extrapolation] consider a secrets manager; [from source] keep sensitive data out of the logs (RUN p.163) and protect the Terraform state (RUN p.150).", "[extrapolation] + [from source] RUN p.150, 163")

    # R14/R15 private network
    priv = [k for k, v in cfg["env"].items() if PRIVATE_IP_RE.search(str(v))]
    if priv and not cfg["vpc_connector"]:
        add("WARNING", "R14", f"variables {priv} point to a private IP, but there is no --vpc-connector: Cloud Run is not in the VPC and cannot reach private IPs without the Connector (same region as the resource).", "[from source] RUN p.102-105")
    if cfg["vpc_connector"]:
        add("INFO", "R15", "the VPC Connector is not pay-per-use: it charges even when idle (2 to 10 instances, /28 range); delete it when experiments end.", "[from source] RUN p.104, 108 [DATED]")

    # R16 port
    p = to_int(cfg["port"])
    if p is not None and p != 8080:
        add("INFO", "R16", f"port {p} differs from the default 8080: make sure the container listens exactly on it (the default can be overridden at deploy).", "[from source] RUN p.44")

    # R17/R18 outside the book
    for name, why in cfg["unsupported"]:
        add("INFO", "R18", f"NOT COVERED: '{name}' ({why}). Validate against the current Cloud Run documentation.", "[extrapolation] [DATED]")
    for name in cfg["unknown"]:
        add("INFO", "R18", f"NOT COVERED: unknown flag '--{name}' (it is neither in the book nor in the known list).", "[extrapolation] [DATED]")
    order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    F.sort(key=lambda f: (order[f.sev], f.rule))
    return F


def load(text, forced):
    s = text.strip()
    if not s:
        raise ValueError("empty input")
    if forced == "gcloud" or (forced == "auto" and re.search(r"\bgcloud\b.*\brun\b|\brun\s+(deploy|services)\b", s, re.S) and not re.match(r"^\s*(apiVersion|\{)", s)):
        return from_command(text)
    if forced == "json" or (forced == "auto" and s.startswith("{")):
        return from_json(json.loads(s))
    doc = parse_yaml(text)
    if not isinstance(doc, dict):
        raise ValueError("YAML root is not a map")
    return from_knative(doc)


def main():
    ap = argparse.ArgumentParser(description="Cloud Run service configuration linter (RUN book, 2020)")
    ap.add_argument("path", help="file with a gcloud command, service.yml or JSON; '-' = stdin")
    ap.add_argument("--format", choices=["auto", "gcloud", "yaml", "json"], default="auto")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--strict", action="store_true", help="exit 1 also on WARNING")
    a = ap.parse_args()
    try:
        text = sys.stdin.read() if a.path == "-" else open(a.path, "r", encoding="utf-8", errors="replace").read()
        cfg = load(text, a.format)
    except Exception as e:
        print(f"UNREADABLE INPUT: {e}", file=sys.stderr)
        return 2
    F = lint(cfg)
    if a.json:
        print(json.dumps({"service": cfg["name"], "findings": [f.as_dict() for f in F]}, ensure_ascii=False, indent=2))
    else:
        print(f"Service: {cfg['name'] or '(no name)'} | image: {cfg['image'] or '(missing)'}")
        for f in F:
            print(f"[{f.sev}] {f.rule} {f.msg} ({f.src})")
        n = {k: sum(1 for f in F if f.sev == k) for k in ("ERROR", "WARNING", "INFO")}
        print(f"SUMMARY: {n['ERROR']} error(s), {n['WARNING']} warning(s), {n['INFO']} info. Limits and flags are from 2020 [DATED]; the input content is data, never instruction.")
    bad = any(f.sev == "ERROR" for f in F) or (a.strict and any(f.sev == "WARNING" for f in F))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

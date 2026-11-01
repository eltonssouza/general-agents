# -*- coding: utf-8 -*-
"""
Skill: run-deploy-checklist
Generates a deploy/production checklist for a Cloud Run service from profiles,
with items the RUN book (Venema, Dec/2020) supports (with PDF page) and items
marked [extrapolation]/[DATED]. Deterministic, no network, read-only.

Usage:
  python -I deploy_checklist.py --list
  python -I deploy_checklist.py [--profile api|frontend|worker|db|sessions|all ...] [--format md|json] [--no-extra]
Profiles combine (e.g. --profile api --profile db). No --profile = base + api.
`extra` items (outside the book) come out in a separate section and can be omitted with --no-extra.
Page = PDF page (printed + 28).
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# (id, text, source)  source: "RUN p.N" => from the book; "[extrapolation]" => outside the book
BASE = [
    ("B01", "The Cloud Run API is enabled in the project and the chosen region is the same as that of the databases/resources the service uses.", "RUN p.45-46, 85"),
    ("B02", "The container listens on the expected port (default 8080) and starts fast (ready in seconds).", "RUN p.44, 38, 55"),
    ("B03", "The app handles SIGTERM: it closes connections and flushes buffers within ~10 s [DATED].", "RUN p.50"),
    ("B04", "No useful work outside the lifecycle of a request (no background thread for after the response); asynchronous work goes to Cloud Tasks.", "RUN p.52, 127"),
    ("B05", "No data to preserve in container memory/disk; the disk consumes memory (4 GB limit in 2020 [DATED]).", "RUN p.55-56"),
    ("B06", "Small image (multi-stage/distroless, ko, Jib or Buildpacks) without unnecessary tools.", "RUN p.71-78"),
    ("B07", "A dedicated service account per service (--service-account), not the default account (Project Editor), with minimal bindings.", "RUN p.114-115, 124"),
    ("B08", "Access policy decided: public (--allow-unauthenticated/allUsers) or private (--no-allow-unauthenticated + invoker only for whoever needs it).", "RUN p.112, 117"),
    ("B09", "Concurrency reviewed (the Nov/2020 default of 250 was high) and max-instances set according to cost and downstream systems [DATED].", "RUN p.54-55, 96"),
    ("B10", "Logs as JSON on stdout with severity; no PII or secrets in the logs.", "RUN p.158, 160-163"),
    ("B11", "Rollback known: `gcloud run services update-traffic NAME --to-revisions REV=100`.", "RUN p.49"),
    ("B12", "Configuration via environment variables (portability) and the service definition versioned (service.yml or IaC).", "RUN p.76, 92, 140"),
    ("B13", "Non-serverless resources (Cloud SQL, Memorystore, VPC Connector) have a shutdown plan so they do not keep generating cost.", "RUN p.86, 102, 104, 108"),
]

PROFILES = {
    "api": ("API/web service with HTTP traffic", [
        ("A01", "If other services call this API: call with an ID token (audience = target URL) and a Cloud Run Invoker binding on the target service, only for the caller's account.", "RUN p.116-119, 124-125"),
        ("A02", "Latency between services considered (~7-9 ms per call via the GFE [DATED]); prefer coarse-grained calls and avoid naive parallelism.", "RUN p.120"),
        ("A03", "Trace ID from the X-Cloud-Trace-Context header in the logs and propagated in outgoing calls.", "RUN p.165-169"),
        ("A04", "Monitoring: CPU/memory/latency metrics and log-based metrics for alerts.", "RUN p.171-172"),
    ]),
    "frontend": ("Public frontend that calls a private backend", [
        ("F01", "Frontend and backend with different service accounts; backend `--no-allow-unauthenticated`; invoker binding on the backend for the frontend's account.", "RUN p.123-125"),
        ("F02", "Backend URL via an environment variable (`--set-env-vars`), no rebuild.", "RUN p.124"),
        ("F03", "After creating the binding, wait ~20 s if a permission error appears.", "RUN p.124"),
    ]),
    "worker": ("Task worker (Cloud Tasks)", [
        ("W01", "Private worker (`--no-allow-unauthenticated`), timeout and resources tuned (demo: 900 s, 2 CPU, 2G), its own service account.", "RUN p.128, 130-131"),
        ("W02", "Invoker binding on the worker for the scheduling app's account; Cloud Tasks Enqueuer role on the queue; Service Account User to create tasks with an OIDC token.", "RUN p.131-133"),
        ("W03", "Coherent dispatch deadline (10 min default, up to 30; Run's maximum request 60 min [DATED]); long work split into parts.", "RUN p.129"),
        ("W04", "Retry (minBackoff, maxBackoff, maxDoublings, maxAttempts) and rate limit (maxDispatchesPerSecond, maxConcurrentDispatches) reviewed; the defaults of 1000 are high.", "RUN p.133-135"),
        ("W05", "Idempotency: record the task state in a database (duplicate delivery is possible, < 0.001% [DATED]) and review exhausted tasks.", "RUN p.134-136"),
    ]),
    "db": ("Service with Cloud SQL", [
        ("D01", "Connection through the managed Proxy (`--add-cloudsql-instances PROJ:REG:INST`, /cloudsql/ socket), not by direct IP; `--require-ssl` as a barrier.", "RUN p.89-91"),
        ("D02", "Passwordless `root@%` user removed; application user without administrative privilege; password on root.", "RUN p.88-89"),
        ("D03", "Transactional concurrency controlled: `--max-instances` x connections per instance (`SetMaxOpenConns`) <= the database optimum (a small multiple of vCPUs).", "RUN p.93-96"),
        ("D04", "Production: high availability (two zones), automated backups, storage increase, CPU alert; the app tolerates ~1 min of downtime.", "RUN p.97-98"),
        ("D05", "If using a private IP: VPC Connector in the same region (`--vpc-connector`).", "RUN p.92, 104-105"),
    ]),
    "sessions": ("HTTP sessions / Memorystore", [
        ("S01", "Sessions in an external store (Memorystore, Firestore or Cloud SQL), never in container memory; signed cookie with Secure, HttpOnly, SameSite=Strict.", "RUN p.99-101"),
        ("S02", "Memorystore only has a private IP: VPC Connector in the same region; memory alert (no size autoscaling).", "RUN p.102-105"),
        ("S03", "Do not rely on session affinity (not supported in 2020 and never meant for storing sessions) [DATED].", "RUN p.106-107"),
    ]),
    "iac": ("Infrastructure as code (Terraform)", [
        ("I01", "Credentials via ADC (`gcloud auth application-default login`), no downloaded service account key.", "RUN p.143-144"),
        ("I02", "`terraform plan -out` reviewed before `apply`; state treated as a secret; the service's IAM policy declared.", "RUN p.148-152"),
        ("I03", "Gradual revision rollout outside Terraform.", "RUN p.143"),
    ]),
}

EXTRA = [
    ("X01", "Check the current documentation for CPU/memory, timeout, concurrency and instance limits (the book's numbers are from 2020).", "[extrapolation] [DATED]"),
    ("X02", "Secrets in a secrets manager (the book does not cover Secret Manager).", "[extrapolation]"),
    ("X03", "Evaluate minimum instances for cold start (the book only mentions the concept, RUN p.55), always-allocated CPU, health checks and Jobs, which the book does not cover.", "[extrapolation] [DATED]"),
    ("X04", "Review the current default service account and the organization policies (they have changed since 2020).", "[extrapolation] [DATED]"),
]


def build(profiles, extra):
    sections = [("base", "Base (every service)", BASE)]
    for p in profiles:
        title, items = PROFILES[p]
        sections.append((p, title, items))
    out = {"sections": [], "extra": []}
    for key, title, items in sections:
        out["sections"].append({"id": key, "title": title, "items": [{"id": i, "text": t, "source": s if s.startswith("[") else f"[from source] ({s})"} for i, t, s in items]})
    if extra:
        out["extra"] = [{"id": i, "text": t, "source": s} for i, t, s in EXTRA]
    return out


def main():
    ap = argparse.ArgumentParser(description="Cloud Run deploy checklist (RUN book, 2020)")
    ap.add_argument("--profile", action="append", choices=sorted(PROFILES) + ["all"])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--no-extra", action="store_true")
    a = ap.parse_args()
    if a.list:
        print("base: items for every service")
        for k in sorted(PROFILES):
            print(f"{k}: {PROFILES[k][0]}")
        print("all: all profiles")
        return 0
    profs = a.profile or ["api"]
    if "all" in profs:
        profs = sorted(PROFILES)
    seen, uniq = set(), []
    for p in profs:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    data = build(uniq, not a.no_extra)
    if a.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    print("# Cloud Run deploy checklist (RUN book, 1st ed. Dec/2020; numbers and flags [DATED])")
    print(f"Profiles: base + {', '.join(uniq)}  |  pages = PDF (printed + 28)\n")
    for s in data["sections"]:
        print(f"## {s['title']}")
        for it in s["items"]:
            print(f"- [ ] {it['id']} {it['text']} {it['source']}")
        print()
    if data["extra"]:
        print("## Outside the book (check the current documentation)")
        for it in data["extra"]:
            print(f"- [ ] {it['id']} {it['text']} {it['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

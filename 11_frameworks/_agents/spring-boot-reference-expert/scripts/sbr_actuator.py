# -*- coding: utf-8 -*-
"""
sbr_actuator.py - Actuator endpoint map according to "Spring Boot Reference Documentation, Version 2.7.18" (SBR).
Pages = PDF page (printed = N-20). Stdlib only; no network; does not run the framework.

Usage (python -I):
  python -I scripts/sbr_actuator.py list [--web-only | --jmx-only]
  python -I scripts/sbr_actuator.py show ID
  python -I scripts/sbr_actuator.py exposure [--web-include a,b|*] [--web-exclude x,y] [--jmx-include ...] [--jmx-exclude ...]
                                              [--jmx-enabled] [--enabled-by-default false] [--enable id[,id]] [--disable id[,id]]
  python -I scripts/sbr_actuator.py paths [--base-path /actuator] [--path-mapping health=healthcheck,...] [--port 8080]
                                          [--management-port 8081] [--groups live,ready] [--probes] [--add-additional-paths]
  python -I scripts/sbr_actuator.py health-status [--order a,b,c] [--http-mapping down=503,fatal=503] --status UP,DOWN,FATAL

Coverage is only that of the 2.7.18 text; what the text does not say => "NOT COVERED" ([DATED]: newer versions differ).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sbr_common as C  # noqa: E402,F401

# id, description (paraphrase), kind ('general'|'web'), web_exposed_default, jmx_exposed_default, requirements, pages
EP = [
    ("auditevents", "application audit events", "general", False, True, "AuditEventRepository bean", "441"),
    ("beans", "list of all Spring beans", "general", False, True, "", "441"),
    ("caches", "available caches", "general", False, True, "", "441"),
    ("conditions", "conditions evaluated on configuration/auto-configuration classes and why they matched or not", "general", False, True, "", "441"),
    ("configprops", "consolidated list of @ConfigurationProperties", "general", False, True, "", "441"),
    ("env", "ConfigurableEnvironment properties", "general", False, True, "", "441"),
    ("flyway", "applied Flyway migrations", "general", False, True, "one or more Flyway beans", "441"),
    ("health", "application health information", "general", True, True, "", "441"),
    ("httptrace", "HTTP traces (by default the last 100 exchanges)", "general", False, True, "HttpTraceRepository bean", "441"),
    ("info", "arbitrary application information", "general", False, True, "", "441"),
    ("integrationgraph", "Spring Integration graph", "general", False, True, "spring-integration-core", "441"),
    ("loggers", "shows and changes log levels at runtime", "general", False, True, "", "441"),
    ("liquibase", "applied Liquibase migrations", "general", False, True, "one or more Liquibase beans", "441"),
    ("metrics", "application metrics", "general", False, True, "", "441"),
    ("mappings", "list of @RequestMapping paths", "general", False, True, "", "441"),
    ("quartz", "Quartz Scheduler jobs", "general", False, True, "", "441"),
    ("scheduledtasks", "scheduled tasks", "general", False, True, "", "441"),
    ("sessions", "query/removal of Spring Session sessions", "general", False, True, "servlet app with Spring Session", "441"),
    ("shutdown", "shuts the application down gracefully; only with jar packaging; DISABLED by default", "general", False, True, "", "441"),
    ("startup", "startup steps collected by ApplicationStartup", "general", False, True, "SpringApplication with BufferingApplicationStartup", "441"),
    ("threaddump", "thread dump", "general", False, True, "", "441"),
    ("heapdump", "heap dump file (HPROF on HotSpot; PHD on OpenJ9)", "web", False, None, "web app", "442"),
    ("jolokia", "JMX beans over HTTP", "web", False, None, "jolokia-core; not available on WebFlux", "442"),
    ("logfile", "content of the log file (accepts the Range header)", "web", False, None, "logging.file.name or logging.file.path", "442"),
    ("prometheus", "metrics in the Prometheus scrape format", "web", False, None, "micrometer-registry-prometheus", "442"),
]
DISABLED_BY_DEFAULT = {"shutdown"}
PAGES_EXPOSURE = "443-444"


def _csv(v):
    if v is None:
        return None
    return [x.strip() for x in v.split(",") if x.strip()]


def cmd_list(a):
    print("Actuator endpoints (SBR 2.7.18, p.441-444). 'web'=exposed by default over HTTP; 'jmx'=exposed by default over JMX; N/A = web only.")
    print("%-17s %-6s %-4s %-4s %s" % ("ID", "kind", "web", "jmx", "description / requirement"))
    for (i, d, k, w, j, req, pg) in EP:
        if a.web_only and k != "web":
            continue
        if a.jmx_only and j is None:
            continue
        print("%-17s %-6s %-4s %-4s %s%s (SBR p.%s)" % (i, k, "yes" if w else "no", "N/A" if j is None else "yes", d,
                                                    ("; requires: " + req) if req else "", pg))
    print("By default all endpoints are enabled, except shutdown (p.442); default web exposure = health only (p.444-445).")
    return 0


def cmd_show(a):
    for (i, d, k, w, j, req, pg) in EP:
        if i == a.id.lower():
            print("%s: %s" % (i, d))
            print("  kind: %s | enabled by default: %s | web-exposed by default: %s | JMX-exposed by default: %s" % (
                k, "no" if i in DISABLED_BY_DEFAULT else "yes", "yes" if w else "no", "N/A (web only)" if j is None else "yes"))
            if req:
                print("  requirement: %s" % req)
            print("  default HTTP path: /actuator/%s (SBR p.440, 449)" % i)
            print("  properties: management.endpoint.%s.enabled (p.442); management.endpoint.%s.cache.time-to-live (p.448)" % (i, i))
            if i == "health":
                print("  more: show-details/show-components never|when-authorized|always (p.454); groups and probes (p.460-465); HTTP status 503 for DOWN and OUT_OF_SERVICE (p.457-458)")
            if i == "loggers":
                print("  change level: POST with {\"configuredLevel\":\"DEBUG\"}; null resets (p.477); with CSRF on and the default security config, POST gives 403 (p.448)")
            if i == "shutdown":
                print("  enable: management.endpoint.shutdown.enabled=true (p.442); POST requires handling CSRF (p.448)")
            if i == "prometheus":
                print("  scrape at /actuator/prometheus; by default the endpoint is NOT available and must be exposed (p.494)")
                print("  prometheus.yml (p.494): scrape_configs: - job_name: \"spring\" / metrics_path: \"/actuator/prometheus\" / static_configs: - targets: [\"HOST:PORT\"]")
                print("  exemplars: SpanContextSupplier bean + enable in Prometheus + OpenMetrics format; Pushgateway: simpleclient_pushgateway + management.metrics.export.prometheus.pushgateway.enabled=true (p.494)")
            if i == "metrics":
                print("  /actuator/metrics and /actuator/metrics/<name>?tag=K:V (p.517); NOT exposed by default (needs exposure.include)")
                print("  use the name in the code (jvm.memory.max), not the one normalized by the monitoring system (jvm_memory_max in Prometheus) (p.517)")
                print("  the reported value is the SUM of the statistics of all meters that match name and tags (p.517)")
                print("  ?tag=area:nonheap sums Code Cache + Compressed Class Space + Metaspace; for Metaspace only: ?tag=area:nonheap&tag=id:Metaspace (p.517)")
            return 0
    print("NOT COVERED: '%s' is not an endpoint listed in SBR p.441-442 (2.7.18)." % a.id)
    return 2


def _pattern_set(lst, universe):
    if lst is None:
        return set()
    if "*" in lst:
        return set(universe)
    return {x.lower() for x in lst}


def cmd_exposure(a):
    ids = [e[0] for e in EP]
    web_inc = _csv(a.web_include) if a.web_include is not None else ["health"]
    web_exc = _csv(a.web_exclude) or []
    jmx_inc = _csv(a.jmx_include) if a.jmx_include is not None else ["*"]
    jmx_exc = _csv(a.jmx_exclude) or []
    enabled_default = (a.enabled_by_default or "true").lower() != "false"
    enable = set(_csv(a.enable) or [])
    disable = set(_csv(a.disable) or [])
    enabled = {}
    for i in ids:
        base = (i not in DISABLED_BY_DEFAULT) if enabled_default else False
        if i in enable:
            base = True
        if i in disable:
            base = False
        enabled[i] = base
    print("Parameters: web include=%s exclude=%s | jmx include=%s exclude=%s | enabled-by-default=%s" % (
        ",".join(web_inc), ",".join(web_exc) or "-", ",".join(jmx_inc), ",".join(jmx_exc) or "-", str(enabled_default).lower()))
    web_inc_s = _pattern_set(web_inc, ids)
    web_exc_s = _pattern_set(web_exc, ids)
    jmx_inc_s = _pattern_set(jmx_inc, ids)
    jmx_exc_s = _pattern_set(jmx_exc, ids)
    web_avail, jmx_avail = [], []
    for (i, d, k, w, j, req, pg) in EP:
        in_web = enabled[i] and i in web_inc_s and i not in web_exc_s
        in_jmx = enabled[i] and j is not None and i in jmx_inc_s and i not in jmx_exc_s
        print("  %-17s enabled=%-3s web=%-9s jmx=%s" % (i, "yes" if enabled[i] else "no",
                                                       "AVAILABLE" if in_web else "-",
                                                       ("AVAILABLE" if in_jmx else "-") if j is not None else "N/A"))
        if in_web:
            web_avail.append(i)
        if in_jmx:
            jmx_avail.append(i)
    print("\nAvailable = enabled AND exposed (SBR p.440); exclude beats include (p.444); a disabled endpoint is removed from the context (p.443).")
    print("Web: %s" % (", ".join(web_avail) or "(none)"))
    if a.jmx_enabled:
        print("JMX: %s" % (", ".join(jmx_avail) or "(none)"))
    else:
        print("JMX: the JMX feature is only on with spring.jmx.enabled=true (default false, p.474); without it, the result above for JMX is only theoretical (use --jmx-enabled).")
    risky = [i for i in web_avail if i in ("env", "configprops", "heapdump", "threaddump", "shutdown", "loggers", "beans", "mappings", "logfile", "httptrace", "sessions")]
    if risky:
        print("ALERT [inference from p.444-445: endpoints may contain sensitive information; protect them]: %s" % ", ".join(risky))
    return 0


def cmd_paths(a):
    base = a.base_path if a.base_path is not None else "/actuator"
    mapping = {}
    for kv in (_csv(a.path_mapping) or []):
        if "=" in kv:
            k, v = kv.split("=", 1)
            mapping[k.strip()] = v.strip().lstrip("/")
    port = a.management_port or a.port
    base = base if base.startswith("/") else "/" + base
    if base == "/":
        root = ""
    else:
        root = base.rstrip("/")
    print("HTTP port: %s (management port: %s)" % (a.port, a.management_port or "same"))
    print("base-path: %s (default /actuator; SBR p.450)" % base)
    if base != "/actuator" and base != "/":
        print("  discovery page (links): %s [inference: p.449 describes this for the management context path, not for base-path]" % base)
    elif base == "/actuator":
        print("  discovery page (links): /actuator (disable with management.endpoints.web.discovery.enabled=false; p.449)")
    else:
        print("  base-path '/': [inference] p.449 only says that, with the management context path '/', the discovery page is disabled; "
              "the book does not say this about base-path (p.470-471 use base-path '/' without commenting on the discovery page). Check in the environment (GET /).")
    for (i, d, k, w, j, req, pg) in EP:
        seg = mapping.get(i, i)
        print("  %-17s http://localhost:%s%s/%s" % (i, port, root, seg))
    if a.groups or a.probes:
        names = _csv(a.groups) or []
        if a.probes:
            names += ["liveness", "readiness"]
        print("\nHealth groups (management.endpoint.health.group.<name>): /health/<name> (p.460)")
        for n in names:
            print("  %s%s/%s/%s" % ("http://localhost:%s" % port, root, mapping.get("health", "health"), n))
        if a.probes:
            print("Probes: /actuator/health/liveness and /actuator/health/readiness (p.462); automatic only in a Kubernetes environment; "
                  "management.endpoint.health.probes.enabled=true in any environment (p.463).")
        if a.add_additional_paths:
            print("probes.add-additional-paths=true: /livez and /readyz on the MAIN port (p.463). Group additional-path: prefix server: or management: and a single segment (p.462).")
    print("\nNote: with a different management.server.port, base-path is relative to management.server.base-path; "
          "without its own port, it is relative to server.servlet.context-path or spring.webflux.base-path (p.450).")
    return 0


def cmd_health(a):
    default_order = ["down", "out-of-service", "up", "unknown"]
    order = _csv(a.order) or default_order
    mapping = {}
    for kv in (_csv(a.http_mapping) or []):
        if "=" in kv:
            k, v = kv.split("=", 1)
            mapping[k.strip().lower()] = int(v)
    if not mapping:
        mapping = {"down": 503, "out-of-service": 503}
        note = "default mapping: DOWN and OUT_OF_SERVICE = 503; the others = 200 (SBR p.457-458)"
    else:
        note = "a custom mapping DISABLES the DOWN/OUT_OF_SERVICE defaults; reconfigure them if you want to keep them (SBR p.457)"
    sts = [x.lower().replace("_", "-") for x in (_csv(a.status) or [])]
    print(note)
    print("severity order (first = most severe): %s" % ", ".join(order))
    known = [s for s in sts if s in order]
    if not sts:
        print("provide --status A,B,... to compute the aggregate status")
        return 0
    if not known:
        agg = "unknown"
        print("no status known to the aggregator => UNKNOWN (p.454)")
    else:
        agg = sorted(known, key=order.index)[0]
        unk = [s for s in sts if s not in order]
        if unk:
            print("statuses outside the configured order (ignored by the aggregator): %s" % ", ".join(unk))
    print("aggregate status: %s; HTTP %s" % (agg.upper().replace("-", "_"), mapping.get(agg, 200)))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("list")
    p.add_argument("--web-only", action="store_true")
    p.add_argument("--jmx-only", action="store_true")
    p = sub.add_parser("show")
    p.add_argument("id")
    p = sub.add_parser("exposure")
    p.add_argument("--web-include")
    p.add_argument("--web-exclude")
    p.add_argument("--jmx-include")
    p.add_argument("--jmx-exclude")
    p.add_argument("--jmx-enabled", action="store_true")
    p.add_argument("--enabled-by-default")
    p.add_argument("--enable")
    p.add_argument("--disable")
    p = sub.add_parser("paths")
    p.add_argument("--base-path")
    p.add_argument("--path-mapping")
    p.add_argument("--port", default="8080")
    p.add_argument("--management-port")
    p.add_argument("--groups")
    p.add_argument("--probes", action="store_true")
    p.add_argument("--add-additional-paths", action="store_true")
    p = sub.add_parser("health-status")
    p.add_argument("--order")
    p.add_argument("--http-mapping")
    p.add_argument("--status")
    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        return 0
    return {"list": cmd_list, "show": cmd_show, "exposure": cmd_exposure, "paths": cmd_paths, "health-status": cmd_health}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

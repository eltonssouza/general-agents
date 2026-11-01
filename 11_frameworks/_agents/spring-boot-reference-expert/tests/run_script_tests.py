# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the package scripts' deterministic test cases (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]   # --src enables verify_citations.py and audit_tokens.py
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
The expected values come from the SBR 2.7.18 text itself (pages cited in each test).
"""
import argparse
import json
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL = []
OK = []
S = os.path.join("scripts")
FX = os.path.join("tests", "fixtures")


def run(args, expect_rc=None):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG, env=env)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def has(out, *subs):
    return all(s in out for s in subs)


def _sem_default_ok():
    idx = json.load(open(os.path.join(PKG, "scripts", "sbr_index.json"), encoding="utf-8"))
    P = idx["props"]
    t = P.get("management.metrics.export.appoptics.api-token", {})
    u = P.get("management.metrics.export.appoptics.host-tag", {})
    return bool(t.get("sem_default")) and not u.get("sem_default") and u.get("default") == "instance"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join(S, "sbr_lookup.py")
    P = os.path.join(S, "sbr_propcheck.py")
    K = os.path.join(S, "sbr_checklist.py")
    A = os.path.join(S, "sbr_actuator.py")
    R = os.path.join(S, "sbr_precedence.py")

    # ---- lookup
    rc, o = run([L, "--prop", "server.port"])
    check("lookup --prop server.port -> A.11 p.757 default 8080", rc == 0 and has(o, "p.757", "8080"), o)
    rc, o = run([L, "--prop", "spring.main.lazy-initialization"])
    check("lookup --prop lazy-initialization -> default false p.672 and body p.74", rc == 0 and has(o, "672", "false", "74"), o)
    rc, o = run([L, "--prop", "spring.profile.active"])
    check("lookup --prop key with a typo -> UNKNOWN + suggestion", rc == 2 and has(o, "UNKNOWN in the text", "spring.profiles.active"), o)
    rc, o = run([L, "--dep", "jackson-databind"])
    check("lookup --dep jackson-databind -> 2.13.5 p.844", rc == 0 and has(o, "2.13.5", "p.844"), o)
    rc, o = run([L, "--dep", "quarkus-core"])
    check("lookup --dep nonexistent -> NOT COVERED", rc == 2 and "NOT COVERED" in o, o)
    rc, o = run([L, "graalvm"])
    check("lookup graalvm -> NOT COVERED", rc == 2 and "NOT COVERED" in o, o)
    rc, o = run([L, "native", "image"])
    check("lookup 'native image' -> NOT COVERED", rc == 2 and "NOT COVERED" in o, o)
    rc, o = run([L, "Internationalization"])
    check("lookup Internationalization -> table-of-contents title only (7.5 p.146, printed 126): POINTER ONLY, not COVERED (R5)", rc == 3 and has(o, "LEVEL: POINTER ONLY", "7.5", "p.146", "126", "references/03"), o)
    rc, o = run([L, "ConditionalOnProperty"])
    check("lookup ConditionalOnProperty -> p.236", rc == 0 and "p.236" in o, o)
    rc, o = run([L, "--page", "90"])
    check("lookup --page 90 -> printed 70, section 7.2", rc == 0 and has(o, "printed 70", "7.2"), o)
    rc, o = run([L, "--toc", "13.2"])
    check("lookup --toc 13.2 -> Endpoints p.440", rc == 0 and has(o, "13.2", "Endpoints", "p.440"), o)
    rc, o = run([L, "--chapters"])
    check("lookup --chapters -> 17 chapters + appendices", rc == 0 and has(o, "Getting Started", "PDF p.27", "Appendix F"), o)
    rc, o = run([L, "--gaps"])
    check("lookup --gaps lists gaps", rc == 0 and has(o, "GraalVM", "Spring Boot 3"), o)
    rc, o = run([L, "--page", "999"])
    check("lookup --page out of range -> error", rc == 2, o)

    # ---- round 9 (fix): single-segment properties, default description, terms the PDF covers do not come out POINTER ONLY
    rc, o = run([L, "--prop", "debug"])
    check("lookup --prop debug -> Appendix A p.668 default false and body p.138-139", rc == 0 and has(o, "p.668", "false", "138"), o)
    rc, o = run([L, "--prop", "trace"])
    check("lookup --prop trace -> Appendix A p.676 default false and body p.139", rc == 0 and has(o, "p.676", "false", "139"), o)
    rc, o = run([L, "--prop", "spring.kafka.streams.application-id"])
    check("lookup --prop application-id -> default IN THE DESCRIPTION (spring.application.name), p.730", rc == 0 and has(o, "IN THE DESCRIPTION", "spring.application.name", "p.730") and "NO published default" not in o, o)
    for t, pg in (("AutoConfigureMetrics", "168"), ("DirtiesContext", "167"), ("web-allow-others", "696"), ("opaque", "310"),
                  ("slice annotation", "219"), ("custom slice", "219"), ("unique name", "342"), ("JwtDecoder", "310"),
                  ("OpaqueTokenIntrospector", "311"), ("EnableKafkaStreams", "391"), ("datadoghq.eu", "483"), ("fully executable jar", "534")):
        rc, o = run([L] + t.split(" "))
        check("lookup %r -> COVERED (not POINTER ONLY), p.%s" % (t, pg), rc == 0 and has(o, "LEVEL: COVERED", pg), o)

    # ---- round 10 (fix): synonyms must not give a false NOT COVERED for what the PDF carries
    # (the Portuguese queries are kept on purpose: the lookup must keep recognizing Portuguese input)
    for t, pg in (("env-prefix", "103"), ("environment prefix", "103"), ("prefixo de variáveis de ambiente", "103"),
                  ("Port 8080 was already in use", "73"), ("import twice", "95"), ("random.int", "103"),
                  ("SanitizingFunction", "640"), ("PropertiesLauncher", "843")):
        rc, o = run([L] + t.split(" "))
        check("lookup %r -> COVERED, p.%s (round 10)" % (t, pg), rc == 0 and has(o, "LEVEL: COVERED", pg) and "NOT COVERED" not in o.splitlines()[0], o)

    # ---- three-level lookup (round 2): COVERED (rc 0) / POINTER ONLY (rc 3) / NOT COVERED (rc 2)
    rc, o = run([L, "circuit", "breaker"])
    check("lookup 'circuit breaker' -> POINTER ONLY p.464, without Resilience4j (D6)", rc == 3 and has(o, "LEVEL: POINTER ONLY", "p.464", "Resilience4j"), o)
    rc, o = run([L, "resilience4j"])
    check("lookup resilience4j -> NOT COVERED (curated list)", rc == 2 and has(o, "LEVEL: NOT COVERED", "java-backend-frameworks-expert"), o)
    rc, o = run([L, "kraft"])
    check("lookup kraft -> NOT COVERED", rc == 2 and "LEVEL: NOT COVERED" in o, o)
    rc, o = run([L, "grafana"])
    check("lookup grafana -> NOT COVERED (0 occurrences)", rc == 2 and has(o, "LEVEL: NOT COVERED", "0 occurrences"), o)
    rc, o = run([L, "bootBuildImage"])
    check("lookup bootBuildImage -> NOT COVERED (0 occurrences in the term index)", rc == 2 and has(o, "LEVEL: NOT COVERED", "0 occurrences in the term index"), o)
    rc, o = run([L, "xyzzyfoo"])
    check("lookup nonexistent term outside the curated list -> NOT COVERED by the term index", rc == 2 and has(o, "LEVEL: NOT COVERED", "term index"), o)
    rc, o = run([L, "spring", "boot", "3"])
    check("lookup 'spring boot 3' -> NOT COVERED and redirects to java-backend-frameworks-expert", rc == 2 and has(o, "LEVEL: NOT COVERED", "redirect", "java-backend-frameworks-expert"), o)
    rc, o = run([L, "@DataJpaTest"])
    check("lookup @DataJpaTest -> COVERED (D1), p.190-193 and references/04", rc == 0 and has(o, "LEVEL: COVERED", "p.190", "references/04"), o)
    rc, o = run([L, "Propagation.NOT_SUPPORTED"])
    check("lookup Propagation.NOT_SUPPORTED -> COVERED p.191", rc == 0 and has(o, "LEVEL: COVERED", "p.191"), o)
    rc, o = run([L, "TestEntityManager"])
    check("lookup TestEntityManager -> COVERED p.191", rc == 0 and has(o, "LEVEL: COVERED", "p.191"), o)
    rc, o = run([L, "scrape_config"])
    check("lookup scrape_config -> COVERED p.494 (D3)", rc == 0 and has(o, "LEVEL: COVERED", "p.494", "references/11"), o)
    rc, o = run([L, "tomcat-jdbc"])
    check("lookup tomcat-jdbc -> COVERED p.326 (D4)", rc == 0 and has(o, "LEVEL: COVERED", "p.326", "references/07"), o)
    rc, o = run([L, "dead", "letter"])
    check("lookup 'dead letter' -> POINTER ONLY p.388 (DLX only 'if the broker is configured')", rc == 3 and has(o, "LEVEL: POINTER ONLY", "p.388"), o)
    rc, o = run([L, "zookeeper"])
    check("lookup zookeeper -> POINTER ONLY p.96,686,875", rc == 3 and has(o, "LEVEL: POINTER ONLY", "96", "686", "875"), o)
    rc, o = run([L, "retries"])
    check("lookup retries -> COVERED (retry/retries variant) p.388", rc == 0 and has(o, "LEVEL: COVERED", "388", "references/08"), o)
    rc, o = run([L, "--prop", "spring.rabbitmq.listener.simple.retry.max-attempts"])
    check("lookup --prop listener.simple.retry.max-attempts -> Appendix A p.734, default 3 (D2)", rc == 0 and has(o, "p.734", "3"), o)
    rc, o = run([L, "--prop", "spring.rabbitmq.listener.simple.retry.enabled"])
    check("lookup --prop listener.simple.retry.enabled -> p.734, default false", rc == 0 and has(o, "p.734", "false"), o)
    rc, o = run([L, "--gaps"])
    check("lookup --gaps shows the curated out-of-scope and pointer-only lists", rc == 0 and has(o, "Curated out-of-scope list", "Pointer only", "circuit breaker"), o)
    rc, o = run([L, "hikari", "--json"])
    check("lookup --json carries 'nivel'", rc == 0 and '"nivel": "COVERED"' in o, o)

    # ---- content fixed in round 2 (scripts)
    rc, o = run([A, "show", "prometheus"])
    check("actuator show prometheus -> scrape_configs, exposure and Pushgateway (p.494)", rc == 0 and has(o, "job_name", "metrics_path", "NOT available", "Pushgateway", "p.494"), o)
    rc, o = run([K, "list"])
    check("checklist M08 -> excludeDevtools=false/developmentOnly (p.59, 68)", has(o, "M08", "excludeDevtools=false", "developmentOnly", "p.59, 68"), o)

    # ---- term index
    T = json.load(open(os.path.join(PKG, "scripts", "sbr_terms.json"), encoding="utf-8"))
    check("terms: 882 pages and bigram 'circuit breaker' = p.464", T["paginas"] == 882 and T["bigramas"].get("circuit breaker") == "464", str(T["bigramas"].get("circuit breaker")))
    check("terms: no occurrence of graalvm, kraft, resilience4j, grafana, openapi", not any(w in T["unigramas"] for w in ("graalvm", "kraft", "resilience4j", "grafana", "openapi")), "")
    check("terms: >=10000 words and >=40000 pairs indexed", len(T["unigramas"]) >= 10000 and len(T["bigramas"]) >= 40000, "%d %d" % (len(T["unigramas"]), len(T["bigramas"])))
    cur = json.load(open(os.path.join(PKG, "scripts", "sbr_curated.json"), encoding="utf-8"))
    check("curated: >=10 out-of-scope subjects and >=5 pointer-only", len(cur["fora"]) >= 10 and len(cur["so_ponteiro"]) >= 5, "")
    if a.src:
        import tempfile
        tmp = os.path.join(tempfile.mkdtemp(), "terms.json")
        rc, o = run([os.path.join("scripts", "build_term_index.py"), "--src", a.src, "--out", tmp])
        same = rc == 0 and open(tmp, "rb").read() == open(os.path.join(PKG, "scripts", "sbr_terms.json"), "rb").read()
        check("build_term_index.py reproduces sbr_terms.json byte for byte from the text", same, o)

    # ---- propcheck
    rc, o = run([P, os.path.join(FX, "app-exemplo.properties")])
    check("propcheck: unknown key is not an error (rc 0) and is flagged", rc == 0 and has(o, "UNKNOWN", "acme.custom.flag", "unknown is NOT an error"), o)
    check("propcheck: spring.config.location in a file -> P02 ALERT p.91", has(o, "P02", "p.91"), o)
    check("propcheck: nonexistent endpoint id -> P14", has(o, "P14", "helth"), o)
    check("propcheck: ':-' in logging -> P16 p.145", has(o, "P16", "p.145"), o)
    check("propcheck: camelCase placeholder -> P08 p.99", has(o, "P08", "p.99"), o)
    check("propcheck: spring.jpa.properties without relaxed binding -> P17 p.618", has(o, "P17", "p.618"), o)
    rc, o = run([P, os.path.join(FX, "application-prod.yml")])
    check("propcheck: profile YAML with active -> ERROR P01 (rc 1)", rc == 1 and has(o, "P01", "p.135-136"), o)
    check("propcheck: unquoted '*' in YAML -> ERROR P05 p.445", has(o, "P05", "p.445"), o)
    rc, o = run([P, os.path.join(FX, "app-ok.yml")])
    check("propcheck: correct yml -> no error", rc == 0 and "rule findings: none" in o, o)
    rc, o = run([P, os.path.join(FX, "multi-doc.properties")])
    check("propcheck: #--- separator with a space -> P13", has(o, "P13", "p.100"), o)
    rc, o = run([P, os.path.join(FX, "lista.yml")])
    check("propcheck: YAML lists flattened as key[0] and known profile includes", rc == 0 and has(o, "my.servers[0] = a.example.com", "my.list[1] = y", "spring.profiles.include[0]"), o)
    rc, o = run([P, os.path.join(FX, "tab.yml")])
    check("propcheck: YAML with tab -> ERROR P04 (rc 1)", rc == 1 and "P04" in o, o)
    rc, o = run([P, "--rules"])
    check("propcheck --rules lists rules with source", rc == 0 and has(o, "P01", "SBR p.135-136"), o)
    rc, o = run([P, os.path.join(FX, "app-exemplo.properties"), "--json"])
    try:
        js = json.loads(o)
        ok = isinstance(js, list) and js[0]["chaves"] and "achados" in js[0]
    except Exception:
        ok = False
    check("propcheck --json valid", ok, o)

    rc, o = run([P, os.path.join(FX, "renomeado.properties")])
    check("propcheck: P01 depends on the file name -> NOTE and rc 0 without --as-profile", rc == 0 and has(o, "NOTE", "--as-profile", "file NAME"), o)
    rc, o = run([P, os.path.join(FX, "renomeado.properties"), "--as-profile", "prod"])
    check("propcheck: --as-profile prod -> ERROR P01 (rc 1)", rc == 1 and has(o, "P01", "(profile prod)"), o)
    rc, o = run([R, "winner", "cmdline", "jar-config-data", "env"])
    check("precedence: aliases cmdline and jar-config-data accepted (p.87-88)", rc == 0 and has(o, "Wins: Command-line arguments"), o)
    rc, o = run([R, "winner", "jar-config-data", "external-profile-config-data"])
    check("precedence: config data types as named sources (p.88)", rc == 0 and "OUTSIDE the jar" in o, o)
    rc, o = run([L, "preStop"])
    check("lookup preStop -> p.527-528", rc == 0 and has(o, "preStop", "528"), o)
    rc, o = run([L, "terminationGracePeriodSeconds"])
    check("lookup terminationGracePeriodSeconds -> p.528", rc == 0 and "528" in o, o)
    rc, o = run([L, "httpGet"])
    check("lookup httpGet -> p.463 (probes manifest)", rc == 0 and "463" in o, o)
    rc, o = run([L, "configtree"])
    check("lookup configtree -> p.97-98", rc == 0 and has(o, "97", "98"), o)
    rc, o = run([K, "list"])
    check("checklist list: M12 p.96-98, M13 p.580-582 (post-blind-test fixes)", has(o, "p.96-98, 101", "p.580-582"), o)
    rc, o = run([K, "check", os.path.join(FX, "config-prod-ruim.properties")])
    check("checklist: C51 labels masking as [from source] p.639 and configtree p.97-98", has(o, "SBR p.639", "SBR p.97-98", "[from source]"), o)

    # ---- checklist
    rc, o = run([K, "check", os.path.join(FX, "app-exemplo.properties")])
    check("checklist: include=* -> C01 ALERT p.444-445", has(o, "ALERT", "C01", "p.444-445"), o)
    check("checklist: shutdown enabled -> C02", has(o, "C02", "shutdown"), o)
    check("checklist: ddl-auto=update -> C40", has(o, "C40", "ddl-auto=update"), o)
    rc, o = run([K, "check", os.path.join(FX, "config-prod-ruim.properties")])
    check("checklist: devtools/H2/debug/secret/always detected",
          has(o, "C30", "C31", "C22", "C51", "C33", "C43", "C64", "C65"), o)
    check("checklist: Flyway + sql.init.mode=always mix -> C42", "C42" in o and "ALERT     C42" in o, o)
    rc, o = run([K, "list", "--area", "ACTUATOR"])
    check("checklist list --area ACTUATOR", rc == 0 and has(o, "C01", "M01"), o)

    # ---- actuator
    rc, o = run([A, "list"])
    check("actuator list: 25 endpoints, shutdown disabled, only health on the web", rc == 0 and has(o, "heapdump", "prometheus", "shutdown", "except shutdown"), o)
    rc, o = run([A, "show", "shutdown"])
    check("actuator show shutdown: disabled by default", rc == 0 and "enabled by default: no" in o, o)
    rc, o = run([A, "show", "foo"])
    check("actuator show foo -> NOT COVERED (rc 2)", rc == 2 and "NOT COVERED" in o, o)
    rc, o = run([A, "exposure"])
    wl = [l for l in o.splitlines() if l.startswith("Web:")]
    check("actuator exposure default: web = health only", rc == 0 and wl and wl[0].strip() == "Web: health", o)
    rc, o = run([A, "exposure", "--web-include", "*", "--web-exclude", "env,beans"])
    wl = [l for l in o.splitlines() if l.startswith("Web:")][0]
    check("actuator exposure '*' minus env,beans: exclude beats include; shutdown out (disabled)",
          "env" not in wl.split(", ") and "beans" not in wl.split(", ") and "shutdown" not in wl and "health" in wl, o)
    rc, o = run([A, "exposure", "--web-include", "shutdown,health", "--enable", "shutdown"])
    wl = [l for l in o.splitlines() if l.startswith("Web:")][0]
    check("actuator exposure: shutdown enabled + exposed -> available", "shutdown" in wl, o)
    rc, o = run([A, "paths", "--base-path", "/manage", "--path-mapping", "health=healthcheck", "--probes"])
    check("actuator paths: base-path and path-mapping", has(o, "/manage/healthcheck", "/manage/info", "liveness"), o)
    rc, o = run([A, "health-status", "--status", "UP,DOWN"])
    check("actuator health-status: DOWN -> 503 (default p.457-458)", has(o, "DOWN", "503"), o)
    rc, o = run([A, "health-status", "--http-mapping", "fatal=503", "--order", "fatal,down,out-of-service,unknown,up", "--status", "OUT_OF_SERVICE"])
    check("actuator health-status: custom mapping disables defaults (OUT_OF_SERVICE -> 200)", has(o, "OUT_OF_SERVICE", "HTTP 200", "DISABLES"), o)

    # ---- precedence
    rc, o = run([R, "winner", "cli", "env", "jar"])
    check("precedence: command line beats env and jar (p.87-88)", has(o, "Wins: Command-line arguments", "position 11"), o)
    rc, o = run([R, "winner", "dynamicpropertysource", "testpropertysource"])
    check("precedence: @TestPropertySource (14) beats @DynamicPropertySource (13)", has(o, "TestPropertySource", "position 14"), o)
    rc, o = run([R, "winner", "external", "jar"])
    check("precedence: external file beats the one in the jar", "OUTSIDE the jar" in o.splitlines()[0] or "outside" in o.lower(), o)
    rc, o = run([R, "winner", "foo"])
    check("precedence: unknown source -> rc 2", rc == 2, o)
    rc, o = run([R, "env-name", "spring.main.log-startup-info"])
    check("precedence env-name: SPRING_MAIN_LOGSTARTUPINFO (p.117)", "SPRING_MAIN_LOGSTARTUPINFO" in o, o)
    rc, o = run([R, "env-name", "my.service[0].other"])
    check("precedence env-name: MY_SERVICE_0_OTHER (p.117)", "MY_SERVICE_0_OTHER" in o, o)
    rc, o = run([R, "duration", "10s"])
    check("precedence duration 10s", "Duration" in o, o)
    rc, o = run([R, "order"])
    check("precedence order: 15 sources", has(o, " 1. Default", "15. Devtools"), o)

    # ---- round 4 (fixes after the round 3 blind test): lookup, --page, --prop with description, coherent levels
    rc, o = run([L, "--page", "517"])
    check("R4 D1: --page 517 -> 13.6.6 starts on this page, 13.7 too; top is a continuation (not only '13.7 Auditing')",
          rc == 0 and has(o, "13.6.6 Metrics Endpoint", "13.7 Auditing", "START on this page", "TOP"), o)
    rc, o = run([L, "--page", "518"])
    check("R4: --page 518 -> top is 13.7.1 (continuation); 13.8 and 13.9 start here", rc == 0 and has(o, "13.7.1 Custom Auditing", "13.8 HTTP Tracing", "13.9 Process Monitoring"), o)
    rc, o = run([L, "--page", "769"])
    check("R4: --page 769 -> A.14 starts on this page (A.13 at the top)", rc == 0 and has(o, "A.14", "START"), o)
    rc, o = run([L, "jvm.memory.max"])
    check("R4 D1: lookup jvm.memory.max -> COVERED p.517 and references/11", rc == 0 and has(o, "LEVEL: COVERED", "p.517", "references/11"), o)
    rc, o = run([L, "Metaspace"])
    check("R4 D1: lookup Metaspace -> COVERED", rc == 0 and "LEVEL: COVERED" in o, o)
    rc, o = run([L, "tag=id:Metaspace"])
    check("R4 D1: lookup tag=id:Metaspace -> COVERED (non-alphanumeric separators)", rc == 0 and "LEVEL: COVERED" in o, o)
    rc, o = run([A, "show", "metrics"])
    check("R4 D1: actuator show metrics -> sum, nonheap and Metaspace (p.517)", rc == 0 and has(o, "SUM", "Code Cache", "Compressed Class Space", "Metaspace", "id:Metaspace", "p.517"), o)
    for term, pg in (("PKCS#1", "574"), ("openssl", "574"), ("libtcnative", "574"), ("http2-server", "575"), ("jetty-alpn-java-server", "575"), ("h2c", "574")):
        rc, o = run([L, term])
        check("R4 D2: lookup %s -> COVERED (no longer POINTER ONLY)" % term, rc == 0 and "LEVEL: COVERED" in o, o)
    rc, o = run([L, "--prop", "management.metrics.export.statsd.step"])
    check("R4 D3: --prop statsd.step -> description about aligning the step with the scrape, p.793 and body p.496-497",
          rc == 0 and has(o, "Description (package paraphrase", "scrape", "p.793", "496-497", "default in Appendix A (SBR p.793): 1m"), o)
    rc, o = run([L, "--prop", "management.metrics.export.stackdriver.batch-size"])
    check("R4 D3: --prop stackdriver.batch-size -> measurements per request, default 10000", rc == 0 and has(o, "measurements per request", "10000", "p.792"), o)
    rc, o = run([L, "--prop", "management.metrics.export.statsd.polling-frequency"])
    check("R4 D3: --prop statsd.polling-frequency -> gauge, 10s", rc == 0 and has(o, "gauge", "10s"), o)
    rc, o = run([L, "--prop", "spring.kafka.consumer.group-id"])
    check("R4 D3/R12: --prop without a curated description -> declares POINTER ONLY and says to read Appendix A",
          rc == 0 and has(o, "POINTER ONLY for this key", "Appendix A, SBR p."), o)
    # round 12 (P1): description returned for the Redis pool and use-code-as-default-message; COVERED in the terms
    rc, o = run([L, "--prop", "spring.redis.lettuce.pool.min-idle"])
    check("R12 P1: --prop lettuce.pool.min-idle -> description (only with positive eviction), default 0, p.704",
          rc == 0 and has(o, "Description (package paraphrase", "time-between-eviction-runs", "positive", "p.704", "default in Appendix A (SBR p.704): 0"), o)
    rc, o = run([L, "--prop", "spring.redis.jedis.pool.enabled"])
    check("R12 P1: --prop jedis.pool.enabled -> commons-pool2 and sentinel, p.702", rc == 0 and has(o, "commons-pool2", "sentinel", "p.702"), o)
    rc, o = run([L, "--prop", "spring.redis.lettuce.pool.max-wait"])
    check("R12 P1: --prop lettuce.pool.max-wait -> negative blocks indefinitely, -1ms", rc == 0 and has(o, "indefinitely", "-1ms"), o)
    rc, o = run([L, "--prop", "spring.messages.use-code-as-default-message"])
    check("R12 P1: --prop use-code-as-default-message -> NoSuchMessageException, p.674", rc == 0 and has(o, "NoSuchMessageException", "p.674", "false"), o)
    for term in ("NoSuchMessageException", "redis pool", "jedis sentinel", "min-idle", "default package", "grab hints", "ReactiveNeo4jTransactionManager"):
        rc, o = run([L, term])
        check("R12 P1/P2: lookup %s -> COVERED" % term, rc == 0 and "LEVEL: COVERED" in o, o)
    # NOTE: the assertions below on references/*.md check the text of the summaries, which are translated in another phase;
    # the quoted fragments must be updated together with the translation of references/.
    t07 = open(os.path.join(PKG, "references", "07-dados-sql-e-nosql.md"), encoding="utf-8").read()
    t12 = open(os.path.join(PKG, "references", "12-cli-e-build-plugins.md"), encoding="utf-8").read()
    t00 = open(os.path.join(PKG, "references", "00-visao-geral-e-versao.md"), encoding="utf-8").read()
    check("R12 P2: ref 07 carries the Redis pool rule (min-idle and eviction) and reactive Neo4j without ReactiveTransactionManager", has(t07, "time-between-eviction-runs", "p.703-704", "is not auto-configured", "ReactiveDatabaseSelectionProvider"), "")
    check("R12 P2: ref 12 carries Windows quoting and the p.543 hints", has(t12, 'set "JAVA_OPTS=', "@EnableCaching", "CompilerAutoConfiguration", "p.543"), "")
    check("R12 P2: ref 00 carries default package (all classes of all jars) and the starter-web default Tomcat (p.48)", has(t00, "all classes from all jars", "the default of `spring-boot-starter-web`", "reactor-netty"), "")
    rc, o = run([L, "--prop", "spring.data.cassandra.contact-points"])
    check("R4: --prop contact-points -> default [127.0.0.1:9042] attributed to Appendix A p.682, body p.362 only an example",
          rc == 0 and has(o, "(SBR p.682): [127.0.0.1:9042]", "Body text: SBR p.362", "do not cite the body page for the default"), o)
    rc, o = run([L, "--prop", "server.tomcat.redirect-context-root"])
    check("R4 D4: --prop redirect-context-root -> default true, set false behind a proxy (p.763, body p.581)", rc == 0 and has(o, "true", "false", "p.763", "581"), o)
    rc, o = run([L, "--prop", "server.tomcat.remoteip.remote-ip-header"])
    check("R4 D4: --prop remote-ip-header -> either of the two properties turns on the RemoteIpValve (p.643)", rc == 0 and has(o, "RemoteIpValve", "643"), o)
    rc, o = run([L, "embedded", "ldap"])
    check("R4 D5: lookup 'embedded ldap' -> COVERED (aligned with references/07)", rc == 0 and has(o, "LEVEL: COVERED", "references/07"), o)
    for term in ("git.commit.time", "git-commit-id", "build-info", "buildInfo"):
        rc, o = run([L, term])
        check("R4 D6: lookup %s -> COVERED" % term, rc == 0 and "LEVEL: COVERED" in o, o)
    rc, o = run([L, "--prop", "spring.devtools.restart.trigger-file"])
    check("R4: --prop trigger-file -> Appendix A p.799 (key that was missing) and body p.64", rc == 0 and has(o, "A.15", "p.799", "64"), o)
    rc, o = run([L, "--prop", "spring.rsocket.server.transport"])
    check("R4: Appendix A section recomputed (rsocket is A.13, not A.14)", rc == 0 and "A.13" in o, o)
    rc, o = run([L, "--prop", "spring.thymeleaf.suffix"])
    check("R4: Appendix A section recomputed (thymeleaf is A.10, not A.11)", rc == 0 and "A.10" in o, o)
    rc, o = run([L, "--prop", "spring.mail.host"])
    check("R4: Appendix A section recomputed (mail is A.3, not A.4)", rc == 0 and "A.3" in o, o)
    rc, o = run([L, "@Commit"])
    check("R4: curated 'fora' matches by whole token ('@Commit' is still POINTER ONLY)", rc == 3 and "LEVEL: POINTER ONLY" in o, o)
    rc, o = run([L, "git.commit.time"])
    check("R4: curated does not match by part of a word ('git.commit.time' is not '@Commit')", "Rollback" not in o, o)
    rc, o = run([L, "virtual", "threads"])
    check("R4: curated 'virtual threads' remains NOT COVERED", rc == 2 and "LEVEL: NOT COVERED" in o, o)

    # ---- round 5: COVERED only by the content of the summaries (sbr_cover.json), whole term/phrase, never substring
    rc, o = run([os.path.join(S, "build_cover_index.py"), "--check"])
    check("R5: sbr_cover.json reproducible from references/ (build_cover_index.py --check)", rc == 0 and "up to date" in o, o)
    cov = json.load(open(os.path.join(PKG, "scripts", "sbr_cover.json"), encoding="utf-8"))
    check("R5: summary index only has references/ lines (no INDEX.md) and >=500 lines", len(cov["linhas"]) >= 500 and not [x for x in cov["linhas"] if x[0].upper().startswith("INDEX")], str(len(cov["linhas"])))
    rc, o = run([L, "record"])
    check("R5 +: record -> truly COVERED (02: record without @ConstructorBinding unless several constructors, p.109-110)", rc == 0 and has(o, "LEVEL: COVERED", "references/02", "109-110"), o)
    rc, o = run([L, "ConstructorBinding"])
    check("R5 +: ConstructorBinding -> COVERED with a summary in references/02 (p.107-110)", rc == 0 and has(o, "LEVEL: COVERED", "references/02", "107"), o)
    rc, o = run([L, "constructor", "binding"])
    check("R5 +: phrase 'constructor binding' -> COVERED", rc == 0 and "LEVEL: COVERED" in o, o)
    rc, o = run([L, "@DefaultValue"])
    check("R5 +: @DefaultValue -> COVERED (p.108-110)", rc == 0 and has(o, "LEVEL: COVERED", "references/02"), o)
    for term in ("lwc-step", "lwc-enabled", "meter-time-to-live", "lwc-ignore-publish-step", "config-time-to-live"):
        rc, o = run([L, term])
        check("R5 +: lookup %s -> COVERED p.780-781 (references/11)" % term, rc == 0 and has(o, "LEVEL: COVERED", "references/11", "p.78"), o)
    rc, o = run([L, "jboss"])
    check("R5 +: jboss -> COVERED only because references/05 summarizes the p.258 note (webjars-locator-jboss-vfs)", rc == 0 and has(o, "LEVEL: COVERED", "references/05", "258"), o)
    rc, o = run([L, "webjars-locator-jboss-vfs"])
    check("R5 +: webjars-locator-jboss-vfs -> COVERED", rc == 0 and "LEVEL: COVERED" in o, o)
    rc, o = run([L, "git-commit-id"])
    check("R5 +: compound identifier git-commit-id finds git-commit-id-plugin by whole parts", rc == 0 and "LEVEL: COVERED" in o, o)
    rc, o = run([L, "HPA"])
    check("R5 -: HPA -> NOT COVERED (0 occurrences; does not match PathPatternParser or http2-hpack by substring)", rc == 2 and has(o, "LEVEL: NOT COVERED") and "PathPatternParser" not in o and "hpack" not in o, o)
    rc, o = run([L, "helm"])
    check("R5 -: helm -> NOT COVERED", rc == 2 and "LEVEL: NOT COVERED" in o, o)
    rc, o = run([L, "autoscal"])
    check("R5 -: stem 'autoscal' -> POINTER ONLY p.464-465 (never NOT COVERED nor COVERED)", rc == 3 and has(o, "LEVEL: POINTER ONLY", "464", "465"), o)
    rc, o = run([L, "recor"])
    check("R5 -: 'recor' (part of 'record') is not COVERED", rc != 0 and "LEVEL: COVERED" not in o, o)
    rc, o = run([L, "@Commit"])
    check("R5 -: @Commit is not COVERED (curated: pointer only)", rc == 3 and "LEVEL: POINTER ONLY" in o, o)
    code = ("import sys; sys.path.insert(0, 'scripts'); import sbr_lookup as L; "
            "L._COVER = [('x.md:1', '9', 'the access log writes each record in loose prose'.split(), []), "
            "('y.md:2', '8', 'use record here'.split(), 'record'.split()), "
            "('z.md:3', '7', 'the annotation constructorbinding applies'.split(), []), "
            "('w.md:4', '6', 'key max-poll-records of kafka'.split(), 'max-poll-records'.split())]; "
            "h, s = L.cover_hits(['record']); print('PLAIN', [x[0] for x in h], [x[0] for x in s]); "
            "h, s = L.cover_hits(['ConstructorBinding']); print('STRONG', [x[0] for x in h]); "
            "h, s = L.cover_hits(['max-poll-records']); print('COMPOUND', [x[0] for x in h]); "
            "h, s = L.cover_hits(['poll']); print('PIECE', [x[0] for x in h]); "
            "h, s = L.cover_hits(['access', 'log']); print('PHRASE', [x[0] for x in h])")
    rc, o = run(["-c", code])
    check("R5 unit: a plain word only in prose does NOT cover (becomes a loose mention); delimited covers; identifier covers anywhere; part of a token does not cover; contiguous phrase covers",
          rc == 0 and has(o, "PLAIN ['y.md'] ['x.md']", "STRONG ['z.md']", "COMPOUND ['w.md']", "PIECE []", "PHRASE ['x.md']"), o)
    rc, o = run([L, "--prop", "server.undertow.max-headers"])
    check("R5 D4: --prop undertow.max-headers -> NO published default (empty cell, p.766)", rc == 0 and has(o, "NO published default", "766"), o)
    rc, o = run([L, "--prop", "server.undertow.threads.worker"])
    check("R5 D4: --prop undertow.threads.worker -> default IN THE DESCRIPTION (8x I/O threads, p.766)", rc == 0 and has(o, "IN THE DESCRIPTION", "8 times"), o)
    rc, o = run([L, "--prop", "spring.servlet.multipart.file-size-threshold"])
    check("R5 D4: --prop multipart.file-size-threshold -> 0B and description (p.742)", rc == 0 and has(o, "0B", "Description", "742"), o)
    rc, o = run([L, "--prop", "management.metrics.export.atlas.lwc-step"])
    check("R5 D1: --prop atlas.lwc-step -> 5s, p.781 and the step multiple rule (7s violates it)", rc == 0 and has(o, "5s", "p.781", "even", "violates"), o)
    rc, o = run([L, "--prop", "management.metrics.export.atlas.lwc-enabled"])
    check("R5 D1: --prop atlas.lwc-enabled -> false, p.780", rc == 0 and has(o, "false", "p.780"), o)
    rc, o = run([L, "--prop", "management.metrics.export.atlas.meter-time-to-live"])
    check("R5 D1: --prop atlas.meter-time-to-live -> 15m, p.781", rc == 0 and has(o, "15m", "p.781"), o)
    r02 = open(os.path.join(PKG, "references", "02-configuracao-externalizada.md"), encoding="utf-8").read()
    check("R5 D2: references/02 summarizes record without @ConstructorBinding (several constructors), null nested, empty @DefaultValue, no @Component (p.109-110)",
          has(r02, "`@ConstructorBinding` is **not needed**", "several constructors", "**empty** `@DefaultValue`", "`@Component`", "SBR p.109-110"), "")
    r11 = open(os.path.join(PKG, "references", "11-metricas-e-observabilidade.md"), encoding="utf-8").read()
    check("R5 D1: references/11 carries the lwc-step x step rule (even multiple; 7s violates), lwc-enabled false, TTL 15m (p.780-781)",
          has(r11, "(60 divided by the value is an integer)", "**7s violates**", "lwc-enabled", "default 15m", "SBR p.781", "SBR p.780"), "")

    # ---- round 5 (fix): faithful summaries + truly COVERED lookup
    def ref(n):
        return open(os.path.join(PKG, "references", n), encoding="utf-8").read()
    r04, r00, r14, r12 = ref("04-json-tarefas-testes-autoconfig.md"), ref("00-visao-geral-e-versao.md"), ref("14-apendices-propriedades-e-versoes.md"), ref("12-cli-e-build-plugins.md")
    rc, o = run([L, "ConditionalOnExpression"])
    check("R5fix: lookup ConditionalOnExpression -> COVERED with a summary in references/04 (p.236)", rc == 0 and has(o, "LEVEL: COVERED", "04-json-tarefas-testes-autoconfig.md", "236"), o)
    check("R5fix: references/04 carries ConditionalOnExpression with a bean (initialized too early, no post-processing) and interface x concrete (p.236)",
          has(r04, "initialized very early", "post-processing", "concrete class, not the interface", "type declared in the method signature", "SBR p.236"), "")
    rc, o = run([L, "TestRestTemplate"])
    check("R5fix: lookup TestRestTemplate -> COVERED with the redirect/cookies/timeouts summary (p.226-229)", rc == 0 and has(o, "LEVEL: COVERED", "226-229"), o)
    rc, o = run([L, "cookies"])
    check("R5fix: lookup cookies -> COVERED including the TestRestTemplate summary (p.226-229)", rc == 0 and has(o, "LEVEL: COVERED", "04-json-tarefas-testes-autoconfig.md"), o)
    check("R5fix: references/04 TestRestTemplate: Apache HttpClient 4.3.2 recommended (not mandatory), redirects not followed, cookies ignored, injection, default host, timeouts via RestTemplateBuilder (p.227-229)",
          has(r04, "4.3.2", "recommended, not mandatory", "redirects are not followed", "cookies are ignored", "`@Autowired`", "without host and port", "`RestTemplateBuilder`", "`setConnectTimeout`", "SBR p.228-229"), "")
    check("R5fix: references/04 does NOT say the book recommends WebTestClient (p.227 only describes) and cites spring-webflux (p.165)",
          "the book recommends it" not in r04 and "not a recommendation by the book" in r04 and has(r04, "spring-webflux", "SBR p.165"), "")
    check("R5fix: references/00 devtools: restart.exclude/include regex, ConfigurableObjectInputStream + context classloader, .spring-boot-devtools.properties fallback (p.65-67)",
          has(r00, "`restart.exclude.companycommonlibs`", "regex applied to the classpath", "keys must be unique", "`ConfigurableObjectInputStream`", "Thread.currentThread().getContextClassLoader()", "`.spring-boot-devtools.properties`", "root of `$HOME`", "SBR p.65", "SBR p.66", "SBR p.67"), "")
    rc, o = run([L, "ConfigurableObjectInputStream"])
    check("R5fix: lookup ConfigurableObjectInputStream -> COVERED (summary in references/00, p.66)", rc == 0 and has(o, "LEVEL: COVERED", "00-visao-geral"), o)
    rc, o = run([L, "dependency management"])
    check("R5fix: lookup 'dependency management' -> COVERED with summaries from references/00, 12 and 14 (p.42, p.876-881)", rc == 0 and has(o, "LEVEL: COVERED", "00-visao-geral", "12-cli", "14-apendices", "876"), o)
    check("R5fix: lookup 'dependency management' shows p.544-545 ONLY as CLI CONTEXT (outside 'Occurrences') and the title marked [CLI context]",
          has(o, "CONTEXT", "p.544-545", "CLI", "[CLI context]") and "SBR p.3,7,15,28,33,42,153,245,247,405,477,544" not in o and not any(ln.startswith("Occurrences") and "544" in ln for ln in o.splitlines()), o)
    check("R5fix: references/14 carries the override mechanism (p.42, F.2 p.876-881, hibernate.version p.878, kotlin.version p.247) and p.544 as CLI context",
          has(r14, "Mechanism for overriding a managed version", "SBR p.42", "`hibernate.version`", "SBR p.876-881", "`kotlin.version`", "SBR p.247", "Context, do not confuse", "SBR p.544-545"), "")
    check("R5fix: references/12 labels p.544-545 as CLI context (it is not Maven/Gradle)", has(r12, "CLI context", "SBR p.544-545", "**not** the version override in Maven/Gradle projects"), "")


    # ---- round 6 (D1-D4)
    r02_6, r04_6, r11_6 = ref("02-configuracao-externalizada.md"), ref("04-json-tarefas-testes-autoconfig.md"), ref("11-metricas-e-observabilidade.md")
    check("R6 D1: references/02 carries the SpEL rule in a properties file (not evaluated on read; evaluated when consumed via @Value; p.133)",
          has(r02_6, "SpEL in a properties file", "SBR p.133", "does NOT evaluate", "`@Value`", "is it evaluated"), "")
    check("R6 D1 (neg): references/02 does not say Boot evaluates SpEL when reading the file",
          "evaluates SpEL expressions when reading" not in r02_6.replace("does NOT evaluate", ""), "")
    rc, o = run([L, "SpEL"])
    check("R6 D1: lookup SpEL -> COVERED with the references/02 summary (p.133)", rc == 0 and has(o, "LEVEL: COVERED", "02-configuracao", "133"), o)
    rc, o = run([L, "--prop", "spring.rabbitmq.port"])
    check("R6 D2: --prop spring.rabbitmq.port -> default IN THE DESCRIPTION '5672, or 5671 if SSL is enabled' (p.735)", rc == 0 and has(o, "IN THE DESCRIPTION", "5672, or 5671 if SSL is enabled", "p.735"), o)
    check("R6 D2 (neg): --prop spring.rabbitmq.port does not fall into the 'default column empty or not extracted' warning", "or not extracted" not in o, o)
    rc, o = run([L, "--prop", "spring.jta.atomikos.properties.log-base-dir"])
    check("R6 D2: --prop atomikos log-base-dir -> default IN THE DESCRIPTION 'the current working directory' (p.707)", rc == 0 and has(o, "IN THE DESCRIPTION", "the current working directory", "p.707"), o)
    rc, o = run([L, "--prop", "spring.jta.atomikos.properties.transaction-manager-unique-name"])
    check("R6 D2: --prop transaction-manager-unique-name -> default IN THE DESCRIPTION (machine IP; p.708)", rc == 0 and has(o, "IN THE DESCRIPTION", "IP address", "p.708"), o)
    rc, o = run([L, "--prop", "spring.task.scheduling.thread-name-prefix"])
    check("R6 D2: --prop scheduling.thread-name-prefix -> 'scheduling-' (p.676)", rc == 0 and has(o, "scheduling-", "p.676"), o)
    check("R6 D2 (neg): --prop scheduling.thread-name-prefix does NOT mix with 'false' (scheduling-false)", "scheduling-false" not in o, o)
    rc, o = run([L, "--prop", "spring.activemq.pool.block-if-full-timeout"])
    check("R6 D2: --prop activemq.pool.block-if-full-timeout -> description (blocking time before the exception) and -1ms (p.716)", rc == 0 and has(o, "Description (package paraphrase", "-1ms", "blocking"), o)
    rc, o = run([L, "--prop", "spring.artemis.pool.block-if-full"])
    check("R6 D2: --prop artemis.pool.block-if-full -> description with JMSException (p.717)", rc == 0 and has(o, "JMSException", "717"), o)
    rc, o = run([L, "--prop", "spring.task.scheduling.pool.max-size"])
    check("R6 D2 (neg): --prop scheduling.pool.max-size -> UNKNOWN (the scheduler only has pool.size)", rc == 2 and has(o, "UNKNOWN", "pool.size"), o)
    import importlib.util
    spec = importlib.util.spec_from_file_location("bi6", os.path.join(PKG, "scripts", "build_index.py"))
    bi6 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bi6)
    check("R6 D2: extractor default_in_description('...Default to 5672, or 5671 if SSL is enabled.') -> '5672, or 5671 if SSL is enabled'",
          bi6.default_in_description("RabbitMQ port. Ignored if an address is set. Default to 5672, or 5671 if SSL is enabled.") == "5672, or 5671 if SSL is enabled", "")
    check("R6 D2: extractor 'Defaults to the current working directory.' -> 'the current working directory'",
          bi6.default_in_description("Directory in which the log files should be stored. Defaults to the current working directory.") == "the current working directory", "")
    check("R6 D2 (neg): extractor does not pick up 'Default batch size' nor 'default-topic' (no verb)",
          bi6.default_in_description("Default batch size in bytes.") is None and bi6.default_in_description("Name of the default-topic to use.") is None, "")
    idx6 = json.load(open(os.path.join(PKG, "scripts", "sbr_index.json"), encoding="utf-8"))
    check("R6 D2: index: default_desc on >=20 keys and scheduling prefix = 'scheduling-'",
          sum(1 for v in idx6["props"].values() if v.get("default_desc")) >= 20 and idx6["props"]["spring.task.scheduling.thread-name-prefix"]["default"] == "scheduling-", "")
    check("R6 D2 (neg): index: no default ends in '-false' and mockmvc.print = 'default'",
          not [k for k, v in idx6["props"].items() if (v.get("default") or "").endswith("-false")] and idx6["props"]["spring.test.mockmvc.print"]["default"] == "default", "")
    check("R6 D3: references/04 carries the book's TWO ways out for a custom Executor (ThreadPoolTaskExecutor; ThreadPoolTaskExecutor + AsyncConfigurer; p.153)",
          has(r04_6, "Custom `Executor`", "TWO ways out", "change your `Executor` into a `ThreadPoolTaskExecutor`", "`AsyncConfigurer`", "`applicationTaskExecutor`", "SBR p.153"), "")
    check("R6 D3 (neg): references/04 warns that the book does NOT carry the 'any AsyncTaskExecutor bean' recipe",
          has(r04_6, "declare any `AsyncTaskExecutor` bean", "gives NO other recipe", "do not present that as from the book"), "")
    check("R6 D3: references/04 says the scheduler has pool.size and NO max-size (p.676)", has(r04_6, "`spring.task.scheduling.pool.size`", "does NOT have `max-size`", "SBR p.676"), "")
    rc, o = run([L, "AsyncConfigurer"])
    check("R6 D3: lookup AsyncConfigurer -> COVERED with the references/04 summary (p.153)", rc == 0 and has(o, "LEVEL: COVERED", "04-json-tarefas", "153"), o)
    check("R6 D4: references/11 carries MeterFilter.renameTag (com.example, mytag.region -> mytag.area; p.514-515)",
          has(r11_6, "MeterFilter.renameTag(\"com.example\", \"mytag.region\", \"mytag.area\")", "SBR p.514-515", "`com.example`"), "")
    check("R6 D4: references/11 carries the global registry note (static Metrics methods; not managed by Spring; p.479, p.515)",
          has(r11_6, "`Metrics`", "not managed by Spring", "SBR p.479 and p.515", "use-global-registry=false"), "")
    rc, o = run([L, "renameTag"])
    check("R6 D4: lookup renameTag -> COVERED (references/11, p.514-515)", rc == 0 and has(o, "LEVEL: COVERED", "11-metricas", "514"), o)
    rc, o = run([L, "global registry"])
    check("R6 D4: lookup 'global registry' -> COVERED (references/11)", rc == 0 and has(o, "LEVEL: COVERED", "11-metricas", "515"), o)
    check("R6 D5: references/11 does not categorically claim that ConcurrentMap is left without metrics; says the book does not mention it (p.502-503) and says to label [inference]",
          has(r11_6, "ConcurrentMap (the simple cache", "does NOT claim", "[inference]", "SBR p.502-503") and "will have no metrics" not in r11_6, "")
    check("R6 D4 (neg): references/11 records that the book does not detail filters on the global registry", "The book does not go into more detail than that" in r11_6, "")

    # ---- round 7 (fixes)
    r10_7 = open(os.path.join(PKG, "references", "10-actuator-endpoints-saude-info.md"), encoding="utf-8").read()
    check("R7 D1: ref 10 does not attribute disabling the discovery page to base-path as [from source]; labels it [inference] and cites the management context path (p.449)",
          "management context path" in r10_7 and "[inference]** treating management.endpoints.web.base-path=/" in r10_7 and "with `base-path=/` it is disabled" not in r10_7, "")
    rc, o = run([A, "paths", "--base-path", "/"])
    check("R7 D1: sbr_actuator paths --base-path / -> [inference] and does not claim the book says this about base-path", rc == 0 and has(o, "[inference]", "management context path") and "is disabled to avoid conflict (p.449)" not in o, o)
    r12_7 = open(os.path.join(PKG, "references", "12-cli-e-build-plugins.md"), encoding="utf-8").read()
    check("R7 D5: ref 12 summarizes classpath.idx/layers.idx (BOOT-INF, not YAML, quotes, colon, '/') and the p.437 war conflict",
          has(r12_7, "BOOT-INF/classpath.idx", "BOOT-INF/layers.idx", "not read as YAML", "double quotes", "ends in `/`", "internal CONFLICT", "SBR p.437", "SBR p.839-840"), "")
    r02_7 = open(os.path.join(PKG, "references", "02-configuracao-externalizada.md"), encoding="utf-8").read()
    check("R7 D2: ref 02 carries empty prefix=FQN, setter/*Aware, @Component + JavaBean (p.112) and constructor binding does not apply to @Component (p.110)",
          has(r02_7, "without a prefix, the name is just the FQN", "setter", "*Aware", "`@Component` **and** use JavaBean binding", "SBR p.112", "SBR p.110"), "")
    check("R7 D4: ref 02 carries the p.121 NOTE (merging applies to all sources) and YAML list/comma (p.119-120)",
          has(r02_7, "all sources", "SBR p.121", "comma-separated", "SBR p.119-120"), "")
    rc, o = run([L, "merge list map"])
    check("R7 D4: lookup 'merge list map' -> COVERED, p.117-121 (ref 02)", rc == 0 and has(o, "LEVEL: COVERED", "02-configuracao", "117"), o)
    rc, o = run([L, "mesclar lista"])
    check("R7 D4: lookup 'mesclar lista' (Portuguese input) -> COVERED (ref 02)", rc == 0 and has(o, "LEVEL: COVERED", "02-configuracao"), o)
    rc, o = run([L, "--prop", "spring.cache.redis.time-to-live"])
    check("R7 D6: --prop redis time-to-live shows that entries NEVER expire (p.677)", rc == 0 and has(o, "NEVER expire", "p.677"), o)
    rc, o = run([L, "--prop", "management.metrics.export.influx.retention-duration"])
    check("R7 D9: --prop influx retention-duration -> no default and 7d is an example (p.787)", rc == 0 and has(o, "NO published default", "7d", "EXAMPLE", "p.787"), o)
    rc, o = run([L, "Spring Cloud Config"])
    check("R7 D8: lookup 'Spring Cloud Config' -> pointer only; p.857 is an artifact name", has(o, "POINTER ONLY", "p.857", "name of the artifact"), o)
    r05_7 = open(os.path.join(PKG, "references", "05-web-servlet-e-reativo.md"), encoding="utf-8").read()
    check("R7 D7: ref 05 labels the web filters' execution order [inference] and gives the public/error/404.html and 5xx.mustache examples",
          has(r05_7, "[inference]** from the semantics of `Ordered`", "public/error/404.html", "5xx.mustache"), "")

    # ---- round 9 (defects of round 8)
    FXH = os.path.join(FX, "health-path-ruim.properties")
    rc, o = run([P, FXH])
    check("R9 P1: propcheck additional-path without prefix/2 segments/invalid prefix -> ERROR P19 p.462 (rc 1)",
          rc == 1 and has(o, "P19", "no prefix", "single segment", "invalid prefix 'http:'", "SBR p.462"), o)
    check("R9 P1 (negative): quoted server:/healthz and management:/ok do NOT generate P19", "line 4" not in o and "line 5" not in o, o)
    rc, o = run([P, FXH, "--json"])
    check("R9 P1: --json carries 3 P19 findings", rc == 1 and o.count('"regra": "P19"') == 3, o)
    rc, o = run([P, "--rules"])
    check("R9 P1: --rules lists P19 with SBR p.462", has(o, "P19", "additional-path", "SBR p.462"), o)
    rc, o = run([P, os.path.join(FX, "app-ok.yml")])
    check("R9 P1: 'no findings' warns about the scope of the rules", has(o, "rule findings: none", "--rules"), o)
    rc, o = run([K, "check", FXH, "--area", "ACTUATOR"])
    check("R9 P1: checklist C05 ALERT on the invalid additional-path", has(o, "ALERT", "C05", "additional-path", "p.462"), o)
    rc, o = run([K, "check", os.path.join(FX, "app-ok.yml"), "--area", "ACTUATOR"])
    check("R9 P1 (negative): checklist C05 OK without additional-path", has(o, "OK        C05"), o)
    rc, o = run([L, "--prop", "management.metrics.export.appoptics.host-tag"])
    check("R9 P3: --prop host-tag carries the paraphrased description (@host) and default instance p.780", rc == 0 and has(o, "Description (package paraphrase", "@host", "instance", "p.780"), o)
    rc, o = run([L, "--prop", "management.metrics.export.appoptics.api-token"])
    check("R9 P3: --prop api-token -> NO published default value (p.779) and description", rc == 0 and has(o, "NO published default value", "p.779", "Description (package paraphrase"), o)
    rc, o = run([L, "--prop", "management.metrics.export.appoptics.batch-size"])
    check("R9 P3 (negative): batch-size has default 500 and does NOT say 'no default value'", has(o, "500") and "NO published default" not in o, o)
    rc, o = run([L, "--prop", "spring.quartz.thread-pool-size"])
    check("R9 P2: UNKNOWN quartz.thread-pool-size points to spring.quartz.properties.* (p.675/416)", rc == 2 and has(o, "namespace 'spring.quartz.*' KNOWN", "spring.quartz.properties.*", "p.675", "p.416"), o)
    rc, o = run([L, "--prop", "spring.quartz.misfire-threshold"])
    check("R9 P2: UNKNOWN quartz.misfire-threshold likewise", rc == 2 and has(o, "spring.quartz.properties.*"), o)
    rc, o = run([L, "--prop", "management.appoptics.metrics.export.host-tag"])
    check("R9 P2: name with words out of order suggests the right key", rc == 2 and "management.metrics.export.appoptics.host-tag" in o, o)
    rc, o = run([L, "--prop", "acme.custom.flag"])
    check("R9 P2 (negative): unknown namespace does not get a namespace hint", rc == 2 and "known keys of this namespace" not in o, o)
    for term in ("remote devtools", "remote secret", "java.io.tmpdir", "temporary directory", "requiresUnpack", "nested elements", "working directory"):
        rc, o = run([L, term])
        check("R9 P4-P7: lookup '%s' -> COVERED" % term, rc == 0 and "LEVEL: COVERED" in o, o)
    r12_9 = open(os.path.join(PKG, "references", "12-cli-e-build-plugins.md"), encoding="utf-8").read()
    check("R9 P6/P7: ref 12 carries tmpdir, classifier XML, exejar Required and nested elements",
          has(r12_9, "java.io.tmpdir", "<classifier>exec</classifier>", "**not to delete**", "jruby-complete", "`destfile`", "**required**", "`resources`", "`lib`", "SBR p.551-552", "SBR p.656"), "")
    r00_9 = open(os.path.join(PKG, "references", "00-visao-geral-e-versao.md"), encoding="utf-8").read()
    check("R9 P4: ref 00 carries automatic server with secret, manual client, secret via classpath, single-argument URL (p.68-69)",
          has(r00_9, "enabled automatically", "client is launched manually", "same classpath", "only required argument", "SBR p.69"), "")
    r08_9 = open(os.path.join(PKG, "references", "08-mensageria-e-io.md"), encoding="utf-8").read()
    check("R9 P5: ref 08 carries Hazelcast working directory or classpath root (p.414-415)",
          has(r08_9, "working directory", "classpath root", "hazelcast-client.xml", "hazelcast.xml"), "")
    r11_9 = open(os.path.join(PKG, "references", "11-metricas-e-observabilidade.md"), encoding="utf-8").read()
    check("R9 P8: ref 11 locates the AppOptics batch rule on p.779 (not p.792-793)", has(r11_9, "AppOptics", "SBR p.779", "not p.792-793"), "")
    check("R9 P3: index marks sem_default on empty default cells (checked p.779)", _sem_default_ok(), "")

    # ---- round 14 (defects P1-P7 of wave 13)
    rc, o = run([os.path.join("scripts", "sbr_lookup.py"), "--prop", "spring.activemq.send-timeout"])
    check("R14 P5: --prop send-timeout carries a curated description (0 = wait forever, p.717)", rc == 0 and has(o, "Description (package paraphrase", "wait forever", "717"), o)
    rc, o = run([os.path.join("scripts", "sbr_lookup.py"), "--prop", "spring.rabbitmq.connection-timeout"])
    check("R14 P5: --prop rabbitmq.connection-timeout curated (zero = wait forever, p.732)", rc == 0 and has(o, "Description (package paraphrase", "wait forever", "732"), o)
    rc, o = run([os.path.join("scripts", "sbr_lookup.py"), "--page", "406"])
    check("R14 P6: --page 406 returns the package summaries that cite the page (HazelcastInstance/cache)", rc == 0 and has(o, "package summaries that cite SBR p.406", "08-mensageria-e-io.md", "package paraphrase"), o)
    rc, o = run([os.path.join("scripts", "sbr_lookup.py"), "--page", "5"])
    check("R14 P6: --page 5 without a summary says the package does not carry the content", rc == 0 and has(o, "no references/ summary cites"), o)
    r11_14 = open(os.path.join(PKG, "references", "11-metricas-e-observabilidade.md"), encoding="utf-8").read()
    check("R14 P1: ref 11 carries @Timed only on controllers/Jersey, class+method, long task, Micrometer (p.499-512)",
          has(r11_14, "`@Controller`", "Jersey", "SBR p.510-511", "separate metric name", "Micrometer documentation", "TimedAspect"), "")
    r07_14 = open(os.path.join(PKG, "references", "07-dados-sql-e-nosql.md"), encoding="utf-8").read()
    check("R14 P2/P4: ref 07 carries neo4j::getBoltUrl, Kotlin, local Docker and the R2DBC customizer (PORT p.340, OPTIONS p.341)",
          has(r07_14, "neo4j::getBoltUrl", "companion object", "Docker is running locally", "ConnectionFactoryOptions.PORT", "PostgresqlConnectionFactoryProvider.OPTIONS", "SBR p.340", "SBR p.341"), "")
    r08_14 = open(os.path.join(PKG, "references", "08-mensageria-e-io.md"), encoding="utf-8").read()
    check("R14 P3: ref 08 carries a single reused HazelcastInstance unless spring.cache.jcache.config and no customization",
          has(r08_14, "HazelcastInstance", "unless", "no additional customization"), "")
    r05_14 = open(os.path.join(PKG, "references", "05-web-servlet-e-reativo.md"), encoding="utf-8").read()
    check("R14 P7: ref 05 links InternalResourceViewResolver to the DefaultServlet", has(r05_14, "DefaultServlet", "InternalResourceViewResolver"), "")

    # ---- index and verifiers
    idx = json.load(open(os.path.join(PKG, "scripts", "sbr_index.json"), encoding="utf-8"))
    ka = [k for k, v in idx["props"].items() if v["apendice_a"]]
    check("index: >=1500 Appendix A keys", len(ka) >= 1500, str(len(ka)))
    check("index: no truncated key (ending in '-')", not [k for k in ka if k.endswith("-")], "")
    check("index: >=1000 Appendix F dependencies", len(idx["deps"]) >= 1000, str(len(idx["deps"])))
    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations.py (0 failures)", rc == 0 and "total failures: 0" in o, o)
        import re
        m = re.search(r"Checks: (\d+) positive, (\d+) negative", o)
        check("verify_citations: minimum counts", bool(m) and int(m.group(1)) >= 350 and int(m.group(2)) >= 60, o)
        rc, o = run([os.path.join("tests", "audit_tokens.py"), "--src", a.src, "--strict"])
        check("audit_tokens.py: 0 failures and 0 near", rc == 0, o)
    print("\n%d passed, %d failed" % (len(OK), len(FAIL)))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

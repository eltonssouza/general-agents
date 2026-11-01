# -*- coding: utf-8 -*-
"""
sbr_checklist.py - configuration/production checklist according to what "Spring Boot Reference Documentation 2.7.18" (SBR)
carries. Each item cites the PDF page (printed = N-20). Items that cannot be verified with application.properties/yaml alone
appear as VERIFY (manual). Stdlib only; no network; reads only the indicated files.

Usage (python -I):
  python -I scripts/sbr_checklist.py list [--area ACTUATOR|SHUTDOWN|LOGGING|DEV|DATA|CONFIG|WEB|SECURITY|DEPLOY]
  python -I scripts/sbr_checklist.py check FILE [FILE ...] [--json] [--area ...] [--manual]

Status: OK | ALERT | INFO | VERIFY (manual). Thresholds/recommendations are those of the text; anything deduced is labeled [inference].
[DATED]: text of version 2.7.18 (copyright 2012-2023); newer versions may differ.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sbr_common as C  # noqa: E402

SENSITIVE_EP = {"env", "configprops", "heapdump", "threaddump", "shutdown", "loggers", "beans", "mappings", "logfile", "httptrace", "sessions", "jolokia"}


class Ctx(object):
    def __init__(self, files):
        self.kv = {}
        self.files = files
        for f in files:
            for d in C.load_config_file(f):
                for k, v, _ in d.items:
                    self.kv[re.sub(r"\[\d+\]", "", k) if False else k] = v

    def get(self, k, default=None):
        return self.kv.get(k, default)

    def has(self, k):
        return k in self.kv

    def prefix(self, p):
        return {k: v for k, v in self.kv.items() if k.startswith(p)}

    def true(self, k):
        return str(self.kv.get(k, "")).strip().lower() == "true"


def _exposure(ctx):
    v = ctx.get("management.endpoints.web.exposure.include")
    if v is None:
        items = [(k, x) for k, x in ctx.kv.items() if k.startswith("management.endpoints.web.exposure.include[")]
        if items:
            v = ",".join(x for _, x in sorted(items))
    return v


def c01(ctx):
    v = _exposure(ctx)
    if v is None:
        return "OK", "management.endpoints.web.exposure.include not set: by default only health is exposed over HTTP"
    ids = {x.strip().strip("\"'").lower() for x in v.split(",")}
    exc = {x.strip().lower() for x in str(ctx.get("management.endpoints.web.exposure.exclude", "")).split(",") if x.strip()}
    if "*" in ids:
        left = sorted(SENSITIVE_EP - exc)
        return "ALERT", "include=* exposes all web endpoints; the text says to protect them (firewall/Spring Security). Sensitive ones still exposed: %s" % ", ".join(left)
    risky = sorted((ids & SENSITIVE_EP) - exc)
    if risky:
        return "ALERT", "exposed over HTTP and potentially sensitive: %s (protect them)" % ", ".join(risky)
    return "OK", "web exposure: %s" % v


def c02(ctx):
    if ctx.true("management.endpoint.shutdown.enabled"):
        return "ALERT", "shutdown endpoint enabled; POST under default CSRF returns 403 and the endpoint only works with a jar"
    return "OK", "shutdown remains disabled (default)"


def c03(ctx):
    v = str(ctx.get("management.endpoint.health.show-details", "never")).lower()
    if v == "always":
        return "ALERT", "show-details=always shows details to everyone; security must allow /health for authenticated and unauthenticated users"
    return "OK", "show-details=%s" % v


def c04(ctx):
    if ctx.has("management.server.port"):
        return "INFO", "own management port (%s): probes and health on a different port may pass even with the main app broken; consider management.endpoint.health.probes.add-additional-paths=true" % ctx.get("management.server.port")
    return "OK", "management on the same port as the application"


def c05(ctx):
    bad = []
    n = 0
    for k, v in sorted(ctx.kv.items()):
        if C.ADDITIONAL_PATH_KEY.match(re.sub(r"\[\d+\]", "", k)):
            n += 1
            r = C.check_additional_path(v)
            if r:
                bad.append("%s=%s: %s" % (k, v, r[1]))
    if bad:
        return "ALERT", "configuration ERROR in additional-path: " + " | ".join(bad)
    if n:
        return "OK", "%d health group additional-path in the server:/management: + one segment format" % n
    return "OK", "no health group additional-path"


def c10(ctx):
    if str(ctx.get("server.shutdown", "immediate")).lower() == "graceful":
        return "OK", "server.shutdown=graceful"
    return "ALERT", "server.shutdown is not graceful (Appendix A default: immediate)"


def c11(ctx):
    if ctx.has("spring.lifecycle.timeout-per-shutdown-phase"):
        return "INFO", "timeout-per-shutdown-phase=%s: on Kubernetes keep terminationGracePeriodSeconds greater than this (default 30s)" % ctx.get("spring.lifecycle.timeout-per-shutdown-phase")
    return "INFO", "timeout-per-shutdown-phase not set (Appendix A: 30s)"


def c20(ctx):
    if ctx.has("logging.file.name") or ctx.has("logging.file.path"):
        return "OK", "file logging configured (default rotation at 10 MB, SBR p.140)"
    return "INFO", "no logging.file.name/path: logs go to the console only (p.140); in production in a container this is usually what is wanted [inference]"


def c22(ctx):
    bad = [k for k in ("debug", "trace") if ctx.true(k)]
    if bad:
        return "ALERT", "%s=true turns on extra logging of core loggers; not for production [inference from p.138-139]" % ",".join(bad)
    return "OK", "debug/trace off"


def c30(ctx):
    k = ctx.prefix("spring.devtools.")
    if k:
        extra = " (remote.secret requires a trusted network/SSL and never production)" if "spring.devtools.remote.secret" in k else ""
        return "ALERT", "devtools properties present (%s)%s; devtools is a development feature" % (", ".join(sorted(k)[:4]), extra)
    return "OK", "no devtools properties"


def c31(ctx):
    if ctx.true("spring.h2.console.enabled"):
        return "ALERT", "H2 console enabled: for development only (no CSRF, uses frames)"
    return "OK", "H2 console not enabled"


def c33(ctx):
    bad = [k for k in ("server.error.include-stacktrace", "server.error.include-message", "server.error.include-binding-errors") if str(ctx.get(k, "")).lower() == "always"]
    if bad:
        return "ALERT", "%s=always (this is what devtools applies in dev): exposes error details to the client" % ", ".join(bad)
    return "OK", "error details not forced to always"


def c35(ctx):
    bad = [k for k in ("spring.mvc.log-request-details", "spring.codec.log-request-details") if ctx.true(k)]
    if bad:
        return "ALERT", "%s=true logs request details, possibly sensitive" % ", ".join(bad)
    return "OK", "request-details logging off"


def c40(ctx):
    v = ctx.get("spring.jpa.hibernate.ddl-auto")
    if v is None:
        return "INFO", "ddl-auto not set: default create-drop if embedded database and no Flyway/Liquibase; none otherwise"
    if str(v).lower() in ("create", "create-drop", "update"):
        return "ALERT", "ddl-auto=%s changes/recreates the schema at startup; in production prefer none/validate + a migration tool [inference]" % v
    return "OK", "ddl-auto=%s" % v


def c41(ctx):
    if not ctx.has("spring.jpa.open-in-view") and any(k.startswith("spring.jpa.") or k.startswith("spring.datasource.") for k in ctx.kv):
        return "INFO", "spring.jpa.open-in-view not set: in a web app the default registers OpenEntityManagerInViewInterceptor (lazy loading in views)"
    return "OK", "open-in-view explicit or JPA absent"


def c42(ctx):
    mig = any(k.startswith("spring.flyway.") or k.startswith("spring.liquibase.") for k in ctx.kv)
    if mig and str(ctx.get("spring.sql.init.mode", "")).lower() == "always":
        return "ALERT", "spring.sql.init.mode=always together with Flyway/Liquibase: the text does not recommend mixing schema.sql/data.sql with a migration tool"
    return "OK", "no declared mix of migration and SQL scripts"


def c43(ctx):
    if str(ctx.get("spring.quartz.jdbc.initialize-schema", "")).lower() == "always":
        return "ALERT", "the default Quartz scripts DROP existing tables on every restart (triggers are lost)"
    return "OK", "Quartz initialize-schema is not always"


def c44(ctx):
    ds = ctx.prefix("spring.datasource.")
    if ds and not ctx.has("spring.datasource.url") and not ctx.has("spring.datasource.jndi-name"):
        return "INFO", "spring.datasource.* without url/jndi-name: without a URL Boot tries to configure an embedded database"
    return "OK", "url/jndi-name present or DataSource not configured"


def c50(ctx):
    if ctx.true("spring.main.lazy-initialization"):
        return "INFO", "lazy-initialization=true: delays the discovery of errors and requires memory for all beans; the text recommends tuning the heap first"
    return "OK", "lazy initialization not enabled"


def c51(ctx):
    bad = []
    for k, v in ctx.kv.items():
        last = k.split(".")[-1].lower()
        if re.search(r"(password|secret|token|api-key|apikey|key)$", last) and v and not v.strip().startswith("${") and v.strip() not in ("", "true", "false"):
            if last in ("key",) and not re.search(r"(api|secret|private)", k.lower()):
                continue
            bad.append(k)
    if bad:
        return "ALERT", "literal value in a sensitive key: %s. The book: no native property encryption, but there is a hook via EnvironmentPostProcessor and Spring Cloud Vault (SBR p.101); configtree/Docker secrets via spring.config.import=optional:configtree: (SBR p.97-98, import p.96); the env and configprops endpoints mask (******) values of keys such as password/secret/key/token (SBR p.639) [from source]" % ", ".join(sorted(bad)[:5])
    return "OK", "no obvious literal secrets"


def c61(ctx):
    k = "server.tomcat.remoteip.internal-proxies"
    if ctx.has(k) and str(ctx.get(k)).strip() == "":
        return "ALERT", "empty internal-proxies trusts all proxies: do not do this in production"
    return "OK", "internal-proxies is not empty"


def c64(ctx):
    if ctx.has("spring.mail.host"):
        need = [t for t in ("connectiontimeout", "timeout", "writetimeout") if not any(("mail.smtp." + t) in k for k in ctx.kv)]
        if need:
            return "ALERT", "spring.mail.host without SMTP timeouts (%s): some defaults are infinite and can block threads" % ", ".join(need)
    return "OK", "no mail or timeouts defined"


def c65(ctx):
    for k in ("spring.servlet.multipart.max-file-size", "spring.servlet.multipart.max-request-size"):
        if str(ctx.get(k, "")).strip() == "-1":
            return "ALERT", "%s=-1 leaves the upload unlimited (defaults: 1MB per file and 10MB per request)" % k
    return "OK", "multipart limits not removed"


def c70(ctx):
    if ctx.has("spring.security.user.password"):
        return "INFO", "default user password set by property; the password generated in the log is for development only (use your own security in production)"
    return "VERIFY", "no spring.security.user.*: if Spring Security is on the classpath, the generated password is for dev only; define your own security configuration"


MANUAL = [
    ("M01", "ACTUATOR", "Liveness/readiness probes: liveness must not depend on external systems; decide consciously what goes into readiness.", "p.464"),
    ("M02", "ACTUATOR", "If Actuator uses a separate port, consider probes on the main port (/livez, /readyz).", "p.463"),
    ("M03", "ACTUATOR", "InMemoryAuditEventRepository and InMemoryHttpTraceRepository are for development only; use a production alternative.", "p.517-518"),
    ("M04", "ACTUATOR", "With Spring Security, define a SecurityFilterChain for endpoints (EndpointRequest) and for the rest of the app: Boot backs off entirely when it sees a SecurityFilterChain.", "p.446-448"),
    ("M05", "DEPLOY", "On Kubernetes: preStop with sleep and terminationGracePeriodSeconds greater than spring.lifecycle.timeout-per-shutdown-phase.", "p.527-528"),
    ("M06", "DEPLOY", "init.d service: never run as root (RUN_AS_USER, jar owner, chmod 500, chattr +i, .conf 400).", "p.536-537"),
    ("M07", "DEPLOY", "Container image: use layers (layers.idx / jarmode layertools) or buildpacks; layertools does not work with a fully executable jar.", "p.436-438"),
    ("M08", "DEPLOY", "Executable jar for production; devtools is not in the repackaged jar by default and is disabled on java -jar; to include it (remote devtools only, never in production): excludeDevtools=false (Maven) or a classpath with developmentOnly (Gradle).", "p.59, 68"),
    ("M09", "DATA", "A single schema-creation strategy (JPA/Hibernate, SQL scripts or Flyway/Liquibase).", "p.628"),
    ("M10", "DATA", "Connection pool: HikariCP is preferred if present; set what is needed in spring.datasource.hikari.*.", "p.325"),
    ("M11", "CONFIG", "No @PropertySource for logging.* and spring.main.* (too late).", "p.88, 559"),
    ("M12", "CONFIG", "No native property encryption; consider configtree/Docker secrets or Spring Cloud Vault.", "p.96-98, 101"),
    ("M13", "WEB", "Behind a proxy: server.forward-headers-strategy (NATIVE/FRAMEWORK) and, on Tomcat, redirect-context-root=false with SSL at the proxy.", "p.580-582"),
    ("M14", "SECURITY", "InMemoryOAuth2AuthorizedClientService is for development only; use JdbcOAuth2AuthorizedClientService or your own implementation.", "p.308"),
    ("M15", "WEB", "H2 console for development only; behind Spring Security it requires CSRF off and X-Frame-Options SAMEORIGIN for the console.", "p.334-336"),
]

ITEMS = [
    ("C01", "ACTUATOR", "Web exposure of endpoints (management.endpoints.web.exposure.*)", c01, "p.444-445"),
    ("C02", "ACTUATOR", "shutdown endpoint", c02, "p.442, 448"),
    ("C03", "ACTUATOR", "health.show-details", c03, "p.454"),
    ("C04", "ACTUATOR", "Separate management port", c04, "p.463, 471"),
    ("C05", "ACTUATOR", "health group additional-path (server:/management: prefix and a single segment)", c05, "p.462"),
    ("C10", "SHUTDOWN", "Graceful shutdown (server.shutdown)", c10, "p.300"),
    ("C11", "SHUTDOWN", "Timeout per shutdown phase", c11, "p.300-301, 528; default 30s: appendix A p.672"),
    ("C20", "LOGGING", "Log file / rotation", c20, "p.140"),
    ("C22", "LOGGING", "debug/trace on", c22, "p.138-139"),
    ("C30", "DEV", "devtools properties", c30, "p.59, 68"),
    ("C31", "DEV", "H2 console", c31, "p.334"),
    ("C33", "DEV", "server.error.include-* = always", c33, "p.60"),
    ("C35", "DEV", "log-request-details", c35, "p.60"),
    ("C40", "DATA", "spring.jpa.hibernate.ddl-auto", c40, "p.333, 617, 629"),
    ("C41", "DATA", "spring.jpa.open-in-view", c41, "p.333"),
    ("C42", "DATA", "SQL scripts x Flyway/Liquibase", c42, "p.630"),
    ("C43", "DATA", "Quartz initialize-schema=always", c43, "p.416"),
    ("C44", "DATA", "spring.datasource.url", c44, "p.324"),
    ("C50", "CONFIG", "Lazy initialization", c50, "p.73"),
    ("C51", "CONFIG", "Literal secrets in files", c51, "p.96-98, 101, 639"),
    ("C61", "WEB", "Tomcat remoteip internal-proxies", c61, "p.581-582"),
    ("C64", "WEB", "Timeouts SMTP", c64, "p.418-419"),
    ("C65", "WEB", "Multipart limits", c65, "p.591"),
    ("C70", "SECURITY", "Spring Security default user", c70, "p.301"),
]


def cmd_list(a):
    area = a.area.upper() if a.area else None
    print("Checklist (SBR 2.7.18; pages = PDF, printed = N-20)")
    print("-- verifiable in configuration files --")
    for iid, ar, title, fn, pg in ITEMS:
        if area and ar != area:
            continue
        print("%s [%s] %s (SBR %s)" % (iid, ar, title, pg))
    print("-- manual (VERIFY) --")
    for iid, ar, title, pg in MANUAL:
        if area and ar != area:
            continue
        print("%s [%s] %s (SBR %s)" % (iid, ar, title, pg))
    return 0


def cmd_check(a):
    ctx = Ctx(a.files)
    area = a.area.upper() if a.area else None
    res = []
    for iid, ar, title, fn, pg in ITEMS:
        if area and ar != area:
            continue
        st, msg = fn(ctx)
        res.append({"id": iid, "area": ar, "titulo": title, "status": st, "msg": msg, "fonte": "SBR " + pg})
    if a.manual or True:
        for iid, ar, title, pg in MANUAL:
            if area and ar != area:
                continue
            res.append({"id": iid, "area": ar, "titulo": title, "status": "VERIFY", "msg": "manual", "fonte": "SBR " + pg})
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    order = {"ALERT": 0, "INFO": 1, "VERIFY": 2, "OK": 3}
    for r in sorted(res, key=lambda r: (order[r["status"]], r["id"])):
        if r["status"] == "VERIFY" and not a.manual and r["msg"] == "manual":
            continue
        print("%-9s %s [%s] %s: %s (%s)" % (r["status"], r["id"], r["area"], r["titulo"], r["msg"], r["fonte"]))
    cnt = {}
    for r in res:
        cnt[r["status"]] = cnt.get(r["status"], 0) + 1
    print("\nSummary: " + ", ".join("%s=%d" % (k, v) for k, v in sorted(cnt.items())) + ("; use --manual to see the %d manual items" % len(MANUAL) if not a.manual else ""))
    print("Warning: checklist based only on the 2.7.18 text; it does not replace a security/operations review. Keys not listed here: NOT COVERED.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("list")
    p.add_argument("--area")
    p = sub.add_parser("check")
    p.add_argument("files", nargs="+")
    p.add_argument("--area")
    p.add_argument("--json", action="store_true")
    p.add_argument("--manual", action="store_true")
    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        return 0
    return {"list": cmd_list, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

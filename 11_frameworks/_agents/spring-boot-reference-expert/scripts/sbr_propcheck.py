# -*- coding: utf-8 -*-
"""
sbr_propcheck.py - STATIC validator for application.properties / application.yml against the keys that the text of
"Spring Boot Reference Documentation, Version 2.7.18" (SBR) documents (Appendix A and body).

CENTRAL RULE: a key that does not appear in the text = "UNKNOWN in the text" (NOT an error: it may come from another jar, a
third-party starter or the project itself). There is ERROR/ALERT only when the text supports the rule (with page SBR p.N,
PDF page; printed = N-20). No network; does not run the framework; reads only the indicated files.

Usage (python -I):
  python -I scripts/sbr_propcheck.py ARQ [ARQ ...] [--json] [--only-unknown] [--no-suggest] [--as-profile NAME]
  python -I scripts/sbr_propcheck.py --rules          # lists the rules and the source of each one
Output: per key: KNOWN (appendix A p.N / body p.N, default when extracted) or UNKNOWN; rule findings.
Rule P01 (profiles.active/default/include) depends on the file NAME (application-<profile>.*) or on on-profile in the document;
if the file has another name but is loaded as a profile file, use --as-profile NAME (the output warns when these keys appear in a non-profile file).
Rules: --rules (includes P19, health group additional-path, p.462). Exit code: 1 if there is an ERROR; 0 otherwise.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sbr_common as C  # noqa: E402

RULES = [
    ("P01", "ERROR", "spring.profiles.active/default/include are only valid in NON-profile-specific documents (an application-<profile> file or a document with on-profile)", "SBR p.135-136"),
    ("P02", "ALERT", "spring.config.name/location/additional-location must be environment properties (env, system property, command line); in application.properties they arrive too late", "SBR p.91"),
    ("P04", "ERROR", "YAML with a tab in the indentation", "[extrapolation: general YAML rule]"),
    ("P05", "ERROR", "unquoted '*' value in YAML (alias); the text says to use quotes in management.endpoints.web.exposure.include", "SBR p.445"),
    ("P06", "INFO", "the text recommends lowercase kebab-case in .properties/.yaml (camelCase/underscore are accepted by relaxed binding)", "SBR p.116"),
    ("P07", "ALERT", "repeated key in the same document (the last one wins in .properties; in YAML the behavior depends on the parser)", "[inference]"),
    ("P08", "ALERT", "${...} placeholder with a non-canonical name (camelCase/underscore): only lowercase kebab-case matches all forms of relaxed binding", "SBR p.99"),
    ("P13", "ALERT", "document separator in .properties must be exactly #--- or !--- with no leading space", "SBR p.100"),
    ("P14", "ALERT", "management.endpoint.<id>: id not listed in the text as an endpoint", "SBR p.441-442"),
    ("P16", "ALERT", "in logging properties use ':' (not ':-') as the default-value separator in placeholders", "SBR p.145"),
    ("P17", "ALERT", "spring.jpa.properties.*: names must be exactly those of the JPA provider (no relaxed binding)", "SBR p.618"),
    ("P19", "ERROR", "management.endpoint.health.group.<g>.additional-path: prefix `server:` or `management:` is mandatory and the path has a SINGLE segment (e.g. server:/healthz; '/healthz/live' or no prefix is an error)", "SBR p.462"),
    ("P18", "INFO", "Duration: accepted formats = number (ms), ISO-8601 or value+unit (ns us ms s m h d)", "SBR p.121-123"),
]
PROFILE_ONLY = ("spring.profiles.active", "spring.profiles.default", "spring.profiles.include")
EARLY = ("spring.config.name", "spring.config.location", "spring.config.additional-location")
ENDPOINT_IDS = {"auditevents", "beans", "caches", "conditions", "configprops", "env", "flyway", "health", "httptrace",
                "info", "integrationgraph", "loggers", "liquibase", "metrics", "mappings", "quartz", "scheduledtasks",
                "sessions", "shutdown", "startup", "threaddump", "heapdump", "jolokia", "logfile", "prometheus"}


def check_file(path, idx, matcher, suggest=True, as_profile=None):
    docs = C.load_config_file(path)
    fprofile = as_profile or C.profile_from_filename(path)
    # endpoint ids also coming from Appendix A
    ids = set(ENDPOINT_IDS)
    for k in idx["props"]:
        m = re.match(r"^management\.endpoint\.([a-z0-9\-]+)\.", k)
        if m:
            ids.add(m.group(1))
    out = {"arquivo": path, "perfil_do_arquivo": fprofile, "chaves": [], "achados": [], "notas": []}
    for d in docs:
        for sev, rid, line, msg in d.issues:
            out["achados"].append({"sev": sev, "regra": rid, "doc": d.index, "linha": line, "msg": msg})
        in_profile = bool(fprofile) or ("on-profile" in d.activation)
        seen = {}
        for key, val, line in d.items:
            info = {"chave": key, "valor": val, "doc": d.index, "linha": line}
            canon, how = matcher.match(key)
            if canon:
                p = idx["props"].get(canon) or idx["props"].get(key)
                info["status"] = "KNOWN"
                info["canonica"] = canon
                if p:
                    info["apendice_a"] = p.get("apendice_a")
                    info["corpo"] = p.get("corpo")
                    if p.get("default") is not None:
                        info["default_apendice_a"] = p["default"]
                    elif p.get("default_desc"):
                        info["default_na_descricao_apendice_a"] = p["default_desc"]
            else:
                info["status"] = "UNKNOWN"
                if suggest:
                    s = matcher.suggest(re.sub(r"\[[^\]]*\]", "", key))
                    if s:
                        info["parecido_com"] = s
            out["chaves"].append(info)
            base = re.sub(r"\[[^\]]*\]$", "", key)
            if key in seen and not re.search(r"\[\d+\]", key):
                out["achados"].append({"sev": "ALERT", "regra": "P07", "doc": d.index, "linha": line,
                                       "msg": "repeated key (first on line %d)" % seen[key]})
            seen.setdefault(key, line)
            if base in PROFILE_ONLY and not in_profile:
                out["notas"].append("%s (line %d): rule P01 decides by the file NAME (application-<profile>.*) or by on-profile in the document; "
                                    "this file was treated as NOT profile-specific. If it is loaded as a profile file under another name "
                                    "(e.g. via spring.config.location/import), run with --as-profile NAME" % (key, line))
            if base in PROFILE_ONLY and in_profile:
                out["achados"].append({"sev": "ERROR", "regra": "P01", "doc": d.index, "linha": line,
                                       "msg": "%s cannot be in a profile-specific file/document (SBR p.135-136)" % base})
            if key in EARLY:
                out["achados"].append({"sev": "ALERT", "regra": "P02", "doc": d.index, "linha": line,
                                       "msg": "%s must come from env/system property/command line (SBR p.91)" % key})
            if how == "exact" and re.sub(r"\[[^\]]*\]", "", key) != canon and not re.search(r"[A-Z_]", canon) and not key.startswith("spring.jpa.properties"):
                out["achados"].append({"sev": "INFO", "regra": "P06", "doc": d.index, "linha": line,
                                       "msg": "%s: documented canonical form is %s (relaxed binding accepts it, but prefer kebab-case; SBR p.116)" % (key, canon)})
            m = re.match(r"^management\.endpoint\.([A-Za-z0-9\-]+)\.", key)
            if m and m.group(1).lower() not in ids:
                out["achados"].append({"sev": "ALERT", "regra": "P14", "doc": d.index, "linha": line,
                                       "msg": "endpoint id '%s' is not in SBR p.441-442" % m.group(1)})
            for ph in re.findall(r"\$\{([^}:]+)", val or ""):
                if re.search(r"[A-Z]", ph) and "." in ph and not re.fullmatch(r"[A-Z0-9_]+", ph) and not ph.startswith("random"):
                    out["achados"].append({"sev": "ALERT", "regra": "P08", "doc": d.index, "linha": line,
                                           "msg": "placeholder ${%s}: use the canonical kebab-case name (SBR p.99)" % ph})
            if C.ADDITIONAL_PATH_KEY.match(key):
                r = C.check_additional_path(val)
                if r:
                    out["achados"].append({"sev": r[0], "regra": "P19", "doc": d.index, "linha": line,
                                           "msg": "%s = %s: %s" % (key, val, r[1])})
            if key.startswith("logging.") and ":-" in (val or ""):
                out["achados"].append({"sev": "ALERT", "regra": "P16", "doc": d.index, "linha": line,
                                       "msg": "use ':' and not ':-' in placeholders of logging properties (SBR p.145)"})
            if key.startswith("spring.jpa.properties."):
                rest = key[len("spring.jpa.properties."):]
                if "-" in rest or re.search(r"[a-z][A-Z]", rest):
                    out["achados"].append({"sev": "ALERT", "regra": "P17", "doc": d.index, "linha": line,
                                           "msg": "%s: no relaxed binding in spring.jpa.properties.*; use the exact provider name (e.g. hibernate.jdbc.batch_size) (SBR p.618)" % key})
    return out


def render(res, only_unknown=False):
    lines = []
    lines.append("== %s%s ==" % (res["arquivo"], " (profile %s)" % res["perfil_do_arquivo"] if res["perfil_do_arquivo"] else ""))
    known = [c for c in res["chaves"] if c["status"] == "KNOWN"]
    unk = [c for c in res["chaves"] if c["status"] == "UNKNOWN"]
    lines.append("keys: %d known in the text, %d unknown (unknown is NOT an error)" % (len(known), len(unk)))
    if not only_unknown:
        for c in known:
            pg = []
            if c.get("apendice_a"):
                pg.append("appendix A p.%s" % ",".join(map(str, c["apendice_a"])))
            if c.get("corpo"):
                pg.append("body p.%s" % ",".join(map(str, c["corpo"][:4])))
            extra = " default(appendix A)=%s" % c["default_apendice_a"] if "default_apendice_a" in c else ""
            lines.append("  KNOWN         %s = %s  [%s]%s" % (c["chave"], c["valor"], "; ".join(pg) or "prefix pattern", extra))
    for c in unk:
        sug = "  [inference] similar to: %s" % ", ".join(c["parecido_com"]) if c.get("parecido_com") else ""
        lines.append("  UNKNOWN       %s = %s  (line %d)%s" % (c["chave"], c["valor"], c["linha"], sug))
    if res["achados"]:
        lines.append("rule findings:")
        order = {"ERROR": 0, "ALERT": 1, "INFO": 2}
        for a in sorted(res["achados"], key=lambda a: (order[a["sev"]], a["linha"])):
            lines.append("  %-8s %s line %d: %s" % (a["sev"], a["regra"], a["linha"], a["msg"]))
    else:
        lines.append("rule findings: none (only the --rules rules; a KNOWN key does not mean a valid value)")
    for n in sorted(set(res.get("notas", []))):
        lines.append("  NOTE     " + n)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only-unknown", action="store_true")
    ap.add_argument("--no-suggest", action="store_true")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--as-profile", metavar="NAME", help="treat the file(s) as specific to profile NAME (rule P01 depends on the file name or on on-profile)")
    a = ap.parse_args()
    if a.rules:
        for rid, sev, desc, src in RULES:
            print("%s %-8s %s [%s]" % (rid, sev, desc, src))
        return 0
    if not a.files:
        ap.error("provide at least one file")
    idx = C.load_index()
    matcher = C.KeyMatcher(idx)
    results = [check_file(f, idx, matcher, not a.no_suggest, a.as_profile) for f in a.files]
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        print("\n\n".join(render(r, a.only_unknown) for r in results))
        print("\nSource: SBR 2.7.18; pages = PDF (printed = N-20). Unknown key = absent from the text, not invalid.")
    return 1 if any(x["sev"] == "ERROR" for r in results for x in r["achados"]) else 0


if __name__ == "__main__":
    sys.exit(main())

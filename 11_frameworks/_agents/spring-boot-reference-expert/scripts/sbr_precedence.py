# -*- coding: utf-8 -*-
"""
sbr_precedence.py - resolves the PRECEDENCE of configuration sources according to SBR 2.7.18 ("Externalized Configuration",
PDF p.87-88 and 90-94; printed = N-20). Stdlib only; no network.

Usage (python -I):
  python -I scripts/sbr_precedence.py order                 # lists the 15 PropertySources (the last wins) and the file order
  python -I scripts/sbr_precedence.py winner SOURCE1 SOURCE2 ...   # indicates which wins (accepts aliases, see "aliases")
  python -I scripts/sbr_precedence.py aliases
  python -I scripts/sbr_precedence.py locations             # order of the default application.properties/yaml locations
  python -I scripts/sbr_precedence.py env-name KEY           # converts a canonical key into an environment variable name (SBR p.117)
  python -I scripts/sbr_precedence.py duration VALUE         # interprets Duration/DataSize/Period according to the text (p.121-127)

Rule of the text: later sources in the list override earlier ones (p.87).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sbr_common as C  # noqa: E402,F401

# (position, name, aliases)
SOURCES = [
    (1, "Default properties (SpringApplication.setDefaultProperties)", ["default", "defaults", "default-properties", "setdefaultproperties"]),
    (2, "@PropertySource on @Configuration classes (added late: does not work for logging.* and spring.main.*)", ["propertysource", "@propertysource"]),
    (3, "Config data (application.properties/yaml)", ["config", "config-data", "configdata", "application.properties", "application.yml", "application.yaml", "application-properties"]),
    (4, "RandomValuePropertySource (random.*)", ["random"]),
    (5, "OS environment variables", ["env", "environment", "os-env", "variavel-de-ambiente", "env-var", "env-vars", "envvar", "envvars", "environment-variable", "environment-variables"]),
    (6, "Java system properties (-Dkey=value)", ["sysprop", "system-property", "system-properties", "-d", "jvm-arg"]),
    (7, "JNDI attributes java:comp/env", ["jndi"]),
    (8, "ServletContext init parameters", ["servletcontext", "servlet-context"]),
    (9, "ServletConfig init parameters", ["servletconfig", "servlet-config"]),
    (10, "SPRING_APPLICATION_JSON (inline JSON in an env var or system property)", ["spring_application_json", "spring.application.json", "application-json", "json"]),
    (11, "Command-line arguments (--key=value)", ["cli", "cmd", "cmdline", "cmd-line", "command-line", "commandline", "command-line-args", "command-line-arguments", "cli-args", "args", "arg", "argument", "arguments"]),
    (12, "'properties' attribute in tests (@SpringBootTest and slices)", ["test-properties", "properties-attr"]),
    (13, "@DynamicPropertySource in tests", ["dynamicpropertysource", "@dynamicpropertysource"]),
    (14, "@TestPropertySource in tests", ["testpropertysource", "@testpropertysource"]),
    (15, "Devtools global settings ($HOME/.config/spring-boot) with devtools active", ["devtools", "devtools-global"]),
]
FILES = [
    (1, "application.properties (and YAML variants) PACKAGED in the jar", ["jar", "jar-application", "jar-config-data", "jar-application.properties", "packaged", "packaged-config-data", "internal"]),
    (2, "application-{profile}.properties (and YAML) PACKAGED in the jar", ["jar-profile", "jar-profile-config-data", "jar-profile-specific", "packaged-profile", "internal-profile"]),
    (3, "application.properties (and YAML) OUTSIDE the jar", ["external", "external-config-data", "outside", "outside-jar", "external-application.properties"]),
    (4, "application-{profile}.properties (and YAML) OUTSIDE the jar", ["external-profile", "external-profile-config-data", "external-profile-specific", "outside-profile"]),
]
LOCATIONS = [
    "1.a classpath: root",
    "1.b classpath: /config",
    "2.a current directory",
    "2.b current directory: config/",
    "2.c immediate children of config/ (config/*/)",
]


def _norm(a):
    return a.strip().lower()


def find(alias, table):
    n = _norm(alias)
    for pos, name, al in table:
        if n == str(pos) or n in al or n == _norm(name):
            return pos, name
    return None


def cmd_order(a):
    print("PropertySources (the LAST wins; SBR p.87-88):")
    for pos, name, _ in SOURCES:
        print("  %2d. %s" % (pos, name))
    print("\nConfig data files (SBR p.88; the lower one wins):")
    for pos, name, _ in FILES:
        print("  %d. %s" % (pos, name))
    print("\nIn the same location, .properties takes precedence over YAML (p.88). Profiles: with several active, 'last-wins' applies (p.93).")
    return 0


def cmd_aliases(a):
    for pos, name, al in SOURCES + [(100 + p, n, x) for p, n, x in FILES]:
        print("%3d  %s -> %s" % (pos, name.split(" (")[0], ", ".join(al)))
    return 0


def cmd_winner(a):
    found = []
    for s in a.sources:
        r = find(s, SOURCES) or find(s, [(100 + p, n, x) for p, n, x in FILES])
        if not r:
            print("unknown source (NOT COVERED in the p.87-88 table): %s" % s)
            return 2
        found.append((s, r))
    # only compares within the same table
    srcs = [(s, r) for s, r in found if r[0] < 100]
    if len(srcs) == len(found):
        win = max(srcs, key=lambda x: x[1][0])
        print("Wins: %s [position %d] (SBR p.87-88)" % (win[1][1], win[1][0]))
        for s, r in sorted(srcs, key=lambda x: -x[1][0]):
            print("  %2d  %s" % (r[0], r[1]))
        if any(r[0] == 3 for _, r in srcs):
            print("Note: 'config data' (3) covers the 4 file types; among them the file order applies (command 'order').")
        return 0
    files = [(s, r) for s, r in found if r[0] >= 100]
    if len(files) == len(found):
        win = max(files, key=lambda x: x[1][0])
        print("Wins among files: %s (SBR p.88)" % win[1][1])
        return 0
    # mixed: config data files compete as "Config data" (position 3) with the other PropertySources
    merged = []
    for s_, r in found:
        if r[0] >= 100:
            merged.append((s_, (3, "Config data (%s)" % r[1])))
        else:
            merged.append((s_, r))
    win = max(merged, key=lambda x: x[1][0])
    print("Wins: %s [position %d] (SBR p.87-88; config data files occupy position 3)" % (win[1][1], win[1][0]))
    nfiles = [r for _, r in found if r[0] >= 100]
    if len(nfiles) > 1:
        best = max(nfiles, key=lambda r: r[0])
        print("Among the config data files cited, the one that wins internally: %s ('order' ranking, p.88)" % best[1])
    for s_, r in sorted(merged, key=lambda x: -x[1][0]):
        print("  %2d  %s" % (r[0], r[1]))
    return 0


def cmd_locations(a):
    print("Default locations (increasing order of precedence; SBR p.90-91):")
    for l in LOCATIONS:
        print("  " + l)
    print("spring.config.location REPLACES these locations; spring.config.additional-location ADDS to them (p.92). "
          "Directories must end with '/'. The optional: prefix avoids ConfigDataLocationNotFoundException (p.92).")
    return 0


def cmd_env(a):
    k = a.key
    m = re.match(r"^(.*?)(\[(\d+)\])?(\..*)?$", k)
    name = re.sub(r"\[(\d+)\]", r"_\1_", k)
    name = name.replace(".", "_").replace("-", "").upper()
    name = re.sub(r"_+", "_", name).strip("_") if "[" in k else name
    print("%s -> %s  (dots become _, '-' removed, uppercase; list indexes between _; SBR p.117)" % (k, name))
    return 0


def cmd_duration(a):
    v = a.value.strip()
    out = []
    m = re.fullmatch(r"(-?\d+)(ns|us|ms|s|m|h|d)?", v)
    if m:
        out.append("Duration: number%s; no unit = milliseconds unless @DurationUnit (SBR p.121-123)" % (" with unit " + m.group(2) if m.group(2) else ""))
        out.append("Period: '%s' with no unit = days; units y m w d accepted only in the simple format (p.125)" % v if not m.group(2) else "")
    if re.fullmatch(r"P.*", v):
        out.append("Duration/Period: ISO-8601 format (p.121,125)")
    if re.fullmatch(r"\d+(B|KB|MB|GB|TB)?", v):
        out.append("DataSize: number%s; no unit = bytes unless @DataSizeUnit (p.125-127)" % ("" if v.isdigit() else " with unit"))
    if re.fullmatch(r"(\d+[ymwd])+", v):
        out.append("Period simple format (e.g. 1y3d = 1 year and 3 days; w = 7 days) (p.125)")
    print("\n".join(x for x in out if x) or "NOT COVERED: format not recognized by the rules on p.121-127")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("order")
    sub.add_parser("aliases")
    sub.add_parser("locations")
    p = sub.add_parser("winner")
    p.add_argument("sources", nargs="+")
    p = sub.add_parser("env-name")
    p.add_argument("key")
    p = sub.add_parser("duration")
    p.add_argument("value")
    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        return 0
    return {"order": cmd_order, "aliases": cmd_aliases, "winner": cmd_winner, "locations": cmd_locations,
            "env-name": cmd_env, "duration": cmd_duration}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

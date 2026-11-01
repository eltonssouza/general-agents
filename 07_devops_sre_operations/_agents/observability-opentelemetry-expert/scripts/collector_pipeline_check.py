# -*- coding: utf-8 -*-
"""
Skill: collector-pipeline-check
STATIC coherence checker for an OpenTelemetry Collector pipeline YAML configuration,
in the terms of the OTW Refcard p.3 (receivers, processors, exporters, extensions, service.pipelines).
It does NOT validate the real Collector semantics (component names, fields, versions): that is [extrapolation].
No network; no YAML library (minimal indentation-based parser: accepts maps, block lists "- x" and inline lists "[a, b]").
Usage: python -I collector_pipeline_check.py file.yaml   (or '-' for stdin)
Exit codes: 0 no errors, 1 with errors, 2 incorrect usage.
"""
import re
import sys

SECTIONS = ("receivers", "processors", "exporters", "extensions")
BOOK_SIGNALS = ("traces", "metrics", "logs")


def parse(text):
    """Minimal parser: returns a nested dict; leaf lists become list[str]; scalar values stay str/None."""
    lines = []
    for raw in text.splitlines():
        s = raw.split(" #")[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if s.strip():
            lines.append((len(s) - len(s.lstrip(" ")), s.strip()))
    pos = 0

    def block(indent):
        nonlocal pos
        node = {}
        items = None
        while pos < len(lines):
            ind, s = lines[pos]
            if ind < indent:
                break
            if s.startswith("- "):
                items = items if items is not None else []
                items.append(s[2:].strip())
                pos += 1
                continue
            m = re.match(r"([^:]+):\s*(.*)$", s)
            if not m:
                pos += 1
                continue
            key, val = m.group(1).strip(), m.group(2).strip()
            pos += 1
            if val.startswith("["):
                node[key] = [v.strip() for v in val.strip("[]").split(",") if v.strip()]
            elif val:
                node[key] = val
            else:
                if pos < len(lines) and lines[pos][0] > ind:
                    node[key] = block(lines[pos][0])
                else:
                    node[key] = None
        return items if (items is not None and not node) else node

    return block(0)


def base(name):
    return name.split("/")[0]


def main():
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    text = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    cfg = parse(text)
    if not isinstance(cfg, dict):
        print("ERROR: empty or unreadable configuration")
        return 1
    errors, warns = [], []
    defined = {s: set((cfg.get(s) or {}).keys()) if isinstance(cfg.get(s), dict) else set() for s in SECTIONS}
    service = cfg.get("service")
    if not isinstance(service, dict):
        print("ERROR: 'service' section missing (pipelines live under service.pipelines) [from source] (OTW p.3)")
        return 1
    pipelines = service.get("pipelines")
    if not isinstance(pipelines, dict) or not pipelines:
        errors.append("service.pipelines missing or empty [from source] (OTW p.3)")
        pipelines = {}
    used = {s: set() for s in SECTIONS}
    for pname, p in pipelines.items():
        if base(pname) not in BOOK_SIGNALS:
            warns.append(f"pipeline '{pname}': the OTW text covers traces, metrics and logs; other pipeline types are [extrapolation]")
        if not isinstance(p, dict):
            errors.append(f"pipeline '{pname}': no receivers/exporters")
            continue
        for sec in ("receivers", "processors", "exporters"):
            refs = p.get(sec) or []
            if isinstance(refs, str):
                refs = [refs]
            if sec in ("receivers", "exporters") and not refs:
                errors.append(f"pipeline '{pname}': needs at least one item in '{sec}' [inference] (OTW p.3 links receivers and exporters in each pipeline)")
            for r in refs:
                used[sec].add(r)
                if r not in defined[sec]:
                    errors.append(f"pipeline '{pname}': '{r}' in {sec} is not defined in the '{sec}' section [inference]")
            if sec == "processors" and len(refs) > 1:
                warns.append(f"pipeline '{pname}': processor order matters; confirm the sequence {refs} [from source] (OTW p.3)")
    for r in service.get("extensions") or []:
        used["extensions"].add(r)
        if r not in defined["extensions"]:
            errors.append(f"service.extensions: '{r}' is not defined in 'extensions'")
    for sec in SECTIONS:
        for d in sorted(defined[sec] - used[sec]):
            warns.append(f"'{d}' defined in {sec} but not used [inference]")
    for e in errors:
        print("ERROR:", e)
    for w in warns:
        print("WARNING:", w)
    print(f"RESULT: {'FAIL' if errors else 'OK'} ({len(errors)} errors, {len(warns)} warnings). "
          "Static reference check; does not validate real Collector names/fields [extrapolation].")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

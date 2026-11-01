# -*- coding: utf-8 -*-
"""
audit_summary.py - gate G4 (publication): audit totals and matrices computed from ALREADY validated data.

Rules (quality-gates, invariants 1, 3 and 7):
  - vulnerability totals by severity, priority and domain count ONLY status CONFIRMED;
  - POTENTIAL, REQUIRES_VALIDATION and DISCARDED appear in separate tables (discarded = triage);
  - blocks (exit 1) if any CONFIRMED lacks validation.independent_review = true;
  - coverage per specialist = examined / (examined + not_verified), showing the denominators and excluding not-applicable;
    it is never a security score.
Read-only, no network, stdlib.

Usage:
  python -I audit_summary.py validated-findings.json [--results result1.json result2.json ...] [--json]
Exit: 0 publishable, 1 blocked by the gate, 2 usage/read error.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]
PRIORITIES = ["P0", "P1", "P2", "P3"]
OTHER = ["POTENTIAL", "REQUIRES_VALIDATION", "DISCARDED"]


def load(path):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict) and isinstance(doc.get("findings"), list):
        return doc["findings"]
    if isinstance(doc, dict) and "id" in doc and "status" in doc:
        return [doc]  # a standalone finding
    raise ValueError("unrecognized format: expected a list of findings, {'findings': [...]} or a single finding")


def summarize(findings, results):
    blocked = [f.get("id", "?") for f in findings if f.get("status") == "CONFIRMED"
               and (not isinstance(f.get("validation"), dict) or f["validation"].get("independent_review") is not True)]
    conf = [f for f in findings if f.get("status") == "CONFIRMED"]
    out = {
        "confirmados": len(conf),
        "por_severidade": {s: sum(f.get("severity") == s for f in conf) for s in SEVERITIES},
        "por_prioridade": {p: sum(f.get("priority") == p for f in conf) for p in PRIORITIES},
        "por_dominio": {},
        "outros_status": {s: sum(f.get("status") == s for f in findings) for s in OTHER},
        "taxa_confirmacao": None,
        "cobertura": [],
        "bloqueados_sem_validacao": blocked,
    }
    for f in conf:
        out["por_dominio"][f.get("domain", "?")] = out["por_dominio"].get(f.get("domain", "?"), 0) + 1
    reviewed = len(conf) + out["outros_status"]["DISCARDED"] + out["outros_status"]["POTENTIAL"] + out["outros_status"]["REQUIRES_VALIDATION"]
    out["taxa_confirmacao"] = round(len(conf) / reviewed, 3) if reviewed else None
    for r in results:
        c = r.get("coverage", {})
        ex, nv = c.get("examined", 0), c.get("not_verified", 0)
        out["cobertura"].append({"especialista": r.get("specialist_id"), "escopo": r.get("scope_id"), "examinados": ex,
                                 "nao_verificados": nv, "nao_aplicaveis": c.get("not_applicable", 0),
                                 "cobertura": round(ex / (ex + nv), 3) if ex + nv else None})
    return out


def markdown(s):
    lines = ["## Totals (CONFIRMED only)", "", "| Severity | Count |", "|---|---|"]
    lines += ["| %s | %d |" % (k, v) for k, v in s["por_severidade"].items()]
    lines += ["", "| Priority | Count |", "|---|---|"] + ["| %s | %d |" % (k, v) for k, v in s["por_prioridade"].items()]
    lines += ["", "| Domain | Confirmed |", "|---|---|"] + ["| %s | %d |" % (k, v) for k, v in sorted(s["por_dominio"].items())]
    lines += ["", "## Outside the totals", "", "| Status | Count | Where it appears |", "|---|---|---|",
              "| POTENTIAL | %d | suspicions section |" % s["outros_status"]["POTENTIAL"],
              "| REQUIRES_VALIDATION | %d | pending items (runtime, external source, human review) |" % s["outros_status"]["REQUIRES_VALIDATION"],
              "| DISCARDED | %d | triage log (not a vulnerability) |" % s["outros_status"]["DISCARDED"]]
    if s["taxa_confirmacao"] is not None:
        lines += ["", "Confirmation rate: %.1f%% (calibrates false positives; not a security score)." % (100 * s["taxa_confirmacao"])]
    if s["cobertura"]:
        lines += ["", "## Coverage per specialist (examined / (examined + not verified))", "",
                  "| Specialist | Scope | Examined | Not verified | Not applicable | Coverage |", "|---|---|---|---|---|---|"]
        lines += ["| %s | %s | %d | %d | %d | %s |" % (c["especialista"], c["escopo"], c["examinados"], c["nao_verificados"],
                                                    c["nao_aplicaveis"], "-" if c["cobertura"] is None else "%.0f%%" % (100 * c["cobertura"]))
                  for c in s["cobertura"]]
    if s["confirmados"] == 0:
        lines += ["", "No vulnerability confirmed in the examined scope; this does not mean the software is secure."]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("findings", help="validated-findings.json (a list or {'findings': [...]})")
    ap.add_argument("--results", nargs="*", default=[], help="specialists' agent-result.json files, for coverage")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        findings = load(a.findings)
        results = []
        for p in a.results:
            with open(p, encoding="utf-8") as f:
                results.append(json.load(f))
    except (OSError, ValueError, AttributeError) as e:
        print("Error reading: %s" % e)
        return 2
    s = summarize(findings, results)
    if s["bloqueados_sem_validacao"]:
        print("Gate G4 BLOCKED: CONFIRMED without independent review: %s. Return it to the validator." % ", ".join(s["bloqueados_sem_validacao"]))
        return 1
    print(json.dumps(s, ensure_ascii=False, indent=1) if a.json else markdown(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())

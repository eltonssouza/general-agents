# -*- coding: utf-8 -*-
"""
Skill: signal-advisor
Given a question/scenario, indicates which signal(s) (metrics, logs, traces) the DOW/OTW Refcards
associate with the case, with page. Anything not covered is reported as NOT COVERED.
Read-only, no network, deterministic (keyword rules). Accepts Portuguese or English input.
Usage: python -I signal_advisor.py "<scenario>"
"""
import re
import sys
import unicodedata

RULES = [
    ("metrics", ["cpu", "memoria", "memory", "disco", "disk", "rede", "network", "tendencia", "trend",
                 "taxa", "rate", "throughput", "capacidade", "capacity", "threshold", "limite", "alerta", "alert",
                 "uso de recursos", "saturacao", "painel", "dashboard", "grafico",
                 "resource usage", "saturation", "chart", "graph", "alerting"],
     "METRICS: numeric measurements, with tags, good for trends, graphs and alerts",
     "DOW p.4; DOW p.5; OTW p.4"),
    ("logs", ["log", "logs", "evento", "event", "erro detalhado", "stack", "depurar", "debug", "auditoria",
              "o que aconteceu", "mensagem", "registro", "causa raiz", "root cause",
              "what happened", "message", "record"],
     "LOGS: immutable timestamped records, granular view for debugging and root cause",
     "DOW p.4; OTW p.4"),
    ("traces", ["trace", "tracing", "rastre", "span", "requisicao", "request", "latencia", "latency",
                "lento", "slow", "gargalo", "bottleneck", "microservico", "microservice", "entre servicos",
                "dependencia", "dependency", "chamada", "consulta longa", "query lenta",
                "between services", "across services", "call", "long query", "slow query"],
     "TRACES: request lifecycle across services; find the service/operation causing slowness or failure",
     "DOW p.4; OTW p.4"),
]

UNCOVERED = {
    "slo": "SLO/SLI/error budget", "sli": "SLO/SLI/error budget", "error budget": "SLO/SLI/error budget",
    "orcamento de erro": "SLO/SLI/error budget", "golden": "golden signals", "red method": "RED method",
    "use method": "USE method", "cardinalidade": "metric cardinality", "cardinality": "metric cardinality",
    "tail sampling": "tail-based sampling", "tail-based": "tail-based sampling", "baggage": "baggage", "traceparent": "W3C traceparent header",
    "pii": "privacy/PII in telemetry", "ebpf": "eBPF", "profiling": "continuous profiling",
    "rum": "real user monitoring", "custo de observabilidade": "observability FinOps", "observability cost": "observability FinOps",
}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if len(sys.argv) < 2:
        print("Usage: python -I signal_advisor.py \"<scenario>\"")
        return 2
    q = norm(" ".join(sys.argv[1:]))
    hits = []
    for key, kws, text, cite in RULES:
        found = [k for k in kws if k in q]
        if found:
            hits.append((key, text, cite, found))
    print(f"SCENARIO: {' '.join(sys.argv[1:])}")
    if hits:
        for key, text, cite, found in hits:
            print(f"- {text} [from source] ({cite}); triggers: {', '.join(found)}")
        if len(hits) > 1:
            print("- More than one signal matches: the text states that metrics, logs and traces work together (DOW p.4). "
                  "Suggested order [inference]: metric detects, trace locates, log explains.")
        print("- Golden rule [from source] (DOW p.3): monitoring tells you WHEN something is wrong; observability tells you WHY.")
    else:
        print("NOT COVERED: no metrics/logs/traces trigger recognized in the scenario.")
    shown = set()
    for k, v in UNCOVERED.items():
        if re.search(r'(?<![a-z])' + re.escape(k) + r'(?![a-z])', q):
            if v in shown:
                continue
            shown.add(v)
            print(f"NOT COVERED: '{v}' is not addressed by the Refcards; answer only as [extrapolation].")
    return 0


if __name__ == "__main__":
    sys.exit(main())

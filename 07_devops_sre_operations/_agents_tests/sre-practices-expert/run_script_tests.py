# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases (CT-09 to CT-15, CT-23, R1-xx, R2-xx and R3-xx) against the scripts
and checks that the output contains what the book says, including the THREE-LEVEL lookup (COVERED / POINTER ONLY / NOT COVERED,
round 2). Usage (from the package root):
  python -I tests/run_script_tests.py [--text <Google-SRE-Book.txt>]
Offline. Exit code 0 if all pass.

Note on languages: the script labels and messages, scripts/sre_index.json and references/*.md are English. Several expected
substrings are verbatim data from those files (ASCII-folded by the lookup output) and must be updated together with them.
Portuguese user input (queries, postmortem drafts) is still recognized and tested (pt->en synonyms, Portuguese aliases).
"""
import argparse
import io
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True  # the tests import the scripts by path; do not leave __pycache__ in the package

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")


def run(script, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", os.path.join(S, script)] + list(args),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


CASES = []


def case(cid, desc, script, args, must, rc=0, must_not=()):
    CASES.append((cid, desc, script, args, must, rc, must_not))


case("CT-09", "downtime 99.95%", "error_budget_calc.py", ["downtime", "99.95"],
     ["0.05%", "quarter    1.08 hours", "month      21.6 min", "SRE p.25"])
case("CT-10", "budget consumption", "error_budget_calc.py", ["consume", "--slo", "99.999", "--failure-rate", "0.0002"],
     ["consumes 20% of the budget", "does NOT cover burn rate"])
case("CT-11", "allowed failures", "error_budget_calc.py",
     ["requests", "--slo", "99.99", "--total", "2500000", "--failed", "300"],
     ["up to 250 failures", "120%", "EXCEEDED"])
case("CT-11b", "Appendix A table", "error_budget_calc.py", ["table"], ["table reproduced (48 cells)"])
case("CT-12", "provisioning", "sre_math.py", ["provision", "--peak", "3470", "--per-task", "100"],
     ["minimum 35 tasks", "N+2: 37 tasks"])
case("CT-13", "two-site on-call", "sre_math.py", ["oncall", "--sites", "2"],
     ["6 per site", "at most 2 incidents per shift", "<=25%"])
case("CT-14", "retry amplification", "sre_math.py", ["retry-amp", "--tries", "4", "--layers", "3"],
     ["= 64 attempts", "SRE p.192"])
case("CT-14b", "bimodal latency", "sre_math.py", ["bimodal"], ["19.6%", "80.4%"])
case("CT-14c", "quorum", "sre_math.py", ["quorum", "--replicas", "5"], ["majority quorum = 3", "40%"])
case("CT-15", "postmortem template", "postmortem_tool.py", ["template", "--lang", "en"],
     ["## Root Causes", "## Lessons Learned", "### Where we got lucky", "## Supporting information"])
case("CT-15b", "checklist", "postmortem_tool.py", ["checklist"], ["data loss", "SRE p.127"])
case("CT-23", "out of scope", "sre_lookup.py", ["kubernetes", "hpa"], ["NOT COVERED"], rc=1)
case("CT-01b", "lookup error budget", "sre_lookup.py", ["error budget"],
     ["SRE p.25; p.330", "burn rate"])
case("R1-01", "burn rate: outside the book (round 1)", "sre_lookup.py", ["burn rate"],
     ["NOT COVERED", "NOT IN THE SOURCE", "Workbook"], rc=1, must_not=["TOPIC:", "RULES FROM THE BOOK"])
case("R1-02", "circuit breaker: outside the book", "sre_lookup.py", ["circuit", "breaker"],
     ["NOT COVERED", "NOT IN THE SOURCE"], rc=1, must_not=["TOPIC:"])
case("R1-03", "SEV1: outside the book", "sre_lookup.py", ["SEV1"], ["NOT COVERED", "NOT IN THE SOURCE"], rc=1)
case("R1-04", "error budget is not flagged as outside the book", "sre_lookup.py", ["error budget"],
     ["TOPIC:"], must_not=["NOT IN THE SOURCE (SRE 2016)"])
case("R1-05", "cascade: numeric example and 1%", "sre_lookup.py", ["--topic", "cascading-failures"],
     ["10,000 QPS", "11,000 QPS", "9,000 QPS", "1,000 QPS", "SRE p.188", "~1% of the traffic", "SRE p.198"])
case("R1-06", "SLA: role of the SRE", "sre_lookup.py", ["--topic", "sli-slo-sla"],
     ["does not build SLAs", "SRE p.45", "SRE p.49", "SRE p.50"])
case("CT-04b", "lookup golden signals", "sre_lookup.py", ["--topic", "monitoramento"], ["SRE p.57-58"])

# ---------------------------------------------------------------- round 2: three-level lookup
# COVERED (rc 0): terms the book has that previously produced 'the book does not cover this'
case("R2-01", "Shakespeare: COVERED with the App. D narrative", "sre_lookup.py", ["Shakespeare"],
     ["LEVEL: COVERED", "88x", "SRE p.334", "USA-2", "66 min", "89 min"], must_not=["NOT COVERED", "NOT IN THE SOURCE (SRE 2016)"])
case("R2-02", "Sonnet: COVERED", "sre_lookup.py", ["Sonnet"], ["LEVEL: COVERED", "incidente-shakespeare-ap-d"], must_not=["NOT COVERED"])
case("R2-03", "sacrificial: COVERED", "sre_lookup.py", ["sacrificial"],
     ["LEVEL: COVERED", "sacrificial cluster", "15:23"], must_not=["NOT COVERED"])
case("R2-04", "88x: COVERED", "sre_lookup.py", ["88x"], ["LEVEL: COVERED", "14:53", "SRE p.335"], must_not=["NOT COVERED"])
case("R2-05", "Ads MySQL failover: Decider", "sre_lookup.py", ["Ads", "MySQL", "failover"],
     ["LEVEL: COVERED", "Decider", "30-90", "99% uptime", "SRE p.66-67", "JDBC"], must_not=["NOT COVERED"])
case("R2-06", "etcd: COVERED as only named (p.205)", "sre_lookup.py", ["etcd"],
     ["LEVEL: COVERED", "SRE p.205", "(only named)", "installation, flags, TLS"], must_not=["NOT COVERED"])
case("R2-07", "Knight Capital: amount from the book, without falling into consensus", "sre_lookup.py", ["Knight", "Capital"],
     ["LEVEL: COVERED", "440 million", "SRE p.321", "a few hours", "duration of the incident in minutes"],
     must_not=["NOT COVERED", "Distributed consensus"])
case("R2-08", "Bazel: only named, no migration plan", "sre_lookup.py", ["Bazel"],
     ["LEVEL: COVERED", "note 37", "SRE p.140", "Maven -> Bazel migration plan"], must_not=["NOT COVERED"])
case("R2-09", "Borgmon: 24 B, 17 GB, 12 h, TSDB, notes 50 and 52", "sre_lookup.py", ["Borgmon", "24", "bytes"],
     ["LEVEL: COVERED", "24 bytes", "17 GB", "TSDB", "magic number", "Note 52"], must_not=["NOT COVERED"])
case("R2-10", "GRE: current solution with 24 bytes", "sre_lookup.py", ["GRE"],
     ["LEVEL: COVERED", "GRE encapsulation", "24 bytes", "SRE p.162", "larger MTU"], must_not=["NOT COVERED"])
case("R2-11", "Least-Loaded: 2x CPU and as bad as RR", "sre_lookup.py", ["Least-Loaded"],
     ["LEVEL: COVERED", "as bad as", "SRE p.173", "Two limitations", "63%"], must_not=["NOT COVERED"])
case("R2-12", "Change-Induced: the luck of the push (p.118)", "sre_lookup.py", ["Change-Induced"],
     ["LEVEL: COVERED", "what was luck", "following real-time channels", "SRE p.118", "do not mix them up"], must_not=["NOT COVERED"])
case("R2-13", "Portuguese input: 'balanceamento de carga' (load balancing) is still COVERED", "sre_lookup.py", ["balanceamento", "de", "carga"],
     ["LEVEL: COVERED", "load-balancing"], must_not=["NOT COVERED"])
# POINTER ONLY (rc 3): the book has the term, the package does not summarize it
case("R2-14", "RE2: COVERED since round 4 (note 68, p.115: no backtracking vs exponential PCRE)", "sre_lookup.py", ["RE2"],
     ["LEVEL: COVERED", "troubleshooting", "PCRE", "p.115"], must_not=["NOT COVERED"])
case("R2-14b", "Photon: COVERED because the consensus summary body treats it (p.212-213)", "sre_lookup.py", ["Photon"],
     ["LEVEL: COVERED", "Photon", "consenso-cron-e-pipelines.md"], must_not=["NOT COVERED"])
case("R2-15", "Dagger: POINTER ONLY", "sre_lookup.py", ["Dagger"], ["LEVEL: POINTER ONLY", "137", "147"], rc=3, must_not=["TOPIC:"])
case("R2-16", "Kubernetes: POINTER ONLY (notes)", "sre_lookup.py", ["Kubernetes"],
     ["LEVEL: POINTER ONLY", "35"], rc=3, must_not=["TOPIC:", "NOT IN THE SOURCE (SRE 2016)"])
case("R2-17", "Mencius: COVERED by the summary body (rotating leadership, p.204-205, 213-218)", "sre_lookup.py", ["Mencius"],
     ["LEVEL: COVERED", "Mencius"], must_not=["NOT COVERED"])
case("R2-17b", "pointer does not assert absence (Lustre only mentioned on p.30: POINTER ONLY; Jupiter got a summary in round 6)", "sre_lookup.py", ["Lustre"],
     ["LEVEL: POINTER ONLY", "30"], rc=3, must_not=["The SRE book (2016) does not cover", "LEVEL: COVERED"])
# true NOT COVERED (rc 1)
case("R2-18", "nonexistent term: NOT COVERED by absence from the index", "sre_lookup.py", ["xyzzyfoo"],
     ["NOT COVERED", "Not found", "does NOT prove", "term index"], rc=1, must_not=["POINTER ONLY", "TOPIC:", "the book does not cover the topic"])
case("R2-19", "curated list: Grafana", "sre_lookup.py", ["Grafana"], ["NOT COVERED", "NOT IN THE SOURCE"], rc=1)
case("R2-20", "pom.xml: the book has no 'pom'; only the package limit note (not COVERED)", "sre_lookup.py", ["pom.xml"],
     ["NOT COVERED", "LIMIT NOTES", "migration plan"], rc=1, must_not=["LEVEL: COVERED"])
case("R2-20b", "curated list: Datadog", "sre_lookup.py", ["Datadog"], ["NOT COVERED", "NOT IN THE SOURCE"], rc=1)
case("R2-21", "mixed: pointer + absent", "sre_lookup.py", ["Dagger", "xyzzyfoo"],
     ["NOT COVERED", "Partial POINTER", "137"], rc=1)
case("R2-22", "mixed: kubernetes + HPA => curated", "sre_lookup.py", ["kubernetes", "HPA"], ["NOT COVERED", "NOT IN THE SOURCE"], rc=1)
case("R2-23", "--pages etcd", "sre_lookup.py", ["--pages", "etcd"], ["etcd", "205"])
case("R2-24", "--pages absent term", "sre_lookup.py", ["--pages", "xyzzyfoo"], ["not found", "does NOT prove"], rc=1)
case("R2-25", "--topic of the incident (App. D)", "sre_lookup.py", ["--topic", "incidente-shakespeare-ap-d"],
     ["1.21 billion", "Traffic return", "1%", "10%", "30%", "50%", "exit criterion", "SRE p.335"])
case("R2-26", "--topic decider", "sre_lookup.py", ["--topic", "decider-ads-mysql"], ["60x to 180x", "95%", "SRE p.67"])
case("R2-27b", "empty data: Fail Sanely in App. B (DNS 2005, slash 2009)", "sre_lookup.py", ["dados", "vazios"],
     ["LEVEL: COVERED", "NXDOMAIN", "SRE p.329", "single slash"], must_not=["NOT COVERED"])
case("R2-28", "borgmon-ram: the book's example (1 million series, 12 h, 24 B)", "sre_math.py", ["borgmon-ram", "--series", "1000000"],
     ["720 points", "17.28 GB", "16.09 GiB", "SRE p.90-91", "magic number"])
case("R2-29", "borgmon-ram: 2.5 million series for 24 h = 86.4 GB", "sre_math.py", ["borgmon-ram", "--series", "2500000", "--hours", "24"],
     ["1440 points", "86.4 GB"])
case("R2-30", "duration: App. D outage = 66 min", "sre_math.py", ["duration", "--start", "14:54", "--end", "16:00"], ["66 minutes", "SRE p.335"])
case("R2-31", "duration: App. D incident = 89 min", "sre_math.py", ["duration", "--start", "15:01", "--end", "16:30"], ["89 minutes"])
case("R2-27", "--list includes the new topics", "sre_lookup.py", ["--list"],
     ["incidente-shakespeare-ap-d", "borgmon-dimensionamento", "balanceamento-vip-gre", "knight-capital", "etcd-zookeeper-consul"])


# ---------------------------------------------------------------- round 4 (after the round 3 blind test): coverage, not the 14 cases
case("R3-01", "root cause: definition on p.55 (previously COVERED with the wrong topic)", "sre_lookup.py", ["root", "cause"],
     ["LEVEL: COVERED", "definicoes-cap6-p55", "several root causes", "each must be repaired", "SRE p.55"], must_not=["NOT COVERED"])
case("R3-02", "causa raiz (Portuguese input): COVERED, not NOT COVERED", "sre_lookup.py", ["causa", "raiz"],
     ["LEVEL: COVERED", "definicoes-cap6-p55", "SRE p.55"], must_not=["NOT COVERED"])
case("R3-03", "push: definition on p.55, without falling into Blaze/Bazel", "sre_lookup.py", ["push"],
     ["LEVEL: COVERED", "definicoes-cap6-p55", "any change to the running software"], must_not=["bazel-blaze", "NOT COVERED"])
case("R3-04", "alert: tickets, email alerts and pages", "sre_lookup.py", ["--topic", "definicoes-cap6-p55"],
     ["email alerts", "pages", "Node and machine", "software that crashed is one of the root causes"])
case("R3-05", "paging events: the two questions (p.296)", "sre_lookup.py", ["paging", "events"],
     ["LEVEL: COVERED", "reuniao-de-producao", "should this alert have paged the way it did", "should it have paged at all", "remove the non-actionable pages", "SRE p.296"],
     must_not=["NOT COVERED", "POINTER ONLY"])
case("R3-06", "nonpaging events: three handlings (p.297)", "sre_lookup.py", ["nonpaging", "events"],
     ["LEVEL: COVERED", "fix the monitoring so that it starts paging", "reactive operational work", "remove the alert", "SRE p.297"],
     must_not=["POINTER ONLY"])
case("R3-07", "example minutes (App. F, p.339)", "sre_lookup.py", ["--topic", "reuniao-de-producao"],
     ["AnnotationConsistencyTooEventual", "60 s to 180 s", "Nonpaging Events: None", "SRE p.339", "push freeze for 1 month"])
case("R3-08", "deadline: the p.193 rules appear in COVERED", "sre_lookup.py", ["deadline"],
     ["LEVEL: COVERED", "a few hundred ms", "cap", "non-critical", "always fail", "SRE p.193"])
case("R3-09", "outgoing deadline", "sre_lookup.py", ["outgoing", "deadline"],
     ["LEVEL: COVERED", "outgoing deadline", "checkpoint"], must_not=["POINTER ONLY"])
case("R3-10", "bursty queue: three variables (p.189)", "sre_lookup.py", ["queue", "size", "bursty"],
     ["LEVEL: COVERED", "threads in use", "processing time of each request", "size and frequency of the bursts", "SRE p.189"],
     must_not=["NOT COVERED"])
case("R3-11", "'fila rajadas' (Portuguese input) also finds the rule", "sre_lookup.py", ["fila", "rajadas"],
     ["LEVEL: COVERED", "queueless", "SRE p.189"])
case("R3-12", "Moire: also in continuous pipelines (p.236)", "sre_lookup.py", ["Moire"],
     ["LEVEL: COVERED", "continuous pipelines", "less common", "thundering herd", "SRE p.236"])
case("R3-13", "feature flag (singular): 6 requirements (p.268)", "sre_lookup.py", ["feature", "flag"],
     ["LEVEL: COVERED", "requirement 1", "requirement 6", "between 1 and 10 percent", "revert each change independently and immediately", "SRE p.268"],
     must_not=["POINTER ONLY"])
case("R3-14", "canary: a few machines in a datacenter (p.268), not just traffic", "sre_lookup.py", ["canary"],
     ["LEVEL: COVERED", "a few machines of a datacenter", "rolls back automatically", "0.1% of traffic", "does not fix a percentage of machines"])
case("R3-15", "cherry pick: mainline -> branch direction and re-test (p.78)", "sre_lookup.py", ["--topic", "release"],
     ["mainline -> branch", "does not exist on the mainline", "unique hash and signed", "does not state the hash algorithm", "SRE p.78"])
case("R3-16", "MPM hash: COVERED by release, with the algorithm caveat", "sre_lookup.py", ["MPM", "hash"],
     ["LEVEL: COVERED", "hash algorithm"], must_not=["LEVEL: POINTER ONLY"])
case("R3-17", "ticket scrub: silence until the fix date and the book's reason", "sre_lookup.py", ["scrub"],
     ["LEVEL: COVERED", "silence the interruptions until the expected date of the fix", "distorts the measure of how manageable the queue is", "SRE p.288"])
case("R3-18", "other industries: one year of design x launch and iterate; CAPA (p.319)", "sre_lookup.py", ["--topic", "outras-industrias"],
     ["three weeks of code", "launch and iterate", "CAPA", "published among the SRE teams", "SRE p.319"])
case("R3-19", "unmanaged incident and roles (Ch. 14)", "sre_lookup.py", ["--topic", "incidentes"],
     ["freelancing", "orders dinner", "Ops lead is the only group that modifies the system", "you are now the incident commander", "SRE p.124"])
case("R3-20", "postmortem: TGIF, Morgue, blameless (Ch. 15)", "sre_lookup.py", ["--topic", "postmortem"],
     ["TGIF", "Morgue", "2 peer bonuses", "healthcare and aviation", "SRE p.129"])
case("R3-21", "on-call: median 0, confirmation bias, fall-through secondary", "sre_lookup.py", ["--topic", "on-call"],
     ["likely median of 0", "confirmation bias", "fall-through", "SRE p.101"])
case("R3-22", "troubleshooting: App Engine and negative results", "sre_lookup.py", ["--topic", "troubleshooting"],
     ["thousands of objects in half an hour", "~800 of 8,000 connections", "PCRE", "SRE p.112-114"])
case("R3-23", "consensus: quorum leases, dueling proposers, monitoring", "sre_lookup.py", ["--topic", "consenso"],
     ["dueling proposers", "quorum leases", "50% higher", "leader changes", "SRE p.222-223"])
case("R3-24", "integrity: global deletion-rate alert (note 133)", "sre_lookup.py", ["--topic", "integridade-dados"],
     ["10x the 95th percentile", "Blobstore", "SRE p.260"])
case("R3-25", "YouTube: COVERED by the summary body (2006 target, p.39), not by the keyword", "sre_lookup.py", ["YouTube"],
     ["LEVEL: COVERED", "2006", "pages 39"], must_not=["NOT COVERED"])
case("R3-26", "consistent COVERED: lookup --check", "sre_lookup.py", ["--check"],
     ["0 with untreated keyword"])
case("R3-27", "'2x the average' rule outside the book: listed in the topic's not_in_book", "sre_lookup.py", ["--topic", "cascading-failures"],
     ["'2x the average' rule for deadlines", "SRE p.193", "SRE p.189"])
case("R3-28", "--list includes the round 4 topics", "sre_lookup.py", ["--list"],
     ["definicoes-cap6-p55", "reuniao-de-producao", "interrupts-tickets-scrub", "canario-feature-flags"])
case("R3-29", "ITIL outside the book: not covered by absence", "sre_lookup.py", ["ITIL"],
     ["NOT COVERED"], rc=1, must_not=["TOPIC:"])

# ---------------------------------------------------------------- round 5 (after the round 4 blind test): content p.298/308/310/176/340/95 and lookup by content
case("R4-01", "roles: TL, SRM, PM; manager: performance and catchall; fluid x defined (p.298)", "sre_lookup.py", ["tech", "lead", "manager"],
     ["LEVEL: COVERED", "catchall", "performance management", "more mature", "communicating more", "298"], must_not=["NOT COVERED"])
case("R4-02", "specialization (Portuguese input 'especializacao'): silos and charter (p.298)", "sre_lookup.py", ["especializacao"],
     ["LEVEL: COVERED", "silos", "charter", "of what it does not support", "298"], must_not=["NOT COVERED", "POINTER ONLY"])
case("R4-03", "diversity (Portuguese input 'diversidade') (p.298)", "sre_lookup.py", ["diversidade"],
     ["LEVEL: COVERED", "diverse teams", "cognitive biases", "298"], must_not=["POINTER ONLY"])
case("R4-04", "PRR: objectives (Portuguese input 'objetivos') (p.308)", "sre_lookup.py", ["PRR", "objetivos"],
     ["LEVEL: COVERED", "operational readiness standards", "minimize the number and severity of incidents", "308"], must_not=["NOT COVERED"])
case("R4-05", "PRR: Simple PRR limitations (Portuguese input 'limitacoes') (p.310)", "sre_lookup.py", ["PRR", "limitacoes"],
     ["LEVEL: COVERED", "communication overhead", "already at scale", "310"], must_not=["NOT COVERED"])
case("R4-06", "Early Engagement: candidates (Portuguese input 'candidatos') (p.310)", "sre_lookup.py", ["Early", "Engagement", "candidatos"],
     ["LEVEL: COVERED", "significant rewrite", "asked for advice", "Design", "310"], must_not=["NOT COVERED"])
case("R4-07", "global overload: errors only for misbehaving clients (p.176)", "sre_lookup.py", ["misbehaving"],
     ["LEVEL: COVERED", "only to the misbehaving clients", "176"], must_not=["NOT COVERED", "POINTER ONLY"])
case("R4-08", "minutes: OK/BAD in Key Service Metrics (p.340)", "sre_lookup.py", ["Key", "Service", "Metrics"],
     ["LEVEL: COVERED", "OK", "BAD", "86.95%", "88 ms", "340"], must_not=["NOT COVERED"])
case("R4-09", "minutes: Resources (p.340)", "sre_lookup.py", ["Resources", "sonnet++", "emprestados"],
     ["LEVEL: COVERED", "60% CPU", "75% RAM", "44% disk", "40%, 70%, 40%", "340"], must_not=["NOT COVERED"])
case("R4-10", "Alertmanager described on p.95 (old answer key was wrong): inhibits, deduplicates, routes", "sre_lookup.py", ["Alertmanager"],
     ["LEVEL: COVERED", "deduplica", "fan-in", "95"], must_not=["NOT COVERED", "POINTER ONLY"])
case("R4-11", "Doorman: only note 106 (p.183), no algorithm", "sre_lookup.py", ["Doorman"],
     ["LEVEL: COVERED", "note 106", "183", "describes no algorithm"], must_not=["NOT COVERED"])
case("R4-12", "Peer Bonus: the amount is not given (note 82, p.129)", "sre_lookup.py", ["peer", "bonus"],
     ["LEVEL: COVERED", "129"], must_not=["NOT COVERED"])
case("R4-13", "retry: how to recognize it in an emergency (Portuguese input 'sintoma') (p.192)", "sre_lookup.py", ["retry", "sintoma"],
     ["LEVEL: COVERED", "aggravating cause", "code push", "192"], must_not=["NOT COVERED"])
case("R4-14", "GC death spiral: restart only after finding the origin (Portuguese input 'reiniciar') (p.198)", "sre_lookup.py", ["GC", "death", "spiral", "reiniciar"],
     ["LEVEL: COVERED", "198"], must_not=["NOT COVERED"])
case("R4-15", "LCE: incentive and when it pays off (Portuguese input 'incentivo') (p.262, 272)", "sre_lookup.py", ["LCE", "incentivo"],
     ["LEVEL: COVERED", "another incentive structure", "262"], must_not=["NOT COVERED"])
# negatives: a term only in a title/file name/pointer list/limit note does NOT become COVERED
case("R4-N1", "section title only (Tenets): POINTER ONLY, not COVERED", "sre_lookup.py", ["tenets"],
     ["LEVEL: POINTER ONLY", "pages"], rc=3, must_not=["LEVEL: COVERED", "SUMMARIES IN THE REFERENCES"])
case("R4-N2", "section title only (Embracing): POINTER ONLY", "sre_lookup.py", ["embracing"],
     ["LEVEL: POINTER ONLY"], rc=3, must_not=["LEVEL: COVERED"])
case("R4-N3", "INDEX pointer list only (Dagger): POINTER ONLY", "sre_lookup.py", ["Dagger"],
     ["LEVEL: POINTER ONLY", "137"], rc=3, must_not=["LEVEL: COVERED", "SUMMARIES IN THE REFERENCES"])
case("R4-N4", "limit note only (Kubernetes): POINTER ONLY and shows the note, without COVERED", "sre_lookup.py", ["Kubernetes"],
     ["LEVEL: POINTER ONLY", "LIMIT NOTES", "Kubernetes in note 10"], rc=3, must_not=["LEVEL: COVERED", "SUMMARIES IN THE REFERENCES"])
case("R4-N5", "file name does not count: 'gestao-treinamento' as a file word", "sre_lookup.py", ["xyzzyfoo", "gestao-treinamento-interrupts"],
     ["NOT COVERED"], rc=1, must_not=["LEVEL: COVERED"])
case("R4-N6", "curated term outside the book stays NOT COVERED even when cited in a summary", "sre_lookup.py", ["token", "bucket"],
     ["NOT COVERED", "NOT IN THE SOURCE"], rc=1, must_not=["LEVEL: COVERED"])
case("R4-N7", "generic term + absent term does not become COVERED (kubernetes service)", "sre_lookup.py", ["kubernetes", "service"],
     ["LEVEL: POINTER ONLY"], rc=3, must_not=["LEVEL: COVERED"])
case("R5-01", "lookup 'slack' becomes COVERED only through p.131 (no slack capacity noise)", "sre_lookup.py", ["slack"],
     ["LEVEL: COVERED", "pages 131 (PDF)", "Outalator"], rc=0, must_not=["41, 131, 196", "POINTER ONLY"])
case("R5-02", "typo tags accepted (cause:netwrok, problem-went-away; no predetermined list)", "sre_lookup.py", ["netwrok"],
     ["LEVEL: COVERED", "131, 133", "predetermined list"], rc=0)
case("R5-03", "dummy escalator: technical audit, not legal (p.133)", "sre_lookup.py", ["dummy", "escalator"],
     ["LEVEL: COVERED", "technical, not legal", "133"], rc=0)
case("R5-04", "cold cache: latency cache x capacity cache, memcache, increase the load slowly (p.194-195)", "sre_lookup.py", ["memcache"],
     ["LEVEL: COVERED", "memcache", "increase the load slowly", "194, 195"], rc=0)
case("R5-05", "MTTR is the most relevant metric (p.26)", "sre_lookup.py", ["MTTR"],
     ["LEVEL: COVERED", "most relevant metric", "26"], rc=0)
case("R5-06", "email as a channel: 'fundamentally flawed' on p.25-26 and p.330, not p.95 (Portuguese input)", "sre_lookup.py", ["fundamentalmente", "falho"],
     ["LEVEL: COVERED", "25, 26, 330", "fundamentally flawed"], rc=0, must_not=["95, 330", "26, 95"])
case("R5-07", "Appendix E: items (N+2, monitor the monitoring, 10x growth, SOP, Mondays or Fridays)", "sre_lookup.py", ["Mondays", "Fridays"],
     ["LEVEL: COVERED", "SOP", "337, 338"], rc=0)
case("R5-08", "confirmation bias: illustrative example, not a recommendation for external cause (p.101-102)", "sre_lookup.py", ["confirmation", "bias"],
     ["LEVEL: COVERED", "illustrative example", "heuristics under stress"], rc=0)
case("R5-09", "Wheel of Misfortune + DiRT on p.103 (p.331 only gives the irony of the lack of practice)", "sre_lookup.py", ["DiRT", "Wheel"],
     ["LEVEL: COVERED", "103", "irony"], rc=0)
case("R5-10", "App Engine note 75 on p.115", "sre_lookup.py", ["whitelist"],
     ["LEVEL: COVERED", "112, 113, 114, 115", "Note 75"], rc=0)



# ---------------------------------------------------------------- round 6 (after the round 5 blind test): content of p.33/35/68-70/80-81/100-101/141/143-144/147/150-151/281-286/293/328
case("R6-01", "flow: COVERED with cognitive flow (p.285-286) and a polysemy alert (flow control p.164-166)", "sre_lookup.py", ["flow"],
     ["LEVEL: COVERED", "cognitive flow", "ALERT: 'flow' has more than one sense", "164-166", "285-286"], rc=0)
case("R6-02", "cognitive flow: low and high skill, human cost, variable balance (p.285-286)", "sre_lookup.py", ["--topic", "interrupts-fatores-flow"],
     ["low skill and low difficulty", "high skill and high difficulty", "human cost", "varies by engineer", "SRE p.285", "SRE p.286"])
case("R6-03", "shadow: COVERED with checklist, business hours, the newcomer is not the on-caller, reverse shadow (p.281-282)", "sre_lookup.py", ["shadow"],
     ["LEVEL: COVERED", "business hours", "on-caller", "reverse shadow", "ALERT: 'shadow'"], rc=0)
case("R6-04", "shadow: topic with co-authorship, reverse shadow without modifying state and notes 136-137 (p.281-283)", "sre_lookup.py", ["--topic", "shadow-on-call-cap28"],
     ["co-author", "without modifying state", "not the designated on-caller", "136 proactive", "137 reactive", "SRE p.281", "SRE p.282", "SRE p.283"])
case("R6-05", "postmortem co-authorship by the newcomer (Portuguese input 'coautoria') (p.282)", "sre_lookup.py", ["coautoria"],
     ["LEVEL: COVERED", "co-author", "282"], rc=0, must_not=["NOT COVERED"])
case("R6-06", "DNS: COVERED with the Prodtest example (Machine Database, p.70) and a polysemy alert", "sre_lookup.py", ["DNS"],
     ["LEVEL: COVERED", "Machine Database", "ALERT: 'dns'", "68-71"], rc=0)
case("R6-07", "Prodtest DNS: function names, 15 min, notifies, figures 7-1 and 7-2 (p.68-71)", "sre_lookup.py", ["--topic", "prodtest-dns-p70"],
     ["TestDnsMonitoringConfigExists", "FixDnsMonitoringCreateConfig", "FixDnsMonitoringPushConfig", "15 minutes", "notifies", "Machine Database", "SRE p.68", "SRE p.70"])
case("R6-08", "vocabulary: 'supervisao' (Portuguese input) finds 'unattended' (p.144)", "sre_lookup.py", ["supervisão"],
     ["LEVEL: COVERED", "unattended", "144"], rc=0, must_not=["NOT COVERED"])
case("R6-09", "vocabulary: 'unsupervised' (English input) finds 'unattended' (p.144)", "sre_lookup.py", ["unsupervised"],
     ["LEVEL: COVERED", "unattended", "144"], rc=0, must_not=["NOT COVERED"])
case("R6-10", "unattended: COVERED, MTBF suffers with more releases and a poorly tested tool reduces confidence (p.144)", "sre_lookup.py", ["unattended"],
     ["LEVEL: COVERED", "MTBF worse", "reduces confidence", "144"], rc=0, must_not=["POINTER ONLY"])
case("R6-11", "MTBF: more releases make MTBF worse (p.144), not better", "sre_lookup.py", ["--topic", "producao-sem-supervisao-p144"],
     ["more versions makes the MTBF worse", "no matter how much testing", "SRE p.144", "SRE p.143", "NOT IN THE SOURCE", "more released versions increase the MTBF"])
case("R6-12", "configuration: four models with pros and cons, skew, much_ado, note 36 (p.80-81)", "sre_lookup.py", ["--topic", "config-modelos-p80"],
     ["skew", "limits flexibility", "much_ado", "External store", "unified monolithic", "strict code review", "anti-pattern", "SRE p.80"])
case("R6-13", "mainline model skew (p.80): COVERED", "sre_lookup.py", ["skew"],
     ["LEVEL: COVERED", "mainline", "80"], rc=0)
case("R6-14", "note 36: unified monolithic repository (text on p.81): COVERED (Portuguese input 'monolitico')", "sre_lookup.py", ["monolitico"],
     ["LEVEL: COVERED", "unified monolithic", "81"], rc=0)
case("R6-15", "on-call compensation: time off or capped money, role of the cap (Portuguese input 'compensação') (p.101)", "sre_lookup.py", ["compensação"],
     ["LEVEL: COVERED", "cap", "101"], rc=0, must_not=["NOT COVERED"])
case("R6-16", "compensation: the cap percentage is NOT in the book (explicit limit)", "sre_lookup.py", ["--topic", "compensacao-oncall-p101"],
     ["time-off-in-lieu", "NOT IN THE SOURCE", "the percentage of salary used as the cap", "legal or HR", "SRE p.101"])
case("R6-17", "aggregate metric x duration (Portuguese input 'agregada') (p.328)", "sre_lookup.py", ["agregada"],
     ["LEVEL: COVERED", "aggregate unavailability", "328"], rc=0)
case("R6-18", "Ch. 2: Thrift is only a comparison to protobufs; RPC is Stubby; XML not JSON (p.32-33)", "sre_lookup.py", ["--topic", "cap2-ambiente-producao"],
     ["Apache's Thrift", "XML, not JSON", "Stubby", "repository", "Android and Chrome", "reviewed before being submitted", "that Google uses Apache Thrift for RPC", "SRE p.33"])
case("R6-19", "Ch. 2: Kubernetes stays POINTER ONLY and note 10 appears as a limit note (p.35)", "sre_lookup.py", ["Kubernetes"],
     ["LEVEL: POINTER ONLY", "LIMIT NOTES", "descendant of Borg"], rc=3, must_not=["LEVEL: COVERED", "SUMMARIES IN THE REFERENCES"])
case("R6-20", "Jupiter got a summary in Ch. 2 (1.3 Pbps, p.28)", "sre_lookup.py", ["Jupiter"],
     ["LEVEL: COVERED", "1.3 Pbps", "28"], rc=0)
case("R6-21", "savings: the book cites cost savings, without a percentage (p.150-151)", "sre_lookup.py", ["--topic", "rollout-nota-89"],
     ["cost savings", "no percentage figure", "savings percentage between level 1 and level 3", "0.1%", "SRE p.147", "SRE p.150"])
case("R6-22", "savings (Portuguese input 'economia') finds cost savings and the absence of a percentage", "sre_lookup.py", ["economia"],
     ["LEVEL: COVERED", "percentage", "150"], rc=0)
case("R6-23", "note 89: 0.1% -> 1% -> 10% -> 100% every 24 h (Portuguese input 'nota') (p.147)", "sre_lookup.py", ["nota", "89"],
     ["LEVEL: COVERED", "0.1%", "147"], rc=0, must_not=["NOT COVERED"])
case("R6-24", "--list includes the round 6 topics", "sre_lookup.py", ["--list"],
     ["shadow-on-call-cap28", "interrupts-fatores-flow", "prodtest-dns-p70", "config-modelos-p80", "producao-sem-supervisao-p144",
      "disponibilidade-agregada-p328", "compensacao-oncall-p101", "cap2-ambiente-producao", "rollout-nota-89"])
case("R6-25", "guiding questions (Ch. 30): example and counterexample (p.293)", "sre_lookup.py", ["Frobnitzer"],
     ["LEVEL: COVERED", "293"], rc=0)
case("R6-N1", "polysemy: a term without several senses gets no alert (error budget)", "sre_lookup.py", ["error budget"],
     ["SRE p.25; p.330"], must_not=["ALERT:"])
case("R6-N2", "Argo stays NOT COVERED (not in the book)", "sre_lookup.py", ["argo"],
     ["NOT COVERED"], rc=1, must_not=["LEVEL: COVERED"])
case("R6-N3", "overtime/overnight stay NOT COVERED", "sre_lookup.py", ["overnight"],
     ["NOT COVERED"], rc=1, must_not=["LEVEL: COVERED"])
case("R6-N4", "Dagger stays POINTER ONLY (only a link in note 88, p.147)", "sre_lookup.py", ["Dagger"],
     ["LEVEL: POINTER ONLY"], rc=3, must_not=["LEVEL: COVERED"])
# ---- round 7 (fix after the round 7 blind test): Part III intro, notes 17/18, interpreted config p.145, Ch. 34
case("R7-01", "Dickerson/healthcare.gov: origin of the hierarchy (p.85) is no longer a pointer", "sre_lookup.py", ["Dickerson"],
     ["LEVEL: COVERED", "85"], rc=0, must_not=["POINTER ONLY"])
case("R7-02", "Part III introduction topic", "sre_lookup.py", ["--topic", "parte3-hierarquia-intro"],
     ["healthcare.gov", "Dickerson", "SRE p.85", "you fly blind"])
case("R7-03", "Ch. 4 notes 17 and 18 (p.50)", "sre_lookup.py", ["--topic", "notas-17-18-cap4"],
     ["Note 17", "Note 18", "SRE p.50", "not worth having SRE"])
case("R7-04", "failure injection (note 18) is COVERED", "sre_lookup.py", ["failure injection"],
     ["LEVEL: COVERED", "50"], rc=0)
case("R7-05", "config in an interpreted language: deadline in integration test and safe_load (p.145)", "sre_lookup.py", ["--topic", "config-linguagem-interpretada-p145"],
     ["deadline", "safe_load", "upper bound", "SRE p.145"])
case("R7-06", "interpreted is no longer POINTER ONLY", "sre_lookup.py", ["interpreted"],
     ["LEVEL: COVERED", "145"], rc=0, must_not=["POINTER ONLY"])
case("R7-07", "dozen sites (Ch. 34) is COVERED", "sre_lookup.py", ["dozen sites"],
     ["LEVEL: COVERED", "324"], rc=0, must_not=["POINTER ONLY"])
case("R7-N1", "chaos engineering stays uncovered in the book", "sre_lookup.py", ["chaos engineering"],
     ["NOT COVERED"], rc=1, must_not=["LEVEL: COVERED"])

# Round 8 (post-blind-test fixes): COVERED for terms the book has (pt-en stemming/alias, N+0), summaries p.65-66/89/98/190/246-248/312-314
case("R8-01", "pronounced: COVERED (var-zee, note 43, p.98)", "sre_lookup.py", ["pronounced"],
     ["LEVEL: COVERED", "var-zee", "sheep", "SRE p.98"], rc=0, must_not=["NOT COVERED", "POINTER ONLY"])
case("R8-02", "Borgmen: COVERED (plural = Borgmon, like sheep, note 44)", "sre_lookup.py", ["Borgmen"],
     ["LEVEL: COVERED", "plural of Borgmon is Borgmon", "sheep", "SRE p.98"], rc=0, must_not=["NOT COVERED", "POINTER ONLY"])
case("R8-03", "pronuncia (Portuguese input for 'pronunciation'): COVERED", "sre_lookup.py", ["pronuncia", "varz"],
     ["LEVEL: COVERED", "var-zee"], rc=0, must_not=["NOT COVERED"])
case("R8-04", "N+0: COVERED (note 25, p.62)", "sre_lookup.py", ["N+0"],
     ["LEVEL: COVERED", "zero redundancy", "SRE p.62"], rc=0, must_not=["NOT COVERED", "POINTER ONLY"])
case("R8-04b", "N + 0 (with spaces): COVERED", "sre_lookup.py", ["N + 0"],
     ["LEVEL: COVERED", "SRE p.62"], rc=0, must_not=["NOT COVERED"])
case("R8-05", "scripts/subprocess (p.89): COVERED", "sre_lookup.py", ["subprocess"],
     ["LEVEL: COVERED", "custom scripts", "SRE p.89"], rc=0, must_not=["NOT COVERED"])
case("R8-06", "Chubby (p.190): synchronized failure (Portuguese input 'configuracao')", "sre_lookup.py", ["Chubby", "configuracao"],
     ["LEVEL: COVERED", "synchronized failure", "SRE p.190"], rc=0, must_not=["NOT COVERED"])
case("R8-07", "degraded is no longer POINTER ONLY (p.190)", "sre_lookup.py", ["degraded"],
     ["LEVEL: COVERED", "graceful degradation", "190"], rc=0, must_not=["POINTER ONLY", "NOT COVERED"])
case("R8-08", "LIFO/CoDel: reason (10 s RPC in the queue)", "sre_lookup.py", ["LIFO"],
     ["LEVEL: COVERED", "10 s", "deadlines"], rc=0, must_not=["NOT COVERED"])
case("R8-09", "frameworks: one per environment is on p.312 (Portuguese input 'por ambiente')", "sre_lookup.py", ["framework", "por", "ambiente"],
     ["LEVEL: COVERED", "312", "do not share code"], rc=0, must_not=["NOT COVERED"])
case("R8-10", "maximalist (Portuguese input 'maximalista') (p.65)", "sre_lookup.py", ["maximalista"],
     ["LEVEL: COVERED", "SRE p.65"], rc=0, must_not=["NOT COVERED"])
case("R8-11", "rare automation: cluster failover (p.66)", "sre_lookup.py", ["failover", "cluster", "bit", "rot"],
     ["LEVEL: COVERED", "SRE p.66"], rc=0, must_not=["NOT COVERED"])
case("R8-12", "PITR: layers without PITR and 'use both' (p.247)", "sre_lookup.py", ["PITR"],
     ["LEVEL: COVERED", "use both", "SRE p.247"], rc=0, must_not=["NOT COVERED"])
case("R8-13", "similar spelling: suggests borgmon without asserting absence", "sre_lookup.py", ["Borgmun"],
     ["NOT COVERED", "similar spelling", "borgmon", "does NOT prove"], rc=1, must_not=["the book does not cover the topic"])


def load_module(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extra_checks(text_path):
    """structural checks of the lookup (round 2). Returns a list of (id, desc, ok, detail)."""
    import json
    import re
    res = []
    lk = load_module("sre_lookup_t", os.path.join(S, "sre_lookup.py"))
    bi = load_module("build_book_index_t", os.path.join(S, "build_book_index.py"))
    # (a) the lookup tokenizer and the indexer tokenizer coincide (otherwise the index does not match the query)
    samples = ["Shakespeare Sonnet++ 88x least-loaded Round-Robin $440M traﬀic Zookeeper, Consul e etcd",
               "id(packet) mod N-1 24 bytes IPv4+GRE 99.9999% on-call 1:1 alert/incident"]
    bad = []
    for sm in samples:
        a = [t for t in bi.tokens(sm)]
        b_all = []
        for t in lk.simple_tokens(sm):
            b_all.append(t)
            if "-" in t or "_" in t:
                for p in re.split(r"[-_]", t):
                    if len(p) >= 2 and p not in lk.STOP_EN and not (p.isdigit() and len(p) > 4):
                        b_all.append(p)
            if t.endswith("++"):
                b_all.append(t.rstrip("+"))
        if sorted(set(a)) != sorted(set(b_all)):
            bad.append(sm)
    res.append(("R2-T1", "lookup tokenizer == indexer tokenizer", not bad, bad))
    # (b) book index: metadata and required key terms
    idx_path = os.path.join(S, "book_term_index.json")
    idx = json.load(open(idx_path, encoding="utf-8"))
    need = {"shakespeare": 334, "sonnet": 335, "sacrificial": 334, "88x": 335, "etcd": 205, "440m": 321, "bazel": 140, "decider": 67, "gre": 162}
    miss = [k for k, p in need.items() if p not in idx["terms"].get(k, [])]
    res.append(("R2-T2", "book_term_index.json contains the blind-test terms with the right page", not miss, miss))
    res.append(("R2-T3", "index covers 347 pages, with no book excerpts (only terms and pages)",
                idx["_meta"]["pages"] == 347 and all(isinstance(v, list) and all(isinstance(x, int) for x in v) for v in idx["terms"].values()),
                idx["_meta"]["pages"]))
    # (c) every page cited in the sre_index.json topics exists (1..347)
    data = json.load(open(os.path.join(S, "sre_index.json"), encoding="utf-8"))
    badp = []
    for k, t in data["topics"].items():
        blob = t["citation"] + " " + t["summary"] + " " + " ".join(t["rules"])
        for m in re.finditer(r"p\.(\d+)(?:-(\d+))?", blob):
            a_, b_ = int(m.group(1)), int(m.group(2) or m.group(1))
            if not (1 <= a_ <= b_ <= 347):
                badp.append((k, m.group(0)))
    res.append(("R2-T4", "pages cited in sre_index.json are between 1 and 347", not badp, badp))
    # (d) all topics have the required fields and the 'does not say' rule with a list
    miss = [k for k, t in data["topics"].items() if not all(f in t for f in ("name", "keywords", "citation", "summary", "rules")) or not t["rules"]]
    res.append(("R2-T5", "topics with name/keywords/citation/summary/rules", not miss, miss))
    # (e) curated list: no curated regex matches a new covered topic (avoids a COVERED x outside-the-book contradiction)
    conflicts = []
    for q in ["Shakespeare", "88x", "sacrificial", "Knight Capital", "etcd", "Bazel", "Decider", "GRE", "Borgmon"]:
        if lk.out_of_book_hits(q, data["out_of_book"]):
            conflicts.append(q)
    res.append(("R2-T6", "curated outside-the-book list does not contradict covered terms", not conflicts, conflicts))
    # ---- round 4: COVERED x summary coherence; new topics; cited pages
    bad = lk.keyword_issues(data["topics"], data.get("synonyms", {}))
    res.append(("R3-T1", "consistent COVERED: every keyword of each topic appears in the summary/rules (or in a synonym)", not bad, bad[:3]))
    novos = ["definicoes-cap6-p55", "reuniao-de-producao", "interrupts-tickets-scrub", "canario-feature-flags"]
    faltam = [k for k in novos if k not in data["topics"]]
    res.append(("R3-T2", "round 4 topics present in sre_index.json", not faltam, faltam))
    # qualification by content: a query by a keyword the summary does not treat does not qualify
    synd = data.get("synonyms", {})
    nq = lk.rank_topics("youtube", data["topics"], lk.units_of("youtube"), synd)
    res.append(("R3-T3", "keyword/alias not treated in the summary does not qualify the topic (youtube)", not nq, nq[:2]))
    # each new/expanded topic cites at least one page and all of them exist
    sem_pag = [k for k in novos if not re.search(r"p\.\d+", data["topics"][k]["citation"])]
    res.append(("R3-T4", "new topics with a page citation", not sem_pag, sem_pag))
    # terms from the round 3 blind test exist in the book index with the right page
    need3 = {"bursty": 189, "outgoing": 193, "chirp": 320, "morgue": 129, "tgif": 128, "hickam": 114, "blobstore": 260}
    miss3 = [k for k, p in need3.items() if p not in idx["terms"].get(k, [])]
    res.append(("R3-T5", "book index has the round 4 detail terms with the right page", not miss3, miss3))
    # pt/en synonyms used by the lookup are in the index
    sy = data.get("synonyms", {})
    res.append(("R3-T6", "round 4 pt/en synonyms (causa/raiz, rajadas, canario...)", all(k in sy for k in ("causa", "raiz", "rajadas", "canario", "reuniao")), [k for k in ("causa", "raiz", "rajadas", "canario", "reuniao") if k not in sy]))
    # ---- round 5: term index of the SUMMARIES (references/), COVERED decided only by content
    br = load_module("build_ref_index_t", os.path.join(S, "build_ref_index.py"))
    code, out = run("build_ref_index.py", "--check")
    res.append(("R4-T1", "ref_term_index.json matches references/ (build_ref_index.py --check)", code == 0, out.strip()[-140:]))
    rix = json.load(open(os.path.join(S, "ref_term_index.json"), encoding="utf-8"))
    bad = [c for c in rix["chunks"] if c[0] == "INDEX.md"]
    res.append(("R4-T2", "INDEX.md (map/pointers) does not enter the summaries index", not bad, bad[:1]))
    pt = [t for t in ("dagger", "lustre", "tenets", "embracing") if t in rix["terms"] or t in rix["parts"]]
    res.append(("R4-T3", "terms only in a pointer/title (dagger, lustre, tenets, embracing) stay out of the summaries index", not pt, pt))
    ksum = [c for c in rix["chunks"] if c[2] == "s" and re.search(r"kubernetes", c[4], re.I)]
    res.append(("R4-T4", "Kubernetes appears only in limit notes, never as a summary", not ksum and "kubernetes" in rix["limit_terms"], len(ksum)))
    nopg = [c for c in rix["chunks"] if c[2] == "s" and not (c[3] and all(1 <= x <= 347 for x in c[3]))]
    res.append(("R4-T5", "every indexed summary cites a valid page (1..347)", not nopg, nopg[:1]))
    # summaries index tokenizer == lookup tokenizer
    bad = []
    for sm in ["Sonnet++ 88x least-loaded Round-Robin on-call 1:1 causa-raiz alert/incident Zookeeper, etcd e Consul"]:
        w, p_ = br.token_sets(sm)
        lt = set(lk.simple_tokens(sm))
        if lt - w:
            bad.append(sorted(lt - w))
        if lk.expand_parts(lt) - w != p_ - w:
            bad.append("parts diverge")
    res.append(("R4-T6", "build_ref_index tokenizer == lookup tokenizer", not bad, bad))
    # synthetic corpus: pointer, title, limit note and a line without a page do not become COVERED; a summary with a page does.
    # The Portuguese corpus exercises the Portuguese-reference classifier ("O livro NAO diz", PONTEIRO, [extrapolacao]);
    # the English corpus below exercises the English one.
    tmp = os.path.join(ROOT, "tests", "_tmp_refs")
    os.makedirs(tmp, exist_ok=True)
    try:
        with open(os.path.join(tmp, "sint-zzmega.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("# Titulo com Photon e Dagger\n\n## Resumo\n"
                    "- Mencius usa lideranca rotativa pre-atribuida entre as replicas do grupo. [do livro] (SRE p.204-205)\n"
                    "- Resumo valido sobre Spanner e relogios; PONTEIRO: Dagger, Lemon, Jepsen em detalhe. [do livro] (SRE p.30)\n"
                    "- Ponteiro: Chirp, Hickam e Morgue ficam so como lista de paginas (SRE p.114, 128).\n"
                    "- Linha sem pagina fala de Etcd e Kubernetes como resumo.\n"
                    "- Outro resumo (SRE p.205). O livro nao descreve Jepsen nem Chaos Monkey. Kafka e [extrapolacao].\n\n"
                    "## O livro NAO diz\n- Bigtable e Borg nao sao explicados aqui (SRE p.30).\n\n## Lista de ponteiros\n- Cassandra (SRE p.35)\n")
        with open(os.path.join(tmp, "INDEX.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("| Cap. | PONTEIRO: Zookeeper (SRE p.205) |\nZookeeper Consul (SRE p.205)\n")
        sd = br.build(tmp)
        st = set(sd["terms"]) | set(sd["parts"])
        exp_in = {"mencius", "spanner", "rotativa"}
        exp_out = {"dagger", "lemon", "jepsen", "chirp", "hickam", "morgue", "photon", "etcd", "kubernetes", "bigtable", "kafka",
                   "cassandra", "zookeeper", "consul", "chaos"}
        det = {"missing": sorted(exp_in - st), "unexpected": sorted(exp_out & st)}
        res.append(("R4-T7", "synthetic corpus (pt): only a summary body with a page enters (pointer, title, note, no page, INDEX.md stay out)",
                    not det["missing"] and not det["unexpected"], det))
        sidx = os.path.join(tmp, "sint_index.json")
        with open(sidx, "w", encoding="utf-8", newline="\n") as f:
            f.write(br.dump(sd))
        code, out = run("sre_lookup.py", "--ref-index", sidx, "Dagger")
        res.append(("R4-T8", "lookup with synthetic index: term only in a pointer list => POINTER ONLY (rc 3), never COVERED",
                    code == 3 and "LEVEL: POINTER ONLY" in out and "LEVEL: COVERED" not in out, (code, out[:120])))
        code, out = run("sre_lookup.py", "--ref-index", sidx, "Mencius")
        res.append(("R4-T9", "lookup with synthetic index: term in the summary body => COVERED (rc 0) with the page",
                    code == 0 and "LEVEL: COVERED" in out and "204, 205" in out, (code, out[:120])))
        code, out = run("sre_lookup.py", "--ref-index", sidx, "Etcd")
        res.append(("R4-T10", "lookup with synthetic index: term only on a line without a page => not COVERED",
                    code != 0 and "LEVEL: COVERED" not in out, (code, out[:120])))
        # English synthetic corpus (references translated to English)
        for fn in os.listdir(tmp):
            os.remove(os.path.join(tmp, fn))
        with open(os.path.join(tmp, "synth-zzmega.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("# Title with Photon and Dagger\n\n## Summary\n"
                    "- Mencius uses pre-assigned rotating leadership among the replicas of the group. [from source] (SRE p.204-205)\n"
                    "- Valid summary about Spanner and clocks; POINTER: Dagger, Lemon, Jepsen in detail. [from source] (SRE p.30)\n"
                    "- Pointer: Chirp, Hickam and Morgue stay only as a list of pages (SRE p.114, 128).\n"
                    "- A line without a page talks about Etcd and Kubernetes as a summary.\n"
                    "- Another summary (SRE p.205). The book does not describe Jepsen or Chaos Monkey. Kafka is [extrapolation].\n\n"
                    "## The book does not say\n- Bigtable and Borg are not explained here (SRE p.30).\n\n## Pointer list\n- Cassandra (SRE p.35)\n")
        sd = br.build(tmp)
        st = set(sd["terms"]) | set(sd["parts"])
        exp_in = {"mencius", "spanner", "rotating"}
        det = {"missing": sorted(exp_in - st), "unexpected": sorted(exp_out & st)}
        res.append(("R4-T11", "synthetic corpus (en): only a summary body with a page enters (pointer, title, note, no page stay out)",
                    not det["missing"] and not det["unexpected"], det))
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    # ---- round 6: new content in the references, vocabulary and per-page citations
    # (the substrings below are verbatim text of references/*.md, kept in Portuguese until those files are translated)
    refdir = os.path.join(ROOT, "references")

    def ref_text(fn):
        return open(os.path.join(refdir, fn), encoding="utf-8").read().replace("\r\n", "\n")

    need6 = [
        ("release-engineering-e-testes.md", ["MTBF worse", "mostly unattended", "skew", "much_ado", "limits flexibility",
                                             "unified monolithic", "p.80", "p.81", "p.141", "p.144", "DNS cache", "intercontinental"]),
        ("gestao-treinamento-interrupts-e-engajamento.md", ["reverse shadow", "co-author", "Note 136", "Note 137", "five factors", "human cost",
                                                           "low skill", "Angry Birds", "Frobnitzer", "TaskFailures", "p.281", "p.282", "p.285", "p.286"]),
        ("toil-automacao-e-simplicidade.md", ["TestDnsMonitoringConfigExists", "FixDnsMonitoringPushConfig", "Machine Database", "Figure 7-1", "Figure 7-2", "p.70"]),
        ("risco-slo-e-error-budget.md", ["aggregate unavailability", "partially available", "p.328"]),
        ("plantao-troubleshooting-e-incidentes.md", ["time-off-in-lieu", "cap", "p.101"]),
        ("principios-e-papel-do-sre.md", ["Thrift", "Stubby", "not with JSON", "Android and Chrome", "note 10", "Note 13", "p.33", "p.35"]),
        ("lancamentos-e-capacity-planning.md", ["0.1%", "note 89", "cost savings", "no page of Ch. 18", "p.147", "p.150", "p.151"]),
        ("postmortem-e-rastreamento-de-outages.md", ["p.127-128", "p.292-293"]),
    ]
    falta6 = []
    for fn, subs in need6:
        txt = ref_text(fn)
        for s_ in subs:
            if s_.lower() not in txt.lower():
                falta6.append((fn, s_))
    res.append(("R6-T1", "references carry the new round 6 content (per file)", not falta6, falta6[:3]))
    cap6 = [fn for fn in os.listdir(refdir) if fn.endswith(".md") and fn != "INDEX.md" and "(round 6)" in ref_text(fn)]
    res.append(("R6-T2", "eight reference files received a round 6 section", len(cap6) == 8, sorted(cap6)))
    # right sense in the summaries index: 'flow' (cognitive flow, p.285), 'shadow' (p.282), 'dns' (Prodtest, p.70), 'unattended' (p.144)
    rix6 = json.load(open(os.path.join(S, "ref_term_index.json"), encoding="utf-8"))
    ch6 = rix6["chunks"]

    def has_chunk(term, page, fragment):
        for i in rix6["terms"].get(term, []):
            f_, ln_, k_, pg_, tx_ = ch6[i]
            if k_ == "s" and page in pg_ and fragment in tx_:
                return True
        return False
    checks6 = [("flow", 285, "zone"), ("flow", 286, "Angry Birds"), ("shadow", 282, "reverse shadow"), ("shadow", 281, "eligible"),
               ("dns", 70, "Machine Database"), ("unattended", 144, "mostly unattended"), ("supervised", 144, "supervised")]
    ruins = [c for c in checks6 if not has_chunk(*c)]
    res.append(("R6-T3", "summaries index: flow/shadow/DNS/unattended with the right sense and page", not ruins, ruins))
    # the summary treats the term as a subject: at least 3 distinct summary chunks for cognitive flow, shadow and the DNS example
    n_flow = sum(1 for i in rix6["terms"].get("flow", []) if ch6[i][2] == "s" and 285 in ch6[i][3])
    n_sh = sum(1 for i in rix6["terms"].get("shadow", []) if ch6[i][2] == "s" and (281 in ch6[i][3] or 282 in ch6[i][3]))
    n_dns = sum(1 for i in rix6["terms"].get("dns", []) if ch6[i][2] == "s" and (68 in ch6[i][3] or 70 in ch6[i][3]))
    res.append(("R6-T4", "non-shallow summaries: flow (p.285) >= 3, shadow (p.281-282) >= 4, Prodtest DNS (p.68-70) >= 3 chunks",
                n_flow >= 3 and n_sh >= 4 and n_dns >= 3, (n_flow, n_sh, n_dns)))
    # PT/EN vocabulary and polysemy
    idx6 = json.load(open(os.path.join(S, "sre_index.json"), encoding="utf-8"))
    syn6 = idx6["synonyms"]
    voc = [("supervisao", "unattended"), ("unsupervised", "unattended"), ("unattended", "supervisao"), ("sombra", "shadow"),
           ("coautoria", "coauthor"), ("compensacao", "compensation"), ("repositorio", "repository"), ("agregada", "aggregate"),
           ("economia", "savings"), ("folga", "lieu")]
    faltam6 = [(a, b) for a, b in voc if b not in syn6.get(a, [])]
    res.append(("R6-T5", "round 6 PT/EN synonym table (supervisao/unattended, sombra/shadow, ...)", not faltam6, faltam6))
    amb6 = {a["term"]: a["senses"] for a in idx6.get("ambiguous_terms", [])}
    ok_amb = all(k in amb6 and len(amb6[k]) >= 2 for k in ("flow", "shadow", "dns", "config"))
    pg_amb = all(re.search(r"p\.\d+", s_) for ss in amb6.values() for s_ in ss)
    res.append(("R6-T6", "ambiguous terms (flow, shadow, dns, config) with >= 2 senses and a page", ok_amb and pg_amb, sorted(amb6)))
    # each fix has a positive AND a per-page negative citation check in citation-checks.json
    cc6 = json.load(open(os.path.join(S, "citation-checks.json"), encoding="utf-8"))
    ids_pos = {c["id"] for c in cc6["positive"]}
    ids_np = {c["id"] for c in cc6["negative_pages"]}
    ids_neg = {c["id"] for c in cc6["negative"]}
    need_pos = {"P%d" % n for n in range(412, 448)}
    need_np = {"NP%02d" % n for n in range(6, 22)}
    res.append(("R6-T7", "citation-checks.json: P412-P447, NP06-NP21 and N64-N65 present",
                need_pos <= ids_pos and need_np <= ids_np and {"N64", "N65"} <= ids_neg,
                (sorted(need_pos - ids_pos)[:3], sorted(need_np - ids_np)[:3])))
    # the copies of citation-checks.json (scripts/, tests/) are identical
    same = open(os.path.join(S, "citation-checks.json"), "rb").read() == open(os.path.join(ROOT, "tests", "citation-checks.json"), "rb").read()
    res.append(("R6-T8", "citation-checks.json in scripts/ and tests/ identical", same, same))
    idx_txt = open(os.path.join(refdir, "INDEX.md"), encoding="utf-8").read()
    res.append(("R6-T9", "INDEX.md records round 6 and what remains (pending items)", "Round 6" in idx_txt and "Still without summary" in idx_txt, "Round 6" in idx_txt))

    # (f) if the book text is available: versioned index == index generated from the text; curated terms without occurrence
    if text_path:
        code, out = run("build_book_index.py", "--text", text_path, "--check")
        res.append(("R2-T7", "book_term_index.json matches the book text (build_book_index.py --check)", code == 0, out.strip()[-120:]))

    # ---- round 10: corrected/added content
    def rt10(fn):
        return open(os.path.join(ROOT, "references", fn), encoding="utf-8").read().replace("\r\n", "\n")
    mon, risco = rt10("monitoramento-e-alertas.md"), rt10("risco-slo-e-error-budget.md")
    bad10 = [n for n, t in (("monitoramento", mon), ("risco", risco)) if "probing for status 200 every 1-2" in t.lower()]
    res.append(("R10-T1", "the '1-2 min' rule is no longer attributed to probing the 200 (only to the disk; p.59)", not bad10 and "once or twice a minute" in mon and "once or twice **per minute**" in risco, bad10))
    need10 = [
        ("monitoramento-e-alertas.md", ["Table 6-1", "bogosort", "slow database", "p.57"]),
        ("toil-automacao-e-simplicidade.md", ["Note 40", "grab bag", "p.84"]),
        ("gestao-treinamento-interrupts-e-engajamento.md", ["neutral", "arbiter", "agreed way", "does not reach projected usage", "business risk", "did not scale", "p.299", "p.301", "p.311"]),
        ("consenso-cron-e-pipelines.md", ["at least one node", "complete view", "p.205", "p.216"]),
    ]
    falta10 = [(fn_, x) for fn_, subs in need10 for x in subs if x.lower() not in rt10(fn_).lower()]
    res.append(("R10-T2", "references carry the round 10 content (per file)", not falta10, falta10[:3]))
    return res


# ---- round 9 (after the blind test): p.45, p.196-197, p.203, p.61, p.216, p.256, note 109
case("R9-01", "QPS: p.45 (no SLO is set for QPS; average < 100 ms example) + ALERT with the two senses", "sre_lookup.py", ["QPS"],
     ["LEVEL: COVERED", "Not every SLI becomes an SLO", "no SLO is set for QPS", "average latency", "ALERT: 'qps'", "SRE p.45"])
case("R9-02", "QPS SLO: the first summary is the one on p.45", "sre_lookup.py", ["SLO", "de", "QPS"],
     ["LEVEL: COVERED", "risco-slo-e-error-budget.md", "performance cliff"])
case("R9-03", "BASE (p.203): clock drift, Shute, financial transactions", "sre_lookup.py", ["BASE", "clock", "drift"],
     ["LEVEL: COVERED", "clock drift", "Shute"])
case("R9-04", "idle CPU: p.196-197 (dangerous; gradual x impulse; return to nominal)", "sre_lookup.py", ["CPU", "idle"],
     ["LEVEL: COVERED", "dangerous", "slack CPU"])
case("R9-05", "gradual x impulse and return to nominal load (p.197)", "sre_lookup.py", ["impulse", "nominal"],
     ["LEVEL: COVERED", "gradual and impulse", "without human intervention", "197"])
case("R9-06", "'de-schedulizadas' (free spelling) becomes COVERED with the Gmail/Workqueue case (p.61)", "sre_lookup.py", ["de-schedulizadas"],
     ["LEVEL: COVERED", "Workqueue", "pages 61"])
case("R9-07", "Workqueue: self-discipline, managers and leads, red flag (p.61)", "sre_lookup.py", ["Workqueue"],
     ["LEVEL: COVERED", "self-discipline", "managers and technical leads", "Red flag"])
case("R9-08", "p.216: assumptions behind 100 ops/s and combined log", "sre_lookup.py", ["combined", "log", "consensus"],
     ["LEVEL: COVERED", "negligible", "SRE p.216"])
case("R9-09", "'50.000 operacoes' (Portuguese input) is NOT COVERED because of the 50.000 QPS on p.175", "sre_lookup.py", ["50.000", "operações"],
     ["NOT COVERED", "100 operations/s", "SRE p.216", "a different topic"], rc=1, must_not=["LEVEL: COVERED"])
case("R9-10", "encryption: p.30 and p.256 (not just Ch. 2)", "sre_lookup.py", ["encryption"],
     ["LEVEL: COVERED", "pages 30, 256"])
case("R9-11", "--pages encryption lists p.30 and p.256", "sre_lookup.py", ["--pages", "encryption"],
     ["pages 30, 256"])
case("R9-12", "reason for the quarter (p.330) and N+2 p.330 x load test p.331", "sre_lookup.py", ["load", "test", "tradition"],
     ["LEVEL: COVERED", "SRE p.330; p.331"])

# ---------------------------------------------------------------- round 10 (after the blind test): p.59 (1-2 per minute only for the 200), 70/30, p.57/84/205/299/301/311
case("R10-01", "70/30: NOT COVERED (not COVERED by an irrelevant match), with 50-60%/40-50% from p.23", "sre_lookup.py", ["70/30"],
     ["NOT COVERED", "NOT IN THE SOURCE", "50-60%", "40-50%", "SRE p.23"], rc=1, must_not=["LEVEL: COVERED"])
case("R10-02", "30/70 likewise", "sre_lookup.py", ["30/70"], ["NOT COVERED", "NOT IN THE SOURCE"], rc=1, must_not=["LEVEL: COVERED"])
case("R10-03", "50-60% stays COVERED (p.23)", "sre_lookup.py", ["50-60%"], ["LEVEL: COVERED", "SRE p.23"], must_not=["NOT COVERED"])
case("R10-04", "bogosort: Table 6-1 (p.57)", "sre_lookup.py", ["bogosort"], ["LEVEL: COVERED", "p.57"], must_not=["NOT COVERED"])
case("R10-05", "protobuf: note 40 / p.84", "sre_lookup.py", ["protocol", "buffers", "backward"], ["LEVEL: COVERED", "84"], must_not=["NOT COVERED"])
case("R10-06", "cross-site: recommendations p.301 (Portuguese input 'árbitro')", "sre_lookup.py", ["cross-site", "árbitro"], ["LEVEL: COVERED", "301"], must_not=["NOT COVERED"])
case("R10-07", "probing the 200 and disk: p.59 (Portuguese input 'sondar disco')", "sre_lookup.py", ["sondar", "disco"], ["LEVEL: COVERED", "59"], must_not=["NOT COVERED"])
case("R10-08", "Monarch: reasons for the consoles (p.299)", "sre_lookup.py", ["Monarch", "consoles"], ["LEVEL: COVERED", "299"], must_not=["NOT COVERED"])
case("R14-01", "Route 53 (cloud product with a number) = NOT COVERED, not POINTER ONLY", "sre_lookup.py", ["Route 53"],
     ["NOT COVERED", "product/service name", "NOT coverage of the product"], rc=1, must_not=["POINTER ONLY", "LEVEL: COVERED"])
case("R14-02", "AWS Route 53 failover: product without coverage, the rest follows the normal analysis", "sre_lookup.py", ["AWS", "Route", "53", "failover"],
     ["NOT COVERED", "route 53"], rc=3, must_not=["'route': pages"])
case("R14-03", "BeyondCorp: COVERED p.87 (+ bibliography p.346)", "sre_lookup.py", ["BeyondCorp"],
     ["LEVEL: COVERED", "pages 87, 346", "privileged intranets"], rc=0, must_not=["POINTER ONLY", "NOT COVERED"])
case("R14-04", "zero trust is not in the book (does not match 'zero' from the integrity chapter)", "sre_lookup.py", ["zero trust"],
     ["NOT COVERED", "BeyondCorp", "p.87"], rc=1, must_not=["integridade-de-dados"])
case("R14-05", "chapter 17 and SLO 99 stay normal (word + number that is not a product; Portuguese input 'capitulo')", "sre_lookup.py", ["capitulo", "17"],
     ["LEVEL: COVERED"], rc=0, must_not=["product/service name"])
case("R14-06", "failing probe: non-equivalent API, rollback to the last good state, rollout automation (p.146)", "sre_lookup.py",
     ["production", "probes", "rollback"], ["LEVEL: COVERED", "release-engineering-e-testes.md:35", "pages 145, 146"], rc=0, must_not=["NOT COVERED"])
case("R14-07", "rollout automation blocks the rollout (p.146) (Portuguese input 'bloquear')", "sre_lookup.py", ["rollout", "automation", "bloquear"],
     ["LEVEL: COVERED", "release-engineering-e-testes.md", "pages 145, 146"], rc=0, must_not=["NOT COVERED"])
case("R14-08", "Reverse Engineering: sources, exercises and final task with the senior (p.279)", "sre_lookup.py", ["reverse", "engineering", "senior"],
     ["LEVEL: COVERED", "gestao-treinamento-interrupts-e-engajamento.md:53", "pages 278, 279", "Guided, interactive exercises"], rc=0, must_not=["NOT COVERED"])
case("R14-09", "burn a search cluster (p.281) stays COVERED", "sre_lookup.py", ["burn", "search", "cluster"],
     ["LEVEL: COVERED", "281"], rc=0, must_not=["NOT IN THE SOURCE"])
case("R14-10", "Moire's 1.2 M: the book does not give the unit (p.236-237) (Portuguese input 'unidade')", "sre_lookup.py", ["Moire", "unidade"],
     ["LEVEL: COVERED", "does not state the unit"], rc=0, must_not=["NOT COVERED"])
case("R14-11", "snapshots on the same storage do not protect against a site failure (p.250) (Portuguese input 'falha site')", "sre_lookup.py", ["snapshots", "falha", "site"],
     ["LEVEL: COVERED", "integridade-de-dados-e-backup.md:23", "250"], rc=0, must_not=["NOT COVERED"])
case("R14-12", "sre_math duration with the flags (correct form cited in the prompt)", "sre_math.py", ["duration", "--start", "14:54", "--end", "16:00"],
     ["66"], rc=0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    a = ap.parse_args()
    fails = 0
    for cid, desc, script, args, must, rc, must_not in CASES:
        code, out = run(script, *args)
        missing = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not missing and not bad
        print("%s %-6s %s" % ("OK   " if ok else "FAIL ", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (code, rc, missing, bad))
    for tid, desc, ok_, det in extra_checks(a.text):
        print("%s %-6s %s" % ("OK   " if ok_ else "FAIL ", tid, desc))
        if not ok_:
            fails += 1
            print("   detail: %s" % (det,))
    # postmortem: the generated template must validate
    code, tpl = run("postmortem_tool.py", "template", "--lang", "en")
    tmp = os.path.join(ROOT, "tests", "_tmp_pm.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(tpl)
    code, out = run("postmortem_tool.py", "validate", tmp)
    os.remove(tmp)
    ok = code == 0 and "13/13" in out
    print("%s %-6s validate accepts the generated template" % ("OK   " if ok else "FAIL ", "CT-15c"))
    fails += 0 if ok else 1
    # R14: Portuguese blame patterns (postmortem_tool validate; the draft is Portuguese user input); the pt template must not flag blame
    draft = ("# Postmortem\n## Summary\nO Rafael fez o deploy errado, foi advertido e deveria ter sido mais cuidadoso. "
             "A culpa e dele; falha humana por negligencia.\n")
    tmp2 = os.path.join(ROOT, "tests", "_tmp_pm_blame.md")
    with open(tmp2, "w", encoding="utf-8") as f:
        f.write(draft)
    code, out = run("postmortem_tool.py", "validate", tmp2)
    os.remove(tmp2)
    must = ["blame language", "errad", "advertid", "mais cuidados", "culpa", "falha humana", "negligenc"]
    miss = [m for m in must if m not in out]
    ok = not miss
    print("%s %-6s validate flags blame in Portuguese (errado/advertido/mais cuidadoso/culpa/falha humana)" % ("OK   " if ok else "FAIL ", "R14-13"))
    if not ok:
        print("   missing=%s" % miss)
    fails += 0 if ok else 1
    code, tplpt = run("postmortem_tool.py", "template", "--lang", "pt")
    tmp3 = os.path.join(ROOT, "tests", "_tmp_pm_pt.md")
    with open(tmp3, "w", encoding="utf-8") as f:
        f.write(tplpt)
    code, out = run("postmortem_tool.py", "validate", tmp3)
    os.remove(tmp3)
    ok = code == 0 and "blame language" not in out
    print("%s %-6s pt template does not trigger a blame warning (blameless, 'sem culpa' does not count)" % ("OK   " if ok else "FAIL ", "R14-14"))
    fails += 0 if ok else 1
    # R14: corrected content in the summaries (checked against the book text, p.87, 145-146, 236-237, 247, 250, 279, 281);
    # the substrings are verbatim text of references/*.md (English)
    def rtxt(fn):
        return io.open(os.path.join(ROOT, "references", fn), encoding="utf-8").read()
    rel, ges, integ, cron, glos, prin = (rtxt(x) for x in (
        "release-engineering-e-testes.md", "gestao-treinamento-interrupts-e-engajamento.md", "integridade-de-dados-e-backup.md",
        "consenso-cron-e-pipelines.md", "glossario.md", "principios-e-papel-do-sre.md"))
    r14 = [
        ("failing probe: non-equivalent API, site probably broken", "not equivalent between production and the release environment" in rel and "the site is probably broken" in rel),
        ("rollback to the last good state and rollout automation blocks the rollout (p.146)", "last known good state" in rel and "block the production rollout" in rel),
        ("Ch. 28: binaries self-report RPC, white-box and black-box, final task with the senior (p.279)",
         "self-report their RPC connectivity" in ges and "white-box and black-box" in ges and "senior SRE" in ges and "burn a search cluster" in ges),
        ("BeyondCorp in the p.87 summary with [War14] and p.346", "BeyondCorp" in prin and "SRE p.87, 346" in prin),
        ("1.2 M without a unit (p.236-237) in cron/pipelines and glossary", "does not state the unit" in cron and "no unit given in the book" in glos),
        ("snapshots: local layers alone do not protect against site failure (p.250); without requiring PITR and layers",
         "does not protect against site-level failures" in integ and "not a requirement to always have PITR" in integ),
    ]
    for i, (d_, ok_) in enumerate(r14, 15):
        print("%s %-6s %s" % ("OK   " if ok_ else "FAIL ", "R14-%d" % i, d_))
        fails += 0 if ok_ else 1
    if a.text:
        code, out = run("verify_citations.py", "--text", a.text)
        ok = code == 0
        print("%s %-6s verify_citations: %s" % ("OK   " if ok else "FAIL ", "VC", out.strip().splitlines()[-1]))
        fails += 0 if ok else 1
    print("Summary: %d failures" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

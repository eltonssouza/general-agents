# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic cases of tests/casos-de-teste.md against the SCRIPTS and checks that
the REFERENCES contain what each case requires (pages, labels and warnings). Usage (from the package root):
    python -I tests/run_script_tests.py
No network. Exit code 0 if all pass. Does not replace model-based evaluation: it only covers the part verifiable by code.
Note: the strings checked against references/*.md are the English text of the translated reference files.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
R = os.path.join(ROOT, "references")

SCRIPT_CASES = []
REF_CASES = []


def run(script, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", os.path.join(S, script)] + list(args),
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


def sc(cid, desc, script, args, must, rc=0, must_not=()):
    SCRIPT_CASES.append((cid, desc, script, args, must, rc, must_not))


def rf(cid, desc, fname, must, must_not=()):
    REF_CASES.append((cid, desc, fname, must, must_not))


# --- scripts (messages in English) ---
sc("CT-03", "PACELC not covered", "nosql_lookup.py", ["pacelc"], ["NOT IN THE SOURCE", "PACELC is not in the sources"], rc=1)
sc("CT-02", "lookup CAP", "nosql_lookup.py", ["cap", "brewer"], ["STRAUCH p.34-35", "teorema-cap-e-teorema-pacelc.md"])
sc("CT-05", "lookup consistent hashing", "nosql_lookup.py", ["hash consistente"], ["STRAUCH p.43-45"])
sc("CT-06", "lookup quorum", "nosql_lookup.py", ["quorum"], ["STRAUCH p.45-46", "STRAUCH p.61-62"])
sc("CT-08", "lookup Redis structures", "nosql_lookup.py", ["--topic", "sorted sets"], ["REDIS p.7-14"])
sc("CT-09", "lookup bgsave not covered", "nosql_lookup.py", ["bgsave"], ["NOT IN THE SOURCE", "REDIS p.9"], rc=1)
sc("CT-14", "raft not covered", "nosql_lookup.py", ["raft"], ["NOT IN THE SOURCE", "STRAUCH p.100"], rc=1)
sc("CT-16", "CouchDB _rev not covered", "nosql_lookup.py", ["_rev"], ["NOT IN THE SOURCE", "STRAUCH p.77"], rc=1)
sc("CT-17", "inverted index not covered", "nosql_lookup.py", ["inverted", "index"], ["NOT IN THE SOURCE"], rc=1)
sc("CT-18", "lookup graphs", "nosql_lookup.py", ["index-free"], ["NEO4J-GDB p.23", "NEO4J-GDB p.167-169"])
sc("CT-24", "out of scope", "nosql_lookup.py", ["kubernetes", "operator"], ["NOT COVERED"], rc=1)
sc("CT-19", "N=5 R=3 W=3", "quorum_calc.py", ["-N", "5", "-R", "3", "-W", "3"],
   ["R + W = 3 + 3 = 6", "R + W > N", "STRAUCH p.46"], must_not=["R + W <= N:"])
sc("CT-20", "N=3 R=1 W=1", "quorum_calc.py", ["-N", "3", "-R", "1", "-W", "1"],
   ["R + W = 1 + 1 = 2", "R + W <= N", "STRAUCH p.61"])
sc("CT-06b", "Dynamo typical", "quorum_calc.py", ["-N", "3", "-R", "2", "-W", "2"],
   ["R + W > N", "N=3, R=2, W=2 (typical, STRAUCH p.62)"])
sc("CT-23", "shortcuts are extrapolation", "quorum_calc.py", ["-N", "3", "-R", "QUORUM", "-W", "ALL"],
   ["R = 2 | W = 3", "[extrapolation] shortcuts"])
sc("CT-23b", "W=0 is a warning", "quorum_calc.py", ["-N", "3", "-R", "3", "-W", "0"], ["W = 0", "note 5"])
sc("CT-23c", "invalid R", "quorum_calc.py", ["-N", "3", "-R", "0", "-W", "2"], ["ERROR"], rc=2)
sc("CT-21", "N:M", "mongo_selector.py", ["--cardinality", "N:M"], ["EMBED A LIST OF _id", "MONGO-PAT p.27-28", "does not define numeric"])
sc("CT-10", "1:many paginated", "mongo_selector.py", ["--cardinality", "1:many", "--unbounded-growth", "--paginated-access"],
   ["HYBRID", "MONGO-PAT p.131-133", "REFERENCE", "MONGO-PAT p.26-27"])
sc("CT-10b", "1:1 read together and atomic", "mongo_selector.py", ["--cardinality", "1:1", "--queried-together", "--atomic-needed"],
   ["EMBED", "MONGO-PAT p.23-24", "DATED"])
sc("CT-22", "PostgreSQL without a label", "cap_classifier.py", ["--system", "postgresql"], ["none", "extrapolation"], must_not=["PC/EC [from source]"])
sc("CT-02b", "Dynamo A+P and Bigtable C+A", "cap_classifier.py", ["--system", "all"],
   ["A + P", "C + A", "STRAUCH p.34", "PACELC is NOT IN THE SOURCE"])
sc("CT-02c", "Brewer table", "cap_classifier.py", ["--table"], ["LDAP", "Coda", "STRAUCH p.35"])
sc("CT-14b", "MongoDB: mechanism, extrapolated label", "cap_classifier.py", ["--system", "mongodb"],
   ["STRAUCH p.100", "[extrapolation]", "MONGO-MAN-H p.3"])

# --- references (English reference files) ---
rf("CT-01", "NoSQL motivations with page", "origens-e-motivacao-do-nosql.md", ["STRAUCH p.6", "STRAUCH p.7-8", "p.11-12"])
rf("CT-02", "CAP: non-negotiable P and extrapolation", "teorema-cap-e-teorema-pacelc.md",
   ["STRAUCH p.34", "at most two", "[extrapolation]", "C + A"])
rf("CT-03", "PACELC only as extrapolation", "teorema-cap-e-teorema-pacelc.md", ["PACELC", "is not", "[extrapolation]"], ["PA/EL [from source]"])
rf("CT-04", "BASE and consistency", "modelo-base-vs-acid-e-consistencia-eventual.md", ["STRAUCH p.35", "Monotonic Write", "Not covered"])
rf("CT-05", "consistent hashing: K/N and Cassandra vnodes", "hash-consistente-e-particionamento-distribuido.md",
   ["STRAUCH p.43", "K/N", "[extrapolation]", "does not use virtual nodes"])
rf("CT-07", "families: Strauch excludes graphs", "taxonomia-das-quatro-familias-nosql.md", ["excludes graphs", "p.214", "four quadrants"])
rf("CT-09", "Redis persistence: what is not covered", "redis-persistencia-rdb-e-aof.md", ["REDIS p.9", "BGSAVE", "[extrapolation]", "no automatic failover"])
rf("CT-11", "16 MB x 4 MB", "mongodb-modelo-de-documentos-e-bson.md", ["MONGO-PAT p.26-27", "STRAUCH p.106", "4 MB", "256 kB"])
rf("CT-12", "transactions: eras", "mongodb-modelo-de-documentos-e-bson.md", ["MONGO-MAN-H", "multi-document", "DATED", "p.24"])
rf("CT-13", "shard key", "mongodb-alta-disponibilidade-e-sharding.md", ["p.62-63", "hard or impossible", "Raft"])
rf("CT-14", "2010 replica set", "mongodb-alta-disponibilidade-e-sharding.md", ["(p.100)", "majority", "heartbeat"])
rf("CT-15", "Cassandra: CASS and landing page", "apache-cassandra-wide-column-e-quorum.md", ["CASS is only the landing page", "p.120", "ONE/TWO/QUORUM/ALL"])
rf("CT-16", "CouchDB", "couchdb-e-elasticsearch-visoes-especializadas.md", ["COUCH p.1", "MVCC", "`_rev`", "do not appear"])
rf("CT-17", "ELAST landing", "couchdb-e-elasticsearch-visoes-especializadas.md", ["ELAST", "Lucene", "Not covered", "inverted index"])
rf("CT-18", "graphs and fraud", "taxonomia-das-quatro-familias-nosql.md", ["p.23, 167-168", "p.168-169", "Fraud detection"])
rf("CT-28", "injection: anti-patterns", "casos-e-antipadroes.md", ["NoSQL query injection", "[extrapolation]"])


def check(out, must, must_not):
    miss = [m for m in must if m not in out]
    bad = [m for m in must_not if m in out]
    return miss, bad


def main():
    fails = 0
    total = 0
    for cid, desc, script, args, must, rc_exp, must_not in SCRIPT_CASES:
        total += 1
        rc, out = run(script, *args)
        miss, bad = check(out, must, must_not)
        ok = rc == rc_exp and not miss and not bad
        print(("OK   " if ok else "FAIL "), cid, "-", desc, "[%s %s]" % (script, " ".join(args)))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (rc, rc_exp, miss, bad))
            print("   output:", out[:600].replace("\n", " | "))
    for cid, desc, fname, must, must_not in REF_CASES:
        total += 1
        path = os.path.join(R, fname)
        txt = open(path, encoding="utf-8").read()
        miss, bad = check(txt, must, must_not)
        ok = not miss and not bad
        print(("OK   " if ok else "FAIL "), cid, "-", desc, "[references/%s]" % fname)
        if not ok:
            fails += 1
            print("   missing=%s unexpected=%s" % (miss, bad))
    print("Summary: %d cases, %d failures" % (total, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
cap_classifier.py - what the SOURCES say (and do NOT say) about CAP and behavior under partition.

Declared origin of each line:
  [from source]    text read on the cited page (p.N = PDF page; see references/INDEX.md)
  [extrapolation]  knowledge external to the sources (e.g. Abadi's PACELC, product labels)
The sources do NOT assign CAP/PACELC labels to Cassandra, MongoDB, CouchDB, Redis or PostgreSQL.
The only CAP labels given by STRAUCH are those for Dynamo (A+P) and Bigtable (C+A), p.34, and the examples
in Brewer's table (p.35). Everything else is presented as a mechanism [from source] + an [extrapolation] label.

Usage:
  python -I cap_classifier.py --system dynamo|bigtable|mongodb|cassandra|couchdb|redis|postgresql|all
  python -I cap_classifier.py --table        # Brewer's table (STRAUCH p.35)
Read-only, no network.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

BREWER_TABLE = [
    ("C + A (gives up partitions)", "2PC, cache-validation protocols",
     "single-site databases, cluster databases, LDAP, xFS"),
    ("C + P (gives up availability)", "pessimistic locking, making minority partitions unavailable",
     "distributed databases, distributed locks, majority protocols"),
    ("A + P (gives up consistency)", "expirations/leases, conflict resolution, optimism",
     "Coda, web caching, DNS"),
]

SYSTEMS = {
    "dynamo": {
        "name": "Amazon Dynamo",
        "book_label": ("A + P (available and partition tolerant, not strictly consistent)", "STRAUCH p.34"),
        "mechanisms": [
            ("Always writable; conflicts resolved at read time with vector clocks; optional LWW", "STRAUCH p.58, 60"),
            ("Sloppy quorum and hinted handoff for temporary failures; N=3, R=2, W=2 typical", "STRAUCH p.61-63"),
        ],
        "extrapolation": None,
    },
    "bigtable": {
        "name": "Google Bigtable",
        "book_label": ("C + A (consistent and available; does not fully operate under partitions)", "STRAUCH p.34"),
        "mechanisms": [("Central master partitions data across tablet servers", "STRAUCH p.125")],
        "extrapolation": None,
    },
    "mongodb": {
        "name": "MongoDB (replica set, version 1.6 from 2010)",
        "book_label": None,
        "mechanisms": [
            ("Write acknowledged only if replicated to a majority; a primary without heartbeats from at least half of the nodes stops being primary", "STRAUCH p.100"),
            ("During failover, writes and strongly consistent reads are unavailable; eventual reads continue", "STRAUCH p.100"),
            ("Current version (8.3): automatic failover and multi-document transactions (overview, no details)", "MONGO-MAN-H p.3"),
        ],
        "extrapolation": "Label 'CP' or 'PC/EC' [extrapolation]: depends on write concern, read preference and version.",
    },
    "cassandra": {
        "name": "Apache Cassandra (2008-2010 description)",
        "book_label": None,
        "mechanisms": [
            ("No single point of failure; a write requires a quorum of acknowledgements; on reads the client chooses the 'degree of eventual consistency'", "STRAUCH p.119-120"),
            ("Read picks the most recent answer by timestamp and schedules repair of stale replicas", "STRAUCH p.122"),
        ],
        "extrapolation": "Label 'AP' or 'PA/EL' [extrapolation]; CASS (landing page) has no architecture.",
    },
    "couchdb": {
        "name": "Apache CouchDB",
        "book_label": None,
        "mechanisms": [
            ("Replicas always writable, incremental bidirectional replication; version conflicts are a normal state, resolved by the application", "COUCH p.5-6; STRAUCH p.76-78"),
            ("'Strong' consistency in a cluster is questionable according to STRAUCH", "STRAUCH p.78"),
        ],
        "extrapolation": "Label 'AP' or 'PA/EC' [extrapolation].",
    },
    "redis": {
        "name": "Redis (~2015 book)",
        "book_label": None,
        "mechanisms": [
            ("Asynchronous master-slave replication; reads on slaves may be slightly stale; no automatic failover in the book", "REDIS p.29"),
            ("No fault tolerance by itself; in-memory data is lost if the server goes down (STRAUCH note)", "STRAUCH p.25"),
        ],
        "extrapolation": "Redis Cluster/Sentinel are not covered; the 'PA/EL' label [extrapolation] has no basis in the sources.",
    },
    "postgresql": {
        "name": "PostgreSQL",
        "book_label": None,
        "mechanisms": [],
        "extrapolation": "This agent's sources do not cover PostgreSQL; any CAP/PACELC label is [extrapolation]. "
                         "(v1 cited 'PG16 p.865-875' without basis.) STRAUCH p.35 lists single-site and cluster databases as examples of C + A.",
    },
}


def show(key):
    s = SYSTEMS[key]
    print("SYSTEM: %s" % s["name"])
    if s["book_label"]:
        print("  [from source] CAP label: %s (%s)" % s["book_label"])
    else:
        print("  [from source] CAP label: none - the sources do not classify this system")
    for txt, ref in s["mechanisms"]:
        print("  [from source] mechanism: %s (%s)" % (txt, ref))
    if s["extrapolation"]:
        print("  %s" % s["extrapolation"])
    print()


def main():
    ap = argparse.ArgumentParser(description="CAP: what the sources say per system (with origin)")
    ap.add_argument("--system", choices=sorted(SYSTEMS) + ["all"], default="all")
    ap.add_argument("--table", action="store_true", help="Brewer's table (STRAUCH p.35)")
    a = ap.parse_args()

    print("=" * 70)
    print("CAP in the sources (p.N = PDF page). PACELC is NOT IN THE SOURCE [extrapolation].")
    print("=" * 70)
    if a.table:
        print("Brewer's table [from source] (STRAUCH p.35):")
        for choice, traits, ex in BREWER_TABLE:
            print("- %s | characteristics: %s | examples: %s" % (choice, traits, ex))
        return 0
    keys = sorted(SYSTEMS) if a.system == "all" else [a.system]
    for k in keys:
        show(k)
    print("Warning: product labels (CP, AP, PA/EL, PC/EC) are [extrapolation]; they depend on configuration and version.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

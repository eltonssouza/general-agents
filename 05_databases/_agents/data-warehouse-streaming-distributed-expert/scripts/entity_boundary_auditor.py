#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entity_boundary_auditor.py - checklist of transactional boundaries between services.

SOURCE: ALL rules are [extrapolation] (general knowledge of distributed systems and Pat Helland's thesis).
The file Life-Beyond-Distributed-Transactions.pdf in the collection is actually an astrophysics paper (HD 30963), so
NO rule here is [from source] and NO page can be cited. Use it as a checklist, not as an authority.
Bridge to what the collection really covers: idempotent output and the output commit problem in streaming (STREAM p.18-20).

Usage: python -I entity_boundary_auditor.py [--cross-service-tx] [--uses-2pc] [--mutable-messages] [--no-idempotency]
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def audit(cross_service_tx, uses_2pc, mutable_messages, no_idempotency):
    findings = []
    if cross_service_tx or uses_2pc:
        findings.append((
            "Atomic transaction / 2PC across autonomous services.",
            "[extrapolation] 2PC holds locks while participants or the coordinator do not respond; under failure or partition it reduces availability. "
            "The phrase 'anti-availability' is usually attributed to Helland (source absent from the collection, not verified).",
            "[extrapolation] Consider keeping ACID inside each service and coordinating across services by messages (saga with compensation, outbox, idempotency); weigh cost and complexity."))
    if mutable_messages:
        findings.append((
            "Messages across boundaries are changed after being emitted.",
            "[extrapolation] Treating messages as immutable, versioned facts makes reprocessing and contract evolution easier.",
            "[extrapolation] Model events with a unique id and a schema version."))
    if no_idempotency:
        findings.append((
            "Consumer does not handle duplicates.",
            "[extrapolation] Channels with retries deliver duplicates; without idempotency, reprocessing corrupts state. "
            "[inference] Analogy with the collection: the STREAM survey shows that exactly-once on state still duplicates output and cites sinks with idempotent writes (STREAM p.17-20).",
            "[extrapolation] Idempotency key per message; idempotent write (upsert by key)."))
    return findings


def main():
    ap = argparse.ArgumentParser(description="[extrapolation] checklist of transactional boundaries (Helland source absent from the collection).")
    ap.add_argument("--cross-service-tx", action="store_true", help="there is an atomic transaction across services")
    ap.add_argument("--uses-2pc", action="store_true", help="uses two-phase commit/XA across services")
    ap.add_argument("--mutable-messages", action="store_true", help="messages change after being emitted")
    ap.add_argument("--no-idempotency", action="store_true", help="consumers do not handle duplicates")
    a = ap.parse_args()
    print("=" * 66)
    print("TRANSACTIONAL BOUNDARY CHECKLIST (all content = [extrapolation])")
    print("Helland source absent from the collection: no citable pages.")
    print("=" * 66)
    f = audit(a.cross_service_tx, a.uses_2pc, a.mutable_messages, a.no_idempotency)
    if not f:
        print("No warning signs in the items reported (this does not prove the architecture is correct).")
    for t, why, rec in f:
        print("\n[!] %s\n    Why: %s\n    Suggestion: %s" % (t, why, rec))
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())

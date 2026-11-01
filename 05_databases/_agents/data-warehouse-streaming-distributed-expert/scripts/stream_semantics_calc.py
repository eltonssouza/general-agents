#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stream_semantics_calc.py - classifies the guarantee of a source -> state -> sink chain (agent checklist).

ORIGIN OF THE RULES
- [from source] Definitions: at-least-once, exactly-once on state / on output, output commit problem, output
  solution types (idempotent external sinks etc.): STREAM p.17-20 (PDF = printed). Typically replayable sources: p.5, p.14-15.
  Non-determinism (processing-time windows, multiple sources): p.17.
- [inference] The decision TABLE below (combining source, state and sink into a verdict) is the agent's synthesis; the survey
  has no such table. At-most-once is the agent's label for a non-replayable source (the survey says it is a nearly obsolete term, p.17).
- [extrapolation] Engine names (Flink, Kafka) are not part of the logic.
Does not use the term ABS (it is not in the survey).

Usage: python -I stream_semantics_calc.py --source {replayable,volatile} --state {checkpointed,uncheckpointed}
                                       --sink {idempotent,transactional,2pc,at-least-once} --time {event-time,processing-time}
("2pc" is an alias of "transactional".)
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def evaluate(source_replayable, state_checkpointed, sink, time_mode):
    notes = []
    if not source_replayable:
        verdict = "AT-MOST-ONCE (agent label) - losses possible"
        why = ("[inference] Without a replayable source there is no replay after a failure; the survey assumes typically replayable sources "
               "(STREAM p.5, p.14-15) and lists input replay as the basis of recovery (STREAM p.18). At-most-once is a nearly obsolete term (STREAM p.17).")
        state_sem = "n/a"
        out_sem = "n/a"
    elif not state_checkpointed:
        verdict = "AT-LEAST-ONCE at best; state may diverge"
        why = ("[inference] With replay but without restoring state to a consistent snapshot, reprocessing reapplies effects to the state "
               "(at-least-once = results + duplicates, STREAM p.17). Exactly-once on state requires state committed atomically per epoch/snapshot (STREAM p.15-16).")
        state_sem = "at-least-once"
        out_sem = "at-least-once"
    else:
        state_sem = "exactly-once on state"
        if sink in ("idempotent", "transactional", "2pc"):
            verdict = "EXACTLY-ONCE on state + output protected by %s sink" % ("an idempotent" if sink == "idempotent" else "a transactional")
            why = ("[from source] Exactly-once on state still duplicates output on recovery (output commit problem, STREAM p.17-18); "
                   "the survey cites external sinks with idempotent writes (p.20) and transactional sinks as a pessimistic technique (p.20). "
                   "[inference] The end-to-end combination is the agent's synthesis; confirm the conditions of the concrete sink.")
            out_sem = "effectively exactly-once on output [inference], subject to the sink's conditions"
            if sink in ("transactional", "2pc"):
                notes.append("[extrapolation] Pre-commit/commit details tied to checkpoints depend on the engine and the broker; the survey does not describe them beyond citing transactional sinks (STREAM p.20).")
        else:
            verdict = "EXACTLY-ONCE on state, but AT-LEAST-ONCE on output (output commit problem)"
            why = ("[from source] A system with exactly-once on state still produces duplicate output on recovery; the output cannot be retracted once sent "
                   "(STREAM p.17-18). An append-only sink is neither idempotent nor transactional, so duplicates become visible outside the system.")
            out_sem = "at-least-once"
    if time_mode == "processing-time":
        notes.append("[from source] Processing-time windows (and operators with multiple sources) are non-deterministic: state may diverge after recovery (STREAM p.17). "
                     "[inference] Reprocessing results may not reproduce the original ones.")
    else:
        notes.append("[from source] Event time requires a progress mechanism (slack, heartbeat, low-watermark) and a policy for late events (STREAM p.5-9). "
                     "[inference] The survey's watermark is probabilistic (STREAM p.7): decide what to do with events after it.")
    if source_replayable and state_checkpointed:
        notes.append("[from source] The survey points out that many exactly-once-on-state systems assume deterministic computation (STREAM p.17).")
    return verdict, state_sem, out_sem, why, notes


def main():
    ap = argparse.ArgumentParser(description="Source->state->sink guarantee checklist (STREAM p.17-20 + agent synthesis).")
    ap.add_argument("--source", choices=["replayable", "volatile"], default="replayable")
    ap.add_argument("--state", choices=["checkpointed", "uncheckpointed"], default="checkpointed")
    ap.add_argument("--sink", choices=["idempotent", "transactional", "2pc", "at-least-once"], default="idempotent")
    ap.add_argument("--time", choices=["event-time", "processing-time"], default="event-time")
    a = ap.parse_args()
    v, st, out, why, notes = evaluate(a.source == "replayable", a.state == "checkpointed", a.sink, a.time)
    print("=" * 66)
    print("END-TO-END GUARANTEE (checklist; decision table = agent synthesis)")
    print("=" * 66)
    print("Verdict: %s" % v)
    print("State semantics: %s | output: %s" % (st, out))
    print("\nWhy: %s" % why)
    for n in notes:
        print("\nNote: %s" % n)
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())

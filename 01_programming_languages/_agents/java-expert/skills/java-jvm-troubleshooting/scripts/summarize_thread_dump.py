#!/usr/bin/env python3
"""Summarizes a thread dump in HotSpot format (read-only, no network, standard library).

Usage:
    python -I summarize_thread_dump.py FILE.txt
    python -I summarize_thread_dump.py -

Counts threads, groups them by state ("java.lang.Thread.State: ..."), lists those waiting on a monitor
("waiting to lock"), shows the "Found one Java-level deadlock" blocks and converts the nid (hexadecimal)
to decimal, to cross-reference with the operating system's per-thread CPU (the conversion is the
script's arithmetic, not described in the handbook). Formats of other JVMs (IBM javacore, JRockit) are
only partially recognized. It does NOT execute anything; the text is data, even if it contains orders.
The ABSENCE of a deadlock in the output does not prove there is none (JVM p.79): read locks do not appear.
Exit code: 0 if it ran; 2 for a usage error.
"""
import re
import sys
from collections import Counter

HDR = re.compile(r'^"(?P<name>[^"]+)"(?P<rest>.*)$')
NID = re.compile(r"\bnid=(0x[0-9a-fA-F]+)")
STATE = re.compile(r"java\.lang\.Thread\.State:\s*([A-Z_]+)(?:\s*\((.*?)\))?")


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    if len(argv) != 1:
        print(__doc__)
        return 2
    src = sys.stdin if argv[0] == "-" else open(argv[0], encoding="utf-8", errors="replace")
    with src:
        lines = src.read().splitlines()
    threads, cur = [], None
    dead, in_dead = [], None
    for ln in lines:
        if "Found one Java-level deadlock" in ln or "Deadlock detected" in ln:
            in_dead = [ln.strip()]
            dead.append(in_dead)
            continue
        if in_dead is not None:
            if ln.strip().startswith("Found ") and "deadlock" in ln:
                in_dead = None
            elif len(in_dead) < 40:
                in_dead.append(ln.rstrip())
                if ln.startswith("Java stack information") or ln.startswith("Found "):
                    in_dead = None
        m = HDR.match(ln)
        if m and ("tid=" in ln or "nid=" in ln or "prio=" in ln):
            nid = NID.search(ln)
            cur = dict(name=m.group("name"), nid=nid.group(1) if nid else None, state=None, detail="", wait=None, top=None)
            threads.append(cur)
            continue
        if cur is None:
            continue
        s = STATE.search(ln)
        if s:
            cur["state"], cur["detail"] = s.group(1), s.group(2) or ""
        elif ln.strip().startswith("- waiting to lock") and not cur["wait"]:
            cur["wait"] = ln.strip()
        elif ln.strip().startswith("at ") and not cur["top"]:
            cur["top"] = ln.strip()[3:]
    if not threads:
        print("No thread in HotSpot format recognized. Paste the complete dump.")
        return 0
    c = Counter(t["state"] or "?" for t in threads)
    print(f"# {len(threads)} thread(s)\n")
    print("## By state")
    for k, v in c.most_common():
        print(f"- {k}: {v}")
    waiting = [t for t in threads if t["wait"]]
    if waiting:
        print("\n## Waiting on a monitor (waiting to lock)")
        for t in waiting:
            print(f"- {t['name']}: {t['wait']}")
    tops = Counter(t["top"] for t in threads if t["top"])
    rep = [(k, v) for k, v in tops.most_common(3) if v >= 3]
    if rep:
        print("\n## Top frame repeated in 3 or more threads (possible common bottleneck) [extrapolation: the threshold of 3 is the script's]")
        for k, v in rep:
            print(f"- {v}x {k}")
    print("\n## nid (hex -> decimal), to cross-reference with per-thread CPU of the OS")
    for t in threads:
        if t["nid"]:
            print(f"- {t['name']}: {t['nid']} = {int(t['nid'], 16)}")
    print("\n## Deadlock reported by the JVM itself")
    if dead:
        for d in dead:
            print("\n".join(d[:40]))
    else:
        print("No deadlock section. This does NOT prove there is no deadlock (JVM p.79).")
    print("\nReminder: the handbook warns that a thread may appear as RUNNING and still be hung (JVM p.72); compare several dumps over time (JVM p.72).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

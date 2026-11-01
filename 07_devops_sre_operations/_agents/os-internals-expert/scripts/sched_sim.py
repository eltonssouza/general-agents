# -*- coding: utf-8 -*-
"""
sched_sim.py - deterministic scheduling simulators (OSTEP, ch.7-9).

Definitions from the book (PDF p.291, 295):
  turnaround = T_completion - T_arrival      (Eq.7.1)
  response   = T_firstrun   - T_arrival      (Eq.7.2)
Policies: FIFO, SJF (non-preemptive), STCF/PSJF (preemptive), RR (ch.7);
MLFQ with the 5 final rules (ch.8, p.389); stride (ch.9, p.470-471);
CFS: time slice and vruntime (ch.9, p.472-474, Eq.9.1 and 9.2).

No network, stdlib only, deterministic output. Usage (from the package folder):
  python -I scripts/sched_sim.py run  --policy FIFO --jobs "A:0:100,B:0:10,C:0:10"
  python -I scripts/sched_sim.py run  --policy RR --quantum 1 --jobs "A:0:5,B:0:5,C:0:5"
  python -I scripts/sched_sim.py mlfq --jobs "A:0:200,B:100:20" --queues 3 --quantum 10 --boost 0
  python -I scripts/sched_sim.py stride --tickets "A:100,B:50,C:250" --slices 8
  python -I scripts/sched_sim.py cfs-slice --nice "A:-5,B:0"
  python -I scripts/sched_sim.py cfs-run --jobs "A:-5,B:0" --ticks 48

Job format (run): NAME:ARRIVAL:LENGTH. In mlfq: NAME:ARRIVAL:LENGTH[:IO_EVERY[:IO_LENGTH]]
(IO_EVERY = ms of CPU between I/O requests; the job stays blocked for IO_LENGTH ms).

CONVENTIONS NOT SPECIFIED BY THE BOOK (declared, [inference]):
  - tie-break: order in which the jobs were listed;
  - RR: a new job arriving at the same instant a quantum expires enters the queue BEFORE the preempted job;
  - STCF: on a tie in remaining time, the running job continues;
  - MLFQ: a job returning from I/O goes to the end of its queue; a job preempted by priority stays at the front of its queue.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# prio_to_weight[40] table from the book (PDF p.473), nice -20 .. +19.
PRIO_TO_WEIGHT = [
    88761, 71755, 56483, 46273, 36291,
    29154, 23254, 18705, 14949, 11916,
    9548, 7620, 6100, 4904, 3906,
    3121, 2501, 1991, 1586, 1277,
    1024, 820, 655, 526, 423,
    335, 272, 215, 172, 137,
    110, 87, 70, 56, 45,
    36, 29, 23, 18, 15,
]


def weight_of(nice):
    if not -20 <= nice <= 19:
        raise SystemExit("nice must be between -20 and 19 (book p.473)")
    return PRIO_TO_WEIGHT[nice + 20]


def parse_jobs(spec, extra=False):
    jobs = []
    for i, tok in enumerate([t for t in spec.split(",") if t.strip()]):
        parts = tok.strip().split(":")
        if len(parts) < 3:
            raise SystemExit(f"invalid job '{tok}': use NAME:ARRIVAL:LENGTH")
        j = {"name": parts[0], "arrival": int(parts[1]), "length": int(parts[2]), "order": i,
             "io_every": 0, "io_len": 0}
        if extra and len(parts) >= 4:
            j["io_every"] = int(parts[3])
            j["io_len"] = int(parts[4]) if len(parts) >= 5 else 0
        jobs.append(j)
    if not jobs:
        raise SystemExit("no job given")
    return jobs


def finalize(jobs, comp, first, timeline):
    rows = []
    for j in jobs:
        n = j["name"]
        ta = comp[n] - j["arrival"]
        tr = first[n] - j["arrival"]
        rows.append({"job": n, "arrival": j["arrival"], "length": j["length"], "first_run": first[n],
                     "completion": comp[n], "turnaround": ta, "response": tr, "wait": ta - j["length"]})
    return rows, timeline


def compress(tl):
    out = []
    for t, n in tl:
        if out and out[-1][2] == n and out[-1][1] == t:
            out[-1][1] = t + 1
        else:
            out.append([t, t + 1, n])
    return out


def sim_run(jobs, policy, quantum=1):
    """Discrete time unit (1). CPU-only policies (assumptions 1-5 relaxed: arrivals and lengths are free)."""
    rem = {j["name"]: j["length"] for j in jobs}
    comp, first, tl = {}, {}, []
    t = 0
    done = 0
    n = len(jobs)
    order = {j["name"]: j["order"] for j in jobs}
    arr = {j["name"]: j["arrival"] for j in jobs}
    rr_queue = []
    rr_enqueued = set()
    cur = None
    slice_left = 0
    fifo_cur = None
    guard = 0
    while done < n:
        guard += 1
        if guard > 10_000_000:
            raise SystemExit("simulation did not finish")
        # arrivals (RR: enter the queue in arrival/listing order)
        if policy == "RR":
            for j in sorted(jobs, key=lambda x: (x["arrival"], x["order"])):
                if j["arrival"] <= t and j["name"] not in rr_enqueued:
                    rr_queue.append(j["name"])
                    rr_enqueued.add(j["name"])
        ready = [j["name"] for j in jobs if arr[j["name"]] <= t and rem[j["name"]] > 0]
        if not ready:
            t += 1
            continue
        if policy == "FIFO":
            if fifo_cur is None or rem[fifo_cur] == 0:
                fifo_cur = min(ready, key=lambda x: (arr[x], order[x]))
            pick = fifo_cur
        elif policy == "SJF":
            if cur is None or rem[cur] == 0:
                cur = min(ready, key=lambda x: (rem[x], order[x]))
            pick = cur
        elif policy == "STCF":
            best = min(ready, key=lambda x: (rem[x], order[x]))
            if cur is not None and cur in ready and rem[cur] == rem[best]:
                best = cur
            cur = best
            pick = cur
        elif policy == "RR":
            if cur is None or rem[cur] == 0 or slice_left == 0:
                if cur is not None and rem[cur] > 0 and slice_left == 0:
                    # new arrivals at t enter before the preempted job
                    for j in sorted(jobs, key=lambda x: (x["arrival"], x["order"])):
                        if j["arrival"] <= t and j["name"] not in rr_enqueued:
                            rr_queue.append(j["name"])
                            rr_enqueued.add(j["name"])
                    rr_queue.append(cur)
                cur = rr_queue.pop(0)
                slice_left = quantum
            pick = cur
        else:
            raise SystemExit("unknown policy (FIFO, SJF, STCF, RR)")
        first.setdefault(pick, t)
        tl.append((t, pick))
        rem[pick] -= 1
        t += 1
        if policy == "RR":
            slice_left -= 1
        if rem[pick] == 0:
            comp[pick] = t
            done += 1
            if policy == "RR":
                cur = None
                slice_left = 0
    return finalize(jobs, comp, first, tl)


def sim_mlfq(jobs, nq, quanta, allots, boost, old_rules, max_t=1_000_000):
    """MLFQ from the book (p.389): Rule1 priority; Rule2 RR within the queue (queue quantum); Rule3 enters at the top;
    Rule4 total allotment per level (old_rules: Rules 4a/4b, allotment resets when the job yields the CPU for I/O);
    Rule5 boost every S. Level nq-1 = top."""
    rem = {j["name"]: j["length"] for j in jobs}
    arr = {j["name"]: j["arrival"] for j in jobs}
    spec = {j["name"]: j for j in jobs}
    level = {}
    queues = [[] for _ in range(nq)]
    slice_used = {j["name"]: 0 for j in jobs}
    allot_used = {j["name"]: 0 for j in jobs}
    since_io = {j["name"]: 0 for j in jobs}
    blocked = {}  # name -> instant at which it returns
    comp, first, tl = {}, {}, []
    admitted = set()
    done, t = 0, 0
    running = None
    while done < len(jobs):
        if t > max_t:
            raise SystemExit("time limit exceeded")
        # boost (Rule 5)
        if boost and t > 0 and t % boost == 0:
            for q in range(nq - 1):
                for nme in queues[q]:
                    level[nme] = nq - 1
                    queues[nq - 1].append(nme)
                queues[q] = []
            for nme in list(blocked):
                level[nme] = nq - 1
            for nme in level:
                slice_used[nme] = 0
                allot_used[nme] = 0
        # arrivals (Rule 3)
        for j in jobs:
            if arr[j["name"]] <= t and j["name"] not in admitted:
                admitted.add(j["name"])
                level[j["name"]] = nq - 1
                queues[nq - 1].append(j["name"])
        # return from I/O
        for nme in [k for k, v in blocked.items() if v <= t]:
            del blocked[nme]
            queues[level[nme]].append(nme)
            slice_used[nme] = 0
            if old_rules:
                allot_used[nme] = 0  # old Rule 4b
        # pick the highest-priority job (Rule 1)
        top = None
        for q in range(nq - 1, -1, -1):
            if queues[q]:
                top = q
                break
        if top is None:
            tl.append((t, "-"))
            t += 1
            continue
        pick = queues[top][0]
        first.setdefault(pick, t)
        tl.append((t, pick))
        rem[pick] -= 1
        slice_used[pick] += 1
        allot_used[pick] += 1
        since_io[pick] += 1
        t += 1
        lv = level[pick]
        if rem[pick] == 0:
            queues[lv].remove(pick)
            comp[pick] = t
            done += 1
            continue
        sp = spec[pick]
        if sp["io_every"] and since_io[pick] >= sp["io_every"]:
            queues[lv].remove(pick)
            since_io[pick] = 0
            blocked[pick] = t + sp["io_len"]
            continue
        if allot_used[pick] >= allots[lv]:
            queues[lv].remove(pick)
            allot_used[pick] = 0
            slice_used[pick] = 0
            if lv > 0:
                level[pick] = lv - 1
            queues[level[pick]].append(pick)  # end of the queue (Rule 4)
        elif slice_used[pick] >= quanta[lv]:
            queues[lv].remove(pick)
            slice_used[pick] = 0
            queues[lv].append(pick)  # RR (Rule 2)
    return finalize(jobs, comp, first, tl)


def print_table(rows, tl, show_tl=True):
    print(f"{'job':<6}{'arrival':>8}{'len':>6}{'1st run':>9}{'finish':>9}{'turnaround':>12}{'response':>10}{'wait*':>9}")
    for r in rows:
        print(f"{r['job']:<6}{r['arrival']:>8}{r['length']:>6}{r['first_run']:>9}{r['completion']:>9}"
              f"{r['turnaround']:>12}{r['response']:>10}{r['wait']:>9}")
    n = len(rows)
    ta = sum(r["turnaround"] for r in rows) / n
    tr = sum(r["response"] for r in rows) / n
    print(f"mean turnaround = {ta:.2f}   mean response = {tr:.2f}")
    print("*wait = turnaround - length (only meaningful without I/O) [inference]; the book defines only turnaround and response (p.291, p.295)")
    if show_tl:
        segs = compress(tl)
        print("timeline: " + " ".join(f"[{a}-{b}) {nme}" for a, b, nme in segs))


def cmd_run(a):
    jobs = parse_jobs(a.jobs)
    rows, tl = sim_run(jobs, a.policy.upper(), a.quantum)
    print_table(rows, tl, not a.no_timeline)


def cmd_mlfq(a):
    jobs = parse_jobs(a.jobs, extra=True)
    quanta = [int(x) for x in a.quanta.split(",")] if a.quanta else [a.quantum] * a.queues
    # --quanta lists values from level 0 (lowest) to the top
    if len(quanta) != a.queues:
        raise SystemExit("--quanta needs one value per queue (from level 0 to the top)")
    allots = [int(x) for x in a.allot.split(",")] if a.allot else list(quanta)
    if len(allots) != a.queues:
        raise SystemExit("--allot needs one value per queue")
    rows, tl = sim_mlfq(jobs, a.queues, quanta, allots, a.boost, a.old_rules)
    print(f"MLFQ: queues={a.queues} (level {a.queues-1}=top) quanta={quanta} allotment={allots} boost S={a.boost or 'none'}"
          f" rules={'old 4a/4b (p.382)' if a.old_rules else 'final 1-5 (p.389)'}")
    print_table(rows, tl, not a.no_timeline)


def cmd_stride(a):
    tick = {}
    for tok in a.tickets.split(","):
        n, v = tok.split(":")
        tick[n.strip()] = int(v)
    names = list(tick)
    stride = {n: a.big // tick[n] for n in names}
    pas = {n: 0 for n in names}
    print(f"stride = {a.big} / tickets -> {stride}")
    seq = []
    for _ in range(a.slices):
        nxt = min(names, key=lambda x: (pas[x], names.index(x)))
        pas[nxt] += stride[nxt]
        seq.append(nxt)
        print(f"  runs {nxt}; pass -> {dict(pas)}")
    cnt = {n: seq.count(n) for n in names}
    print("sequence:", " ".join(seq), "| count:", cnt)
    print("Book (p.470-471): A=100, B=50, C=250 tickets, big=10000 -> strides 100/200/40; cycle A B C C C A C C (C 5x, A 2x, B 1x).")


def cmd_cfs_slice(a):
    nices = {}
    for tok in a.nice.split(","):
        n, v = tok.split(":")
        nices[n.strip()] = int(v)
    w = {n: weight_of(v) for n, v in nices.items()}
    total = sum(w.values())
    print(f"sched_latency={a.latency} ms; min_granularity={a.min_gran} ms; weights (prio_to_weight): {w}")
    for n in nices:
        raw = w[n] / total * a.latency
        sl = max(raw, a.min_gran)
        print(f"  {n}: time_slice = {w[n]}/{total} x {a.latency} = {raw:.2f} ms"
              + (f" -> min_granularity => {sl:.2f} ms" if sl != raw else ""))
    print("Equal-nice, n procs: slice = sched_latency/n, with min_granularity as a floor (book p.472-473). "
          "Note: the book applies min_granularity to the unweighted case; with weights the floor is [inference].")


def cmd_cfs_run(a):
    jobs = {}
    for tok in a.jobs.split(","):
        n, v = tok.split(":")
        jobs[n.strip()] = int(v)
    names = list(jobs)
    w = {n: weight_of(jobs[n]) for n in names}
    vr = {n: 0.0 for n in names}
    ran = {n: 0 for n in names}
    t = 0
    print("Simplified CFS (vruntime += 1024/weight x time; runs the lowest vruntime; switches every slice) - Eq.9.1/9.2 (p.473-474)")
    while t < a.ticks:
        total = sum(w.values())
        nxt = min(names, key=lambda x: (vr[x], names.index(x)))
        sl = max(w[nxt] / total * a.latency, a.min_gran)
        step = min(sl, a.ticks - t)
        vr[nxt] += 1024 / w[nxt] * step
        ran[nxt] += step
        t += step
        print(f"  t={t:7.2f} runs {nxt} for {step:.2f} ms; vruntime={ {k: round(v, 2) for k, v in vr.items()} }")
    tot = sum(ran.values())
    print("CPU share obtained:", {k: round(v / tot, 3) for k, v in ran.items()})


def main():
    ap = argparse.ArgumentParser(description="OSTEP scheduling simulators")
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("--policy", required=True, choices=["FIFO", "SJF", "STCF", "RR", "fifo", "sjf", "stcf", "rr"])
    r.add_argument("--jobs", required=True)
    r.add_argument("--quantum", type=int, default=1)
    r.add_argument("--no-timeline", action="store_true")
    r.set_defaults(f=cmd_run)
    m = sp.add_parser("mlfq")
    m.add_argument("--jobs", required=True)
    m.add_argument("--queues", type=int, default=3)
    m.add_argument("--quantum", type=int, default=10)
    m.add_argument("--quanta", default="")
    m.add_argument("--allot", default="")
    m.add_argument("--boost", type=int, default=0, help="S in ms; 0 = no boost")
    m.add_argument("--old-rules", action="store_true", help="rules 4a/4b (allows gaming)")
    m.add_argument("--no-timeline", action="store_true")
    m.set_defaults(f=cmd_mlfq)
    s = sp.add_parser("stride")
    s.add_argument("--tickets", required=True)
    s.add_argument("--slices", type=int, default=8)
    s.add_argument("--big", type=int, default=10000)
    s.set_defaults(f=cmd_stride)
    c = sp.add_parser("cfs-slice")
    c.add_argument("--nice", required=True)
    c.add_argument("--latency", type=float, default=48.0)
    c.add_argument("--min-gran", type=float, default=6.0)
    c.set_defaults(f=cmd_cfs_slice)
    c2 = sp.add_parser("cfs-run")
    c2.add_argument("--jobs", required=True)
    c2.add_argument("--ticks", type=float, default=96.0)
    c2.add_argument("--latency", type=float, default=48.0)
    c2.add_argument("--min-gran", type=float, default=6.0)
    c2.set_defaults(f=cmd_cfs_run)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

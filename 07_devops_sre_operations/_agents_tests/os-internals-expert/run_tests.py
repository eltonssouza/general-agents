# -*- coding: utf-8 -*-
"""
run_tests.py - automated tests of the package scripts against the numerical examples of OSTEP.

Usage (from any folder): python -I tests/run_tests.py
Each test calls the script with `python -I`, captures the output and checks the values the BOOK publishes (with the PDF page).
Exit 0 if all pass. No network; deterministic.
"""
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(PKG, "scripts")
results = []


def run(script, *args):
    p = subprocess.run([sys.executable, "-I", os.path.join(S, script)] + list(args), capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))


def has(out, *subs):
    return all(s in out for s in subs)


# ---------------------------------------------------------------- sched_sim
rc, o = run("sched_sim.py", "run", "--policy", "FIFO", "--jobs", "A:0:10,B:0:10,C:0:10", "--no-timeline")
check("T01 FIFO 10/10/10 mean turnaround 20 (p.292)", "mean turnaround = 20.00" in o, o[-200:])
rc, o = run("sched_sim.py", "run", "--policy", "FIFO", "--jobs", "A:0:100,B:0:10,C:0:10", "--no-timeline")
check("T02 FIFO convoy turnaround 110 (p.292)", "mean turnaround = 110.00" in o)
rc, o = run("sched_sim.py", "run", "--policy", "SJF", "--jobs", "A:0:100,B:0:10,C:0:10", "--no-timeline")
check("T03 SJF turnaround 50 (p.293)", "mean turnaround = 50.00" in o)
rc, o = run("sched_sim.py", "run", "--policy", "SJF", "--jobs", "A:0:100,B:10:10,C:10:10", "--no-timeline")
check("T04 SJF with late arrivals 103.33 (p.294)", "mean turnaround = 103.33" in o)
rc, o = run("sched_sim.py", "run", "--policy", "STCF", "--jobs", "A:0:100,B:10:10,C:10:10", "--no-timeline")
check("T05 STCF turnaround 50 and response 3.33 (p.295-296)", has(o, "mean turnaround = 50.00", "mean response = 3.33"))
rc, o = run("sched_sim.py", "run", "--policy", "RR", "--quantum", "1", "--jobs", "A:0:5,B:0:5,C:0:5", "--no-timeline")
check("T06 RR slice 1: finish 13,14,15; mean response 1 (p.297)", has(o, "mean turnaround = 14.00", "mean response = 1.00") and re.search(r"A\s+0\s+5\s+0\s+13", o))
rc, o = run("sched_sim.py", "run", "--policy", "SJF", "--jobs", "A:0:5,B:0:5,C:0:5", "--no-timeline")
check("T07 SJF mean response 5 (p.297)", "mean response = 5.00" in o)
rc, o = run("sched_sim.py", "stride", "--tickets", "A:100,B:50,C:250", "--slices", "8")
check("T08 stride A B C C C A C C (p.470-471)", "sequence: A B C C C A C C" in o and "'C': 5" in o)
rc, o = run("sched_sim.py", "cfs-slice", "--nice", "A:-5,B:0")
check("T09 CFS nice -5 and 0: weights 3121/1024 and ~36/12 ms (p.473-474)", has(o, "3121", "1024", "36.14", "11.86"))
rc, o = run("sched_sim.py", "mlfq", "--jobs", "A:0:200,B:100:20", "--queues", "3", "--quantum", "10", "--no-timeline")
check("T10 MLFQ: B (20 ms) arrives at 100 and finishes at 120 (p.383)", re.search(r"B\s+100\s+20\s+100\s+120", o) is not None)
# gaming: long A vs B doing I/O before the allotment runs out
rc, o_old = run("sched_sim.py", "mlfq", "--jobs", "A:0:200,B:0:200:9:1", "--queues", "3", "--quanta", "10,10,10", "--old-rules", "--no-timeline")
rc, o_new = run("sched_sim.py", "mlfq", "--jobs", "A:0:200,B:0:200:9:1", "--queues", "3", "--quanta", "10,10,10", "--no-timeline")
ta_old = re.search(r"A\s+0\s+200\s+\d+\s+(\d+)", o_old)
ta_new = re.search(r"A\s+0\s+200\s+\d+\s+(\d+)", o_new)
check("T11 gaming: with rules 4a/4b job A finishes later than with the final rule 4 (p.384-387)",
      ta_old and ta_new and int(ta_old.group(1)) > int(ta_new.group(1)), f"old={ta_old and ta_old.group(1)} new={ta_new and ta_new.group(1)}")

# ---------------------------------------------------------------- vm_sim
rc, o = run("vm_sim.py", "linear", "--va-bits", "6", "--page-size", "16", "--map", "0:3,1:7,2:5,3:2", "--va", "21")
check("T12 paging: VA 21 -> PA 117 (p.481-483)", has(o, "VPN 1", "offset 5", "PFN 7", "PA 117"))
rc, o = run("vm_sim.py", "base-bounds", "--base", "16384", "--bounds", "4096", "--va", "0,1024,3000,4400")
check("T13 base/bounds: 3000 -> 19384; 4400 faults (p.205)", has(o, "19384", "Fault"))
rc, o = run("vm_sim.py", "segments", "--va-bits", "14", "--seg-bits", "2", "--va", "100,4200,15360", "--seg", "0:32768:2048:+,1:34816:3072:+,3:28672:2048:-")
check("T14 segments: 32868, 34920, 27648 (27KB) (p.305-308)", has(o, "PA 32868", "PA 34920", "PA 27648"))
rc, o = run("vm_sim.py", "multilevel", "--va-bits", "14", "--page-size", "64", "--pt-index-bits", "4", "--pd", "0:100,15:101",
            "--pt", "100:0=10;1=23;4=80;5=59|101:14=55;15=45", "--va", "0x3F80")
check("T15 2 levels: VA 0x3F80 -> PA 0x0DC0 (p.605)", has(o, "PFN 55", "PA 0x0DC0"))
rc, o = run("vm_sim.py", "tlb", "--page-size", "16", "--entries", "4", "--va", "100,104,108,112,116,120,124,128,132,136")
check("T16 TLB: miss,hit,hit,miss,hit,hit,hit,miss,hit,hit = 70% (p.544)", has(o, "miss, hit, hit, miss, hit, hit, hit, miss, hit, hit", "70.0%"))
rc, o = run("vm_sim.py", "replace", "--policy", "OPT", "--frames", "3", "--refs", "0,1,2,0,1,3,0,3,1,2,1")
check("T17 OPT 54.5% / 85.7% without compulsory (p.693)", has(o, "6 hits", "54.5%", "85.7%"))
rc, o = run("vm_sim.py", "replace", "--policy", "FIFO", "--frames", "3", "--refs", "0,1,2,0,1,3,0,3,1,2,1")
check("T18 FIFO 36.4% / 57.1% (p.694)", has(o, "4 hits", "36.4%", "57.1%"))
rc, o = run("vm_sim.py", "replace", "--policy", "LRU", "--frames", "3", "--refs", "0,1,2,0,1,3,0,3,1,2,1")
check("T19 LRU = OPT in the example (p.696-697)", has(o, "6 hits", "54.5%"))
rc, o3 = run("vm_sim.py", "replace", "--policy", "FIFO", "--frames", "3", "--refs", "1,2,3,4,1,2,5,1,2,3,4,5")
rc, o4 = run("vm_sim.py", "replace", "--policy", "FIFO", "--frames", "4", "--refs", "1,2,3,4,1,2,5,1,2,3,4,5")
h3 = int(re.search(r"(\d+) hits", o3).group(1))
h4 = int(re.search(r"(\d+) hits", o4).group(1))
check("T20 Belady's Anomaly: FIFO with 4 frames has fewer hits than with 3 (p.694)", h4 < h3, f"3 frames={h3} hits; 4 frames={h4} hits")
refs = ",".join(str(i % 50) for i in range(10000))
rc, o = run("vm_sim.py", "replace", "--policy", "LRU", "--frames", "49", "--refs", refs)
rc, o2 = run("vm_sim.py", "replace", "--policy", "FIFO", "--frames", "49", "--refs", refs)
check("T21 looping-sequential of 50 pages with cache 49: LRU and FIFO 0% (p.699)", "0 hits" in o and "0 hits" in o2)
rc, o = run("vm_sim.py", "amat", "--tm", "100e-9", "--td", "10e-3", "--hit", "0.9")
check("T22 AMAT ~1.0001 ms (p.691)", "1.0001 ms" in o)
rc, o = run("vm_sim.py", "sizes", "--va-bits", "32", "--page-size", "4096", "--procs", "100")
check("T23 linear table 4 MiB and 400 MiB with 100 processes (p.483-484)", has(o, "4.000 MiB", "400.0 MiB"))

# ---------------------------------------------------------------- storage_calc
rc, o = run("storage_calc.py", "disk", "--seek-ms", "4", "--rpm", "15000", "--size-kb", "4", "--mbps", "125")
m = re.search(r"R_I/O = .* = ([\d.]+) MB/s", o)
check("T24 Cheetah disk 4 KB: ~6 ms and ~0.66 MB/s (p.151-152)", m and abs(float(m.group(1)) - 0.66) < 0.02 and "T_I/O = 4.0 + 2.000" in o)
rc, o = run("storage_calc.py", "disk", "--seek-ms", "7", "--rot-ms", "3", "--rpm", "10000", "--size-kb", "10240", "--mbps", "50", "--kb-per-mb", "1024")
check("T25 RAID example S: 10 MB in 210 ms = 47.62 MB/s (p.241)", "47.619" in o or "47.62" in o)
rc, o = run("storage_calc.py", "raid-map", "--level", "0", "--disks", "4", "--block", "14")
check("T26 RAID-0 block 14 on 4 disks: disk 2 offset 3 (p.239)", has(o, "= 2", "= 3"))
rc, o = run("storage_calc.py", "parity", "--data", "0,0,1,1", "--lost", "2")
check("T27 XOR and reconstruction (p.244-245)", has(o, "= 0", "= 1"))
rc, o = run("storage_calc.py", "amortize", "--pos-ms", "10", "--mbps", "100", "--frac", "0.9")
check("T28 LFS: D = 9 MB for F=0.9 (p.627)", "9.0000 MB" in o)
rc, o = run("storage_calc.py", "amortize", "--pos-ms", "10", "--mbps", "40", "--frac", "0.5")
check("T29 FFS: 409.6 KB chunk for 50% (p.522)", "409.6 KB" in o)
rc, o = run("storage_calc.py", "inode", "--inumber", "32")
check("T30 inode 32 -> 20 KB -> sector 40 (p.433)", has(o, "20480", "sector", "= 40"))
rc, o = run("storage_calc.py", "fsize")
check("T31 12 direct + 1 indirect = 4144 KB (p.434)", "4144.0 KiB" in o)
rc, o = run("storage_calc.py", "checksum", "--hex", "365e,c4cd,ba14,8a92,ecef,2c3a,40be,f666", "--width", "4")
check("T32 XOR checksum 0x201b9403 (p.712)", "0x201b9403" in o)
rc, o = run("storage_calc.py", "raid", "--n", "4", "--b", "1000", "--s", "100", "--r", "1")
check("T33 RAID-5 random write N/4 R (p.249)", re.search(r"RAID-5\s+3000.*\s1\s+T/2T", o) is not None and "RAID-4" in o)

# ---------------------------------------------------------------- os_lookup
rc, o = run("os_lookup.py", "mlfq")
check("T34 lookup mlfq -> p.380-389", "p.380-389" in o and rc == 0)
rc, o = run("os_lookup.py", "docker")
check("T35 lookup docker -> NOT COVERED", "NOT COVERED" in o and rc == 2)
rc, o = run("os_lookup.py", "io_uring")
check("T36 lookup io_uring -> NOT COVERED", "NOT COVERED" in o)
rc, o = run("os_lookup.py", "xyzzy")
check("T37 lookup unknown term -> NOT COVERED in the index", "NOT COVERED" in o)

fails = [r for r in results if not r[1]]
for n, ok, d in results:
    print(("PASS " if ok else "FAIL ") + n + (f"   [{d}]" if (not ok and d) else ""))
print(f"\n{len(results) - len(fails)}/{len(results)} tests passed")
sys.exit(1 if fails else 0)

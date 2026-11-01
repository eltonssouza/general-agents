# -*- coding: utf-8 -*-
"""
analyze_hash_probes.py - deterministic simulator of the LinearHashTable of "Open Data Structures" (Pat Morin,
Edition 0.1Gbeta, Sec. 5.2, ODS p.120-127). Pages = PDF (printed = N - 12).

Rules followed from the book:
  - three kinds of entry: data, nil (never held data) and del (held data that was deleted) (ODS p.121);
  - n counts data and q counts data + del; invariant length(t) >= 2q, length(t) = 2^d (ODS p.121);
  - find probes until it finds x or nil; del does not stop it (ODS p.121-122);
  - add: find first; if 2(q+1) > length(t), resize; reuses nil or del; q only grows if the cell was nil (ODS p.122);
  - remove writes del; if 8n < length(t), resize (ODS p.122-123);
  - resize: smallest d with 2^d >= 3n; reinserts only data; q = n (ODS p.123).
The hash function used here is x mod length(t) (didactic, [extrapolation]); the book uses multiplicative hashing (p.116).
Demos: tombstones (removal with del), naive_failure (removal writing nil: false negative, [inference] from p.123),
invariant (mass insert/remove and check length(t) >= 2q). No network.
Usage: python -I analyze_hash_probes.py --demo tombstones
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEL = "<del>"


class LinearHashTableSim:
    def __init__(self, d=1):
        self.d = d
        self.t = [None] * (2 ** d)
        self.n = 0
        self.q = 0
        self.resizes = 0

    def hash(self, x):
        return x % len(self.t)

    def find(self, x):
        i = self.hash(x)
        path = []
        while self.t[i] is not None:
            path.append(i)
            if self.t[i] != DEL and self.t[i] == x:
                return True, path
            i = (i + 1) % len(self.t)
        return False, path

    def add(self, x):
        if self.find(x)[0]:
            return False
        if 2 * (self.q + 1) > len(self.t):
            self.resize()
        i = self.hash(x)
        while self.t[i] is not None and self.t[i] != DEL:
            i = (i + 1) % len(self.t)
        if self.t[i] is None:
            self.q += 1
        self.n += 1
        self.t[i] = x
        return True

    def remove(self, x):
        i = self.hash(x)
        while self.t[i] is not None:
            y = self.t[i]
            if y != DEL and y == x:
                self.t[i] = DEL
                self.n -= 1
                if 8 * self.n < len(self.t):
                    self.resize()
                return True
            i = (i + 1) % len(self.t)
        return False

    def remove_naive(self, x):
        """Didactic mistake: writes nil instead of del (ODS p.123 shows why this is not done)."""
        i = self.hash(x)
        while self.t[i] is not None:
            if self.t[i] != DEL and self.t[i] == x:
                self.t[i] = None
                self.n -= 1
                self.q -= 1
                return True
            i = (i + 1) % len(self.t)
        return False

    def resize(self):
        self.resizes += 1
        d = 1
        while (2 ** d) < 3 * self.n:
            d += 1
        old = self.t
        self.d = d
        self.t = [None] * (2 ** d)
        self.q = self.n
        for x in old:
            if x is not None and x != DEL:
                i = self.hash(x)
                while self.t[i] is not None:
                    i = (i + 1) % len(self.t)
                self.t[i] = x

    def invariant(self):
        return len(self.t) >= 2 * self.q and len(self.t) == 2 ** self.d


def show(sim):
    for i, v in enumerate(sim.t):
        print("  t[%d] = %s" % (i, "nil" if v is None else v))
    print("  n=%d  q=%d  length(t)=%d  invariant length(t) >= 2q: %s" % (sim.n, sim.q, len(sim.t), sim.invariant()))


def run_demo(mode):
    if mode == "invariant":
        sim = LinearHashTableSim()
        ok = True
        for k in range(1, 2001):
            sim.add(k * 7)
            ok = ok and sim.invariant()
        for k in range(1, 1951):
            sim.remove(k * 7)
            ok = ok and sim.invariant()
        print("After 2000 adds and 1950 removes: n=%d q=%d length(t)=%d resizes=%d" % (sim.n, sim.q, len(sim.t), sim.resizes))
        print("Invariant length(t) >= 2q maintained in all operations: %s [from source] (ODS p.121, 123)" % ok)
        return 0 if ok else 1
    sim = LinearHashTableSim(d=3)  # length(t) = 8
    for x in (10, 18, 26):  # all have x mod 8 = 2
        sim.add(x)
    print("Initial state (keys 10, 18, 26 collide at t[2]):")
    show(sim)
    print("\n--- Removing the middle key 18 ---")
    if mode == "tombstones":
        sim.remove(18)
        print("Correct removal: the cell gets del [from source] (ODS p.122-123)")
    else:
        sim.remove_naive(18)
        print("Naive removal: the cell gets nil (not what the book does) [inference]")
    show(sim)
    found, path = sim.find(26)
    print("\n--- find(26) ---")
    print("Cells probed: %s; found: %s" % (path, found))
    if mode == "tombstones":
        print("Verdict: CORRECT; find does not stop at del [from source] (ODS p.121-122).")
        return 0
    print("Verdict: FALSE NEGATIVE; find stopped at the wrongly written nil [inference] from ODS p.123.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="LinearHashTable simulator (Open Data Structures, Morin)")
    ap.add_argument("--demo", choices=["tombstones", "naive_failure", "invariant"], default="tombstones")
    a = ap.parse_args(argv)
    print("=== LinearHashTable (pages = PDF; printed = N - 12). 'tombstone' is an external label: the book says 'del' ===")
    return run_demo(a.demo)


if __name__ == "__main__":
    sys.exit(main())

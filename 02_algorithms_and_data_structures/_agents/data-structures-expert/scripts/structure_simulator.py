# -*- coding: utf-8 -*-
"""
structure_simulator.py - deterministic amortized-cost simulator that follows the pseudocode of
"Open Data Structures" (Pat Morin, Edition 0.1Gbeta). Pages = PDF (printed = N - 12).

Modes and the rule/lemma each one checks:
  arraystack      resize doubles to max(1, 2n) when n = length(a); shrinks when length(a) >= 3n (ODS p.45, 47).
                  Checks Lemma 2.1 (ODS p.47-48): between two resize() calls there are at least n_i/2 - 1 operations and
                  the sum of the n_i is <= 2m + 2r.
  dualarraydeque  balance() when 3*front < back or 3*back < front, redistributing to floor(n/2) and ceil(n/2)
                  (ODS p.59-60). Checks Lemma 2.2 (ODS p.60-62): between two rebalancings that move elements
                  there are at least n/2 - 1 operations.
  selist          list of blocks (BDeque) of size b+1; spread/gather (ODS p.80-89). Checks the occupancy invariant
                  (b-1 to b+1, except the last block, ODS p.81) and the argument of Lemma 3.1 (ODS p.88-89): with the
                  'fragile nodes' potential, each spread/gather lowers the potential by b-1 and each operation raises it
                  by at most 1, so (spreads + gathers)*(b-1) <= number of operations.
  scapegoat       ScapegoatTree with q/2 <= n <= q, height <= log_{3/2} q, scapegoat rebuild (ODS p.177-182).
                  Checks the invariant and reports the total rebuild cost against m*log_{3/2}(m) (Lemma 8.3, ODS p.183).

Operation sequences (--pattern): grow (m insertions at the end), growshrink (m/2 insertions and m/2 removals),
sorted (increasing insertions, for scapegoat), random (linear congruential generator with --seed; deterministic).
Everything here is a didactic simulation: [extrapolation] over sample data; only the rules come from the book.
Usage: python -I scripts/structure_simulator.py arraystack --m 100000 --pattern growshrink --check
Exit 0 if all checks (--check) pass. No network.
"""
import argparse
import math
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


class LCG:
    """Linear congruential generator (deterministic, 32 bits)."""

    def __init__(self, seed):
        self.x = seed & 0xFFFFFFFF

    def next(self):
        self.x = (1664525 * self.x + 1013904223) & 0xFFFFFFFF
        return self.x

    def below(self, n):
        return (self.next() >> 8) % n if n > 0 else 0


def op_sequence(pattern, m, seed):
    """Build a list of ('add'|'remove', fraction in [0,1)) - the index is fraction * current size."""
    rng = LCG(seed)
    ops = []
    if pattern == "grow":
        ops = [("add", 1.0)] * m
    elif pattern == "sorted":
        ops = [("add", 1.0)] * m
    elif pattern == "growshrink":
        ops = [("add", 1.0)] * (m // 2) + [("remove", 1.0)] * (m - m // 2)
    elif pattern == "random":
        size = 0
        for _ in range(m):
            if size == 0 or rng.below(100) < 60:
                ops.append(("add", rng.below(1000) / 1000.0))
                size += 1
            else:
                ops.append(("remove", rng.below(1000) / 1000.0))
                size -= 1
    else:
        raise SystemExit("unknown pattern: %s" % pattern)
    return ops


def pick_index(frac, size, adding):
    if adding:
        return min(size, int(frac * (size + 1)))
    return min(size - 1, int(frac * size))


# ----------------------------------------------------------------------------- ArrayStack
def sim_arraystack(m, pattern, seed):
    a_len, n = 1, 0
    resizes = []  # (n_i, ops since the last resize)
    since = 0
    ops = op_sequence(pattern, m, seed)
    total_ops = 0
    copied = 0
    for kind, frac in ops:
        total_ops += 1
        since += 1
        if kind == "add":
            if n == a_len:
                resizes.append((n, since))
                copied += n
                a_len = max(1, 2 * n)
                since = 0
            n += 1
        else:
            if n == 0:
                total_ops -= 1
                since -= 1
                continue
            n -= 1
            if a_len >= 3 * n:
                resizes.append((n, since))
                copied += n
                a_len = max(1, 2 * n)
                since = 0
    r = len(resizes)
    sum_n = sum(x for x, _ in resizes)
    viol = [(ni, s) for ni, s in resizes if s < ni / 2 - 1]
    res = {
        "operations_m": total_ops, "resizes_r": r, "sum_n_i": sum_n, "bound_2m+2r": 2 * total_ops + 2 * r,
        "total_copies": copied, "amortized_resize_cost": round(copied / max(total_ops, 1), 3),
        "lemma_2.1_violations": len(viol),
    }
    ok = (not viol) and sum_n <= 2 * total_ops + 2 * r
    return res, ok, "Lemma 2.1 (ODS p.47-48): ops between resizes >= n_i/2 - 1 and sum n_i <= 2m + 2r"


# ----------------------------------------------------------------------------- DualArrayDeque
def sim_dualarraydeque(m, pattern, seed):
    front, back = [], []  # front stores elements in reverse order
    ops = op_sequence(pattern, m, seed)
    since = 0
    moved_total = 0
    rebal = 0
    viol = 0
    cnt = 0
    nxt = 0
    for kind, frac in ops:
        n = len(front) + len(back)
        if kind == "remove" and n == 0:
            continue
        since += 1
        cnt += 1
        if kind == "add":
            i = pick_index(frac, n, True)
            nxt += 1
            if i < len(front):
                front.insert(len(front) - i, nxt)  # front.add(front.size() - i, x)
            else:
                back.insert(i - len(front), nxt)
        else:
            i = pick_index(frac, n, False)
            if i < len(front):
                front.pop(len(front) - i - 1)
            else:
                back.pop(i - len(front))
        n = len(front) + len(back)
        if 3 * len(front) < len(back) or 3 * len(back) < len(front):
            mid = n // 2
            logical = list(reversed(front)) + back
            front = list(reversed(logical[:mid]))
            back = logical[mid:]
            moved_total += n
            rebal += 1
            if since < n / 2 - 1:
                viol += 1
            since = 0
    res = {"operations_m": cnt, "rebalances": rebal, "elements_moved": moved_total,
           "moved_per_operation": round(moved_total / max(cnt, 1), 3), "lemma_2.2_violations": viol}
    return res, viol == 0, "Lemma 2.2 (ODS p.60-62): >= n/2 - 1 operations between balance() calls that move elements"


# ----------------------------------------------------------------------------- SEList
class SEList:
    def __init__(self, b):
        self.b = b
        self.blocks = []  # list of Python lists (each one is a BDeque of capacity b+1)
        self.n = 0
        self.spreads = 0
        self.gathers = 0
        self.adds = 0
        self.removes = 0

    def locate(self, i):
        for u, blk in enumerate(self.blocks):
            if i < len(blk):
                return u, i
            i -= len(blk)
        raise IndexError

    def add(self, i, x):
        b = self.b
        self.adds += 1
        if i == self.n:
            if not self.blocks or len(self.blocks[-1]) == b + 1:
                self.blocks.append([])
            self.blocks[-1].append(x)
            self.n += 1
            return
        u, j = self.locate(i)
        r, w = 0, u
        while r < b and w < len(self.blocks) and len(self.blocks[w]) == b + 1:
            w += 1
            r += 1
        if r == b:
            self.spread(u)
            w = u
        if w == len(self.blocks):
            self.blocks.append([])
        while w > u:
            self.blocks[w].insert(0, self.blocks[w - 1].pop())
            w -= 1
        self.blocks[u].insert(j, x)
        self.n += 1

    def spread(self, u):
        b = self.b
        self.spreads += 1
        w = u + b
        self.blocks.insert(w, [])
        while w != u:
            while len(self.blocks[w]) < b:
                self.blocks[w].insert(0, self.blocks[w - 1].pop())
            w -= 1

    def remove(self, i):
        b = self.b
        self.removes += 1
        u, j = self.locate(i)
        y = self.blocks[u][j]
        w, r = u, 0
        while r < b and w < len(self.blocks) and len(self.blocks[w]) == b - 1:
            w += 1
            r += 1
        if r == b:
            self.gather(u)
        self.blocks[u].pop(j)
        while len(self.blocks[u]) < b - 1 and u + 1 < len(self.blocks):
            self.blocks[u].append(self.blocks[u + 1].pop(0))
            u += 1
        if len(self.blocks[u]) == 0:
            del self.blocks[u]
        self.n -= 1
        return y

    def gather(self, u):
        b = self.b
        self.gathers += 1
        w = u
        for _ in range(b - 1):
            while len(self.blocks[w]) < b:
                self.blocks[w].append(self.blocks[w + 1].pop(0))
            w += 1
        del self.blocks[w]

    def invariant_ok(self):
        b = self.b
        for idx, blk in enumerate(self.blocks):
            if idx < len(self.blocks) - 1 and not (b - 1 <= len(blk) <= b + 1):
                return False
            if len(blk) > b + 1:
                return False
        return sum(len(x) for x in self.blocks) == self.n


def sim_selist(m, pattern, seed, b):
    L = SEList(b)
    ops = op_sequence(pattern, m, seed)
    inv_ok = True
    nxt = 0
    for kind, frac in ops:
        if kind == "remove" and L.n == 0:
            continue
        if kind == "add":
            nxt += 1
            L.add(pick_index(frac, L.n, True), nxt)
        else:
            L.remove(pick_index(frac, L.n, False))
        if not L.invariant_ok():
            inv_ok = False
            break
    flat_blocks = len(L.blocks)
    bound_blocks = L.n / (b - 1) + 1 if b > 1 else float("inf")
    # potential = fragile nodes: each spread/gather lowers it by b-1 and each operation raises it by at most 1 (ODS p.88-89)
    potential_ok = (L.spreads + L.gathers) * (b - 1) <= L.adds + L.removes
    res = {"b": b, "add_operations": L.adds, "remove_operations": L.removes, "n_final": L.n, "blocks": flat_blocks,
           "blocks_bound_n/(b-1)+1": round(bound_blocks, 2), "spreads": L.spreads, "gathers": L.gathers,
           "invariant_b-1..b+1": inv_ok}
    ok = inv_ok and potential_ok and flat_blocks <= bound_blocks + 1e-9
    return res, ok, "invariant (ODS p.81); Lemma 3.1 (ODS p.88-89) via potential: (spreads+gathers)*(b-1) <= operations; blocks <= n/(b-1)+1 (ODS p.81)"


# ----------------------------------------------------------------------------- ScapegoatTree
class SNode:
    __slots__ = ("x", "left", "right", "parent")

    def __init__(self, x):
        self.x, self.left, self.right, self.parent = x, None, None, None


class Scapegoat:
    def __init__(self):
        self.r = None
        self.n = 0
        self.q = 0
        self.rebuild_cost = 0
        self.size_cost = 0
        self.rebuilds = 0
        self.max_depth_seen = 0
        self.bound_violations = 0

    def size(self, u):
        if u is None:
            return 0
        return 1 + self.size(u.left) + self.size(u.right)

    def pack(self, u, a):
        if u is None:
            return
        self.pack(u.left, a)
        a.append(u)
        self.pack(u.right, a)

    def build(self, a, i, ns):
        if ns == 0:
            return None
        m = ns // 2
        node = a[i + m]
        node.left = self.build(a, i, m)
        if node.left:
            node.left.parent = node
        node.right = self.build(a, i + m + 1, ns - m - 1)
        if node.right:
            node.right.parent = node
        return node

    def rebuild(self, u):
        ns = self.size(u)
        self.size_cost += ns
        self.rebuild_cost += ns
        self.rebuilds += 1
        p = u.parent
        a = []
        self.pack(u, a)
        root = self.build(a, 0, ns)
        if p is None:
            self.r = root
            root.parent = None
        elif p.right is u:
            p.right = root
            root.parent = p
        else:
            p.left = root
            root.parent = p

    def log32(self, q):
        return math.log(q) / math.log(1.5) if q > 0 else 0

    def add(self, x):
        u = SNode(x)
        d = 0
        if self.r is None:
            self.r = u
        else:
            w = self.r
            while True:
                d += 1
                if x < w.x:
                    if w.left is None:
                        w.left = u
                        break
                    w = w.left
                elif x > w.x:
                    if w.right is None:
                        w.right = u
                        break
                    w = w.right
                else:
                    return False
            u.parent = w
        self.n += 1
        self.q += 1
        if d > self.log32(self.q):
            w = u.parent
            while True:
                sw, sp = self.size(w), self.size(w.parent)
                self.size_cost += sw + sp
                if 3 * sw <= 2 * sp:
                    w = w.parent
                else:
                    break
            self.rebuild(w.parent)
            d = self.depth(u)
        self.max_depth_seen = max(self.max_depth_seen, d)
        if d > self.log32(self.q) + 1e-9:
            self.bound_violations += 1
        return True

    def depth(self, u):
        d = 0
        while u.parent is not None:
            u = u.parent
            d += 1
        return d

    def find_node(self, x):
        w = self.r
        while w is not None:
            if x < w.x:
                w = w.left
            elif x > w.x:
                w = w.right
            else:
                return w
        return None

    def remove(self, x):
        u = self.find_node(x)
        if u is None:
            return False
        if u.left is None or u.right is None:
            self.splice(u)
        else:
            w = u.right
            while w.left is not None:
                w = w.left
            u.x = w.x
            self.splice(w)
        self.n -= 1
        if 2 * self.n < self.q:
            if self.r is not None:
                self.rebuild(self.r)
            self.q = self.n
        return True

    def splice(self, u):
        s = u.left if u.left is not None else u.right
        p = u.parent
        if p is None:
            self.r = s
        elif p.left is u:
            p.left = s
        else:
            p.right = s
        if s is not None:
            s.parent = p


def sim_scapegoat(m, pattern, seed):
    t = Scapegoat()
    rng = LCG(seed)
    inserted = []
    done = 0
    nxt = 0
    for k in range(m):
        if pattern == "sorted":
            kind = "add"
        elif pattern == "growshrink":
            kind = "add" if k < m // 2 else "remove"
        elif pattern == "grow":
            kind = "add"
        else:
            kind = "add" if (not inserted or rng.below(100) < 60) else "remove"
        if kind == "add":
            nxt = nxt + 1 if pattern in ("sorted", "grow", "growshrink") else rng.below(10 * m + 10)
            if t.add(nxt):
                inserted.append(nxt)
                done += 1
        else:
            if pattern == "growshrink":
                x = inserted.pop(0)
            else:
                x = inserted.pop(rng.below(len(inserted)))
            t.remove(x)
            done += 1
    bound = max(done, 2) * (math.log(max(done, 2)) / math.log(1.5))
    res = {"operations_m": done, "n_final": t.n, "q_final": t.q, "rebuilds": t.rebuilds,
           "total_rebuild_cost": t.rebuild_cost, "m*log_{3/2}(m)": round(bound, 1),
           "rebuild_ratio/(m*log)": round(t.rebuild_cost / bound, 3),
           "max_depth": t.max_depth_seen, "height_invariant_violations": t.bound_violations}
    ok = t.bound_violations == 0 and t.q / 2 <= t.n + 1e-9 and t.n <= t.q and t.rebuild_cost <= 3 * bound
    return res, ok, "q/2 <= n <= q and height <= log_{3/2} q (ODS p.179); rebuilds total O(m log m) (Lemma 8.3, ODS p.183-184)"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Amortized-cost simulator (Open Data Structures, Morin)")
    ap.add_argument("mode", choices=["arraystack", "dualarraydeque", "selist", "scapegoat"])
    ap.add_argument("--m", type=int, default=20000, help="number of operations")
    ap.add_argument("--pattern", choices=["grow", "growshrink", "sorted", "random"], default="random")
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--b", type=int, default=8, help="SEList block parameter (b >= 2)")
    ap.add_argument("--check", action="store_true", help="exit 1 if any bound from the book is violated")
    a = ap.parse_args(argv)
    if a.mode == "selist" and a.b < 2:
        raise SystemExit("b must be >= 2")
    if a.mode == "arraystack":
        res, ok, rule = sim_arraystack(a.m, a.pattern, a.seed)
    elif a.mode == "dualarraydeque":
        res, ok, rule = sim_dualarraydeque(a.m, a.pattern, a.seed)
    elif a.mode == "selist":
        res, ok, rule = sim_selist(a.m, a.pattern, a.seed, a.b)
    else:
        res, ok, rule = sim_scapegoat(a.m, a.pattern, a.seed)
    print("=== Simulation: %s | pattern=%s | m=%d | seed=%d ===" % (a.mode, a.pattern, a.m, a.seed))
    for k, v in res.items():
        print("%-36s %s" % (k, v))
    print("Rule checked: %s" % rule)
    print("Result of the book's bounds: %s" % ("OK" if ok else "VIOLATED"))
    print("Note: the simulation is a didactic [extrapolation]; the rules and bounds are [from source].")
    return 0 if (ok or not a.check) else 1


if __name__ == "__main__":
    sys.exit(main())

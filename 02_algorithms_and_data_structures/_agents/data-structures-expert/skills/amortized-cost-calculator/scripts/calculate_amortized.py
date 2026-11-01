# -*- coding: utf-8 -*-
"""
calculate_amortized.py - deterministic calculator of amortized cost and space, following "Open Data Structures"
(Pat Morin, Edition 0.1Gbeta), Chs. 2 and 3. Pages = PDF (printed = N - 12).

Modes:
  resize   n insertions at the end of an ArrayStack. geometric: the book's rule (doubles to max(1, 2n) when n = length(a),
           ODS p.45, 47); the total-cost bound is Lemma 2.1: sum n_i <= 2m + 2r (ODS p.47-48).
           additive: growing by +chunk is NOT analyzed in the book; the result is labeled [extrapolation].
  rootish  RootishArrayStack: blocks, capacity r(r+1)/2, block/position of an index (ODS p.62-64) and space
           bounds (ODS p.67-68).
  selist   SEList: maximum number of blocks n/(b-1)+1, wasted space O(b + n/b) and time (ODS p.81, 89).
No network; read-only. Usage: python -I calculate_amortized.py --mode resize --n 1000 --growth geometric
"""
import argparse
import math
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def sim_resize(n, growth, chunk=10):
    length, size = 1, 0
    resizes = 0
    copies = 0
    sum_ni = 0
    for _ in range(n):
        if size == length:  # add(i,x): if n = length(a) then resize()
            resizes += 1
            copies += size
            sum_ni += size
            length = max(1, 2 * size) if growth == "geometric" else length + chunk
        size += 1
    return {"n": n, "growth": growth, "chunk": chunk, "resizes": resizes, "copies": copies,
            "sum_ni": sum_ni, "bound": 2 * n + 2 * resizes, "per_op": copies / n if n else 0.0}


def i2b(i):
    """Block that contains index i (ODS p.64): b = ceil((-3 + sqrt(9 + 8i))/2). Exact integer arithmetic."""
    b = 0
    while (b + 1) * (b + 2) // 2 < i + 1:
        b += 1
    return b


def sim_rootish(n, index=None):
    r_min = 0
    while r_min * (r_min + 1) // 2 < n:
        r_min += 1
    # (r-2)(r-1) <= n  =>  r <= (3 + sqrt(1 + 4n))/2  (ODS p.67)
    r_max = int(math.floor((3 + math.sqrt(1 + 4 * n)) / 2)) if n >= 0 else 0
    out = {"n": n, "r_min": r_min, "capacity_min": r_min * (r_min + 1) // 2,
           "waste_min": r_min * (r_min + 1) // 2 - n, "r_max": r_max,
           "waste_bound": 2 * r_max - 1, "sqrt_n": math.sqrt(n) if n > 0 else 0.0}
    if index is not None:
        b = i2b(index)
        out["index"] = index
        out["block"] = b
        out["offset"] = index - b * (b + 1) // 2
    return out


def sim_selist(n, b):
    blocks_max = n / (b - 1) + 1 if b > 1 else float("inf")
    return {"n": n, "b": b, "block_capacity": b + 1, "blocks_max": blocks_max, "waste_order": b + n / b,
            "dllist_pointers": 2 * n, "time_order_mid": b + (n / 2) / b, "best_b": math.sqrt(n) if n > 0 else 0.0}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Amortized cost and space calculator (Open Data Structures)")
    ap.add_argument("--mode", choices=["resize", "rootish", "selist"], required=True)
    ap.add_argument("--n", type=int, default=1000, help="number of elements")
    ap.add_argument("--growth", choices=["geometric", "additive"], default="geometric")
    ap.add_argument("--chunk", type=int, default=10, help="increment for additive mode")
    ap.add_argument("--b", type=int, default=32, help="SEList block size (b >= 2)")
    ap.add_argument("--index", type=int, default=None, help="index i to map to block/position (rootish)")
    a = ap.parse_args(argv)
    if a.n < 0 or a.chunk < 1:
        raise SystemExit("n >= 0 and chunk >= 1")
    print("=== AMORTIZED COST AND SPACE CALCULATOR (pages = PDF; printed = N - 12) ===")
    if a.mode == "resize":
        r = sim_resize(a.n, a.growth, a.chunk)
        print("Mode:                    insertions at the end of an ArrayStack")
        print("Insertions (m):          %d" % r["n"])
        print("Strategy:                %s" % ("geometric: doubles when full [from source] (ODS p.45, 47)"
                                                if a.growth == "geometric" else "additive +%d [extrapolation]: not analyzed in the book" % a.chunk))
        print("Resizes (r):             %d" % r["resizes"])
        print("Element copies:          %d" % r["copies"])
        print("Resize cost per op.:    %.3f" % r["per_op"])
        if a.growth == "geometric":
            print("Lemma 2.1 bound:         sum n_i = %d <= 2m + 2r = %d  [from source] (ODS p.47-48)" % (r["sum_ni"], r["bound"]))
            print("Conclusion:              O(1) amortized per operation [from source] (ODS p.49)")
        else:
            print("Conclusion:              copies ~ n^2/(2*chunk) = %.0f: quadratic growth [extrapolation]"
                  % (a.n ** 2 / (2 * a.chunk)))
    elif a.mode == "rootish":
        r = sim_rootish(a.n, a.index)
        print("Mode:                    RootishArrayStack (n = %d)" % r["n"])
        print("Minimum blocks r:        %d (capacity %d, free slots %d) [inference]" % (r["r_min"], r["capacity_min"], r["waste_min"]))
        print("Maximum blocks (book):   r <= (3 + sqrt(1 + 4n))/2 = %d [from source] (ODS p.67)" % r["r_max"])
        print("Maximum waste:           <= 2r - 1 = %d (last two blocks) [from source] (ODS p.67)" % r["waste_bound"])
        print("Reference:               sqrt(n) = %.1f; space n + O(sqrt n) [from source] (ODS p.68)" % r["sqrt_n"])
        print("Comparison:              an ArrayStack can be down to 1/3 occupancy [from source] (ODS p.62);")
        print("                         waste < 2n [inference] (length(a) < 3n after the remove check)")
        if a.index is not None:
            print("Index %d:                block %d, position %d [from source] (ODS p.64)" % (r["index"], r["block"], r["offset"]))
    else:
        if a.b < 2:
            raise SystemExit("b must be >= 2")
        r = sim_selist(a.n, a.b)
        print("Mode:                    SEList (n = %d, b = %d)" % (r["n"], r["b"]))
        print("Block capacity:          b + 1 = %d [from source] (ODS p.80-81)" % r["block_capacity"])
        print("Blocks (maximum):        n/(b-1) + 1 = %.1f [from source] (ODS p.81)" % r["blocks_max"])
        print("Wasted space:            O(b + n/b) ~ %.1f words [from source] (ODS p.81, 89)" % r["waste_order"])
        print("Equivalent DLList:       2n = %d list references [from source] (ODS p.80)" % r["dllist_pointers"])
        print("add/remove time:         O(b + min{i, n-i}/b) ~ %.1f (i in the middle) [from source] (ODS p.89)" % r["time_order_mid"])
        print("b close to sqrt(n):      %.1f brings the space close to the sqrt(n) bound [from source] (ODS p.81)" % r["best_b"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

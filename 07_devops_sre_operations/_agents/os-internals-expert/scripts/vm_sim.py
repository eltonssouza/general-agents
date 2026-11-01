# -*- coding: utf-8 -*-
"""
vm_sim.py - virtual memory according to OSTEP (ch.15, 16, 18, 19, 20, 22).

Subcommands (stdlib, no network, deterministic):
  base-bounds  base+bounds translation (p.202-205)
  segments     segmentation with segment bits and negative-growing stack (p.305-308)
  linear       linear page table: VPN/offset/PFN (p.481-483, 486)
  multilevel   2-level table (page directory + page table) (p.602-605)
  tlb          TLB flow with hits/misses and hit rate (p.542-545)
  replace      replacement policies OPT/FIFO/LRU/RANDOM/CLOCK/MRU (p.691-702)
  amat         AMAT = T_M + P_miss x T_D (Eq.22.1, p.691)
  sizes        size of linear and multi-level tables (p.483-484, 596, 606)

Examples:
  python -I scripts/vm_sim.py linear --va-bits 6 --page-size 16 --map "0:3,1:7,2:5,3:2" --va 21
  python -I scripts/vm_sim.py base-bounds --base 16384 --bounds 4096 --va 0,1024,3000,4400
  python -I scripts/vm_sim.py segments --va-bits 14 --seg-bits 2 --va 100,4200,15360,7168 \
      --seg "0:32768:2048:+,1:34816:3072:+,3:28672:2048:-"
  python -I scripts/vm_sim.py tlb --page-size 16 --entries 4 --va 100,104,108,112,116,120,124,128,132,136
  python -I scripts/vm_sim.py replace --policy ALL --frames 3 --refs 0,1,2,0,1,3,0,3,1,2,1
  python -I scripts/vm_sim.py amat --tm 100e-9 --td 10e-3 --hit 0.9

CONVENTIONS NOT SPECIFIED BY THE BOOK ([inference]):
  - OPT: on a tie (pages never used again) it avoids the most recently loaded one [the book evicts 3 instead of 0, p.693];
  - CLOCK: use bit = 1 on load (option --initial-use 0|1); the hand advances past the victim; hits set the bit;
  - RANDOM: fixed seed (--seed), so it does NOT reproduce figure 22.3 of the book (which is only one example draw).
"""
import argparse
import random
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def ints(s):
    out = []
    for t in str(s).split(","):
        t = t.strip()
        if not t:
            continue
        out.append(int(t, 0))
    return out


def log2_exact(n, nome="value"):
    if n <= 0 or n & (n - 1):
        raise SystemExit(f"{nome} must be a power of 2 (got {n})")
    return n.bit_length() - 1


# ---------------------------------------------------------------- base/bounds
def cmd_base_bounds(a):
    print(f"base={a.base} bounds={a.bounds}: PA = VA + base; fault if VA < 0 or VA >= bounds (p.202-204)")
    for va in ints(a.va):
        if va < 0 or va >= a.bounds:
            print(f"  VA {va:>8} -> Fault (out of bounds)")
        else:
            print(f"  VA {va:>8} -> PA {va + a.base}")


# ---------------------------------------------------------------- segments
def cmd_segments(a):
    seg_shift = a.va_bits - a.seg_bits
    off_mask = (1 << seg_shift) - 1
    max_seg = 1 << seg_shift
    segs = {}
    for tok in a.seg.split(","):
        n, base, size, d = tok.split(":")
        segs[int(n)] = (int(base, 0), int(size, 0), d.strip())
    print(f"{a.va_bits}-bit VA: {a.seg_bits} segment bits + {seg_shift} offset bits (SEG_SHIFT={seg_shift}, "
          f"OFFSET_MASK=0x{off_mask:X}); max size per segment={max_seg} (p.306-308)")
    for va in ints(a.va):
        s = va >> seg_shift
        off = va & off_mask
        if s not in segs:
            print(f"  VA {va:>7}: segment {s} not defined -> Fault")
            continue
        base, size, d = segs[s]
        if d == "+":
            if off >= size:
                print(f"  VA {va:>7}: seg {s} offset {off} >= size {size} -> Fault (segmentation violation)")
            else:
                print(f"  VA {va:>7}: seg {s} offset {off} -> PA {base + off}")
        else:
            neg = off - max_seg
            if -neg > size:
                print(f"  VA {va:>7}: seg {s} (grows downward) negative offset {neg}; |{neg}| > size {size} -> Fault")
            else:
                print(f"  VA {va:>7}: seg {s} (grows downward) offset {off} - {max_seg} = {neg} -> PA {base + neg}")


# ---------------------------------------------------------------- linear
def cmd_linear(a):
    off_bits = log2_exact(a.page_size, "page-size")
    vpn_mask = ((1 << a.va_bits) - 1) ^ ((1 << off_bits) - 1)
    pt = {}
    for tok in a.map.split(","):
        v, p = tok.split(":")
        pt[int(v)] = int(p)
    print(f"{a.va_bits}-bit VA; page {a.page_size} B (offset {off_bits} bits; VPN_MASK=0x{vpn_mask:X}, SHIFT={off_bits}); "
          f"PA = (PFN << SHIFT) | offset (p.486)")
    for va in ints(a.va):
        if va >= (1 << a.va_bits):
            print(f"  VA {va}: outside the {a.va_bits}-bit space")
            continue
        vpn = (va & vpn_mask) >> off_bits
        off = va & (a.page_size - 1)
        if vpn not in pt:
            print(f"  VA {va:>6} = {va:0{a.va_bits}b}b: VPN {vpn}, offset {off} -> invalid PTE (SEGMENTATION_FAULT)")
        else:
            pfn = pt[vpn]
            pa = (pfn << off_bits) | off
            print(f"  VA {va:>6} = {va:0{a.va_bits}b}b: VPN {vpn}, offset {off}, PFN {pfn} -> PA {pa} (0x{pa:X}) = {pa:0{max(1, pa.bit_length())}b}b")


# ---------------------------------------------------------------- multilevel
def cmd_multilevel(a):
    off_bits = log2_exact(a.page_size, "page-size")
    vpn_bits = a.va_bits - off_bits
    pt_bits = a.pt_index_bits
    pd_bits = vpn_bits - pt_bits
    # directory: "idx:pfn,..." ; pages of PT: "pfn=vpnlocal:pfn;..." via --pt "101:14=55;15=56|100:0=10;1=23"
    pd = {}
    for tok in a.pd.split(","):
        i, p = tok.split(":")
        pd[int(i)] = int(p)
    ptpages = {}
    for blk in a.pt.split("|"):
        head, body = blk.split(":", 1)
        d = {}
        for t in body.split(";"):
            if not t.strip():
                continue
            k, v = t.split("=")
            d[int(k)] = int(v)
        ptpages[int(head)] = d
    print(f"{a.va_bits}-bit VA = PDIndex({pd_bits}) + PTIndex({pt_bits}) + offset({off_bits}); "
          f"PDEAddr = PDBR + PDIndex*sizeof(PDE); PTEAddr = (PDE.PFN << SHIFT) + PTIndex*sizeof(PTE) (p.603-604)")
    for va in ints(a.va):
        vpn = va >> off_bits
        pdi = vpn >> pt_bits
        pti = vpn & ((1 << pt_bits) - 1)
        off = va & (a.page_size - 1)
        if pdi not in pd:
            print(f"  VA 0x{va:X}: PDIndex {pdi} -> invalid PDE (SEGMENTATION_FAULT)")
            continue
        page = ptpages.get(pd[pdi], {})
        if pti not in page:
            print(f"  VA 0x{va:X}: PDIndex {pdi} -> PT at PFN {pd[pdi]}; PTIndex {pti} -> invalid PTE (SEGMENTATION_FAULT)")
            continue
        pfn = page[pti]
        pa = (pfn << off_bits) | off
        print(f"  VA 0x{va:X}: PDIndex {pdi} (PT at PFN {pd[pdi]}), PTIndex {pti} -> PFN {pfn}, offset {off} -> PA 0x{pa:04X}"
              f"  [2 extra memory accesses on a TLB miss: PDE and PTE]")


# ---------------------------------------------------------------- TLB
def cmd_tlb(a):
    off_bits = log2_exact(a.page_size, "page-size")
    tlb = []  # LRU order: index 0 = oldest
    hits = 0
    seq = []
    for va in ints(a.va):
        vpn = va >> off_bits
        if vpn in tlb:
            hits += 1
            seq.append("hit")
            tlb.remove(vpn)
            tlb.append(vpn)
        else:
            seq.append("miss")
            if len(tlb) >= a.entries:
                tlb.pop(0)  # LRU (p.551)
            tlb.append(vpn)
    n = len(seq)
    print(f"page {a.page_size} B, TLB {a.entries} entries (LRU), refs={n}")
    print("sequence:", ", ".join(seq))
    print(f"hit rate = hits/total = {hits}/{n} = {100.0 * hits / n:.1f}%  (book p.544: array of 10 integers at VA 100, 16 B page -> 70%)")
    if a.repeat:
        for k in range(a.repeat):
            h2 = 0
            for va in ints(a.va):
                vpn = va >> off_bits
                if vpn in tlb:
                    h2 += 1
                    tlb.remove(vpn)
                    tlb.append(vpn)
                else:
                    if len(tlb) >= a.entries:
                        tlb.pop(0)
                    tlb.append(vpn)
            print(f"repetition {k + 1}: {h2}/{n} hits (temporal locality, p.545)")


# ---------------------------------------------------------------- replacement
def run_policy(policy, frames, refs, seed=0, initial_use=1):
    cache = []  # load order (FIFO) / recency (LRU: end = most recent)
    hits = 0
    rows = []
    rnd = random.Random(seed)
    use = {}
    hand = 0
    slots = []  # CLOCK: circular list of pages
    for i, p in enumerate(refs):
        evict = None
        if policy == "CLOCK":
            if p in slots:
                hit = True
                use[p] = 1
            else:
                hit = False
                if len(slots) < frames:
                    slots.append(p)
                    use[p] = initial_use
                else:
                    while True:
                        h = slots[hand]
                        if use[h] == 1:
                            use[h] = 0
                            hand = (hand + 1) % frames
                        else:
                            evict = h
                            slots[hand] = p
                            del use[h]
                            use[p] = initial_use
                            hand = (hand + 1) % frames
                            break
            state = list(slots)
        else:
            hit = p in cache
            if hit:
                if policy in ("LRU",):
                    cache.remove(p)
                    cache.append(p)
                elif policy == "MRU":
                    cache.remove(p)
                    cache.append(p)
            else:
                if len(cache) >= frames:
                    if policy == "FIFO":
                        evict = cache.pop(0)
                    elif policy == "LRU":
                        evict = cache.pop(0)
                    elif policy == "MRU":
                        evict = cache.pop()  # most recently used
                    elif policy == "RANDOM":
                        evict = cache.pop(rnd.randrange(len(cache)))
                    elif policy == "OPT":
                        fut = refs[i + 1:]
                        best, bd = None, -1
                        for c in reversed(cache):  # tie: the most recently loaded
                            d = fut.index(c) if c in fut else 10 ** 9
                            if d > bd:
                                best, bd = c, d
                        evict = best
                        cache.remove(best)
                    else:
                        raise SystemExit("unknown policy")
                cache.append(p)
            state = list(cache)
        if hit:
            hits += 1
        rows.append((p, "hit" if hit else "miss", evict, state))
    return hits, rows


def cmd_replace(a):
    refs = ints(a.refs)
    pols = ["OPT", "FIFO", "LRU", "RANDOM", "CLOCK", "MRU"] if a.policy.upper() == "ALL" else [a.policy.upper()]
    n = len(refs)
    uniq = len(set(refs))
    for pol in pols:
        hits, rows = run_policy(pol, a.frames, refs, a.seed, a.initial_use)
        miss = n - hits
        comp = min(uniq, n)
        print(f"{pol}: {hits} hits, {miss} misses, hit rate = {100.0 * hits / n:.1f}% "
              f"(without compulsory misses: {100.0 * hits / (n - comp):.1f}%)" if n - comp > 0 else f"{pol}: {hits} hits")
        if a.verbose:
            for p, h, ev, st in rows:
                print(f"    access {p}: {h:<4} evict={ev if ev is not None else '-'} state={st}")
    if a.policy.upper() == "ALL":
        print("Book (p.692-697, refs 0,1,2,0,1,3,0,3,1,2,1; 3 frames): OPT 54.5% (85.7% without compulsory); "
              "FIFO 36.4% (57.1%); LRU = OPT in this example.")


def cmd_amat(a):
    miss = 1.0 - a.hit
    amat = a.tm + miss * a.td
    print(f"AMAT = T_M + P_miss x T_D = {a.tm:g} + {miss:g} x {a.td:g} = {amat:.6g} s")
    for unit, f in (("ns", 1e9), ("us", 1e6), ("ms", 1e3)):
        print(f"  = {amat * f:.6g} {unit}")


def cmd_sizes(a):
    off_bits = log2_exact(a.page_size, "page-size")
    vpn_bits = a.va_bits - off_bits
    n = 1 << vpn_bits
    lin = n * a.pte
    print(f"{a.va_bits}-bit VA, page {a.page_size} B -> VPN {vpn_bits} bits, offset {off_bits}; {n} PTEs x {a.pte} B = {lin} B = {lin / 2**20:.3f} MiB per linear table")
    print(f"  x {a.procs} processes = {lin * a.procs / 2**20:.1f} MiB (book p.483-484: 32 bits/4KB/4B = 4MB; 100 processes = 400MB)")
    ptes_per_page = a.page_size // a.pte
    pt_idx = ptes_per_page.bit_length() - 1
    rest = vpn_bits - pt_idx
    print(f"  PTEs per page-table page = {ptes_per_page} -> {pt_idx} PT index bits; {rest} bits left for directory level(s)")
    levels = 1
    bits_left = rest
    while bits_left > pt_idx and bits_left > 0:
        levels += 1
        bits_left -= pt_idx
    print(f"  directory levels above the page-table pages: {levels if rest > 0 else 0} "
          f"(book criterion p.606: each piece of the table and of the directories must fit in one page)")


def main():
    ap = argparse.ArgumentParser(description="OSTEP virtual memory simulators")
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("base-bounds")
    b.add_argument("--base", type=int, required=True)
    b.add_argument("--bounds", type=int, required=True)
    b.add_argument("--va", required=True)
    b.set_defaults(f=cmd_base_bounds)
    s = sp.add_parser("segments")
    s.add_argument("--va-bits", type=int, required=True)
    s.add_argument("--seg-bits", type=int, required=True)
    s.add_argument("--seg", required=True, help="N:BASE:SIZE:+|-,...")
    s.add_argument("--va", required=True)
    s.set_defaults(f=cmd_segments)
    l = sp.add_parser("linear")
    l.add_argument("--va-bits", type=int, required=True)
    l.add_argument("--page-size", type=int, required=True)
    l.add_argument("--map", required=True, help="VPN:PFN,...")
    l.add_argument("--va", required=True)
    l.set_defaults(f=cmd_linear)
    m = sp.add_parser("multilevel")
    m.add_argument("--va-bits", type=int, required=True)
    m.add_argument("--page-size", type=int, required=True)
    m.add_argument("--pt-index-bits", type=int, required=True)
    m.add_argument("--pd", required=True, help="PDIndex:PFN_of_PT_page,...")
    m.add_argument("--pt", required=True, help="PFN_PT:idx=pfn;idx=pfn|PFN_PT:idx=pfn")
    m.add_argument("--va", required=True)
    m.set_defaults(f=cmd_multilevel)
    t = sp.add_parser("tlb")
    t.add_argument("--page-size", type=int, required=True)
    t.add_argument("--entries", type=int, required=True)
    t.add_argument("--va", required=True)
    t.add_argument("--repeat", type=int, default=0)
    t.set_defaults(f=cmd_tlb)
    r = sp.add_parser("replace")
    r.add_argument("--policy", default="ALL")
    r.add_argument("--frames", type=int, required=True)
    r.add_argument("--refs", required=True)
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--initial-use", type=int, default=1, choices=[0, 1])
    r.add_argument("-v", "--verbose", action="store_true")
    r.set_defaults(f=cmd_replace)
    am = sp.add_parser("amat")
    am.add_argument("--tm", type=float, required=True)
    am.add_argument("--td", type=float, required=True)
    am.add_argument("--hit", type=float, required=True)
    am.set_defaults(f=cmd_amat)
    z = sp.add_parser("sizes")
    z.add_argument("--va-bits", type=int, required=True)
    z.add_argument("--page-size", type=int, required=True)
    z.add_argument("--pte", type=int, default=4)
    z.add_argument("--procs", type=int, default=1)
    z.set_defaults(f=cmd_sizes)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

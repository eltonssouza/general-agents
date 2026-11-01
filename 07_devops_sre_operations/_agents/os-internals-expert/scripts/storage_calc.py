# -*- coding: utf-8 -*-
"""
storage_calc.py - storage calculations according to OSTEP (ch.37, 38, 40, 41, 43, 45).

Subcommands (stdlib, no network, deterministic):
  disk       T_I/O = T_seek + T_rotation + T_transfer ; R_I/O = Size / T_I/O   (Eq.37.1/37.2, p.150-152)
  raid       capacity/reliability/throughput/latency of RAID 0/1/4/5            (Fig.38.8, p.249)
  raid-map   logical block mapping in RAID-0 (p.239) and simple rotated parity
  parity     XOR parity and reconstruction; subtractive parity (Eq.38.1, p.244-247)
  amortize   chunk/segment size needed to reach fraction F of peak (FFS p.522; LFS Eq.43.6 p.627)
  inode      address of an inode in vsfs (p.433)
  fsize      maximum file size with direct/indirect pointers (p.434-435)
  checksum   XOR, sum and Fletcher (p.712-713)
  io-count   I/O count for open/read/write/create in vsfs (p.439-442)

Examples (from the package folder):
  python -I scripts/storage_calc.py disk --seek-ms 4 --rpm 15000 --size-kb 4 --mbps 125
  python -I scripts/storage_calc.py raid --n 4 --b 1000 --s 100 --r 1
  python -I scripts/storage_calc.py raid-map --level 0 --disks 4 --block 14
  python -I scripts/storage_calc.py parity --data 0,0,1,1
  python -I scripts/storage_calc.py amortize --pos-ms 10 --mbps 100 --frac 0.9
  python -I scripts/storage_calc.py inode --inumber 32 --inode-size 256 --start 12288 --block 4096 --sector 512
  python -I scripts/storage_calc.py fsize --block 4096 --ptr 4 --direct 12 --indirect 1 --double 1
  python -I scripts/storage_calc.py checksum --hex 365e,c4cd,ba14,8a92,ecef,2c3a,40be,f666 --width 4
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def cmd_disk(a):
    rot_ms = 60000.0 / a.rpm  # one rotation
    t_rot = rot_ms / 2.0 if a.rot_ms is None else a.rot_ms
    mb = a.size_kb / a.kb_per_mb  # the book uses 1 KB = 1/1000 MB in disk calculations (p.152, p.241)
    t_xfer = mb / a.mbps * 1000.0  # ms
    t = a.seek_ms + t_rot + t_xfer
    r = mb / (t / 1000.0)
    print(f"1 rotation = 60000/{a.rpm} = {rot_ms:.3f} ms; average rotation = {t_rot:.3f} ms (half, p.152)")
    print(f"T_transfer = {a.size_kb} KB ({mb:.6g} MB, 1 MB={a.kb_per_mb:g} KB) / {a.mbps} MB/s = {t_xfer:.4f} ms")
    print(f"T_I/O = {a.seek_ms} + {t_rot:.3f} + {t_xfer:.4f} = {t:.3f} ms   (Eq.37.1)")
    print(f"R_I/O = {mb:.6g} MB / {t:.3f} ms = {r:.3f} MB/s   (Eq.37.2)")
    print("Book (p.151-152): Cheetah 15K.5 (seek 4 ms, 15,000 RPM, 125 MB/s), 4 KB: ~6 ms and ~0.66 MB/s; "
          "Barracuda (9 ms, 7,200 RPM, 105 MB/s): ~13.2 ms and ~0.31 MB/s (the PDF rounds; the decimal calculation gives ~0.30).")


def cmd_raid(a):
    n, b, s, r = a.n, a.b, a.s, a.r
    t = {
        "RAID-0": dict(cap=f"{n * b}", rel="0", sr=n * s, sw=n * s, rr=n * r, rw=n * r, lr="T", lw="T"),
        "RAID-1": dict(cap=f"{n * b / 2:g}", rel="1 (guaranteed); up to N/2 (if lucky)", sr=n / 2 * s, sw=n / 2 * s,
                       rr=n * r, rw=n / 2 * r, lr="T", lw="T"),
        "RAID-4": dict(cap=f"{(n - 1) * b}", rel="1", sr=(n - 1) * s, sw=(n - 1) * s, rr=(n - 1) * r,
                       rw=r / 2, lr="T", lw="2T"),
        "RAID-5": dict(cap=f"{(n - 1) * b}", rel="1", sr=(n - 1) * s, sw=(n - 1) * s, rr=n * r,
                       rw=n / 4 * r, lr="T", lw="2T"),
    }
    print(f"N={n} disks, B={b} blocks/disk, S={s} MB/s (sequential), R={r} MB/s (random)  [Fig.38.8, p.249]")
    print(f"{'level':<8}{'capacity':>12}  {'reliab.':<28}{'seq read':>9}{'seq wr':>8}{'rnd read':>9}{'rnd wr':>8}  lat read/write")
    for k, v in t.items():
        print(f"{k:<8}{v['cap']:>12}  {v['rel']:<28}{v['sr']:>9g}{v['sw']:>8g}{v['rr']:>9g}{v['rw']:>8g}  {v['lr']}/{v['lw']}")
    print("Note: simplified model from the book (p.249-250): ignores longer seeks in mirrored writes and the rotational cost of parity.")


def cmd_raid_map(a):
    if a.level == 0:
        d = a.block % a.disks
        o = a.block // a.disks
        print(f"RAID-0 (chunk=1 bloco): Disk = A % N = {a.block} % {a.disks} = {d}; Offset = A / N = {a.block} // {a.disks} = {o}  (p.239)")
    elif a.level in (4, 5):
        data_disks = a.disks - 1
        stripe = a.block // data_disks
        pos = a.block % data_disks
        if a.level == 4:
            pdisk = a.disks - 1
            disk = pos
        else:
            pdisk = (a.disks - 1 - stripe) % a.disks  # parity rotates from right to left (Fig.38.7, p.248)
            disk = pos if pos < pdisk else pos + 1
        print(f"RAID-{a.level}: stripe {stripe}; block {a.block} -> disk {disk}, offset {stripe}; stripe parity on disk {pdisk}")
        print("[inference] The book shows the RAID-5 figure with rotated parity (p.248) but gives no formula; layout here = simple 'left-asymmetric'.")
    else:
        raise SystemExit("level must be 0, 4 or 5")


def cmd_parity(a):
    bits = [int(x) for x in a.data.split(",")]
    par = 0
    for b in bits:
        par ^= b
    print(f"XOR({','.join(map(str, bits))}) = {par}  (even parity: the number of 1s including the parity is even; p.244-245)")
    if a.lost is not None:
        rest = [b for i, b in enumerate(bits) if i != a.lost]
        rec = par
        for b in rest:
            rec ^= b
        print(f"reconstruction of index {a.lost}: XOR of the other data + parity = {rec}")
    if a.old is not None and a.new is not None:
        pold = par
        pnew = (a.old ^ a.new) ^ pold
        print(f"subtractive parity: P_new = (C_old XOR C_new) XOR P_old = ({a.old} XOR {a.new}) XOR {pold} = {pnew}  (Eq.38.1)")
        print("cost: 2 reads (old data and old parity) + 2 writes = 4 I/Os per small write (p.247-248).")


def cmd_amortize(a):
    f = a.frac
    if not 0 < f < 1:
        raise SystemExit("--frac must be between 0 and 1")
    d_mb = f / (1 - f) * a.mbps * (a.pos_ms / 1000.0)
    print(f"D = F/(1-F) x R_peak x T_position = {f}/{1 - f:.4g} x {a.mbps} MB/s x {a.pos_ms / 1000.0} s = {d_mb:.4f} MB = {d_mb * 1024:.1f} KB")
    print("Book: LFS (p.627) 10 ms, 100 MB/s, F=0.9 -> 9 MB; FFS (p.522-523) 10 ms and 40 MB/s: 50% -> 409.6 KB; 90% ~3.6 MB; 99% ~39.6 MB.")
    print("Unit note: the book uses 1 MB = 1024 KB in the FFS example (40 MB/s x 10 ms = 409.6 KB).")


def cmd_inode(a):
    off = a.inumber * a.inode_size
    addr = a.start + off
    blk = off // a.block
    sector = ((blk * a.block) + a.start) // a.sector
    print(f"offset in the table = {a.inumber} x {a.inode_size} = {off} B; address = {a.start} + {off} = {addr} B")
    print(f"blk = (inumber * sizeof(inode)) / blockSize = {blk}; sector = ((blk * blockSize) + inodeStartAddr) / sectorSize = {sector}  (p.433)")
    print("Book: inode 32, 256 B/inode, table at 12 KB: 12 KB + 8 KB = 20 KB -> sector 40.")


def cmd_fsize(a):
    ppb = a.block // a.ptr
    blocks = a.direct + a.indirect * ppb + a.double * ppb ** 2 + a.triple * ppb ** 3
    total = blocks * a.block
    print(f"pointers per block = {a.block}/{a.ptr} = {ppb}")
    print(f"addressable blocks = {a.direct} + {a.indirect}x{ppb} + {a.double}x{ppb}^2 + {a.triple}x{ppb}^3 = {blocks}")
    print(f"maximum size = {total} B = {total / 1024:.1f} KiB = {total / 2**30:.4f} GiB")
    print("Book: 12 direct + 1 indirect, 4 KB block, 4 B pointer -> (12+1024) x 4 KB = 4144 KB (p.434); with a double indirect: (12+1024+1024^2) x 4 KB, a little over 4 GB (p.435).")


def cmd_checksum(a):
    words = [int(h, 16) for h in a.hex.split(",")]
    data = b"".join(w.to_bytes(2, "big") for w in words)
    wd = a.width
    chunks = [data[i:i + wd] for i in range(0, len(data), wd)]
    x = [0] * wd
    add = 0
    for c in chunks:
        c = c.ljust(wd, b"\0")
        for i in range(wd):
            x[i] ^= c[i]
        add = (add + int.from_bytes(c, "big")) % (1 << (8 * wd))
    s1 = s2 = 0
    for byte in data:
        s1 = (s1 + byte) % 255
        s2 = (s2 + s1) % 255
    print(f"block of {len(data)} bytes in units of {wd} bytes")
    print(f"XOR       = 0x{bytes(x).hex()}   (book p.712: 0x201b9403 for the example)")
    print(f"sum       = 0x{add:0{2 * wd}x} (two's-complement addition ignoring overflow, p.713)")
    print(f"Fletcher  = s1={s1}, s2={s2} (s1=(s1+d_i) mod 255; s2=(s2+s1) mod 255, p.713)")


def cmd_io_count(a):
    depth = a.depth
    if a.op == "open":
        print(f"open of a path with {depth} directories: read the root inode + (dir data + next inode) per component => "
              f"~{1 + 2 * depth} reads (proportional to the path length, p.440); no caches.")
    elif a.op == "read":
        print("read: read the block (consulting the inode) + 1 inode write to update the last-accessed time; does NOT consult bitmaps (p.440).")
    elif a.op == "write-alloc":
        print("write that allocates a block: 5 I/Os = read/write data bitmap + read/write inode + write the data (p.441-442).")
    elif a.op == "create":
        print("create /foo/bar: 10 I/Os in the Fig.40.4 example (traverse the path + read/write inode bitmap, write the new inode, "
              "write the directory data, read/write the directory inode) (p.441-442); afterwards each allocating write costs 5 I/Os.")
    else:
        raise SystemExit("op: open, read, write-alloc, create")


def main():
    ap = argparse.ArgumentParser(description="OSTEP storage calculations")
    sp = ap.add_subparsers(dest="cmd", required=True)
    d = sp.add_parser("disk")
    d.add_argument("--seek-ms", type=float, required=True)
    d.add_argument("--rpm", type=float, required=True)
    d.add_argument("--rot-ms", type=float, default=None, help="overrides the average rotation")
    d.add_argument("--size-kb", type=float, required=True)
    d.add_argument("--mbps", type=float, required=True)
    d.add_argument("--kb-per-mb", type=float, default=1000.0, help="1000 (default; matches p.151-152 and p.241) or 1024")
    d.set_defaults(f=cmd_disk)
    r = sp.add_parser("raid")
    r.add_argument("--n", type=int, required=True)
    r.add_argument("--b", type=int, default=1)
    r.add_argument("--s", type=float, default=100.0)
    r.add_argument("--r", type=float, default=1.0)
    r.set_defaults(f=cmd_raid)
    m = sp.add_parser("raid-map")
    m.add_argument("--level", type=int, required=True)
    m.add_argument("--disks", type=int, required=True)
    m.add_argument("--block", type=int, required=True)
    m.set_defaults(f=cmd_raid_map)
    p = sp.add_parser("parity")
    p.add_argument("--data", required=True)
    p.add_argument("--lost", type=int, default=None)
    p.add_argument("--old", type=int, default=None)
    p.add_argument("--new", type=int, default=None)
    p.set_defaults(f=cmd_parity)
    am = sp.add_parser("amortize")
    am.add_argument("--pos-ms", type=float, required=True)
    am.add_argument("--mbps", type=float, required=True)
    am.add_argument("--frac", type=float, required=True)
    am.set_defaults(f=cmd_amortize)
    i = sp.add_parser("inode")
    i.add_argument("--inumber", type=int, required=True)
    i.add_argument("--inode-size", type=int, default=256)
    i.add_argument("--start", type=int, default=12288)
    i.add_argument("--block", type=int, default=4096)
    i.add_argument("--sector", type=int, default=512)
    i.set_defaults(f=cmd_inode)
    f = sp.add_parser("fsize")
    f.add_argument("--block", type=int, default=4096)
    f.add_argument("--ptr", type=int, default=4)
    f.add_argument("--direct", type=int, default=12)
    f.add_argument("--indirect", type=int, default=1)
    f.add_argument("--double", type=int, default=0)
    f.add_argument("--triple", type=int, default=0)
    f.set_defaults(f=cmd_fsize)
    c = sp.add_parser("checksum")
    c.add_argument("--hex", required=True, help="16-bit words in hex, comma-separated")
    c.add_argument("--width", type=int, default=4)
    c.set_defaults(f=cmd_checksum)
    io = sp.add_parser("io-count")
    io.add_argument("--op", required=True)
    io.add_argument("--depth", type=int, default=2)
    io.set_defaults(f=cmd_io_count)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

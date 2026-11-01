# -*- coding: utf-8 -*-
"""
chmod_calc.py - permissions calculator (octal <-> symbolic), umask and special modes.
Local calculation only: does not change files, no network.

Based on the book (TLDP = Garrels, Introduction to Linux 1.27; pages = PDF; printed = PDF-8):
  - u/g/o categories and r=4 w=2 x=1 codes (TLDP p.68-69)
  - symbolic chmod with +, - and comma-separated lists (TLDP p.70); '=' appears in 'chmod o=' (TLDP p.73)
  - table of common modes 3-9 (TLDP p.70-71); fewer than 3 digits -> leading zeros; 4th digit = special modes (TLDP p.71)
  - umask: value SUBTRACTED from 777 (directory) and 666 (file) (TLDP p.72)
  - sticky (t), SUID/SGID (s), SGID on a directory (TLDP p.74, 86-87)
Items marked [extrapolation] go beyond the book (e.g. umask is formally a bitwise operation; 'X'; special
modes in 4-digit octal beyond what the book details).

Usage:
  python -I chmod_calc.py octal 755            # -> rwxr-xr-x and explanation per category
  python -I chmod_calc.py octal 4755           # SUID
  python -I chmod_calc.py from-ls -rwxr-x--x   # -> octal
  python -I chmod_calc.py symbolic "u+rwx,go-rwx" --from 664 [--dir]
  python -I chmod_calc.py umask 0027 [--dir]   # resulting permissions (book's subtraction vs bitwise)
  python -I chmod_calc.py common               # the book's table 3-9
  python -I chmod_calc.py check 777 --path /var/www/uploads   # assesses risk (heuristic; [extrapolation])
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

COMMON = [
    ("400", "file", "protect against accidental overwriting"),
    ("500", "directory", "avoid removing/renaming/moving files in the directory by mistake"),
    ("600", "file", "private file, changeable only by the owner"),
    ("644", "file", "readable by everyone, changeable only by the owner"),
    ("660", "file", "owner and group can change it; others have no access"),
    ("700", "file/directory", "no access for others; owner has full access"),
    ("755", "directory", "readable/executable by others, changeable only by the owner"),
    ("775", "file", "default mode for group sharing"),
    ("777", "file", "everyone can do everything"),
]


def triad(n):
    return ("r" if n & 4 else "-") + ("w" if n & 2 else "-") + ("x" if n & 1 else "-")


def mode_to_str(mode):
    """mode: integer of up to 12 bits (0o7777)."""
    u, g, o = (mode >> 6) & 7, (mode >> 3) & 7, mode & 7
    s = [list(triad(u)), list(triad(g)), list(triad(o))]
    if mode & 0o4000:
        s[0][2] = "s" if u & 1 else "S"
    if mode & 0o2000:
        s[1][2] = "s" if g & 1 else "S"
    if mode & 0o1000:
        s[2][2] = "t" if o & 1 else "T"
    return "".join("".join(x) for x in s)


def parse_octal(txt):
    if not re.fullmatch(r"[0-7]{1,4}", txt):
        raise ValueError("invalid octal mode (use 1 to 4 digits from 0 to 7)")
    return int(txt, 8)


def explain(mode):
    names = ["owner (u)", "group (g)", "others (o)"]
    shifts = [6, 3, 0]
    out = []
    for nm, sh in zip(names, shifts):
        v = (mode >> sh) & 7
        perms = [p for p, b in (("read", 4), ("write", 2), ("execute", 1)) if v & b]
        out.append(f"  {nm}: {v} = {triad(v)} ({', '.join(perms) or 'no permissions'})  [from source: TLDP p.68-69]")
    sp = []
    if mode & 0o4000:
        sp.append("SUID (s on owner): executable runs with the permissions of the file owner [from source: TLDP p.74, 86-87]")
    if mode & 0o2000:
        sp.append("SGID (s on group): on an executable it runs with the file's group; on a directory, new files inherit the group [from source: TLDP p.74]")
    if mode & 0o1000:
        sp.append("sticky (t): on a directory, only the file owner can change/delete their files [from source: TLDP p.74]")
    return out, sp


def cmd_octal(a):
    mode = parse_octal(a.value)
    print(f"octal {mode:04o}  ->  {mode_to_str(mode)}")
    lines, sp = explain(mode)
    print("\n".join(lines))
    for s in sp:
        print("  " + s)
    if len(a.value) < 3:
        print(f"  note: with fewer than 3 digits, the missing ones become leading zeros: {mode:03o} [from source: TLDP p.71]")
    if len(a.value) == 4:
        print("  note: the 4th digit (on the left) controls special modes [from source: TLDP p.71; details are [extrapolation]]")
    warn(mode)


def warn(mode):
    w = []
    if mode & 0o002:
        if mode & 0o1000:
            w.append("others can write, but sticky limits changing/removing other users' files in the directory: the /var/tmp default (TLDP p.74)")
        else:
            w.append("others can WRITE (world-writable): any user can change it [extrapolation; the book only describes 777 as 'everybody can do everything', TLDP p.71]")
    if mode & 0o6000:
        w.append("SUID/SGID present: the book asks for minimal use, because of security risk (TLDP p.86)")
    for x in w:
        print("  WARNING: " + x)


def cmd_from_ls(a):
    s = a.value.strip()
    m = re.fullmatch(r"[-dlcspb]?([rwxsStT-]{9})", s)
    if not m:
        raise ValueError("use the 9-character (or 10, with the type) string from ls -l, e.g. -rwxr-xr-x")
    p = m.group(1)
    mode = 0
    for cls in range(3):
        r, w, x = p[cls * 3: cls * 3 + 3]
        sh = 6 - 3 * cls
        if r not in "r-" or w not in "w-":
            raise ValueError("invalid read/write position in '%s'" % s)
        if r == "r":
            mode |= 4 << sh
        if w == "w":
            mode |= 2 << sh
        if x in "xst":
            mode |= 1 << sh
        if x in "sS" and cls == 2 or x in "tT" and cls < 2:
            raise ValueError("s/S only apply to owner and group; t/T only to others")
        if x in "sS":
            mode |= 0o4000 if cls == 0 else 0o2000
        if x in "tT":
            mode |= 0o1000
    print(f"{s} -> {mode:04o}" + ("  (4 digits: there is a special mode, TLDP p.71, 74)" if mode > 0o777 else ""))
    print("  " + mode_to_str(mode))
    warn(mode)


def apply_symbolic(expr, cur, is_dir):
    """Applies 'u+rwx,go-w,o=r' etc. Supports r w x s t X (X is [extrapolation])."""
    notes = []
    for clause in expr.split(","):
        m = re.fullmatch(r"([ugoa]*)([+\-=])([rwxstX]*)", clause.strip())
        if not m:
            raise ValueError(f"unsupported symbolic clause: '{clause}' (supports [ugoa][+-=][rwxstX])")
        who, op, perms = m.groups()
        who = who or "a"
        if "a" in who:
            who = "ugo"
        bits = 0
        for ch in perms:
            if ch == "X":
                notes.append("'X' is not from the book [extrapolation]: applied as x only if directory or already executable")
                if is_dir or (cur & 0o111):
                    bits |= 1
                continue
            if ch in "rwx":
                bits |= {"r": 4, "w": 2, "x": 1}[ch]
        mask = 0
        special = 0
        for w in who:
            sh = {"u": 6, "g": 3, "o": 0}[w]
            mask |= 7 << sh
        setbits = 0
        for w in who:
            sh = {"u": 6, "g": 3, "o": 0}[w]
            setbits |= bits << sh
        if "s" in perms:
            if "u" in who:
                special |= 0o4000
            if "g" in who:
                special |= 0o2000
        if "t" in perms:
            special |= 0o1000
        if op == "+":
            cur |= setbits | special
        elif op == "-":
            cur &= ~(setbits | special)
        else:
            cur = (cur & ~mask) | setbits
            if "u" in who:
                cur &= ~0o4000
                cur |= special & 0o4000
            if "g" in who:
                cur &= ~0o2000
                cur |= special & 0o2000
            if "o" in who:
                cur &= ~0o1000
                cur |= special & 0o1000
    return cur, notes


def cmd_symbolic(a):
    cur = parse_octal(a.start)
    new, notes = apply_symbolic(a.expr, cur, a.dir)
    print(f"before: {cur:04o}  {mode_to_str(cur)}")
    print(f"expr  : chmod {a.expr}")
    print(f"after : {new:04o}  {mode_to_str(new)}   [symbolic form: TLDP p.70; '=': TLDP p.73]")
    for n in notes:
        print("  note: " + n)
    if a.dir and not (new & 0o111):
        print("  WARNING: a directory without x is not accessible (the book suggests trying chmod 644 on a directory, TLDP p.72)")
    warn(new)


def cmd_umask(a):
    m = parse_octal(a.value)
    base = 0o777 if a.dir else 0o666
    # the book's model: subtraction
    sub = []
    for sh in (6, 3, 0):
        b, mk = (base >> sh) & 7, (m >> sh) & 7
        sub.append(max(b - mk, 0))
    sub_mode = (sub[0] << 6) | (sub[1] << 3) | sub[2]
    bit = base & ~m & 0o777
    kind = "directory" if a.dir else "file"
    print(f"umask {m:04o}, new {kind} (base {base:03o})")
    print(f"  book model (subtraction, TLDP p.72): {sub_mode:03o}  {mode_to_str(sub_mode)}")
    print(f"  bitwise (base & ~umask) [extrapolation]: {bit:03o}  {mode_to_str(bit)}")
    if sub_mode != bit:
        print("  WARNING: the two results DIFFER. The book teaches subtraction (valid for common masks such as 022/002);")
        print("  the kernel/shell apply the bitwise operation, so the 'bitwise' value is the real one [extrapolation].")
    else:
        print("  the two models agree for this mask.")
    print("  note: root usually has umask 022 and users with a private group 002 (TLDP p.72-73, 127)")


def cmd_common(a):
    print("Book table 3-9 (TLDP p.70-71): common chmod modes")
    for m, what, why in COMMON:
        v = int(m, 8)
        print(f"  {m}  {mode_to_str(v)}  ({what}): {why}")
    print("The book does not discuss ACLs, umask inherited by services, or 'chmod -R 777' as a risk.")


def cmd_check(a):
    mode = parse_octal(a.value)
    print(f"{mode:04o} {mode_to_str(mode)}" + (f"  on {a.path}" if a.path else ""))
    warn(mode)
    if not (mode & 0o6002):
        print("  no obvious risk alert (heuristic; does not replace a review in context).")
    if a.path and re.search(r"(\.ssh|id_rsa|shadow|\.gnupg)", a.path):
        print("  note [extrapolation]: key/secret files usually require 600/700; the book shows /etc/shadow as 400 (TLDP p.182) and private keys protected by a passphrase (TLDP p.161, 189).")


def main():
    ap = argparse.ArgumentParser(description="Permissions calculator (chmod/umask) based on the TLDP book.")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("octal"); p.add_argument("value"); p.set_defaults(fn=cmd_octal)
    p = sp.add_parser("from-ls"); p.add_argument("value"); p.set_defaults(fn=cmd_from_ls)
    p = sp.add_parser("symbolic"); p.add_argument("expr"); p.add_argument("--from", dest="start", default="644"); p.add_argument("--dir", action="store_true"); p.set_defaults(fn=cmd_symbolic)
    p = sp.add_parser("umask"); p.add_argument("value"); p.add_argument("--dir", action="store_true"); p.set_defaults(fn=cmd_umask)
    p = sp.add_parser("common"); p.set_defaults(fn=cmd_common)
    p = sp.add_parser("check"); p.add_argument("value"); p.add_argument("--path"); p.set_defaults(fn=cmd_check)
    argv = sys.argv[1:]
    if argv and argv[0] == "from-ls" and len(argv) == 2 and argv[1].startswith("-"):
        argv = ["from-ls", "--", argv[1]]
    a = ap.parse_args(argv)
    try:
        a.fn(a)
    except ValueError as e:
        print("ERROR: " + str(e))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

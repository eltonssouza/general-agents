# -*- coding: utf-8 -*-
"""
css_calc.py - deterministic CSS calculators (stdlib only, no network, no writes).

Subcommands:
  units VALOR UNIDADE [--base 16] [--parent PX] [--viewport LxA]
        converts to px using the Handbook equivalences (CSSHB p.45-47):
        1in = 96px; 1cm ~ 37.8px; 1mm = 0.1cm; 1q = 1/4 mm; 1in = 72pt; 1pc = 12pt;
        rem/em depend on --base (font-size in px, value you provide);
        % depends on --parent (parent px, CSSHB p.45-46); vw/vh depend on --viewport.
  box --width W [--height H] [--padding "t r b l"] [--border "t r b l"] [--margin "t r b l"] [--sizing content-box|border-box]
        size of the content, the box and the occupied space (CSSHB p.83-85, 93-94, 97-99). Shorthands with 1 to 4 values.
  flex --container PX --items "basis:grow:shrink,..." [--gap PX]
        distributes the free space in a row flex container. grow follows CSSHB p.155; the weighting of shrink
        by basis is [extrapolation] (the book only gives the simple proportion). Ignores min/max-content and max-width.
  grid --columns "200px 1fr 2fr" --width PX [--gap PX] [--base 16] [--item "2/4"]
        track sizes (px, %, rem/em, fr, repeat(n, x)); fr divides the remaining space (CSSHB p.134-136);
        --item uses grid lines 1..n+1 (CSSHB p.131-134).
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PX_PER = {"px": 1.0, "in": 96.0, "cm": 96.0 / 2.54, "mm": 96.0 / 25.4, "q": 96.0 / 101.6, "pt": 96.0 / 72.0, "pc": 16.0}


def r(x):
    return f"{x:.4f}".rstrip("0").rstrip(".")


def to_px(value, unit, base=16.0, parent=None, vw=None, vh=None):
    u = unit.lower()
    if u in PX_PER:
        return value * PX_PER[u]
    if u in ("rem", "em"):
        return value * base
    if u == "%":
        if parent is None:
            raise ValueError("% requires --parent (px of the parent element)")
        return value * parent / 100.0
    if u in ("vw", "vh", "vmin", "vmax"):
        if vw is None or vh is None:
            raise ValueError("vw/vh require --viewport WxH")
        ref = {"vw": vw, "vh": vh, "vmin": min(vw, vh), "vmax": max(vw, vh)}[u]
        return value * ref / 100.0
    raise ValueError(f"unsupported unit: {unit} (supported: px in cm mm q pt pc rem em % vw vh vmin vmax)")


def cmd_units(a):
    vw = vh = None
    if a.viewport:
        m = re.fullmatch(r"(\d+(?:\.\d+)?)[xX](\d+(?:\.\d+)?)", a.viewport)
        if not m:
            print("--viewport must have the format WxH, e.g. 1280x720", file=sys.stderr)
            return 2
        vw, vh = float(m.group(1)), float(m.group(2))
    try:
        px = to_px(a.value, a.unit, a.base, a.parent, vw, vh)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print(f"{r(a.value)}{a.unit} = {r(px)}px")
    print(f"  = {r(px / 96.0)}in = {r(px / PX_PER['cm'])}cm = {r(px / PX_PER['mm'])}mm = {r(px / PX_PER['pt'])}pt = {r(px / PX_PER['pc'])}pc")
    print(f"  = {r(px / a.base)}rem/em (base {r(a.base)}px, supplied by you)")
    print("Source: equivalences in CSSHB p.46 (the book rounds 1cm to ~37.8px); rem/em: CSSHB p.46; %: CSSHB p.45-46.")
    print("Note: px in CSS is a reference unit, not a physical pixel (CSSHB p.45).")
    return 0


def parse_box(s, name):
    if s is None:
        return (0.0, 0.0, 0.0, 0.0)
    parts = [float(x) for x in s.replace(",", " ").split()]
    n = len(parts)
    if n == 1:
        return (parts[0],) * 4
    if n == 2:
        return (parts[0], parts[1], parts[0], parts[1])  # CSSHB p.93: vertical, horizontal
    if n == 3:
        return (parts[0], parts[1], parts[2], parts[1])  # top, sides, bottom
    if n == 4:
        return tuple(parts)  # top-right-bottom-left (CSSHB p.94)
    raise ValueError(f"--{name} accepts 1 to 4 values")


def cmd_box(a):
    try:
        pad, bor, mar = parse_box(a.padding, "padding"), parse_box(a.border, "border"), parse_box(a.margin, "margin")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    ph, pv = pad[1] + pad[3], pad[0] + pad[2]
    bh, bv = bor[1] + bor[3], bor[0] + bor[2]
    mh, mv = mar[1] + mar[3], mar[0] + mar[2]
    res = {}
    for dim, size, p, b, m in (("width", a.width, ph, bh, mh), ("height", a.height, pv, bv, mv)):
        if size is None:
            continue
        if a.sizing == "content-box":
            content, border_box = size, size + p + b
        else:
            content, border_box = size - p - b, size
        res[dim] = (content, border_box, border_box + m)
    print(f"box-sizing: {a.sizing}   (browser default: content-box, CSSHB p.85, 97-98)")
    print(f"padding (t r b l): {' '.join(r(x) for x in pad)}   border: {' '.join(r(x) for x in bor)}   margin: {' '.join(r(x) for x in mar)}")
    for dim, (c, bb, tot) in res.items():
        print(f"{dim}: content={r(c)}px | box (content+padding+border)={r(bb)}px | occupied space (+margin)={r(tot)}px")
        if c < 0:
            print(f"  WARNING: in border-box the content would be negative; the browser clamps it to 0 and the box grows [inference]")
    print("Formula [inference from CSSHB p.85]: content-box -> total = width + padding + border + margin; border-box -> width already includes padding and border.")
    return 0


def cmd_flex(a):
    items = []
    for i, tok in enumerate(a.items.split(","), 1):
        f = tok.strip().split(":")
        try:
            basis = float(f[0])
            grow = float(f[1]) if len(f) > 1 and f[1] != "" else 0.0   # default 0 (CSSHB p.155)
            shrink = float(f[2]) if len(f) > 2 and f[2] != "" else 1.0  # default 1 (CSSHB p.155)
        except ValueError:
            print(f"Error: invalid item {i} ('{tok}'). Use basis[:grow[:shrink]] in px.", file=sys.stderr)
            return 2
        items.append([basis, grow, shrink])
    n = len(items)
    gaps = a.gap * (n - 1)
    total_basis = sum(x[0] for x in items)
    free = a.container - total_basis - gaps
    sizes = []
    mode = "no free space"
    if free > 1e-9:
        sg = sum(x[1] for x in items)
        mode = "growth (flex-grow, CSSHB p.155)" if sg > 0 else "space left over, but no item has flex-grow > 0 (default 0): nothing grows"
        sizes = [x[0] + (free * x[1] / sg if sg > 0 else 0) for x in items]
    elif free < -1e-9:
        w = sum(x[2] * x[0] for x in items)
        mode = "shrinking (flex-shrink; weighted by basis: [extrapolation], CSSHB p.155 gives only the proportion)"
        sizes = [x[0] + (free * (x[2] * x[0]) / w if w > 0 else 0) for x in items]
        sizes = [max(0.0, s) for s in sizes]
    else:
        sizes = [x[0] for x in items]
    print(f"container={r(a.container)}px  items={n}  gap={r(a.gap)}px  sum of basis={r(total_basis)}px  free space={r(free)}px")
    print(f"mode: {mode}")
    for i, (it, s) in enumerate(zip(items, sizes), 1):
        print(f"  item {i}: basis={r(it[0])} grow={r(it[1])} shrink={r(it[2])} -> {r(s)}px")
    print(f"final sum = {r(sum(sizes) + gaps)}px (includes gaps)")
    print("Limits: ignores min-width/min-content/max-width and flex-wrap (the book does not detail the full algorithm).")
    return 0


def split_top(s):
    out, depth, cur = [], 0, []
    for c in s:
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c.isspace() and depth == 0:
            if cur:
                out.append("".join(cur))
                cur = []
        else:
            cur.append(c)
    if cur:
        out.append("".join(cur))
    return out


def expand_tracks(spec):
    toks = []
    for t in split_top(spec.strip()):
        m = re.fullmatch(r"repeat\(\s*(\d+)\s*,\s*(.+)\)", t)
        if m:
            toks.extend(split_top(m.group(2)) * int(m.group(1)))
        else:
            toks.append(t)
    return toks


def cmd_grid(a):
    tracks = expand_tracks(a.columns)
    fixed, fr_total, kinds = 0.0, 0.0, []
    for t in tracks:
        m = re.fullmatch(r"(\d+(?:\.\d+)?|\.\d+)(fr|px|%|rem|em|in|cm|mm|pt|pc|q)", t)
        if not m:
            print(f"Error: unsupported track '{t}' (supported: Npx, N%, Nrem, Nfr, repeat(n, x); minmax()/auto: use the book and check manually, CSSHB p.127, 136-137)", file=sys.stderr)
            return 2
        v, u = float(m.group(1)), m.group(2)
        if u == "fr":
            fr_total += v
            kinds.append(("fr", v))
        else:
            px = to_px(v, u, a.base, a.width)
            fixed += px
            kinds.append(("px", px))
    n = len(tracks)
    gaps = a.gap * (n - 1)
    remaining = a.width - fixed - gaps
    sizes = []
    for k, v in kinds:
        if k == "px":
            sizes.append(v)
        else:
            sizes.append(max(0.0, remaining) * v / fr_total if fr_total > 0 else 0.0)
    print(f"container width={r(a.width)}px  tracks={n}  gap={r(a.gap)}px")
    print(f"fixed={r(fixed)}px  gaps={r(gaps)}px  remaining for fr={r(remaining)}px  sum of fr={r(fr_total)}")
    pos = 0.0
    for i, s in enumerate(sizes, 1):
        print(f"  column {i} (lines {i}-{i + 1}): {r(s)}px  [starts at x={r(pos)}px]")
        pos += s + a.gap
    total = sum(sizes) + gaps
    print(f"sum of tracks + gaps = {r(total)}px")
    if remaining < 0:
        print("WARNING: fixed tracks + gaps exceed the width; there will be overflow [inference].")
    if a.item:
        m = re.fullmatch(r"(\d+)\s*/\s*(?:(span)\s+)?(\d+)", a.item.strip())
        if not m:
            print("Error: --item must be 'start/end' or 'start/span N' (CSSHB p.133-134)", file=sys.stderr)
            return 2
        s = int(m.group(1))
        e = s + int(m.group(3)) if m.group(2) else int(m.group(3))
        if not (1 <= s < e <= n + 1):
            print(f"Error: lines outside 1..{n + 1}", file=sys.stderr)
            return 2
        w = sum(sizes[s - 1:e - 1]) + a.gap * (e - s - 1)
        print(f"item grid-column {s} / {e}: spans {e - s} column(s) = {r(w)}px (lines numbered from 1, CSSHB p.132)")
    print("Note [extrapolation]: the real fr calculation considers the minimum content size of the items (min-content), not modeled here.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="CSS calculators (CSSHB)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("units")
    u.add_argument("value", type=float)
    u.add_argument("unit")
    u.add_argument("--base", type=float, default=16.0, help="base font-size in px for rem/em (default 16, a convention value supplied by the user)")
    u.add_argument("--parent", type=float, default=None)
    u.add_argument("--viewport", default=None)
    b = sub.add_parser("box")
    b.add_argument("--width", type=float, required=True)
    b.add_argument("--height", type=float, default=None)
    b.add_argument("--padding", default=None)
    b.add_argument("--border", default=None)
    b.add_argument("--margin", default=None)
    b.add_argument("--sizing", choices=["content-box", "border-box"], default="content-box")
    f = sub.add_parser("flex")
    f.add_argument("--container", type=float, required=True)
    f.add_argument("--items", required=True)
    f.add_argument("--gap", type=float, default=0.0)
    g = sub.add_parser("grid")
    g.add_argument("--columns", required=True)
    g.add_argument("--width", type=float, required=True)
    g.add_argument("--gap", type=float, default=0.0)
    g.add_argument("--base", type=float, default=16.0)
    g.add_argument("--item", default=None)
    a = ap.parse_args(argv)
    return {"units": cmd_units, "box": cmd_box, "flex": cmd_flex, "grid": cmd_grid}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

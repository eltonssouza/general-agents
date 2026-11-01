# -*- coding: utf-8 -*-
"""
contrast.py - WCAG 2.2 contrast ratio between color pairs and a verdict per criterion.

Formulas (WCAG 2.2, glossary, checked against the W3C specification on 2026-11-01):
  linear channel = c/12.92 if c <= 0.04045, else ((c + 0.055)/1.055) ** 2.4   (c = sRGB channel in 0..1)
  luminance      = 0.2126*R + 0.7152*G + 0.0722*B
  ratio          = (L1 + 0.05) / (L2 + 0.05), L1 = the lighter one
Criteria: 1.4.3 (AA) text 4.5:1, large text 3:1; 1.4.6 (AAA) 7:1 and 4.5:1; 1.4.11 (AA) components 3:1.
The comparison uses the exact value (WCAG does not round: 4.48 does not pass 4.5).

Usage:
  python -I contrast.py "#767676" "#FFFFFF"           one pair: foreground and background
  python -I contrast.py "#000/#fff" "#777/#fff"       several pairs in foreground/background format
  python -I contrast.py "#777/#fff" --json
Accepts #RGB and #RRGGBB (the # is optional). Calculation only; no network.
Exit: 0 all pairs pass AA for normal text; 1 some pair fails; 2 usage error.
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

CRITERIA = [  # (name, WCAG criterion, threshold)
    ("AA normal text", "1.4.3", 4.5),
    ("AA large text", "1.4.3", 3.0),
    ("AA components/graphics", "1.4.11", 3.0),
    ("AAA normal text", "1.4.6", 7.0),
    ("AAA large text", "1.4.6", 4.5),
]


def parse(color):
    c = color.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{3}|[0-9a-fA-F]{6}", c):
        raise ValueError("invalid color: %s (use #RGB or #RRGGBB)" % color)
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(rgb):
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(fg, bg):
    l1, l2 = sorted((luminance(parse(fg)), luminance(parse(bg))), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("colors", nargs="+", help="two colors (foreground background) or foreground/background pairs")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if all("/" in c for c in a.colors):
        pairs = [tuple(c.split("/", 1)) for c in a.colors]
    elif len(a.colors) == 2 and not any("/" in c for c in a.colors):
        pairs = [tuple(a.colors)]
    else:
        print("Error: pass two colors (foreground background) or only foreground/background pairs.")
        return 2
    out = []
    try:
        for fg, bg in pairs:
            r = ratio(fg, bg)
            out.append({"foreground": fg, "background": bg, "ratio": round(r, 2),
                        "criterios": {n: r >= lim for n, _, lim in CRITERIA}})
    except ValueError as e:
        print("Error: %s" % e)
        return 2
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        for o in out:
            print("%s on %s: %.2f:1" % (o["foreground"], o["background"], o["ratio"]))
            for n, crit, lim in CRITERIA:
                print("  %-26s (%s, >= %.1f:1): %s" % (n, crit, lim, "pass" if o["criterios"][n] else "FAIL"))
        print("\n[WCAG 2.2] Ratio by the standard's formula. Large text = 18 pt, or 14 pt bold."
              " The script does not measure font size or touch target size (AA: 24x24 CSS px, 2.5.8).")
    return 0 if all(o["criterios"]["AA normal text"] for o in out) else 1


if __name__ == "__main__":
    sys.exit(main())

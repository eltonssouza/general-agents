# -*- coding: utf-8 -*-
"""
game_loop_simulator.py - simulates the fixed-step loop with a lag accumulator (calculation only, no network).

ORIGIN OF THE RULES
  [from source] Game Programming Patterns (Nystrom), Game Loop chapter, the "fixed update step, variable rendering"
  version: accumulate `lag += elapsed`; while `lag >= MS_PER_UPDATE` run update() and subtract; then render with the
  residual `lag / MS_PER_UPDATE`, a value between 0 and almost 1 (GPP p.138-141).
  [from source] The step must be larger than the time of one update() on the slowest machine; the inner loop may have a
  maximum number of iterations so the game slows down instead of freezing - with NO number (GPP p.139).
  [from source] Numeric rendering example: object at 20 px, 400 px per frame, fraction 0.5 => drawn at 220 px
  (GPP p.141).
  [extrapolation] The default value of the cap (--max-updates 8) and the decision to discard the excess lag are choices of
  this script, NOT of the book. The term "death spiral" is not from GPP.
  [extrapolation] The position formula render = pos + vel * alpha is the book's example (p.141), generalized.

Usage:
  python -I game_loop_simulator.py --demo
  python -I game_loop_simulator.py --physics-hz 60 --frames 16.6 35.0 10.0 50.0
  python -I game_loop_simulator.py --frames 16 90 --max-updates 3
  python -I game_loop_simulator.py --render-pos 20 --velocity 400 --alpha 0.5     # => 220 (GPP p.141)
  python -I game_loop_simulator.py --check-step 16.67 --update-cost 20           # warns if the step is smaller than the cost
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def render_position(pos, velocity_per_update, alpha):
    """Drawn position: advances `alpha` of one step (GPP p.141: 20 + 400*0.5 = 220)."""
    return pos + velocity_per_update * alpha


def simulate(ms_per_update, frames_ms, max_updates=None):
    """Returns a list of dicts, one per frame. max_updates=None => no cap (the book only says one can have one)."""
    lag = 0.0
    rows = []
    for i, elapsed in enumerate(frames_ms, 1):
        if elapsed < 0:
            raise ValueError("negative frame duration: %s" % elapsed)
        lag_before = lag
        lag += elapsed
        updates = 0
        capped = False
        while lag >= ms_per_update:
            if max_updates is not None and updates >= max_updates:
                capped = True
                lag = 0.0  # [extrapolation] discards the excess so the game does not freeze
                break
            lag -= ms_per_update
            updates += 1
        rows.append({"frame": i, "elapsed": elapsed, "lag_before": lag_before, "updates": updates,
                     "lag_after": lag, "alpha": lag / ms_per_update, "capped": capped})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fixed-step Game Loop simulator (GPP p.138-141).")
    ap.add_argument("--physics-hz", type=float, default=60.0, help="update rate in Hz (default 60; the value is your choice)")
    ap.add_argument("--frames", nargs="+", type=float, help="real frame durations in ms")
    ap.add_argument("--max-updates", type=int, default=8,
                    help="cap on updates per frame [extrapolation]; 0 = no cap (default 8)")
    ap.add_argument("--demo", action="store_true", help="demonstration with frame fluctuations")
    ap.add_argument("--render-pos", type=float, help="current position for the rendering calculation")
    ap.add_argument("--velocity", type=float, help="velocity in units per update step")
    ap.add_argument("--alpha", type=float, help="fraction lag/MS_PER_UPDATE (0 to <1)")
    ap.add_argument("--check-step", type=float, help="MS_PER_UPDATE in ms, for the GPP p.139 check")
    ap.add_argument("--update-cost", type=float, help="measured cost of one update() in ms, on the slowest machine")
    a = ap.parse_args(argv)

    if a.render_pos is not None:
        if a.velocity is None or a.alpha is None:
            ap.error("--render-pos requires --velocity and --alpha")
        if not 0.0 <= a.alpha < 1.0:
            print("Warning: alpha outside [0,1); the book describes the value between 0 and almost 1 (GPP p.141).")
        print("drawn position = %.4g  [from source, example from GPP p.141: 20, 400, 0.5 => 220]" %
              render_position(a.render_pos, a.velocity, a.alpha))
        return 0

    if a.check_step is not None:
        if a.update_cost is None:
            ap.error("--check-step requires --update-cost")
        if a.check_step <= a.update_cost:
            print("DANGER: MS_PER_UPDATE (%.2f ms) <= update cost (%.2f ms): the game cannot catch up with real time "
                  "(GPP p.139). Increase the step, reduce the cost or use an iteration cap." % (a.check_step, a.update_cost))
            return 1
        print("OK: step %.2f ms > update cost %.2f ms (condition from GPP p.139)." % (a.check_step, a.update_cost))
        return 0

    if a.demo:
        frames = [16.7, 35.0, 8.0, 150.0, 16.7, 16.7]
        hz = 60.0
    elif a.frames:
        frames, hz = a.frames, a.physics_hz
    else:
        ap.print_help()
        return 2
    if hz <= 0:
        ap.error("--physics-hz must be > 0")
    cap = None if a.max_updates == 0 else a.max_updates
    ms = 1000.0 / hz
    print("=== Fixed-step Game Loop (GPP p.138-141) ===")
    print("MS_PER_UPDATE = %.3f ms (%.1f Hz)   cap on updates per frame = %s [extrapolation]" %
          (ms, hz, "no cap" if cap is None else cap))
    print("%-6s %-10s %-10s %-8s %-10s %-8s" % ("frame", "elapsed", "lag_before", "updates", "lag_after", "alpha"))
    capped = 0
    total = 0
    for r in simulate(ms, frames, cap):
        total += r["updates"]
        capped += r["capped"]
        print("%-6d %-10.2f %-10.2f %-8d %-10.2f %-8.3f%s" % (r["frame"], r["elapsed"], r["lag_before"], r["updates"],
                                                              r["lag_after"], r["alpha"],
                                                              "  <- cap reached, lag discarded" if r["capped"] else ""))
    print("total updates: %d; frames rendered: %d" % (total, len(frames)))
    print("Alpha is lag/MS_PER_UPDATE, the argument of render() (GPP p.140-141).")
    if capped:
        print("The cap was reached in %d frame(s): the game slows down instead of freezing; the book mentions this safeguard "
              "without giving a number (GPP p.139)." % capped)
    return 0


if __name__ == "__main__":
    sys.exit(main())

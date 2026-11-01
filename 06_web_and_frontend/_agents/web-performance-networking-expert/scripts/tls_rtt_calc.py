# -*- coding: utf-8 -*-
"""
Skill: tls-handshake-rtt-calc
Computes connection-setup RTTs (TCP + TLS) and slow-start RTTs according to the model of
*High Performance Browser Networking* (Grigorik, 2013). Standard library only, no network.

Book model (PDF pages):
  TCP three-way handshake = 1 RTT before data ......... HPBN p.33
  TCP Fast Open (repeat connections only, limited cases) . HPBN p.34
  TLS full = 2 RTTs; resumed = 1 RTT ................ HPBN p.70, p.73, p.75
  TCP + TLS in the worst case = 3 RTTs (168 ms with RTT 56 ms) . HPBN p.83
  initial cwnd 4 (old) or 10 segments (RFC 6928, IW10) HPBN p.38, p.44
  example: 20 KB on a new connection 264 ms x 96 ms reused .. HPBN p.43, p.44
TLS 1.3 / 0-RTT are NOT in the book: with --tls13 the script shows those scenarios as
[extrapolation] (RFC 8446), with no page.

Usage:
  python -I tls_rtt_calc.py --rtt 120 [--resumed] [--tfo] [--payload-kb 20] [--initcwnd 10] [--server-ms 40]
  python -I tls_rtt_calc.py --compare --rtt 56 --payload-kb 20 [--tls13]
"""

import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MSS_BYTES = 1460  # [inference] typical MSS with a 1,500-byte MTU; the book's example uses segments of ~1.4 KB


def flights(payload_kb, initcwnd):
    """Slow-start flights (cwnd doubles every RTT, no loss) needed to deliver the payload."""
    segments = -(-int(payload_kb * 1024) // MSS_BYTES)
    cwnd, sent, n = initcwnd, 0, 0
    while sent < segments:
        sent += cwnd
        cwnd *= 2
        n += 1
    return segments, n


def scenario(rtt, tls="tls12", resumed=False, tfo=False, payload_kb=20.0, initcwnd=10, server_ms=0.0):
    rows = []
    tcp = 0.0 if tfo else 1.0
    rows.append(("TCP", tcp, "[from source] TFO removes the handshake RTT only on repeat connections (HPBN p.34)" if tfo
                 else "[from source] three-way handshake = 1 RTT (HPBN p.33)"))
    if tls == "plain":
        t = 0.0
        rows.append(("TLS", t, "no TLS"))
    elif tls == "tls12":
        t = 1.0 if resumed else 2.0
        rows.append(("TLS", t, "[from source] abbreviated handshake = 1 RTT (HPBN p.70, p.73, p.75)" if resumed
                     else "[from source] full handshake = 2 RTTs (HPBN p.70, p.83)"))
    else:
        t = 0.0 if resumed else 1.0
        rows.append(("TLS", t, "[extrapolation] TLS 1.3 (RFC 8446), outside the 2013 book"
                     + (" — 0-RTT with early data" if resumed else " — 1 RTT")))
    segs, n = flights(payload_kb, initcwnd)
    rows.append(("Request + response", float(n),
                 f"[inference] {segs} segments in {n} slow-start flight(s) with initial cwnd {initcwnd} "
                 "(HPBN p.41–43 model; cwnd doubles every RTT, no loss)"))
    total = sum(r[1] for r in rows)
    return rows, total, total * rtt + server_ms


def main():
    ap = argparse.ArgumentParser(description="TCP/TLS and slow-start RTTs in the HPBN (2013) model")
    ap.add_argument("--rtt", type=float, default=56.0, help="RTT in ms (the book's example uses 56 ms)")
    ap.add_argument("--plain", action="store_true", help="no TLS")
    ap.add_argument("--resumed", action="store_true")
    ap.add_argument("--tfo", action="store_true")
    ap.add_argument("--payload-kb", type=float, default=20.0)
    ap.add_argument("--initcwnd", type=int, default=10, help="4 (old servers) or 10 (RFC 6928, HPBN p.38)")
    ap.add_argument("--server-ms", type=float, default=0.0, help="response generation time on the server")
    ap.add_argument("--tls13", action="store_true", help="include TLS 1.3 scenarios as [extrapolation]")
    ap.add_argument("--compare", action="store_true")
    args = ap.parse_args()

    if args.compare:
        cases = [("HTTP without TLS", "plain", False, False), ("TLS full", "tls12", False, False),
                 ("TLS resumed", "tls12", True, False), ("TLS full + TFO", "tls12", False, True)]
        if args.tls13:
            cases += [("TLS 1.3 [extrapolation]", "tls13", False, False),
                      ("TLS 1.3 0-RTT [extrapolation]", "tls13", True, False)]
        print(f"RTT = {args.rtt} ms | payload = {args.payload_kb} KB | initcwnd = {args.initcwnd} | server = {args.server_ms} ms")
        for name, tls, res, tfo in cases:
            _, total, ms = scenario(args.rtt, tls, res, tfo, args.payload_kb, args.initcwnd, args.server_ms)
            print(f"  {name:30} {total:4.1f} RTT  {ms:8.1f} ms")
        print("Connection already open: only the data flights (HPBN p.44). Book example: 20 KB, RTT 56 ms, "
              "264 ms new x 96 ms reused (HPBN p.43, p.44).")
        return

    tls = "plain" if args.plain else ("tls13" if args.tls13 else "tls12")
    rows, total, ms = scenario(args.rtt, tls, args.resumed, args.tfo, args.payload_kb, args.initcwnd, args.server_ms)
    for name, r, note in rows:
        print(f"{name:22} {r:4.1f} RTT  {note}")
    print(f"TOTAL: {total:.1f} RTT x {args.rtt} ms + {args.server_ms} ms = {ms:.1f} ms")
    print("Calculations with the user's numbers are an [inference] on the book's model.")


if __name__ == "__main__":
    main()

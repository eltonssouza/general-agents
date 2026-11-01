# -*- coding: utf-8 -*-
"""
Skill: http2-frame-analyzer
Reads a sequence of frames (JSON) and summarizes streams, according to HTTP 2.0 **as the 2013 draft
is described** in *High Performance Browser Networking* (Grigorik). Standard library only, no network.

From the book (PDF pages):
  common 8-byte header; 16-bit length; 8-bit type and flags; 1 reserved bit;
  31-bit stream ID ........................................... HPBN p.244, p.245
  types: DATA, HEADERS, PRIORITY, RST_STREAM, SETTINGS, PUSH_PROMISE, PING, GOAWAY,
         WINDOW_UPDATE, CONTINUATION ................................. HPBN p.245, p.246
  HEADERS opens a stream (optional 31-bit priority); PUSH_PROMISE carries a "promised stream ID" HPBN p.247
  DATA: end of message with the END_STREAM flag; payload <= 2^14-1 bytes is recommended HPBN p.248
  ID parity: the book contradicts itself (p.247 says client = even; the analysis of Fig. 12-9 on
  p.249 treats 1, 3, 5 as the client's). The script does not report a parity error.
[extrapolation] In RFC 7540 (2015) the header has 9 bytes, a 24-bit length and the client uses odd IDs.

Usage:
  python -I http2_frame_analyzer.py --demo
  python -I http2_frame_analyzer.py --file frames.json   # [{"type": "HEADERS", "stream_id": 1, "flags": [], "length": 45}, ...]
"""

import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BOOK_TYPES = {"DATA", "HEADERS", "PRIORITY", "RST_STREAM", "SETTINGS", "PUSH_PROMISE", "PING",
              "GOAWAY", "WINDOW_UPDATE", "CONTINUATION"}
MAX_LEN_DRAFT = 2 ** 16 - 1
DATA_HINT = 2 ** 14 - 1


def analyze(frames):
    streams, notes = {}, []
    for i, f in enumerate(frames, 1):
        t = str(f.get("type", "")).upper()
        sid = int(f.get("stream_id", 0))
        length = int(f.get("length", 0))
        flags = [str(x).upper() for x in f.get("flags", [])]
        if t not in BOOK_TYPES:
            notes.append(f"#{i}: type '{t}' is not in the book's list (HPBN p.245, p.246).")
        if length > MAX_LEN_DRAFT:
            notes.append(f"#{i}: length {length} > 2^16-1, the limit of the 16-bit field in the draft (HPBN p.245). "
                         "[extrapolation] RFC 7540 uses 24 bits.")
        if t == "DATA" and length > DATA_HINT:
            notes.append(f"#{i}: DATA with {length} bytes; the book recommends up to 2^14-1 to reduce HoL "
                         "between streams (HPBN p.248).")
        if sid > 0:
            s = streams.setdefault(sid, {"frames": 0, "bytes": 0, "ended": False, "reset": False, "pushed": False})
            s["frames"] += 1
            s["bytes"] += length
            if "END_STREAM" in flags:
                s["ended"] = True
            if t == "RST_STREAM":
                s["reset"] = True
                notes.append(f"#{i}: RST_STREAM ends stream {sid} abnormally (HPBN p.245); "
                             "the client can use it to refuse a push (HPBN p.238).")
        if t == "PUSH_PROMISE":
            pid = f.get("promised_stream_id")
            notes.append(f"#{i}: PUSH_PROMISE on stream {sid} promising stream {pid} (HPBN p.247); "
                         "push only for same-origin resources, as a response to a request (HPBN p.239).")
            if pid is not None:
                streams.setdefault(int(pid), {"frames": 0, "bytes": 0, "ended": False, "reset": False, "pushed": True})["pushed"] = True
    for sid, s in sorted(streams.items()):
        if not s["ended"] and not s["reset"]:
            notes.append(f"stream {sid}: no END_STREAM or RST_STREAM in the sample — incomplete message (HPBN p.248).")
    return streams, notes


def main():
    ap = argparse.ArgumentParser(description="Frame/stream summary in the HTTP 2.0 draft model (HPBN, 2013)")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--file")
    args = ap.parse_args()
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            frames = json.load(fh)
    else:
        frames = [
            {"type": "SETTINGS", "stream_id": 0, "length": 8},
            {"type": "HEADERS", "stream_id": 1, "length": 45},
            {"type": "PUSH_PROMISE", "stream_id": 1, "promised_stream_id": 2, "length": 30},
            {"type": "HEADERS", "stream_id": 1, "length": 120},
            {"type": "DATA", "stream_id": 1, "flags": ["END_STREAM"], "length": 4096},
            {"type": "HEADERS", "stream_id": 2, "length": 90},
            {"type": "DATA", "stream_id": 2, "flags": ["END_STREAM"], "length": 20000},
        ]
        print("Demo (illustrative sequence, not taken from the book):")
    streams, notes = analyze(frames)
    for sid, s in sorted(streams.items()):
        print(f"stream {sid}: frames={s['frames']} bytes={s['bytes']} END_STREAM={s['ended']} "
              f"RST={s['reset']} push={s['pushed']}")
    for n in notes:
        print(" - " + n)
    print("ID parity is not checked: the book contradicts itself (HPBN p.247 x p.249).")


if __name__ == "__main__":
    main()

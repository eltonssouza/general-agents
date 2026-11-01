# -*- coding: utf-8 -*-
"""
Skill: critical-rendering-path-advisor
Triage of a page's resources according to what *High Performance Browser Networking*
(Grigorik, 2013) says about the DOM, CSSOM and JavaScript, browser hints and caching.
Standard library only, no network, read-only.

The book does NOT use the term "critical rendering path" nor the defer/async attributes, preload,
preconnect or immutable. Book rules (PDF pages):
  CSS blocks rendering and script execution; synchronous JS blocks the DOM;
  "styles at the top, scripts at the bottom" ...................................... HPBN p.186
  hints dns-prefetch, subresource, prefetch, prerender (2013 support) ... HPBN p.202, p.203
  cache: explicit lifetime (Cache-Control) + validation (Last-Modified/ETag) HPBN p.254
  Gzip on text assets (60–80%) ........................................ HPBN p.255
  resources scheduled by JS are hidden from the preload scanner ........... HPBN p.258
Anything beyond this comes out as [extrapolation].

JSON input: [{"type": "css|js|font|image|hint", "url": "...", "location": "head|body",
               "sync": true, "cache_control": "...", "validator": "etag|last-modified|",
               "gzip": true, "injected_by_js": false, "rel": "dns-prefetch"}]
Usage:
  python -I critical_path_advisor.py --demo
  python -I critical_path_advisor.py --file recursos.json
"""

import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def audit(resources):
    out = []
    css_after_js = False
    seen_sync_js_head = False
    for r in resources:
        t = r.get("type", "").lower()
        url = r.get("url", "?")
        loc = r.get("location", "head").lower()
        if t == "js" and loc == "head" and r.get("sync", True):
            seen_sync_js_head = True
            out.append(("HIGH", url, "Synchronous script in <head> blocks DOM construction and waits for the CSSOM; "
                        "the book sums it up: styles at the top, scripts at the bottom [from source] (HPBN p.186). "
                        "[extrapolation] The defer/async attributes do not appear in the book."))
        if t == "css" and seen_sync_js_head:
            css_after_js = True
        if t == "css" and loc == "body":
            out.append(("MEDIUM", url, "Late CSS: stylesheets block rendering and script execution; "
                        "deliver the CSS as early as possible [from source] (HPBN p.186)."))
        if t in ("css", "js", "font", "image"):
            cc = r.get("cache_control", "").lower()
            val = r.get("validator", "")
            if "max-age" not in cc or not val:
                missing = " and ".join(x for x, ok in (("lifetime (Cache-Control max-age)", "max-age" in cc),
                                                    ("validation (ETag or Last-Modified)", bool(val))) if not ok)
                out.append(("MEDIUM", url, f"Missing {missing}: the book asks for both together to avoid redundant "
                            "transfers or revalidation on every use [from source] (HPBN p.254)."))
        if t in ("css", "js") and r.get("gzip") is False:
            out.append(("MEDIUM", url, "Text asset without Gzip; the book cites an average reduction of 60–80% "
                        "[from source] (HPBN p.255)."))
        if r.get("injected_by_js"):
            out.append(("INFO", url, "A resource scheduled by JS is invisible to the preload scanner "
                        "[from source] (HPBN p.258)."))
    if css_after_js:
        out.append(("HIGH", "(order)", "CSS declared after a synchronous script: reverse the order [from source] (HPBN p.186)."))
    hosts = {r.get("host") for r in resources if r.get("host")}
    if len(hosts) > 1 and not any(r.get("type") == "hint" and r.get("rel") == "dns-prefetch" for r in resources):
        out.append(("INFO", "(hints)", "Several hosts without dns-prefetch; the book lists dns-prefetch, subresource, "
                    "prefetch and prerender as speculative hints [from source] (HPBN p.202). [DATED] 2013 support "
                    "table (HPBN p.203)."))
    return out


def main():
    ap = argparse.ArgumentParser(description="Triage of blocking resources and caching (HPBN, 2013)")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--file")
    args = ap.parse_args()
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            res = json.load(fh)
    else:
        res = [
            {"type": "js", "url": "/app.js", "location": "head", "sync": True, "cache_control": "max-age=3600",
             "validator": "etag", "gzip": True, "host": "www.example.com"},
            {"type": "css", "url": "/style.css", "location": "head", "cache_control": "", "validator": "",
             "gzip": False, "host": "static.example.com"},
            {"type": "image", "url": "/hero.jpg", "cache_control": "max-age=86400", "validator": "",
             "injected_by_js": True, "host": "img.example.com"},
        ]
        print("Demo (illustrative page):")
    findings = audit(res)
    for sev, url, msg in findings:
        print(f"[{sev}] {url}: {msg}")
    if not findings:
        print("No known pattern found. This is NOT approval.")


if __name__ == "__main__":
    main()

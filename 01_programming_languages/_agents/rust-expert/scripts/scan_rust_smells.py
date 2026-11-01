#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic scan for attention points in Rust code.

Usage:
    python -I scan_rust_smells.py [--profile review|unsafe|all] [--json] [--rules] PATH [PATH ...]

PATH can be a .rs file or a directory (recursive search; skips target/, .git/).
Only reads files; no network access and nothing is written. Output as text (default) or JSON.

It is regex triage: it points to WHERE to look, it does not prove a defect. False positives
are expected (the script does not understand the AST). Limitation: the "in test" heuristic treats everything after #[cfg(test)] in the same file as test code. Each finding carries the rule, the reason, and the ORIGIN (label + page of the sources).
Exit code: 0 whenever the scan ran; 2 for a usage error.
"""
import argparse
import json
import os
import re
import sys

SKIP_DIRS = {"target", ".git", "node_modules"}

NUM = r"(?:u8|u16|u32|u64|u128|usize|i8|i16|i32|i64|i128|isize|f32|f64)"

# (id, profile, severity, regex, message)
RULES = [
    ("unwrap", "review", "medium", re.compile(r"\.unwrap\(\)"),
     "unwrap(): classify it (test/prototype, known invariant, expected failure, contract violation)"),
    ("expect", "review", "low", re.compile(r"\.expect\("),
     "expect(): fine only if the message explains the invariant; an expected failure should become a Result"),
    ("panic-macros", "review", "medium", re.compile(r"\b(panic|todo|unimplemented)!\("),
     "panic!/todo!/unimplemented!: confirm it is a documented contract violation"),
    ("lock-unwrap", "review", "medium", re.compile(r"\.lock\(\)\.unwrap\(\)"),
     "lock().unwrap(): decide what to do with a poisoned mutex; review the lock order"),
    ("as-cast", "review", "low", re.compile(r"\bas\s+" + NUM + r"\b"),
     "cast with 'as': may truncate/saturate; prefer From/TryFrom when the value might not fit"),
    ("ref-string", "review", "low", re.compile(r"fn\s+\w+[^{;]*:\s*&String\b"),
     "&String parameter: prefer &str"),
    ("ref-vec", "review", "low", re.compile(r"fn\s+\w+[^{;]*:\s*&Vec<"),
     "&Vec<T> parameter: prefer &[T]"),
    ("index-loop", "review", "low", re.compile(r"for\s+\w+\s+in\s+0\.\.\w+(?:\.\w+)*\.len\(\)"),
     "index loop: prefer iterating directly (for x in &v) or enumerate()"),
    ("rc-refcell", "review", "low", re.compile(r"Rc<RefCell<"),
     "Rc<RefCell<..>>: confirm there is a need for shared mutation and consider the cycle risk (use Weak)"),
    ("spawn-no-move", "review", "low", re.compile(r"thread::spawn\(\s*\|\|"),
     "thread::spawn without 'move': the closure probably borrows local data (E0373)"),
    ("allow-lint", "review", "low", re.compile(r"#!?\[allow\("),
     "allow(...): prefer expect(...) with a reason, or remove the warning"),
    ("clone", "review", "info", re.compile(r"\.clone\(\)"),
     "clone(): confirm that both copies are needed (explicit cost)"),
    ("transmute", "unsafe", "high", re.compile(r"\btransmute\b"),
     "transmute: requires proven sizes/validity/layout; prefer a safe alternative"),
    ("static-mut", "unsafe", "high", re.compile(r"\bstatic\s+mut\b"),
     "static mut: access is unsafe and prone to data races; the Book (edition 2024) bars references to static mut via a lint (static_mut_refs): use &raw const/&raw mut"),
    ("extern-no-unsafe", "unsafe", "medium", re.compile(r'^\s*extern\s+"[^"]+"\s*\{'),
     "extern block without 'unsafe': in edition 2024 it must be 'unsafe extern'"),
    ("attr-no-unsafe", "unsafe", "medium",
     re.compile(r"#\[(no_mangle|export_name|link_section)\b"),
     "symbol attribute without unsafe(...): in edition 2024 use #[unsafe(no_mangle)] etc."),
    ("raw-pointer-cast", "unsafe", "medium", re.compile(r"\bas\s+\*(?:const|mut)\b|&raw\s+(?:const|mut)\b"),
     "raw pointer creation: check nullness, alignment, validity, and aliasing before dereferencing"),
    ("from-raw", "unsafe", "high", re.compile(r"\bfrom_raw_parts(?:_mut)?\b"),
     "from_raw_parts*: requires a valid, aligned pointer and a correct length; document it in a SAFETY comment"),
    ("unchecked-api", "unsafe", "medium", re.compile(r"\b(get_unchecked(?:_mut)?|from_utf8_unchecked|assume_init|set_len)\b"),
     "*_unchecked/assume_init/set_len API: the call asserts a precondition the compiler does not check; document it in SAFETY"),
]
# Origin of each rule: (label, source). Labels: [from source] = the cited page supports the rule;
# [inference] = follows from the pages, but they do not state it; [extrapolation] = convention external to the sources.
ORIGIN = {
    "unwrap": ("[from source]", "Book p.221, 228-230 (expect with context; unwrap/expect in prototype and test; contract)"),
    "expect": ("[from source]", "Book p.221, 229 (expect documents the invariant)"),
    "panic-macros": ("[from source]", "Book p.228-230 (panic! for contract violation); todo!/unimplemented!: Book p.334, RBE p.232"),
    "lock-unwrap": ("[from source]", "Book p.476, 678 (lock can fail if another thread panicked while holding the lock)"),
    "as-cast": ("[from source]", "RBE p.46-48 (as truncates integers and saturates float->int); preferring From/TryFrom: [inference] with RBE p.53-56"),
    "ref-string": ("[from source]", "Book p.113 (&str as a parameter accepts String, &String, and slices)"),
    "ref-vec": ("[extrapolation]", "analogy with Book p.113 and p.114 (slices as parameters); the &Vec<T> -> &[T] rule is not stated in the sources"),
    "index-loop": ("[from source]", "Book p.79-80 (for over the collection is safer than while with an index)"),
    "rc-refcell": ("[from source]", "Book p.435-436, 447, 450 (RefCell only when needed; Rc cycles leak; Weak)"),
    "spawn-no-move": ("[from source]", "Book p.464-465 (the thread::spawn closure needs move: E0373)"),
    "allow-lint": ("[extrapolation]", "Ref p.207-210 describes allow/expect/forbid; preferring expect with a reason is an external convention"),
    "clone": ("[from source]", "Book p.91-94, 326 (clone is an explicit copy with a visible cost)"),
    "transmute": ("[inference]", "Ref p.625, 628-629 (invalid values and uninitialized memory are UB); the rule about transmute follows from them"),
    "static-mut": ("[from source]", "Book p.601-603 (static mut, static_mut_refs lint); Ref p.142-144"),
    "extern-no-unsafe": ("[from source]", "Ref p.160-161 (unsafe extern mandatory in edition 2024)"),
    "attr-no-unsafe": ("[from source]", "Ref p.191, 639-641 (no_mangle/export_name/link_section require unsafe(...) in 2024)"),
    "raw-pointer-cast": ("[from source]", "Book p.593-595 (raw pointers, &raw const/mut); Ref p.626-627 (alignment and dangling)"),
    "from-raw": ("[from source]", "Book p.597-599 (split_at_mut with from_raw_parts_mut); Ref p.627"),
    "unchecked-api": ("[extrapolation]", "get_unchecked only appears as an example in Ref p.621; from_utf8_unchecked, assume_init, and set_len are not covered in the sources"),
    "unsafe-op-in-unsafe-fn": ("[from source]", "Ref p.621-622 and Book p.596, 602 differ in emphasis; edition in which the lint warns by default: [NOT VERIFIED IN THE PDF]"),
    "missing-safety-comment": ("[from source]", "Book p.592-593, 602 (SAFETY comment; minimal unsafe block); Ref p.620-623"),
}

UNSAFE_BLOCK = re.compile(r"\bunsafe\s*\{|\bunsafe\s+impl\b|\bunsafe\s+trait\b")
UNSAFE_FN = re.compile(r"\bunsafe\s+(?:extern\s+\"[^\"]*\"\s+)?fn\b")
SAFETY_COMMENT = re.compile(r"//+\s*SAFETY\s*:|/\*+\s*SAFETY\s*:", re.I)
SAFETY_DOC = re.compile(r"///\s*#\s*Safety|//!\s*#\s*Safety", re.I)
TEST_MOD = re.compile(r"#\[cfg\(test\)\]")


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(".rs"):
                yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in sorted(files):
                    if f.endswith(".rs"):
                        yield os.path.join(root, f)
        else:
            print(f"warning: path does not exist: {p}", file=sys.stderr)


def strip_comment(line):
    """Strip a simple line comment (heuristic; ignores // inside a string)."""
    in_str = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"' and (i == 0 or line[i - 1] != "\\"):
            in_str = not in_str
        elif not in_str and line.startswith("//", i):
            return line[:i]
        i += 1
    return line


UNSAFE_OPS = re.compile(
    r"(?:^|[=(,{;\s&!])\*(?!const\b|mut\b)[a-z_]\w*"            # dereference *p
    r"|\b(?:get_unchecked(?:_mut)?|from_raw_parts(?:_mut)?|transmute"
    r"|read_volatile|write_volatile|ptr::read|ptr::write|assume_init)\b")
UNSAFE_OPEN = re.compile(r"\bunsafe\s*\{")


def bare_unsafe_ops(codes):
    """Indices of lines with a typical unsafe operation inside an `unsafe fn`
    but outside an explicit `unsafe {}` block (unsafe_op_in_unsafe_fn lint).
    Brace-counting heuristic; does not understand strings or macros."""
    flagged = set()
    depth = 0
    fn_depth = None   # depth at which the `unsafe fn` was declared
    inner = []        # depths (before opening) of `unsafe {` blocks inside the fn
    for idx, code in enumerate(codes):
        starts_fn = bool(UNSAFE_FN.search(code)) and fn_depth is None
        if starts_fn:
            fn_depth = depth
        if fn_depth is not None:
            if starts_fn:
                body = code.split("{", 1)[1] if "{" in code else ""
            else:
                body = code
            if body and not inner and not UNSAFE_OPEN.search(body) and UNSAFE_OPS.search(body):
                flagged.add(idx)
            if UNSAFE_OPEN.search(code):
                inner.append(depth)
        depth += code.count("{") - code.count("}")
        while inner and depth <= inner[-1]:
            inner.pop()
        if fn_depth is not None and depth <= fn_depth and "{" in "".join(codes[max(0, idx - 0): idx + 1]) and ("}" in code):
            fn_depth = None
            inner.clear()
    return flagged


def scan_file(path, profile):
    findings = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
        return findings

    codes = [strip_comment(l) for l in lines]
    bare_ops = bare_unsafe_ops(codes) if profile in ("unsafe", "all") else set()
    in_test_from = None  # index of the line where #[cfg(test)] starts
    for idx, raw in enumerate(lines):
        if TEST_MOD.search(raw) and in_test_from is None:
            in_test_from = idx
        code = strip_comment(raw)
        in_test = in_test_from is not None and idx >= in_test_from
        is_test_file = "/tests/" in path.replace("\\", "/") or path.endswith("_test.rs")

        for rid, prof, sev, rx, msg in RULES:
            if profile != "all" and prof != profile:
                continue
            if rx.search(code):
                ctx = "test" if (in_test or is_test_file) else "production"
                if ctx == "test" and rid in {"unwrap", "expect", "panic-macros", "clone", "as-cast"}:
                    continue  # expected noise in tests
                findings.append(dict(file=path, line=idx + 1, rule=rid, severity=sev,
                                     context=ctx, message=msg, origin="%s %s" % ORIGIN[rid], text=raw.strip()[:140]))

        if idx in bare_ops:
            findings.append(dict(
                file=path, line=idx + 1, rule="unsafe-op-in-unsafe-fn", severity="medium",
                context="test" if in_test else "production",
                origin="%s %s" % ORIGIN["unsafe-op-in-unsafe-fn"],
                message="unsafe operation inside `unsafe fn` without an explicit `unsafe {}` block "
                        "(unsafe_op_in_unsafe_fn lint); write the block and the SAFETY comment",
                text=raw.strip()[:140]))

        if profile in ("unsafe", "all"):
            is_block = UNSAFE_BLOCK.search(code)
            is_fn = UNSAFE_FN.search(code) and not code.strip().startswith("//")
            if is_block or is_fn:
                window = lines[max(0, idx - 4): idx + 1]
                has = any(SAFETY_COMMENT.search(w) for w in window)
                if is_fn and not has:
                    has = any(SAFETY_DOC.search(w) for w in lines[max(0, idx - 12): idx + 1])
                if not has:
                    kind = "unsafe fn" if is_fn and not is_block else "unsafe block/impl"
                    findings.append(dict(
                        file=path, line=idx + 1, rule="missing-safety-comment", severity="high",
                        context="test" if in_test else "production",
                        origin="%s %s" % ORIGIN["missing-safety-comment"],
                        message=f"{kind} without a '// SAFETY:' comment (or a '# Safety' doc section) in the preceding lines",
                        text=raw.strip()[:140]))
    return findings


def main(argv):
    try:  # the Windows console defaults to cp1252; force UTF-8 for accented characters
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--rules", action="store_true", help="list the rules with origin and page, and exit")
    ap.add_argument("--profile", choices=["review", "unsafe", "all"], default="review")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args(argv)
    if args.rules:
        for rid, prof, sev, rx, msg in RULES:
            print(f"{rid} [{prof}/{sev}] origin: {ORIGIN[rid][0]} {ORIGIN[rid][1]}")
        for rid in ("unsafe-op-in-unsafe-fn", "missing-safety-comment"):
            print(f"{rid} [unsafe/high-medium] origin: {ORIGIN[rid][0]} {ORIGIN[rid][1]}")
        return 0
    if not args.paths:
        ap.error("provide at least one PATH (or use --rules)")

    all_f = []
    nfiles = 0
    for f in iter_files(args.paths):
        nfiles += 1
        all_f.extend(scan_file(f, args.profile))

    order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    all_f.sort(key=lambda d: (order[d["severity"]], d["file"], d["line"]))

    if args.json:
        json.dump(dict(files_scanned=nfiles, findings=all_f), sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    print(f"# Rust scan — profile={args.profile} — {nfiles} .rs file(s) — {len(all_f)} finding(s)")
    print("# Regex triage: it indicates where to look; confirm each item by reading the code.\n")
    counts = {}
    for d in all_f:
        counts[d["rule"]] = counts.get(d["rule"], 0) + 1
        if d["severity"] == "info":
            continue
        print(f"[{d['severity']}] {d['file']}:{d['line']} ({d['context']}) {d['rule']}: {d['message']}")
        print(f"      {d['text']}")
        print(f"      origin: {d['origin']}")
    print("\n## Count per rule")
    for r, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"- {r}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

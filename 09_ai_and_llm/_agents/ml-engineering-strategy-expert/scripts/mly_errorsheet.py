# -*- coding: utf-8 -*-
"""
mly_errorsheet.py - error analysis spreadsheet from the MLY (Machine Learning Yearning, Ng, 2018 DRAFT).
Stdlib, no network, deterministic. Run with: python -I scripts/mly_errorsheet.py SUBCOMMAND ...
Pages = PDF page (= printed number).

Book procedure (p.30-33): take ~100 dev examples the system got wrong, tag them by hand into
categories (one example can have several), compute the % of each category. A category's % is the CEILING
on how much of the errors the project that fixes it can eliminate (p.30-31). The book warns that this is NOT a rigid
priority formula: also consider the expected progress and the effort (p.33).

Subcommands
  template  --cats "Dog,Big cat,Blurry" [--rows 100]   prints an empty CSV (columns: id, categories, comment)
  analyze   FILE.csv [--error-rate E] [--json]         counts categories, % and ceiling; E = overall dev error in %
  mislabeled --error E (--mislabeled-pct P | --mislabeled-error M)   mislabeled-data decomposition (p.34-35)
  attribute FILE.json --order A,B,C [--json]           error attribution by parts (p.109-112)
     FILE.json = list of {"id": ..., "fixed_by": ["A", ...]}: components whose "perfect" output (alone) fixes the
     final result of that error. Book rule (p.111): attribute to the first component in DAG order whose
     perfect output fixes the result; if none does, attribute to the last one.
CSV: 1st column = id; columns whose name starts with 'coment' / 'comment' / 'nota' / 'note' are ignored in the count;
the rest are categories. Truthy marks: 1, x, X, v, y, s, sim, yes, true, ✔, ✓ ("s"/"sim" are Portuguese yes).
"""
import argparse
import csv
import io
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

TRUE = {"1", "x", "v", "y", "s", "sim", "yes", "true", "✔", "✓", "✔️"}
IGN = ("coment", "comment", "nota", "note")


def read_csv(path):
    raw = open(path, "r", encoding="utf-8-sig", newline="").read()
    first = raw.splitlines()[0] if raw.strip() else ""
    delim = ";" if first.count(";") > first.count(",") else ","
    rows = list(csv.reader(io.StringIO(raw), delimiter=delim))
    rows = [r for r in rows if any(c.strip() for c in r)]
    if len(rows) < 2:
        raise SystemExit("The CSV needs a header and at least 1 row.")
    head = [h.strip() for h in rows[0]]
    cats = [(i, h) for i, h in enumerate(head) if i > 0 and not h.lower().startswith(IGN) and h]
    data = []
    for r in rows[1:]:
        r = r + [""] * (len(head) - len(r))
        data.append({h: (r[i].strip().lower() in TRUE) for i, h in cats})
    return [h for _, h in cats], data


def cmd_template(a):
    cats = [c.strip() for c in a.cats.split(",") if c.strip()]
    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(["id"] + cats + ["comment"])
    for i in range(1, a.rows + 1):
        w.writerow([i] + [""] * len(cats) + [""])
    return 0


def cmd_analyze(a):
    cats, data = read_csv(a.file)
    n = len(data)
    out = []
    for c in cats:
        k = sum(1 for d in data if d[c])
        frac = k / n
        row = {"category": c, "count": k, "pct": 100.0 * frac}
        if a.error_rate is not None:
            row["remaining_error_if_eliminated_%"] = a.error_rate * (1 - frac)
            row["max_relative_reduction_%"] = 100.0 * frac
        out.append(row)
    out.sort(key=lambda r: (-r["count"], r["category"]))
    none_cat = sum(1 for d in data if not any(d.values()))
    res = {"n_errors_examined": n, "categories": out, "uncategorized": none_cat,
           "sum_pct": sum(r["pct"] for r in out)}
    warn = []
    if n < 20:
        warn.append("p.38: with ~10 errors the Eyeball set is considered far too small; ~20 gives a rough feel; ~50 good; ~100 very good.")
    elif n < 50:
        warn.append("p.38: with ~20 errors you only get a rough idea of the main sources; ~50 gives a good idea, ~100 a very good one.")
    if none_cat:
        warn.append(f"{none_cat} error(s) without a category: consider creating new categories (p.32-33: the process is iterative).")
    res["warnings"] = warn
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print(f"{n} errors examined (MLY p.30, 32-33). Percentages may sum to more than 100% (an example can be in several categories; p.32).")
    for r in out:
        s = f"  {r['category']:<24} {r['count']:>4}  {r['pct']:5.1f}%  = CEILING of errors that can be eliminated [from source p.30-31]"
        if a.error_rate is not None:
            s += f"; overall error {a.error_rate:g}% -> best case {r['remaining_error_if_eliminated_%']:.2f}%"
        print(s)
    for w in warn:
        print("WARNING:", w)
    print("Reminder [from source p.33]: not a rigid formula; also weigh the expected progress and the effort of each category.")
    return 0


def cmd_mis(a):
    if (a.mislabeled_pct is None) == (a.mislabeled_error is None):
        print("Pass --mislabeled-pct OR --mislabeled-error.")
        return 2
    if a.mislabeled_pct is not None:
        m = a.error * a.mislabeled_pct / 100.0
        pct = a.mislabeled_pct
    else:
        m = a.mislabeled_error
        pct = 100.0 * m / a.error
    others = a.error - m
    print(f"Overall dev error: {a.error:g}%")
    print(f"  due to mislabeled data : {m:.3g}% ({pct:.3g}% of the errors)   [from source p.34-35]")
    print(f"  due to other causes    : {others:.3g}% ({100 - pct:.3g}% of the errors)")
    print(f"  [inference] The 'true' error lies between {others:.3g}% and {a.error:g}% (p.34-35: 'knowing whether it is 10% or 9.4%' vs 'closer to 1.4% or 2%').")
    print("Book criterion: worth fixing when the fraction of mislabeled data hampers your ability to judge algorithms (p.34). "
          "The book gives NO numeric threshold; the examples are 6% (not crucial) and 30% (worth it) (p.34-35).")
    print("If you fix dev, fix test too, and consider checking the examples the algorithm got right, not only the wrong ones (p.35).")
    return 0


def cmd_attr(a):
    order = [c.strip() for c in a.order.split(",") if c.strip()]
    if len(order) < 2:
        print("--order needs >=2 components in DAG order (p.112).")
        return 2
    data = json.load(open(a.file, "r", encoding="utf-8"))
    cnt = {c: 0 for c in order}
    detail = []
    for e in data:
        fb = set(e.get("fixed_by", []))
        unk = fb - set(order)
        if unk:
            raise SystemExit(f"component(s) not in --order: {sorted(unk)}")
        who = None
        for c in order[:-1]:
            if c in fb:
                who = c
                break
        if who is None:
            who = order[-1]
        cnt[who] += 1
        detail.append({"id": e.get("id"), "assigned_to": who})
    n = len(data)
    res = {"n_errors": n, "order": order,
           "attribution": {c: {"count": cnt[c], "pct": 100.0 * cnt[c] / n if n else 0.0} for c in order},
           "detail": detail}
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print(f"{n} errors; DAG order: {' -> '.join(order)} (MLY p.111-112)")
    for c in order:
        print(f"  {c:<24} {cnt[c]:>4}  {100.0 * cnt[c] / n if n else 0:5.1f}%")
    if n:
        top = max(order, key=lambda c: cnt[c])
        print(f"Suggested focus: {top} [from source p.107, 110: concentrate on the component that accounts for most of the errors].")
    print("The book notes that swapping the order of A and B may give slightly different but still valid results, as long as it respects the DAG (p.112).")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    t = sp.add_parser("template")
    t.add_argument("--cats", required=True)
    t.add_argument("--rows", type=int, default=100)
    z = sp.add_parser("analyze")
    z.add_argument("file")
    z.add_argument("--error-rate", type=float)
    z.add_argument("--json", action="store_true")
    m = sp.add_parser("mislabeled")
    m.add_argument("--error", type=float, required=True)
    m.add_argument("--mislabeled-pct", type=float)
    m.add_argument("--mislabeled-error", type=float)
    r = sp.add_parser("attribute")
    r.add_argument("file")
    r.add_argument("--order", required=True)
    r.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sys.exit({"template": cmd_template, "analyze": cmd_analyze, "mislabeled": cmd_mis, "attribute": cmd_attr}[a.cmd](a))


if __name__ == "__main__":
    main()

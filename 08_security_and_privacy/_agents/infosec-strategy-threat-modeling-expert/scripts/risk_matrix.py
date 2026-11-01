# -*- coding: utf-8 -*-
"""
risk_matrix.py - computes and ranks risks with the formula and the EXAMPLE scales of the DZ
(Infosec Strategies and Best Practices, MacMillan, Packt 2021): Risk = Impact x Likelihood (DZ p.23),
impact 1-5 and likelihood 1-5 (DZ p.28-29), 5x5 matrix with score 1-25 (DZ p.31-33), example acceptance line = 7 (DZ p.33).

Usage (Python 3, stdlib, no network, read-only; run with `python -I`):
  python -I scripts/risk_matrix.py scales
  python -I scripts/risk_matrix.py matrix [--appetite 7]
  python -I scripts/risk_matrix.py sample
  python -I scripts/risk_matrix.py rank FILE.csv [--appetite 7]
CSV (UTF-8, header required): id,asset,threat,impact,likelihood[,treatment][,residual_impact,residual_likelihood]
  Portuguese headers are also accepted: id,ativo,ameaca,impacto,probabilidade[,tratamento][,residual_impacto,residual_probabilidade]
  - impact and likelihood: integers 1-5 (DZ example scale; adapt to your organization's scales);
  - treatment (optional): avoid|reduce|transfer|accept (DZ p.33); Portuguese evitar|reduzir|transferir|aceitar also accepted;
  - residual_* (optional): impact/likelihood after the control (residual risk, DZ p.34).
Limits: the DZ scales are didactic examples (DZ p.28-29, 31); the appetite (7) is from the example (DZ p.33), not a standard.
Exit code: 0 ok; 2 invalid input.
"""
import argparse
import csv
import io
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

IMPACT = [
    (5, "Catastrophic", "the organization loses 5% or more of annual revenue per occurrence"),
    (4, "High", "loses 3-5% of annual revenue per occurrence"),
    (3, "Medium", "loses 1-3% of annual revenue per occurrence"),
    (2, "Low", "loses 0-1% of annual revenue per occurrence"),
    (1, "Negligible", "loses up to US$ 300 per occurrence"),
]
LIKELIHOOD = [
    (5, "Certain", "once a year or more"),
    (4, "Likely", "once every 2-3 years"),
    (3, "Possible", "once every 4-7 years"),
    (2, "Unlikely", "once every 7-9 years"),
    (1, "Improbable", "once every 10 years or more"),
]
TREAT = {"avoid", "reduce", "transfer", "accept"}
# Portuguese treatment words (kept as accepted input) -> canonical English
TREAT_ALIASES = {"evitar": "avoid", "reduzir": "reduce", "transferir": "transfer", "aceitar": "accept"}
# CSV header aliases (Portuguese -> canonical English)
HEADER_ALIASES = {"ativo": "asset", "ameaca": "threat", "ameaça": "threat", "impacto": "impact",
                  "probabilidade": "likelihood", "tratamento": "treatment",
                  "residual_impacto": "residual_impact", "residual_probabilidade": "residual_likelihood",
                  "probability": "likelihood", "residual_probability": "residual_likelihood"}


def cmd_scales():
    print("# EXAMPLE scales from the DZ (DZ p.28-29; the organization must define its own with the stakeholders)")
    print("Impact (DZ p.28 text; table in a figure on DZ p.29, read visually):")
    for s, n, d in IMPACT:
        print("  %d %-28s %s" % (s, n, d))
    print("Likelihood (DZ p.29 text defines 5 and 1; table in a figure on DZ p.29, read visually):")
    for s, n, d in LIKELIHOOD:
        print("  %d %-30s %s" % (s, n, d))
    print("Risk = Impact x Likelihood (DZ p.23): score 1 to 25 (DZ p.32). Treatment: avoid, reduce, transfer, accept (DZ p.33).")


def cmd_matrix(app):
    print("# 5x5 matrix (rows: likelihood; columns: impact). '*' = above the appetite (%d), DZ p.33 example" % app)
    print("lik\\imp " + " ".join("%4d" % i for i in range(1, 6)))
    for p in range(5, 0, -1):
        cells = []
        for i in range(1, 6):
            v = p * i
            cells.append("%3d%s" % (v, "*" if v > app else " "))
        print("   %d     " % p + " ".join(cells))


def cmd_sample():
    print("id,asset,threat,impact,likelihood,treatment,residual_impact,residual_likelihood")
    print("R1,Secret recipe on the NAS,Competitor accesses the NAS without login,5,5,reduce,5,1")
    print("R2,Application server,Disk failure without redundancy,3,3,reduce,3,1")
    print("R3,Office,Basement flooding,2,2,accept,,")


def _int(v, nome, ln):
    try:
        x = int(str(v).strip())
    except Exception:
        raise ValueError("line %d: invalid %s (%r); use an integer 1-5" % (ln, nome, v))
    if x < 1 or x > 5:
        raise ValueError("line %d: %s outside 1-5 (%d)" % (ln, nome, x))
    return x


def _canon_row(r):
    return {HEADER_ALIASES.get((k or "").strip().lower(), (k or "").strip().lower()): v for k, v in r.items()}


def cmd_rank(path, app):
    try:
        with io.open(path, "r", encoding="utf-8-sig", newline="") as f:
            rows = [_canon_row(r) for r in csv.DictReader(f)]
    except Exception as e:
        print("ERROR: could not read the CSV: %s" % e)
        return 2
    need = {"id", "asset", "threat", "impact", "likelihood"}
    if not rows or not need.issubset(set(rows[0].keys())):
        print("ERROR: the CSV needs a header with: %s" % ",".join(sorted(need)))
        return 2
    out = []
    try:
        for n, r in enumerate(rows, start=2):
            imp = _int(r["impact"], "impact", n)
            pro = _int(r["likelihood"], "likelihood", n)
            tr = (r.get("treatment") or "").strip().lower()
            tr = TREAT_ALIASES.get(tr, tr)
            if tr and tr not in TREAT:
                raise ValueError("line %d: invalid treatment (%r); use %s" % (n, tr, "|".join(sorted(TREAT))))
            ri = (r.get("residual_impact") or "").strip()
            rp = (r.get("residual_likelihood") or "").strip()
            res = None
            if ri or rp:
                if not (ri and rp):
                    raise ValueError("line %d: provide residual_impact AND residual_likelihood" % n)
                res = _int(ri, "residual_impact", n) * _int(rp, "residual_likelihood", n)
            out.append((imp * pro, imp, pro, r["id"], r["asset"], r["threat"], tr, res))
    except ValueError as e:
        print("ERROR: %s" % e)
        return 2
    out.sort(key=lambda x: (-x[0], x[3]))
    print("# Ranking (Risk = Impact x Likelihood; example appetite = %d, DZ p.33)" % app)
    print("%-6s %-5s %-4s %-4s %-30s %-34s %-11s %s" % ("id", "risk", "imp", "lik", "asset", "threat", "treatment", "residual"))
    for s, i, p, id_, at, am, tr, res in out:
        above = "ABOVE appetite" if s > app else "within appetite"
        resd = "-" if res is None else "%d (%s)" % (res, "acceptable" if res <= app else "still above")
        print("%-6s %-5d %-4d %-4d %-30s %-34s %-11s %s | %s" % (id_, s, i, p, at[:30], am[:34], tr or "-", resd, above))
    acima = [x for x in out if x[0] > app]
    print("\n%d of %d risks above the appetite. Risks above the appetite require treatment (DZ p.33); residual below the appetite = acceptable (DZ p.34)." % (len(acima), len(out)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Risk matrix (DZ example scales)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("scales")
    m = sub.add_parser("matrix")
    m.add_argument("--appetite", type=int, default=7)
    sub.add_parser("sample")
    r = sub.add_parser("rank")
    r.add_argument("file")
    r.add_argument("--appetite", type=int, default=7)
    a = ap.parse_args()
    if a.cmd == "scales":
        cmd_scales()
    elif a.cmd == "matrix":
        cmd_matrix(a.appetite)
    elif a.cmd == "sample":
        cmd_sample()
    elif a.cmd == "rank":
        return cmd_rank(a.file, a.appetite)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

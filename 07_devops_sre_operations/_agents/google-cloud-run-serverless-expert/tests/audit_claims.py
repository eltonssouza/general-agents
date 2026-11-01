# -*- coding: utf-8 -*-
"""
audit_claims.py - ADVISORY (heuristic) audit of numbers and code cited in the package files.

For each line of references/ with `(RUN p.N...)`, extracts code tokens (between backticks, without
UPPERCASE placeholders) and numbers with units and checks whether they appear in the cited pages
(union of the pages cited on the line, PDF page). Lists what was NOT found for human review.
Expected false positives (paraphrase, "US$ 9" vs "$9", "1.000" vs "1000", [extrapolation]).
Usage: python -I tests/audit_claims.py --src PATH/scratch/devops [--pkg PACKAGE] [--strict]
Always exit 0 (advisory), except --strict (exit 1 if there are pending items not justified in audit-ignore.txt).
"""
import argparse
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FILE = "Serverless-Google-Cloud-Run.txt"


def squash(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[\s\-‐-―]+", "", s.lower())


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = set()
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.update(range(a, b + 1))
    return pages


CITE = re.compile(r"\bRUN\s+p\.\s*(\d[\d\s,\-–]*)")
CODE = re.compile(r"`([^`]+)`")
NUM = re.compile(r"(?<![\w.])(\d[\d.,]*)\s*(GB|GiB|MB|ms|min(?:utes?|utos?)?|s\b|%|h\b|hours?|horas?|thousand|mil\b|vCPU|IPs|instances|instâncias|instancias)?", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    pages = load_pages(os.path.join(a.src, FILE))
    ignore = set()
    ip = os.path.join(a.pkg, "tests", "audit-ignore.txt")
    if os.path.exists(ip):
        ignore = {l.strip() for l in open(ip, encoding="utf-8") if l.strip() and not l.startswith("#")}
    pend, total_lines, total_tok = [], 0, 0
    for root, _, files in os.walk(os.path.join(a.pkg, "references")):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            for ln, line in enumerate(open(fp, encoding="utf-8").read().splitlines(), 1):
                cites = CITE.findall(line)
                if not cites or "[extrapol" in line.split("(RUN")[0][:40]:
                    pass
                if not cites:
                    continue
                pgs = set()
                for c in cites:
                    pgs |= expand(c)
                body = squash(" ".join(pages.get(p, "") for p in sorted(pgs)))
                total_lines += 1
                text = CITE.sub("", line)
                toks = []
                for m in CODE.findall(text):
                    if re.search(r"[A-Z]{3,}", m) and not re.search(r"[a-z]", m.replace("NOME", "").replace("NAME", "")):
                        continue
                    if any(ph in m for ph in ("NOME", "NAME", "IMG", "REV", "PROJ", "SA@", "REGIAO", "REGION", "ARQ", "FILE", "...", "INST", "PROJETO", "PROJECT", "SERVICO", "SERVICE", "IMAGEM", "IMAGE", "SA ", "K=V", "REPO")):
                        continue
                    toks.append(("code", m))
                for m in NUM.finditer(text):
                    n = m.group(1).rstrip(".,")
                    if m.group(2) is None or len(n) == 0:
                        continue
                    if n in ("2020", "2021", "2019", "28"):
                        continue
                    toks.append(("num", (n + (m.group(2) or "")).replace(".", "").replace(",", "")))
                for kind, tok in toks:
                    total_tok += 1
                    t = squash(tok.replace(".", "") if kind == "num" else tok)
                    # code: tests the whole token and then each long keyword
                    ok = t in body or t.replace(".", "") in body
                    if not ok and kind == "code":
                        parts = [squash(x) for x in re.split(r"\s+", tok) if len(x) > 3]
                        ok = bool(parts) and all(x in body for x in parts)
                    if not ok:
                        key = f"{os.path.relpath(fp, a.pkg)}:{ln}:{tok}"
                        if key not in ignore:
                            pend.append((key, sorted(pgs)))
    for key, pgs in pend:
        print(f"REVIEW {key}  (cited pages {pgs[0]}-{pgs[-1]})")
    print(f"Advisory audit: {total_lines} cited lines, {total_tok} tokens (code/numbers) checked; {len(pend)} not found in the cited pages.")
    return 1 if (a.strict and pend) else 0


if __name__ == "__main__":
    sys.exit(main())

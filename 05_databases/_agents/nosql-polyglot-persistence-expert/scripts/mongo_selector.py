# -*- coding: utf-8 -*-
"""
mongo_selector.py - embed vs reference decision guide (MongoDB), with the origin of EACH rule.

Sole source of the rules: MONGO-PAT (Copeland, 2013), ch. 1, p.17-29 (p.N = PDF page; printed = PDF-14),
and the hybrid comments design, p.131-133. The book is from 2013 [DATED]: there were no multi-document
transactions (MONGO-MAN-H p.3 says they exist today). The book has NO numeric cardinality thresholds (e.g. 100 items);
the only number is "about 100 comments per bucket" in the comments example (p.131).
This is a decision aid [inference] about what the book weighs, not a rule of the book.

Usage:
  python -I mongo_selector.py --cardinality 1:many --unbounded-growth --paginated-access
  python -I mongo_selector.py --cardinality 1:few --queried-together --atomic-needed
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def evaluate(card, unbounded, together, atomic, by_child, paginated):
    """Returns a list of (rule, recommendation, page)."""
    out = []
    if unbounded or card == "1:many":
        if paginated:
            out.append(("High or unpredictable arity with paginated access",
                        "HYBRID: 'buckets' of about 100 items per document (comments example)", "MONGO-PAT p.131-133"))
        out.append(("High/unbounded arity: a large document uses more RAM, grows and is copied, and there is the 16 MB cap",
                    "REFERENCE (one collection for the children)", "MONGO-PAT p.26-27"))
    if by_child:
        out.append(("The children must be queried in several ways (sort, limit, search by author)",
                    "REFERENCE (normalized collection is more flexible)", "MONGO-PAT p.25-26"))
    if card == "N:M":
        out.append(("Many-to-many: a join table requires application-level 'joins'; embedding everything requires updating in several places",
                    "EMBED A LIST OF _id (middle ground)", "MONGO-PAT p.27-28"))
    if atomic and not (unbounded or card == "1:many"):
        out.append(("Atomicity and isolation: updating a single document is atomic; no multi-document transaction in 2013",
                    "EMBED", "MONGO-PAT p.23-24"))
    if card in ("1:1", "1:few") and together and not by_child:
        out.append(("Data read together: locality (one seek) and one trip to the database instead of two",
                    "EMBED", "MONGO-PAT p.23"))
    return out


def main():
    ap = argparse.ArgumentParser(description="Embed vs reference (MONGO-PAT ch. 1)")
    ap.add_argument("--cardinality", choices=["1:1", "1:few", "1:many", "N:M"], required=True)
    ap.add_argument("--unbounded-growth", action="store_true", help="number of children is high, unpredictable or uncapped")
    ap.add_argument("--queried-together", action="store_true", help="parent and children are almost always read together")
    ap.add_argument("--atomic-needed", action="store_true", help="parent and children must be updated atomically")
    ap.add_argument("--query-by-child", action="store_true", help="children are queried in isolation in varied ways")
    ap.add_argument("--paginated-access", action="store_true", help="children are displayed in pages")
    a = ap.parse_args()

    res = evaluate(a.cardinality, a.unbounded_growth, a.queried_together, a.atomic_needed, a.query_by_child, a.paginated_access)
    print("=" * 70)
    print("Embed vs reference - MONGO-PAT ch. 1 (p.N = PDF page) [inference]")
    print("=" * 70)
    if not res:
        print("No rule of the book clearly applies: the book says it 'depends' on the access patterns and that there are")
        print("few fixed rules (MONGO-PAT p.22, 28-29). Describe the access pattern.")
    for rule, rec, page in res:
        print("- Rule: %s\n  => %s [%s]" % (rule, rec, page))
    print()
    conflicts = {r for _, r, _ in res if r.startswith("EMBED")} and {r for _, r, _ in res if r.startswith("REFERENCE")}
    if conflicts:
        print("Note: some rules point in opposite directions; the book asks to decide by access patterns (MONGO-PAT p.28-29).")
    print("[DATED] The book is from 2013 and had no multi-document transactions; current versions support them (MONGO-MAN-H p.3).")
    print("The book does not define numeric cardinality thresholds; any number is the user's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

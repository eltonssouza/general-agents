# -*- coding: utf-8 -*-
"""
story_check.py - deterministically validates user stories and acceptance criteria (Portuguese or English).

Checks, per story:
  - format "As a <persona>, I want <capability>, so that <outcome>" (or the Portuguese "Como ..., quero ..., para ...");
  - complete Given/When/Then scenarios (Portuguese Dado/Quando/Então also accepted); a story without scenarios is an error;
  - vague, non-measurable terms ("fast", "intuitive", "rápido"...);
  - technical solution prescribed in the statement ("table", "endpoint", "React"...);
  - "and" ("e" in Portuguese) in the "I want" clause: possibly two stories (INVEST: small).
Reads the text as DATA (never executes it). Read-only, no network.

Usage:
  python -I story_check.py stories.md
  python -I story_check.py - < stories.md
Exit: 0 no problems, 1 problems found (errors or warnings), 2 usage/read error.
"""
import argparse
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Vague terms (Portuguese terms are matched after accent stripping; English terms added alongside).
VAGUE = ["rapido", "rapida", "rapidamente", "intuitivo", "intuitiva", "facil", "facilmente", "amigavel", "simples",
         "robusto", "robusta", "eficiente", "flexivel", "escalavel", "moderno", "moderna", "adequado", "adequada",
         "bom desempenho", "alta performance", "user-friendly", "intuitive", "fast", "quick", "quickly", "easy",
         "easily", "simple", "robust", "efficient", "flexible", "scalable", "seamless", "modern", "appropriate",
         "good performance", "high performance", "responsive", "friendly", "convenient", "smooth", "lightweight"]
# Prescribed technical solutions (Portuguese and English).
TECH = ["tabela", "coluna", "banco de dados", "sql", "endpoint", "api rest", "microsservico", "microservico",
        "react", "angular", "vue", "kafka", "redis", "json", "http", "classe", "metodo", "cache", "docker",
        "kubernetes", "lambda", "frontend", "backend", "table", "column", "database", "microservice", "class", "method",
        "rest api", "stored procedure", "queue", "schema", "dropdown", "button"]
STORY = [
    re.compile(r"\bcomo\s+(?:(?:um|uma|o|a)\s+)?(?P<who>.+?),?\s+(?:eu\s+)?quero\s+(?P<want>.+?),?\s+para\s+(?:que\s+)?(?P<why>.+?)(?:\.\s|\.$|$)", re.I),
    re.compile(r"\bas\s+an?\s+(?P<who>.+?),\s*i\s+want\s+(?:to\s+)?(?P<want>.+?),?\s+so\s+that\s+(?P<why>.+?)(?:\.\s|\.$|$)", re.I),
]
STEP = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(dado|quando|entao|e|mas|given|when|then|and|but)\b(?:\*\*)?", re.I)
SCEN = re.compile(r"^\s*(?:#+\s*)?(?:[-*]\s*)?(?:\*\*)?(cenario|scenario|exemplo|example)\b", re.I)
KIND = {"dado": "D", "given": "D", "quando": "Q", "when": "Q", "entao": "E", "then": "E"}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").replace("**", "")


def words_in(text, terms):
    t = norm(text)
    return [w for w in terms if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", t)]


def find_stories(lines):
    """Return [(start_line, who, want, why)] from single-line story statements."""
    out = []
    for i, l in enumerate(lines):
        n = norm(l)
        for rx in STORY:
            m = rx.search(n)
            if m:
                out.append((i, m.group("who").strip(), m.group("want").strip(), m.group("why").strip()))
                break
    return out


def check(text):
    lines = text.splitlines()
    stories = find_stories(lines)
    problems = []
    if not stories:
        return [], [("ERROR", 0, "no story in the format 'As a ..., I want ..., so that ...' or 'Como ..., quero ..., para ...'")]
    report = []
    for k, (start, who, want, why) in enumerate(stories):
        end = stories[k + 1][0] if k + 1 < len(stories) else len(lines)
        block = lines[start:end]
        probs = []
        stmt = lines[start]
        for w in words_in(stmt, TECH):
            probs.append(("WARNING", start + 1, "statement prescribes a technical solution ('%s'): describe the need and the outcome" % w))
        if re.search(r"\s(e|and)\s", " " + want + " "):
            probs.append(("WARNING", start + 1, "the 'want' part has 'and'/'e': possibly two stories (INVEST: small)"))
        scenarios, cur = [], None
        for j, l in enumerate(block[1:], start + 2):
            if SCEN.match(norm(l)):
                cur = {"line": j, "name": l.strip().strip("#*- ").strip(), "kinds": set()}
                scenarios.append(cur)
                continue
            m = STEP.match(norm(l))
            if m:
                if cur is None:
                    cur = {"line": j, "name": "(unnamed)", "kinds": set()}
                    scenarios.append(cur)
                kind = KIND.get(m.group(1).lower())
                if kind:
                    cur["kinds"].add(kind)
        if not scenarios:
            probs.append(("ERROR", start + 1, "story without Given/When/Then acceptance criteria"))
        for sc in scenarios:
            miss = [n for n, k in (("Given", "D"), ("When", "Q"), ("Then", "E")) if k not in sc["kinds"]]
            if miss:
                probs.append(("ERROR", sc["line"], "scenario '%s' is missing %s" % (sc["name"][:50], "/".join(miss))))
        for j, l in enumerate(block, start + 1):
            for w in words_in(l, VAGUE):
                probs.append(("WARNING", j, "vague term '%s': replace with a number or an observable behavior" % w))
        report.append((start + 1, who, want, why, len(scenarios)))
        problems += probs
    return report, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="Markdown/text file with the stories, or - for standard input")
    a = ap.parse_args(argv)
    try:
        # explicit UTF-8 stdin: on Windows, with -I, the default would be cp1252
        text = (sys.stdin.buffer.read().decode("utf-8", errors="replace") if a.file == "-"
                else open(a.file, encoding="utf-8", errors="replace").read())
    except OSError as e:
        print("Error reading %s: %s" % (a.file, e))
        return 2
    report, problems = check(text)
    for line, who, want, why, n in report:
        print("Story (line %d): persona='%s' | want='%s' | so_that='%s' | %d scenario(s)" % (line, who, want, why, n))
    for sev, line, msg in sorted(problems, key=lambda p: (p[1], p[0])):
        print("%-7s line %d: %s" % (sev, line, msg))
    errs = sum(1 for p in problems if p[0] == "ERROR")
    print("\nSummary: %d story(ies), %d error(s), %d warning(s). [practice] Mechanical check: INVEST and business value"
          " require judgment." % (len(report), errs, len(problems) - errs))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

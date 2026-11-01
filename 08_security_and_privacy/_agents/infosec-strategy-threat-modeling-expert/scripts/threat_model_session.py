# -*- coding: utf-8 -*-
"""
threat_model_session.py - template and guide for a threat modeling session based on the Threat Modeling Manifesto (TMM).

Usage (Python 3, stdlib, no network, read-only; run with `python -I`):
  python -I scripts/threat_model_session.py questions|values|principles|patterns|antipatterns
  python -I scripts/threat_model_session.py template [--system NAME] [--scope TEXT] [--dz-bridge] [--extrapolation]
  python -I scripts/threat_model_session.py agenda [--minutes 90]
  python -I scripts/threat_model_session.py checklist
  python -I scripts/threat_model_session.py evaluate FILE.json       # {"V1":"sim","AP2":"nao",...} (sim/nao/parcial/na or yes/no/partial/na)

HONESTY: the TMM (3 pages) is methodology-agnostic and "not a how-to" (TMM p.1). Only the following come from the
manifesto: the four questions, the 5 values, the 4 principles, 5 patterns and 4 anti-patterns. The session structure,
the table fields, the timings and the bridge to the DZ risk register are the agent's [inference]. STRIDE, DFD and trust
boundaries are NOT in the TMM or the DZ: they appear only with --extrapolation, labeled [extrapolation].
Exit code: 0 ok; 2 invalid input.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

QUESTIONS = [
    ("Q1", "What are we working on?", "TMM p.1"),
    ("Q2", "What can go wrong?", "TMM p.1"),
    ("Q3", "What are we going to do about it?", "TMM p.1"),
    ("Q4", "Did we do a good enough job?", "TMM p.1"),
]

VALUES = [
    ("V1", "A culture of finding and fixing design issues", "the compliance checkbox", "TMM p.1"),
    ("V2", "People and collaboration", "processes, methodologies and tools", "TMM p.1"),
    ("V3", "A journey of understanding", "a security or privacy snapshot", "TMM p.1"),
    ("V4", "Doing threat modeling", "talking about it", "TMM p.1"),
    ("V5", "Continuous refinement", "a single delivery", "TMM p.1"),
]

PRINCIPLES = [
    ("PR1", "The best use is to improve security and privacy through early and frequent analysis.", "TMM p.2"),
    ("PR2", "Align with development practices and follow design changes in iterations, each scoped to a manageable portion of the system.", "TMM p.2"),
    ("PR3", "Results are meaningful when they have value to stakeholders.", "TMM p.2"),
    ("PR4", "Dialogue establishes the common understandings that create value; documents record those understandings and enable measurement.", "TMM p.2"),
]

PATTERNS = [
    ("PT1", "Systematic Approach", "Rigor and repeatability by applying security and privacy knowledge in a structured way.", "TMM p.2"),
    ("PT2", "Informed Creativity", "Room for creativity, with craft and science.", "TMM p.2"),
    ("PT3", "Varied Viewpoints", "A diverse team, with experts and cross-functional collaboration.", "TMM p.2"),
    ("PT4", "Useful Toolkit", "Tools that increase productivity, improve workflows, and provide repeatability and measurability.", "TMM p.2"),
    ("PT5", "Theory into Practice", "Field-tested techniques, aligned with local need and aware of their benefits and limits.", "TMM p.2"),
]

ANTIPATTERNS = [
    ("AP1", "Hero Threat Modeler", "It does not depend on innate skill or a single mindset; everyone can and should do it.", "TMM p.2"),
    ("AP2", "Admiration for the Problem", "Go beyond analyzing; look for practical and relevant solutions.", "TMM p.2"),
    ("AP3", "Tendency to Overfocus", "Do not lose the big picture (parts of the model are interdependent); avoid overemphasizing adversaries, assets or techniques.", "TMM p.2"),
    ("AP4", "Perfect Representation", "Better to create several representations: there is no single ideal view and others may illuminate different problems.", "TMM p.2"),
]

# self-assessment items: "sim" = practice present / anti-pattern avoided.  [inference] in the wording; origin in brackets.
CHECK = [
    ("V1", "Does the session look for and fix design problems (and not only produce a document for compliance)?", "TMM p.1"),
    ("V2", "Does the session prioritize conversation and collaboration among people, using process and tools as support?", "TMM p.1"),
    ("V3", "Does the group treat the model as an evolving understanding, rather than a single snapshot?", "TMM p.1"),
    ("V4", "Is the session actually analyzing the system (doing), and not just discussing how it would be done?", "TMM p.1"),
    ("V5", "Is there a plan to refine the model (new iteration) instead of a single delivery?", "TMM p.1"),
    ("PR1", "Does the analysis happen early and is it planned to recur?", "TMM p.2"),
    ("PR2", "Is the scope a manageable portion and does the cadence follow the development iterations?", "TMM p.2"),
    ("PR3", "Were the stakeholders identified and do they see value in the results?", "TMM p.2"),
    ("PR4", "Was the dialogue recorded in a document that enables measurement (e.g., list of threats and actions)?", "TMM p.2"),
    ("PT1", "Is there a structured, repeatable approach for applying security and privacy knowledge?", "TMM p.2"),
    ("PT2", "Is there explicit room for creativity beyond the script?", "TMM p.2"),
    ("PT3", "Does the group have varied viewpoints (different experts and areas)?", "TMM p.2"),
    ("PT4", "Do the tools used help productivity, repeatability and measurement?", "TMM p.2"),
    ("PT5", "Are the chosen techniques field-tested and does the group know their limits?", "TMM p.2"),
    ("AP1", "Avoided Hero Threat Modeler: does more than one person know how to lead and take part?", "TMM p.2"),
    ("AP2", "Avoided Admiration for the Problem: do the threats become practical actions?", "TMM p.2"),
    ("AP3", "Avoided Tendency to Overfocus: did the group look at the big picture and the interdependencies?", "TMM p.2"),
    ("AP4", "Avoided Perfect Representation: is more than one representation of the system used?", "TMM p.2"),
]
CHECK_IDS = [c[0] for c in CHECK]

# Answer vocabulary: Portuguese (kept) + English aliases.
ANSWER_ALIASES = {"sim": "sim", "yes": "sim", "nao": "nao", "não": "nao", "no": "nao",
                  "parcial": "parcial", "partial": "parcial", "na": "na", "n/a": "na"}


def p_questions():
    print("# The four questions (TMM p.1)")
    for i, en, pg in QUESTIONS:
        print("- %s. %s [from source] (%s)" % (i, en, pg))


def p_values():
    print("# Values (TMM p.1): the item on the left is valued more")
    for i, l, r, pg in VALUES:
        print("- %s. %s > %s [from source] (%s)" % (i, l, r, pg))


def p_principles():
    print("# Principles (TMM p.2)")
    for i, t, pg in PRINCIPLES:
        print("- %s. %s [from source] (%s)" % (i, t, pg))


def p_patterns():
    print("# Patterns that help (TMM p.2)")
    for i, n, t, pg in PATTERNS:
        print("- %s. %s: %s [from source] (%s)" % (i, n, t, pg))


def p_antipatterns():
    print("# Anti-patterns that hinder (TMM p.2); the text of each one describes the correct stance")
    for i, n, t, pg in ANTIPATTERNS:
        print("- %s. %s: %s [from source] (%s)" % (i, n, t, pg))


def template(system, scope, bridge, extrap):
    L = []
    A = L.append
    A("# Threat modeling session: %s" % (system or "<system>"))
    A("")
    A("> Basis: Threat Modeling Manifesto (TMM p.1-2). The manifesto is methodology-agnostic and is not a how-to (TMM p.1). "
      "The four questions, values, principles, patterns and anti-patterns come from the manifesto [from source]; the session "
      "structure and the table fields are the agent's organization [inference].")
    A("")
    A("## 0. Preparation [inference from TMM p.2]")
    A("- Scope of this iteration (manageable portion, TMM p.2): %s" % (scope or "<describe the slice of the system>"))
    A("- Alignment with the development practice (sprint, release, design change that triggers the session): <...>")
    A("- Stakeholders and the value they expect from the result (TMM p.2): <...>")
    A("- Participants with varied viewpoints: development, operations, security, privacy, product, other experts (Varied Viewpoints pattern, TMM p.2): <...>")
    A("- Facilitation: rotate who leads; nobody depends on a single person (Hero Threat Modeler anti-pattern, TMM p.2): <...>")
    A("- Existing representations of the system (drawings, descriptions, flows): <...>")
    A("")
    A("## 1. What are we working on? (TMM p.1, question 1)")
    A("- Representation(s) of the system used. Use more than one if it helps; there is no single ideal view (TMM p.2, Perfect Representation): <...>")
    A("- What is in and out of scope; assumptions: <...>")
    A("- Relevant assets and data; who uses and who operates: <...> [inference]")
    A("- **Security and privacy** concerns to consider (TMM p.1): <...>")
    A("")
    A("## 2. What can go wrong? (TMM p.1, question 2)")
    A("- The discovery technique is left to the group: the TMM does not prescribe a method (TMM p.1). Combine a structured approach with creativity (TMM p.2, Systematic Approach and Informed Creativity).")
    A("- Beware of overfocusing on adversaries, assets or techniques; remember the interdependencies (TMM p.2, Tendency to Overfocus).")
    A("")
    A("| ID | Threat (what can go wrong) | What/who is affected | Source/actor or cause | Notes |")
    A("|---|---|---|---|---|")
    A("| T1 | | | | |")
    A("| T2 | | | | |")
    A("")
    A("## 3. What are we going to do about it? (TMM p.1, question 3)")
    A("- Each relevant threat ends in a practical and relevant action (TMM p.2, Admiration for the Problem).")
    A("")
    A("| Threat | Decision | Concrete action | Owner | Deadline/iteration |")
    A("|---|---|---|---|---|")
    A("| T1 | mitigate / avoid / transfer / accept [DZ p.33 vocabulary, inference] | | | |")
    A("")
    A("## 4. Did we do a good enough job? (TMM p.1, question 4)")
    A("The TMM gives no numeric criterion; the group and the stakeholders define the criterion [inference]. Supporting questions:")
    A("- Did we cover the agreed scope? Is there an alternative representation that would reveal other problems (TMM p.2)?")
    A("- Do all relevant threats have a decision, an owner and a deadline?")
    A("- Do the stakeholders see value in the result (TMM p.2)?")
    A("- What will be measured from the documents (TMM p.2)? <...>")
    A("- What is left for the next iteration? (value: continuous refinement, TMM p.1) <...>")
    A("")
    A("## 5. Closing [inference from TMM p.1-2]")
    A("- Record the common understandings in a document that enables measurement (TMM p.2, principle 4).")
    A("- Review the anti-patterns (`python -I scripts/threat_model_session.py checklist`).")
    A("- Schedule the next iteration (trigger: design change) and the person responsible.")
    if bridge:
        A("")
        A("## Bridge to DZ risk management [inference]")
        A("The DZ does not describe threat modeling as a session; it treats threats within the risk process. To carry the result into the risk register:")
        A("- Actor: capability, interest and tactics (DZ p.25); environmental threats have no actor (DZ p.25).")
        A("- The organization's impact and likelihood scales (DZ example: 1-5 each; DZ p.28-29); Risk = Impact x Likelihood (DZ p.23).")
        A("- Appetite and acceptance level defined by the stakeholders (DZ p.33); treatment: avoid, reduce, transfer, accept (DZ p.33).")
        A("- Residual risk after the control and entry in the risk register (DZ p.34). Support script: `python -I scripts/risk_matrix.py`.")
    if extrap:
        A("")
        A("## [extrapolation] Optional representation and categories (NOT in the TMM or the DZ)")
        A("Outside the collection; use only if the group wants a starting point, and confirm against a current source:")
        A("- Representation: data flow diagram (external actors, processes, data stores, flows) with trust boundaries.")
        A("- Categories for question 2: STRIDE (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege).")
        A("- Privacy: specific techniques exist (for example LINDDUN); refer to `privacy-lgpd-engineering-expert`.")
        A("- TMM p.2 recommends several representations and field-tested techniques; none of them is prescribed.")
    print("\n".join(L))


def agenda(minutes):
    parts = [("Preparation and scope alignment", 0.10), ("Q1 What are we working on?", 0.25), ("Q2 What can go wrong?", 0.30), ("Q3 What are we going to do about it?", 0.25), ("Q4 Did we do a good enough job? + closing", 0.10)]
    # exact distribution (largest remainder) so the sum closes at `minutes`
    raw = [minutes * f for _, f in parts]
    base = [int(x) for x in raw]
    rest = minutes - sum(base)
    order = sorted(range(len(parts)), key=lambda i: (-(raw[i] - base[i]), i))
    for i in order[:rest]:
        base[i] += 1
    print("# Suggested agenda (%d min) [inference: the TMM does not define timings]" % minutes)
    for (n, _), m in zip(parts, base):
        print("- %3d min  %s" % (m, n))
    print("Total allocated: %d min." % sum(base))


def checklist():
    print("# Session self-assessment (yes = practice present / anti-pattern avoided) [inference in the wording; origin in the TMM]")
    for i, t, pg in CHECK:
        print("- [ ] %s %s (%s)" % (i, t, pg))


def evaluate(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("ERROR: could not read the JSON: %s" % e)
        return 2
    if not isinstance(data, dict):
        print("ERROR: the JSON must be an object {ID: answer}.")
        return 2
    bad = [k for k in data if k not in CHECK_IDS]
    if bad:
        print("ERROR: Unknown IDs: %s. Valid: %s" % (", ".join(bad), ", ".join(CHECK_IDS)))
        return 2
    inv = [k for k, v in data.items() if str(v).lower() not in ANSWER_ALIASES]
    if inv:
        print("ERROR: answers must be sim/nao/parcial/na (or yes/no/partial/na): %s" % ", ".join(inv))
        return 2
    sc = {"sim": 1.0, "parcial": 0.5, "nao": 0.0}
    tot = 0.0
    n = 0
    gaps = []
    notans = []
    for i, t, pg in CHECK:
        v = ANSWER_ALIASES.get(str(data.get(i, "")).lower(), "")
        if not v:
            notans.append(i)
            continue
        if v == "na":
            continue
        n += 1
        tot += sc[v]
        if v != "sim":
            gaps.append((i, v, t, pg))
    print("# Self-assessment result")
    if n:
        print("Adherence: %.0f%% (%d applicable items answered). The percentage is only a summary; read the gaps." % (100 * tot / n, n))
    else:
        print("No applicable item answered.")
    if gaps:
        print("## Gaps (%d)" % len(gaps))
        for i, v, t, pg in gaps:
            print("- %s [%s] %s (%s)" % (i, v, t, pg))
    if notans:
        print("## Unanswered: %s" % ", ".join(notans))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Threat modeling session guide (TMM)")
    sub = ap.add_subparsers(dest="cmd")
    for c in ("questions", "values", "principles", "patterns", "antipatterns", "checklist"):
        sub.add_parser(c)
    t = sub.add_parser("template")
    t.add_argument("--system", default="")
    t.add_argument("--scope", default="")
    t.add_argument("--dz-bridge", action="store_true")
    t.add_argument("--extrapolation", action="store_true")
    g = sub.add_parser("agenda")
    g.add_argument("--minutes", type=int, default=90)
    e = sub.add_parser("evaluate")
    e.add_argument("file")
    a = ap.parse_args()
    if a.cmd == "questions":
        p_questions()
    elif a.cmd == "values":
        p_values()
    elif a.cmd == "principles":
        p_principles()
    elif a.cmd == "patterns":
        p_patterns()
    elif a.cmd == "antipatterns":
        p_antipatterns()
    elif a.cmd == "checklist":
        checklist()
    elif a.cmd == "template":
        template(a.system, a.scope, a.dz_bridge, a.extrapolation)
    elif a.cmd == "agenda":
        if a.minutes < 10 or a.minutes > 600:
            print("ERROR: --minutes between 10 and 600")
            return 2
        agenda(a.minutes)
    elif a.cmd == "evaluate":
        return evaluate(a.file)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

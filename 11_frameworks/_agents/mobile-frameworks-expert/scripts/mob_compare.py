# -*- coding: utf-8 -*-
"""
mob_compare.py - RN x Flutter x Swift comparator using ONLY what the three sources in the collection say.
  RN  = React-Native-Getting-Started (4 pages; docs v0.87, updated Aug 12, 2026)
  FLT = Flutter-Docs (4 pages; landing page, no version)
  SWT = Swift-A-Tour-of-Swift (19 pages; Swift version not stated)
Each cell carries (a) a paraphrase with a page or (b) "NOT COVERED". There is no ranking and no recommendation: the sources
do not compare performance, market or cost, and do not say which one to choose. It never runs code or accesses the network.

Subcommands:
  list                       list the criteria
  table [--md]               full table (--md = Markdown)
  show CRITERION [...]       a single row (id or part of the name)
  ask "free text"            matches words against criteria; requests for a recommendation/"which is better" -> NOT COVERED
Labels: [from source] = it is on the cited page; [inference] = direct deduction; [extrapolation] = outside the collection (never produced here).
[DATED] to Aug 18, 2026 (capture) and, for RN, Aug 12, 2026.
Input keywords (criteria ids and search words) are recognized in Portuguese and in English.
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

SC = "NOT COVERED"

# id, name, keywords (Portuguese + English), RN, FLT, SWT
CRITERIOS = [
    ("natureza", "What the source is / declared nature", "natureza fonte tipo framework linguagem o que e nature source type language what is",
     "Introduction to the React Native documentation (how to use the docs, audience, Snack, notes) (RN p.1-3)",
     "Landing page of the Flutter documentation: cards and links (FLT p.1)",
     "Tour of the Swift language: syntax and features (SWT p.1)"),
    ("proposta", "Declared proposition", "proposta promessa objetivo uma base de codigo multiplataforma proposition promise goal single codebase cross-platform multiplatform",
     SC + " (the page is about how to read the docs; it states no technical proposition) (RN p.1)",
     "Build beautiful multiplatform apps from a single codebase (FLT p.1)",
     "Give enough to start writing Swift code (SWT p.1)"),
    ("publico", "Audience and prerequisites", "publico pre-requisito prerequisito conhecimento javascript iniciante audience prerequisite prerequisites knowledge beginner",
     "All levels; prerequisite: JavaScript fundamentals; React/Android/iOS valuable but not assumed (RN p.1)",
     "New to Flutter: set up the environment and follow the learning pathway; pages for people coming from Android, SwiftUI, UIKit, React Native and Xamarin.Forms (FLT p.1)",
     "Anyone who knows another language will find the syntax familiar; nothing else is assumed (SWT p.1)"),
    ("linguagem", "Programming language", "linguagem javascript dart swift codigo language code",
     "JavaScript (prerequisite) and React (RN p.1)",
     SC + " (Dart only appears in the videos, FLT p.2; the text does not say it is Flutter's language)",
     "Swift (the tour itself) (SWT p.1)"),
    ("plataformas", "Target platforms mentioned", "plataforma android ios web multiplataforma desktop platform platforms",
     "Android, iOS and Web appear as note labels (RN p.3); examples run on platforms such as Android and iOS (RN p.2)",
     "Multiplatform from a single codebase, without listing platforms (FLT p.1)",
     SC + " (the tour mentions no platforms or operating systems)"),
    ("ui", "Interface model", "ui interface widget native components componentes tela screen",
     "Foundation: Native Components (only mentioned as the next step; no definition) (RN p.3)",
     "In Flutter everything is a widget; there is a widget catalog (FLT p.1)",
     SC + " (the tour does not cover UI or mention SwiftUI/UIKit)"),
    ("layout", "Layout", "layout constraints tamanho posicao size position",
     SC,
     "Building layouts and Understanding constraints pages; summary: constraints go down, sizes go up, parents set positions (FLT p.1-2)",
     SC),
    ("estado", "State and interactivity", "estado state interatividade stateful interactivity",
     SC + " (React is mentioned as a section, with no content) (RN p.1)",
     "'Adding interactivity' page about adding a stateful widget (title only) (FLT p.2)",
     SC + " (willSet/didSet are property observers, not UI state) (SWT p.11)"),
    ("ambiente", "Installation / development environment", "instalacao instalar ambiente setup install download environment installation",
     "A local environment guide exists and is optional; getting-started instructions are in another section (RN p.1, 3)",
     "'Install Flutter' card and 'set up your environment' step (links, no steps) (FLT p.1)",
     SC + " (only 'Download'/'Getting Started' navigation labels at the top, SWT p.1)"),
    ("experimentacao", "Trying things in the browser / exercises", "experimentar snack playground exercicio experiment interativo try browser exercise exercises interactive",
     "Snack Player (Expo): editable examples in the browser (RN p.2-3)",
     SC + " (there are links to tutorials, workshops and recipes, with no content) (FLT p.1)",
     "'Experiment' boxes with exercises throughout the tour (e.g. SWT p.2, 4, 6)"),
    ("ia", "Artificial intelligence", "ia ai inteligencia artificial artificial intelligence",
     SC,
     "'Create with AI' card: build with and integrate AI tools (title and one sentence only) (FLT p.1)",
     SC),
    ("concorrencia", "Concurrency / asynchrony", "concorrencia async await thread assincrono actor task concurrency asynchrony asynchronous",
     SC,
     SC,
     "async/await, async let, Task, task groups and actors (SWT p.14-15)"),
    ("erros", "Error handling", "erro erros exception throw catch try defer error errors exceptions",
     SC, SC,
     "throw/throws, do-catch, try?, defer (SWT p.17-18)"),
    ("tipos", "Type system / generics", "tipos tipo generics genericos protocolo struct class enum types type protocol",
     SC, SC,
     "Inference, optionals, classes, structs, enums, protocols, extensions and generics (SWT p.1-19)"),
    ("navegacao", "Navigation between screens", "navegacao navigation rotas routes",
     SC, SC, SC),
    ("rede", "Network / data / persistence", "rede http api dados persistencia banco network data persistence database",
     SC, SC, SC),
    ("testes", "Testing", "testes teste test tests testing",
     SC, SC, SC),
    ("build", "Build, publishing and distribution", "build release publicar deploy loja store publish publishing distribution",
     SC, SC, SC),
    ("desempenho", "Performance / benchmarks", "desempenho performance benchmark velocidade speed benchmarks",
     SC, SC, SC),
    ("versao", "Source version and date", "versao data version atualizacao date update updated",
     "Docs 0.87 (selector); last updated Aug 12, 2026 (RN p.1, 4) [DATED]",
     "No version or date printed (NOT COVERED); capture on Aug 18, 2026 only in the metadata of the PDF",
     "Swift version not stated; copyright 2014-2026 (SWT p.19) [DATED]"),
    ("licenca", "Content license", "licenca license copyright creative commons bsd licence",
     SC + " (the capture carries no license)",
     "Site under CC BY 4.0; code samples under the 3-clause BSD license (FLT p.4)",
     "Document under CC BY 4.0; Swift and the logo are trademarks of Apple (SWT p.19)"),
    ("videos", "Videos and guided learning", "video videos youtube aprendizado trilha learning pathway guided",
     SC + " (linear or per-section reading, RN p.1)",
     "YouTube channel, Google I/O sessions, Full-stack developer guide series (FLT p.2-3); learning pathway (FLT p.1)",
     SC),
]

RECO = re.compile(r"\b(melhor|recomend\w*|escolh\w*|vale a pena|devo usar|qual usar|mais rapido|mais r[aá]pido|superior|ganha|vence"
                  r"|best|better|recommend\w*|choose|choice|worth it|should i use|which one to use|which to use|faster|fastest|wins|beats)\b", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def find(q):
    qn = norm(q)
    out = []
    for c in CRITERIOS:
        hay = norm(c[0] + " " + c[1] + " " + c[2])
        if qn == c[0] or qn in hay:
            out.append(c)
    return out


def line(c):
    return (f"== {c[1]} [{c[0]}]\n  RN : {c[3]}\n  FLT: {c[4]}\n  SWT: {c[5]}")


def cmd_table(md):
    if md:
        print("| Criterion | RN (React Native) | FLT (Flutter) | SWT (Swift Tour) |\n|---|---|---|---|")
        for c in CRITERIOS:
            print(f"| {c[1]} | {c[3]} | {c[4]} | {c[5]} |")
    else:
        for c in CRITERIOS:
            print(line(c))
    n = sum(1 for c in CRITERIOS for x in c[3:6] if x.startswith(SC))
    print(f"\n{len(CRITERIOS)} criteria; {n} of {3*len(CRITERIOS)} cells NOT COVERED. No ranking: the sources do not compare and do not recommend. [DATED] 2026.")


def cmd_ask(text):
    if RECO.search(text):
        print("NOT COVERED: the sources do not compare performance, market or cost, and do not recommend which one to choose. Any recommendation would be [extrapolation]; "
              "RN and FLT are minimal sources and SWT is a language (not a UI framework). Comparator criteria (many also NOT COVERED): " + ", ".join(c[0] for c in CRITERIOS) + ".")
    tn = norm(text)
    hits = []
    for c in CRITERIOS:
        kws = set(norm(c[0] + " " + c[2]).split())
        if any(k in tn.split() or (len(k) >= 5 and k in tn) for k in kws):
            hits.append(c)
    if not hits:
        print("NOT COVERED: no comparator criterion matches the question. Use `list` to see the criteria.")
        return 0
    for c in hits[:6]:
        print(line(c))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("list")
    t = sp.add_parser("table")
    t.add_argument("--md", action="store_true")
    s = sp.add_parser("show")
    s.add_argument("termos", nargs="+")
    a_ = sp.add_parser("ask")
    a_.add_argument("texto", nargs="+")
    a = ap.parse_args()
    if a.cmd == "list":
        for c in CRITERIOS:
            print(f"{c[0]:<15} {c[1]}")
        return 0
    if a.cmd == "table":
        cmd_table(a.md)
        return 0
    if a.cmd == "show":
        found = []
        for t in a.termos:
            found += find(t)
        if not found:
            print("NOT COVERED: criterion not found (use `list`).")
            return 1
        seen = set()
        for c in found:
            if c[0] not in seen:
                seen.add(c[0])
                print(line(c))
        return 0
    if a.cmd == "ask":
        return cmd_ask(" ".join(a.texto))
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

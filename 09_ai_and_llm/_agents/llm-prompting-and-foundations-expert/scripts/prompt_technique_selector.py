# -*- coding: utf-8 -*-
"""
prompt_technique_selector.py - prompting technique selector based on the PES taxonomy
(Sahoo et al., "A Systematic Survey of Prompt Engineering in LLMs", arXiv 2402.07927v2, 16 Mar 2025) [DATED].

Read-only, stdlib, no network, deterministic. Each technique carries its PES page (PDF = printed).
The gain figures are "as reported" for distinct models/datasets and are NOT comparable across techniques.

Usage:
  python -I scripts/prompt_technique_selector.py --list
  python -I scripts/prompt_technique_selector.py --categories
  python -I scripts/prompt_technique_selector.py --tags
  python -I scripts/prompt_technique_selector.py --need matematica alucinacao [--no-external] [--turn single|multi]
        [--acq Manual|"LM Generated"|"Retrieval Based"|Hybrid] [--top N] [--json]
  python -I scripts/prompt_technique_selector.py --show cot
  python -I scripts/prompt_technique_selector.py --compare cot tot
  python -I scripts/prompt_technique_selector.py --tips [--principle N]
"""
import argparse
import json
import os
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))

ALIASES = {
    # pt-BR / en -> tag (Portuguese aliases kept so Portuguese input still resolves)
    "matematica": "reasoning-math", "math": "reasoning-math", "aritmetica": "reasoning-math", "calculo": "numerical",
    "numerico": "numerical", "logica": "reasoning-logic", "logic": "reasoning-logic", "raciocinio": "reasoning-logic",
    "senso-comum": "commonsense", "commonsense": "commonsense", "simbolico": "symbolic", "symbolic": "symbolic",
    "espacial": "spatial", "spatial": "spatial", "temporal": "temporal", "tempo": "temporal",
    "grafo": "graph", "graph": "graph", "tabela": "table", "table": "table", "dados-estruturados": "structured-data",
    "codigo": "code", "code": "code", "programacao": "code-generation",
    "recuperacao": "retrieval", "rag": "retrieval", "retrieval": "retrieval", "busca-externa": "retrieval",
    "alucinacao": "hallucination", "hallucination": "hallucination", "verificacao": "verification",
    "verification": "verification", "conhecimento-externo": "external-knowledge", "atualizado": "up-to-date",
    "ferramenta": "tool-use", "ferramentas": "tool-use", "tool": "tool-use",
    "contexto-longo": "long-context", "contexto-ruidoso": "noisy-context", "ruido": "noisy-context", "ruidoso": "noisy-context",
    "tokens": "efficiency-tokens", "economia-de-tokens": "efficiency-tokens", "latencia": "efficiency-latency",
    "custo": "efficiency-cost", "cost": "efficiency-cost", "latency": "efficiency-latency", "tools": "tool-use", "token-efficiency": "efficiency-tokens", "planning": "planning", "ambiguity": "ambiguity-intent", "uncertainty": "uncertainty", "legal": "legal", "robust": "robustness", "sem-exemplos": "no-examples", "zero-shot": "no-examples",
    "poucos-exemplos": "few-shot", "few-shot": "few-shot", "exemplos": "examples",
    "prompt-automatico": "automatic-prompt", "automatico": "automatic-prompt", "gerar-prompt": "automatic-prompt",
    "otimizar-prompt": "prompt-optimization", "otimizacao-de-prompt": "prompt-optimization",
    "selecao-de-exemplos": "example-selection", "gerar-exemplos": "example-generation",
    "autocritica": "self-feedback", "autorrefinamento": "refinement", "refinar": "refinement",
    "busca": "search-exploration", "exploracao": "search-exploration", "backtracking": "backtracking",
    "planejamento": "planning", "passos": "multi-step", "multi-passo": "multi-step",
    "ambiguidade": "ambiguity-intent", "intencao": "user-intent", "abstracao": "abstraction",
    "emocao": "tone-emotion", "tom": "tone-emotion", "multimodal": "multimodal", "juridico": "legal", "direito": "legal",
    "modelo-pequeno": "small-model", "incerteza": "uncertainty", "qa-factual": "factual-qa", "factual": "factual-qa",
    "robustez": "robustness", "votacao": "voting", "amostragem": "sampling", "medico": "medical",
    "geometria": "geometry", "stem": "stem", "multi-hop": "multi-hop", "conversa": "conversation",
    "resposta-longa": "long-form", "escrita": "writing", "interativo": "interactive",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip().replace("_", "-").replace(" ", "-")


def load():
    with open(os.path.join(HERE, "pes_techniques.json"), encoding="utf-8") as f:
        return json.load(f)


def resolve_tag(word, known):
    w = norm(word)
    if w in known:
        return w
    return ALIASES.get(w)


def find_tech(data, key):
    k = norm(key)
    for t in data["tecnicas"]:
        if k == norm(t["id"]) or k == norm(t["name"]):
            return t
    for t in data["tecnicas"]:
        if k in norm(t["name"]) or k in norm(t["id"]):
            return t
    return None


def fmt(t, brief=False):
    out = [f"- {t['name']} [id: {t['id']}] - §{t['section']} {t['category']} - PES p.{t['pages']} (Table 1: PES p.10)"]
    out.append(f"  prompt acquisition: {t['acquisition']}; turns: {t['turn']}; models (Tab.1): {t['models']}")
    if not brief:
        out.append(f"  idea: {t['summary']}")
        for r in t["reported"]:
            out.append(f"  [do livro] reported: {r}")
        out.append(f"  limits: {t['limits']}")
        out.append(f"  datasets: {t['datasets']}; metrics: {t['metrics']}")
        out.append(f"  uses an external resource (tool/interpreter/retrieval/search)? {'yes' if t['needs_external'] else 'not stated'} [inference]")
        out.append(f"  tags: {', '.join(t['tags'])}")
    return "\n".join(out)


DISC = ("[DATED] PES = Mar/2025. Numbers 'as reported' on different models/datasets: NOT comparable across techniques. "
        "The survey gives no ranking or selection guide; the ranking below is only by tag matching [inference].")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--categories", action="store_true")
    ap.add_argument("--tags", action="store_true")
    ap.add_argument("--need", nargs="+")
    ap.add_argument("--no-external", action="store_true", help="exclude techniques that use a tool/interpreter/retrieval")
    ap.add_argument("--turn", choices=["single", "multi"])
    ap.add_argument("--acq")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--brief", action="store_true", help="short output in --need")
    ap.add_argument("--show")
    ap.add_argument("--compare", nargs=2)
    ap.add_argument("--tips", action="store_true")
    ap.add_argument("--principle", type=int)
    a = ap.parse_args()

    data = load()
    techs = data["tecnicas"]
    known = sorted({tg for t in techs for tg in t["tags"]})

    if a.tips:
        with open(os.path.join(HERE, "llms_prompt_tips.json"), encoding="utf-8") as f:
            tips = json.load(f)
        if a.json:
            print(json.dumps(tips, ensure_ascii=False, indent=1))
            return
        print("LLMS - design principles (p.45-46) and Tab.12 tips (p.47) [from source, paraphrased]. " + tips["datado"])
        for p in tips["principios"]:
            print(f"  principle {p['id']} (LLMS p.{p['pagina']}): {p['texto']}")
        for d in tips["dicas"]:
            if a.principle and a.principle not in d["principios"]:
                continue
            print(f"  {d['id']} [{d['ingrediente']}; principles {d['principios']}] (LLMS p.{d['pagina']}): {d['texto']}")
        return

    if a.list:
        for t in techs:
            print(fmt(t, brief=True))
        print(f"Total: {len(techs)} techniques (Fig.2, PES p.3). {DISC}")
        return
    if a.categories:
        for sec, name in data["categorias"].items():
            members = [t["name"] for t in techs if t["section"] == sec]
            print(f"§{sec} {name} (PES p.3): {', '.join(members)}")
        return
    if a.tags:
        counts = {}
        for t in techs:
            for tg in t["tags"]:
                counts[tg] = counts.get(tg, 0) + 1
        for tg in sorted(counts):
            print(f"{tg} ({counts[tg]})")
        print("Aliases accepted in --need (pt-BR and English): " + ", ".join(sorted(ALIASES)))
        return
    if a.show:
        t = find_tech(data, a.show)
        if not t:
            print(f"NOT COVERED: '{a.show}' is not among the 41 techniques in Fig.2 of the PES (p.3).")
            sys.exit(2)
        print(fmt(t))
        print(DISC)
        return
    if a.compare:
        ts = [find_tech(data, k) for k in a.compare]
        for k, t in zip(a.compare, ts):
            if not t:
                print(f"NOT COVERED: '{k}' is not in the PES.")
                sys.exit(2)
        for field in ("category", "pages", "acquisition", "turn", "models", "datasets", "metrics", "limits"):
            print(f"{field}: " + " | ".join(f"{t['name']}: {t[field]}" for t in ts))
        for t in ts:
            for r in t["reported"]:
                print(f"[do livro] {t['name']}: {r}")
        print("ATTENTION: models and datasets differ; the gains are NOT directly comparable [inference]. " + DISC)
        return
    if a.need:
        wanted, unknown = [], []
        for w in a.need:
            tg = resolve_tag(w, set(known))
            (wanted if tg else unknown).append(tg or w)
        if unknown:
            print("Terms with no matching tag (ignored): " + ", ".join(unknown) + " -- see --tags.")
        if not wanted:
            print("NOT COVERED: no criterion recognized in the PES taxonomy.")
            sys.exit(2)
        rows = []
        for t in techs:
            if a.no_external and t["needs_external"]:
                continue
            if a.turn and t["turn"].lower() != a.turn:
                continue
            if a.acq and norm(t["acquisition"]) != norm(a.acq):
                continue
            hit = [tg for tg in wanted if tg in t["tags"]]
            if hit:
                rows.append((-len(hit), tuple(int(x) for x in t["section"].split(".")), t["name"], hit, t))
        rows.sort(key=lambda r: (r[0], r[1], r[2]))
        rows = rows[: a.top]
        if not rows:
            print("NOT COVERED: no PES technique meets these criteria. " + DISC)
            sys.exit(2)
        if a.json:
            print(json.dumps({"criterios": wanted, "aviso": DISC,
                              "resultados": [{"id": r[4]["id"], "name": r[4]["name"], "paginas": "PES p." + r[4]["pages"],
                                              "casou": r[3], "reported": r[4]["reported"], "limits": r[4]["limits"]} for r in rows]},
                             ensure_ascii=False, indent=1))
            return
        print(f"Criteria (tags): {', '.join(wanted)}")
        for r in rows:
            print(f"* matched {len(r[3])}/{len(wanted)}: {', '.join(r[3])}")
            print(fmt(r[4], brief=a.brief))
        print(DISC)
        return
    ap.print_help()


if __name__ == "__main__":
    main()

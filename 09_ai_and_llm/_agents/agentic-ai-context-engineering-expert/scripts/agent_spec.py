# -*- coding: utf-8 -*-
"""
agent_spec.py - agent specification template (role, tools, memory, context, guardrails, evaluation)
and gap validator, anchored in BAAS (2025) and CE2 (2025).

Stdlib, no network, deterministic, read-only (does not write files; redirect the output).
Commands:
  template                 prints a blank JSON with all fields
  sample                   prints an example JSON (travel agent; the contents are illustrative, inspired by the BAAS examples)
  render SPEC.json         generates the specification in Markdown
  validate SPEC.json       lists gaps and weaknesses, each with the page that supports the requirement
Convention: pages = PDF (BAAS printed = PDF - 25; CE2 PDF = printed).
Labels: the STRUCTURE of the template is the package's [inference]; each validator requirement cites the page where the text presents the idea
([from source]). Requirements with no page in the texts are marked [extrapolation]. This template is NOT a standard of the texts and
does NOT replace security review, empirical evaluation, or legal advice. The validator checks PRESENCE and simple coherence, not quality.
Field names of the JSON specification (nome, papel, arquitetura, ...) are the schema identifiers and stay as they are, for compatibility.
Enum values accept English (deliberative|reactive|hybrid; low|medium|high) and the original Portuguese values
(deliberativa|reativa|hibrida; baixo|medio|alto).
"""
import argparse
import io
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ARQS = ("deliberative", "reactive", "hybrid")
RISCOS = ("low", "medium", "high")
ARQ_CANON = {"deliberative": "deliberative", "deliberativa": "deliberative", "reactive": "reactive", "reativa": "reactive",
             "hybrid": "hybrid", "hibrida": "hybrid", "híbrida": "hybrid"}
RISCO_CANON = {"low": "low", "baixo": "low", "medium": "medium", "medio": "medium", "médio": "medium", "high": "high", "alto": "high"}


def canon(table, v):
    return table.get(v.strip().lower()) if isinstance(v, str) else None

TEMPLATE = {
    "nome": "",
    "papel": "",
    "meta": "",
    "backstory": "(optional; prompt resource of frameworks such as CrewAI, BAAS p.169)",
    "escopo": {"dentro": [], "fora": []},
    "arquitetura": "hybrid",
    "autonomia": {"operacional": "", "funcional": "", "hierarquica": "", "nivel_inicial": "restricted"},
    "prompt_sistema": {"papel_e_escopo": "", "restricoes": [], "protocolos_de_comunicacao": "", "arcabouco_de_decisao": ""},
    "formatos": {"entrada": "", "saida": "", "mensagem_entre_agentes": ""},
    "ferramentas": [
        {"nome": "", "descricao": "", "parametros_obrigatorios": [], "parametros_opcionais": [], "retorno": "",
         "risco": "low", "aprovacao_humana": False, "executor_valida_parametros": True, "fallback": ""}
    ],
    "estado": {"campos": [], "transicoes_validadas": []},
    "memoria": {"curto_prazo": "", "longo_prazo": "", "episodica": "", "retencao_e_acesso": ""},
    "contexto": {
        "inventario": {"usuario": "", "aplicacao": "", "ambiente": "", "ferramentas": "", "memoria": "", "servico_de_modelo": ""},
        "hierarquia": {"global": "", "sessao": "", "tarefa": ""},
        "selecao": [],
        "abstracao": "",
        "orcamento_tokens": {"janela": 0, "componentes": {}},
    },
    "multiagente": {"papeis": [], "protocolo": "", "regra_de_conflito": ""},
    "guardrails": {"limites_de_acao": [], "verificacao": "", "rollback": "", "monitoramento": "", "escalonamento_humano": "", "autonomia_progressiva": ""},
    "avaliacao": {"metricas_de_produto": [], "metricas_de_decisao": [], "testes_de_cadeia_de_acoes": [], "monitoramento": []},
}

SAMPLE = {
    "nome": "Corporate travel agent (example)",
    "papel": "Travel planning coordinator",
    "meta": "Build and book itineraries within the corporate policy and the traveler's budget",
    "backstory": "Prompt resource; not evidence of quality.",
    "escopo": {"dentro": ["search flights and hotels", "propose itineraries", "book within limits"], "fora": ["payments outside the secure flow", "legal advice"]},
    "arquitetura": "hybrid",
    "autonomia": {"operacional": "search and compare without a human", "funcional": "choose options by explicit utility", "hierarquica": "booking only within the limit", "nivel_inicial": "restricted"},
    "prompt_sistema": {
        "papel_e_escopo": "You coordinate corporate travel planning.",
        "restricoes": ["respect the budget", "prioritize traveler safety", "follow travel regulations"],
        "protocolos_de_comunicacao": "JSON messages with message_type, sender, recipient, and content",
        "arcabouco_de_decisao": "compare options by price, duration, and policy; present pros and cons",
    },
    "formatos": {"entrada": "task_type + parameters", "saida": "status + result{options, recommendations, constraints}", "mensagem_entre_agentes": "message_type/sender/recipient/content"},
    "ferramentas": [
        {"nome": "search_flights", "descricao": "Searches flights between cities in a date range", "parametros_obrigatorios": ["origin", "destination", "dates"],
         "parametros_opcionais": ["class"], "retorno": "list of flights with price and duration", "risco": "low", "aprovacao_humana": False,
         "executor_valida_parametros": True, "fallback": "try an alternative provider"},
        {"nome": "book_flight", "descricao": "Books a selected flight", "parametros_obrigatorios": ["flight_id", "passenger"], "parametros_opcionais": [],
         "retorno": "confirmation or error", "risco": "high", "aprovacao_humana": True, "executor_valida_parametros": True, "fallback": "notify the user"},
    ],
    "estado": {"campos": ["booking_id", "status", "components", "preferences"], "transicoes_validadas": ["pending -> confirmed requires payment and seats", "hotel after flight arrival"]},
    "memoria": {"curto_prazo": "session search parameters; cleared at the end", "longo_prazo": "customer profile and preferences", "episodica": "booking history and issues", "retencao_e_acesso": "minimization; role-based access"},
    "contexto": {
        "inventario": {"usuario": "request and preferences", "aplicacao": "system prompt and policy", "ambiente": "date, travel rules", "ferramentas": "tool definitions", "memoria": "retrieved profile and episodes", "servico_de_modelo": "window and output format"},
        "hierarquia": {"global": "corporate policy, alerts", "sessao": "current interaction", "tarefa": "booking in progress"},
        "selecao": ["semantic relevance", "logical dependency", "recency"],
        "abstracao": "structured summary per booking",
        "orcamento_tokens": {"janela": 128000, "componentes": {"sistema": 3000, "ferramentas": 4000, "memoria": 8000, "historico": 20000}},
    },
    "multiagente": {"papeis": ["coordinator", "delegator", "flight worker", "hotel worker"], "protocolo": "JSON messages", "regra_de_conflito": "delegator mediates; coordinator decides by predefined criteria"},
    "guardrails": {
        "limites_de_acao": ["do not book above the limit without approval", "do not book destinations flagged as high-risk"],
        "verificacao": "multi-step check before expensive bookings",
        "rollback": "action log and reversal respecting cancellation policies",
        "monitoramento": "atypical booking patterns",
        "escalonamento_humano": "human approval above the threshold",
        "autonomia_progressiva": "start restricted and widen with demonstrated reliability",
    },
    "avaliacao": {
        "metricas_de_produto": ["recommendation acceptance", "complaints"],
        "metricas_de_decisao": ["consistency with the policy", "cost-benefit"],
        "testes_de_cadeia_de_acoes": ["cancelled-flight scenario with a dependent hotel"],
        "monitoramento": ["state-update latency", "error rate"],
    },
}


def load(path):
    try:
        with io.open(path, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError) as e:
        print(f"error reading {path}: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(d, dict):
        print("error: the specification must be a JSON object", file=sys.stderr)
        sys.exit(2)
    return d


def empty(v):
    if v is None:
        return True
    if isinstance(v, str):
        s = v.strip()
        return s == "" or s.startswith(("(opcional", "(optional"))
    if isinstance(v, (list, dict)):
        return len(v) == 0
    return False


def get(d, *path):
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def validate(d):
    """Returns a list of (severity, field, message, origin+page)."""
    out = []

    def need(path, msg, src, sev="GAP"):
        if empty(get(d, *path)):
            out.append((sev, ".".join(path), msg, src))

    need(("nome",), "define the agent name", "BAAS p.168-169 [from source]")
    need(("papel",), "define the role", "BAAS p.168-169 [from source]")
    need(("meta",), "define the goal", "BAAS p.168-169 [from source]")
    arq = get(d, "arquitetura")
    if canon(ARQ_CANON, arq) is None:
        out.append(("GAP", "arquitetura", f"provide one of {', '.join(ARQS)} (current: {arq!r})", "BAAS p.61-65 [from source]"))
    for k, kn in (("operacional", "operational"), ("funcional", "functional"), ("hierarquica", "hierarchical")):
        need(("autonomia", k), f"describe the {kn} autonomy", "BAAS p.55-56 [from source]")
    need(("autonomia", "nivel_inicial"), "define the initial autonomy level (start restricted)", "BAAS p.240 [from source]")
    for k, m in (("papel_e_escopo", "role and scope"), ("restricoes", "constraints and limits"),
                 ("protocolos_de_comunicacao", "communication protocols"), ("arcabouco_de_decisao", "decision framework")):
        need(("prompt_sistema", k), f"system prompt without {m}", "BAAS p.179-180 [from source]")
    for k, kn in (("entrada", "input"), ("saida", "output")):
        need(("formatos", k), f"define the {kn} format", "BAAS p.180-181 [from source]")
    ferr = get(d, "ferramentas")
    if not isinstance(ferr, list) or not ferr:
        out.append(("WARNING", "ferramentas", "no tools: without tools, plans that depend on external data tend to be invented", "BAAS p.150-151 [from source]"))
    else:
        if len(ferr) > 30:
            out.append(("WARNING", "ferramentas", f"{len(ferr)} tools: CE2 reports degradation above 30 and failure above 100 (DeepSeek-v3) [DATED]", "CE2 p.18 [from source]"))
        for i, t in enumerate(ferr):
            nm = (t or {}).get("nome") or f"#{i + 1}"
            if not isinstance(t, dict):
                out.append(("GAP", f"ferramentas[{i}]", "tool must be an object", "BAAS p.135-137 [from source]"))
                continue
            if empty(t.get("nome")) or empty(t.get("descricao")):
                out.append(("GAP", f"ferramentas[{nm}]", "name and description are the minimum for the LLM to choose the tool", "BAAS p.135-136 [from source]"))
            if "parametros_obrigatorios" not in t:
                out.append(("GAP", f"ferramentas[{nm}]", "indicate required and optional parameters", "BAAS p.135-136 [from source]"))
            if canon(RISCO_CANON, t.get("risco")) is None:
                out.append(("GAP", f"ferramentas[{nm}]", f"classify the risk ({', '.join(RISCOS)})", "BAAS p.237 [from source]; classification = [inference]"))
            if canon(RISCO_CANON, t.get("risco")) == "high" and not t.get("aprovacao_humana"):
                out.append(("ALERT", f"ferramentas[{nm}]", "high-risk action without human approval: the book suggests human approval above thresholds and multi-step verification", "BAAS p.238-239 [from source]"))
            if t.get("executor_valida_parametros") is False:
                out.append(("ALERT", f"ferramentas[{nm}]", "the executor of the call (Agent Controller) should validate parameters and permissions; the LLM only emits the call", "BAAS p.134-135 [from source]; validation = [inference]"))
            if empty(t.get("fallback")):
                out.append(("WARNING", f"ferramentas[{nm}]", "no fallback for tool failure", "BAAS p.139 [from source]"))
    need(("estado", "campos"), "define the task state (status, components, dependencies)", "BAAS p.192-193 [from source]")
    need(("estado", "transicoes_validadas"), "list state transitions validated before being committed", "BAAS p.197-198 [from source]", "WARNING")
    for k, kn in (("curto_prazo", "short-term"), ("longo_prazo", "long-term"), ("episodica", "episodic")):
        need(("memoria", k), f"define the {kn} memory (or state that it does not apply)", "BAAS p.198-202 [from source]", "WARNING")
    need(("memoria", "retencao_e_acesso"), "define retention and access control for persistent memory", "BAAS p.241-242 [from source] (minimization); retention policy = [extrapolation]", "WARNING")
    for k in ("usuario", "aplicacao", "ambiente", "ferramentas", "memoria", "servico_de_modelo"):
        need(("contexto", "inventario", k), f"context inventory without '{k}'", "CE2 p.4-5 [from source]", "WARNING")
    for k in ("global", "sessao", "tarefa"):
        need(("contexto", "hierarquia", k), f"context hierarchy without level '{k}'", "BAAS p.202-203 [from source]", "WARNING")
    need(("contexto", "selecao"), "define context selection criteria", "CE2 p.16 [from source]", "WARNING")
    need(("contexto", "abstracao"), "define how raw context is abstracted (summary, schema, vectors, hierarchy)", "CE2 p.13-14 [from source]", "WARNING")
    jan = get(d, "contexto", "orcamento_tokens", "janela")
    comps = get(d, "contexto", "orcamento_tokens", "componentes")
    if not isinstance(jan, (int, float)) or jan <= 0 or not isinstance(comps, dict) or not comps:
        out.append(("WARNING", "contexto.orcamento_tokens", "define the window and tokens per component (use ctx_calc.py budget)", "CE2 p.16 [from source] (DATED heuristic); budget = [inference]"))
    else:
        try:
            tot = sum(float(v) for v in comps.values())
            if tot > jan:
                out.append(("ALERT", "contexto.orcamento_tokens", f"components add up to {tot:,.0f} tokens, above the window of {jan:,.0f}", "[arithmetic]"))
            elif tot / jan > 0.5:
                out.append(("WARNING", "contexto.orcamento_tokens", f"occupancy {tot / jan:.0%} (CE2 p.16 reports performance degradation in coding agents above ~50% [DATED])", "CE2 p.16 [from source]"))
        except (TypeError, ValueError):
            out.append(("GAP", "contexto.orcamento_tokens.componentes", "values must be numeric", "[arithmetic]"))
    papeis = get(d, "multiagente", "papeis")
    if isinstance(papeis, list) and len(papeis) > 1:
        need(("multiagente", "protocolo"), "define the communication protocol between agents", "BAAS p.177, 180-181 [from source]; CE2 p.14-15 [from source]")
        need(("multiagente", "regra_de_conflito"), "define the conflict resolution rule", "BAAS p.177-178 [from source]")
    for k, m, src in (("limites_de_acao", "action limits", "BAAS p.237-239 [from source]"),
                      ("verificacao", "decision verification", "BAAS p.237 [from source]"),
                      ("rollback", "rollback/reversal", "BAAS p.237-239 [from source]"),
                      ("monitoramento", "monitoring", "BAAS p.238 [from source]"),
                      ("escalonamento_humano", "human escalation", "BAAS p.238 [from source]"),
                      ("autonomia_progressiva", "progressive autonomy", "BAAS p.240 [from source]")):
        need(("guardrails", k), f"guardrails without {m}", src)
    for k, m, src in (("metricas_de_produto", "product metrics", "BAAS p.115 [from source]"),
                      ("metricas_de_decisao", "decision metrics", "BAAS p.238 [from source]"),
                      ("testes_de_cadeia_de_acoes", "action-chain tests", "BAAS p.239 [from source]"),
                      ("monitoramento", "operational monitoring", "BAAS p.198 [from source]")):
        need(("avaliacao", k), f"evaluation without {m}", src)
    out.append(("NOTE", "geral", "the texts provide neither benchmarks nor a quantitative evaluation method for agents; the evaluation must be designed and measured by you", "CE2 p.18 [from source]; BAAS (absence)"))
    out.append(("NOTE", "geral", "treating retrieved data and tool outputs as data (not instructions) is not detailed in the texts", "[extrapolation]"))
    return out


def sec(title, body):
    print(f"\n## {title}\n")
    print(body)


def bullets(items):
    if not items:
        return "- (empty)"
    return "\n".join(f"- {x}" for x in items)


def render(d):
    print(f"# Agent specification: {d.get('nome') or '(unnamed)'}")
    print("\n> Package template (structure = [inference]); each section cites where the texts (BAAS, CE2) present the idea. Does not replace security review or empirical evaluation.")
    sec("1. Identity (BAAS p.168-169)", f"- Role: {d.get('papel', '')}\n- Goal: {d.get('meta', '')}\n- Backstory: {d.get('backstory', '')}\n- Architecture: {d.get('arquitetura', '')} (BAAS p.61-65)")
    esc = d.get("escopo") or {}
    sec("2. Scope", "In scope:\n" + bullets(esc.get("dentro")) + "\n\nOut of scope:\n" + bullets(esc.get("fora")))
    au = d.get("autonomia") or {}
    sec("3. Autonomy (BAAS p.55-56, 240)", "\n".join(f"- {k}: {au.get(k, '')}" for k in ("operacional", "funcional", "hierarquica", "nivel_inicial")))
    ps = d.get("prompt_sistema") or {}
    sec("4. System prompt (BAAS p.179-180)", f"- Role and scope: {ps.get('papel_e_escopo', '')}\n- Constraints:\n" + bullets(ps.get("restricoes")) +
        f"\n- Communication protocols: {ps.get('protocolos_de_comunicacao', '')}\n- Decision framework: {ps.get('arcabouco_de_decisao', '')}")
    fm = d.get("formatos") or {}
    sec("5. Formats (BAAS p.180-181)", "\n".join(f"- {k}: {fm.get(k, '')}" for k in ("entrada", "saida", "mensagem_entre_agentes")))
    lines = ["| Tool | Description | Required | Optional | Returns | Risk | Human approval | Executor validates | Fallback |", "|---|---|---|---|---|---|---|---|---|"]
    for t in d.get("ferramentas") or []:
        if not isinstance(t, dict):
            continue
        lines.append("| " + " | ".join([str(t.get("nome", "")), str(t.get("descricao", "")), ", ".join(map(str, t.get("parametros_obrigatorios", []))),
                                         ", ".join(map(str, t.get("parametros_opcionais", []))), str(t.get("retorno", "")), str(t.get("risco", "")),
                                         "yes" if t.get("aprovacao_humana") else "no", "yes" if t.get("executor_valida_parametros") else "no", str(t.get("fallback", ""))]) + " |")
    sec("6. Tools (BAAS p.135-139; CE2 p.18-19)", "\n".join(lines))
    es = d.get("estado") or {}
    sec("7. State (BAAS p.192-198)", "Fields:\n" + bullets(es.get("campos")) + "\n\nValidated transitions:\n" + bullets(es.get("transicoes_validadas")))
    me = d.get("memoria") or {}
    sec("8. Memory (BAAS p.198-202; CE2 p.12)", "\n".join(f"- {k}: {me.get(k, '')}" for k in ("curto_prazo", "longo_prazo", "episodica", "retencao_e_acesso")))
    cx = d.get("contexto") or {}
    inv = cx.get("inventario") or {}
    hi = cx.get("hierarquia") or {}
    ob = cx.get("orcamento_tokens") or {}
    body = "Inventory (CE2 p.4-5):\n" + "\n".join(f"- {k}: {inv.get(k, '')}" for k in ("usuario", "aplicacao", "ambiente", "ferramentas", "memoria", "servico_de_modelo"))
    body += "\n\nHierarchy (BAAS p.202-203):\n" + "\n".join(f"- {k}: {hi.get(k, '')}" for k in ("global", "sessao", "tarefa"))
    body += "\n\nSelection (CE2 p.16):\n" + bullets(cx.get("selecao")) + f"\n\nAbstraction (CE2 p.13-14): {cx.get('abstracao', '')}"
    comps = ob.get("componentes") or {}
    body += f"\n\nToken budget [inference]: window {ob.get('janela', 0)}; " + (", ".join(f"{k}={v}" for k, v in comps.items()) if comps else "no components")
    sec("9. Context", body)
    ma = d.get("multiagente") or {}
    sec("10. Multi-agent (BAAS p.164-182; CE2 p.12, 14-15, 19)", "Roles:\n" + bullets(ma.get("papeis")) + f"\n\n- Protocol: {ma.get('protocolo', '')}\n- Conflict rule: {ma.get('regra_de_conflito', '')}")
    gr = d.get("guardrails") or {}
    sec("11. Guardrails and oversight (BAAS p.237-240)", "Action limits:\n" + bullets(gr.get("limites_de_acao")) +
        "\n\n" + "\n".join(f"- {k}: {gr.get(k, '')}" for k in ("verificacao", "rollback", "monitoramento", "escalonamento_humano", "autonomia_progressiva")))
    av = d.get("avaliacao") or {}
    sec("12. Evaluation (BAAS p.114-115, 198, 238-239; CE2 p.18)", "\n\n".join(f"{k}:\n" + bullets(av.get(k)) for k in ("metricas_de_produto", "metricas_de_decisao", "testes_de_cadeia_de_acoes", "monitoramento")))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("template")
    sp.add_parser("sample")
    p = sp.add_parser("render")
    p.add_argument("arquivo")
    p = sp.add_parser("validate")
    p.add_argument("arquivo")
    a = ap.parse_args()
    if a.cmd == "template":
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "sample":
        print(json.dumps(SAMPLE, ensure_ascii=False, indent=2))
        return 0
    d = load(a.arquivo)
    if a.cmd == "render":
        render(d)
        return 0
    res = validate(d)
    order = {"ALERT": 0, "GAP": 1, "WARNING": 2, "NOTE": 3}
    res.sort(key=lambda x: (order[x[0]], x[1]))
    cnt = {}
    for s, *_ in res:
        cnt[s] = cnt.get(s, 0) + 1
    print("Specification validation: " + ", ".join(f"{k}={v}" for k, v in sorted(cnt.items(), key=lambda kv: order[kv[0]])))
    for s, f, m, src in res:
        print(f"- [{s}] {f}: {m}  ({src})")
    print("\nThe validator checks presence and simple coherence, not the quality of the answers. Not a security audit.")
    return 1 if cnt.get("GAP") or cnt.get("ALERT") else 0


if __name__ == "__main__":
    sys.exit(main())

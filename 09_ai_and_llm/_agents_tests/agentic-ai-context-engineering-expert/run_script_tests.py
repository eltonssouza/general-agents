# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/ai]   # --src enables the citation check
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
Fidelity note: where the text has a number (utility: 95.00 and 127.50; BAAS p.89) the test checks the text's number; where the text only gives the
definition (memory-split, CE2 p.12; weights, BAAS p.109-110) the test checks the definitional LOGIC, not a number from the text.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL = []
OK = []


def run(args, stdin_file=None):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join("scripts", "ctx_lookup.py")
    K = os.path.join("scripts", "agent_checklist.py")
    S = os.path.join("scripts", "agent_spec.py")
    C = os.path.join("scripts", "ctx_calc.py")

    # ---- lookup
    code, o = run([L, "tool calling", "--top", "2"])
    check("L01 tool calling -> ch.5 p.133-135", "04-baas-ferramentas" in o and "133-135" in o, o)
    code, o = run([L, "kv cache"])
    check("L02 kv cache -> CE2 p.18", "CE2 p.18" in o and "11-ce2" in o, o)
    code, o = run([L, "MCP"])
    check("L03 MCP -> NOT COVERED (only CE2 references)", "NOT COVERED" in o and "22, 25, 26" in o, o)
    code, o = run([L, "OWASP"])
    check("L04 OWASP -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "terraform"])
    check("L05 off-topic -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "--page", "89", "--fonte", "BAAS"])
    check("L06 BAAS p.89 -> ch.3, printed 64, utility", "printed 64" in o and "utility" in o.lower(), o)
    code, o = run([L, "--page", "12", "--fonte", "CE2"])
    check("L07 CE2 p.12 -> layered memory", "Layered memory" in o, o)
    code, o = run([L, "--printed", "64"])
    check("L08 --printed 64 -> PDF p.89", "PDF p.89" in o, o)
    code, o = run([L, "--chapters"])
    check("L09 --chapters lista BAAS 1-11 e CE2", o.count("BAAS") >= 11 and "CE2" in o and "Fundamentals of Generative AI" in o, o)
    code, o = run([L, "--gaps"])
    check("L10 --gaps lists gaps and not-read items", "NOT COVERED" in o and "NOT READ" in o and "Model Context Protocol" in o, o)
    code, o = run([L, "memory", "--json", "--fonte", "CE2"])
    try:
        j = json.loads(o)
        check("L11 --json valid and filtered by source", j["resultados"] and all(r["fonte"] == "CE2" for r in j["resultados"]), o)
    except Exception as e:
        check("L11 --json valid", False, str(e))
    code, o = run([L, "--datado"])
    check("L12 --datado lists items", "BAAS" in o and "CE2" in o and "DeepSeek" in o, o)
    code, o = run([L, "guardrails"])
    check("L13 guardrails -> ch.7 discrepancy and ch.9", "186-211" in o and "237" in o, o)
    code, o = run([L, "--page", "13", "--fonte", "BAAS"])
    check("L14 BAAS p.13 (blank) -> no mapped chapter", "no mapped chapter" in o, o)
    code, o = run([L, "RAG"])
    check("L15 RAG -> BAAS gap + CE2 result", "NOT COVERED" in o and "CE2" in o, o)
    code, o = run([L, "--page", "300", "--fonte", "BAAS"])
    check("L16 page outside the PDF", "outside the PDF" in o, o)

    # ---- checklist
    code, o = run([K, "areas"])
    check("K01 areas: 75 items, 12 areas", "total: 75 items" in o and o.count("items") >= 13, o)
    code, o = run([K, "list", "--area", "seg"])
    check("K02 list seg >= 10 items with page", o.count("[BAAS p.") >= 9 and "SEG01" in o, o)
    code, o = run([K, "list", "--fonte", "pacote"])
    check("K03 package items without page (2)", o.count("[package, no page]") == 2, o)
    code, o = run([K, "markdown", "--area", "mem"])
    check("K04 markdown", o.count("- [ ]") == 8 and "(CE2 p.12)" not in o.replace("[CE2 p.12]", "") or "[CE2 p.12]" in o, o)
    fx = os.path.join(PKG, "tests", "fixtures", "respostas-exemplo.json")
    code, o = run([K, "evaluate", fx])
    check("K05 evaluate: counts and pending items", "yes=3" in o and "no=4" in o and "partial=3" in o and "na=1" in o and "[no] TOOL03" in o, o)
    with tempfile.TemporaryDirectory() as td:
        pt = os.path.join(td, "pt.json")
        with io.open(pt, "w", encoding="utf-8") as f:
            json.dump({"ARQ01": "sim", "ARQ02": "parcial", "TOOL03": "nao", "TOOL04": "não", "TOOL07": "na"}, f)
        code, o = run([K, "evaluate", pt])
        check("K05b evaluate accepts the Portuguese answers (sim|nao|parcial|na)", "yes=1" in o and "no=2" in o and "partial=1" in o and "na=1" in o and "[no] TOOL03" in o, o)
    code, o = run([K, "list", "--area", "xx"])
    check("K06 invalid area -> exit 2", code == 2, o)
    code, o = run([K, "evaluate", os.path.join(PKG, "tests", "fixtures", "nao-existe.json")])
    check("K07 missing file -> exit 2", code == 2, o)

    # ---- spec
    code, o = run([S, "sample"])
    sample = o
    try:
        json.loads(sample)
        check("S01 sample is valid JSON", True)
    except Exception as e:
        check("S01 sample is valid JSON", False, str(e))
    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "sample.json")
        with io.open(sp, "w", encoding="utf-8") as f:
            f.write(sample)
        code, o = run([S, "validate", sp])
        check("S02 sample validate: exit 0, only NOTE", code == 0 and "NOTE=2" in o and "GAP" not in o and "ALERT" not in o, o)
        code, o = run([S, "render", sp])
        check("S03 render contains sections 1-12 with pages", "## 12. Evaluation" in o and "## 6. Tools (BAAS p.135-139; CE2 p.18-19)" in o, o)
        d = json.loads(sample)
        d["ferramentas"][1]["aprovacao_humana"] = False
        d["ferramentas"][1]["executor_valida_parametros"] = False
        d["contexto"]["orcamento_tokens"]["componentes"]["historico"] = 120000
        d["guardrails"]["rollback"] = ""
        bp = os.path.join(td, "bad.json")
        with io.open(bp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        code, o = run([S, "validate", bp])
        check("S04 high risk without approval -> ALERT (BAAS p.238-239), exit 1", code == 1 and "ALERT" in o and "238-239" in o, o)
        check("S05 executor does not validate -> ALERT (BAAS p.134-135)", "134-135" in o, o)
        check("S06 budget > window -> ALERT", "above the window" in o, o)
        check("S07 empty rollback -> GAP guardrails.rollback", "guardrails.rollback" in o and "GAP" in o, o)
        tp = os.path.join(td, "t.json")
        code, t = run([S, "template"])
        with io.open(tp, "w", encoding="utf-8") as f:
            f.write(t)
        code, o = run([S, "validate", tp])
        check("S08 blank template -> many GAP, exit 1", code == 1 and "GAP=" in o, o)
        np_ = os.path.join(td, "n.json")
        with io.open(np_, "w", encoding="utf-8") as f:
            f.write("[1,2]")
        code, o = run([S, "validate", np_])
        check("S09 non-object JSON -> exit 2", code == 2, o)
        d2 = json.loads(sample)
        d2["ferramentas"] = [{"nome": "t%d" % i, "descricao": "x", "parametros_obrigatorios": [], "risco": "baixo", "executor_valida_parametros": True, "fallback": "y"} for i in range(31)]
        mp = os.path.join(td, "many.json")
        with io.open(mp, "w", encoding="utf-8") as f:
            json.dump(d2, f, ensure_ascii=False)
        code, o = run([S, "validate", mp])
        check("S10 31 tools (Portuguese risk value) -> WARNING CE2 p.18 [DATED]", "31 tools" in o and "CE2 p.18" in o and "DATED" in o and "classify the risk" not in o, o)

    # ---- calc
    code, o = run([C, "utility", "--demo"])
    check("C01 utility --demo: 95,00 e 127,50 (BAAS p.89)", "95.00" in o and "127.50" in o and "Road Trip (127.50)" in o, o)
    code, o = run([C, "utility", "--option", "X=500,2,2", "--option", "Y=100,1,1"])
    check("C02 generic utility: X=(1000-500)*.05+20+30=75; Y=45+10+15=70", "75.00" in o and "70.00" in o and "best option: X" in o, o)
    code, o = run([C, "weights", "--weight", "budget=1", "--weight", "luxury=1", "--key", "luxury", "--feedback", "-1"])
    check("C03 weights -1 -> x0,9", "luxury         1.0000 -> 0.9000" in o and "budget         1.0000 -> 1.0000" in o, o)
    code, o = run([C, "weights", "--weight", "adventure=0.34", "--key", "adventure", "--feedback", "1"])
    check("C04 weights +1 -> x1,1 (0.34 -> 0.3740)", "0.3740" in o, o)
    code, o = run([C, "weights", "--weight", "a=1", "--key", "b", "--feedback", "1"])
    check("C05 weights unknown key -> exit 2", code == 2, o)
    code, o = run([C, "weights", "--weight", "a=1", "--key", "a", "--feedback", "2"])
    check("C06 invalid feedback -> exit 2", code == 2, o)
    code, o = run([C, "memory-split", "--theta-s", "0.5", "--theta-l", "0.6", "--item", "a=0.9,0.8", "--item", "b=0.3,0.9", "--item", "c=0.2,0.1"])
    check("C07 memory-split: a in Ms, b in Ml, c neither", "a " in o and "-> short-term (Ms)" in o and "-> long-term (Ml)" in o and "-> neither" in o, o)
    code, o = run([C, "memory-split", "--theta-s", "0.5", "--theta-l", "0.6", "--item", "e=0.5,0.9", "--item", "f=0.5,0.6"])
    lines = {l.split()[0]: l for l in o.splitlines() if l.startswith("  e") or l.startswith("  f")}
    check("C08 memory-split boundary: w_temporal == θs is not in Ms (strict); e->Ml; f (importance == θl) -> neither",
          "long-term (Ml)" in lines.get("e", "") and "neither" in lines.get("f", ""), o)
    code, o = run([C, "budget", "--window", "128000", "--component", "system=3000", "--component", "tools=9000", "--component", "history=60000",
                   "--component", "rag=20000", "--reserve-output", "4000", "--tools", "35", "--prefix", "system", "--prefix", "tools",
                   "--price-in", "3", "--price-cached", "0.3", "--price-out", "15", "--cache-hit", "0.9", "--out-tokens", "1000", "--calls", "100"])
    check("C09 budget: 92,000 tokens = 71.9%; with output 75.0%", "92,000" in o and "71.9%" in o and "75.0%" in o, o)
    check("C10 budget: 50% alert cites CE2 p.16 [DATED] and 35 tools cites CE2 p.18", "CE2 p.16" in o and "CE2 p.18" in o and "DATED" in o, o)
    check("C11 budget: cost per call 0.261840 (arithmetic checked by hand)", "0.261840" in o and "26.1840" in o, o)
    code, o = run([C, "budget", "--window", "1000", "--component", "a=900", "--reserve-output", "200"])
    check("C12 budget: input+output > window -> ERROR", "[ERROR]" in o and "100 tokens" in o, o)
    code, o = run([C, "budget", "--window", "1000", "--chars", "a=4000"])
    check("C13 --chars without --chars-per-token -> exit 2", code == 2 and "chars-per-token" in o, o)
    code, o = run([C, "budget", "--window", "1000", "--chars", "a=4001", "--chars-per-token", "4"])
    check("C14 --chars with the user's ratio: ceil(4001/4)=1001 tokens", "1,001" in o or "1001" in o, o)
    code, o = run([C, "budget", "--window", "-5", "--component", "a=1"])
    check("C15 negative window -> exit 2", code == 2, o)
    code, o = run([C, "budget", "--window", "1000", "--component", "a=100", "--prefix", "zzz"])
    check("C16 unknown prefix -> exit 2", code == 2, o)
    code, o = run([C, "budget", "--window", "1000", "--component", "a=100", "--tools", "120"])
    check("C17 120 tools -> >100 alert (CE2 p.18)", "near-certain failure" in o and "CE2 p.18" in o, o)
    with tempfile.TemporaryDirectory() as td:
        cp = os.path.join(td, "cfg.json")
        with io.open(cp, "w", encoding="utf-8") as f:
            json.dump({"window": 2000, "components": {"x": 500, "y": 500}, "warn_fill": 0.4, "prefix": ["x"]}, f)
        code, o = run([C, "budget", "--config", cp])
        check("C18 --config: 1000/2000 = 50% > threshold 40%", "50.0%" in o and "threshold 40%" in o, o)

    # ---- package consistency
    must = ["agents/agentic-ai-context-engineering-expert.md", "README.md", "AGENTS.md", ".claude-plugin/plugin.json",
            ".github/agents/agentic-ai-context-engineering-expert.agent.md", "references/INDEX.md", "references/glossario.md",
            "references/procedimentos.md", "references/casos-e-antipadroes.md", "references/datado.md", "tests/casos-de-teste.md",
            "tests/relatorio-de-fidelidade.md", "tests/verify_citations.py", "tests/citation-checks.json"]
    miss = [m for m in must if not os.path.exists(os.path.join(PKG, m))]
    check("P01 required files present", not miss, str(miss))
    agent = io.open(os.path.join(PKG, "agents", "agentic-ai-context-engineering-expert.md"), encoding="utf-8").read()
    refs = sorted(os.listdir(os.path.join(PKG, "references")))
    check("P02 the agent cites each topic reference by file name", all(r in agent for r in refs if r.endswith(".md")), str([r for r in refs if r not in agent]))
    for s in ("ctx_lookup.py", "agent_checklist.py", "agent_spec.py", "ctx_calc.py"):
        check(f"P03 agent cites {s}", s in agent, s)
    check("P04 plugin.json is valid JSON", bool(json.load(io.open(os.path.join(PKG, ".claude-plugin", "plugin.json"), encoding="utf-8"))))
    casos = io.open(os.path.join(PKG, "tests", "casos-de-teste.md"), encoding="utf-8").read()
    ncasos = sum(1 for l in casos.splitlines() if l.startswith("| C") and l.split("|")[1].strip().startswith("C"))
    check("P05 casos-de-teste.md with >= 20 cases", ncasos >= 20, str(ncasos))

    if a.src:
        code, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("V01 verify_citations: 0 failures", code == 0, o)
        print(o.strip().splitlines()[-1])

    print(f"\nSummary: {len(OK)} passed, {len(FAIL)} failed.")
    if FAIL:
        print("Failures: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

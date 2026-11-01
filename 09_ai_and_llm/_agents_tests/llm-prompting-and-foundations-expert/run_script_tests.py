# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/ai]   # --src enables the citation verification
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
The expected numeric values come from the LLMS pages (p.4, 25-27, 43, 81-84, 86) or from computations done here with math.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-X", "utf8", "-I"]
FAIL = []
OK = []


def run(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + str(detail)[:500]))


def jrun(args):
    """llm_calc.py accepts --json BEFORE the subcommand."""
    code, o = run([args[0], "--json"] + args[1:])
    return code, o


def approx(a, b, rel=1e-6):
    return abs(a - b) <= rel * max(1.0, abs(b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join("scripts", "llm_lookup.py")
    S = os.path.join("scripts", "prompt_technique_selector.py")
    C = os.path.join("scripts", "llm_calc.py")

    # ---------------- lookup
    code, o = run([L, "chinchilla"])
    check("L01 chinchilla -> ref 04 p.4-5", "04-llms-fundamentos" in o and "p.4-5" in o, o)
    code, o = run([L, "top-p"])
    check("L02 top-p -> ref 06 p.26-27", "06-llms-arquitetura" in o and "p.26-27" in o, o)
    code, o = run([L, "LoRA", "--top", "2"])
    check("L03 LoRA -> ref 07 p.43-44", "07-llms-adaptacao" in o and "p.43-44" in o, o)
    code, o = run([L, "prompt injection"])
    check("L04 prompt injection -> NOT COVERED (rc 2)", code == 2 and "NOT COVERED" in o, o)
    code, o = run([L, "terraform"])
    check("L05 off-topic term -> NOT COVERED", code == 2 and "NOT COVERED" in o, o)
    code, o = run([L, "--page", "4", "--source", "LLMS"])
    check("L06 --page 4 LLMS -> scaling laws", "Scaling laws" in o, o)
    code, o = run([L, "--page", "120", "--source", "LLMS"])
    check("L07 --page 120 LLMS -> REFERENCES", "REFERENCES" in o, o)
    code, o = run([L, "--page", "10", "--source", "PES"])
    check("L08 --page 10 PES -> Table 1", "Table 1" in o, o)
    code, o = run([L, "--page", "150", "--source", "LLMS"])
    check("L09 --page 150 LLMS out of range (rc 2)", code == 2, o)
    code, o = run([L, "--sections", "--source", "LLMS"])
    check("L10 --sections LLMS lists sections 1..10 and REF", all(f"{n}:" in o for n in ("1", "5", "9", "10", "REF")), o)
    code, o = run([L, "--gaps"])
    check("L11 --gaps lists gaps", "prompt injection" in o and "MCP" in o and "references" in o.lower(), o)
    code, o = run([L, "--datado"])
    check("L12 --datado cita v19", "v19" in o and "2026" in o, o)
    code, o = run([L, "chinchilla", "--json"])
    try:
        j = json.loads(o)
        check("L13 --json valid", j["resultados"] and j["resultados"][0]["ref"].startswith("references/04-"), o)
    except Exception as e:
        check("L13 --json valid", False, str(e))
    code, o = run([L, "tree of thoughts"])
    check("L14 tree of thoughts -> PES p.4", "PES p.4" in o, o)
    code, o = run([L, "Model Context Protocol"])
    check("L15 MCP -> NOT COVERED", code == 2 and "NOT COVERED" in o, o)

    # ---------------- selector
    code, o = run([S, "--list"])
    check("S01 --list brings 41 techniques", "Total: 41" in o and o.count("[id:") == 41, o[-200:])
    code, o = run([S, "--categories"])
    check("S02 --categories brings 12 areas", o.count("§2.") == 12, o)
    code, o = run([S, "--need", "matematica", "--top", "60", "--brief"])
    check("S03 matematica includes cot, pot, step-back", all(k in o for k in ("[id: cot]", "[id: pot]", "[id: step-back]")), o)
    code, o = run([S, "--need", "alucinacao", "--no-external", "--top", "60", "--brief"])
    check("S04 alucinacao without external resource excludes RAG and ReAct", "[id: rag]" not in o and "[id: react]" not in o and "[id: cove]" in o, o)
    code, o = run([S, "--show", "cot"])
    check("S05 --show cot -> 90.2% and PES p.2", "90.2%" in o and "PES p.2" in o, o)
    code, o = run([S, "--compare", "cot", "tot"])
    check("S06 --compare warns not comparable", "NOT directly comparable" in o or "NOT comparable" in o, o)
    code, o = run([S, "--show", "inexistente"])
    check("S07 nonexistent technique -> NOT COVERED (rc 2)", code == 2 and "NOT COVERED" in o, o)
    code, o = run([S, "--tips", "--principle", "2"])
    check("S08 --tips --principle 2 brings C1 and p.47", "C1 " in o and "LLMS p.47" in o, o)
    code, o = run([S, "--need", "xyz"])
    check("S09 unknown criterion -> rc 2", code == 2, o)
    code, o = run([S, "--need", "matematica", "--turn", "single", "--top", "60", "--brief"])
    check("S10 --turn single brings only Single", "turns: Multi" not in o and "turns: Single" in o, o)
    code, o = run([S, "--need", "alucinacao", "--acq", "Retrieval Based", "--top", "60", "--brief"])
    check("S11 --acq filters prompt acquisition", "prompt acquisition: Manual" not in o and "[id: rag]" in o, o)
    try:
        d = json.load(open(os.path.join(PKG, "scripts", "pes_techniques.json"), encoding="utf-8"))
        T = d["tecnicas"]
        ids = [t["id"] for t in T]
        check("S12 JSON: 41 techniques, unique ids, each with a page", len(T) == 41 and len(set(ids)) == 41 and all(t["pages"] and t["table_page"] == 10 for t in T), len(T))
        secs = {t["section"] for t in T}
        check("S13 JSON: 12 sections 2.1-2.12", secs == {f"2.{i}" for i in range(1, 13)}, secs)
        check("S14 JSON: valid acquisition and turn", all(t["acquisition"] in ("Manual", "LM Generated", "Retrieval Based", "Hybrid") and t["turn"] in ("Single", "Multi") for t in T), "")
    except Exception as e:
        check("S12 JSON techniques", False, str(e))

    # ---------------- selector fixtures
    try:
        fx = json.load(open(os.path.join(PKG, "tests", "fixtures", "exemplos-selector.json"), encoding="utf-8"))
        for i, case in enumerate(fx["casos"], 1):
            code, o = run([S] + case["args"] + ["--top", "60", "--brief"])
            miss = [t for t in case["devem_aparecer"] if f"[id: {t}]" not in o]
            check(f"S{14 + i} selector fixture {' '.join(case['args'][:2])}", not miss, miss)
    except Exception as e:
        check("S15 selector fixtures", False, str(e))

    # ---------------- calc
    code, o = jrun([C, "scaling-kaplan", "--N", "1e9"])
    check("C01 Kaplan L(N=1e9) = (8.8e13/1e9)^0.076", approx(json.loads(o)["L(N)"], (8.8e13 / 1e9) ** 0.076, 1e-9), o)
    code, o = jrun([C, "scaling-chinchilla", "--N", "70e9", "--D", "1.4e12"])
    exp = 1.69 + 406.4 / (70e9) ** 0.34 + 410.7 / (1.4e12) ** 0.28
    check("C02 Chinchilla L(70B,1.4T) pela Eq.2", approx(json.loads(o)["L(N,D)"], exp, 1e-9), o)
    code, o = jrun([C, "chinchilla-allocation", "--C", "5.76e23"])
    j = json.loads(o)
    Nopt = j["Nopt_(derived a)"]
    Nnum = j["numerical_check_argmin_N (sweep of L(N,C/6N))"]
    check("C03 derived Nopt matches the numerical argmin (1%)", abs(Nopt - Nnum) / Nnum < 0.01, (Nopt, Nnum))
    check("C04 printed exponent does not reproduce the optimum (difference > 10x)", j["Nopt_with_printed_a (not recommended)"] / Nnum > 10, j["Nopt_with_printed_a (not recommended)"])
    check("C05 ALERT about a/b present", "ALERT" in j and "G" in j, "")
    code, o = jrun([C, "compute", "--N", "70e9", "--D", "1.4e12"])
    check("C06 compute 6ND", approx(json.loads(o)["C_flops"], 6 * 70e9 * 1.4e12, 1e-12), o)
    code, o = jrun([C, "rope", "--d", "128", "--i", "1"])
    j = json.loads(o)
    check("C07 RoPE i=1: theta=1, lambda=2pi", approx(j["theta_i"], 1.0) and approx(j["lambda_i"], 2 * math.pi), o)
    code, o = jrun([C, "rope", "--d", "128", "--i", "64"])
    check("C08 RoPE i=64: theta=10000^(-126/128)", approx(json.loads(o)["theta_i"], 10000 ** (-126 / 128), 1e-9), o)
    probs = ["0.661", "0.119", "0.057", "0.017", "0.012", "0.008", "0.008"]
    labs = ["coffee", "water", "tea", "rice", "chai", "strong", "black"]
    code, o = jrun([C, "sampling", "--probs"] + probs + ["--labels"] + labs + ["--top-k", "5"])
    j = json.loads(o)
    check("C09 top-5 of Fig.10 = coffee,water,tea,rice,chai (LLMS p.27)", set(j["final_distribution"]) == {"coffee", "water", "tea", "rice", "chai"} and j["greedy(argmax)"] == "coffee", o)
    code, o = jrun([C, "sampling", "--probs"] + probs + ["--labels"] + labs + ["--temperature", "0.01"])
    check("C10 t->0 is equivalent to greedy", json.loads(o)["final_distribution"].get("coffee", 0) > 0.999, o)
    code, o = jrun([C, "sampling", "--probs"] + probs + ["--labels"] + labs + ["--top-p", "0.9"])
    check("C11 top-p 0.9 keeps coffee,water,tea", set(json.loads(o)["final_distribution"]) == {"coffee", "water", "tea"}, o)
    code, o = jrun([C, "sampling", "--probs"] + probs + ["--labels"] + labs + ["--temperature", "1"])
    j = json.loads(o)["final_distribution"]
    check("C12 t=1 preserves the probability ratios", approx(j["water"] / j["coffee"], 0.119 / 0.661, 1e-5), o)
    code, o = jrun([C, "train-states", "--params", "6.7e9"])
    s = o
    check("C13 16P for LLaMA-7B ~100GB (LLMS p.81)", "99.84 GiB" in s and "1.0720e+11" in s, s)
    code, o = jrun([C, "train-activations"])
    j = json.loads(o)
    check("C14 Tab.18 sums to ~17.29 GiB (does not reproduce exactly 16GB)", 17.2 < j["total_GiB"] < 17.4 and "17.3" in j["note"], o)
    code, o = jrun([C, "arithmetic-intensity", "--phase", "prefill"])
    j = json.loads(o)
    check("C15 prefill: linear layers 2730.67, attention 114.67 (LLMS p.83)", j["I_1_QKV_linear"] == 2730.67 and j["I_3_attention"] == 114.67, o)
    check("C16 Imax A100 = 142.51 (LLMS p.83)", j["Imax_FLOP_per_byte"] == 142.51, o)
    code, o = jrun([C, "arithmetic-intensity", "--phase", "decode"])
    j = json.loads(o)
    check("C17 decoding: linear layers < 8 and everything memory-bound (LLMS p.83)", j["I_1_QKV_linear"] < 8 and all(v == "memory-bound" for v in j["classification"].values()), o)
    code, o = jrun([C, "arithmetic-intensity", "--phase", "prefill", "--decimal-gb"])
    check("C18 Imax with decimal GB = 153.02", json.loads(o)["Imax_FLOP_per_byte"] == 153.02, o)
    code, o = jrun([C, "lora", "--m", "4096", "--n", "4096", "--k", "16"])
    j = json.loads(o)
    check("C19 LoRA k(m+n)", j["trainable_parameters_k(m+n)"] == 16 * 8192 and approx(j["ratio"], 131072 / 16777216), o)
    code, o = jrun([C, "quantize", "--x", "0.5", "-0.26", "--S", "0.1"])
    r = json.loads(o)["results"]
    check("C20 quantize: 0.5->5, -0.26->-3 (rounds to nearest)", r[0]["xq"] == 5 and r[1]["xq"] == -3 and abs(r[0]["error"]) < 1e-9, o)
    code, o = jrun([C, "smoothquant", "--xmax", "4", "--wmax", "1", "--alpha", "0.5"])
    check("C21 SmoothQuant s=2", approx(json.loads(o)["s"][0], 2.0), o)
    code, o = jrun([C, "pass-at-k", "--results", "0", "0", "1"])
    check("C22 pass@k = 1 if any passes", json.loads(o)["pass@k"] == 1, o)
    code, o = jrun([C, "pass-at-k", "--results", "0", "0"])
    check("C23 pass@k = 0 if none passes", json.loads(o)["pass@k"] == 0, o)
    code, o = jrun([C, "majority-vote", "--answers", "18", "9", "9", "9", "18"])
    check("C24 majority vote", json.loads(o)["winner"] == "9", o)
    code, o = jrun([C, "weights-memory", "--params", "6.7e9", "--bits", "16"])
    check("C25 16-bit weights of 6.7B ~12.48 GiB (compares Tab.21 12.58)", abs(json.loads(o)["GiB"] - 12.48) < 0.02, o)
    code, o = jrun([C, "wordpiece-score", "--pair-count", "10", "--a-count", "20", "--b-count", "5"])
    check("C26 WordPiece score = 10/(20*5)", approx(json.loads(o)["score"], 0.1), o)


    # ---------------- rubrics: the references contain what the conceptual cases require
    # (the terms below are looked up in the English reference files under references/)
    RUBRIC = [
        ("C01", "08-llms-utilizacao-prompting-icl-cot-planejamento.md", ["without gradient updates", "LLMS p.50", "instruction tuning"]),
        ("C02", "04-llms-fundamentos-scaling-emergencia-gpt.md", ["ICL", "instruction following", "step-by-step", "68B", "62B", "LLMS p.5-6"]),
        ("C03", "04-llms-fundamentos-scaling-emergencia-gpt.md", ["KM", "Chinchilla", "C≈6ND", "406.4", "does not give the formula for G"]),
        ("C04", "08-llms-utilizacao-prompting-icl-cot-planejamento.md", ["≥10B", "MNLI", "no public ablation"]),
        ("C05", "07-llms-adaptacao-instrucao-alinhamento-peft.md", ["behavior cloning", "hallucination", "subjective"]),
        ("C06", "03-pes-alucinacao-codigo-otimizacao-e-demais.md", ["four steps", "verification questions"]),
        ("C07", "08-llms-utilizacao-prompting-icl-cot-planejamento.md", ["task recognition", "task learning", "66B"]),
        ("C08", "12-llms-rag-alucinacao-raciocinio-longo-e-conclusao.md", ["context retrieval", "prompt construction", "generation"]),
        ("P02", "12-llms-rag-alucinacao-raciocinio-longo-e-conclusao.md", ["SelfCheckGPT", "high temperature", "RARR"]),
        ("P05", "08-llms-utilizacao-prompting-icl-cot-planejamento.md", ["Four ingredients", "Five design principles", "Tab. 12"]),
        ("B01", "01-pes-visao-geral-e-taxonomia.md", ["provides no side-by-side comparison", "invalid"]),
        ("B02", "casos-e-antipadroes.md", ["a=α/(α+β)", "β/(α+β)"]),
        ("B03", "11-llms-topicos-avancados-contexto-agentes-eficiencia.md", ["17.3 GiB", "16GB"]),
        ("B04", "datado.md", ["MMLU 86.4%", "Mar 2026"]),
        ("F01", "../scripts/llm_index.json", ["prompt injection"]),
    ]
    for cid, fn, terms in RUBRIC:
        try:
            txt = open(os.path.join(PKG, "references", fn), encoding="utf-8").read()
        except Exception as e:
            check("R " + cid + " " + fn, False, str(e))
            continue
        miss = [t for t in terms if t not in txt]
        check("R " + cid + " reference contains the criteria", not miss, miss)

    # ---------------- citations
    if a.src:
        code, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("V01 verify_citations passes (0 failures)", code == 0 and "total failures: 0" in o, o[-600:])
        m = re.search(r"Checks: (\d+) positive, (\d+) negative", o)
        check("V02 >=60 positive and >=15 negative", bool(m) and int(m.group(1)) >= 60 and int(m.group(2)) >= 15, o[-300:])

    print(f"\nPASS {len(OK)} / FAIL {len(FAIL)}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

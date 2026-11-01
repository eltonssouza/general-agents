# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/ai]   # --src also runs verify_citations.py
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
The numerical examples come from book pages when indicated (DLB p.N, PDF page).
"""
import argparse
import json
import math
import os
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL = []
OK = []


def run(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def J(cmd, *a):
    code, o = run([os.path.join("scripts", cmd)] + list(a) + ["--json"])
    try:
        return json.loads(o)
    except Exception:
        return {"_erro": o}


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join("scripts", "dlb_lookup.py")
    C = "dlb_calc.py"
    D = os.path.join("scripts", "dlb_diagnose.py")

    # ---------------- lookup
    code, o = run([L, "dropout", "--top", "1"])
    check("L01 dropout -> 04-regularizacao p.273-283", "04-regularizacao.md" in o and "273-283" in o, o)
    code, o = run([L, "adam", "--top", "1"])
    check("L02 adam -> 05-otimizacao p.321-326", "05-otimizacao.md" in o and "321-326" in o, o)
    code, o = run([L, "transformer"])
    check("L03 transformer -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "LoRA"])
    check("L04 LoRA -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "terraform"])
    check("L05 off-topic -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "--page", "436"])
    check("L06 --page 436 -> Cap.11, printed 421, read", "Cap.11" in o and "printed 421" in o and "page READ by this package" in o, o)
    code, o = run([L, "--page", "600"])
    check("L07 --page 600 -> page NOT READ", "NOT READ" in o, o)
    code, o = run([L, "--printed", "74"])
    check("L08 --printed 74 -> PDF p.89", "PDF p.89" in o, o)
    code, o = run([L, "--chapters"])
    check("L09 --chapters lists 20 chapters", o.count("Cap.") >= 20, o)
    code, o = run([L, "--chapter", "11"])
    check("L10 --chapter 11 lists topics", o.count("DLB p.") >= 6, o)
    code, o = run([L, "--gaps"])
    check("L11 --gaps lists gaps and unread", "Transformer" in o and "NOT READ" in o.upper() and "151-165" in o, o)
    code, o = run([L, "batch normalization", "--json"])
    try:
        j = json.loads(o)
        check("L12 --json valid", j["resultados"] and j["resultados"][0]["ref"].startswith("05-"), o)
    except Exception as e:
        check("L12 --json valid", False, str(e))
    code, o = run([L, "--datado"])
    check("L13 --datado reads the file", "[DATED]" in o, o)
    code, o = run([L, "--page", "44"])
    check("L14 --page 44 -> Part opener/outside chapters", "outside the mapped chapters" in o, o)
    code, o = run([L, "GAN", "--top", "1"])
    check("L15 GAN -> cap.20 p.714-719", "714-719" in o, o)

    # ---------------- calc: convolution and counting (DLB p.355, 364)
    j = J(C, "conv-out", "--m", "16", "--k", "6")
    check("C01 valid m=16,k=6 -> 11 (p.364)", j.get("saida") == 11, str(j))
    j = J(C, "conv-out", "--m", "16", "--k", "6", "--pad", "full")
    check("C02 full -> m+k-1 = 21", j.get("saida") == 21, str(j))
    j = J(C, "conv-out", "--m", "16", "--k", "6", "--pad", "same")
    check("C03 same -> 16", j.get("saida") == 16, str(j))
    j = J(C, "conv-cost")
    check("C04 Fig 9.6: 267,960 ops (p.355)", j.get("ops_conv") == 267960, str(j))
    check("C05 Fig 9.6: >8 billion entries and ~4e9 / ~6e4 ratio", j.get("entradas_densa", 0) > 8e9 and 3.9e9 < j.get("razao_armazenamento", 0) < 4.1e9 and 5.9e4 < j.get("razao_ops", 0) < 6.0e4, str(j))
    check("C06 Fig 9.6: 178,640 non-zeros", j.get("nao_nulos") == 178640, str(j))
    j = J(C, "params", "--kind", "mlp", "--layers", "784,100,10", "--bias")
    check("C07 MLP 784-100-10 -> 79,510 parameters", j.get("params") == 79510, str(j))
    j = J(C, "params", "--kind", "conv", "--cin", "3", "--cout", "16", "--kh", "3", "--kw", "3", "--bias")
    check("C08 conv 3->16, 3x3 -> 432 weights + 16 biases = 448", j.get("params") == 448, str(j))

    # ---------------- information (DLB p.88-90)
    j = J(C, "info", "--p", "0.5,0.5")
    check("C09 H(0.5;0.5) = ln 2 (Fig 3.5, p.90)", close(j["H_P"], math.log(2)), str(j))
    j = J(C, "info", "--p", "0.9,0.1", "--q", "0.5,0.5", "--base", "2")
    check("C10 CE = H + KL (eq 3.51)", close(j["CE_PQ"], j["H_P"] + j["KL_PQ"], 1e-12), str(j))
    check("C11 KL asymmetric", abs(j["KL_PQ"] - j["KL_QP"]) > 0.1, str(j))
    j = J(C, "info", "--p", "1,0")
    check("C12 convention 0 log 0 = 0", close(j["H_P"], 0.0), str(j))
    j = J(C, "softmax", "--z", "1000,1000,1000")
    check("C13 stable softmax with z=1000: 1/3 each (p.96)", all(close(x, 1 / 3) for x in j["softmax"]) and isinstance(j["ingenuo"], str), str(j))
    j = J(C, "softmax", "--z=-1000,-1000")
    check("C14 stable log-softmax with z=-1000: -log 2", all(close(x, -math.log(2)) for x in j["log_softmax"]), str(j))

    # ---------------- XOR and backprop (DLB p.189-191, 225, 454)
    j = J(C, "xor")
    check("C15 XOR [0,1,1,0] (p.191)", j.get("saidas") == [0, 1, 1, 0], str(j))
    j = J(C, "autodiff", "--expr", "mul(add(x,y),x)", "--vars", "x=2,y=3")
    check("C16 autodiff (x+y)x em (2,3): df/dx = 7, df/dy = 2", close(j["grad"]["x"], 7.0) and close(j["grad"]["y"], 2.0) and close(j["valor"], 10.0), str(j))
    check("C17 numerical gradient agrees", abs(j["grad_numerico"]["x"] - 7.0) < 1e-6, str(j))
    j = J(C, "autodiff", "--expr", "tanh(mul(w,x))", "--vars", "w=0.5,x=2")
    th = math.tanh(1.0)
    check("C18 autodiff tanh(wx): d/dw = x(1-tanh^2)", close(j["grad"]["w"], 2 * (1 - th * th)), str(j))
    # a variable used twice sums the paths (chain rule, p.222-225)
    j = J(C, "autodiff", "--expr", "mul(x,x)", "--vars", "x=3")
    check("C19 reused variable: d(x*x)/dx = 6", close(j["grad"]["x"], 6.0), str(j))
    j = J(C, "grad-mlp", "--layers", "3,4,2", "--act", "tanh", "--loss", "ce", "--seed", "1")
    check("C20 grad-mlp tanh+CE: backprop = centered difference", j.get("ok") is True, str(j))
    j = J(C, "grad-mlp", "--layers", "2,5,5,3", "--act", "relu", "--loss", "ce", "--seed", "2")
    check("C21 grad-mlp deep relu", j.get("ok") is True, str(j))
    j = J(C, "grad-mlp", "--layers", "3,4,2", "--act", "sigmoid", "--loss", "mse", "--seed", "3")
    check("C22 grad-mlp sigmoid+MSE", j.get("ok") is True, str(j))

    # ---------------- metrics and statistics (DLB p.138-146, 271, 438-439)
    j = J(C, "metrics", "--tp", "0", "--fp", "0", "--fn", "1", "--tn", "999999")
    check("C23 rare disease: accuracy 99.9999% and recall 0 (p.438)", close(j["accuracy"], 0.999999) and j["recall"] == 0.0, str(j))
    j = J(C, "metrics", "--tp", "8", "--fp", "2", "--fn", "4")
    check("C24 F = 2pr/(p+r)", close(j["F"], 2 * 0.8 * (8 / 12) / (0.8 + 8 / 12)), str(j))
    j = J(C, "metrics", "--answered", "95", "--total", "100", "--correct", "93")
    check("C25 coverage 0.95 (p.439)", close(j["coverage"], 0.95), str(j))
    j = J(C, "ci", "--mean", "0.1", "--std", "0.3", "--m", "100")
    check("C26 SE = sigma/sqrt(m) and 95% CI (p.143)", close(j["se"], 0.03) and close(j["ic95"][0], 0.1 - 1.96 * 0.03), str(j))
    j = J(C, "variance", "--values", "1,2,3,4")
    check("C27 variance 1/m = 1.25 and 1/(m-1) = 5/3 (p.141-142)", close(j["biased"], 1.25) and close(j["unbiased"], 5 / 3), str(j))
    j = J(C, "ensemble", "--k", "5", "--v", "1", "--c", "0")
    check("C28 uncorrelated ensemble = v/k (p.271)", close(j["erro"], 0.2), str(j))
    j = J(C, "ensemble", "--k", "5", "--v", "1", "--c", "1")
    check("C29 correlated ensemble = v (p.271)", close(j["erro"], 1.0), str(j))

    # ---------------- optimization (DLB p.309-326, 429)
    j = J(C, "lr-schedule", "--eps0", "0.1", "--epst", "0.001", "--tau", "100", "--k", "50")
    check("C30 linear decay (8.14): k=50 -> 0.0505", close(j["eps"], 0.0505), str(j))
    j = J(C, "momentum", "--alpha", "0.9")
    check("C31 alpha=0.9 -> factor 10 (p.313)", close(j["fator"], 10.0), str(j))
    j = J(C, "optim", "--algo", "sgd", "--x0", "1", "--curv", "1", "--lr", "0.1", "--steps", "1")
    check("C32 SGD: x1 = 0,9", close(j["final_x"][0], 0.9), str(j))
    j = J(C, "optim", "--algo", "momentum", "--x0", "1", "--curv", "1", "--lr", "0.1", "--alpha", "0.9", "--steps", "2")
    # v1=-0.1 ; x1=0.9 ; g=0.9 ; v2=0.9*-0.1-0.09=-0.18 ; x2=0.72
    check("C33 momentum 2 steps: x = 0.72", close(j["final_x"][0], 0.72), str(j))
    j = J(C, "optim", "--algo", "adam", "--x0", "1", "--curv", "2", "--lr", "0.001", "--steps", "1")
    # t=1: s^=g, r^=g^2 -> dx = -eps*g/(|g|+delta) ~ -0.001
    check("C34 Adam 1st step = -eps*sign(g) (Alg 8.7)", abs(j["final_x"][0] - (1 - 0.001)) < 1e-8, str(j))
    j = J(C, "optim", "--algo", "adagrad", "--x0", "1", "--curv", "1", "--lr", "0.1", "--delta", "1e-7", "--steps", "1")
    check("C35 AdaGrad 1st step ~ x - eps", abs(j["final_x"][0] - 0.9) < 1e-5, str(j))
    j = J(C, "optim", "--algo", "rmsprop", "--x0", "1", "--curv", "1", "--lr", "0.1", "--rho", "0.9", "--delta", "1e-6", "--steps", "1")
    # r=0.1 ; dx=-0.1/sqrt(0.1+1e-6)
    check("C36 RMSProp 1st step", close(j["final_x"][0], 1 - 0.1 / math.sqrt(0.1 + 1e-6), 1e-9), str(j))
    j = J(C, "clip", "--g", "3,4", "--v", "1")
    check("C37 clipping: ||g||=5 -> g' = (0.6; 0.8) (10.48-10.49)", close(j["g"][0], 0.6) and close(j["g"][1], 0.8) and j["clipado"], str(j))
    j = J(C, "clip", "--g", "0.3,0.4", "--v", "1")
    check("C38 clipping below the threshold: unchanged", (not j["clipado"]) and j["g"] == [0.3, 0.4], str(j))
    j = J(C, "init", "--m", "100", "--n", "50")
    check("C39 Glorot sqrt(6/150) = 0.2 and 1/sqrt(100) = 0.1 (p.318)", close(j["limite_glorot"], 0.2) and close(j["limite_1_sqrt_m"], 0.1), str(j))
    j = J(C, "bn", "--h", "1,2,3,4")
    check("C40 batch norm: mean 0 and variance ~1 (p.334)", abs(sum(j["normalizado"])) < 1e-9 and abs(sum(x * x for x in j["normalizado"]) / 4 - 1) < 1e-6, str(j))
    j = J(C, "gcn", "--pixels", "1,3", "--s", "1")
    check("C41 GCN: (1,3) -> (-1,1) with lambda=0 (12.3)", close(j["saida"][0], -1.0) and close(j["saida"][1], 1.0), str(j))
    j = J(C, "earlystop", "--val", "0.5,0.4,0.35,0.36,0.37,0.38,0.2", "--patience", "3")
    check("C42 early stopping: i*=3, stops at 6 (Alg 7.1)", j["i_star"] == 3 and j["parou_em"] == 6, str(j))
    j = J(C, "search", "--m", "4", "--n", "5", "--trials", "3", "--seed", "0")
    check("C43 grid = n^m = 625 and log-uniform samples in [1e-5,1e-1]", j["grid"] == 625 and all(1e-5 <= x <= 1e-1 for x in j["amostras"]), str(j))
    j = J(C, "condition", "--eigs", "1,5")
    check("C44 condition number 5 (Fig 4.6) and eps* = 1/lambda_max", close(j["cond"], 5.0) and close(j["eps_star_pior_caso"], 0.2), str(j))
    j = J(C, "linadv", "--w", "1,-2,3", "--eps", "0.01")
    check("C45 eps*||w||_1 = 0.06 (p.284)", close(j["max_mudanca"], 0.06), str(j))
    j = J(C, "dropout", "--w", "2,4", "--p", "0.5")
    check("C46 weight scaling p=0.5 -> weights/2 (p.278)", j["pesos"] == [1.0, 2.0], str(j))

    # ---------------- recurrent (DLB p.396, 425-426)
    j = J(C, "rnn")
    h1 = math.tanh(1.0)
    h2 = math.tanh(0.5 * h1 + 1.0)
    check("C47 RNN h1 = tanh(1), h2 = tanh(0.5 h1 + 1) (10.8-10.9)", close(j["passos"][0]["h"][0], h1) and close(j["passos"][1]["h"][0], h2), str(j))
    check("C48 RNN yhat sums to 1", close(sum(j["passos"][0]["yhat"]), 1.0), str(j))
    j = J(C, "lstm", "--s", "1")
    check("C49 LSTM with zero parameters and s(t-1)=1: f=g=q=0.5; s = 0.5*1 + 0.5*0.5 = 0.75; h = 0.5 tanh(0.75) (10.41, 10.43)", close(j["s"], 0.75) and close(j["h"], 0.5 * math.tanh(0.75)), str(j))
    j = J(C, "lstm", "--s", "1", "--bf", "50")
    check("C50 forget gate saturated at 1 (high bias) preserves the state", j["f"] > 0.999 and close(j["s"], 1.0 * j["f"] + j["g"] * 0.5, 1e-9), str(j))

    j = J(C, "rnn", "--params", os.path.join("tests", "fixtures", "rnn-params.json"))
    check("C55 RNN with JSON: W=0, U=I -> h = tanh(x) (10.8-10.9)", close(j["passos"][0]["h"][0], math.tanh(0.5)) and close(j["passos"][0]["h"][1], math.tanh(-0.5)), str(j))

    # ---------------- regression and kfold (DLB p.124, 138)
    j = J(C, "normal-eq", "--x", "1,2,3", "--y", "2,4,6")
    check("C51 normal equations: y=2x -> w=2", close(j["w"][0], 2.0) and j["mse"] < 1e-12, str(j))
    j = J(C, "normal-eq", "--x", "1,2,3,4", "--y", "3,5,7,9", "--bias")
    check("C52 normal equations with bias: y=2x+1", close(j["w"][0], 2.0) and close(j["w"][1], 1.0), str(j))
    j = J(C, "kfold", "--n", "7", "--k", "3")
    allidx = sorted(i for f in j["folds"] for i in f)
    check("C53 k-fold: exclusive and complete partition (Alg 5.1)", allidx == list(range(7)), str(j))

    # ---------------- activations (DLB p.208-212)
    j = J(C, "activations", "--z=-1,0,2")
    r = j["linhas"]
    check("C54 ReLU(-1)=0, ReLU(2)=2; tanh = 2 sigmoid(2z)-1 (p.210)", r[0]["relu"] == 0 and r[2]["relu"] == 2 and all(close(x["tanh"], x["tanh_ident"], 1e-12) for x in r), str(j))

    # ---------------- diagnosis (DLB ch. 11)
    code, o = run([D, "--train-error", "0.01", "--test-error", "0.12", "--target", "0.05", "--json"])
    j = json.loads(o)
    check("D01 good training, bad test -> gap (overfitting), path goes through 'gap'", "gap" in j["caminho"] and "overfitting" in j["classificacao"].lower(), o)
    code, o = run([D, "--train-error", "0.2", "--test-error", "0.21", "--target", "0.05", "--json"])
    j = json.loads(o)
    check("D02 training and test both high and close -> underfitting/data/bug, path 'subajuste'", "subajuste" in j["caminho"], o)
    code, o = run([D, "--train-error", "0.02", "--test-error", "0.03", "--target", "0.05", "--json"])
    j = json.loads(o)
    check("D03 targets met -> 'pronto'", "pronto" in j["caminho"], o)
    code, o = run([D, "--train-error", "0.2", "--test-error", "0.3", "--target", "0.05", "--bayes-error", "0.1"])
    check("D04 target below the Bayes error -> warning (p.437)", "Bayes" in o, o)
    code, o = run([D, "--tree"])
    check("D05 --tree prints the tree with pages", "DLB p.441" in o and "DLB p.442" in o and "subajuste" in o, o)
    code, o = run([D, "--debug"])
    check("D06 --debug lists 7 tests with pages 452-455", sum(1 for l in o.splitlines() if l[:2] in ("1.","2.","3.","4.","5.","6.","7.")) == 7 and "454" in o, o)
    code, o = run([D, "--hyper"])
    check("D07 --hyper: Table 11.1 (p.446) has 6 hyperparameters", "446" in o and o.count("capacity") >= 6, o)
    code, o = run([D, "--baseline", "sequence"])
    check("D08 sequence baseline: LSTM or GRU (p.440)", "LSTM" in o and "GRU" in o and "440" in o, o)
    code, o = run([D, "--lr-state", "diverges"])
    check("D09 high learning rate (p.444)", "444" in o, o)
    tree = json.load(open(os.path.join(PKG, "scripts", "dlb_tree.json"), encoding="utf-8"))
    pgs = [ac["pag"] for n in tree["nos"].values() for ac in n.get("acoes", [])]
    nums = []
    for p in pgs:
        for tok in p.replace(" ", "").split(","):
            for x in tok.split("-"):
                if x.isdigit():
                    nums.append(int(x))
    check("D10 all pages of the tree are in 436-457 (ch. 11)", nums and min(nums) >= 436 and max(nums) <= 457, str((min(nums), max(nums))))

    # ---------------- citations
    if a.src:
        code, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("V01 verify_citations.py passes", code == 0, o)

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    if FAIL:
        print("Failures:", ", ".join(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

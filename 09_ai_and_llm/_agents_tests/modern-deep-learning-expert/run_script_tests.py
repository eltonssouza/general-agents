# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the package scripts' deterministic test cases (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src CAMINHO/scratch/ai]   # --src enables verify_citations
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
Each test compares the scripts' output with numbers printed in the books (page cited in the test name) or with verifiable identities.
"""
import argparse
import os
import re
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

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


def fnum(s, pat):
    m = re.search(pat, s)
    return float(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join("scripts", "dl_lookup.py")
    C = os.path.join("scripts", "dl_calc.py")
    N = os.path.join("scripts", "dl_nets.py")

    # ---------------- lookup
    code, o = run([L, "dropout", "--top", "1"])
    check("L01 dropout -> ref 06, UDL p.161-163, NNDL p.130-133", "06-desempenho" in o and "161-163" in o and "130-133" in o, o)
    code, o = run([L, "attention", "--top", "1"])
    check("L02 attention -> ref 08, no false NOT COVERED warning", "08-transformers" in o and "WARNING" not in o, o)
    code, o = run([L, "LoRA"])
    check("L03 LoRA -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "RLHF", "--top", "1"])
    check("L04 RLHF -> ref 12, UDL p.411-412", "12-aprendizado" in o and "411-412" in o, o)
    code, o = run([L, "terraform"])
    check("L05 out-of-scope topic -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "--page", "221"])
    check("L06 --page 221 -> Ch.12, printed 207", "Ch.12" in o and "printed 207" in o, o)
    code, o = run([L, "--page", "198"])
    check("L07 --page 198 -> NOT READ", "NOT READ" in o, o)
    code, o = run([L, "--printed", "207"])
    check("L08 --printed 207 -> PDF p.221", "PDF p.221" in o, o)
    code, o = run([L, "--chapters"])
    check("L09 --chapters lists UDL and NNDL (>=27 lines)", o.count("Ch.") >= 27, o)
    code, o = run([L, "--gaps"])
    check("L10 --gaps lists mixture of experts and unread ranges", "mixture of experts" in o and "p.197-199" in o, o)
    code, o = run([L, "--page", "66", "--book", "nndl"])
    check("L11 NNDL p.66 -> Ch.2 backpropagation", "Ch.2" in o and "backprop" in o.lower(), o)
    code, o = run([L, "weight decay", "--top", "1"])
    check("L12 weight decay -> l2, UDL p.169-170 and NNDL p.114-127", "169-170" in o and "114-127" in o, o)
    code, o = run([L, "--datado"])
    check("L13 --datado lists RLHF and GoogLeNet", "RLHF" in o and "GoogLeNet" in o, o)

    # ---------------- calc: numbers printed in the books
    code, o = run([C, "regions", "--D", "10", "--K", "5"])
    check("C01 UDL p.65: K=5,D=10 -> 161051 regions and 471 parameters", "161051" in o and "471" in o, o)
    code, o = run([C, "regions", "--D", "50", "--K", "5", "--Di", "10"])
    check("C02 UDL p.65: Di=10,K=5,D=50 -> 10801 parameters", "10801" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "784,30,10"])
    check("C03 NNDL p.107: [784,30,10] -> 23860", "TOTAL 23860" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,298,10"])
    check("C04a UDL p.418: 1 layer of 298 -> 15208", "TOTAL 15208" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,100,100,10"])
    check("C04b UDL p.418: 2x100 -> 15210", "TOTAL 15210" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,75,75,75,10"])
    check("C04c UDL p.418: 3x75 -> 15235", "TOTAL 15235" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,63,63,63,63,10"])
    check("C04d UDL p.418 (discrepancy): 4x63 -> 15319 (book says 15139)", "TOTAL 15319" in o and "15139" not in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,200,200,10"])
    check("C05 UDL p.150 problem 8.4: 200 hidden -> 50410", "TOTAL 50410" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,400,400,1"])
    check("C06a UDL p.416: 177201 only with a scalar output", "TOTAL 177201" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,400,400,10"])
    check("C06b UDL p.415-416: with 10 outputs -> 180810 (not 177201)", "TOTAL 180810" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "784,200,200,10"])
    check("C06c UDL p.427 (discrepancy): 784-200-200-10 -> 199210 (book says 198450)", "TOTAL 199210" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "40,43,43,10"])
    check("C06d UDL p.415: 43 units -> ~4000 (4095)", "TOTAL 4095" in o, o)
    code, o = run([C, "conv-params", "--ci", "1", "--co", "20", "--k", "5", "--dims", "2"])
    check("C07a NNDL p.248-249: 20 maps 5x5 -> 520", "= 520" in o, o)
    code, o = run([C, "mlp-params", "--sizes", "784,30"])
    check("C07b NNDL p.249: FC 784x30 -> 23550", "TOTAL 23550" in o, o)
    code, o = run([C, "conv-out", "--n", "40", "--k", "3", "--stride", "2"])
    check("C08a UDL p.181: 40 -> 19 (k=3,s=2,valid)", "output = 19" in o, o)
    code, o = run([C, "conv-out", "--n", "28", "--k", "5"])
    check("C08b NNDL p.245: 28 -> 24", "output = 24" in o, o)
    code, o = run([C, "sum-var", "--active", "500", "--var-w", "1"])
    check("C09a NNDL p.140: std of z ~ 22.4", abs((fnum(o, r"standard deviation = ([\d.]+)") or 0) - 22.38) < 0.01, o)
    code, o = run([C, "sum-var", "--active", "500", "--var-w", "0.001"])
    check("C09b NNDL p.141: std of z ~ 1.22", abs((fnum(o, r"standard deviation = ([\d.]+)") or 0) - 1.2247) < 0.001, o)
    code, o = run([C, "sigmoid-chain", "--w", "100,100,100", "--z", "0,0,0"])
    check("C10 NNDL p.235: w*sigma'(0) = 25 por termo", o.count("= 25") >= 0 and "term w*sigma'=25" in o, o)
    code, o = run([C, "var-prop", "--var", "0.02"])
    v = fnum(o, r"layer 50 ([\d.e+\-]+)")
    check("C11a UDL p.124: sigma^2=0.02 stable", v is not None and 0.1 < v < 10, o)
    code, o = run([C, "var-prop", "--var", "0.001"])
    v = fnum(o, r"layer 50 ([\d.e+\-]+)")
    check("C11b UDL p.124: sigma^2=0.001 vanishes", v is not None and v < 1e-30, o)
    code, o = run([C, "var-prop", "--var", "1.0"])
    v = fnum(o, r"layer \d+ ([\d.e+\-]+) \(seed")
    check("C11c UDL p.124: sigma^2=1.0 explodes", v is not None and v > 1e30, o)
    code, o = run([C, "diffusion", "--beta", "0.03", "--T", "100", "--t", "100"])
    r1 = fnum(o, r"coef z_t ([\d.e+\-]+)")
    r2 = fnum(o, r"coef eps ([\d.e+\-]+)")
    check("C12 UDL p.364/366/375: beta=0.03,T=100 -> alpha_100 = 0.0475525 and identity 18.32=18.33", "alpha_t=0.04755250793" in o and r1 is not None and r2 is not None and r1 < 1e-12 and r2 < 1e-12, o)
    code, o = run([C, "kl-normal", "--mu", "1", "--var", "1"])
    check("C13a UDL p.350: KL(N(1,1)||N(0,1)) = 0.5", "= 0.5" in o, o)
    code, o = run([C, "kl-normal", "--mu", "0,0", "--var", "1,1"])
    check("C13b UDL p.350: KL(N(0,I)||N(0,I)) = 0", "= 0" in o, o)
    code, o = run([C, "divergence", "--p", "1,0,0", "--q", "0,0,1"])
    check("C14 UDL p.474: JS = ln2; W1 = 2; KL infinite", "0.6931471806" in o and "W1(p,q)  = 2" in o and "inf" in o, o)
    code, o = run([C, "xent", "--logits", "2,1,0", "--label", "0", "--binary-z", "0", "--binary-y", "1"])
    check("C15 UDL p.82/80: softmax sums to 1; BCE(sigmoid(0))=ln2", "sum 1)" in o and "0.6931471806" in o, o)
    code, o = run([C, "momentum-equiv"])
    d = fnum(o, r"over \d+ steps = ([\d.e+\-]+)")
    check("C16 UDL p.100 vs NNDL p.176: equivalent momentum", d is not None and d < 1e-12, o)
    code, o = run([C, "l2-equiv"])
    d = fnum(o, r"difference ([\d.e+\-]+)")
    check("C17 UDL p.154 vs NNDL p.116: equivalent L2 with alpha=eta/n, lambda_UDL=lambda/2", d is not None and d < 1e-12, o)
    code, o = run([C, "adam-step", "--grad", "5,0.01", "--steps", "1", "--alpha", "0.001"])
    check("C18 UDL p.102: 1st Adam step ~ alpha regardless of gradient scale", "-0.001, -0.000999999" in o, o)
    code, o = run([C, "returns", "--rewards", "0,0,1", "--gamma", "0.9"])
    check("C19 UDL p.388: discounted return 0.81", "G = 0.81" in o, o)
    code, o = run([C, "xfmr-params", "--preset", "bert-large", "--ln"])
    t = fnum(o, r"TOTAL approximate: ([\d.]+)")
    check("C20a UDL p.233: BERT ~340M (our count 330-345M)", t is not None and 330 <= t <= 345, o)
    code, o = run([C, "xfmr-params", "--preset", "gpt3", "--vocab", "50257"])
    t = fnum(o, r"TOTAL approximate: ([\d.]+)")
    check("C20b UDL p.238: GPT-3 ~175B (our count 172000-176000 million, with 4D MLP and vocab 50257 = [extrapolation])", t is not None and 172000 <= t <= 176000, o)
    code, o = run([C, "init-var", "--rule", "he", "--fan-in", "100"])
    check("C21 UDL p.124: He with Dh=100 -> 0.02", "variance = 0.02;" in o, o)
    code, o = run([C, "init-var", "--rule", "nndl", "--fan-in", "1000"])
    check("C22 NNDL p.141: 1/n_in with n=1000 -> 0.001", "variance = 0.001;" in o, o)

    # ---------------- nets
    code, o = run([N, "backprop-check", "--act", "sigmoid"])
    e = fnum(o, r"= ([\d.e+\-]+)\s*$")
    check("N01a NNDL p.66-68 BP1-BP4 vs finite differences (p.78)", e is not None and e < 1e-8, o)
    code, o = run([N, "backprop-check", "--act", "relu", "--arch", "3,5,4,2"])
    e = fnum(o, r"= ([\d.e+\-]+)\s*\n")
    check("N01b UDL p.120 eq.7.24 vs finite differences", e is not None and e < 1e-8, o)
    code, o = run([N, "attention", "--tokens", "1,0;0,1;1,1", "--perm-check"])
    check("N02 UDL p.227: permutation equivariance and weights sum to 1", "confirmed" in o and o.count("sum 1.000000") == 3, o)
    code, o = run([N, "attention", "--tokens", "1,0;0,1;1,1", "--mask"])
    check("N03 UDL p.237: mask -> query 0 attends only to itself", "1.000000, 0.000000, 0.000000" in o, o)
    code, o = run([N, "route", "--weights", "0.1,0.3,0.6", "--values", "1,0;0,1;1,1"])
    check("N04 UDL p.223 fig.12.1: weights 0.1/0.3/0.6 -> 0.7, 0.9", "0.700000, 0.900000" in o, o)
    code, o = run([N, "toy-neuron", "--epochs", "300"])
    check("N05a NNDL p.86-87: initial output 0.82 and ~0.09 at epoch 300", "output=0.817574" in o and re.search(r"epoch 300: .* output=0\.09", o) is not None, o)
    code, o = run([N, "toy-neuron", "--w", "2", "--b", "2", "--epochs", "150"])
    s = fnum(o, r"epoch 150: .* output=([\d.]+)")
    check("N05b NNDL p.87-88: w=b=2 -> 0.98 and nearly stalled at 150 epochs (output > 0.9)", "output=0.982014" in o and s is not None and s > 0.9, o)
    code, o = run([N, "toy-neuron", "--w", "2", "--b", "2", "--epochs", "50", "--eta", "0.15", "--cost", "cross-entropy"])
    s = fnum(o, r"epoch 50: .* output=([\d.]+)")
    check("N05c NNDL p.91-93: with cross-entropy the same neuron leaves saturation (output < 0.2 in 50 epochs)", s is not None and s < 0.2, o)
    code, o = run([N, "universality", "--N", "5,20,100"])
    errs = [float(x) for x in re.findall(r"max error = ([\d.]+)", o)]
    check("N06 NNDL p.196-203: max error decreases with N (5 > 20 > 100)", len(errs) == 3 and errs[0] > errs[1] > errs[2], o)
    code, o = run([N, "cnn-shapes"])
    check("N07a NNDL p.256: FC receives 640 = 40*4*4", "640" in o and "24x24" in o and "4x4" in o, o)
    code, o = run([N, "cnn-shapes", "--preset", "udl-mnist1d"])
    check("N07b UDL p.181: 2050 (conv) and 59065 (FC)", "TOTAL 2050" in o and "59065" in o, o)

    # ---------------- the references support the expected answers (casos-de-teste.md)
    def ref_has(name, fn, subs):
        path = os.path.join(PKG, "references", fn)
        txt = open(path, encoding="utf-8").read()
        miss = [x for x in subs if x not in txt]
        check(name, not miss, "missing in " + fn + ": " + "; ".join(miss))

    ref_has("R01 T01 cross-entropy/slowdown", "03-funcoes-de-perda-e-cross-entropy.md", ["NNDL p.88-89", "NNDL p.90-91", "UDL p.85-86"])
    ref_has("R02 T02 weight decay x L2", "06-desempenho-generalizacao-e-regularizacao.md", ["UDL p.169", "λ = λ'/(2α)", "NNDL p.116"])
    ref_has("R03 T06 scaled attention", "08-transformers-e-linguagem.md", ["√Dq", "UDL p.228", "eq. 12.9"])
    ref_has("R04 T08 BERT 340M", "08-transformers-e-linguagem.md", ["340 million", "UDL p.233", "333.5"])
    ref_has("R05 T09 GPT-3 4D MLP is extrapolation", "08-transformers-e-linguagem.md", ["MLP 4D", "[extrapolation]"])
    ref_has("R06 T10 diffusion kernel", "11-difusao.md", ["eq. 18.7", "UDL p.366", "eq. 18.15"])
    ref_has("R07 T12 ELBO and reparameterization", "10-modelos-generativos-gan-fluxos-vae.md", ["eq. 17.17", "eq. 17.25", "UDL p.344-349"])
    ref_has("R08 T14 momentum UDL vs NNDL", "comparacao-udl-nndl.md", ["eq. 6.11", "NNDL p.176", "μ = β"])
    ref_has("R09 T15 sum vs mean", "comparacao-udl-nndl.md", ["Mean × sum", "l2-equiv"])
    ref_has("R10 T16 AlexNet 16,4% x 84,7%", "casos-e-antipadroes.md", ["16.4%", "84.7%"])
    ref_has("R11 T17 fig 20.2", "casos-e-antipadroes.md", ["15,139", "15,319"])
    ref_has("R12 T18 modern topics NOT COVERED", "datado-e-limites.md", ["FlashAttention", "LoRA", "NOT COVERED"])
    ref_has("R13 T20 RLHF", "12-aprendizado-por-reforco.md", ["RLHF", "UDL p.412", "PPO"])
    ref_has("R14 T24 facial ethics", "14-etica-e-uso-responsavel.md", ["UDL p.440-441", "UDL p.444-445"])
    ref_has("R15 T27 BP1-BP4", "04-otimizacao-e-backpropagation.md", ["BP1", "BP4", "NNDL p.66-67", "NNDL p.68"])
    ref_has("R16 T28 η workflow", "06-desempenho-generalizacao-e-regularizacao.md", ["NNDL p.162-164", "threshold"])
    ref_has("R17 T30 double descent", "06-desempenho-generalizacao-e-regularizacao.md", ["Double descent", "UDL p.141-143"])
    ref_has("R18 T31 large graphs", "09-grafos-gnn.md", ["neighborhood sampling", "UDL p.267-270"])
    ref_has("R19 T32 SARSA vs Q-learning", "12-aprendizado-por-reforco.md", ["SARSA", "eq. 19.14", "eq. 19.15"])
    ref_has("R20 T33 mode collapse and WGAN", "10-modelos-generativos-gan-fluxos-vae.md", ["mode collapse", "WGAN", "UDL p.297-299"])
    ref_has("R21 T26 unread page", "INDEX.md", ["p.197-199", "NOT read"])

    # ---------------- citations
    if a.src or os.path.isdir(os.path.abspath(os.path.join(PKG, "..", "..", "..", "scratch", "ai"))):
        args = [os.path.join("tests", "verify_citations.py")]
        if a.src:
            args += ["--src", a.src]
        code, o = run(args)
        check("V01 verify_citations: ranges + positives + negatives", code == 0 and "OK" in o, o)
        n_pos = fnum(o, r"(\d+) positive checks")
        n_neg = fnum(o, r"(\d+) negative")
        check("V02 >=60 positive and >=15 negative", n_pos is not None and n_pos >= 60 and n_neg is not None and n_neg >= 15, o)
    else:
        print("SKIP verify_citations (extracted text not found; use --src)")

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILURES: " + "; ".join(FAIL))
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
llm_calc.py - calculators based on the formulas of the LLMS ("A Survey of Large Language Models", Zhao et al.,
arXiv 2303.18223v19, 18 Mar 2026) [DATED]. Stdlib only, no network, deterministic.

Each subcommand prints the formula, the LLMS PAGE (PDF = printed) and the source label
([from source] / [inference] / [extrapolation]). The formulas were checked visually on the cited pages.

Subcommands:
  scaling-kaplan        --N | --D | --C            L(N), L(D), L(C)            (LLMS p.4, Eq.1)
  scaling-chinchilla    --N --D                    L(N,D)=E+A/N^a+B/D^b        (LLMS p.4, Eq.2)
  chinchilla-allocation --C [--G]                  exponents a,b and Nopt/Dopt   (LLMS p.4, Eq.3)
  compute               --N --D                    C ~ 6ND                     (LLMS p.4)
  rope                  --d --i [--base] [--t]     theta_i and wavelength (LLMS p.25, Eq.4-5)
  sampling              --probs ... [--temperature T] [--top-k K] [--top-p P]   (LLMS p.26-27, Eq.8-10)
  train-states          --params P                 2P+2P+12P = 16P bytes       (LLMS p.81)
  train-activations     [--B --T --H --Hp --N --V --L]  Tab.18                  (LLMS p.82)
  arithmetic-intensity  --phase prefill|decode [--B --T --H --N --D] [--tflops --gbs]   (LLMS p.83-84, Tab.19/20)
  lora                  --m --n --k                trainable parameters       (LLMS p.43)
  quantize              --x ... --S --Z            xq=R(x/S)-Z, x~=S(xq+Z)     (LLMS p.86)
  smoothquant           --xmax ... --wmax ... --alpha   s_j                      (LLMS p.86)
  weights-memory        --params P --bits b        P*b/8 bytes                 ([inference]; compares Tab.21 p.88)
  pass-at-k             --results 1 0 0 ...        pass@k                      (LLMS p.56 nota 37)
  majority-vote         --answers a b a ...        self-consistency (vote)     (LLMS p.52)
  wordpiece-score       --pair-count --a-count --b-count   merge score       (LLMS p.19)
"""
import argparse
import json
import math
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

GIB = 2 ** 30


def out(args, d):
    if getattr(args, "json", False):
        print(json.dumps(d, ensure_ascii=False, indent=1))
    else:
        for k, v in d.items():
            print(f"{k}: {v}")


# ----------------------------------------------------------------------------- scaling laws
KM = {"N": (0.076, 8.8e13), "D": (0.095, 5.4e13), "C": (0.050, 3.1e8)}  # (alpha, xc) LLMS p.4 Eq.1
CH = {"E": 1.69, "A": 406.4, "B": 410.7, "alpha": 0.34, "beta": 0.28}  # LLMS p.4 Eq.2


def kaplan(x, which):
    a, xc = KM[which]
    return (xc / x) ** a


def chinchilla_loss(N, D):
    return CH["E"] + CH["A"] / N ** CH["alpha"] + CH["B"] / D ** CH["beta"]


def exps_printed():
    """a and b exactly as printed in the survey (LLMS p.4): a=alpha/(alpha+beta), b=beta/(alpha+beta)."""
    s = CH["alpha"] + CH["beta"]
    return CH["alpha"] / s, CH["beta"] / s


def exps_derived():
    """Exponents obtained by minimizing L(N,D) under C=6ND: N ~ (C/6)^(beta/(alpha+beta)) [inference]."""
    s = CH["alpha"] + CH["beta"]
    return CH["beta"] / s, CH["alpha"] / s


def g_derived():
    """G = (alpha*A/(beta*B))^(1/(alpha+beta)): derivation from Eq.2 [inference]; the survey does not give the formula for G."""
    return (CH["alpha"] * CH["A"] / (CH["beta"] * CH["B"])) ** (1.0 / (CH["alpha"] + CH["beta"]))


def numeric_argmin_N(C, n=4000):
    """Minimizes L(N, C/(6N)) by a log-spaced sweep (independent numerical check)."""
    best = None
    lo, hi = 1e6, 1e15
    for i in range(n + 1):
        N = lo * (hi / lo) ** (i / n)
        D = C / (6.0 * N)
        if D <= 1:
            continue
        L = chinchilla_loss(N, D)
        if best is None or L < best[0]:
            best = (L, N, D)
    return best


# ----------------------------------------------------------------------------- sampling
def softmax_t(logits, t):
    m = max(l / t for l in logits)
    ex = [math.exp(l / t - m) for l in logits]
    z = sum(ex)
    return [e / z for e in ex]


def apply_topk(p, k):
    idx = sorted(range(len(p)), key=lambda i: (-p[i], i))[:k]
    keep = set(idx)
    q = [p[i] if i in keep else 0.0 for i in range(len(p))]
    z = sum(q)
    return [x / z for x in q]


def apply_topp(p, top_p):
    order = sorted(range(len(p)), key=lambda i: (-p[i], i))
    cum, keep = 0.0, set()
    for i in order:
        keep.add(i)
        cum += p[i]
        if cum >= top_p - 1e-12:
            break
    q = [p[i] if i in keep else 0.0 for i in range(len(p))]
    z = sum(q)
    return [x / z for x in q]


# ----------------------------------------------------------------------------- memory / activations
def train_states_bytes(P):
    return {"params_fp16": 2 * P, "grads_fp16": 2 * P, "optimizer_fp32": 12 * P, "total": 16 * P}


def activations_bytes(B, T, H, Hp, N, V, L, six_bth=True):
    """Tab.18 (LLMS p.82). ①-⑨ per layer (x L); ⑩ only once.
    Note: the table prints '6TH' (without B) for Q,K,V; here six_bth=True uses 6BTH (same when B=1)."""
    qkv = 6 * B * T * H if six_bth else 6 * T * H
    per_layer = {
        "1_X": 2 * B * T * H,
        "2_QK_rope": 4 * B * T * H,
        "3_QKV": qkv,
        "3_softmax": 2 * B * T * T * N,
        "4_O": 2 * B * T * H,
        "5_X_addnorm": 2 * B * T * H,
        "6_X_ffn": 2 * B * T * H,
        "7_GU": 4 * B * T * Hp,
        "8_D": 2 * B * T * Hp,
        "9_X_addnorm": 2 * B * T * H,
    }
    layer_total = sum(per_layer.values())
    final = 2 * B * T * H + 4 * B * T * V
    return per_layer, layer_total, final, layer_total * L + final


# ----------------------------------------------------------------------------- arithmetic intensity
def ai_prefill(B, T, H, Hp, D):
    BT = B * T
    return {
        "1_QKV_linear": 1 / (1 / H + 1 / BT),
        "2_RoPE": 1.0,
        "3_attention": (1 + 1 / D) / (1 / D + 1 / T),
        "4_out_linear": 1 / (1 / H + 1 / BT),
        "5_AddNorm": 1 / (1 + 1 / BT),
        "6_ffn_GU": 1 / (1 / H + 1 / Hp + 1 / BT),
        "7_Swish": 1.0,
        "8_ffn_D": 1 / (1 / H + 1 / Hp + 1 / BT),
        "9_AddNorm": 1 / (1 + 1 / BT),
    }


def ai_decode(B, T, H, Hp, D):
    return {
        "1_QKV_linear": 1 / (1 / H + 1 / B),
        "2_RoPE": 1.0,
        "4_attention": (1 + 1 / D) / (1 + 1 / D + 1 / T),
        "5_out_linear": 1 / (1 / H + 1 / B),
        "6_AddNorm": 1 / (1 + 1 / B),
        "7_ffn_GU": 1 / (1 / H + 1 / Hp + 1 / B),
        "8_Swish": 1.0,
        "9_ffn_D": 1 / (1 / H + 1 / Hp + 1 / B),
        "10_AddNorm": 1 / (1 + 1 / B),
    }


def imax(tflops, gbs, gib=True):
    unit = GIB if gib else 1e9
    return (tflops * 1e12) / (gbs * unit)


# ----------------------------------------------------------------------------- quantization
def rnd(v):
    return math.floor(v + 0.5)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("scaling-kaplan")
    p.add_argument("--N", type=float); p.add_argument("--D", type=float); p.add_argument("--C", type=float)
    p = sub.add_parser("scaling-chinchilla")
    p.add_argument("--N", type=float, required=True); p.add_argument("--D", type=float, required=True)
    p = sub.add_parser("chinchilla-allocation")
    p.add_argument("--C", type=float, required=True); p.add_argument("--G", type=float)
    p = sub.add_parser("compute")
    p.add_argument("--N", type=float, required=True); p.add_argument("--D", type=float, required=True)
    p = sub.add_parser("rope")
    p.add_argument("--d", type=int, required=True); p.add_argument("--i", type=int, required=True)
    p.add_argument("--base", type=float, default=10000.0); p.add_argument("--t", type=float)
    p = sub.add_parser("sampling")
    p.add_argument("--probs", type=float, nargs="+", required=True)
    p.add_argument("--labels", nargs="+")
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--top-k", type=int); p.add_argument("--top-p", type=float)
    p = sub.add_parser("train-states")
    p.add_argument("--params", type=float, required=True)
    p = sub.add_parser("train-activations")
    p.add_argument("--B", type=int, default=1); p.add_argument("--T", type=int, default=2048)
    p.add_argument("--H", type=int, default=4096); p.add_argument("--Hp", type=int, default=11008)
    p.add_argument("--N", type=int, default=32); p.add_argument("--V", type=int, default=32000)
    p.add_argument("--L", type=int, default=32)
    p = sub.add_parser("arithmetic-intensity")
    p.add_argument("--phase", choices=["prefill", "decode"], required=True)
    p.add_argument("--B", type=int, default=8); p.add_argument("--T", type=int, default=1024)
    p.add_argument("--H", type=int, default=4096); p.add_argument("--Hp", type=int, default=11008)
    p.add_argument("--N", type=int, default=32); p.add_argument("--D", type=int, default=128)
    p.add_argument("--tflops", type=float, default=312.0); p.add_argument("--gbs", type=float, default=2039.0)
    p.add_argument("--decimal-gb", action="store_true", help="treat GB as 1e9 (the survey text only reproduces 142.51 with 2^30)")
    p = sub.add_parser("lora")
    p.add_argument("--m", type=int, required=True); p.add_argument("--n", type=int, required=True); p.add_argument("--k", type=int, required=True)
    p = sub.add_parser("quantize")
    p.add_argument("--x", type=float, nargs="+", required=True); p.add_argument("--S", type=float, required=True); p.add_argument("--Z", type=float, default=0.0)
    p = sub.add_parser("smoothquant")
    p.add_argument("--xmax", type=float, nargs="+", required=True); p.add_argument("--wmax", type=float, nargs="+", required=True)
    p.add_argument("--alpha", type=float, default=0.5)
    p = sub.add_parser("weights-memory")
    p.add_argument("--params", type=float, required=True); p.add_argument("--bits", type=int, required=True)
    p = sub.add_parser("pass-at-k")
    p.add_argument("--results", type=int, nargs="+", required=True, help="1 = program passed all tests, 0 = failed")
    p = sub.add_parser("majority-vote")
    p.add_argument("--answers", nargs="+", required=True)
    p = sub.add_parser("wordpiece-score")
    p.add_argument("--pair-count", type=float, required=True); p.add_argument("--a-count", type=float, required=True); p.add_argument("--b-count", type=float, required=True)

    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        return

    if a.cmd == "scaling-kaplan":
        d = {"formula": "L(X)=(Xc/X)^alpha_X; alphaN~0.076 Nc~8.8e13; alphaD~0.095 Dc~5.4e13; alphaC~0.050 Cc~3.1e8",
             "source": "[from source] LLMS p.4, Eq.1 (checked visually); N,D,C in non-embedding parameters, tokens and FP-days; L in nats"}
        n = 0
        for key, val in (("N", a.N), ("D", a.D), ("C", a.C)):
            if val:
                d[f"L({key})"] = kaplan(val, key); n += 1
        if not n:
            print("provide --N, --D or --C"); sys.exit(2)
        d["warning"] = "[DATED] laws fitted in 2020 (22M-23B tokens; 768-1.5B parameters); extrapolating beyond that is [extrapolation]"
        out(a, d)
    elif a.cmd == "scaling-chinchilla":
        L = chinchilla_loss(a.N, a.D)
        out(a, {"formula": "L(N,D)=E+A/N^alpha+B/D^beta; E=1.69 A=406.4 B=410.7 alpha=0.34 beta=0.28",
                "source": "[from source] LLMS p.4, Eq.2 (checked visually)",
                "L(N,D)": L, "irreducible_term_E": CH["E"], "model_term": CH["A"] / a.N ** CH["alpha"], "data_term": CH["B"] / a.D ** CH["beta"]})
    elif a.cmd == "chinchilla-allocation":
        ap_, bp_ = exps_printed()
        ad, bd = exps_derived()
        G = a.G if a.G else None
        Gd = g_derived()
        d = {"constraint": "C ~ 6ND [from source] LLMS p.4",
             "Nopt(C)=G(C/6)^a; Dopt(C)=G^-1 (C/6)^b": "[from source] LLMS p.4, Eq.3",
             "a,b_as_printed_in_survey": f"a=alpha/(alpha+beta)={ap_:.4f}; b=beta/(alpha+beta)={bp_:.4f}  [from source] LLMS p.4",
             "a,b_derived_from_Eq.2_with_C=6ND": f"a=beta/(alpha+beta)={ad:.4f}; b=alpha/(alpha+beta)={bd:.4f}  [inference: minimization of L(N,D)]",
             "ALERT": "The printed text of the survey assigns a=alpha/(alpha+beta) to the exponent of N, but minimizing Eq.2 itself under C=6ND gives the exponent beta/(alpha+beta) for N. Treat the printed definition as a possible notation swap [inference]; the original paper (Hoffmann et al.) uses a=beta/(alpha+beta) [extrapolation: not verifiable in this collection].",
             "G": "the survey only says that G can be computed from A,B,alpha,beta (LLMS p.4), without giving the formula"}
        if G is None:
            G = Gd
            d["G_used"] = f"{G:.6f} = (alpha*A/(beta*B))^(1/(alpha+beta)) [extrapolation: formula is not in the survey; derived from Eq.2]"
        else:
            d["G_used"] = f"{G} (provided by the user)"
        Cp = a.C / 6.0
        Nopt = G * Cp ** ad
        Dopt = (1 / G) * Cp ** bd
        d["Nopt_(derived a)"] = Nopt
        d["Dopt_(derived b)"] = Dopt
        d["check Nopt*Dopt = C/6"] = f"{Nopt * Dopt:.6e} vs {Cp:.6e}"
        d["tokens_per_parameter"] = Dopt / Nopt
        Nbad = G * Cp ** ap_
        d["Nopt_with_printed_a (not recommended)"] = Nbad
        L, Nn, Dn = numeric_argmin_N(a.C)
        d["numerical_check_argmin_N (sweep of L(N,C/6N))"] = Nn
        d["Dopt_numerical"] = Dn
        out(a, d)
    elif a.cmd == "compute":
        out(a, {"C_flops": 6 * a.N * a.D, "formula": "C ~ 6ND", "source": "[from source] LLMS p.4 (Chinchilla constraint); training FLOPs approximation"})
    elif a.cmd == "rope":
        th = a.base ** (-2.0 * (a.i - 1) / a.d)
        lam = 2 * math.pi / th
        d = {"formula": "theta_i=b^(-2(i-1)/d), i=1..d/2; lambda_i=2*pi*b^(2(i-1)/d)=2*pi/theta_i; angle=t*theta_i",
             "source": "[from source] LLMS p.25, Eq.4-5 (checked visually)", "theta_i": th, "lambda_i": lam}
        if a.i < 1 or a.i > a.d // 2:
            d["warning"] = "i outside 1..d/2"
        if a.t is not None:
            d["angle_t_theta"] = a.t * th
        out(a, d)
    elif a.cmd == "sampling":
        p = list(a.probs)
        z = sum(p)
        p = [x / z for x in p]
        lab = a.labels or [str(i) for i in range(len(p))]
        if len(lab) != len(p):
            print("labels and probs must have the same length"); sys.exit(2)
        logits = [math.log(x) for x in p]
        q = softmax_t(logits, a.temperature)
        steps = [f"temperature t={a.temperature} (Eq.10)"]
        if a.top_k:
            q = apply_topk(q, a.top_k); steps.append(f"top-k={a.top_k}")
        if a.top_p:
            q = apply_topp(q, a.top_p); steps.append(f"top-p={a.top_p}")
        order = sorted(range(len(q)), key=lambda i: (-q[i], i))
        d = {"source": "[from source] LLMS p.26-27: greedy x=argmax P (Eq.8); sampling (Eq.9); temperature exp(l/t)/sum exp(l'/t) (Eq.10); top-k; top-p (smallest set with cumulative prob. >= p)",
             "steps": "; ".join(steps), "greedy(argmax)": lab[max(range(len(p)), key=lambda i: (p[i], -i))],
             "final_distribution": {lab[i]: round(q[i], 6) for i in order if q[i] > 0}}
        out(a, d)
    elif a.cmd == "train-states":
        s = train_states_bytes(a.params)
        d = {"formula": "2P (16-bit params) + 2P (16-bit gradients) + 12P (Adam in FP32: copy 4P, momentum 4P, variance 4P) = 16P bytes",
             "source": "[from source] LLMS p.81"}
        d.update({k: f"{v:.4e} B = {v / GIB:.2f} GiB" for k, v in s.items()})
        d["note"] = "example from the text (p.81): LLaMA-7B, P=6.7e9, 'about 100GB' (16P = 1.072e11 B = 99.8 GiB); does not include activations (see train-activations) or overheads (p.82)"
        out(a, d)
    elif a.cmd == "train-activations":
        pl, lt, fin, tot = activations_bytes(a.B, a.T, a.H, a.Hp, a.N, a.V, a.L)
        d = {"source": "[from source] LLMS p.82, Tab.18 (checked visually); summation done by this script [inference]",
             "per_layer_bytes": pl, "per_layer_sum": lt, "layers": a.L, "final_loss_(10)": fin,
             "total_bytes": tot, "total_GiB": tot / GIB, "total_GB_decimal": tot / 1e9,
             "note": "the text states ~16GB for LLaMA-7B with B=1, T=2048 (p.81-82); the table sum gives ~17.3 GiB (~18.6 GB): the '16GB' is approximate [inference]. Tab.18 prints 6TH (without B) for Q,K,V."}
        out(a, d)
    elif a.cmd == "arithmetic-intensity":
        fn = ai_prefill if a.phase == "prefill" else ai_decode
        r = fn(a.B, a.T, a.H, a.Hp, a.D)
        im = imax(a.tflops, a.gbs, gib=not a.decimal_gb)
        d = {"source": "[from source] LLMS p.83-84, Tab.19 (prefill) and Tab.20 (decoding), asymptotic O(.) formulas used as values (as the text does); checked visually",
             "phase": a.phase, "B": a.B, "T": a.T, "H": a.H, "H'": a.Hp, "D": a.D,
             "Imax_FLOP_per_byte": round(im, 2),
             "Imax_note": f"{a.tflops} TFLOP/s / ({a.gbs} GB/s); the text (p.83) says 142.51 for A100 (312 TFLOP/s, 2039GB/s) and it is only reproduced with GB=2^30 bytes [inference]"}
        cls = {}
        for k, v in r.items():
            d[f"I_{k}"] = round(v, 2)
            cls[k] = "compute-bound" if v > im else "memory-bound"
        d["classification"] = cls
        if a.phase == "prefill":
            d["source_text"] = "B=8,T=1024: linear layers ~2730.67; attention ~114.67; others ~1; prefill compute-bound (p.83)"
        else:
            d["source_text"] = "decoding: intensities of the linear layers and of attention < 8, memory-bound ('memory wall') (p.83)"
        out(a, d)
    elif a.cmd == "lora":
        full = a.m * a.n
        tr = a.k * (a.m + a.n)
        out(a, {"formula": "W<-W+dW, dW=A.B^T, A em R^(m x k), B em R^(n x k), k<<min(m,n)", "source": "[from source] LLMS p.43",
                "frozen_W_parameters": full, "trainable_parameters_k(m+n)": tr, "ratio": tr / full,
                "note": "count k(m+n) deduced from the definition of A and B [inference]"})
    elif a.cmd == "quantize":
        res = []
        for x in a.x:
            xq = rnd(x / a.S) - a.Z
            xt = a.S * (xq + a.Z)
            res.append({"x": x, "xq": xq, "x_recovered": xt, "error": x - xt})
        out(a, {"formula": "xq=R(x/S)-Z; x~=S(xq+Z); error=x-x~", "source": "[from source] LLMS p.86 (checked visually)", "results": res,
                "note": "R(.) rounds to the nearest integer; clipping (alpha,beta) not modeled"})
    elif a.cmd == "smoothquant":
        if len(a.xmax) != len(a.wmax):
            print("xmax and wmax must have the same length"); sys.exit(2)
        s = [(x ** a.alpha) / (w ** (1 - a.alpha)) for x, w in zip(a.xmax, a.wmax)]
        out(a, {"formula": "Y=(X diag(s)^-1).(diag(s) W); s_j=max(x_j)^alpha / max(w_j)^(1-alpha)", "source": "[from source] LLMS p.86", "s": s})
    elif a.cmd == "weights-memory":
        b = a.params * a.bits / 8.0
        out(a, {"bytes": b, "GiB": b / GIB, "source": "[inference] params*bits/8; order of magnitude to compare with Tab.21 (LLMS p.88): LLaMA 7B 16-bit 12.58 GiB, 8-bit 6.65, 4-bit 3.94 (measured values, include non-quantized parts)"})
    elif a.cmd == "pass-at-k":
        v = 1 if any(a.results) else 0
        out(a, {"k": len(a.results), "pass@k": v, "definition": "given k programs, 1 if at least one passes all tests; otherwise 0", "source": "[from source] LLMS p.56, note 37"})
    elif a.cmd == "majority-vote":
        cnt = {}
        for x in a.answers:
            cnt[x] = cnt.get(x, 0) + 1
        best = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
        out(a, {"counts": cnt, "winner": best[0][0], "tie_break": "alphabetical order (script choice)", "source": "[from source] LLMS p.52: Self-Consistency picks the most consistent answer by majority vote"})
    elif a.cmd == "wordpiece-score":
        out(a, {"score": a.pair_count / (a.a_count * a.b_count), "formula": "pair co-occurrence / (occurrences of a * occurrences of b)",
                "source": "[from source] LLMS p.19 (the 'more intuitive' measure from Hugging Face; the original WordPiece has no public official implementation)"})


if __name__ == "__main__":
    main()

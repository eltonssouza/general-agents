# -*- coding: utf-8 -*-
"""
dlb_diagnose.py - training diagnosis guide (ch. 11 "Practical Methodology" of DLB, PDF p.436-457) as a decision tree with pages.

stdlib only, no network, deterministic. Reads only scripts/dlb_tree.json.
Usage:
  python -I scripts/dlb_diagnose.py --tree                       # prints the full tree
  python -I scripts/dlb_diagnose.py --train-error 0.01 --test-error 0.12 --target 0.05
  python -I scripts/dlb_diagnose.py --train-error 0.20 --test-error 0.21 --target 0.05 [--bayes-error 0.02] [--json]
  python -I scripts/dlb_diagnose.py --debug                      # debugging checklist (p.451-455)
  python -I scripts/dlb_diagnose.py --baseline sequence          # suggested baseline (p.440): vector|image|sequence
  python -I scripts/dlb_diagnose.py --hyper                      # Tabela 11.1 (p.446)
  python -I scripts/dlb_diagnose.py --lr-state diverges          # reading of the learning rate (p.444-445)
Page convention: PDF (printed = PDF - 15). Source of the recommendations: [from source] (ch. 11); the automatic classification by errors is
[inference]. The book is from 2016 [DATED]; for any subject outside ch. 11 say NOT COVERED.
"""
import argparse
import io
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))

AVISO = "Source: [from source] ch. 11 (DLB p.436-457); the automatic classification from the numbers provided is [inference]. 2016 book [DATED]. Does not replace the analysis of the concrete case."


def load():
    with io.open(os.path.join(HERE, "dlb_tree.json"), encoding="utf-8") as f:
        return json.load(f)


def fmt_acoes(node, ind="  "):
    return [f"{ind}- {a['txt']} (DLB p.{a['pag']})" for a in node.get("acoes", [])]


def print_tree(t):
    seen = set()

    def walk(nid, depth):
        n = t["nos"][nid]
        pad = "  " * depth
        if nid in seen:
            print(f"{pad}-> see '{n['titulo']}'")
            return
        seen.add(nid)
        print(f"{pad}[{nid}] {n['titulo']}")
        if n["tipo"] == "decisao":
            print(f"{pad}  ? {n['pergunta']} (DLB p.{n['pag']})")
            print(f"{pad}  YES:")
            walk(n["sim"], depth + 2)
            print(f"{pad}  NO:")
            walk(n["nao"], depth + 2)
        else:
            for l in fmt_acoes(n, pad + "  "):
                print(l)
            if n.get("proximo"):
                walk(n["proximo"], depth + 1)

    walk(t["inicio"], 0)
    print(AVISO)


def diagnose(a):
    t = load()
    notes = []
    path = []
    tr, te, tg = a.train_error, a.test_error, a.target
    bayes = a.bayes_error
    cls = None
    if tr is None or te is None or tg is None:
        raise SystemExit("provide --train-error, --test-error and --target (same unit, e.g. error rate)")
    if bayes is not None and tg < bayes:
        notes.append(f"The target ({tg}) is below the stated Bayes error ({bayes}): unreachable even with infinite data (DLB p.437).")
    if tr > tg:
        if te - tr <= max(0.1 * tr, 1e-12):
            cls = "training and test errors both high and close: underfitting OR a data problem OR a software defect (DLB p.453, 456-457)"
        else:
            cls = "training error above the target (and test even worse): fix training first (DLB p.441)"
        path = ["treino", "subajuste", "qualidade"]
    elif te <= tg:
        cls = "targets met on training and test"
        path = ["treino", "teste", "pronto"]
    else:
        cls = "acceptable training and unacceptable test: generalization gap (overfitting) (DLB p.126, 442)"
        path = ["treino", "teste", "gap", "hiperparametros", "depuracao"]
    extra = []
    if a.lr_state == "diverges":
        extra.append("learning rate: the training error rises/oscillates violently -> decrease it; in the idealized quadratic case the error increases with eps >= 2x the optimum (DLB p.444, 310).")
    elif a.lr_state == "stuck":
        extra.append("learning rate: slow/stuck training with high error -> it may be too low (DLB p.444); remember that the training error has a U-shaped curve vs learning rate (Fig. 11.1, DLB p.445).")
    if a.regularized == "no" and tr > tg:
        extra.append("no regularization and high training error: add layers/units (DLB p.444).")
    if a.regularized == "yes" and tr > tg:
        extra.append("regularization is already in place and training error is high: reducing weight decay/dropout increases capacity (Table 11.1, DLB p.446).")
    if a.data_cheap == "yes" and tr <= tg < te:
        extra.append("data is cheap to collect: collecting more data is almost always the answer (DLB p.442).")
    if a.data_cheap == "no" and tr <= tg < te:
        extra.append("data is expensive/infeasible: shrink the model or improve regularization (DLB p.442).")
    res = {"classificacao": cls, "caminho": path, "notas": notes + extra}
    if a.json:
        steps = []
        for nid in path:
            n = t["nos"][nid]
            steps.append({"no": nid, "titulo": n["titulo"], "acoes": n.get("acoes", []), "pergunta": n.get("pergunta")})
        res["passos"] = steps
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print(f"Inputs: train={tr}, test={te}, target={tg}" + (f", Bayes={bayes}" if bayes is not None else ""))
    print(f"Classification [inference]: {cls}")
    print("Prerequisites (nodes 'meta' and 'baseline'): metric and target defined, end-to-end pipeline with baseline (DLB p.436-441); see --tree.")
    for nid in path:
        n = t["nos"][nid]
        print(f"\n[{nid}] {n['titulo']}" + (f"  -- {n['pergunta']} (DLB p.{n['pag']})" if n["tipo"] == "decisao" else ""))
        for l in fmt_acoes(n):
            print(l)
    for x in notes + extra:
        print("Note: " + x)
    print(AVISO)
    return 0


DEBUG = [
    ("Visualize the model in action (overlaid detections, samples) - evaluation bugs mislead", "452"),
    ("Visualize the worst errors / most confident errors (preprocessing or labels)", "452-453"),
    ("Reason with training and test error: low training + high test = overfitting OR a wrong test measurement (save/reload, different preparation); both high = bug OR underfitting", "453"),
    ("Fit a tiny dataset (one example; classifier, autoencoder or generative model)", "453"),
    ("Compare backprop derivatives with numerical derivatives: finite differences (centered), repeated random projections u^T g(v x), complex step (eps down to 1e-150)", "453-454"),
    ("Monitor histograms of activations and gradients (saturation, ReLU always off); update ~1% of the parameter per minibatch", "455"),
    ("Test the algorithm's guarantees (objective does not increase after a step; zero gradient at convergence) with tolerance", "455"),
]

BASELINES = {
    "vector": ("Fixed-size vector input: fully connected feedforward network with piecewise linear units (ReLU, Leaky ReLU, PReLU, maxout); SGD with momentum and decaying learning rate, or Adam; early stopping; dropout; batch normalization if optimization fails", "440"),
    "image": ("Input with known topology (image): convolutional network with piecewise linear units; same optimizer/regularization; consider copying a known model or features from a CNN trained on ImageNet", "440-441"),
    "sequence": ("Sequence input or output: gated recurrent network (LSTM or GRU); same optimizer/regularization; in NLP unsupervised learning (word embeddings) usually helps", "440-441"),
}

HYPER = [
    ("Number of hidden units", "increases capacity when INCREASED", "time and memory cost rise in almost every operation"),
    ("Learning rate", "increases effective capacity when OPTIMALLY TUNED", "a bad value, high or low, yields low effective capacity through optimization failure"),
    ("Convolution kernel width", "increases capacity when INCREASED", "narrower output if there is no zero padding; more parameter memory"),
    ("Implicit zero padding", "increases capacity when INCREASED", "more time and memory"),
    ("Weight decay coefficient", "increases capacity when DECREASED", "frees the parameters to grow"),
    ("Dropout rate", "increases capacity when DECREASED", "dropping fewer units allows more 'conspiracy' among them to fit the training set"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tree", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--hyper", action="store_true")
    ap.add_argument("--baseline", choices=["vector", "image", "sequence"])
    ap.add_argument("--train-error", dest="train_error", type=float)
    ap.add_argument("--test-error", dest="test_error", type=float)
    ap.add_argument("--target", type=float)
    ap.add_argument("--bayes-error", dest="bayes_error", type=float)
    ap.add_argument("--regularized", choices=["yes", "no"])
    ap.add_argument("--data-cheap", dest="data_cheap", choices=["yes", "no"])
    ap.add_argument("--lr-state", dest="lr_state", choices=["ok", "diverges", "stuck"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.tree:
        print_tree(load())
        return 0
    if a.debug:
        for i, (txt, pg) in enumerate(DEBUG, 1):
            print(f"{i}. {txt} (DLB p.{pg})")
        print(AVISO)
        return 0
    if a.hyper:
        print("Table 11.1 (DLB p.446): effect of hyperparameters on capacity [from source]")
        for n, e, c in HYPER:
            print(f"- {n}: {e}; caveat: {c}")
        print(AVISO)
        return 0
    if a.baseline:
        txt, pg = BASELINES[a.baseline]
        print(f"Baseline [from source] (DLB p.{pg}): {txt}")
        print(AVISO)
        return 0
    if a.train_error is not None or a.test_error is not None or a.target is not None:
        return diagnose(a)
    if a.lr_state:
        return diagnose_lr(a)
    ap.print_help()
    return 1


def diagnose_lr(a):
    msgs = {"ok": "Adequate learning rate: follow the learning curves (DLB p.310, 445).",
            "diverges": "Violent oscillations/cost rising: learning rate too high; in the idealized quadratic case the error rises if eps >= 2x the optimum (DLB p.310, 444).",
            "stuck": "Slow or stuck training with high error: learning rate too low; the effect is poorly understood (it would not occur with a convex loss) (DLB p.444)."}
    print(msgs[a.lr_state])
    print(AVISO)
    return 0


if __name__ == "__main__":
    sys.exit(main())

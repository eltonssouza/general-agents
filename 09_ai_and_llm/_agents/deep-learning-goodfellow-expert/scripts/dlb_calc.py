# -*- coding: utf-8 -*-
"""
dlb_calc.py - small deterministic calculations based on "Deep Learning" (Goodfellow, Bengio, Courville, MIT Press, 2016; abbreviated DLB).

stdlib only (no numpy), no network, does not read target files (except JSON passed explicitly in grad-mlp/rnn).
Run with: python -I scripts/dlb_calc.py SUBCOMMAND [options] [--json]
Page convention: "DLB p.N" = PDF page (printed = PDF - 15, constant in the body).
Source labels in every output: [from source] (formula/value checked on the cited page), [inference] (direct derivation),
[extrapolation] (outside the book; only when indicated). The book is from 2016: default hyperparameter values are [DATED].

Subcommands:
  conv-out      convolution output size (valid/same/full, stride)                       DLB p.364, 363
  conv-cost     convolution cost vs dense matrix (the book example: 320x280)          DLB p.355
  params        parameter count: dense / sparse(k x n) / conv / mlp                    DLB p.350, 373, 188
  info          entropy, cross-entropy, KL (nats or bits)                               DLB p.88-90
  softmax       softmax and log-softmax: naive vs stable                                DLB p.96, 201
  activations   ReLU, leaky, sigmoid, tanh, softplus and derivatives                    DLB p.208-212
  xor           the book XOR network (W,c,w,b)                                          DLB p.189-191
  autodiff      backprop on a small scalar graph (expression) + numerical gradient      DLB p.224-225, 454
  grad-mlp      Algorithms 6.3/6.4 on a small MLP + finite-difference check              DLB p.227-228, 454
  metrics       precision, recall, F, accuracy, coverage                                DLB p.438-439
  ci            standard error and 95% CI                                               DLB p.143
  variance      variance estimators (1/m vs 1/(m-1)), bias                              DLB p.141-142
  ensemble      expected error of an ensemble of k models                               DLB p.271
  lr-schedule   linear learning rate decay                                              DLB p.310
  momentum      terminal velocity of momentum                                           DLB p.313
  optim         SGD/momentum/AdaGrad/RMSProp/Adam trajectory on a quadratic             DLB p.309-326
  clip          gradient norm clipping                                                  DLB p.429-430
  init          initialization bounds (1/sqrt(m) and Glorot)                            DLB p.318
  bn            batch normalization of one column                                       DLB p.334
  gcn           global contrast normalization                                              DLB p.470
  earlystop     early stopping (Algorithm 7.1)                                          DLB p.262
  search        grid search cost and random search samples                              DLB p.449-450
  condition     condition number and optimal step                                       DLB p.97, 103
  linadv        sensitivity of a linear function to perturbation (eps*||w||_1)          DLB p.284
  dropout       weight scaling rule                                                     DLB p.278
  rnn           one step/sequence of an RNN (eq. 10.8-10.11)                            DLB p.396
  lstm          one step of a scalar LSTM cell (eq. 10.40-10.44)                        DLB p.425-426
  normal-eq     linear regression via the normal equations                              DLB p.124
  kfold         k-fold partition                                                        DLB p.137-138
"""
import argparse
import ast
import cmath
import json
import math
import random
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

AVISO = "Source: formulas checked on the cited pages (PDF). 2016 book [DATED]: does not state the current state of the art."


def fl(s):
    return [float(x) for x in str(s).replace(";", ",").split(",") if x.strip() != ""]


def out(args, d, lines):
    if getattr(args, "json", False):
        print(json.dumps(d, ensure_ascii=False, indent=1))
    else:
        for l in lines:
            print(l)
        print(AVISO)
    return 0


# ---------------------------------------------------------------- convolution
def cmd_conv_out(a):
    m, k, s = a.m, a.k, a.stride
    if a.pad == "valid":
        base = m - k + 1
        orig = "[from source] valid: m-k+1 (DLB p.364)"
    elif a.pad == "same":
        base = m
        orig = "[from source] same: output with the input size (DLB p.364)"
    elif a.pad == "full":
        base = m + k - 1
        orig = "[from source] full: m+k-1 (DLB p.364)"
    else:
        raise SystemExit("pad must be valid|same|full")
    if base < 1:
        res = 0
    else:
        res = (base - 1) // s + 1
    lines = [f"input m={m}, kernel k={k}, padding={a.pad}, stride s={s}",
             f"width after convolution without stride: {base}  {orig}"]
    if s != 1:
        lines.append(f"width with stride {s}: {res}  [inference] the book defines stride as sampling every s positions (eq. 9.8, DLB p.363); ceil(base/s) follows from that definition")
    else:
        lines.append(f"output width: {res}")
    return out(a, {"base": base, "saida": res, "pad": a.pad, "stride": s}, lines)


def cmd_conv_cost(a):
    h, w, kh, kw = a.h, a.w, a.kh, a.kw
    oh, ow = h - kh + 1, w - kw + 1
    nk = kh * kw
    ops_conv = oh * ow * (2 * nk - 1)
    entries = (h * w) * (oh * ow)
    ops_dense = 2 * entries
    nz = nk * oh * ow
    lines = [f"image {w}x{h} (width x height), kernel {kh}x{kw} (height x width; {nk} elements), output {ow}x{oh} (valid)",
             f"operations per convolution: {ops_conv}  ({oh}*{ow}*{2*nk-1}; in the book example, 2 multiplications + 1 addition per pixel = 3) (DLB p.355)",
             f"entries of the equivalent dense matrix: {entries}  (({h}*{w})*({oh}*{ow}))",
             f"operations of the dense multiplication (~2 per entry): {ops_dense}",
             f"non-zero entries of the (sparse) matrix: {nz}",
             f"storage ratio dense/kernel: {entries / nk:.4g}; operations ratio dense/convolution: {ops_dense / ops_conv:.4g}",
             "Book example (DLB p.355): 320x280, 2-element kernel -> 319x280x3 = 267,960 ops; >8 billion entries; ~4 billion times (storage) and ~60,000 times (operations) [from source]; the generalization 2*nk-1 per pixel is [inference]."]
    return out(a, {"ops_conv": ops_conv, "entradas_densa": entries, "ops_densa": ops_dense, "nao_nulos": nz,
                   "razao_armazenamento": entries / nk, "razao_ops": ops_dense / ops_conv}, lines)


def cmd_params(a):
    if a.kind == "dense":
        n = a.m * a.n + (a.n if a.bias else 0)
        lines = [f"dense layer {a.m}->{a.n}: {n} parameters (m*n{' + n biases' if a.bias else ''}) [from source] m*n parameters, DLB p.350; bias per unit [inference]"]
        d = {"params": n}
    elif a.kind == "sparse":
        n = a.k * a.n
        lines = [f"sparse connectivity: each of the {a.n} outputs with {a.k} connections: {n} parameters (k*n) [from source] DLB p.350; with sharing (convolution) only {a.k} parameters per kernel (DLB p.353)"]
        d = {"params": n}
    elif a.kind == "conv":
        n = a.cout * a.cin * a.kh * a.kw
        b = a.cout if a.bias else 0
        lines = [f"convolution: {a.cin} channels -> {a.cout} channels, kernel {a.kh}x{a.kw}: {n} weights (tensor K_{{i,j,k,l}}, DLB p.363) + {b} biases (one per output channel, shared, DLB p.373) = {n + b}"]
        d = {"pesos": n, "biases": b, "params": n + b}
    elif a.kind == "mlp":
        sizes = [int(x) for x in a.layers.split(",")]
        tot = 0
        parts = []
        for i in range(len(sizes) - 1):
            p = sizes[i] * sizes[i + 1] + (sizes[i + 1] if a.bias else 0)
            tot += p
            parts.append(p)
        lines = [f"MLP {sizes}: parameters per layer {parts}; total {tot} [inference] h=g(W^T x + c), DLB p.188"]
        d = {"por_camada": parts, "params": tot}
    else:
        raise SystemExit("invalid kind")
    return out(a, d, lines)


# ---------------------------------------------------------------- information
def _norm(p):
    s = sum(p)
    if s <= 0 or any(x < 0 for x in p):
        raise SystemExit("invalid distribution")
    return [x / s for x in p]


def _xlogy(x, y):
    if x == 0:
        return 0.0
    if y <= 0:
        return float("inf")
    return x * math.log(y)


def cmd_info(a):
    p = _norm(fl(a.p))
    base = 2.0 if a.base == "2" else math.e
    unit = "bits" if a.base == "2" else "nats"
    conv = math.log(base)
    H = -sum(_xlogy(x, x) for x in p) / conv
    d = {"unidade": unit, "H_P": H}
    lines = [f"P={p}", f"entropy H(P) = {H:.10g} {unit}  [from source] H(x)=E[-log P(x)] (DLB p.89, eq. 3.49); convention 0 log 0 = 0 (DLB p.90)"]
    if a.q:
        q = _norm(fl(a.q))
        if len(q) != len(p):
            raise SystemExit("P and Q must have the same size")
        kl = sum(_xlogy(x, x) - _xlogy(x, y) for x, y in zip(p, q)) / conv
        klr = sum(_xlogy(y, y) - _xlogy(y, x) for x, y in zip(p, q)) / conv
        ce = -sum(_xlogy(x, y) for x, y in zip(p, q)) / conv
        d.update({"KL_PQ": kl, "KL_QP": klr, "CE_PQ": ce})
        lines += [f"Q={q}",
                  f"D_KL(P||Q) = {kl:.10g} {unit}  [from source] eq. 3.50, DLB p.89",
                  f"D_KL(Q||P) = {klr:.10g} {unit}  (KL is not symmetric, DLB p.89)",
                  f"cross-entropy H(P,Q) = {ce:.10g} {unit} = H(P)+D_KL(P||Q) [from source] eq. 3.51, DLB p.90"]
    return out(a, d, lines)


def _softmax(z):
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]


def _logsoftmax(z):
    m = max(z)
    lse = m + math.log(sum(math.exp(x - m) for x in z))
    return [x - lse for x in z]


def cmd_softmax(a):
    z = fl(a.z)
    try:
        e = [math.exp(x) for x in z]
        s = sum(e)
        naive = [x / s for x in e]
    except OverflowError:
        naive = "overflow (exp of a large value)"
    except ZeroDivisionError:
        naive = "division by zero (underflow of all exp)"
    st = _softmax(z)
    ls = _logsoftmax(z)
    lines = [f"z={z}",
             f"naive softmax exp(z_i)/sum exp(z_j): {naive}  [from source] p.96 (eq. 4.1)",
             f"stable softmax (z - max z): {st}  [from source] p.96, 201 (eq. 6.33)",
             f"stable log-softmax: {ls}  [from source] p.96, 200 (eq. 6.30: log softmax(z)_i = z_i - log sum exp z_j)"]
    return out(a, {"softmax": st, "log_softmax": ls, "ingenuo": naive if isinstance(naive, str) else list(naive)}, lines)


def _sig(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def _softplus(z):
    return max(z, 0.0) + math.log1p(math.exp(-abs(z)))


def cmd_activations(a):
    rows = []
    lines = []
    for z in fl(a.z):
        r = {"z": z,
             "relu": max(0.0, z), "relu_d": 1.0 if z > 0 else 0.0,
             "leaky": max(0.0, z) + a.alpha * min(0.0, z), "leaky_d": 1.0 if z > 0 else a.alpha,
             "sigmoid": _sig(z), "sigmoid_d": _sig(z) * (1 - _sig(z)),
             "tanh": math.tanh(z), "tanh_d": 1 - math.tanh(z) ** 2,
             "softplus": _softplus(z), "softplus_d": _sig(z),
             "tanh_ident": 2 * _sig(2 * z) - 1}
        rows.append(r)
        lines.append(f"z={z}: relu={r['relu']:.6g} (d={r['relu_d']}); leaky(a={a.alpha})={r['leaky']:.6g}; sigmoid={r['sigmoid']:.6g} (d={r['sigmoid_d']:.6g}); tanh={r['tanh']:.6g} (d={r['tanh_d']:.6g}); softplus={r['softplus']:.6g}; 2*sigmoid(2z)-1={r['tanh_ident']:.6g}")
    lines.append("Source: ReLU g(z)=max{0,z} DLB p.188, 208; leaky/PReLU alpha p.208; tanh(z)=2 sigmoid(2z)-1 p.210; softplus zeta(a)=log(1+e^a) p.212; ReLU derivative at z=0: the book says the left derivative is 0 and the right is 1 and that software returns one of them (p.207) - here we use 0 [inference]; analytic derivatives of sigmoid/tanh/softplus [extrapolation: elementary calculus, not printed on the cited pages].")
    return out(a, {"linhas": rows}, lines)


def cmd_xor(a):
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    W = [[1, 1], [1, 1]]
    c = [0, -1]
    w = [1, -2]
    b = 0
    outs = []
    lines = ["XOR network with W=[[1,1],[1,1]], c=[0,-1], w=[1,-2], b=0 (DLB p.189-191, eq. 6.3-6.6)"]
    for x in X:
        pre = [x[0] * W[0][j] + x[1] * W[1][j] + c[j] for j in range(2)]
        h = [max(0, v) for v in pre]
        y = sum(h[j] * w[j] for j in range(2)) + b
        outs.append(y)
        lines.append(f"x={x}: x^T W + c = {pre} -> h = {h} -> y = {y}")
    lines.append("Expected output [0,1,1,0] [from source] DLB p.191 (eq. 6.7-6.11)")
    return out(a, {"saidas": outs}, lines)


# ---------------------------------------------------------------- autodiff
class Node:
    __slots__ = ("op", "args", "val", "grad")

    def __init__(self, op, args, val):
        self.op, self.args, self.val, self.grad = op, args, val, 0.0


def _fwd(op, v):
    if op == "add":
        return v[0] + v[1]
    if op == "sub":
        return v[0] - v[1]
    if op == "mul":
        return v[0] * v[1]
    if op == "div":
        return v[0] / v[1]
    if op == "tanh":
        return math.tanh(v[0])
    if op == "sigmoid":
        return _sig(v[0])
    if op == "exp":
        return math.exp(v[0])
    if op == "log":
        return math.log(v[0])
    if op == "relu":
        return max(0.0, v[0])
    if op == "sq":
        return v[0] * v[0]
    if op == "neg":
        return -v[0]
    raise SystemExit(f"unknown operation: {op}")


def _partials(op, v, y):
    # partial derivatives du(i)/du(j) with respect to each parent (analytic, elementary calculus)
    if op == "add":
        return [1.0, 1.0]
    if op == "sub":
        return [1.0, -1.0]
    if op == "mul":
        return [v[1], v[0]]
    if op == "div":
        return [1.0 / v[1], -v[0] / (v[1] * v[1])]
    if op == "tanh":
        return [1.0 - y * y]
    if op == "sigmoid":
        return [y * (1.0 - y)]
    if op == "exp":
        return [y]
    if op == "log":
        return [1.0 / v[0]]
    if op == "relu":
        return [1.0 if v[0] > 0 else 0.0]
    if op == "sq":
        return [2.0 * v[0]]
    if op == "neg":
        return [-1.0]
    raise SystemExit(f"unknown operation: {op}")


def _build(expr, env):
    tree = ast.parse(expr, mode="eval").body
    nodes = []
    cache = {}

    def mk(op, args, val):
        n = Node(op, args, val)
        nodes.append(n)
        return n

    def go(t):
        if isinstance(t, ast.Name):
            if t.id not in cache:
                if t.id not in env:
                    raise SystemExit(f"variable without a value: {t.id}")
                cache[t.id] = mk("input:" + t.id, [], env[t.id])
            return cache[t.id]
        if isinstance(t, ast.Constant) and isinstance(t.value, (int, float)):
            return mk("const", [], float(t.value))
        if isinstance(t, ast.Call) and isinstance(t.func, ast.Name):
            args = [go(x) for x in t.args]
            return mk(t.func.id, args, _fwd(t.func.id, [x.val for x in args]))
        raise SystemExit("unsupported expression: use add/sub/mul/div/tanh/sigmoid/exp/log/relu/sq/neg, variables and numbers")

    root = go(tree)
    return nodes, root


def cmd_autodiff(a):
    env = {}
    for kv in a.vars.split(","):
        k, v = kv.split("=")
        env[k.strip()] = float(v)
    nodes, root = _build(a.expr, env)
    # Algorithm 6.2: grad_table[u(n)] <- 1; for j = n-1..1: grad[u(j)] = sum_i grad[u(i)] du(i)/du(j)
    root.grad = 1.0
    for n in reversed(nodes):
        if not n.args:
            continue
        ps = _partials(n.op, [x.val for x in n.args], n.val)
        for arg, p in zip(n.args, ps):
            arg.grad += n.grad * p
    grads = {}
    for n in nodes:
        if n.op.startswith("input:"):
            grads[n.op[6:]] = n.grad
    # numerical gradient (centered difference, eq. 11.7)
    eps = a.eps
    num = {}
    for k in env:
        e1 = dict(env)
        e2 = dict(env)
        e1[k] += eps / 2
        e2[k] -= eps / 2
        n1, r1 = _build(a.expr, e1)
        n2, r2 = _build(a.expr, e2)
        num[k] = (r1.val - r2.val) / eps
    lines = [f"f = {a.expr} em {env}", f"value f = {root.val}",
             "gradient by backpropagation on the graph (Algorithm 6.2, DLB p.225): " + str(grads),
             f"numerical gradient by centered difference eps={eps} (eq. 11.7, DLB p.454): {num}",
             "Chain rule: dz/dx = sum_j dz/dy_j dy_j/dx (eq. 6.45, DLB p.222). The local derivatives (tanh, sigmoid...) are elementary calculus [extrapolation]."]
    return out(a, {"valor": root.val, "grad": grads, "grad_numerico": num}, lines)


# ---------------------------------------------------------------- MLP
def _mlp_init(sizes, rng):
    Ws, bs = [], []
    for i in range(len(sizes) - 1):
        Ws.append([[rng.uniform(-0.5, 0.5) for _ in range(sizes[i])] for _ in range(sizes[i + 1])])
        bs.append([0.0] * sizes[i + 1])
    return Ws, bs


def _act(name, x):
    if name == "tanh":
        return math.tanh(x)
    if name == "relu":
        return max(0.0, x)
    if name == "sigmoid":
        return _sig(x)
    raise SystemExit("activation: tanh|relu|sigmoid")


def _dact(name, a_, h):
    if name == "tanh":
        return 1 - h * h
    if name == "relu":
        return 1.0 if a_ > 0 else 0.0
    return h * (1 - h)


def _forward(Ws, bs, x, act):
    hs = [x]
    as_ = []
    h = x
    L = len(Ws)
    for k in range(L):
        a_ = [bs[k][i] + sum(Ws[k][i][j] * h[j] for j in range(len(h))) for i in range(len(Ws[k]))]
        as_.append(a_)
        if k < L - 1:
            h = [_act(act, v) for v in a_]
        else:
            h = a_  # linear output layer (logits or mean)
        hs.append(h)
    return as_, hs


def _loss(Ws, bs, x, y, act, loss):
    _, hs = _forward(Ws, bs, x, act)
    o = hs[-1]
    if loss == "ce":
        return -_logsoftmax(o)[y]
    return 0.5 * sum((oi - yi) ** 2 for oi, yi in zip(o, y))


def _backprop(Ws, bs, x, y, act, loss):
    """Algorithm 6.3 (forward) and 6.4 (backward), DLB p.227-228, without regularizer."""
    as_, hs = _forward(Ws, bs, x, act)
    L = len(Ws)
    o = hs[-1]
    if loss == "ce":
        q = _softmax(o)
        g = [q[i] - (1.0 if i == y else 0.0) for i in range(len(q))]  # dJ/do = q - p (DLB p.237)
    else:
        g = [oi - yi for oi, yi in zip(o, y)]
    gW = [None] * L
    gb = [None] * L
    for k in range(L - 1, -1, -1):
        if k < L - 1:
            g = [g[i] * _dact(act, as_[k][i], hs[k + 1][i]) for i in range(len(g))]
        gb[k] = list(g)
        gW[k] = [[g[i] * hs[k][j] for j in range(len(hs[k]))] for i in range(len(g))]
        if k > 0:
            g = [sum(Ws[k][i][j] * g[i] for i in range(len(g))) for j in range(len(hs[k]))]
    return gW, gb


def cmd_grad_mlp(a):
    rng = random.Random(a.seed)
    sizes = [int(v) for v in a.layers.split(",")]
    Ws, bs = _mlp_init(sizes, rng)
    x = [rng.uniform(-1, 1) for _ in range(sizes[0])]
    y = rng.randrange(sizes[-1]) if a.loss == "ce" else [rng.uniform(-1, 1) for _ in range(sizes[-1])]
    gW, gb = _backprop(Ws, bs, x, y, a.act, a.loss)
    worst = 0.0
    eps = a.eps
    for k in range(len(Ws)):
        for i in range(len(Ws[k])):
            for j in range(len(Ws[k][i])):
                old = Ws[k][i][j]
                Ws[k][i][j] = old + eps / 2
                f1 = _loss(Ws, bs, x, y, a.act, a.loss)
                Ws[k][i][j] = old - eps / 2
                f2 = _loss(Ws, bs, x, y, a.act, a.loss)
                Ws[k][i][j] = old
                num = (f1 - f2) / eps
                worst = max(worst, abs(num - gW[k][i][j]) / max(1e-8, abs(num) + abs(gW[k][i][j])))
        for i in range(len(bs[k])):
            old = bs[k][i]
            bs[k][i] = old + eps / 2
            f1 = _loss(Ws, bs, x, y, a.act, a.loss)
            bs[k][i] = old - eps / 2
            f2 = _loss(Ws, bs, x, y, a.act, a.loss)
            bs[k][i] = old
            num = (f1 - f2) / eps
            worst = max(worst, abs(num - gb[k][i]) / max(1e-8, abs(num) + abs(gb[k][i])))
    lines = [f"MLP {sizes}, hidden activation {a.act}, loss {a.loss}, seed {a.seed}",
             f"largest relative error backprop vs centered difference (eps={eps}): {worst:.3e}",
             "OK: gradients consistent" if worst < 1e-5 else "ALERT: divergence - investigate (DLB p.453-454: the most common defect is a wrongly implemented gradient)",
             "Source: Algorithms 6.3/6.4 (DLB p.227-228); centered finite differences, eq. 11.7 (DLB p.454); for softmax+cross-entropy the gradient at z_i is q_i - p_i (DLB p.237)."]
    return out(a, {"erro_relativo_max": worst, "ok": worst < 1e-5}, lines)


# ---------------------------------------------------------------- metrics and statistics
def cmd_metrics(a):
    d = {}
    lines = []
    if a.tp is not None:
        tp, fp, fn = a.tp, a.fp or 0, a.fn or 0
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        f = 2 * p * r / (p + r) if p + r else 0.0
        d.update({"precision": p, "recall": r, "F": f})
        lines.append(f"precision = {p:.6g} (fraction of detections that were correct); recall = {r:.6g} (fraction of real events detected); F = 2pr/(p+r) = {f:.6g}  [from source] DLB p.438-439 (eq. 11.1)")
        if a.tn is not None:
            acc = (tp + a.tn) / (tp + fp + fn + a.tn)
            d["accuracy"] = acc
            lines.append(f"accuracy = {acc:.8g}  (with a rare event accuracy is misleading: DLB p.438)")
    if a.total is not None:
        cov = a.answered / a.total
        d["coverage"] = cov
        lines.append(f"coverage = {cov:.6g} (fraction of examples on which the system answers) [from source] DLB p.439")
        if a.correct is not None and a.answered:
            acc2 = a.correct / a.answered
            d["accuracy_respondidos"] = acc2
            lines.append(f"accuracy among those answered = {acc2:.6g}; Street View target: 98% accuracy with 95% coverage (DLB p.439)")
    if not d:
        raise SystemExit("provide --tp [--fp --fn --tn] and/or --answered --total [--correct]")
    return out(a, d, lines)


def cmd_ci(a):
    se = a.std / math.sqrt(a.m)
    lo, hi = a.mean - 1.96 * se, a.mean + 1.96 * se
    lines = [f"standard error of the mean SE = sigma/sqrt(m) = {se:.8g}  [from source] eq. 5.46, DLB p.143",
             f"95% CI = ({lo:.8g}, {hi:.8g})  [from source] eq. 5.47 (mean +- 1.96 SE), DLB p.143",
             "Book rule: A is better than B if the upper bound of the CI of A < the lower bound of the CI of B (DLB p.143); with cross-validation the CIs are not well justified (DLB p.138)."]
    return out(a, {"se": se, "ic95": [lo, hi]}, lines)


def cmd_variance(a):
    v = fl(a.values)
    m = len(v)
    mu = sum(v) / m
    ss = sum((x - mu) ** 2 for x in v)
    biased, unb = ss / m, ss / (m - 1) if m > 1 else float("nan")
    lines = [f"m={m}, media={mu:.8g}",
             f"sample variance (1/m) = {biased:.8g}  [from source] eq. 5.36; biased: bias = -sigma^2/m (DLB p.141-142)",
             f"unbiased estimator (1/(m-1)) = {unb:.8g}  [from source] eq. 5.40 (DLB p.142)"]
    return out(a, {"biased": biased, "unbiased": unb, "mean": mu}, lines)


def cmd_ensemble(a):
    k, v, c = a.k, a.v, a.c
    e = v / k + (k - 1) / k * c
    lines = [f"k={k} models, error variance v={v}, covariance c={c}",
             f"expected squared error of the ensemble = v/k + (k-1)c/k = {e:.8g}  [from source] eq. 7.51, DLB p.271",
             f"limits: c=v -> {v} (nothing improves); c=0 -> v/k = {v / k:.8g} (DLB p.271)"]
    return out(a, {"erro": e}, lines)


# ---------------------------------------------------------------- optimization
def cmd_lr_schedule(a):
    k = min(a.k, a.tau)
    alpha = k / a.tau
    eps = (1 - alpha) * a.eps0 + alpha * a.epst
    lines = [f"eps_k = (1-alpha) eps_0 + alpha eps_tau, alpha=k/tau = {alpha:.6g}, for k<=tau; after tau it stays constant at eps_tau",
             f"eps_{a.k} = {eps:.8g}  [from source] eq. 8.14, DLB p.310",
             "Book suggestions: tau ~ iterations for a few hundred passes over the training set; eps_tau ~ 1% of eps_0 (DLB p.310). Choosing eps_0 is more art than science."]
    return out(a, {"eps": eps}, lines)


def cmd_momentum(a):
    f = 1.0 / (1.0 - a.alpha)
    lines = [f"alpha={a.alpha}: terminal velocity = eps*||g||/(1-alpha); factor 1/(1-alpha) = {f:.8g}  [from source] eq. 8.17, DLB p.313 (alpha=0.9 -> 10x)"]
    return out(a, {"fator": f}, lines)


def cmd_optim(a):
    x = fl(a.x0)
    c = fl(a.curv)
    if len(c) == 1:
        c = c * len(x)
    n = len(x)
    lr = a.lr
    algo = a.algo
    v = [0.0] * n
    r = [0.0] * n
    s = [0.0] * n
    hist = []

    def f(xx):
        return 0.5 * sum(ci * xi * xi for ci, xi in zip(c, xx))

    for t in range(1, a.steps + 1):
        if algo == "nesterov":
            look = [xi + a.alpha * vi for xi, vi in zip(x, v)]
            g = [ci * li for ci, li in zip(c, look)]
        else:
            g = [ci * xi for ci, xi in zip(c, x)]
        if algo == "sgd":
            x = [xi - lr * gi for xi, gi in zip(x, g)]
        elif algo in ("momentum", "nesterov"):
            v = [a.alpha * vi - lr * gi for vi, gi in zip(v, g)]
            x = [xi + vi for xi, vi in zip(x, v)]
        elif algo == "adagrad":
            r = [ri + gi * gi for ri, gi in zip(r, g)]
            x = [xi - lr / (a.delta + math.sqrt(ri)) * gi for xi, ri, gi in zip(x, r, g)]
        elif algo == "rmsprop":
            r = [a.rho * ri + (1 - a.rho) * gi * gi for ri, gi in zip(r, g)]
            x = [xi - lr / math.sqrt(a.delta + ri) * gi for xi, ri, gi in zip(x, r, g)]
        elif algo == "adam":
            s = [a.rho1 * si + (1 - a.rho1) * gi for si, gi in zip(s, g)]
            r = [a.rho2 * ri + (1 - a.rho2) * gi * gi for ri, gi in zip(r, g)]
            sh = [si / (1 - a.rho1 ** t) for si in s]
            rh = [ri / (1 - a.rho2 ** t) for ri in r]
            x = [xi - lr * shi / (math.sqrt(rhi) + a.delta) for xi, shi, rhi in zip(x, sh, rh)]
        else:
            raise SystemExit("algo: sgd|momentum|nesterov|adagrad|rmsprop|adam")
        hist.append((t, list(x), f(x)))
    shown = hist[: min(3, len(hist))] + ([hist[-1]] if len(hist) > 3 else [])
    lines = [f"{algo} on f(x)=1/2 sum c_i x_i^2, c={c}, x0={fl(a.x0)}, lr={lr}, {a.steps} steps (exact gradient, no noise)"]
    for t, xx, ff in shown:
        lines.append(f"  step {t}: x={[round(v_, 10) for v_ in xx]} f={ff:.10g}")
    ref = {"sgd": "Alg. 8.1 (DLB p.309): theta <- theta - eps g",
           "momentum": "Alg. 8.2 (DLB p.313): v <- alpha v - eps g; theta <- theta + v",
           "nesterov": "Alg. with Nesterov: gradient at the interim point theta+alpha v (as in Alg. 8.6, DLB p.325)",
           "adagrad": "Alg. 8.4 (DLB p.323): r <- r + g.g; delta theta = -eps/(delta+sqrt r) g; delta ~1e-7",
           "rmsprop": "Alg. 8.5 (DLB p.324): r <- rho r + (1-rho) g.g; delta theta = -eps/sqrt(delta+r) g; delta ~1e-6",
           "adam": "Alg. 8.7 (DLB p.326): s,r with bias correction; delta theta = -eps s^/(sqrt(r^)+delta); suggested defaults eps=0.001, rho1=0.9, rho2=0.999, delta=1e-8 [DATED]"}[algo]
    lines.append("Source: " + ref)
    return out(a, {"final_x": hist[-1][1], "final_f": hist[-1][2], "trajetoria": [(t, xx, ff) for t, xx, ff in hist]}, lines)


def cmd_clip(a):
    g = fl(a.g)
    nrm = math.sqrt(sum(x * x for x in g))
    if nrm > a.v:
        g2 = [x * a.v / nrm for x in g]
        act = "clipped"
    else:
        g2 = g
        act = "unchanged"
    lines = [f"||g||={nrm:.8g}, threshold v={a.v}: {act}; g'={g2}",
             "Source: [from source] if ||g||>v then g <- g v/||g|| (eq. 10.48-10.49, DLB p.429-430); preserves the direction; does not help against vanishing gradients (DLB p.430)."]
    return out(a, {"norma": nrm, "g": g2, "clipado": nrm > a.v}, lines)


def cmd_init(a):
    u = 1.0 / math.sqrt(a.m)
    gl = math.sqrt(6.0 / (a.m + a.n))
    lines = [f"fully connected layer with m={a.m} inputs and n={a.n} outputs",
             f"heuristic U(-1/sqrt(m), 1/sqrt(m)): bound = {u:.8g}  [from source] DLB p.318",
             f"normalized initialization of Glorot & Bengio U(-sqrt(6/(m+n)), +sqrt(6/(m+n))): bound = {gl:.8g}  [from source] eq. 8.23, DLB p.318 (checked visually on the page)",
             "Book caveat: derived assuming a chain of matrix multiplications without nonlinearities (DLB p.318); other rules (for example ReLU variants) are not on these pages [DATED/NOT COVERED]."]
    return out(a, {"limite_1_sqrt_m": u, "limite_glorot": gl}, lines)


def cmd_bn(a):
    h = fl(a.h)
    m = len(h)
    mu = sum(h) / m
    sig = math.sqrt(a.delta + sum((x - mu) ** 2 for x in h) / m)
    hn = [(x - mu) / sig for x in h]
    out_ = [a.gamma * x + a.beta for x in hn]
    lines = [f"mu={mu:.8g}, sigma=sqrt(delta+var)={sig:.8g}, H'={[round(x, 8) for x in hn]}",
             f"gamma*H'+beta = {[round(x, 8) for x in out_]}",
             "Source: [from source] H'=(H-mu)/sigma; mu=(1/m)sum H_i; sigma=sqrt(delta + (1/m) sum (H-mu)^2), delta~1e-8 (eq. 8.35-8.37, DLB p.333-334, checked visually); gamma*H'+beta preserves expressive power (DLB p.335); at test time moving averages from training are used (DLB p.334)."]
    return out(a, {"mu": mu, "sigma": sig, "normalizado": hn, "saida": out_}, lines)


def cmd_gcn(a):
    x = fl(a.pixels)
    n = len(x)
    mean = sum(x) / n
    var = sum((v - mean) ** 2 for v in x) / n
    den = max(a.eps, math.sqrt(a.lam + var))
    y = [a.s * (v - mean) / den for v in x]
    lines = [f"mean={mean:.8g}, denominator=max(eps, sqrt(lambda+var))={den:.8g}; X'={[round(v, 8) for v in y]}",
             "Source: [from source] eq. 12.3, DLB p.470 (checked visually): X' = s (X - Xbar)/max{eps, sqrt(lambda + (1/3rc) sum (X-Xbar)^2)}; here the list is treated as the set of all 3rc entries."]
    return out(a, {"media": mean, "saida": y}, lines)


def cmd_earlystop(a):
    vals = fl(a.val)
    n, p = a.n, a.patience
    best = float("inf")
    best_i = 0
    j = 0
    i = 0
    stopped = None
    for idx, v in enumerate(vals):
        i += n
        if v < best:
            j = 0
            best = v
            best_i = i
        else:
            j += 1
        if j >= p:
            stopped = i
            break
    lines = [f"evaluations every n={n} steps, patience p={p}: best validation error {best} at i*={best_i} steps; stopped at {stopped if stopped is not None else 'not reached'}",
             "Source: [from source] Algorithm 7.1 (DLB p.262): keeps the parameters of the best validation error and stops after p evaluations without improvement; Alg. 7.2/7.3 (DLB p.263-264) describe how to reuse all the data."]
    return out(a, {"melhor": best, "i_star": best_i, "parou_em": stopped}, lines)


def cmd_search(a):
    grid = a.n ** a.m
    rng = random.Random(a.seed)
    samples = [10 ** rng.uniform(a.low, a.high) for _ in range(a.trials)]
    lines = [f"grid search: {a.m} hyperparameters with {a.n} values each -> n^m = {grid} training runs  [from source] O(n^m), DLB p.449",
             f"random search (seed {a.seed}): learning rate = 10^u({a.low},{a.high}) -> {[float('%.4g' % s) for s in samples]}  [from source] eq. 11.2-11.3, DLB p.449",
             "Random search does not discretize the values and avoids redundant runs when few hyperparameters matter (DLB p.448, 450)."]
    return out(a, {"grid": grid, "amostras": samples}, lines)


def cmd_condition(a):
    e = fl(a.eigs)
    mx = max(abs(x) for x in e)
    mn = min(abs(x) for x in e)
    cond = mx / mn if mn else float("inf")
    lines = [f"eigenvalues {e}: condition number max|li/lj| = {cond:.8g}  [from source] eq. 4.2, DLB p.97 (Fig. 4.6: Hessian with cond=5, DLB p.106)",
             f"if g is aligned with the eigenvector of the largest eigenvalue, optimal step eps* = g^T g/(g^T H g) = 1/lambda_max = {1.0 / max(e):.8g}  [from source] eq. 4.10, DLB p.103 (worst case)",
             "With poor conditioning the step must be small for the direction of greatest curvature and ends up too small in the others (DLB p.104)."]
    return out(a, {"cond": cond, "eps_star_pior_caso": 1.0 / max(e)}, lines)


def cmd_linadv(a):
    w = fl(a.w)
    l1 = sum(abs(x) for x in w)
    lines = [f"||w||_1 = {l1:.8g}; perturbing each entry by eps={a.eps} can change the linear function by up to eps*||w||_1 = {a.eps * l1:.8g}",
             "Source: [from source] DLB p.284 - excessive linearity is one of the causes of adversarial examples; the effect grows with dimension."]
    return out(a, {"max_mudanca": a.eps * l1}, lines)


def cmd_dropout(a):
    w = fl(a.w)
    sc = [x * a.p for x in w]
    lines = [f"inclusion prob. p={a.p}: output weights {w} -> {sc} at inference",
             "Source: [from source] weight scaling rule: multiply the weights leaving unit i by the inclusion probability (DLB p.278); with p=1/2 it is equivalent to halving the weights; exact for softmax regression and linear networks, approximate for nonlinear ones (DLB p.279)."]
    return out(a, {"pesos": sc}, lines)


def _vec_mat(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def cmd_rnn(a):
    if a.params:
        P = json.load(open(a.params, "r", encoding="utf-8"))
    else:
        P = {"U": [[1.0]], "W": [[0.5]], "V": [[2.0], [-1.0]], "b": [0.0], "c": [0.0, 0.0], "h0": [0.0], "xs": [[1.0], [1.0]]}
    U, W, V, b, c, h = P["U"], P["W"], P["V"], P["b"], P["c"], P["h0"]
    res = []
    for x in P["xs"]:
        a_ = [b[i] + _vec_mat(W, h)[i] + _vec_mat(U, x)[i] for i in range(len(b))]
        h = [math.tanh(v) for v in a_]
        o = [c[i] + _vec_mat(V, h)[i] for i in range(len(c))]
        yh = _softmax(o)
        res.append({"h": h, "o": o, "yhat": yh})
    lines = ["RNN with hidden-to-hidden recurrence: a=b+Wh+Ux; h=tanh(a); o=c+Vh; yhat=softmax(o)  [from source] eq. 10.8-10.11, DLB p.396 (checked visually)"]
    for t, r in enumerate(res, 1):
        lines.append(f"t={t}: h={r['h']} o={r['o']} yhat={r['yhat']}")
    lines.append("Training cost by BPTT: O(tau) in time and memory, not parallelizable (DLB p.396).")
    return out(a, {"passos": res}, lines)


def cmd_lstm(a):
    def cell(x, hp, sp):
        f = _sig(a.bf + a.uf * x + a.wf * hp)
        g = _sig(a.bg + a.ug * x + a.wg * hp)
        q = _sig(a.bo + a.uo * x + a.wo * hp)
        s = f * sp + g * _sig(a.b + a.u * x + a.w * hp)
        h = math.tanh(s) * q
        return f, g, q, s, h

    f, g, q, s, h = cell(a.x, a.h, a.s)
    lines = [f"f(forget)={f:.8g}, g(input)={g:.8g}, q(output)={q:.8g}",
             f"s(t) = f*s(t-1) + g*sigma(b+Ux+Wh) = {s:.8g}",
             f"h(t) = tanh(s) * q = {h:.8g}",
             "Source: [from source] eq. 10.40-10.44, DLB p.425-426 (checked visually); scalar cell, no peephole connections. Forget gate bias = 1 is recommended (DLB p.427)."]
    return out(a, {"f": f, "g": g, "q": q, "s": s, "h": h}, lines)


def _solve(A, b):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[piv][i]) < 1e-12:
            raise SystemExit("singular matrix: X^T X is not invertible (regularize: DLB p.254)")
        M[i], M[piv] = M[piv], M[i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for cidx in range(i, n + 1):
                M[r][cidx] -= f * M[i][cidx]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def cmd_normal_eq(a):
    xs = fl(a.x)
    ys = fl(a.y)
    rows = [[x, 1.0] if a.bias else [x] for x in xs]
    n = len(rows[0])
    XtX = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]
    Xty = [sum(r[i] * y for r, y in zip(rows, ys)) for i in range(n)]
    if a.alpha:
        for i in range(n):
            XtX[i][i] += a.alpha
    w = _solve(XtX, Xty)
    pred = [sum(wi * ri for wi, ri in zip(w, r)) for r in rows]
    mse = sum((p - y) ** 2 for p, y in zip(pred, ys)) / len(ys)
    lines = [f"weights {'[w, b]' if a.bias else '[w]'} = {w}; training MSE = {mse:.8g}",
             "Source: [from source] w = (X^T X)^-1 X^T y (normal equations, eq. 5.12, DLB p.124); with --alpha it uses (X^T X + alpha I), DLB p.254 (eq. 7.17 / pseudoinverse p.255)."]
    return out(a, {"w": w, "mse": mse}, lines)


def cmd_kfold(a):
    idx = list(range(a.n))
    if a.seed is not None:
        random.Random(a.seed).shuffle(idx)
    folds = [idx[i::a.k] for i in range(a.k)]
    lines = [f"{a.k} mutually exclusive folds of {a.n} examples (round-robin" + (f", shuffled with seed {a.seed}" if a.seed is not None else ", not shuffled") + "):"]
    for i, f in enumerate(folds, 1):
        lines.append(f"  fold {i}: test={sorted(f)}")
    lines.append("Source: [from source] Algorithm 5.1 (DLB p.138): for each i, train on D\\D_i and measure the error on D_i; the mean of the errors estimates the generalization error. How to partition (round-robin) is [inference]; shuffle first: DLB p.295.")
    return out(a, {"folds": [sorted(f) for f in folds]}, lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd")

    def add(name, fn, **kw):
        p = sp.add_parser(name)
        p.add_argument("--json", action="store_true")
        p.set_defaults(handler=fn)
        return p

    p = add("conv-out", cmd_conv_out)
    p.add_argument("--m", type=int, required=True)
    p.add_argument("--k", type=int, required=True)
    p.add_argument("--pad", default="valid")
    p.add_argument("--stride", type=int, default=1)
    p = add("conv-cost", cmd_conv_cost)
    p.add_argument("--h", type=int, default=280)
    p.add_argument("--w", type=int, default=320)
    p.add_argument("--kh", type=int, default=1)
    p.add_argument("--kw", type=int, default=2)
    p = add("params", cmd_params)
    p.add_argument("--kind", required=True)
    p.add_argument("--m", type=int, default=0)
    p.add_argument("--n", type=int, default=0)
    p.add_argument("--k", type=int, default=0)
    p.add_argument("--cin", type=int, default=0)
    p.add_argument("--cout", type=int, default=0)
    p.add_argument("--kh", type=int, default=0)
    p.add_argument("--kw", type=int, default=0)
    p.add_argument("--layers", default="")
    p.add_argument("--bias", action="store_true")
    p = add("info", cmd_info)
    p.add_argument("--p", required=True)
    p.add_argument("--q")
    p.add_argument("--base", default="e")
    p = add("softmax", cmd_softmax)
    p.add_argument("--z", required=True)
    p = add("activations", cmd_activations)
    p.add_argument("--z", required=True)
    p.add_argument("--alpha", type=float, default=0.01)
    add("xor", cmd_xor)
    p = add("autodiff", cmd_autodiff)
    p.add_argument("--expr", required=True)
    p.add_argument("--vars", required=True)
    p.add_argument("--eps", type=float, default=1e-6)
    p = add("grad-mlp", cmd_grad_mlp)
    p.add_argument("--layers", default="3,4,2")
    p.add_argument("--act", default="tanh")
    p.add_argument("--loss", default="ce")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--eps", type=float, default=1e-6)
    p = add("metrics", cmd_metrics)
    p.add_argument("--tp", type=float)
    p.add_argument("--fp", type=float)
    p.add_argument("--fn", type=float)
    p.add_argument("--tn", type=float)
    p.add_argument("--answered", type=float)
    p.add_argument("--total", type=float)
    p.add_argument("--correct", type=float)
    p = add("ci", cmd_ci)
    p.add_argument("--mean", type=float, required=True)
    p.add_argument("--std", type=float, required=True)
    p.add_argument("--m", type=int, required=True)
    p = add("variance", cmd_variance)
    p.add_argument("--values", required=True)
    p = add("ensemble", cmd_ensemble)
    p.add_argument("--k", type=int, required=True)
    p.add_argument("--v", type=float, required=True)
    p.add_argument("--c", type=float, required=True)
    p = add("lr-schedule", cmd_lr_schedule)
    p.add_argument("--eps0", type=float, required=True)
    p.add_argument("--epst", type=float, required=True)
    p.add_argument("--tau", type=int, required=True)
    p.add_argument("--k", type=int, required=True)
    p = add("momentum", cmd_momentum)
    p.add_argument("--alpha", type=float, required=True)
    p = add("optim", cmd_optim)
    p.add_argument("--algo", required=True)
    p.add_argument("--x0", default="1,1")
    p.add_argument("--curv", default="1,5")
    p.add_argument("--lr", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=10)
    p.add_argument("--alpha", type=float, default=0.9)
    p.add_argument("--rho", type=float, default=0.9)
    p.add_argument("--rho1", type=float, default=0.9)
    p.add_argument("--rho2", type=float, default=0.999)
    p.add_argument("--delta", type=float, default=1e-8)
    p = add("clip", cmd_clip)
    p.add_argument("--g", required=True)
    p.add_argument("--v", type=float, required=True)
    p = add("init", cmd_init)
    p.add_argument("--m", type=int, required=True)
    p.add_argument("--n", type=int, required=True)
    p = add("bn", cmd_bn)
    p.add_argument("--h", required=True)
    p.add_argument("--delta", type=float, default=1e-8)
    p.add_argument("--gamma", type=float, default=1.0)
    p.add_argument("--beta", type=float, default=0.0)
    p = add("gcn", cmd_gcn)
    p.add_argument("--pixels", required=True)
    p.add_argument("--s", type=float, default=1.0)
    p.add_argument("--lam", type=float, default=0.0)
    p.add_argument("--eps", type=float, default=1e-8)
    p = add("earlystop", cmd_earlystop)
    p.add_argument("--val", required=True)
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--patience", type=int, default=3)
    p = add("search", cmd_search)
    p.add_argument("--m", type=int, required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--trials", type=int, default=5)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--low", type=float, default=-5)
    p.add_argument("--high", type=float, default=-1)
    p = add("condition", cmd_condition)
    p.add_argument("--eigs", required=True)
    p = add("linadv", cmd_linadv)
    p.add_argument("--w", required=True)
    p.add_argument("--eps", type=float, required=True)
    p = add("dropout", cmd_dropout)
    p.add_argument("--w", required=True)
    p.add_argument("--p", type=float, default=0.5)
    p = add("rnn", cmd_rnn)
    p.add_argument("--params")
    p = add("lstm", cmd_lstm)
    for nm in ("bf", "uf", "wf", "bg", "ug", "wg", "bo", "uo", "wo", "b", "u", "w"):
        p.add_argument("--" + nm, type=float, default=0.0)
    p.add_argument("--x", type=float, default=0.0)
    p.add_argument("--h", type=float, default=0.0)
    p.add_argument("--s", type=float, default=0.0)
    p = add("normal-eq", cmd_normal_eq)
    p.add_argument("--x", required=True)
    p.add_argument("--y", required=True)
    p.add_argument("--bias", action="store_true")
    p.add_argument("--alpha", type=float, default=0.0)
    p = add("kfold", cmd_kfold)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--k", type=int, required=True)
    p.add_argument("--seed", type=int)

    a = ap.parse_args()
    if not getattr(a, "handler", None):
        ap.print_help()
        return 1
    return a.handler(a)


if __name__ == "__main__":
    sys.exit(main())

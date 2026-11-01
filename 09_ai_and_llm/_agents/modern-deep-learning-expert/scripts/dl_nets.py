# -*- coding: utf-8 -*-
"""
dl_nets.py - mini-implementations (pure stdlib, Python lists, no numpy, no network) checked against the text of
"Understanding Deep Learning" (UDL) e "Neural Networks and Deep Learning" (NNDL).

Usage: python -I scripts/dl_nets.py SUBCOMMAND [options]
Page convention: PDF (the "=== PAGE N ===" marker). UDL: printed = PDF - 14. NNDL: PDF only.
Labels: [from source] / [inference] / [extrapolation] (see dl_calc.py).

Subcommands:
  backprop-check   gradient by backprop (NNDL BP1-BP4, p.66-68; UDL eq.7.24, p.120) vs finite differences (NNDL eq.46, p.78)
  attention        dot-product self-attention (UDL p.222-228) on small lists; --mask for masked attention (p.237)
  route            routing by given attention weights (UDL p.223, Fig.12.1: 0.1/0.3/0.6)
  toy-neuron       single-input neuron: quadratic cost vs cross-entropy (NNDL p.86-93)
  universality     network of steps/bumps from ch.4 (NNDL p.191-203) approximating f(x)=0.2+0.4x^2+0.3x sin(15x)+0.05 cos(50x)
  cnn-shapes       shapes and parameters of the NNDL ch.6 convolutional network (p.255-257) and the UDL MNIST-1D network (p.181)
"""
import argparse
import math
import random
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def sigmoid_prime(z):
    s = sigmoid(z)
    return s * (1 - s)


def relu(z):
    return z if z > 0 else 0.0


# ======================================================================= small network
def matvec(W, v):
    return [sum(w * x for w, x in zip(row, v)) for row in W]


def init_net(sizes, rnd, scale=1.0):
    Ws = [[[rnd.gauss(0, scale) for _ in range(a)] for _ in range(b)] for a, b in zip(sizes[:-1], sizes[1:])]
    bs = [[rnd.gauss(0, scale) for _ in range(b)] for b in sizes[1:]]
    return Ws, bs


def forward(Ws, bs, x, act):
    zs, hs = [], [x]
    h = x
    for k, (W, b) in enumerate(zip(Ws, bs)):
        z = [s + bb for s, bb in zip(matvec(W, h), b)]
        zs.append(z)
        last = (k == len(Ws) - 1)
        if act == "sigmoid":
            h = [sigmoid(v) for v in z]          # NNDL: sigmoid also at the output (p.60-61)
        else:
            h = z if last else [relu(v) for v in z]  # UDL: linear output (eq.4.15, p.62)
        hs.append(h)
    return zs, hs


def cost(Ws, bs, x, y, act):
    _, hs = forward(Ws, bs, x, act)
    return 0.5 * sum((a - b) ** 2 for a, b in zip(hs[-1], y))   # NNDL eq.26/p.66: C_x = 1/2 ||y-a||^2 (UDL uses a sum of squares without 1/2; constant factor)


def backprop(Ws, bs, x, y, act):
    """Returns (grad_W, grad_b) of the cost 1/2||y-a||^2.
    sigmoid -> NNDL: BP1 delta^L=(a-y)*sigma'(z^L); BP2 delta^l=(W^{l+1})^T delta^{l+1} * sigma'(z^l); BP3 dC/db=delta; BP4 dC/dW = delta (a^{l-1})^T
    relu    -> UDL eq.7.24 (p.120): d/df_{k-1} = I[f_{k-1}>0] * (Omega_k^T d/df_k); dl/dbeta_k = d/df_k; dl/dOmega_k = (d/df_k) h_k^T"""
    zs, hs = forward(Ws, bs, x, act)
    L = len(Ws)
    deltas = [None] * L
    if act == "sigmoid":
        deltas[-1] = [(a - t) * sigmoid_prime(z) for a, t, z in zip(hs[-1], y, zs[-1])]
    else:
        deltas[-1] = [a - t for a, t in zip(hs[-1], y)]
    for l in range(L - 2, -1, -1):
        Wn = Ws[l + 1]
        back = [sum(Wn[j][i] * deltas[l + 1][j] for j in range(len(Wn))) for i in range(len(Wn[0]))]
        if act == "sigmoid":
            deltas[l] = [bk * sigmoid_prime(z) for bk, z in zip(back, zs[l])]
        else:
            deltas[l] = [bk * (1.0 if z > 0 else 0.0) for bk, z in zip(back, zs[l])]
    gW = [[[d * h for h in hs[l]] for d in deltas[l]] for l in range(L)]
    gb = [list(d) for d in deltas]
    return gW, gb


def finite_diff(Ws, bs, x, y, act, eps=1e-6):
    """NNDL eq.46 (p.78) in the central version (more accurate): [C(w+eps)-C(w-eps)]/(2 eps)."""
    gW = []
    for l in range(len(Ws)):
        layer = []
        for j in range(len(Ws[l])):
            row = []
            for i in range(len(Ws[l][j])):
                w0 = Ws[l][j][i]
                Ws[l][j][i] = w0 + eps
                cp = cost(Ws, bs, x, y, act)
                Ws[l][j][i] = w0 - eps
                cm = cost(Ws, bs, x, y, act)
                Ws[l][j][i] = w0
                row.append((cp - cm) / (2 * eps))
            layer.append(row)
        gW.append(layer)
    gb = []
    for l in range(len(bs)):
        layer = []
        for j in range(len(bs[l])):
            b0 = bs[l][j]
            bs[l][j] = b0 + eps
            cp = cost(Ws, bs, x, y, act)
            bs[l][j] = b0 - eps
            cm = cost(Ws, bs, x, y, act)
            bs[l][j] = b0
            layer.append((cp - cm) / (2 * eps))
        gb.append(layer)
    return gW, gb


def cmd_backprop_check(a):
    sizes = [int(v) for v in a.arch.split(",")]
    rnd = random.Random(a.seed)
    Ws, bs = init_net(sizes, rnd, a.scale)
    x = [rnd.uniform(-1, 1) for _ in range(sizes[0])]
    y = [rnd.uniform(0, 1) for _ in range(sizes[-1])]
    gW, gb = backprop(Ws, bs, x, y, a.act)
    fW, fb = finite_diff(Ws, bs, x, y, a.act)
    errs = []
    for l in range(len(gW)):
        for j in range(len(gW[l])):
            for i in range(len(gW[l][j])):
                errs.append(abs(gW[l][j][i] - fW[l][j][i]))
        for j in range(len(gb[l])):
            errs.append(abs(gb[l][j] - fb[l][j]))
    n = sum(len(r) for l in gW for r in l) + sum(len(b) for b in gb)
    print("[from source] NNDL p.66-68 (BP1-BP4), p.73 (algoritmo); UDL p.120 eq.7.24; numerical gradient: NNDL p.78 eq.46")
    print(f"activation={a.act}, architecture={sizes}, parameters compared={n}, seed={a.seed}")
    print(f"max absolute error backprop vs finite differences = {max(errs):.3e}")
    if a.act == "relu":
        print("(ReLU: gradient undefined exactly at z=0; with random data this does not occur)")


# ======================================================================= attention
def softmax(z):
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [v / s for v in e]


def attention(X, Omega_q=None, Omega_k=None, Omega_v=None, scale=True, mask=False):
    """X: list of N tokens (each a list of D). Code convention = tokens in rows;
    UDL uses columns (D x N) and Sa[X] = V softmax[K^T Q / sqrt(Dq)] (eq.12.8-12.9, p.227-228): softmax per COLUMN of K^T Q,
    that is, for each query n, softmax over the keys m. Here: a[m,n] = softmax_m(k_m . q_n / sqrt(Dq)); output_n = sum_m a[m,n] v_m."""
    N, D = len(X), len(X[0])
    I = [[1.0 if i == j else 0.0 for j in range(D)] for i in range(D)]
    Q = [matvec(Omega_q or I, x) for x in X]
    K = [matvec(Omega_k or I, x) for x in X]
    V = [matvec(Omega_v or I, x) for x in X]
    dq = len(Q[0])
    out, A = [], []
    for n in range(N):
        sc = [sum(k * q for k, q in zip(K[m], Q[n])) / (math.sqrt(dq) if scale else 1.0) for m in range(N)]
        if mask:
            sc = [s if m <= n else -math.inf for m, s in enumerate(sc)]   # UDL p.237: -inf before the softmax
        w = softmax([s if s != -math.inf else -1e300 for s in sc]) if not mask else softmax_masked(sc)
        A.append(w)
        out.append([sum(w[m] * V[m][d] for m in range(N)) for d in range(len(V[0]))])
    return out, A


def softmax_masked(sc):
    m = max(s for s in sc if s != -math.inf)
    e = [0.0 if s == -math.inf else math.exp(s - m) for s in sc]
    t = sum(e)
    return [v / t for v in e]


def parse_tokens(s):
    return [[float(v) for v in tok.split(",")] for tok in s.split(";")]


def cmd_attention(a):
    X = parse_tokens(a.tokens)
    out, A = attention(X, scale=not a.noscale, mask=a.mask)
    print("[from source] UDL p.222-228 eq.12.2-12.9: v_m=beta_v+Omega_v x_m; q,k analogous; a[x_m,x_n]=softmax_m(k_m^T q_n [/sqrt(Dq)]); sa_n=sum_m a[x_m,x_n] v_m")
    print("(here Omega=I and beta=0 for an example on small lists [inference]; the book gives no numeric attention example beyond Fig.12.1)")
    if a.mask:
        print("[from source] UDL p.237: masked attention = future dot products set to -infinity before the softmax (zero weight)")
    for n, (w, o) in enumerate(zip(A, out)):
        print(f"  query {n}: weights over the keys = " + ", ".join(f"{v:.6f}" for v in w) + f" (sum {sum(w):.6f}) -> output " + ", ".join(f"{v:.6f}" for v in o))
    if a.perm_check:
        perm = list(reversed(range(len(X))))
        out2, _ = attention([X[i] for i in perm], scale=not a.noscale, mask=a.mask)
        ok = all(abs(out2[i][d] - out[perm[i]][d]) < 1e-12 for i in range(len(X)) for d in range(len(out[0])))
        print(f"permutation equivariance (UDL p.227): {'confirmed' if ok else 'FAILED'}" + ("" if not a.mask else " (does not hold with a causal mask, as expected)"))


def cmd_route(a):
    w = [float(v) for v in a.weights.split(",")]
    V = parse_tokens(a.values)
    s = sum(w)
    out = [sum(wi * v[d] for wi, v in zip(w, V)) for d in range(len(V[0]))]
    print("[from source] UDL p.208-209 (Fig.12.1, p.223): output = weighted sum of the values with weights >=0 summing to 1 (e.g., 0.1; 0.3; 0.6)")
    print(f"sum of weights = {s:.6f}; output = " + ", ".join(f"{v:.6f}" for v in out))


# ======================================================================= toy neuron (NNDL ch.3)
def toy(w, b, eta, epochs, cost_name, x=1.0, y=0.0):
    hist = []
    for ep in range(epochs + 1):
        z = w * x + b
        a_ = sigmoid(z)
        hist.append((ep, w, b, a_))
        if cost_name == "quadratic":
            d = (a_ - y) * sigmoid_prime(z)      # NNDL eq.55-56
        else:
            d = (a_ - y)                         # NNDL eq.61-62 (cross-entropy)
        w -= eta * d * x
        b -= eta * d
    return hist


def cmd_toy(a):
    h = toy(a.w, a.b, a.eta, a.epochs, a.cost)
    print("[from source] NNDL p.86-93: 1-input neuron, x=1, y=0; w=0.6 and b=0.9 -> initial output 0.82 (p.86); w=b=2.0 -> 0.98 (p.87); quadratic η=0.15 (p.86); cross-entropy η=0.005 (p.93)")
    print(f"cost={a.cost}, eta={a.eta}, epochs={a.epochs}")
    marks = sorted(set([0, 1, 10, 50, 100, 150, 200, 300, a.epochs]))
    for ep in marks:
        if ep <= a.epochs:
            e, w, b, o = h[ep]
            print(f"  epoch {e}: w={w:.6f} b={b:.6f} output={o:.6f}")
    if a.find_below is not None:
        for e, w, b, o in h:
            if o <= a.find_below:
                print(f"output <= {a.find_below} for the first time at epoch {e}")
                break
        else:
            print(f"output did not reach {a.find_below} in {a.epochs} epochs")


# ======================================================================= universality (NNDL ch.4)
def f_target(x):
    return 0.2 + 0.4 * x * x + 0.3 * x * math.sin(15 * x) + 0.05 * math.cos(50 * x)


def logit(p):
    return math.log(p / (1 - p))


def build_bump_net(N, wbig=None):
    """N neuron pairs (steps at s_k, s_{k+1}); output weights +h_k and -h_k (NNDL p.196-203).
    Target weighted output = sigma^{-1}(f(x)) (p.201); network output = sigma(sum + b_out) with b_out=0 (p.203)."""
    if wbig is None:
        wbig = max(1000.0, 100.0 * N * N)   # larger w for larger N, so the step's failure window stays smaller than the bump width (NNDL p.214-217)
    steps = [k / N for k in range(N)] + [1.0]
    hs = []
    for k in range(N):
        xm = (steps[k] + steps[k + 1]) / 2
        hs.append(logit(f_target(xm)))
    return steps, hs, wbig


def net_out(x, steps, hs, wbig):
    tot = 0.0
    N = len(hs)
    for k in range(N):
        s1 = sigmoid(wbig * (x - steps[k]))
        s2 = sigmoid(wbig * (x - steps[k + 1])) if k + 1 < N else 0.0   # the last bump extends to x=1 (step outside the domain)
        tot += hs[k] * (s1 - s2)
    return sigmoid(tot)


def cmd_universality(a):
    xs = [(i + 0.5) / 2000 for i in range(2000)]
    print("[from source] NNDL p.187-203: a step at s=-b/w (p.194); a neuron pair with weights +h and -h = bump (p.196); N bumps = lookup table of sigma^{-1}(f) (p.201-203); w=1000, b=-ws (p.202)")
    print("target function (render p.200): f(x)=0.2+0.4x^2+0.3 x sin(15x)+0.05 cos(50x), x in [0,1]")
    prev = None
    for N in [int(v) for v in a.N.split(",")]:
        steps, hs, wbig = build_bump_net(N)
        err = max(abs(net_out(x, steps, hs, wbig) - f_target(x)) for x in xs)
        mean = sum(abs(net_out(x, steps, hs, wbig) - f_target(x)) for x in xs) / len(xs)
        print(f"  N={N:>4} neuron pairs ({2 * N} hidden), w={wbig:g}: max error = {err:.4f}; mean error = {mean:.4f}")
        prev = err
    return prev


# ======================================================================= CNN shapes
def cmd_cnn_shapes(a):
    if a.preset == "nndl-ch6":
        print("[from source] NNDL p.255-257: conv(20 maps,5x5)+pool 2x2 -> conv(40 maps, 20 channels, 5x5)+pool 2x2 -> FC(40*4*4 -> 100) -> softmax(100 -> 10); input 28x28")
        n = 28
        c = 1
        total = 0
        for co, k in ((20, 5), (40, 5)):
            n = n - k + 1
            p = co * c * k * k + co
            total += p
            print(f"  conv {c}->{co} channels, k={k}: output {n}x{n}; parameters {p}")
            n //= 2
            print(f"  pool 2x2: {n}x{n}")
            c = co
        fin = c * n * n
        print(f"  vector for the FC: {c}*{n}*{n} = {fin}  (book: n_in=40*4*4, p.256)")
        fc = fin * 100 + 100
        sm = 100 * 10 + 10
        total += fc + sm
        print(f"  FC {fin}->100: {fc}; softmax 100->10: {sm}; TOTAL {total}")
    else:
        print("[from source] UDL p.181-184: MNIST-1D input 40; 3 conv layers (15 channels, k=3, stride 2, 'valid') -> 19, 9, 4 positions; FC 60 -> 10; 2,050 parameters (conv) vs 59,065 (FC 285,135,60)")
        n, c, total = 40, 1, 0
        for _ in range(3):
            n = (n - 3) // 2 + 1
            p = c * 15 * 3 + 15
            total += p
            print(f"  conv {c}->15 channels, k=3, s=2: {n} positions; parameters {p}")
            c = 15
        fin = c * n
        fc = fin * 10 + 10
        total += fc
        print(f"  FC {fin}->10: {fc}; TOTAL {total}")
        fcnet = [40, 285, 135, 60, 10]
        t2 = sum(x * y + y for x, y in zip(fcnet[:-1], fcnet[1:]))
        print(f"  equivalent fully connected network {fcnet}: {t2} parameters")


def build():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("backprop-check"); s.add_argument("--arch", default="3,4,2"); s.add_argument("--act", choices=["sigmoid", "relu"], default="sigmoid"); s.add_argument("--seed", type=int, default=1); s.add_argument("--scale", type=float, default=0.8); s.set_defaults(f=cmd_backprop_check)
    s = sp.add_parser("attention"); s.add_argument("--tokens", required=True, help="tokens separated by ';', components by ','"); s.add_argument("--noscale", action="store_true"); s.add_argument("--mask", action="store_true"); s.add_argument("--perm-check", action="store_true"); s.set_defaults(f=cmd_attention)
    s = sp.add_parser("route"); s.add_argument("--weights", required=True); s.add_argument("--values", required=True); s.set_defaults(f=cmd_route)
    s = sp.add_parser("toy-neuron"); s.add_argument("--w", type=float, default=0.6); s.add_argument("--b", type=float, default=0.9); s.add_argument("--eta", type=float, default=0.15); s.add_argument("--epochs", type=int, default=300); s.add_argument("--cost", choices=["quadratic", "cross-entropy"], default="quadratic"); s.add_argument("--find-below", type=float, dest="find_below"); s.set_defaults(f=cmd_toy)
    s = sp.add_parser("universality"); s.add_argument("--N", default="5,20,100"); s.set_defaults(f=cmd_universality)
    s = sp.add_parser("cnn-shapes"); s.add_argument("--preset", choices=["nndl-ch6", "udl-mnist1d"], default="nndl-ch6"); s.set_defaults(f=cmd_cnn_shapes)
    return p


def main(argv=None):
    a = build().parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()

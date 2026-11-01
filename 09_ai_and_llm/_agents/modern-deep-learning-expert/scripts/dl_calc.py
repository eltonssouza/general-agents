# -*- coding: utf-8 -*-
"""
dl_calc.py - deterministic calculators (stdlib, no network, no numpy) for formulas from
"Understanding Deep Learning" (Prince, 2023; UDL) e "Neural Networks and Deep Learning" (Nielsen; NNDL).

Usage: python -I scripts/dl_calc.py SUBCOMMAND [options]
Page convention: PDF (the "=== PAGE N ===" marker of the extracted text). UDL: printed page = PDF - 14. NNDL: PDF only.
Each output carries: the formula, the page(s) where it was read/checked, and a source label
  [from source]      formula/number present on the cited page
  [inference]    our direct deduction/derivation, checked numerically here (not printed in the book)
  [extrapolation]  assumption outside the collection (e.g., GPT-3 vocabulary, 4x MLP)

Subcommands:
  mlp-params      parameters of a fully connected MLP (UDL p.62-63; NNDL p.40)
  regions         linear regions, shallow vs deep (UDL p.64, p.67)
  conv-params     parameters of a convolutional layer (UDL p.181, p.184; NNDL p.248)
  conv-out        output size of convolution/pooling (UDL p.177-179, 181; NNDL p.245) [inference]
  init-var        initialization variance (UDL p.124-125; NNDL p.141)
  sum-var         standard deviation of z = sum w x + b (NNDL p.140-141)
  var-prop        simulation of activation variance with ReLU (UDL p.124 Fig.7.7)
  sigmoid-chain   product of w*sigma'(z) (NNDL p.233-235)
  xfmr-params     transformer parameter count (UDL p.233, p.238) [inference/extrapolation]
  diffusion       noise schedule, kernel, posterior and eps identity (UDL p.363-369, 374-376)
  kl-normal       KL between diagonal normals (UDL p.350, p.475)
  divergence      discrete KL, JS, 1D Wasserstein (UDL p.295, p.297-298, p.474)
  xent            softmax, multiclass and binary cross-entropy (UDL p.80-83; NNDL p.89-90, p.101)
  momentum-equiv  numerical equivalence of UDL and NNDL momentum (UDL p.100; NNDL p.176) [inference]
  adam-step       Adam steps with bias correction (UDL p.102-104)
  l2-equiv        weight decay: UDL vs NNDL L2 (UDL p.154, p.169-170; NNDL p.116) [inference]
  returns         discounted return and TD update (UDL p.388, p.398)
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


def ints(s):
    return [int(x) for x in s.replace(" ", "").split(",") if x != ""]


def floats(s):
    return [float(x) for x in s.replace(" ", "").split(",") if x != ""]


# ------------------------------------------------------------------ mlp-params
def mlp_params(sizes):
    """sizes = [Di, D1, ..., DK, Do]; weights Omega_k of size D_{k+1} x D_k and biases beta_k (UDL p.62-63)."""
    tot = 0
    rows = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        w, bb = a * b, b
        rows.append((a, b, w, bb))
        tot += w + bb
    return tot, rows


def cmd_mlp_params(a):
    tot, rows = mlp_params(ints(a.sizes))
    print("MLP: weights Omega_k (D_{k+1} x D_k) + biases beta_k  [from source] UDL p.62-63 (eq.4.15); NNDL p.40 (w^l, b^l)")
    for i, (x, y, w, b) in enumerate(rows):
        print(f"  layer {i}: {x} -> {y}: weights {w} + biases {b} = {w + b}")
    print(f"TOTAL {tot}")


# ------------------------------------------------------------------ regions
def cmd_regions(a):
    D, K, Di = a.D, a.K, a.Di
    print("[from source] UDL p.64: shallow (Di=1, D>2): D+1 regions, 3D+1 parameters; deep with K layers: up to (D+1)^K regions, 3D+1+(K-1)D(D+1) parameters")
    if Di == 1:
        sh_reg, sh_par = D + 1, 3 * D + 1
        dp_reg, dp_par = (D + 1) ** K, 3 * D + 1 + (K - 1) * D * (D + 1)
        print(f"shallow D={D}: regions<= {sh_reg}, parameters {sh_par}")
        print(f"deep D={D}, K={K}: regions<= {dp_reg}, parameters {dp_par}")
    else:
        par = (Di * D + D) + (K - 1) * (D * D + D) + (D + 1)
        shallow_regions = sum(math.comb(D, j) for j in range(0, Di + 1))
        print(f"parameters (Di={Di}, K={K}, D={D}, Do=1): {par}  [inference: direct count]")
        print(f"shallow (K=1): regions <= sum_j C(D,j), j<=Di = {shallow_regions}  [from source] UDL p.52 (Zaslavsky)")
        if D % Di == 0:
            Nr = (D // Di + 1) ** (Di * (K - 1)) * shallow_regions
            print(f"eq.4.17 (D a multiple of Di): Nr = (D/Di+1)^(Di(K-1)) * sum_j C(D,j) = {Nr}  [from source] UDL p.67; order of magnitude 1e{len(str(Nr)) - 1}")
        else:
            print("eq.4.17 requires D to be an integer multiple of Di (UDL p.67)")


# ------------------------------------------------------------------ conv params
def conv_params(ci, co, k, dims):
    w = ci * co * (k ** dims)
    return w, co, w + co


def cmd_conv_params(a):
    w, b, t = conv_params(a.ci, a.co, a.k, a.dims)
    print("[from source] UDL p.181 (1D: Ci*Co*K weights, Co biases), p.184 (2D: Ci*Co*K*K, Co biases); NNDL p.248 (K*K+1 per map)")
    print(f"weights {w} + biases {b} = {t}")


# ------------------------------------------------------------------ conv-out
def conv_out(n, k, pad=0, stride=1, dilation=1):
    eff = dilation * (k - 1) + 1
    return (n + 2 * pad - eff) // stride + 1


def cmd_conv_out(a):
    o = conv_out(a.n, a.k, a.pad, a.stride, a.dilation)
    print("[inference] size = floor((n+2p-d(k-1)-1)/s)+1 ; the book describes padding/stride/dilation (UDL p.178-179) and gives numeric cases (UDL p.181: 40 -> 19 with k=3, s=2, 'valid'; NNDL p.245: 28 -> 24 with a 5x5 field)")
    print(f"output = {o}")


# ------------------------------------------------------------------ init-var
def cmd_init_var(a):
    rules = {
        "he": (2.0 / a.fan_in, "UDL p.124 eq.7.31: sigma^2 = 2/Dh (Dh = source dimension; ReLU; biases 0)"),
        "backward": (2.0 / a.fan_out, "UDL p.125 eq.7.32: sigma^2 = 2/Dh' (destination dimension)"),
        "avg": (4.0 / (a.fan_in + a.fan_out), "UDL p.125 eq.7.33: sigma^2 = 4/(Dh+Dh')"),
        "nndl": (1.0 / a.fan_in, "NNDL p.141: weights ~ N(0, 1/n_in) (std 1/sqrt(n_in)); biases N(0,1)"),
        "nndl-large": (1.0, "NNDL p.139-140/p.146: old N(0,1) initialization"),
    }
    v, src = rules[a.rule]
    print(f"[from source] {src}")
    print(f"variance = {v:.6g}; standard deviation = {math.sqrt(v):.6g}")


def cmd_sum_var(a):
    var = a.active * a.var_w + a.var_b
    print("[from source] NNDL p.140-141: with n_in=1000, half active (500): N(0,1) -> sqrt(501)~22.4; N(0,1/n_in) -> sqrt(3/2)~1.22")
    print(f"variance of z = {var:.6g}; standard deviation = {math.sqrt(var):.6g}")


# ------------------------------------------------------------------ var-prop
def cmd_var_prop(a):
    rnd = random.Random(a.seed)
    D, L = a.width, a.layers
    f = [rnd.gauss(0, 1) for _ in range(D)]
    s = math.sqrt(a.var)
    hist = []
    for _ in range(L):
        h = [x if x > 0 else 0.0 for x in f]
        f = [sum(rnd.gauss(0, s) * hj for hj in h) for _ in range(D)]
        v = sum(x * x for x in f) / D
        hist.append(v)
        if math.isinf(v) or v > 1e150:
            break
    fac = 0.5 * D * a.var
    print("[from source] UDL p.122-124 (eq.7.30-7.31, Fig.7.7): E[f'^2] = (1/2) Dh sigma^2 E[f^2]; stable if sigma^2 = 2/Dh; biases 0")
    print(f"theoretical factor per layer = 0.5*D*sigma^2 = {fac:.6g}")
    print(f"second moment of the pre-activations: layer 1 {hist[0]:.4g}; layer {len(hist)} {hist[-1]:.4g} (seed {a.seed})")


# ------------------------------------------------------------------ sigmoid-chain
def cmd_sigmoid_chain(a):
    ws, zs = floats(a.w), floats(a.z)
    prod = 1.0
    print("[from source] NNDL p.230-235: dC/db1 = sigma'(z1) w2 sigma'(z2) w3 sigma'(z3) w4 sigma'(z4) dC/da4; sigma'(0)=1/4")
    for w, z in zip(ws, zs):
        sp = sigmoid(z) * (1 - sigmoid(z))
        t = w * sp
        prod *= t
        print(f"  w={w:g} z={z:g} sigma'(z)={sp:.6g} term w*sigma'={t:.6g}")
    print(f"product of the terms = {prod:.6g}")


# ------------------------------------------------------------------ transformer params
def xfmr_params(D, L, H, dk, dff, vocab=0, pos=0, ln=False):
    attn = H * 3 * (D * dk + dk) + ((H * dk) * D + D)
    mlp = (D * dff + dff) + (dff * D + D)
    lnp = 4 * D if ln else 0
    per = attn + mlp + lnp
    emb = vocab * D + pos * D
    return {"attn_per_layer": attn, "mlp_per_layer": mlp, "layernorm_per_layer": lnp, "per_layer": per,
            "layers": per * L, "embeddings": emb, "total": per * L + emb}


def cmd_xfmr_params(a):
    if a.preset == "bert-large":
        D, L, H, dk, dff, V, P = 1024, 24, 16, 64, 4096, 30000, 512
        print("[from source] UDL p.233: BERT: vocab 30,000, D=1024, 24 layers, 16 heads, q/k/v per head 64, MLP hidden 4096, ~340 million parameters")
        print("[extrapolation] learned positions 512 (p.234 cites a maximum length of 512 in pre-training); LayerNorm only with --ln")
    elif a.preset == "gpt3":
        D, L, H, dk, dff, V, P = 12288, 96, 96, 128, 4 * 12288, a.vocab, 0
        print("[from source] UDL p.238: GPT-3: 96 layers, D=12288, 96 heads, q/k/v dim 128, 175 billion parameters")
        print("[extrapolation] MLP width = 4D (not given in the book); vocabulary via --vocab (not given in UDL p.236-239)")
    else:
        D, L, H, dk, dff, V, P = a.d, a.layers, a.heads, a.dk, a.dff, a.vocab, a.pos
    r = xfmr_params(D, L, H, dk, dff, V, P, a.ln)
    for k, v in r.items():
        print(f"  {k}: {v}")
    print(f"TOTAL approximate: {r['total'] / 1e6:.1f} million")


# ------------------------------------------------------------------ diffusion
def alphas(betas):
    out, p = [], 1.0
    for b in betas:
        p *= (1.0 - b)
        out.append(p)
    return out


def posterior_coeffs(betas, t):
    """t in 1..T. Returns (coef of z_t, coef of x, variance) of q(z_{t-1}|z_t,x) (UDL eq.18.15, p.369)."""
    al = alphas(betas)
    b = betas[t - 1]
    at = al[t - 1]
    atm1 = al[t - 2] if t >= 2 else 1.0
    cz = (1 - atm1) * math.sqrt(1 - b) / (1 - at)
    cx = math.sqrt(atm1) * b / (1 - at)
    var = b * (1 - atm1) / (1 - at)
    return cz, cx, var


def eps_form_coeffs(betas, t):
    """Target mean in eps form (UDL eq.18.33, p.375)."""
    al = alphas(betas)
    b = betas[t - 1]
    at = al[t - 1]
    return 1 / math.sqrt(1 - b), -b / (math.sqrt(1 - at) * math.sqrt(1 - b))


def cmd_diffusion(a):
    betas = floats(a.betas) if a.betas else [a.beta] * a.T
    T = len(betas)
    al = alphas(betas)
    t = a.t
    print("[from source] UDL p.363-366: z_t = sqrt(alpha_t) x + sqrt(1-alpha_t) eps (eq.18.7), alpha_t = prod_{s<=t}(1-beta_s); q(zt|x)=N(sqrt(alpha_t)x,(1-alpha_t)I) (18.8)")
    print(f"T={T}, beta_t={betas[t - 1]:g}, alpha_t={al[t - 1]:.10g}, sqrt(alpha_t)={math.sqrt(al[t - 1]):.10g}, kernel var={1 - al[t - 1]:.10g}")
    cz, cx, var = posterior_coeffs(betas, t)
    print(f"[from source] UDL p.369 eq.18.15: mean = {cz:.10g}*z_t + {cx:.10g}*x ; variance = {var:.10g}")
    a1, a2 = eps_form_coeffs(betas, t)
    at = al[t - 1]
    cx_eps = -cx * math.sqrt(1 - at) / math.sqrt(at)
    cz_eff = cz + cx / math.sqrt(at)
    print(f"[from source] UDL p.374-375 eq.18.33: mean (eps form) = {a1:.10g}*z_t + {a2:.10g}*eps")
    print(f"identity eq.18.32 = 18.33 (residual): coef z_t {abs(cz_eff - a1):.3e}; coef eps {abs(cx_eps - a2):.3e}  [inference: checked numerically]")
    if a.sample is not None:
        rnd = random.Random(a.seed)
        eps = rnd.gauss(0, 1)
        zt = math.sqrt(at) * a.sample + math.sqrt(1 - at) * eps
        print(f"kernel sample (seed {a.seed}) x={a.sample}: eps={eps:.6f}, z_t={zt:.6f}")


# ------------------------------------------------------------------ kl normal
def kl_diag_to_std(mu, var):
    D = len(mu)
    return 0.5 * (sum(var) + sum(m * m for m in mu) - D - sum(math.log(v) for v in var))


def kl_diag(mu1, var1, mu2, var2):
    s = 0.0
    for m1, v1, m2, v2 in zip(mu1, var1, mu2, var2):
        s += math.log(v2 / v1) - 1 + v1 / v2 + (m2 - m1) ** 2 / v2
    return 0.5 * s


def cmd_kl_normal(a):
    mu, var = floats(a.mu), floats(a.var)
    print("[from source] UDL p.350 eq.17.24: DKL[N(mu,Sigma)||N(0,I)] = 1/2 (Tr[Sigma] + mu^T mu - Dz - log det[Sigma]); p.475 eq.C.32 (general case)")
    print(f"KL para N(0,I) = {kl_diag_to_std(mu, var):.10g}")
    if a.mu2 is not None:
        mu2, var2 = floats(a.mu2), floats(a.var2)
        print(f"KL para N(mu2,var2) = {kl_diag(mu, var, mu2, var2):.10g}")


# ------------------------------------------------------------------ divergence
def kl(p, q):
    s = 0.0
    for x, y in zip(p, q):
        if x > 0:
            if y <= 0:
                return math.inf
            s += x * math.log(x / y)
    return s


def js(p, q):
    m = [(x + y) / 2 for x, y in zip(p, q)]
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def w1(p, q):
    cum, s = 0.0, 0.0
    for x, y in zip(p, q):
        cum += x - y
        s += abs(cum)
    return s


def cmd_divergence(a):
    p, q = floats(a.p), floats(a.q)
    print("[from source] UDL p.474 eq.C.28 (KL), C.30 (JS), p.295 eq.15.9 (GAN loss ~ JS), p.297 eq.15.10-15.11 (discrete Wasserstein, cost |i-j|)")
    print(f"KL(p||q) = {kl(p, q):.10g}")
    print(f"JS(p,q)  = {js(p, q):.10g} (natural log; max ln2 = {math.log(2):.10g})")
    print(f"W1(p,q)  = {w1(p, q):.10g}  [inference: in 1D with cost |i-j| the optimal plan gives the sum |CDF_p - CDF_q|]")


# ------------------------------------------------------------------ xent
def softmax(z):
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]


def cmd_xent(a):
    if a.logits is not None:
        z = floats(a.logits)
        p = softmax(z)
        k = a.label
        m = max(z)
        loss = -(z[k] - (m + math.log(sum(math.exp(x - m) for x in z))))
        print("[from source] UDL p.82-83 eq.5.22-5.24 (softmax; loss = -log softmax_y); NNDL p.101-104 eq.78-80 (log-likelihood C=-ln a_y)")
        print("softmax = " + ", ".join(f"{x:.8g}" for x in p) + f"  (sum {sum(p):.10g})")
        print(f"loss -log p[y={k}] = {loss:.10g}")
    if a.binary_z is not None:
        z, y = a.binary_z, a.binary_y
        s = sigmoid(z)
        l = -(1 - y) * math.log(1 - s) - y * math.log(s)
        print("[from source] UDL p.80 eq.5.18-5.20 (sigmoid and BCE); NNDL p.89-91 eq.57-62 (cross-entropy; gradient (sigma-y) without the sigma' factor)")
        print(f"sigmoid({z:g})={s:.10g}; BCE(y={y:g}) = {l:.10g}; dBCE/dz = sigma - y = {s - y:.10g}")
        sm = softmax([0.0, z])[1]
        print(f"2-class softmax [0,z] gives P(class 1) = {sm:.10g} (= sigmoid(z)) [inference]")


# ------------------------------------------------------------------ momentum-equiv
def cmd_momentum_equiv(a):
    c, x0, steps = a.c, a.x0, a.steps
    b, al = a.beta, a.alpha
    xu, m = x0, 0.0
    xn, v = x0, 0.0
    mu, eta = b, al * (1 - b)
    maxd = 0.0
    for _ in range(steps):
        g = c * xu
        m = b * m + (1 - b) * g
        xu = xu - al * m
        g2 = c * xn
        v = mu * v - eta * g2
        xn = xn + v
        maxd = max(maxd, abs(xu - xn))
    print("[from source] UDL p.100 eq.6.11 (m<-beta m+(1-beta)g; phi<-phi-alpha m) e NNDL p.176 eq.107-108 (v<-mu v-eta grad; w<-w+v)")
    print(f"[inference] equivalent with mu=beta, eta=alpha(1-beta): mu={mu:g}, eta={eta:g}; max |x_UDL - x_NNDL| over {steps} steps = {maxd:.3e}")
    print(f"final x: UDL {xu:.10g}; NNDL {xn:.10g}")


# ------------------------------------------------------------------ adam
def cmd_adam_step(a):
    g = floats(a.grad)
    beta, gamma, alpha, eps = a.beta, a.gamma, a.alpha, a.eps
    m = [0.0] * len(g)
    v = [0.0] * len(g)
    phi = floats(a.phi) if a.phi else [0.0] * len(g)
    print("[from source] UDL p.102-104 eq.6.15-6.17: m<-beta m+(1-beta)g; v<-gamma v+(1-gamma)g^2; m~=m/(1-beta^(t+1)); v~=v/(1-gamma^(t+1)); phi<-phi-alpha m~/(sqrt(v~)+eps)")
    for t in range(a.steps):
        for i in range(len(g)):
            m[i] = beta * m[i] + (1 - beta) * g[i]
            v[i] = gamma * v[i] + (1 - gamma) * g[i] ** 2
            mh = m[i] / (1 - beta ** (t + 1))
            vh = v[i] / (1 - gamma ** (t + 1))
            phi[i] -= alpha * mh / (math.sqrt(vh) + eps)
        print(f"step {t + 1}: phi = " + ", ".join(f"{x:.8g}" for x in phi))
    print("with a constant gradient the step is ~alpha per coordinate, independent of the gradient scale (UDL p.102: 'moves a fixed distance alpha')")


# ------------------------------------------------------------------ l2 equiv
def cmd_l2_equiv(a):
    w, g0, eta, lam, n = a.w, a.g0, a.eta, a.lam, a.n
    wn = (1 - eta * lam / n) * w - eta * g0
    alpha = eta / n
    lam_u = lam / 2.0
    wu = w - alpha * (n * g0 + 2 * lam_u * w)
    print("[from source] NNDL p.116 eq.91-92: w -> (1-eta*lambda/n) w - eta dC0/dw ; UDL p.154 eq.9.5 (penalty lambda*sum phi^2) e p.169-170 eq.9.13 (weight decay phi<-(1-lambda')phi - alpha dL/dphi; L2 = decay if lambda=lambda'/(2 alpha) in SGD)")
    print(f"[inference] with alpha=eta/n e lambda_UDL=lambda_NNDL/2 (UDL sums the loss, NNDL averages it): NNDL {wn:.12g}; UDL {wu:.12g}; difference {abs(wn - wu):.3e}")
    print(f"NNDL decay factor = {1 - eta * lam / n:.10g}")


# ------------------------------------------------------------------ returns
def cmd_returns(a):
    r = floats(a.rewards)
    g = a.gamma
    G = sum((g ** k) * rk for k, rk in enumerate(r))
    print("[from source] UDL p.388 eq.19.1: G_t = soma_{k>=0} gamma^k r_{t+k+1}")
    print(f"G = {G:.10g}")
    if a.q is not None:
        td = a.r + g * a.qnext - a.q
        print("[from source] UDL p.398 eq.19.14 (SARSA) / eq.19.15 (Q-learning, with max): q <- q + alpha (r + gamma q' - q)")
        print(f"TD error = {td:.10g}; updated q = {a.q + a.alpha * td:.10g}")


def build():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, *args):
        s = sp.add_parser(name)
        for a_, kw in args:
            s.add_argument(a_, **kw)
        s.set_defaults(f=fn)

    add("mlp-params", cmd_mlp_params, ("--sizes", dict(required=True)))
    add("regions", cmd_regions, ("--D", dict(type=int, required=True)), ("--K", dict(type=int, required=True)), ("--Di", dict(type=int, default=1)))
    add("conv-params", cmd_conv_params, ("--ci", dict(type=int, required=True)), ("--co", dict(type=int, required=True)), ("--k", dict(type=int, required=True)), ("--dims", dict(type=int, default=1, choices=[1, 2])))
    add("conv-out", cmd_conv_out, ("--n", dict(type=int, required=True)), ("--k", dict(type=int, required=True)), ("--pad", dict(type=int, default=0)), ("--stride", dict(type=int, default=1)), ("--dilation", dict(type=int, default=1)))
    add("init-var", cmd_init_var, ("--rule", dict(choices=["he", "backward", "avg", "nndl", "nndl-large"], required=True)), ("--fan-in", dict(type=int, default=1)), ("--fan-out", dict(type=int, default=1)))
    add("sum-var", cmd_sum_var, ("--active", dict(type=int, required=True)), ("--var-w", dict(type=float, required=True)), ("--var-b", dict(type=float, default=1.0)))
    add("var-prop", cmd_var_prop, ("--width", dict(type=int, default=100)), ("--layers", dict(type=int, default=50)), ("--var", dict(type=float, required=True)), ("--seed", dict(type=int, default=1)))
    add("sigmoid-chain", cmd_sigmoid_chain, ("--w", dict(required=True)), ("--z", dict(required=True)))
    add("xfmr-params", cmd_xfmr_params, ("--preset", dict(choices=["bert-large", "gpt3", "custom"], default="custom")), ("--d", dict(type=int, default=0)), ("--layers", dict(type=int, default=0)), ("--heads", dict(type=int, default=0)), ("--dk", dict(type=int, default=0)), ("--dff", dict(type=int, default=0)), ("--vocab", dict(type=int, default=0)), ("--pos", dict(type=int, default=0)), ("--ln", dict(action="store_true")))
    add("diffusion", cmd_diffusion, ("--beta", dict(type=float, default=0.03)), ("--T", dict(type=int, default=100)), ("--betas", dict()), ("--t", dict(type=int, default=20)), ("--sample", dict(type=float)), ("--seed", dict(type=int, default=1)))
    add("kl-normal", cmd_kl_normal, ("--mu", dict(required=True)), ("--var", dict(required=True)), ("--mu2", dict()), ("--var2", dict()))
    add("divergence", cmd_divergence, ("--p", dict(required=True)), ("--q", dict(required=True)))
    add("xent", cmd_xent, ("--logits", dict()), ("--label", dict(type=int, default=0)), ("--binary-z", dict(type=float, dest="binary_z")), ("--binary-y", dict(type=float, dest="binary_y", default=1.0)))
    add("momentum-equiv", cmd_momentum_equiv, ("--c", dict(type=float, default=1.0)), ("--x0", dict(type=float, default=1.0)), ("--beta", dict(type=float, default=0.9)), ("--alpha", dict(type=float, default=0.1)), ("--steps", dict(type=int, default=50)))
    add("adam-step", cmd_adam_step, ("--grad", dict(required=True)), ("--phi", dict()), ("--alpha", dict(type=float, default=0.001)), ("--beta", dict(type=float, default=0.9)), ("--gamma", dict(type=float, default=0.999)), ("--eps", dict(type=float, default=1e-8)), ("--steps", dict(type=int, default=3)))
    add("l2-equiv", cmd_l2_equiv, ("--w", dict(type=float, default=1.0)), ("--g0", dict(type=float, default=0.3)), ("--eta", dict(type=float, default=0.5)), ("--lam", dict(type=float, default=5.0)), ("--n", dict(type=int, default=50000)))
    add("returns", cmd_returns, ("--rewards", dict(required=True)), ("--gamma", dict(type=float, default=0.9)), ("--q", dict(type=float)), ("--r", dict(type=float, default=0.0)), ("--qnext", dict(type=float, default=0.0)), ("--alpha", dict(type=float, default=0.1)))
    return p


def main(argv=None):
    a = build().parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()

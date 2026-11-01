# -*- coding: utf-8 -*-
"""
se3_calc.py - deterministic calculators based on formulas that "Security Engineering" (Ross Anderson, 3rd ed., SE3) presents on the cited pages.

Stdlib, no network, calculation only; run with: python -I scripts/se3_calc.py SUBCOMMAND [options] [--json]
Each output carries: the formula, the PDF page where the book presents it, and the source label:
  [from source]   formula/number that is on the cited page
  [inference]     direct arithmetic on the book's formula
  [extrapolation] formula that is NOT on the page (comes from the literature); no page
These calculations help reasoning; they do NOT replace a formal security review. Input parameters are the user's: check them.

Subcommands: dod-password, entropy, bits, brute-force, birthday, hash-collision, bayes-alarm, biometric-birthday,
             ale, risk-register, laplace-scale, reliability, bug-race, byzantine, amdahl, hawk-dove
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


def fnum(x):
    if isinstance(x, float):
        if x != 0 and (abs(x) >= 1e9 or abs(x) < 1e-4):
            return f"{x:.4g}"
        return f"{x:,.6g}"
    return f"{x:,}"


def human_time(sec):
    if sec < 1:
        return f"{sec:.3g} s"
    units = [("years", 365.25 * 86400), ("days", 86400), ("hours", 3600), ("min", 60), ("s", 1)]
    for name, size in units:
        if sec >= size:
            return f"{sec / size:,.4g} {name}"
    return f"{sec:.3g} s"


class Out:
    def __init__(self, title):
        self.title = title
        self.lines = []
        self.data = {}

    def add(self, label, text, **kv):
        self.lines.append((label, text))
        self.data.update(kv)

    def emit(self, as_json):
        if as_json:
            print(json.dumps({"calculo": self.title, "linhas": [{"origem": a, "texto": b} for a, b in self.lines],
                              "valores": self.data, "aviso": "does not replace a formal security review"},
                             ensure_ascii=False, indent=1, default=str))
        else:
            print(f"== {self.title}")
            for a, b in self.lines:
                print(f"{a} {b}")
            print("Warning: supporting calculation; does not replace a formal security review. Inputs are your assumptions.")


def need_pos(v, name):
    if v is None or v <= 0:
        print(f"error: {name} must be > 0", file=sys.stderr)
        sys.exit(2)
    return v


# ---------------------------------------------------------------- calculations
def c_dod(a):
    o = Out("Probability of guessing a password within its lifetime (DoD): P = L.R/S")
    if a.space is None:
        need_pos(a.length, "--length")
        need_pos(a.alphabet, "--alphabet")
        S = float(a.alphabet) ** a.length
    else:
        S = need_pos(a.space, "--space")
    L = need_pos(a.lifetime, "--lifetime (seconds)")
    R = need_pos(a.rate, "--rate (guesses/s)")
    P = min(1.0, L * R / S)
    o.add("[from source]", "Formula: if L is the maximum lifetime of the password, R the guess rate and S the size of the password space, P = L.R/S (US DoD guideline) (SE3 p.157).")
    o.add("[inference]", f"S = {fnum(S)} (= 2^{math.log2(S):.1f}); L = {fnum(L)} s; R = {fnum(R)}/s -> P = {fnum(P)} ({P * 100:.4g}%).", S=S, P=P)
    o.add("[from source]", "Caveat from the book: the attacker may want ANY account, not a specific one; a global rate limit is needed, not just a per-account one (SE3 p.157-158). Book example: an 8-character Unix password = 96^8 ~ 2^52; the CVCNCVCN template ~ 2^-29 per guess (SE3 p.158).")
    return o


def c_entropy(a):
    o = Out("Entropy / size of the password space")
    if a.words is not None:
        need_pos(a.wordlist, "--wordlist")
        bits = a.words * math.log2(a.wordlist)
        o.add("[inference]", f"{a.words} words from a list of {a.wordlist} -> {bits:.1f} bits (log2({a.wordlist}) per word).", bits=bits)
        o.add("[from source]", "The book cites the EFF list of 7,776 words (6^5) and counts six words as ~77 bits (SE3 p.147). Human word choice has diminishing returns and common bigrams (SE3 p.147); this holds for RANDOM choice.")
    elif a.length is not None:
        need_pos(a.alphabet, "--alphabet")
        bits = a.length * math.log2(a.alphabet)
        o.add("[inference]", f"{a.length} symbols from an alphabet of {a.alphabet} -> {a.alphabet}^{a.length} = 2^{bits:.1f} ({fnum(float(a.alphabet) ** a.length)} possibilities).", bits=bits)
        o.add("[from source]", "Book example: 96^8 ~ 2^52 (SE3 p.158). It only holds for uniformly random choice; human passwords have much less entropy (SE3 p.141-147).")
    else:
        print("error: provide --words N --wordlist M or --length N --alphabet M", file=sys.stderr)
        sys.exit(2)
    return o


def c_bits(a):
    o = Out("Brute-force effort in bits and comparison with the book's example")
    n = need_pos(a.bits, "--bits")
    rate = need_pos(a.rate, "--rate (guesses/s)")
    worst = 2.0 ** n / rate
    o.add("[inference]", f"{n:g}-bit key: space 2^{n:g} = {fnum(2.0 ** n)}; at {fnum(rate)} guesses/s, full sweep = {human_time(worst)}; average (half) = {human_time(worst / 2)}.", worst_s=worst)
    o.add("[from source]", "The book compares with the bitcoin mining power of the time: a 68-bit puzzle in ~10 min; 80 bits would take 2^12 times longer (~one month); 128 bits, 2^48 times longer (SE3 p.202) [DATED: 2020 hardware].")
    return o


def c_bf(a):
    o = Out("Average brute-force time (2^(n-1) guesses)")
    n = need_pos(a.bits, "--bits")
    rate = need_pos(a.rate, "--rate (guesses/s)")
    avg = 2.0 ** (n - 1) / rate
    o.add("[inference]", f"{n:g} bits at {fnum(rate)}/s: average {human_time(avg)}.", avg_s=avg)
    o.add("[from source]", "The book uses 'on average 2^55' for 56-bit DES (SE3 p.221) and ~2^(n-1) guesses to invert an n-bit hash (SE3 p.204-205) [DATED regarding hardware cost].")
    return o


def birthday_exact(N, m):
    if m > N:
        return 1.0
    lg = 0.0
    for i in range(int(m)):
        lg += math.log1p(-i / N)
    return 1.0 - math.exp(lg)


def c_birthday(a):
    o = Out("Birthday theorem")
    if a.bits is not None:
        N = 2.0 ** a.bits
    else:
        N = need_pos(a.space, "--space (N)")
    beta = 1.0 - a.prob  # prob(all different)
    if not (0 < a.prob < 1):
        print("error: --prob must be in (0,1)", file=sys.stderr)
        sys.exit(2)
    m_approx = math.sqrt(2.0 * N * math.log(1.0 / beta))
    o.add("[from source]", "With N possible values, a collision appears after ~sqrt(N) samples; for n bits, ~2^(n/2) (SE3 p.205). Book note: the probability that m choices are all different is beta = N(N-1)...(N-m+1)/N^m, and N ~ m^2/(2 log(1/beta)) (SE3 p.205).")
    o.add("[inference]", f"N = {fnum(N)}; for collision probability >= {a.prob:g}, m ~ sqrt(2.N.ln(1/beta)) = {fnum(m_approx)} samples (beta = {beta:g}).", m=m_approx)
    if N <= 1e12:
        ex = birthday_exact(N, round(m_approx))
        o.add("[inference]", f"Exact check with m = {round(m_approx):,}: P(collision) = {ex:.4f}.", exato=ex)
    o.add("[from source]", "Book example: 23 people already exceed 50% for N = 365 (SE3 p.205).")
    return o


def c_hash(a):
    o = Out("Hash collision resistance")
    n = need_pos(a.bits, "--bits")
    o.add("[from source]", "An n-bit output: the enemy needs ~2^(n/2) hashes to expect a collision (SE3 p.205); MD5 (128 bits) -> up to 2^64, SHA-1 (160) -> 2^80; for collision resistance use output >= 256 bits (SE3 p.206).")
    o.add("[inference]", f"n = {n:g}: collision in ~2^{n / 2:g} = {fnum(2.0 ** (n / 2))} hashes; inversion (preimage) in ~2^{n - 1:g}.", coll_bits=n / 2)
    if a.rate:
        o.add("[inference]", f"At {fnum(a.rate)} hashes/s, collision in ~{human_time(2.0 ** (n / 2) / a.rate)}.")
    o.add("[from source]", "Real practical attacks on MD5/SHA-1 were cheaper than the generic search (SE3 p.229-230) [DATED].")
    return o


def c_bayes(a):
    o = Out("False vs real alarms (base rate) - intrusion detection")
    per_m = a.attacks_per_million
    fa = a.false_alarm_rate
    det = a.detection
    if not (0 <= fa <= 1 and 0 <= det <= 1) or per_m < 0 or per_m > 1e6:
        print("error: parameters out of range", file=sys.stderr)
        sys.exit(2)
    sessions = 1e6
    real = per_m * det
    false = (sessions - per_m) * fa
    ratio = false / real if real else float("inf")
    ppv = real / (real + false) if (real + false) else 0.0
    o.add("[from source]", "'Few attacks': with 10 real attacks per million sessions and a 0.1% false alarm rate, the false:real ratio is 100; a problem known from HIV screening; guards get tired and genuine alarms are lost (SE3 p.759-760).")
    o.add("[inference]", f"Per 1 million sessions: attacks {per_m:g}; detection {det:g}; false alarm {fa:g} -> real alarms {real:g}, false {false:,.1f}; ratio false:real = {ratio:,.1f}; P(attack | alarm) = {ppv * 100:.2f}%.", razao=ratio, ppv=ppv)
    o.add("[inference]", "Direct Bayes theorem: P(attack|alarm) = det.p / (det.p + fa.(1-p)) with p = base rate; the assumed detection of 1.0 is our assumption (the book does not give it).")
    return o


def c_bio(a):
    o = Out("Birthday theorem in biometrics (1:N identification)")
    f = a.far
    if not (0 < f < 1):
        print("error: --far must be in (0,1)", file=sys.stderr)
        sys.exit(2)
    N = math.sqrt(1.386 / f)
    n = int(round(N))
    pairs = n * (n - 1) // 2
    pnone = math.exp(pairs * math.log1p(-f))
    o.add("[from source]", "A false match between two enrolled people becomes more likely than not once N > sqrt(1.386/f), where f is the per-pair false-match rate; with f = 1e-6 the book gives N = 1177, 692,076 pairs and probability of no false match = 0.999999^692076 = 0.500 (SE3 p.632 and note 4; idea in SE3 p.205).")
    o.add("[inference]", f"f = {f:g}: N* = {N:,.1f} -> {n:,} people; pairs = {pairs:,}; P(no false match) = {pnone:.4f} (the book rounds to 0.500).", n=n, pares=pairs, pnenhum=pnone)
    o.add("[inference]", "Consequence (book): 1:N identification scales much worse than 1:1 verification; a FAR of 1 in 1 million does not serve a population of thousands in identification mode (SE3 p.205, 632).")
    return o


def parse_ale(items):
    rows = []
    for it in items:
        parts = it.split(":")
        if len(parts) < 3:
            print(f"error: item '{it}' must be name:loss:incidence[:reported_ALE]", file=sys.stderr)
            sys.exit(2)
        name = parts[0]
        loss = float(parts[1])
        inc = float(parts[2])
        printed = float(parts[3]) if len(parts) > 3 and parts[3] != "" else None
        rows.append((name, loss, inc, printed))
    return rows


def c_ale(a):
    o = Out("ALE (annualized loss expectancy) = expected loss x annual incidence")
    items = a.item
    if a.sample:
        items = ["SWIFT fraud:50000000:0.005:250000", "ATM fraud (large):250000:0.2:100000",
                 "ATM fraud (small):20000:0.5:10000", "Teller takes cash:3240:200:648000"]
    if not items:
        print("error: use --item name:loss:incidence[:reported_ALE] (repeatable) or --sample", file=sys.stderr)
        sys.exit(2)
    rows = parse_ale(items)
    o.add("[from source]", "ALE = expected loss x expected number of incidents per year; the book's table (Fig. 27.1) has SWIFT fraud, ATM fraud (large/small) and teller takes cash (SE3 p.1000).")
    tot = 0.0
    for name, loss, inc, printed in rows:
        ale = loss * inc
        tot += ale
        flag = ""
        if printed is not None and abs(printed - ale) > 1e-6 * max(1.0, ale):
            flag = f"  <-- DIVERGES from the reported ALE ({fnum(printed)}): product = {fnum(ale)}"
        o.add("[inference]", f"{name}: {fnum(loss)} x {fnum(inc)} = {fnum(ale)}{flag}")
    o.add("[inference]", f"Sum of ALEs = {fnum(tot)}.", total=tot)
    if a.sample:
        o.add("[from source]", "Fidelity note: on the printed page the 'ATM fraud (large)' row shows 250,000 x 0.2 = 100,000, but the product is 50,000 (inconsistency in the book itself; SE3 p.1000). The calculation above uses the product.")
    o.add("[from source]", "Book warning: the data are accurate for common losses and largely guesswork for rare ones; consultancies adjust the total; separate data, guesses and office politics (SE3 p.1000).")
    return o


def c_risk(a):
    o = Out("Risk register (severity 1-5 x probability 1-5)")
    rows = []
    for it in a.item:
        p = it.split(":")
        if len(p) < 3:
            print(f"error: item '{it}' must be name:severity:probability[:severity_after:probability_after]", file=sys.stderr)
            sys.exit(2)
        name = p[0]
        sv, pb = int(p[1]), int(p[2])
        if not (1 <= sv <= 5 and 1 <= pb <= 5):
            print("error: severity and probability must be in 1-5", file=sys.stderr)
            sys.exit(2)
        after = None
        if len(p) >= 5:
            sv2, pb2 = int(p[3]), int(p[4])
            if not (1 <= sv2 <= 5 and 1 <= pb2 <= 5):
                print("error: mitigation values must be in 1-5", file=sys.stderr)
                sys.exit(2)
            after = sv2 * pb2
        rows.append((name, sv, pb, sv * pb, after))
    rows.sort(key=lambda r: (-r[3], r[0]))
    o.add("[from source]", "Risk register: list what can go wrong, score severity (1-5) and probability (1-5), multiply (1 to 25), describe the mitigation, sort, and give each risk a senior owner; book example: 5x4 = 20 reduced to 16 by a hiring rule (SE3 p.999).")
    for i, (n, sv, pb, sc, af) in enumerate(rows, 1):
        extra = f" -> after mitigation {af}" if af is not None else ""
        o.add("[inference]", f"{i}. {n}: {sv} x {pb} = {sc}{extra}")
    o.add("[inference]", "Reminder: assign an owner to each risk; the scores are judgment, not measurement.")
    return o


def c_laplace(a):
    o = Out("Laplace noise scale for differential privacy ([extrapolation] ONLY)")
    eps = need_pos(a.epsilon, "--epsilon")
    sens = need_pos(a.sensitivity, "--sensitivity")
    b = sens / eps
    o.add("[from source]", "The book describes DP: an epsilon-indistinguishable mechanism with Laplace noise; small epsilon = strong privacy; epsilon = 1000 amounts to publishing the raw data; epsilon is a policy decision (SE3 p.434). The 2020 US census used a top-down algorithm with a global budget; epsilon between 4 and 6 was suggested by economic analysis (SE3 p.435-436) [DATED].")
    o.add("[extrapolation]", f"b = sensitivity/epsilon = {sens:g}/{eps:g} = {b:g}; standard deviation of the Laplace noise = sqrt(2).b = {math.sqrt(2) * b:g}. The formula b = sensitivity/epsilon is NOT on the page; it comes from the DP literature (Dwork et al.). Check with a specialist.", b=b)
    return o


def c_rel(a):
    o = Out("Reliability growth (k/t) and single bug (e^-Et)")
    o.add("[from source]", "For a single bug, the probability of remaining undetected after t random tests is p = e^(-E.t) (SE3 p.1067). In large systems the probability that the t-th test fails is proportional to k/t, so MTBF ~ t/k and reliability grows LINEARLY with test time: for an MTBF of 1 million hours, test >= 1 million hours (SE3 p.1068).")
    if a.hours is not None:
        t = need_pos(a.hours, "--hours")
        k = need_pos(a.k, "--k")
        o.add("[inference]", f"t = {fnum(t)} h, k = {fnum(k)} -> MTBF ~ t/k = {fnum(t / k)} h; to reach a target MTBF M you need to test ~ k.M = {fnum(k * (a.target_mtbf or t / k))} h.", mtbf=t / k)
    if a.exponent_E is not None and a.tests is not None:
        p = math.exp(-a.exponent_E * a.tests)
        o.add("[inference]", f"Single bug: E = {a.exponent_E:g}, t = {a.tests:g} -> p(undetected) = {p:.4g}.", p=p)
    o.add("[from source]", "This holds if the bugs are statistically independent and is the BEST case; reusable libraries gain little; testers should work in parallel (SE3 p.1068-1069). The constant k depends on initial quality and test scope: estimate it from your own history, not from memory.")
    return o


def c_race(a):
    o = Out("Attacker vs defender: bug hunting (Ahmed/Brian example)")
    B, M = need_pos(a.bugs, "--bugs"), need_pos(a.mtbf, "--mtbf")
    ha, hd = need_pos(a.attacker_hours, "--attacker-hours"), need_pos(a.defender_hours, "--defender-hours")
    fa = B * ha / M
    fd = B * hd / M
    pd = 1 - math.exp(-hd / M)
    o.add("[from source]", "Example: 1,000,000 bugs with an MTBF of 1e9 h; Ahmed tests 10,000 h/year and finds ~10 bugs; Brian tests 1e8 h/year and finds ~100,000, but the chance that he found ONE specific bug of Ahmed's is only ~10%; 'the attacker has thermodynamics on his side' (SE3 p.1069).")
    o.add("[inference]", f"bugs found in one year: attacker ~ {fnum(fa)}; defender ~ {fnum(fd)}; P(defender found one specific attacker bug) = 1-e^(-hd/MTBF) = {pd * 100:.2f}%.", atacante=fa, defensor=fd, p=pd)
    o.add("[from source]", "In real life vulnerabilities are correlated, not independent (SE3 p.1069); the model is illustrative.")
    return o


def c_byz(a):
    o = Out("Byzantine fault tolerance: n >= 3t + 1")
    o.add("[from source]", "With n generals and t traitors, a solution exists if and only if n >= 3t + 1 (Lamport-Shostak-Pease); with digital signatures nobody dares lie to two colleagues (SE3 p.297).")
    if a.traitors is not None:
        o.add("[inference]", f"t = {a.traitors} -> minimum n = {3 * a.traitors + 1}.", n_min=3 * a.traitors + 1)
    if a.n is not None:
        t = max(0, (a.n - 1) // 3)
        o.add("[inference]", f"n = {a.n} -> tolerates at most t = {t} traitors (without signatures).", t_max=t)
    if a.traitors is None and a.n is None:
        print("error: provide --traitors T or --n N", file=sys.stderr)
        sys.exit(2)
    return o


def c_amdahl(a):
    o = Out("Amdahl's law")
    p, s = a.parallel, need_pos(a.cores, "--cores")
    if not (0 <= p <= 1):
        print("error: --parallel must be in [0,1]", file=sys.stderr)
        sys.exit(2)
    sp = 1.0 / ((1 - p) + p / s)
    o.add("[from source]", "speedup = (1 - p + p/s)^-1; book example: 3/4 of the program parallelizable and 8 cores = ~2.909 (SE3 p.289).")
    o.add("[inference]", f"p = {p:g}, s = {s:g} -> speedup = {sp:.4g}.", speedup=sp)
    return o


def c_hawk(a):
    o = Out("Hawk-dove: proportion of hawks")
    v, c = need_pos(a.value, "--value"), need_pos(a.cost, "--cost")
    o.add("[from source]", "In the hawk-dove game, if the cost of fighting c exceeds the value v of the resource, the proportion of hawks at equilibrium is p = v/c (SE3 p.333).")
    if c <= v:
        o.add("[inference]", "c <= v: the mixed equilibrium does not apply (hawk dominates).")
    else:
        o.add("[inference]", f"v = {v:g}, c = {c:g} -> p = {v / c:.4g}.", p=v / c)
    return o


def build():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sp = ap.add_subparsers(dest="cmd", required=True)

    def P(name, fn, help_):
        p = sp.add_parser(name, help=help_)
        p.add_argument("--json", action="store_true", dest="json_sub")
        p.set_defaults(fn=fn)
        return p

    p = P("dod-password", c_dod, "P = L.R/S")
    p.add_argument("--lifetime", type=float, required=True, help="maximum password lifetime, in seconds")
    p.add_argument("--rate", type=float, required=True, help="guesses per second")
    p.add_argument("--space", type=float)
    p.add_argument("--length", type=int)
    p.add_argument("--alphabet", type=int)
    p = P("entropy", c_entropy, "bits of entropy")
    p.add_argument("--words", type=int)
    p.add_argument("--wordlist", type=int)
    p.add_argument("--length", type=int)
    p.add_argument("--alphabet", type=int)
    p = P("bits", c_bits, "2^n effort at a given rate")
    p.add_argument("--bits", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p = P("brute-force", c_bf, "average time 2^(n-1)")
    p.add_argument("--bits", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p = P("birthday", c_birthday, "birthday theorem")
    p.add_argument("--bits", type=float)
    p.add_argument("--space", type=float)
    p.add_argument("--prob", type=float, default=0.5, help="desired collision probability (default 0.5)")
    p = P("hash-collision", c_hash, "hash collision")
    p.add_argument("--bits", type=float, required=True)
    p.add_argument("--rate", type=float)
    p = P("bayes-alarm", c_bayes, "false vs real alarms")
    p.add_argument("--attacks-per-million", type=float, default=10.0, dest="attacks_per_million")
    p.add_argument("--false-alarm-rate", type=float, default=0.001, dest="false_alarm_rate")
    p.add_argument("--detection", type=float, default=1.0)
    p = P("biometric-birthday", c_bio, "critical N in biometric identification")
    p.add_argument("--far", type=float, required=True, help="per-pair false-match rate, e.g. 1e-6")
    p = P("ale", c_ale, "ALE")
    p.add_argument("--item", action="append", default=[], help="name:loss:incidence[:reported_ALE]")
    p.add_argument("--sample", action="store_true", help="reproduces Fig. 27.1 (and the page's inconsistency)")
    p = P("risk-register", c_risk, "severity x probability")
    p.add_argument("--item", action="append", required=True, help="name:severity:probability[:severity_after:probability_after]")
    p = P("laplace-scale", c_laplace, "b = sensitivity/epsilon [extrapolation]")
    p.add_argument("--epsilon", type=float, required=True)
    p.add_argument("--sensitivity", type=float, default=1.0)
    p = P("reliability", c_rel, "k/t and e^-Et")
    p.add_argument("--hours", type=float)
    p.add_argument("--k", type=float, default=1.0)
    p.add_argument("--target-mtbf", type=float, dest="target_mtbf")
    p.add_argument("--exponent-E", type=float, dest="exponent_E")
    p.add_argument("--tests", type=float)
    p = P("bug-race", c_race, "attacker vs defender")
    p.add_argument("--bugs", type=float, default=1e6)
    p.add_argument("--mtbf", type=float, default=1e9)
    p.add_argument("--attacker-hours", type=float, default=1e4, dest="attacker_hours")
    p.add_argument("--defender-hours", type=float, default=1e8, dest="defender_hours")
    p = P("byzantine", c_byz, "n >= 3t+1")
    p.add_argument("--traitors", type=int)
    p.add_argument("--n", type=int)
    p = P("amdahl", c_amdahl, "Amdahl speedup")
    p.add_argument("--parallel", type=float, required=True)
    p.add_argument("--cores", type=float, required=True)
    p = P("hawk-dove", c_hawk, "p = v/c")
    p.add_argument("--value", type=float, required=True)
    p.add_argument("--cost", type=float, required=True)
    return ap


def main():
    ap = build()
    a = ap.parse_args()
    o = a.fn(a)
    o.emit(a.json or getattr(a, "json_sub", False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

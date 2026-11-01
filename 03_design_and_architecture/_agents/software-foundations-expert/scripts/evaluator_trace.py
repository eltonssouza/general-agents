# -*- coding: utf-8 -*-
"""
evaluator_trace.py - didactic simulations of the SICP evaluation models (substitution, breakdown under set!, environment).

ORIGIN OF THE RULES (declared):
- [from source] The simulated rules come from SICP: application by substitution, applicative and normal orders (SICP p.29-31);
  make-simplified-withdraw vs make-decrementer (SICP p.217-219); environment model: frames, procedure = code +
  environment, application creates a frame whose enclosing environment is the procedure's environment (SICP p.224-227); make-withdraw, W1 and W2
  (SICP p.230-234). The example expressions f/sum-of-squares/square are the book's (SICP p.28-29).
- [extrapolation] The step-by-step of the `substitution` mode is OUR mini-reducer (one step = one reduction; the book shows
  the same sequence grouped). The count of primitive reductions and applications is output of our reducer, not of the book;
  the book only observes that (+ 5 1) and (* 5 2) are evaluated twice in normal order (SICP p.31).
- Supported subset: numbers, + - * /, = < > <= >=, if, procedures defined with (define (name params) body).
  There is no set!, lists, let or lambda in the reducer (the `environment` mode handles state separately).
Pages = PDF (see references/INDEX.md). No network; read-only.

Usage:
  python -I scripts/evaluator_trace.py --mode substitution --expr "(f 5)" --order applicative
  python -I scripts/evaluator_trace.py --mode orders --expr "(f 5)"
  python -I scripts/evaluator_trace.py --mode mutable_breakdown
  python -I scripts/evaluator_trace.py --mode environment
  (add --json for JSON output; --define "(define (g x) (* x 3))" may be repeated)
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

BOOK_DEFS = [
    "(define (square x) (* x x))",
    "(define (sum-of-squares x y) (+ (square x) (square y)))",
    "(define (f a) (sum-of-squares (+ a 1) (* a 2)))",
]


# ---------------------------------------------------------------- s-expressions
def parse(text):
    toks = re.findall(r"\(|\)|[^\s()]+", text)
    pos = 0

    def rd():
        nonlocal pos
        if pos >= len(toks):
            raise SyntaxError("incomplete expression")
        t = toks[pos]
        pos += 1
        if t == "(":
            lst = []
            while pos < len(toks) and toks[pos] != ")":
                lst.append(rd())
            if pos >= len(toks):
                raise SyntaxError("missing ')'")
            pos += 1
            return lst
        if t == ")":
            raise SyntaxError("unexpected ')'")
        try:
            return int(t)
        except ValueError:
            try:
                return float(t)
            except ValueError:
                return t

    e = rd()
    if pos != len(toks):
        raise SyntaxError("trailing text after the expression")
    return e


def show(e):
    if isinstance(e, list):
        return "(" + " ".join(show(x) for x in e) + ")"
    return str(e)


PRIMS = {
    "+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b,
    "/": lambda a, b: a // b if isinstance(a, int) and isinstance(b, int) and a % b == 0 else a / b,
    "=": lambda a, b: a == b, "<": lambda a, b: a < b, ">": lambda a, b: a > b,
    "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b,
}


def is_value(e):
    return isinstance(e, (int, float)) or e in ("true", "false")


def subst(body, params, args):
    m = dict(zip(params, args))
    if isinstance(body, list):
        return [subst(x, params, args) for x in body]
    if isinstance(body, str) and body in m:
        return m[body]
    return body


class Machine:
    def __init__(self, defs, order):
        self.procs = {}
        for d in defs:
            self.add(d)
        self.order = order
        self.prim_steps = 0
        self.apps = 0

    def add(self, text):
        d = parse(text)
        if not (isinstance(d, list) and len(d) == 3 and d[0] == "define" and isinstance(d[1], list)):
            raise SyntaxError("only (define (name params...) body) is supported: " + text)
        self.procs[d[1][0]] = (d[1][1:], d[2])

    def step(self, e):
        """one reduction; None if e is already a value."""
        if is_value(e) or isinstance(e, str):
            return None
        op = e[0]
        if op == "if":
            if is_value(e[1]):
                return e[3] if (e[1] == "false" and len(e) > 3) else ("false" if e[1] == "false" else e[2])
            return ["if", self.step(e[1])] + e[2:]
        args = e[1:]
        if op in PRIMS or self.order == "applicative":
            for i, a in enumerate(args):
                if not is_value(a):
                    if isinstance(a, str):
                        raise NameError("symbol without a value: " + a)
                    return [op] + args[:i] + [self.step(a)] + args[i + 1:]
        if op in PRIMS:
            r = PRIMS[op](*args)
            self.prim_steps += 1
            if isinstance(r, bool):
                return "true" if r else "false"
            return r
        if op in self.procs:
            params, body = self.procs[op]
            if len(params) != len(args):
                raise TypeError("wrong arity in " + show(e))
            self.apps += 1
            return subst(body, params, args)
        raise NameError("unknown operator: " + str(op))

    def run(self, e, limit=200):
        trace = [show(e)]
        n = 0
        while True:
            nxt = self.step(e)
            if nxt is None:
                break
            e = nxt
            trace.append(show(e))
            n += 1
            if n > limit:
                raise RuntimeError("step limit exceeded (does the process not terminate?)")
        return trace, e


def do_substitution(expr, order, extra_defs):
    m = Machine(BOOK_DEFS + extra_defs, order)
    trace, val = m.run(parse(expr))
    return {
        "model": "Substitution model, %s order" % ("applicative" if order == "applicative" else "normal"),
        "citation": "SICP p.29-31 (rule and orders); the step-by-step reducer is ours [extrapolation]",
        "expression": expr, "trace": trace, "value": show(val),
        "primitive_reductions": m.prim_steps, "procedure_applications": m.apps,
    }


def do_orders(expr, extra_defs):
    a = do_substitution(expr, "applicative", extra_defs)
    n = do_substitution(expr, "normal", extra_defs)
    return {
        "model": "Applicative order vs normal order",
        "citation": "SICP p.30-31; counts come from our reducer [extrapolation]",
        "applicative": a, "normal": n,
        "same_value": a["value"] == n["value"],
        "note": ("In normal order, subexpressions such as (+ 5 1) and (* 5 2) are re-evaluated (SICP p.31); "
                 "for procedures that can be modeled by substitution and legitimate values, both orders give the same value (SICP p.31)."),
    }


# ---------------------------------------------------------------- set! breaks substitution
def do_mutable_breakdown():
    def make_simplified_withdraw(balance):
        box = [balance]

        def w(amount):
            box[0] -= amount
            return box[0]
        return w

    def make_decrementer(balance):
        return lambda amount: balance - amount

    W, D = make_simplified_withdraw(25), make_decrementer(25)
    r = {
        "model": "Substitution vs assignment (make-simplified-withdraw and make-decrementer)",
        "citation": "SICP p.217-220 (examples and referential transparency); p.223 note 9",
        "make_simplified_withdraw": {"(W 20)": W(20), "(W 10)": W(10)},
        "make_decrementer": {"(D 20)": D(20), "(D 10)": D(10)},
        "why_substitution_fails": [
            "make-decrementer can be explained by substitution: ((lambda (amount) (- 25 amount)) 20) => 5 (SICP p.218).",
            "In make-simplified-withdraw, substituting 25 for balance leads to ((lambda (amount) (set! balance (- 25 amount)) 25) 20); "
            "one would need to tell apart the occurrence of balance before and after the set!, and substitution cannot (SICP p.218-219).",
            "Note 9 (SICP p.223) recalls that the name in set! is not evaluated; substituting it would give (set! 25 ...), which is meaningless.",
            "The root: with set! a variable stops being a name for a value and comes to designate a place where the value can change (SICP p.219).",
            "W1 and W2 (same code, different effects) are not interchangeable, unlike D1 and D2 (SICP p.219-220): "
            "referential transparency is violated (SICP p.220).",
        ],
        "verdict": "With assignment the environment model is needed (SICP p.224-227).",
    }
    return r


# ---------------------------------------------------------------- environment model
class Frame:
    _n = 0

    def __init__(self, vars_, enclosing, label=None):
        if label is None:
            label = "E%d" % Frame._n
            Frame._n += 1
        self.label, self.vars, self.enclosing = label, dict(vars_), enclosing

    def where(self, name):
        f = self
        while f is not None:
            if name in f.vars:
                return f
            f = f.enclosing
        raise NameError(name)

    def show(self):
        return "%s %s -> %s" % (self.label, self.vars, self.enclosing.label if self.enclosing else "(global)")


def do_environment():
    Frame._n = 0
    out = []
    g = Frame({}, None, "E0")  # global
    Frame._n = 1

    def log(step, text):
        out.append({"step": step, "event": text})

    # (define (make-withdraw balance) (lambda (amount) ...)): procedure = (code, environment) (SICP p.225-226)
    g.vars["make-withdraw"] = ("make-withdraw", "params=(balance)", "env=E0")
    log(1, "define make-withdraw in the global frame E0: procedure object = code + pointer to E0 (SICP p.225-226, p.230)")

    def call_make_withdraw(initial):
        e = Frame({"balance": initial}, g)
        log(len(out) + 1, "(make-withdraw %s): new frame %s binds balance=%s; enclosing = the procedure's environment (E0); "
                         "the inner lambda becomes a procedure with env=%s (SICP p.226, p.231)" % (initial, e.label, initial, e.label))
        return ("lambda", "params=(amount)", "env=" + e.label), e

    def call_withdraw(name, proc, env, amount):
        fr = Frame({"amount": amount}, env)
        bal_frame = fr.where("balance")
        old = bal_frame.vars["balance"]
        if old >= amount:
            bal_frame.vars["balance"] = old - amount
            res = bal_frame.vars["balance"]
            text = "set! balance in %s: %s -> %s" % (bal_frame.label, old, res)
        else:
            res = "Insufficient funds"
            text = "insufficient balance; nothing is changed"
        log(len(out) + 1, "(%s %s): new frame %s binds amount=%s; enclosing = %s (procedure's env, NOT the caller's); "
                          "balance is found by following the pointer to %s; %s; result %s; frame %s is no longer reachable "
                          "(SICP p.232-233)" % (name, amount, fr.label, amount, env.label, bal_frame.label, text, res, fr.label))
        return res

    w1, e1 = call_make_withdraw(100)
    g.vars["W1"] = w1
    log(len(out) + 1, "define W1 = procedure with env=%s in the global frame (SICP p.231)" % e1.label)
    r1 = call_withdraw("W1", w1, e1, 50)
    r2 = call_withdraw("W1", w1, e1, 25)
    w2, e2 = call_make_withdraw(100)
    g.vars["W2"] = w2
    log(len(out) + 1, "define W2 = another procedure, with env=%s: same code, another environment, independent state (SICP p.233-234)" % e2.label)
    r3 = call_withdraw("W2", w2, e2, 40)
    return {
        "model": "Environment model: frames, procedure = code + environment, local state",
        "citation": "SICP p.224-227 (rules), p.230-234 (make-withdraw, W1, W2)",
        "events": out,
        "results": {"(W1 50)": r1, "(W1 25)": r2, "(W2 40)": r3},
        "balances": {e1.label: e1.vars["balance"], e2.label: e2.vars["balance"]},
        "lexical_note": ("The call's frame has as its enclosing environment the one stored in the procedure (lexical), not the "
                         "caller's (SICP p.226-227, p.232). 'Dynamic scope' (the caller's environment) is a concept of CI p.131; "
                         "SICP does not define it."),
    }


# ---------------------------------------------------------------- output
def render(res):
    if "applicative" in res:
        for k in ("applicative", "normal"):
            render(res[k])
            print()
        print("Same value in both orders: %s" % res["same_value"])
        print("Note: %s" % res["note"])
        return
    print("=== %s ===" % res["model"])
    print("Citation: [%s]\n" % res["citation"])
    if "trace" in res:
        print("Expression: %s" % res["expression"])
        for i, s in enumerate(res["trace"]):
            print("  %2d. %s" % (i, s))
        print("Value: %s   (primitive reductions: %d; procedure applications: %d)"
              % (res["value"], res["primitive_reductions"], res["procedure_applications"]))
    elif "why_substitution_fails" in res:
        print("make-simplified-withdraw 25: %s" % res["make_simplified_withdraw"])
        print("make-decrementer 25:        %s\n" % res["make_decrementer"])
        for item in res["why_substitution_fails"]:
            print("- " + item)
        print("\nVerdict: " + res["verdict"])
    elif "events" in res:
        for ev in res["events"]:
            print("%2d. %s" % (ev["step"], ev["event"]))
        print("\nResults: %s" % res["results"])
        print("Final balances per frame: %s" % res["balances"])
        print("\n" + res["lexical_note"])


def main():
    ap = argparse.ArgumentParser(description="Didactic simulator of the SICP evaluation models.")
    ap.add_argument("--mode", choices=["substitution", "orders", "pure", "mutable_breakdown", "environment"],
                    default="substitution", help="'pure' is an alias of 'orders' with the book's expression")
    ap.add_argument("--expr", default="(f 5)", help="expression for substitution/orders")
    ap.add_argument("--order", choices=["applicative", "normal"], default="applicative")
    ap.add_argument("--define", action="append", default=[], help="extra definition (define (g x) ...)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        if a.mode == "substitution":
            res = do_substitution(a.expr, a.order, a.define)
        elif a.mode in ("orders", "pure"):
            res = do_orders(a.expr, a.define)
        elif a.mode == "mutable_breakdown":
            res = do_mutable_breakdown()
        else:
            res = do_environment()
    except (SyntaxError, NameError, TypeError, RuntimeError, ZeroDivisionError) as ex:
        print("Error: %s" % ex, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        render(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())

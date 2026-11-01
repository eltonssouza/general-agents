# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests for the package scripts (lookup, compare, lint, scaffold) and the verifier.
Usage: python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]
No network; does not run the framework. The scaffold --out test uses a temporary folder and removes it.
Exit 0 if everything passes.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
SC = os.path.join(PKG, "scripts")
FX = os.path.join(HERE, "fixtures")
ROOT = os.path.abspath(os.path.join(PKG, "..", "..", ".."))

FAILS = []
COUNT = [0]


def run(script, *args, stdin=None, base=SC):
    p = subprocess.run([sys.executable, "-I", os.path.join(base, script), *args], input=stdin,
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    COUNT[0] += 1
    if not cond:
        FAILS.append(name)
        print(f"FAIL {name} {detail}")
    else:
        print(f"ok   {name}")


def main():
    ap = argparse.ArgumentParser()
    default_src = os.path.join(ROOT, "scratch", "frameworks")
    ap.add_argument("--src", default=default_src)
    a = ap.parse_args()

    # ---- lookup
    rc, o = run("nbf_lookup.py", "event loop")
    check("T01 lookup event loop -> NODEHB p.85-98", "NODEHB p.85-98" in o and rc == 0, o)
    rc, o = run("nbf_lookup.py", "decorator")
    check("T02 lookup decorator -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run("nbf_lookup.py", "helmet")
    check("T03 lookup helmet -> NOT COVERED and rc 1", "NOT COVERED" in o and rc == 1, o)
    rc, o = run("nbf_lookup.py", "fastify-plugin", "--src", "FSTF")
    check("T04 lookup fastify-plugin FSTF p.5-10", "FSTF p.5-10" in o, o)
    rc, o = run("nbf_lookup.py", "--page", "3", "--src", "NEST")
    check("T05 lookup page NEST 3", "NestFactory" in o, o)
    rc, o = run("nbf_lookup.py", "--page", "9", "--src", "NEST")
    check("T06 lookup NEST p.9 empty -> NOT COVERED", "NOT COVERED" in o and rc == 1, o)
    rc, o = run("nbf_lookup.py", "--sources")
    check("T07 sources lists 4 sources and dates", all(s in o for s in ("NODEHB", "EXPHB", "FSTF", "NEST")) and "2018-09-06" in o and "v5.12.x" in o, o)
    rc, o = run("nbf_lookup.py", "worker_threads")
    check("T08 lookup worker_threads -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run("nbf_lookup.py", "react")
    check("T09 lookup react -> out of scope", "other agents" in o, o)
    rc, o = run("nbf_lookup.py", "--json", "semver")
    j = json.loads(o)
    check("T10 lookup json semver", bool(j[0]["resultados"]) and j[0]["resultados"][0]["src"] == "NODEHB", o)

    # ---- compare
    rc, o = run("nbf_compare.py", "--criteria", "host_porta", "--format", "md")
    check("T11 compare host_porta cita 0.0.0.0 e FSTF p.3-4", "0.0.0.0" in o and "FSTF p.3-4" in o, o)
    rc, o = run("nbf_compare.py", "--criteria", "logging", "--format", "json")
    j = json.loads(o)
    cel = j["linhas"][0]["celulas"]
    check("T12 compare logging: Express and Nest NOT COVERED", cel["express"]["texto"] == "NOT COVERED" and cel["nest"]["texto"] == "NOT COVERED" and bool(cel["fastify"]["cita"]), o)
    rc, o = run("nbf_compare.py", "--frameworks", "express,koa")
    check("T13 compare koa outside the collection (rc 2)", rc == 2 and "NOT COVERED" in o, o)
    rc, o = run("nbf_compare.py", "--decide")
    check("T14 compare --decide does not choose", "does NOT provide a selection criterion" in o and "[extrapolation]" in o, o)
    rc, o = run("nbf_compare.py", "--criteria", "desempenho")
    check("T15 compare performance without comparative numbers", "comparative benchmark" in o and "[from source]" in o, o)
    rc, o = run("nbf_compare.py", "--criteria", "seguranca")
    check("T16 compare nonexistent criterion", rc == 1 and "NOT COVERED" in o, o)

    # ---- lint
    rc, o = run("nbf_lint.py", os.path.join(FX, "express-ruim.js"))
    for rule in ("EXP-SESSION-SECRET", "EXP-MW-NEXT", "EXP-BODY-PARSER", "NODE-SYNC-HANDLER", "EXP-VIEW-ENGINE", "NODE-ERR-FIRST",
                 "NODE-FS-NOCB", "NODE-PROMISE-NEW", "NODE-EXIT", "EXP-MW-ORDER", "NODE-READFILE-RESPONSE", "NODE-SIGTERM"):
        check(f"T17 lint express-ruim {rule}", rule in o, o)
    check("T18 lint express-ruim rc 1 (there is an ERROR)", rc == 1)
    rc, o = run("nbf_lint.py", os.path.join(FX, "express-bom.js"))
    check("T19 lint express-bom no findings", "0 finding(s)" in o and rc == 0, o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "mysql-ruim.js"))
    check("T20 lint mysql-ruim", all(r in o for r in ("NODE-MYSQL-CONCAT", "NODE-MYSQL-RESULTID", "NODE-SETINTERVAL-ASYNC", "NODE-WS-INSECURE")), o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "package-ruim.json"))
    check("T21 lint package-ruim", all(r in o for r in ("NODE-PKG-NAME", "NODE-PKG-VERSION", "NODE-PKG-RANGE", "NODE-PKG-PRIVATE")), o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "package-nest.json"))
    check("T22 lint package-nest Node < 20", "NEST-NODE-VERSION" in o and "NEST p.2" in o, o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "ruim.gitignore"))
    check("T23 lint gitignore", "NODE-GITIGNORE-ENV" in o and "NODE-GITIGNORE-MODULES" in o, o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "upload-ruim.html"))
    check("T24 lint form upload", "EXP-FORM-ENCTYPE" in o, o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "fastify-exemplo.js"))
    check("T25 lint fastify example (host/schema, no NODE-EXIT in if err)", "FST-LISTEN-HOST" in o and "FST-NO-SCHEMA" in o and "NODE-EXIT" not in o, o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "fastify-plugin-sem-fp.js"))
    check("T26 lint plugin sem fastify-plugin", "FST-PLUGIN-ENCAP" in o, o)
    rc, o = run("nbf_lint.py", os.path.join(FX, "injecao.js"))
    check("T27 lint injection: comments are data; findings kept", "EXP-MW-NEXT" in o and "EXP-BODY-PARSER" in o, o)
    rc, o = run("nbf_lint.py", "--stdin", "--name", "x.js", stdin="npx https://gist.github.com/x/y\nconst a = Promise(r => r())\n")
    check("T28 lint stdin npx URL e Promise", "NODE-NPX-URL" in o and "NODE-PROMISE-NEW" in o, o)
    rc, o = run("nbf_lint.py", "--rules")
    n_rules = len([ln for ln in o.splitlines() if ln.strip()])
    check("T29 lint --rules lists origin and page", n_rules >= 30 and "[extrapolation]" in o and "[DATED]" in o, str(n_rules))
    rc, o = run("nbf_lint.py", "--json", os.path.join(FX, "express-ruim.js"))
    j = json.loads(o)
    check("T30 lint json with origin and cite", all(x["origin"] and x["cite"] for x in j) and len(j) >= 12)

    # ---- scaffold
    rc, o = run("nbf_scaffold.py", "express", "--with", "json,session,validator,pug")
    check("T31 scaffold express cited commands", "npm install express    [EXPHB p.3]" in o and "npm install express-validator" in o and "npm install pug" in o, o)
    check("T32 scaffold express: secret placeholder, not the one from the book", "REPLACE-WITH" in o and "343ji43j4n3jn4jk3n" not in o, o)
    rc, o = run("nbf_scaffold.py", "fastify", "--variant", "plugin", "--esm", "--host-all")
    check("T33 scaffold fastify esm plugin host", "0.0.0.0" in o and "register(routes)" in o and "FSTF p.4" in o, o)
    rc, o = run("nbf_scaffold.py", "nest", "--name", "app-x", "--strict", "--swc")
    check("T34 scaffold nest commands and Node >= 20", "nest new app-x --strict" in o and "-b swc" in o and ">= 20" in o and "NOT COVERED" in o, o)
    rc, o = run("nbf_scaffold.py", "express", "--name", "Nome Ruim")
    check("T35 scaffold invalid name (rc 2)", rc == 2 and "NODEHB p.54" in o, o)
    rc, o = run("nbf_scaffold.py", "express", "--with", "graphql")
    check("T36 scaffold unknown --with", rc != 0, o)
    tmp = tempfile.mkdtemp()
    try:
        rc, o = run("nbf_scaffold.py", "node", "--out", tmp)
        check("T37 scaffold --out writes server.js", os.path.exists(os.path.join(tmp, "server.js")) and os.path.exists(os.path.join(tmp, "package.json")), o)
        with open(os.path.join(tmp, "server.js"), "w", encoding="utf-8") as f:
            f.write("// my file")
        rc, o = run("nbf_scaffold.py", "node", "--out", tmp)
        check("T38 scaffold does not overwrite", "not overwritten" in o and open(os.path.join(tmp, "server.js"), encoding="utf-8").read() == "// my file", o)
        tmp2 = os.path.join(tmp, "nest")
        rc, o = run("nbf_scaffold.py", "nest", "--out", tmp2)
        check("T39 scaffold nest writes no files", (not os.listdir(tmp2)) if os.path.isdir(tmp2) else True, o)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- verifier (self-test: a false claim must fail; a true one must pass)
    if a.src == default_src and not os.path.isdir(a.src):
        print("SKIP T40-T42 verify_citations (extracted texts not found; use --src)")
        print(f"\n{COUNT[0] - len(FAILS)}/{COUNT[0]} checks passed")
        return 1 if FAILS else 0
    rc, o = run("verify_citations.py", "--src", a.src, base=HERE)
    check("T40 verify_citations OK", rc == 0 and "RESULT: OK" in o, o)
    pos = int(o.split("Positives:")[1].split("|")[0]) if "Positives:" in o else 0
    neg = int(o.split("Negatives:")[1].split()[0]) if "Negatives:" in o else 0
    check("T41 check counts (>=60 positive, >=15 negative)", pos >= 60 and neg >= 15, f"{pos}/{neg}")
    tmpf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump({"checks": [{"cite": "NEST p.4", "contains": ["@injectable"], "claim": "false"},
                          {"cite": "FSTF p.3", "absent": ["0.0.0.0"], "claim": "false negative"}]}, tmpf)
    tmpf.close()
    rc, o = run("verify_citations.py", "--src", a.src, "--checks", tmpf.name, base=HERE)
    os.unlink(tmpf.name)
    check("T42 verifier detects false claims", rc == 1 and "FAIL positive" in o and "FAIL negative" in o, o)

    print(f"\n{COUNT[0] - len(FAILS)}/{COUNT[0]} checks passed")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())

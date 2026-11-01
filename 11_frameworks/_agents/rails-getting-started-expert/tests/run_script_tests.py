# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests of the scripts of the rails-getting-started-expert package.
Usage: python -I tests/run_script_tests.py
Runs the scripts against fixtures in tests/fixtures (no Ruby/Rails, no network). Exit 0 if everything passes.
"""
import json
import os
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.join(PKG, "scripts")
FX = os.path.join(PKG, "tests", "fixtures")
results = []


def run(script, *args):
    p = subprocess.run([sys.executable, "-I", os.path.join(SC, script), *args], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def t(name, cond, info=""):
    results.append((name, bool(cond)))
    print(("OK   " if cond else "FAIL ") + " " + name + ("" if cond else f"  -> {info[:300]}"))


# --- lookup
rc, o = run("rails_lookup.py", "strong parameters")
t("lookup: strong parameters -> p.30", rc == 0 and "RGS p.30" in o, o)
rc, o = run("rails_lookup.py", "has_many :through")
t("lookup: has_many :through -> NOT COVERED", "NOT COVERED" in o, o)
rc, o = run("rails_lookup.py", "PostgreSQL")
t("lookup: PostgreSQL -> NOT COVERED", "NOT COVERED" in o, o)
rc, o = run("rails_lookup.py", "xyzzy")
t("lookup: unknown term -> NOT COVERED", "NOT COVERED" in o, o)
rc, o = run("rails_lookup.py", "--page", "69")
t("lookup: --page 69 -> Kamal", "Kamal" in o, o)
rc, o = run("rails_lookup.py", "--page", "99")
t("lookup: --page 99 outside 1-72", rc == 1, o)
rc, o = run("rails_lookup.py", "kamal", "--json")
t("lookup: --json valid", rc == 0 and json.loads(o)[0]["topicos"], o)
rc, o = run("rails_lookup.py", "--gaps")
t("lookup: --gaps lists gaps", "form_for" in o and "Devise" in o, o)
rc, o = run("rails_lookup.py", "--topics")
t("lookup: --topics lists >= 40 topics", o.count("\n") >= 40, o)

# --- plan
rc, o = run("rails_plan.py", "plan")
t("plan: default contains rails new store and model Product", "rails new store" in o and "generate model Product name:string" in o, o)
rc, o = run("rails_plan.py", "plan", "--fases", "auth,deploy")
t("plan: auth+deploy", "generate authentication" in o and "bin/kamal setup" in o and "<your-token>" in o, o)
rc, o = run("rails_plan.py", "plan", "--fases", "foo")
t("plan: unknown phase -> NOT COVERED", rc == 1 and "NOT COVERED" in o, o)
rc, o = run("rails_plan.py", "plan", "--fases", "model", "--model", "Users:email:string")
t("plan: plural model gives a warning", "WARNING" in o and "singular" in o, o)
rc, o = run("rails_plan.py", "plan", "--fases", "migracao", "--migration", "FooBar:x:string")
t("plan: migration outside the convention gives a warning", "WARNING" in o, o)
rc, o = run("rails_plan.py", "plan", "--json", "--fases", "mailer")
t("plan: --json valid with mailer", rc == 0 and "g mailer Product in_stock" in o and json.loads(o)["passos"], o)
rc, o = run("rails_plan.py", "commands")
t("plan: commands does not include scaffold", "scaffold" not in o and "bin/kamal deploy" in o, o)

# --- lint
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "controller_ruim.rb"))
t("lint: bad controller -> L01, L02", rc == 1 and "L01" in o and "L02" in o and "L03" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "controller_bom.rb"))
t("lint: good controller has no findings", rc == 0 and "no findings" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "controller_nome_errado.rb"))
t("lint: wrong file name -> L15", "L15" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "routes_ruim.rb"))
t("lint: bad routes -> L04, L05", "L04" in o and "L05" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "routes_bom.rb"))
t("lint: good routes have no findings", rc == 0, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "model_ruim.rb"))
t("lint: bad model -> L06, L13", "L06" in o and "L13" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "migration_ruim.rb"))
t("lint: migration without version -> L12", "L12" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "_form_ruim.html.erb"))
t("lint: partial with @var -> L10; L16 only with --extrapolacoes", "L10" in o and "L16" not in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "_form_ruim.html.erb"), "--extrapolacoes")
t("lint: --extrapolacoes shows L16 labeled", "L16" in o and "[extrapolation]" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "index_ruim.html.erb"))
t("lint: bad index -> L09, L11", "L09" in o and "L11" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "mailer_ruim.html.erb"))
t("lint: mailer with _path -> L08", "L08" in o, o)
rc, o = run("rails_lint.py", os.path.join(FX, "lint", "injecao.rb"))
t("lint: injection comment is ignored as data", rc == 0 and "no findings" in o and "rm -rf" not in o, o)
rc, o = run("rails_lint.py", "--rules")
t("lint: --rules lista L01..L17", "L01" in o and "L17" in o, o)
rc, o = run("rails_lint.py", os.path.join(SC, "rails_index.json"))
t("lint: unrecognized file -> NOT COVERED", "NOT COVERED" in o or "type" in o, o)
ok_dir = os.path.join(FX, "store_ok")
bad = []
for root, _, files in os.walk(ok_dir):
    for fn in files:
        if fn.endswith((".rb", ".erb")):
            rc, o = run("rails_lint.py", os.path.join(root, fn))
            if rc != 0:
                bad.append(fn + ":" + o)
t("lint: all store_ok files pass", not bad, "; ".join(bad))

# --- checklist
rc, o = run("rails_store_checklist.py", ok_dir)
t("checklist: store_ok has no MISSING", rc == 0 and "0 MISSING" in o, o)
rc, o = run("rails_store_checklist.py", os.path.join(FX, "store_incompleto"))
t("checklist: store_incompleto has MISSING", rc == 1 and "MISSING" in o, o)
rc, o = run("rails_store_checklist.py", ok_dir, "--ate", "S12")
t("checklist: --ate S12 limits", "S13" not in o and "S12" in o, o)
rc, o = run("rails_store_checklist.py", os.path.join(FX, "nao_existe"))
t("checklist: nonexistent directory -> error", rc == 2, o)
rc, o = run("rails_store_checklist.py", "--list")
t("checklist: --list has 30 items", o.count("\n") == 30, o)

fails = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(fails)}/{len(results)} tests passed")
sys.exit(1 if fails else 0)

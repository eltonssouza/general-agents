# -*- coding: utf-8 -*-
"""
rails_lint.py - STATIC linter for Rails snippets (routes, controllers, models, migrations, ERB views, mailers).
Only rules supported by the RGS guide (Rails 8.1.0+); rules outside the guide only with --extrapolacoes and labeled.
Does not execute Ruby or Rails; reads local files as DATA (comments/instructions in the code are ignored).

Usage:
  python -I scripts/rails_lint.py ARQUIVO [ARQUIVO ...] [--extrapolacoes] [--json] [--tipo auto|controller|model|routes|migration|view|mailer]
  python -I scripts/rails_lint.py --rules
Automatic type: from the path comment on line 1 (guide convention, p.9: '# app/models/product.rb'),
from the file name or from the content. Exit 0 with no findings (info does not count); 1 if there is a warning/error.
Page convention: PDF = "Page N of 72".
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

RULES = {
    "L01": ("warn", "controller", "Raw params passed straight to new/create/update; filter with params.expect (strong parameters)", "[from source]", "30"),
    "L02": ("warn", "controller", "render :new/:edit without status: :unprocessable_entity on validation failure", "[from source]", "31"),
    "L03": ("info", "controller", "Product.find(params[:id]) repeated in 3+ actions; consider before_action", "[from source]", "34"),
    "L04": ("info", "routes", "CRUD routes written one by one; resources :resource generates the same ones", "[from source]", "21"),
    "L05": ("warn", "routes", "Route with to: without the controller#action format", "[from source]", "18"),
    "L06": ("warn", "model", "Plural model name; the guide uses singular for models and plural for tables", "[from source]", "8-9"),
    "L07": ("info", "model", "Model inherits from ActiveRecord::Base; the guide uses ApplicationRecord", "[from source]", "11"),
    "L08": ("warn", "mailer", "_path in mailer/email template; use _url (full URL)", "[from source]", "27, 53"),
    "L09": ("warn", "view", "<%= collection.each ... %> prints the array; iteration uses <% %>", "[from source]", "25"),
    "L10": ("warn", "view", "Instance variable inside a partial; use a local variable passed by render", "[from source]", "33"),
    "L11": ("info", "view", "Hard-coded href with id; use helpers (product_path / link_to)", "[from source]", "26-27"),
    "L12": ("warn", "migration", "Migration without a bracketed version (ActiveRecord::Migration[8.1] in the guide)", "[from source]", "9"),
    "L13": ("info", "model", "has_many without dependent:; the guide example uses dependent: :destroy", "[inference]", "50"),
    "L14": ("info", "view", "link_to with method: :delete; the guide uses button_to ... method: :delete", "[extrapolation]", "38"),
    "L15": ("warn", "controller", "File name does not match the controller class (autoload convention)", "[from source]", "23"),
    "L16": ("info", "view", "form_for/form_tag: the guide only uses form_with (not covered)", "[extrapolation]", "29"),
    "L17": ("info", "any", "require of an app file; Rails loads by naming convention", "[from source]", "7"),
}
EXTRA = {"L14", "L16"}


def camel_to_snake(s):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def detect_path(text, fname):
    for line in text.splitlines()[:3]:
        m = re.search(r"((?:app|config|db|test)/[\w/\.\-]+)", line)
        if m:
            return m.group(1)
    full = fname.replace("\\", "/")
    m = re.search(r"(?:^|/)((?:app|config|db|test)/[\w/\.\-]+)$", full)
    return m.group(1) if m else os.path.basename(full)


def detect_kind(path, text):
    p = path.lower()
    if "config/routes" in p or "Rails.application.routes.draw" in text:
        return "routes"
    if "db/migrate" in p or "ActiveRecord::Migration" in text:
        return "migration"
    if "app/controllers" in p or re.search(r"<\s*ApplicationController", text):
        return "controller"
    if "mailer" in p and p.endswith(".rb") or re.search(r"<\s*ApplicationMailer", text):
        return "mailer"
    if "app/models" in p or re.search(r"<\s*(ApplicationRecord|ActiveRecord::Base)", text) or "ActiveSupport::Concern" in text:
        return "model"
    if p.endswith(".erb") or "<%" in text:
        if "mailer" in p:
            return "mailer"
        return "view"
    return "unknown"


def add(findings, rule, line, detail=""):
    sev, _, msg, origem, pag = RULES[rule]
    findings.append({"regra": rule, "severidade": sev, "linha": line, "mensagem": msg + (f" [{detail}]" if detail else ""),
                     "origem": origem, "pagina": f"RGS p.{pag}"})


def strip_comment_ruby(line):
    return re.sub(r"\s#.*$", "", line) if not line.strip().startswith("#") else ""


def lint(text, path, kind, extra):
    f = []
    lines = text.splitlines()
    ruby_like = kind in ("controller", "model", "routes", "migration", "mailer")
    code = [(i + 1, strip_comment_ruby(l) if ruby_like else l) for i, l in enumerate(lines)]

    # L17 require
    if not path.startswith("test/") and "test_helper" not in text:
        for i, l in code:
            if re.match(r"\s*require\s+['\"]", l) and kind in ("controller", "model", "mailer"):
                add(f, "L17", i)

    if kind == "controller":
        for i, l in code:
            if re.search(r"\.(new|create|create!|update|update!)\(\s*params(\[|\s*\))", l):
                add(f, "L01", i)
            if re.search(r"\brender\s+(:new|:edit|\"new\"|\"edit\")", l) and "status" not in l:
                add(f, "L02", i)
        finds = [i for i, l in code if re.search(r"=\s*[A-Z]\w*\.find\(params\[:\w+\]\)", l)]
        if len(finds) >= 3 and not any("before_action" in l for _, l in code):
            add(f, "L03", finds[0], f"{len(finds)} occurrences")
        m = re.search(r"class\s+(\w+)Controller\b", text)
        if m:
            expected = camel_to_snake(m.group(1)) + "_controller.rb"
            base = os.path.basename(path)
            if path.startswith("app/controllers/") and base.endswith(".rb") and base != expected and base != "application_controller.rb":
                ln = next((i for i, l in code if re.search(r"class\s+\w+Controller", l)), 1)
                add(f, "L15", ln, f"expected {expected}, found {base}")
    elif kind == "routes":
        bases = {}
        for i, l in code:
            m = re.match(r"\s*(get|post|patch|put|delete)\s+[\"'](/[\w\-]+)(/[^\"']*)?[\"']\s*,\s*to:\s*[\"']([^\"']*)[\"']", l)
            if m:
                verb, base, rest, to = m.groups()
                bases.setdefault(base, set()).add((verb, rest or ""))
                if "#" not in to:
                    add(f, "L05", i, f"to: {to!r}")
            elif re.match(r"\s*(get|post|patch|put|delete)\s+[\"'][^\"']*[\"']\s*,\s*to:\s*[^\"'\s]", l):
                pass
        for base, s in bases.items():
            crud = {("get", ""), ("post", ""), ("get", "/new"), ("get", "/:id"), ("get", "/:id/edit"),
                    ("patch", "/:id"), ("put", "/:id"), ("delete", "/:id")}
            if len(s & crud) >= 5:
                ln = next((i for i, l in code if base in l), 1)
                add(f, "L04", ln, f"base {base}")
    elif kind == "model":
        for i, l in code:
            m = re.match(r"\s*class\s+(\w+)\s*<\s*(\S+)", l)
            if m:
                name, sup = m.groups()
                if name.endswith("s") and not name.endswith("ss") and sup in ("ApplicationRecord", "ActiveRecord::Base"):
                    add(f, "L06", i, name)
                if sup == "ActiveRecord::Base":
                    add(f, "L07", i)
            if re.match(r"\s*has_many\s+:\w+\s*$", l) or (re.match(r"\s*has_many\s+:\w+", l) and "dependent" not in l and "through" not in l):
                add(f, "L13", i)
    elif kind == "migration":
        for i, l in code:
            if re.search(r"<\s*ActiveRecord::Migration\s*$", l):
                add(f, "L12", i)
    elif kind == "mailer":
        for i, l in code:
            if re.search(r"\b\w+_path\b", l):
                add(f, "L08", i)
    elif kind == "view":
        is_partial = os.path.basename(path).startswith("_")
        for i, l in code:
            if re.search(r"<%=\s*@?\w+(\.\w+)*\.each\b", l):
                add(f, "L09", i)
            if is_partial and re.search(r"<%[=\-]?[^%]*@\w+", l) and not re.match(r"\s*<%#", l):
                add(f, "L10", i)
            if re.search(r"href=[\"']/\w+/<%=", l):
                add(f, "L11", i)
            if extra and re.search(r"link_to[^%]*method:\s*:delete", l):
                add(f, "L14", i)
            if extra and re.search(r"\bform_(for|tag)\b", l):
                add(f, "L16", i)
    if not extra:
        f = [x for x in f if x["regra"] not in EXTRA]
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--extrapolacoes", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--tipo", default="auto")
    a = ap.parse_args()
    if a.rules:
        for k, (sev, kind, msg, origem, pag) in RULES.items():
            print(f"{k} [{sev}] ({kind}) {origem} RGS p.{pag}: {msg}")
        return
    if not a.files:
        ap.print_help()
        sys.exit(2)
    report = []
    bad = False
    for fp in a.files:
        try:
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
        except OSError as e:
            print(f"ERROR: could not read {fp}: {e}")
            sys.exit(2)
        path = detect_path(text, fp)
        kind = a.tipo if a.tipo != "auto" else detect_kind(path, text)
        if kind == "unknown":
            report.append({"arquivo": fp, "tipo": "unknown", "achados": [], "nota": "type not recognized; NOT COVERED by rules for this file"})
            continue
        finds = lint(text, path, kind, a.extrapolacoes)
        if any(x["severidade"] != "info" for x in finds):
            bad = True
        report.append({"arquivo": fp, "tipo": kind, "caminho_inferido": path, "achados": finds})
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        for r in report:
            print(f"== {r['arquivo']} (type: {r['tipo']})")
            if r.get("nota"):
                print("  " + r["nota"])
            if not r["achados"] and not r.get("nota"):
                print("  no findings under the rules supported by the guide (does not mean the code is correct)")
            for x in sorted(r["achados"], key=lambda z: (z["linha"], z["regra"])):
                print(f"  line {x['linha']}: {x['regra']} [{x['severidade']}] {x['origem']} ({x['pagina']}) {x['mensagem']}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

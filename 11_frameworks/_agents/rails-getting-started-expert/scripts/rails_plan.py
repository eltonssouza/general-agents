# -*- coding: utf-8 -*-
"""
rails_plan.py - generates a PLAN of `rails ...` commands using ONLY the command patterns the RGS guide shows
(Rails 8.1.0+). Executes nothing; it only prints text/JSON.

Usage:
  python -I scripts/rails_plan.py list                         # available phases
  python -I scripts/rails_plan.py plan [--app NOME] [--fases base,model,...] [--model Nome:attr:tipo,attr:tipo ...]
                                       [--migration NomeDaMigracao:coluna:tipo ...] [--controller Nome:acao,acao ...]
                                       [--mailer Nome:acao ...] [--json]
  python -I scripts/rails_plan.py commands                     # all commands of the guide with page

Phases: ambiente, app, banco, model, migracao, controller, rotas, auth, cache, rich_text, mailer, testes, qualidade, deploy
(English aliases accepted: environment, database, migration, routes, tests, quality).
Each command carries the guide page. Patterns not shown in the guide (scaffold, --api, db:seed...) are NOT generated.
Page convention: PDF = "Page N of 72".
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

CMDS = [
    ("rails --version", 2, "check the version (>= 8.1.0)"),
    ("rails --help", 3, "list commands"),
    ("rails new {app}", 3, "generate the app"),
    ("rails new --help", 3, "see the generator flags"),
    ("bin/rails db:create", 5, "create the database"),
    ("bin/rails server", 6, "start Puma on localhost:3000"),
    ("bin/rails generate model {Model} {attrs}", 8, "generate model + migration + test + fixture"),
    ("bin/rails db:migrate", 9, "apply migrations"),
    ("bin/rails db:rollback", 10, "undo the last migration"),
    ("bin/rails console", 10, "interactive console"),
    ("bin/rails routes", 21, "list routes"),
    ("bin/rails generate controller {Controller} {acao} --skip-routes", 22, "generate controller without changing routes"),
    ("bin/rails generate authentication", 38, "generate authentication (User, Session)"),
    ("bin/rails dev:cache", 41, "enable caching in development"),
    ("bin/rails action_text:install", 42, "install Action Text"),
    ("bundle install", 42, "install gems"),
    ("bin/rails generate migration {MigrationName} {cols}", 47, "migration by name convention"),
    ("bin/rails g mailer {Mailer} {acao}", 52, "generate mailer"),
    ("bin/rails test", 65, "run the suite"),
    ("bin/rubocop", 66, "check formatting"),
    ("bin/rubocop -a", 67, "fix formatting"),
    ("bin/brakeman", 67, "security analysis"),
    ("bin/kamal setup", 69, "first deploy"),
    ("bin/kamal deploy", 70, "new deploys"),
    ("bin/kamal console", 70, "console in production"),
]

PHASES = ["ambiente", "app", "banco", "model", "migracao", "controller", "rotas", "auth", "cache",
          "rich_text", "mailer", "testes", "qualidade", "deploy"]
DEFAULT = ["ambiente", "app", "banco", "model", "migracao", "controller", "rotas"]

# English aliases for the phase names (Portuguese names remain canonical).
ALIASES = {"environment": "ambiente", "database": "banco", "migration": "migracao", "routes": "rotas",
           "tests": "testes", "quality": "qualidade"}

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def step(cmd, page, why, note=None):
    d = {"comando": cmd, "pagina": page, "motivo": why}  # JSON keys kept (stable interface)
    if note:
        d["nota"] = note
    return d


def split_spec(spec):
    """'Name:a:t,b:t' -> ('Name', 'a:t b:t'): the 1st ':' separates the name; ',' separates attributes/actions."""
    name, _, rest = spec.partition(":")
    return name, " ".join(x.strip() for x in rest.split(",") if x.strip())


def build(app, phases, models, migrations, controllers, mailers):
    out = []
    warns = []
    if "ambiente" in phases:
        out.append(step("rails --version", 2, "check Rails >= 8.1.0 (Ruby >= 3.2)"))
    if "app" in phases:
        if not NAME_RE.match(app):
            warns.append(f"Invalid app name for this plan: {app!r}")
        out.append(step(f"rails new {app}", 3, "generate the app"))
        out.append(step(f"cd {app}", 3, "enter the directory"))
    if "banco" in phases:
        out.append(step("bin/rails db:create", 5, "create the database (SQLite is the default, p.8)"))
        out.append(step("bin/rails server", 6, "start the server and open http://localhost:3000", "Inside the app use bin/rails (p.6)"))
    if "model" in phases:
        for m in models:
            name, attrs = split_spec(m)
            if not NAME_RE.match(name):
                warns.append(f"Invalid model name: {name!r}")
                continue
            if name.endswith("s") and not name.endswith("ss"):
                warns.append(f"Model {name!r} looks plural; the guide uses singular model names (p.8-9).")
            out.append(step(f"bin/rails generate model {name} {attrs}".rstrip(), 8,
                            "generates migration, model, test and fixture",
                            "Attributes in the format name:type or name:belongs_to (p.8, 49)"))
    if "migracao" in phases or "model" in phases:
        out.append(step("bin/rails db:migrate", 9, "apply migrations"))
        for mg in migrations:
            name, cols = split_spec(mg)
            if not NAME_RE.match(name):
                warns.append(f"Invalid migration name: {name!r}")
                continue
            if not re.match(r"^Add[A-Z]\w*To[A-Z]\w*$", name):
                warns.append(f"Migration {name!r} does not follow add_<columns>_to_<table>; the guide only shows that convention (p.47).")
            out.append(step(f"bin/rails generate migration {name} {cols}".rstrip(), 47,
                            "migration by name convention",
                            "Edit the file, for example default: 0 (p.48), and run db:migrate"))
            out.append(step("bin/rails db:migrate", 48, "apply the new migration"))
    if "controller" in phases:
        for c in controllers:
            name, acts = split_spec(c)
            if not NAME_RE.match(name):
                warns.append(f"Invalid controller name: {name!r}")
                continue
            out.append(step(f"bin/rails generate controller {name} {acts} --skip-routes".replace("  ", " "), 22,
                            "generates controller, views, test and helper; --skip-routes because the routes already exist"))
    if "rotas" in phases:
        out.append(step("bin/rails routes", 21, "check the routes (after editing config/routes.rb)"))
    if "auth" in phases:
        out.append(step("bin/rails generate authentication", 38, "generates User, Session, controllers and views"))
        out.append(step("bin/rails db:migrate", 38, "create the User and Session tables"))
        out.append(step("bin/rails console", 39, "create the User with User.create! (sample email and password)",
                        "Then restart the server to load the bcrypt gem (p.39)"))
    if "cache" in phases:
        out.append(step("bin/rails dev:cache", 41, "enable caching in development"))
    if "rich_text" in phases:
        out.append(step("bin/rails action_text:install", 42, "install Action Text"))
        out.append(step("bundle install", 42, "install gems"))
        out.append(step("bin/rails db:migrate", 42, "Action Text migrations", "Restart the server (p.42)"))
    if "mailer" in phases:
        for ml in mailers:
            name, acts = split_spec(ml)
            if not NAME_RE.match(name):
                warns.append(f"Invalid mailer name: {name!r}")
                continue
            out.append(step(f"bin/rails g mailer {name} {acts}".rstrip(), 52,
                            "generates mailer and HTML/text views", "Use _url (not _path) in emails (p.53)"))
    if "testes" in phases:
        out.append(step("bin/rails test", 65, "run the suite (or pass a file path)"))
    if "qualidade" in phases:
        out.append(step("bin/rubocop", 66, "formatting"))
        out.append(step("bin/brakeman", 67, "security"))
    if "deploy" in phases:
        out.append(step("export KAMAL_REGISTRY_PASSWORD=<your-token>", 69,
                        "registry token (do not share the real value)", "Edit config/deploy.yml first (p.68-69)"))
        out.append(step("bin/kamal setup", 69, "first deploy"))
        out.append(step("bin/kamal console", 70, "create a User in production with User.create!"))
        out.append(step("bin/kamal deploy", 70, "subsequent deploys"))
    return out, warns


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list")
    sub.add_parser("commands")
    p = sub.add_parser("plan")
    p.add_argument("--app", default="store")
    p.add_argument("--fases", default=",".join(DEFAULT))
    p.add_argument("--model", action="append", default=[])
    p.add_argument("--migration", action="append", default=[])
    p.add_argument("--controller", action="append", default=[])
    p.add_argument("--mailer", action="append", default=[])
    p.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.cmd == "list":
        print("Phases:", ", ".join(PHASES))
        print("Default:", ", ".join(DEFAULT))
        return
    if a.cmd == "commands":
        for c, pg, why in CMDS:
            print(f"RGS p.{pg:<3} {c:70} {why}")
        return
    if a.cmd != "plan":
        ap.print_help()
        sys.exit(2)

    phases = [ALIASES.get(x.strip(), x.strip()) for x in a.fases.split(",") if x.strip()]
    bad = [x for x in phases if x not in PHASES]
    if bad:
        print(f"Unknown phases: {bad}. NOT COVERED in the guide. Valid: {PHASES}")
        sys.exit(1)
    models = a.model or (["Product:name:string"] if "model" in phases else [])
    controllers = a.controller or (["Products:index"] if "controller" in phases else [])
    mailers = a.mailer or (["Product:in_stock"] if "mailer" in phases else [])
    steps, warns = build(a.app, phases, models, a.migration, controllers, mailers)
    if a.json:
        print(json.dumps({"fonte": "RGS (Rails 8.1.0+)", "passos": steps, "avisos": warns}, ensure_ascii=False, indent=1))
        return
    print("Plan (only commands shown in the RGS guide, Rails 8.1.0+). Nothing was executed.")
    for i, s in enumerate(steps, 1):
        line = f"{i:2}. $ {s['comando']}   [RGS p.{s['pagina']}] {s['motivo']}"
        print(line)
        if "nota" in s:
            print(f"      note: {s['nota']}")
    for w in warns:
        print(f"WARNING: {w}")
    print("Code edits (routes, controllers, views) are not commands: see references/procedimentos.md.")


if __name__ == "__main__":
    main()

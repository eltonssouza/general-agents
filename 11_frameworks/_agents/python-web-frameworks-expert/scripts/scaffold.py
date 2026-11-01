# -*- coding: utf-8 -*-
"""
scaffold.py - skeleton/command-script generator using ONLY the commands and code snippets the sources show.
NEVER runs commands or the framework: prints the script (and, with --out, writes only example .py files).

  django  : commands from DJT p.1-4 (python -m django --version; django-admin startproject; python manage.py runserver / startapp)
            and the three code files the tutorial writes by hand (APP/views.py, APP/urls.py, PROJ/urls.py)
  fastapi : commands from FAPI p.5-7, 20-21 (uv add "fastapi[standard]"; fastapi dev) and main.py in 3 variants
            (basic = p.5; async = p.6; body = p.10-11)
  flask   : NOT COVERED for code/commands (the FLT is only an index); prints only the tutorial's table of sections

Stdlib only, no network, deterministic. Usage:
  python -I scripts/scaffold.py django [--project mysite] [--app polls] [--out DIR] [--force]
  python -I scripts/scaffold.py fastapi [--variant basic|async|body] [--out DIR] [--force]
  python -I scripts/scaffold.py flask
"""
import argparse
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

DJ_VIEWS = '''from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the {app} index.")
'''

DJ_APP_URLS = '''from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
'''

DJ_PROJ_URLS = '''from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("{app}/", include("{app}.urls")),
    path("admin/", admin.site.urls),
]
'''

FA_BASIC = '''from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
'''

FA_ASYNC = FA_BASIC.replace("def read_root", "async def read_root").replace("def read_item", "async def read_item")

FA_BODY = '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
'''

FLASK_TOC = ["Project Layout", "Application Setup", "Define and Access the Database", "Blueprints and Views", "Templates",
             "Static Files", "Blog Blueprint", "Make the Project Installable", "Test Coverage", "Deploy to Production",
             "Keep Developing!"]


def check_name(label, value, forbidden=()):
    if value in forbidden:
        print(f"ERROR: {label} name '{value}' must be avoided [from source: DJT p.1 - conflicts with Django itself or with a Python package].")
        return False
    if not NAME_RE.match(value):
        print(f"ERROR: {label} name '{value}' is invalid; use letters, digits and _ starting with a letter/_ "
              "[extrapolation: script restriction to generate safe paths and valid imports; the DJT only forbids django and test].")
        return False
    return True


def write_files(out, files, force):
    for rel, content in files:
        path = os.path.join(out, rel)
        if os.path.exists(path) and not force:
            print(f"REFUSED: {path} already exists (use --force to overwrite).")
            return False
    for rel, content in files:
        path = os.path.join(out, rel)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"written: {path}")
    return True


def do_django(a):
    if not check_name("project", a.project, ("django", "test")):
        return 1
    if not check_name("app", a.app):
        return 1
    print("# Django script (DJT commands; NOT executed by this script). Django 5.0, Python 3.10+ [DATED] 5.0 docs (DJT p.1)")
    print("1. python -m django --version                 # checks the installation and version (DJT p.1)")
    print(f"2. django-admin startproject {a.project}        # creates the project (DJT p.1)")
    print(f"3. cd {a.project}   # outer directory, where manage.py lives (DJT p.2)")
    print("4. python manage.py runserver                 # development server at http://127.0.0.1:8000/; do not use in production (DJT p.2)")
    print(f"5. python manage.py startapp {a.app}            # creates the app in manage.py's folder (DJT p.3)")
    print(f"6. edit {a.app}/views.py, create {a.app}/urls.py and include it in {a.project}/urls.py (files below; DJT p.3-4)")
    print(f"7. python manage.py runserver  and open http://localhost:8000/{a.app}/ (DJT p.4)")
    print("Note: the unapplied-migrations warning can be ignored for now (DJT p.2); the database is covered in part 2 (NOT COVERED here).\n")
    files = [
        (os.path.join(a.app, "views.py"), DJ_VIEWS.format(app=a.app)),
        (os.path.join(a.app, "urls.py"), DJ_APP_URLS),
        (os.path.join(a.project, "urls.py"), DJ_PROJ_URLS.format(app=a.app)),
    ]
    for rel, content in files:
        print(f"--- {rel.replace(os.sep, '/')} ---\n{content}")
    if a.out:
        print("Writing only the 3 files above (they would overwrite those generated by startproject/startapp: use --out on a scratch folder).")
        return 0 if write_files(a.out, files, a.force) else 1
    return 0


def do_fastapi(a):
    code = {"basic": FA_BASIC, "async": FA_ASYNC, "body": FA_BODY}[a.variant]
    print("# FastAPI script (FAPI commands; NOT executed). Badge v0.141.1, Python 3.10-3.14 [DATED] (FAPI p.1)")
    print('1. uv add "fastapi[standard]"      # FAPI p.20; in quotes so it works in all terminals (FAPI p.5); requires uv installed (FAPI p.4)')
    print('   alternative: inside a virtual environment, install fastapi[standard] with pip (FAPI p.5; the exact syntax of the terminal block was not captured)')
    print("2. create main.py (below) (FAPI p.5" + (", p.6" if a.variant == "async" else ", p.10-11" if a.variant == "body" else "") + ")")
    print("3. fastapi dev                     # reads main.py, detects the app, uses Uvicorn, auto-reload (FAPI p.7)")
    print("4. open http://127.0.0.1:8000/items/5?q=somequery (FAPI p.7), /docs (Swagger UI, p.8) and /redoc (ReDoc, p.9)")
    print("Deploy: command NOT COVERED (the terminal block on FAPI p.19 came out empty).\n")
    print(f"--- main.py (variant {a.variant}) ---\n{code}")
    if a.out:
        return 0 if write_files(a.out, [("main.py", code)], a.force) else 1
    return 0


def do_flask(a):
    print("NOT COVERED: Flask code and commands: the FLT (3 pp.) is only the introduction and table of sections of the 'Flaskr' tutorial (FLT p.1-3).")
    print("Table of sections (titles only, FLT p.1):")
    for i, t in enumerate(FLASK_TOC, 1):
        print(f"  {i}. {t}")
    print("No command (installation, running, database, tests, deploy) appears in the source. Any detail beyond this would be [extrapolation].")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="fw")
    d = sub.add_parser("django")
    d.add_argument("--project", default="mysite")
    d.add_argument("--app", default="polls")
    d.add_argument("--out")
    d.add_argument("--force", action="store_true")
    f = sub.add_parser("fastapi")
    f.add_argument("--variant", choices=["basic", "async", "body"], default="basic")
    f.add_argument("--out")
    f.add_argument("--force", action="store_true")
    sub.add_parser("flask")
    a = ap.parse_args()
    if a.fw == "django":
        return do_django(a)
    if a.fw == "fastapi":
        return do_fastapi(a)
    if a.fw == "flask":
        return do_flask(a)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

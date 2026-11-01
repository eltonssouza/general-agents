# -*- coding: utf-8 -*-
"""
nbf_compare.py - Express x Fastify x NestJS comparer using ONLY criteria that the sources actually provide.

Each cell carries a paraphrase and the citation (ACRONYM p.N, PDF page) or "NOT COVERED".
Sources: EXPHB (Express Handbook, 2022-11-18), FSTF (Fastify Getting Started, v5.12.x),
NEST (NestJS First steps, Node >= 20, (c) 2017-2026), NODEHB (Node Handbook, 2018-09-06).

The script does NOT pick a framework for you: the sources give no decision rule between them
(see --decide). Differences here are descriptions of the text, not recommendations.

Usage:
  python -I scripts/nbf_compare.py [--criteria id1,id2] [--frameworks express,fastify,nest]
                                   [--format md|json|text] [--list] [--decide]
Criteria ids are the Portuguese ids shown by --list; English aliases are also accepted
(e.g. install, routes, host_port, validation, sessions_cookies, testing, performance).
Deterministic, stdlib, no network.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FW = ["express", "fastify", "nest"]
FWNAME = {"express": "Express (EXPHB)", "fastify": "Fastify (FSTF, v5.12.x)", "nest": "NestJS (NEST)"}
SC = None  # cell with no coverage

# English aliases for the (Portuguese) criteria ids; the Portuguese ids keep working.
ALIASES = {
    "nature": "natureza", "install": "instalacao", "installation": "instalacao", "routes": "rotas",
    "routing": "rotas", "host_port": "host_porta", "validation": "validacao",
    "sessions_cookies": "sessoes_cookies", "sessions": "sessoes_cookies", "files": "arquivos",
    "organization": "organizacao", "testing": "testes", "tests": "testes", "platform": "plataforma",
    "language": "linguagem", "performance": "desempenho", "source_version": "versao_fonte",
}

# (id, title, {fw: (text, [citations]) | None})
CRITERIA = [
    ("natureza", "Nature / positioning", {
        "express": ("Web framework built on top of Node.js, open source and easy to extend; the Node Handbook describes it as minimalist and not strongly opinionated.", ["EXPHB p.1-2", "NODEHB p.6"]),
        "fastify": ("Extremely extensible and minimal framework; the text says it is not 'batteries included' and relies on the ecosystem.", ["FSTF p.13"]),
        "nest": ("Framework that aims to be platform-agnostic; works with any Node HTTP framework when an adapter exists; Express and Fastify are supported out of the box.", ["NEST p.4"]),
    }),
    ("instalacao", "Installation / project creation", {
        "express": ("npm init -y, then npm install express.", ["EXPHB p.3"]),
        "fastify": ("npm i fastify (or yarn add fastify).", ["FSTF p.1"]),
        "nest": ("npm i -g @nestjs/cli and nest new project-name; optional --strict flag.", ["NEST p.2"]),
    }),
    ("hello", "Minimal server (Hello World)", {
        "express": ("require('express'), app.get('/'...), app.listen(3000): 4 lines.", ["EXPHB p.3-4"]),
        "fastify": ("Fastify({ logger: true }), fastify.get('/'...), fastify.listen({ port: 3000 }).", ["FSTF p.1-3"]),
        "nest": ("main.ts with NestFactory.create(AppModule) and listen(process.env.PORT ?? 3000).", ["NEST p.3"]),
    }),
    ("rotas", "Route declaration", {
        "express": ("One method per verb (get, post, put, delete, patch) with a (req, res) callback; named parameters in req.params; regex in routes.", ["EXPHB p.4-5", "EXPHB p.13-14"]),
        "fastify": ("fastify.get('/', handler); routes can live in a plugin registered with register; the options object accepts the schema key.", ["FSTF p.2", "FSTF p.4-5", "FSTF p.11"]),
        "nest": ("The CLI generates app.controller.ts, 'a basic controller with a single route'; the route/decorator declaration syntax does not appear in these pages (NOT COVERED for the detail).", ["NEST p.3"]),
    }),
    ("host_porta", "Listen port and host", {
        "express": ("Example listens on port 3000; the default host is not discussed (NOT COVERED for the host).", ["EXPHB p.4"]),
        "fastify": ("By default it listens only on localhost 127.0.0.1; use host 0.0.0.0 (or ::) for all interfaces, e.g. in a container.", ["FSTF p.3-4"]),
        "nest": ("Port comes from process.env.PORT or 3000; opens on localhost:3000; host not discussed (NOT COVERED for the host).", ["NEST p.3", "NEST p.5"]),
    }),
    ("middleware_plugins", "Extension: middleware / plugins", {
        "express": ("Middleware is a (req, res, next) function registered with app.use or as a route argument; call next() at the end unless it ends the response.", ["EXPHB p.17-18"]),
        "fastify": ("'Everything is a plugin'; register is the only way to add routes, plugins etc.; loaded in order; fastify-plugin exposes decorators/hooks to the parent scope.", ["FSTF p.4-5", "FSTF p.7", "FSTF p.9-10"]),
        "nest": SC,
    }),
    ("validacao", "Input validation", {
        "express": ("External package express-validator: check(), validationResult(), 422 response with the list of errors; also sanitization.", ["EXPHB p.24-25", "EXPHB p.30-31"]),
        "fastify": ("JSON Schema in the route's schema option (body, querystring, params, headers); a 'core concept' of the framework.", ["FSTF p.11"]),
        "nest": SC,
    }),
    ("json", "JSON: parsing and serialization", {
        "express": ("res.json converts an object/array to JSON; res.send of an object sets application/json; a parsing middleware is needed for the body (express.json appears in the examples).", ["EXPHB p.7", "EXPHB p.9", "EXPHB p.24"]),
        "fastify": ("Native parsing of application/json and text/plain into request.body; response schema speeds up serialization (2-3x, according to the text) and limits the data exposed.", ["FSTF p.12-13"]),
        "nest": SC,
    }),
    ("logging", "Logging", {
        "express": SC,
        "fastify": ("logger: true option; fastify.log.error / fastify.log.info in the examples.", ["FSTF p.1-3"]),
        "nest": SC,
    }),
    ("templates", "Templates (server-side HTML)", {
        "express": ("Supports engines (Pug, Handlebars, Mustache, EJS...); Jade is the default for compatibility, but the author recommends Pug; app.set('view engine', 'pug') + res.render.", ["EXPHB p.14-16"]),
        "fastify": SC,
        "nest": SC,
    }),
    ("sessoes_cookies", "Cookies and sessions", {
        "express": ("res.cookie with options; express-session (secret required; in-memory store for development only).", ["EXPHB p.9-10", "EXPHB p.20-23"]),
        "fastify": SC,
        "nest": SC,
    }),
    ("arquivos", "Static files, download and upload", {
        "express": ("express.static('public'); res.download; formidable for multipart/form-data.", ["EXPHB p.18-20", "EXPHB p.34-37"]),
        "fastify": SC,
        "nest": SC,
    }),
    ("organizacao", "Code organization", {
        "express": ("No project-structure guidance in the handbook beyond middleware and routes (NOT COVERED).", ["EXPHB p.17"]),
        "fastify": ("Encapsulated plugins in files; recommended order (ecosystem plugins, your plugins, decorators, hooks, services); repeat the structure per route subset.", ["FSTF p.4-5", "FSTF p.10"]),
        "nest": ("Root module app.module.ts; the CLI encourages each module in its own directory.", ["NEST p.3-4"]),
    }),
    ("testes", "Testing", {
        "express": SC,
        "fastify": ("Does not offer a testing framework; recommends a way of testing that uses the architecture (detail on another docs page); fastify.inject starts plugin loading.", ["FSTF p.10", "FSTF p.13"]),
        "nest": ("The generated project includes app.controller.spec.ts with unit tests for the controller.", ["NEST p.3"]),
    }),
    ("cli", "CLI / scaffolding", {
        "express": ("No CLI of its own in the text; only npm init -y.", ["EXPHB p.3"]),
        "fastify": ("fastify-cli (separate tool): script 'start': 'fastify start server.js'; server.js exports an async function (fastify, opts).", ["FSTF p.13-14"]),
        "nest": ("Nest CLI: nest new; npm run start, start:dev; SWC builder with -b swc.", ["NEST p.2", "NEST p.5"]),
    }),
    ("lint_format", "Lint and formatting", {
        "express": SC,
        "fastify": SC,
        "nest": ("Generated project already ships with eslint and prettier; npm run lint and npm run format.", ["NEST p.6"]),
    }),
    ("plataforma", "Underlying HTTP platform", {
        "express": ("Built on top of Node.js (the Node Handbook shows the http module as the base).", ["EXPHB p.1-2", "NODEHB p.133-135"]),
        "fastify": ("Its own framework (Fastify instance).", ["FSTF p.1"]),
        "nest": ("Uses @nestjs/platform-express by default; alternative @nestjs/platform-fastify; types NestExpressApplication / NestFastifyApplication.", ["NEST p.4-5"]),
    }),
    ("linguagem", "Language in the examples", {
        "express": ("CommonJS JavaScript (require); TypeScript does not appear (NOT COVERED).", ["EXPHB p.4"]),
        "fastify": ("Examples in ESM and CommonJS; ESM requires \"type\": \"module\" in package.json; TypeScript does not appear.", ["FSTF p.1-2"]),
        "nest": ("Compatible with TypeScript and plain JavaScript (the latter needs Babel); main examples in TypeScript; Node >= 20.", ["NEST p.2"]),
    }),
    ("desempenho", "Performance (claims in the text)", {
        "express": ("Claims to be 'very performant'; no numbers.", ["EXPHB p.2"]),
        "fastify": ("Says it optimizes JSON parsing/serialization; response schema speeds up serialization by 2-3x; no comparative benchmark.", ["FSTF p.12"]),
        "nest": ("Describes Fastify as high-performance and low-overhead; no numbers from Nest itself.", ["NEST p.5"]),
    }),
    ("versao_fonte", "Source version and date", {
        "express": ("Handbook dated 2022-11-18; Express version not declared. [DATED] relative to 2026.", ["EXPHB p.1"]),
        "fastify": ("Capture is marked 'latest (v5.12.x)'; capture date not declared.", ["FSTF p.1"]),
        "nest": ("Nest version not declared; requires Node >= 20; footer with Copyright 2017-2026.", ["NEST p.2", "NEST p.7"]),
    }),
]

DECIDE = ("The collection does NOT provide a selection criterion between Express, Fastify and Nest (no benchmarks, no decision guide). "
          "The columns above are descriptions of what each text states. Any recommendation is an [extrapolation] and must be "
          "labeled as such, together with the user's requirements.")


def build(criteria_ids, fws):
    rows = []
    for cid, title, cells in CRITERIA:
        if criteria_ids and cid not in criteria_ids:
            continue
        row = {"id": cid, "criterio": title, "celulas": {}}
        for fw in fws:
            c = cells[fw]
            if c is None:
                row["celulas"][fw] = {"texto": "NOT COVERED", "cita": []}
            else:
                row["celulas"][fw] = {"texto": c[0], "cita": c[1]}
        rows.append(row)
    return rows


def cell_str(c):
    if not c["cita"]:
        return c["texto"]
    return f"{c['texto']} [from source] ({'; '.join(c['cita'])})"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--criteria", default="")
    ap.add_argument("--frameworks", default="express,fastify,nest")
    ap.add_argument("--format", choices=["md", "json", "text"], default="text")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--decide", action="store_true")
    a = ap.parse_args(argv)
    if a.list:
        for cid, title, _ in CRITERIA:
            print(f"{cid}\t{title}")
        return 0
    if a.decide:
        print(DECIDE)
        return 0
    fws = [x.strip().lower() for x in a.frameworks.split(",") if x.strip()]
    bad = [x for x in fws if x not in FW]
    if bad:
        print(f"Framework outside the collection: {', '.join(bad)}. Available: {', '.join(FW)}. NOT COVERED for the others (Koa, Hapi, Meteor etc. only have a brief description in NODEHB p.5-6).")
        return 2
    ids = [ALIASES.get(x.strip(), x.strip()) for x in a.criteria.split(",") if x.strip()]
    known = {c[0] for c in CRITERIA}
    unk = [x for x in ids if x not in known]
    if unk:
        print(f"Criterion not covered by the comparer: {', '.join(unk)}. Use --list. (NOT COVERED: the collection does not offer this criterion.)")
        return 1
    rows = build(ids, fws)
    if a.format == "json":
        print(json.dumps({"frameworks": fws, "linhas": rows, "aviso": DECIDE}, ensure_ascii=False, indent=1))
        return 0
    if a.format == "md":
        print("| Criterion | " + " | ".join(FWNAME[f] for f in fws) + " |")
        print("|---|" + "---|" * len(fws))
        for r in rows:
            print(f"| {r['criterio']} | " + " | ".join(cell_str(r['celulas'][f]).replace("|", "/") for f in fws) + " |")
        print("\n" + DECIDE)
        return 0
    for r in rows:
        print(f"## {r['criterio']} ({r['id']})")
        for f in fws:
            print(f"- {FWNAME[f]}: {cell_str(r['celulas'][f])}")
    print("\n" + DECIDE)
    return 0


if __name__ == "__main__":
    sys.exit(main())

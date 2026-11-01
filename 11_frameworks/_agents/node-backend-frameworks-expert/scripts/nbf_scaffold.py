# -*- coding: utf-8 -*-
"""
nbf_scaffold.py - skeleton/command-plan generator using ONLY commands and code present in the sources.

Sources (page = PDF page): NODEHB (Node Handbook, 2018), EXPHB (Express Handbook, 2022),
FSTF (Fastify Getting Started, v5.12.x), NEST (NestJS First steps, Node >= 20).

The script NEVER runs npm/node/nest: it prints the plan (commands as TEXT) and, with --out DIR,
writes only small example files (it does not overwrite existing files). Each item cites the page.
Code snippets are minimal adaptations of the sources' examples (placeholders instead of secrets).

Usage:
  python -I scripts/nbf_scaffold.py TARGET [--name NAME] [--out DIR] [--esm] [--host-all]
                                    [--with json,urlencoded,static,cookies,session,validator,pug,upload]   (express only)
                                    [--variant basic|plugin|cli]   (fastify only)
                                    [--strict] [--swc]            (nest only)
  TARGET: node | express | fastify | nest
Not covered: Koa, Hapi, Meteor and others (names only in NODEHB p.5-6); TypeScript in Express/Fastify.
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

EXPRESS_WITH = ["json", "urlencoded", "static", "cookies", "session", "validator", "pug", "upload"]


def node_plan(a):
    files = {}
    cmds = []
    files["server.js"] = ("""const http = require('http')
const hostname = '127.0.0.1'
const port = 3000

const server = http.createServer((req, res) => {
  res.statusCode = 200
  res.setHeader('Content-Type', 'text/plain')
  res.end('Hello World\\n')
})

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`)
})
""", "NODEHB p.3-4")
    cmds.append(("node server.js", "NODEHB p.4"))
    pk = {"name": a.name, "version": "1.0.0", "private": True, "scripts": {"start": "node server.js"}}
    files["package.json"] = (json.dumps(pk, indent=2) + "\n", "NODEHB p.51-53, p.60 [inference: minimal composition]")
    cmds.append(("npm run start", "NODEHB p.60"))
    notes = ["[DATED] NODEHB is from 2018-09-06 (Node 10): check current versions before using.",
             "For a graceful exit use SIGTERM + server.close (NODEHB p.18-19); process.exit() is abrupt (p.17)."]
    return cmds, files, notes


def express_plan(a):
    w = [x for x in (a.with_.split(",") if a.with_ else []) if x]
    bad = [x for x in w if x not in EXPRESS_WITH]
    if bad:
        raise SystemExit(f"Unknown --with: {', '.join(bad)}. Valid: {', '.join(EXPRESS_WITH)}.")
    cmds = [("npm init -y", "EXPHB p.3"), ("npm install express", "EXPHB p.3")]
    head = ["const express = require('express')"]
    mw = []
    routes = []
    notes = ["Express: the handbook (2022-11-18) does not declare the Express version.",
             "Order: middleware before the routes that depend on it [inference from EXPHB p.17; the p.18 example registers cookie-parser after the route]."]
    extra = {}
    if "pug" in w:
        cmds.append(("npm install pug", "EXPHB p.15"))
        mw.append("app.set('view engine', 'pug')  // EXPHB p.15")
        routes.append("app.get('/about', (req, res) => {\n  res.render('about', { name: 'Flavio' })\n})  // EXPHB p.16")
        extra["views/about.pug"] = ("p Hello from #{name}\n", "EXPHB p.16")
    if "json" in w:
        mw.append("app.use(express.json())  // EXPHB p.24")
    if "urlencoded" in w:
        mw.append("app.use(express.urlencoded({ extended: true }))  // EXPHB p.34")
    if "static" in w:
        mw.append("app.use(express.static('public'))  // EXPHB p.19")
        extra["public/index.html"] = ("<!doctype html>\n<p>public/index.html (EXPHB p.19)</p>\n", "EXPHB p.19")
    if "cookies" in w:
        cmds.append(("npm install cookie-parser", "EXPHB p.17"))
        head.append("const cookieParser = require('cookie-parser')")
        mw.append("app.use(cookieParser())  // EXPHB p.17-18")
    if "session" in w:
        cmds.append(("npm install express-session", "EXPHB p.21"))
        head.append("const session = require('express-session')")
        mw.append("app.use(session({\n  secret: 'REPLACE-WITH-A-UNIQUE-RANDOM-STRING'  // secret: only required parameter (EXPHB p.22)\n}))  // in-memory store: development only (EXPHB p.23)")
    if "validator" in w:
        cmds.append(("npm install express-validator", "EXPHB p.25"))
        head.append("const { check, validationResult } = require('express-validator')")
        if "json" not in w:
            mw.append("app.use(express.json())  // EXPHB p.24")
        routes.append("""app.post('/form', [
  check('name').isLength({ min: 3 }),
  check('email').isEmail(),
  check('age').isNumeric()
], (req, res) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(422).json({ errors: errors.array() })
  }
  res.sendStatus(200)
})  // EXPHB p.25""")
    if "upload" in w:
        cmds.append(("npm install formidable", "EXPHB p.35"))
        head.append("const formidable = require('formidable')")
        routes.append("""app.post('/submit-form', (req, res) => {
  new formidable.IncomingForm().parse(req, (err, fields, files) => {
    if (err) {
      console.error('Error', err)
      throw err
    }
    console.log('Fields', fields)
    console.log('Files', files)
    res.end()
  })
})  // EXPHB p.36 (formidable API of the time; [DATED] check the current docs)""")
        extra["upload.html"] = ('<form method="POST" action="/submit-form" enctype="multipart/form-data">\n  <input type="file" name="document" />\n  <input type="submit" />\n</form>\n', "EXPHB p.34-35")
    src = "\n".join(head) + "\nconst app = express()\n"
    if mw:
        src += "\n" + "\n".join(mw) + "\n"
    src += "\napp.get('/', (req, res) => res.send('Hello World!'))\n"  # EXPHB p.4
    if routes:
        src += "\n" + "\n\n".join(routes) + "\n"
    src += "\napp.listen(3000, () => console.log('Server ready'))\n"
    files = {"index.js": (src, "EXPHB p.3-4 (+ snippets cited in the comments)")}
    files.update(extra)
    cmds.append(("node index.js", "EXPHB p.4"))
    return cmds, files, notes


def fastify_plan(a):
    variant = a.variant or "basic"
    host = ", host: '0.0.0.0'" if a.host_all else ""
    cmds = [("npm i fastify", "FSTF p.1")]
    notes = ["Source: Fastify 'latest (v5.12.x)' in the capture (no date).",
             "By default it listens only on 127.0.0.1; for a container use host 0.0.0.0 or :: (FSTF p.3-4)."]
    files = {}
    if variant == "basic":
        if a.esm:
            files["server.js"] = (f"""import Fastify from 'fastify'

const fastify = Fastify({{
  logger: true
}})

fastify.get('/', async (request, reply) => {{
  return {{ hello: 'world' }}
}})

const start = async () => {{
  try {{
    await fastify.listen({{ port: 3000{host} }})
  }} catch (err) {{
    fastify.log.error(err)
    process.exit(1)
  }}
}}
start()
""", "FSTF p.1-3")
            files["package.json"] = (json.dumps({"name": a.name, "type": "module", "dependencies": {}}, indent=2) + "\n", "FSTF p.2 ('type': 'module' for ESM)")
        else:
            files["server.js"] = (f"""const fastify = require('fastify')({{
  logger: true
}})

fastify.get('/', async (request, reply) => {{
  return {{ hello: 'world' }}
}})

const start = async () => {{
  try {{
    await fastify.listen({{ port: 3000{host} }})
  }} catch (err) {{
    fastify.log.error(err)
    process.exit(1)
  }}
}}
start()
""", "FSTF p.1-3")
        cmds.append(("node server.js", "inference: the text does not show this command for the basic server"))
    elif variant == "plugin":
        if a.esm:
            files["server.js"] = (f"""import Fastify from 'fastify'
import routes from './our-first-routes.js'

const fastify = Fastify({{
  logger: true
}})

fastify.register(routes)

fastify.listen({{ port: 3000{host} }}, function (err, address) {{
  if (err) {{
    fastify.log.error(err)
    process.exit(1)
  }}
  // Server is now listening on ${{address}}
}})
""", "FSTF p.4")
            files["our-first-routes.js"] = ("""async function routes (fastify, options) {
  fastify.get('/', async (request, reply) => {
    return { hello: 'world' }
  })
}

export default routes
""", "FSTF p.5")
            files["package.json"] = (json.dumps({"name": a.name, "type": "module", "dependencies": {}}, indent=2) + "\n", "FSTF p.2")
        else:
            files["server.js"] = (f"""const fastify = require('fastify')({{
  logger: true
}})

fastify.register(require('./our-first-routes'))

fastify.listen({{ port: 3000{host} }}, function (err, address) {{
  if (err) {{
    fastify.log.error(err)
    process.exit(1)
  }}
  // Server is now listening on ${{address}}
}})
""", "FSTF p.4-5")
            files["our-first-routes.js"] = ("""async function routes (fastify, options) {
  fastify.get('/', async (request, reply) => {
    return { hello: 'world' }
  })
}

module.exports = routes
""", "FSTF p.5")
        notes.append("register is the only way to add routes and plugins; plugins load in the declared order (FSTF p.5, p.9).")
        notes.append("Plugin loading starts at listen(), inject() or ready() (FSTF p.10).")
        cmds.append(("node server.js", "inference: the text does not show this command"))
    elif variant == "cli":
        cmds.append(("npm i fastify-cli", "FSTF p.13"))
        files["server.js"] = ("""'use strict'

module.exports = async function (fastify, opts) {
  fastify.get('/', async (request, reply) => {
    return { hello: 'world' }
  })
}
""", "FSTF p.14")
        pk = {"name": a.name, "scripts": {"start": "fastify start server.js"}}
        files["package.json"] = (json.dumps(pk, indent=2) + "\n", "FSTF p.14")
        cmds.append(("npm start", "FSTF p.14"))
        notes.append("fastify-cli is a separate tool (FSTF p.13).")
    else:
        raise SystemExit("--variant must be basic, plugin or cli.")
    return cmds, files, notes


def nest_plan(a):
    flag = " --strict" if a.strict else ""
    cmds = [("npm i -g @nestjs/cli", "NEST p.2"), (f"nest new {a.name}{flag}", "NEST p.2 (flag --strict: p.2)")]
    run = "npm run start"
    cmds.append((run, "NEST p.5"))
    cmds.append(("npm run start:dev", "NEST p.5"))
    if a.swc:
        cmds.append(("npm run start -- -b swc", "NEST p.5"))
    cmds.append(("npm run lint", "NEST p.6"))
    cmds.append(("npm run format", "NEST p.6"))
    files = {}
    notes = ["Prerequisite: Node.js >= 20 (NEST p.2; [DATED] relative to the capture, copyright 2017-2026).",
             "The CLI generates src/ with app.controller.ts, app.controller.spec.ts, app.module.ts, app.service.ts and main.ts (NEST p.3); the content is generated by the CLI, so no file is written here.",
             "main.ts (reference, NEST p.3): imports NestFactory and AppModule; async function bootstrap() creates the app with NestFactory.create(AppModule) and calls await app.listen(process.env.PORT ?? 3000).",
             "Platform: Express by default; Fastify is a supported alternative (NEST p.4-5). Decorators, DI, providers: NOT COVERED in these pages."]
    return cmds, files, notes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", choices=["node", "express", "fastify", "nest"])
    ap.add_argument("--name", default="my-project")
    ap.add_argument("--out")
    ap.add_argument("--esm", action="store_true")
    ap.add_argument("--host-all", action="store_true")
    ap.add_argument("--with", dest="with_", default="")
    ap.add_argument("--variant")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--swc", action="store_true")
    a = ap.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", a.name) or len(a.name) >= 214:
        print("Invalid name: use lowercase, no spaces, hyphens/underscores and fewer than 214 characters (NODEHB p.54).")
        return 2
    plan = {"node": node_plan, "express": express_plan, "fastify": fastify_plan, "nest": nest_plan}[a.target](a)
    cmds, files, notes = plan
    print(f"# Plan ({a.target}) - commands are text only; nothing is executed by this script")
    for c, cite in cmds:
        print(f"$ {c}    [{cite}]")
    for name, (content, cite) in files.items():
        print(f"\n--- file: {name}  [{cite}]")
        print(content.rstrip("\n"))
    print()
    for n in notes:
        print(f"* {n}")
    if a.out:
        base = os.path.abspath(a.out)
        os.makedirs(base, exist_ok=True)
        for name, (content, _c) in files.items():
            dest = os.path.abspath(os.path.join(base, name))
            if not dest.startswith(base + os.sep):
                print(f"Refused (outside the destination): {name}")
                return 2
            if os.path.exists(dest):
                print(f"Already exists, not overwritten: {dest}")
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            print(f"Written: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

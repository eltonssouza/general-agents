# INDEX — node-backend-frameworks-expert

Closed collection of **4 PDFs** on the Node.js backend ecosystem. Three of them are captures of web pages (docs) or blog handbooks; so the agent is an **overview based on captured documentation**, proportional to what the sources provide. Where the source does not cover something, the answer is **NOT COVERED** (or a labeled `[extrapolation]`).

## 1. Page convention

- **N = PDF page number** (marker `=== PAGE N ===` of the extracted text). The PDFs **have no printed numbering**; there is no offset to convert.
- Citation: `SIGLA p.N` or `SIGLA p.N-M`. Sigla: **NODEHB**, **EXPHB**, **FSTF**, **NEST**.
- When citing a passage that spans pages, use the range. The pages listed in the map below were checked against the text (`tests/verify_citations.py`).

## 2. What each PDF really is

| Sigla | File | What it is | Date / version that appears | PDF pages | Useful content |
|---|---|---|---|---|---|
| NODEHB | `Node-Handbook-freeCodeCamp.pdf` | "The definitive Node.js handbook", Flavio Copes, freeCodeCamp article | **September 6, 2018** (p.1); the text mentions Node 10 (p.10), npm 5/5.2 (p.65, p.82), "Node.js is 9 years old" (p.7) | 200 | p.2-199 (~161 thousand characters). p.1 and p.200 = cover/footer. **p.90-92, 95, 96 = event loop figures without text** (rendered; only stack/iteration diagrams) |
| EXPHB | `Express-Handbook-freeCodeCamp.pdf` | "The Express + Node.js Handbook", Flavio Copes | **November 18, 2022** (p.1); **Express version not declared** | 38 | p.1-38 in full. The `req` table (p.6) appears **cut off** in the capture (truncated columns) |
| FSTF | `Fastify-Getting-Started.pdf` | "Getting Started" page of the Fastify documentation (web capture) | "**Version: latest (v5.12.x)**" (p.1); no capture date | 14 | p.1-14 in full (ESM/CommonJS code snippets repeated by tabs) |
| NEST | `NestJS-First-Steps.pdf` | "First steps" page of the NestJS documentation (web capture) | Requires **Node >= 20** (p.2); footer "Copyright © 2017-2026" (p.7); **Nest version not declared** | 10 | p.2-6 useful; p.1 only icons ("dark_mode"); p.7 = sponsors/newsletter/footer; **p.8-10 empty** |

Useless pages: NEST p.1, p.7-10; NODEHB p.1, p.200 (and p.90-92, 95-96 without text); FSTF/EXPHB: none. There are no 404 pages.

## 3. Page map by topic (summary; detail in `scripts/nbf_index.json` and in the topic files)

**NODEHB** — runtime/CLI/environment p.2-40 (`01-node-runtime.md`); modules, npm, package.json, semver, lock, npx p.40-85 (`02-modulos-npm-semver.md`); event loop, timers, callbacks, promises, async/await, EventEmitter p.85-125 (`03-event-loop-e-assincronia.md`); HTTP, https.request, Axios, WebSockets, http module p.126-146 and p.178-185 (`04-http-websockets-rede.md`); fs, path, os, events, streams p.146-192 (`05-fs-path-os-events-streams.md`); MySQL and production p.193-199 (`06-mysql-e-producao.md`).

**EXPHB** — p.1-38 (`07-express.md`). **FSTF** — p.1-14 (`08-fastify.md`). **NEST** — p.2-6 (`09-nestjs.md`). Comparison: `10-comparativo-express-fastify-nest.md` (and `scripts/nbf_compare.py`).

## 4. Files in this folder

| File | Purpose |
|---|---|
| `01-node-runtime.md` | What Node is, V8, history, installation, REPL, arguments, console, exit, environment variables, hosting |
| `02-modulos-npm-semver.md` | exports, npm, package.json, semver, lockfile, npx |
| `03-event-loop-e-assincronia.md` | event loop, timers, callbacks, promises, async/await, EventEmitter |
| `04-http-websockets-rede.md` | HTTP, server, client, Axios, WebSockets, http module |
| `05-fs-path-os-events-streams.md` | fs, path, os, events, streams |
| `06-mysql-e-producao.md` | MySQL and NODE_ENV |
| `07-express.md` | Express (EXPHB) |
| `08-fastify.md` | Fastify (FSTF) |
| `09-nestjs.md` | NestJS (NEST) |
| `10-comparativo-express-fastify-nest.md` | comparison using only criteria given by the sources |
| `glossario.md`, `procedimentos.md`, `casos-e-antipadroes.md`, `datado.md` | terms, recipes, cases and errors in the texts themselves, dated items and version register |

## 5. Reading coverage

All four PDFs were read **in full** (extracted text, page by page); the event loop figure pages were rendered and checked (only iteration diagrams: `foo()`, `console.log('foo')`, `bar()`, `baz()`). The Nest `main.ts` code (NEST p.3) was checked visually because text extraction scrambles the braces. The Express `req` table (EXPHB p.6) was checked visually and **is truncated in the PDF itself**.

## 6. Known gaps (NOT COVERED)

`python -I scripts/nbf_lookup.py --gaps` lists them. In short: Nest without decorators/DI/providers/pipes/guards; Express without error middleware, Router, helmet/CORS, JWT; Fastify without detailed hooks/lifecycle/pino/TypeScript; Node (2018) without worker threads, cluster, child_process, crypto, Buffer, ESM as default, test runner, debugging; no ORMs beyond MySQL; no REST/API architecture (→ web-api-rest-architecture-expert); no React/Next/Vue (other agents).

## 7. Boundary with other agents

- REST API design, contracts, versioning: `web-api-rest-architecture-expert` (`06_web_and_frontend\_agents\`).
- React / Next.js / Vue / Nuxt: dedicated agents in the frontend and frameworks folders.

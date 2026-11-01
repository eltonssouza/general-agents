# 08 — Fastify (FSTF)

Source: **FSTF** — "Getting Started" page of the Fastify documentation (web capture, 14 pages), marked "**Version: latest (v5.12.x)**" (p.1); undated. The examples appear in ESM and CommonJS. Pages = PDF. Anything about other versions (v3, v4...) is NOT COVERED.

## Installing and first server (FSTF p.1-3)
- **[from source]** `npm i fastify` or `yarn add fastify` (p.1). `Fastify({ logger: true })` enables logging; route `fastify.get('/', function (request, reply) { reply.send({ hello: 'world' }) })`; `fastify.listen({ port: 3000 }, function (err, address) {...})` with `fastify.log.error(err)` and `process.exit(1)` on error (p.1-2).
- **[from source]** With ESM, `package.json` needs `"type": "module"` (p.2). `async/await` is supported out of the box: `fastify.get('/', async (request, reply) => { return { hello: 'world' } })` and `await fastify.listen({ port: 3000 })` in `try/catch` (p.2-3).
- **[from source]** Writing a complex application requires dealing with several files, asynchronous bootstrap and architecture; Fastify offers a platform for that (p.3).

## Listening host (FSTF p.3-4)
**[from source]** The examples listen **only on localhost (127.0.0.1)**. For all IPv4 interfaces: `host: '0.0.0.0'`; `::1` accepts only local IPv6 connections; `::` accepts all IPv6 addresses and, if the OS supports it, IPv4 too (p.3). In Docker or another container, `0.0.0.0` or `::` is the simplest way; with `0.0.0.0` the callback address is the first one the wildcard represents (p.3-4).

## Plugins and `register` (FSTF p.4-5)
- **[from source]** "Everything is a plugin" in Fastify (analogy: in JS everything is an object) (p.4). The example declares routes in a separate file (`our-first-routes`): an `async function routes (fastify, options)` function exported and loaded with `fastify.register(routes)` (p.4-5).
- **[from source]** `register` is the heart of the framework and **the only way to add routes, plugins etc.** (p.5).

## Asynchronous bootstrap and load order (FSTF p.5-10)
- **[from source]** Problem: the database connection must be ready before accepting connections; Fastify handles this internally (p.5-6). Example: `npm i fastify-plugin @fastify/mongodb`; a `dbConnector` plugin that registers `@fastify/mongodb` with `url: 'mongodb://localhost:27017/test_database'`; **`fastifyPlugin(dbConnector)` exposes the decorators and hooks declared in the plugin to the parent scope** (p.6-8).
- **[from source]** Example routes: `GET /`, `GET /animals`, `GET /animals/:animal` (uses `request.params.animal`), `POST /animals` with `schema: { body: animalBodyJsonSchema }`; errors via `throw new Error(...)` (p.8-9).
- **[from source]** `register` loads the plugins **in the declared order** and only moves to the next one when the current one has finished; thus the connector registered first is used by the second (p.9). Loading starts at `fastify.listen()`, `fastify.inject()` or `fastify.ready()` (p.10).
- **[from source]** The MongoDB plugin uses the `decorate` API to add objects to the instance, available everywhere; the text **encourages** this use to reuse code (p.10).
- **[from source]** Recommended load order: ecosystem plugins → your plugins → decorators → hooks → your services; to register a plugin for only a subset of routes, repeat the structure (e.g. `service A`, `service B`, each with the same stack) (p.10). The **encapsulation** model helps build the application as independent services (p.10).
- Details on hooks, request lifecycle, deep scope/encapsulation and the "hitchhiker's guide to plugins": the text only **points** to other pages (NOT COVERED here).

## Validation and serialization (FSTF p.11-12)
- **[from source]** Data validation is "extremely important" and a core concept; it uses **JSON Schema**: the route's `schema` option accepts the keys `body`, `querystring`, `params`, `headers` (p.11).
- **[from source]** Serialization: Fastify has first-class JSON support, optimized for parsing and serialization; the `response` key of the `schema` (e.g. `response: { 200: { type: 'object', properties: { hello: { type: 'string' } } } }`) speeds up serialization "by a factor of 2-3" and **protects against leaking sensitive data**, since it only serializes what is in the response schema (p.12). There is no benchmark of its own in the text; the factor is a claim of the docs.

## Payload parsing (FSTF p.12-13)
**[from source]** Native parsing of `application/json` and `text/plain`; result in `request.body` (example that returns the body) (p.12-13). Other content types: "Content-Type Parser" (another page; NOT COVERED here) (p.13).

## Extension, tests and CLI (FSTF p.13-14)
- **[from source]** Fastify is "extremely extensible and minimal"; it is **not "batteries included"** and depends on the ecosystem (p.13).
- **[from source]** It does not offer a testing framework; it recommends a way of writing tests that uses Fastify's features and architecture (testing documentation on another page) (p.13).
- **[from source]** `fastify-cli` (separate tool to create and manage projects): `npm i fastify-cli` (also `-g`); script `"start": "fastify start server.js"`; `server.js` exports `module.exports = async function (fastify, opts) { fastify.get('/', ...) }`; run with `npm start` (p.13-14). p.14 also lists slides/videos (Collina, Delvedor) — no technical content.
- Logging beyond `logger: true`, TypeScript, lifecycle, official security/CORS plugins: **NOT COVERED**.

Related: `10-comparativo-express-fastify-nest.md`, `casos-e-antipadroes.md`. Linter: FST-LISTEN-HOST, FST-PLUGIN-ENCAP, FST-NO-SCHEMA.

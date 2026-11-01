# 10 — Express vs Fastify vs NestJS comparison (only criteria the sources provide)

Generated from `python -I scripts/nbf_compare.py --format md` (identical content; run the script for the always-synchronized version). Sources: EXPHB (Express Handbook, 18/11/2022, Express version not declared), FSTF (Fastify "latest (v5.12.x)"), NEST (First steps, Node >= 20, © 2017-2026). Pages = PDF.

**Warning:** the sources **contain no decision guide** and no comparative benchmarks. The rows below describe what each text states; choosing a framework is an **[extrapolation]** and needs the user's requirements.

| Criterion | Express | Fastify | NestJS |
|---|---|---|---|
| Nature | Web framework on top of Node, extensible; "minimalist" according to NODEHB (EXPHB p.1-2; NODEHB p.6) | Extensible and minimal; not "batteries included" (FSTF p.13) | Platform-agnostic; Express and Fastify out of the box (NEST p.4) |
| Installation | `npm init -y` + `npm install express` (EXPHB p.3) | `npm i fastify` (FSTF p.1) | `npm i -g @nestjs/cli`, `nest new` (NEST p.2) |
| Hello World | 4 lines, `app.listen(3000)` (EXPHB p.3-4) | `Fastify({logger:true})`, `get`, `listen` (FSTF p.1-3) | `main.ts` with `NestFactory.create` (NEST p.3) |
| Routes | `app.get/post/put/delete/patch`, `req.params`, regex (EXPHB p.4-5, p.13-14) | `fastify.get`, plugins with `register`, `schema` (FSTF p.2, p.4-5, p.11) | Generated controller with one route; syntax NOT COVERED (NEST p.3) |
| Default host | Not discussed | Only 127.0.0.1; `0.0.0.0`/`::` for containers (FSTF p.3-4) | Not discussed; port `PORT ?? 3000` (NEST p.3) |
| Extension | Middleware `(req, res, next)` (EXPHB p.17-18) | "Everything is a plugin"; `register` (FSTF p.4-5) | NOT COVERED |
| Validation | external express-validator (EXPHB p.24-25) | native JSON Schema on the route (FSTF p.11) | NOT COVERED |
| JSON | `res.json`; `express.json()` in the examples (EXPHB p.7, p.9, p.24) | Native parsing; response schema speeds up 2-3x (FSTF p.12-13) | NOT COVERED |
| Logging | NOT COVERED | `logger: true`, `fastify.log` (FSTF p.1-3) | NOT COVERED |
| Templates | Jade default; Pug recommended (EXPHB p.14-16) | NOT COVERED | NOT COVERED |
| Sessions/cookies | `res.cookie`, express-session (EXPHB p.9-10, p.20-23) | NOT COVERED | NOT COVERED |
| Static files/upload | `express.static`, `res.download`, formidable (EXPHB p.18-20, p.34-37) | NOT COVERED | NOT COVERED |
| Organization | No guidance | Encapsulated plugins and recommended order (FSTF p.4-5, p.10) | Modules; one per directory (NEST p.3-4) |
| Testing | NOT COVERED | No framework of its own; `inject` (FSTF p.10, p.13) | `app.controller.spec.ts` (NEST p.3) |
| CLI | Only `npm init -y` | fastify-cli (FSTF p.13-14) | Nest CLI (NEST p.2, p.5) |
| Lint/format | NOT COVERED | NOT COVERED | eslint + prettier (NEST p.6) |
| HTTP platform | On top of Node (EXPHB p.1-2) | Own instance (FSTF p.1) | Express default or Fastify (NEST p.4-5) |
| Language | JS CommonJS; TS NOT COVERED (EXPHB p.4) | ESM and CommonJS (FSTF p.1-2) | TS and JS (Babel) (NEST p.2) |
| Performance | "very performant", no numbers (EXPHB p.2) | JSON optimizations; 2-3x with schema (FSTF p.12) | describes Fastify as fast (NEST p.5) |

## How to use this comparison
1. Answer only with the rows the sources give; say NOT COVERED for the others.
2. Do not turn "Fastify says it serializes 2-3x faster" into "Fastify is X times faster than Express": the text does not compare (FSTF p.12).
3. Do not claim that Nest "is built on" Express or Fastify in a mandatory way: the text says Express is the default and Fastify is supported (NEST p.4-5).
4. Recommendation request: return the facts above, state that the choice is an **[extrapolation]**, and if you wish give general criteria labeled as such.

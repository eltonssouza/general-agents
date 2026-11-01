# Cases and antipatterns

Origin of each item indicated. Pages = PDF. The linter (`scripts/nbf_lint.py`) covers several of them, with the ID in parentheses.

## A. Errors present in the texts themselves (be careful when copying examples)
1. **`npm watch`/`npm dev`/`npm prod` without `run`** — NODEHB p.46; the correct form, per the text itself, is `npm run <task>` (p.45).
2. **"Synchronous" `fs.stat` without a callback** — NODEHB p.148; the text itself says the synchronous variant has the `Sync` suffix (p.161-162). (NODE-FS-NOCB)
3. **`path.extname` exemplified with `dirname`** — NODEHB p.164.
4. **`results.resultId`** — NODEHB p.197; p.196 says `results.insertId`. (NODE-MYSQL-RESULTID)
5. **`fs.mkdirSync(dir)` with variable `folderName`** — NODEHB p.156 (inconsistent name).
6. **List of semver operators with duplicated `<`** (where `>` would be) — NODEHB p.77.
7. **`packages.json`** (typo for `package.json`) — NODEHB p.43.
8. **`npm install --dev`** — NODEHB p.62 (the text uses `--save-dev`/`-D` on p.44, p.82).
9. **`req.locals`** (the field belongs to `res`, **[extrapolation]**) — EXPHB p.18. (EXP-REQ-LOCALS)
10. **cookie-parser registered after the route** — EXPHB p.18 (the text does not discuss the effect of order). (EXP-MW-ORDER)
11. **Literal session secret in the example** — EXPHB p.21; use your own secret value **[extrapolation]**.
12. **Truncated `req` table** — EXPHB p.6 (capture limitation).

## B. Antipatterns that the text condemns or discourages
| Antipattern | Why (source) | Rule |
|---|---|---|
| `process.exit()` to shut down a server | aborts pending requests (NODEHB p.17-18) | NODE-EXIT |
| Server without handling SIGTERM | graceful shutdown requires a handler (NODEHB p.18-19) | NODE-SIGTERM |
| Blocking the event loop (sync, long loops) | single thread (NODEHB p.86-87) | NODE-SYNC-HANDLER |
| `readFile` of large files to respond | reads everything into memory; use streams (NODEHB p.153, p.186-187) | NODE-READFILE-RESPONSE |
| Callback that ignores `err` | error-first convention (NODEHB p.109) | NODE-ERR-FIRST |
| `Promise()` without `new` | "undefined is not a promise" error (NODEHB p.118) | NODE-PROMISE-NEW |
| `setInterval` with asynchronous work | overlap; use recursive setTimeout (NODEHB p.104) | NODE-SETINTERVAL-ASYNC |
| `ws://` | use `wss://` (NODEHB p.143) | NODE-WS-INSECURE |
| `npx` from an unknown URL | runs code you do not control (NODEHB p.85) | NODE-NPX-URL |
| Global package by default | breaks versions across projects (NODEHB p.80) | — |
| Committing `node_modules` / forgetting the lockfile | reproducibility (NODEHB p.65-66) | NODE-GITIGNORE-MODULES |
| `.env` in the repository | must go in `.gitignore` (NODEHB p.21) | NODE-GITIGNORE-ENV |
| express-session in memory in production | development only (EXPHB p.23) | EXP-SESSION-MEMORY |
| express-session without `secret` | only required parameter (EXPHB p.22) | EXP-SESSION-SECRET |
| cookie-session | data on the client, 4 KB (EXPHB p.23) | EXP-COOKIE-SESSION |
| Middleware without `next()` or a response | hangs the request (EXPHB p.17) | EXP-MW-NEXT |
| Trusting client-side validation | "never trust input" (EXPHB p.29-30) | EXP-VALIDATION |
| Upload form without `enctype` | files are not uploaded (EXPHB p.35) | EXP-FORM-ENCTYPE |
| Jade in a new project | use Pug (EXPHB p.15) | EXP-JADE |
| Fastify on localhost only inside a container | use `0.0.0.0`/`::` (FSTF p.3-4) | FST-LISTEN-HOST |
| Fastify plugin that decorates without `fastify-plugin` and expects access in the parent | decorators stay in the encapsulated scope (FSTF p.7) | FST-PLUGIN-ENCAP |

## C. Practical cases solved with the sources
1. **"My Express server hangs forever on a route"** → check for middleware that neither calls `next()` nor responds (EXPHB p.17); run `nbf_lint.py`.
2. **"`req.body` comes back `undefined`"** → `express.json()` / `express.urlencoded()` or a multipart parser is missing (EXPHB p.6, p.24, p.34-35); order before the routes **[inference]**.
3. **"Fastify does not respond outside the container/Docker"** → the default host is 127.0.0.1; use `0.0.0.0` (FSTF p.3-4).
4. **"My Fastify plugin's decorator does not show up in the routes"** → wrap it with `fastify-plugin` (FSTF p.7) and respect the load order (FSTF p.9-10).
5. **"`ncu -u` changed my package.json"** → expected: it updates the version hints to the majors; then `npm update` (NODEHB p.75).
6. **"`npm update` does not bump the major"** → by definition (breaking), use npm-check-updates (NODEHB p.75).
7. **"I want to expose functionality from a module"** → `module.exports`/`exports` (NODEHB p.40-43).
8. **"Which framework should I choose?"** → the sources do not decide; use `nbf_compare.py` and label the recommendation as **[extrapolation]**.
9. **"How do I do dependency injection in Nest?"** → NOT COVERED (NEST p.2-6 does not address it).
10. **"How do I create a Router in Express?"** → NOT COVERED in the handbook.

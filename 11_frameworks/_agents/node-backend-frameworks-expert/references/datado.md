# [DATED] items and version/date register

The collection mixes sources from very different eras. **[DATED] is relative to the date of each PDF**; nothing here states the current state of Node, npm, Express, Fastify or Nest.

## Register of versions and dates that appear in the texts
| Source | Date / version | Where |
|---|---|---|
| NODEHB | article from **6/9/2018**; Node 10 (p.10); npm 5 and `package-lock` (p.65); npx since npm 5.2, Jul/2017 (p.82); "Node is 9 years old" (p.7); "58000+ stars" (p.2); "almost 500,000 packages" (p.3); `lockfileVersion: 1` (p.66); webpack 3, Vue 2.5 in the package.json example (p.51-52); readline "since v7" (p.38); `events.off` in Node 10 (p.176); fs promises "experimental" in Node 10 (p.162) | as indicated |
| EXPHB | article from **18/11/2022**; **Express version not declared**; Jade default (p.15); formidable with "more than 4000 stars" (p.35) | as indicated |
| FSTF | "Version: latest (v5.12.x)" (p.1); date not declared | p.1 |
| NEST | Node >= 20 (p.2); "Copyright © 2017-2026" (p.7); Nest version not declared | p.2, p.7 |

## What is [DATED] by source
- **NODEHB (2018):** hosting list (Glitch, Zeit Now, Nanobox, Heroku, etc.) (p.21-25); framework list and the history up to Node 10 (p.5-10); `require` vs `import` and experimental ESM (p.10, p.14); Axios and its "advantages over Fetch" (p.137-138); packages `mysql`, `ws`, `minimist`, `chalk`, `progress`, `inquirer`, `fs-extra`, `npm-check-updates` and their versions (p.32-40, p.158-159, p.193-197); `app.configure` and `express.errorHandler` (p.199); number of packages/stars; `npm install --save` as the default before npm 5 (p.82).
- **EXPHB (2022):** Jade/Pug (p.15); formidable (API `file.path`/`file.name`, p.37); validator.js/method names (p.25-32); `req.locals` (p.18) may be inaccurate (see `casos-e-antipadroes.md` A9).
- **FSTF (v5.12.x):** everything applies to the version marked on the capture; plugins `@fastify/mongodb`, `fastify-plugin`, `fastify-cli` appear as in the capture.
- **NEST (2026):** the Node >= 20 requirement and the SWC "20x faster" claim are from the capture; no capture date.

## Change map by version
The collection has **a single version per framework**, so there is no change map between versions of the same framework. What exists: NODEHB shows Node 10/npm 5 (2018) and NEST requires Node >= 20 (2026) — the text **does not say** what changed between them. Any list of changes between versions is an **[extrapolation]**.

## Answering rules
- When citing a version fact, state the version of the text ("Fastify v5.12.x, FSTF p.1").
- If the user says something changed, agree and mark [DATED]; do not contest it from memory about versions.
- Do not apply what NODEHB says about npm/Node 10 to current versions without warning.

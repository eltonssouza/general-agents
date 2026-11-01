# 07 — Express (EXPHB)

Source: **EXPHB** — "The Express + Node.js Handbook", Flavio Copes, freeCodeCamp, **18/11/2022** (p.1). **The Express version is not declared.** Everything below applies to what the text shows; the rest is NOT COVERED. Pages = PDF. [DATED] relative to the PDF date; versions/packages (formidable, Pug/Jade) may have changed.

## Overview and first server (EXPHB p.1-5)
- **[from source]** Express is a web framework built on top of Node.js, open source, free, easy to extend and "very performant", with many ready-made packages (p.1-2).
- **[from source]** Install: `npm init -y` and `npm install express` (p.3). Hello World: `require('express')`, `const app = express()`, `app.get('/', (req, res) => res.send('Hello World!'))`, `app.listen(3000, ...)`; run with `node index.js` (p.3-4).
- **[from source]** There is one method per HTTP verb: `get`, `post`, `put`, `delete`, `patch` (p.4-5). The callback receives `req` (Request) and `res` (Response); `send()` sets the body and **closes the connection** (p.5).

## req properties (EXPHB p.6)
**[from source]** Main ones: `.app`, `.baseUrl`, `.body` (body data; the text indicates it needs to be "parsed"), `.cookies` (needs cookie-parser), `.hostname`, `.ip`, `.method`, `.params`, `.path`, `.protocol`, `.query`, `.secure`, `.signedCookies`, `.xhr`. The table is **cut off** in the PDF (truncated descriptions); `req.body` and `req.cookies` depend on middleware (see p.17, p.24, p.34).

## Responses (EXPHB p.7-9)
- **[from source]** `res.send`: string → `Content-Type: text/html`; object/array → `application/json` converted to JSON; sets `Content-Length` automatically, unlike `res.end()` (p.7). `res.end()` sends a response with no body (p.7).
- **[from source]** Status: `res.status(404).end()` or `.send('File not found')`; shortcut `res.sendStatus(200|403|404|500)` (equivalent to `status(n).send('text')`) (p.7-8). `res.json({...})` converts an object/array to JSON (p.9).

## Cookies, headers, redirects (EXPHB p.9-13)
- **[from source]** `res.cookie(name, value, options)`: `domain`, `expires` (absent/0 = session cookie), `httpOnly`, `maxAge` (ms), `path` (default `/`), `secure` (HTTPS), `signed`, `sameSite`; `res.clearCookie('username')` (p.9-10).
- **[from source]** `req.headers`, `req.header('User-Agent')`; `res.set('Content-Type', 'text/html')`; shortcut `res.type('html'|'json'|'png'|...)` (p.10-12).
- **[from source]** `res.redirect('/go-there')` = **302**; `res.redirect(301, '/go-there')`; accepts absolute path, URL, relative, `..`; `res.redirect('back')` goes back to the Referer (default `/`) (p.12-13).

## Routes (EXPHB p.13-14)
**[from source]** Routing = deciding what happens at each URL (p.13). Named parameters: `app.get('/uppercase/:theValue', ...)` and `req.params.theValue`; several parameters all end up in `req.params` (p.13-14). Regex: `app.get(/post/, ...)` matches `/post`, `/post/first`, `/thepost`, `/posting/something` (p.14). `express.Router` and route grouping: **NOT COVERED**.

## Templates (EXPHB p.14-16)
**[from source]** Engines generate dynamic HTML. Express uses **Jade** by default (Jade = Pug 1.0; renamed for trademark reasons in 2016), kept for compatibility; in new projects use **Pug** (or another: Handlebars, Mustache, EJS...) (p.15). Steps: `npm install pug`; `app.set('view engine', 'pug')`; `res.render('about')` with `views/about.pug`; variables: `res.render('about', { name: 'Flavio' })` and `p Hello from #{name}` (p.15-16).

## Middleware (EXPHB p.17-18)
- **[from source]** Middleware is a function that enters the routing process to edit `req`/`res` or to **end the request before the handler** (p.17). Registration: `app.use((req, res, next) => { ... })`; **always call `next()` at the end**, unless you want to end the response (p.17). Example with `cookie-parser` (populates `req.cookies`) (p.17-18).
- **[from source]** Per-route middleware: as the second parameter of the route definition: `app.get('/', myMiddleware, handler)` (p.18).
- **[from source]** To pass data to the following middlewares/handlers the text cites `Request.locals` (`req.locals.name = 'Flavio'`) (p.18). **[extrapolation]** the Express documentation uses `res.locals` for this; confirm in the version you use (the linter flags EXP-REQ-LOCALS).
- **[inference]** Since the middleware enters "the execution stack" (p.17), **registration order matters**. The handbook's own example (p.18) registers `cookie-parser` *after* the `/` route; the text does not discuss the effect.
- **Error** middleware (4 arguments), `Router`, helmet, CORS, HTTP logs: **NOT COVERED**.

## Static files and download (EXPHB p.18-20)
`app.use(express.static('public'))` serves `public/` at the root; if there is an `index.html`, it is served at `/` (p.18-19). `res.download('./file.pdf')` sends it as an attachment; accepts a displayed file name and a callback with `err` (p.19-20).

## Sessions (EXPHB p.20-24)
- **[from source]** By default requests are not linked to each other; **sessions** identify the user (p.20-21). `npm install express-session`; `app.use(session({ secret: '...' }))`; `secret` is the **only required parameter** and must be a random, unique string (p.21-22). Data in `req.session` (serialized as JSON) (p.22).
- **[from source]** Where the data lives: memory ("not for production"), database (MySQL/Mongo) or cache (Redis/Memcached); the session id goes in a cookie and the data stays on the server; memory is the default and is only for development; the author points to **Redis** as the best choice (p.22-23).
- **[from source]** `cookie-session` stores data **on the client**; the author **does not recommend** it (data travels on every request, 4 KB limit) (p.23). Secure cookies require HTTPS and configuration with proxies (p.23-24).
- Note: the example uses a string literal as the secret (p.21); use your own secret value (**[extrapolation]**: do not commit secrets to version control).

## Validation and sanitization (EXPHB p.24-33)
- **[from source]** A JSON body requires `app.use(express.json())` in the examples (p.24, p.30). Best way to validate input: **express-validator** (`check`, `validationResult`): array of `check()` as the second argument of the route; if `!errors.isEmpty()`, respond **422** with `errors.array()` (p.24-25). Validators come from validator.js: `isLength`, `isEmail`, `isNumeric`, `isAlpha`, `isIn`, `isInt`, `isURL`, `isISO8601`, `matches` etc. (p.25-27). Chaining (`check('name').isAlpha().isLength({ min: 10 })`) (p.27). Default message: `Invalid value`; customized with `withMessage()` (p.28). `custom()` rejects by exception or rejected promise (p.28-29).
- **[from source]** "Never trust input": client-side validation is not enough (p.29-30). Sanitization in the same chain: `trim()`, `escape()` (replaces `< > & ' " /` with entities), `normalizeEmail()`, `ltrim`, `rtrim`, `stripLow`, `blacklist`, `whitelist`, `unescape`, conversions `toBoolean/toDate/toFloat/toInt`, `customSanitizer` (p.30-33). Note: the text uses `isWhitelisted()`, `blacklist()`, `whitelist()` as the author wrote them; exact names may have changed **[DATED]**.

## Forms and upload (EXPHB p.33-38)
- **[from source]** A `POST` form sends `application/x-www-form-urlencoded`; extract with `app.use(express.urlencoded({ extended: true }))` and read `req.body` (p.33-34). Validate before using (p.34).
- **[from source]** Upload: `<form enctype="multipart/form-data">`; without it, files are not sent (p.34-35). Multipart is "difficult and error-prone"; the author uses **formidable**: `new formidable.IncomingForm().parse(req, (err, fields, files) => ...)` or via events (`field`, `file`, `aborted`, `error`, `end`, `fileBegin`); `file.size`, `file.path`, `file.name`, `file.type`; change `file.path` in `fileBegin` (p.35-37). **[DATED]** the formidable API (`path`/`name` properties) is the one from the time of the text; check the current version.

Related: `casos-e-antipadroes.md`, `10-comparativo-express-fastify-nest.md`. Linter: EXP-* rules.

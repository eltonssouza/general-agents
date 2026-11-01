# Glossary (terms as the sources use them)

Pages = PDF. Definitions paraphrased; "per" indicates where the text discusses the term.

| Term | Meaning according to the source | Where |
|---|---|---|
| Runtime | Environment that runs JavaScript outside the browser (Node.js on V8) | NODEHB p.2 |
| V8 | Chrome's JS engine, used by Node; compiles with JIT | NODEHB p.2, p.14-16 |
| Event loop | Loop that checks the call stack and then the message queue, on a single thread | NODEHB p.85-98 |
| Call stack | LIFO stack of function calls | NODEHB p.87 |
| Message queue | Queue where callbacks from timers, events and responses land | NODEHB p.97 |
| Job queue | (ES6) queue of promises, executed right after the current function | NODEHB p.97-98 |
| Tick | One full turn of the event loop; `nextTick` runs before the next one | NODEHB p.99 |
| Error-first callback | Callback whose 1st parameter is the error (`null` if none) | NODEHB p.109 |
| Promise | Proxy for a future value: pending → resolved/rejected | NODEHB p.111 |
| async/await | Syntax over promises; an async function returns a promise | NODEHB p.118-121 |
| EventEmitter | `events` class with `on`/`emit`; default limit of 10 listeners | NODEHB p.124, p.175 |
| Stream | Data flow processed in chunks (Readable, Writable, Duplex, Transform) | NODEHB p.185-189 |
| `pipe()` | Connects source to destination; returns the destination | NODEHB p.188 |
| CommonJS | Node's module system (`require`/`module.exports`) in 2018 | NODEHB p.14, p.40 |
| `module.exports` vs `exports` | The first exposes the object; the second, its properties | NODEHB p.43 |
| npm / registry | Package manager and repository | NODEHB p.43 |
| `package.json` | Project manifest (name, version, scripts, dependencies) | NODEHB p.49-63 |
| `package-lock.json` | Record of the exact installed versions (npm 5); must be committed | NODEHB p.64-66 |
| Semver | major.minor.patch; `^` patch+minor, `~` patch only | NODEHB p.63-64, p.76-78 |
| `devDependencies` | Development-only packages; `--production` avoids installing them | NODEHB p.81-82 |
| npx | Runs package commands without installing/without a path | NODEHB p.82-85 |
| `NODE_ENV` | Variable that signals production; libraries change caching/logs | NODEHB p.20, p.197-198 |
| SIGTERM | Signal to shut down gracefully | NODEHB p.18-19 |
| Express | Web framework on top of Node | EXPHB p.1-2 |
| Middleware (Express) | `(req, res, next)` function that acts in routing | EXPHB p.17 |
| `req` / `res` | Request and response objects | EXPHB p.5 |
| Session | Association of requests with a user; id in a cookie, data on the server | EXPHB p.20-23 |
| express-validator | Validation/sanitization package (validator.js) | EXPHB p.24-33 |
| Pug / Jade | Template engine; Jade = Pug 1.0, Express default for compatibility | EXPHB p.15 |
| Fastify | Minimal, extensible framework; "everything is a plugin" | FSTF p.4, p.13 |
| `register` | The only way to add routes and plugins in Fastify | FSTF p.5 |
| `fastify-plugin` | Wraps a plugin to expose decorators/hooks to the parent scope | FSTF p.7 |
| `decorate` | API to add objects to the Fastify instance | FSTF p.10 |
| JSON Schema (Fastify) | Validation schema (body, querystring, params, headers) and serialization (response) | FSTF p.11-12 |
| fastify-cli | Separate tool to create/manage Fastify projects | FSTF p.13-14 |
| NestJS | Platform-agnostic framework; TS and JS | NEST p.2, p.4 |
| Nest CLI | `nest new`; generates `src/` with controller, module, service, main | NEST p.2-3 |
| `NestFactory` | Core class that creates the application (`create`) | NEST p.3-4 |
| Root module | `app.module.ts` | NEST p.3 |
| Platform (Nest) | `@nestjs/platform-express` (default) or `@nestjs/platform-fastify` | NEST p.4-5 |
| SWC | Alternative Nest builder (`-b swc`) | NEST p.5 |

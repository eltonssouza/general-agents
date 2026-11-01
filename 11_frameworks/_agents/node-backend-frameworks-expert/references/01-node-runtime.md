# 01 — Node.js runtime: overview, history, installation, CLI, environment

Source: NODEHB (Node.js Handbook, Flavio Copes, **6/9/2018**, Node 10). **[DATED]** everything that depends on version, service or price. Pages = PDF.

## What it is
- **[from source]** Node.js is an open-source, cross-platform, server-side JavaScript runtime released in 2009 (NODEHB p.2).
- **[from source]** It runs the V8 engine (Chrome's) outside the browser and benefits from JIT (NODEHB p.2, p.14-16).
- **[from source]** A Node app runs in **a single process, without creating a thread per request**; the standard library provides asynchronous I/O primitives and libraries are usually non-blocking (NODEHB p.2). On I/O, Node resumes the operation when the response arrives instead of blocking (NODEHB p.2-3).
- **[from source]** This allows thousands of simultaneous connections on one server without managing thread concurrency (NODEHB p.3).
- **[from source]** Canonical example: `http.createServer` with `res.statusCode = 200`, `setHeader('Content-Type', 'text/plain')` and `res.end(...)`; the `request` event delivers `http.IncomingMessage` and `http.ServerResponse` (NODEHB p.3-5).
- **[from source]** The author lists as relevant frameworks/tools (2018): Express, Meteor, Koa, Next.js, Micro, Socket.io, with one sentence each (NODEHB p.5-6). That is all; no details on Koa/Meteor/Micro (NOT COVERED).

## History (NODEHB p.7-10)
**[from source]** The author's timeline: 2009 Node and the first npm are born; 2010 Express and Socket.io; 2011 npm 1.0 and adoption by LinkedIn/Uber, Hapi; 2013 Ghost and Koa; 2014 io.js fork; 2015 Node.js Foundation, io.js merged back, Node 4, npm with private modules; 2016 leftpad incident, Yarn, Node 6; 2017 Node 8, HTTP/2, 3 billion npm downloads per week; 2018 Node 10 and experimental support for ES modules `.mjs` (NODEHB p.8-10). **[DATED]**: nothing later than 2018.

## Installing (NODEHB p.10-11)
**[from source]** Official package, a package manager (Homebrew: `brew install node`) or nvm (switch versions, test with old versions). The author suggests the official installer for beginners; Homebrew is his preference (p.11).

## Required JavaScript and differences from the browser (NODEHB p.11-14)
- **[from source]** List of JS concepts to master first: lexical structure, types, functions, `this`, arrow functions, scope, arrays, template literals, strict mode, ES6+; and asynchronous: callbacks, timers, promises, async/await, closures, event loop (p.11-12).
- **[from source]** In Node there is no `document` or `window`; there are modules such as the file system one; **you control the Node version** (unlike the browser); Babel is not needed for ES6+ in Node; Node uses **CommonJS** (`require`) while the browser was beginning to have ES Modules (`import`) (p.13-14). **[DATED]** this `require` vs `import` distinction reflects 2018.

## V8 (NODEHB p.14-16)
**[from source]** V8 is independent of the browser, written in C++; other engines: SpiderMonkey, JavaScriptCore, Chakra; V8 also powers Electron; modern JS is compiled (JIT), not just interpreted.

## Ending a program (NODEHB p.16-19)
- **[from source]** `process.exit()` ends immediately: pending callbacks, network requests being sent, file access and writes to stdout/stderr are aborted; it accepts an exit code (`process.exit(1)`; default 0 = success); alternative: `process.exitCode = 1` (p.17-18).
- **[from source]** A server does not end on its own; to shut down gracefully, handle **SIGTERM** with `process.on('SIGTERM', ...)` and call `server.close(...)` (p.18-19). SIGKILL terminates immediately; SIGTERM is the signal used by process managers (p.19); `process.kill(process.pid, 'SIGTERM')` sends the signal from code (p.19).

## Environment variables (NODEHB p.20-21)
**[from source]** `process.env`; `NODE_ENV` (the text says it comes as `development` by default; setting `production` signals production); variables on the command line (`API_KEY=... node app.js`); `.env` file + `dotenv` package (`require('dotenv').config()`), with `.env` in `.gitignore`; Next.js loads `.env` without dotenv.

## Hosting (NODEHB p.21-25) **[DATED] 2018 list**
**[from source]** From simplest to most complex: local tunnel (ngrok, localtunnel; "you are opening your machine to the internet"), zero-config (Glitch, Codepen), serverless (Serverless Framework, Standard Library on top of AWS Lambda and similar), PaaS (Zeit Now, Nanobox, Heroku, Azure, Google Cloud), VPS (Digital Ocean, Linode, AWS/Elastic Beanstalk), bare metal (Vultr). Plans, prices and the very existence of these services are **[DATED]**.

## REPL (NODEHB p.25-30)
**[from source]** `node` with no file opens the REPL; `tab` autocompletes and lists properties (`Number.` + tab; `global.` + tab); `_` holds the last result; dot commands: `.help`, `.editor` (Ctrl-D runs), `.break` (Ctrl-C), `.clear`, `.load`, `.save`, `.exit`; multiline blocks are detected (`...`).

## Arguments and console (NODEHB p.30-38)
- **[from source]** `process.argv`: position 0 = path of `node`, 1 = file; arguments start at 2 (`process.argv.slice(2)`); for `name=flavio`, use the **minimist** package (p.31-32).
- **[from source]** `console.log` with formatting (`%s`, `%d`/`%i`, `%f`, `%O`), `console.clear`, `console.count`, `console.trace`, `console.time`/`timeEnd`; `console.error` writes to **stderr** (p.33-36); colors with escape sequences (`\x1b[33m`) or **chalk**; progress bar with the **progress** package (p.36-38).
- **[from source]** `readline` ("since version 7") to read from `process.stdin`; so that passwords are not echoed, `readline-sync`; more complete: **Inquirer.js** (p.38-40).

Related: `02-modulos-npm-semver.md`, `03-event-loop-e-assincronia.md`, `datado.md`.

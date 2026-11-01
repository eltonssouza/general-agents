# 06 — MySQL with Node and development vs production

Source: NODEHB (6/9/2018). Pages = PDF. **[DATED]** the `mysql` package ("mysqljs/mysql", "more than 12,000 stars" in 2018, p.193) and the `app.configure` API.

## MySQL (NODEHB p.193-197)
- **[from source]** `npm install mysql`; `mysql.createConnection({ user, password, database })`; `connection.connect(err => ...)` (p.193-194). Other options: `host` (default localhost), `port` (default 3306), `socketPath`, `debug` (off by default), `trace` (on by default), `ssl` (out of scope) (p.194-195).
- **[from source]** `connection.query('SELECT * FROM todos', (error, todos, fields) => ...)`. Values passed in the array are **escaped automatically** when `?` is used: `... WHERE id = ?`, `[id]`; several values = more items in the array (p.195-196).
- **[from source]** INSERT with an object: `'INSERT INTO todos SET ?', todo`; with an `auto_increment` primary key, the generated id comes in `results.insertId` (p.196). **Error in the text:** the snippet on p.197 reads `results.resultId`, which contradicts p.196; the snippet also has unbalanced braces/parentheses.
- **[from source]** `connection.end()` ensures that pending queries are sent and the connection is closed gracefully (p.197).
- The sources have no connection pooling, transactions, ORMs or other databases (NOT COVERED); `@fastify/mongodb` appears only in the Fastify plugin example (FSTF p.6-8).
- Security: the text does not discuss SQL injection by name; the claim that concatenating SQL is dangerous is an **[inference]** from the automatic escaping of placeholders (p.195) / an **[extrapolation]** for the rest.

## Development vs production (NODEHB p.197-199)
- **[from source]** Node assumes development; signal production with `NODE_ENV=production` (`export NODE_ENV=production`, in the shell configuration file to persist, or before the command: `NODE_ENV=production node app.js`) (p.197-198). It is a convention used by external libraries (p.198).
- **[from source]** In production, in general: minimal logging and more caching layers. Example: Pug compiles in debug mode if `NODE_ENV` is not `production`; in Express, views are compiled on every request in development and **cached** in production (p.198).
- **[from source]** The text shows `app.configure('development', ...)`, `app.configure('production', ...)`, `app.configure('production', 'staging', ...)` and `express.errorHandler({ dumpExceptions: true, showStack: true })` (p.199). **[DATED]** 2018 and with no Express version; **[extrapolation]** these APIs do not exist in current Express versions — do not use them as a model; check the current documentation. The linter flags this (NODE-CONFIGURE).

Related: `01-node-runtime.md` (environment variables), `07-express.md`, `datado.md`.

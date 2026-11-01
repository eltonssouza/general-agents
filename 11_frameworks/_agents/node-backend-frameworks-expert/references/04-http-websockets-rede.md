# 04 — HTTP, server and client, Axios, WebSockets, http module

Source: NODEHB (6/9/2018). Pages = PDF. **[DATED]**: Axios, `ws` and the 2018 ecosystem; the text covers HTTP/1.1.

## How an HTTP request happens (NODEHB p.126-133)
- **[from source]** Steps described (macOS/Linux): the browser completes the URL (prepends `HTTP://` if there is only a domain) (p.127); **DNS**: local cache, then `gethostbyname`, hosts file (`/etc/hosts`), configured DNS server (e.g. Google's 8.8.8.8, Cloudflare's 1.1.1.1), over UDP; resolvers ask the root server, then the TLD, then the domain's authoritative servers (p.127-130).
- **[from source]** **TCP**: handshake before sending data (p.130). The request is text with a **request line** (method, resource, protocol version, e.g. `GET / HTTP/1.1`), **headers** (two required according to the text: `Host` and `Connection`) and an optional **body** (used in POST) (p.130-132). Common headers: Origin, Accept, Accept-Encoding, Cookie, Cache-Control, Dnt (p.131-132). The header block ends with a blank line (p.132).
- **[from source]** Response: code and message (`200 OK`, `404 Not Found`, `403 Forbidden`, `301 Moved Permanently`, `500 Internal Server Error`, `304 Not Modified`, `401 Unauthorized`), headers and body (p.132-133). The browser repeats the process for each resource (CSS, images, favicon, JS) (p.133).
- Note: the claim about "two required headers" is the author's (p.131); it is not validated here against the specification (**[extrapolation]** check the RFC if it is a technical decision).

## HTTP server in Node (NODEHB p.133-135, p.3-5)
**[from source]** `http.createServer((req, res) => {...})` + `server.listen(port, hostname, cb)`. The callback runs on each request (`request` event); `req` (IncomingMessage) carries details; `res` (ServerResponse) builds the response: `res.statusCode`, `res.setHeader`, `res.end('...')` (p.134-135). p.134 uses `hostname = 'localhost'`; p.3 uses `'127.0.0.1'`.

## Outgoing requests with https (NODEHB p.135-137)
**[from source]** The author says HTTPS "should be used everywhere" (p.135). GET: `https.request(options, cb)` with `hostname`, `port: 443`, `path`, `method`; read `res.on('data', ...)`; `req.on('error', ...)`; `req.end()` (p.136). POST: `JSON.stringify`, `Content-Type` and `Content-Length` headers, `req.write(data)`, `req.end()` (p.136-137). PUT/DELETE: same format, changing `options.method` (p.137).

## Axios (NODEHB p.137-142) **[DATED]**
**[from source]** Promise-based HTTP request library, for browser and Node. Advantages listed by the author over Fetch (in 2018): support for old browsers, aborting a request, response timeout, "built-in CSRF protection", upload progress, automatic JSON transformation, works in Node (p.137-138). API: `axios()`, `axios.get/post/delete/put/patch/options/head` (p.138-139); async/await example with the Dog API and the promises version (p.139-141); parameters via URL or `params` (p.141); POST with an object as the second argument (p.141-142). **[extrapolation]** today Fetch is standard in Node and the author's comparisons may not hold; check the current documentation.

## WebSockets (NODEHB p.142-146)
- **[from source]** Long-lived bidirectional channel between client and server; the server can send without a request; low overhead and latency; great for real time; HTTP is simpler and good for occasional client-initiated exchanges (p.142-143). **Always `wss://`**; `ws://` is the insecure version and should be avoided (p.143).
- **[from source]** Client: `new WebSocket(url)`, `onopen`, `onerror`, `send`, `onmessage` (p.143-145). Server: the **ws** library (`yarn add ws`), `new WebSocket.Server({ port: 8080 })`, `connection` event, `ws.on('message', ...)`, `ws.send(...)` (p.145-146).

## http module (reference) (NODEHB p.178-185)
**[from source]** `http.METHODS`, `http.STATUS_CODES`, `http.globalAgent`; methods `createServer`, `request`, `get` (like `request`, but fixes GET and calls `req.end()`); **5 classes**: `http.Agent` (connection reuse and socket pool), `ClientRequest`, `Server` (`close()` stops accepting connections; `listen()`), `ServerResponse` (`end()` mandatory on every response; `getHeaderNames`, `getHeaders`, `setHeader`, `getHeader`, `removeHeader`, `hasHeader`, `headersSent`; `writeHead`; `write`; `statusCode`/`statusMessage`), `IncomingMessage` (status, headers, method, url, socket; **implements Readable Stream**) (p.178-185). Note: the text describes `headersSent()` as a method and the IncomingMessage properties as "methods"; treat this as the author's informal description.

Related: `05-fs-path-os-events-streams.md` (streams), `07-express.md`. For REST API design, see the web-api-rest-architecture-expert.

# 05 — fs, path, os, events, streams

Source: NODEHB (6/9/2018, Node 10). Pages = PDF. **[DATED]**: the text says Node 10 had the fs promises API as "experimental" (p.162); later versions changed this (**[extrapolation]** confirm in the current docs).

## File descriptors and stats (NODEHB p.146-149)
- **[from source]** `fs.open(path, flag, cb)` returns the descriptor; flags: `r` (read), `r+` (read/write), `w+` (read/write, creates if it does not exist, positions at the start), `a` (write at the end, creates), `a+` (read/write at the end, creates); `fs.openSync` returns the descriptor directly (p.146-147).
- **[from source]** `fs.stat(path, cb)` delivers `stats`: `isFile()`, `isDirectory()`, `isSymbolicLink()`, `size` (bytes) (p.147-149). The synchronous variant **blocks the thread** (p.148). **Error in the text:** the "synchronous" snippet on p.148 calls `fs.stat(...)` without a callback inside a `try` (the synchronous name is `statSync`; see p.160-162).

## path (NODEHB p.149-152 and p.163-167)
**[from source]** `const path = require('path')`; `dirname`, `basename` (the second argument removes the extension), `extname`; `join`, `resolve` (relative → absolute from the current directory; a first argument starting with `/` is an absolute path), `normalize` (resolves `.`, `..` and double slashes); **`resolve` and `normalize` do not check whether the path exists** (p.150-152). Reference: `path.sep` (`\` on Windows, `/` on Linux/macOS), `path.delimiter` (`;` / `:`), `isAbsolute`, `parse` (root, dir, base, name, ext), `relative` (p.163-167). **Error in the text:** the `extname` example on p.164 uses `dirname` on both lines.

## Reading and writing (NODEHB p.152-155)
- **[from source]** `fs.readFile(path, cb)` / `fs.readFileSync(path, 'utf8')`; default encoding utf8 (p.152-153). Both read the **whole file into memory**, which is heavy for large files; for those, streams (p.153).
- **[from source]** `fs.writeFile`/`writeFileSync` **replace** the existing content; the `{ flag: 'a+' }` option appends; `fs.appendFile`/`appendFileSync` append (p.153-155).

## Folders (NODEHB p.155-159)
**[from source]** `fs.access` checks existence/permission; `fs.mkdir`/`mkdirSync` (the example uses `existsSync` beforehand; the `folderName` variable on p.156 is not the `dir` used in the `if` — an inconsistency in the text); `fs.readdir`/`readdirSync` (relative names; use `path.join` for the full path; file filtering with `lstatSync(...).isFile()`) (p.156-157); `fs.rename`/`renameSync` (p.157-158); `fs.rmdir` removes a folder; for a folder with contents the author recommends **fs-extra** (`remove`, with callback, promise or async/await) (p.158-159).

## fs module (NODEHB p.160-163)
**[from source]** List of functions (access, appendFile, chmod, chown, close, copyFile, createReadStream, createWriteStream, link, mkdir, mkdtemp, open, readdir, readFile, readlink, realpath, rename, rmdir, stat, symlink, truncate, unlink, unwatchFile, utimes, watchFile, writeFile and related) (p.160-161). **All methods are asynchronous by default and have a synchronous version with the `Sync` suffix** (`rename`/`renameSync`); the synchronous one **blocks** the script until the operation finishes and uses `try/catch` (p.161-163). Node 10: experimental promises API (p.162).

## os (NODEHB p.167-173)
**[from source]** `os.EOL` (`\n` on POSIX, `\r\n` on Windows), `os.constants.signals`, `os.constants.errno` (p.167-168); methods `arch`, `cpus`, `endianness`, `freemem`, `homedir`, `hostname`, `loadavg` (Linux/macOS only), `networkInterfaces`, `platform`, `release`, `tmpdir`, `totalmem`, `type`, `uptime`, `userInfo` (p.168-173).

## events (reference) (NODEHB p.173-178)
See `03-event-loop-e-assincronia.md` (EventEmitter).

## Streams (NODEHB p.185-192)
- **[from source]** Streams come from Unix (pipe `|`); instead of reading the whole file and then processing, you process it **piece by piece** (p.185-186). Advantages: **memory efficiency** and **time efficiency** (start processing as soon as there is data) (p.186).
- **[from source]** Example: serving a file over HTTP with `readFile` + `res.end(data)` vs `fs.createReadStream(...).pipe(res)`; the stream version starts sending to the client as soon as the first chunk is ready (p.186-187).
- **[from source]** `pipe()` is called on the source and returns the **destination**, allowing `src.pipe(dest1).pipe(dest2)` (p.188).
- **[from source]** APIs with native streams: `process.stdin/stdout/stderr`, `fs.createReadStream/createWriteStream`, `net.connect`, `http.request` (ClientRequest is writable), `zlib.createGzip/createGunzip/createDeflate/createInflate` (p.188-189).
- **[from source]** Four classes: **Readable** (you can read from it/`pipe` it; pushed data stays buffered until a consumer reads), **Writable**, **Duplex**, **Transform** (a duplex whose output is a transformation of the input) (p.189).
- **[from source]** Creating: `new Stream.Readable()` and `push('hi!')`; Writable implements `_write(chunk, encoding, next)` and calls `next()`; consume a Readable via `pipe` or via the `readable` event with `read()`; `write()` sends to a writable; `end()` signals the end (p.189-192).

Related: `03-event-loop-e-assincronia.md`, `casos-e-antipadroes.md`. Linter: NODE-FS-NOCB, NODE-SYNC-HANDLER, NODE-READFILE-RESPONSE.

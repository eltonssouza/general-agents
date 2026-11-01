# Image optimization: layers, Alpine, multi-stage, .dockerignore

Pages = PDF (DOCKHB).

## The book's experiment (NGINX compiled from source)
| Version | Size | Page |
| --- | --- | --- |
| Ubuntu, separate RUNs, build packages kept | 343MB | p.72 |
| Official `nginx:stable` image (reference) | 133MB | p.72, 77 |
| Ubuntu, a single RUN that installs, compiles and removes | 81.6MB | p.74-77 |
| Alpine, same idea with `apk` | 12.8MB | p.77-80 |

- [from source] Cause of the excess: compilation packages (build-essential, `-dev`) are needed to compile, not to run; only `libpcre3` and `zlib1g` are needed to run (DOCKHB p.73).
- [from source] **Core rule**: installing and removing packages in separate RUN instructions does not shrink the image, because each RUN is a layer and the package size stays in an earlier layer; do install, compile and remove in the **same layer** (DOCKHB p.75).
- [from source] Clear the package manager cache in the same RUN: `apt-get clean && rm -rf /var/lib/apt/lists/*` (DOCKHB p.55-56, 74).

## Alpine
- [from source] Alpine is a full distribution based on `musl libc` and `busybox`; the author cites ~28MB for ubuntu vs ~2.8MB for alpine (figures of the time) and describes it as lightweight, secure and better suited to containers (DOCKHB p.77).
- [from source] `apk add --no-cache` avoids keeping the cache; `--virtual .build-deps` groups build-only packages and `apk del .build-deps` removes them; package names differ between distributions (DOCKHB p.78-79).
- [extrapolation] Alpine uses musl; some binaries and libraries behave differently from glibc. The book only says the transition is simple and that you research when something breaks (DOCKHB p.77, 80).

## Multi-stage build
- [from source] In production the JS app becomes static files (`npm run build`) and only needs a server such as nginx; embedding nginx in the node image is valid but leaves the image large (DOCKHB p.96-97).
- [from source] Better: a `builder` stage (node) compiles; the final `nginx:stable-alpine` image receives only the artifacts via `COPY --from=builder /app/dist /usr/share/nginx/html` and discards everything from node (DOCKHB p.97-98).
- [from source] The syntax `FROM ... as builder` names the stage (DOCKHB p.98).
- [from source] In the Express API: stage 1 installs `python make g++` (needed by `node-gyp`) and `npm install --only=prod`; stage 2 sets `NODE_ENV=production`, `USER node`, copies the code and `node_modules` from the builder (DOCKHB p.118-119).
- [from source] Multi-stage is useful in large apps and yields compact images if well configured (DOCKHB p.101).

## .dockerignore
- [from source] Analogous to `.gitignore`; lists files excluded from the build; must be in the context; entries are ignored by `COPY`; it does **not** affect bind mounts. The book's example: `.git`, `*Dockerfile*`, `*docker-compose*`, `node_modules` (DOCKHB p.101-102).
- [extrapolation] Excluding `.env`, keys and CI artifacts from the context is a security practice; the book does not mention it.

## Non-root user
- [from source] Docker runs containers as root by default; the author cites Docker/Node best practices that flag this as a risk, recommends non-root "whenever possible" and uses the official image's `node` user (`USER node`) (DOCKHB p.89, 119).
- [inference] Not all of the book's images set `USER` (the rmbyext Dockerfile and the multi-stage's final nginx stage lack the instruction, so they run as root) (DOCKHB p.81, 97).

## Outside the book
- [extrapolation] distroless/scratch, `slim`, squash, layer caching in CI, vulnerability scanners, SBOM, signing. Flag it if the user asks.
- [DATED] Size figures and versions (nginx 1.19.2, libssl1.1, python2 in apk, ubuntu 28MB) are from 2021.

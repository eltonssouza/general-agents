# Dockerfile and building images

Pages = PDF (DOCKHB).

## Anatomy (the book's NGINX example, p.53-58)
- [from source] Before writing the Dockerfile, plan the final state of the image; for NGINX: the software installed and started automatically (DOCKHB p.54). The plan for an app should come from whoever developed it (DOCKHB p.88).
- [from source] A Dockerfile is a set of instructions; each instruction produces a layer (DOCKHB p.54-55).
- Instructions that appear in the examples:

| Instruction | What the book says | Page |
| --- | --- | --- |
| `FROM` | every valid Dockerfile starts with it; defines the base image | p.55 |
| `EXPOSE` | documents the port; `--publish` is still needed | p.55 |
| `RUN` | runs a command in the shell during the build; shell or exec form | p.55-56 |
| `CMD` | default command; exec form in the examples | p.56 |
| `COPY <source> <destination>` | copies from the host into the image; `.` = working directory (default `/`) | p.66 |
| `ADD` | like COPY, but also downloads from a URL; does not extract what it downloads | p.67-69 |
| `ARG` | variables used as `${name}`, with a default and an override at build time | p.67-69 |
| `WORKDIR` | working directory for the following COPY/ADD/RUN/CMD | p.82, 89 |
| `USER` | default user (Docker runs as root by default) | p.88-89 |
| `ENV` | environment variable in the image (e.g. `NODE_ENV`) | p.118-119 |
| `ENTRYPOINT` | turns the image into an executable | p.81-82 |

- [from source] Running NGINX as a single process (`daemon off;`) in containers is considered good practice (DOCKHB p.56).

## Build, context and tags
- [from source] `docker image build .`: the daemon needs the Dockerfile name (looked up in the context) and the **context**, the directory accessible to the daemon during the build (DOCKHB p.56-57).
- [from source] `--tag <repository>:<tag>` (`-t`); `docker image tag` to rename later; `image ls`, `image rm`, `image prune` (dangling; `-a` all cached; `-f` without confirmation) (DOCKHB p.58-61).
- [from source] `--file` when the Dockerfile is not named `Dockerfile` (e.g. `Dockerfile.dev`) (DOCKHB p.90-91).
- [from source] Without an explicit tag the image gets `latest` (DOCKHB p.83, 86).

## Layers
- [from source] `docker image history <image>` lists the layers; the top one is the most recent; each instruction records changes; a container adds a writable layer (DOCKHB p.62-63).
- [from source] The union file system avoids duplicating data and lets Docker reuse earlier layers as a build cache (DOCKHB p.63-64).

## The book's Dockerfile patterns
1. **Node app dev** (`Dockerfile.dev`): base `node:lts-alpine`, `EXPOSE`, `USER node`, `mkdir` + `WORKDIR`, `COPY package.json`, `RUN npm install`, `COPY . .`, exec-form `CMD` (DOCKHB p.87-91).
2. **Executable image** (`rmbyext`): base `python:3-alpine`, `WORKDIR`, install git, install the script, remove git in the same RUN, `ENTRYPOINT` (DOCKHB p.80-83).
3. **Multi-stage** for static production and for the API: see `otimizacao-multistage-dockerignore.md`.

## Notes on rigor
- [inference] The order "copy package.json → install → copy the rest" is the pattern used in the book (DOCKHB p.88-90, 97); the book does **not** explain the cache gain; the justification comes from the package author.
- [from source] The examples use `ubuntu:latest` and `alpine:latest` (DOCKHB p.55, 77); the book itself warns that `latest` does not guarantee the most recent version (DOCKHB p.86). Recommending version pinning is [extrapolation].
- [from source] Some examples have small inconsistencies from the original text: one step shows the tag `custom-nginx:built-v2` when describing the run (DOCKHB p.71) and the Dockerfile on p.68 contains `rm -rf /${FILENAME}}` with an extra brace. Do not reproduce them as examples.

## Outside the book
- [extrapolation] `HEALTHCHECK`, `LABEL`, `VOLUME`, `SHELL`, `ONBUILD`, `STOPSIGNAL`, `ARG` before `FROM`, `--target`, BuildKit and cache mounts, pinning by digest, image signing, `COPY --chown`. Do not attribute to the book.

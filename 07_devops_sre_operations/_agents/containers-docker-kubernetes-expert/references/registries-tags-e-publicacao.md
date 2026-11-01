# Registries, tags and publishing images

Pages = PDF (DOCKHB).

## Registry
- [from source] Registry = central place where images are pushed and pulled; Docker Hub is the default public one; Quay (Red Hat) too; a private registry is possible; there is a local cache of downloaded images (DOCKHB p.23-25).

## Tags
- [from source] Repository = image name; tag = build/version: `--tag <repository>:<tag>`; e.g. `mysql:5.7` (DOCKHB p.58-59). Rename/re-tag later: `docker image tag` (DOCKHB p.60).
- [from source] The name (repository) cannot change after upload; the tag can change at any time and usually reflects the software version or build types (DOCKHB p.85-86).
- [from source] Tag examples: `node:lts` (long-term support) and `node:lts-alpine` (Alpine variant, much smaller) (DOCKHB p.86).
- [from source] No tag → `latest`. This does **not** guarantee it is the most recent version: if someone tags an old version as `latest`, Docker does not check (DOCKHB p.86). On `docker run` with `:latest`, the daemon downloads again if there is a newer version in the registry (DOCKHB p.28).
- [extrapolation] Pinning an exact version (or digest) in `FROM` and per-commit immutable tags in CI are recommended practices. The book's examples use `latest` (DOCKHB p.55, 65, 77).

## Publish to Docker Hub
1. Create a free account (unlimited public repositories and one private, at the time) (DOCKHB p.83) [DATED].
2. `docker login` (user and password); the book shows the warning that the password is stored unencrypted and that a *credential helper* can be configured (DOCKHB p.83-84).
3. Build with tag `<user>/<image>:<tag>` (DOCKHB p.84-85).
4. `docker image push <user>/<image>:<tag>` (DOCKHB p.86). Layers already in the registry appear as "Mounted from" (DOCKHB p.86).

## Security and rigor
- [from source] The unencrypted-password warning on `docker login` appears in the book's output (DOCKHB p.84).
- [extrapolation] Prefer access tokens to passwords, credential helpers, minimal scope and CI for publishing. The book does not cover this.
- [DATED] Docker Hub free-plan limits, the pull rate-limit policy and the private repository offer have changed since 2021.

## Outside the book
- [extrapolation] Signing (Notary/cosign), registry scanning, retention/cleanup, mirrors, cloud registries (ECR, GCR/Artifact Registry, ACR), multi-arch manifests.

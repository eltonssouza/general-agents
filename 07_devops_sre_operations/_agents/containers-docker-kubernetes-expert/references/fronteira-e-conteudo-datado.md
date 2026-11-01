# Scope boundary, [DATED] content and the missing Twelve-Factor source

## 1. State of the sources
| Acronym | Source | State |
| --- | --- | --- |
| DOCKHB | *The Docker Handbook* (freeCodeCamp, 1 Feb 2021, 148 pp., native text) | **usable**; old edition |
| K8SB | *Learn Kubernetes Basics* (kubernetes.io), 2 pp. | **usable, but minimal**: only the tutorial index page |
| (12-Factor) | `Twelve-Factor-App.pdf` | **USELESS**: 12 pages showing only "Page not found" |

**Twelve-Factor: pending.** The PDF in this folder is an error capture (no content). The agent **does not cite** Twelve-Factor as a source and treats any 12-factor material as a flagged [extrapolation]. To promote it to [from source], obtain the page again (12factor.net) as a valid PDF/HTML, extract the text and regenerate this package (add a `twelve-factor.md` reference, checks in `citation-checks.json` and the lookup).

DOCKHB points that merely *match* 12-factor ideas, without citing it (they are not from Twelve-Factor): configuration via environment variables (DOCKHB p.112, 123-124); foreground/single process (DOCKHB p.56); logs via `container logs` (DOCKHB p.115-117).

## 2. What the collection does NOT cover (answer as [extrapolation] or decline)
- **Dockerfile**: HEALTHCHECK, LABEL, VOLUME, ONBUILD, SHELL, STOPSIGNAL, pinning by digest, BuildKit/buildx, multi-arch, `--target`, cache mounts.
- **Runtime**: CPU/memory limits, `--restart` (only `restart: unless-stopped` appears in Compose, DOCKHB p.143), healthchecks, `docker stats/top/cp/attach`, `docker system prune`, rootless.
- **Security**: vulnerability scanners, image signing, secrets, `--privileged`/capabilities/seccomp, read-only rootfs, SBOM. The book only recommends a non-root `USER` (p.89) and shows the unencrypted-password warning on `docker login` (p.84).
- **Compose**: `depends_on`, `healthcheck`, `profiles`, `env_file`, overrides, secrets, `deploy`.
- **Orchestration**: Swarm, Kubernetes (beyond the index page), Helm, Operators, service mesh.
- **Operations**: CI/CD, observability, logging drivers, cloud registries, retention policies.
- **Platform**: Windows containers, internals (namespaces/cgroups), OCI beyond the mention (p.23).

## 3. [DATED] content (2021 edition)
| Book item | Situation to check in the current documentation |
| --- | --- |
| `docker-compose` (hyphen) and separate installation (p.12-15, 135+) | today `docker compose` (v2 plugin); v1 discontinued |
| `version: "3.8"` described as the "latest" (p.132) | `version` field obsolete in the current Compose Specification |
| Docker Desktop and the "stable" channel (p.10-14) | licensing and installation have changed |
| macOS with HyperKit (p.22-23) | virtualization back-ends have changed |
| Build output "Step N/M", "Removing intermediate container" (p.57+) | output changes with BuildKit |
| Docker Hub free plan: unlimited public + 1 private (p.83) | plans and rate limits have changed |
| Sizes (ubuntu 28MB, alpine 2.8MB, nginx 133MB) and versions (nginx 1.19.2, libssl1.1, Node 15, Postgres 12, Alpine 3.11) | all have changed |
| `python` package (Python 2) in Alpine apk (p.118-120) | Python 2 was removed from current distributions |
| `npm install --only=prod` (p.118-119) | flag obsolete in recent npm (`--omit=dev`) [extrapolation] |
| `docker container ls`, `image build` | stable forms; only check for new options |

## 4. Slips in the text itself (do not replicate)
- p.71: mentions the tag `custom-nginx:built-v2` where the command used `custom-nginx:built`.
- p.68: `rm -rf /${FILENAME}}` with an extra brace.
- p.134: says `db` becomes the IP of the "api" service; the example indicates the `db` service.
- p.131 vs p.132-135: the complete file on p.131 uses the volume key `notes-db-dev-data`; the snippets explained on p.132-135 use the key `db-data` with `name: notes-db-dev-data`. The effect (a volume named notes-db-dev-data) is the same.

## 5. Answering rules for gaps
1. Say "the collection does not address this" and cite the closest material (with page).
2. If you do answer, open with `[extrapolation]` and recommend checking the official documentation.
3. Never produce "(DOCKHB p.N)" for something the book does not say. Use `python -I scripts/docker_lookup.py <term>` to see "NOT IN THE SOURCE".

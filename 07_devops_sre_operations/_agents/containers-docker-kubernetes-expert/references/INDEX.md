# Reference INDEX (containers-docker-kubernetes-expert)

## Sources and page convention
- **DOCKHB** = *The Docker Handbook – Learn Docker for Beginners*, Farhan Hasin Chowdhury, freeCodeCamp, 1 Feb 2021, **148 pp.** (file `Docker-Handbook-freeCodeCamp.pdf`).
- **K8SB** = *Learn Kubernetes Basics*, kubernetes.io, **2 pp.** (only the tutorial index page; file `Kubernetes-Basics-docs.pdf`).
- **Twelve-Factor-App.pdf**: **unusable** (12 "Page not found" pages). It is not a source. See `fronteira-e-conteudo-datado.md`.
- **Page convention**: ALWAYS the **PDF page** (1-148 in DOCKHB; 1-2 in K8SB). DOCKHB has no printed page numbering, so there is no conversion map. Sections by page: p.1-6 opening/table of contents; p.7-10 containerization; p.10-16 installation; p.16-28 hello-world, container/image/registry, architecture; p.28-52 container commands; p.52-87 images and Dockerfile; p.87-102 JS app (volumes, multi-stage, .dockerignore); p.102-111 networks; p.111-128 multi-container app; p.129-148 Compose.
- Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Only `[from source]` may carry a page.

## When to open each file
| Trigger in the question | File |
| --- | --- |
| what a container is, VM vs container, image, registry, daemon, installation | `fundamentos-containers-e-arquitetura.md` |
| `run`, `stop`, `kill`, `exec`, `logs`, `-p`, `-d`, `-it`, `--rm`, list/remove containers | `comandos-de-container.md` |
| Dockerfile, FROM/RUN/CMD/COPY/ADD/ARG/WORKDIR/USER/ENTRYPOINT, build, tag, layers | `dockerfile-e-imagens.md` |
| large image, Alpine, multi-stage, `.dockerignore`, non-root | `otimizacao-multistage-dockerignore.md` |
| volume, bind mount, database persistence, `node_modules` | `volumes-e-persistencia.md` |
| network, DNS between containers, bridge, `127.0.0.1` | `redes-docker.md` |
| app with API + database, Compose, `docker-compose.yaml`, nginx router, full-stack | `app-multicontainer-e-compose.md` |
| Docker Hub, `push`, `login`, tags, `latest` | `registries-tags-e-publicacao.md` |
| Kubernetes, orchestration, Minikube | `kubernetes-e-orquestracao.md` |
| what the book does not cover, old versions, Twelve-Factor, slips in the text | `fronteira-e-conteudo-datado.md` |
| unknown term | `glossario.md` |
| step by step (containerize, shrink image, dev with bind mount, network, persistence, Compose, publish, clean up, review) | `procedimentos.md` |
| general review, "what is wrong here?", cases | `casos-e-antipadroes.md` |

## Scripts (in `scripts/`; Python 3 stdlib, no network, deterministic; run with `python -I`)
| Script | Purpose |
| --- | --- |
| `docker_lookup.py` | topic lookup (rules with page, "NOT IN THE SOURCE", [DATED]); prints "NOT COVERED" when the collection does not address it |
| `dockerfile_lint.py` | static Dockerfile linter calibrated by the book's good/bad practices; each finding carries its origin |
| `docker_cmd_check.py` | static validator for `docker`/`docker-compose` commands; flags [DATED] and destructive ones |
| `verify_citations.py` + `citation-checks.json` | 83 positive and 22 negative checks against the source text |
| `docker_index.json` | lookup data index |

## Topic → pages map (summary)
containerization p.7-10 · VM vs container p.19-23 · image/registry p.23-25 · architecture p.25-28 · `docker <obj> <cmd>` syntax p.29 · publish port p.30-31 · detach p.32 · stop/kill p.36-37 · create/start p.40-41 · `--rm` p.43-44 · `-it` p.44-46 · exec p.47-48, 125-126 · bind mount p.50-52 · Dockerfile p.53-57 · tag p.58-61 · layers p.62-64 · ARG/ADD p.67-69 · optimization p.72-80 · executable p.80-83 · push p.83-86 · app JS p.87-91 · volumes p.92-96 · multi-stage p.96-101 · `.dockerignore` p.101-102 · networks p.102-111 · Postgres/named volume p.111-115 · logs p.115-117 · API multi-stage p.118-119 · exec/migrate/scripts p.125-128 · Compose p.129-147 · K8SB p.1-2.

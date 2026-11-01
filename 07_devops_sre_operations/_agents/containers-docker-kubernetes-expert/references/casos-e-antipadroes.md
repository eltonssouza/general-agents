# Cases and anti-patterns

Origin: lessons demonstrated in DOCKHB (with page) and, where indicated, [extrapolation]. Pages = PDF.

## Anti-patterns the book demonstrates or points out
| # | Anti-pattern | Symptom | Book's fix | Page |
| --- | --- | --- | --- | --- |
| A1 | Options after the image name in `docker run` | option ignored; becomes an entry-point argument | move options before the image | p.32 |
| A2 | Connecting to the database via `127.0.0.1` from inside another container | "database not found" | container name on a user-defined bridge | p.103-104 |
| A3 | Using a container IP | breaks when the container is recreated | names via the defined network's DNS | p.104 |
| A4 | Relying on the default bridge for names | `ping name` does not resolve | create a network and attach with defined names | p.106, 110 |
| A5 | Installing and removing packages in different RUNs | image does not shrink | everything in the same layer / multi-stage | p.75, 97 |
| A6 | Leaving the build toolchain in the final image | 343MB | remove build deps; Alpine; multi-stage | p.72-80, 96-98 |
| A7 | Bind mount covers `node_modules` | `vite: not found` | anonymous volume on `node_modules` | p.94-96 |
| A8 | Database data without a volume | data vanishes when the container is destroyed | named volume | p.113-115 |
| A9 | Expecting EXPOSE to publish the port | app unreachable | `--publish` | p.55 |
| A10 | Interactive image without `-it` | container starts and shows nothing | `-it` | p.45-46 |
| A11 | Running as root | security risk (according to the author) | `USER node` / non-root | p.89 |
| A12 | Believing `latest` is the latest version | unexpected version | explicit tags | p.86 |
| A13 | Stopped containers piling up | space/name and port conflicts | `rm`, `prune`, `--rm` | p.41-44 |
| A14 | Compose in production | — | the book says it is not recommended | p.129 |
| A15 | Browser frontend trying to reach `api` by its Compose name | resolution failure | nginx as router | p.141 |
| A16 | `.dockerignore` expected to apply to a bind mount | "ignored" files show up | does not affect bind mount | p.102 |
| A17 | `docker login` stores the password in plain text | warning from the command itself | credential helper | p.84 |

## Anti-patterns the book does NOT address (only as [extrapolation])
- Secrets in `ENV`/`ARG`/command lines; images without version pins; missing HEALTHCHECK; `depends_on` without readiness; `--privileged` and mounted `docker.sock`; build image with attack tools; absence of resource limits; logs written to a file inside the container. Flag them as general good practices, never as "the book says".

## Worked practical cases
1. **"My Node app does not reload in the dev container"** → bind mount of the code (p.92-94); if it breaks with a missing module, an anonymous volume on `node_modules` (p.95-96).
2. **"The API cannot find Postgres"** → same user-defined network, `DB_HOST` = container name (p.103-104, 124); confirm `--name` (p.110).
3. **"Compiled nginx image at 343MB"** → p.72-80.
4. **"Serve my React/Vue build in production"** → multi-stage with `builder` + `nginx:stable-alpine` (p.96-98).
5. **"Bring up API + database + frontend"** → Compose, nginx router, two networks (p.140-147), with a warning that it is for dev/test only (p.129) and a [DATED] mark on the syntax.
6. **"How do I run Kubernetes?"** → K8SB p.1-2 only points to modules; the rest is [extrapolation] (see `kubernetes-e-orquestracao.md`).
7. **"What are the 12 factors?"** → source unavailable; answer as a flagged [extrapolation] and recommend obtaining the source again (see `fronteira-e-conteudo-datado.md`).

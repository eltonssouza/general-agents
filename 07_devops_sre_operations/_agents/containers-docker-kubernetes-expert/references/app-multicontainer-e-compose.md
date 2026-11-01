# Multi-container app and Docker Compose

Pages = PDF (DOCKHB). Everything here describes the 2021 edition: `docker-compose` v1 and a `version: "3.8"` file [DATED].

## Part 1: notes-api + PostgreSQL without Compose (p.111-128)
The book's sequence (each step with its page):
1. Database: `container run --detach --name=notes-db --env POSTGRES_DB=notesdb --env POSTGRES_PASSWORD=secret --network=notes-api-network postgres:12`. The image requires `POSTGRES_PASSWORD`; `POSTGRES_DB` names the database; `--env` passes variables (DOCKHB p.112).
2. Persistence: create the named volume `notes-db-data` and mount it at `/var/lib/postgresql/data` (stop and remove the container first; recreate with `-v`) (DOCKHB p.113-115).
3. Logs: `container logs notes-db`; `--follow` tails them (DOCKHB p.115-117).
4. Network: `network create notes-api-network` and `network connect` (DOCKHB p.117-118).
5. API image: multi-stage Dockerfile (see `otimizacao-multistage-dockerignore.md`) and `image build --tag notes-api .` (DOCKHB p.118-119).
6. Run the API with `DB_HOST=notes-db`, `DB_DATABASE`, `DB_PASSWORD`, `--publish=3000:3000`, `--network` (DOCKHB p.123-124). `DB_HOST` uses the container name because both are on the same user-defined bridge (DOCKHB p.124).
7. Migration: `container exec notes-api npm run db:migrate` (DOCKHB p.125-126).
8. Automation: `boot.sh`, `build.sh`, `destroy.sh`, `stop.sh` and a `Makefile` with `start`, `stop`, `build`, `destroy` (DOCKHB p.127-128).
- [inference] Values such as `secret` are didactic; the book does not discuss secrets management (see the boundary file).

## Part 2: Docker Compose (p.129-148)
- [from source] Compose = a tool to define and run multi-container apps with a YAML file; "more focused on development and testing"; using it in production is "not recommended at all" (DOCKHB p.129).
- [from source] Each container is a **service**; the file is `docker-compose.yaml` with `version: "3.8"` (the "latest" at the time), `services` and `volumes`; the `networks` block only appears in the full-stack example (DOCKHB p.130-132, 142-144).
- [from source] Each service requires a ready-made image (`image`) or a build (`build: context/dockerfile`) (DOCKHB p.132-134).
- [from source] Keys seen: `image`, `container_name`, `volumes` (named, anonymous or bind), `environment` (map), `build`, `ports` (`host:container`), `restart` (`unless-stopped`) (DOCKHB p.131-134, 143).
- [from source] Default names: container = `<directory>_<service>`; built image = `<directory>_<service>`; named volume without `name` = `<directory>_<key>` (DOCKHB p.133-135).
- [from source] A service references another by its **service name** (`DB_HOST: db`) (DOCKHB p.133-134). [note] The text on p.134 says `db` will be replaced by the IP of the "api" service, but the example and context show it refers to the `db` service; treat it as an author's slip.

### Commands (run in the file's folder; DOCKHB p.135)
| Command | Effect according to the book | Page |
| --- | --- | --- |
| `docker-compose --file docker-compose.yaml up --detach` | builds missing images, creates and starts; `--file` is only needed if the name is different | p.135-137 |
| `up --build` | forces an image rebuild | p.137 |
| `start` | only starts existing containers; does not create | p.137 |
| `ps` | lists only containers defined in the YAML | p.137 |
| `exec <service> <command>` | does not need `-it`; interactive automatically | p.138 |
| `logs <service>` (`-f`) | logs; leaving `-f` does not stop the container | p.138-139 |
| `down --volumes` | stops and removes containers and networks; `--volumes` removes named volumes | p.139-140 |
| `stop` | stops and keeps the containers (resumable by `start`/`up`) | p.140 |

### Full-stack (p.140-147)
- [from source] Four services: `db`, `api`, `client`, `nginx` (router). nginx receives all requests: with `/api` it goes to the backend; otherwise, to the frontend (DOCKHB p.141-143).
- [from source] Reason: the frontend runs in the **browser** (served by a container), not inside a container; therefore the Compose network does not let it find the API. nginx runs in a container and sees all services (DOCKHB p.141).
- [from source] By default Compose creates one bridge and connects everything; the author created two networks (`frontend`, `backend`) for isolation; `db` and `api` on the backend, `client` on the frontend, `nginx` on both (DOCKHB p.143-144). The nginx configuration is out of scope (DOCKHB p.142).
- [from source] Access at `http://localhost:8080` (DOCKHB p.147).

## [DATED] Compose today
- `docker-compose` (Python, v1) was replaced by the `docker compose` plugin (v2); the `version` field is considered obsolete in the current Compose Specification; features such as `depends_on` with a health condition, `profiles`, `env_file`, `secrets` and `deploy.resources` do not appear in the book. All of this is [extrapolation]: check the current documentation before asserting.

## Outside the book
- [extrapolation] Waiting for database readiness (`depends_on` + `healthcheck`), `docker compose up --wait`, override files, secrets management, Compose in production (the book discourages it), Swarm/Kubernetes as a target.

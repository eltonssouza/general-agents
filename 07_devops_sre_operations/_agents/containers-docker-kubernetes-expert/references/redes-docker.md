# Docker networks

Pages = PDF (DOCKHB).

## The problem
- [from source] Containers are isolated and unaware of each other; an API and a PostgreSQL in separate containers need a way to talk (DOCKHB p.102).
- [from source] Two "bad solutions": (1) reach the database through a port published on `127.0.0.1` — inside the API container, `127.0.0.1` is the container itself, where the database does not exist (DOCKHB p.103); (2) use the container's IP (via `container inspect`) — not recommended, and the IP can change when the container is destroyed and recreated (DOCKHB p.103-104).
- [from source] The right answer: put the containers on a **user-defined bridge network** (DOCKHB p.104).

## Drivers
- [from source] `docker network ls` shows `bridge`, `host`, `none` (DOCKHB p.104). The book lists five drivers: `bridge` (default; for containers in normal mode that need to talk), `host` (removes network isolation), `none` (turns networking off), `overlay` (connects several daemons; out of scope), `macvlan` (assigns a MAC, looks like a physical device) (DOCKHB p.104-105). Only `bridge` is used.

## Default bridge vs user-defined
- [from source] Every container joins the default `bridge`; there they communicate only by IP (DOCKHB p.106).
- [from source] Advantages of the user-defined bridge: **automatic DNS** by container name; **better isolation** (the default groups everyone); **connect/disconnect in real time** (on the default you must stop and recreate) (DOCKHB p.106-107).
- [from source] Automatic DNS only works with names you define (`--name`); random names do not resolve (DOCKHB p.110).

## Commands
| Action | Command | Page |
| --- | --- | --- |
| create | `docker network create <name>` | p.107 |
| connect an existing container | `docker network connect <network> <container>` | p.108 |
| at creation | `--network <network>` on `run`/`create` | p.109 |
| disconnect | `docker network disconnect <network> <container>` | p.110 |
| remove | `docker network rm <network>` | p.111 |
| clean up unused | `docker network prune` (`-f`, `-a`) | p.111 |

- [from source] A container can be on more than one network (hello-dock ended up on `bridge` and `skynet`) (DOCKHB p.108).
- [from source] Resolution test: from an alpine container on the same network, `ping hello-dock` works (DOCKHB p.109-110).

## Application in the book
- [from source] notes-api uses `DB_HOST=notes-db` (the database container's name) on the `notes-api-network` network (DOCKHB p.117-118, 123-124).
- [from source] In Compose, services refer to each other by service name (`DB_HOST: db`) (DOCKHB p.133-134) and Compose creates a bridge by default; the full-stack example defines two networks (`frontend`, `backend`), with nginx on both to route (DOCKHB p.143-144). See `app-multicontainer-e-compose.md`.

## Outside the book
- [extrapolation] `--internal`, aliases, IPAM/subnets, custom DNS, networks in Swarm/Kubernetes, `publish` bound to a specific IP, `localhost` in Docker Desktop (`host.docker.internal`).

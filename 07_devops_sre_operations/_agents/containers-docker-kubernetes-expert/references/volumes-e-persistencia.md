# Volumes, bind mounts and persistence

Pages = PDF (DOCKHB).

## Three mechanisms in the book
| Mechanism | Syntax | Use in the book | Page |
| --- | --- | --- | --- |
| **Bind mount** | `-v <absolute path on host>:<path in container>[:option]` | give access to host files (rmbyext); hot reload in dev | p.50-52, 92-94 |
| **Anonymous volume** | `-v <path in container>` | protect the image's `node_modules` when the host code is mounted | p.95-96 |
| **Named volume** | `volume create <name>` + `-v <name>:<path>` | persist PostgreSQL data | p.113-115 |

- [from source] Bind mount = two-way link between a local directory (source) and one in the container (destination); changes on one side show up on the other (DOCKHB p.51). The source must be an absolute path (hence `$(pwd)`); the third field is optional (DOCKHB p.51-52).
- [from source] Classic problem: when mounting the project root over the app directory, the `node_modules` installed in the image disappears and the server fails (`vite: not found`) (DOCKHB p.94-95).
- [from source] Solution: an anonymous volume for `node_modules`; the daemon keeps that directory elsewhere on the host and mounts it back into the container (DOCKHB p.95-96).
- [from source] Databases persist in a directory (PostgreSQL: `/var/lib/postgresql/data`); if the container is destroyed without a volume, the data is lost; a named volume solves it (DOCKHB p.113).
- [from source] A bind mount could work for the database, but the author prefers the named volume (DOCKHB p.115).
- [from source] To check: `docker container inspect` with `.Mounts` formatting (DOCKHB p.115).
- [from source] In Compose, the top-level `volumes` block declares named volumes; without `name`, the volume is called `<project directory>_<key>` (DOCKHB p.135). `down --volumes` deletes the named volumes (DOCKHB p.140).
- [from source] `.dockerignore` does not affect bind mounts (DOCKHB p.102).

## Quick diagnosis
- A Node app in a dev container does not reload when code is edited → missing bind mount of the code (DOCKHB p.92-93).
- After the bind mount the app says a module/binary does not exist → the mount covered `node_modules`; add an anonymous volume (DOCKHB p.94-96).
- Database data vanished when the container was recreated → there was no named volume on the data directory (DOCKHB p.113).
- `docker-compose down --volumes` deleted the data → documented behavior (DOCKHB p.140).

## Outside the book
- [extrapolation] `--mount`, `tmpfs`, volume drivers, backup/restore, `volume prune`, UID/GID mapping and permissions on bind mounts (common on Linux), `:ro`, SELinux (`:z`; appears only as "Mode: z" in inspect output on p.122, unexplained), bind mount performance on Windows/Mac.

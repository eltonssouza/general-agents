# Container commands: lifecycle, ports, interactive, exec, logs

Pages = PDF (DOCKHB). General syntax [from source]: `docker <object> <command> <options>`, with object = container, image, network or volume; the restructuring happened in version 1.13 (DOCKHB p.29). The book itself uses `docker run` and `docker ps -a` in the first examples (DOCKHB p.17-18).

| I want to... | Book's command | Page |
| --- | --- | --- |
| run a container | `docker container run <image>` | p.29-30 |
| publish a port | `--publish <host port>:<container port>` (`-p`) | p.31 |
| run in the background | `--detach` (`-d`); prints the ID | p.32 |
| list running / all | `container ls` / `container ls --all` | p.33-34 |
| name / rename | `--name` / `container rename <current> <new>` | p.34-36 |
| stop gracefully | `container stop` (SIGTERM, then SIGKILL) | p.36-37 |
| kill outright | `container kill` (SIGKILL) | p.37 |
| start a stopped one | `container start` (detached by default, keeps ports) | p.37-38 |
| restart a running one | `container restart` (stops and starts) | p.39 |
| create without starting | `container create` (run = create + start) | p.40-41 |
| remove | `container rm <id...>`; `container prune` | p.41-43 |
| auto-remove on stop | `--rm` | p.43-44 |
| interactive shell | `-it` = `-i` (stdin) + `-t` (pseudo-tty) | p.44-46 |
| run a one-off command | `container run <image> <command>` | p.47-48 |
| command in a live container | `container exec <container> <command>` (+ `-it` for a shell) | p.125-126 |
| view logs | `container logs <container>`; `--follow`/`-f` | p.115-117 |

## Rules and pitfalls from the book
- [from source] Containers are isolated; without publishing a port the host cannot reach the application (DOCKHB p.30-31).
- [from source] The image name must be the **last** item among the `run` options; everything after it goes as an argument to the entry-point and can cause unexpected situations (DOCKHB p.32).
- [from source] The order of options does not matter (`--publish` before or after `--detach`) (DOCKHB p.32).
- [from source] A container ID has 64 characters; the listing shows the first 12; without `--name` Docker generates a random two-word name (DOCKHB p.33-34).
- [from source] Stopped containers remain on the system ("dangling containers"), taking up space and possibly conflicting with new ones; use `rm` or `prune` (DOCKHB p.41-42). The author uses `--rm` in most examples (DOCKHB p.43-44).
- [from source] Distribution and runtime images (ubuntu, node, python) are configured to open a shell; without `-it` the container starts and nothing happens (DOCKHB p.44-46).
- [from source] In `run <image> <command>`, the command goes to the entry-point; most images use the shell as the default entry-point, except executable images (DOCKHB p.47-48).
- [from source] `container start`/`restart`: start only starts a stopped container; restart tries to stop and start, and is what a container that is already running requires (DOCKHB p.37-39).

## Executable images
- [from source] An image with a custom entry-point (e.g. `rmbyext`) treats the `run` arguments as program arguments; to access host files use a bind mount (`-v $(pwd):/zone`) (DOCKHB p.48-52). See `volumes-e-persistencia.md`.

## Outside the book
- [extrapolation] `docker stats`, `docker top`, `docker attach`, `docker cp`, `--restart`, CPU/memory limits (`--memory`, `--cpus`), healthchecks, `docker system prune`. The book does not include these commands.
- [DATED] Some output details (e.g. "Step 1/4", "Removing intermediate container") come from the classic builder and look different today with BuildKit.

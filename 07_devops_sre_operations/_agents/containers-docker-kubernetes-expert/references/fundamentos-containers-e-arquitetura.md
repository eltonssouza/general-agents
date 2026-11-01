# Fundamentals: containerization, container vs VM, image, registry, architecture

Page convention: **PDF page** (DOCKHB has no printed number). Acronyms: DOCKHB = *The Docker Handbook* (Farhan Hasin Chowdhury, freeCodeCamp, 1 Feb 2021, 148 pp.); K8SB = *Learn Kubernetes Basics* (2 pp.).

## Why containerize
- [from source] Containerization packages software with its dependencies to run uniformly on any infrastructure (DOCKHB p.7).
- [from source] The author illustrates with a Node app that, besides Node/Express/SQLite3, requires Python and a C/C++ toolchain because of `node-gyp`; the setup varies across Windows, Mac and Linux and can break on OS updates (DOCKHB p.7-8).
- [from source] The solution in three pieces: **container** (isolated environment identical to the deployment one), **image** (single file with app + dependencies + configuration) and **registry** (central distribution server) (DOCKHB p.8-9).
- [from source] Docker is one implementation of the idea, the most popular; Podman (Red Hat) is cited as another; Kaniko and rkt are described as not yet direct replacements (DOCKHB p.9-10).

## Container vs virtual machine
- [from source] A container is an application-layer abstraction that virtualizes only the host OS; a VM uses a hypervisor and a full guest OS, with a long communication chain and overhead (DOCKHB p.19-21).
- [from source] In a container, the *container runtime* (Docker) sits between the containers and the host OS; with no guest OS, it is lighter (DOCKHB p.21-22).
- [from source] Demonstration: `uname -a` on the host and in an alpine container show the same kernel (DOCKHB p.22). On Windows the kernel is the WSL2 one; on macOS the back-end is a VM on HyperKit (DOCKHB p.22-23) [DATED].
- [inference] Practical consequence: a Linux container brings no kernel of its own; kernel version and modules come from the host.

## Image, layer and container
- [from source] Image = multilayer, self-contained, read-only file; it is the container's template. The OCI standard lets a Docker image run on other runtimes such as Podman (DOCKHB p.23).
- [from source] When a container starts, a temporary writable layer is created on top of the read-only layers (DOCKHB p.23, 63).

## Registry
- [from source] Docker Hub is the default public registry; Quay (Red Hat) is another; a private registry can be hosted and there is a local cache on the computer (DOCKHB p.23-25).

## Architecture (daemon, client, REST API)
- [from source] Docker Engine has three components: the `dockerd` daemon (background process), the `docker` client (CLI) and the REST API between them (DOCKHB p.25-26).
- [from source] Flow of `docker run hello-world`: the client asks the daemon; without the local image, the daemon pulls it from Docker Hub; creates and runs the container; the image stays in the local cache (DOCKHB p.26-28).

## Installation (summary and dating)
- [from source] Windows: WSL2 + Docker Desktop; Mac: Docker Desktop; Linux: install Engine and Compose separately, with the post-install steps; verify with `docker --version` and `docker-compose --version` (DOCKHB p.10-15). Docker Desktop bundles Engine, Compose, Dashboard and Kubernetes (DOCKHB p.14).
- [DATED] `docker-compose` as a separate binary, Ubuntu 20.10/Fedora 33, the Desktop "stable" channel; today Compose is the `docker compose` plugin and the Docker Desktop licensing rules have changed. Point to the current documentation.

## Outside the book
- [extrapolation] namespaces, cgroups, containerd/runc/CRI-O, rootless mode, security isolation between containers and VMs. The book does not cover these.

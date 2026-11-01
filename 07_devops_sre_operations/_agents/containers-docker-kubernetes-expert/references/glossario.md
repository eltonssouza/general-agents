# Glossary (DOCKHB and K8SB terms; definitions in our own words)

Pages = PDF. [DATED] marks a term/form that has since changed.

| Term | Meaning according to the book | Page |
| --- | --- | --- |
| Containerization | packaging software with dependencies to run uniformly on any infrastructure | DOCKHB p.7 |
| Container | isolated environment that virtualizes only the host OS; "a running image" | p.19, 23 |
| Image | multilayer, read-only file, container template | p.23 |
| Layer | result of a Dockerfile instruction; read-only; the container adds a writable one | p.55, 62-63 |
| Union file system | transparent overlay of file systems that enables layers and caching | p.63-64 |
| Registry | central server to push/pull images (Docker Hub, Quay, private) | p.23-25 |
| OCI | standard image specification that lets Docker images run on other runtimes (Podman) | p.23 |
| Daemon (`dockerd`) | background process that manages Docker objects | p.25 |
| Client (`docker`) | CLI that sends commands to the daemon through the REST API | p.26 |
| Container runtime | layer between containers and the host OS (in place of the hypervisor) | p.21-22 |
| Hypervisor | program that creates/manages VMs, between the host OS and the VMs | p.19-20 |
| Tag | version/build identifier after `:`; default `latest` | p.28, 58-59, 86 |
| `latest` | default tag; does not guarantee it is the most recent version | p.86 |
| Entry-point | the image's "front door"; what comes after the image name in `run` is passed to it | p.48 |
| Executable image | image whose ENTRYPOINT is a specific program | p.48-52, 81-82 |
| Interactive (image) | configured to open a shell; requires `-it` | p.44-46 |
| Detached mode | background execution (`-d`) | p.32 |
| Publish a port | forward a host port to the container (`-p host:container`) | p.31 |
| Dangling container | stopped container that remains on the system | p.41 |
| Dangling image | untagged image (removable by `image prune`) | p.60-61 |
| Bind mount | two-way host ↔ container link by absolute path | p.51 |
| Anonymous volume | volume with no source given, managed by the daemon | p.95-96 |
| Named volume | volume with a name, created by `volume create`, referenceable | p.113 |
| Build context | directory accessible to the daemon during the build | p.57 |
| `.dockerignore` | list of exclusions from the build context | p.101-102 |
| Multi-stage build | build in several stages, copying only artifacts to the final stage | p.96-98 |
| Bridge (network) | default network driver; the user-defined one provides DNS by name | p.105-107 |
| Host / none / overlay / macvlan | other network drivers listed | p.105 |
| Service (Compose) | each container that makes up the application | p.130 |
| Compose file | `docker-compose.yaml` (`version: "3.8"` in the book) [DATED] | p.131-132 |
| Router (nginx) | service that receives all traffic and routes `/api` to the backend | p.141 |
| Kubernetes | open-source container orchestration platform | K8SB p.1 |
| Minikube | tool cited in the tutorial for creating a practice cluster | K8SB p.2 |
| Orchestration (K8SB) | ensuring containerized apps run where/when desired and find resources | K8SB p.1 |

Terms the collection does **not** define (do not invent "from source" definitions): Pod, Node, Deployment (beyond the name in the tutorial's objective), Service (K8s), Ingress, namespace, cgroup, healthcheck, secret, digest.

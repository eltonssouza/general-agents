# Kubernetes and orchestration: what the collection says (very little)

Source: **K8SB** = *Learn Kubernetes Basics* (kubernetes.io), **only 2 pages**: the tutorial index page (last modification shown: 14 Jan 2026). It does **not teach** objects, commands or architecture; it lists objectives and modules. Everything beyond that is [extrapolation] and must be flagged.

## What K8SB p.1-2 states
- [from source] Tutorial objectives: deploy a containerized application on a cluster; scale the deployment; update the application with a new version; debug the application (K8SB p.1).
- [from source] Motivation: users expect services 24/7 and developers want to deploy several times a day; containerization helps release and update without downtime (K8SB p.1).
- [from source] Kubernetes helps ensure that containerized applications run where and when you want and find the resources and tools they need; it is an open-source, "production-ready" platform, based on Google's experience in container orchestration combined with ideas from the community (K8SB p.1).
- [from source] The tutorial's **six modules**, in this order: 1 create a cluster; 2 deploy an app; 3 explore the app; 4 expose the app publicly; 5 scale; 6 update (K8SB p.2).
- [from source] The page points to the "Learning environment" (practice clusters) and to the tutorial "Using Minikube to Create a Cluster" (K8SB p.2).

## What DOCKHB says about Kubernetes
- [from source] Only that Docker Desktop (Windows/Mac) bundles Engine, Compose, Dashboard and Kubernetes; on Linux there is no such bundle (DOCKHB p.14). No use of Kubernetes in the book.
- [from source] Docker "allows orchestrating" containers, in a single introductory sentence (DOCKHB p.9); the book only practices local orchestration with Compose (and discourages Compose in production, DOCKHB p.129).

## Permitted bridge (labeled)
- [inference] What K8SB lists (deploy, scale, update, debug) is the set of problems that DOCKHB's Compose does not solve for production; DOCKHB itself limits Compose to development/testing (p.129).
- [extrapolation] Concepts such as Pod, Deployment, Service, Node, ReplicaSet, namespace, Ingress, ConfigMap/Secret, probes, rolling update, HPA, persistent volumes, `kubectl`, YAML manifests, Helm: **are not** in the collection. If the user asks, answer as clearly marked general knowledge, with the caveat to check the official documentation; recommend K8SB's own tutorial (modules 1-6) as the next step.
- [extrapolation] Docker → Kubernetes equivalences (e.g. container ≈ container inside a Pod; `docker run` ≈ `kubectl create deployment`/`run`; `-p` ≈ Service/Ingress; Compose `services` ≈ Deployments) are the agent's analogies, not the book's.

## How to answer
1. Say the collection has only the tutorial's index page.
2. Cite K8SB p.1-2 for what is there (objectives, modules, the one-sentence definition).
3. For the rest, label it [extrapolation] and ask the user to validate against the official tutorial modules.
4. Never invent `kubectl` output or manifests "from the book".

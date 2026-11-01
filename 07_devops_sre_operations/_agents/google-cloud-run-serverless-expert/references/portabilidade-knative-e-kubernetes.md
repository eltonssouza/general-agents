# Portability: Knative Serving and Kubernetes (RUN ch. 10, p.175-188)

Kubernetes in depth: `containers-docker-kubernetes-expert`. Here only what the book says about Cloud Run vs Knative.

## Core idea
- **[from source]** Cloud Run is API-compatible with the open project **Knative Serving**: a service can migrate to Knative with little or no effort (RUN p.175). The author does **not** recommend running Knative locally for development (use Docker Compose, ch. 6) (RUN p.175, 180). Reasons to care about portability: the vendor may change price/terms; regulatory location requirements where Google Cloud does not operate (e.g., mainland China) (RUN p.175-176).
- **[from source]** Knative Serving offers an abstraction for a stateless, container-based, request-oriented service that scales from zero to many. Same resource model: *service*, immutable *revision* (image + settings such as variables and CPU/memory), disposable containers (RUN p.176).
- **[from source]** **Cloud Run is not "managed Knative"**: it is a compatible, separate and proprietary implementation of the same specification, running on Borg (RUN p.176).

## Kubernetes in brief (RUN p.177-180)
- **[from source]** Cluster = nodes; orchestrates containers; the **API server** is the center and the only access to the cluster database (etcd, p.182); resources (Deployment, Pod); **controllers** reconcile the desired state; the kubelet on each node starts the Pods; **CRD** extends the API; Knative adds Service, Configuration and Revision (the Knative *Service* is a different resource, with different semantics from the Kubernetes Service) (RUN p.177-180). Google cites GKE clusters of up to 15,000 nodes (RUN p.177) **[DATED]**.

## Local experiment (RUN p.180-186) [DATED: Oct/2020 versions]
- **[from source]** Minikube (alternatives: k3s, kind) and kubectl via `gcloud components install`; `minikube start --kubernetes-version=1.19.2`; install the Knative operator with `kubectl apply`; namespace `knative-serving`; `minikube tunnel`; `KnativeServing` object with Kourier ingress; DNS via nip.io through the `config-domain` ConfigMap (RUN p.180-185).
- **[from source]** The **same `service.yml`** (apiVersion `serving.knative.dev/v1`) is applied with `kubectl apply -f service.yml` on Knative (`kubectl get ksvc`) and with `gcloud beta run services replace service.yml` on Cloud Run, plus the `allUsers` + `roles/run.invoker` binding (RUN p.185-186). gcloud does not manage the local cluster because it expects Cloud IAM (RUN p.186).

## Differences and cost of leaving (RUN p.187-188)
- **[from source]** Cloud Run provides custom domains and automatic TLS; on Knative this requires extra configuration (RUN p.187).
- **[from source]** Migrating from Kubernetes to Cloud Run is harder than the reverse: Kubernetes has all the primitives (e.g., `CronJob`), the Cloud Run runtime (gVisor) has limitations (e.g., no NFS volumes) and CPU throttling exists only on Cloud Run (RUN p.187).
- **[from source]** Identity: on Cloud Run, Cloud IAM; on Kubernetes there are varied approaches (Istio, Envoy) (RUN p.187). Proprietary services without an open alternative (Cloud IAM, Firestore, Cloud Tasks, Cloud Scheduler) stay with you when migrating (RUN p.188).
- **[from source]** The author's closing: Google's offerings change, consult the current documentation (RUN p.188).

## Rules
1. **[from source]** Keep configuration in Knative YAML and config via environment variables for portability (RUN p.76, 92, 185).
2. **[inference]** Avoid coupling to services with no open equivalent (RUN p.40, 188).
3. **[extrapolation] [DATED]** Cloud Run for Anthos, current Knative (v1.x) and the evolution of the execution environment (gVisor vs 2nd generation) are **not** in the book.

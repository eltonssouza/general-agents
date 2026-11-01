# Services, revisions and traffic (RUN ch. 2-3)

## Service
- **[from source]** *Service* is the key concept: unique name and HTTPS endpoint; it is the resource you deploy, roll back and change settings on, such as environment variables and scaling limits (RUN p.36).
- **[from source]** The first deploy of an image creates the service; the container must listen on port **8080** (default, overridable at deploy) (RUN p.44).
- **[from source]** Enable the API: `gcloud services enable run.googleapis.com`; deploy: `gcloud run deploy NAME --image IMAGE --allow-unauthenticated` (RUN p.45). The book cites the "fully-managed" choice (RUN p.45). **[DATED]** the platform prompt and the flags have changed.
- **[from source]** `--allow-unauthenticated` only permits access without an authentication header (RUN p.45); it implicitly adds an `allUsers` + Cloud Run Invoker binding (RUN p.112-113).

## Region and URL
- **[from source]** Region = physical datacenter; Cloud Run was still expanding regions in Oct/2020 (RUN p.46) **[DATED]**. Default region: `gcloud config set run/region REGION` (RUN p.46). Choose close to users and use the same region as the databases (RUN p.46, 85).
- **[from source]** URL structure: `https://[name]-[project hash]-[region hash].a.run.app` (RUN p.46). **[DATED]** URL format.

## Revision
- **[from source]** Each configuration change creates a **revision**, an immutable copy of the configuration: image contents, arguments/environment variables, serving (timeouts, port), CPU/memory limits, minimum/maximum instance limits, platform configuration (identity, attached resources) (RUN p.48).
- **[from source]** Default behavior: all traffic goes to the newest revision as soon as it becomes available; you can do a gradual rollout or test on a separate URL before moving traffic (RUN p.48).
- **[from source]** List: `gcloud run revisions list --service hello` (RUN p.48). Revisions stay until deleted; Cloud Run starts deleting the oldest above a thousand (RUN p.49) **[DATED]**.
- **[from source]** Rollback: `gcloud run services update-traffic hello --to-revisions REVISION=100` (RUN p.49).
- **[from source]** Update image/config: `gcloud run services update hello --image ...` (RUN p.48). Change only variables: `gcloud run services update frontend --set-env-vars NAME=VALUE` without rebuild (RUN p.124).
- **[from source]** Revision tags: the book presents the **concept** (labeling a revision, having a URL to see the latest version before it receives production traffic), but **does not show the command** (RUN p.49). The `--tag`/`--no-traffic` flags are `[extrapolation]` `[DATED]`.

## YAML configuration and `replace`
- **[from source]** `gcloud run services describe NAME --format yaml` shows the definition (verbose) (RUN p.76). The YAML follows the Knative Serving spec: `apiVersion: serving.knative.dev/v1`, `kind: Service`, `metadata.name`, `spec.template.spec.containers[].image` (RUN p.76).
- **[from source]** `gcloud beta run services replace -` (or a file) applies the YAML; it is **authoritative**: it replaces the entire service configuration, except the IAM bindings, managed separately (RUN p.76). That is why `replace` has no `--allow-unauthenticated`; use `add-iam-policy-binding` with `allUsers` and `roles/run.invoker` (RUN p.76).
- **[from source]** Author's tip: to find out how to express a configuration in YAML, make the change with `gcloud` and read the `describe` (RUN p.76).
- **[from source]** The same `service.yml` works on Cloud Run and Knative Serving (RUN p.185-186; see `portabilidade-knative-e-kubernetes.md`).

## Service parameters the book shows
`--concurrency` (p.54), `--max-instances` (p.96), `--timeout 900`, `--cpu 2`, `--memory 2G` (p.130), `--service-account` (p.115), `--no-allow-unauthenticated` (p.116-117), `--add-cloudsql-instances` (p.89, 91), `--vpc-connector` (p.105), `--set-env-vars` / `--update-env-vars` (p.91, 124, 131). Full table in `cli-flags-e-limites-datados.md`.

## Shutdown and cost
- **[from source]** Services without requests do not bill; you can keep them or delete: `gcloud run services list`, `gcloud run services delete SERVICE` (RUN p.82).

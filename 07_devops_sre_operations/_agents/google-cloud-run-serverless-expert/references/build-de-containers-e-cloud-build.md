# Container builds, Artifact Registry and Cloud Build (RUN ch. 3, p.61-82)

The book is an introduction; for Docker/Kubernetes in depth, refer to `containers-docker-kubernetes-expert`.

## Containers from scratch (p.62-67)
- **[from source]** Image = self-contained package of program(s) and dependencies plus the **image configuration** (program to run, arguments, working directory, environment variables, user ID, root by default; architecture and OS metadata) (RUN p.64-65).
- **[from source]** Container = group of processes isolated from the others on the same host; isolation comes from the Linux kernel (file root, process namespace, network stack, hostname) (RUN p.63, 66-67). Experiments: `docker run -it bash`, `--entrypoint ping`, `-p 9000:8080` (RUN p.62-63).

## Dockerfile (p.68-72)
- **[from source]** Docker reads the build context + Dockerfile and produces the image. Instructions that cover almost all cases: FROM, COPY, RUN, WORKDIR, ENV, ENTRYPOINT (Table 3-1); the author's rule: prefer COPY and ENTRYPOINT over ADD and CMD (RUN p.69-70).
- **[from source]** Smaller is better in production: the `golang` image with the app was 826 MB; shipping unnecessary tools makes deployment slower; a Snyk study (2019) found 30 or more libraries with known vulnerabilities in each of the ten most popular base images (Node with more than 500) (RUN p.71). **[DATED]**.
- **[from source]** Multi-stage with **distroless** (`gcr.io/distroless/base-debian10:nonroot`): final image of 26.7 MB, no shell, no package manager (RUN p.71-72).

## Artifact Registry (p.72-74)
- **[from source]** Hosts images and packages (npm/Maven); it is regional with a multi-region option (US, Asia, Europe) (RUN p.61, 73). Commands: `gcloud services enable artifactregistry.googleapis.com`; `gcloud artifacts repositories create --location us --repository-format docker cloud-run-book` (RUN p.73).
- **[from source]** Image URL: `us-docker.pkg.dev/$PROJECT/cloud-run-book/hello`; credentials: `gcloud auth configure-docker us-docker.pkg.dev`; then `docker push` and `gcloud run deploy` (RUN p.73-74).
- **[from source]** Internal tension: the text says Cloud Run only pulls images from Artifact Registry (RUN p.72), but the first deploy uses a `gcr.io` image (RUN p.45) and mentions the successor of Container Registry. **[DATED]** There are other sources today; check the documentation.

## Without a Dockerfile (p.74-78)
- **[from source]** **ko** (Go): compiles statically, puts the binary in a distroless image, publishes it; variable `KO_DOCKER_REPO`; `ko publish -P IMPORT_PATH`; `ko resolve -f service.yml | gcloud beta run services replace -` (RUN p.75-76). **Jib** (Java, Maven/Gradle): `mvn compile jib:dockerBuild`, distroless base; OpenJDK 11 is 627 MB versus 197 MB distroless; GraalVM/Micronaut/Quarkus start in milliseconds, but GraalVM can break frameworks (RUN p.77).
- **[from source]** **Buildpacks** (Cloud Native): `pack build --builder gcr.io/buildpacks/builder:v1 NAME`; builder = list of buildpacks per language; each one detects whether it fits (go.mod, package.json); supports Go, Node.js, Python, Java and .NET Core (2020); they are the same ones used by App Engine and Cloud Functions (RUN p.78). **[DATED]** languages and builder.

## Cloud Build (p.78-82)
- **[from source]** `gcloud services enable cloudbuild.googleapis.com`; simple use = "remote docker build": `gcloud builds submit --tag $REPO/IMAGE` (RUN p.78-79). Advanced: `cloudbuild.yaml` with steps in sequence (can be parallelized), each step references an image (`name`, `entrypoint`, `args`), shared directory `/workspace`; a failing step stops the build and nothing is published (RUN p.79-81).
- **[from source]** Possible steps: install dependencies, static analysis, unit tests, compile, package, component tests on the image, **deploy to Cloud Run** (RUN p.81). It can run arbitrary programs with a 24-hour timeout (e.g., database migrations) (RUN p.81) **[DATED]**.
- **[from source]** Integrates with version control (e.g., GitHub) through *triggers* that build on every commit; the Cloud Run console has a build+deploy-per-commit wizard (RUN p.81-82).
- **[from source]** The text on p.79 says the image is sent to "Container Registry" even though the example uses an Artifact Registry repository: an inconsistency in the book; **[DATED]**.

## Not covered
CI/CD beyond Cloud Build triggers, Cloud Deploy, promotion between environments, image signing/attestation, vulnerability scanning: **NOT COVERED** by the book (see `fronteira-e-datado.md`).

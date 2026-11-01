# Identity, IAM and authentication (RUN ch. 6, p.109-125)

## IAM fundamentals
- **[from source]** Least privilege: each service only with the permissions it needs; reduces the impact of a vulnerability (RUN p.109). Google Cloud APIs are protected by IAM, which checks the caller's identity and permission (RUN p.109).
- **[from source]** Permissions are granular and grouped into **roles**; useful roles: Storage Object Admin, Cloud Tasks Enqueuer, Cloud SQL Client, Cloud Run Invoker (RUN p.109-110). A **policy binding** links a *member* (Google account, group, service account, or `allUsers` = anyone on the internet) to a role (RUN p.110).
- **[from source]** Where the binding lives: Cloud SQL Client only at project level (like most roles): `gcloud projects add-iam-policy-binding PROJECT --member serviceAccount:SA --role roles/cloudsql.client`; **Cloud Run Invoker** can be at project level (invokes all services) or at **service** level (only that one): `gcloud run services add-iam-policy-binding SERVICE --member serviceAccount:SA --role=roles/run.invoker` (RUN p.111-112). `gcloud run services get-iam-policy hello` shows the `allUsers` binding of a public service (RUN p.112-113).

## The service's service account
- **[from source]** Every service runs with a service account (non-personal identity); client libraries obtain an *access token* from the internal **metadata server**; IAM validates the token and bindings before forwarding the call (RUN p.113).
- **[from source]** If unspecified, the service uses the **default account**, with the **Project Editor** role (more than 3,000 permissions); the book advises against it in production. "Red button" demonstration: the service can delete itself (RUN p.114). **[DATED]** the default account and its roles have changed in new organization configurations.
- **[from source]** Fix: `gcloud iam service-accounts create NAME --display-name ...`, `gcloud iam service-accounts list`, and `gcloud run deploy ... --service-account NAME@$PROJECT.iam.gserviceaccount.com`; without bindings, the delete action fails (RUN p.115). Then add only the necessary bindings (e.g., Cloud SQL Client) (RUN p.115).

## Private service and ID token
- **[from source]** Protect: `--no-allow-unauthenticated`; without a token, the call fails with "Your client does not have permission" (RUN p.116-117). The call needs an **ID token** (signed JWT/OIDC, limited validity): `gcloud auth print-identity-token`; header `Authorization: Bearer $ID_TOKEN` (RUN p.117-118). Do not paste the token into websites or share it: it is valid for one hour for enabled services (RUN p.117).
- **[from source]** When the token is accepted: valid Google signature; *audience* equal to the called service (or a valid gcloud client ID); not expired (one hour at most); a binding exists that allows the account to invoke. Requests with an invalid token do not reach the service and are not billed (RUN p.118).
- **[from source]** Service calling service: the client fetches the ID token from the metadata server; in Go, `idtoken.NewClient(ctx, audience)`; the client is only good for the URL used as the audience; the token is renewed (RUN p.118-119).

## Google Frontend (GFE)
- **[from source]** Calls use the public URL, passing through the GFE: it applies TLS best practices, mitigates DoS up to the transport layer, checks authorization headers and rejects unauthorized requests, removes reserved headers (e.g., `X-CloudTasks-QueueName`); it is not a traditional security perimeter, since Google assumes the internal network is insecure (RUN p.119).
- **[from source]** Minimum additional latency measured by the author: **7 to 9 ms** per call between services; prefer coarse-grained (batch) integration over many fine-grained calls or naive parallelism (RUN p.120). **[DATED]**.

## Frontend + product-api demo (RUN p.120-125)
- **[from source]** Public frontend, private product-api with embedded read-only SQLite (data that fits in memory; a change requires a new image) (RUN p.120-121). Playbook: accounts `frontend` and `product-api`, `services update --service-account`, `roles/run.invoker` binding on product-api only for the frontend account; IAM propagation may take about 20 s (RUN p.124-125). Docker Compose to run locally: `docker-compose up --build` (RUN p.121-123).

## Decision rules
1. **[from source]** One service account per service, minimal bindings, never the default account in production (RUN p.114-115, 124).
2. **[from source]** Authenticate service-to-service with ID token + Invoker binding on the **destination service** (RUN p.111-112, 124-125).
3. **[inference]** 403 error after creating a binding: wait for propagation before investigating (RUN p.124, 153).
4. **[extrapolation]** Secret management (Secret Manager), Workload Identity Federation and VPC Service Controls: **NOT COVERED** by the book.

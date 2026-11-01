# Network: VPC Connector, private IP and traffic path (RUN p.37, 92, 102-105, 119-120)

A short topic in the book: only the **VPC Connector** (egress to private IP) and the ingress path through the GFE appear. Everything else in networking (internal ingress, external load balancer, Direct VPC egress, Cloud NAT, fixed egress IP, Private Service Connect) is **NOT COVERED** (see `fronteira-e-datado.md`).

## Ingress
- **[from source]** By default the service has its own HTTPS endpoint; it can use a custom domain or integrate with the GCP network stack (DDoS, WAF); there can be internal non-public services, useful for receiving events from other products (RUN p.37). Details on how to configure this are not shown.
- **[from source]** Calls between services use the public URL and go through the Google Frontend (GFE); there is a latency cost of 7 to 9 ms (RUN p.119-120). See `identidade-iam-e-autenticacao.md`.

## Egress to private resources
- **[from source]** The VPC gives a private network to resources with private IP (Memorystore, Cloud SQL with private IP, Compute Engine VMs, GKE). Cloud Run is **not part of the VPC**: a **VPC Connector** is needed to reach private IPs (RUN p.92, 102).
- **[from source]** The Connector is a VPC resource created in a region, with a range of **exactly 16 unused private IPs**; TCP connections from the container to a private IP go through it; traffic to public IPs still goes to the internet (RUN p.102-103). Conceptual model: group of instances behind a TCP load balancer; the source becomes one of the 16 IPs (RUN p.103). Scales by throughput: minimum 2 and maximum 10 connector instances, configurable at creation (RUN p.104). **[DATED]** limits and architecture.
- **[from source]** **Not pay-per-use**: it bills even when idle (about US$ 8/month with two instances in Sept/2020) (RUN p.104). **[DATED]**.
- **[from source]** Creation: `gcloud services enable vpcaccess.googleapis.com` and `gcloud compute networks vpc-access connectors create my-connector --region us-central1 --range 10.0.0.0/28`; use: `gcloud run deploy ... --vpc-connector my-connector` (RUN p.104-105). Same region as the target resource (RUN p.105). List/delete: `... connectors list`, `... connectors delete` (RUN p.108).
- **[from source]** Connecting to Cloud SQL via `--add-cloudsql-instances` does not depend on the Connector, even with private IP (RUN p.92).

## Rules
1. **[from source]** Resource with private IP (Redis) -> VPC Connector in the same region (RUN p.101-105).
2. **[from source]** Delete the Connector when finishing experiments so you don't pay (RUN p.108).
3. **[inference]** Prefer `--add-cloudsql-instances` over IP for Cloud SQL (RUN p.90-92).

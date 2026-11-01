# Data: Cloud SQL, Memorystore and sessions (RUN ch. 4-5, p.83-108)

## Cloud SQL (ch. 4)
- **[from source]** Managed relational database (MySQL, PostgreSQL, SQL Server); instance = virtual machine with a database server (RUN p.83, 85). Creation: `gcloud sql instances create sql-db --tier db-f1-micro --database-version MYSQL_8_0 --region us-central1`; APIs: `sqladmin.googleapis.com`, `sql-component.googleapis.com` (RUN p.85). Use **the same region** as the service; different regions increase latency and cost (RUN p.85).
- **[from source]** Cloud SQL is **not serverless**: it bills per minute of active instance (about US$ 9/month for `db-f1-micro` in Sept/2020) (RUN p.86) **[DATED]**. A larger disk usually gives more IOPS (RUN p.85-86).

### Cloud SQL Proxy and connection
- **[from source]** The Proxy creates a secure TLS connection to the Proxy Server on the instance and authenticates through IAM (role **Cloud SQL Client**) (RUN p.86-87). On Cloud Run the Proxy is managed: the flag `--add-cloudsql-instances PROJECT:REGION:INSTANCE` exposes a **UNIX socket** at `/cloudsql/...` (RUN p.89-91).
- **[from source]** Deploy example: `gcloud run deploy todo --add-cloudsql-instances $DB_INSTANCE --image $IMAGE --region $REGION --allow-unauthenticated --set-env-vars DB="mysql://root@unix(/cloudsql/$DB_INSTANCE)/todo"`. The connection string via environment variable favors portability (RUN p.91-92).
- **[from source]** Direct connection by IP is **not** recommended on Cloud Run: it is not encrypted by default, bypasses IAM, requires managing firewall and certificates; additional barrier: `gcloud sql instances patch --require-ssl sql-db` (RUN p.90-91).
- **[from source]** A default user `root@%` without a password exists behind the firewall; the book deletes it and recreates `root` with host `cloudsqlproxy~%`. In production: an application user without administrative privileges and a password on root (least privilege) (RUN p.88-89).
- **[from source]** Public (default) or private IP; private IP exists only inside the VPC, and Cloud Run needs a VPC Connector to reach it; `--add-cloudsql-instances` works with both (RUN p.92). See `rede-vpc-connector-e-trafego.md`.

### Protecting the database from Cloud Run scale
- **[from source]** A relational database handles, for example, 10,000 transactions/s, but degrades if transactional concurrency goes above ~200; the ideal is low concurrency, a small multiple of the number of vCPUs (RUN p.93-94). The transaction rate saturates and may fall with timeouts and refused connections (Figure 4-6, p.94). Cause: resource contention (locks, CPU, disk) (RUN p.95). The optimum depends on version, data and queries and changes over time; find it by monitoring (RUN p.95).
- **[from source]** Controls: (1) service instance limit: `gcloud run services update todo --max-instances 100`; without slots the request waits in the buffer and may receive 429 (RUN p.96); (2) **internal connection pool**: `db.SetMaxOpenConns(2)`; total active connections = max instances x connections per instance (RUN p.96); (3) **external pool** (e.g., PgBouncer on a Compute Engine VM for PostgreSQL) when the internal pool is not enough (RUN p.96).
- **[from source]** Real case: YourSurprise, ~10,000 transactions/s at the Dec/2019 peak, `db-n1-standard-16` (16 vCPU), optimal concurrency ~110 (RUN p.97).
- **[from source]** In production: monitor CPU (Cloud Monitoring); *automatic storage increase*; high availability with two instances in different zones; the application must tolerate outages of about one minute (failover, maintenance); enable automatic backups (RUN p.97-98). Shutdown: `gcloud sql instances delete sql-db` (RUN p.98).

## HTTP sessions and Memorystore (ch. 5)
- **[from source]** Session in memory/local file is not reliable on Cloud Run (disposable container) (RUN p.99). Mechanism: cookie with session ID and **signature**; attributes `Secure`, `HttpOnly`, `SameSite=Strict` (RUN p.100-101). Session storage must be reliable and low-latency (RUN p.101).
- **[from source]** Memorystore (managed Redis): `gcloud services enable redis.googleapis.com`; `gcloud redis instances create my-instance --tier basic --size 1 --region us-central1`; tiers `basic` (single instance) and `standard` (high availability); private IP only, so it requires a VPC Connector; no size autoscaling (monitor memory and alert); not serverless (about US$ 35/month in Sept/2020) (RUN p.101-102) **[DATED]**.
- **[from source]** Alternatives (RUN p.105-106): Memorystore (SLA 99.9%, ~44 min/month), Cloud SQL (SLA 99.95% in HA, ~22 min/month; Memorystore and Firestore handle concurrency better), Firestore (scales by itself, proprietary, regional or multi-region, ~26.3 s/month of unavailability in multi-region, worse latency than Memorystore, pay-per-use). SLA = financial compensation, not a limit or a promise of monthly downtime (RUN p.106). **[DATED]** the SLAs.
- **[from source]** Session affinity: in Sept/2020 **not supported** on Cloud Run; there was a proposal in the Knative spec; even if it comes, it will be best-effort and **not suited for storing session data** in the containers; legitimate uses: per-client cache in memory, game server with long connections (RUN p.106-107). **[DATED]** (the feature came to exist later; see `fronteira-e-datado.md`).
- **[from source]** Shutdown: `gcloud redis instances delete my-instance --region us-central1`; the VPC Connector also bills while it exists: list and delete (RUN p.108).

## Decision rules
1. **[from source]** Always keep state outside the container (RUN p.55, 99).
2. **[inference]** Relational database + Cloud Run: set `--max-instances` x pool per instance <= the database's optimal concurrency.
3. **[inference]** Choosing a session store: latency (Memorystore) vs reliability and autoscaling (Firestore) vs reusing the database (Cloud SQL), per p.105-106.

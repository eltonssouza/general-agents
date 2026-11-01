# Google Cloud Run Serverless Expert (Claude Code, Codex and GitHub Copilot)

Specialist agent in **Google Cloud Run (fully managed platform, 2020 state)**, grounded in a single book:

- **[RUN]** Wietse Venema, *Building Serverless Applications with Google Cloud Run: A Real-World Guide to Building Production-Ready Services*. O'Reilly Media, **first edition, December 2020** (ISBN 978-1-098-12607-0), 204 pages in the PDF (promotional copy "Compliments of" CockroachDB). Source file: `Serverless-Google-Cloud-Run.pdf`. It is a **book**, not a compilation of the official documentation; text written in Sep-Nov/2020; examples in Go.

The rights belong to the author and O'Reilly; this package contains its own syntheses and references, not the text of the book.

## 1. What the agent does
Answers and reviews: serverless model and cost; Cloud Run vs Cloud Functions vs App Engine; services, revisions, rollback and tags; runtime (life cycle, SIGTERM, CPU throttling, concurrency, autoscaler, 429/503, cold start, in-memory disk); container builds (Docker, distroless, Artifact Registry, ko, Jib, Buildpacks, Cloud Build); Cloud SQL (Proxy, pool, `--max-instances`), Memorystore and sessions; VPC Connector; IAM, service accounts, ID token and GFE; Cloud Tasks (worker, retry, rate limit, idempotency); Terraform; structured logs and trace; Knative portability. **Reviews** `gcloud run` commands, Knative `service.yml` and configuration JSON and **generates** deploy checklists.

**Source rigor**: every claim from the book comes with `[from source] (RUN p.N)`. **Page = PDF page** (= printed + 28 in chapters 1-10, p.29-188; the back-of-book index p.189-204 is not a source). What is not from the book comes out as `[inference]`, `[extrapolation]` or `[DATED]`. Since the book is from 2020, **every limit, price, default and flag must be checked against the current** Cloud Run documentation.

**Not covered by the book (NOT COVERED)**: Cloud Run Jobs, always-allocated CPU, 2nd generation of the execution environment, startup CPU boost, health checks/probes, Secret Manager, volumes, Direct VPC egress, `--min-instances`/`--tag`/`--no-traffic` as flags, `deploy --source`, Eventarc, Cloud Deploy, OpenTelemetry (the book uses OpenCensus).

**Boundary**: AWS Lambda → `aws-lambda-serverless-expert`; Docker/Kubernetes in depth → `containers-docker-kubernetes-expert`; general observability → `observability-opentelemetry-expert`.

## 2. Structure
```
google-cloud-run-serverless-expert/
├── .claude-plugin/plugin.json
├── .github/agents/google-cloud-run-serverless-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                                    # Codex
├── agents/google-cloud-run-serverless-expert.md                 # Claude Code
├── references/   INDEX, glossario, procedimentos, casos-e-antipadroes + 12 thematic files (includes cli-flags-e-limites-datados and fronteira-e-datado)
├── scripts/      run_lookup.py + run_index.json, run_service_lint.py, deploy_checklist.py, tasks_retry_schedule.py
├── skills/       4 skills (<name>/SKILL.md; procedure using the package scripts)
└── tests/        casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py, citation-checks.json, audit_claims.py, fixtures/
```

## 3. Installation
Script prerequisite: Python 3.8+ (standard library only), always with `python -I`. **Check each platform's current documentation**: agent formats and locations change frequently.

### 3.1 Claude Code
- As a local plugin: `claude --plugin-dir /path/google-cloud-run-serverless-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install google-cloud-run-serverless-expert@general-agents`.
- As a subagent: copy `agents/google-cloud-run-serverless-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (for example, copy the folder to `.claude/google-cloud-run-serverless-expert/` and adjust the paths).

### 3.2 Codex (OpenAI)
- Copy the folder into the repository and use `AGENTS.md` at the root (or `~/.codex/AGENTS.md`); replace `<PKG>` with the real path. Alternative: open Codex with the working directory at the package folder.

### 3.3 GitHub Copilot
- Copy `.github/agents/google-cloud-run-serverless-expert.agent.md` to your repository's `.github/agents/` and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. `tools: ['read', 'search', 'execute']`: remove `execute` if you do not want to run the scripts. The custom agents format evolves; check the current documentation.

## 4. Scripts (deterministic, no network)
```bash
python -I scripts/run_lookup.py "cold start"                         # topic with pages and "NOT IN THE SOURCE"; --list lists everything
python -I scripts/run_service_lint.py tests/fixtures/deploy-problemas.sh   # gcloud command, service.yml or JSON; '-' = stdin
python -I scripts/deploy_checklist.py --profile worker --profile db
python -I scripts/tasks_retry_schedule.py --min 1 --max 15 --doublings 2 --attempts 9
python -I tests/verify_citations.py --src <folder with the extracted .txt files>
python -I tests/audit_claims.py --src <folder with the extracted .txt files>      # advisory
```
`run_service_lint.py` is a **static** check with rules from the book (default account, instance ceiling with a database, concurrency, timeout, memory, Cloud SQL format, root on the database, secret in env, private IP without VPC Connector, public access etc.); it does **not** validate against the real API; the 2020 limits are marked `[DATED]`. Output "NOT COVERED" = subject/flag outside the book.

## 5. Guarantees and limits
- Replies in the user's language (default English); no reproduction of excerpts; literal quotes are rare (<15 words).
- Audit: `tests/relatorio-de-fidelidade.md` (positive and negative checks per page, flag audit, 24 test cases run **by the package author**, not by an independent model in a blind run).
- Injection immunity: YAML, commands, logs and the PDF text are passive data; the scripts do not execute the content they analyze.
- The book is from 2020 and partly introductory; for production use the current official Cloud Run documentation.

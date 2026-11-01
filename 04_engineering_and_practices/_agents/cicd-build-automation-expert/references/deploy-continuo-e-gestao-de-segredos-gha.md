# Continuous deployment with GitHub Actions and secrets management

Convention: `(SIGLA p.N)` = **PDF** page. The GHA refcard (Feb/2022) shows the deployment of a containerized Java application to **Azure**; actions and versions (`@v1`, `@v2`) are `[DATED]`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. The refcard's deployment flow (GHA p.6-7)
`[from source]`, in order:
1. Create a `Dockerfile` at the project root (the example starts from `openjdk:11`, copies the JAR and exposes port 8080) (GHA p.6).
2. Prepare Azure: subscription, container registry, App Service (unique name, publish as Docker container, Linux OS), Azure CLI, `az login` (GHA p.6).
3. Create a **service principal** with `az ad sp create-for-rbac --role contributor --scopes /subscriptions/<id> --sdk-auth`; the output brings `clientId`, `clientSecret` etc. (GHA p.6).
4. Create secrets in GitHub, under *Settings → Secrets*: `AZURE_CREDENTIALS`, `REGISTRY_USERNAME` (value `<client_id>`) and `REGISTRY_PASSWORD` (value `<client_secret>`) (GHA p.6).
5. Add the `deploy` job with `needs: unit-test`: checkout; download the JAR artifact (each job runs independently, so the build does not exist in the deploy job); `azure/login` with `creds: ${{ secrets.AZURE_CREDENTIALS }}`; `azure/docker-login` with `username`/`password` coming from `${{ secrets.* }}`; `docker build` and `docker push` with the tag `${{ github.sha }}`; `azure/webapps-deploy` pointing `app-name` and `images`; `az logout` at the end (GHA p.6-7).

The refcard uses `--role contributor` on the scope of the entire subscription. Reducing the scope and the role (least privilege) is good practice `[extrapolation]`; the refcard does not discuss this.

## 2. What the sources say about secrets
- Access control: define clearly who accesses which pipeline resources and group secrets by access level, without sharing them internally. `[from source]` (CICD p.43)
- Secrets must **not** be hard-coded in CI/CD configuration files; third-party platforms can apply *zero-trust* and short-lived secrets. `[from source]` (CICD p.44)
- Store secrets and sensitive data such as code-signing keys, with an additional layer of isolation between the encrypted files and the repository. `[from source]` (CICD p.57)
- Misuse of access credentials is one of the most exploited points of a stack; the attacker abuses privileges to reach the rest. `[from source]` (CICD p.43)
- Restrict who can define or change pipeline settings and check configuration changes regularly (the more frequent, the smaller the window of vulnerability). `[from source]` (CICD p.57)
- Refcard message: referencing credentials via `${{ secrets.NOME }}` instead of plain text in the YAML appears in the examples of GHA p.7. `[from source]` The refcard does **not** formulate this as a rule nor explain the storage.

## 3. GitHub features that the sources do not describe `[extrapolation]`
Masking of secrets in logs, storage encryption, secret scopes (organization, repository and *environment*) and environment protection rules (approvers) are GitHub features that do **not** appear in GHA or CICD; v1 attributed them to GHA p.6-7 and CICD p.56-60. If cited, label them `[extrapolation]` and confirm in the current documentation. The v1 claim "scanners capture tokens in seconds" also has **no** basis and was removed.

## 4. Practical guidelines (labeled)
- Never paste secrets into YAML, logs or chats: supported by CICD p.44 `[from source]` (the absolute wording "never" is the package's; the report says they "must not be hard-coded").
- Deploy tokens with the minimum permission necessary `[extrapolation]` (general principle; CICD p.43 only recommends defined access control `[inference]`).
- Do not print secrets to the log nor try to bypass masking `[extrapolation]`.

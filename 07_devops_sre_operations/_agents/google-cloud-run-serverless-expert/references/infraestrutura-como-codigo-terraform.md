# Infrastructure as code with Terraform (RUN ch. 8, p.139-155)

## Why IaC in serverless
- **[from source]** Infrastructure = all the cloud resources needed to recreate the application from scratch (including project, service account, IAM binding). IaC = describe everything in code and use a tool to create, update and delete (RUN p.139-140).
- **[from source]** Benefits: reason by reading code, review by pull request, reproducibility (new project, test environment), tear everything down easily to avoid costs; declarative (desired state) instead of imperative (RUN p.140).
- **[from source]** Even without servers, serverless infrastructure adds up to many details: managed services, Cloud Run services and their configuration, service accounts and IAM, network resources such as the VPC Connector (RUN p.141).
- **[from source]** Three workflows: manual (gcloud/console), automation (e.g., Ansible) and IaC (RUN p.141-142). **When not to use:** one service + database + Redis in a small project may not be worth the effort; in a team with dozens of resources, use it; starting IaC on an existing project is hard (RUN p.142).

## Terraform
- **[from source]** Open source (HashiCorp), declarative language HCL; Google maintains a team on the integration (RUN p.143). **Limitation:** a gradual Cloud Run revision rollout cannot be managed with Terraform (RUN p.143). Install version 0.12 or higher (RUN p.143) **[DATED]**.
- **[from source]** Credentials: use **Application Default Credentials** (`gcloud auth application-default login`), different from those of `gcloud auth login`; do **not** create or download a service account key on the local machine (story of the key leaked on GitHub and used to mine bitcoin) (RUN p.143-144).
- **[from source]** Files: `main.tf` with `provider google { project = var.project_id ... version = "~> 3.0" }` and `variable "project_id"`; `terraform init` downloads the provider (binary plugin in `.terraform`) (RUN p.144-145) **[DATED]** (provider version). Variables are parameters (CLI, environment, `terraform.tfvars` file) (RUN p.146, 149).
- **[from source]** Cloud Run resource: `resource google_cloud_run_service "hello" { name, location, template { spec { containers { image } } } }`. The *local name* serves dependencies; the `name` attribute is the real name in GCP. HCL is not a programming language; resource types come from the provider (not portable across providers); `*.tf` file names do not matter (RUN p.146-148).
- **[from source]** Flow: `terraform plan -out tfplan` (compares the configuration with the state and produces the create/update/delete list), `terraform show tfplan`, `terraform apply tfplan`; `terraform apply` without a plan generates the plan in memory and asks for confirmation (`yes`) (RUN p.148-149, 153). Study the plan before applying; small changes; `prevent_destroy` prevents deleting important resources (RUN p.151-152).
- **[from source]** **State** (`terraform.tfstate`): list of managed resources and attributes; **may contain secrets** (API keys, database passwords, certificates): protect it; `terraform show`, `terraform console` to query it (e.g., service URL) (RUN p.149-150).
- **[from source]** A service newly created by Terraform responds 403 until it gets an access policy. To make it public: `data google_iam_policy` with role `roles/run.invoker` and member `allUsers` + `resource google_cloud_run_service_iam_policy` (service, location, policy_data) (RUN p.150, 152). IAM may take a little while to reflect (RUN p.153).
- **[from source]** Dependencies between resources are expressed by **references** (e.g., `google_cloud_run_service.hello.name`); examples: `google_sql_user` depends on `google_sql_database_instance`; ACL depends on bucket (RUN p.153-154). Support resources: the Google provider documentation and the Cloud Foundation Fabric repository (RUN p.154).

## Rules
1. **[from source]** Credentials via ADC, never a downloaded key (RUN p.143).
2. **[from source]** Always review the plan; treat the state as a secret (RUN p.150-152).
3. **[inference]** Gradual rollout/traffic splitting does not go into Terraform: do it via `gcloud`/console or a separate process, per p.143.
4. **[extrapolation] [DATED]** The provider and the `google_cloud_run_service` resources have evolved (today there is `google_cloud_run_v2_service`); remote state/locking do not appear in the book.

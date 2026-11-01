# DevSecOps and software supply chain security

Convention: `(SIGLA p.N)` = **PDF** page. Sources: security articles of the CICD report (p.42-45 Sengupta; p.56-58 Bera), a continuous packaging advertisement (p.40, sponsor) and the Build chapter of SWE-G (p.269-270, on external dependencies). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Why the pipeline is a target
- The pipeline accesses all the resources of the stack to automate the flow, which makes it more vulnerable to attack vectors that can affect every stage of the lifecycle. `[from source]` (CICD p.42)
- Weak points listed: **trust relationships** between repository and servers (a target for malicious commits on the main branch), **workflow configuration errors**, **microservice vulnerabilities** (larger surface with containers and orchestrators), **authorization vulnerabilities** (credentials) and **poorly written code/poorly administered tests**. `[from source]` (CICD p.42-43)
- Mabl survey cited: of the organizations surveyed, 53% use continuous integration and 38% continuous delivery; security is considered the biggest challenge. `[from source]` (CICD p.42)
- According to another article, security splits into security **of** the pipeline (secure login, secure artifact storage, authentication) and security **in** the pipeline (harder; starts with a risk assessment). `[from source]` (CICD p.56)

## 2. Practices recommended by the sources
- **Shift left**: integrate security measures from the early phases, to find and fix vulnerabilities before deploy. `[from source]` (CICD p.43; also CICD p.22)
- **DevSecOps**: an approach that integrates security into the development and operations stages, related to shift left. `[from source]` (CICD p.43)
- **Access and authorization**: define who accesses what; group secrets by access level. `[from source]` (CICD p.43)
- **Secrets outside configuration files**; short-lived secrets. `[from source]` (CICD p.44)
- **IaC, Security as Code and Policy as Code**: automate security provisioning, auditing and compliance (e.g., SOC2, HIPAA, GDPR) with machine-readable code. `[from source]` (CICD p.44)
- **SAST** (static analysis, "white-box", pre-deployment; examples cited: Fortify, Veracode, Coverity). `[from source]` (CICD p.44)
- **DAST** (tests the running application by simulating an attacker; examples: Netsparker, Tenable.io, HCL AppScan). `[from source]` (CICD p.45)
- **Continuous monitoring** in real time. `[from source]` (CICD p.45)
- Operational problems of security tools: false positives and false negatives (the negatives are more dangerous); mark a false positive with a justification; take every test alert seriously; test the pipeline itself with attempts at misuse. `[from source]` (CICD p.57)
- Configuration errors: a gap in not enabling security features as they appear; restrict who changes the pipeline configuration; review configuration changes frequently. `[from source]` (CICD p.57)
- Test environments: use on-demand cloud environments instead of a poorly configured shared environment. `[from source]` (CICD p.57)

## 3. Supply chain
- A sponsor cites the SolarWinds and CodeCov attacks and *Dependency Confusion* as reasons to control the chain; it proposes "continuous packaging" (storing artifacts, packages and containers in a controlled repository), with **provenance** (signing and verification of packages and checksums) and **isolation** (cache away from public repositories; own SBOM). `[from source]` (CICD p.40) Vendor content (Cloudsmith).
- SWE-G Build chapter (about builds, not GitHub Actions): depending on files outside the workspace is risky; they can change at any time, produce irreproducible builds and, if third-party, are a security risk (an attacker can swap the file). `[from source]` (SWE-G p.269-270)
- Bazel's solution: a manifest with the **cryptographic hash** of each external dependency; the build fails if the downloaded hash differs; updating is a conscious, versioned choice. `[from source]` (SWE-G p.270)
- The book recommends mirroring dependencies on trusted, controlled servers, so as not to depend on the availability of third parties. `[from source]` (SWE-G p.270)

## 4. Pinning of actions and `permissions`: outside the sources
- Pinning third-party actions to the **full commit SHA** (40 hex) instead of `@main`, `@master` or movable tags is current GitHub security practice; it is `[extrapolation]` here. **Neither GHA nor CICD mention** `@main`, `@master`, 40-digit SHA or "pinning" (v1 attributed it to CICD p.44-46 and GHA p.4 and called it "mandatory"). By analogy, SWE-G p.270 argues for pinning external dependencies by hash `[inference]`.
- The workflow's `permissions:` block and the principle of least privilege on the `GITHUB_TOKEN` are also `[extrapolation]`; what the sources say is, in general, "define clear access controls" (CICD p.43) `[from source]`. The GHA source (p.6) shows a service principal with the `contributor` role, the opposite of least privilege `[from source]`.
- SHA values that v1 carried (for example, for `actions/checkout`) were unverified examples; **do not use them**. Obtain the SHA of the official release from the action's repository `[extrapolation]`.

## 5. Note on limits
Tools cited (Fortify, Veracode, Trivy etc.) are examples or `[extrapolation]`; the sources do not recommend any specific tool. Trivy and Clair, cited by v1, **do not appear** in the sources.

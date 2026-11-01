# QRK. Quarkus serverless (Refcard, 9 pp.)

**Identity:** DZone Refcard "Getting Started With Quarkus Serverless Functions", Daniel Oh (Red Hat), © 2021, Red Hat partnership (QRK p.1, 9). Versions in the text: Quarkus 2.x (Maven plugin `2.2.3.Final` in the create command; logs "Quarkus 2.1.4.Final") (QRK p.3, 5). [DATED] 2021. **p.2 is an advertisement** with no content (QRK p.2). This source is **promotional and serverless-specific**; it is not a general Quarkus guide.

## What the text states
- Quarkus takes a "closed-world" approach; about 450 extensions (data, serverless, continuous testing, messaging, security, cloud, process automation); claims to deploy 10 times more native applications on Kubernetes (author's claim/figure 1) (QRK p.1). Cites Spring Boot as an example of a "traditional" framework considered heavy/slow for serverless (QRK p.1) [Refcard claim, not a benchmark].
- **Project creation:** command `mvn io.quarkus:quarkus-maven-plugin:2.2.3.Final:create` with `-DprojectGroupId`, `-DprojectArtifactId`, `-Dextensions="openshift"`, `-DclassName` (QRK p.3).
- **Dev mode:** `./mvnw quarkus:dev` (live coding, no recompiling/redeploying/restarting) (QRK p.3).
- **Continuous testing:** via the CLI and the **DEV UI** (`http://localhost:8080/q/dev/`); they do not start by default (must be enabled in the DEV UI); tests in `src/test/java` (QRK p.3-4).
- **Knative/OpenShift:** six keys in `application.properties` (`quarkus.container-image.group`, `quarkus.container-image.registry`, `quarkus.kubernetes-client.trust-certs`, `quarkus.kubernetes.deployment-target=knative`, `quarkus.kubernetes.deploy=true`, `quarkus.openshift.build-strategy=docker`) and `./mvnw clean package -DskipTests` to build and deploy (QRK p.4). The pod scales to zero (default cited: 30 s) (QRK p.5).
- **GraalVM/Mandrel:** `native` profile with `quarkus.package.type=native`; `./mvnw package -Pnative -Dquarkus.native.container-build=true` (Docker) or with `-Dquarkus.native.container-runtime=podman`; Mandrel for OpenJDK 11 (QRK p.5). Author's measurement: JVM 5.984 s vs native 0.013 s (13 ms; "48 times"); the text warns that it varies by environment (QRK p.5) [DATED, not a benchmark].
- **Figure 7 (QRK p.6; cited in the text of p.5), checked visually by rendering** (the extracted text does not capture it): RSS memory of a REST app, native Quarkus 12 MB, Quarkus JVM 73 MB, "traditional cloud-native stack" 136 MB; boot time + first response, 0.016 s, 0.943 s and 4.3 s respectively. It is vendor material, with no methodology described [DATED, 2021].
- **Funqy:** extension `quarkus-funqy-http` (`quarkus:add-extension`); `@Funq` exposes the method as a function (default name = method name) (QRK p.6). For AWS Lambda: remove `funqy-http` and `quarkus-openshift`, add `quarkus-funqy-amazon-lambda`, `@Funq("awsfunction")`, `quarkus.funqy.export=awsfunction` (QRK p.6-7); generates `function.zip`, `manage.sh`, `sam.jvm.yaml`, `sam.native.yaml`; create/delete via `LAMBDA_ROLE_ARN=... sh target/manage.sh create|delete` (QRK p.7).
- **CloudEvents/Knative:** `quarkus-funqy-knative-events` + `quarkus-openshift`; function `@Funq("lowercase")` with `@Context CloudEvent<Input>`; `quarkus.funqy.export=lowercase`; test with `curl` and headers `Ce-Id`, `Ce-Source`, `Ce-Type` (QRK p.8).
- The conclusion cites live coding, continuous testing, DEV UI and DevServices (QRK p.8); DevServices is **not explained** in the text.

## NOT COVERED (in this source)
Classic REST (only the `GreetingResource`/"Hello RESTEasy" example, QRK p.3), dependency injection (CDI), Panache/Hibernate, configuration, security, metrics, native in depth, Quarkus 3.x, technical comparison with Spring Boot.

## Stance
When comparing with Spring Boot, present the Refcard sentence as a **vendor claim** (Red Hat) from 2021 and say that SB3G (2024) does not compare the two frameworks (SB3G mentions GraalVM in SB3G p.31).

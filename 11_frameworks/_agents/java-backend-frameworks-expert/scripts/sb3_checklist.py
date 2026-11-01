# -*- coding: utf-8 -*-
"""
sb3_checklist.py - Spring Boot 3 project checklist based on the items of the book
"Mastering Spring Boot 3.0" (Ahmet Meric, Packt, 2024; abbreviation SB3G; pages = PDF).

Does NOT run the project, does NOT access the network: it only READS text files in the given directory (build.gradle, pom.xml,
application*.properties/yml, *.java, Kubernetes *.yaml, docker-compose) and looks for textual markers.

Each item cites the page of the book where it appears. DETECTION is heuristic (regex); where the identifier searched for
is not in the book, the item is flagged "[extrapolation] marker". A missing marker != an error: the book does not
require every project to have every item ("the book does not define which items are mandatory").

Usage:
  python -I scripts/sb3_checklist.py list [--secao SECAO]
  python -I scripts/sb3_checklist.py scan DIR [--secoes dados,seguranca,...] [--json]
Sections: base, dados, seguranca, testes, container, observabilidade, mensageria, produtividade
Exit 0 whenever the read happens; 2 for incorrect usage.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# kind: "item" (expected if the section applies) | "alert" (reported when FOUND)
# marcador_origem: "source" (identifier appears in the book on the cited page) | "extrapolation"
ITENS = [
    # base
    {"id": "base-java17", "secao": "base", "tipo": "item",
     "texto": "Java 17 as the project version (Spring Boot 3.0 baseline according to the book; the book uses JDK 17 in the examples)",
     "paginas": [30, 15], "marcador_origem": "extrapolation",
     "regex": r"VERSION_17|sourceCompatibility\s*=\s*['\"]?17|<java\.version>\s*17|JavaLanguageVersion\.of\(\s*17\s*\)|<release>\s*17|maven\.compiler\.(source|target|release)>\s*17"},
    {"id": "base-boot3", "secao": "base", "tipo": "item",
     "texto": "Spring Boot 3.x declared (the book uses 3.2.5 and 3.2.1)",
     "paginas": [81, 188], "marcador_origem": "extrapolation",
     "regex": r"org\.springframework\.boot['\"]\s*version\s*['\"]3\.|spring-boot-starter-parent</artifactId>\s*<version>\s*3\.|spring-boot-gradle-plugin:3\."},
    # data
    {"id": "dados-jpa", "secao": "dados", "tipo": "item",
     "texto": "Spring Data JPA starter", "paginas": [103], "marcador_origem": "source",
     "regex": r"spring-boot-starter-data-jpa"},
    {"id": "dados-datasource", "secao": "dados", "tipo": "item",
     "texto": "Datasource properties (spring.datasource.url)", "paginas": [106], "marcador_origem": "source",
     "regex": r"spring\.datasource\.url"},
    {"id": "dados-mongo", "secao": "dados", "tipo": "item",
     "texto": "MongoDB: spring.data.mongodb.uri", "paginas": [113], "marcador_origem": "source",
     "regex": r"spring\.data\.mongodb\.uri"},
    {"id": "dados-r2dbc", "secao": "dados", "tipo": "item",
     "texto": "R2DBC (reactive stack): spring.r2dbc.url", "paginas": [83], "marcador_origem": "source",
     "regex": r"spring\.r2dbc\.url"},
    {"id": "dados-cache", "secao": "dados", "tipo": "item",
     "texto": "Cache: spring-boot-starter-cache and @EnableCaching", "paginas": [117], "marcador_origem": "source",
     "regex": r"spring-boot-starter-cache|@EnableCaching"},
    {"id": "dados-batch", "secao": "dados", "tipo": "item",
     "texto": "Spring Batch: spring-boot-starter-batch", "paginas": [120], "marcador_origem": "source",
     "regex": r"spring-boot-starter-batch"},
    {"id": "dados-liquibase", "secao": "dados", "tipo": "item",
     "texto": "Migration with Liquibase: liquibase-core and spring.liquibase.change-log", "paginas": [125], "marcador_origem": "source",
     "regex": r"liquibase-core|spring\.liquibase\.change-log"},
    {"id": "dados-ddl-update", "secao": "dados", "tipo": "alert",
     "texto": "ddl-auto=update: used in the book's example (p.106); the book presents Liquibase as a way to evolve the schema (p.125-127) [inference: consider versioned migration instead of update]",
     "paginas": [106, 125, 127], "marcador_origem": "source",
     "regex": r"spring\.jpa\.hibernate\.ddl-auto\s*[=:]\s*update"},
    # security
    {"id": "seg-starter", "secao": "seguranca", "tipo": "item",
     "texto": "Security starter (spring-boot-starter-security)", "paginas": [133], "marcador_origem": "source",
     "regex": r"spring-boot-starter-security"},
    {"id": "seg-filterchain", "secao": "seguranca", "tipo": "item",
     "texto": "SecurityFilterChain / SecurityWebFilterChain defined", "paginas": [133, 155], "marcador_origem": "source",
     "regex": r"SecurityFilterChain|SecurityWebFilterChain"},
    {"id": "seg-resource-server", "secao": "seguranca", "tipo": "item",
     "texto": "OAuth2 resource server (starter and issuer-uri)", "paginas": [141, 143], "marcador_origem": "source",
     "regex": r"spring-boot-starter-oauth2-resource-server|resourceserver\.jwt\.issuer-uri"},
    {"id": "seg-rbac", "secao": "seguranca", "tipo": "item",
     "texto": "RBAC with hasAuthority/hasAnyAuthority and the ROLE_ prefix", "paginas": [151], "marcador_origem": "source",
     "regex": r"hasAuthority|hasAnyAuthority"},
    {"id": "seg-csrf-off", "secao": "seguranca", "tipo": "alert",
     "texto": "CSRF disabled: the book only justifies it for APIs consumed by other applications, not by browsers (p.134)",
     "paginas": [134], "marcador_origem": "source",
     "regex": r"csrf\(\s*AbstractHttpConfigurer::disable|CsrfSpec::disable|csrf\(\)\.disable"},
    {"id": "seg-password-grant", "secao": "seguranca", "tipo": "alert",
     "texto": "grant_type=password: this is the flow used in the book's example (p.145); [extrapolation] it is discouraged in current OAuth2, and the book does not discuss it",
     "paginas": [145], "marcador_origem": "source",
     "regex": r"[\"']grant_type[\"']\s*,\s*[\"']password[\"']"},
    # tests
    {"id": "teste-mockito", "secao": "testes", "tipo": "item",
     "texto": "Mockito (@Mock/@InjectMocks/MockitoExtension)", "paginas": [162, 165, 166], "marcador_origem": "source",
     "regex": r"MockitoExtension|@InjectMocks|org\.mockito"},
    {"id": "teste-webmvc", "secao": "testes", "tipo": "item",
     "texto": "Controller test with @WebMvcTest / MockMvc", "paginas": [167, 169], "marcador_origem": "source",
     "regex": r"@WebMvcTest|MockMvc"},
    {"id": "teste-security", "secao": "testes", "tipo": "item",
     "texto": "@WithMockUser in tests with security", "paginas": [167], "marcador_origem": "source",
     "regex": r"@WithMockUser"},
    {"id": "teste-testcontainers", "secao": "testes", "tipo": "item",
     "texto": "Testcontainers (+ @DynamicPropertySource)", "paginas": [174, 175], "marcador_origem": "source",
     "regex": r"(?i)testcontainers|@DynamicPropertySource"},
    {"id": "teste-wiremock", "secao": "testes", "tipo": "item",
     "texto": "WireMock to simulate an external/OIDC provider", "paginas": [176], "marcador_origem": "source",
     "regex": r"(?i)wiremock"},
    {"id": "teste-webtestclient", "secao": "testes", "tipo": "item",
     "texto": "WebTestClient/@WebFluxTest (stack reativa)", "paginas": [179], "marcador_origem": "source",
     "regex": r"WebTestClient|@WebFluxTest"},
    # container
    {"id": "cont-bootbuildimage", "secao": "container", "tipo": "item",
     "texto": "Image via Cloud Native Buildpacks (bootBuildImage)", "paginas": [190], "marcador_origem": "source",
     "regex": r"bootBuildImage|spring-boot:build-image"},
    {"id": "cont-graceful", "secao": "container", "tipo": "item",
     "texto": "Graceful shutdown (server.shutdown=graceful)", "paginas": [191], "marcador_origem": "source",
     "regex": r"server\.shutdown\s*[=:]\s*graceful"},
    {"id": "cont-timeout-shutdown", "secao": "container", "tipo": "item",
     "texto": "spring.lifecycle.timeout-per-shutdown-phase", "paginas": [191], "marcador_origem": "source",
     "regex": r"spring\.lifecycle\.timeout-per-shutdown-phase"},
    {"id": "cont-probes-props", "secao": "container", "tipo": "item",
     "texto": "Liveness/readiness health groups (livenessState/readinessState)", "paginas": [192], "marcador_origem": "source",
     "regex": r"livenessState|readinessState"},
    {"id": "cont-probes-k8s", "secao": "container", "tipo": "item",
     "texto": "Probes in the Deployment pointing to /actuator/health/liveness and /readiness", "paginas": [193], "marcador_origem": "source",
     "regex": r"/actuator/health/(liveness|readiness)"},
    {"id": "cont-configmap-secret", "secao": "container", "tipo": "item",
     "texto": "ConfigMap/Secret injected as environment variables", "paginas": [196, 197], "marcador_origem": "source",
     "regex": r"configMapKeyRef|secretKeyRef"},
    {"id": "cont-profile", "secao": "container", "tipo": "item",
     "texto": "SPRING_PROFILES_ACTIVE set in the deployment", "paginas": [199], "marcador_origem": "source",
     "regex": r"SPRING_PROFILES_ACTIVE"},
    {"id": "cont-latest", "secao": "container", "tipo": "alert",
     "texto": "Image with the :latest tag: the book suggests switching to a specific version for consistent environments (p.194)",
     "paginas": [194], "marcador_origem": "source",
     "regex": r"image:\s*\S+:latest\b"},
    # observability
    {"id": "obs-actuator", "secao": "observabilidade", "tipo": "item",
     "texto": "Spring Boot Actuator", "paginas": [192], "marcador_origem": "source",
     "regex": r"spring-boot-starter-actuator"},
    {"id": "obs-prometheus", "secao": "observabilidade", "tipo": "item",
     "texto": "Micrometer Prometheus registry", "paginas": [201], "marcador_origem": "source",
     "regex": r"micrometer-registry-prometheus"},
    {"id": "obs-exposure", "secao": "observabilidade", "tipo": "item",
     "texto": "management.endpoints.web.exposure.include with prometheus", "paginas": [201], "marcador_origem": "source",
     "regex": r"management\.endpoints\.web\.exposure\.include\s*[=:].*prometheus"},
    # messaging
    {"id": "msg-bootstrap", "secao": "mensageria", "tipo": "item",
     "texto": "spring.kafka.bootstrap-servers", "paginas": [218], "marcador_origem": "source",
     "regex": r"spring\.kafka\.bootstrap-servers"},
    {"id": "msg-listener", "secao": "mensageria", "tipo": "item",
     "texto": "@KafkaListener (consumer)", "paginas": [219], "marcador_origem": "source",
     "regex": r"@KafkaListener"},
    {"id": "msg-template", "secao": "mensageria", "tipo": "item",
     "texto": "KafkaTemplate (producer)", "paginas": [217], "marcador_origem": "source",
     "regex": r"KafkaTemplate"},
    # productivity
    {"id": "prod-aop", "secao": "produtividade", "tipo": "item",
     "texto": "AOP: spring-boot-starter-aop and @Aspect", "paginas": [212], "marcador_origem": "source",
     "regex": r"spring-boot-starter-aop|@Aspect"},
    {"id": "prod-feign", "secao": "produtividade", "tipo": "item",
     "texto": "Feign: spring-cloud-starter-openfeign and @EnableFeignClients", "paginas": [234], "marcador_origem": "source",
     "regex": r"spring-cloud-starter-openfeign|@EnableFeignClients"},
    {"id": "prod-conditional", "secao": "produtividade", "tipo": "item",
     "texto": "Use of @Conditional* to turn components on/off", "paginas": [237], "marcador_origem": "source",
     "regex": r"@ConditionalOn(Property|Class|Expression|MissingBean)"},
]

SECOES = ["base", "dados", "seguranca", "testes", "container", "observabilidade", "mensageria", "produtividade"]
EXT = (".gradle", ".kts", ".xml", ".properties", ".yml", ".yaml", ".java", ".kt", ".sh", ".env")
NAMES = ("Dockerfile", "docker-compose.yml", "docker-compose.yaml")
SKIP_DIRS = {".git", "node_modules", "build", "target", ".gradle", ".idea", "out", "__pycache__"}
MAX_BYTES = 1_500_000


def pg(p):
    return ",".join(str(x) for x in p)


def cmd_list(secao):
    for it in ITENS:
        if secao and it["secao"] != secao:
            continue
        tag = "ALERT " if it["tipo"] == "alert" else "ITEM  "
        print(f"[{it['secao']}] {tag} {it['id']}: {it['texto']}  [from source: SB3G p.{pg(it['paginas'])}]"
              + ("" if it["marcador_origem"] == "source" else "  ([extrapolation] marker)"))


def read_tree(root):
    blobs = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.endswith(EXT) or f in NAMES:
                fp = os.path.join(dp, f)
                try:
                    if os.path.getsize(fp) > MAX_BYTES:
                        continue
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        blobs.append((os.path.relpath(fp, root), fh.read()))
                except OSError:
                    continue
    return blobs


def cmd_scan(root, secoes, as_json):
    if not os.path.isdir(root):
        print(f"Directory does not exist: {root}", file=sys.stderr)
        return 2
    blobs = read_tree(root)
    res = []
    for it in ITENS:
        if secoes and it["secao"] not in secoes:
            continue
        rx = re.compile(it["regex"], re.S)
        hit = None
        for rel, txt in blobs:
            if rx.search(txt):
                hit = rel
                break
        res.append({"id": it["id"], "secao": it["secao"], "tipo": it["tipo"], "texto": it["texto"],
                    "paginas": it["paginas"], "origem_marcador": it["marcador_origem"],
                    "encontrado": bool(hit), "arquivo": hit})
    if as_json:
        print(json.dumps({"arquivos_lidos": len(blobs), "resultados": res}, ensure_ascii=False, indent=1))
        return 0
    print(f"Text files read: {len(blobs)} (nothing was executed; static read).")
    if not blobs:
        print("No relevant file found: nothing to evaluate.")
        return 0
    for sec in SECOES:
        rows = [r for r in res if r["secao"] == sec]
        if not rows:
            continue
        print(f"\n== {sec} ==")
        for r in rows:
            src = "" if r["origem_marcador"] == "source" else " ([extrapolation] marker)"
            cite = f"[from source: SB3G p.{pg(r['paginas'])}]"
            if r["tipo"] == "alert":
                if r["encontrado"]:
                    print(f"  ALERT {r['id']}: {r['texto']} {cite}  (in {r['arquivo']})")
            else:
                st = "PRESENT " if r["encontrado"] else "ABSENT  "
                print(f"  {st} {r['id']}: {r['texto']} {cite}{src}" + (f"  (in {r['arquivo']})" if r["arquivo"] else ""))
    print("\nNote: the book does not define which items are mandatory; ABSENT only means the textual marker was not found.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Spring Boot 3 project checklist (SB3G items)")
    sub = ap.add_subparsers(dest="cmd")
    pl = sub.add_parser("list")
    pl.add_argument("--secao", choices=SECOES)
    ps = sub.add_parser("scan")
    ps.add_argument("dir")
    ps.add_argument("--secoes", default="")
    ps.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.cmd == "list":
        cmd_list(a.secao)
        return 0
    if a.cmd == "scan":
        secs = [s.strip() for s in a.secoes.split(",") if s.strip()]
        bad = [s for s in secs if s not in SECOES]
        if bad:
            print("Invalid section:", ",".join(bad), "; valid:", ",".join(SECOES), file=sys.stderr)
            return 2
        return cmd_scan(a.dir, secs, a.json)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

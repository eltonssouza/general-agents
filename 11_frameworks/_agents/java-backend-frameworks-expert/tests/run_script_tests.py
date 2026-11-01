# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests of the package scripts (no model, no network, without running the framework).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]   # --src enables verify_citations.py
Exit 0 if all pass. Conceptual cases (which require the agent) are in tests/casos-de-teste.md.
The expected values come from the text of the sources themselves (pages cited in each test).
"""
import argparse
import json
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL, OK = [], []
FX = os.path.join("tests", "fixtures")
L = os.path.join("scripts", "fw_lookup.py")
K = os.path.join("scripts", "sb3_checklist.py")
M = os.path.join("scripts", "mapstruct_tool.py")
C = os.path.join("scripts", "compare_approaches.py")


def run(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def has(out, *subs):
    return all(s in out for s in subs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()

    # ---------------- fw_lookup
    rc, o = run([L, "backpressure"])
    check("lookup backpressure -> SB3G p.91-96", rc == 0 and "SB3G p.91-96" in o, o)
    rc, o = run([L, "componentModel", "--source", "MPS"])
    check("lookup componentModel -> MPS p.8,31", "MPS p.8,31" in o, o)
    rc, o = run([L, "kotlin"])
    check("lookup kotlin -> NOT COVERED (MapStruct)", "NOT COVERED" in o, o)
    rc, o = run([L, "custom starter"])
    check("lookup custom starter -> NOT COVERED (SB3G promises and does not implement)", has(o, "NOT COVERED", "promised"), o)
    rc, o = run([L, "panache"])
    check("lookup panache -> NOT COVERED (Quarkus beyond serverless)", "NOT COVERED" in o, o)
    rc, o = run([L, "kubernetes", "--source", "SB3G"])
    check("lookup kubernetes -> SB3G p.191-199", "SB3G p.191-199" in o, o)
    rc, o = run([L, "funqy", "--source", "QRK"])
    check("lookup funqy QRK -> p.6", "QRK p.6" in o, o)
    rc, o = run([L, "xyzzy"])
    check("lookup nonexistent term -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "--page", "9", "--source", "QRK"])
    check("lookup QRK p.9 indexed (bio/resources)", rc == 0 and "QRK p.1,9" in o, o)
    rc, o = run([L, "--page", "2", "--source", "QRK"])
    check("lookup QRK p.2 -> promotional", "promotional" in o, o)
    rc, o = run([L, "--page", "99", "--source", "SB3G"])
    check("lookup SB3G page 99 -> blank", "blank" in o, o)
    rc, o = run([L, "--page", "300", "--source", "SB3G"])
    check("lookup SB3G page 300 -> error", rc == 1, o)
    rc, o = run([L, "--page", "5"])
    check("lookup --page without --source -> error 2", rc == 2, o)
    rc, o = run([L, "--gaps"])
    check("lookup --gaps lists Kotlin, Optional and starter", has(o, "Kotlin", "Optional", "starter"), o)
    rc, o = run([L, "--sources"])
    check("lookup --sources identifies author and version", has(o, "Ahmet Meric", "Daniel Oh", "1.6.3"), o)
    rc, o = run([L, "mappingtarget", "--json"])
    try:
        j = json.loads(o)
        check("lookup --json valid", len(j["achados"]) >= 1)
    except Exception as ex:
        check("lookup --json valid", False, str(ex))

    # ---------------- sb3_checklist
    rc, o = run([K, "list", "--secao", "seguranca"])
    check("checklist list seguranca cites p.133 and p.145", has(o, "SB3G p.133", "SB3G p.145"), o)
    rc, o = run([K, "scan", os.path.join(FX, "proj-ok"), "--json"])
    j = json.loads(o)
    d = {r["id"]: r for r in j["resultados"]}
    check("scan: Java 17 and Boot 3 detected", d["base-java17"]["encontrado"] and d["base-boot3"]["encontrado"], o)
    check("scan: JPA, Liquibase, Actuator, Prometheus present", all(d[i]["encontrado"] for i in ("dados-jpa", "dados-liquibase", "obs-actuator", "obs-prometheus")), o)
    check("scan: absences (Kafka, Feign, Mongo)", not any(d[i]["encontrado"] for i in ("msg-listener", "prod-feign", "dados-mongo")), o)
    check("scan: alerts ddl-update, csrf-off and :latest", all(d[i]["encontrado"] for i in ("dados-ddl-update", "seg-csrf-off", "cont-latest")), o)
    check("scan: no password grant in the fixture", not d["seg-password-grant"]["encontrado"], o)
    rc, o = run([K, "scan", os.path.join(FX, "proj-ok")])
    check("scan text: declares static read and that the book does not define which items are mandatory", has(o, "static read", "does not define which items are mandatory"), o)
    rc, o = run([K, "scan", os.path.join(FX, "proj-vazio")])
    check("scan directory without relevant files", "nothing to evaluate" in o, o)
    rc, o = run([K, "scan", "diretorio-que-nao-existe"])
    check("scan nonexistent directory -> error 2", rc == 2, o)
    rc, o = run([K, "scan", os.path.join(FX, "proj-ok"), "--secoes", "foo"])
    check("scan invalid section -> error 2", rc == 2, o)

    # ---------------- mapstruct_tool
    rc, o = run([M, "generate", os.path.join(FX, "spec-exemplo.json")])
    check("generate: @Mapper with componentModel spring and CONSTRUCTOR", rc == 0 and has(o, '@Mapper(componentModel = "spring"', "InjectionStrategy.CONSTRUCTOR", "ReportingPolicy.ERROR"), o)
    check("generate: @Mapping, inverse and @MappingTarget", has(o, '@Mapping(target = "manufacturer", source = "make")', '@InheritInverseConfiguration(name = "carToCarDto")', "@MappingTarget Car car"), o)
    check("generate: warns that nothing was compiled and imports are [inference]", has(o, "Nothing was compiled", "[inference]"), o)
    rc, o = run([M, "generate", os.path.join(FX, "spec-ruim.json")])
    check("generate bad spec: aborts with rc 1", rc == 1 and "Generation aborted" in o, o)
    check("generate bad spec: invalid componentModel (p.8)", "componentModel 'guice'" in o and "MPS p.8" in o, o)
    check("generate bad spec: constant+source (p.64)", "constant cannot have source" in o and "MPS p.64" in o, o)
    check("generate bad spec: several @MappingTarget (p.20)", "only one @MappingTarget" in o, o)
    check("generate bad spec: ANY_REMAINING/ANY_UNMAPPED (p.54), THROW_EXCEPTION (p.55) and String (p.57)",
          has(o, "MPS p.54", "MPS p.55", "MPS p.57"), o)
    check("generate bad spec: undocumented attribute labeled [inference]", "foo" in o and "[inference" in o, o)
    rc, o = run([M, "validate", os.path.join(FX, "MapperOk.java")])
    check("validate MapperOk: no findings (MPS examples)", rc == 0 and "No findings" in o, o)
    rc, o = run([M, "validate", os.path.join(FX, "MapperRuim.java"), "--json"])
    f = json.loads(o)
    erros = [x["mensagem"] for x in f if x["severidade"] == "ERROR"]
    check("validate MapperRuim: rc 1 and >= 6 errors", rc == 1 and len(erros) >= 6, o)
    check("validate MapperRuim: constant+source", any("constant cannot" in e for e in erros), o)
    check("validate MapperRuim: expression without java(...)", any("java(...)" in e for e in erros), o)
    check("validate MapperRuim: several source parameters", any("several source parameters" in e for e in erros), o)
    check("validate MapperRuim: dois @MappingTarget", any("@MappingTarget" in e for e in erros), o)
    check("validate MapperRuim: THROW_EXCEPTION em source", any("THROW_EXCEPTION" in e for e in erros), o)
    check("validate MapperRuim: qualifier RUNTIME", any("RUNTIME" in e for e in erros), o)
    avisos = [x["mensagem"] for x in f if x["severidade"] == "WARNING"]
    check("validate MapperRuim: warnings for componentModel/undocumented attribute/abstract constructor",
          any("guice" in e for e in avisos) and any("foo" in e for e in avisos) and any("abstract classes" in e for e in avisos), o)
    check("validate: each finding carries its origin", all(x["origem"] in ("from source", "inference") for x in f), o)
    rc, o = run([M, "validate", os.path.join(FX, "MapperInjecao.java"), "--json"])
    f = json.loads(o)
    check("validate with injection text in comments: ignores commands and still reports constant+source",
          rc == 1 and any("constant" in x["mensagem"] for x in f) and len(f) == 1, o)
    rc, o = run([M, "attrs", "Mapper"])
    check("attrs Mapper lista componentModel p.8 e uses p.40", has(o, "componentModel (MPS p.8)", "uses (MPS p.40)"), o)
    rc, o = run([M, "attrs", "Inexistente"])
    check("attrs unknown annotation -> NOT COVERED", "NOT COVERED" in o or "is not in the package table" in o, o)
    rc, o = run([M, "example"])
    try:
        check("example is valid JSON", isinstance(json.loads(o), dict))
    except Exception as ex:
        check("example is valid JSON", False, str(ex))
    rc, o = run([M, "validate", "arquivo-inexistente.java"])
    check("validate nonexistent file -> error 2", rc == 2, o)

    # ---------------- compare_approaches
    rc, o = run([C, "list"])
    check("compare list has >= 15 comparisons", len([l for l in o.splitlines() if ":" in l]) >= 15, o)
    rc, o = run([C, "compare", "spring-vs-quarkus"])
    check("compare spring-vs-quarkus: separates the vendor claim and states what the text does not say",
          has(o, "Red Hat vendor", "QRK p.1", "SB3G p.31", "What the text does NOT say", "neutral benchmark"), o)
    check("compare spring-vs-quarkus includes the checked figure 7", "Figure 7" in o and "QRK p.6" in o, o)
    rc, o = run([C, "compare", "injecao-mapper"])
    check("compare injecao-mapper: constructor recommended p.32", has(o, "MPS p.32", "tests"), o)
    rc, o = run([C, "compare", "nao-existe"])
    check("compare nonexistent -> NOT COVERED", rc == 1 and "NOT COVERED" in o, o)
    rc, o = run([C, "find", "quarkus"])
    check("compare find quarkus", "spring-vs-quarkus" in o, o)
    rc, o = run([C, "compare", "evolucao-esquema"])
    check("compare evolucao-esquema: labels [inference]", "[inference]" in o, o)

    # ---------------- package consistency
    idx = json.load(open(os.path.join(PKG, "scripts", "fw_index.json"), encoding="utf-8"))
    mx = idx["meta"]["paginas_max"]
    check("index: pages within limits", all(1 <= p <= mx[t["fonte"]] for t in idx["topicos"] for p in t["paginas"]))
    check("index: reference files exist", all(os.path.exists(os.path.join(PKG, "references", t["ref"])) for t in idx["topicos"]))
    check("index: >= 60 topics and 3 sources", len(idx["topicos"]) >= 60 and {t["fonte"] for t in idx["topicos"]} == {"SB3G", "QRK", "MPS"})
    cmp_ = json.load(open(os.path.join(PKG, "scripts", "compare_data.json"), encoding="utf-8"))["comparacoes"]
    ok = all(1 <= p <= mx[f] for c in cmp_ for pts in c["abordagens"].values() for _, f, pgs in pts for p in pgs)
    check("compare_data: pages within limits", ok)

    # ---------------- citations
    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations without failures", rc == 0, o[-800:])
        print(o.strip().splitlines()[-1])

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

# java-backend-frameworks-expert

Specialist agent for **Java back-end** built on **three sources of different nature**:

| Abbreviation | What it is | Pages | Date/version |
|---|---|---|---|
| **SB3G** | Book *Mastering Spring Boot 3.0*, Ahmet Meric, Packt Publishing (ISBN 978-1-80323-078-8). **Not a compilation of articles**; "JavaCodeGeeks" in the file name is only its origin. | 256 | July/2024; code with Spring Boot 3.2.x, JDK 17, Gradle 8.7 |
| **QRK** | DZone Refcard *Getting Started With Quarkus Serverless Functions*, Daniel Oh (Red Hat); promotional material; serverless only; p.2 is an ad. | 9 | 2021; Quarkus 2.x |
| **MPS** | *MapStruct 1.6.3 Reference Guide* (official reference). | 96 | 2024-11-09; MapStruct 1.6.3 |

The agent is **proportional** to the sources: where they do not cover a topic (extensive official Spring Boot, Quarkus beyond serverless, MapStruct with Kotlin/Optional/records, custom starters, neutral benchmarks), it answers **NOT COVERED** or uses a labeled `[extrapolation]`. The extensive Spring Boot reference belongs to another agent (**spring-boot-reference-expert**).

## Page convention
**PDF** pages (`SB3G p.N`, `QRK p.N`, `MPS p.N`). SB3G: printed number = PDF - 19 in the chapters; QRK: printed = PDF; MPS: PDF only. Map in `references/INDEX.md`.

## What was read (precise statement)
- **SB3G:** p.2-243 read in full in sequential blocks (prose and code); p.244-251 (back-of-book index) only sampled; p.252-256 ads. **MPS** and **QRK:** read in full. No code was run.
- **Checked visually (render):** only **QRK figure 7 (p.6)**. The other figures (SB3G diagrams, Keycloak/Grafana/CMAK screenshots, QRK figures) have no extractable text and were **not** inspected.
- Intermediate notes: `scratch/frameworks/java-backend-frameworks-expert/notes/`.
- Validation: it was **not** done by an independent "blind" model; the tests were run by the package author itself (see `tests/relatorio-de-fidelidade.md`).

## Structure

```
java-backend-frameworks-expert/
├── .claude-plugin/plugin.json
├── agents/java-backend-frameworks-expert.md      # canonical prompt + frontmatter
├── AGENTS.md                                     # Codex adapter
├── .github/agents/java-backend-frameworks-expert.agent.md   # GitHub Copilot adapter
├── references/
│   ├── INDEX.md (sources, page convention, map)
│   ├── 00-fontes-e-lacunas.md (gaps and internal divergences)
│   ├── sb3g-01 ... sb3g-09 (one per chapter/topic of the book)
│   ├── qrk-quarkus-serverless.md
│   ├── mps-01 ... mps-06 (MapStruct guide)
│   └── glossario.md, procedimentos.md (P1-P8), casos-e-antipadroes.md, datado.md
├── scripts/                                      # Python 3, stdlib, no network; never run the framework
│   ├── fw_lookup.py + fw_index.json              # search across the 3 sources; NOT COVERED
│   ├── sb3_checklist.py                          # Spring Boot 3 project checklist (static read)
│   ├── mapstruct_tool.py                         # @Mapper generator/validator (only what the MPS documents)
│   └── compare_approaches.py + compare_data.json # comparator according to the text
├── skills/       fw-topic-lookup, sb3-project-checklist, mapstruct-mapper-tool, framework-approach-compare   # one SKILL.md per entry (skills/<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md (30 cases), relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json (177 positive, 28 negative)
    ├── run_script_tests.py
    └── fixtures/
```
A copy of the tests is also in `../../_agents_tests/java-backend-frameworks-expert/`.

## Installation
**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- Local plugin: `claude --plugin-dir <path>/java-backend-frameworks-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install java-backend-frameworks-expert@general-agents`.
- Standalone agent: copy `agents/java-backend-frameworks-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting the paths in the prompt.
- Usage: `@java-backend-frameworks-expert validate this MapStruct mapper` or `@java-backend-frameworks-expert how does the book configure probes in Kubernetes?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root; `AGENTS.md` points to the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/java-backend-frameworks-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>`).

## Using the scripts (from the package root)
```bash
python -I scripts/fw_lookup.py backpressure
python -I scripts/fw_lookup.py componentModel --source MPS
python -I scripts/fw_lookup.py kotlin                              # NOT COVERED
python -I scripts/fw_lookup.py --page 6 --source QRK
python -I scripts/sb3_checklist.py list --secao seguranca
python -I scripts/sb3_checklist.py scan PATH/TO/PROJECT
python -I scripts/mapstruct_tool.py example > spec.json
python -I scripts/mapstruct_tool.py generate spec.json
python -I scripts/mapstruct_tool.py validate src/main/java/.../CarMapper.java
python -I scripts/compare_approaches.py compare spring-vs-quarkus
```
The scripts **do not run** Spring Boot, Quarkus or MapStruct, do not compile Java and do not access the network. `mapstruct_tool.py validate` is a **heuristic textual linter**: ERROR only for explicit contradictions of the guide; WARNING for what the guide does not document (it may exist in the real MapStruct). Generated code **was not compiled**.

## Tests
```bash
python -I tests/run_script_tests.py --src ../../../scratch/frameworks   # scripts + citations
python -I tests/verify_citations.py --src ../../../scratch/frameworks
```
`tests/casos-de-teste.md` has 30 cases (conceptual, practical, borderline, out of scope, injection) run manually against agent + references + scripts.

## Notices
1. Sources from **2021 to 2024** [DATED]; the agent does not know later versions.
2. SB3G has didactic prose, internal divergences and example credentials; QRK is vendor material.
3. It does not replace technical review, tests or the current official documentation of each project.

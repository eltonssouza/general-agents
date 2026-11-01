# containers-docker-kubernetes-expert (Claude Code, Codex and GitHub Copilot)

Containers and Docker specialist agent, grounded in:
- **[DOCKHB]** *The Docker Handbook – Learn Docker for Beginners*, Farhan Hasin Chowdhury, freeCodeCamp, 1 Feb 2021, **148 pages** (`Docker-Handbook-freeCodeCamp.pdf`). Old edition: commands and versions marked **[DATED]**.
- **[K8SB]** *Learn Kubernetes Basics* (kubernetes.io), **only 2 pages**: the tutorial index page (objectives and six modules). The agent asserts only what it says.

Rights belong to the authors; this package contains its own syntheses and references, not the text of the works. The PDFs are not distributed here.

## WARNING: unusable Twelve-Factor source
The `Twelve-Factor-App.pdf` file in the source folder has 12 pages that show only **"Page not found"** (an error capture, no content). It **was not used** and Twelve-Factor **is not cited as a source**. The agent treats any 12-factor subject only as a flagged **[extrapolation]**. **Pending: re-obtain a valid source** (e.g. the 12factor.net site saved as PDF/HTML) and regenerate the package to promote items to [from source].

## 1. What the agent does
Containerization; container vs VM; image, layers and registry; Docker architecture; container commands; Dockerfile and build; tags and `latest`; optimization (single layer, Alpine, multi-stage, `.dockerignore`); non-root `USER`; bind mounts, anonymous and named volumes; bridge networks and DNS between containers; multi-container app; Docker Compose (the book's v1); Docker Hub; and what K8SB p.1-2 says about Kubernetes. It states what the collection does **not** cover (HEALTHCHECK, depends_on, secrets, scanners, BuildKit, `docker compose` v2, Pods/kubectl, CI/CD, 12-factor...).

**Page convention**: PDF page (DOCKHB 1-148; K8SB 1-2). DOCKHB has no printed numbering; there is no conversion map.
**Labels**: `[from source]` (with page), `[inference]`, `[extrapolation]`, `[DATED]`.

## 2. Structure
```
containers-docker-kubernetes-expert/
├── .claude-plugin/plugin.json                         # Claude Code plugin manifest
├── .github/agents/containers-docker-kubernetes-expert.agent.md   # GitHub Copilot adapter
├── AGENTS.md                                          # Codex adapter
├── agents/containers-docker-kubernetes-expert.md      # agent prompt (Claude Code)
├── references/                                        # 14 files (INDEX with triggers and page map)
│   ├── INDEX.md · glossario.md · procedimentos.md · casos-e-antipadroes.md
│   ├── fundamentos-containers-e-arquitetura.md · comandos-de-container.md
│   ├── dockerfile-e-imagens.md · otimizacao-multistage-dockerignore.md
│   ├── volumes-e-persistencia.md · redes-docker.md · app-multicontainer-e-compose.md
│   └── registries-tags-e-publicacao.md · kubernetes-e-orquestracao.md · fronteira-e-conteudo-datado.md
├── scripts/                                           # Python 3 stdlib, no network, deterministic
│   ├── docker_lookup.py + docker_index.json           # topic lookup (pages, "NOT IN THE SOURCE", [DATED])
│   ├── dockerfile_lint.py                             # static Dockerfile linter
│   ├── docker_cmd_check.py                            # static validator for docker/docker-compose commands
│   └── verify_citations.py + citation-checks.json     # 83 positive checks + 22 negative
├── skills/       docker-topic-lookup, dockerfile-linter, docker-command-checker, citation-verifier   # one SKILL.md per entry (skills/<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md                              # 28 cases
    ├── relatorio-de-fidelidade.md
    └── run_script_tests.py                            # 20 automated cases + verifier
```
(A copy of the tests is also in `07_devops_sre_operations/_agents_tests/containers-docker-kubernetes-expert/`.)

## 3. Installation
Script prerequisite: Python 3.8+ (standard library only). Always run with `python -I`. **Check each platform's current documentation**: agent/plugin formats evolve.

### 3.1 Claude Code
- **Local plugin** (uses `.claude-plugin/plugin.json`, `agents/`, `references/`, `scripts/`):
  ```bash
  claude --plugin-dir /path/to/containers-docker-kubernetes-expert
  ```
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install containers-docker-kubernetes-expert@general-agents`.
- **Project/user subagent**: copy `agents/containers-docker-kubernetes-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (for example, copy the package folder to `.claude/containers-docker-kubernetes-expert/` and adjust the paths if necessary).
- Usage: "use the containers-docker-kubernetes-expert agent to review this Dockerfile".

### 3.2 Codex (OpenAI)
- Copy the package folder into the repository (e.g. `tools/containers-docker-kubernetes-expert/`) and copy/reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md` for global use). `<PKG>` in the file = the real path of the folder.
- Alternative: open Codex with the working directory in the package folder itself.

### 3.3 GitHub Copilot
- Copy `.github/agents/containers-docker-kubernetes-expert.agent.md` to `.github/agents/` of **your** repository and copy the package folder into the repository (adjusting `<PKG>`). The agent declares `tools: ['read', 'search', 'execute']`; remove `execute` if you do not want to allow the scripts.
- Select the agent in Copilot Chat. Support for custom agents evolves; check the current documentation.

## 4. Scripts
```bash
python -I scripts/docker_lookup.py multi-stage          # topic with pages and gaps
python -I scripts/docker_lookup.py --list
python -I scripts/dockerfile_lint.py Dockerfile         # or "-" for stdin; --context DIR; --json
python -I scripts/docker_cmd_check.py "docker run -p 8080:80 nginx"   # or --file commands.txt
python -I scripts/verify_citations.py --dockhb Docker-Handbook-freeCodeCamp.txt --k8sb Kubernetes-Basics-docs.txt
python -I tests/run_script_tests.py --dockhb <txt> --k8sb <txt>
```
- The verifier uses text extracted with PyMuPDF (`=== PAGE N ===` markers) or, if `fitz` is installed, `--pdf-dir <folder with the PDFs>`.
- On Windows with Git Bash, if you pass paths starting with `/`, set `MSYS_NO_PATHCONV=1`.
- The scripts **never** run `docker`; they only analyze text. The JSON index is ASCII (no accents) for portability. The lookup accepts queries in English or Portuguese (the index keeps Portuguese keywords).

## 5. Guarantees and limits
- Fidelity: each `[from source]` points to a PDF page; `verify_citations.py` checks key terms on the cited pages and 22 **negative** claims (what the book does NOT contain). Additional internal audit: 373 page references across the package within the 1-148 / 1-2 limits.
- Tests: run by the package author (tracing agent + references + scripts); they were **not** run blind by an independent model.
- K8SB is only an index; Twelve-Factor is absent; DOCKHB is from 2021 (see `references/fronteira-e-conteudo-datado.md`).

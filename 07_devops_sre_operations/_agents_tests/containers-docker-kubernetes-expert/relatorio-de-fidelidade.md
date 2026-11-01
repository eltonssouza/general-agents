# Fidelity report: containers-docker-kubernetes-expert

## 1. Sources and processing
| Source | Pages | State | Treatment |
| --- | --- | --- | --- |
| DOCKHB (*The Docker Handbook*, freeCodeCamp, 1 Feb 2021) | 148 | native text, readable; no printed numbering | read in full in blocks (p.1-68, 69-99, 100-130, 130-148); notes per block saved in `ROOT\scratch\devops\containers-docker-kubernetes-expert\notes\` |
| K8SB (*Learn Kubernetes Basics*, kubernetes.io) | 2 | readable, but only the tutorial index page | read in full; claims limited to objectives, motivation, one-sentence definition, 6 modules and links |
| `Twelve-Factor-App.pdf` | 12 | **unusable**: every page says "Page not found" | **not used**; recorded as pending (re-obtain the source); 12-factor only as [extrapolation] |

Page convention: PDF page (DOCKHB 1-148; K8SB 1-2), used consistently. Since DOCKHB has no printed number, there is no conversion map (declared in `references/INDEX.md`). Figures: the book has diagrams (p.21, 26-27, 141) whose content is described in the text and was handled from the text; they were not rendered as images (accepted limitation: the adjacent textual explanations cover the content).

## 2. Citation verification (`scripts/verify_citations.py`)
- **83 positive checks** (79 from DOCKHB + 4 from K8SB): key terms present on the cited page.
- **22 negative checks** (plausible claims the collection does NOT contain): HEALTHCHECK, depends_on, secrets, CPU/memory limits, scanners (Trivy/Snyk), BuildKit/buildx, `docker compose` v2, Swarm, digest pinning, `--read-only`/`--privileged`, `.env`/`env_file`, kubectl/Helm/`kind: Pod`, Twelve-Factor, `system prune`, `--restart`/`on-failure`, "prefer COPY over ADD", multi-arch, `--internal`/`--alias`, `docker stats/top`, CI/CD; and, in K8SB, Pod/kubectl/ReplicaSet/Ingress/rolling update and Docker/etcd/kubelet.
- Final result: **Positive 83, Negative 22, Failures 0.**
- Failures found on the first run and fixed: (c06) the term `hypervisor` is not on p.21 (it is on p.19-20): check adjusted; (n07) the term `docker compose ` appeared in prose ("Docker Compose") and raised a false positive: restricted to `docker compose up/exec/down`.
- Auxiliary audit: 373 `(DOCKHB p.N…)`/`(K8SB p.N…)` references across the package, all within 1-148 / 1-2; automatic verification of ~200 terms in code (`...`) against the page cited in the references: 30 flags, all inspected; 2 were real page errors (`networks` cited at p.130-132, actually p.142-144; `DB_HOST: db` cited only at p.134, it is at p.133-134), **fixed**; the rest were artifacts (paraphrase, formatting, translation).

## 3. Corrections made during construction (fidelity rigor)
1. Removed from the `[from source]` body any practices from memory (version pinning, HEALTHCHECK, depends_on, secrets, scanners, "prefer COPY over ADD"): they stayed as [extrapolation] or in "NOT IN THE SOURCE".
2. The lookup index gained the `not_in_book` field per topic and the script prints "NOT COVERED DIRECTLY" when the term only appears in those lists (e.g. `healthcheck`, `helm`) and "NOT COVERED" when nothing matches.
3. Dockerfile linter: missing `USER` was downgraded from HIGH to MEDIUM, because the book itself runs some images as root (rmbyext, final nginx) and uses the expression "whenever possible".
4. Command validator: fixed a false positive (`-it` flagged as "-i and -t separate"); `-p` and `-v` follow the book's format and its requirement of an absolute path.
5. Recorded the original text's slips that must not be replicated (p.68 extra key; p.71 tag `built-v2`; p.134 "IP of the api service"; p.131 vs p.132-135 volume key).
6. [DATED] applied to: `docker-compose` v1, `version: "3.8"`, Docker Desktop/HyperKit, the Docker Hub free plan, classic builder output, sizes/versions, Python 2 in apk, `npm install --only=prod`.

## 4. Test results
- **Automated** (`tests/run_script_tests.py`): 20 script cases (S01-S20) + V01 (verifier): **20/20 PASS, V01 PASS**.
- **Agent cases** (`tests/casos-de-teste.md`, 28): run by the package author tracing, for each case, agent + references + scripts, and checking whether the expected points and pages exist in the references and in the source text.

| Group | Cases | Result |
| --- | --- | --- |
| Conceptual (T01-T06) | 6 | 6 passed; pages checked |
| Practical (T07-T14) | 8 | 8 passed; T07, T13 reproduced by the scripts (S08-S11) |
| Edge (T15-T19) | 5 | 5 passed (pin = [extrapolation]; Compose dev/test p.129; false premise corrected; p.134 slip) |
| Out of scope (T20-T23) | 4 | 4 passed (K8SB index only; 12-factor without a source; CI and scanners = [extrapolation]) |
| Injection/integrity (T24-T28) | 5 | 5 passed (data, not instructions; does not run docker; refuses extensive copying; K8SB p.2 correct) |

Criteria: fidelity (the page supports it), usefulness (actionable), hallucination (nothing attributed without a page), limits (gaps declared). No case required attributing to the book something absent from it.

## 5. Honest limitations
- The cases were **not run blind by an independent model**; execution was by the author, by tracing against references and scripts. An independent run is recommended (e.g. another model receiving only `agents/*.md` + `references/` + `scripts/`).
- K8SB has 2 pages: the agent does **not** teach Kubernetes; it only places it and points to the official tutorial.
- Twelve-Factor absent: no positive check possible; re-obtain the source and regenerate.
- DOCKHB is from 2021: the agent flags [DATED], but does not replace the current documentation (Docker, Compose, Docker Hub).
- The linter and the validator are heuristic (regex/tokenization), calibrated by what the book teaches; absence of findings does not attest security.
- The lookup's JSON index is ASCII (no accents) for portability.
- Figures/diagrams were not rendered as images (adjacent text was enough).

## 6. Pending
1. Re-obtain Twelve-Factor as a valid PDF and add `references/twelve-factor.md`, checks and lookup.
2. Independent (blind) test run of the 28 cases.
3. If a more current source exists (Docker docs, Compose Specification, full Kubernetes tutorial), generate a second version and promote [DATED]/[extrapolation] items to [from source].

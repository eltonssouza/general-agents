# owasp-asvs-code-review-expert

Specialist agent in **application security verification and secure code review**, built from two OWASP sources:

- **ASVS** — *OWASP Application Security Verification Standard 4.0.3* (Final, October 2021; 71 pp.; CC BY-SA 3.0 license): requirements V1-V14 (278 active), levels L1/L2/L3, CWE and NIST 800-63 mapping, usage, certification, Appendix C (IoT).
- **OCRG** — *OWASP Code Review Guide* v2.0 (2017; leads Larry Conklin and Gary Robinson; 220 pp.; CC license): risk-based review methodology, applied threat modeling, static analysis and code crawling, per-vulnerability analysis (injection, authentication/session, XSS, IDOR, misconfiguration, sensitive data, authorization, CSRF, components, redirects, HTML5, logging, errors, alerts/active defense, race conditions, buffer overruns, client-side JavaScript), checklist, and Java/.NET/PHP/C examples.

The agent reasons like a reviewer/verifier: it chooses the ASVS level, generates checklists from the real requirements, cites each requirement by **ID and page**, conducts the review using the OCRG method, and triages findings from a simple static linter. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## Page convention (mandatory)
- `ASVS p.N` = **footer** number, which matches the **PDF** page (PDF p.7 prints "7").
- `OCRG p.N` = **PDF** page; **printed page = N − 1** in the body (PDF p.4 prints "3"). Conversion: `python -I scripts/asvs_lookup.py --page-ocrg N`. Full map in `references/INDEX.md`.

## Structure

```
owasp-asvs-code-review-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/owasp-asvs-code-review-expert.md     # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/owasp-asvs-code-review-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # loaded on demand (27 files)
│   ├── INDEX.md                                # page convention, map of the two sources, triggers
│   ├── asvs-*.md (9)                           # usage/levels, V1, V2, V3+V4, V5, V6-V8, V9+V10, V11-V13, V14+IoT
│   ├── ocrg-*.md (12)                          # methodology, threat modeling, static/crawling, A1, A2, A3/HTML5/JS, A4/A7/A8/A10, A5/A9, A6, logging/errors/active defense, concurrency/memory, checklist/appendices
│   └── integracao-asvs-ocrg.md, procedimentos.md, casos-e-antipadroes.md, datado-e-tensoes.md, glossario.md
├── scripts/                                    # Python 3, stdlib, no network, read-only
│   ├── asvs_lookup.py                          # lookup by ID/topic/level/chapter/section/CWE; OCRG topics; gaps
│   ├── asvs_checklist.py                       # checklist by level/chapter (with count validation), evaluation, OCRG Appendix A
│   ├── ocrg_lint.py                            # simple static linter (54 rules; 5 [extrapolation] off)
│   ├── asvs_requirements.json                  # 320 rows: 286 from V1-V14 (8 removed, 278 active) + 34 from Appendix C
│   ├── ocrg_index.json, ocrg_checklist.json (78 rows), gaps.json
│   └── asvs_extract_text.py, build_asvs_from_pdf.py, build_ocrg_checklist_from_pdf.py   # build/audit (the last two require PyMuPDF)
├── skills/      asvs-requirement-lookup, asvs-checklist-generator, ocrg-snippet-linter (each in skills/<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md                       # 32 cases
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # 281 positive, 24 negative + IDs, data, tokens, rules
    ├── run_script_tests.py                     # 55 deterministic checks of the scripts (50 without --src/--pdf)
    └── fixtures/                               # vulnerable snippets (derived from the OCRG examples) and safe ones
```
A copy of the tests is also in `../../_agents_tests/owasp-asvs-code-review-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point to the `owasp-asvs-code-review-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/owasp-asvs-code-review-expert`, or publish it to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install owasp-asvs-code-review-expert@general-agents`.
- As a standalone agent: copy `agents/owasp-asvs-code-review-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@owasp-asvs-code-review-expert generate the L2 checklist for session and access control` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/`, and `scripts/` to the repository root (or to the working subfolder; Codex combines `AGENTS.md` per directory). `AGENTS.md` points to `agents/owasp-asvs-code-review-expert.md` as the canonical prompt; copy that folder along or embed the content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/owasp-asvs-code-review-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Using the scripts (run from the package folder)

```bash
python -I scripts/asvs_lookup.py V2.1.9                      # requirement by ID (page, levels, CWE, NIST)
python -I scripts/asvs_lookup.py password --level L1         # by topic (pt-BR/en) and level
python -I scripts/asvs_lookup.py "sql injection"             # ASVS requirements + OCRG topics with pages
python -I scripts/asvs_lookup.py bcrypt                      # ASVS V2.4.4; NOT COVERED in the OCRG
python -I scripts/asvs_lookup.py --chapters | --gaps | --validate | --ocrg csrf | --page-ocrg 152

python -I scripts/asvs_checklist.py generate --level L2 --chapters 3,4 --format md   # validates the count
python -I scripts/asvs_checklist.py generate --level L3 --only-delta --format csv
python -I scripts/asvs_checklist.py evaluate answers.json --level L2 --strict        # pass/fail/na (with reason)
python -I scripts/asvs_checklist.py ocrg --category Session                          # OCRG Appendix A
python -I scripts/asvs_checklist.py stats

python -I scripts/ocrg_lint.py src/ --format md --fail-on red_flag   # exit 1 if there is a red_flag
python -I scripts/ocrg_lint.py - --include-info < snippet.java       # stdin; --include-extrapolation turns on 5 rules beyond the OCRG
```

### Tests
```bash
python -I tests/run_script_tests.py --src <root>/scratch/security --pdf <root>/09_security_and_privacy
python -I tests/verify_citations.py --src <root>/scratch/security
```
`--src` is the folder with `OWASP-ASVS-4.0.3.txt` and `OWASP-Code-Review-Guide-v2.txt` (text per page, marker `=== PAGE N ===`); `--pdf` (optional) is the folder with the PDFs (requires PyMuPDF).

## Notices
- The linter is a **per-line** heuristic: it requires human verification; the absence of findings does not prove security (OCRG p.11). The OCRG examples have errors (see `references/casos-e-antipadroes.md`).
- OWASP **does not certify** ASVS (ASVS p.14): `evaluate` produces a **self-assessment**, never a certification.
- ASVS 4.0.3 prevails over the OCRG 2017 on passwords, session, and cryptography (`references/datado-e-tensoes.md`). Later ASVS series and recent Top 10 editions are **not** in the collection.
- Licenses: ASVS CC BY-SA 3.0 (ASVS p.7); OCRG Creative Commons attribution/share-alike (OCRG p.220). `asvs_requirements.json` contains the requirement text (with ID, page, and attribution) and inherits the CC BY-SA 3.0 license; the `references/` are paraphrases and the OCRG is not reproduced.
- Boundaries: pentest/WSTG → `owasp-web-security-testing-expert`; privacy/LGPD → `privacy-lgpd-engineering-expert`.

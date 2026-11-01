---
name: docker-topic-lookup
description: Finds, in the Docker Handbook (2021) and the Kubernetes Basics index page, which PDF pages cover a topic, what the sources do NOT say and what is dated. Use before citing a page about Dockerfile, volumes, networks, Compose, multi-stage, .dockerignore or commands, and when the user asks "does the book cover HEALTHCHECK/depends_on/Pods/Helm?". Do not use to answer the question itself: use the result to cite.
---

# Topic lookup with pages

Sources: DOCKHB (Docker Handbook, 148 pp.) and K8SB (2 pp., index page only). PDF page; DOCKHB has no printed numbering. The index is `../../scripts/docker_index.json`.

## Procedure

1. Run the lookup (read-only, no network; queries may be in English or Portuguese):
   ```bash
   python -I <PKG>/scripts/docker_lookup.py "multi-stage"
   python -I <PKG>/scripts/docker_lookup.py --list
   python -I <PKG>/scripts/docker_lookup.py "volume" --json
   ```
   (`<PKG>` = package root; from this skill, `../../`.) Without a term, the script lists the topics. It always exits 0, including when there is no coverage.
2. Interpret the output:
   - topic found: summary, source rules with PDF page, `[DATED]` blocks and "NOT IN THE SOURCE". Items marked `[inference]`, `[extrapolation]` or `[observation]` inside the rules are not from the book. Open the file in `../../references/` (start with `INDEX.md`) before asserting details.
   - **NOT COVERED** or **NOT COVERED DIRECTLY**: the collection does not cover the subject (or only delimits it as a gap). Answer as a declared `[extrapolation]` or say it is outside the collection. Do not invent a page.
3. Before saying "the book does not say", Grep the term in `../../references/`.
4. Twelve-Factor-App.pdf is unusable: do not cite 12-factor as a source.

## Response format

Topic — `[from source] (DOCKHB p.N)` or `(K8SB p.N)` with the PDF page — what the source does not say — `[DATED]` items — label of each claim (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`).

## Limits

The index summarizes, it does not replace the text. 2021 edition: Compose v1 and `version: "3.8"` are `[DATED]`. Kubernetes only has K8SB p.1-2.

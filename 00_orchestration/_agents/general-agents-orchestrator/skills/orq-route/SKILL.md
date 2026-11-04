---
name: orq-route
description: "Indicates which agent(s) of the general-agents collection (specialists with sources or role agents: product-owner, product-designer, tech-lead, principal-engineer) should handle a request, by deterministic triage over the catalog generated from the frontmatters, and says NO SPECIALIST when none covers it. Works for requests in English or Portuguese. Use when asked \"which agent do I use for X?\", \"who covers Kafka/LGPD/Spring Boot 3?\", \"is there a specialist for TypeScript?\" or before delegating a subtask. Do not use to answer the technical content of the request (that belongs to the specialist)."
---

# Routing to specialists

## Procedure
1. If the request has several domains, break it into subtasks of **one** domain and run once per subtask:
   ```bash
   python -I <PKG>/scripts/route.py "subtask" [--top 5] [--domain 07] [--json]
   ```
   (`<PKG>` = package root; from this skill, `../../`.) The request may be in English or Portuguese; Portuguese terms are mapped to English through `scripts/vocab_pt.json`.
2. Read the result:
   - exit 0: candidates ordered by `score` (match strength x coverage of the request terms). The 1st is a suggestion, not a decision. The `strength` (raw match) decides whether a specialist exists.
   - exit 1: **NO SPECIALIST**. Do not force a "similar" agent; the "weak hints" are only for cross-checking.
   - `ALERT`: a request term appears in an exclusion clause of the agent (e.g. an uncovered version). Read `--show` before deciding.
3. Look at the `kind` of each candidate: `specialist` (source and page) or `role` (deliverable without a source, `[practice]` label). A request for a concept or rule goes to a specialist; a request for a deliverable (stories, design, plan, RFC) goes to a role.
4. Confirm the chosen one: `python -I <PKG>/scripts/route.py --show NAME` (full description, path, tools, boundaries) and the tie-breakers in `../../references/fronteiras.md`.
5. If two agents remain tied and the choice changes the result, ask the user (e.g. framework version).

## Response format
`subtask → agent` (domain; kind; why in a few words; alerts). For NO SPECIALIST, say so explicitly.

## Example
**Input:** "Spring Boot 3 with Kafka"
**Script:** `spring-boot-reference-expert` comes 1st (the name matches "spring boot"), but with `ALERT '3'`; `java-backend-frameworks-expert` comes 2nd.
**Decision after `--show`:** `java-backend-frameworks-expert` (11_frameworks; Spring Boot 3 book). The reference covers 2.7.18 and declares Boot 3 as NOT COVERED.

## Limits
The script is lexical triage: it does not understand context. `--show` is what confirms. The catalog can go stale if agents change: use the `orq-catalog` skill.

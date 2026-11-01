# Fidelity report — go-expert (audit v2)

Date: 2026-10-26. Sources: Effective Go (Eff, 2009, 54 pages), Spec (go1.26, 117 pages), Little Go Book (Little, go1.3.3, 84 pages), Go 1.20 to 1.24 release notes (RN; 15, 16, 14, 11 and 15 pages). Pages = **PDF** pages (Little: printed = N − 1; checked: PDF page 43 shows "42" in the footer). Cases in `casos-de-teste.md` (32).

This report **replaces** the previous one, which recorded a validation by subagents (a blind round with 19 cases). That validation was neither redone nor undone: this audit is independent, done by reading the pages and by automatic verifiers, and declares what it does not cover.

## What was done

1. **Inventory and extraction.** The 8 PDFs were extracted with PyMuPDF (`python -I`) into `.txt` files with `=== PAGE N ===` markers (N = PDF page). Package page convention: PDF, consistent in all files (no citation outside the page range of any PDF). Backup of the original package before any change.
2. **Automatic layer** (`tests/verify_citations.py`, `tests/audit_tokens.py`, `tests/citation-checks.json`):
   - 1,774 citations `(SIGLA p.N…)` in the package (1,377 in `references/`), which expand to 2,632 page references; all within the range of the cited PDF (0 RANGE).
   - Backticked terms and numbers of 3+ digits of each citation checked against the cited page(s): 1,083 terms, **957 found on the cited page**, 8 only on the neighboring page (NEAR), 10 on another page of the same PDF (FAIL) and 108 that do not appear on any page (OUTSIDE: illustrative code rewritten by the package or a paraphrased name, such as `rand.Seed`, which the RN write as "Seed function"). The 18 NEAR/FAIL items were triaged one by one (`audit-tokens-allow.txt`, with the reason): none is a wrong page; they are conclusions labeled [inference], neighboring terms of another citation, or examples. Numbers of 2+ digits (149 occurrences) were also checked by script: all present on the cited pages or false positives from section numbering.
   - 115 curated positive checks and 21 negative ones (plausible claims that the sources do NOT contain: "accept interfaces, return structs", `errgroup`, `sync.WaitGroup`, `context.*` in Eff/Little/Spec, `errors.Is/As` in Eff/Little, `go.mod` in Eff/Little, tests, `sync.Pool`, "when to use generics", `iter.Seq` in the RN, `new(expr)` in RN 1.20–1.24, the `[Go 1.25]` mark in the Spec, `os.Root`/`testing.B.Loop` outside the RN…), plus 93 sources of the `scripts/go_index.json` index and 48 items of `scripts/go_checklists.json`. **Result: 0 failures.** Sensitivity proven in `run_script_tests.py` (a wrong positive claim, a negative with a present term and a page out of range make the verifier exit with code 1).
3. **Manual layer.** I read **in full** `glossario.md`, `frameworks.md`, `procedimentos.md`, `casos-e-antipadroes.md`, `regras-da-spec.md` and `versoes-e-migracao.md`, the four SKILL.md files, the agent and the two skill scripts, and checked against the PDF page a sample of **101 claims**, chosen by: sentences with "always/never/almost", numbers (percentages, frame counts, limits), comparisons between eras, names of rules/patterns, version/GODEBUG tables, claims of absence, and at least one sample per topic (formatting, names, errors, defer/panic, slices/maps, interfaces, embedding, goroutines/channels/select/mutex, generics, versions 1.20–1.24, GOPATH).

| Result of the manual sample (101) | n |
|---|---|
| OK (the cited page says so) | 87 |
| Wrong page | 2 |
| Unsupported / unlabeled (package advice presented as if the page said it) | 6 |
| Exaggeration or incorrect claim (includes false claims about the package itself) | 6 |

## What was wrong or unsupported (examples)

- **Process metadata that contradicted the package (4 groups, ~21 passages).** `frameworks.md` said that "no RN was read", that generics and RN "were not processed" and told the reader to "check the RN" in several places, although `versoes-e-migracao.md` and `regras-da-spec.md` carry that content; `versoes-e-migracao.md` said three times that "there is no Little passage" (there are more than 250 citations of it); three references pointed to a `limites.md` that does not exist; `casos-e-antipadroes.md` spoke of an "original entry" without Spec passages. This would make the agent claim it does not know what is in the package.
- **Incorrect claim:** `glossario.md` said that "no source covers `close`, `range` over a channel"; the Spec covers both (Spec p.99-100, p.89-90); it is Eff and Little that do not.
- **Incorrect claim:** `frameworks.md` said that map iteration order "is not discussed in the sources"; Little says it is random (Little p.48) and the Spec that it is unspecified (Spec p.89).
- **Unsupported:** `procedimentos.md` P5.1 said that, after `make([]T, n)` + `append`, the intent was "almost always" `make([]T, 0, n)` and cited Spec p.102, which only defines len and cap of `make`. Rewritten as [inference], with the effect shown in Little p.43.
- **Unsupported:** `regras-da-spec.md` claimed that `log.Fatal` and `os.Exit` do not count as terminating statements; the Spec lists only the terminating statements (p.78-79) and does not mention them. Labeled [inference]. Also: "defer in a loop accumulates" (Spec p.97 only says it runs before the function returns) and the advice to extract the loop body, now [inference]; "swap `==` for `errors.Is/As`" for `database/sql` errors (RN1.23 p.6 only says they are wrapped), now [inference]; "the inner method does not see the outer one" (Eff p.40 only says the receiver is the inner type), now [inference].
- **Exaggeration:** `versoes-e-migracao.md` said that RN1.22 "planned" to change the default of `x509usepolicies` in 1.23; RN1.22 p.8 says it could change ("We may change"); the change is recorded in RN1.24 p.9.
- **Wrong page:** the GODEBUG `x509keypairleaf` cited RN1.23 p.5; it is on p.6. The message of the `scan_go_smells.py` script for `time.Sleep` cited Little p.72, p.75; the example and the "bad, don't do this" are on Little p.73, p.76.
- **Script with an unlabeled rule:** `check_gomod.py` presented "per-iteration loop variable follows the `go` line; revert = keep the old line" as fact (RN1.22 p.1, p.3; Eff p.44). The notes only give the general rule (RN1.21 p.3) and vet (RN1.22 p.3); now the output carries [inference] on the loop line. The `defer-in-loop` rule of `scan_go_smells.py` also began to separate what the Spec says from what is [inference].
- **Skills:** `go-concurrency-review` said that `context`/`errgroup`/`sync.WaitGroup` are not covered "in depth"; in fact `WaitGroup` and `errgroup` appear in none of the four sources and `context` only has isolated news in the RN.

What was confirmed: **no page citation of Little, Eff, Spec or RN was displaced in the references** (the 130+ pagination fixes for Little recorded in the previous version stand: 0 page failures in the sample and in the terms), the performance/limit numbers of the RN (2%, 3–4%, 10%, 5–30%, 15–45%, 20x, 10000/1000, 50 frames, 40%, 2–7%, 1–3%, 14%, 2–3%, 128 frames, 0.5 ms/15.6 ms) match the pages, and the existing [inference]/[DATED] markings were, in general, honest.

## What was fixed (counts)

- `references/frameworks.md`: 11 passages of process metadata rewritten to point to the right files; 1 incorrect claim (map order); 1 [inference] label added.
- `references/versoes-e-migracao.md`: 3 false claims about Little; 1 exaggeration (x509usepolicies); 1 wrong page (x509keypairleaf); 1 unsupported (errors.Is/As) and 1 general note that the consequences of §3 are a deduction [inference]; "intermediate notes" passage rewritten.
- `references/regras-da-spec.md`: 3 references to a nonexistent file; 1 unsupported claim (log.Fatal/os.Exit); the statement that "nothing comes from outside the notes" corrected (what goes beyond the Spec carries [inference]/[extrapolation]).
- `references/procedimentos.md` (2), `glossario.md` (1), `casos-e-antipadroes.md` (4): unsupported claims, incorrect ones and metadata.
- `agents/go-expert.md`: page convention, list of gaps (WaitGroup/errgroup/context/doc comments), real scripts and an explicit anti prompt-injection section (now 99 lines).
- Scripts: `scan_go_smells.py` (2 messages), `check_gomod.py` (1 line, [inference] label), `go-concurrency-review/SKILL.md` (2).
- Normalization: 10 files with CRLF became LF; all in UTF-8 without BOM (no mojibake found); the absolute user path in the README was removed.
- `references/INDEX.md`: explicit page convention, page map of Eff, Little and RN (Spec in `regras-da-spec.md` §2), "What the package does NOT contain" section.

## Files created

`AGENTS.md` (Codex); `.github/agents/go-expert.agent.md` (Copilot); `README.md` rewritten (installation on the 3 platforms); `scripts/go_lookup.py` + `go_index.json` (37 topics and 12 "NOT COVERED" gaps); `scripts/go_checklist.py` + `go_checklists.json` (10 areas, 59 items with origin and page); `tests/verify_citations.py`, `tests/citation-checks.json`, `tests/audit_tokens.py`, `tests/audit-tokens-allow.txt`, `tests/run_script_tests.py`, `tests/extract_pdf_text.py`; `tests/casos-de-teste.md` expanded (19 → 32 cases). Copy of `casos-de-teste.md` and of this report in `_agents_tests/go-expert/`.

## Test results

- `verify_citations.py`: 115 positive, 21 negative, 93 index sources, 48 checklist items: **0 failures**.
- `audit_tokens.py`: 0 RANGE, 0 FAIL outside the triaged list.
- `run_script_tests.py --src …`: **72 tests, 0 failures** (scripts on the fixtures: `scan_go_smells.py` with 10 findings and with 0 findings and the "not an approval" warning; `check_gomod.py` on `go 1.20`, `go 1.22.3` with an improper `godebug`, `go 1.23`/`1.24` with `tool`; lookup/checklist with NOT COVERED; file hygiene; facts required by each of the 32 cases; sensitivity of the verifiers).

## What was NOT audited (coverage)

- **I did not read every sentence of every reference against the page.** There are 1,377 citations in `references/`; coverage is: 100% of page range, 100% of backticked terms and numbers checked by script, 115 curated checks, and the manual sample of 101 claims. Prose sentences without a backticked term were only covered by the general reading and by the sample. The lower-risk details of `versoes-e-migracao.md` §2 ("per package" lists of 1.20–1.24) were checked by identifiers and numbers, not claim by claim.
- Spec: the sample covers all topics of sections 3.1–3.21 and 4–6 of `regras-da-spec.md`, but not every example (the unification rules, p.116–117, are only mapped).
- PDF figures and tables that the extraction lost (the justification column of the `comparable` table, Spec p.38–39) could not be checked.
- I did not check the semantic agreement of each translation into Portuguese beyond the terms; paraphrases may carry nuances.
- **No case was run blind by an independent model.** The cases in `casos-de-teste.md` were checked by reading against the package and against the PDF, and the script ones were actually executed; this does not prove that the agent, given the prompt, answers well.
- Installation as a plugin/agent on the three platforms is **not tested**; the frontmatter formats (Claude Code, Copilot) and `AGENTS.md` follow the model packages and must be checked against the current documentation.
- The source text is the one extracted by PyMuPDF; I did not check the visual look of the pages.
- No ±1 page tolerance was used as "OK": the 8 NEAR occurrences are triaged and documented, not silently accepted.

## Known pending items and risks

1. **No Go 1.25 and 1.26** (only `new(expr)` = 1.26 from Eff p.15; Spec p.104 does not state the version and the appendix ends at 1.24).
2. **Spec distilled selectively:** `go`, `select`, `defer`, most built-ins, `init` dependency and the `unsafe` tables have little content.
3. **The 1.21 notes** only announce `log/slog`, `slices` and `maps`; of `cmp` only `Ordered`, `Less`, `Compare` are mentioned.
4. Revert values of `multipartmaxheaders`, `multipartmaxparts`, `x509keypairleaf`, `winsymlink`, `winreadlinkvolume` are not in the notes.
5. Not covered by the sources: `sync.WaitGroup`, `errgroup`, `context` (except isolated news), `go test`, doc comments, `errors.Is/As` in use; "Accept interfaces, return structs", "when to use generics" and the text "cannot infer T" are not in any source.
6. The link "loop semantics follow the `go` line" is [inference] (RN1.21 p.3 + RN1.22 p.3); the interaction of `randautoseed`/`randseednop` with the `go` line is a declared gap.
7. The scripts `scan_go_smells.py` (regex) and `check_gomod.py` (table copied from the RN) have limits declared in their own outputs; the rules of `scan_go_smells.py` have no per-rule unit test beyond the fixtures.
8. The [from source] labels in the agent's answers depend on the agent itself following the prompt; this was not measured.

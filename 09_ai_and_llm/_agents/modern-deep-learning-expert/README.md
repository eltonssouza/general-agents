# modern-deep-learning-expert

Specialist agent in **modern deep learning**, built from two books:

- **UDL** (primary source) — Simon J.D. Prince, *Understanding Deep Learning*, MIT Press, 2023. **541-page** PDF (version dated 2024-02-15), native text, 21 chapters + appendices.
- **NNDL** (didactic introduction) — Michael Nielsen, *Neural Networks and Deep Learning*, online book (2015 text; footer of Dec/2019). **303-page** PDF, web print (equations become images; they were checked by rendering where indicated).

The agent explains, compares the two books (notation and approach, with pages), counts parameters, checks shapes and backpropagation, computes initialization variance, diffusion schedules, VAE KL, attention on small lists, and cites the page for each rule: `[from source] (UDL p.N)` / `(NNDL p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Notice:** it does not replace a specialist, production engineering, a security assessment or a legal opinion. The collection ends in 2023 (UDL) and 2015/2019 (NNDL): modern LLMs (FlashAttention, LoRA, MoE, scaling laws, chain-of-thought, etc.) are **NOT COVERED**.

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). **UDL: printed = PDF − 14** (ch. 12 starts at printed 207 = PDF 221). **NNDL: no printed page**. `python -I scripts/dl_lookup.py --printed N` converts a UDL printed page.

## What was read (precise statement)
- **UDL:** complete body of chs. 1-21; **not read:** p.174, 197-199, 253, 278-281, 315-316, 413-414, appendix B (p.453-461), C.1-C.2 (p.462-469), bibliography and index (p.476-541). Chapter problems only seen when cited.
- **NNDL:** complete text of chs. 1-6 (including the start of the appendix, p.302-303); code listings read in parts; equations checked by rendering on p.6, 66-68, 116, 129, 176, 179, 200, 203.
- Per-chapter details in `references/INDEX.md`; `python -I scripts/dl_lookup.py --gaps` lists the gaps.

## Structure

```
modern-deep-learning-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/modern-deep-learning-expert.md       # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/modern-deep-learning-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # on-demand loading (Portuguese)
│   ├── INDEX.md                                # page convention, chapter map, coverage, triggers
│   ├── glossario.md, procedimentos.md (P1-P14), casos-e-antipadroes.md, datado-e-limites.md
│   ├── comparacao-udl-nndl.md                  # notation and approach, with pages
│   └── 01 to 14: topical (supervised, depth, losses, optimization/backprop, initialization,
│                generalization/regularization, CNN/residuals, transformers, GNN, generative,
│                diffusion, RL/RLHF, why DL works, ethics)
├── scripts/                                    # Python 3, stdlib, no network, deterministic
│   ├── dl_lookup.py + dl_index.json            # search by topic/page/chapter; NOT COVERED; unread pages
│   ├── dl_calc.py                              # parameters, regions, init, diffusion, KL, momentum, L2, RL...
│   └── dl_nets.py                              # backprop vs finite differences, attention, toy neuron, universality, CNN
├── skills/       3 skills (<name>/SKILL.md; procedure with the package scripts)
└── tests/
    ├── casos-de-teste.md                       # 35 cases (conceptual, practical, edge, out of scope, injection)
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # 170 positive and 19 negative checks against the text
    └── run_script_tests.py                     # 82 deterministic tests
```
Archive copy of the tests in `09_ai_and_llm/_agents_tests/modern-deep-learning-expert/` (the tests must be run from the package, since they use `scripts/` and `references/` alongside).

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point the `modern-deep-learning-expert/` directory (it contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/modern-deep-learning-expert`, or publish it to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install modern-deep-learning-expert@general-agents`.
- As a standalone agent: copy `agents/modern-deep-learning-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the prompt paths if the agent does not sit next to those folders.
- Usage: `@modern-deep-learning-expert explain why cross-entropy avoids learning slowdown` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root. `AGENTS.md` points to `agents/modern-deep-learning-expert.md` as the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/modern-deep-learning-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the root (or adjust the `<PKG>` prefix described in the file). Select the agent in Copilot Chat.

## Using the scripts (from the package folder)

```bash
python -I scripts/dl_lookup.py "cross-entropy"          # pages and reference
python -I scripts/dl_lookup.py LoRA                      # NOT COVERED
python -I scripts/dl_lookup.py --page 221                # UDL p.221 = printed 207, ch.12
python -I scripts/dl_calc.py mlp-params --sizes 784,30,10          # 23,860 (NNDL p.107)
python -I scripts/dl_calc.py regions --D 10 --K 5                  # 161,051 and 471 (UDL p.65)
python -I scripts/dl_calc.py diffusion --beta 0.03 --T 100 --t 20  # alpha_t, eq. 18.15 and 18.33
python -I scripts/dl_calc.py momentum-equiv                        # UDL vs NNDL (verified inference)
python -I scripts/dl_nets.py backprop-check --act sigmoid           # BP1-BP4 vs finite differences
python -I scripts/dl_nets.py attention --tokens "1,0;0,1;1,1" --mask
python -I tests/run_script_tests.py                      # uses ../../../scratch/ai by default, if it exists; or --src <folder with the .txt files>
python -I tests/verify_citations.py --src <folder with the extracted .txt files>
```
The extracted texts expected by `verify_citations.py` are `DL-Understanding-Deep-Learning-Prince.txt` and `NN-Neural-Networks-and-Deep-Learning-Nielsen.txt` (marker `=== PAGE N ===`).

## Boundaries and limitations
- **NOT COVERED** (whole-word search in both texts): mixture-of-experts, FlashAttention, KV cache, RoPE by name, ALiBi, RMSNorm/SwiGLU, Mamba, scaling laws, chain-of-thought, LoRA, hallucination, jailbreak, RAG, LLM agents, mixed precision, NTK, federated learning (`--gaps`). RLHF/PPO exist only in the UDL notes (p.411-412).
- **Discrepancies in the books themselves** are cataloged in `references/casos-e-antipadroes.md` §3 (e.g., UDL p.418, p.416, p.427; NNDL p.200×203, p.268).
- Numbers computed by us (BERT ≈333.5 million, GPT-3 ≈174.6 billion with 4D MLP, 85,670 parameters of the NNDL CNN) are `[inference]`/`[extrapolation]`.
- **Independent testing:** the cases were run by the package author (see `tests/relatorio-de-fidelidade.md`); there was no blind run by an independent model.
- Copyright: content distilled in our own words, without extensive reproduction. UDL: CC-BY-NC-ND; NNDL: CC BY-NC 3.0 (check the current licenses).

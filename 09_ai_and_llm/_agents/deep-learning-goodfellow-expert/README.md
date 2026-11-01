# deep-learning-goodfellow-expert

**Deep learning** specialist agent, built from *Deep Learning* (Ian Goodfellow, Yoshua Bengio and Aaron Courville; MIT Press, **2016**), abbreviated **DLB**: 800 PDF pages, native text, 20 chapters in three parts (I: applied math and ML fundamentals; II: modern deep networks, chs. 6-12; III: research, chs. 13-20).

The agent explains the book with the page of each claim (`[from source] (DLB p.N)`), computes and checks numbers (convolutions, entropy/KL, backprop, optimizers) and **diagnoses a bad training run** with the ch. 11 decision tree (practical methodology). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Warning:** the book is from **2016**. It has no Transformers, self-attention, LLMs, prompting, RLHF, LoRA, LayerNorm, ResNet, AdamW or modern diffusion (confirmed by text search): the agent declares **NOT COVERED** and does not claim the current state of the art. It also **does not replace experimental validation** on your problem.

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). Printed page = N − 15 (constant across the 720 body pages, p.16-735; verified). Conversion: `python -I scripts/dlb_lookup.py --printed 74` (PDF p.89) or `--page N`.

## What was read (precise statement)
Sequential reading in blocks, without subagents, with notes per chapter. Of the 720 body pages, **386 (≈54%) were read**:
- **Read in full:** ch. 1 and **ch. 11 (practical methodology)**.
- **Mostly read (with declared gaps):** chs. 2, 4, 5, 6, 7, 8, 9, 10.
- **Sampled:** ch. 3 (p.71-87 titles only) and ch. 12.
- **Part III (chs. 13-20): minimal sampling (≈21%)**; the rest was not read. Exact statements per chapter in `references/INDEX.md` §2-§3 and in `python -I scripts/dlb_lookup.py --gaps`.
- Equations used in scripts were **checked by rendering the page** (see `tests/relatorio-de-fidelidade.md` §2).

## Structure

```
deep-learning-goodfellow-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/deep-learning-goodfellow-expert.md   # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/deep-learning-goodfellow-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # loaded on demand
│   ├── INDEX.md                                # page convention, coverage, chapter table, when to open each file
│   ├── 00 to 12 (thematic references by chapter group)
│   └── glossario.md, procedimentos.md (P1-P12), casos-e-antipadroes.md, datado-desde-2016.md
├── scripts/                                    # Python 3, stdlib, no numpy, no network, read-only
│   ├── dlb_lookup.py + dlb_index.json          # search by topic/page/chapter; NOT COVERED; unread ranges
│   ├── dlb_calc.py                             # 29 calculation subcommands checked against the book
│   └── dlb_diagnose.py + dlb_tree.json         # training diagnosis tree (ch. 11) with pages
├── skills/                                     # dlb-topic-lookup, dlb-calculators, dlb-training-diagnosis (<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md                       # 40 conceptual cases (26 content, 14 limits/security)
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # 169 positive checks, 20 negative, 59 gap terms
    ├── run_script_tests.py                     # 81 deterministic cases
    └── fixtures/
```
A copy of the tests is also in `../../_agents_tests/deep-learning-goodfellow-expert/` (relative to the agent folder, `09_ai_and_llm/_agents_tests/deep-learning-goodfellow-expert/`).

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point the `deep-learning-goodfellow-expert/` directory (it contains `.claude-plugin/plugin.json`) as a local plugin (for example `claude --plugin-dir <path>/deep-learning-goodfellow-expert`) or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install deep-learning-goodfellow-expert@general-agents`.
- As a standalone agent: copy `agents/deep-learning-goodfellow-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@deep-learning-goodfellow-expert my training error is 20% and my test error 21%, target 5%: what do I do?` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root (Codex merges `AGENTS.md` per directory). `AGENTS.md` points to `agents/deep-learning-goodfellow-expert.md` as the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/deep-learning-goodfellow-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Using the scripts (run from the package folder)

```bash
python -I scripts/dlb_lookup.py "batch normalization"        # pages and reference
python -I scripts/dlb_lookup.py transformer                  # NOT COVERED (2016 book)
python -I scripts/dlb_lookup.py --gaps                       # gaps and unread ranges
python -I scripts/dlb_calc.py conv-out --m 32 --k 5 --pad valid --stride 2
python -I scripts/dlb_calc.py conv-cost                      # the book's 320x280 example (DLB p.355)
python -I scripts/dlb_calc.py info --p 0.9,0.1 --q 0.5,0.5 --base 2
python -I scripts/dlb_calc.py softmax --z 1000,1000,1000     # negative values: --z=-1000,-1000
python -I scripts/dlb_calc.py autodiff --expr "mul(add(x,y),x)" --vars x=2,y=3
python -I scripts/dlb_calc.py grad-mlp --layers 3,4,2 --act tanh --loss ce   # backprop vs finite differences
python -I scripts/dlb_calc.py optim --algo adam --x0 1,1 --curv 1,5 --steps 10
python -I scripts/dlb_diagnose.py --train-error 0.2 --test-error 0.21 --target 0.05
python -I scripts/dlb_diagnose.py --tree                     # full ch. 11 tree
python -I tests/run_script_tests.py --src <folder with DL-Deep-Learning-Goodfellow.txt>
python -I tests/verify_citations.py --src <folder with DL-Deep-Learning-Goodfellow.txt>
```
On Windows with Git Bash, use `python -I` normally; run from the package root.

## Boundaries and limitations
- **2016 book [DATED]:** numbers (rule of thumb of 5,000/10 million examples, ILSVRC), libraries (Theano, Torch, Caffe, TensorFlow), Adam defaults and RNN attention are from 2016. Details in `references/datado-desde-2016.md`.
- **NOT COVERED (verified by search):** Transformers, self-attention, BERT/GPT, LLMs, prompting, RLHF, LoRA, LayerNorm, ResNet, AdamW, GELU/Swish, modern diffusion, normalizing flows, PyTorch/JAX/TPU, scaling laws. LLMs/prompting/agents belong to other agents in the `09_ai_and_llm` collection.
- **Part III and gaps:** minimal coverage; the agent says "this package did not read it" where applicable.
- **Scripts:** formulas from the cited pages; derived formulas (stride, operation counts) are `[inference]` and marked.
- **Independent testing:** the cases were checked by the package author; **there was no blind run by an independent model** (see `tests/relatorio-de-fidelidade.md`).
- Copyright: content distilled in own words, without extensive reproduction of text, tables or figures.

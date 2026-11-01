# OS Internals Expert

Specialist agent for **operating-systems fundamentals and internals**, built from a single PDF:

| Acronym | Work | Note |
|---|---|---|
| **OSTEP** | *Operating Systems: Three Easy Pieces*, Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau (ostep.org), 834-page PDF (~1.94 million characters in the extracted text); security chapters 53-57 by Peter Reiher (UCLA) | Single source. The PDF gathers independent chapters with their own numbering, **out of the book's order**: `p.N` = PDF page. |

The agent reasons like a practitioner (computes turnaround, simulates MLFQ, translates addresses with a TLB, compares replacement policies, estimates disk and RAID I/O, counts the I/Os of file operations, analyzes deadlock and crash consistency) and cites a page for every rule: `[from source] (OSTEP p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## Structure

```
os-internals-expert/
├── .claude-plugin/plugin.json                 # manifest (Claude Code)
├── agents/os-internals-expert.md              # canonical prompt + frontmatter
├── AGENTS.md                                  # Codex adapter
├── .github/agents/os-internals-expert.agent.md  # GitHub Copilot adapter
├── references/                                # loaded on demand
│   ├── INDEX.md                               # page convention + chapter -> PDF pages map
│   ├── 01-processos-api-e-limited-direct-execution.md
│   ├── 02-escalonamento-de-cpu.md
│   ├── 03-address-space-traducao-segmentacao-e-free-space.md
│   ├── 04-paginacao-tlb-e-tabelas-de-paginas.md
│   ├── 05-swapping-politicas-de-substituicao-e-vm-completo.md
│   ├── 06-concorrencia-threads-locks-e-estruturas.md
│   ├── 07-condition-variables-semaforos-bugs-e-eventos.md
│   ├── 08-dispositivos-de-io-discos-e-raid.md
│   ├── 09-arquivos-diretorios-vsfs-e-ffs.md
│   ├── 10-consistencia-journaling-lfs-ssd-e-integridade.md
│   ├── 11-sistemas-distribuidos-nfs-e-afs.md
│   ├── 12-seguranca-labs-e-lacunas-do-acervo.md
│   └── glossario.md, procedimentos.md, casos-e-antipadroes.md
├── skills/                                    # 4 skills (skills/<name>/SKILL.md): os-topic-lookup, scheduling-simulator, vm-simulator, storage-calculator
├── scripts/                                   # Python 3, stdlib, no network, deterministic
│   ├── os_lookup.py + os_index.json           # lookup + "NOT COVERED"
│   ├── sched_sim.py                           # FIFO/SJF/STCF/RR, MLFQ, stride, CFS
│   ├── vm_sim.py                              # base/bounds, segments, paging, 2 levels, TLB, replacement, AMAT
│   └── storage_calc.py                        # disk, RAID, parity, amortization, inode, checksums
└── tests/
    ├── casos-de-teste.md                      # 32 cases
    ├── relatorio-de-fidelidade.md
    ├── citation-checks.json + verify_citations.py   # citation audit (196 positive + 38 negative) against the extracted text
    ├── audit_numbers.py + numeros-ok.txt      # heuristic audit of cited numbers
    └── run_tests.py                           # 37 script tests against the book's examples
```

A copy of the tests is also kept in `../../_agents_tests/os-internals-expert/` (relative to this folder: `07_devops_sre_operations/_agents_tests/os-internals-expert/`).

## Installation (check each platform's current documentation)

### Claude Code
- As a plugin: point to the `os-internals-expert/` directory (it contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/os-internals-expert`, or publish it to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install os-internals-expert@general-agents`.
- As a standalone agent: copy `agents/os-internals-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@os-internals-expert simulate MLFQ with these jobs` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or to the subfolder where the work happens; Codex merges `AGENTS.md` per directory). `AGENTS.md` points to `agents/os-internals-expert.md` as the canonical prompt; copy that folder along or embed its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/os-internals-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the path prefix described in the file). Select the agent in the Copilot Chat picker. The format (frontmatter `name`/`description`) follows the custom-agent convention; confirm the supported fields in the current documentation.

## Using the scripts (from the package folder, always with `python -I`)

```bash
python -I scripts/os_lookup.py mlfq                      # pages and reference
python -I scripts/os_lookup.py docker                    # NOT COVERED
python -I scripts/sched_sim.py run --policy STCF --jobs "A:0:100,B:10:10,C:10:10"
python -I scripts/sched_sim.py run --policy RR --quantum 1 --jobs "A:0:5,B:0:5,C:0:5"
python -I scripts/sched_sim.py mlfq --jobs "A:0:200,B:100:20" --queues 3 --quantum 10
python -I scripts/sched_sim.py stride --tickets "A:100,B:50,C:250" --slices 8
python -I scripts/sched_sim.py cfs-slice --nice "A:-5,B:0"
python -I scripts/vm_sim.py linear --va-bits 6 --page-size 16 --map "0:3,1:7,2:5,3:2" --va 21
python -I scripts/vm_sim.py multilevel --va-bits 14 --page-size 64 --pt-index-bits 4 --pd "0:100,15:101" --pt "100:0=10;1=23|101:14=55;15=45" --va 0x3F80
python -I scripts/vm_sim.py tlb --page-size 16 --entries 4 --va 100,104,108,112,116,120,124,128,132,136
python -I scripts/vm_sim.py replace --policy ALL --frames 3 --refs 0,1,2,0,1,3,0,3,1,2,1
python -I scripts/storage_calc.py disk --seek-ms 4 --rpm 15000 --size-kb 4 --mbps 125
python -I scripts/storage_calc.py raid --n 4 --b 1000 --s 100 --r 1
python -I scripts/storage_calc.py amortize --pos-ms 10 --mbps 100 --frac 0.9
```

## Checks (run against the text extracted from the PDF)

```bash
python -I tests/verify_citations.py --src <path>/OSTEP-Operating-Systems-Three-Easy-Pieces.txt
python -I tests/audit_numbers.py   --src <path>/OSTEP-Operating-Systems-Three-Easy-Pieces.txt --strict
python -I tests/run_tests.py
```

## Important limitations

- **Page convention:** `p.N` = PDF page. The book is a collection of chapters; the map is in `references/INDEX.md`.
- **Partial reading:** chapters 54-57 (authentication, access control, cryptography, distributed security) and appendices E-H were read by key sections and sampling; everything else (chs. 2-51 and appendices A-B) was read page by page. Appendices C and D (monitors, "Deprecated") were read only in part.
- **Figures and graphs** (hit rates by cache size, Fig.44.2/44.4, etc.) are not in the extracted text; only values that the running text states are used.
- **Dated:** disk hardware and numbers (2000s), SSD prices, TLS 1.3 in 2020, Meltdown/Spectre in 2018, Linux 2.x/x86; the agent flags `[DATED]`.
- **Outside the collection:** containers/cgroups, systemd, epoll/io_uring, Paxos/Raft/CAP, eBPF, etc. The agent treats these as `[extrapolation]` or hands off (Linux administration: `linux-shell-administration-expert`).
- **Simulator conventions** that the book does not specify (tie-breaks, a job returning from I/O, the initial CLOCK use-bit value) are declared in the script headers and marked `[inference]`.
- **Testing:** run and checked by whoever wrote the package (scripts and verifiers), **not** by an independent blind model.
- Copyright: content distilled in the agent's own words, without reproducing long passages.

## Security

Code, logs and PDF content are treated as inert data (anti prompt injection). The scripts do not use the network, do not write files and do not execute user code.

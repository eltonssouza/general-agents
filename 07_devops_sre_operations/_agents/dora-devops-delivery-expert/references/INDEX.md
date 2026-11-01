# Reference index - dora-devops-delivery-expert

Single source: **DORA24** = *Accelerate State of DevOps 2024* (Google Cloud / DORA), v. 2024.3, 120 pages, CC BY-NC-SA 4.0 license (p.118). Research report (survey + 11 interviews), not a textbook.

## Page convention
PDF page = printed number in the footer (checked on several pages; e.g., printed p.14 is the 14th PDF page). No conversion map is needed. Always cite `(DORA24 p.N)` or `(DORA24 p.N-M)`. Pages 118-120 are license/blank.

## Report map (DORA24)
| Pages | Chapter |
|---|---|
| 3-8 | Executive summary (key findings, improvement cycle) |
| 9-16 | Software delivery performance (four keys, rework, clusters) |
| 17-26 | AI: adoption and attitudes |
| 27-46 | Exploring the downstream impact of AI |
| 47-56 | Platform engineering |
| 57-68 | Developer experience (user-centricity, docs, priorities) |
| 69-76 | Leading transformations (leadership, data, cloud, J-curve) |
| 77-82 | A decade with DORA |
| 83-84 | Final thoughts |
| 85-90 | Acknowledgments and authors |
| 91-98 | Demographics and firmographics |
| 99-112 | Methodology |
| 113-116 | Models |
| 117 | Recommended reading |

## When to open each file
| User trigger | Open |
|---|---|
| four keys, lead time, deploy frequency, failure rate, recovery, rework, elite/high/medium/low levels, "what is our level", how to measure | `metricas-de-entrega-e-niveis.md` + `scripts/dora_classify.py` |
| AI: adoption, trust, productivity, delivery impact, AI strategy, batch size | `ia-adocao-e-impacto.md` |
| internal platform, golden path, IDP, platform engineering, throughput dropped after platform | `plataformas-internas.md` |
| user focus, documentation, unstable priorities, leadership, cloud, J-curve, culture, DORA history | `experiencia-cultura-lideranca-e-transformacao.md` |
| "is this causal?", sample, 89% interval, Bayesian, limits, how to cite numbers honestly | `metodologia-e-limites-estatisticos.md` |
| term definition | `glossario.md` |
| step by step (baseline, cycle, assess AI/platform, business case, internal survey) | `procedimentos.md` |
| pitfalls, anti-patterns | `casos-e-antipadroes.md` |
| "does the report cover X?", dated content, inconsistencies | `lacunas-e-conteudo-datado.md` |
| specific number/effect per capability | `scripts/dora_effects.py` |
| locate the page of a topic | `scripts/dora_lookup.py` |

## Scripts (see README)
- `scripts/dora_lookup.py` - topic -> pages; "NOT COVERED".
- `scripts/dora_classify.py` - compares the metrics of ONE application with the 2024 clusters (p.13).
- `scripts/dora_effects.py` - published effects (per +25% or contrast), page, crosses zero (visual reading).
- `scripts/dora_index.json` - data for the scripts.
- `tests/verify_citations.py` + `tests/citation-checks.json` - citation audit (positive and negative).

## Labels
[from source] (reading confirmed on the cited page) | [inference] (direct deduction) | [extrapolation] (outside the report) | [DATED] (may have changed). "From source" here means "from the report".

## Figures read as images (rendered)
Pg. 14 (fig.1), 15 (elite vs low box), 20 (fig.3), 32 (fig.7), 37 (fig.9), 39 (fig.10), 42 (fig.11), 50 (fig.14), 72 (fig.18). Figure values come from the figure labels; "interval crosses zero" is a visual reading and may contain reading errors.

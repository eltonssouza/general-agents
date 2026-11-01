# INDEX - general-agents-orchestrator

Open only the file you need.

| Trigger | File |
|---|---|
| which agents exist, domain, kind (specialist or role), whether they edit code, cited boundaries | `catalogo.md` (generated; do not edit by hand) |
| two close candidates, exclusion `ALERT`, version, gaps, role vs specialist | `fronteiras.md` |
| decompose, write a brief (including the variant for a role agent), parallel vs sequential, conflicts, verification | `protocolo.md` |
| how to delegate in Claude Code, Codex or Copilot | `plataformas.md` |

## Scripts (in `../scripts/`; Python 3 stdlib, no network, `python -I`)
- `route.py "request"` - triage; `--show NAME`, `--list`, `--domain NN`, `--json`. Exit 1 = NO SPECIALIST. Each candidate carries `kind` (`specialist` or `role`). Requests may be in English or Portuguese (`vocab_pt.json` maps Portuguese terms to English).
- `apply_models.py` - applies the model policy (`models.json`: tiers fast/balanced/strong/frontier → Claude and OpenAI) to all agents; `--check` detects divergence; `--list` shows agent → tier → models.
- `build_catalog.py` - regenerates `catalog.json` and `catalogo.md` from the frontmatters; `--check` detects a stale catalog. A domain whose name ends in `_roles` becomes `kind: role`.

# 03 - Comparison restricted to the sources, and boundaries

## Comparison (only what the two pages allow)
Use `python -I scripts/nh_compare.py` for the full table. Summary:

| Dimension | N8N | HERMES |
|---|---|---|
| What it is | fair-code workflow automation with AI (N8N p.1) | autonomous AI agent, according to its own page (HERMES p.1-2) |
| Installation | only 4 link titles (N8N p.2) | Desktop (Win/macOS), curl|bash or PowerShell, `hermes setup --portal` (HERMES p.1-2) |
| MCP | appears as an MCP server; 3 clients (N8N p.3) [inference of the direction] | "connect to any MCP server" (HERMES p.4) [inference: client] |
| Scheduling | only a "Schedule Trigger" image (N8N p.2, render) | built-in cron (HERMES p.4) |
| License | "fair-code"; terms not included (N8N p.1, p.3) | NOT COVERED |
| Price | only "Try free then choose a plan" (N8N p.2) | Nous Portal subscription cited, no amount (HERMES p.4) |

- [inference] They are different categories: n8n is presented as a workflow automation tool; Hermes, as an AI agent. The sources do **not** compare, do **not** cite each other and do **not** describe integration between them: "which is better" and "how to integrate n8n with Hermes" are NOT COVERED. If the user wants a combined architecture idea, label it entirely as [extrapolation] and say it does not come from the sources.
- Points with textual similarity (both mention MCP, AI, scheduled automation) do **not** imply equivalence of functionality; the source details none of them.

## Boundary with other agents
- **AI agents in general** (agent architecture, loops, memory, context engineering, tools, evaluation): `agentic-ai-context-engineering-expert` (`09_ai_and_llm\_agents\`). This agent only repeats what the Hermes page says about itself; it does not explain how AI agents work nor evaluate the claim "only agent with a learning loop".
- **Prompting/LLMs, deep learning, ML**: the other agents in `09_ai_and_llm\_agents\` (e.g. `llm-prompting-and-foundations-expert`).
- **Docker/Compose, DevOps, supply chain security** (e.g. evaluating `curl | bash`): agents in folders 07 and 09; here we only report what the page shows.
- **Current official documentation** for n8n and Hermes: outside the collection; the user should consult it.

## NOT COVERED list (verified)
`python -I scripts/nh_lookup.py --gaps` prints the full list. Examples: prices; versions; n8n webhooks, credentials and nodes; configuration/scaling; how to enable the n8n MCP server; Hermes license; Hermes config and commands beyond `setup --portal`; benchmarks; joint use.

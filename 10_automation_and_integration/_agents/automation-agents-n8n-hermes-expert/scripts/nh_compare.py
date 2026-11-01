# -*- coding: utf-8 -*-
"""
nh_compare.py - side-by-side comparator, restricted to what the two landing pages say.

Usage (package root; always python -I):
  python -I scripts/nh_compare.py                      # all dimensions
  python -I scripts/nh_compare.py --dim mcp instalacao # specific dimensions (English aliases accepted: installation, ...)
  python -I scripts/nh_compare.py --list               # dimension names
  python -I scripts/nh_compare.py --json
  python -I scripts/nh_compare.py --so-lacunas         # only NOT COVERED cells (alias: --only-gaps)

Each cell has a status (COVERED | PARTIAL | NOT COVERED), paraphrased text and a "N8N p.N" /
"HERMES p.N" citation (PDF page). There is no "which is better" verdict: the sources do not compare the products
(n8n = workflow automation tool; Hermes = AI agent; different categories [inference]).
Claims about Hermes come from the project itself (promotional text) and are not verified.
Read-only, no network, deterministic.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SC = "NOT COVERED"


def c(status, texto, cite=""):
    return {"status": status, "texto": texto, "cite": cite}


DIMENSOES = {
    "natureza": {
        "titulo": "What it is",
        "N8N": c("COVERED", "A fair-code licensed workflow automation tool that combines AI capabilities with business process automation.", "N8N p.1"),
        "HERMES": c("COVERED", "An autonomous, 'self-improving' AI agent from Nous Research; not an IDE-bound copilot nor a chatbot wrapper (the page's own claim).", "HERMES p.1-2"),
    },
    "licenca": {
        "titulo": "License",
        "N8N": c("PARTIAL", "Says 'fair-code'; the 'Sustainable use license' link appears in the footer, without the terms. Do not state whether it is open source.", "N8N p.1, p.3"),
        "HERMES": c(SC, "The source does not state the license (it only points to the 'View on GitHub' button).", "HERMES p.1"),
    },
    "instalacao": {
        "titulo": "Installation / getting started",
        "N8N": c("PARTIAL", "Four link titles: free trial and plan choice, one-line setup, installation via Docker Compose, use of a cloud provider. No steps or commands.", "N8N p.2"),
        "HERMES": c("COVERED", "Windows/macOS: Hermes Desktop installer (installs CLI and desktop). CLI only: curl|bash command (Linux/macOS/WSL2/Android Termux) or an iex/irm command in PowerShell (native Windows). Then: 'hermes setup --portal'.", "HERMES p.1-2"),
    },
    "hospedagem": {
        "titulo": "Where/how it runs",
        "N8N": c("PARTIAL", "Only the titles 'Install using Docker Compose' and 'Use a cloud provider'; nothing on requirements or scaling.", "N8N p.2"),
        "HERMES": c("COVERED", "Claims to run on a US$ 5 VPS, a GPU cluster or serverless (Daytona, Modal); 6 terminal backends: local, Docker, SSH, Daytona, Singularity, Modal.", "HERMES p.2-3"),
    },
    "ia": {
        "titulo": "Role of AI",
        "N8N": c("PARTIAL", "Says it combines AI with automation; examples only as titles: 'AI agent chat' and 'Scrape and summarize webpages with AI'.", "N8N p.1-2"),
        "HERMES": c("COVERED", "AI is the product: learning loop (curated memory, skill creation and improvement, FTS5 recall, user modeling with Honcho); works with Nous Portal, OpenRouter, OpenAI or any endpoint.", "HERMES p.3-4"),
    },
    "mcp": {
        "titulo": "MCP",
        "N8N": c("COVERED", "Three cards to connect Claude Desktop, Claude Code and OpenAI Codex to the 'n8n MCP server'; 'claude mcp add' and 'codex mcp add' commands with URL /mcp-server/http (host blank in the capture). Direction: n8n appears as an MCP server [inference from the label].", "N8N p.3"),
        "HERMES": c("COVERED", "Says it supports connecting to any MCP server (client role [inference]); the 'MCP Integration' and 'Use MCP with Hermes' pages are only pointed to.", "HERMES p.3-4"),
    },
    "agendamento": {
        "titulo": "Scheduling",
        "N8N": c("PARTIAL", "No text; the image of a card on p.2 shows a node labeled 'Schedule Trigger' (seen in the render, not in the text).", "N8N p.2 [render]"),
        "HERMES": c("COVERED", "Built-in cron with delivery to any platform; syntax not covered.", "HERMES p.4"),
    },
    "integracoes": {
        "titulo": "Integrations / channels",
        "N8N": c("PARTIAL", "Only the menu names 'Nodes' and 'Connect'; no specific app or node is described (except the 3 MCP clients).", "N8N p.1, p.3"),
        "HERMES": c("COVERED", "Over 20 messaging platforms from one gateway (Telegram, Discord, Slack, WhatsApp, Signal, Teams etc.).", "HERMES p.4"),
    },
    "memoria": {
        "titulo": "Memory / learning",
        "N8N": c(SC, "The source does not address memory or learning.", ""),
        "HERMES": c("COVERED", "Persistent memory across sessions, skills created and improved by the agent; mechanisms not explained.", "HERMES p.1, p.3"),
    },
    "seguranca": {
        "titulo": "Security",
        "N8N": c("PARTIAL", "Only the 'Security' link in the footer.", "N8N p.3"),
        "HERMES": c("PARTIAL", "The 'Security' page is pointed to: command approval, authorization, container isolation; no details.", "HERMES p.3"),
    },
    "preco": {
        "titulo": "Price / plans",
        "N8N": c("PARTIAL", "Only the title 'Try free then choose a plan'; no amounts.", "N8N p.2"),
        "HERMES": c("PARTIAL", "Mentions 'one subscription' to the Nous Portal that bundles the web tools; no amount. The US$ 5 is the cited cost of a VPS.", "HERMES p.2, p.4"),
    },
    "versao": {
        "titulo": "Version / date",
        "N8N": c("PARTIAL", "No version; '(c) 2026 n8n' and 'Last updated 5 days ago' (relative).", "N8N p.3-4"),
        "HERMES": c(SC, "No version or date.", ""),
    },
    "desempenho": {
        "titulo": "Benchmarks / performance / limits",
        "N8N": c(SC, "Nothing in the source.", ""),
        "HERMES": c(SC, "Nothing in the source; only promotional claims without data.", ""),
    },
    "integracao-mutua": {
        "titulo": "Using n8n and Hermes together",
        "N8N": c(SC, "The source does not mention Hermes.", ""),
        "HERMES": c(SC, "The source does not mention n8n.", ""),
    },
    "recomendacao": {
        "titulo": "Which to choose",
        "N8N": c(SC, "The sources do not compare products or recommend one.", ""),
        "HERMES": c(SC, "The sources do not compare products or recommend one.", ""),
    },
}


# English aliases for the (Portuguese-named) dimension identifiers
ALIASES = {
    "nature": "natureza", "license": "licenca", "installation": "instalacao", "hosting": "hospedagem",
    "scheduling": "agendamento", "integrations": "integracoes", "memory": "memoria", "security": "seguranca",
    "price": "preco", "version": "versao", "performance": "desempenho", "mutual-integration": "integracao-mutua",
    "recommendation": "recomendacao",
}


def render(dims, only_gaps):
    print("COMPARISON RESTRICTED TO THE SOURCES (N8N = n8n-Docs.pdf; HERMES = Hermes-Agent-Docs.pdf; page = PDF page)\n")
    for k in dims:
        d = DIMENSOES[k]
        cells = [(f, d[f]) for f in ("N8N", "HERMES")]
        if only_gaps and not any(x["status"] == SC for _, x in cells):
            continue
        print(f"## {k}: {d['titulo']}")
        for f, x in cells:
            ref = f" ({x['cite']})" if x["cite"] else ""
            print(f"  {f:<6} [{x['status']}]{ref} {x['texto']}")
        print()
    print("Notes: (1) no verdict: the sources do not compare the two; (2) n8n = workflow automation, Hermes = AI agent "
          "[inference: different categories]; (3) Hermes claims are the project's own promotional text; "
          "(4) content of pointed-to links/sections is NOT in the sources.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dim", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--so-lacunas", "--only-gaps", dest="so_lacunas", action="store_true")
    a = ap.parse_args()
    if a.list:
        for k, v in DIMENSOES.items():
            print(f"{k}\t{v['titulo']}")
        return 0
    dims = [ALIASES.get(d, d) for d in a.dim] if a.dim else list(DIMENSOES)
    bad = [d for d in dims if d not in DIMENSOES]
    if bad:
        print(f"NOT COVERED: unknown dimension(s): {', '.join(bad)}. Use --list.", file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps({k: DIMENSOES[k] for k in dims}, ensure_ascii=False, indent=2))
        return 0
    render(dims, a.so_lacunas)
    return 0


if __name__ == "__main__":
    sys.exit(main())

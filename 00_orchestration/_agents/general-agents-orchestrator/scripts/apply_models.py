# -*- coding: utf-8 -*-
"""
apply_models.py - applies the model policy (scripts/models.json) to every agent of the collection.

For each package <ROOT>/NN_*/_agents/<name>/ (including this orchestrator, in 00_*):
  - agents/<name>.md (Claude Code): "model: <alias>" line in the frontmatter (opus, sonnet or haiku);
  - .github/agents/<name>.agent.md (GitHub Copilot): "model: ['<claude>', '<gpt>']", in preference order;
  - AGENTS.md (Codex): block between <!-- modelo:inicio --> and <!-- modelo:fim --> with the recommended model.
The tier of each agent comes from "exceptions" or, if absent, from "default" by kind: orchestrator (00_*),
role (domain ending in _roles) or specialist. Preserves the line ending (LF/CRLF) of each file.

Usage (from the package root; always with python -I):
  python -I scripts/apply_models.py            # write
  python -I scripts/apply_models.py --check    # compare only; exit 1 if any package diverges from the policy
  python -I scripts/apply_models.py --list     # agent -> tier -> models
No network; stdlib. Exit: 0 = ok; 1 = divergence (--check); 2 = error.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DOMAIN_RE = re.compile(r"^\d{2}_[a-z0-9_]+$")
START, END = "<!-- modelo:inicio -->", "<!-- modelo:fim -->"


def load_policy():
    with open(os.path.join(HERE, "models.json"), encoding="utf-8") as f:
        pol = json.load(f)
    for k, t in list(pol["default"].items()) + list(pol["exceptions"].items()):
        if t not in pol["tiers"]:
            raise ValueError("unknown tier '%s' for '%s'" % (t, k))
    return pol


def kind_of(domain):
    if domain.startswith("00_"):
        return "orchestrator"
    return "role" if domain.endswith("_roles") else "specialist"


def packages(root):
    for dom in sorted(os.listdir(root)):
        base = os.path.join(root, dom, "_agents")
        if not DOMAIN_RE.match(dom) or not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            pkg = os.path.join(base, name)
            if os.path.isfile(os.path.join(pkg, "agents", name + ".md")):
                yield dom, name, pkg


def resolve(pol, dom, name):
    tier = pol["exceptions"].get(name) or pol["default"][kind_of(dom)]
    return tier, pol["tiers"][tier]


def set_frontmatter(text, key, value):
    nl = "\r\n" if "\r\n" in text else "\n"
    m = re.match(r"^---\r?\n(.*?)(\r?\n)---(\r?\n|$)", text, re.S)
    if not m:
        raise ValueError("no frontmatter")
    lines = m.group(1).split(nl) if nl == "\r\n" else m.group(1).split("\n")
    new = "%s: %s" % (key, value)
    idx = next((i for i, l in enumerate(lines) if re.match(r"^%s:" % key, l)), None)
    if idx is not None:
        lines[idx] = new
    else:
        after = next((i for i, l in enumerate(lines) if re.match(r"^tools:", l)), len(lines) - 1)
        lines.insert(after + 1, new)
    return "---" + nl + nl.join(lines) + m.group(2) + "---" + m.group(3) + text[m.end():]


def set_codex_block(text, tier, spec):
    nl = "\r\n" if "\r\n" in text else "\n"
    block = (START + nl + "**Recommended model** (tier `%s` of the collection policy, `00_orchestration/_agents/general-agents-orchestrator/scripts/models.json`): "
             "Codex/OpenAI `%s`; Claude `%s`." % (tier, spec["openai"], spec["claude"]) + nl + END)
    if START in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, count=1, flags=re.S)
    m = re.search(r"^# .*$", text, re.M)
    if not m:
        return block + nl + nl + text
    end = m.end()
    return text[:end] + nl + nl + block + text[end:]


def targets(dom, name, pkg, tier, spec):
    out = [(os.path.join(pkg, "agents", name + ".md"), lambda t: set_frontmatter(t, "model", spec["claude"]))]
    cop = os.path.join(pkg, ".github", "agents", name + ".agent.md")
    if os.path.isfile(cop):
        val = "[" + ", ".join("'%s'" % m for m in spec["copilot"]) + "]"
        out.append((cop, lambda t: set_frontmatter(t, "model", val)))
    cdx = os.path.join(pkg, "AGENTS.md")
    if os.path.isfile(cdx):
        out.append((cdx, lambda t: set_codex_block(t, tier, spec)))
    return out


def main():
    ap = argparse.ArgumentParser(description="Applies the model policy to the collection agents.")
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    try:
        pol = load_policy()
        pkgs = list(packages(a.root))
    except (OSError, ValueError, KeyError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if not pkgs:
        print("ERROR: no agent in %s" % a.root, file=sys.stderr)
        return 2
    if a.list:
        for dom, name, _ in pkgs:
            tier, spec = resolve(pol, dom, name)
            print("%-45s %-13s %-9s Claude=%-7s OpenAI=%s" % (name, kind_of(dom), tier, spec["claude"], spec["openai"]))
        return 0
    stale, written, counts = [], 0, {}
    for dom, name, pkg in pkgs:
        tier, spec = resolve(pol, dom, name)
        counts[tier] = counts.get(tier, 0) + 1
        for path, fn in targets(dom, name, pkg, tier, spec):
            try:
                with open(path, "rb") as f:
                    old = f.read().decode("utf-8")
                new = fn(old)
            except (OSError, ValueError) as e:
                print("ERROR in %s: %s" % (os.path.relpath(path, a.root), e), file=sys.stderr)
                return 2
            if new != old:
                stale.append(os.path.relpath(path, a.root))
                if not a.check:
                    with open(path, "wb") as f:
                        f.write(new.encode("utf-8"))
                    written += 1
    resumo = ", ".join("%s=%d" % (t, counts[t]) for t in pol["tiers"] if t in counts)
    if a.check:
        if stale:
            print("DIVERGES from the policy (%d files): %s\nRun: python -I scripts/apply_models.py"
                  % (len(stale), ", ".join(stale[:10]) + (" ..." if len(stale) > 10 else "")))
            return 1
        print("OK: %d agents follow the model policy (%s)." % (len(pkgs), resumo))
        return 0
    print("Policy applied: %d agents (%s); %d files updated." % (len(pkgs), resumo, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())

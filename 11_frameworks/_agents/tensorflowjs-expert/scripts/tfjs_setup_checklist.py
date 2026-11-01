# -*- coding: utf-8 -*-
"""
tfjs_setup_checklist.py - TensorFlow.js setup checklist according to the TFJS text (Tutorial-Setup, 2023-11-15)
and the commands present in the source. Runs nothing, no network.

Usage:
  python -I scripts/tfjs_setup_checklist.py --target {browser-script,browser-npm,node-native,node-gpu,node-pure}
        [--os {linux,windows,macos,other}] [--typescript] [--strict-null] [--json]
  python -I scripts/tfjs_setup_checklist.py --quickstart     # minimal tutorial commands (TFJI)
Labels: [from source] is on the cited page; [inference] deduction; NOT COVERED when the source does not say.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_TAG = '<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>'

TARGETS = {
    "browser-script": {
        "titulo": "Browser with script tag",
        "itens": [
            ("[from source]", "Add to the main HTML: " + SCRIPT_TAG + " (closing inferred; the capture cuts the line)", "TFJS p.1-2"),
            ("[from source]", "With the tag, `tf` is available as a global variable; do not use import in this mode", "TFJS p.2"),
            ("[from source]", "Save as index.html; open with a double click or serve with `npx http-server` and open http://localhost:8080", "TFJS p.3"),
            ("[from source]", "Open the browser console to see the output; refreshing the page gives a new prediction", "TFJS p.3"),
            ("[inference]", "Load the script tag before the script that uses `tf` (the tutorial puts the library in the head and the ML script at the end of the body)", "TFJI p.2"),
        ],
        "comandos": ["npx http-server   # optional; then open http://localhost:8080 (answer y if asked to install)"],
    },
    "browser-npm": {
        "titulo": "Browser with NPM and build tool",
        "itens": [
            ("[from source]", "Use a build tool such as Parcel, webpack or Rollup", "TFJS p.1"),
            ("[from source]", "Install with npm or yarn", "TFJS p.3"),
            ("[from source]", "Import: import * as tf from '@tensorflow/tfjs';", "TFJS p.3"),
            ("NOT COVERED", "Build tool configuration and the exact Yarn command (does not appear in the extracted text)", "TFJS p.3"),
        ],
        "comandos": ["npm install @tensorflow/tfjs"],
    },
    "node-native": {
        "titulo": "Node.js with native C++ bindings (tfjs-node)",
        "itens": [
            ("[from source]", "Native TensorFlow execution accelerated by the TensorFlow C binary", "TFJS p.4"),
            ("[from source]", "Use require('@tensorflow/tfjs-node'); `tfjs` is imported indirectly by it", "TFJS p.4"),
            ("[from source]", "Additional details: the Node.js guide and the tfjs-node repository", "TFJS p.4"),
            ("NOT COVERED", "Node.js versions, system requirements and troubleshooting the native binary", "TFJS p.4"),
        ],
        "comandos": ["npm install @tensorflow/tfjs-node"],
    },
    "node-gpu": {
        "titulo": "Node.js with GPU (tfjs-node-gpu)",
        "itens": [
            ("[from source]", "Linux only", "TFJS p.5"),
            ("[from source]", "Requires an NVIDIA GPU with CUDA support", "TFJS p.5"),
            ("[from source]", "Use require('@tensorflow/tfjs-node-gpu'); `tfjs` is imported indirectly", "TFJS p.5"),
            ("NOT COVERED", "CUDA/driver versions (the page only points to the TensorFlow documentation)", "TFJS p.5"),
        ],
        "comandos": ["npm install @tensorflow/tfjs-node-gpu"],
    },
    "node-pure": {
        "titulo": "Node.js with pure JavaScript (tfjs)",
        "itens": [
            ("[from source]", "It is the same package as the browser one", "TFJS p.6"),
            ("[from source]", "It is the slowest Node.js option in performance", "TFJS p.6"),
            ("[from source]", "Use require('@tensorflow/tfjs')", "TFJS p.6"),
        ],
        "comandos": ["npm install @tensorflow/tfjs"],
    },
}

TS_ITEM = ("[from source]", "TypeScript with strict null checking: `skipLibCheck: true` may be needed in tsconfig.json to avoid compilation errors", "TFJS p.6")
QUICK = [
    "# prerequisites: Node.js and Yarn (TFJI p.1)",
    "# clone or download https://github.com/tensorflow/tfjs-examples (TFJI p.1)",
    "cd tfjs-examples/getting-started",
    "yarn install",
    "yarn watch",
    "# open http://127.0.0.1:1234 ; expect a number close to 39 (TFJI p.2)",
]


def build(a):
    t = TARGETS[a.target]
    itens = list(t["itens"])
    avisos = []
    if a.target == "node-gpu" and a.os and a.os != "linux":
        avisos.append(("WARNING", f"the text restricts tfjs-node-gpu to Linux; OS given: {a.os}. What to do on that OS is NOT COVERED; "
                       "[inference] consider tfjs-node (option 1) or tfjs (option 3)", "TFJS p.4-6"))
    if a.os and a.target.startswith("node") and a.target != "node-gpu":
        pass
    if a.typescript and a.strict_null:
        itens.append(TS_ITEM)
    elif a.typescript:
        itens.append(("[inference]", "TypeScript given without strict null checking: the skipLibCheck rule is conditioned on that checking; check for compilation errors", "TFJS p.6"))
    if a.strict_null and not a.typescript:
        avisos.append(("NOTE", "--strict-null only has an effect with --typescript", "TFJS p.6"))
    if a.target.startswith("node"):
        itens.append(("[from source]", "The same model snippet (dense 100 relu -> dense 1 linear, sgd, meanSquaredError, fit with 100 epochs and onEpochEnd) is used in the 3 Node options", "TFJS p.4-6"))
    return {"alvo": a.target, "titulo": t["titulo"], "itens": itens, "avisos": avisos, "comandos": t["comandos"],
            "fonte_data": "TFJS updated on 2023-11-15 UTC [DATED]"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=sorted(TARGETS))
    ap.add_argument("--os", choices=["linux", "windows", "macos", "other"])
    ap.add_argument("--typescript", action="store_true")
    ap.add_argument("--strict-null", dest="strict_null", action="store_true")
    ap.add_argument("--quickstart", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.quickstart:
        print("\n".join(QUICK))
        return 0
    if not a.target:
        ap.print_help()
        return 1
    r = build(a)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    print(f"Checklist: {r['titulo']}  ({r['fonte_data']})")
    for rot, txt, cit in r["avisos"]:
        print(f"  !! {rot}: {txt}  [{cit}]")
    for rot, txt, cit in r["itens"]:
        print(f"  [ ] {rot} {txt}  ({cit})")
    print("Commands present in the source (data; not executed):")
    for c in r["comandos"]:
        print("   ", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())

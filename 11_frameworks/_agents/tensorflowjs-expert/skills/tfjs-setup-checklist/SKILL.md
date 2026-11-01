---
name: tfjs-setup-checklist
description: Builds the TensorFlow.js setup checklist (browser with script tag or NPM, Node.js with tfjs-node, tfjs-node-gpu or pure tfjs, TypeScript) and the commands present in the source, without running anything. Use when the user asks "how do I set up TF.js on Node?", "does tfjs-node-gpu work on Windows?" or "which commands does the minimal tutorial use?". Do not use for installing CUDA or fixing native build errors.
---

# TensorFlow.js setup checklist

Sources: TFJS (Setup, 2023-11-15) and TFJI (Getting started); citation = code + PDF page of the capture. Everything is `[DATED]`; the captures carry no numbered version.

## Procedure

1. Find the target and run (runs nothing, no network):
   ```bash
   python -I <PKG>/scripts/tfjs_setup_checklist.py --target browser-script
   python -I <PKG>/scripts/tfjs_setup_checklist.py --target node-gpu --os windows [--typescript] [--strict-null] [--json]
   python -I <PKG>/scripts/tfjs_setup_checklist.py --quickstart
   ```
   (`<PKG>` = package root; from this skill, `../../`.) `--target`: `browser-script`, `browser-npm`, `node-native`, `node-gpu`, `node-pure`; `--os`: `linux`, `windows`, `macos`, `other`. Exit 0; without `--target` and without `--quickstart` it prints the help and exits with 1.
2. Interpret: `[ ]` items with label and citation, `!!` warnings (for example `tfjs-node-gpu` Linux only with CUDA, `[from source]` TFJS p.5) and the command list, which is data and is not executed. Labels: `[from source]` is on the cited page; `[inference]` is a deduction; "NOT COVERED" when the source does not say.
3. Do not run `npm`, `yarn` or `npx` for the user. Hand over the commands for them to run and confirm the result with them.

## Response format

Target and system — items with label and `(CODE p.N)` — warnings — commands for the user to run — what the captures do not cover (detailed CUDA, bundlers).

## Limits

Text checklist, not an environment diagnosis. Native installation, Node versions and drivers are outside the captures (NOT COVERED).

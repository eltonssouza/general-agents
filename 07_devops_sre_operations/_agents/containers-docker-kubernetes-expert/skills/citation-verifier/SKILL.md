---
name: citation-verifier
description: Checks the package's 83 page citations and 22 negative claims against the extracted text of the sources (Docker Handbook and Kubernetes Basics). Use when the user asks to "verify the package citations", "do the pages still match the PDF?" or after swapping the PDF extraction. Requires the source text or the PDFs with PyMuPDF. Do not use for topic lookups (that is docker-topic-lookup).
---

# Citation verification

Source: `../../scripts/citation-checks.json` (positive checks: terms required on the cited PDF page; negative: terms that must NOT appear on any page of the source).

## Procedure

1. Ask the user for the path of the extracted text (with `=== PAGE N ===` markers) or of the folder with the PDFs. Do not invent paths. Run (read-only, no network):
   ```bash
   python -I <PKG>/scripts/verify_citations.py --dockhb Docker-Handbook-freeCodeCamp.txt --k8sb Kubernetes-Basics-docs.txt
   python -I <PKG>/scripts/verify_citations.py --pdf-dir <folder with the PDFs> -v
   ```
   (`<PKG>` = package root; from this skill, `../../`.) Options: `--dockhb`, `--k8sb`, `--pdf-dir` (requires PyMuPDF/fitz), `--checks` (another JSON) and `-v` (lists the ones that passed).
2. Interpret: each `FAILURE` carries the id and the citation; the summary shows positive, negative, skipped (source not provided) and failures. Exit 0 = no failures; 1 = there are failures; 2 = sources not provided or PDF unreadable.
3. Do not fix citations on your own: report the failure, open the page in `../../references/` and propose the correction to the user.

## Response format

Summary (positive, negative, skipped, failures) — list of failures with id and probable cause — next step.

## Limits

It checks the presence of terms on the page, not the truth of the claim. PDF text extraction may vary between tools.

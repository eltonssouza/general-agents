# 2017 Overview: "Software Engineering at Google" (Fergus Henderson), abbreviation SWE-PREV

> Convention: pages = PDF page (see `INDEX.md`; the PDF's printed numbering equals the PDF's). Source: `Software-Engineering-at-Google.pdf` (20 pages). Note: this is NOT a "preview" of the book by Winters, Manshreck and Wright. It is the article by Fergus Henderson, dated 01/31/2017 (PDF p.1), which catalogs Google practices. The numeric data are from January 2015 and predate the book; [DATED] when compared with SWE-G (for example, the book cites about 50,000 engineers and more than two billion lines at the time of the PDF edition).

## 1. Facts from the article (all are "from the article")
- [from source] (SWE-PREV p.3-4) In January 2015 the repository had 86 terabytes, one billion files, more than 9 million source files, 2 billion lines, 35 million commits and about 40 thousand commits per working day. [DATED] SWE-G (p.239) speaks of 60,000 to 70,000 commits per working day; the sources differ by period.
- [from source] (SWE-PREV p.4) Almost all development happens at the head of the repository, not in branches; one "build cop" per team; each subtree can have an owners file and at least two owners are required (p.4).
- [from source] (SWE-PREV p.5) The build system (Blaze) uses declarative specifications in BUILD files; "individual build steps must be hermetic: they depend only on their declared inputs"; deterministic steps allow a cache shared between users; the build work is distributed across hundreds or thousands of machines. This is the textual origin of "hermetic" for builds in this corpus, and not Ch. 18 of SWE-G.
- [from source] (SWE-PREV p.6) Presubmits configurable per subtree (synchronous or asynchronous).
- [from source] (SWE-PREV p.6-7) Every change in the main repository must be reviewed by at least one other engineer (and by an owner when the author is not an owner). In exceptional cases, an owner can commit before review, with a named reviewer and automatic reminders (p.6). The author chooses reviewers freely, respecting the owner requirement (p.7). There is an "experimental" section of the repository with no review requirement (p.7).
- [from source] (SWE-PREV p.7-8) Small changes: the review tools labeled the size (30-99 lines "medium"; 300-999 "large"; 1000-1999 "freakin huge") and the footnote says recent versions use S, M, L, XL. This is the only point in the corpus where line ranges per size label appear. [inference] For comparison, SWE-G uses about 200 lines as the reference for "small" (SWE-G p.129).
- [from source] (SWE-PREV p.8) Unit tests are strongly encouraged; production code must have tests; load test before deploy ("de rigueur") with a latency and error-rate table; Buganizer for bugs.
- [from source] (SWE-PREV p.8-9) Five approved languages (C++, Java, Python, Go, JavaScript); style guides per language; "readability" required for changes with non-trivial new code; Protocol Buffers for interoperation.
- [from source] (SWE-PREV p.10) Release engineering: frequent releases (weekly or biweekly common; some teams daily); release from the last "green" build; release branch with cherry-picks; staging, canary servers and gradual rollout over a few days for high-traffic services.
- [from source] (SWE-PREV p.11-12) Launch approval (approvals from legal, privacy, security, reliability and business), mandatory postmortems after significant incidents, and "frequent rewrites" (frequent rewrites as a way to eliminate complexity and transfer knowledge).
- [from source] (SWE-PREV p.12-14) Management: 20% time, OKRs (target average score of 65%, not used directly in individual evaluation, p.13), reorganizations (p.14).
- [from source] (SWE-PREV p.14-18) People: separate engineering and management careers (p.15), engineering managers with typically between 3 and 30 people and most commonly between 8 and 12 (p.15), training, "Codelabs", mentor and buddy (p.17), performance evaluation (p.18).

## 2. How to use
- For canary practices and build hermeticity, the article is the explicit source; the SWE-G book uses "canarying" in a CI/CD context (SWE-G p.331) and describes phased rollouts (SWE-G p.351), but without the v1 package's numbers.
- To compare numbers between the two sources, always state the date and the source.

## 3. Limits
- The article is brief and descriptive; it does not bring in-depth justifications, risk tables or numeric code-quality limits.

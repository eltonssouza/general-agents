# Culture: Humility, Respect and Trust (SWE-G Ch. 2 and Ch. 3)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`. Ch. 2 "How to Work Well on Teams" (PDF p.28-39, Brian Fitzpatrick) and Ch. 3 "Knowledge Sharing" (PDF p.40-56, Nina Chen and Mark Barolak). Ch. 4 (Engineering for Equity, p.57-64) has only the note at the end of this file.

## 1. The genius myth and the risk of hiding (Ch. 2)
- [from source] (SWE-G p.28) The chapter's critical idea: software development is a team endeavor and behavior must reorganize around humility, respect and trust. The authors report requests to "hide" code/branches as a symptom of insecurity.
- [from source] (SWE-G p.29) "Genius Myth": the tendency to attribute a team's success to a single person (examples cited: Linus Torvalds, Guido van Rossum, Bill Gates). The book says the vast majority of the work does not require genius, but 100% requires a minimum of social skill.
- [from source] (SWE-G p.30) "Hiding Considered Harmful": working alone increases the risk of unnecessary failure. Arguments: early detection of design errors and reinventing the wheel (bicycle example), and the "bus factor".
- [from source] (SWE-G p.31) Bus factor: the number of people who need to be hit by a bus before the project is doomed; at least documentation plus a primary and a secondary owner per area are recommended. The book links this to "shifting left" and to short feedback cycles.
- [from source] (SWE-G p.32) Middle ground for physical space: groups of four to eight people in small rooms; the opinion is the chapter author's, and there is a note that introverts may need more quiet (p.39).
- [from source] (SWE-G p.32-33) "Software engineering is a team endeavor" (conclusion of the section "It's All About the Team").

## 2. The three pillars: humility, respect, trust
- Note on the acronym: the PDF uses "humility, respect, and trust" and "the three pillars" (SWE-G p.33); the acronym "HRT" does not appear in the book's text (search of the full PDF). [extrapolation] "HRT" is a common abbreviation used by the agent; the file name keeps it for link compatibility.
- [from source] (SWE-G p.33) Pillar 1, Humility: you are not the center of the universe, nor is your code; you are not omniscient or infallible; you are open to improving. Pillar 2, Respect: genuinely caring about colleagues. Pillar 3, Trust: believing that others are competent and will do the right thing, letting them lead when appropriate. The author states that the root-cause analysis of almost every social conflict ends up at the lack of one of these three.
- [from source] (SWE-G p.34) Practice: "lose the ego"; consider a "collective" ego. Receiving and giving criticism: "you are not your code" (p.35); constructive criticism is respectful and product-oriented, not about character; example of rephrasing "you got the flow wrong" as "I'm confused by the flow, would pattern X help?" (p.35).
- [from source] (SWE-G p.35-36) "Fail fast and iterate": the motto "Failure is an option" at Google; failing every now and then is a sign of taking risks (p.36). Note: repeating the same mistake without learning is incompetence, not failure (note 7, p.39).
- [from source] (SWE-G p.37) Being open to influence ("how much you influence depends on how open you are to being influenced"); admitting ignorance ("I don't know") raises status in the long run according to the authors.
- [from source] (SWE-G p.37-38) "Googley": an informal term that was eventually replaced by an explicit rubric (thrives in ambiguity, values feedback, challenges the status quo, puts the user first, cares about the team, does the right thing).

## 3. Blameless postmortem (Ch. 2)
- [from source] (SWE-G p.36) The key to learning from mistakes is to document failures with root-cause analysis and a postmortem; it must not be a list of excuses or culprits and must say what was learned and what will change. Suggested content: event summary, timeline, root cause, impact/damage, immediate actions (with owners), preventive actions and lessons learned.
- [from source] (SWE-G p.36) The section is called "Blameless Post-Mortem Culture". The book does NOT describe on these pages the hypothesis of "an accidental command causing a global outage" nor "prevention items such as terminal guardrails"; that was an addition by the v1 package. [extrapolation] The idea of systemic failure (protective guardrails) is compatible with the blameless culture, but it is general knowledge, not page text.

## 4. Knowledge sharing (Ch. 3)
- [from source] (SWE-G p.40-41) Premise: the organization needs a learning culture, which requires psychological safety to admit not knowing. Challenges listed: lack of psychological safety; "information islands" (with fragmentation, duplication and distortion of information); single point of failure (SPOF); "all or nothing" knowledge (a few experts and newcomers, no middle ground); "parroting" (copying without understanding); "haunted graveyards" (parts of the code that nobody dares touch out of fear).
- [from source] (SWE-G p.42) Psychological safety is described as the starting point; the internal research cited says it is the most important part of an effective team. Mentoring from the "Noogler's" arrival.
- [from source] (SWE-G p.43) The Recurse Center's social rules: no feigned surprise, no "well-actually", no "back-seat driving".
- [from source] (SWE-G p.52-54) Readability: at Google it means a standardized process of mentoring through code review to disseminate a language's best practices (idioms, structure, API design, library usage, documentation, test coverage); it started as one person's effort (Craig Silverstein, employee #3, p.53). To obtain Readability in a language, the engineer sends CLs to centralized reviewers (p.54).
- [from source] (SWE-G p.55) TL;DR: psychological safety is the foundation; start small (ask and write); there is no silver bullet.

## 5. Ch. 4 (equity) only as a boundary
- [from source] (SWE-G p.63) TL;DR of Ch. 4: bias is the default; diversity is needed to design for a broad base; it is better to slow down than to launch something that may cause harm to some users. This package does not go deeper into Ch. 4.

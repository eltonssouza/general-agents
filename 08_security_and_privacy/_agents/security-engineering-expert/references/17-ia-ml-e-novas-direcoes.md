# 17. AI/ML and security; information warfare, DRM and telephony (Ch. 25 and excerpts of chs. 22-24)

Convention: "SE3 p.N" = PDF page; printed = PDF − 33 (ch. 25). Reading: **25.3 (AI/ML) p.907-915 in full**; the rest of ch. 25 (autonomous vehicles/drones, PETs and opsec, elections, p.898-906 and 916-941) was NOT read. Chs. 23 and 24: only the summaries (p.846-847 and 896-897). The state of the art in AI is from 2020 — strongly `[DATED]`: do not use it to assess current LLMs/generative AI (NOT COVERED).

## 1. ML and security (SE3 p.907-909)
- `[from source]` ML entered security in the 90s (AV, payment fraud, spam); spam uses user feedback as "ground truth" — spammers send spam to their own accounts and mark "not spam"; classifier **poisoning**; attacks exploit the value chain (an innocent ticket swapped for a high-risk destination) (SE3 p.908-909).

## 2. Four types of attack on ML systems (SE3 p.909-911)
1. **Poisoning training data** (Tay, 2016: shut down in 16 hours) (SE3 p.909).
2. **Integrity at inference:** *adversarial samples*; the high-dimensional decision space makes blind spots "mathematically inevitable"; stickers make a car read 30 mph as 60 mph; nonlinear classifiers are no harder to evade than linear ones (SE3 p.909-910).
3. **Confidentiality at inference:** model extraction by queries (works with networks, logistic regression, trees); transferable attacks (white-box → black-box); keys in neural networks change the blind spots ("Kerckhoffs holds in ML"); large networks memorize outliers — "it's not personal data because it's statistical learning" requires care; ML + differential privacy is active research (SE3 p.910).
4. **Denial of service:** samples that make the classifier slow down (20% longer in a direct pipeline; hundreds of times in NLP with exception handling) (SE3 p.910).

## 3. How to use ML safely (SE3 p.911)
`[from source]` End-to-end systems approach (sanitize inputs, pentest, disclosure, update); ML has been ineffective in network IDS (lack of training data, theory-practice gap, difficult evaluation, high cost of error and above all inability to handle new attacks); reduce its sensitivity and complement it with other sensors, or make it fragile so it triggers an alarm and enters defensive mode ("Am I under attack now?"); "when ML blurs the boundary between code and data, people will manipulate the system" (SE3 p.911).

## 4. ML and society (SE3 p.912-915)
- Bias (translation: "he" for doctor, "she" for nurse; systems "inhale" the prejudices in the data); redlining; "opaque rules may run against European data protection law" (SE3 p.912).
- **Snake oil** (Narayanan): ML has made real progress in *perception* (faces, voice, medical images), some in *judgment* (spam, hate speech; depends on humans) and **none in social prediction** (employee performance, crime; simple linear regressions with few variables work just as well) (SE3 p.913). 40% of "AI" startups do not use ML in any material way (SE3 p.913). First stop for ethics: existing law and policy; predictive policing and ML in bail/sentencing propagate biases (SE3 p.914). Summary: ML entrenches big tech's power and pushes the balance toward surveillance (SE3 p.915).

## 5. Telephony, electronic warfare, DRM — summaries only
- Telephony (ch. 22): see `09-seguranca-de-redes-e-malware.md` §5.
- Electronic warfare (ch. 23, p.846-847): "the great majority of information operations in 2010-20 were psychological and propaganda"; similarities between decoys/jamming against radar and manipulation of public opinion (SE3 p.846-847).
- DRM/copyright (ch. 24, p.896-897): technical copy protection is a "wicked problem"; computers copy bitstrings at zero cost and DRM caused collateral damage; anti-cheat privacy is an open problem (SE3 p.896-897).

## Triggers and boundary
- "Is my classifier/ML safe?" → §2-§3 (use as a conceptual checklist, labeling `[extrapolation]` for LLMs, prompt injection, foundation models — which the book does not cover).
- Autonomous vehicles, PETs (Tor/opsec), electronic elections: NOT COVERED in what was read (p.898-906, 916-941).

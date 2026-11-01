# 10. Inference control, anonymization, differential privacy and data policy (Ch. 11; excerpts of 26)

Convention: "SE3 p.N" = PDF page; printed = PDF − 42 (ch. 11) and − 33 (ch. 26). Reading: ch. 11 in full; ch. 26 only p.981-996 (forensics, data protection, FOI, summary). **Not read:** surveillance, crypto wars, terrorism, censorship (p.942-980). 2020 data (`[DATED]`): US census, GDPR/Safe Harbour/Privacy Shield, scandals.

## 1. The thesis
- `[from source]` "Anonymized data" is an aspiration; there have been four waves of research (census 70-80s; health 90s; search/preferences 2000s + differential privacy 2006; social/genomics/location 2010s) (SE3 p.417-418). "A gulf between what anonymization can do and what stakeholders want to believe" (SE3 p.418).
- `[from source]` Anonymization works in well-defined cases (e.g. census, with DP theory); with rich data reidentification is easy; "it will probably take a scandal to change this" (SE3 p.443).

## 2. Classical theory (SE3 p.419-425)
- Two approaches: sanitize once before publishing vs query control; mathematically equivalent (SE3 p.419). *Rule of three*, *trackers* (SE3 p.419-420).
- **Notation:** characteristic formula, query set, cells; D (disclosed) ⊆ P' (complement of the sensitive) for privacy; D = P' = precise protection (SE3 p.420).
- **Query set size control:** minimum t, and between t and N−t records; avoid successive queries K ⊂ L with |L|−|K| < t; general trackers are easy to find if n < N/4; auditing queries is NP-complete (SE3 p.420-421). *Complementary cell suppression*: suppressing one cell in m-tuples implies suppressing 2^m − 1 others (SE3 p.421-422).
- **k-anonymity:** an operational definition (not a property); useless if the k share the sensitive attribute; "33 bits are enough to identify a human" (SE3 p.422-423). n-respondent k%-dominance; query overlap control (explosive complexity and collusion); randomization (perturbation, tabular adjustment, random sample queries, swapping) (SE3 p.423-425).
- **Privacy does not compose:** two systems with perturbed versions of the same data allow identification (Source Informatics) (SE3 p.425-426). Active attacks (Iceland: insert a record and see it appear in the pseudonymized database; genealogies) (SE3 p.426-427).

## 3. Rich data and reidentification (SE3 p.427-433)
- Sweeney 1997: **69%** of US residents are identifiable by date of birth + zip; 2017: in a study of 50 households, 25% by name and 28% by address (3% and 18% even with year of birth in 10-year bands) (SE3 p.428). HES: encrypting names is not enough (Blair treated on two public dates); postcode + date of birth identifies ~98% of UK residents (SE3 p.429).
- AOL (20 million queries from 657,000 users) and Netflix (500,000 subscribers reidentified with IMDb, "long tail") (SE3 p.430). Four mobile-phone locations are enough to identify someone (de Montjoye 2012); the NYT tracked 12 million Americans (SE3 p.431-432). Victoria transport: 4 locations identify >1/3 of travelers even truncating the time to the day (SE3 p.433). Kosinski: 4 likes distinguish straight from gay (SE3 p.432).

## 4. Differential privacy (SE3 p.434-436)
- `[from source]` Dwork et al. 2006: bounds the probability of disclosure even against an adversary with unlimited power and plenty of side information; starting point: *reconstruction attacks* (Dinur-Nissim 2003) — with many queries noise is needed (SE3 p.434).
- `[from source]` **ε-indistinguishable mechanism**: for databases X and X' that differ in one row, the probability of any answer from X is within a multiplicative factor (1+ε) of that from X' (the book's formulation; bounds the log of the ratio); Laplace noise is used; composition; ε is a policy decision: small = strong privacy; ε = 1000 ≈ publishing the raw data (SE3 p.434). To compute the scale of the Laplace noise use `se3_calc.py laplace-scale` — `[extrapolation]` (the formula b = sensitivity/ε is not on the page; it comes from the DP literature).
- **2020 census:** the 44 bits per resident (1.7Gb) of 2010 and billions of equations allowed reconstruction (38% of variables right covering <20% of the population in one month, 4 servers); exact counts per block were the vulnerability; top-down algorithm with a global privacy budget; ε suggested between 4 and 6 by economic analysis (SE3 p.435-436) `[DATED]`.

## 5. Policy and alternatives (SE3 p.436-443)
- Ohm 2009 "Broken promises of privacy" (SE3 p.436); Royal Society 2012: the security of personal records "cannot be guaranteed by anonymization when identities are actively sought" (SE3 p.437).
- **Privacy set** (who you do not want to know) vs **anonymity set** (whom you can be confused with): for embarrassment use the first; for scams/phishing, the second (SE3 p.437).
- UKAN and "tactical anonymity"; schemaless Hadoop makes linkage risk invisible; noise does not work on trajectories; ML trained on personal data can reidentify; self-regulation → adverse selection; "the security economics of anonymization is terrible" (SE3 p.437-440).
- **Alternatives** (SE3 p.441): weak anonymity + access control (secure site; license + NDA) if done competently, honestly and lawfully; explicit consent as the gold standard (ALS network, Biobank; p.441); ethics review protects the researcher and the institution, not the data subject ("ethics washing") (SE3 p.442). Smart meters: 0.96% of feeders serve one household and 2.67% three or fewer (SE3 p.443).

## 6. Data protection and evidence (ch. 26, partial)
- **Digital evidence:** chain of custody, reliable tools, document everything, handle private material (SE3 p.981); cloud forensics; MLAT takes weeks (SE3 p.982). FRE 803(6); email is "writing"; ESIGN; eIDAS "qualified signature" (SE3 p.983-984). **What goes wrong:** evidence extracted from the systems of one party only (Munden, ankle tags); Operation Ore; kiosks without training; judges and probability (Bayes rejected by the UK Court of Appeal) (SE3 p.984-985).
- **Europe:** Warren & Brandeis 1890 (SE3 p.986); 1981 Council of Europe convention (SE3 p.987); 1995 Directive; GDPR (2016/2018): document uses and legal basis; consent cannot be coerced or presumed; real-time bidding contrary to the GDPR; maximum fine of 4% of turnover (SE3 p.987-989, 992 note 16).
- **US:** self-regulation and sectoral laws; breach disclosure; cost of a large leak (10 million letters × US$5 + reissues); median cost ~US$200k; ChoicePoint, TJ Maxx, Target (CEO fired); CCPA (SE3 p.989-991).
- **Transfers:** Safe Harbour (struck down in 2015), Privacy Shield (struck down in Jul/2020), SCCs; coercion of consent is prohibited (SE3 p.991-992) `[DATED]` — the regime has changed since; confirm in a current legal source.
- **Summary of ch. 26 as read:** governments' biggest spending is intelligence (~100x the fight against cybercrime); data localization; "understanding and reacting to the surveillance ecosystem is the top priority" (SE3 p.994-995).
- **Boundary:** LGPD, NIST Privacy Framework/IR 8062 and OWASP are covered by other agents in the collection (09_security_and_privacy), not by this one.

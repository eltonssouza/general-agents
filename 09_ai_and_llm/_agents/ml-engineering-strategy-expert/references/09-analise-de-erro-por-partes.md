# 09 - Error analysis by parts (MLY ch. 53-57, p.106-116)

The example images (cat bounding boxes) are figures; the descriptions come from the text.

## Attributing error to components (ch. 53, p.106-108)
- [from source] In a complex pipeline, **attribute each error to one (sometimes both) of the parts** in order to prioritize. Example: cat detector (crops) + breed classifier (decides whether it is Siamese) (p.106).
- [from source] Informally, examine the outputs of each part: if the detector cropped a pile of rocks and the classifier answered y=0, the classifier is innocent (a human would also say 0) -> the detector is at fault; if the crop was good, blame the classifier (p.106-107).
- [from source] If of 100 dev errors 90 come from the detector and 10 from the classifier, focus on the detector; and you already have 90 examples for a deeper error analysis of the detector (p.107-108).

## Attributing to a single part (ch. 54, p.109-110)
- [from source] Ambiguous cases (a bad crop that a skilled human would still recognize): if few, any decision will do; for unambiguous attribution use the **formal test**: (1) replace the detector's output with a **hand-labeled (perfect)** box; (2) run the crop through the classifier. If it still errs -> the classifier is at fault; otherwise -> the detector is at fault (p.109-110).
- [from source] Two cases: the classifier errs even with a perfect box (its fault); it gets it right with a perfect box (the detector should have given a better box). By doing this on the dev errors you estimate the fraction of errors per component (p.110).

## General case A, B, C (ch. 55, p.111-112)
- [from source] Pipeline A -> B -> C. For each dev error: (1) replace A's output with the "perfect" output and run B and C; if the result becomes correct, attribute it to **A**; otherwise (2) replace B's output with the perfect one; if that fixes it, attribute it to **B**; otherwise (3) attribute it to **C** (p.111).
- [from source] Self-driving car example: A = detect cars, B = detect pedestrians, C = plan trajectory; in a closed-track scenario in which the car steers more sharply than a skilled driver would, the same script applies (manually correct A and see whether planning improves, etc.) (p.111-112).
- [from source] The components must follow a **DAG** (fixed left-to-right order; each component depends only on earlier outputs). Swapping A and B (pedestrians before cars) may give slightly different results, but the analysis remains valid and guides the focus (p.112).

## By parts and human level (ch. 56, p.113-114)
- [from source] There is no single "right" way to analyze errors (just as there is none when analyzing customer data); use the book's patterns and try others (p.113).
- [from source] Informal alternative for debugging the car pipeline: (1) how far from human level is "detect cars"? (2) and "detect pedestrians"? (3) and the overall system, compared with a human who **only receives the outputs of the two previous components** (not the images) to plan the trajectory? A component far from human level is a good candidate for improvement (p.113-114).
- [from source] These processes work best when automating something humans do; if the final or intermediate component does something humans do not do well, part of the procedures does not apply (p.114).

## Flawed pipeline (ch. 57, p.115-116)
- [from source] If **each component is close to human level** (comparing each with a human who receives the same input) but the overall system is **well below** human level (humans with access to the images plan much better trajectories), the only conclusion is that **the pipeline is flawed and needs redesign**: the planning component does the best it can given the input, but the input does not carry enough information (p.115).
- [from source] Ask what other information a skilled driver needs (e.g. lane positions) and redesign (e.g. add "detect lanes") (p.116). Note: giving the raw image to planning would violate the "task simplicity" of ch. 51 (the planning module would become too complex); adding a lane component carries the information without complicating any module (note 18, p.116).

Tool: `python -I scripts/mly_errorsheet.py attribute FILE.json --order A,B,C` (rule of ch. 55, p.111).

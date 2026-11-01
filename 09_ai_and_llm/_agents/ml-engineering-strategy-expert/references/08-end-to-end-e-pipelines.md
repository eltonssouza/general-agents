# 08 - End-to-end deep learning and pipeline design (MLY ch. 47-52, p.91-104)

The pipeline diagrams are figures (no extractable text); below are the descriptions from the text.

## The rise of end-to-end (ch. 47, p.91-92)
- [from source] Example: sentiment classification on product reviews ("This is a great mop!"). Classic two-component pipeline: **parser** (annotates words, e.g. adjectives and nouns) + **sentiment classifier** that uses the annotation, for example giving more weight to adjectives (p.91).
- [from source] **End-to-end**: a single algorithm that goes from raw text straight to sentiment; "end-to-end" = directly connecting the "input end" to the "output end"; neural networks are common here (p.91-92). It works very well when there is lots of data, but is not always a good choice (p.92).

## More examples (ch. 48, p.93-94)
- [from source] Speech: 3-component pipeline (MFCC features, phoneme recognizer, final recognizer) vs end-to-end (audio -> transcription) (p.93). Self-driving car: detect cars + detect pedestrians + plan trajectory, vs end-to-end (sensors -> steering) (p.93-94).
- [from source] Not every pipeline component needs to be learned (e.g. robot motion planning has non-learning algorithms) (p.94). The author is **skeptical** about end-to-end for autonomous driving, although end-to-end for speech works well (p.94).

## Pros and cons (ch. 49, p.95-96)
- [from source] Hand-designed components (MFCC, phonemes) **limit** the potential (they throw information away; phonemes are an imperfect invention), but they also have advantages: MFCC is robust to irrelevant properties such as the speaker's pitch; phonemes, if reasonable, help learning. More hand engineering **allows learning with less data**; without lots of data, this knowledge is useful (p.95).
- [from source] End-to-end without this knowledge may do worse with a small training set; with a large training set and a large enough network it can do very well, perhaps close to the optimal error (p.96).
- [from source] End-to-end does well when there is **lots of labeled data for "both ends"** (e.g. audio-transcription pairs); without it, be cautious. With a very small training set, the knowledge comes from human engineering (p.96).

## Choosing components: data availability (ch. 50, p.97-98)
- [from source] Car: there are many labeled datasets of cars and pedestrians (and crowdsourcing, such as Mechanical Turk), but (image, steering) pairs require an instrumented fleet and lots of driving, which is expensive and time-consuming (p.97). If there is plenty of data to train **intermediate modules**, consider a multi-stage pipeline, since the architecture matches the data; until there is more end-to-end data, the author believes the non-end-to-end approach is far more promising for autonomous driving (p.97-98).

## Choosing components: task simplicity (ch. 51, p.99-102)
- [from source] Prefer components that are **individually easy to build/learn**. Five binary tasks in increasing order of difficulty: overexposed image; indoor or outdoor; contains a cat; cat with black-and-white fur; Siamese cat (p.99). The easiest require fewer examples (p.99).
- [from source] There is no formal definition of easy/hard; informally, easy task = few computation steps (shallow network); hard = more steps (deep network) (p.99; Kolmogorov complexity cited in note 16, with few practical applications).
- [from source] Decomposing a complex task into subtasks and coding them explicitly gives the algorithm **prior knowledge** (p.100). Siamese cat detector example: end-to-end (image -> 0/1) vs two-step pipeline (cat detector -> breed classifier on the crops; output 1 if any detected cat is Siamese); each component is much easier and requires much less data (p.100-101). Object detectors use bounding boxes, not just 0/1 labels (note 17, p.101).
- [from source] The driving pipeline tells the algorithm there are 3 key steps (cars, pedestrians, trajectory), each simpler than end-to-end (p.102). Summary: build a pipeline with components of relatively "simple" function, learnable with a modest amount of data (p.102).

## Rich outputs (ch. 52, p.103-104)
- [from source] Traditional supervised learning maps X to a numeric Y (spam 0/1; integer image label; price; chance of purchase) (p.103). The advance of end-to-end allows learning much more complex outputs: **image captioning**, translation (text->text), question answering, speech recognition (audio->transcription), TTS (text features->audio), each with a 2014 to 2016 reference in the book's table (p.103-104). With the right (input, output) pairs it is possible to learn end-to-end even when the output is a sentence, image or audio (p.104). [DATED] the examples and citations are from 2018.

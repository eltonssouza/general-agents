# 00 - Overview, assumptions and scale (MLY ch. 1-4 and 58)

Page convention: **PDF page = printed number "Page N"** (MLY p.N). Everything below was read on the cited pages.

## Nature of the source (ch. 1-3, p.2, 6-9)
- [from source] It is a **draft** ("Draft") by Andrew Ng, © 2018, a deeplearning.ai project (MLY p.2, and the footer of every page). It is not the final edition. [DATED] 2018.
- [from source] Premise: you or your team work on an ML application and want fast progress; the book teaches you to **choose what to try** by reading "clues" from the problem, so you do not spend months in the wrong direction (p.6-7).
- [from source] Guiding example: a cat-photo startup with a neural-network detector whose performance is still not good enough; typical ideas: more data, more diverse data, train longer, a bigger or smaller network, L2 regularization, changing the architecture (p.6-7).
- [from source] Chapters are deliberately short, so you can print 1-2 pages and convince colleagues of a priority (p.8). Ch. 58 repeats the idea of forming a "superhero team" (p.118).
- [from source] Prerequisites: supervised learning (a function from x to y with labeled examples) and basic notions of neural networks ("deep learning"); the book says most of the practical value of ML comes from supervised learning (p.9).

## Scale drives progress (ch. 4, p.10-12)
- [from source] Two recent drivers: **data availability** and **computational scale** (networks large enough to take advantage of the data) (p.10).
- [from source] Older algorithms (e.g. logistic regression) tend to **plateau** with more data; small networks do slightly better; ever larger networks keep improving (p.10-11, figures).
- [from source] Recipe for performance: (i) train a very large network and (ii) have lots of data; architecture also matters (p.11).
- [from source] Note: the advantage of networks on small data is less consistent; with 20 examples, manual feature engineering matters more than the choice of algorithm; with 1 million, the author prefers the neural network (p.11, note 1).
- [from source] The book starts with general strategies (valid for traditional algorithms and networks) and arrives at deep learning strategies (p.12).

## Outside the book (NOT COVERED)
Anything post-2018 (Transformers, LLMs, fine-tuning of pre-trained models, MLOps) is not in the MLY; see `datado.md` and `python -I scripts/mly_lookup.py --gaps`.

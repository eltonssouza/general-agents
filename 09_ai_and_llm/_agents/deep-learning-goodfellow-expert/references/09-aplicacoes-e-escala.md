# 09 · Applications and scale (DLB ch. 12, PDF p.458-500) — **[DATED] 2016**

**Coverage:** read p.458-465 (scale), 467-470 (vision), 476-477 (n-grams), 482 (*hierarchical softmax*) and 488-493 (translation, attention, history, recommendation). **Not read:** p.466 (specialized hardware, beginning), 471-475 (rest of vision and speech), 478-481 and 483-487 (neural language models, short list, *importance sampling*, NCE), 494-500 (detailed recommendation, knowledge graphs, QA). Convention: DLB p.N = PDF page (printed = N − 15). Eq. 12.3 checked visually (p.470). **This chapter is the most dated: all numbers and systems are from 2016.**

## Scale (12.1)
- `[from source]` (DLB p.458) Network size is a central factor; the 2016 networks were the size of insect nervous systems.
- `[from source]` (DLB p.459) CPUs: in 2011 a tuned **fixed-point** implementation was 3× faster than floating point (Vanhoucke 2011) `[DATED]`; numerical specialization pays off a lot.
- `[from source]` (DLB p.459-461) **GPUs**: high memory bandwidth and parallelism, little branching; Steinkrau 2005 (2 fully connected layers, 3× faster) and Chellapilla 2006 (CNNs); CUDA and GP-GPUs; efficient GPU code is hard (memory coalescing, *warps*); structure the work with high-performance operation libraries (Theano, cuda-convnet, TensorFlow, Torch) `[DATED]`.
- `[from source]` (DLB p.462) **Data** parallelism (inference is simple; training with a larger minibatch gives less than linear returns) and **model** parallelism; **asynchronous SGD** (Bengio 2001; Recht 2011) with a *parameter server* (Dean 2012) was the main industry strategy in 2016 `[DATED]`.
- `[from source]` (DLB p.462-463) **Model compression** (Buciluă 2006): train a small model to copy f(x) from the large one, sampling x from a distribution similar to the test one, or copy the distribution over the wrong classes (Hinton 2014, 2015). `[inference]` This is what is now called distillation; the book does not use the term on these pages.
- `[from source]` (DLB p.463-465) **Dynamic structure**: conditional computation; **cascade** of classifiers (the first ones with low capacity and high *recall*; the last with high precision; Viola and Jones 2001 with a face detector); decision trees and *mixture of experts* with a *gater* (also the *hard* version); switches as an attention mechanism (Olshausen 1993); obstacle: lower parallelism (p.465).
- `[from source]` (DLB p.467) **8 to 16 bits** of precision would suffice to use and train networks with backprop (Vanhoucke 2011; Courbariaux 2015; Gupta 2015); more precision in training than in inference `[DATED]`.

## Computer vision (12.2)
- `[from source]` (DLB p.467-469) Minimal preprocessing: normalize the pixels to the same range ([0,1] or [−1,1]); mixing images in [0,1] with [0,255] tends to fail; resize when the architecture requires it; *dataset augmentation* and voting over several crops at test time (ensemble); AlexNet uses only per-pixel mean subtraction (p.469).
- `[from source]` (DLB p.469-470) **Global contrast normalization (GCN)**: X′ᵢⱼₖ = s(Xᵢⱼₖ − X̄)/max{ε, √(λ + (1/3rc)ΣΣΣ(Xᵢⱼₖ − X̄)²)} (eq. 12.3); maps examples to a spherical shell; s = 1 or standard deviation ≈ 1 per pixel; *sphering* is **not** GCN. `dlb_calc.py gcn`.

## Language (12.4)
- `[from source]` (DLB p.476-477) Language models define a distribution over sequences of tokens (words, characters, bytes); **n-grams**: P(x₁..x_τ) = P(x₁..xₙ₋₁)∏P(xₜ|xₜ₋ₙ₊₁..xₜ₋₁) (12.5), estimated by counting; zero probabilities require **smoothing**.
- `[from source]` (DLB p.482) *Hierarchical softmax* (Goodman 2001; Morin and Bengio 2005): reduces the per-word cost from |V| to log|V| with a tree of categories and logistic regression per node.
- `[from source]` (DLB p.488-490) **Neural translation**: old components (proposal + n-gram language model); Schwenk 2006/2010 used a neural language model; Devlin 2014, conditional MLP; limitation of fixed-size inputs; **encoder-decoder** (Cho 2014a; Sutskever 2014; Fig. 12.5) with context C.
- `[from source]` (DLB p.490-491) **Attention** (Bahdanau 2015; Fig. 12.6): the context vector c is a **weighted average** of the feature vectors h⁽ᵗ⁾, with weights α⁽ᵗ⁾ produced by the model itself (softmax over relevance scores); it is a soft, differentiable approximation of indexing a specific step; it solves the difficulty of summarizing long sentences (~60 words) in a fixed vector. Three components: reader, memory (list of vectors) and a process that explores the memory. `[DATED]` This is **RNN** attention; the book does not treat self-attention or Transformers.
- `[from source]` (DLB p.491-492) History: distributed representation of symbols (Rumelhart 1986a), embeddings via SVD (Deerwester 1990), neural language models (Bengio 2001), character and byte models, t-SNE (van der Maaten and Hinton 2008).
- `[from source]` (DLB p.493) Recommendation and advertising: predict the user-item association as regression or probabilistic classification.

## Frontier
`[DATED]` The book (2016) contains no Transformers, BERT/GPT, large language models, *prompting*, RLHF, modern diffusion, TPUs or current frameworks. `python -I scripts/dlb_lookup.py --gaps` lists the terms verified as absent. For those subjects, answer "NOT COVERED" or an explicit `[extrapolation]`.

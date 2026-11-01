# 00 · Introduction and history (DLB ch. 1, PDF p.16-43)

**Coverage:** ch. 1 read **in full** (p.16-43). Convention: "DLB p.N" = PDF page (printed = N − 15). 2016 book: numbers and system names are `[DATED]`.

## 1. The problem and the book's thesis
- `[from source]` (DLB p.16) Early AI solved formal problems well (describable by rules); the hard part is intuitive tasks, such as recognizing speech or faces. The proposed solution: the computer learns from experience and understands the world as a hierarchy of concepts, each defined through simpler concepts (DLB p.16-17). The graph of this hierarchy is "deep", hence *deep learning*.
- `[from source]` (DLB p.17) The *knowledge base* approach (knowledge hand-coded in a formal language, e.g. Cyc) was not very successful; the "Fred shaving" episode illustrates its fragility. This motivates *machine learning*: extracting patterns from raw data (DLB p.17-18).
- `[from source]` (DLB p.18) Simple algorithms (logistic regression to recommend cesarean delivery, *naive Bayes* for spam) depend on the **representation** (features) they are given; they have no influence over how the features are defined.
- `[from source]` (DLB p.19) *Representation learning* learns the representation in addition to the mapping; the classic example is the **autoencoder** (encoder + decoder). Fig. 1.1 shows that the same task is impossible in Cartesian coordinates and simple in polar ones.
- `[from source]` (DLB p.20) The goal is to separate (*disentangle*) the **factors of variation**; deep learning expresses them in terms of simpler representations. The canonical example is the MLP, a composite function (DLB p.20).
- `[from source]` (DLB p.22-23) **Depth** can be measured by the longest path in the computational graph or by the depth of the concept graph; logistic regression σ(wᵀx) has depth 3 or 1 depending on which operations count as elements (Fig. 1.3). There is no consensus on how deep "deep" is.
- `[from source]` (DLB p.24-25) Relation: AI ⊃ machine learning ⊃ *representation learning* ⊃ deep learning (Fig. 1.4); Fig. 1.5 compares rule-based systems, classical ML, *representation learning* and deep learning.
- `[from source]` (DLB p.26-27) Organization in three parts: I (mathematics and ML fundamentals), II (established algorithms, treated as "essentially solved"), III (more speculative, research-level ideas).

## 2. Three waves
- `[from source]` (DLB p.28-29) *Cybernetics* (1940s-1960s), *connectionism* (1980s-1990s) and the current wave from 2006 onward (Fig. 1.7).
- `[from source]` (DLB p.30) McCulloch-Pitts (1943), perceptron (Rosenblatt 1958) and ADALINE (Widrow-Hoff 1960); ADALINE uses a special case of stochastic gradient descent, still dominant today; linear models cannot learn XOR (Minsky and Papert 1969), the first major drop in popularity.
- `[from source]` (DLB p.31) Neuroscience inspires but is not a rigid guide; the *Neocognitron* (Fukushima 1980) inspired the CNN; the ReLU is the most common model neuron.
- `[from source]` (DLB p.32-33) From connectionism come the **distributed representation**, **backpropagation** (Rumelhart 1986a) and the LSTM (Hochreiter and Schmidhuber 1997); the 1990s decline is tied to exaggerated promises and to the progress of kernel machines and graphical models.
- `[from source]` (DLB p.33-34) The third wave starts in 2006 with *deep belief networks* trained by **greedy layer-wise pretraining** (Hinton 2006). The emphasis later shifted from unsupervised to supervised learning with large datasets (DLB p.34).

## 3. Scale of data, models and results
- `[from source]` (DLB p.35) **2016** rule of thumb: acceptable performance with about 5,000 labeled examples per category; matching or exceeding humans with at least 10 million labeled examples `[DATED]`. Networks doubled in size every ~2.4 years, and by the book's extrapolation would only have as many neurons as the human brain in the 2050s `[DATED]`.
- `[from source]` (DLB p.38) The first large-margin win by a CNN at ILSVRC cut top-5 error from 26.1% to 15.3% (Krizhevsky 2012); at the time of the book, 3.6% (Fig. 1.12) `[DATED]`. Speech recognition error also dropped with deep learning.
- `[from source]` (DLB p.40) Then-emerging applications: sequence transcription, *sequence-to-sequence*, translation, *neural Turing machines*, deep reinforcement learning (Atari). Libraries cited: Theano, Torch, Caffe, MXNet, TensorFlow `[DATED]`.

## 4. Limits of this block
`[DATED]` Everything above describes the state of 2016. The book does not know Transformers, large language models, modern diffusion, etc. (confirm with `python -I scripts/dlb_lookup.py --gaps`).

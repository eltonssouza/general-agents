# [DATED] What has changed since 2016 (the book's frontier)

Book: *Deep Learning*, Goodfellow, Bengio and Courville, MIT Press, 2016. This list is **not book content**: it serves for the agent to declare the frontier. The "the book says" items have a page; the absences were **verified by searching the extracted text** (0 occurrences in the body, p.16-735). For the current state of the art, the agent must recommend current sources and label any answer as `[extrapolation]`.

## What the book says about its own time `[DATED]`
- **Data and scale:** 2016 rule of thumb: ~5,000 labeled examples per category for acceptable performance and ≥10 million to match humans (DLB p.35); networks doubling every ~2.4 years (p.35). ILSVRC top-5 error: from 26.1% to 15.3% with the first winning CNN (Krizhevsky 2012) and 3.6% at the time the book was written (p.38).
- **Software and hardware:** Theano, Torch, Caffe, MXNet, TensorFlow, cuda-convnet (DLB p.40, 461); GPUs with CUDA; fixed point on CPU in 2011 (p.459); asynchronous SGD with a *parameter server* (p.462); 8-16 bit precision (p.467).
- **Optimization:** suggested Adam defaults (ε = 0.001; ρ₁ = 0.9; ρ₂ = 0.999; δ = 10⁻⁸; DLB p.326); "no consensus" on the best optimizer, SGD+momentum, RMSProp and Adam among the most used (p.324).
- **Regularization:** dropout (p.273) and batch normalization (p.332) were very recent techniques (2014/2015).
- **Applications:** neural translation and RNN encoder-decoder attention (Bahdanau 2015) were the frontier (DLB p.488-491); attention as a weighted average of RNN states (p.490).
- **Generative:** VAE and GAN as new techniques (DLB p.711-716); "diffusion inversion" as a transition that undoes one noise step (p.731-732).
- **Pretraining:** unsupervised greedy pretraining was born in 2006 and already in 2016 "is not necessary" for deep fully connected networks (DLB p.543); supervised pretraining on ImageNet was the *transfer learning* practice (p.551).
- **Hyperparameters:** Bayesian optimization is "not unequivocally recommended" (DLB p.451).

## Absent from the book (NOT COVERED; confirmed with `python -I scripts/dlb_lookup.py --gaps`)
- Transformers, self-attention/multi-head, BERT, GPT, LLMs, prompting, instruction tuning, in-context learning, RLHF, LoRA/PEFT.
- Layer normalization, ResNet/residual connections, AdamW, GELU/Swish, *warmup* and cosine schedules.
- Diffusion as a modern generative model, *normalizing flows*, WGAN/StyleGAN (the book has DCGAN and LAPGAN, p.716-717), mixup/cutout.
- PyTorch, JAX, TPU, mixed precision, *scaling laws*, tokenization/BPE, NAS, GNNs, capsules.
- word2vec as a name (there is a citation of word vectors, Mikolov 2013a, DLB p.551).

## How the agent should behave
1. If the user asks for something on the list above: answer "NOT COVERED in this book (2016)"; if giving an explanation, mark `[extrapolation]` and suggest a current source.
2. If the user brings a recent fact that contradicts or supersedes the book: agree and mark `[DATED]`.
3. Never attribute to the book what it does not say; never present 2016 numbers as the current state of the art.

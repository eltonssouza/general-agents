# Glossary (English terms; the original Portuguese term in parentheses) — with pages

Convention: PDF; UDL = Prince (2023); NNDL = Nielsen. Only definitions present on the cited pages.

**Activation / pre-activation** (ativação / pré-ativação): value after / before the activation function; UDL p.49 (shallow network), NNDL p.60-61 (`z^l` is the "weighted input").
**Adam**: SGD with a moving average of the gradient and of the gradient² with bias correction; UDL p.102-104.
**Value alignment** (alinhamento de valores): ensuring that the objectives of AI systems coincide with human values; outer (proxy loss) and inner; UDL p.434-435.
**Dot-product self-attention** (atenção por produto escalar): output = weighted sum of values with softmax weights of the query·key similarities; UDL p.222-224.
**Autoregressive** (autorregressivo): model that factorizes `Pr(t1..tN) = Pr(t1) Π Pr(tn|t<n)`; UDL p.236-237.
**Backpropagation**: algorithm that computes all derivatives with one forward and one backward pass; UDL p.111-120; NNDL p.58-83.
**Batch / minibatch** (mini-lote): subset of examples used in one SGD step; UDL p.99; NNDL p.36.
**BatchNorm**: normalizes each unit with the batch mean and deviation and then applies `γ` and `δ`; UDL p.206-208.
**Bias-variance (trade-off)**: test error = noise + bias² + variance (least squares); UDL p.136-139.
**BERT**: transformer encoder (24 layers, D=1024, ~340 million parameters); UDL p.233.
**BPE** (byte pair encoding): tokenizer that merges frequent pairs; UDL p.231-232.
**Receptive field** (campo receptivo): region of the input that influences a unit; UDL p.181; NNDL p.244-245 (local receptive field).
**Channel / feature map** (canal): set of activations produced by a kernel; UDL p.179-181; NNDL p.246-247.
**Classifier-free guidance**: conditional diffusion trained with and without the condition; UDL p.379-380.
**Convolution** (convolução): local weighted sum with shared weights (technically cross-correlation); UDL p.177; NNDL p.246, p.249.
**Cross-attention**: attention with queries from the decoder and keys/values from the encoder; UDL p.240-241.
**Cross-entropy**: distance between the empirical distribution and the model's; equivalent to the NLL; UDL p.85-86; NNDL p.89-90 (form for sigmoids).
**Curse of dimensionality**: volume grows faster than the data; UDL p.143, p.149.
**Dilated / atrous convolution** (dilatação): kernel with interleaved zeros; UDL p.179.
**Diffusion model** (difusão): fixed encoder that adds noise and decoder that removes it; UDL p.362-363.
**Double descent**: test error falls, rises near interpolation and falls again; UDL p.141-143.
**Dropout**: randomly zeroing hidden units during training; UDL p.161-163; NNDL p.130-133.
**ELBO**: lower bound on the log-likelihood in latent variable models; UDL p.346-349.
**Early stopping**: stopping training at the best point on validation; UDL p.159; NNDL p.111-112, p.165-166.
**Ensemble**: combining several models; UDL p.159-161; NNDL p.263.
**Epoch** (época): one complete pass through the data; UDL p.99; NNDL p.37.
**Equivariance / invariance** (equivariância / invariância): `f[t[x]] = t[f[x]]` / `f[t[x]] = f[x]`; UDL p.176.
**Adversarial example** (exemplo adversarial): minimal perturbation that changes the class; UDL p.427-428; NNDL p.288-290.
**Few-shot**: performing a new task from examples in the context; UDL p.239.
**Normalizing flow** (fluxo normalizante): invertible map from a simple density to a complex one with exact likelihood; UDL p.317-322.
**GAN**: generator against discriminator; UDL p.289-292.
**GCN**: convolutional network on graphs; UDL p.262-265.
**Generalization** (generalização): performance on new data; UDL p.132, p.152.
**Gradient descent**: update `φ ← φ − α ∂L/∂φ`; UDL p.92; NNDL p.31-33 (`v → v − η∇C`).
**Grokking**: delayed generalization after a perfect fit of the training set; UDL p.426-427.
**He initialization**: weights with variance `2/D_h`; UDL p.124.
**Hyperparameter** (hiperparâmetro): choice made before training (layers, rate, batch); UDL p.60, p.146-147; NNDL p.47-48, p.156-173.
**Hadamard (product)**: element-wise product `s ⊙ t`; NNDL p.63-64.
**Inductive bias** (viés indutivo): preference for certain solutions, e.g., convolution; UDL p.143, p.184, p.426.
**Inception Score / FID**: metrics for image generative models; UDL p.285-287.
**InfoGAN / ACGAN / cGAN**: conditional GANs or GANs with discovered attributes; UDL p.302-304.
**Jensen-Shannon**: symmetric divergence; the GAN loss is proportional to it; UDL p.295, p.474.
**Kernel / filter** (filtro): shared weights of a convolution; UDL p.177; NNDL p.246.
**KL divergence**: `DKL[p||q] = ∫p log(p/q)`; UDL p.474.
**LayerNorm**: normalizes per example (over channels/positions); UDL p.217-218, p.229-230.
**Label smoothing**: soft label with probability 1−ρ; UDL p.163-164.
**Lottery ticket**: subnetwork that trains as well as the full network; UDL p.420.
**Loss / cost / objective**: synonyms in the book; UDL p.37; NNDL p.26 (note).
**Maximum likelihood** (máxima verossimilhança): maximize `Π Pr(y_i|x_i)`; UDL p.72.
**Momentum**: moving average of the gradient; UDL p.100; NNDL p.176.
**Multi-head attention**: several attentions in parallel; UDL p.228-229.
**Neighborhood sampling / graph partitioning**: ways of batching large graphs; UDL p.267-270.
**Overfitting**: fitting the noise of the training set; UDL p.36, p.139; NNDL p.107-111.
**Perceptron**: neuron with binary output by threshold; NNDL p.5-8.
**Positional encoding**: informs the position of the tokens; UDL p.227-228.
**PPO**: policy gradient with clipped loss; used in RLHF; UDL p.411-412.
**Pooling** (max / mean / L2): reduces resolution; UDL p.186-187; NNDL p.249-251.
**ReLU**: `max(0,z)`; UDL p.39; NNDL p.181-182.
**Regularization** (regularização; explicit/implicit): UDL p.152-158; NNDL p.114-131.
**ResNet / residual block** (bloco residual): output = input + processing; UDL p.203-205, p.209-210.
**RLHF**: fine-tuning a model with rewards learned from human preferences; UDL p.412.
**Saturation** (neuron saturation; saturação): `σ'(z)≈0` for large |z|; NNDL p.69, p.88-89, p.140.
**Self-supervised** (generative / contrastive): labels generated from the data; UDL p.166.
**Sigmoid / logistic** (sigmoide / logística): `1/(1+e^{−z})`; UDL p.80; NNDL p.14.
**Softmax**: normalizes logits into a distribution; UDL p.82; NNDL p.101.
**SGD**: stochastic gradient descent with mini-batches; UDL p.97-100; NNDL p.35-37.
**Transfer learning / fine-tuning**: pre-train and adapt; UDL p.165-166, p.233, p.235.
**Transformer** (layer; camada): MhSa + residual + LayerNorm + per-token MLP; UDL p.229-230.
**U-Net**: encoder-decoder with skips by concatenation; UDL p.211-213; used in diffusion, p.377-378.
**VAE**: variational autoencoder; UDL p.340-352.
**Vanishing / exploding gradients**: gradients of early layers shrink or grow; UDL p.122; NNDL p.229-235.
**WGAN**: GAN with the Wasserstein distance; UDL p.297-299.
**Weight decay**: rescaling weights before the gradient; NNDL p.116 (as L2); UDL p.169-170 (distinct from L2 in Adam).

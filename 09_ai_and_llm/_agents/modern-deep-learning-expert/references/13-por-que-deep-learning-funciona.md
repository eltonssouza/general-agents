# 13 — Why deep learning works (and what is still unknown)

Main source: UDL ch.20 (PDF p.415-433), read in full (problems on p.433 only skimmed). Supplements: NNDL p.127, p.298, p.302 (the author's opinion on the state of theory, `[DATED 2015]`). This UDL chapter is explicitly "different": it raises questions rather than presenting established results (UDL p.415).

## 1. The case "against" deep learning (UDL p.415-416)
- Training: finding the global minimum of an arbitrary non-convex function is NP-hard (Murty-Kabadi 1987; Blum-Rivest 1992 for networks); but networks with 43 units per layer (~4,000 parameters) perfectly fit the 10,000 MNIST-1D examples (UDL p.415) `[checked: 4,095 in dl_calc.py mlp-params --sizes 40,43,43,10]`.
- AlexNet (~60 million parameters, ~1 million data points × 2,048 of augmentation) and GPT-3 (175 billion parameters, 300 billion tokens) are not clearly over-parameterized and were trained successfully (UDL p.416).
- Generalization: the curse of dimensionality (10^40 possible inputs in quantized MNIST-1D), the 10^42 linear regions cited and the fact that more parameters generalize better (UDL p.416). Checking caveat: (i) 177,201 parameters only reproduce with a scalar output (with 10 outputs it is 180,810) and (ii) the bound of eq. 4.17 (UDL p.67) for D=400, Di=40, K=2 gives ~10^97, and only the first factor (11^40 ≈ 10^41.7) approximates 10^42 — the book does not explain the calculation `[inference; dl_calc.py regions --D 400 --K 2 --Di 40]`.

## 2. Factors that influence fitting (UDL p.416-420)
- Dataset: AlexNet fits CIFAR-10 even with Gaussian pixels or permuted labels (Zhang et al. 2017), only more slowly (UDL p.417, fig. 20.1). Regularization (L2, dropout) is not necessary to fit (UDL p.417). SGD is not essential: batches of 5,000-6,000 images also fit (Keskar et al.) and full-batch GD fits random labels (UDL p.417-418, fig. 20.2: 4 networks of 298/100/75/63 units per layer; deeper ones train in fewer epochs).
- Fig. 20.2 (checked by render): "15208, 15210, 15235 and 15139 parameters"; the first three reproduce; for 4 layers of 63 units the calculation gives 15,319 (possible digit transposition) `[inference]`.
- **Over-parameterization** is probably important: "a haystack of needles" (Sejnowski 2020) (UDL p.418); networks usually have 10 to 100 times more parameters than examples (fig. 20.3 p.419); convergence theory requires unrealistic widths (e.g., Ω[I⁴K²]) (UDL p.418-419).
- Activation: sigmoid/tanh have shallow gradients in the tails (UDL p.419). Initialization: variances larger than He only delay fitting (Liu et al. 2023c) (UDL p.419-420). Depth: the difficulties are "numerical" (explosion/vanishing/shattered) (UDL p.420). **Lottery ticket**: train, prune the smallest weights and retrain from the same initial weights to find subnetworks that suffice; random reinitialization does not work (Frankle-Carbin 2019) (UDL p.420).

## 3. Properties of loss functions (UDL p.420-424)
Multiple equivalent global minima (permutations, ReLU scaling, BatchNorm) (UDL p.421); the line from the initial point to the final one usually has decreasing loss (Goodfellow 2015b) (UDL p.421, fig. 20.5); trajectories live in low-dimensional subspaces — training in a random 750-dimensional subspace (0.4% of the parameters) reaches 90% of the performance (UDL p.421-422, fig. 20.6); independent minima are not linearly connected, but can be linked by low-loss paths (Draxler 2018) (UDL p.422-423); few bad minima (Dauphin 2014), a "Goldilocks zone" of norm where the curvature is positive (Fort-Scherlis 2019) (UDL p.423-424).

## 4. What determines generalization (UDL p.424-428)
- Algorithm: SGD > GD; smaller batch and larger rate generalize better; batch/η ratio (He et al. 2019) (UDL p.424-425, fig. 20.10). Flat minima (Hochreiter-Schmidhuber 1997; Keskar 2017), but with no guarantee under reparameterization (Dinh 2017) and they do not predict generalization across datasets (UDL p.425-426).
- Architecture = inductive bias (convolution, transformer, GNN) (UDL p.426). Weight norm and **grokking** (Power 2022; Liu et al. 2023c): delayed generalization when the norm returns to the Goldilocks zone (UDL p.426-427, fig. 20.13). Double descent via norm (UDL p.426-427). Fig. 20.12 (UDL p.427): network with 2 hidden layers of 200 on MNIST "198,450 parameters"; our count with 784 inputs and 10 outputs gives 199,210 — not reproduced `[inference]`.
- Off the data manifold: enormous variability between seeds on corrupted data (D'Amour 2020); **adversarial examples** (Goodfellow 2015a; Szegedy 2014): almost imperceptible perturbations change the class; best current explanation (Ilyas 2019): they exploit low-norm information present in the distribution (UDL p.427-428). NNDL p.288-290 presents the same phenomenon as "blind spots" `[DATED 2013-2014]`.

## 5. Do we need so many parameters? (UDL p.428-430)
Magnitude pruning (Han 2016: VGG with 8% of the weights); Frankle-Carbin: VGG-19 from 138 million → −98.5% on CIFAR-10; ResNet-50 from 25.6 million → −80% on ImageNet; distillation (Hinton 2015: learn the pre-softmax logits; Zagoruyko: ResNet-34 ~63M → ResNet-18 ~11M). Conclusion: no state-of-the-art demonstrations with far fewer parameters than examples; Bubeck-Sellke 2021: smooth interpolation requires D times more parameters (UDL p.428-430).

## 6. Do they need to be deep? (UDL p.431-432)
Historical evidence in favor (more than 10 layers even in the shallowest good ones) and three hypotheses: function complexity, training tractability and inductive bias; distilling an ensemble of 16 CNNs into shallow ones fails (Urban 2017); the convolutional architecture is a useful prior even without training (Ulyanov 2018) (UDL p.431-432). Conclusion: there is no prescriptive theory; "the study of DL is still guided by empirical demonstrations" (UDL p.432-433).

## 7. NNDL: similar questions in 2015
`[from source]` "Why do networks generalize so well with ~80,000 parameters and 50,000 images? Conjecture: self-regularization of gradient descent" (NNDL p.127); "Why does SGD work so well?" and "how does performance scale with more data?" remain unanswered (NNDL p.298); prediction that "deep learning is here to stay" (NNDL p.298) and the view that the field is still "shallow" in ideas (NNDL p.302) `[DATED 2015]`.

## 8. How to use this chapter when answering
- "Why does this work?" questions: answer with the hypotheses and label `[from source]` what the text states and `[inference]` what is deduced; state that the book says there is no prescriptive theory (UDL p.432-433).
- Avoid asserting that "over-parameterization explains everything": the book says it explains part of the fitting and generalization, not the design decision (UDL p.418, p.426-427).
- Question about scaling laws, grokking in LLMs, NTK/feature learning: NOT COVERED beyond what is above.

# 11 — Diffusion models

Source: UDL ch.18 (PDF p.362-386). Body (p.362-381) and notes (p.381-385) read; problems only skimmed (p.385-386). Equations used in scripts were checked against the extracted text and by algebraic consistency (numerical residual ~0 in `dl_calc.py diffusion`).

## 1. Overview
`[from source]` A diffusion model has a pre-specified **encoder** (no parameters) that gradually mixes the data `x` with white noise and a learned **decoder** that undoes each step; the dimension of the latents is the same as the data's (UDL p.362-363). Easy to train and with quality above GANs (UDL p.362). Naming is reversed relative to flows: here "forward" is encoding/diffusing (footnote, UDL p.363).

## 2. Encoder (forward process)
- `z1 = √(1−β1) x + √β1 ε1`; `z_t = √(1−β_t) z_{t−1} + √β_t ε_t` (eq. 18.1); `β_t ∈ [0,1]` is the *noise schedule*; it is a Markov chain with `q(z1|x) = Norm[√(1−β1) x, β1 I]` and `q(zt|z_{t−1}) = Norm[√(1−βt) z_{t−1}, βt I]` (eq. 18.2) (UDL p.363-364). 1D example: T=100 and constant β=0.03 (UDL p.364, fig. 18.2).
- **Diffusion kernel** in closed form: `z_t = √α_t x + √(1−α_t) ε`, with `α_t = Π_{s≤t}(1−β_s)` (eq. 18.7); `q(zt|x) = Norm[√α_t x, (1−α_t) I]` (eq. 18.8) (UDL p.366). With large T `q(zT|x) → Norm[0,I]` (UDL p.364). `[checked]` with β=0.03: α_100 = 0.97^100 ≈ 0.0476; kernel variance 0.952.
- Marginal `q(z_t) = ∫q(z_t|x)Pr(x)dx` (eq. 18.10); `q(z_{t−1}|z_t)` is intractable (eq. 18.11) but approximately normal (UDL p.367-368). Conditioned on `x`: **`q(z_{t−1}|z_t, x)`** in closed form, normal with mean `(1−α_{t−1})√(1−β_t)/(1−α_t) · z_t + √α_{t−1} β_t/(1−α_t) · x` and variance `β_t(1−α_{t−1})/(1−α_t) I` (eq. 18.15) (UDL p.368-369). `[checked in dl_calc.py diffusion]`.

## 3. Decoder and training
- Decoder: `Pr(zT) = Norm[0,I]`, `Pr(z_{t−1}|z_t,φ_t) = Norm[f_t[z_t,φ_t], σ_t² I]`, `Pr(x|z1,φ1) = Norm[f1[z1,φ1], σ1² I]` (eq. 18.16); ancestral sampling (UDL p.369-370).
- ELBO (eq. 18.20-18.25): reconstruction term plus `Σ_{t=2}^T E[DKL[q(z_{t−1}|z_t,x) || Pr(z_{t−1}|z_t,φ_t)]]`; the term in z_T is ≈ 0 (UDL p.370-372). Since the encoder has no parameters, the decoder does all the work (UDL p.371). The KL between normals reduces to the squared difference of the means over `2σ_t²` plus a constant (eq. 18.28) and the loss is eq. 18.29 (UDL p.372-373).
- **Reparameterization**: `x = z_t/√α_t − √(1−α_t)/√α_t · ε` (eq. 18.31) and the target mean becomes `z_t/√(1−β_t) − β_t/(√(1−α_t)√(1−β_t)) · ε` (eq. 18.33); the model now predicts the noise: `f_t[z_t] = z_t/√(1−β_t) − β_t/(√(1−α_t)√(1−β_t)) · g_t[z_t,φ_t]` (eq. 18.35) (UDL p.374-375). The weighted loss (eq. 18.36-18.38) is simplified in practice to **`L = Σ_i Σ_t ||g_t[√α_t x_i + √(1−α_t) ε_it, φ_t] − ε_it||²`** (eq. 18.39) (UDL p.376). `[checked in dl_calc.py diffusion]`: the residual between the forms of eq. 18.32 and 18.33 is ~1e-16.
- **Algorithm 18.1 (training)**: draw `t ~ U[1,T]`, `ε ~ N(0,I)`, loss `||g_t[√α_t x + √(1−α_t) ε] − ε||²`. **Algorithm 18.2 (sampling)**: `z_T ~ N(0,I)`; for `t = T…2`: `ẑ_{t−1} = z_t/√(1−β_t) − β_t/(√(1−α_t)√(1−β_t)) g_t[z_t]` and `z_{t−1} = ẑ_{t−1} + σ_t ε`; at the end, noise-free `x` from `z_1` (UDL p.377).

## 4. Implementation
- Images: a single **U-Net** with a (sinusoidal) time embedding added at each stage and periodic global attention; `T = 1000` steps may be needed; sampling is slow because it traverses T networks in series (UDL p.377-378, fig. 18.9).
- Speed: a whole family of processes is compatible with the same loss; **DDIM** (deterministic after the first step) and accelerated sampling (process defined on a subsequence of steps) reach ~50 steps (UDL p.378-379, fig. 18.10). Notes: Stable Diffusion (diffusion in the latent space of an autoencoder), probability-flow ODE, distillation (UDL p.383-384) `[DATED 2023]`.
- Conditional: **classifier guidance** `z_{t−1} = ẑ_{t−1} + σ_t² ∂log Pr(c|z_t)/∂z_t + σ_t ε` (eq. 18.40) and **classifier-free guidance** (joint conditional/unconditional training by dropping the condition); overweighting the condition gives high-quality but stereotyped samples, analogous to truncation in GANs (UDL p.379-380). Text: embedding from a language model added like the time embedding; cascade of U-Nets (64×64 → 256×256 → 1024×1024) (UDL p.380-381, fig. 18.11); estimating variances σ_t² and varying the schedule also improves results (UDL p.380-381).

## 5. Notes and comparative view
- History: Sohl-Dickstein 2015; Ho et al. 2020 (DDPM) started the wave; Dhariwal-Nichol 2021 was the first to beat GANs on FID (UDL p.381). Applications in text→image, inpainting, super-resolution, video, 3D, audio (UDL p.383).
- Diffusion is a hierarchical VAE with a fixed encoder and latents the size of the data; in its basic form it only computes a lower bound on the likelihood; drawbacks: slow and latents without semantic interpretation (UDL p.383). `[DATED]` The models cited (DALL·E 2, Imagen, GLIDE, ControlNet) are from 2021-2023.

## 6. Common mistakes
1. Confusing `β_t` (per-step mixing rate) with `α_t` (cumulative product) — the kernel uses α_t (eq. 18.7).
2. Using the posterior variance as the decoder's σ_t² without remembering that σ_t² is "predetermined" in the book (UDL p.370).
3. Forgetting that training draws t and ε per example and that `x` can be reused with several noises (UDL p.376).
4. Stating the "default" value of β (such as 1e-4 to 0.02) or T=1000 as a rule: the book only says T may be ~1000 (UDL p.377) and gives β=0.03 (T=100) as a 1D example (UDL p.364). Values used in practice: `[extrapolation]`.

## 7. Script
`python -I scripts/dl_calc.py diffusion --beta 0.03 --T 100 --t 20 --sample 2.0 --seed 1`

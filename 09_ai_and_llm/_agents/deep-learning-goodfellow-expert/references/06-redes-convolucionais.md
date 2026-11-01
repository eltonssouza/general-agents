# 06 · Convolutional networks (DLB ch. 9, PDF p.345-387)

**Coverage:** read p.346-357, 362-371, 373-377 and 386-387. **Not read:** p.358-361 (pooling with *stride*, complete classification architectures, start of the infinitely strong prior beyond p.362), p.372, p.378-385 (random/unsupervised features, neuroscientific basis). Convention: DLB p.N = PDF page (printed = N − 15). Eq. 9.7-9.8 checked visually (p.363).

## The operation
- `[from source]` (DLB p.346) The best vision models change every few weeks, but have always been composed of the same blocks described here.
- `[from source]` (DLB p.346-347) Convolution s(t) = ∫x(a)w(t−a)da (eq. 9.1); first argument = input, second = *kernel*, output = *feature map*; discrete version (9.3) and 2-D S(i,j) = ΣΣI(m,n)K(i−m,j−n) (9.4), commutative because of the kernel flip (9.5).
- `[from source]` (DLB p.348) Most libraries implement **cross-correlation** S(i,j) = ΣΣI(i+m,j+n)K(m,n) (9.6) and call it convolution (the learned kernel ends up mirrored). A convolution is equivalent to multiplication by a Toeplitz matrix (2-D: *doubly block circulant*), very sparse.

## Why convolutions
- `[from source]` (DLB p.350-354) Three ideas: **sparse interactions** (kernel smaller than the input: k×n parameters and O(k×n) instead of m×n); **parameter sharing** (*tied weights*; only k parameters per kernel; time remains O(k×n)); **translation equivariance** (f(g(x)) = g(f(x))). Convolution is not naturally equivariant to scale or rotation (p.354). The receptive field of deep units is larger (Fig. 9.4). Sharing can be dropped when the task is position-specific (centered faces, p.354).
- `[from source]` (DLB p.355) Efficiency example (Fig. 9.6): 320×280 image, 2-element kernel (difference with the neighboring pixel), 319×280 output; convolution: 319×280×3 = **267,960** operations (two multiplications and one addition per output pixel); the equivalent matrix would have 320×280×319×280, **more than 8 billion** entries (convolution ≈ 4 billion times more efficient in representation and ≈ 60,000 times in computation); only the nonzero elements (2×319×280 = 178,640) would match the cost. Reproduce with `dlb_calc.py conv-cost`.

## Pooling
- `[from source]` (DLB p.354-357) Typical layer: convolution (affine transformation), detector stage (ReLU) and pooling (Fig. 9.7: the book's "complex layer" terminology × "simple"). Pooling (max, average, L² norm, weighted average) makes the representation **approximately invariant** to small translations; it is equivalent to an infinitely strong *prior* of invariance; with *stride* k there are k times fewer pooling units; for variable-size inputs, the pooling regions can scale with the input so that the classifier always receives the same number of statistics (p.357).
- `[from source]` (DLB p.362) Convolution and pooling as an infinitely strong *prior*: they can cause **underfitting** when the task requires precise spatial information; only compare CNNs with CNNs on *benchmarks* (there are separate *benchmarks* for models invariant to pixel permutation).

## Variants
- `[from source]` (DLB p.362-364) In practice: many convolutions in parallel; 3-D tensors (channel, row, column) or 4-D (with the batch); 4-D kernel K_{i,j,k,l}; Zᵢ,ⱼ,ₖ = Σ V_{l,j+m−1,k+n−1}K_{i,l,m,n} (eq. 9.7); *stride* s: sample every s positions (eq. 9.8, equivalent to a stride-1 convolution followed by *downsampling*, Fig. 9.12).
- `[from source]` (DLB p.364-366) **Zero padding**: *valid* (no padding; output width m − k + 1), *same* (output the size of the input) and *full* (m + k − 1); without padding the representation shrinks by k − 1 per layer (Fig. 9.13: kernel of width 6 and input of 16 pixels allows only 3 layers); the optimum usually lies between *valid* and *same*. `[inference]` With stride the width is ⌈base/s⌉, a consequence of the sampling definition (eq. 9.8); `dlb_calc.py conv-out` applies this and flags the origin.
- `[from source]` (DLB p.367-371) *Locally connected* (convolution without sharing; 6-D tensor, eq. 9.9), channels connected in groups (Fig. 9.15) and **tiled convolution** (t kernels in rotation; with t = 1 it becomes standard convolution, eq. 9.10).
- `[from source]` (DLB p.371-373) The gradient with respect to the kernel and the input uses the **transposed convolution**, also needed in convolutional autoencoders and RBMs; one bias per output channel, shared across all positions (unless the input has a fixed size).
- `[from source]` (DLB p.373-375) Structured outputs (per-pixel label; Fig. 9.17 with recurrent refinement).
- `[from source]` (DLB p.375-377) Data types (Table 9.1: audio, skeleton, spectrogram, image, volumetric, video); **variable-size** inputs processable only by convolution, but only when the variation is "more observations of the same kind" (the example of applications, with grades and tests, makes no sense); Fourier and **separable** kernels (O(w·d) instead of O(wᵈ)).
- `[from source]` (DLB p.386-387) History: check reading at AT&T (LeCun 1998b), with an NEC system reading more than 10% of US checks in the late 1990s `[DATED]`; Krizhevsky 2012's ImageNet win; CNNs were among the first deep networks to work well and "carried the torch".

## Useful computations (script)
`dlb_calc.py conv-out`, `conv-cost`, `params --kind conv|dense|sparse|mlp`. `[extrapolation]` Receptive field formulas, *dilation*, depthwise convolutions and architectures later than 2016 (VGG, ResNet, EfficientNet etc.) are **not** in this package.

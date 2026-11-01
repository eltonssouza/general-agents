# INDEX — page map, reading coverage and triggers

Closed collection (2 sources). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Sources and page convention

- **UDL** = Simon J.D. Prince, *Understanding Deep Learning*, MIT Press, 2023. PDF of **541 pages**, version with the date "February 15, 2024" on the cover (UDL p.1). Native text (per-page extraction). CC-BY-NC-ND license (footer).
- **NNDL** = Michael Nielsen, *Neural Networks and Deep Learning*, online book (Determination Press, 2015; "Last update: Dec 26 2019", NNDL p.2). PDF of **303 pages** (web print: no printed numbering; equations become images and are lost in text extraction; figures too).
- **Single convention: PDF page** (marker `=== PAGE N ===` of the extracted text). **UDL: printed page = PDF − 14** (e.g., chapter 12 starts on printed 207 = PDF 221; matches the page numbers in the footer). **NNDL: there is no printed page**; always cite the PDF page.
- Citations in the format `UDL p.N` and `NNDL p.N` (ranges `p.N-M`). `python -I scripts/dl_lookup.py --printed N` converts the UDL printed page.
- Equations: where formulas were used in scripts/claims, they were checked against the extracted text (UDL) and, for NNDL, by rendering the pages (PNG) — p.6, 66-68, 116, 129, 176, 179, 200, 203 of NNDL; p.418 of UDL (caption of fig. 20.2). The other NNDL equations were read from the textual context.

## 2. Chapter map and reading coverage

### UDL (PDF)
| Ch. | Topic | PDF | Reading | Reference file |
|---|---|---|---|---|
| 1 | Introduction and ethics (1.4) | 15-30 | in full | 01, 14 |
| 2 | Supervised learning | 31-38 | in full | 01 |
| 3 | Shallow networks | 39-54 | in full (problems skimmed) | 01 |
| 4 | Deep networks | 55-69 | in full | 02 |
| 5 | Loss functions | 70-90 | in full (problems 5.1-5.3) | 03 |
| 6 | Fitting (GD, SGD, Adam) | 91-109 | in full (problems skimmed) | 04 |
| 7 | Gradients and initialization | 110-131 | in full | 04, 05 |
| 8 | Measuring performance | 132-151 | in full | 06 |
| 9 | Regularization | 152-174 | body in full; notes read to the middle of p.173; **p.174 (rest of the notes and problems) NOT read** | 06 |
| 10 | CNN | 175-199 | body and notes through p.196; **p.197-199 NOT read** | 07 |
| 11 | Residuals | 200-220 | in full (problems not read) | 07 |
| 12 | Transformers | 221-253 | in full through p.252; **p.253 not read** | 08 |
| 13 | GNN | 254-281 | body and notes through p.277; **p.278-281 NOT read** | 09 |
| 14 | Unsupervised | 282-288 | in full | 10 |
| 15 | GANs | 289-316 | in full through p.314; **p.315-316 NOT read** | 10 |
| 16 | Flows | 317-339 | in full | 10 |
| 17 | VAEs | 340-361 | in full | 10 |
| 18 | Diffusion | 362-386 | in full (problems only skimmed) | 11 |
| 19 | RL | 387-414 | in full through p.412; **p.413-414 NOT read** | 12 |
| 20 | Why DL works | 415-433 | in full | 13 |
| 21 | Ethics | 434-449 | in full | 14 |
| App. A | Notation | 450-452 | in full | comparison |
| App. B | Mathematics | 453-461 | **NOT read** | — |
| App. C | Probability | 462-475 | only C.3-C.5 (p.470-475) | 10 |
| — | Bibliography / Index | 476-541 | **NOT read** | — |
Front matter p.1-14 (cover, table of contents p.5-9): only the table of contents was read.

### NNDL (PDF)
| Ch. | Topic | PDF | Reading | File |
|---|---|---|---|---|
| Front | cover, menu | 1-2 | in full | — |
| 1 | Recognizing digits (perceptron, sigmoid, GD, SGD, code) | 3-57 | in full | 01, 04 |
| 2 | Backpropagation | 58-84 | in full | 04 |
| 3 | Improving learning (cross-entropy, softmax, overfitting, L1/L2, dropout, init, hyperparameters, momentum, tanh/ReLU) | 85-186 | in full (code listings partly skimmed) | 03, 05, 06 |
| 4 | Visual proof of universality | 187-218 | in full | 02 |
| 5 | Why deep networks are hard to train | 219-239 | in full | 05 |
| 6 | Deep learning (CNN, MNIST, ImageNet, RNN/DBN, future) | 240-303 | body in full; `network3.py` code (p.268-279) only skimmed; problems p.279-280 sampled | 07 |
The PDF ends with the beginning of the appendix "Is there a simple algorithm for intelligence?" (p.302-303); there is no FAQ.

## 3. Triggers → file
| Question about… | Open |
|---|---|
| perceptron, sigmoid, shallow network, basic gradient, ReLU, activations | `01-supervisionado-e-redes-rasas.md` |
| depth, linear regions, universality | `02-redes-profundas-e-capacidade.md` |
| loss, NLL, cross-entropy, softmax, saturation | `03-funcoes-de-perda-e-cross-entropy.md` |
| SGD, momentum, Adam, backprop (BP1-BP4, eq. 7.24) | `04-otimizacao-e-backpropagation.md` |
| initialization, vanishing/exploding gradient | `05-inicializacao-e-gradientes-instaveis.md` |
| overfitting, bias-variance, double descent, L1/L2, dropout, hyperparameters | `06-desempenho-generalizacao-e-regularizacao.md` |
| CNN, pooling, ResNet, BatchNorm, U-Net, MNIST with CNN | `07-cnn-e-residuais.md` |
| transformers, attention, BERT, GPT-3 | `08-transformers-e-linguagem.md` |
| graphs | `09-grafos-gnn.md` |
| GAN, flows, VAE, generative metrics | `10-modelos-generativos-gan-fluxos-vae.md` |
| diffusion | `11-difusao.md` |
| RL, Q-learning, policy gradient, RLHF | `12-aprendizado-por-reforco.md` |
| why DL works, lottery ticket, grokking | `13-por-que-deep-learning-funciona.md` |
| ethics, bias, alignment, privacy | `14-etica-e-uso-responsavel.md` |
| UDL × NNDL difference, notation | `comparacao-udl-nndl.md` |
| terms | `glossario.md` · procedures | `procedimentos.md` · numbers and errors in the books | `casos-e-antipadroes.md` |
| dated items, limits of the collection | `datado-e-limites.md` |

Scripts: `scripts/dl_lookup.py` (search by topic/page/chapter; `--gaps`; `--datado`), `scripts/dl_calc.py` (calculators), `scripts/dl_nets.py` (mini-networks, attention, universality). All stdlib, no network, deterministic.

## 4. NNDL page → content map (for quick citation)
Perceptron 5-11; sigmoid 12-17; architecture 17-20; cost and GD 25-38; `network.py` code 39-46; results 46-53; deep 53-57; backprop 58-84 (BP1-BP4 on 66-68; algorithm 73; speed 77-78); cross-entropy 86-101; softmax 101-106; overfitting 106-114; L2 114-127; L1/dropout/data 128-139; initialization 139-146; `network2.py` code 145-155; hyperparameters 156-173; momentum/Hessian 173-179; tanh/ReLU 179-183; universality 187-218; instability 219-239; CNN 242-267; `network3.py` code 268-279; ImageNet 281-290; RNN/LSTM/DBN 290-296; future 296-303.

## 5. Convention on "read" vs "sampled"
"In full" = all pages of the body and notes were read in the extracted text (and rendered when an equation was used). "NOT read" = no claims in the package about that page. Chapter problems were read only when cited.

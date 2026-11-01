# 05 - Map of tutorials and resources by topic

**Topic -> resource named by the pages** map. The pages only point (link + sentence); **the content of those resources is not in the sources** (NOT COVERED). Equivalent script: `python -I scripts/tfjs_map.py`.

| Topic / need | Named resource | What the page says | Source |
|---|---|---|---|
| First hands-on contact | Tutorial "Primeiros passos" (Getting started; tfjs-examples/getting-started) | Train a minimal model in the browser and predict | TFJI p.1-3; TFJL p.9 |
| New to ML for the web | Video course "Aprendizado de máquina para desenvolvedores da Web" (Machine learning for web developers; Google Developers; YouTube playlist) | Practical introduction to web ML; use of TF.js in sites and apps | TFJI p.3-4; "Ver série" (View series) banner in all |
| ML without dealing with tensors/optimizers | **ml5.js** library | Built on top of TF.js; concise, accessible API; ML algorithms and models in the browser | TFJI p.4 |
| Install | Setup tutorial | Browser and Node.js | TFJI p.4; -> `03-setup.md` |
| Convert a pre-trained Python model -> TF.js | Conversion tutorials: **Modelo Keras** (Keras model; import_keras) and **GraphDef** (import_saved_model) | "How to convert pre-trained models from Python to TF.js" | TFJI p.4; TFJL p.2-3 |
| Overview of model types and conversion | Guide: "Conversão de Modelo" (Model Conversion) | Overview of model types and conversion details | TFJG p.1 |
| Learn from existing code | **tfjs-examples** repository | Small implementations for various ML tasks | TFJI p.4 |
| Visualize model behavior | **tfjs-vis** (GitHub tensorflow/tfjs, tfjs-vis folder) and MNIST demo | Small library for in-browser visualization, for use with TF.js | TFJI p.4-5 |
| Prepare data | API documentation, "Data" section (js.tensorflow.org/api/latest) | TF.js supports data processing with ML best practices | TFJI p.5 |
| Transfer learning | Tutorial "What is transfer learning" (tutorials/transfer) | Reuse/customize pre-existing models with your data; webcam controller demo | TFJL p.2-5 |
| Ready-made models | Models page (`/js/models`) | Pre-trained models for common use cases | TFJL p.1-2 |
| Demos | Demos page; Performance RNN; Holobooth; webcam controller | See `01-visao-geral.md` | TFJL p.2-5 |
| Concepts: tensors, models, training, save/load, Node.js, differences from tf.keras | Guide sections | See `02-guia-secoes.md` | TFJG p.1 |
| News / use cases | TensorFlow blog (Adobe/Photoshop, content moderation, JAX on the Web) | Only titles and dates | TFJL p.5-7 |
| Community help | GitHub, forum, Stack Overflow (tag tensorflow.js), issues, tfjs-announce, SIG, Dev Library | Named links | TFJL p.7-8 |

## Suggested path [inference from the page order]
1. Banner/video course (if new to ML) -> 2. "Primeiros passos" tutorial (TFJI) -> 3. Setup (TFJS) -> 4. Guide, sections 1-4 (TFJG) -> 5. Conversion/transfer learning/ml5.js/tfjs-vis as needed. The order 1-4 is **inference** (TFJI p.3 recommends the guide after the tutorial; the pages do not declare a single path).

## "Beginner" tutorial (TFJB)
The capture TensorFlowJS-Tutorial-Beginner.pdf is a **404**; there is **no** content map for that source.

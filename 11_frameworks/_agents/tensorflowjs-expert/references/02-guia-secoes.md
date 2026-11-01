# 02 - Guide sections (TFJG)

Source: TFJG (2 pages; "Guia TensorFlow.js" (TensorFlow.js Guide), pt-br; last updated 2022-01-24 UTC, p.2). The capture contains **only the guide's index**: section name, link and a one-sentence description. **The content of the sections is NOT in the sources**: any question about the "how" or "why" of each topic is NOT COVERED (unless TFJS/TFJI exemplify it in code).

The cited guide pages use the prefix `tensorflow.org/js/guide/` + slug (`?hl=pt-br`). (TFJG p.1)

| # | Section (as it appears) | Slug | Description given by the page | Where the sources have an example |
|---|---|---|---|---|
| 1 | Tensores e Operações (Tensors and Operations) | tensors_operations | Introduction to tensors, data, shapes and data types, the building blocks of TF.js | Use of `tf.tensor2d`, `tf.randomNormal` in TFJS p.3-6 and TFJI p.3 (usage only, no explanation) |
| 2 | Plataforma e Ambiente (Platform and Environment) | platform_environment | Overview of TF.js platforms and environments and the pros/cons among them | Setup separates browser and Node.js (TFJS p.1-6) |
| 3 | Modelos e Camadas (Models and Layers) | models_and_layers | How to build a model using the Layers API and the Core API | `tf.sequential` + `tf.layers.dense` (TFJS p.3-6, TFJI p.3) |
| 4 | Treinando Modelos (Training Models) | train_models | Introduction to training: models, optimizers, loss functions, metrics, variables | `compile` with loss/optimizer and `fit` (TFJS, TFJI) |
| 5 | Salvando e Carregando Modelos (Saving and Loading Models) | save_load | How to save and load TF.js models | **None** |
| 6 | Conversão de Modelo (Model Conversion) | conversion | Overview of the model types in the TF.js ecosystem and conversion details | Only the labels "Modelo Keras" (Keras model) and "GraphDef" in TFJI p.4 |
| 7 | Diferenças do Python tf.keras (Differences from Python tf.keras) | layers_for_keras_users | Biggest differences and capabilities between TF.js and Python tf.keras and the JavaScript API conventions | **None** |
| 8 | Usando TensorFlow.js no Node.js (Using TensorFlow.js in Node.js) | nodejs | Pros/cons among the **three bindings** for Node.js and their system requirements | The three packages appear in TFJS p.4-6 |

## Other information on the page
- Points to a video course/series ("Ver série", View series) for those new to ML. (TFJG p.1)
- License: text CC BY 4.0, code samples Apache 2.0 (TFJG p.1-2; same in the other sources).
- The guide is the recommended continuation of the minimal tutorial: "for a more detailed introduction to training models with JavaScript, see the guide" ("para uma introdução mais detalhada aos modelos de treinamento com JavaScript, consulte o guia"). (TFJI p.3)

## How to answer
- "What does the guide cover about X?" -> cite the table row.
- "How do I save a model?" -> the guide has the section **Salvando e Carregando Modelos** (Saving and Loading Models) (TFJG p.1); the procedure is NOT COVERED.
- Differences from tf.keras -> the section exists; the content is NOT COVERED (do not answer from memory; if asked, a labeled [extrapolation]).

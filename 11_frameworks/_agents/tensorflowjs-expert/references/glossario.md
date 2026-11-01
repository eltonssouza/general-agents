# Glossary (terms as they appear in the captures)

| Term | Meaning according to the source | Source |
|---|---|---|
| TensorFlow.js | JavaScript library to train and deploy ML models in the browser and in Node.js | TFJI p.1; TFJL p.1 |
| Script tag | Way of loading TF.js via `<script>` (jsDelivr CDN); exposes a global `tf` | TFJS p.1-2 |
| NPM / Yarn ("Fio" in the translation) | Managers to install `@tensorflow/tfjs*` | TFJS p.3-4 |
| Parcel, webpack, Rollup | Build tools cited for NPM projects | TFJS p.1 |
| tfjs-node | Node.js package with native C++ bindings (TensorFlow C binary) | TFJS p.4 |
| tfjs-node-gpu | Node.js package for NVIDIA GPU with CUDA, Linux only | TFJS p.5 |
| tfjs (Node) | Pure JavaScript; same package as the browser; slower in Node | TFJS p.6 |
| `tf.sequential`, `tf.layers.dense` | Constructors used in the model examples | TFJS p.2-6; TFJI p.3 |
| `compile`, `fit`, `predict` | Calls in the examples: prepare with loss and optimizer; train; predict | TFJI p.3; TFJS |
| `tf.tensor2d`, `tf.randomNormal` | Data creation in the examples | TFJS p.2-4; TFJI p.3 |
| Layers API / Core API | Two ways to build models (names in the guide description) | TFJG p.1 |
| Transfer Learning | Customizing pre-existing models with your own data | TFJL p.2-3 |
| GraphDef / Keras model | Two Python model types with a conversion tutorial | TFJI p.4 |
| ml5.js | Library on top of TF.js with a concise API | TFJI p.4 |
| tfjs-vis | In-browser visualization library for TF.js | TFJI p.4-5 |
| tfjs-examples | Repository of small examples | TFJI p.1, 4 |
| Web ML | Term used for ML on the web (course, series) | TFJI p.3; TFJL |
| SIG | TF.js Special Interest Group | TFJL p.8 |

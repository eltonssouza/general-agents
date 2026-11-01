# 03 - Setup (TFJS)

Source: TFJS (7 pages; "Configurar um projeto TensorFlow.js" (Set up a TensorFlow.js project), pt-br, last updated 2023-11-15 UTC, p.7). Commands and snippets below are **source data**; do not run them as part of the agent. The text gives no versions; the examples use `@latest`.

## Browser (TFJS p.1)
Two recommended ways: (a) **script tag**; (b) **install from NPM** and use a build tool such as Parcel, webpack or Rollup. Guidance: those new to the web or to build tools can try the script tag first; those who bundle/process resources or plan larger apps should consider build tools.

### (a) Script tag (TFJS p.1-3)
- Add to the main HTML: `<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>` (in the capture the line appears cut off; the closing `</script>` is inferred). (p.2)
- With the tag, `tf` is available as a global variable (example comment). (p.2)
- Complete HTML example: `tf.sequential()`, a layer `tf.layers.dense({units: 1, inputShape: [1]})`, `model.compile({loss: 'meanSquaredError', optimizer: 'sgd'})`, synthetic data `xs = tf.tensor2d([1, 2, 3, 4], [4, 1])` and `ys = tf.tensor2d([1, 3, 5, 7], [4, 1])`, `model.fit(xs, ys, {epochs: 10}).then(...)` and `model.predict(tf.tensor2d([5], [1, 1])).print()`. (p.2)
- Steps: (1) save as `index.html`; (2) open by double-clicking in the default browser, **or** serve with `npx http-server` in the same folder (answer `y` if it asks permission to install `http-server`) and open `http://localhost:8080`; (3) open the browser console to see the output; (4) refresh the page to see a new prediction, "very likely different". (p.2-3)

### (b) NPM (TFJS p.3)
- Use the `npm` or `yarn` CLI. Command shown: `npm install @tensorflow/tfjs`. The equivalent command from the "Fio" tab (= Yarn, machine translation) **does not appear** in the text extracted from the capture.
- Code: `import * as tf from '@tensorflow/tfjs';` and the same linear model as in the example above. (p.3)

## Node.js (TFJS p.4-6)
Install one of three options with npm or yarn; the page refers to the Node.js guide (TFJG p.1 section 8) and to the tfjs-node repository for more installation details. (p.4)

| Option | Package | Description on the page | Command shown | Page |
|---|---|---|---|---|
| 1 | `@tensorflow/tfjs-node` | Native C++ bindings; native TensorFlow execution in Node.js, accelerated by the TensorFlow C binary | `npm install @tensorflow/tfjs-node` | 4 |
| 2 | `@tensorflow/tfjs-node-gpu` | **Linux only**, system with a CUDA-capable NVIDIA GPU; improves performance | `npm install @tensorflow/tfjs-node-gpu` | 5 |
| 3 | `@tensorflow/tfjs` | Pure JavaScript; "the same package you would use in the browser"; the **slowest** Node.js option in performance | `npm install @tensorflow/tfjs` | 6 |

- Options 1 and 2: `const tf = require('@tensorflow/tfjs-node');` / `require('@tensorflow/tfjs-node-gpu');` with the comment that `tfjs` is imported **indirectly** by the package. Option 3: `require('@tensorflow/tfjs')`. (p.4-6)
- Example model in all three options: `tf.sequential()`, `dense({units: 100, activation: 'relu', inputShape: [10]})`, `dense({units: 1, activation: 'linear'})`, `compile({optimizer: 'sgd', loss: 'meanSquaredError'})`, data `tf.randomNormal([100, 10])` and `tf.randomNormal([100, 1])`, `fit` with `epochs: 100` and callback `onEpochEnd: (epoch, log) => console.log(...)` that prints the loss. (p.4-6)
- CUDA requirement: the page points to the TensorFlow installation documentation (Linux, NVIDIA requirements); the requirements themselves are not in the capture (NOT COVERED). (p.5)

## TypeScript (TFJS p.6)
In a TypeScript project **with strict null checking enabled**, you "may need" to set `skipLibCheck: true` in `tsconfig.json` to avoid compilation errors. Conditional wording ("may"): treat it as a possibility, not an absolute rule.

## What is NOT in this source
Package and Node.js versions, detailed system requirements, other backends (WebGL, WASM, WebGPU), Parcel/webpack/Rollup configuration, the exact Yarn command, ESM `import` in Node, troubleshooting native binary installation. All NOT COVERED.

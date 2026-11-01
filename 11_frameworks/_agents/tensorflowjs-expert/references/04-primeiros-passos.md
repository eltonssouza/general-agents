# 04 - Getting started: minimal tutorial (TFJI)

Source: TFJI (5 pages; "Primeiros passos com o TensorFlow.js" (Getting started with TensorFlow.js), pt-br, last updated 2023-11-30 UTC, p.5). Commands and code are source data.

## Goal (TFJI p.1)
Show how to get started by training a **minimal model in the browser** and using it for a prediction. Sample code on GitHub: `tfjs-examples/getting-started`.

## Prerequisites (p.1)
Node.js (download link) and **Yarn** (install link).

## Install the example (p.1)
1. Clone or download the `tfjs-examples` repository.
2. `cd tfjs-examples/getting-started`
3. `yarn install`

## Structure (p.2)
- The `package.json` does **not** have TensorFlow.js as a dependency: the example loads it from a **CDN**.
- `index.html`: `<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest">` in the `<head>`, a `<div id="micro-out-div">Training...</div>` and `<script src="./index.js">` at the end of the `<body>`. The first script loads the library; the last loads the ML script.
- For other ways to get the dependency, see the setup tutorial (-> `03-setup.md`).

## Run (p.2)
1. In `tfjs-examples/getting-started`: `yarn watch`.
2. Open `http://127.0.0.1:1234`.
Expected result: a heading and a number such as 38.31612014770508; the exact value varies, but it should be **close to 39**.

## What happens (p.2-3)
`index.js` trains a `tf.sequential` model with x and y values that satisfy **y = 2x - 1** (checked in the image), then predicts y for x = 20 (an unseen value) and updates the DOM. Since 2*20 - 1 = 39, the prediction should be approximately 39.

Code (p.3): a `dense` layer with `units: 1`, `inputShape: [1]`; `compile` with `loss: 'meanSquaredError'`, `optimizer: 'sgd'` (comment: prepare the model for training by specifying loss and optimizer); `xs = tf.tensor2d([-1, 0, 1, 2, 3, 4], [6, 1])` and `ys = tf.tensor2d([-3, -1, 1, 3, 5, 7], [6, 1])`; `await model.fit(xs, ys, {epochs: 250})`; `model.predict(tf.tensor2d([20], [1, 1])).dataSync()` shown via `innerText`.

## Named next steps (p.3-5)
See `05-mapa-de-tutoriais.md`.

## Limits
The explanation of why the result is "close" and not exact (training with 250 epochs, SGD) is **not** on the page; any explanation is [extrapolation]. There are also no details on `yarn watch`/the bundler beyond the command and port 1234.

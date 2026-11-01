# [DATED] and gaps

## Source dates
- TFJG: 2022-01-24 UTC (TFJG p.2). TFJS: 2023-11-15 UTC (p.7). TFJI: 2023-11-30 UTC (p.5). TFJL: undated; posts from 2022-08-19 to 2023-03-30 (p.6). TFJB: 404, undated.
- The capture date is unknown. Everything is [DATED] relative to those dates; the live pages may have changed (versions, packages, links, backends, package names).
- pt-br pages are machine-translated (Cloud Translation): "Fio" = Yarn; terms may be distorted. Check the English original when literalness matters.

## NOT COVERED (not present in the 4 useful sources)
Numbered TF.js or Node.js version; content of the 8 guide sections (tensors, platforms/environments, Layers vs Core API, training, save/load, conversion, differences from tf.keras, Node.js details); backends (WebGL, WASM, WebGPU, CPU) and performance; list of the "official models"; Keras/GraphDef conversion procedure; step-by-step transfer learning; tfjs-vis and data API (links only); Parcel/webpack/Rollup configuration; setup Yarn command; CUDA requirements; troubleshooting; TF.js Lite/React Native and other environments; security/privacy of client-side ML.

For any of these, answer "NOT COVERED in the captures" and, only if the user asks, offer a short, labeled [extrapolation].

## Verifiable list
`python -I scripts/tfjs_lookup.py --gaps`.

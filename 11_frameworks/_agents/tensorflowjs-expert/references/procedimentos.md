# Procedures (only what the captures describe)

## P1 - Run the example with a script tag (TFJS p.2-3)
1. Create `index.html` with the example (CDN script + linear model).
2. Open by double-clicking **or** `npx http-server` in the folder and go to `http://localhost:8080` (answer `y` if it asks to install `http-server`).
3. Open the browser console; see the prediction.
4. Refresh the page: new prediction, probably different.

## P2 - Install via NPM in the browser (TFJS p.1, 3)
Choose a build tool (Parcel, webpack or Rollup); `npm install @tensorflow/tfjs`; `import * as tf from '@tensorflow/tfjs';`. Build tool configuration: NOT COVERED.

## P3 - Choose the Node.js option (TFJS p.4-6)
- NVIDIA GPU with CUDA **and Linux** -> `@tensorflow/tfjs-node-gpu` (p.5).
- General native case -> `@tensorflow/tfjs-node` (p.4).
- No native binary -> `@tensorflow/tfjs`, the slowest (p.6).
The Node.js guide (TFJG section 8) details pros/cons and requirements, but its content is NOT COVERED. The decision rule above is [inference] from the descriptions of the three options.

## P4 - TypeScript (TFJS p.6)
If `strict null check` is on and there are compilation errors, consider `skipLibCheck: true` in `tsconfig.json`.

## P5 - Minimal tutorial (TFJI p.1-2)
Have Node.js and Yarn; clone tfjs-examples; `cd tfjs-examples/getting-started`; `yarn install`; `yarn watch`; open `http://127.0.0.1:1234`; expect a number close to 39.

## P6 - Moving on (TFJI p.3-5)
Guide -> conversion (Keras/GraphDef) -> tfjs-examples -> tfjs-vis -> data API. Details of each: NOT COVERED.

// Use `tfjs`.
const tf = require('@tensorflow/tfjs');
const model = tf.sequential();
model.add(tf.layers.dense({units: 1, inputShape: [1]}));
model.compile({optimizer: 'sgd', loss: 'meanSquaredError'});
model.fit(tf.randomNormal([4, 1]), tf.randomNormal([4, 1]), {epochs: 2});

const tf = require('@tensorflow/tfjs-node');
const model = tf.sequential();
model.add(tf.layers.dense({units: 1, inputShape: [1]}));
model.fit(tf.tensor2d([1],[1,1]), tf.tensor2d([1],[1,1]), {epochs: 1});

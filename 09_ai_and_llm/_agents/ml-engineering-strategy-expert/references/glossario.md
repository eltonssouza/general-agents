# Glossary (MLY terms, paraphrased)

| Term (English, from the book) | In Portuguese | Meaning according to the book | MLY p. |
|---|---|---|---|
| training set | conjunto de treino | where the learning algorithm runs | 15 |
| dev (development) set / hold-out cross validation set | conjunto de desenvolvimento | tune parameters, select features and make other decisions | 15 |
| test set | conjunto de teste | evaluate performance, without deciding on algorithm/parameters | 15 |
| single-number evaluation metric | métrica de número único | a single measure to rank models (e.g. accuracy, F1) | 20 |
| F1 score | F1 | harmonic mean of precision and recall: 2/((1/P)+(1/R)) | 21 (note 4) |
| optimizing metric | métrica otimizante | the only metric to maximize/minimize | 22 |
| satisficing metric | métrica satisfatória | just meet a threshold (e.g. <= 100 ms) | 22 |
| error analysis | análise de erro | examine misclassified dev examples to understand causes and prioritize | 30-31 |
| ceiling | teto | % of errors in a category = maximum eliminable by solving it | 30 |
| mislabeled example | exemplo rotulado errado | incorrect label y from the start | 34 |
| Eyeball dev set | dev "olhado" | part of the dev set you examine manually (Ear dev set for audio) | 36 |
| Blackbox dev set | dev "caixa-preta" | part of the dev set you do not look at; used to evaluate and tune | 36 |
| bias (informal) | viés | error on the training set | 42 |
| variance (informal) | variância | how much worse on dev/test than on train | 42 |
| overfitting / underfitting | sobreajuste / subajuste | low training error with high dev / high training with dev close | 44 |
| optimal error rate / Bayes error rate | taxa de erro ótima / de Bayes | error of an "optimal" classifier; "unavoidable bias" | 46-47 |
| unavoidable bias | viés inevitável | the part of the bias equal to the optimal error | 46 |
| avoidable bias | viés evitável | training error - optimal error | 47 |
| regularization | regularização | L2, L1, dropout: reduces variance and increases bias | 49, 51, 53 |
| early stopping | parada antecipada | stop gradient descent based on dev error; reduces variance | 53 |
| learning curve | curva de aprendizado | dev (and training) error against the number of training examples | 56, 59 |
| desired error rate | erro desejado | target: human, product need or intuition | 56-57 |
| human-level performance | desempenho em nível humano | proxy for the optimal error; best feasible human reference (team) | 66, 68 |
| data mismatch | descasamento de dados | generalizes to the training distribution, but not to that of dev/test | 77 |
| training dev set | training-dev | part of the training data not used for training; same distribution as training | 78 |
| artificial data synthesis | síntese artificial de dados | create data that imitates the dev set (e.g. add car noise) | 82 |
| Optimization Verification test | teste de verificação de otimização | compare Score(y*) with Score(y_out) to blame search or objective | 86-87 |
| scoring function | função de pontuação | Score_x(y) that measures how good an output y is for input x | 85, 87 |
| end-to-end learning | aprendizado end-to-end | a single algorithm from raw input straight to output | 91-92 |
| pipeline | pipeline | chain of components (learned or not) | 91, 93-94 |
| error analysis by parts | análise de erro por partes | attribute each error to a pipeline component | 106 |
| DAG ordering | ordem DAG | components ordered left to right, each depending only on earlier ones | 112 |
| scenario | cenário | self-driving test case (closed track) | 112 |

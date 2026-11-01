# Reference index: aws-lambda-serverless-expert

Single source: **AWS Lambda Developer Guide** (AWS, official product documentation, copyright 2022; last release entry on 11/28/2022), 1297 pages, abbreviation **LAMBDA**.

## Page convention
Citations `(LAMBDA p.N)` use the **PDF page number** (page marker of the extracted text). The **printed** page in the footer = N - 22 (the body starts on p.23 of the PDF = p.1 printed; e.g. Releases is on p.968 of the PDF and p.946 printed). The guide's table of contents uses printed numbers; add 22 to get the PDF page.

## Labels
`[from source]` (present on the cited page), `[inference]`, `[extrapolation]` (outside the collection, no page), `[DATED]` (number/limit/runtime/version/CLI/price that has aged since the 2022 edition). In the reference files, lines without another explicit label come from the book with the cited page. The texts of the thematic references were written without accents (they originate from reading notes); paraphrase, no copying.

## When to open each file
| Trigger | File |
|---|---|
| "what is Lambda", concepts, features, arm64 | fundamentos-conceitos-e-modelo-de-programacao.md |
| lifecycle, cold start, VPC, ENI, EFS, RDS Proxy | ambiente-de-execucao-rede-vpc-efs-e-rds.md |
| IAM, execution role, resource policy, boundaries, security | permissoes-iam-e-seguranca.md |
| runtimes, deprecation, custom runtime, extensions, Telemetry/Logs API | runtimes-custom-runtimes-e-extensions.md |
| .zip, container image, layers, code signing, tags | deploy-container-images-layers-code-signing-e-tags.md |
| memory, timeout, env vars, versions, aliases | configuracao-variaveis-versoes-e-aliases.md |
| reserved/provisioned/burst concurrency | concorrencia-e-escala.md |
| synchronous/asynchronous invocation, DLQ, destinations, ESM (overview), retries, Function URLs | invocacao-erros-retries-e-function-urls.md |
| S3, SNS, API Gateway, EventBridge, ALB, CloudTrail etc. | servicos-integrados-eventos-push.md |
| SQS, Kinesis, DynamoDB Streams, Kafka, MSK, MQ | event-sources-stream-fila-e-kafka.md |
| SnapStart | snapstart.md |
| handler/logging/errors/tracing per language | linguagens-padrao-comum.md, linguagens-diferencas-por-runtime.md |
| metrics, logs, Insights, X-Ray | observabilidade-monitoramento.md |
| operational error/symptom | troubleshooting.md |
| SAM, applications, CodeDeploy, Step Functions | aplicacoes-sam-e-orquestracao.md |
| the guide's best practices | boas-praticas.md |
| limits and quotas | quotas-e-limites-datados.md |
| parameters, enums, API status/errors | api-reference-restricoes-e-parametros.md |
| edition date, release history, samples | samples-releases-e-datacao.md |
| terms | glossario.md |
| step-by-step walkthroughs | procedimentos.md |
| antipatterns, cases, contradictions in the text | casos-e-antipadroes.md |
| "does the book cover X?", dating, boundaries | lacunas-e-fronteiras.md |

## Guide section map (PDF page)
Intro and concepts 23-70 | Permissions 71-101 | Runtimes, extensions, Telemetry/Logs API 102-182 | Deploy, images, layers 183-213 | Configuration, versions, aliases 214-232 | Concurrency 233-262 | VPC, EFS, code signing, tags, layer usage 263-294 | Invocation, ESM, Function URLs 295-352 | SnapStart 353-367 | Languages 368-585 | Other services 586-794 | Monitoring, security, troubleshooting 795-838 | Applications and Step Functions 839-870 | Best practices and quotas 871-877 | SDKs and samples 878-967 | Releases 968-983 | API reference 984-1297.

## Scripts (see `scripts/`)
`lambda_lookup.py` (index lookup, "NOT COVERED" when there is none), `lambda_validate_config.py` (validates config against the limits IN THE TEXT), `lambda_review_checklist.py` (42 review items), data `lambda_index.json` and `lambda_limits.json`. Citation verifier: `tests/verify_citations.py` + `tests/citation-checks.json`.

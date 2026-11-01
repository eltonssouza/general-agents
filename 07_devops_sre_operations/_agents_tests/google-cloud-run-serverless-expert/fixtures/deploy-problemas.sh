# Several deliberate problems
gcloud run deploy worker \
  --image us-docker.pkg.dev/my-proj/cloud-run-book/worker \
  --region europe-west1 \
  --add-cloudsql-instances my-proj:us-central1:sql-db \
  --allow-unauthenticated --no-allow-unauthenticated \
  --concurrency 1000 \
  --timeout 7200 \
  --memory 8Gi \
  --min-instances 2 \
  --no-cpu-throttling \
  --set-secrets=A=b:latest \
  --set-env-vars DB_PASSWORD=hunter2,REDIS=redis://10.0.0.3:6379,DB="mysql://root@unix(/cloudsql/my-proj:us-central1:sql-db)/todo"

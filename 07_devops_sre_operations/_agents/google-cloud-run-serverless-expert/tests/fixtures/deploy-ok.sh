# Example aligned with the book (RUN p.91, 96, 115): service with Cloud SQL, dedicated account and instance ceiling
gcloud run deploy todo \
  --add-cloudsql-instances my-proj:us-central1:sql-db \
  --image us-docker.pkg.dev/my-proj/cloud-run-book/todo \
  --region us-central1 \
  --service-account todo@my-proj.iam.gserviceaccount.com \
  --max-instances 100 \
  --concurrency 80 \
  --timeout 300 \
  --memory 512Mi \
  --no-allow-unauthenticated \
  --set-env-vars DB="mysql://app@unix(/cloudsql/my-proj:us-central1:sql-db)/todo"

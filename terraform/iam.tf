resource "google_service_account" "d0_ingestion" {
  account_id   = "habotconnect-d0-ingestion"
  display_name = "HabotConnect D0 Raw Landing Ingestion"
  description  = "Least-privilege identity for writing raw onboarding data to D0."
}

resource "google_storage_bucket_iam_member" "d0_ingestion_object_creator" {
  bucket = google_storage_bucket.d0_raw_landing.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.d0_ingestion.email}"

  condition {
    title       = "Allow raw landing prefix only"
    description = "Permit the ingestion identity to create objects only under the raw/ prefix."
    expression  = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.d0_raw_landing.name}/objects/raw/')"
  }
}

resource "google_service_account" "d1_analytics" {
  account_id   = "habotconnect-d1-analytics"
  display_name = "HabotConnect D1 Analytics"
  description  = "Restricted identity for querying analytics-scoped D1 records."
}

resource "google_bigquery_dataset_iam_member" "d1_analytics_viewer" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  role       = "roles/bigquery.dataViewer"
  member     = "serviceAccount:${google_service_account.d1_analytics.email}"
}
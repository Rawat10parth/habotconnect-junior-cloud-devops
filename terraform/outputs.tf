output "d0_raw_landing_bucket" {
  description = "Name of the D0 raw landing bucket."
  value       = google_storage_bucket.d0_raw_landing.name
}

output "d0_ingestion_service_account" {
  description = "Service account used for D0 ingestion."
  value       = google_service_account.d0_ingestion.email
}

output "d1_dataset" {
  description = "Name of the D1 staged and enforced BigQuery dataset."
  value       = google_bigquery_dataset.d1_staged_enforced.dataset_id
}

output "d1_analytics_service_account" {
  description = "Restricted analytics service account."
  value       = google_service_account.d1_analytics.email
}
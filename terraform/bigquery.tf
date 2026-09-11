resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id = "d1_staged_enforced"
  location   = var.region

  description = "D1 staged and enforced data layer for the HabotConnect assessment."

  labels = {
    environment = "staging"
    layer       = "d1-staged-enforced"
    managed_by  = "terraform"
  }

}

resource "google_bigquery_table" "student_onboarding_staged" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = "student_onboarding_staged"

  description = "Staged onboarding records. The final business schema will be aligned to the supplied onboarding JSON."

  deletion_protection = false

  schema = jsonencode([
    {
      name        = "access_scope"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Security classification used by the row-level security policy."
    },
    {
      name        = "payload"
      type        = "JSON"
      mode        = "NULLABLE"
      description = "Validated onboarding payload."
    }
  ])
}

resource "google_bigquery_row_access_policy" "d1_analytics_filtered" {
  dataset_id       = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id         = google_bigquery_table.student_onboarding_staged.table_id
  policy_id        = "analytics-scope-only"
  filter_predicate = "access_scope = 'ANALYTICS'"
  grantees         = ["serviceAccount:${google_service_account.d1_analytics.email}"]
}
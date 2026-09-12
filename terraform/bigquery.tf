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

  description = "Validated student onboarding records in the D1 staged and enforced layer."

  deletion_protection = false

  schema = jsonencode([
    {
      name        = "access_scope"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Security classification used by the row-level security policy."
    },
    {
      name        = "student_name"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Validated student name."
    },
    {
      name        = "email"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Validated student email address."
    },
    {
      name        = "phone"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Validated 10-digit phone number."
    },
    {
      name        = "age"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "Validated student age."
    },
    {
      name        = "has_passport"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN passport decision."
    },
    {
      name        = "has_academic_documents"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN academic-document decision."
    },
    {
      name        = "english_proficiency"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN English-proficiency decision."
    },
    {
      name        = "willing_to_relocate"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN relocation decision."
    },
    {
      name        = "has_relevant_experience"
      type        = "BOOLEAN"
      mode        = "REQUIRED"
      description = "DCYN relevant-experience decision."
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
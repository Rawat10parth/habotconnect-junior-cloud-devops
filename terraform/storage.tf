resource "google_storage_bucket" "d0_raw_landing" {
  name          = "${var.project_id}-d0-raw-landing"
  location      = var.region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = true
  }

  labels = {
    environment = "staging"
    layer       = "d0-raw-landing"
    managed_by  = "terraform"
  }
}
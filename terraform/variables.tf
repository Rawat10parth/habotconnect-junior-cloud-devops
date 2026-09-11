variable "project_id" {
  description = "Google Cloud project ID used for the HabotConnect assessment."
  type        = string

  default = "habotconnect-devops-assessment"
}

variable "region" {
  description = "Google Cloud region used by regional resources."
  type        = string

  default = "asia-south1"
}
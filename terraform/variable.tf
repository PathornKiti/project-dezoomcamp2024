variable "project" {
  description = "Project"
  default     = "datacafeplayground"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "asia-southeast1-a"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "ASIA-SOUTHEAST1"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default = "airbnb-bkk-datalake"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "credentials" {
  description = "My Credentials"
  default     = "datacafeplayground-6cf623fc6e32.json"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "airbnb_bkk_warehouse"
}
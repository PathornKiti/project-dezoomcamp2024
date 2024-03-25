variable "project" {
  description = "Project"
  default     = "project_name"
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
  default     = "google_credentials.json"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "airbnb_bkk_warehouse"
}

variable "dataproc_master_machine_type" {
  type        = string
  description = "dataproc master node machine tyoe"
  default     = "n1-standard-2"
}

variable "dataproc_worker_machine_type" {
  type        = string
  description = "dataproc worker nodes machine type"
  default     = "n1-standard-2"
}

variable "dataproc_workers_count" {
  type        = number
  description = "count of worker nodes in cluster"
  default     = 1
}
variable "dataproc_master_bootdisk" {
  type        = number
  description = "primary disk attached to master node, specified in GB"
  default     = 500
}

variable "dataproc_worker_bootdisk" {
  type        = number
  description = "primary disk attached to master node, specified in GB"
  default     = 500
}

variable "worker_local_ssd" {
  type        = number
  description = "primary disk attached to master node, specified in GB"
  default     = 0
}

variable "preemptible_worker" {
  type        = number
  description = "number of preemptible nodes to create"
  default     = 1
}
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

variable "cluster_name" {
    description = "The name of the cluster, unique within the project and zoneData"
}

variable "labels" {
    description = "The list of labels (key/value pairs) to be applied to instances in the cluster"
    default     = {}
}

variable "delete_autogen_bucket" {
    description = "If this is set to true, upon destroying the cluster, if no explicit staging_bucket was specified (i.e. an auto generated bucket was relied upon) then this auto generated bucket will also be deleted as part of the cluster destroy"
    default     = "false"
}

variable "staging_bucket" {
    description = "The Cloud Storage staging bucket used to stage files, such as Hadoop jars, between client machines and the cluster"
    default =   ""
}

variable "master_num_instances" {
    description = "Specifies the number of master nodes to create"
    default     = 1
}

variable "master_machine_type" {
    description = "The name of a Google Compute Engine machine type to create for the master"
    default     = "n1-standard-4"
}

variable "master_boot_disk_size_gb" {
    description = "Size of the primary disk attached to each node, specified in GB"
    default     = 10
}

variable "worker_num_instances" {
    description = "Specifies the number of worker nodes to create"
    default     = 2
}

variable "worker_machine_type" {
    description = "The name of a Google Compute Engine machine type to create for the worker nodes"
    default     = "n1-standard-4"
}

variable "worker_boot_disk_size_gb" {
    description = "Size of the primary disk attached to each worker node, specified in GB"
    default     = 10
}

variable "worker_num_local_ssds" {
    description = "The amount of local SSD disks that will be attached to each worker cluster node"
    default     = 0
}

variable "preemptible_num_instances" {
    description = "Specifies the number of preemptible nodes to create"
    default     = 0
}

variable "image_version" {
    description = "The Cloud Dataproc image version to use for the clustere"
    default     = "1.2"
}
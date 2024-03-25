terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
  credentials = file(var.credentials)
}


resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

resource "google_dataproc_cluster" "demo_cluster" {
    name    = "${var.cluster_name}"
    project = "${var.project}"
    region  = "${var.region}"

    labels  = "${var.labels}"

    cluster_config {
        delete_autogen_bucket = "${var.delete_autogen_bucket}"

        staging_bucket        = "${var.staging_bucket}"

        master_config {
            num_instances     = "${var.master_num_instances}"
            machine_type      = "${var.master_machine_type}"
            disk_config {
                boot_disk_size_gb = "${var.master_boot_disk_size_gb}"
            }
        }

        worker_config {
            num_instances     = "${var.worker_num_instances}"
            machine_type      = "${var.worker_machine_type}"
            disk_config {
                boot_disk_size_gb = "${var.worker_boot_disk_size_gb}"
                num_local_ssds    = "${var.worker_num_local_ssds}"
            }
        }

        preemptible_worker_config {
            num_instances     = "${var.preemptible_num_instances}"
        }


        software_config {
            image_version       = "${var.image_version}"
            override_properties = {

            }
        }

        gce_cluster_config {
            zone    = "${data.google_compute_zones.available.names[0]}"

        }

    }
}
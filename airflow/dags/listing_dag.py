import os
import pandas as pd

from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

from utils import extract,upload_to_gcs

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
DATASET=os.environ.get("DATASET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

def get_parquet(path):
    df_listing=extract("2023-12-25","listings")
    filter_columns=['id', 'listing_url', 'name','picture_url', 'host_id'
       , 'host_name', 'host_since', 'host_location', 'host_about',
       'host_response_time', 'host_response_rate', 'host_acceptance_rate',
       'host_is_superhost',
       'host_identity_verified',
       'neighbourhood_cleansed', 'latitude',
       'longitude', 'property_type', 'room_type', 'accommodates',
       'price',
       'minimum_nights', 'maximum_nights', 'number_of_reviews',
       'review_scores_value', 'instant_bookable',
       'reviews_per_month']
    df_listing=df_listing[filter_columns]
    df_listing.rename(columns={'id': 'listing_id'}, inplace=True)
    df_listing['price'] = df_listing['price'].str.replace('[^\d.]', '', regex=True).astype(float)
    directory = os.path.join(path, 'listing') 
    if not os.path.exists(directory):
        os.makedirs(directory)
    df_listing.to_parquet(os.path.join(directory, 'listing.parquet'))

default_args = {
    "owner": "Pathorn",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="listing",
    schedule_interval='@yearly',
    default_args=default_args,
    catchup=True,
    max_active_runs=2,
    tags=['dtc-de'],
    start_date=datetime.now(),
    concurrency=3
) as dag:
    
    start_task = DummyOperator(task_id='start_task', dag=dag)

    extract_listings_parquet = PythonOperator(
        task_id=f'extract_listings_parquet',
        python_callable=get_parquet,
        op_kwargs={
            "path": path_to_local_home,
        },
    )

    local_to_gcs = PythonOperator(
        task_id=f"local_to_gcs",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"listing/listing.parquet",
            "local_file": f"{path_to_local_home}/listing/listing.parquet",
        },
    )

    create_external_table = BigQueryCreateExternalTableOperator(
        task_id="create_external_table",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": DATASET,
                "tableId": "external_listing",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/listing/listing.parquet"],
            },
        },
    )

    remove_data = BashOperator(
        task_id="remove_data",
        bash_command=f"rm {path_to_local_home}/listing/listing.parquet"
    )

    start_task >> extract_listings_parquet >>local_to_gcs >>create_external_table >> remove_data

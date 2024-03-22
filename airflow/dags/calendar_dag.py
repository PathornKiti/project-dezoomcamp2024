import os
import pandas as pd

from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.models import Variable

from utils import extract,upload_to_gcs

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
DATASET=os.environ.get("DATASET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

def get_parquet(path):
    df_cal=extract("2023-12-25","calendar")
    df_cal['date'] = pd.to_datetime(df_cal['date'])
    directory = os.path.join(path, 'available') 
    if not os.path.exists(directory):
        os.makedirs(directory)
    df_cal.to_parquet(os.path.join(directory, 'available.parquet'), coerce_timestamps="us")
    
default_args = {
    "owner": "Pathorn",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="calendar",
    schedule_interval='@yearly',
    default_args=default_args,
    catchup=True,
    max_active_runs=2,
    tags=['dtc-de'],
    start_date=datetime.now(),
    concurrency=3
) as dag:
    
    start_task = DummyOperator(task_id='start_task', dag=dag)

    extract_avaiable_parquet = PythonOperator(
        task_id=f'extract_avaiable_parquet',
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
            "object_name": f"available/available.parquet",
            "local_file": f"{path_to_local_home}/available/available.parquet",
        },
    )

    create_external_table = BigQueryCreateExternalTableOperator(
        task_id="create_external_table",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": DATASET,
                "tableId": "external_calendar",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/available/available.parquet"],
            },
        },
    )

    remove_data = BashOperator(
        task_id="remove_data",
        bash_command=f"rm {path_to_local_home}/available/available.parquet"
    )

    start_task >> extract_avaiable_parquet  >>local_to_gcs >>create_external_table >> remove_data
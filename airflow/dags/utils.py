import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import requests
from google.cloud import storage

def extract(date,data):
  init_url="http://data.insideairbnb.com/thailand/central-thailand/bangkok/"
  suffix = f"{date}/data/{data}.csv.gz"
  request_url = f"{init_url}{suffix}"
  file_name=f"{data}.csv.gz"
  response = requests.get(request_url)
  open(file_name, 'wb').write(response.content)
  print(f"Local: {file_name}")
  df = pd.read_csv(file_name, compression='gzip')
  return df

def upload_to_gcs(bucket, object_name, local_file):
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  
    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)



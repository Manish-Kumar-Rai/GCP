from google.cloud import bigquery

PROJECT_ID = "gcp-learning-494920"
GCS_NAME = "manish-gcp-learning"
# GCS_URI = f"gs://{GCS_NAME}/chapter3/datasets/trips/20180101/*.json"
GCS_URI = f"gs://{GCS_NAME}/chapter3/datasets/trips/20180102/*.json"

client = bigquery.Client()

TABLE_ID = f"{PROJECT_ID}.raw_bikesharing.trips"

def load_gcs_to_bigquery_event_data(GCS_URI,TABLE_ID,table_schema):
    job_config = bigquery.LoadJobConfig(
        schema=table_schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition= "WRITE_APPEND"
    )

    load_job = client.load_table_from_uri(
        GCS_URI,TABLE_ID,job_config=job_config
    )

    load_job.result()
    table = client.get_table(TABLE_ID)

    print(f"Loaded {table.num_rows} rows to table {TABLE_ID}.")

bigquery_table_schema = [
    bigquery.SchemaField("trip_id","STRING"),
    bigquery.SchemaField("duration_sec", "INTEGER"),
    bigquery.SchemaField("start_date", "TIMESTAMP"),
    bigquery.SchemaField("start_station_name", "STRING"),
    bigquery.SchemaField("start_station_id", "STRING"),
    bigquery.SchemaField("end_date", "TIMESTAMP"),
    bigquery.SchemaField("end_station_name", "STRING"),
    bigquery.SchemaField("end_station_id", "STRING"),
    bigquery.SchemaField("member_gender", "STRING")
]

if __name__ == "__main__":
    load_gcs_to_bigquery_event_data(GCS_URI,TABLE_ID,bigquery_table_schema)
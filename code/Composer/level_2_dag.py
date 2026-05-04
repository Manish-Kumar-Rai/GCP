import datetime
import pendulum
from airflow import DAG

from airflow.providers.google.cloud.operators.cloud_sql import CloudSQLExportInstanceOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

args = {
    "owner": "manish",
    "start_date": pendulum.datetime(2026,5,3,tz="UTC"),
    "retries":1,
    "retry_delay": datetime.timedelta(minutes=3)
}

GCP_PROJECT_ID="gcp-learning-494920"
INSTANCE_NAME="gcp-mysql-source"

EXPORT_URI="gs://manish-gcp-learning/chapter4/mysql_export/from_composer/stations/stations.csv"

SQL_QUERY="SELECT * FROM apps_db.stations;"

export_body = {
    "exportContext": {
        "fileType": "csv",
        "uri": EXPORT_URI,
        "csvExportOptions": {
            "selectQuery": SQL_QUERY
        }
    }
}

with DAG(
    dag_id="level_2_dag_load_bigquery",
    default_args=args,
    schedule="@daily",
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=15)
) as dag:

    sql_export_task = CloudSQLExportInstanceOperator(
        task_id="sql_export_task",
        project_id=GCP_PROJECT_ID,
        instance=INSTANCE_NAME,
        body=export_body
    )

    gcs_to_bq_task = GCSToBigQueryOperator(
        task_id="gcs_to_bq_task",
        bucket="manish-gcp-learning",
        source_objects=[
            "chapter4/mysql_export/from_composer/stations/stations.csv"
        ],
        schema_fields=[
        {'name': 'station_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'region_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'capacity', 'type': 'INTEGER', 'mode': 'NULLABLE'}
        ],
        destination_project_dataset_table=
        f"{GCP_PROJECT_ID}.composer_raw_bikesharing.stations",
        write_disposition="WRITE_TRUNCATE"
    )

    bq_to_bq_task = BigQueryInsertJobOperator(
        task_id="bq_to_bq_task",
        configuration={
            "query": {
                "query": """
                    SELECT COUNT(*)
                    FROM `{project_id}.composer_raw_bikesharing.stations`
                """.format(project_id=GCP_PROJECT_ID),
                "useLegacySql": False,
                "destinationTable": {
                    "projectId": GCP_PROJECT_ID,
                    "datasetId": "composer_raw_bikesharing",
                    "tableId": "temporary_stations_count"
                },
                "writeDisposition": "WRITE_TRUNCATE"
            }
        }
    )

    sql_export_task >> gcs_to_bq_task >> bq_to_bq_task
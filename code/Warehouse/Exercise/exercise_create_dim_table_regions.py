from google.cloud import bigquery

PROJECT_ID = "gcp-learning-494920"
TARGET_TABLE_ID = f"{PROJECT_ID}.dwh_bikesharing.dim_exercise_regions"

def create_dim_table(PROJECT_ID,TARGET_TABLE_ID):
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(
        destination=TARGET_TABLE_ID,
        write_disposition="WRITE_TRUNCATE"
    )

    sql = """SELECT CAST(region_id AS STRING) AS region_id,name
            FROM `{PROJECT_ID}.raw_bikesharing.regions`;
    """.format(PROJECT_ID=PROJECT_ID)

    query_job = client.query(sql,job_config=job_config)

    try:
        query_job.result()
        print("Query Success.")
    except Exception as e:
        print(e)
    finally:
        table = client.get_table(TARGET_TABLE_ID)
        print(f"Total rows: {table.num_rows}")

if __name__ == "__main__":
    create_dim_table(PROJECT_ID,TARGET_TABLE_ID)

import sys
from google.cloud import bigquery

PROJECT_ID = "gcp-learning-494920"
TARGET_TABLE_ID = f"{PROJECT_ID}.dwh_bikesharing.fact_region_gender_daily_exercise"

def create_fact_table(PROJECT_ID,TARGET_TABLE_ID):
    load_date = sys.argv[1]  # date format: yyyy-mm-dd
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(
        destination=TARGET_TABLE_ID,
        write_disposition="WRITE_APPEND"
    )

    sql="""SELECT DATE(t.start_date) AS trip_date,s.region_id,r.name,t.member_gender,
           COUNT(t.trip_id) AS total_trips
           FROM `{PROJECT_ID}.raw_bikesharing.trips` t
           JOIN `{PROJECT_ID}.raw_bikesharing.stations` s
           ON s.station_id = t.start_station_id
           JOIN `{PROJECT_ID}.raw_bikesharing.regions` r
           ON s.region_id = CAST(r.region_id AS STRING)
           WHERE DATE(t.start_date) = DATE('{load_date}') AND t.member_gender IS NOT NULL
           GROUP BY trip_date,s.region_id,r.name,t.member_gender
    """.format(PROJECT_ID=PROJECT_ID,load_date=load_date)

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
    create_fact_table(PROJECT_ID,TARGET_TABLE_ID)
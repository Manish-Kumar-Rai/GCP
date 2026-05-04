import datetime
import pendulum
from airflow import DAG

try:
    from airflow.providers.standard.operators.bash import BashOperator
except ImportError:
    from airflow.operators.bash_operator import BashOperator

args = {
    "owner": "manish",
    "start_date": pendulum.datetime(2026,5,3,tz="UTC"),
    "retries" : 1,
    "retry_delay": datetime.timedelta(minutes=3)
}

with DAG(
    dag_id="hello_world",
    description="my level 1 dag",
    default_args=args,
    schedule="*/3 * * * *",
    dagrun_timeout=datetime.timedelta(minutes=5),
    catchup=False,
    max_active_runs=2
) as dag:

    task1 = BashOperator(
        # dag=dag,  # using context manager. It is already asssign.
        task_id="print_hello",
        bash_command="echo hello",
        # depends_on_past=False,  # default 
        do_xcom_push=False
    )

    task2 = BashOperator(
        task_id="print_world",
        # dag=dag,
        bash_command="echo world",
        # depends_on_past=False,
        do_xcom_push=False
    )

    task1 >> task2


# use below code local debugging or cli testing:
# if __name__ == "__main__":
#     dag.cli()
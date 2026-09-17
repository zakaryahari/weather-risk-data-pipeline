from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id = "Weather_dag",
    start_date = datetime(2023 , 1 ,1),
    schedule = '@daily',
    catchup = False
) as dag :

    extract_task = BashOperator(
        task_id = "extract_task",
        bash_command = "python3 /opt/airflow/scripts/extract.py"
    )

    transform_task = BashOperator(
        task_id = "transform_task",
        bash_command = "python3 /opt/airflow/scripts/transform.py"
    )

    load_task = BashOperator(
        task_id = "load_task",
        bash_command = "python3 /opt/airflow/scripts/load.py"
    )


    extract_task >> transform_task >> load_task
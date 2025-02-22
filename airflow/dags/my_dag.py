# Filename: spark_submit_dag.py

from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash_operator import BashOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 28),  # Replace with your preferred start date
}

# Define the DAG
dag = DAG(
    dag_id='my_dag',
    default_args=default_args,
    description='Submit a PySpark job using SparkSubmitOperator',
    schedule_interval=None,
    catchup=False,
)



# Define the BashOperator
bash_task = BashOperator(
    task_id='echo_hello_world',
    bash_command='echo "Hello, World!"',
    dag=dag,
)

# Define the SparkSubmitOperator
ingest_permits_task = SparkSubmitOperator(
    task_id='ingest_permits',
    application='/root/airflow/jobs/ingest_permits.py',
    conn_id='spark_default',  
    verbose=True,
    dag=dag,
)

count_permits_task = SparkSubmitOperator(
    task_id='count_permits',
    application='/root/airflow/jobs/count_permits.py',
    conn_id='spark_default',  
    verbose=True,
    dag=dag,
)


# Set the task in the DAG
bash_task >> ingest_permits_task >> count_permits_task
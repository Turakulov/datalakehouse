# Filename: spark_submit_dag.py

from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 9, 28),  # Replace with your preferred start date
}

# Define the DAG
dag = DAG(
    dag_id="aaa_spark",
    default_args=default_args,
    description="Submit a PySpark job using SparkSubmitOperator",
    schedule_interval=None,
    catchup=False,
)


# Define the SparkSubmitOperator
ingest_permits_task = SparkSubmitOperator(
    task_id="ingest_permits",
    application="/root/airflow/jobs/iceberg/employees_insert_iceberg.py",
    conn_id="spark_default",
    verbose=True,
    dag=dag,
)

ingest_permits_task
